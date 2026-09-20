"""CORE check: execute a pinned OSV scan and reject every vulnerability.

The consumer owns the exact scanner version and lockfile list.  This check
owns verdict semantics: only a completed, parseable, clean scan can pass.
Missing tooling, a version mismatch, an absent lockfile, an execution error,
or malformed output is incomplete evidence and therefore cannot become green.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any

from tc_fitness.check_evidence import report_finding
from tc_fitness.lib import REPO_ROOT

DEFAULT_TIMEOUT = 180


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


class ScanStatus(StrEnum):
    """Terminal evidence states for one scanner invocation."""

    EXECUTED = "executed"
    MISSING_TOOL = "missing-tool"
    INCOMPLETE = "incomplete"


@dataclass(frozen=True)
class ScanExecution:
    """Scanner evidence kept separate from the vulnerability verdict."""

    status: ScanStatus
    report: dict[str, Any] | None = None
    detail: str = ""


Runner = Callable[[Path, tuple[str, ...], str], ScanExecution]
mutants_x__reported_version__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__reported_version__mutmut)
def _reported_version(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"version probe failed: {exc}")
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(r"\b(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+|\+[0-9A-Za-z.-]+)?)\b", output)
    if process.returncode != 0 or match is None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"version probe returned {process.returncode}: {output[:240]}",
        )
    return match.group(1)


def x__reported_version__mutmut_orig(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"version probe failed: {exc}")
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(r"\b(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+|\+[0-9A-Za-z.-]+)?)\b", output)
    if process.returncode != 0 or match is None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"version probe returned {process.returncode}: {output[:240]}",
        )
    return match.group(1)


def x__reported_version__mutmut_1(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = None
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"version probe failed: {exc}")
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(r"\b(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+|\+[0-9A-Za-z.-]+)?)\b", output)
    if process.returncode != 0 or match is None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"version probe returned {process.returncode}: {output[:240]}",
        )
    return match.group(1)


def x__reported_version__mutmut_2(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            None,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"version probe failed: {exc}")
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(r"\b(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+|\+[0-9A-Za-z.-]+)?)\b", output)
    if process.returncode != 0 or match is None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"version probe returned {process.returncode}: {output[:240]}",
        )
    return match.group(1)


def x__reported_version__mutmut_3(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            [binary, "--version"],
            capture_output=None,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"version probe failed: {exc}")
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(r"\b(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+|\+[0-9A-Za-z.-]+)?)\b", output)
    if process.returncode != 0 or match is None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"version probe returned {process.returncode}: {output[:240]}",
        )
    return match.group(1)


def x__reported_version__mutmut_4(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            text=None,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"version probe failed: {exc}")
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(r"\b(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+|\+[0-9A-Za-z.-]+)?)\b", output)
    if process.returncode != 0 or match is None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"version probe returned {process.returncode}: {output[:240]}",
        )
    return match.group(1)


def x__reported_version__mutmut_5(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            text=True,
            check=None,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"version probe failed: {exc}")
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(r"\b(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+|\+[0-9A-Za-z.-]+)?)\b", output)
    if process.returncode != 0 or match is None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"version probe returned {process.returncode}: {output[:240]}",
        )
    return match.group(1)


def x__reported_version__mutmut_6(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            text=True,
            check=False,
            timeout=None,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"version probe failed: {exc}")
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(r"\b(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+|\+[0-9A-Za-z.-]+)?)\b", output)
    if process.returncode != 0 or match is None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"version probe returned {process.returncode}: {output[:240]}",
        )
    return match.group(1)


def x__reported_version__mutmut_7(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"version probe failed: {exc}")
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(r"\b(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+|\+[0-9A-Za-z.-]+)?)\b", output)
    if process.returncode != 0 or match is None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"version probe returned {process.returncode}: {output[:240]}",
        )
    return match.group(1)


def x__reported_version__mutmut_8(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            [binary, "--version"],
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"version probe failed: {exc}")
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(r"\b(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+|\+[0-9A-Za-z.-]+)?)\b", output)
    if process.returncode != 0 or match is None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"version probe returned {process.returncode}: {output[:240]}",
        )
    return match.group(1)


def x__reported_version__mutmut_9(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"version probe failed: {exc}")
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(r"\b(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+|\+[0-9A-Za-z.-]+)?)\b", output)
    if process.returncode != 0 or match is None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"version probe returned {process.returncode}: {output[:240]}",
        )
    return match.group(1)


def x__reported_version__mutmut_10(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"version probe failed: {exc}")
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(r"\b(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+|\+[0-9A-Za-z.-]+)?)\b", output)
    if process.returncode != 0 or match is None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"version probe returned {process.returncode}: {output[:240]}",
        )
    return match.group(1)


def x__reported_version__mutmut_11(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            text=True,
            check=False,
            )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"version probe failed: {exc}")
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(r"\b(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+|\+[0-9A-Za-z.-]+)?)\b", output)
    if process.returncode != 0 or match is None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"version probe returned {process.returncode}: {output[:240]}",
        )
    return match.group(1)


def x__reported_version__mutmut_12(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            [binary, "XX--versionXX"],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"version probe failed: {exc}")
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(r"\b(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+|\+[0-9A-Za-z.-]+)?)\b", output)
    if process.returncode != 0 or match is None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"version probe returned {process.returncode}: {output[:240]}",
        )
    return match.group(1)


def x__reported_version__mutmut_13(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            [binary, "--VERSION"],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"version probe failed: {exc}")
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(r"\b(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+|\+[0-9A-Za-z.-]+)?)\b", output)
    if process.returncode != 0 or match is None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"version probe returned {process.returncode}: {output[:240]}",
        )
    return match.group(1)


def x__reported_version__mutmut_14(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            [binary, "--version"],
            capture_output=False,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"version probe failed: {exc}")
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(r"\b(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+|\+[0-9A-Za-z.-]+)?)\b", output)
    if process.returncode != 0 or match is None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"version probe returned {process.returncode}: {output[:240]}",
        )
    return match.group(1)


def x__reported_version__mutmut_15(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            text=False,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"version probe failed: {exc}")
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(r"\b(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+|\+[0-9A-Za-z.-]+)?)\b", output)
    if process.returncode != 0 or match is None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"version probe returned {process.returncode}: {output[:240]}",
        )
    return match.group(1)


def x__reported_version__mutmut_16(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            text=True,
            check=True,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"version probe failed: {exc}")
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(r"\b(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+|\+[0-9A-Za-z.-]+)?)\b", output)
    if process.returncode != 0 or match is None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"version probe returned {process.returncode}: {output[:240]}",
        )
    return match.group(1)


def x__reported_version__mutmut_17(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(None, detail=f"version probe failed: {exc}")
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(r"\b(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+|\+[0-9A-Za-z.-]+)?)\b", output)
    if process.returncode != 0 or match is None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"version probe returned {process.returncode}: {output[:240]}",
        )
    return match.group(1)


def x__reported_version__mutmut_18(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=None)
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(r"\b(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+|\+[0-9A-Za-z.-]+)?)\b", output)
    if process.returncode != 0 or match is None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"version probe returned {process.returncode}: {output[:240]}",
        )
    return match.group(1)


def x__reported_version__mutmut_19(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(detail=f"version probe failed: {exc}")
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(r"\b(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+|\+[0-9A-Za-z.-]+)?)\b", output)
    if process.returncode != 0 or match is None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"version probe returned {process.returncode}: {output[:240]}",
        )
    return match.group(1)


def x__reported_version__mutmut_20(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, )
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(r"\b(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+|\+[0-9A-Za-z.-]+)?)\b", output)
    if process.returncode != 0 or match is None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"version probe returned {process.returncode}: {output[:240]}",
        )
    return match.group(1)


def x__reported_version__mutmut_21(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"version probe failed: {exc}")
    output = None
    match = re.search(r"\b(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+|\+[0-9A-Za-z.-]+)?)\b", output)
    if process.returncode != 0 or match is None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"version probe returned {process.returncode}: {output[:240]}",
        )
    return match.group(1)


def x__reported_version__mutmut_22(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"version probe failed: {exc}")
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = None
    if process.returncode != 0 or match is None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"version probe returned {process.returncode}: {output[:240]}",
        )
    return match.group(1)


def x__reported_version__mutmut_23(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"version probe failed: {exc}")
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(None, output)
    if process.returncode != 0 or match is None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"version probe returned {process.returncode}: {output[:240]}",
        )
    return match.group(1)


def x__reported_version__mutmut_24(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"version probe failed: {exc}")
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(r"\b(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+|\+[0-9A-Za-z.-]+)?)\b", None)
    if process.returncode != 0 or match is None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"version probe returned {process.returncode}: {output[:240]}",
        )
    return match.group(1)


def x__reported_version__mutmut_25(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"version probe failed: {exc}")
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(output)
    if process.returncode != 0 or match is None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"version probe returned {process.returncode}: {output[:240]}",
        )
    return match.group(1)


def x__reported_version__mutmut_26(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"version probe failed: {exc}")
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(r"\b(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+|\+[0-9A-Za-z.-]+)?)\b", )
    if process.returncode != 0 or match is None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"version probe returned {process.returncode}: {output[:240]}",
        )
    return match.group(1)


def x__reported_version__mutmut_27(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"version probe failed: {exc}")
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(r"XX\b(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+|\+[0-9A-Za-z.-]+)?)\bXX", output)
    if process.returncode != 0 or match is None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"version probe returned {process.returncode}: {output[:240]}",
        )
    return match.group(1)


def x__reported_version__mutmut_28(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"version probe failed: {exc}")
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(r"\b(\d+\.\d+\.\d+(?:-[0-9a-za-z.-]+|\+[0-9a-za-z.-]+)?)\b", output)
    if process.returncode != 0 or match is None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"version probe returned {process.returncode}: {output[:240]}",
        )
    return match.group(1)


def x__reported_version__mutmut_29(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"version probe failed: {exc}")
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(r"\b(\d+\.\d+\.\d+(?:-[0-9A-ZA-Z.-]+|\+[0-9A-ZA-Z.-]+)?)\b", output)
    if process.returncode != 0 or match is None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"version probe returned {process.returncode}: {output[:240]}",
        )
    return match.group(1)


def x__reported_version__mutmut_30(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"version probe failed: {exc}")
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(r"\b(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+|\+[0-9A-Za-z.-]+)?)\b", output)
    if process.returncode != 0 and match is None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"version probe returned {process.returncode}: {output[:240]}",
        )
    return match.group(1)


def x__reported_version__mutmut_31(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"version probe failed: {exc}")
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(r"\b(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+|\+[0-9A-Za-z.-]+)?)\b", output)
    if process.returncode == 0 or match is None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"version probe returned {process.returncode}: {output[:240]}",
        )
    return match.group(1)


def x__reported_version__mutmut_32(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"version probe failed: {exc}")
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(r"\b(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+|\+[0-9A-Za-z.-]+)?)\b", output)
    if process.returncode != 1 or match is None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"version probe returned {process.returncode}: {output[:240]}",
        )
    return match.group(1)


def x__reported_version__mutmut_33(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"version probe failed: {exc}")
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(r"\b(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+|\+[0-9A-Za-z.-]+)?)\b", output)
    if process.returncode != 0 or match is not None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"version probe returned {process.returncode}: {output[:240]}",
        )
    return match.group(1)


def x__reported_version__mutmut_34(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"version probe failed: {exc}")
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(r"\b(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+|\+[0-9A-Za-z.-]+)?)\b", output)
    if process.returncode != 0 or match is None:
        return ScanExecution(
            None,
            detail=f"version probe returned {process.returncode}: {output[:240]}",
        )
    return match.group(1)


def x__reported_version__mutmut_35(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"version probe failed: {exc}")
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(r"\b(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+|\+[0-9A-Za-z.-]+)?)\b", output)
    if process.returncode != 0 or match is None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=None,
        )
    return match.group(1)


def x__reported_version__mutmut_36(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"version probe failed: {exc}")
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(r"\b(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+|\+[0-9A-Za-z.-]+)?)\b", output)
    if process.returncode != 0 or match is None:
        return ScanExecution(
            detail=f"version probe returned {process.returncode}: {output[:240]}",
        )
    return match.group(1)


def x__reported_version__mutmut_37(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"version probe failed: {exc}")
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(r"\b(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+|\+[0-9A-Za-z.-]+)?)\b", output)
    if process.returncode != 0 or match is None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            )
    return match.group(1)


def x__reported_version__mutmut_38(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"version probe failed: {exc}")
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(r"\b(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+|\+[0-9A-Za-z.-]+)?)\b", output)
    if process.returncode != 0 or match is None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"version probe returned {process.returncode}: {output[:241]}",
        )
    return match.group(1)


def x__reported_version__mutmut_39(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"version probe failed: {exc}")
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(r"\b(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+|\+[0-9A-Za-z.-]+)?)\b", output)
    if process.returncode != 0 or match is None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"version probe returned {process.returncode}: {output[:240]}",
        )
    return match.group(None)


def x__reported_version__mutmut_40(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"version probe failed: {exc}")
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(r"\b(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+|\+[0-9A-Za-z.-]+)?)\b", output)
    if process.returncode != 0 or match is None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"version probe returned {process.returncode}: {output[:240]}",
        )
    return match.group(2)

mutants_x__reported_version__mutmut['_mutmut_orig'] = x__reported_version__mutmut_orig # type: ignore # mutmut generated
mutants_x__reported_version__mutmut['x__reported_version__mutmut_1'] = x__reported_version__mutmut_1 # type: ignore # mutmut generated
mutants_x__reported_version__mutmut['x__reported_version__mutmut_2'] = x__reported_version__mutmut_2 # type: ignore # mutmut generated
mutants_x__reported_version__mutmut['x__reported_version__mutmut_3'] = x__reported_version__mutmut_3 # type: ignore # mutmut generated
mutants_x__reported_version__mutmut['x__reported_version__mutmut_4'] = x__reported_version__mutmut_4 # type: ignore # mutmut generated
mutants_x__reported_version__mutmut['x__reported_version__mutmut_5'] = x__reported_version__mutmut_5 # type: ignore # mutmut generated
mutants_x__reported_version__mutmut['x__reported_version__mutmut_6'] = x__reported_version__mutmut_6 # type: ignore # mutmut generated
mutants_x__reported_version__mutmut['x__reported_version__mutmut_7'] = x__reported_version__mutmut_7 # type: ignore # mutmut generated
mutants_x__reported_version__mutmut['x__reported_version__mutmut_8'] = x__reported_version__mutmut_8 # type: ignore # mutmut generated
mutants_x__reported_version__mutmut['x__reported_version__mutmut_9'] = x__reported_version__mutmut_9 # type: ignore # mutmut generated
mutants_x__reported_version__mutmut['x__reported_version__mutmut_10'] = x__reported_version__mutmut_10 # type: ignore # mutmut generated
mutants_x__reported_version__mutmut['x__reported_version__mutmut_11'] = x__reported_version__mutmut_11 # type: ignore # mutmut generated
mutants_x__reported_version__mutmut['x__reported_version__mutmut_12'] = x__reported_version__mutmut_12 # type: ignore # mutmut generated
mutants_x__reported_version__mutmut['x__reported_version__mutmut_13'] = x__reported_version__mutmut_13 # type: ignore # mutmut generated
mutants_x__reported_version__mutmut['x__reported_version__mutmut_14'] = x__reported_version__mutmut_14 # type: ignore # mutmut generated
mutants_x__reported_version__mutmut['x__reported_version__mutmut_15'] = x__reported_version__mutmut_15 # type: ignore # mutmut generated
mutants_x__reported_version__mutmut['x__reported_version__mutmut_16'] = x__reported_version__mutmut_16 # type: ignore # mutmut generated
mutants_x__reported_version__mutmut['x__reported_version__mutmut_17'] = x__reported_version__mutmut_17 # type: ignore # mutmut generated
mutants_x__reported_version__mutmut['x__reported_version__mutmut_18'] = x__reported_version__mutmut_18 # type: ignore # mutmut generated
mutants_x__reported_version__mutmut['x__reported_version__mutmut_19'] = x__reported_version__mutmut_19 # type: ignore # mutmut generated
mutants_x__reported_version__mutmut['x__reported_version__mutmut_20'] = x__reported_version__mutmut_20 # type: ignore # mutmut generated
mutants_x__reported_version__mutmut['x__reported_version__mutmut_21'] = x__reported_version__mutmut_21 # type: ignore # mutmut generated
mutants_x__reported_version__mutmut['x__reported_version__mutmut_22'] = x__reported_version__mutmut_22 # type: ignore # mutmut generated
mutants_x__reported_version__mutmut['x__reported_version__mutmut_23'] = x__reported_version__mutmut_23 # type: ignore # mutmut generated
mutants_x__reported_version__mutmut['x__reported_version__mutmut_24'] = x__reported_version__mutmut_24 # type: ignore # mutmut generated
mutants_x__reported_version__mutmut['x__reported_version__mutmut_25'] = x__reported_version__mutmut_25 # type: ignore # mutmut generated
mutants_x__reported_version__mutmut['x__reported_version__mutmut_26'] = x__reported_version__mutmut_26 # type: ignore # mutmut generated
mutants_x__reported_version__mutmut['x__reported_version__mutmut_27'] = x__reported_version__mutmut_27 # type: ignore # mutmut generated
mutants_x__reported_version__mutmut['x__reported_version__mutmut_28'] = x__reported_version__mutmut_28 # type: ignore # mutmut generated
mutants_x__reported_version__mutmut['x__reported_version__mutmut_29'] = x__reported_version__mutmut_29 # type: ignore # mutmut generated
mutants_x__reported_version__mutmut['x__reported_version__mutmut_30'] = x__reported_version__mutmut_30 # type: ignore # mutmut generated
mutants_x__reported_version__mutmut['x__reported_version__mutmut_31'] = x__reported_version__mutmut_31 # type: ignore # mutmut generated
mutants_x__reported_version__mutmut['x__reported_version__mutmut_32'] = x__reported_version__mutmut_32 # type: ignore # mutmut generated
mutants_x__reported_version__mutmut['x__reported_version__mutmut_33'] = x__reported_version__mutmut_33 # type: ignore # mutmut generated
mutants_x__reported_version__mutmut['x__reported_version__mutmut_34'] = x__reported_version__mutmut_34 # type: ignore # mutmut generated
mutants_x__reported_version__mutmut['x__reported_version__mutmut_35'] = x__reported_version__mutmut_35 # type: ignore # mutmut generated
mutants_x__reported_version__mutmut['x__reported_version__mutmut_36'] = x__reported_version__mutmut_36 # type: ignore # mutmut generated
mutants_x__reported_version__mutmut['x__reported_version__mutmut_37'] = x__reported_version__mutmut_37 # type: ignore # mutmut generated
mutants_x__reported_version__mutmut['x__reported_version__mutmut_38'] = x__reported_version__mutmut_38 # type: ignore # mutmut generated
mutants_x__reported_version__mutmut['x__reported_version__mutmut_39'] = x__reported_version__mutmut_39 # type: ignore # mutmut generated
mutants_x__reported_version__mutmut['x__reported_version__mutmut_40'] = x__reported_version__mutmut_40 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_execute_scan__mutmut)
def execute_scan(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_orig(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_1(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = None
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_2(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which(None)
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_3(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("XXosv-scannerXX")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_4(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("OSV-SCANNER")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_5(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is not None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_6(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(None, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_7(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail=None)

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_8(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_9(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, )

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_10(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="XXosv-scanner is not on PATHXX")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_11(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on path")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_12(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="OSV-SCANNER IS NOT ON PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_13(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = None
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_14(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(None, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_15(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=None)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_16(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_17(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, )
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_18(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported == scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_19(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            None,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_20(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=None,
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_21(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_22(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_23(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = None
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_24(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = None
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_25(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = None
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_26(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(None)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_27(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                None,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_28(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=None,
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_29(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_30(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_31(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = None
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_32(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root * declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_33(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(None)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_34(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                None,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_35(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=None,
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_36(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_37(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_38(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(None)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_39(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = None
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_40(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(None, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_41(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, None, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_42(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=None) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_43(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_44(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_45(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, ) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_46(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=False) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_47(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_48(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            None,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_49(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=None,
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_50(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_51(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_52(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(None)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_53(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {'XX, XX'.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_54(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = None
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_55(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "XXscanXX", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_56(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "SCAN", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_57(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "XXsourceXX", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_58(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "SOURCE", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_59(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "XX--formatXX", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_60(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--FORMAT", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_61(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "XXjsonXX"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_62(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "JSON"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_63(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(None)
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_64(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("XX--lockfileXX", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_65(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--LOCKFILE", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_66(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(None)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_67(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = None
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_68(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            None,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_69(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=None,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_70(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=None,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_71(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=None,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_72(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=None,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_73(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=None,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_74(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_75(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_76(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_77(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_78(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_79(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_80(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=False,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_81(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=False,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_82(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_83(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(None, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_84(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=None)
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_85(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_86(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, )
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_87(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) and not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_88(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_89(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (1, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_90(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 2) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_91(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_92(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            None,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_93(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=None,
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_94(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_95(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_96(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:241]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_97(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = None
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_98(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(None)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_99(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(None, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_100(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=None)
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_101(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_102(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, )
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_103(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = None
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_104(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(None)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_105(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_106(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(None, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_107(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=None)
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_108(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_109(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, )
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_110(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 or not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_111(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode != 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_112(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 2 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_113(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_114(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(None):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_115(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            None,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_116(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=None,
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_117(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_118(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_119(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="XXscan returned exit 1 with no vulnerabilities in its reportXX",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_120(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="SCAN RETURNED EXIT 1 WITH NO VULNERABILITIES IN ITS REPORT",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def x_execute_scan__mutmut_121(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(None, report=report)


def x_execute_scan__mutmut_122(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, report=None)


def x_execute_scan__mutmut_123(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(report=report)


def x_execute_scan__mutmut_124(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    root = repo_root.resolve()
    paths: list[Path] = []
    for lockfile in lockfiles:
        declared = Path(lockfile)
        if declared.is_absolute():
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must be repository-relative: {lockfile}",
            )
        try:
            path = (root / declared).resolve()
            path.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            return ScanExecution(
                ScanStatus.INCOMPLETE,
                detail=f"declared lockfile must resolve beneath repository root: {lockfile}",
            )
        paths.append(path)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    if process.returncode == 1 and not vulnerability_ids(report):
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail="scan returned exit 1 with no vulnerabilities in its report",
        )
    return ScanExecution(ScanStatus.EXECUTED, )

mutants_x_execute_scan__mutmut['_mutmut_orig'] = x_execute_scan__mutmut_orig # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_1'] = x_execute_scan__mutmut_1 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_2'] = x_execute_scan__mutmut_2 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_3'] = x_execute_scan__mutmut_3 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_4'] = x_execute_scan__mutmut_4 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_5'] = x_execute_scan__mutmut_5 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_6'] = x_execute_scan__mutmut_6 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_7'] = x_execute_scan__mutmut_7 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_8'] = x_execute_scan__mutmut_8 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_9'] = x_execute_scan__mutmut_9 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_10'] = x_execute_scan__mutmut_10 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_11'] = x_execute_scan__mutmut_11 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_12'] = x_execute_scan__mutmut_12 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_13'] = x_execute_scan__mutmut_13 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_14'] = x_execute_scan__mutmut_14 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_15'] = x_execute_scan__mutmut_15 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_16'] = x_execute_scan__mutmut_16 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_17'] = x_execute_scan__mutmut_17 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_18'] = x_execute_scan__mutmut_18 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_19'] = x_execute_scan__mutmut_19 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_20'] = x_execute_scan__mutmut_20 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_21'] = x_execute_scan__mutmut_21 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_22'] = x_execute_scan__mutmut_22 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_23'] = x_execute_scan__mutmut_23 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_24'] = x_execute_scan__mutmut_24 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_25'] = x_execute_scan__mutmut_25 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_26'] = x_execute_scan__mutmut_26 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_27'] = x_execute_scan__mutmut_27 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_28'] = x_execute_scan__mutmut_28 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_29'] = x_execute_scan__mutmut_29 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_30'] = x_execute_scan__mutmut_30 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_31'] = x_execute_scan__mutmut_31 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_32'] = x_execute_scan__mutmut_32 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_33'] = x_execute_scan__mutmut_33 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_34'] = x_execute_scan__mutmut_34 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_35'] = x_execute_scan__mutmut_35 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_36'] = x_execute_scan__mutmut_36 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_37'] = x_execute_scan__mutmut_37 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_38'] = x_execute_scan__mutmut_38 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_39'] = x_execute_scan__mutmut_39 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_40'] = x_execute_scan__mutmut_40 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_41'] = x_execute_scan__mutmut_41 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_42'] = x_execute_scan__mutmut_42 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_43'] = x_execute_scan__mutmut_43 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_44'] = x_execute_scan__mutmut_44 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_45'] = x_execute_scan__mutmut_45 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_46'] = x_execute_scan__mutmut_46 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_47'] = x_execute_scan__mutmut_47 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_48'] = x_execute_scan__mutmut_48 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_49'] = x_execute_scan__mutmut_49 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_50'] = x_execute_scan__mutmut_50 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_51'] = x_execute_scan__mutmut_51 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_52'] = x_execute_scan__mutmut_52 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_53'] = x_execute_scan__mutmut_53 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_54'] = x_execute_scan__mutmut_54 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_55'] = x_execute_scan__mutmut_55 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_56'] = x_execute_scan__mutmut_56 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_57'] = x_execute_scan__mutmut_57 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_58'] = x_execute_scan__mutmut_58 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_59'] = x_execute_scan__mutmut_59 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_60'] = x_execute_scan__mutmut_60 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_61'] = x_execute_scan__mutmut_61 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_62'] = x_execute_scan__mutmut_62 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_63'] = x_execute_scan__mutmut_63 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_64'] = x_execute_scan__mutmut_64 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_65'] = x_execute_scan__mutmut_65 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_66'] = x_execute_scan__mutmut_66 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_67'] = x_execute_scan__mutmut_67 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_68'] = x_execute_scan__mutmut_68 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_69'] = x_execute_scan__mutmut_69 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_70'] = x_execute_scan__mutmut_70 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_71'] = x_execute_scan__mutmut_71 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_72'] = x_execute_scan__mutmut_72 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_73'] = x_execute_scan__mutmut_73 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_74'] = x_execute_scan__mutmut_74 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_75'] = x_execute_scan__mutmut_75 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_76'] = x_execute_scan__mutmut_76 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_77'] = x_execute_scan__mutmut_77 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_78'] = x_execute_scan__mutmut_78 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_79'] = x_execute_scan__mutmut_79 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_80'] = x_execute_scan__mutmut_80 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_81'] = x_execute_scan__mutmut_81 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_82'] = x_execute_scan__mutmut_82 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_83'] = x_execute_scan__mutmut_83 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_84'] = x_execute_scan__mutmut_84 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_85'] = x_execute_scan__mutmut_85 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_86'] = x_execute_scan__mutmut_86 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_87'] = x_execute_scan__mutmut_87 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_88'] = x_execute_scan__mutmut_88 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_89'] = x_execute_scan__mutmut_89 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_90'] = x_execute_scan__mutmut_90 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_91'] = x_execute_scan__mutmut_91 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_92'] = x_execute_scan__mutmut_92 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_93'] = x_execute_scan__mutmut_93 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_94'] = x_execute_scan__mutmut_94 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_95'] = x_execute_scan__mutmut_95 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_96'] = x_execute_scan__mutmut_96 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_97'] = x_execute_scan__mutmut_97 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_98'] = x_execute_scan__mutmut_98 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_99'] = x_execute_scan__mutmut_99 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_100'] = x_execute_scan__mutmut_100 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_101'] = x_execute_scan__mutmut_101 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_102'] = x_execute_scan__mutmut_102 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_103'] = x_execute_scan__mutmut_103 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_104'] = x_execute_scan__mutmut_104 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_105'] = x_execute_scan__mutmut_105 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_106'] = x_execute_scan__mutmut_106 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_107'] = x_execute_scan__mutmut_107 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_108'] = x_execute_scan__mutmut_108 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_109'] = x_execute_scan__mutmut_109 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_110'] = x_execute_scan__mutmut_110 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_111'] = x_execute_scan__mutmut_111 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_112'] = x_execute_scan__mutmut_112 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_113'] = x_execute_scan__mutmut_113 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_114'] = x_execute_scan__mutmut_114 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_115'] = x_execute_scan__mutmut_115 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_116'] = x_execute_scan__mutmut_116 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_117'] = x_execute_scan__mutmut_117 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_118'] = x_execute_scan__mutmut_118 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_119'] = x_execute_scan__mutmut_119 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_120'] = x_execute_scan__mutmut_120 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_121'] = x_execute_scan__mutmut_121 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_122'] = x_execute_scan__mutmut_122 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_123'] = x_execute_scan__mutmut_123 # type: ignore # mutmut generated
mutants_x_execute_scan__mutmut['x_execute_scan__mutmut_124'] = x_execute_scan__mutmut_124 # type: ignore # mutmut generated
mutants_x__report_error__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__report_error__mutmut)
def _report_error(report: object) -> str | None:
    if not isinstance(report, dict) or "results" not in report or not isinstance(report["results"], list):
        return "results must be present as a list"
    for result in report["results"]:
        if not isinstance(result, Mapping) or not isinstance(result.get("packages"), list):
            return "every result must contain a packages list"
        for package in result["packages"]:
            if not isinstance(package, Mapping) or not isinstance(package.get("vulnerabilities"), list):
                return "every package must contain a vulnerabilities list"
            for vulnerability in package["vulnerabilities"]:
                if not isinstance(vulnerability, Mapping) or not str(vulnerability.get("id", "")).strip():
                    return "every vulnerability must contain a non-empty id"
    return None


def x__report_error__mutmut_orig(report: object) -> str | None:
    if not isinstance(report, dict) or "results" not in report or not isinstance(report["results"], list):
        return "results must be present as a list"
    for result in report["results"]:
        if not isinstance(result, Mapping) or not isinstance(result.get("packages"), list):
            return "every result must contain a packages list"
        for package in result["packages"]:
            if not isinstance(package, Mapping) or not isinstance(package.get("vulnerabilities"), list):
                return "every package must contain a vulnerabilities list"
            for vulnerability in package["vulnerabilities"]:
                if not isinstance(vulnerability, Mapping) or not str(vulnerability.get("id", "")).strip():
                    return "every vulnerability must contain a non-empty id"
    return None


def x__report_error__mutmut_1(report: object) -> str | None:
    if not isinstance(report, dict) or "results" not in report and not isinstance(report["results"], list):
        return "results must be present as a list"
    for result in report["results"]:
        if not isinstance(result, Mapping) or not isinstance(result.get("packages"), list):
            return "every result must contain a packages list"
        for package in result["packages"]:
            if not isinstance(package, Mapping) or not isinstance(package.get("vulnerabilities"), list):
                return "every package must contain a vulnerabilities list"
            for vulnerability in package["vulnerabilities"]:
                if not isinstance(vulnerability, Mapping) or not str(vulnerability.get("id", "")).strip():
                    return "every vulnerability must contain a non-empty id"
    return None


def x__report_error__mutmut_2(report: object) -> str | None:
    if not isinstance(report, dict) and "results" not in report or not isinstance(report["results"], list):
        return "results must be present as a list"
    for result in report["results"]:
        if not isinstance(result, Mapping) or not isinstance(result.get("packages"), list):
            return "every result must contain a packages list"
        for package in result["packages"]:
            if not isinstance(package, Mapping) or not isinstance(package.get("vulnerabilities"), list):
                return "every package must contain a vulnerabilities list"
            for vulnerability in package["vulnerabilities"]:
                if not isinstance(vulnerability, Mapping) or not str(vulnerability.get("id", "")).strip():
                    return "every vulnerability must contain a non-empty id"
    return None


def x__report_error__mutmut_3(report: object) -> str | None:
    if isinstance(report, dict) or "results" not in report or not isinstance(report["results"], list):
        return "results must be present as a list"
    for result in report["results"]:
        if not isinstance(result, Mapping) or not isinstance(result.get("packages"), list):
            return "every result must contain a packages list"
        for package in result["packages"]:
            if not isinstance(package, Mapping) or not isinstance(package.get("vulnerabilities"), list):
                return "every package must contain a vulnerabilities list"
            for vulnerability in package["vulnerabilities"]:
                if not isinstance(vulnerability, Mapping) or not str(vulnerability.get("id", "")).strip():
                    return "every vulnerability must contain a non-empty id"
    return None


def x__report_error__mutmut_4(report: object) -> str | None:
    if not isinstance(report, dict) or "XXresultsXX" not in report or not isinstance(report["results"], list):
        return "results must be present as a list"
    for result in report["results"]:
        if not isinstance(result, Mapping) or not isinstance(result.get("packages"), list):
            return "every result must contain a packages list"
        for package in result["packages"]:
            if not isinstance(package, Mapping) or not isinstance(package.get("vulnerabilities"), list):
                return "every package must contain a vulnerabilities list"
            for vulnerability in package["vulnerabilities"]:
                if not isinstance(vulnerability, Mapping) or not str(vulnerability.get("id", "")).strip():
                    return "every vulnerability must contain a non-empty id"
    return None


def x__report_error__mutmut_5(report: object) -> str | None:
    if not isinstance(report, dict) or "RESULTS" not in report or not isinstance(report["results"], list):
        return "results must be present as a list"
    for result in report["results"]:
        if not isinstance(result, Mapping) or not isinstance(result.get("packages"), list):
            return "every result must contain a packages list"
        for package in result["packages"]:
            if not isinstance(package, Mapping) or not isinstance(package.get("vulnerabilities"), list):
                return "every package must contain a vulnerabilities list"
            for vulnerability in package["vulnerabilities"]:
                if not isinstance(vulnerability, Mapping) or not str(vulnerability.get("id", "")).strip():
                    return "every vulnerability must contain a non-empty id"
    return None


def x__report_error__mutmut_6(report: object) -> str | None:
    if not isinstance(report, dict) or "results" in report or not isinstance(report["results"], list):
        return "results must be present as a list"
    for result in report["results"]:
        if not isinstance(result, Mapping) or not isinstance(result.get("packages"), list):
            return "every result must contain a packages list"
        for package in result["packages"]:
            if not isinstance(package, Mapping) or not isinstance(package.get("vulnerabilities"), list):
                return "every package must contain a vulnerabilities list"
            for vulnerability in package["vulnerabilities"]:
                if not isinstance(vulnerability, Mapping) or not str(vulnerability.get("id", "")).strip():
                    return "every vulnerability must contain a non-empty id"
    return None


def x__report_error__mutmut_7(report: object) -> str | None:
    if not isinstance(report, dict) or "results" not in report or isinstance(report["results"], list):
        return "results must be present as a list"
    for result in report["results"]:
        if not isinstance(result, Mapping) or not isinstance(result.get("packages"), list):
            return "every result must contain a packages list"
        for package in result["packages"]:
            if not isinstance(package, Mapping) or not isinstance(package.get("vulnerabilities"), list):
                return "every package must contain a vulnerabilities list"
            for vulnerability in package["vulnerabilities"]:
                if not isinstance(vulnerability, Mapping) or not str(vulnerability.get("id", "")).strip():
                    return "every vulnerability must contain a non-empty id"
    return None


def x__report_error__mutmut_8(report: object) -> str | None:
    if not isinstance(report, dict) or "results" not in report or not isinstance(report["results"], list):
        return "XXresults must be present as a listXX"
    for result in report["results"]:
        if not isinstance(result, Mapping) or not isinstance(result.get("packages"), list):
            return "every result must contain a packages list"
        for package in result["packages"]:
            if not isinstance(package, Mapping) or not isinstance(package.get("vulnerabilities"), list):
                return "every package must contain a vulnerabilities list"
            for vulnerability in package["vulnerabilities"]:
                if not isinstance(vulnerability, Mapping) or not str(vulnerability.get("id", "")).strip():
                    return "every vulnerability must contain a non-empty id"
    return None


def x__report_error__mutmut_9(report: object) -> str | None:
    if not isinstance(report, dict) or "results" not in report or not isinstance(report["results"], list):
        return "RESULTS MUST BE PRESENT AS A LIST"
    for result in report["results"]:
        if not isinstance(result, Mapping) or not isinstance(result.get("packages"), list):
            return "every result must contain a packages list"
        for package in result["packages"]:
            if not isinstance(package, Mapping) or not isinstance(package.get("vulnerabilities"), list):
                return "every package must contain a vulnerabilities list"
            for vulnerability in package["vulnerabilities"]:
                if not isinstance(vulnerability, Mapping) or not str(vulnerability.get("id", "")).strip():
                    return "every vulnerability must contain a non-empty id"
    return None


def x__report_error__mutmut_10(report: object) -> str | None:
    if not isinstance(report, dict) or "results" not in report or not isinstance(report["results"], list):
        return "results must be present as a list"
    for result in report["XXresultsXX"]:
        if not isinstance(result, Mapping) or not isinstance(result.get("packages"), list):
            return "every result must contain a packages list"
        for package in result["packages"]:
            if not isinstance(package, Mapping) or not isinstance(package.get("vulnerabilities"), list):
                return "every package must contain a vulnerabilities list"
            for vulnerability in package["vulnerabilities"]:
                if not isinstance(vulnerability, Mapping) or not str(vulnerability.get("id", "")).strip():
                    return "every vulnerability must contain a non-empty id"
    return None


def x__report_error__mutmut_11(report: object) -> str | None:
    if not isinstance(report, dict) or "results" not in report or not isinstance(report["results"], list):
        return "results must be present as a list"
    for result in report["RESULTS"]:
        if not isinstance(result, Mapping) or not isinstance(result.get("packages"), list):
            return "every result must contain a packages list"
        for package in result["packages"]:
            if not isinstance(package, Mapping) or not isinstance(package.get("vulnerabilities"), list):
                return "every package must contain a vulnerabilities list"
            for vulnerability in package["vulnerabilities"]:
                if not isinstance(vulnerability, Mapping) or not str(vulnerability.get("id", "")).strip():
                    return "every vulnerability must contain a non-empty id"
    return None


def x__report_error__mutmut_12(report: object) -> str | None:
    if not isinstance(report, dict) or "results" not in report or not isinstance(report["results"], list):
        return "results must be present as a list"
    for result in report["results"]:
        if not isinstance(result, Mapping) and not isinstance(result.get("packages"), list):
            return "every result must contain a packages list"
        for package in result["packages"]:
            if not isinstance(package, Mapping) or not isinstance(package.get("vulnerabilities"), list):
                return "every package must contain a vulnerabilities list"
            for vulnerability in package["vulnerabilities"]:
                if not isinstance(vulnerability, Mapping) or not str(vulnerability.get("id", "")).strip():
                    return "every vulnerability must contain a non-empty id"
    return None


def x__report_error__mutmut_13(report: object) -> str | None:
    if not isinstance(report, dict) or "results" not in report or not isinstance(report["results"], list):
        return "results must be present as a list"
    for result in report["results"]:
        if isinstance(result, Mapping) or not isinstance(result.get("packages"), list):
            return "every result must contain a packages list"
        for package in result["packages"]:
            if not isinstance(package, Mapping) or not isinstance(package.get("vulnerabilities"), list):
                return "every package must contain a vulnerabilities list"
            for vulnerability in package["vulnerabilities"]:
                if not isinstance(vulnerability, Mapping) or not str(vulnerability.get("id", "")).strip():
                    return "every vulnerability must contain a non-empty id"
    return None


def x__report_error__mutmut_14(report: object) -> str | None:
    if not isinstance(report, dict) or "results" not in report or not isinstance(report["results"], list):
        return "results must be present as a list"
    for result in report["results"]:
        if not isinstance(result, Mapping) or isinstance(result.get("packages"), list):
            return "every result must contain a packages list"
        for package in result["packages"]:
            if not isinstance(package, Mapping) or not isinstance(package.get("vulnerabilities"), list):
                return "every package must contain a vulnerabilities list"
            for vulnerability in package["vulnerabilities"]:
                if not isinstance(vulnerability, Mapping) or not str(vulnerability.get("id", "")).strip():
                    return "every vulnerability must contain a non-empty id"
    return None


def x__report_error__mutmut_15(report: object) -> str | None:
    if not isinstance(report, dict) or "results" not in report or not isinstance(report["results"], list):
        return "results must be present as a list"
    for result in report["results"]:
        if not isinstance(result, Mapping) or not isinstance(result.get("packages"), list):
            return "XXevery result must contain a packages listXX"
        for package in result["packages"]:
            if not isinstance(package, Mapping) or not isinstance(package.get("vulnerabilities"), list):
                return "every package must contain a vulnerabilities list"
            for vulnerability in package["vulnerabilities"]:
                if not isinstance(vulnerability, Mapping) or not str(vulnerability.get("id", "")).strip():
                    return "every vulnerability must contain a non-empty id"
    return None


def x__report_error__mutmut_16(report: object) -> str | None:
    if not isinstance(report, dict) or "results" not in report or not isinstance(report["results"], list):
        return "results must be present as a list"
    for result in report["results"]:
        if not isinstance(result, Mapping) or not isinstance(result.get("packages"), list):
            return "EVERY RESULT MUST CONTAIN A PACKAGES LIST"
        for package in result["packages"]:
            if not isinstance(package, Mapping) or not isinstance(package.get("vulnerabilities"), list):
                return "every package must contain a vulnerabilities list"
            for vulnerability in package["vulnerabilities"]:
                if not isinstance(vulnerability, Mapping) or not str(vulnerability.get("id", "")).strip():
                    return "every vulnerability must contain a non-empty id"
    return None


def x__report_error__mutmut_17(report: object) -> str | None:
    if not isinstance(report, dict) or "results" not in report or not isinstance(report["results"], list):
        return "results must be present as a list"
    for result in report["results"]:
        if not isinstance(result, Mapping) or not isinstance(result.get("packages"), list):
            return "every result must contain a packages list"
        for package in result["XXpackagesXX"]:
            if not isinstance(package, Mapping) or not isinstance(package.get("vulnerabilities"), list):
                return "every package must contain a vulnerabilities list"
            for vulnerability in package["vulnerabilities"]:
                if not isinstance(vulnerability, Mapping) or not str(vulnerability.get("id", "")).strip():
                    return "every vulnerability must contain a non-empty id"
    return None


def x__report_error__mutmut_18(report: object) -> str | None:
    if not isinstance(report, dict) or "results" not in report or not isinstance(report["results"], list):
        return "results must be present as a list"
    for result in report["results"]:
        if not isinstance(result, Mapping) or not isinstance(result.get("packages"), list):
            return "every result must contain a packages list"
        for package in result["PACKAGES"]:
            if not isinstance(package, Mapping) or not isinstance(package.get("vulnerabilities"), list):
                return "every package must contain a vulnerabilities list"
            for vulnerability in package["vulnerabilities"]:
                if not isinstance(vulnerability, Mapping) or not str(vulnerability.get("id", "")).strip():
                    return "every vulnerability must contain a non-empty id"
    return None


def x__report_error__mutmut_19(report: object) -> str | None:
    if not isinstance(report, dict) or "results" not in report or not isinstance(report["results"], list):
        return "results must be present as a list"
    for result in report["results"]:
        if not isinstance(result, Mapping) or not isinstance(result.get("packages"), list):
            return "every result must contain a packages list"
        for package in result["packages"]:
            if not isinstance(package, Mapping) and not isinstance(package.get("vulnerabilities"), list):
                return "every package must contain a vulnerabilities list"
            for vulnerability in package["vulnerabilities"]:
                if not isinstance(vulnerability, Mapping) or not str(vulnerability.get("id", "")).strip():
                    return "every vulnerability must contain a non-empty id"
    return None


def x__report_error__mutmut_20(report: object) -> str | None:
    if not isinstance(report, dict) or "results" not in report or not isinstance(report["results"], list):
        return "results must be present as a list"
    for result in report["results"]:
        if not isinstance(result, Mapping) or not isinstance(result.get("packages"), list):
            return "every result must contain a packages list"
        for package in result["packages"]:
            if isinstance(package, Mapping) or not isinstance(package.get("vulnerabilities"), list):
                return "every package must contain a vulnerabilities list"
            for vulnerability in package["vulnerabilities"]:
                if not isinstance(vulnerability, Mapping) or not str(vulnerability.get("id", "")).strip():
                    return "every vulnerability must contain a non-empty id"
    return None


def x__report_error__mutmut_21(report: object) -> str | None:
    if not isinstance(report, dict) or "results" not in report or not isinstance(report["results"], list):
        return "results must be present as a list"
    for result in report["results"]:
        if not isinstance(result, Mapping) or not isinstance(result.get("packages"), list):
            return "every result must contain a packages list"
        for package in result["packages"]:
            if not isinstance(package, Mapping) or isinstance(package.get("vulnerabilities"), list):
                return "every package must contain a vulnerabilities list"
            for vulnerability in package["vulnerabilities"]:
                if not isinstance(vulnerability, Mapping) or not str(vulnerability.get("id", "")).strip():
                    return "every vulnerability must contain a non-empty id"
    return None


def x__report_error__mutmut_22(report: object) -> str | None:
    if not isinstance(report, dict) or "results" not in report or not isinstance(report["results"], list):
        return "results must be present as a list"
    for result in report["results"]:
        if not isinstance(result, Mapping) or not isinstance(result.get("packages"), list):
            return "every result must contain a packages list"
        for package in result["packages"]:
            if not isinstance(package, Mapping) or not isinstance(package.get("vulnerabilities"), list):
                return "XXevery package must contain a vulnerabilities listXX"
            for vulnerability in package["vulnerabilities"]:
                if not isinstance(vulnerability, Mapping) or not str(vulnerability.get("id", "")).strip():
                    return "every vulnerability must contain a non-empty id"
    return None


def x__report_error__mutmut_23(report: object) -> str | None:
    if not isinstance(report, dict) or "results" not in report or not isinstance(report["results"], list):
        return "results must be present as a list"
    for result in report["results"]:
        if not isinstance(result, Mapping) or not isinstance(result.get("packages"), list):
            return "every result must contain a packages list"
        for package in result["packages"]:
            if not isinstance(package, Mapping) or not isinstance(package.get("vulnerabilities"), list):
                return "EVERY PACKAGE MUST CONTAIN A VULNERABILITIES LIST"
            for vulnerability in package["vulnerabilities"]:
                if not isinstance(vulnerability, Mapping) or not str(vulnerability.get("id", "")).strip():
                    return "every vulnerability must contain a non-empty id"
    return None


def x__report_error__mutmut_24(report: object) -> str | None:
    if not isinstance(report, dict) or "results" not in report or not isinstance(report["results"], list):
        return "results must be present as a list"
    for result in report["results"]:
        if not isinstance(result, Mapping) or not isinstance(result.get("packages"), list):
            return "every result must contain a packages list"
        for package in result["packages"]:
            if not isinstance(package, Mapping) or not isinstance(package.get("vulnerabilities"), list):
                return "every package must contain a vulnerabilities list"
            for vulnerability in package["XXvulnerabilitiesXX"]:
                if not isinstance(vulnerability, Mapping) or not str(vulnerability.get("id", "")).strip():
                    return "every vulnerability must contain a non-empty id"
    return None


def x__report_error__mutmut_25(report: object) -> str | None:
    if not isinstance(report, dict) or "results" not in report or not isinstance(report["results"], list):
        return "results must be present as a list"
    for result in report["results"]:
        if not isinstance(result, Mapping) or not isinstance(result.get("packages"), list):
            return "every result must contain a packages list"
        for package in result["packages"]:
            if not isinstance(package, Mapping) or not isinstance(package.get("vulnerabilities"), list):
                return "every package must contain a vulnerabilities list"
            for vulnerability in package["VULNERABILITIES"]:
                if not isinstance(vulnerability, Mapping) or not str(vulnerability.get("id", "")).strip():
                    return "every vulnerability must contain a non-empty id"
    return None


def x__report_error__mutmut_26(report: object) -> str | None:
    if not isinstance(report, dict) or "results" not in report or not isinstance(report["results"], list):
        return "results must be present as a list"
    for result in report["results"]:
        if not isinstance(result, Mapping) or not isinstance(result.get("packages"), list):
            return "every result must contain a packages list"
        for package in result["packages"]:
            if not isinstance(package, Mapping) or not isinstance(package.get("vulnerabilities"), list):
                return "every package must contain a vulnerabilities list"
            for vulnerability in package["vulnerabilities"]:
                if not isinstance(vulnerability, Mapping) and not str(vulnerability.get("id", "")).strip():
                    return "every vulnerability must contain a non-empty id"
    return None


def x__report_error__mutmut_27(report: object) -> str | None:
    if not isinstance(report, dict) or "results" not in report or not isinstance(report["results"], list):
        return "results must be present as a list"
    for result in report["results"]:
        if not isinstance(result, Mapping) or not isinstance(result.get("packages"), list):
            return "every result must contain a packages list"
        for package in result["packages"]:
            if not isinstance(package, Mapping) or not isinstance(package.get("vulnerabilities"), list):
                return "every package must contain a vulnerabilities list"
            for vulnerability in package["vulnerabilities"]:
                if isinstance(vulnerability, Mapping) or not str(vulnerability.get("id", "")).strip():
                    return "every vulnerability must contain a non-empty id"
    return None


def x__report_error__mutmut_28(report: object) -> str | None:
    if not isinstance(report, dict) or "results" not in report or not isinstance(report["results"], list):
        return "results must be present as a list"
    for result in report["results"]:
        if not isinstance(result, Mapping) or not isinstance(result.get("packages"), list):
            return "every result must contain a packages list"
        for package in result["packages"]:
            if not isinstance(package, Mapping) or not isinstance(package.get("vulnerabilities"), list):
                return "every package must contain a vulnerabilities list"
            for vulnerability in package["vulnerabilities"]:
                if not isinstance(vulnerability, Mapping) or str(vulnerability.get("id", "")).strip():
                    return "every vulnerability must contain a non-empty id"
    return None


def x__report_error__mutmut_29(report: object) -> str | None:
    if not isinstance(report, dict) or "results" not in report or not isinstance(report["results"], list):
        return "results must be present as a list"
    for result in report["results"]:
        if not isinstance(result, Mapping) or not isinstance(result.get("packages"), list):
            return "every result must contain a packages list"
        for package in result["packages"]:
            if not isinstance(package, Mapping) or not isinstance(package.get("vulnerabilities"), list):
                return "every package must contain a vulnerabilities list"
            for vulnerability in package["vulnerabilities"]:
                if not isinstance(vulnerability, Mapping) or not str(None).strip():
                    return "every vulnerability must contain a non-empty id"
    return None


def x__report_error__mutmut_30(report: object) -> str | None:
    if not isinstance(report, dict) or "results" not in report or not isinstance(report["results"], list):
        return "results must be present as a list"
    for result in report["results"]:
        if not isinstance(result, Mapping) or not isinstance(result.get("packages"), list):
            return "every result must contain a packages list"
        for package in result["packages"]:
            if not isinstance(package, Mapping) or not isinstance(package.get("vulnerabilities"), list):
                return "every package must contain a vulnerabilities list"
            for vulnerability in package["vulnerabilities"]:
                if not isinstance(vulnerability, Mapping) or not str(vulnerability.get(None, "")).strip():
                    return "every vulnerability must contain a non-empty id"
    return None


def x__report_error__mutmut_31(report: object) -> str | None:
    if not isinstance(report, dict) or "results" not in report or not isinstance(report["results"], list):
        return "results must be present as a list"
    for result in report["results"]:
        if not isinstance(result, Mapping) or not isinstance(result.get("packages"), list):
            return "every result must contain a packages list"
        for package in result["packages"]:
            if not isinstance(package, Mapping) or not isinstance(package.get("vulnerabilities"), list):
                return "every package must contain a vulnerabilities list"
            for vulnerability in package["vulnerabilities"]:
                if not isinstance(vulnerability, Mapping) or not str(vulnerability.get("id", None)).strip():
                    return "every vulnerability must contain a non-empty id"
    return None


def x__report_error__mutmut_32(report: object) -> str | None:
    if not isinstance(report, dict) or "results" not in report or not isinstance(report["results"], list):
        return "results must be present as a list"
    for result in report["results"]:
        if not isinstance(result, Mapping) or not isinstance(result.get("packages"), list):
            return "every result must contain a packages list"
        for package in result["packages"]:
            if not isinstance(package, Mapping) or not isinstance(package.get("vulnerabilities"), list):
                return "every package must contain a vulnerabilities list"
            for vulnerability in package["vulnerabilities"]:
                if not isinstance(vulnerability, Mapping) or not str(vulnerability.get("")).strip():
                    return "every vulnerability must contain a non-empty id"
    return None


def x__report_error__mutmut_33(report: object) -> str | None:
    if not isinstance(report, dict) or "results" not in report or not isinstance(report["results"], list):
        return "results must be present as a list"
    for result in report["results"]:
        if not isinstance(result, Mapping) or not isinstance(result.get("packages"), list):
            return "every result must contain a packages list"
        for package in result["packages"]:
            if not isinstance(package, Mapping) or not isinstance(package.get("vulnerabilities"), list):
                return "every package must contain a vulnerabilities list"
            for vulnerability in package["vulnerabilities"]:
                if not isinstance(vulnerability, Mapping) or not str(vulnerability.get("id", )).strip():
                    return "every vulnerability must contain a non-empty id"
    return None


def x__report_error__mutmut_34(report: object) -> str | None:
    if not isinstance(report, dict) or "results" not in report or not isinstance(report["results"], list):
        return "results must be present as a list"
    for result in report["results"]:
        if not isinstance(result, Mapping) or not isinstance(result.get("packages"), list):
            return "every result must contain a packages list"
        for package in result["packages"]:
            if not isinstance(package, Mapping) or not isinstance(package.get("vulnerabilities"), list):
                return "every package must contain a vulnerabilities list"
            for vulnerability in package["vulnerabilities"]:
                if not isinstance(vulnerability, Mapping) or not str(vulnerability.get("XXidXX", "")).strip():
                    return "every vulnerability must contain a non-empty id"
    return None


def x__report_error__mutmut_35(report: object) -> str | None:
    if not isinstance(report, dict) or "results" not in report or not isinstance(report["results"], list):
        return "results must be present as a list"
    for result in report["results"]:
        if not isinstance(result, Mapping) or not isinstance(result.get("packages"), list):
            return "every result must contain a packages list"
        for package in result["packages"]:
            if not isinstance(package, Mapping) or not isinstance(package.get("vulnerabilities"), list):
                return "every package must contain a vulnerabilities list"
            for vulnerability in package["vulnerabilities"]:
                if not isinstance(vulnerability, Mapping) or not str(vulnerability.get("ID", "")).strip():
                    return "every vulnerability must contain a non-empty id"
    return None


def x__report_error__mutmut_36(report: object) -> str | None:
    if not isinstance(report, dict) or "results" not in report or not isinstance(report["results"], list):
        return "results must be present as a list"
    for result in report["results"]:
        if not isinstance(result, Mapping) or not isinstance(result.get("packages"), list):
            return "every result must contain a packages list"
        for package in result["packages"]:
            if not isinstance(package, Mapping) or not isinstance(package.get("vulnerabilities"), list):
                return "every package must contain a vulnerabilities list"
            for vulnerability in package["vulnerabilities"]:
                if not isinstance(vulnerability, Mapping) or not str(vulnerability.get("id", "XXXX")).strip():
                    return "every vulnerability must contain a non-empty id"
    return None


def x__report_error__mutmut_37(report: object) -> str | None:
    if not isinstance(report, dict) or "results" not in report or not isinstance(report["results"], list):
        return "results must be present as a list"
    for result in report["results"]:
        if not isinstance(result, Mapping) or not isinstance(result.get("packages"), list):
            return "every result must contain a packages list"
        for package in result["packages"]:
            if not isinstance(package, Mapping) or not isinstance(package.get("vulnerabilities"), list):
                return "every package must contain a vulnerabilities list"
            for vulnerability in package["vulnerabilities"]:
                if not isinstance(vulnerability, Mapping) or not str(vulnerability.get("id", "")).strip():
                    return "XXevery vulnerability must contain a non-empty idXX"
    return None


def x__report_error__mutmut_38(report: object) -> str | None:
    if not isinstance(report, dict) or "results" not in report or not isinstance(report["results"], list):
        return "results must be present as a list"
    for result in report["results"]:
        if not isinstance(result, Mapping) or not isinstance(result.get("packages"), list):
            return "every result must contain a packages list"
        for package in result["packages"]:
            if not isinstance(package, Mapping) or not isinstance(package.get("vulnerabilities"), list):
                return "every package must contain a vulnerabilities list"
            for vulnerability in package["vulnerabilities"]:
                if not isinstance(vulnerability, Mapping) or not str(vulnerability.get("id", "")).strip():
                    return "EVERY VULNERABILITY MUST CONTAIN A NON-EMPTY ID"
    return None

mutants_x__report_error__mutmut['_mutmut_orig'] = x__report_error__mutmut_orig # type: ignore # mutmut generated
mutants_x__report_error__mutmut['x__report_error__mutmut_1'] = x__report_error__mutmut_1 # type: ignore # mutmut generated
mutants_x__report_error__mutmut['x__report_error__mutmut_2'] = x__report_error__mutmut_2 # type: ignore # mutmut generated
mutants_x__report_error__mutmut['x__report_error__mutmut_3'] = x__report_error__mutmut_3 # type: ignore # mutmut generated
mutants_x__report_error__mutmut['x__report_error__mutmut_4'] = x__report_error__mutmut_4 # type: ignore # mutmut generated
mutants_x__report_error__mutmut['x__report_error__mutmut_5'] = x__report_error__mutmut_5 # type: ignore # mutmut generated
mutants_x__report_error__mutmut['x__report_error__mutmut_6'] = x__report_error__mutmut_6 # type: ignore # mutmut generated
mutants_x__report_error__mutmut['x__report_error__mutmut_7'] = x__report_error__mutmut_7 # type: ignore # mutmut generated
mutants_x__report_error__mutmut['x__report_error__mutmut_8'] = x__report_error__mutmut_8 # type: ignore # mutmut generated
mutants_x__report_error__mutmut['x__report_error__mutmut_9'] = x__report_error__mutmut_9 # type: ignore # mutmut generated
mutants_x__report_error__mutmut['x__report_error__mutmut_10'] = x__report_error__mutmut_10 # type: ignore # mutmut generated
mutants_x__report_error__mutmut['x__report_error__mutmut_11'] = x__report_error__mutmut_11 # type: ignore # mutmut generated
mutants_x__report_error__mutmut['x__report_error__mutmut_12'] = x__report_error__mutmut_12 # type: ignore # mutmut generated
mutants_x__report_error__mutmut['x__report_error__mutmut_13'] = x__report_error__mutmut_13 # type: ignore # mutmut generated
mutants_x__report_error__mutmut['x__report_error__mutmut_14'] = x__report_error__mutmut_14 # type: ignore # mutmut generated
mutants_x__report_error__mutmut['x__report_error__mutmut_15'] = x__report_error__mutmut_15 # type: ignore # mutmut generated
mutants_x__report_error__mutmut['x__report_error__mutmut_16'] = x__report_error__mutmut_16 # type: ignore # mutmut generated
mutants_x__report_error__mutmut['x__report_error__mutmut_17'] = x__report_error__mutmut_17 # type: ignore # mutmut generated
mutants_x__report_error__mutmut['x__report_error__mutmut_18'] = x__report_error__mutmut_18 # type: ignore # mutmut generated
mutants_x__report_error__mutmut['x__report_error__mutmut_19'] = x__report_error__mutmut_19 # type: ignore # mutmut generated
mutants_x__report_error__mutmut['x__report_error__mutmut_20'] = x__report_error__mutmut_20 # type: ignore # mutmut generated
mutants_x__report_error__mutmut['x__report_error__mutmut_21'] = x__report_error__mutmut_21 # type: ignore # mutmut generated
mutants_x__report_error__mutmut['x__report_error__mutmut_22'] = x__report_error__mutmut_22 # type: ignore # mutmut generated
mutants_x__report_error__mutmut['x__report_error__mutmut_23'] = x__report_error__mutmut_23 # type: ignore # mutmut generated
mutants_x__report_error__mutmut['x__report_error__mutmut_24'] = x__report_error__mutmut_24 # type: ignore # mutmut generated
mutants_x__report_error__mutmut['x__report_error__mutmut_25'] = x__report_error__mutmut_25 # type: ignore # mutmut generated
mutants_x__report_error__mutmut['x__report_error__mutmut_26'] = x__report_error__mutmut_26 # type: ignore # mutmut generated
mutants_x__report_error__mutmut['x__report_error__mutmut_27'] = x__report_error__mutmut_27 # type: ignore # mutmut generated
mutants_x__report_error__mutmut['x__report_error__mutmut_28'] = x__report_error__mutmut_28 # type: ignore # mutmut generated
mutants_x__report_error__mutmut['x__report_error__mutmut_29'] = x__report_error__mutmut_29 # type: ignore # mutmut generated
mutants_x__report_error__mutmut['x__report_error__mutmut_30'] = x__report_error__mutmut_30 # type: ignore # mutmut generated
mutants_x__report_error__mutmut['x__report_error__mutmut_31'] = x__report_error__mutmut_31 # type: ignore # mutmut generated
mutants_x__report_error__mutmut['x__report_error__mutmut_32'] = x__report_error__mutmut_32 # type: ignore # mutmut generated
mutants_x__report_error__mutmut['x__report_error__mutmut_33'] = x__report_error__mutmut_33 # type: ignore # mutmut generated
mutants_x__report_error__mutmut['x__report_error__mutmut_34'] = x__report_error__mutmut_34 # type: ignore # mutmut generated
mutants_x__report_error__mutmut['x__report_error__mutmut_35'] = x__report_error__mutmut_35 # type: ignore # mutmut generated
mutants_x__report_error__mutmut['x__report_error__mutmut_36'] = x__report_error__mutmut_36 # type: ignore # mutmut generated
mutants_x__report_error__mutmut['x__report_error__mutmut_37'] = x__report_error__mutmut_37 # type: ignore # mutmut generated
mutants_x__report_error__mutmut['x__report_error__mutmut_38'] = x__report_error__mutmut_38 # type: ignore # mutmut generated
mutants_x_vulnerability_ids__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_vulnerability_ids__mutmut)
def vulnerability_ids(report: Mapping[str, Any]) -> list[str]:
    """Return every reported advisory id without a suppression/baseline path."""
    found: list[str] = []
    for result in report.get("results", []) or []:
        for package in result.get("packages", []) or []:
            for vulnerability in package.get("vulnerabilities", []) or []:
                vulnerability_id = str(vulnerability.get("id", "")).strip()
                if vulnerability_id:
                    found.append(vulnerability_id)
    return sorted(set(found))


def x_vulnerability_ids__mutmut_orig(report: Mapping[str, Any]) -> list[str]:
    """Return every reported advisory id without a suppression/baseline path."""
    found: list[str] = []
    for result in report.get("results", []) or []:
        for package in result.get("packages", []) or []:
            for vulnerability in package.get("vulnerabilities", []) or []:
                vulnerability_id = str(vulnerability.get("id", "")).strip()
                if vulnerability_id:
                    found.append(vulnerability_id)
    return sorted(set(found))


def x_vulnerability_ids__mutmut_1(report: Mapping[str, Any]) -> list[str]:
    """Return every reported advisory id without a suppression/baseline path."""
    found: list[str] = None
    for result in report.get("results", []) or []:
        for package in result.get("packages", []) or []:
            for vulnerability in package.get("vulnerabilities", []) or []:
                vulnerability_id = str(vulnerability.get("id", "")).strip()
                if vulnerability_id:
                    found.append(vulnerability_id)
    return sorted(set(found))


def x_vulnerability_ids__mutmut_2(report: Mapping[str, Any]) -> list[str]:
    """Return every reported advisory id without a suppression/baseline path."""
    found: list[str] = []
    for result in report.get("results", []) and []:
        for package in result.get("packages", []) or []:
            for vulnerability in package.get("vulnerabilities", []) or []:
                vulnerability_id = str(vulnerability.get("id", "")).strip()
                if vulnerability_id:
                    found.append(vulnerability_id)
    return sorted(set(found))


def x_vulnerability_ids__mutmut_3(report: Mapping[str, Any]) -> list[str]:
    """Return every reported advisory id without a suppression/baseline path."""
    found: list[str] = []
    for result in report.get(None, []) or []:
        for package in result.get("packages", []) or []:
            for vulnerability in package.get("vulnerabilities", []) or []:
                vulnerability_id = str(vulnerability.get("id", "")).strip()
                if vulnerability_id:
                    found.append(vulnerability_id)
    return sorted(set(found))


def x_vulnerability_ids__mutmut_4(report: Mapping[str, Any]) -> list[str]:
    """Return every reported advisory id without a suppression/baseline path."""
    found: list[str] = []
    for result in report.get("results", None) or []:
        for package in result.get("packages", []) or []:
            for vulnerability in package.get("vulnerabilities", []) or []:
                vulnerability_id = str(vulnerability.get("id", "")).strip()
                if vulnerability_id:
                    found.append(vulnerability_id)
    return sorted(set(found))


def x_vulnerability_ids__mutmut_5(report: Mapping[str, Any]) -> list[str]:
    """Return every reported advisory id without a suppression/baseline path."""
    found: list[str] = []
    for result in report.get([]) or []:
        for package in result.get("packages", []) or []:
            for vulnerability in package.get("vulnerabilities", []) or []:
                vulnerability_id = str(vulnerability.get("id", "")).strip()
                if vulnerability_id:
                    found.append(vulnerability_id)
    return sorted(set(found))


def x_vulnerability_ids__mutmut_6(report: Mapping[str, Any]) -> list[str]:
    """Return every reported advisory id without a suppression/baseline path."""
    found: list[str] = []
    for result in report.get("results", ) or []:
        for package in result.get("packages", []) or []:
            for vulnerability in package.get("vulnerabilities", []) or []:
                vulnerability_id = str(vulnerability.get("id", "")).strip()
                if vulnerability_id:
                    found.append(vulnerability_id)
    return sorted(set(found))


def x_vulnerability_ids__mutmut_7(report: Mapping[str, Any]) -> list[str]:
    """Return every reported advisory id without a suppression/baseline path."""
    found: list[str] = []
    for result in report.get("XXresultsXX", []) or []:
        for package in result.get("packages", []) or []:
            for vulnerability in package.get("vulnerabilities", []) or []:
                vulnerability_id = str(vulnerability.get("id", "")).strip()
                if vulnerability_id:
                    found.append(vulnerability_id)
    return sorted(set(found))


def x_vulnerability_ids__mutmut_8(report: Mapping[str, Any]) -> list[str]:
    """Return every reported advisory id without a suppression/baseline path."""
    found: list[str] = []
    for result in report.get("RESULTS", []) or []:
        for package in result.get("packages", []) or []:
            for vulnerability in package.get("vulnerabilities", []) or []:
                vulnerability_id = str(vulnerability.get("id", "")).strip()
                if vulnerability_id:
                    found.append(vulnerability_id)
    return sorted(set(found))


def x_vulnerability_ids__mutmut_9(report: Mapping[str, Any]) -> list[str]:
    """Return every reported advisory id without a suppression/baseline path."""
    found: list[str] = []
    for result in report.get("results", []) or []:
        for package in result.get("packages", []) and []:
            for vulnerability in package.get("vulnerabilities", []) or []:
                vulnerability_id = str(vulnerability.get("id", "")).strip()
                if vulnerability_id:
                    found.append(vulnerability_id)
    return sorted(set(found))


def x_vulnerability_ids__mutmut_10(report: Mapping[str, Any]) -> list[str]:
    """Return every reported advisory id without a suppression/baseline path."""
    found: list[str] = []
    for result in report.get("results", []) or []:
        for package in result.get(None, []) or []:
            for vulnerability in package.get("vulnerabilities", []) or []:
                vulnerability_id = str(vulnerability.get("id", "")).strip()
                if vulnerability_id:
                    found.append(vulnerability_id)
    return sorted(set(found))


def x_vulnerability_ids__mutmut_11(report: Mapping[str, Any]) -> list[str]:
    """Return every reported advisory id without a suppression/baseline path."""
    found: list[str] = []
    for result in report.get("results", []) or []:
        for package in result.get("packages", None) or []:
            for vulnerability in package.get("vulnerabilities", []) or []:
                vulnerability_id = str(vulnerability.get("id", "")).strip()
                if vulnerability_id:
                    found.append(vulnerability_id)
    return sorted(set(found))


def x_vulnerability_ids__mutmut_12(report: Mapping[str, Any]) -> list[str]:
    """Return every reported advisory id without a suppression/baseline path."""
    found: list[str] = []
    for result in report.get("results", []) or []:
        for package in result.get([]) or []:
            for vulnerability in package.get("vulnerabilities", []) or []:
                vulnerability_id = str(vulnerability.get("id", "")).strip()
                if vulnerability_id:
                    found.append(vulnerability_id)
    return sorted(set(found))


def x_vulnerability_ids__mutmut_13(report: Mapping[str, Any]) -> list[str]:
    """Return every reported advisory id without a suppression/baseline path."""
    found: list[str] = []
    for result in report.get("results", []) or []:
        for package in result.get("packages", ) or []:
            for vulnerability in package.get("vulnerabilities", []) or []:
                vulnerability_id = str(vulnerability.get("id", "")).strip()
                if vulnerability_id:
                    found.append(vulnerability_id)
    return sorted(set(found))


def x_vulnerability_ids__mutmut_14(report: Mapping[str, Any]) -> list[str]:
    """Return every reported advisory id without a suppression/baseline path."""
    found: list[str] = []
    for result in report.get("results", []) or []:
        for package in result.get("XXpackagesXX", []) or []:
            for vulnerability in package.get("vulnerabilities", []) or []:
                vulnerability_id = str(vulnerability.get("id", "")).strip()
                if vulnerability_id:
                    found.append(vulnerability_id)
    return sorted(set(found))


def x_vulnerability_ids__mutmut_15(report: Mapping[str, Any]) -> list[str]:
    """Return every reported advisory id without a suppression/baseline path."""
    found: list[str] = []
    for result in report.get("results", []) or []:
        for package in result.get("PACKAGES", []) or []:
            for vulnerability in package.get("vulnerabilities", []) or []:
                vulnerability_id = str(vulnerability.get("id", "")).strip()
                if vulnerability_id:
                    found.append(vulnerability_id)
    return sorted(set(found))


def x_vulnerability_ids__mutmut_16(report: Mapping[str, Any]) -> list[str]:
    """Return every reported advisory id without a suppression/baseline path."""
    found: list[str] = []
    for result in report.get("results", []) or []:
        for package in result.get("packages", []) or []:
            for vulnerability in package.get("vulnerabilities", []) and []:
                vulnerability_id = str(vulnerability.get("id", "")).strip()
                if vulnerability_id:
                    found.append(vulnerability_id)
    return sorted(set(found))


def x_vulnerability_ids__mutmut_17(report: Mapping[str, Any]) -> list[str]:
    """Return every reported advisory id without a suppression/baseline path."""
    found: list[str] = []
    for result in report.get("results", []) or []:
        for package in result.get("packages", []) or []:
            for vulnerability in package.get(None, []) or []:
                vulnerability_id = str(vulnerability.get("id", "")).strip()
                if vulnerability_id:
                    found.append(vulnerability_id)
    return sorted(set(found))


def x_vulnerability_ids__mutmut_18(report: Mapping[str, Any]) -> list[str]:
    """Return every reported advisory id without a suppression/baseline path."""
    found: list[str] = []
    for result in report.get("results", []) or []:
        for package in result.get("packages", []) or []:
            for vulnerability in package.get("vulnerabilities", None) or []:
                vulnerability_id = str(vulnerability.get("id", "")).strip()
                if vulnerability_id:
                    found.append(vulnerability_id)
    return sorted(set(found))


def x_vulnerability_ids__mutmut_19(report: Mapping[str, Any]) -> list[str]:
    """Return every reported advisory id without a suppression/baseline path."""
    found: list[str] = []
    for result in report.get("results", []) or []:
        for package in result.get("packages", []) or []:
            for vulnerability in package.get([]) or []:
                vulnerability_id = str(vulnerability.get("id", "")).strip()
                if vulnerability_id:
                    found.append(vulnerability_id)
    return sorted(set(found))


def x_vulnerability_ids__mutmut_20(report: Mapping[str, Any]) -> list[str]:
    """Return every reported advisory id without a suppression/baseline path."""
    found: list[str] = []
    for result in report.get("results", []) or []:
        for package in result.get("packages", []) or []:
            for vulnerability in package.get("vulnerabilities", ) or []:
                vulnerability_id = str(vulnerability.get("id", "")).strip()
                if vulnerability_id:
                    found.append(vulnerability_id)
    return sorted(set(found))


def x_vulnerability_ids__mutmut_21(report: Mapping[str, Any]) -> list[str]:
    """Return every reported advisory id without a suppression/baseline path."""
    found: list[str] = []
    for result in report.get("results", []) or []:
        for package in result.get("packages", []) or []:
            for vulnerability in package.get("XXvulnerabilitiesXX", []) or []:
                vulnerability_id = str(vulnerability.get("id", "")).strip()
                if vulnerability_id:
                    found.append(vulnerability_id)
    return sorted(set(found))


def x_vulnerability_ids__mutmut_22(report: Mapping[str, Any]) -> list[str]:
    """Return every reported advisory id without a suppression/baseline path."""
    found: list[str] = []
    for result in report.get("results", []) or []:
        for package in result.get("packages", []) or []:
            for vulnerability in package.get("VULNERABILITIES", []) or []:
                vulnerability_id = str(vulnerability.get("id", "")).strip()
                if vulnerability_id:
                    found.append(vulnerability_id)
    return sorted(set(found))


def x_vulnerability_ids__mutmut_23(report: Mapping[str, Any]) -> list[str]:
    """Return every reported advisory id without a suppression/baseline path."""
    found: list[str] = []
    for result in report.get("results", []) or []:
        for package in result.get("packages", []) or []:
            for vulnerability in package.get("vulnerabilities", []) or []:
                vulnerability_id = None
                if vulnerability_id:
                    found.append(vulnerability_id)
    return sorted(set(found))


def x_vulnerability_ids__mutmut_24(report: Mapping[str, Any]) -> list[str]:
    """Return every reported advisory id without a suppression/baseline path."""
    found: list[str] = []
    for result in report.get("results", []) or []:
        for package in result.get("packages", []) or []:
            for vulnerability in package.get("vulnerabilities", []) or []:
                vulnerability_id = str(None).strip()
                if vulnerability_id:
                    found.append(vulnerability_id)
    return sorted(set(found))


def x_vulnerability_ids__mutmut_25(report: Mapping[str, Any]) -> list[str]:
    """Return every reported advisory id without a suppression/baseline path."""
    found: list[str] = []
    for result in report.get("results", []) or []:
        for package in result.get("packages", []) or []:
            for vulnerability in package.get("vulnerabilities", []) or []:
                vulnerability_id = str(vulnerability.get(None, "")).strip()
                if vulnerability_id:
                    found.append(vulnerability_id)
    return sorted(set(found))


def x_vulnerability_ids__mutmut_26(report: Mapping[str, Any]) -> list[str]:
    """Return every reported advisory id without a suppression/baseline path."""
    found: list[str] = []
    for result in report.get("results", []) or []:
        for package in result.get("packages", []) or []:
            for vulnerability in package.get("vulnerabilities", []) or []:
                vulnerability_id = str(vulnerability.get("id", None)).strip()
                if vulnerability_id:
                    found.append(vulnerability_id)
    return sorted(set(found))


def x_vulnerability_ids__mutmut_27(report: Mapping[str, Any]) -> list[str]:
    """Return every reported advisory id without a suppression/baseline path."""
    found: list[str] = []
    for result in report.get("results", []) or []:
        for package in result.get("packages", []) or []:
            for vulnerability in package.get("vulnerabilities", []) or []:
                vulnerability_id = str(vulnerability.get("")).strip()
                if vulnerability_id:
                    found.append(vulnerability_id)
    return sorted(set(found))


def x_vulnerability_ids__mutmut_28(report: Mapping[str, Any]) -> list[str]:
    """Return every reported advisory id without a suppression/baseline path."""
    found: list[str] = []
    for result in report.get("results", []) or []:
        for package in result.get("packages", []) or []:
            for vulnerability in package.get("vulnerabilities", []) or []:
                vulnerability_id = str(vulnerability.get("id", )).strip()
                if vulnerability_id:
                    found.append(vulnerability_id)
    return sorted(set(found))


def x_vulnerability_ids__mutmut_29(report: Mapping[str, Any]) -> list[str]:
    """Return every reported advisory id without a suppression/baseline path."""
    found: list[str] = []
    for result in report.get("results", []) or []:
        for package in result.get("packages", []) or []:
            for vulnerability in package.get("vulnerabilities", []) or []:
                vulnerability_id = str(vulnerability.get("XXidXX", "")).strip()
                if vulnerability_id:
                    found.append(vulnerability_id)
    return sorted(set(found))


def x_vulnerability_ids__mutmut_30(report: Mapping[str, Any]) -> list[str]:
    """Return every reported advisory id without a suppression/baseline path."""
    found: list[str] = []
    for result in report.get("results", []) or []:
        for package in result.get("packages", []) or []:
            for vulnerability in package.get("vulnerabilities", []) or []:
                vulnerability_id = str(vulnerability.get("ID", "")).strip()
                if vulnerability_id:
                    found.append(vulnerability_id)
    return sorted(set(found))


def x_vulnerability_ids__mutmut_31(report: Mapping[str, Any]) -> list[str]:
    """Return every reported advisory id without a suppression/baseline path."""
    found: list[str] = []
    for result in report.get("results", []) or []:
        for package in result.get("packages", []) or []:
            for vulnerability in package.get("vulnerabilities", []) or []:
                vulnerability_id = str(vulnerability.get("id", "XXXX")).strip()
                if vulnerability_id:
                    found.append(vulnerability_id)
    return sorted(set(found))


def x_vulnerability_ids__mutmut_32(report: Mapping[str, Any]) -> list[str]:
    """Return every reported advisory id without a suppression/baseline path."""
    found: list[str] = []
    for result in report.get("results", []) or []:
        for package in result.get("packages", []) or []:
            for vulnerability in package.get("vulnerabilities", []) or []:
                vulnerability_id = str(vulnerability.get("id", "")).strip()
                if vulnerability_id:
                    found.append(None)
    return sorted(set(found))


def x_vulnerability_ids__mutmut_33(report: Mapping[str, Any]) -> list[str]:
    """Return every reported advisory id without a suppression/baseline path."""
    found: list[str] = []
    for result in report.get("results", []) or []:
        for package in result.get("packages", []) or []:
            for vulnerability in package.get("vulnerabilities", []) or []:
                vulnerability_id = str(vulnerability.get("id", "")).strip()
                if vulnerability_id:
                    found.append(vulnerability_id)
    return sorted(None)


def x_vulnerability_ids__mutmut_34(report: Mapping[str, Any]) -> list[str]:
    """Return every reported advisory id without a suppression/baseline path."""
    found: list[str] = []
    for result in report.get("results", []) or []:
        for package in result.get("packages", []) or []:
            for vulnerability in package.get("vulnerabilities", []) or []:
                vulnerability_id = str(vulnerability.get("id", "")).strip()
                if vulnerability_id:
                    found.append(vulnerability_id)
    return sorted(set(None))

mutants_x_vulnerability_ids__mutmut['_mutmut_orig'] = x_vulnerability_ids__mutmut_orig # type: ignore # mutmut generated
mutants_x_vulnerability_ids__mutmut['x_vulnerability_ids__mutmut_1'] = x_vulnerability_ids__mutmut_1 # type: ignore # mutmut generated
mutants_x_vulnerability_ids__mutmut['x_vulnerability_ids__mutmut_2'] = x_vulnerability_ids__mutmut_2 # type: ignore # mutmut generated
mutants_x_vulnerability_ids__mutmut['x_vulnerability_ids__mutmut_3'] = x_vulnerability_ids__mutmut_3 # type: ignore # mutmut generated
mutants_x_vulnerability_ids__mutmut['x_vulnerability_ids__mutmut_4'] = x_vulnerability_ids__mutmut_4 # type: ignore # mutmut generated
mutants_x_vulnerability_ids__mutmut['x_vulnerability_ids__mutmut_5'] = x_vulnerability_ids__mutmut_5 # type: ignore # mutmut generated
mutants_x_vulnerability_ids__mutmut['x_vulnerability_ids__mutmut_6'] = x_vulnerability_ids__mutmut_6 # type: ignore # mutmut generated
mutants_x_vulnerability_ids__mutmut['x_vulnerability_ids__mutmut_7'] = x_vulnerability_ids__mutmut_7 # type: ignore # mutmut generated
mutants_x_vulnerability_ids__mutmut['x_vulnerability_ids__mutmut_8'] = x_vulnerability_ids__mutmut_8 # type: ignore # mutmut generated
mutants_x_vulnerability_ids__mutmut['x_vulnerability_ids__mutmut_9'] = x_vulnerability_ids__mutmut_9 # type: ignore # mutmut generated
mutants_x_vulnerability_ids__mutmut['x_vulnerability_ids__mutmut_10'] = x_vulnerability_ids__mutmut_10 # type: ignore # mutmut generated
mutants_x_vulnerability_ids__mutmut['x_vulnerability_ids__mutmut_11'] = x_vulnerability_ids__mutmut_11 # type: ignore # mutmut generated
mutants_x_vulnerability_ids__mutmut['x_vulnerability_ids__mutmut_12'] = x_vulnerability_ids__mutmut_12 # type: ignore # mutmut generated
mutants_x_vulnerability_ids__mutmut['x_vulnerability_ids__mutmut_13'] = x_vulnerability_ids__mutmut_13 # type: ignore # mutmut generated
mutants_x_vulnerability_ids__mutmut['x_vulnerability_ids__mutmut_14'] = x_vulnerability_ids__mutmut_14 # type: ignore # mutmut generated
mutants_x_vulnerability_ids__mutmut['x_vulnerability_ids__mutmut_15'] = x_vulnerability_ids__mutmut_15 # type: ignore # mutmut generated
mutants_x_vulnerability_ids__mutmut['x_vulnerability_ids__mutmut_16'] = x_vulnerability_ids__mutmut_16 # type: ignore # mutmut generated
mutants_x_vulnerability_ids__mutmut['x_vulnerability_ids__mutmut_17'] = x_vulnerability_ids__mutmut_17 # type: ignore # mutmut generated
mutants_x_vulnerability_ids__mutmut['x_vulnerability_ids__mutmut_18'] = x_vulnerability_ids__mutmut_18 # type: ignore # mutmut generated
mutants_x_vulnerability_ids__mutmut['x_vulnerability_ids__mutmut_19'] = x_vulnerability_ids__mutmut_19 # type: ignore # mutmut generated
mutants_x_vulnerability_ids__mutmut['x_vulnerability_ids__mutmut_20'] = x_vulnerability_ids__mutmut_20 # type: ignore # mutmut generated
mutants_x_vulnerability_ids__mutmut['x_vulnerability_ids__mutmut_21'] = x_vulnerability_ids__mutmut_21 # type: ignore # mutmut generated
mutants_x_vulnerability_ids__mutmut['x_vulnerability_ids__mutmut_22'] = x_vulnerability_ids__mutmut_22 # type: ignore # mutmut generated
mutants_x_vulnerability_ids__mutmut['x_vulnerability_ids__mutmut_23'] = x_vulnerability_ids__mutmut_23 # type: ignore # mutmut generated
mutants_x_vulnerability_ids__mutmut['x_vulnerability_ids__mutmut_24'] = x_vulnerability_ids__mutmut_24 # type: ignore # mutmut generated
mutants_x_vulnerability_ids__mutmut['x_vulnerability_ids__mutmut_25'] = x_vulnerability_ids__mutmut_25 # type: ignore # mutmut generated
mutants_x_vulnerability_ids__mutmut['x_vulnerability_ids__mutmut_26'] = x_vulnerability_ids__mutmut_26 # type: ignore # mutmut generated
mutants_x_vulnerability_ids__mutmut['x_vulnerability_ids__mutmut_27'] = x_vulnerability_ids__mutmut_27 # type: ignore # mutmut generated
mutants_x_vulnerability_ids__mutmut['x_vulnerability_ids__mutmut_28'] = x_vulnerability_ids__mutmut_28 # type: ignore # mutmut generated
mutants_x_vulnerability_ids__mutmut['x_vulnerability_ids__mutmut_29'] = x_vulnerability_ids__mutmut_29 # type: ignore # mutmut generated
mutants_x_vulnerability_ids__mutmut['x_vulnerability_ids__mutmut_30'] = x_vulnerability_ids__mutmut_30 # type: ignore # mutmut generated
mutants_x_vulnerability_ids__mutmut['x_vulnerability_ids__mutmut_31'] = x_vulnerability_ids__mutmut_31 # type: ignore # mutmut generated
mutants_x_vulnerability_ids__mutmut['x_vulnerability_ids__mutmut_32'] = x_vulnerability_ids__mutmut_32 # type: ignore # mutmut generated
mutants_x_vulnerability_ids__mutmut['x_vulnerability_ids__mutmut_33'] = x_vulnerability_ids__mutmut_33 # type: ignore # mutmut generated
mutants_x_vulnerability_ids__mutmut['x_vulnerability_ids__mutmut_34'] = x_vulnerability_ids__mutmut_34 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ__init____mutmut: MutantDict = {}  # type: ignore
mutants_xǁOsvScannerScaǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁOsvScannerScaǁ_execute__mutmut: MutantDict = {}  # type: ignore
mutants_xǁOsvScannerScaǁevaluate__mutmut: MutantDict = {}  # type: ignore
mutants_xǁOsvScannerScaǁrun__mutmut: MutantDict = {}  # type: ignore


class OsvScannerSca:
    """Pinned, no-grandfathering SCA contract for consumer lockfiles."""

    name = "osv-scanner-sca"

    @_mutmut_mutated(mutants_xǁOsvScannerScaǁ__init____mutmut)
    def __init__(
        self,
        repo_root: Path | None = None,
        *,
        scanner_version: str | None,
        lockfiles: Sequence[str] = (),
        required: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
        runner: Runner | None = None,
    ) -> None:
        self.active = scanner_version is not None
        if scanner_version is not None and not re.fullmatch(r"\d+\.\d+\.\d+", scanner_version):
            raise ValueError("scanner_version must be an exact x.y.z pin")
        if self.active and required and not lockfiles:
            raise ValueError("required OSV scanning must declare at least one lockfile")
        self.repo_root = (repo_root or REPO_ROOT).resolve()
        self.scanner_version = scanner_version or ""
        self.lockfiles = tuple(lockfiles)
        self.required = required
        self.timeout = timeout
        self._runner = runner

    def xǁOsvScannerScaǁ__init____mutmut_orig(
        self,
        repo_root: Path | None = None,
        *,
        scanner_version: str | None,
        lockfiles: Sequence[str] = (),
        required: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
        runner: Runner | None = None,
    ) -> None:
        self.active = scanner_version is not None
        if scanner_version is not None and not re.fullmatch(r"\d+\.\d+\.\d+", scanner_version):
            raise ValueError("scanner_version must be an exact x.y.z pin")
        if self.active and required and not lockfiles:
            raise ValueError("required OSV scanning must declare at least one lockfile")
        self.repo_root = (repo_root or REPO_ROOT).resolve()
        self.scanner_version = scanner_version or ""
        self.lockfiles = tuple(lockfiles)
        self.required = required
        self.timeout = timeout
        self._runner = runner

    def xǁOsvScannerScaǁ__init____mutmut_1(
        self,
        repo_root: Path | None = None,
        *,
        scanner_version: str | None,
        lockfiles: Sequence[str] = (),
        required: bool = False,
        timeout: int = DEFAULT_TIMEOUT,
        runner: Runner | None = None,
    ) -> None:
        self.active = scanner_version is not None
        if scanner_version is not None and not re.fullmatch(r"\d+\.\d+\.\d+", scanner_version):
            raise ValueError("scanner_version must be an exact x.y.z pin")
        if self.active and required and not lockfiles:
            raise ValueError("required OSV scanning must declare at least one lockfile")
        self.repo_root = (repo_root or REPO_ROOT).resolve()
        self.scanner_version = scanner_version or ""
        self.lockfiles = tuple(lockfiles)
        self.required = required
        self.timeout = timeout
        self._runner = runner

    def xǁOsvScannerScaǁ__init____mutmut_2(
        self,
        repo_root: Path | None = None,
        *,
        scanner_version: str | None,
        lockfiles: Sequence[str] = (),
        required: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
        runner: Runner | None = None,
    ) -> None:
        self.active = None
        if scanner_version is not None and not re.fullmatch(r"\d+\.\d+\.\d+", scanner_version):
            raise ValueError("scanner_version must be an exact x.y.z pin")
        if self.active and required and not lockfiles:
            raise ValueError("required OSV scanning must declare at least one lockfile")
        self.repo_root = (repo_root or REPO_ROOT).resolve()
        self.scanner_version = scanner_version or ""
        self.lockfiles = tuple(lockfiles)
        self.required = required
        self.timeout = timeout
        self._runner = runner

    def xǁOsvScannerScaǁ__init____mutmut_3(
        self,
        repo_root: Path | None = None,
        *,
        scanner_version: str | None,
        lockfiles: Sequence[str] = (),
        required: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
        runner: Runner | None = None,
    ) -> None:
        self.active = scanner_version is None
        if scanner_version is not None and not re.fullmatch(r"\d+\.\d+\.\d+", scanner_version):
            raise ValueError("scanner_version must be an exact x.y.z pin")
        if self.active and required and not lockfiles:
            raise ValueError("required OSV scanning must declare at least one lockfile")
        self.repo_root = (repo_root or REPO_ROOT).resolve()
        self.scanner_version = scanner_version or ""
        self.lockfiles = tuple(lockfiles)
        self.required = required
        self.timeout = timeout
        self._runner = runner

    def xǁOsvScannerScaǁ__init____mutmut_4(
        self,
        repo_root: Path | None = None,
        *,
        scanner_version: str | None,
        lockfiles: Sequence[str] = (),
        required: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
        runner: Runner | None = None,
    ) -> None:
        self.active = scanner_version is not None
        if scanner_version is not None or not re.fullmatch(r"\d+\.\d+\.\d+", scanner_version):
            raise ValueError("scanner_version must be an exact x.y.z pin")
        if self.active and required and not lockfiles:
            raise ValueError("required OSV scanning must declare at least one lockfile")
        self.repo_root = (repo_root or REPO_ROOT).resolve()
        self.scanner_version = scanner_version or ""
        self.lockfiles = tuple(lockfiles)
        self.required = required
        self.timeout = timeout
        self._runner = runner

    def xǁOsvScannerScaǁ__init____mutmut_5(
        self,
        repo_root: Path | None = None,
        *,
        scanner_version: str | None,
        lockfiles: Sequence[str] = (),
        required: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
        runner: Runner | None = None,
    ) -> None:
        self.active = scanner_version is not None
        if scanner_version is None and not re.fullmatch(r"\d+\.\d+\.\d+", scanner_version):
            raise ValueError("scanner_version must be an exact x.y.z pin")
        if self.active and required and not lockfiles:
            raise ValueError("required OSV scanning must declare at least one lockfile")
        self.repo_root = (repo_root or REPO_ROOT).resolve()
        self.scanner_version = scanner_version or ""
        self.lockfiles = tuple(lockfiles)
        self.required = required
        self.timeout = timeout
        self._runner = runner

    def xǁOsvScannerScaǁ__init____mutmut_6(
        self,
        repo_root: Path | None = None,
        *,
        scanner_version: str | None,
        lockfiles: Sequence[str] = (),
        required: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
        runner: Runner | None = None,
    ) -> None:
        self.active = scanner_version is not None
        if scanner_version is not None and re.fullmatch(r"\d+\.\d+\.\d+", scanner_version):
            raise ValueError("scanner_version must be an exact x.y.z pin")
        if self.active and required and not lockfiles:
            raise ValueError("required OSV scanning must declare at least one lockfile")
        self.repo_root = (repo_root or REPO_ROOT).resolve()
        self.scanner_version = scanner_version or ""
        self.lockfiles = tuple(lockfiles)
        self.required = required
        self.timeout = timeout
        self._runner = runner

    def xǁOsvScannerScaǁ__init____mutmut_7(
        self,
        repo_root: Path | None = None,
        *,
        scanner_version: str | None,
        lockfiles: Sequence[str] = (),
        required: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
        runner: Runner | None = None,
    ) -> None:
        self.active = scanner_version is not None
        if scanner_version is not None and not re.fullmatch(None, scanner_version):
            raise ValueError("scanner_version must be an exact x.y.z pin")
        if self.active and required and not lockfiles:
            raise ValueError("required OSV scanning must declare at least one lockfile")
        self.repo_root = (repo_root or REPO_ROOT).resolve()
        self.scanner_version = scanner_version or ""
        self.lockfiles = tuple(lockfiles)
        self.required = required
        self.timeout = timeout
        self._runner = runner

    def xǁOsvScannerScaǁ__init____mutmut_8(
        self,
        repo_root: Path | None = None,
        *,
        scanner_version: str | None,
        lockfiles: Sequence[str] = (),
        required: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
        runner: Runner | None = None,
    ) -> None:
        self.active = scanner_version is not None
        if scanner_version is not None and not re.fullmatch(r"\d+\.\d+\.\d+", None):
            raise ValueError("scanner_version must be an exact x.y.z pin")
        if self.active and required and not lockfiles:
            raise ValueError("required OSV scanning must declare at least one lockfile")
        self.repo_root = (repo_root or REPO_ROOT).resolve()
        self.scanner_version = scanner_version or ""
        self.lockfiles = tuple(lockfiles)
        self.required = required
        self.timeout = timeout
        self._runner = runner

    def xǁOsvScannerScaǁ__init____mutmut_9(
        self,
        repo_root: Path | None = None,
        *,
        scanner_version: str | None,
        lockfiles: Sequence[str] = (),
        required: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
        runner: Runner | None = None,
    ) -> None:
        self.active = scanner_version is not None
        if scanner_version is not None and not re.fullmatch(scanner_version):
            raise ValueError("scanner_version must be an exact x.y.z pin")
        if self.active and required and not lockfiles:
            raise ValueError("required OSV scanning must declare at least one lockfile")
        self.repo_root = (repo_root or REPO_ROOT).resolve()
        self.scanner_version = scanner_version or ""
        self.lockfiles = tuple(lockfiles)
        self.required = required
        self.timeout = timeout
        self._runner = runner

    def xǁOsvScannerScaǁ__init____mutmut_10(
        self,
        repo_root: Path | None = None,
        *,
        scanner_version: str | None,
        lockfiles: Sequence[str] = (),
        required: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
        runner: Runner | None = None,
    ) -> None:
        self.active = scanner_version is not None
        if scanner_version is not None and not re.fullmatch(r"\d+\.\d+\.\d+", ):
            raise ValueError("scanner_version must be an exact x.y.z pin")
        if self.active and required and not lockfiles:
            raise ValueError("required OSV scanning must declare at least one lockfile")
        self.repo_root = (repo_root or REPO_ROOT).resolve()
        self.scanner_version = scanner_version or ""
        self.lockfiles = tuple(lockfiles)
        self.required = required
        self.timeout = timeout
        self._runner = runner

    def xǁOsvScannerScaǁ__init____mutmut_11(
        self,
        repo_root: Path | None = None,
        *,
        scanner_version: str | None,
        lockfiles: Sequence[str] = (),
        required: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
        runner: Runner | None = None,
    ) -> None:
        self.active = scanner_version is not None
        if scanner_version is not None and not re.fullmatch(r"XX\d+\.\d+\.\d+XX", scanner_version):
            raise ValueError("scanner_version must be an exact x.y.z pin")
        if self.active and required and not lockfiles:
            raise ValueError("required OSV scanning must declare at least one lockfile")
        self.repo_root = (repo_root or REPO_ROOT).resolve()
        self.scanner_version = scanner_version or ""
        self.lockfiles = tuple(lockfiles)
        self.required = required
        self.timeout = timeout
        self._runner = runner

    def xǁOsvScannerScaǁ__init____mutmut_12(
        self,
        repo_root: Path | None = None,
        *,
        scanner_version: str | None,
        lockfiles: Sequence[str] = (),
        required: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
        runner: Runner | None = None,
    ) -> None:
        self.active = scanner_version is not None
        if scanner_version is not None and not re.fullmatch(r"\d+\.\d+\.\d+", scanner_version):
            raise ValueError(None)
        if self.active and required and not lockfiles:
            raise ValueError("required OSV scanning must declare at least one lockfile")
        self.repo_root = (repo_root or REPO_ROOT).resolve()
        self.scanner_version = scanner_version or ""
        self.lockfiles = tuple(lockfiles)
        self.required = required
        self.timeout = timeout
        self._runner = runner

    def xǁOsvScannerScaǁ__init____mutmut_13(
        self,
        repo_root: Path | None = None,
        *,
        scanner_version: str | None,
        lockfiles: Sequence[str] = (),
        required: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
        runner: Runner | None = None,
    ) -> None:
        self.active = scanner_version is not None
        if scanner_version is not None and not re.fullmatch(r"\d+\.\d+\.\d+", scanner_version):
            raise ValueError("XXscanner_version must be an exact x.y.z pinXX")
        if self.active and required and not lockfiles:
            raise ValueError("required OSV scanning must declare at least one lockfile")
        self.repo_root = (repo_root or REPO_ROOT).resolve()
        self.scanner_version = scanner_version or ""
        self.lockfiles = tuple(lockfiles)
        self.required = required
        self.timeout = timeout
        self._runner = runner

    def xǁOsvScannerScaǁ__init____mutmut_14(
        self,
        repo_root: Path | None = None,
        *,
        scanner_version: str | None,
        lockfiles: Sequence[str] = (),
        required: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
        runner: Runner | None = None,
    ) -> None:
        self.active = scanner_version is not None
        if scanner_version is not None and not re.fullmatch(r"\d+\.\d+\.\d+", scanner_version):
            raise ValueError("SCANNER_VERSION MUST BE AN EXACT X.Y.Z PIN")
        if self.active and required and not lockfiles:
            raise ValueError("required OSV scanning must declare at least one lockfile")
        self.repo_root = (repo_root or REPO_ROOT).resolve()
        self.scanner_version = scanner_version or ""
        self.lockfiles = tuple(lockfiles)
        self.required = required
        self.timeout = timeout
        self._runner = runner

    def xǁOsvScannerScaǁ__init____mutmut_15(
        self,
        repo_root: Path | None = None,
        *,
        scanner_version: str | None,
        lockfiles: Sequence[str] = (),
        required: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
        runner: Runner | None = None,
    ) -> None:
        self.active = scanner_version is not None
        if scanner_version is not None and not re.fullmatch(r"\d+\.\d+\.\d+", scanner_version):
            raise ValueError("scanner_version must be an exact x.y.z pin")
        if self.active and required or not lockfiles:
            raise ValueError("required OSV scanning must declare at least one lockfile")
        self.repo_root = (repo_root or REPO_ROOT).resolve()
        self.scanner_version = scanner_version or ""
        self.lockfiles = tuple(lockfiles)
        self.required = required
        self.timeout = timeout
        self._runner = runner

    def xǁOsvScannerScaǁ__init____mutmut_16(
        self,
        repo_root: Path | None = None,
        *,
        scanner_version: str | None,
        lockfiles: Sequence[str] = (),
        required: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
        runner: Runner | None = None,
    ) -> None:
        self.active = scanner_version is not None
        if scanner_version is not None and not re.fullmatch(r"\d+\.\d+\.\d+", scanner_version):
            raise ValueError("scanner_version must be an exact x.y.z pin")
        if self.active or required and not lockfiles:
            raise ValueError("required OSV scanning must declare at least one lockfile")
        self.repo_root = (repo_root or REPO_ROOT).resolve()
        self.scanner_version = scanner_version or ""
        self.lockfiles = tuple(lockfiles)
        self.required = required
        self.timeout = timeout
        self._runner = runner

    def xǁOsvScannerScaǁ__init____mutmut_17(
        self,
        repo_root: Path | None = None,
        *,
        scanner_version: str | None,
        lockfiles: Sequence[str] = (),
        required: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
        runner: Runner | None = None,
    ) -> None:
        self.active = scanner_version is not None
        if scanner_version is not None and not re.fullmatch(r"\d+\.\d+\.\d+", scanner_version):
            raise ValueError("scanner_version must be an exact x.y.z pin")
        if self.active and required and lockfiles:
            raise ValueError("required OSV scanning must declare at least one lockfile")
        self.repo_root = (repo_root or REPO_ROOT).resolve()
        self.scanner_version = scanner_version or ""
        self.lockfiles = tuple(lockfiles)
        self.required = required
        self.timeout = timeout
        self._runner = runner

    def xǁOsvScannerScaǁ__init____mutmut_18(
        self,
        repo_root: Path | None = None,
        *,
        scanner_version: str | None,
        lockfiles: Sequence[str] = (),
        required: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
        runner: Runner | None = None,
    ) -> None:
        self.active = scanner_version is not None
        if scanner_version is not None and not re.fullmatch(r"\d+\.\d+\.\d+", scanner_version):
            raise ValueError("scanner_version must be an exact x.y.z pin")
        if self.active and required and not lockfiles:
            raise ValueError(None)
        self.repo_root = (repo_root or REPO_ROOT).resolve()
        self.scanner_version = scanner_version or ""
        self.lockfiles = tuple(lockfiles)
        self.required = required
        self.timeout = timeout
        self._runner = runner

    def xǁOsvScannerScaǁ__init____mutmut_19(
        self,
        repo_root: Path | None = None,
        *,
        scanner_version: str | None,
        lockfiles: Sequence[str] = (),
        required: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
        runner: Runner | None = None,
    ) -> None:
        self.active = scanner_version is not None
        if scanner_version is not None and not re.fullmatch(r"\d+\.\d+\.\d+", scanner_version):
            raise ValueError("scanner_version must be an exact x.y.z pin")
        if self.active and required and not lockfiles:
            raise ValueError("XXrequired OSV scanning must declare at least one lockfileXX")
        self.repo_root = (repo_root or REPO_ROOT).resolve()
        self.scanner_version = scanner_version or ""
        self.lockfiles = tuple(lockfiles)
        self.required = required
        self.timeout = timeout
        self._runner = runner

    def xǁOsvScannerScaǁ__init____mutmut_20(
        self,
        repo_root: Path | None = None,
        *,
        scanner_version: str | None,
        lockfiles: Sequence[str] = (),
        required: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
        runner: Runner | None = None,
    ) -> None:
        self.active = scanner_version is not None
        if scanner_version is not None and not re.fullmatch(r"\d+\.\d+\.\d+", scanner_version):
            raise ValueError("scanner_version must be an exact x.y.z pin")
        if self.active and required and not lockfiles:
            raise ValueError("required osv scanning must declare at least one lockfile")
        self.repo_root = (repo_root or REPO_ROOT).resolve()
        self.scanner_version = scanner_version or ""
        self.lockfiles = tuple(lockfiles)
        self.required = required
        self.timeout = timeout
        self._runner = runner

    def xǁOsvScannerScaǁ__init____mutmut_21(
        self,
        repo_root: Path | None = None,
        *,
        scanner_version: str | None,
        lockfiles: Sequence[str] = (),
        required: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
        runner: Runner | None = None,
    ) -> None:
        self.active = scanner_version is not None
        if scanner_version is not None and not re.fullmatch(r"\d+\.\d+\.\d+", scanner_version):
            raise ValueError("scanner_version must be an exact x.y.z pin")
        if self.active and required and not lockfiles:
            raise ValueError("REQUIRED OSV SCANNING MUST DECLARE AT LEAST ONE LOCKFILE")
        self.repo_root = (repo_root or REPO_ROOT).resolve()
        self.scanner_version = scanner_version or ""
        self.lockfiles = tuple(lockfiles)
        self.required = required
        self.timeout = timeout
        self._runner = runner

    def xǁOsvScannerScaǁ__init____mutmut_22(
        self,
        repo_root: Path | None = None,
        *,
        scanner_version: str | None,
        lockfiles: Sequence[str] = (),
        required: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
        runner: Runner | None = None,
    ) -> None:
        self.active = scanner_version is not None
        if scanner_version is not None and not re.fullmatch(r"\d+\.\d+\.\d+", scanner_version):
            raise ValueError("scanner_version must be an exact x.y.z pin")
        if self.active and required and not lockfiles:
            raise ValueError("required OSV scanning must declare at least one lockfile")
        self.repo_root = None
        self.scanner_version = scanner_version or ""
        self.lockfiles = tuple(lockfiles)
        self.required = required
        self.timeout = timeout
        self._runner = runner

    def xǁOsvScannerScaǁ__init____mutmut_23(
        self,
        repo_root: Path | None = None,
        *,
        scanner_version: str | None,
        lockfiles: Sequence[str] = (),
        required: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
        runner: Runner | None = None,
    ) -> None:
        self.active = scanner_version is not None
        if scanner_version is not None and not re.fullmatch(r"\d+\.\d+\.\d+", scanner_version):
            raise ValueError("scanner_version must be an exact x.y.z pin")
        if self.active and required and not lockfiles:
            raise ValueError("required OSV scanning must declare at least one lockfile")
        self.repo_root = (repo_root and REPO_ROOT).resolve()
        self.scanner_version = scanner_version or ""
        self.lockfiles = tuple(lockfiles)
        self.required = required
        self.timeout = timeout
        self._runner = runner

    def xǁOsvScannerScaǁ__init____mutmut_24(
        self,
        repo_root: Path | None = None,
        *,
        scanner_version: str | None,
        lockfiles: Sequence[str] = (),
        required: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
        runner: Runner | None = None,
    ) -> None:
        self.active = scanner_version is not None
        if scanner_version is not None and not re.fullmatch(r"\d+\.\d+\.\d+", scanner_version):
            raise ValueError("scanner_version must be an exact x.y.z pin")
        if self.active and required and not lockfiles:
            raise ValueError("required OSV scanning must declare at least one lockfile")
        self.repo_root = (repo_root or REPO_ROOT).resolve()
        self.scanner_version = None
        self.lockfiles = tuple(lockfiles)
        self.required = required
        self.timeout = timeout
        self._runner = runner

    def xǁOsvScannerScaǁ__init____mutmut_25(
        self,
        repo_root: Path | None = None,
        *,
        scanner_version: str | None,
        lockfiles: Sequence[str] = (),
        required: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
        runner: Runner | None = None,
    ) -> None:
        self.active = scanner_version is not None
        if scanner_version is not None and not re.fullmatch(r"\d+\.\d+\.\d+", scanner_version):
            raise ValueError("scanner_version must be an exact x.y.z pin")
        if self.active and required and not lockfiles:
            raise ValueError("required OSV scanning must declare at least one lockfile")
        self.repo_root = (repo_root or REPO_ROOT).resolve()
        self.scanner_version = scanner_version and ""
        self.lockfiles = tuple(lockfiles)
        self.required = required
        self.timeout = timeout
        self._runner = runner

    def xǁOsvScannerScaǁ__init____mutmut_26(
        self,
        repo_root: Path | None = None,
        *,
        scanner_version: str | None,
        lockfiles: Sequence[str] = (),
        required: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
        runner: Runner | None = None,
    ) -> None:
        self.active = scanner_version is not None
        if scanner_version is not None and not re.fullmatch(r"\d+\.\d+\.\d+", scanner_version):
            raise ValueError("scanner_version must be an exact x.y.z pin")
        if self.active and required and not lockfiles:
            raise ValueError("required OSV scanning must declare at least one lockfile")
        self.repo_root = (repo_root or REPO_ROOT).resolve()
        self.scanner_version = scanner_version or "XXXX"
        self.lockfiles = tuple(lockfiles)
        self.required = required
        self.timeout = timeout
        self._runner = runner

    def xǁOsvScannerScaǁ__init____mutmut_27(
        self,
        repo_root: Path | None = None,
        *,
        scanner_version: str | None,
        lockfiles: Sequence[str] = (),
        required: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
        runner: Runner | None = None,
    ) -> None:
        self.active = scanner_version is not None
        if scanner_version is not None and not re.fullmatch(r"\d+\.\d+\.\d+", scanner_version):
            raise ValueError("scanner_version must be an exact x.y.z pin")
        if self.active and required and not lockfiles:
            raise ValueError("required OSV scanning must declare at least one lockfile")
        self.repo_root = (repo_root or REPO_ROOT).resolve()
        self.scanner_version = scanner_version or ""
        self.lockfiles = None
        self.required = required
        self.timeout = timeout
        self._runner = runner

    def xǁOsvScannerScaǁ__init____mutmut_28(
        self,
        repo_root: Path | None = None,
        *,
        scanner_version: str | None,
        lockfiles: Sequence[str] = (),
        required: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
        runner: Runner | None = None,
    ) -> None:
        self.active = scanner_version is not None
        if scanner_version is not None and not re.fullmatch(r"\d+\.\d+\.\d+", scanner_version):
            raise ValueError("scanner_version must be an exact x.y.z pin")
        if self.active and required and not lockfiles:
            raise ValueError("required OSV scanning must declare at least one lockfile")
        self.repo_root = (repo_root or REPO_ROOT).resolve()
        self.scanner_version = scanner_version or ""
        self.lockfiles = tuple(None)
        self.required = required
        self.timeout = timeout
        self._runner = runner

    def xǁOsvScannerScaǁ__init____mutmut_29(
        self,
        repo_root: Path | None = None,
        *,
        scanner_version: str | None,
        lockfiles: Sequence[str] = (),
        required: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
        runner: Runner | None = None,
    ) -> None:
        self.active = scanner_version is not None
        if scanner_version is not None and not re.fullmatch(r"\d+\.\d+\.\d+", scanner_version):
            raise ValueError("scanner_version must be an exact x.y.z pin")
        if self.active and required and not lockfiles:
            raise ValueError("required OSV scanning must declare at least one lockfile")
        self.repo_root = (repo_root or REPO_ROOT).resolve()
        self.scanner_version = scanner_version or ""
        self.lockfiles = tuple(lockfiles)
        self.required = None
        self.timeout = timeout
        self._runner = runner

    def xǁOsvScannerScaǁ__init____mutmut_30(
        self,
        repo_root: Path | None = None,
        *,
        scanner_version: str | None,
        lockfiles: Sequence[str] = (),
        required: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
        runner: Runner | None = None,
    ) -> None:
        self.active = scanner_version is not None
        if scanner_version is not None and not re.fullmatch(r"\d+\.\d+\.\d+", scanner_version):
            raise ValueError("scanner_version must be an exact x.y.z pin")
        if self.active and required and not lockfiles:
            raise ValueError("required OSV scanning must declare at least one lockfile")
        self.repo_root = (repo_root or REPO_ROOT).resolve()
        self.scanner_version = scanner_version or ""
        self.lockfiles = tuple(lockfiles)
        self.required = required
        self.timeout = None
        self._runner = runner

    def xǁOsvScannerScaǁ__init____mutmut_31(
        self,
        repo_root: Path | None = None,
        *,
        scanner_version: str | None,
        lockfiles: Sequence[str] = (),
        required: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
        runner: Runner | None = None,
    ) -> None:
        self.active = scanner_version is not None
        if scanner_version is not None and not re.fullmatch(r"\d+\.\d+\.\d+", scanner_version):
            raise ValueError("scanner_version must be an exact x.y.z pin")
        if self.active and required and not lockfiles:
            raise ValueError("required OSV scanning must declare at least one lockfile")
        self.repo_root = (repo_root or REPO_ROOT).resolve()
        self.scanner_version = scanner_version or ""
        self.lockfiles = tuple(lockfiles)
        self.required = required
        self.timeout = timeout
        self._runner = None

    @classmethod
    @_mutmut_mutated(mutants_xǁOsvScannerScaǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", "")),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            required=bool(config.get("required", True)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", "")),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            required=bool(config.get("required", True)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", "")),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            required=bool(config.get("required", True)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(None, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", "")),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            required=bool(config.get("required", True)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=None)
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", "")),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            required=bool(config.get("required", True)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", "")),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            required=bool(config.get("required", True)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", "")),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            required=bool(config.get("required", True)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, )
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", "")),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            required=bool(config.get("required", True)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=True)
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", "")),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            required=bool(config.get("required", True)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            None,
            scanner_version=str(config.get("scanner_version", "")),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            required=bool(config.get("required", True)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=None,
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            required=bool(config.get("required", True)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", "")),
            lockfiles=None,
            required=bool(config.get("required", True)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", "")),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            required=None,
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", "")),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            required=bool(config.get("required", True)),
            timeout=None,
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_13(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            scanner_version=str(config.get("scanner_version", "")),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            required=bool(config.get("required", True)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_14(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            required=bool(config.get("required", True)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_15(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", "")),
            required=bool(config.get("required", True)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_16(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", "")),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_17(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", "")),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            required=bool(config.get("required", True)),
            )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_18(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(None),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            required=bool(config.get("required", True)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_19(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get(None, "")),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            required=bool(config.get("required", True)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_20(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", None)),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            required=bool(config.get("required", True)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_21(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("")),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            required=bool(config.get("required", True)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_22(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", )),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            required=bool(config.get("required", True)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_23(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("XXscanner_versionXX", "")),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            required=bool(config.get("required", True)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_24(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("SCANNER_VERSION", "")),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            required=bool(config.get("required", True)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_25(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", "XXXX")),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            required=bool(config.get("required", True)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_26(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", "")),
            lockfiles=tuple(None),
            required=bool(config.get("required", True)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_27(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", "")),
            lockfiles=tuple(str(None) for value in config.get("lockfiles", ())),
            required=bool(config.get("required", True)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_28(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", "")),
            lockfiles=tuple(str(value) for value in config.get(None, ())),
            required=bool(config.get("required", True)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_29(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", "")),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", None)),
            required=bool(config.get("required", True)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_30(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", "")),
            lockfiles=tuple(str(value) for value in config.get(())),
            required=bool(config.get("required", True)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_31(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", "")),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", )),
            required=bool(config.get("required", True)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_32(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", "")),
            lockfiles=tuple(str(value) for value in config.get("XXlockfilesXX", ())),
            required=bool(config.get("required", True)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_33(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", "")),
            lockfiles=tuple(str(value) for value in config.get("LOCKFILES", ())),
            required=bool(config.get("required", True)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_34(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", "")),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            required=bool(None),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_35(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", "")),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            required=bool(config.get(None, True)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_36(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", "")),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            required=bool(config.get("required", None)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_37(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", "")),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            required=bool(config.get(True)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_38(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", "")),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            required=bool(config.get("required", )),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_39(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", "")),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            required=bool(config.get("XXrequiredXX", True)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_40(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", "")),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            required=bool(config.get("REQUIRED", True)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_41(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", "")),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            required=bool(config.get("required", False)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_42(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", "")),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            required=bool(config.get("required", True)),
            timeout=int(None),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_43(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", "")),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            required=bool(config.get("required", True)),
            timeout=int(config.get(None, DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_44(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", "")),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            required=bool(config.get("required", True)),
            timeout=int(config.get("timeout", None)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_45(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", "")),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            required=bool(config.get("required", True)),
            timeout=int(config.get(DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_46(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", "")),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            required=bool(config.get("required", True)),
            timeout=int(config.get("timeout", )),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_47(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", "")),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            required=bool(config.get("required", True)),
            timeout=int(config.get("XXtimeoutXX", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁOsvScannerScaǁfrom_config__mutmut_48(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        if not config:
            return cls(repo_root, scanner_version=None, required=False)
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", "")),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            required=bool(config.get("required", True)),
            timeout=int(config.get("TIMEOUT", DEFAULT_TIMEOUT)),
        )

    @_mutmut_mutated(mutants_xǁOsvScannerScaǁ_execute__mutmut)
    def _execute(self) -> ScanExecution:
        if self._runner is not None:
            return self._runner(self.repo_root, self.lockfiles, self.scanner_version)
        return execute_scan(
            self.repo_root,
            self.lockfiles,
            self.scanner_version,
            timeout=self.timeout,
        )

    def xǁOsvScannerScaǁ_execute__mutmut_orig(self) -> ScanExecution:
        if self._runner is not None:
            return self._runner(self.repo_root, self.lockfiles, self.scanner_version)
        return execute_scan(
            self.repo_root,
            self.lockfiles,
            self.scanner_version,
            timeout=self.timeout,
        )

    def xǁOsvScannerScaǁ_execute__mutmut_1(self) -> ScanExecution:
        if self._runner is None:
            return self._runner(self.repo_root, self.lockfiles, self.scanner_version)
        return execute_scan(
            self.repo_root,
            self.lockfiles,
            self.scanner_version,
            timeout=self.timeout,
        )

    def xǁOsvScannerScaǁ_execute__mutmut_2(self) -> ScanExecution:
        if self._runner is not None:
            return self._runner(None, self.lockfiles, self.scanner_version)
        return execute_scan(
            self.repo_root,
            self.lockfiles,
            self.scanner_version,
            timeout=self.timeout,
        )

    def xǁOsvScannerScaǁ_execute__mutmut_3(self) -> ScanExecution:
        if self._runner is not None:
            return self._runner(self.repo_root, None, self.scanner_version)
        return execute_scan(
            self.repo_root,
            self.lockfiles,
            self.scanner_version,
            timeout=self.timeout,
        )

    def xǁOsvScannerScaǁ_execute__mutmut_4(self) -> ScanExecution:
        if self._runner is not None:
            return self._runner(self.repo_root, self.lockfiles, None)
        return execute_scan(
            self.repo_root,
            self.lockfiles,
            self.scanner_version,
            timeout=self.timeout,
        )

    def xǁOsvScannerScaǁ_execute__mutmut_5(self) -> ScanExecution:
        if self._runner is not None:
            return self._runner(self.lockfiles, self.scanner_version)
        return execute_scan(
            self.repo_root,
            self.lockfiles,
            self.scanner_version,
            timeout=self.timeout,
        )

    def xǁOsvScannerScaǁ_execute__mutmut_6(self) -> ScanExecution:
        if self._runner is not None:
            return self._runner(self.repo_root, self.scanner_version)
        return execute_scan(
            self.repo_root,
            self.lockfiles,
            self.scanner_version,
            timeout=self.timeout,
        )

    def xǁOsvScannerScaǁ_execute__mutmut_7(self) -> ScanExecution:
        if self._runner is not None:
            return self._runner(self.repo_root, self.lockfiles, )
        return execute_scan(
            self.repo_root,
            self.lockfiles,
            self.scanner_version,
            timeout=self.timeout,
        )

    def xǁOsvScannerScaǁ_execute__mutmut_8(self) -> ScanExecution:
        if self._runner is not None:
            return self._runner(self.repo_root, self.lockfiles, self.scanner_version)
        return execute_scan(
            None,
            self.lockfiles,
            self.scanner_version,
            timeout=self.timeout,
        )

    def xǁOsvScannerScaǁ_execute__mutmut_9(self) -> ScanExecution:
        if self._runner is not None:
            return self._runner(self.repo_root, self.lockfiles, self.scanner_version)
        return execute_scan(
            self.repo_root,
            None,
            self.scanner_version,
            timeout=self.timeout,
        )

    def xǁOsvScannerScaǁ_execute__mutmut_10(self) -> ScanExecution:
        if self._runner is not None:
            return self._runner(self.repo_root, self.lockfiles, self.scanner_version)
        return execute_scan(
            self.repo_root,
            self.lockfiles,
            None,
            timeout=self.timeout,
        )

    def xǁOsvScannerScaǁ_execute__mutmut_11(self) -> ScanExecution:
        if self._runner is not None:
            return self._runner(self.repo_root, self.lockfiles, self.scanner_version)
        return execute_scan(
            self.repo_root,
            self.lockfiles,
            self.scanner_version,
            timeout=None,
        )

    def xǁOsvScannerScaǁ_execute__mutmut_12(self) -> ScanExecution:
        if self._runner is not None:
            return self._runner(self.repo_root, self.lockfiles, self.scanner_version)
        return execute_scan(
            self.lockfiles,
            self.scanner_version,
            timeout=self.timeout,
        )

    def xǁOsvScannerScaǁ_execute__mutmut_13(self) -> ScanExecution:
        if self._runner is not None:
            return self._runner(self.repo_root, self.lockfiles, self.scanner_version)
        return execute_scan(
            self.repo_root,
            self.scanner_version,
            timeout=self.timeout,
        )

    def xǁOsvScannerScaǁ_execute__mutmut_14(self) -> ScanExecution:
        if self._runner is not None:
            return self._runner(self.repo_root, self.lockfiles, self.scanner_version)
        return execute_scan(
            self.repo_root,
            self.lockfiles,
            timeout=self.timeout,
        )

    def xǁOsvScannerScaǁ_execute__mutmut_15(self) -> ScanExecution:
        if self._runner is not None:
            return self._runner(self.repo_root, self.lockfiles, self.scanner_version)
        return execute_scan(
            self.repo_root,
            self.lockfiles,
            self.scanner_version,
            )

    @_mutmut_mutated(mutants_xǁOsvScannerScaǁevaluate__mutmut)
    def evaluate(self) -> tuple[bool, list[str], ScanExecution]:
        if not self.active:
            return True, [], ScanExecution(ScanStatus.EXECUTED, report={"results": []}, detail="unconfigured")
        execution = self._execute()
        if execution.status is not ScanStatus.EXECUTED or execution.report is None:
            return False, [], execution
        report_error = _report_error(execution.report)
        if report_error is not None:
            return (
                False,
                [],
                ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}"),
            )
        findings = vulnerability_ids(execution.report)
        return not findings, findings, execution

    def xǁOsvScannerScaǁevaluate__mutmut_orig(self) -> tuple[bool, list[str], ScanExecution]:
        if not self.active:
            return True, [], ScanExecution(ScanStatus.EXECUTED, report={"results": []}, detail="unconfigured")
        execution = self._execute()
        if execution.status is not ScanStatus.EXECUTED or execution.report is None:
            return False, [], execution
        report_error = _report_error(execution.report)
        if report_error is not None:
            return (
                False,
                [],
                ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}"),
            )
        findings = vulnerability_ids(execution.report)
        return not findings, findings, execution

    def xǁOsvScannerScaǁevaluate__mutmut_1(self) -> tuple[bool, list[str], ScanExecution]:
        if self.active:
            return True, [], ScanExecution(ScanStatus.EXECUTED, report={"results": []}, detail="unconfigured")
        execution = self._execute()
        if execution.status is not ScanStatus.EXECUTED or execution.report is None:
            return False, [], execution
        report_error = _report_error(execution.report)
        if report_error is not None:
            return (
                False,
                [],
                ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}"),
            )
        findings = vulnerability_ids(execution.report)
        return not findings, findings, execution

    def xǁOsvScannerScaǁevaluate__mutmut_2(self) -> tuple[bool, list[str], ScanExecution]:
        if not self.active:
            return False, [], ScanExecution(ScanStatus.EXECUTED, report={"results": []}, detail="unconfigured")
        execution = self._execute()
        if execution.status is not ScanStatus.EXECUTED or execution.report is None:
            return False, [], execution
        report_error = _report_error(execution.report)
        if report_error is not None:
            return (
                False,
                [],
                ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}"),
            )
        findings = vulnerability_ids(execution.report)
        return not findings, findings, execution

    def xǁOsvScannerScaǁevaluate__mutmut_3(self) -> tuple[bool, list[str], ScanExecution]:
        if not self.active:
            return True, [], ScanExecution(None, report={"results": []}, detail="unconfigured")
        execution = self._execute()
        if execution.status is not ScanStatus.EXECUTED or execution.report is None:
            return False, [], execution
        report_error = _report_error(execution.report)
        if report_error is not None:
            return (
                False,
                [],
                ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}"),
            )
        findings = vulnerability_ids(execution.report)
        return not findings, findings, execution

    def xǁOsvScannerScaǁevaluate__mutmut_4(self) -> tuple[bool, list[str], ScanExecution]:
        if not self.active:
            return True, [], ScanExecution(ScanStatus.EXECUTED, report=None, detail="unconfigured")
        execution = self._execute()
        if execution.status is not ScanStatus.EXECUTED or execution.report is None:
            return False, [], execution
        report_error = _report_error(execution.report)
        if report_error is not None:
            return (
                False,
                [],
                ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}"),
            )
        findings = vulnerability_ids(execution.report)
        return not findings, findings, execution

    def xǁOsvScannerScaǁevaluate__mutmut_5(self) -> tuple[bool, list[str], ScanExecution]:
        if not self.active:
            return True, [], ScanExecution(ScanStatus.EXECUTED, report={"results": []}, detail=None)
        execution = self._execute()
        if execution.status is not ScanStatus.EXECUTED or execution.report is None:
            return False, [], execution
        report_error = _report_error(execution.report)
        if report_error is not None:
            return (
                False,
                [],
                ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}"),
            )
        findings = vulnerability_ids(execution.report)
        return not findings, findings, execution

    def xǁOsvScannerScaǁevaluate__mutmut_6(self) -> tuple[bool, list[str], ScanExecution]:
        if not self.active:
            return True, [], ScanExecution(report={"results": []}, detail="unconfigured")
        execution = self._execute()
        if execution.status is not ScanStatus.EXECUTED or execution.report is None:
            return False, [], execution
        report_error = _report_error(execution.report)
        if report_error is not None:
            return (
                False,
                [],
                ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}"),
            )
        findings = vulnerability_ids(execution.report)
        return not findings, findings, execution

    def xǁOsvScannerScaǁevaluate__mutmut_7(self) -> tuple[bool, list[str], ScanExecution]:
        if not self.active:
            return True, [], ScanExecution(ScanStatus.EXECUTED, detail="unconfigured")
        execution = self._execute()
        if execution.status is not ScanStatus.EXECUTED or execution.report is None:
            return False, [], execution
        report_error = _report_error(execution.report)
        if report_error is not None:
            return (
                False,
                [],
                ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}"),
            )
        findings = vulnerability_ids(execution.report)
        return not findings, findings, execution

    def xǁOsvScannerScaǁevaluate__mutmut_8(self) -> tuple[bool, list[str], ScanExecution]:
        if not self.active:
            return True, [], ScanExecution(ScanStatus.EXECUTED, report={"results": []}, )
        execution = self._execute()
        if execution.status is not ScanStatus.EXECUTED or execution.report is None:
            return False, [], execution
        report_error = _report_error(execution.report)
        if report_error is not None:
            return (
                False,
                [],
                ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}"),
            )
        findings = vulnerability_ids(execution.report)
        return not findings, findings, execution

    def xǁOsvScannerScaǁevaluate__mutmut_9(self) -> tuple[bool, list[str], ScanExecution]:
        if not self.active:
            return True, [], ScanExecution(ScanStatus.EXECUTED, report={"XXresultsXX": []}, detail="unconfigured")
        execution = self._execute()
        if execution.status is not ScanStatus.EXECUTED or execution.report is None:
            return False, [], execution
        report_error = _report_error(execution.report)
        if report_error is not None:
            return (
                False,
                [],
                ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}"),
            )
        findings = vulnerability_ids(execution.report)
        return not findings, findings, execution

    def xǁOsvScannerScaǁevaluate__mutmut_10(self) -> tuple[bool, list[str], ScanExecution]:
        if not self.active:
            return True, [], ScanExecution(ScanStatus.EXECUTED, report={"RESULTS": []}, detail="unconfigured")
        execution = self._execute()
        if execution.status is not ScanStatus.EXECUTED or execution.report is None:
            return False, [], execution
        report_error = _report_error(execution.report)
        if report_error is not None:
            return (
                False,
                [],
                ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}"),
            )
        findings = vulnerability_ids(execution.report)
        return not findings, findings, execution

    def xǁOsvScannerScaǁevaluate__mutmut_11(self) -> tuple[bool, list[str], ScanExecution]:
        if not self.active:
            return True, [], ScanExecution(ScanStatus.EXECUTED, report={"results": []}, detail="XXunconfiguredXX")
        execution = self._execute()
        if execution.status is not ScanStatus.EXECUTED or execution.report is None:
            return False, [], execution
        report_error = _report_error(execution.report)
        if report_error is not None:
            return (
                False,
                [],
                ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}"),
            )
        findings = vulnerability_ids(execution.report)
        return not findings, findings, execution

    def xǁOsvScannerScaǁevaluate__mutmut_12(self) -> tuple[bool, list[str], ScanExecution]:
        if not self.active:
            return True, [], ScanExecution(ScanStatus.EXECUTED, report={"results": []}, detail="UNCONFIGURED")
        execution = self._execute()
        if execution.status is not ScanStatus.EXECUTED or execution.report is None:
            return False, [], execution
        report_error = _report_error(execution.report)
        if report_error is not None:
            return (
                False,
                [],
                ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}"),
            )
        findings = vulnerability_ids(execution.report)
        return not findings, findings, execution

    def xǁOsvScannerScaǁevaluate__mutmut_13(self) -> tuple[bool, list[str], ScanExecution]:
        if not self.active:
            return True, [], ScanExecution(ScanStatus.EXECUTED, report={"results": []}, detail="unconfigured")
        execution = None
        if execution.status is not ScanStatus.EXECUTED or execution.report is None:
            return False, [], execution
        report_error = _report_error(execution.report)
        if report_error is not None:
            return (
                False,
                [],
                ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}"),
            )
        findings = vulnerability_ids(execution.report)
        return not findings, findings, execution

    def xǁOsvScannerScaǁevaluate__mutmut_14(self) -> tuple[bool, list[str], ScanExecution]:
        if not self.active:
            return True, [], ScanExecution(ScanStatus.EXECUTED, report={"results": []}, detail="unconfigured")
        execution = self._execute()
        if execution.status is not ScanStatus.EXECUTED and execution.report is None:
            return False, [], execution
        report_error = _report_error(execution.report)
        if report_error is not None:
            return (
                False,
                [],
                ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}"),
            )
        findings = vulnerability_ids(execution.report)
        return not findings, findings, execution

    def xǁOsvScannerScaǁevaluate__mutmut_15(self) -> tuple[bool, list[str], ScanExecution]:
        if not self.active:
            return True, [], ScanExecution(ScanStatus.EXECUTED, report={"results": []}, detail="unconfigured")
        execution = self._execute()
        if execution.status is ScanStatus.EXECUTED or execution.report is None:
            return False, [], execution
        report_error = _report_error(execution.report)
        if report_error is not None:
            return (
                False,
                [],
                ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}"),
            )
        findings = vulnerability_ids(execution.report)
        return not findings, findings, execution

    def xǁOsvScannerScaǁevaluate__mutmut_16(self) -> tuple[bool, list[str], ScanExecution]:
        if not self.active:
            return True, [], ScanExecution(ScanStatus.EXECUTED, report={"results": []}, detail="unconfigured")
        execution = self._execute()
        if execution.status is not ScanStatus.EXECUTED or execution.report is not None:
            return False, [], execution
        report_error = _report_error(execution.report)
        if report_error is not None:
            return (
                False,
                [],
                ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}"),
            )
        findings = vulnerability_ids(execution.report)
        return not findings, findings, execution

    def xǁOsvScannerScaǁevaluate__mutmut_17(self) -> tuple[bool, list[str], ScanExecution]:
        if not self.active:
            return True, [], ScanExecution(ScanStatus.EXECUTED, report={"results": []}, detail="unconfigured")
        execution = self._execute()
        if execution.status is not ScanStatus.EXECUTED or execution.report is None:
            return True, [], execution
        report_error = _report_error(execution.report)
        if report_error is not None:
            return (
                False,
                [],
                ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}"),
            )
        findings = vulnerability_ids(execution.report)
        return not findings, findings, execution

    def xǁOsvScannerScaǁevaluate__mutmut_18(self) -> tuple[bool, list[str], ScanExecution]:
        if not self.active:
            return True, [], ScanExecution(ScanStatus.EXECUTED, report={"results": []}, detail="unconfigured")
        execution = self._execute()
        if execution.status is not ScanStatus.EXECUTED or execution.report is None:
            return False, [], execution
        report_error = None
        if report_error is not None:
            return (
                False,
                [],
                ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}"),
            )
        findings = vulnerability_ids(execution.report)
        return not findings, findings, execution

    def xǁOsvScannerScaǁevaluate__mutmut_19(self) -> tuple[bool, list[str], ScanExecution]:
        if not self.active:
            return True, [], ScanExecution(ScanStatus.EXECUTED, report={"results": []}, detail="unconfigured")
        execution = self._execute()
        if execution.status is not ScanStatus.EXECUTED or execution.report is None:
            return False, [], execution
        report_error = _report_error(None)
        if report_error is not None:
            return (
                False,
                [],
                ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}"),
            )
        findings = vulnerability_ids(execution.report)
        return not findings, findings, execution

    def xǁOsvScannerScaǁevaluate__mutmut_20(self) -> tuple[bool, list[str], ScanExecution]:
        if not self.active:
            return True, [], ScanExecution(ScanStatus.EXECUTED, report={"results": []}, detail="unconfigured")
        execution = self._execute()
        if execution.status is not ScanStatus.EXECUTED or execution.report is None:
            return False, [], execution
        report_error = _report_error(execution.report)
        if report_error is None:
            return (
                False,
                [],
                ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}"),
            )
        findings = vulnerability_ids(execution.report)
        return not findings, findings, execution

    def xǁOsvScannerScaǁevaluate__mutmut_21(self) -> tuple[bool, list[str], ScanExecution]:
        if not self.active:
            return True, [], ScanExecution(ScanStatus.EXECUTED, report={"results": []}, detail="unconfigured")
        execution = self._execute()
        if execution.status is not ScanStatus.EXECUTED or execution.report is None:
            return False, [], execution
        report_error = _report_error(execution.report)
        if report_error is not None:
            return (
                True,
                [],
                ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}"),
            )
        findings = vulnerability_ids(execution.report)
        return not findings, findings, execution

    def xǁOsvScannerScaǁevaluate__mutmut_22(self) -> tuple[bool, list[str], ScanExecution]:
        if not self.active:
            return True, [], ScanExecution(ScanStatus.EXECUTED, report={"results": []}, detail="unconfigured")
        execution = self._execute()
        if execution.status is not ScanStatus.EXECUTED or execution.report is None:
            return False, [], execution
        report_error = _report_error(execution.report)
        if report_error is not None:
            return (
                False,
                [],
                ScanExecution(None, detail=f"scan report is incomplete: {report_error}"),
            )
        findings = vulnerability_ids(execution.report)
        return not findings, findings, execution

    def xǁOsvScannerScaǁevaluate__mutmut_23(self) -> tuple[bool, list[str], ScanExecution]:
        if not self.active:
            return True, [], ScanExecution(ScanStatus.EXECUTED, report={"results": []}, detail="unconfigured")
        execution = self._execute()
        if execution.status is not ScanStatus.EXECUTED or execution.report is None:
            return False, [], execution
        report_error = _report_error(execution.report)
        if report_error is not None:
            return (
                False,
                [],
                ScanExecution(ScanStatus.INCOMPLETE, detail=None),
            )
        findings = vulnerability_ids(execution.report)
        return not findings, findings, execution

    def xǁOsvScannerScaǁevaluate__mutmut_24(self) -> tuple[bool, list[str], ScanExecution]:
        if not self.active:
            return True, [], ScanExecution(ScanStatus.EXECUTED, report={"results": []}, detail="unconfigured")
        execution = self._execute()
        if execution.status is not ScanStatus.EXECUTED or execution.report is None:
            return False, [], execution
        report_error = _report_error(execution.report)
        if report_error is not None:
            return (
                False,
                [],
                ScanExecution(detail=f"scan report is incomplete: {report_error}"),
            )
        findings = vulnerability_ids(execution.report)
        return not findings, findings, execution

    def xǁOsvScannerScaǁevaluate__mutmut_25(self) -> tuple[bool, list[str], ScanExecution]:
        if not self.active:
            return True, [], ScanExecution(ScanStatus.EXECUTED, report={"results": []}, detail="unconfigured")
        execution = self._execute()
        if execution.status is not ScanStatus.EXECUTED or execution.report is None:
            return False, [], execution
        report_error = _report_error(execution.report)
        if report_error is not None:
            return (
                False,
                [],
                ScanExecution(ScanStatus.INCOMPLETE, ),
            )
        findings = vulnerability_ids(execution.report)
        return not findings, findings, execution

    def xǁOsvScannerScaǁevaluate__mutmut_26(self) -> tuple[bool, list[str], ScanExecution]:
        if not self.active:
            return True, [], ScanExecution(ScanStatus.EXECUTED, report={"results": []}, detail="unconfigured")
        execution = self._execute()
        if execution.status is not ScanStatus.EXECUTED or execution.report is None:
            return False, [], execution
        report_error = _report_error(execution.report)
        if report_error is not None:
            return (
                False,
                [],
                ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}"),
            )
        findings = None
        return not findings, findings, execution

    def xǁOsvScannerScaǁevaluate__mutmut_27(self) -> tuple[bool, list[str], ScanExecution]:
        if not self.active:
            return True, [], ScanExecution(ScanStatus.EXECUTED, report={"results": []}, detail="unconfigured")
        execution = self._execute()
        if execution.status is not ScanStatus.EXECUTED or execution.report is None:
            return False, [], execution
        report_error = _report_error(execution.report)
        if report_error is not None:
            return (
                False,
                [],
                ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}"),
            )
        findings = vulnerability_ids(None)
        return not findings, findings, execution

    def xǁOsvScannerScaǁevaluate__mutmut_28(self) -> tuple[bool, list[str], ScanExecution]:
        if not self.active:
            return True, [], ScanExecution(ScanStatus.EXECUTED, report={"results": []}, detail="unconfigured")
        execution = self._execute()
        if execution.status is not ScanStatus.EXECUTED or execution.report is None:
            return False, [], execution
        report_error = _report_error(execution.report)
        if report_error is not None:
            return (
                False,
                [],
                ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}"),
            )
        findings = vulnerability_ids(execution.report)
        return findings, findings, execution

    @_mutmut_mutated(mutants_xǁOsvScannerScaǁrun__mutmut)
    def run(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_orig(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_1(self) -> int:
        if self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_2(self) -> int:
        if not self.active:
            print(None)
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_3(self) -> int:
        if not self.active:
            print("XXPASS osv_scanner_sca (unconfigured)XX")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_4(self) -> int:
        if not self.active:
            print("pass osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_5(self) -> int:
        if not self.active:
            print("PASS OSV_SCANNER_SCA (UNCONFIGURED)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_6(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 1
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_7(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = None
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_8(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_9(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                None,
                ".",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_10(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                None,
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_11(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                None,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_12(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                status=None,
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_13(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                ".",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_14(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_15(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_16(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_17(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "XXdependency-unavailableXX"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_18(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "DEPENDENCY-UNAVAILABLE"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_19(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is not ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_20(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "XXosv-scanner-errorXX",
                ".",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_21(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "OSV-SCANNER-ERROR",
                ".",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_22(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                "XX.XX",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_23(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                status="XXerrorXX",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_24(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                status="ERROR",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_25(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                status="error",
            )
            print(
                None
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_26(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "XXnext: re-run the full fitness gate; run: osv-scanner --versionXX"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_27(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "NEXT: RE-RUN THE FULL FITNESS GATE; RUN: OSV-SCANNER --VERSION"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_28(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 2
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_29(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_30(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding(None, ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_31(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", None, f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_32(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", None)
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_33(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding(".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_34(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_35(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", )
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_36(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("XXvulnerabilityXX", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_37(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("VULNERABILITY", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_38(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", "XX.XX", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_39(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                None
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_40(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(None)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_41(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{'XX, XX'.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_42(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "XXnext: refresh lockfiles and re-run the full fitness gate; XX"
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_43(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "NEXT: REFRESH LOCKFILES AND RE-RUN THE FULL FITNESS GATE; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_44(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(None)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_45(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {'XX XX'.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_46(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 2
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_47(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            None
        )
        return 0

    def xǁOsvScannerScaǁrun__mutmut_48(self) -> int:
        if not self.active:
            print("PASS osv_scanner_sca (unconfigured)")
            return 0
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            report_finding(
                "dependency-unavailable"
                if execution.status is ScanStatus.MISSING_TOOL
                else "osv-scanner-error",
                ".",
                execution.detail,
                status="error",
            )
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            for finding in findings:
                report_finding("vulnerability", ".", f"OSV advisory {finding}")
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 1

mutants_xǁOsvScannerScaǁ__init____mutmut['_mutmut_orig'] = OsvScannerSca.xǁOsvScannerScaǁ__init____mutmut_orig # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ__init____mutmut['xǁOsvScannerScaǁ__init____mutmut_1'] = OsvScannerSca.xǁOsvScannerScaǁ__init____mutmut_1 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ__init____mutmut['xǁOsvScannerScaǁ__init____mutmut_2'] = OsvScannerSca.xǁOsvScannerScaǁ__init____mutmut_2 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ__init____mutmut['xǁOsvScannerScaǁ__init____mutmut_3'] = OsvScannerSca.xǁOsvScannerScaǁ__init____mutmut_3 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ__init____mutmut['xǁOsvScannerScaǁ__init____mutmut_4'] = OsvScannerSca.xǁOsvScannerScaǁ__init____mutmut_4 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ__init____mutmut['xǁOsvScannerScaǁ__init____mutmut_5'] = OsvScannerSca.xǁOsvScannerScaǁ__init____mutmut_5 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ__init____mutmut['xǁOsvScannerScaǁ__init____mutmut_6'] = OsvScannerSca.xǁOsvScannerScaǁ__init____mutmut_6 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ__init____mutmut['xǁOsvScannerScaǁ__init____mutmut_7'] = OsvScannerSca.xǁOsvScannerScaǁ__init____mutmut_7 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ__init____mutmut['xǁOsvScannerScaǁ__init____mutmut_8'] = OsvScannerSca.xǁOsvScannerScaǁ__init____mutmut_8 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ__init____mutmut['xǁOsvScannerScaǁ__init____mutmut_9'] = OsvScannerSca.xǁOsvScannerScaǁ__init____mutmut_9 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ__init____mutmut['xǁOsvScannerScaǁ__init____mutmut_10'] = OsvScannerSca.xǁOsvScannerScaǁ__init____mutmut_10 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ__init____mutmut['xǁOsvScannerScaǁ__init____mutmut_11'] = OsvScannerSca.xǁOsvScannerScaǁ__init____mutmut_11 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ__init____mutmut['xǁOsvScannerScaǁ__init____mutmut_12'] = OsvScannerSca.xǁOsvScannerScaǁ__init____mutmut_12 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ__init____mutmut['xǁOsvScannerScaǁ__init____mutmut_13'] = OsvScannerSca.xǁOsvScannerScaǁ__init____mutmut_13 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ__init____mutmut['xǁOsvScannerScaǁ__init____mutmut_14'] = OsvScannerSca.xǁOsvScannerScaǁ__init____mutmut_14 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ__init____mutmut['xǁOsvScannerScaǁ__init____mutmut_15'] = OsvScannerSca.xǁOsvScannerScaǁ__init____mutmut_15 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ__init____mutmut['xǁOsvScannerScaǁ__init____mutmut_16'] = OsvScannerSca.xǁOsvScannerScaǁ__init____mutmut_16 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ__init____mutmut['xǁOsvScannerScaǁ__init____mutmut_17'] = OsvScannerSca.xǁOsvScannerScaǁ__init____mutmut_17 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ__init____mutmut['xǁOsvScannerScaǁ__init____mutmut_18'] = OsvScannerSca.xǁOsvScannerScaǁ__init____mutmut_18 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ__init____mutmut['xǁOsvScannerScaǁ__init____mutmut_19'] = OsvScannerSca.xǁOsvScannerScaǁ__init____mutmut_19 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ__init____mutmut['xǁOsvScannerScaǁ__init____mutmut_20'] = OsvScannerSca.xǁOsvScannerScaǁ__init____mutmut_20 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ__init____mutmut['xǁOsvScannerScaǁ__init____mutmut_21'] = OsvScannerSca.xǁOsvScannerScaǁ__init____mutmut_21 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ__init____mutmut['xǁOsvScannerScaǁ__init____mutmut_22'] = OsvScannerSca.xǁOsvScannerScaǁ__init____mutmut_22 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ__init____mutmut['xǁOsvScannerScaǁ__init____mutmut_23'] = OsvScannerSca.xǁOsvScannerScaǁ__init____mutmut_23 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ__init____mutmut['xǁOsvScannerScaǁ__init____mutmut_24'] = OsvScannerSca.xǁOsvScannerScaǁ__init____mutmut_24 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ__init____mutmut['xǁOsvScannerScaǁ__init____mutmut_25'] = OsvScannerSca.xǁOsvScannerScaǁ__init____mutmut_25 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ__init____mutmut['xǁOsvScannerScaǁ__init____mutmut_26'] = OsvScannerSca.xǁOsvScannerScaǁ__init____mutmut_26 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ__init____mutmut['xǁOsvScannerScaǁ__init____mutmut_27'] = OsvScannerSca.xǁOsvScannerScaǁ__init____mutmut_27 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ__init____mutmut['xǁOsvScannerScaǁ__init____mutmut_28'] = OsvScannerSca.xǁOsvScannerScaǁ__init____mutmut_28 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ__init____mutmut['xǁOsvScannerScaǁ__init____mutmut_29'] = OsvScannerSca.xǁOsvScannerScaǁ__init____mutmut_29 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ__init____mutmut['xǁOsvScannerScaǁ__init____mutmut_30'] = OsvScannerSca.xǁOsvScannerScaǁ__init____mutmut_30 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ__init____mutmut['xǁOsvScannerScaǁ__init____mutmut_31'] = OsvScannerSca.xǁOsvScannerScaǁ__init____mutmut_31 # type: ignore # mutmut generated

mutants_xǁOsvScannerScaǁfrom_config__mutmut['_mutmut_orig'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_1'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_2'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_3'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_4'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_5'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_6'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_7'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_8'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_9'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_10'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_11'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_12'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_12 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_13'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_13 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_14'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_14 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_15'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_15 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_16'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_16 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_17'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_17 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_18'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_18 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_19'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_19 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_20'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_20 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_21'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_21 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_22'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_22 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_23'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_23 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_24'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_24 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_25'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_25 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_26'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_26 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_27'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_27 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_28'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_28 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_29'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_29 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_30'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_30 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_31'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_31 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_32'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_32 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_33'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_33 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_34'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_34 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_35'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_35 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_36'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_36 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_37'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_37 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_38'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_38 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_39'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_39 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_40'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_40 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_41'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_41 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_42'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_42 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_43'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_43 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_44'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_44 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_45'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_45 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_46'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_46 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_47'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_47 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁfrom_config__mutmut['xǁOsvScannerScaǁfrom_config__mutmut_48'] = OsvScannerSca.xǁOsvScannerScaǁfrom_config__mutmut_48 # type: ignore # mutmut generated

mutants_xǁOsvScannerScaǁ_execute__mutmut['_mutmut_orig'] = OsvScannerSca.xǁOsvScannerScaǁ_execute__mutmut_orig # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ_execute__mutmut['xǁOsvScannerScaǁ_execute__mutmut_1'] = OsvScannerSca.xǁOsvScannerScaǁ_execute__mutmut_1 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ_execute__mutmut['xǁOsvScannerScaǁ_execute__mutmut_2'] = OsvScannerSca.xǁOsvScannerScaǁ_execute__mutmut_2 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ_execute__mutmut['xǁOsvScannerScaǁ_execute__mutmut_3'] = OsvScannerSca.xǁOsvScannerScaǁ_execute__mutmut_3 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ_execute__mutmut['xǁOsvScannerScaǁ_execute__mutmut_4'] = OsvScannerSca.xǁOsvScannerScaǁ_execute__mutmut_4 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ_execute__mutmut['xǁOsvScannerScaǁ_execute__mutmut_5'] = OsvScannerSca.xǁOsvScannerScaǁ_execute__mutmut_5 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ_execute__mutmut['xǁOsvScannerScaǁ_execute__mutmut_6'] = OsvScannerSca.xǁOsvScannerScaǁ_execute__mutmut_6 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ_execute__mutmut['xǁOsvScannerScaǁ_execute__mutmut_7'] = OsvScannerSca.xǁOsvScannerScaǁ_execute__mutmut_7 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ_execute__mutmut['xǁOsvScannerScaǁ_execute__mutmut_8'] = OsvScannerSca.xǁOsvScannerScaǁ_execute__mutmut_8 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ_execute__mutmut['xǁOsvScannerScaǁ_execute__mutmut_9'] = OsvScannerSca.xǁOsvScannerScaǁ_execute__mutmut_9 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ_execute__mutmut['xǁOsvScannerScaǁ_execute__mutmut_10'] = OsvScannerSca.xǁOsvScannerScaǁ_execute__mutmut_10 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ_execute__mutmut['xǁOsvScannerScaǁ_execute__mutmut_11'] = OsvScannerSca.xǁOsvScannerScaǁ_execute__mutmut_11 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ_execute__mutmut['xǁOsvScannerScaǁ_execute__mutmut_12'] = OsvScannerSca.xǁOsvScannerScaǁ_execute__mutmut_12 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ_execute__mutmut['xǁOsvScannerScaǁ_execute__mutmut_13'] = OsvScannerSca.xǁOsvScannerScaǁ_execute__mutmut_13 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ_execute__mutmut['xǁOsvScannerScaǁ_execute__mutmut_14'] = OsvScannerSca.xǁOsvScannerScaǁ_execute__mutmut_14 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁ_execute__mutmut['xǁOsvScannerScaǁ_execute__mutmut_15'] = OsvScannerSca.xǁOsvScannerScaǁ_execute__mutmut_15 # type: ignore # mutmut generated

mutants_xǁOsvScannerScaǁevaluate__mutmut['_mutmut_orig'] = OsvScannerSca.xǁOsvScannerScaǁevaluate__mutmut_orig # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁevaluate__mutmut['xǁOsvScannerScaǁevaluate__mutmut_1'] = OsvScannerSca.xǁOsvScannerScaǁevaluate__mutmut_1 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁevaluate__mutmut['xǁOsvScannerScaǁevaluate__mutmut_2'] = OsvScannerSca.xǁOsvScannerScaǁevaluate__mutmut_2 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁevaluate__mutmut['xǁOsvScannerScaǁevaluate__mutmut_3'] = OsvScannerSca.xǁOsvScannerScaǁevaluate__mutmut_3 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁevaluate__mutmut['xǁOsvScannerScaǁevaluate__mutmut_4'] = OsvScannerSca.xǁOsvScannerScaǁevaluate__mutmut_4 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁevaluate__mutmut['xǁOsvScannerScaǁevaluate__mutmut_5'] = OsvScannerSca.xǁOsvScannerScaǁevaluate__mutmut_5 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁevaluate__mutmut['xǁOsvScannerScaǁevaluate__mutmut_6'] = OsvScannerSca.xǁOsvScannerScaǁevaluate__mutmut_6 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁevaluate__mutmut['xǁOsvScannerScaǁevaluate__mutmut_7'] = OsvScannerSca.xǁOsvScannerScaǁevaluate__mutmut_7 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁevaluate__mutmut['xǁOsvScannerScaǁevaluate__mutmut_8'] = OsvScannerSca.xǁOsvScannerScaǁevaluate__mutmut_8 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁevaluate__mutmut['xǁOsvScannerScaǁevaluate__mutmut_9'] = OsvScannerSca.xǁOsvScannerScaǁevaluate__mutmut_9 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁevaluate__mutmut['xǁOsvScannerScaǁevaluate__mutmut_10'] = OsvScannerSca.xǁOsvScannerScaǁevaluate__mutmut_10 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁevaluate__mutmut['xǁOsvScannerScaǁevaluate__mutmut_11'] = OsvScannerSca.xǁOsvScannerScaǁevaluate__mutmut_11 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁevaluate__mutmut['xǁOsvScannerScaǁevaluate__mutmut_12'] = OsvScannerSca.xǁOsvScannerScaǁevaluate__mutmut_12 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁevaluate__mutmut['xǁOsvScannerScaǁevaluate__mutmut_13'] = OsvScannerSca.xǁOsvScannerScaǁevaluate__mutmut_13 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁevaluate__mutmut['xǁOsvScannerScaǁevaluate__mutmut_14'] = OsvScannerSca.xǁOsvScannerScaǁevaluate__mutmut_14 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁevaluate__mutmut['xǁOsvScannerScaǁevaluate__mutmut_15'] = OsvScannerSca.xǁOsvScannerScaǁevaluate__mutmut_15 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁevaluate__mutmut['xǁOsvScannerScaǁevaluate__mutmut_16'] = OsvScannerSca.xǁOsvScannerScaǁevaluate__mutmut_16 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁevaluate__mutmut['xǁOsvScannerScaǁevaluate__mutmut_17'] = OsvScannerSca.xǁOsvScannerScaǁevaluate__mutmut_17 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁevaluate__mutmut['xǁOsvScannerScaǁevaluate__mutmut_18'] = OsvScannerSca.xǁOsvScannerScaǁevaluate__mutmut_18 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁevaluate__mutmut['xǁOsvScannerScaǁevaluate__mutmut_19'] = OsvScannerSca.xǁOsvScannerScaǁevaluate__mutmut_19 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁevaluate__mutmut['xǁOsvScannerScaǁevaluate__mutmut_20'] = OsvScannerSca.xǁOsvScannerScaǁevaluate__mutmut_20 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁevaluate__mutmut['xǁOsvScannerScaǁevaluate__mutmut_21'] = OsvScannerSca.xǁOsvScannerScaǁevaluate__mutmut_21 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁevaluate__mutmut['xǁOsvScannerScaǁevaluate__mutmut_22'] = OsvScannerSca.xǁOsvScannerScaǁevaluate__mutmut_22 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁevaluate__mutmut['xǁOsvScannerScaǁevaluate__mutmut_23'] = OsvScannerSca.xǁOsvScannerScaǁevaluate__mutmut_23 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁevaluate__mutmut['xǁOsvScannerScaǁevaluate__mutmut_24'] = OsvScannerSca.xǁOsvScannerScaǁevaluate__mutmut_24 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁevaluate__mutmut['xǁOsvScannerScaǁevaluate__mutmut_25'] = OsvScannerSca.xǁOsvScannerScaǁevaluate__mutmut_25 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁevaluate__mutmut['xǁOsvScannerScaǁevaluate__mutmut_26'] = OsvScannerSca.xǁOsvScannerScaǁevaluate__mutmut_26 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁevaluate__mutmut['xǁOsvScannerScaǁevaluate__mutmut_27'] = OsvScannerSca.xǁOsvScannerScaǁevaluate__mutmut_27 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁevaluate__mutmut['xǁOsvScannerScaǁevaluate__mutmut_28'] = OsvScannerSca.xǁOsvScannerScaǁevaluate__mutmut_28 # type: ignore # mutmut generated

mutants_xǁOsvScannerScaǁrun__mutmut['_mutmut_orig'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_orig # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_1'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_1 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_2'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_2 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_3'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_3 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_4'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_4 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_5'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_5 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_6'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_6 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_7'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_7 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_8'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_8 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_9'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_9 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_10'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_10 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_11'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_11 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_12'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_12 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_13'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_13 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_14'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_14 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_15'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_15 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_16'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_16 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_17'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_17 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_18'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_18 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_19'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_19 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_20'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_20 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_21'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_21 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_22'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_22 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_23'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_23 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_24'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_24 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_25'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_25 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_26'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_26 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_27'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_27 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_28'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_28 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_29'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_29 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_30'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_30 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_31'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_31 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_32'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_32 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_33'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_33 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_34'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_34 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_35'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_35 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_36'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_36 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_37'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_37 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_38'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_38 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_39'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_39 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_40'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_40 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_41'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_41 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_42'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_42 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_43'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_43 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_44'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_44 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_45'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_45 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_46'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_46 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_47'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_47 # type: ignore # mutmut generated
mutants_xǁOsvScannerScaǁrun__mutmut['xǁOsvScannerScaǁrun__mutmut_48'] = OsvScannerSca.xǁOsvScannerScaǁrun__mutmut_48 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(config: Mapping[str, Any], *, repo_root: Path | None = None) -> OsvScannerSca:
    return OsvScannerSca.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(config: Mapping[str, Any], *, repo_root: Path | None = None) -> OsvScannerSca:
    return OsvScannerSca.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(config: Mapping[str, Any], *, repo_root: Path | None = None) -> OsvScannerSca:
    return OsvScannerSca.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(config: Mapping[str, Any], *, repo_root: Path | None = None) -> OsvScannerSca:
    return OsvScannerSca.from_config(config, repo_root=None)


def x_build__mutmut_3(config: Mapping[str, Any], *, repo_root: Path | None = None) -> OsvScannerSca:
    return OsvScannerSca.from_config(repo_root=repo_root)


def x_build__mutmut_4(config: Mapping[str, Any], *, repo_root: Path | None = None) -> OsvScannerSca:
    return OsvScannerSca.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=OsvScannerSca.name)
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--scanner-version", required=True)
    parser.add_argument("--lockfile", action="append", default=[])
    args = parser.parse_args(argv)
    return OsvScannerSca(
        args.repo_root,
        scanner_version=args.scanner_version,
        lockfiles=args.lockfile,
    ).run()


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=OsvScannerSca.name)
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--scanner-version", required=True)
    parser.add_argument("--lockfile", action="append", default=[])
    args = parser.parse_args(argv)
    return OsvScannerSca(
        args.repo_root,
        scanner_version=args.scanner_version,
        lockfiles=args.lockfile,
    ).run()


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    parser = None
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--scanner-version", required=True)
    parser.add_argument("--lockfile", action="append", default=[])
    args = parser.parse_args(argv)
    return OsvScannerSca(
        args.repo_root,
        scanner_version=args.scanner_version,
        lockfiles=args.lockfile,
    ).run()


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=None)
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--scanner-version", required=True)
    parser.add_argument("--lockfile", action="append", default=[])
    args = parser.parse_args(argv)
    return OsvScannerSca(
        args.repo_root,
        scanner_version=args.scanner_version,
        lockfiles=args.lockfile,
    ).run()


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=OsvScannerSca.name)
    parser.add_argument(None, type=Path, default=None)
    parser.add_argument("--scanner-version", required=True)
    parser.add_argument("--lockfile", action="append", default=[])
    args = parser.parse_args(argv)
    return OsvScannerSca(
        args.repo_root,
        scanner_version=args.scanner_version,
        lockfiles=args.lockfile,
    ).run()


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=OsvScannerSca.name)
    parser.add_argument("--repo-root", type=None, default=None)
    parser.add_argument("--scanner-version", required=True)
    parser.add_argument("--lockfile", action="append", default=[])
    args = parser.parse_args(argv)
    return OsvScannerSca(
        args.repo_root,
        scanner_version=args.scanner_version,
        lockfiles=args.lockfile,
    ).run()


def x_main__mutmut_5(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=OsvScannerSca.name)
    parser.add_argument(type=Path, default=None)
    parser.add_argument("--scanner-version", required=True)
    parser.add_argument("--lockfile", action="append", default=[])
    args = parser.parse_args(argv)
    return OsvScannerSca(
        args.repo_root,
        scanner_version=args.scanner_version,
        lockfiles=args.lockfile,
    ).run()


def x_main__mutmut_6(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=OsvScannerSca.name)
    parser.add_argument("--repo-root", default=None)
    parser.add_argument("--scanner-version", required=True)
    parser.add_argument("--lockfile", action="append", default=[])
    args = parser.parse_args(argv)
    return OsvScannerSca(
        args.repo_root,
        scanner_version=args.scanner_version,
        lockfiles=args.lockfile,
    ).run()


def x_main__mutmut_7(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=OsvScannerSca.name)
    parser.add_argument("--repo-root", type=Path, )
    parser.add_argument("--scanner-version", required=True)
    parser.add_argument("--lockfile", action="append", default=[])
    args = parser.parse_args(argv)
    return OsvScannerSca(
        args.repo_root,
        scanner_version=args.scanner_version,
        lockfiles=args.lockfile,
    ).run()


def x_main__mutmut_8(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=OsvScannerSca.name)
    parser.add_argument("XX--repo-rootXX", type=Path, default=None)
    parser.add_argument("--scanner-version", required=True)
    parser.add_argument("--lockfile", action="append", default=[])
    args = parser.parse_args(argv)
    return OsvScannerSca(
        args.repo_root,
        scanner_version=args.scanner_version,
        lockfiles=args.lockfile,
    ).run()


def x_main__mutmut_9(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=OsvScannerSca.name)
    parser.add_argument("--REPO-ROOT", type=Path, default=None)
    parser.add_argument("--scanner-version", required=True)
    parser.add_argument("--lockfile", action="append", default=[])
    args = parser.parse_args(argv)
    return OsvScannerSca(
        args.repo_root,
        scanner_version=args.scanner_version,
        lockfiles=args.lockfile,
    ).run()


def x_main__mutmut_10(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=OsvScannerSca.name)
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument(None, required=True)
    parser.add_argument("--lockfile", action="append", default=[])
    args = parser.parse_args(argv)
    return OsvScannerSca(
        args.repo_root,
        scanner_version=args.scanner_version,
        lockfiles=args.lockfile,
    ).run()


def x_main__mutmut_11(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=OsvScannerSca.name)
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--scanner-version", required=None)
    parser.add_argument("--lockfile", action="append", default=[])
    args = parser.parse_args(argv)
    return OsvScannerSca(
        args.repo_root,
        scanner_version=args.scanner_version,
        lockfiles=args.lockfile,
    ).run()


def x_main__mutmut_12(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=OsvScannerSca.name)
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument(required=True)
    parser.add_argument("--lockfile", action="append", default=[])
    args = parser.parse_args(argv)
    return OsvScannerSca(
        args.repo_root,
        scanner_version=args.scanner_version,
        lockfiles=args.lockfile,
    ).run()


def x_main__mutmut_13(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=OsvScannerSca.name)
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--scanner-version", )
    parser.add_argument("--lockfile", action="append", default=[])
    args = parser.parse_args(argv)
    return OsvScannerSca(
        args.repo_root,
        scanner_version=args.scanner_version,
        lockfiles=args.lockfile,
    ).run()


def x_main__mutmut_14(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=OsvScannerSca.name)
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("XX--scanner-versionXX", required=True)
    parser.add_argument("--lockfile", action="append", default=[])
    args = parser.parse_args(argv)
    return OsvScannerSca(
        args.repo_root,
        scanner_version=args.scanner_version,
        lockfiles=args.lockfile,
    ).run()


def x_main__mutmut_15(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=OsvScannerSca.name)
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--SCANNER-VERSION", required=True)
    parser.add_argument("--lockfile", action="append", default=[])
    args = parser.parse_args(argv)
    return OsvScannerSca(
        args.repo_root,
        scanner_version=args.scanner_version,
        lockfiles=args.lockfile,
    ).run()


def x_main__mutmut_16(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=OsvScannerSca.name)
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--scanner-version", required=False)
    parser.add_argument("--lockfile", action="append", default=[])
    args = parser.parse_args(argv)
    return OsvScannerSca(
        args.repo_root,
        scanner_version=args.scanner_version,
        lockfiles=args.lockfile,
    ).run()


def x_main__mutmut_17(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=OsvScannerSca.name)
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--scanner-version", required=True)
    parser.add_argument(None, action="append", default=[])
    args = parser.parse_args(argv)
    return OsvScannerSca(
        args.repo_root,
        scanner_version=args.scanner_version,
        lockfiles=args.lockfile,
    ).run()


def x_main__mutmut_18(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=OsvScannerSca.name)
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--scanner-version", required=True)
    parser.add_argument("--lockfile", action=None, default=[])
    args = parser.parse_args(argv)
    return OsvScannerSca(
        args.repo_root,
        scanner_version=args.scanner_version,
        lockfiles=args.lockfile,
    ).run()


def x_main__mutmut_19(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=OsvScannerSca.name)
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--scanner-version", required=True)
    parser.add_argument("--lockfile", action="append", default=None)
    args = parser.parse_args(argv)
    return OsvScannerSca(
        args.repo_root,
        scanner_version=args.scanner_version,
        lockfiles=args.lockfile,
    ).run()


def x_main__mutmut_20(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=OsvScannerSca.name)
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--scanner-version", required=True)
    parser.add_argument(action="append", default=[])
    args = parser.parse_args(argv)
    return OsvScannerSca(
        args.repo_root,
        scanner_version=args.scanner_version,
        lockfiles=args.lockfile,
    ).run()


def x_main__mutmut_21(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=OsvScannerSca.name)
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--scanner-version", required=True)
    parser.add_argument("--lockfile", default=[])
    args = parser.parse_args(argv)
    return OsvScannerSca(
        args.repo_root,
        scanner_version=args.scanner_version,
        lockfiles=args.lockfile,
    ).run()


def x_main__mutmut_22(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=OsvScannerSca.name)
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--scanner-version", required=True)
    parser.add_argument("--lockfile", action="append", )
    args = parser.parse_args(argv)
    return OsvScannerSca(
        args.repo_root,
        scanner_version=args.scanner_version,
        lockfiles=args.lockfile,
    ).run()


def x_main__mutmut_23(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=OsvScannerSca.name)
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--scanner-version", required=True)
    parser.add_argument("XX--lockfileXX", action="append", default=[])
    args = parser.parse_args(argv)
    return OsvScannerSca(
        args.repo_root,
        scanner_version=args.scanner_version,
        lockfiles=args.lockfile,
    ).run()


def x_main__mutmut_24(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=OsvScannerSca.name)
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--scanner-version", required=True)
    parser.add_argument("--LOCKFILE", action="append", default=[])
    args = parser.parse_args(argv)
    return OsvScannerSca(
        args.repo_root,
        scanner_version=args.scanner_version,
        lockfiles=args.lockfile,
    ).run()


def x_main__mutmut_25(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=OsvScannerSca.name)
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--scanner-version", required=True)
    parser.add_argument("--lockfile", action="XXappendXX", default=[])
    args = parser.parse_args(argv)
    return OsvScannerSca(
        args.repo_root,
        scanner_version=args.scanner_version,
        lockfiles=args.lockfile,
    ).run()


def x_main__mutmut_26(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=OsvScannerSca.name)
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--scanner-version", required=True)
    parser.add_argument("--lockfile", action="APPEND", default=[])
    args = parser.parse_args(argv)
    return OsvScannerSca(
        args.repo_root,
        scanner_version=args.scanner_version,
        lockfiles=args.lockfile,
    ).run()


def x_main__mutmut_27(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=OsvScannerSca.name)
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--scanner-version", required=True)
    parser.add_argument("--lockfile", action="append", default=[])
    args = None
    return OsvScannerSca(
        args.repo_root,
        scanner_version=args.scanner_version,
        lockfiles=args.lockfile,
    ).run()


def x_main__mutmut_28(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=OsvScannerSca.name)
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--scanner-version", required=True)
    parser.add_argument("--lockfile", action="append", default=[])
    args = parser.parse_args(None)
    return OsvScannerSca(
        args.repo_root,
        scanner_version=args.scanner_version,
        lockfiles=args.lockfile,
    ).run()


def x_main__mutmut_29(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=OsvScannerSca.name)
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--scanner-version", required=True)
    parser.add_argument("--lockfile", action="append", default=[])
    args = parser.parse_args(argv)
    return OsvScannerSca(
        None,
        scanner_version=args.scanner_version,
        lockfiles=args.lockfile,
    ).run()


def x_main__mutmut_30(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=OsvScannerSca.name)
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--scanner-version", required=True)
    parser.add_argument("--lockfile", action="append", default=[])
    args = parser.parse_args(argv)
    return OsvScannerSca(
        args.repo_root,
        scanner_version=None,
        lockfiles=args.lockfile,
    ).run()


def x_main__mutmut_31(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=OsvScannerSca.name)
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--scanner-version", required=True)
    parser.add_argument("--lockfile", action="append", default=[])
    args = parser.parse_args(argv)
    return OsvScannerSca(
        args.repo_root,
        scanner_version=args.scanner_version,
        lockfiles=None,
    ).run()


def x_main__mutmut_32(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=OsvScannerSca.name)
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--scanner-version", required=True)
    parser.add_argument("--lockfile", action="append", default=[])
    args = parser.parse_args(argv)
    return OsvScannerSca(
        scanner_version=args.scanner_version,
        lockfiles=args.lockfile,
    ).run()


def x_main__mutmut_33(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=OsvScannerSca.name)
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--scanner-version", required=True)
    parser.add_argument("--lockfile", action="append", default=[])
    args = parser.parse_args(argv)
    return OsvScannerSca(
        args.repo_root,
        lockfiles=args.lockfile,
    ).run()


def x_main__mutmut_34(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=OsvScannerSca.name)
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--scanner-version", required=True)
    parser.add_argument("--lockfile", action="append", default=[])
    args = parser.parse_args(argv)
    return OsvScannerSca(
        args.repo_root,
        scanner_version=args.scanner_version,
        ).run()

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
mutants_x_main__mutmut['x_main__mutmut_17'] = x_main__mutmut_17 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_18'] = x_main__mutmut_18 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_19'] = x_main__mutmut_19 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_20'] = x_main__mutmut_20 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_21'] = x_main__mutmut_21 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_22'] = x_main__mutmut_22 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_23'] = x_main__mutmut_23 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_24'] = x_main__mutmut_24 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_25'] = x_main__mutmut_25 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_26'] = x_main__mutmut_26 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_27'] = x_main__mutmut_27 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_28'] = x_main__mutmut_28 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_29'] = x_main__mutmut_29 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_30'] = x_main__mutmut_30 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_31'] = x_main__mutmut_31 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_32'] = x_main__mutmut_32 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_33'] = x_main__mutmut_33 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_34'] = x_main__mutmut_34 # type: ignore # mutmut generated


if __name__ == "__main__":
    raise SystemExit(main())
