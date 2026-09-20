"""CORE check: license_present — every source file carries a license header.

Source files distributed without a license / SPDX header strip provenance: a
copied file loses the terms it was released under, and an audit can't tell
which license governs a given module. This rule walks the configured source
surface and FAILS on any file missing a recognised license marker near its
top.

Built fresh for the v0.6.0 CORE set (no single donor — taz/kairix enforce
license/NOTICE provenance via ad-hoc checks). Re-expressed as a configurable,
repo-agnostic rule: the marker strings that count as "a header is present"
(``SPDX-License-Identifier``, ``Copyright``, a license name) and the header
scan window are consumer config. The engine ships generic defaults (the
SPDX/Copyright shape every license header shares), not any repo's chosen
license.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: Domain-intrinsic markers every license header shares — not a chosen license.
DEFAULT_MARKERS: tuple[str, ...] = (
    "SPDX-License-Identifier",
    "Copyright",
    "Licensed under",
)
#: How many leading lines of a file are scanned for a marker. A header lives at
#: the very top; scanning the whole file would false-pass on an in-body mention.
DEFAULT_HEADER_LINES = 20

REMEDIATION = _remediation(
    fix=(
        "add a license header to the top of the file — an "
        "`SPDX-License-Identifier: <license>` line (or your repo's standard "
        "copyright / `Licensed under` block) within the first lines of the file."
    ),
    nxt="re-run this check to confirm the gate goes green.",
    run="python -m tc_fitness.core_checks.license_present",
    passing="# SPDX-License-Identifier: MIT",
    forbidden="# (no license header anywhere near the top of the file)",
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x_file_missing_license__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_file_missing_license__mutmut)
def file_missing_license(path: Path, *, markers: Sequence[str], header_lines: int) -> bool:
    """Pure detection helper: True iff none of ``markers`` appears in the header.

    Only the first ``header_lines`` lines are inspected so an in-body mention of
    a marker word does not false-pass. A read / decode error is a violation
    because the configured source could not be evaluated.
    """
    try:
        with path.open(encoding="utf-8") as fh:
            head = "".join(line for _, line in zip(range(header_lines), fh, strict=False))
    except (UnicodeDecodeError, OSError):
        return True
    return not any(marker in head for marker in markers)


def x_file_missing_license__mutmut_orig(path: Path, *, markers: Sequence[str], header_lines: int) -> bool:
    """Pure detection helper: True iff none of ``markers`` appears in the header.

    Only the first ``header_lines`` lines are inspected so an in-body mention of
    a marker word does not false-pass. A read / decode error is a violation
    because the configured source could not be evaluated.
    """
    try:
        with path.open(encoding="utf-8") as fh:
            head = "".join(line for _, line in zip(range(header_lines), fh, strict=False))
    except (UnicodeDecodeError, OSError):
        return True
    return not any(marker in head for marker in markers)


def x_file_missing_license__mutmut_1(path: Path, *, markers: Sequence[str], header_lines: int) -> bool:
    """Pure detection helper: True iff none of ``markers`` appears in the header.

    Only the first ``header_lines`` lines are inspected so an in-body mention of
    a marker word does not false-pass. A read / decode error is a violation
    because the configured source could not be evaluated.
    """
    try:
        with path.open(encoding=None) as fh:
            head = "".join(line for _, line in zip(range(header_lines), fh, strict=False))
    except (UnicodeDecodeError, OSError):
        return True
    return not any(marker in head for marker in markers)


def x_file_missing_license__mutmut_2(path: Path, *, markers: Sequence[str], header_lines: int) -> bool:
    """Pure detection helper: True iff none of ``markers`` appears in the header.

    Only the first ``header_lines`` lines are inspected so an in-body mention of
    a marker word does not false-pass. A read / decode error is a violation
    because the configured source could not be evaluated.
    """
    try:
        with path.open(encoding="XXutf-8XX") as fh:
            head = "".join(line for _, line in zip(range(header_lines), fh, strict=False))
    except (UnicodeDecodeError, OSError):
        return True
    return not any(marker in head for marker in markers)


def x_file_missing_license__mutmut_3(path: Path, *, markers: Sequence[str], header_lines: int) -> bool:
    """Pure detection helper: True iff none of ``markers`` appears in the header.

    Only the first ``header_lines`` lines are inspected so an in-body mention of
    a marker word does not false-pass. A read / decode error is a violation
    because the configured source could not be evaluated.
    """
    try:
        with path.open(encoding="UTF-8") as fh:
            head = "".join(line for _, line in zip(range(header_lines), fh, strict=False))
    except (UnicodeDecodeError, OSError):
        return True
    return not any(marker in head for marker in markers)


def x_file_missing_license__mutmut_4(path: Path, *, markers: Sequence[str], header_lines: int) -> bool:
    """Pure detection helper: True iff none of ``markers`` appears in the header.

    Only the first ``header_lines`` lines are inspected so an in-body mention of
    a marker word does not false-pass. A read / decode error is a violation
    because the configured source could not be evaluated.
    """
    try:
        with path.open(encoding="utf-8") as fh:
            head = None
    except (UnicodeDecodeError, OSError):
        return True
    return not any(marker in head for marker in markers)


def x_file_missing_license__mutmut_5(path: Path, *, markers: Sequence[str], header_lines: int) -> bool:
    """Pure detection helper: True iff none of ``markers`` appears in the header.

    Only the first ``header_lines`` lines are inspected so an in-body mention of
    a marker word does not false-pass. A read / decode error is a violation
    because the configured source could not be evaluated.
    """
    try:
        with path.open(encoding="utf-8") as fh:
            head = "".join(None)
    except (UnicodeDecodeError, OSError):
        return True
    return not any(marker in head for marker in markers)


def x_file_missing_license__mutmut_6(path: Path, *, markers: Sequence[str], header_lines: int) -> bool:
    """Pure detection helper: True iff none of ``markers`` appears in the header.

    Only the first ``header_lines`` lines are inspected so an in-body mention of
    a marker word does not false-pass. A read / decode error is a violation
    because the configured source could not be evaluated.
    """
    try:
        with path.open(encoding="utf-8") as fh:
            head = "XXXX".join(line for _, line in zip(range(header_lines), fh, strict=False))
    except (UnicodeDecodeError, OSError):
        return True
    return not any(marker in head for marker in markers)


def x_file_missing_license__mutmut_7(path: Path, *, markers: Sequence[str], header_lines: int) -> bool:
    """Pure detection helper: True iff none of ``markers`` appears in the header.

    Only the first ``header_lines`` lines are inspected so an in-body mention of
    a marker word does not false-pass. A read / decode error is a violation
    because the configured source could not be evaluated.
    """
    try:
        with path.open(encoding="utf-8") as fh:
            head = "".join(line for _, line in zip(None, fh, strict=False))
    except (UnicodeDecodeError, OSError):
        return True
    return not any(marker in head for marker in markers)


def x_file_missing_license__mutmut_8(path: Path, *, markers: Sequence[str], header_lines: int) -> bool:
    """Pure detection helper: True iff none of ``markers`` appears in the header.

    Only the first ``header_lines`` lines are inspected so an in-body mention of
    a marker word does not false-pass. A read / decode error is a violation
    because the configured source could not be evaluated.
    """
    try:
        with path.open(encoding="utf-8") as fh:
            head = "".join(line for _, line in zip(range(header_lines), None, strict=False))
    except (UnicodeDecodeError, OSError):
        return True
    return not any(marker in head for marker in markers)


def x_file_missing_license__mutmut_9(path: Path, *, markers: Sequence[str], header_lines: int) -> bool:
    """Pure detection helper: True iff none of ``markers`` appears in the header.

    Only the first ``header_lines`` lines are inspected so an in-body mention of
    a marker word does not false-pass. A read / decode error is a violation
    because the configured source could not be evaluated.
    """
    try:
        with path.open(encoding="utf-8") as fh:
            head = "".join(line for _, line in zip(range(header_lines), fh, strict=None))
    except (UnicodeDecodeError, OSError):
        return True
    return not any(marker in head for marker in markers)


def x_file_missing_license__mutmut_10(path: Path, *, markers: Sequence[str], header_lines: int) -> bool:
    """Pure detection helper: True iff none of ``markers`` appears in the header.

    Only the first ``header_lines`` lines are inspected so an in-body mention of
    a marker word does not false-pass. A read / decode error is a violation
    because the configured source could not be evaluated.
    """
    try:
        with path.open(encoding="utf-8") as fh:
            head = "".join(line for _, line in zip(fh, strict=False))
    except (UnicodeDecodeError, OSError):
        return True
    return not any(marker in head for marker in markers)


def x_file_missing_license__mutmut_11(path: Path, *, markers: Sequence[str], header_lines: int) -> bool:
    """Pure detection helper: True iff none of ``markers`` appears in the header.

    Only the first ``header_lines`` lines are inspected so an in-body mention of
    a marker word does not false-pass. A read / decode error is a violation
    because the configured source could not be evaluated.
    """
    try:
        with path.open(encoding="utf-8") as fh:
            head = "".join(line for _, line in zip(range(header_lines), strict=False))
    except (UnicodeDecodeError, OSError):
        return True
    return not any(marker in head for marker in markers)


def x_file_missing_license__mutmut_12(path: Path, *, markers: Sequence[str], header_lines: int) -> bool:
    """Pure detection helper: True iff none of ``markers`` appears in the header.

    Only the first ``header_lines`` lines are inspected so an in-body mention of
    a marker word does not false-pass. A read / decode error is a violation
    because the configured source could not be evaluated.
    """
    try:
        with path.open(encoding="utf-8") as fh:
            head = "".join(line for _, line in zip(range(header_lines), fh, ))
    except (UnicodeDecodeError, OSError):
        return True
    return not any(marker in head for marker in markers)


def x_file_missing_license__mutmut_13(path: Path, *, markers: Sequence[str], header_lines: int) -> bool:
    """Pure detection helper: True iff none of ``markers`` appears in the header.

    Only the first ``header_lines`` lines are inspected so an in-body mention of
    a marker word does not false-pass. A read / decode error is a violation
    because the configured source could not be evaluated.
    """
    try:
        with path.open(encoding="utf-8") as fh:
            head = "".join(line for _, line in zip(range(None), fh, strict=False))
    except (UnicodeDecodeError, OSError):
        return True
    return not any(marker in head for marker in markers)


def x_file_missing_license__mutmut_14(path: Path, *, markers: Sequence[str], header_lines: int) -> bool:
    """Pure detection helper: True iff none of ``markers`` appears in the header.

    Only the first ``header_lines`` lines are inspected so an in-body mention of
    a marker word does not false-pass. A read / decode error is a violation
    because the configured source could not be evaluated.
    """
    try:
        with path.open(encoding="utf-8") as fh:
            head = "".join(line for _, line in zip(range(header_lines), fh, strict=True))
    except (UnicodeDecodeError, OSError):
        return True
    return not any(marker in head for marker in markers)


def x_file_missing_license__mutmut_15(path: Path, *, markers: Sequence[str], header_lines: int) -> bool:
    """Pure detection helper: True iff none of ``markers`` appears in the header.

    Only the first ``header_lines`` lines are inspected so an in-body mention of
    a marker word does not false-pass. A read / decode error is a violation
    because the configured source could not be evaluated.
    """
    try:
        with path.open(encoding="utf-8") as fh:
            head = "".join(line for _, line in zip(range(header_lines), fh, strict=False))
    except (UnicodeDecodeError, OSError):
        return False
    return not any(marker in head for marker in markers)


def x_file_missing_license__mutmut_16(path: Path, *, markers: Sequence[str], header_lines: int) -> bool:
    """Pure detection helper: True iff none of ``markers`` appears in the header.

    Only the first ``header_lines`` lines are inspected so an in-body mention of
    a marker word does not false-pass. A read / decode error is a violation
    because the configured source could not be evaluated.
    """
    try:
        with path.open(encoding="utf-8") as fh:
            head = "".join(line for _, line in zip(range(header_lines), fh, strict=False))
    except (UnicodeDecodeError, OSError):
        return True
    return any(marker in head for marker in markers)


def x_file_missing_license__mutmut_17(path: Path, *, markers: Sequence[str], header_lines: int) -> bool:
    """Pure detection helper: True iff none of ``markers`` appears in the header.

    Only the first ``header_lines`` lines are inspected so an in-body mention of
    a marker word does not false-pass. A read / decode error is a violation
    because the configured source could not be evaluated.
    """
    try:
        with path.open(encoding="utf-8") as fh:
            head = "".join(line for _, line in zip(range(header_lines), fh, strict=False))
    except (UnicodeDecodeError, OSError):
        return True
    return not any(None)


def x_file_missing_license__mutmut_18(path: Path, *, markers: Sequence[str], header_lines: int) -> bool:
    """Pure detection helper: True iff none of ``markers`` appears in the header.

    Only the first ``header_lines`` lines are inspected so an in-body mention of
    a marker word does not false-pass. A read / decode error is a violation
    because the configured source could not be evaluated.
    """
    try:
        with path.open(encoding="utf-8") as fh:
            head = "".join(line for _, line in zip(range(header_lines), fh, strict=False))
    except (UnicodeDecodeError, OSError):
        return True
    return not any(marker not in head for marker in markers)

mutants_x_file_missing_license__mutmut['_mutmut_orig'] = x_file_missing_license__mutmut_orig # type: ignore # mutmut generated
mutants_x_file_missing_license__mutmut['x_file_missing_license__mutmut_1'] = x_file_missing_license__mutmut_1 # type: ignore # mutmut generated
mutants_x_file_missing_license__mutmut['x_file_missing_license__mutmut_2'] = x_file_missing_license__mutmut_2 # type: ignore # mutmut generated
mutants_x_file_missing_license__mutmut['x_file_missing_license__mutmut_3'] = x_file_missing_license__mutmut_3 # type: ignore # mutmut generated
mutants_x_file_missing_license__mutmut['x_file_missing_license__mutmut_4'] = x_file_missing_license__mutmut_4 # type: ignore # mutmut generated
mutants_x_file_missing_license__mutmut['x_file_missing_license__mutmut_5'] = x_file_missing_license__mutmut_5 # type: ignore # mutmut generated
mutants_x_file_missing_license__mutmut['x_file_missing_license__mutmut_6'] = x_file_missing_license__mutmut_6 # type: ignore # mutmut generated
mutants_x_file_missing_license__mutmut['x_file_missing_license__mutmut_7'] = x_file_missing_license__mutmut_7 # type: ignore # mutmut generated
mutants_x_file_missing_license__mutmut['x_file_missing_license__mutmut_8'] = x_file_missing_license__mutmut_8 # type: ignore # mutmut generated
mutants_x_file_missing_license__mutmut['x_file_missing_license__mutmut_9'] = x_file_missing_license__mutmut_9 # type: ignore # mutmut generated
mutants_x_file_missing_license__mutmut['x_file_missing_license__mutmut_10'] = x_file_missing_license__mutmut_10 # type: ignore # mutmut generated
mutants_x_file_missing_license__mutmut['x_file_missing_license__mutmut_11'] = x_file_missing_license__mutmut_11 # type: ignore # mutmut generated
mutants_x_file_missing_license__mutmut['x_file_missing_license__mutmut_12'] = x_file_missing_license__mutmut_12 # type: ignore # mutmut generated
mutants_x_file_missing_license__mutmut['x_file_missing_license__mutmut_13'] = x_file_missing_license__mutmut_13 # type: ignore # mutmut generated
mutants_x_file_missing_license__mutmut['x_file_missing_license__mutmut_14'] = x_file_missing_license__mutmut_14 # type: ignore # mutmut generated
mutants_x_file_missing_license__mutmut['x_file_missing_license__mutmut_15'] = x_file_missing_license__mutmut_15 # type: ignore # mutmut generated
mutants_x_file_missing_license__mutmut['x_file_missing_license__mutmut_16'] = x_file_missing_license__mutmut_16 # type: ignore # mutmut generated
mutants_x_file_missing_license__mutmut['x_file_missing_license__mutmut_17'] = x_file_missing_license__mutmut_17 # type: ignore # mutmut generated
mutants_x_file_missing_license__mutmut['x_file_missing_license__mutmut_18'] = x_file_missing_license__mutmut_18 # type: ignore # mutmut generated
mutants_xǁLicensePresentǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁLicensePresentǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore


class LicensePresent(FitnessRule):
    """Flags source files missing a license / SPDX header."""

    name = "license-present"
    remediation = REMEDIATION
    extensions = (".py",)

    #: Rule-specific config (instance attrs; from_config overrides per consumer).
    markers: tuple[str, ...] = DEFAULT_MARKERS
    header_lines: int = DEFAULT_HEADER_LINES

    @classmethod
    @_mutmut_mutated(mutants_xǁLicensePresentǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> LicensePresent:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, LicensePresent)  # noqa: S101  # narrowing for mypy
        rule.markers = tuple(config.get("markers", DEFAULT_MARKERS))
        rule.header_lines = int(config.get("header_lines", DEFAULT_HEADER_LINES))
        return rule

    @classmethod
    def xǁLicensePresentǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> LicensePresent:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, LicensePresent)  # noqa: S101  # narrowing for mypy
        rule.markers = tuple(config.get("markers", DEFAULT_MARKERS))
        rule.header_lines = int(config.get("header_lines", DEFAULT_HEADER_LINES))
        return rule

    @classmethod
    def xǁLicensePresentǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> LicensePresent:
        rule = None
        assert isinstance(rule, LicensePresent)  # noqa: S101  # narrowing for mypy
        rule.markers = tuple(config.get("markers", DEFAULT_MARKERS))
        rule.header_lines = int(config.get("header_lines", DEFAULT_HEADER_LINES))
        return rule

    @classmethod
    def xǁLicensePresentǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> LicensePresent:
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, LicensePresent)  # noqa: S101  # narrowing for mypy
        rule.markers = tuple(config.get("markers", DEFAULT_MARKERS))
        rule.header_lines = int(config.get("header_lines", DEFAULT_HEADER_LINES))
        return rule

    @classmethod
    def xǁLicensePresentǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> LicensePresent:
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, LicensePresent)  # noqa: S101  # narrowing for mypy
        rule.markers = tuple(config.get("markers", DEFAULT_MARKERS))
        rule.header_lines = int(config.get("header_lines", DEFAULT_HEADER_LINES))
        return rule

    @classmethod
    def xǁLicensePresentǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> LicensePresent:
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, LicensePresent)  # noqa: S101  # narrowing for mypy
        rule.markers = tuple(config.get("markers", DEFAULT_MARKERS))
        rule.header_lines = int(config.get("header_lines", DEFAULT_HEADER_LINES))
        return rule

    @classmethod
    def xǁLicensePresentǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> LicensePresent:
        rule = super().from_config(config, )
        assert isinstance(rule, LicensePresent)  # noqa: S101  # narrowing for mypy
        rule.markers = tuple(config.get("markers", DEFAULT_MARKERS))
        rule.header_lines = int(config.get("header_lines", DEFAULT_HEADER_LINES))
        return rule

    @classmethod
    def xǁLicensePresentǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> LicensePresent:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, LicensePresent)  # noqa: S101  # narrowing for mypy
        rule.markers = None
        rule.header_lines = int(config.get("header_lines", DEFAULT_HEADER_LINES))
        return rule

    @classmethod
    def xǁLicensePresentǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> LicensePresent:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, LicensePresent)  # noqa: S101  # narrowing for mypy
        rule.markers = tuple(None)
        rule.header_lines = int(config.get("header_lines", DEFAULT_HEADER_LINES))
        return rule

    @classmethod
    def xǁLicensePresentǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> LicensePresent:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, LicensePresent)  # noqa: S101  # narrowing for mypy
        rule.markers = tuple(config.get(None, DEFAULT_MARKERS))
        rule.header_lines = int(config.get("header_lines", DEFAULT_HEADER_LINES))
        return rule

    @classmethod
    def xǁLicensePresentǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> LicensePresent:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, LicensePresent)  # noqa: S101  # narrowing for mypy
        rule.markers = tuple(config.get("markers", None))
        rule.header_lines = int(config.get("header_lines", DEFAULT_HEADER_LINES))
        return rule

    @classmethod
    def xǁLicensePresentǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> LicensePresent:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, LicensePresent)  # noqa: S101  # narrowing for mypy
        rule.markers = tuple(config.get(DEFAULT_MARKERS))
        rule.header_lines = int(config.get("header_lines", DEFAULT_HEADER_LINES))
        return rule

    @classmethod
    def xǁLicensePresentǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> LicensePresent:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, LicensePresent)  # noqa: S101  # narrowing for mypy
        rule.markers = tuple(config.get("markers", ))
        rule.header_lines = int(config.get("header_lines", DEFAULT_HEADER_LINES))
        return rule

    @classmethod
    def xǁLicensePresentǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> LicensePresent:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, LicensePresent)  # noqa: S101  # narrowing for mypy
        rule.markers = tuple(config.get("XXmarkersXX", DEFAULT_MARKERS))
        rule.header_lines = int(config.get("header_lines", DEFAULT_HEADER_LINES))
        return rule

    @classmethod
    def xǁLicensePresentǁfrom_config__mutmut_13(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> LicensePresent:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, LicensePresent)  # noqa: S101  # narrowing for mypy
        rule.markers = tuple(config.get("MARKERS", DEFAULT_MARKERS))
        rule.header_lines = int(config.get("header_lines", DEFAULT_HEADER_LINES))
        return rule

    @classmethod
    def xǁLicensePresentǁfrom_config__mutmut_14(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> LicensePresent:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, LicensePresent)  # noqa: S101  # narrowing for mypy
        rule.markers = tuple(config.get("markers", DEFAULT_MARKERS))
        rule.header_lines = None
        return rule

    @classmethod
    def xǁLicensePresentǁfrom_config__mutmut_15(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> LicensePresent:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, LicensePresent)  # noqa: S101  # narrowing for mypy
        rule.markers = tuple(config.get("markers", DEFAULT_MARKERS))
        rule.header_lines = int(None)
        return rule

    @classmethod
    def xǁLicensePresentǁfrom_config__mutmut_16(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> LicensePresent:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, LicensePresent)  # noqa: S101  # narrowing for mypy
        rule.markers = tuple(config.get("markers", DEFAULT_MARKERS))
        rule.header_lines = int(config.get(None, DEFAULT_HEADER_LINES))
        return rule

    @classmethod
    def xǁLicensePresentǁfrom_config__mutmut_17(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> LicensePresent:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, LicensePresent)  # noqa: S101  # narrowing for mypy
        rule.markers = tuple(config.get("markers", DEFAULT_MARKERS))
        rule.header_lines = int(config.get("header_lines", None))
        return rule

    @classmethod
    def xǁLicensePresentǁfrom_config__mutmut_18(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> LicensePresent:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, LicensePresent)  # noqa: S101  # narrowing for mypy
        rule.markers = tuple(config.get("markers", DEFAULT_MARKERS))
        rule.header_lines = int(config.get(DEFAULT_HEADER_LINES))
        return rule

    @classmethod
    def xǁLicensePresentǁfrom_config__mutmut_19(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> LicensePresent:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, LicensePresent)  # noqa: S101  # narrowing for mypy
        rule.markers = tuple(config.get("markers", DEFAULT_MARKERS))
        rule.header_lines = int(config.get("header_lines", ))
        return rule

    @classmethod
    def xǁLicensePresentǁfrom_config__mutmut_20(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> LicensePresent:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, LicensePresent)  # noqa: S101  # narrowing for mypy
        rule.markers = tuple(config.get("markers", DEFAULT_MARKERS))
        rule.header_lines = int(config.get("XXheader_linesXX", DEFAULT_HEADER_LINES))
        return rule

    @classmethod
    def xǁLicensePresentǁfrom_config__mutmut_21(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> LicensePresent:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, LicensePresent)  # noqa: S101  # narrowing for mypy
        rule.markers = tuple(config.get("markers", DEFAULT_MARKERS))
        rule.header_lines = int(config.get("HEADER_LINES", DEFAULT_HEADER_LINES))
        return rule

    @_mutmut_mutated(mutants_xǁLicensePresentǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        return file_missing_license(path, markers=self.markers, header_lines=self.header_lines)

    def xǁLicensePresentǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        return file_missing_license(path, markers=self.markers, header_lines=self.header_lines)

    def xǁLicensePresentǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        return file_missing_license(None, markers=self.markers, header_lines=self.header_lines)

    def xǁLicensePresentǁfile_has_violation__mutmut_2(self, path: Path) -> bool:
        return file_missing_license(path, markers=None, header_lines=self.header_lines)

    def xǁLicensePresentǁfile_has_violation__mutmut_3(self, path: Path) -> bool:
        return file_missing_license(path, markers=self.markers, header_lines=None)

    def xǁLicensePresentǁfile_has_violation__mutmut_4(self, path: Path) -> bool:
        return file_missing_license(markers=self.markers, header_lines=self.header_lines)

    def xǁLicensePresentǁfile_has_violation__mutmut_5(self, path: Path) -> bool:
        return file_missing_license(path, header_lines=self.header_lines)

    def xǁLicensePresentǁfile_has_violation__mutmut_6(self, path: Path) -> bool:
        return file_missing_license(path, markers=self.markers, )

mutants_xǁLicensePresentǁfrom_config__mutmut['_mutmut_orig'] = LicensePresent.xǁLicensePresentǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁLicensePresentǁfrom_config__mutmut['xǁLicensePresentǁfrom_config__mutmut_1'] = LicensePresent.xǁLicensePresentǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁLicensePresentǁfrom_config__mutmut['xǁLicensePresentǁfrom_config__mutmut_2'] = LicensePresent.xǁLicensePresentǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁLicensePresentǁfrom_config__mutmut['xǁLicensePresentǁfrom_config__mutmut_3'] = LicensePresent.xǁLicensePresentǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁLicensePresentǁfrom_config__mutmut['xǁLicensePresentǁfrom_config__mutmut_4'] = LicensePresent.xǁLicensePresentǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁLicensePresentǁfrom_config__mutmut['xǁLicensePresentǁfrom_config__mutmut_5'] = LicensePresent.xǁLicensePresentǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁLicensePresentǁfrom_config__mutmut['xǁLicensePresentǁfrom_config__mutmut_6'] = LicensePresent.xǁLicensePresentǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁLicensePresentǁfrom_config__mutmut['xǁLicensePresentǁfrom_config__mutmut_7'] = LicensePresent.xǁLicensePresentǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁLicensePresentǁfrom_config__mutmut['xǁLicensePresentǁfrom_config__mutmut_8'] = LicensePresent.xǁLicensePresentǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁLicensePresentǁfrom_config__mutmut['xǁLicensePresentǁfrom_config__mutmut_9'] = LicensePresent.xǁLicensePresentǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁLicensePresentǁfrom_config__mutmut['xǁLicensePresentǁfrom_config__mutmut_10'] = LicensePresent.xǁLicensePresentǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁLicensePresentǁfrom_config__mutmut['xǁLicensePresentǁfrom_config__mutmut_11'] = LicensePresent.xǁLicensePresentǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁLicensePresentǁfrom_config__mutmut['xǁLicensePresentǁfrom_config__mutmut_12'] = LicensePresent.xǁLicensePresentǁfrom_config__mutmut_12 # type: ignore # mutmut generated
mutants_xǁLicensePresentǁfrom_config__mutmut['xǁLicensePresentǁfrom_config__mutmut_13'] = LicensePresent.xǁLicensePresentǁfrom_config__mutmut_13 # type: ignore # mutmut generated
mutants_xǁLicensePresentǁfrom_config__mutmut['xǁLicensePresentǁfrom_config__mutmut_14'] = LicensePresent.xǁLicensePresentǁfrom_config__mutmut_14 # type: ignore # mutmut generated
mutants_xǁLicensePresentǁfrom_config__mutmut['xǁLicensePresentǁfrom_config__mutmut_15'] = LicensePresent.xǁLicensePresentǁfrom_config__mutmut_15 # type: ignore # mutmut generated
mutants_xǁLicensePresentǁfrom_config__mutmut['xǁLicensePresentǁfrom_config__mutmut_16'] = LicensePresent.xǁLicensePresentǁfrom_config__mutmut_16 # type: ignore # mutmut generated
mutants_xǁLicensePresentǁfrom_config__mutmut['xǁLicensePresentǁfrom_config__mutmut_17'] = LicensePresent.xǁLicensePresentǁfrom_config__mutmut_17 # type: ignore # mutmut generated
mutants_xǁLicensePresentǁfrom_config__mutmut['xǁLicensePresentǁfrom_config__mutmut_18'] = LicensePresent.xǁLicensePresentǁfrom_config__mutmut_18 # type: ignore # mutmut generated
mutants_xǁLicensePresentǁfrom_config__mutmut['xǁLicensePresentǁfrom_config__mutmut_19'] = LicensePresent.xǁLicensePresentǁfrom_config__mutmut_19 # type: ignore # mutmut generated
mutants_xǁLicensePresentǁfrom_config__mutmut['xǁLicensePresentǁfrom_config__mutmut_20'] = LicensePresent.xǁLicensePresentǁfrom_config__mutmut_20 # type: ignore # mutmut generated
mutants_xǁLicensePresentǁfrom_config__mutmut['xǁLicensePresentǁfrom_config__mutmut_21'] = LicensePresent.xǁLicensePresentǁfrom_config__mutmut_21 # type: ignore # mutmut generated

mutants_xǁLicensePresentǁfile_has_violation__mutmut['_mutmut_orig'] = LicensePresent.xǁLicensePresentǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁLicensePresentǁfile_has_violation__mutmut['xǁLicensePresentǁfile_has_violation__mutmut_1'] = LicensePresent.xǁLicensePresentǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_xǁLicensePresentǁfile_has_violation__mutmut['xǁLicensePresentǁfile_has_violation__mutmut_2'] = LicensePresent.xǁLicensePresentǁfile_has_violation__mutmut_2 # type: ignore # mutmut generated
mutants_xǁLicensePresentǁfile_has_violation__mutmut['xǁLicensePresentǁfile_has_violation__mutmut_3'] = LicensePresent.xǁLicensePresentǁfile_has_violation__mutmut_3 # type: ignore # mutmut generated
mutants_xǁLicensePresentǁfile_has_violation__mutmut['xǁLicensePresentǁfile_has_violation__mutmut_4'] = LicensePresent.xǁLicensePresentǁfile_has_violation__mutmut_4 # type: ignore # mutmut generated
mutants_xǁLicensePresentǁfile_has_violation__mutmut['xǁLicensePresentǁfile_has_violation__mutmut_5'] = LicensePresent.xǁLicensePresentǁfile_has_violation__mutmut_5 # type: ignore # mutmut generated
mutants_xǁLicensePresentǁfile_has_violation__mutmut['xǁLicensePresentǁfile_has_violation__mutmut_6'] = LicensePresent.xǁLicensePresentǁfile_has_violation__mutmut_6 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> LicensePresent:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return LicensePresent.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> LicensePresent:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return LicensePresent.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> LicensePresent:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return LicensePresent.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> LicensePresent:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return LicensePresent.from_config(config, repo_root=None)


def x_build__mutmut_3(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> LicensePresent:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return LicensePresent.from_config(repo_root=repo_root)


def x_build__mutmut_4(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> LicensePresent:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return LicensePresent.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(LicensePresent, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(LicensePresent, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(LicensePresent, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(LicensePresent, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
