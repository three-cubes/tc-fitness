"""CORE check: coverage_floor — per-file line-coverage floor.

Repository-wide coverage averages hide files at 0%: a 91% repo mean can
conceal a source file with no tests at all. This rule enforces a PER-FILE
floor — every source file recorded in a coverage report must clear a minimum
line-coverage percentage — so the gap is surfaced file-by-file rather than
washed out in the mean.

The rule fails whenever any measured source file is below the configured floor.

Ported from kairix ``scripts/checks/check_per_file_coverage.py`` (F7/F9) and
the coverage.xml parsing in tc-agent-zone ``scripts/checks/coverage_ratchet.py``
— re-expressed as a configurable, repo-agnostic rule. The floor, the coverage
report path, and the scan roots are CONFIG the consumer supplies; nothing here
names a repo, a source package, or a hardcoded threshold beyond the
domain-intrinsic default.
"""

from __future__ import annotations

import importlib
import math
from collections.abc import Callable, Mapping
from functools import cached_property
from pathlib import Path
from types import ModuleType
from typing import Any

from tc_fitness.check_evidence import report_finding
from tc_fitness.core_checks import run_core_check
from tc_fitness.core_checks._coverage_evidence import (
    CoverageCounts,
    count_class_coverage,
    coverage_integer,
    resolve_coverage_filename,
    validate_coverage_rate,
)
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: The domain-intrinsic default floor. Per-file line coverage below this is a
#: gap worth surfacing. Overridable per consumer via ``floor_pct``.
DEFAULT_FLOOR_PCT = 90.0

#: Default coverage report location relative to the repo root. Overridable.
DEFAULT_COVERAGE_REPORT = "coverage.xml"

REMEDIATION = _remediation(
    fix=(
        "ask what DEFECT CLASS the coverage gap proxies before padding tests: "
        "a missing failure-mode test at a boundary, a missing scale-bound test, "
        "or a genuinely production-only adapter. Add the test that proves the "
        "behaviour; do not call a function once just to push the percentage up."
    ),
    nxt="re-run this check to confirm the file clears the floor.",
    run="python -m tc_fitness.core_checks.coverage_floor",
    passing="extract testable logic behind a deps seam, then unit-test the branches",
    forbidden="add a no-op test that calls the function once to lift the percentage",
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x__reject_unsafe_xml__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__reject_unsafe_xml__mutmut)
def _reject_unsafe_xml(text: str, source: str) -> None:
    """Reject DTD/entity declarations before any parser runs (XXE guard)."""
    lowered = text.lower()
    if "<!doctype" in lowered or "<!entity" in lowered:
        raise ValueError(f"unsafe coverage XML at {source}: DTD/entity declarations are not allowed")


def x__reject_unsafe_xml__mutmut_orig(text: str, source: str) -> None:
    """Reject DTD/entity declarations before any parser runs (XXE guard)."""
    lowered = text.lower()
    if "<!doctype" in lowered or "<!entity" in lowered:
        raise ValueError(f"unsafe coverage XML at {source}: DTD/entity declarations are not allowed")


def x__reject_unsafe_xml__mutmut_1(text: str, source: str) -> None:
    """Reject DTD/entity declarations before any parser runs (XXE guard)."""
    lowered = None
    if "<!doctype" in lowered or "<!entity" in lowered:
        raise ValueError(f"unsafe coverage XML at {source}: DTD/entity declarations are not allowed")


def x__reject_unsafe_xml__mutmut_2(text: str, source: str) -> None:
    """Reject DTD/entity declarations before any parser runs (XXE guard)."""
    lowered = text.upper()
    if "<!doctype" in lowered or "<!entity" in lowered:
        raise ValueError(f"unsafe coverage XML at {source}: DTD/entity declarations are not allowed")


def x__reject_unsafe_xml__mutmut_3(text: str, source: str) -> None:
    """Reject DTD/entity declarations before any parser runs (XXE guard)."""
    lowered = text.lower()
    if "<!doctype" in lowered and "<!entity" in lowered:
        raise ValueError(f"unsafe coverage XML at {source}: DTD/entity declarations are not allowed")


def x__reject_unsafe_xml__mutmut_4(text: str, source: str) -> None:
    """Reject DTD/entity declarations before any parser runs (XXE guard)."""
    lowered = text.lower()
    if "XX<!doctypeXX" in lowered or "<!entity" in lowered:
        raise ValueError(f"unsafe coverage XML at {source}: DTD/entity declarations are not allowed")


def x__reject_unsafe_xml__mutmut_5(text: str, source: str) -> None:
    """Reject DTD/entity declarations before any parser runs (XXE guard)."""
    lowered = text.lower()
    if "<!DOCTYPE" in lowered or "<!entity" in lowered:
        raise ValueError(f"unsafe coverage XML at {source}: DTD/entity declarations are not allowed")


def x__reject_unsafe_xml__mutmut_6(text: str, source: str) -> None:
    """Reject DTD/entity declarations before any parser runs (XXE guard)."""
    lowered = text.lower()
    if "<!doctype" not in lowered or "<!entity" in lowered:
        raise ValueError(f"unsafe coverage XML at {source}: DTD/entity declarations are not allowed")


def x__reject_unsafe_xml__mutmut_7(text: str, source: str) -> None:
    """Reject DTD/entity declarations before any parser runs (XXE guard)."""
    lowered = text.lower()
    if "<!doctype" in lowered or "XX<!entityXX" in lowered:
        raise ValueError(f"unsafe coverage XML at {source}: DTD/entity declarations are not allowed")


def x__reject_unsafe_xml__mutmut_8(text: str, source: str) -> None:
    """Reject DTD/entity declarations before any parser runs (XXE guard)."""
    lowered = text.lower()
    if "<!doctype" in lowered or "<!ENTITY" in lowered:
        raise ValueError(f"unsafe coverage XML at {source}: DTD/entity declarations are not allowed")


def x__reject_unsafe_xml__mutmut_9(text: str, source: str) -> None:
    """Reject DTD/entity declarations before any parser runs (XXE guard)."""
    lowered = text.lower()
    if "<!doctype" in lowered or "<!entity" not in lowered:
        raise ValueError(f"unsafe coverage XML at {source}: DTD/entity declarations are not allowed")


def x__reject_unsafe_xml__mutmut_10(text: str, source: str) -> None:
    """Reject DTD/entity declarations before any parser runs (XXE guard)."""
    lowered = text.lower()
    if "<!doctype" in lowered or "<!entity" in lowered:
        raise ValueError(None)

mutants_x__reject_unsafe_xml__mutmut['_mutmut_orig'] = x__reject_unsafe_xml__mutmut_orig # type: ignore # mutmut generated
mutants_x__reject_unsafe_xml__mutmut['x__reject_unsafe_xml__mutmut_1'] = x__reject_unsafe_xml__mutmut_1 # type: ignore # mutmut generated
mutants_x__reject_unsafe_xml__mutmut['x__reject_unsafe_xml__mutmut_2'] = x__reject_unsafe_xml__mutmut_2 # type: ignore # mutmut generated
mutants_x__reject_unsafe_xml__mutmut['x__reject_unsafe_xml__mutmut_3'] = x__reject_unsafe_xml__mutmut_3 # type: ignore # mutmut generated
mutants_x__reject_unsafe_xml__mutmut['x__reject_unsafe_xml__mutmut_4'] = x__reject_unsafe_xml__mutmut_4 # type: ignore # mutmut generated
mutants_x__reject_unsafe_xml__mutmut['x__reject_unsafe_xml__mutmut_5'] = x__reject_unsafe_xml__mutmut_5 # type: ignore # mutmut generated
mutants_x__reject_unsafe_xml__mutmut['x__reject_unsafe_xml__mutmut_6'] = x__reject_unsafe_xml__mutmut_6 # type: ignore # mutmut generated
mutants_x__reject_unsafe_xml__mutmut['x__reject_unsafe_xml__mutmut_7'] = x__reject_unsafe_xml__mutmut_7 # type: ignore # mutmut generated
mutants_x__reject_unsafe_xml__mutmut['x__reject_unsafe_xml__mutmut_8'] = x__reject_unsafe_xml__mutmut_8 # type: ignore # mutmut generated
mutants_x__reject_unsafe_xml__mutmut['x__reject_unsafe_xml__mutmut_9'] = x__reject_unsafe_xml__mutmut_9 # type: ignore # mutmut generated
mutants_x__reject_unsafe_xml__mutmut['x__reject_unsafe_xml__mutmut_10'] = x__reject_unsafe_xml__mutmut_10 # type: ignore # mutmut generated
mutants_x__resolve_element_tree__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__resolve_element_tree__mutmut)
def _resolve_element_tree(
    import_module: Callable[[str], ModuleType] = importlib.import_module,
) -> Any:
    """Prefer defusedxml; fall back to stdlib after explicit DTD/entity rejection.

    ``import_module`` is a DI seam so a test can drive either path without
    monkeypatching the production module.
    """
    try:
        from defusedxml import ElementTree as DefusedET

        return DefusedET
    except ImportError:
        return import_module("xml.etree.ElementTree")


def x__resolve_element_tree__mutmut_orig(
    import_module: Callable[[str], ModuleType] = importlib.import_module,
) -> Any:
    """Prefer defusedxml; fall back to stdlib after explicit DTD/entity rejection.

    ``import_module`` is a DI seam so a test can drive either path without
    monkeypatching the production module.
    """
    try:
        from defusedxml import ElementTree as DefusedET

        return DefusedET
    except ImportError:
        return import_module("xml.etree.ElementTree")


def x__resolve_element_tree__mutmut_1(
    import_module: Callable[[str], ModuleType] = importlib.import_module,
) -> Any:
    """Prefer defusedxml; fall back to stdlib after explicit DTD/entity rejection.

    ``import_module`` is a DI seam so a test can drive either path without
    monkeypatching the production module.
    """
    try:
        from defusedxml import ElementTree as DefusedET

        return DefusedET
    except ImportError:
        return import_module(None)


def x__resolve_element_tree__mutmut_2(
    import_module: Callable[[str], ModuleType] = importlib.import_module,
) -> Any:
    """Prefer defusedxml; fall back to stdlib after explicit DTD/entity rejection.

    ``import_module`` is a DI seam so a test can drive either path without
    monkeypatching the production module.
    """
    try:
        from defusedxml import ElementTree as DefusedET

        return DefusedET
    except ImportError:
        return import_module("XXxml.etree.ElementTreeXX")


def x__resolve_element_tree__mutmut_3(
    import_module: Callable[[str], ModuleType] = importlib.import_module,
) -> Any:
    """Prefer defusedxml; fall back to stdlib after explicit DTD/entity rejection.

    ``import_module`` is a DI seam so a test can drive either path without
    monkeypatching the production module.
    """
    try:
        from defusedxml import ElementTree as DefusedET

        return DefusedET
    except ImportError:
        return import_module("xml.etree.elementtree")


def x__resolve_element_tree__mutmut_4(
    import_module: Callable[[str], ModuleType] = importlib.import_module,
) -> Any:
    """Prefer defusedxml; fall back to stdlib after explicit DTD/entity rejection.

    ``import_module`` is a DI seam so a test can drive either path without
    monkeypatching the production module.
    """
    try:
        from defusedxml import ElementTree as DefusedET

        return DefusedET
    except ImportError:
        return import_module("XML.ETREE.ELEMENTTREE")

mutants_x__resolve_element_tree__mutmut['_mutmut_orig'] = x__resolve_element_tree__mutmut_orig # type: ignore # mutmut generated
mutants_x__resolve_element_tree__mutmut['x__resolve_element_tree__mutmut_1'] = x__resolve_element_tree__mutmut_1 # type: ignore # mutmut generated
mutants_x__resolve_element_tree__mutmut['x__resolve_element_tree__mutmut_2'] = x__resolve_element_tree__mutmut_2 # type: ignore # mutmut generated
mutants_x__resolve_element_tree__mutmut['x__resolve_element_tree__mutmut_3'] = x__resolve_element_tree__mutmut_3 # type: ignore # mutmut generated
mutants_x__resolve_element_tree__mutmut['x__resolve_element_tree__mutmut_4'] = x__resolve_element_tree__mutmut_4 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_parse_coverage_report__mutmut)
def parse_coverage_report(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_orig(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_1(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_2(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = None
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_3(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding=None)
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_4(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="XXutf-8XX")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_5(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="UTF-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_6(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(None, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_7(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, None)
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_8(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_9(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, )
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_10(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(None))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_11(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = None
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_12(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_13(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = None

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_14(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(None).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_15(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = None

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_16(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter(None) if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_17(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("XXsourceXX") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_18(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("SOURCE") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_19(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text or s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_20(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = None
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_21(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter(None):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_22(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("XXclassXX"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_23(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("CLASS"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_24(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = None
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_25(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") and ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_26(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get(None) or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_27(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("XXfilenameXX") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_28(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("FILENAME") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_29(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or "XXXX"
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_30(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_31(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            break
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_32(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = None
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_33(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(None, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_34(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, None, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_35(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=None)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_36(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_37(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_38(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, )
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_39(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = None
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_40(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) / 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_41(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(None) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_42(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get(None, "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_43(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", None)) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_44(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_45(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", )) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_46(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("XXline-rateXX", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_47(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("LINE-RATE", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_48(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "XX1.0XX")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_49(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 101.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_50(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            break
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_51(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = None
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_52(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(None)
        if prev is None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_53(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None and rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_54(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is not None or rate < prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_55(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate <= prev:
            out[full] = rate
    return out


def x_parse_coverage_report__mutmut_56(
    report_path: Path,
    *,
    repo_root: Path | None = None,
    element_tree: Any | None = None,
) -> dict[str, float]:
    """Return ``{<source>/<filename>: line-rate-percent}`` from a Cobertura report.

    Cobertura XML declares ``<source>`` roots and emits ``<class filename=...>``
    paths relative to a source. The returned keys resolve absolute, relative and
    multiple source roots to repository-relative paths. Existing files
    disambiguate multiple roots; unresolved ambiguity fails. When multiple
    classes resolve to one key, the LOWEST line-rate wins (the pessimistic
    reading). A missing report yields an empty mapping; the rule treats that as
    missing required evidence.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip() for s in root.iter("source") if s.text and s.text.strip()]

    out: dict[str, float] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        full = resolve_coverage_filename(filename, source_roots, repo_root=repo_root)
        try:
            rate = float(cls.get("line-rate", "1.0")) * 100.0
        except ValueError:
            continue
        prev = out.get(full)
        if prev is None or rate < prev:
            out[full] = None
    return out

mutants_x_parse_coverage_report__mutmut['_mutmut_orig'] = x_parse_coverage_report__mutmut_orig # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_1'] = x_parse_coverage_report__mutmut_1 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_2'] = x_parse_coverage_report__mutmut_2 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_3'] = x_parse_coverage_report__mutmut_3 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_4'] = x_parse_coverage_report__mutmut_4 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_5'] = x_parse_coverage_report__mutmut_5 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_6'] = x_parse_coverage_report__mutmut_6 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_7'] = x_parse_coverage_report__mutmut_7 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_8'] = x_parse_coverage_report__mutmut_8 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_9'] = x_parse_coverage_report__mutmut_9 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_10'] = x_parse_coverage_report__mutmut_10 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_11'] = x_parse_coverage_report__mutmut_11 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_12'] = x_parse_coverage_report__mutmut_12 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_13'] = x_parse_coverage_report__mutmut_13 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_14'] = x_parse_coverage_report__mutmut_14 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_15'] = x_parse_coverage_report__mutmut_15 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_16'] = x_parse_coverage_report__mutmut_16 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_17'] = x_parse_coverage_report__mutmut_17 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_18'] = x_parse_coverage_report__mutmut_18 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_19'] = x_parse_coverage_report__mutmut_19 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_20'] = x_parse_coverage_report__mutmut_20 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_21'] = x_parse_coverage_report__mutmut_21 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_22'] = x_parse_coverage_report__mutmut_22 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_23'] = x_parse_coverage_report__mutmut_23 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_24'] = x_parse_coverage_report__mutmut_24 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_25'] = x_parse_coverage_report__mutmut_25 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_26'] = x_parse_coverage_report__mutmut_26 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_27'] = x_parse_coverage_report__mutmut_27 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_28'] = x_parse_coverage_report__mutmut_28 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_29'] = x_parse_coverage_report__mutmut_29 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_30'] = x_parse_coverage_report__mutmut_30 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_31'] = x_parse_coverage_report__mutmut_31 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_32'] = x_parse_coverage_report__mutmut_32 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_33'] = x_parse_coverage_report__mutmut_33 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_34'] = x_parse_coverage_report__mutmut_34 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_35'] = x_parse_coverage_report__mutmut_35 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_36'] = x_parse_coverage_report__mutmut_36 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_37'] = x_parse_coverage_report__mutmut_37 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_38'] = x_parse_coverage_report__mutmut_38 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_39'] = x_parse_coverage_report__mutmut_39 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_40'] = x_parse_coverage_report__mutmut_40 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_41'] = x_parse_coverage_report__mutmut_41 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_42'] = x_parse_coverage_report__mutmut_42 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_43'] = x_parse_coverage_report__mutmut_43 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_44'] = x_parse_coverage_report__mutmut_44 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_45'] = x_parse_coverage_report__mutmut_45 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_46'] = x_parse_coverage_report__mutmut_46 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_47'] = x_parse_coverage_report__mutmut_47 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_48'] = x_parse_coverage_report__mutmut_48 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_49'] = x_parse_coverage_report__mutmut_49 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_50'] = x_parse_coverage_report__mutmut_50 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_51'] = x_parse_coverage_report__mutmut_51 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_52'] = x_parse_coverage_report__mutmut_52 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_53'] = x_parse_coverage_report__mutmut_53 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_54'] = x_parse_coverage_report__mutmut_54 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_55'] = x_parse_coverage_report__mutmut_55 # type: ignore # mutmut generated
mutants_x_parse_coverage_report__mutmut['x_parse_coverage_report__mutmut_56'] = x_parse_coverage_report__mutmut_56 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_parse_coverage_details__mutmut)
def parse_coverage_details(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_orig(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_1(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = None
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_2(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding=None)
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_3(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="XXutf-8XX")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_4(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="UTF-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_5(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(None, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_6(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, None)
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_7(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_8(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, )
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_9(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(None))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_10(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = None
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_11(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(None)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_12(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag == "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_13(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "XXcoverageXX":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_14(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "COVERAGE":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_15(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError(None)
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_16(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("XXexpected a Cobertura coverage reportXX")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_17(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_18(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("EXPECTED A COBERTURA COVERAGE REPORT")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_19(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = None
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_20(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter(None) if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_21(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("XXsourceXX") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_22(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("SOURCE") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_23(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text or node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_24(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = None
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_25(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter(None):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_26(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("XXclassXX"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_27(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("CLASS"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_28(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = None
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_29(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get(None)
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_30(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("XXfilenameXX")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_31(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("FILENAME")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_32(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_33(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError(None)
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_34(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("XXcoverage class is missing its source filenameXX")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_35(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("COVERAGE CLASS IS MISSING ITS SOURCE FILENAME")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_36(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = None
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_37(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(None, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_38(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, None, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_39(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=None)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_40(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_41(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_42(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, )
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_43(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative not in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_44(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError(None)
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_45(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("XXduplicate source file in coverage reportXX")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_46(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("DUPLICATE SOURCE FILE IN COVERAGE REPORT")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_47(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = None
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_48(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(None, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_49(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, None)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_50(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_51(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, )
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_52(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root * relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_53(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_54(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError(None)
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_55(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("XXempty coverage reportXX")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_56(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("EMPTY COVERAGE REPORT")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_57(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("XXlinesXX", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_58(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("LINES", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_59(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "XXlinesXX", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_60(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "LINES", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_61(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "XXcovered_linesXX"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_62(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "COVERED_LINES"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_63(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("XXbranchesXX", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_64(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("BRANCHES", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_65(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "XXbranchesXX", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_66(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "BRANCHES", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_67(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "XXcovered_branchesXX"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_68(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "COVERED_BRANCHES"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_69(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = None
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_70(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(None)
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_71(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(None, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_72(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, None) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_73(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_74(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, ) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_75(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = None
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_76(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(None)
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_77(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(None, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_78(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, None) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_79(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_80(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, ) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_81(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total and coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_82(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(None) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_83(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(None)) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_84(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) == total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_85(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(None) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_86(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(None)) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_87(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) == covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_88(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError(None)
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_89(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("XXcoverage report totals disagree with file detailXX")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_90(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("COVERAGE REPORT TOTALS DISAGREE WITH FILE DETAIL")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_91(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(None, covered, total)
    return result


def x_parse_coverage_details__mutmut_92(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), None, total)
    return result


def x_parse_coverage_details__mutmut_93(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, None)
    return result


def x_parse_coverage_details__mutmut_94(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(covered, total)
    return result


def x_parse_coverage_details__mutmut_95(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), total)
    return result


def x_parse_coverage_details__mutmut_96(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "branch-rate"), covered, )
    return result


def x_parse_coverage_details__mutmut_97(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get(None), covered, total)
    return result


def x_parse_coverage_details__mutmut_98(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("XXline-rateXX" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_99(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("LINE-RATE" if prefix == "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_100(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix != "lines" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_101(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "XXlinesXX" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_102(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "LINES" else "branch-rate"), covered, total)
    return result


def x_parse_coverage_details__mutmut_103(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "XXbranch-rateXX"), covered, total)
    return result


def x_parse_coverage_details__mutmut_104(report_path: Path, *, repo_root: Path) -> dict[str, CoverageCounts]:
    """Read complete, count-consistent Cobertura detail for strict admission."""
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    root = _resolve_element_tree().fromstring(text)
    if root.tag != "coverage":
        raise ValueError("expected a Cobertura coverage report")
    sources = [node.text.strip() for node in root.iter("source") if node.text and node.text.strip()]
    result: dict[str, CoverageCounts] = {}
    for element in root.iter("class"):
        filename = element.get("filename")
        if not filename:
            raise ValueError("coverage class is missing its source filename")
        relative = resolve_coverage_filename(filename, sources, repo_root=repo_root)
        if relative in result:
            raise ValueError("duplicate source file in coverage report")
        result[relative] = count_class_coverage(element, repo_root / relative)
    if not result:
        raise ValueError("empty coverage report")
    for prefix, total_attr, covered_attr in (
        ("lines", "lines", "covered_lines"),
        ("branches", "branches", "covered_branches"),
    ):
        total = sum(getattr(counts, total_attr) for counts in result.values())
        covered = sum(getattr(counts, covered_attr) for counts in result.values())
        if (
            coverage_integer(root.get(f"{prefix}-valid")) != total
            or coverage_integer(root.get(f"{prefix}-covered")) != covered
        ):
            raise ValueError("coverage report totals disagree with file detail")
        validate_coverage_rate(root.get("line-rate" if prefix == "lines" else "BRANCH-RATE"), covered, total)
    return result

mutants_x_parse_coverage_details__mutmut['_mutmut_orig'] = x_parse_coverage_details__mutmut_orig # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_1'] = x_parse_coverage_details__mutmut_1 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_2'] = x_parse_coverage_details__mutmut_2 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_3'] = x_parse_coverage_details__mutmut_3 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_4'] = x_parse_coverage_details__mutmut_4 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_5'] = x_parse_coverage_details__mutmut_5 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_6'] = x_parse_coverage_details__mutmut_6 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_7'] = x_parse_coverage_details__mutmut_7 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_8'] = x_parse_coverage_details__mutmut_8 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_9'] = x_parse_coverage_details__mutmut_9 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_10'] = x_parse_coverage_details__mutmut_10 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_11'] = x_parse_coverage_details__mutmut_11 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_12'] = x_parse_coverage_details__mutmut_12 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_13'] = x_parse_coverage_details__mutmut_13 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_14'] = x_parse_coverage_details__mutmut_14 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_15'] = x_parse_coverage_details__mutmut_15 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_16'] = x_parse_coverage_details__mutmut_16 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_17'] = x_parse_coverage_details__mutmut_17 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_18'] = x_parse_coverage_details__mutmut_18 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_19'] = x_parse_coverage_details__mutmut_19 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_20'] = x_parse_coverage_details__mutmut_20 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_21'] = x_parse_coverage_details__mutmut_21 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_22'] = x_parse_coverage_details__mutmut_22 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_23'] = x_parse_coverage_details__mutmut_23 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_24'] = x_parse_coverage_details__mutmut_24 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_25'] = x_parse_coverage_details__mutmut_25 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_26'] = x_parse_coverage_details__mutmut_26 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_27'] = x_parse_coverage_details__mutmut_27 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_28'] = x_parse_coverage_details__mutmut_28 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_29'] = x_parse_coverage_details__mutmut_29 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_30'] = x_parse_coverage_details__mutmut_30 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_31'] = x_parse_coverage_details__mutmut_31 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_32'] = x_parse_coverage_details__mutmut_32 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_33'] = x_parse_coverage_details__mutmut_33 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_34'] = x_parse_coverage_details__mutmut_34 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_35'] = x_parse_coverage_details__mutmut_35 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_36'] = x_parse_coverage_details__mutmut_36 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_37'] = x_parse_coverage_details__mutmut_37 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_38'] = x_parse_coverage_details__mutmut_38 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_39'] = x_parse_coverage_details__mutmut_39 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_40'] = x_parse_coverage_details__mutmut_40 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_41'] = x_parse_coverage_details__mutmut_41 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_42'] = x_parse_coverage_details__mutmut_42 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_43'] = x_parse_coverage_details__mutmut_43 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_44'] = x_parse_coverage_details__mutmut_44 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_45'] = x_parse_coverage_details__mutmut_45 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_46'] = x_parse_coverage_details__mutmut_46 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_47'] = x_parse_coverage_details__mutmut_47 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_48'] = x_parse_coverage_details__mutmut_48 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_49'] = x_parse_coverage_details__mutmut_49 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_50'] = x_parse_coverage_details__mutmut_50 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_51'] = x_parse_coverage_details__mutmut_51 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_52'] = x_parse_coverage_details__mutmut_52 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_53'] = x_parse_coverage_details__mutmut_53 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_54'] = x_parse_coverage_details__mutmut_54 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_55'] = x_parse_coverage_details__mutmut_55 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_56'] = x_parse_coverage_details__mutmut_56 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_57'] = x_parse_coverage_details__mutmut_57 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_58'] = x_parse_coverage_details__mutmut_58 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_59'] = x_parse_coverage_details__mutmut_59 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_60'] = x_parse_coverage_details__mutmut_60 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_61'] = x_parse_coverage_details__mutmut_61 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_62'] = x_parse_coverage_details__mutmut_62 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_63'] = x_parse_coverage_details__mutmut_63 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_64'] = x_parse_coverage_details__mutmut_64 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_65'] = x_parse_coverage_details__mutmut_65 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_66'] = x_parse_coverage_details__mutmut_66 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_67'] = x_parse_coverage_details__mutmut_67 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_68'] = x_parse_coverage_details__mutmut_68 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_69'] = x_parse_coverage_details__mutmut_69 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_70'] = x_parse_coverage_details__mutmut_70 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_71'] = x_parse_coverage_details__mutmut_71 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_72'] = x_parse_coverage_details__mutmut_72 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_73'] = x_parse_coverage_details__mutmut_73 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_74'] = x_parse_coverage_details__mutmut_74 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_75'] = x_parse_coverage_details__mutmut_75 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_76'] = x_parse_coverage_details__mutmut_76 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_77'] = x_parse_coverage_details__mutmut_77 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_78'] = x_parse_coverage_details__mutmut_78 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_79'] = x_parse_coverage_details__mutmut_79 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_80'] = x_parse_coverage_details__mutmut_80 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_81'] = x_parse_coverage_details__mutmut_81 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_82'] = x_parse_coverage_details__mutmut_82 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_83'] = x_parse_coverage_details__mutmut_83 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_84'] = x_parse_coverage_details__mutmut_84 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_85'] = x_parse_coverage_details__mutmut_85 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_86'] = x_parse_coverage_details__mutmut_86 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_87'] = x_parse_coverage_details__mutmut_87 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_88'] = x_parse_coverage_details__mutmut_88 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_89'] = x_parse_coverage_details__mutmut_89 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_90'] = x_parse_coverage_details__mutmut_90 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_91'] = x_parse_coverage_details__mutmut_91 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_92'] = x_parse_coverage_details__mutmut_92 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_93'] = x_parse_coverage_details__mutmut_93 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_94'] = x_parse_coverage_details__mutmut_94 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_95'] = x_parse_coverage_details__mutmut_95 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_96'] = x_parse_coverage_details__mutmut_96 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_97'] = x_parse_coverage_details__mutmut_97 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_98'] = x_parse_coverage_details__mutmut_98 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_99'] = x_parse_coverage_details__mutmut_99 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_100'] = x_parse_coverage_details__mutmut_100 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_101'] = x_parse_coverage_details__mutmut_101 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_102'] = x_parse_coverage_details__mutmut_102 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_103'] = x_parse_coverage_details__mutmut_103 # type: ignore # mutmut generated
mutants_x_parse_coverage_details__mutmut['x_parse_coverage_details__mutmut_104'] = x_parse_coverage_details__mutmut_104 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCoverageFloorǁ_report_path__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCoverageFloorǁenumerate_files__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCoverageFloorǁis_in_scope__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCoverageFloorǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCoverageFloorǁrun__mutmut: MutantDict = {}  # type: ignore


class CoverageFloor(FitnessRule):
    """Flags source files whose recorded line coverage is below the floor."""

    name = "coverage-floor"
    remediation = REMEDIATION
    extensions = (".py",)

    #: Rule-specific knobs — instance attrs so ``from_config`` overrides them.
    floor_pct: float = DEFAULT_FLOOR_PCT
    coverage_report: str = DEFAULT_COVERAGE_REPORT
    branch_floor_pct: float | None = None
    critical_branch_files: frozenset[str] = frozenset()
    receipt_config: dict[str, Any] | None = None

    @classmethod
    @_mutmut_mutated(mutants_xǁCoverageFloorǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = None
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, )
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = None
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(None)
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get(None, DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", None))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get(DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", ))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("XXfloor_pctXX", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_13(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("FLOOR_PCT", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_14(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = None
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_15(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(None)
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_16(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get(None, DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_17(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", None))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_18(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get(DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_19(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", ))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_20(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("XXcoverage_reportXX", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_21(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("COVERAGE_REPORT", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_22(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "XXcoverage_receiptXX" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_23(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "COVERAGE_RECEIPT" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_24(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" not in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_25(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get(None) is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_26(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("XXbranch_floor_pctXX") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_27(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("BRANCH_FLOOR_PCT") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_28(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is not None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_29(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError(None)
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_30(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("XXcoverage receipt admission requires independent branch coverageXX")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_31(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("COVERAGE RECEIPT ADMISSION REQUIRES INDEPENDENT BRANCH COVERAGE")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_32(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = None
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_33(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(None)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_34(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = None
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_35(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get(None)
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_36(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("XXbranch_floor_pctXX")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_37(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("BRANCH_FLOOR_PCT")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_38(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = None
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_39(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get(None, [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_40(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", None)
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_41(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get([])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_42(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", )
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_43(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("XXcritical_branch_filesXX", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_44(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("CRITICAL_BRANCH_FILES", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_45(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) and any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_46(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_47(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(None):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_48(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_49(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError(None)
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_50(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("XXcritical_branch_files must be a list of repository-relative filesXX")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_51(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("CRITICAL_BRANCH_FILES MUST BE A LIST OF REPOSITORY-RELATIVE FILES")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_52(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = None
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_53(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(None)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_54(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_55(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = None
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_56(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(None)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_57(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("XXfloor_pctXX", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_58(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("FLOOR_PCT", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_59(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "XXbranch_floor_pctXX"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_60(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "BRANCH_FLOOR_PCT"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_61(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = None
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_62(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(None, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_63(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, None)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_64(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_65(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, )
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_66(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value) and not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_67(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float) and not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_68(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool) and not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_69(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_70(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_71(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(None)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_72(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_73(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 1 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_74(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 < value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_75(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value < 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_76(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 101
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_77(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(None)
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_78(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots and rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_79(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_80(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions == (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_81(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != ("XX.pyXX",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_82(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".PY",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_83(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError(None)
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_84(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("XXstrict coverage requires source roots and Python filesXX")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_85(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_86(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("STRICT COVERAGE REQUIRES SOURCE ROOTS AND PYTHON FILES")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_87(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = None
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_88(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = None
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_89(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(None)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_90(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = None
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_91(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root * source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_92(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir() and not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_93(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts and not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_94(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute() and ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_95(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or "XX..XX" in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_96(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." not in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_97(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_98(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_99(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(None)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_100(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError(None)
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_101(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("XXstrict coverage requires existing repository-relative source rootsXX")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_102(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("STRICT COVERAGE REQUIRES EXISTING REPOSITORY-RELATIVE SOURCE ROOTS")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_103(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(None)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_104(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = None
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_105(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = None
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_106(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(None)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_107(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = None
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_108(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root * path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_109(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots) and not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_110(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py" and not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_111(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts and path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_112(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute() and ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_113(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or "XX..XX" in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_114(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." not in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_115(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix == ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_116(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != "XX.pyXX"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_117(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".PY"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_118(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_119(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(None)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_120(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(None) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_121(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_122(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        None
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_123(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "XXcritical branch file must exist within the measured Python source rootsXX"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_124(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_125(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "CRITICAL BRANCH FILE MUST EXIST WITHIN THE MEASURED PYTHON SOURCE ROOTS"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_126(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(None)
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_127(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(None).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_128(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = None
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_129(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(None)
        elif critical:
            raise ValueError("critical branch files require branch_floor_pct")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_130(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError(None)
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_131(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("XXcritical branch files require branch_floor_pctXX")
        return rule

    @classmethod
    def xǁCoverageFloorǁfrom_config__mutmut_132(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageFloor:
        """Build from config, also reading ``floor_pct`` and ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageFloor)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        if "coverage_receipt" in config:
            if config.get("branch_floor_pct") is None:
                raise ValueError("coverage receipt admission requires independent branch coverage")
            rule.receipt_config = dict(config)
        branch_floor = config.get("branch_floor_pct")
        critical = config.get("critical_branch_files", [])
        if not isinstance(critical, list) or any(not isinstance(path, str) for path in critical):
            raise ValueError("critical_branch_files must be a list of repository-relative files")
        rule.critical_branch_files = frozenset(critical)
        if branch_floor is not None:
            rule.branch_floor_pct = float(branch_floor)
            for name in ("floor_pct", "branch_floor_pct"):
                value = config.get(name, DEFAULT_FLOOR_PCT)
                if (
                    isinstance(value, bool)
                    or not isinstance(value, int | float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 100
                ):
                    raise ValueError(f"{name} must be a finite percentage between zero and 100")
            if not rule._roots or rule._extensions != (".py",):
                raise ValueError("strict coverage requires source roots and Python files")
            measured_roots: set[Path] = set()
            for source_root in rule._roots:
                source = Path(source_root)
                resolved = (rule._repo_root / source).resolve()
                if (
                    source.is_absolute()
                    or ".." in source.parts
                    or not resolved.is_dir()
                    or not resolved.is_relative_to(rule._repo_root)
                ):
                    raise ValueError("strict coverage requires existing repository-relative source roots")
                measured_roots.add(resolved)
            critical_files: set[str] = set()
            for relative in rule.critical_branch_files:
                path = Path(relative)
                resolved = (rule._repo_root / path).resolve()
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or path.suffix != ".py"
                    or not any(resolved.is_relative_to(root) for root in measured_roots)
                    or not resolved.is_file()
                ):
                    raise ValueError(
                        "critical branch file must exist within the measured Python source roots"
                    )
                critical_files.add(resolved.relative_to(rule._repo_root).as_posix())
            rule.critical_branch_files = frozenset(critical_files)
        elif critical:
            raise ValueError("CRITICAL BRANCH FILES REQUIRE BRANCH_FLOOR_PCT")
        return rule

    @_mutmut_mutated(mutants_xǁCoverageFloorǁ_report_path__mutmut)
    def _report_path(self) -> Path:
        if self.receipt_config is not None:
            from tc_fitness.coverage_admission import configured

            report = Path(configured(self.coverage_report))
        else:
            report = Path(self.coverage_report)
        return report if report.is_absolute() else self._repo_root / report

    def xǁCoverageFloorǁ_report_path__mutmut_orig(self) -> Path:
        if self.receipt_config is not None:
            from tc_fitness.coverage_admission import configured

            report = Path(configured(self.coverage_report))
        else:
            report = Path(self.coverage_report)
        return report if report.is_absolute() else self._repo_root / report

    def xǁCoverageFloorǁ_report_path__mutmut_1(self) -> Path:
        if self.receipt_config is None:
            from tc_fitness.coverage_admission import configured

            report = Path(configured(self.coverage_report))
        else:
            report = Path(self.coverage_report)
        return report if report.is_absolute() else self._repo_root / report

    def xǁCoverageFloorǁ_report_path__mutmut_2(self) -> Path:
        if self.receipt_config is not None:
            from tc_fitness.coverage_admission import configured

            report = None
        else:
            report = Path(self.coverage_report)
        return report if report.is_absolute() else self._repo_root / report

    def xǁCoverageFloorǁ_report_path__mutmut_3(self) -> Path:
        if self.receipt_config is not None:
            from tc_fitness.coverage_admission import configured

            report = Path(None)
        else:
            report = Path(self.coverage_report)
        return report if report.is_absolute() else self._repo_root / report

    def xǁCoverageFloorǁ_report_path__mutmut_4(self) -> Path:
        if self.receipt_config is not None:
            from tc_fitness.coverage_admission import configured

            report = Path(configured(None))
        else:
            report = Path(self.coverage_report)
        return report if report.is_absolute() else self._repo_root / report

    def xǁCoverageFloorǁ_report_path__mutmut_5(self) -> Path:
        if self.receipt_config is not None:
            from tc_fitness.coverage_admission import configured

            report = Path(configured(self.coverage_report))
        else:
            report = None
        return report if report.is_absolute() else self._repo_root / report

    def xǁCoverageFloorǁ_report_path__mutmut_6(self) -> Path:
        if self.receipt_config is not None:
            from tc_fitness.coverage_admission import configured

            report = Path(configured(self.coverage_report))
        else:
            report = Path(None)
        return report if report.is_absolute() else self._repo_root / report

    def xǁCoverageFloorǁ_report_path__mutmut_7(self) -> Path:
        if self.receipt_config is not None:
            from tc_fitness.coverage_admission import configured

            report = Path(configured(self.coverage_report))
        else:
            report = Path(self.coverage_report)
        return report if report.is_absolute() else self._repo_root * report

    @cached_property
    def _coverage(self) -> dict[str, float]:
        return parse_coverage_report(self._report_path(), repo_root=self._repo_root)

    @cached_property
    def _details(self) -> dict[str, CoverageCounts]:
        return parse_coverage_details(self._report_path(), repo_root=self._repo_root)

    @cached_property
    def _strict_failures(self) -> dict[str, str]:
        details = self._details
        # Include untracked/new source too; Git tracking cannot make the
        # current package disappear from complete-source measurement.
        sources = {
            path
            for source in self._roots
            for path in (self._repo_root / source).rglob("*.py")
            if path.is_file()
        }
        if not sources:
            raise ValueError("strict coverage source roots contain no Python files")
        failures: dict[str, str] = {}
        for path in sorted(sources):
            relative = self._repo_relative(path).as_posix()
            counts = details.get(relative)
            if counts is None:
                failures[relative] = "missing coverage detail for source file"
                continue
            messages = []
            if counts.line_pct < self.floor_pct:
                messages.append(f"line coverage {counts.line_pct:g}% below {self.floor_pct:g}%")
            branch_floor = 100.0 if relative in self.critical_branch_files else self.branch_floor_pct
            if branch_floor is not None and counts.branch_pct < branch_floor:
                prefix = "critical branch" if relative in self.critical_branch_files else "branch"
                messages.append(f"{prefix} coverage {counts.branch_pct:g}% below {branch_floor:g}%")
            if messages:
                failures[relative] = "; ".join(messages)
        return failures

    @_mutmut_mutated(mutants_xǁCoverageFloorǁenumerate_files__mutmut)
    def enumerate_files(self) -> list[Path]:
        """Enumerate the below-floor files named in the coverage report.

        The source tree is authoritative. A report cannot hide an uncovered
        file by omitting it. A missing or empty report is represented by the
        report path itself so it produces an observable finding.
        """
        if self.branch_floor_pct is not None:
            return [self._repo_root / relative for relative in self._strict_failures]
        if not self._coverage:
            return [self._report_path()]
        return super().enumerate_files()

    def xǁCoverageFloorǁenumerate_files__mutmut_orig(self) -> list[Path]:
        """Enumerate the below-floor files named in the coverage report.

        The source tree is authoritative. A report cannot hide an uncovered
        file by omitting it. A missing or empty report is represented by the
        report path itself so it produces an observable finding.
        """
        if self.branch_floor_pct is not None:
            return [self._repo_root / relative for relative in self._strict_failures]
        if not self._coverage:
            return [self._report_path()]
        return super().enumerate_files()

    def xǁCoverageFloorǁenumerate_files__mutmut_1(self) -> list[Path]:
        """Enumerate the below-floor files named in the coverage report.

        The source tree is authoritative. A report cannot hide an uncovered
        file by omitting it. A missing or empty report is represented by the
        report path itself so it produces an observable finding.
        """
        if self.branch_floor_pct is None:
            return [self._repo_root / relative for relative in self._strict_failures]
        if not self._coverage:
            return [self._report_path()]
        return super().enumerate_files()

    def xǁCoverageFloorǁenumerate_files__mutmut_2(self) -> list[Path]:
        """Enumerate the below-floor files named in the coverage report.

        The source tree is authoritative. A report cannot hide an uncovered
        file by omitting it. A missing or empty report is represented by the
        report path itself so it produces an observable finding.
        """
        if self.branch_floor_pct is not None:
            return [self._repo_root * relative for relative in self._strict_failures]
        if not self._coverage:
            return [self._report_path()]
        return super().enumerate_files()

    def xǁCoverageFloorǁenumerate_files__mutmut_3(self) -> list[Path]:
        """Enumerate the below-floor files named in the coverage report.

        The source tree is authoritative. A report cannot hide an uncovered
        file by omitting it. A missing or empty report is represented by the
        report path itself so it produces an observable finding.
        """
        if self.branch_floor_pct is not None:
            return [self._repo_root / relative for relative in self._strict_failures]
        if self._coverage:
            return [self._report_path()]
        return super().enumerate_files()

    @_mutmut_mutated(mutants_xǁCoverageFloorǁis_in_scope__mutmut)
    def is_in_scope(self, rel: str) -> bool:
        report_rel = self._repo_relative(self._report_path()).as_posix()
        return rel == report_rel or super().is_in_scope(rel)

    def xǁCoverageFloorǁis_in_scope__mutmut_orig(self, rel: str) -> bool:
        report_rel = self._repo_relative(self._report_path()).as_posix()
        return rel == report_rel or super().is_in_scope(rel)

    def xǁCoverageFloorǁis_in_scope__mutmut_1(self, rel: str) -> bool:
        report_rel = None
        return rel == report_rel or super().is_in_scope(rel)

    def xǁCoverageFloorǁis_in_scope__mutmut_2(self, rel: str) -> bool:
        report_rel = self._repo_relative(None).as_posix()
        return rel == report_rel or super().is_in_scope(rel)

    def xǁCoverageFloorǁis_in_scope__mutmut_3(self, rel: str) -> bool:
        report_rel = self._repo_relative(self._report_path()).as_posix()
        return rel == report_rel and super().is_in_scope(rel)

    def xǁCoverageFloorǁis_in_scope__mutmut_4(self, rel: str) -> bool:
        report_rel = self._repo_relative(self._report_path()).as_posix()
        return rel != report_rel or super().is_in_scope(rel)

    def xǁCoverageFloorǁis_in_scope__mutmut_5(self, rel: str) -> bool:
        report_rel = self._repo_relative(self._report_path()).as_posix()
        return rel == report_rel or super().is_in_scope(None)

    @_mutmut_mutated(mutants_xǁCoverageFloorǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        """The report is absent/empty, or a source file is absent/below floor."""
        rel = self._repo_relative(path).as_posix()
        if self.branch_floor_pct is not None:
            return rel in self._strict_failures
        report_rel = self._repo_relative(self._report_path()).as_posix()
        if rel == report_rel:
            return not self._coverage
        measured = self._coverage.get(rel)
        return measured is None or measured < self.floor_pct

    def xǁCoverageFloorǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        """The report is absent/empty, or a source file is absent/below floor."""
        rel = self._repo_relative(path).as_posix()
        if self.branch_floor_pct is not None:
            return rel in self._strict_failures
        report_rel = self._repo_relative(self._report_path()).as_posix()
        if rel == report_rel:
            return not self._coverage
        measured = self._coverage.get(rel)
        return measured is None or measured < self.floor_pct

    def xǁCoverageFloorǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        """The report is absent/empty, or a source file is absent/below floor."""
        rel = None
        if self.branch_floor_pct is not None:
            return rel in self._strict_failures
        report_rel = self._repo_relative(self._report_path()).as_posix()
        if rel == report_rel:
            return not self._coverage
        measured = self._coverage.get(rel)
        return measured is None or measured < self.floor_pct

    def xǁCoverageFloorǁfile_has_violation__mutmut_2(self, path: Path) -> bool:
        """The report is absent/empty, or a source file is absent/below floor."""
        rel = self._repo_relative(None).as_posix()
        if self.branch_floor_pct is not None:
            return rel in self._strict_failures
        report_rel = self._repo_relative(self._report_path()).as_posix()
        if rel == report_rel:
            return not self._coverage
        measured = self._coverage.get(rel)
        return measured is None or measured < self.floor_pct

    def xǁCoverageFloorǁfile_has_violation__mutmut_3(self, path: Path) -> bool:
        """The report is absent/empty, or a source file is absent/below floor."""
        rel = self._repo_relative(path).as_posix()
        if self.branch_floor_pct is None:
            return rel in self._strict_failures
        report_rel = self._repo_relative(self._report_path()).as_posix()
        if rel == report_rel:
            return not self._coverage
        measured = self._coverage.get(rel)
        return measured is None or measured < self.floor_pct

    def xǁCoverageFloorǁfile_has_violation__mutmut_4(self, path: Path) -> bool:
        """The report is absent/empty, or a source file is absent/below floor."""
        rel = self._repo_relative(path).as_posix()
        if self.branch_floor_pct is not None:
            return rel not in self._strict_failures
        report_rel = self._repo_relative(self._report_path()).as_posix()
        if rel == report_rel:
            return not self._coverage
        measured = self._coverage.get(rel)
        return measured is None or measured < self.floor_pct

    def xǁCoverageFloorǁfile_has_violation__mutmut_5(self, path: Path) -> bool:
        """The report is absent/empty, or a source file is absent/below floor."""
        rel = self._repo_relative(path).as_posix()
        if self.branch_floor_pct is not None:
            return rel in self._strict_failures
        report_rel = None
        if rel == report_rel:
            return not self._coverage
        measured = self._coverage.get(rel)
        return measured is None or measured < self.floor_pct

    def xǁCoverageFloorǁfile_has_violation__mutmut_6(self, path: Path) -> bool:
        """The report is absent/empty, or a source file is absent/below floor."""
        rel = self._repo_relative(path).as_posix()
        if self.branch_floor_pct is not None:
            return rel in self._strict_failures
        report_rel = self._repo_relative(None).as_posix()
        if rel == report_rel:
            return not self._coverage
        measured = self._coverage.get(rel)
        return measured is None or measured < self.floor_pct

    def xǁCoverageFloorǁfile_has_violation__mutmut_7(self, path: Path) -> bool:
        """The report is absent/empty, or a source file is absent/below floor."""
        rel = self._repo_relative(path).as_posix()
        if self.branch_floor_pct is not None:
            return rel in self._strict_failures
        report_rel = self._repo_relative(self._report_path()).as_posix()
        if rel != report_rel:
            return not self._coverage
        measured = self._coverage.get(rel)
        return measured is None or measured < self.floor_pct

    def xǁCoverageFloorǁfile_has_violation__mutmut_8(self, path: Path) -> bool:
        """The report is absent/empty, or a source file is absent/below floor."""
        rel = self._repo_relative(path).as_posix()
        if self.branch_floor_pct is not None:
            return rel in self._strict_failures
        report_rel = self._repo_relative(self._report_path()).as_posix()
        if rel == report_rel:
            return self._coverage
        measured = self._coverage.get(rel)
        return measured is None or measured < self.floor_pct

    def xǁCoverageFloorǁfile_has_violation__mutmut_9(self, path: Path) -> bool:
        """The report is absent/empty, or a source file is absent/below floor."""
        rel = self._repo_relative(path).as_posix()
        if self.branch_floor_pct is not None:
            return rel in self._strict_failures
        report_rel = self._repo_relative(self._report_path()).as_posix()
        if rel == report_rel:
            return not self._coverage
        measured = None
        return measured is None or measured < self.floor_pct

    def xǁCoverageFloorǁfile_has_violation__mutmut_10(self, path: Path) -> bool:
        """The report is absent/empty, or a source file is absent/below floor."""
        rel = self._repo_relative(path).as_posix()
        if self.branch_floor_pct is not None:
            return rel in self._strict_failures
        report_rel = self._repo_relative(self._report_path()).as_posix()
        if rel == report_rel:
            return not self._coverage
        measured = self._coverage.get(None)
        return measured is None or measured < self.floor_pct

    def xǁCoverageFloorǁfile_has_violation__mutmut_11(self, path: Path) -> bool:
        """The report is absent/empty, or a source file is absent/below floor."""
        rel = self._repo_relative(path).as_posix()
        if self.branch_floor_pct is not None:
            return rel in self._strict_failures
        report_rel = self._repo_relative(self._report_path()).as_posix()
        if rel == report_rel:
            return not self._coverage
        measured = self._coverage.get(rel)
        return measured is None and measured < self.floor_pct

    def xǁCoverageFloorǁfile_has_violation__mutmut_12(self, path: Path) -> bool:
        """The report is absent/empty, or a source file is absent/below floor."""
        rel = self._repo_relative(path).as_posix()
        if self.branch_floor_pct is not None:
            return rel in self._strict_failures
        report_rel = self._repo_relative(self._report_path()).as_posix()
        if rel == report_rel:
            return not self._coverage
        measured = self._coverage.get(rel)
        return measured is not None or measured < self.floor_pct

    def xǁCoverageFloorǁfile_has_violation__mutmut_13(self, path: Path) -> bool:
        """The report is absent/empty, or a source file is absent/below floor."""
        rel = self._repo_relative(path).as_posix()
        if self.branch_floor_pct is not None:
            return rel in self._strict_failures
        report_rel = self._repo_relative(self._report_path()).as_posix()
        if rel == report_rel:
            return not self._coverage
        measured = self._coverage.get(rel)
        return measured is None or measured <= self.floor_pct

    @_mutmut_mutated(mutants_xǁCoverageFloorǁrun__mutmut)
    def run(self) -> int:
        """Strict independent floors never consult a suppressible baseline."""
        if self.branch_floor_pct is None:
            return super().run()
        failures = dict(self._strict_failures)
        if self.receipt_config is not None:
            from tc_fitness.coverage_admission import receipt_failures

            failures.update(receipt_failures(self._repo_root, self.receipt_config))
        for relative, message in failures.items():
            report_finding(self.name, relative, message)
            print(f"FAIL [{self.name}] {relative}: {message}")
        return int(bool(failures))

    def xǁCoverageFloorǁrun__mutmut_orig(self) -> int:
        """Strict independent floors never consult a suppressible baseline."""
        if self.branch_floor_pct is None:
            return super().run()
        failures = dict(self._strict_failures)
        if self.receipt_config is not None:
            from tc_fitness.coverage_admission import receipt_failures

            failures.update(receipt_failures(self._repo_root, self.receipt_config))
        for relative, message in failures.items():
            report_finding(self.name, relative, message)
            print(f"FAIL [{self.name}] {relative}: {message}")
        return int(bool(failures))

    def xǁCoverageFloorǁrun__mutmut_1(self) -> int:
        """Strict independent floors never consult a suppressible baseline."""
        if self.branch_floor_pct is not None:
            return super().run()
        failures = dict(self._strict_failures)
        if self.receipt_config is not None:
            from tc_fitness.coverage_admission import receipt_failures

            failures.update(receipt_failures(self._repo_root, self.receipt_config))
        for relative, message in failures.items():
            report_finding(self.name, relative, message)
            print(f"FAIL [{self.name}] {relative}: {message}")
        return int(bool(failures))

    def xǁCoverageFloorǁrun__mutmut_2(self) -> int:
        """Strict independent floors never consult a suppressible baseline."""
        if self.branch_floor_pct is None:
            return super().run()
        failures = None
        if self.receipt_config is not None:
            from tc_fitness.coverage_admission import receipt_failures

            failures.update(receipt_failures(self._repo_root, self.receipt_config))
        for relative, message in failures.items():
            report_finding(self.name, relative, message)
            print(f"FAIL [{self.name}] {relative}: {message}")
        return int(bool(failures))

    def xǁCoverageFloorǁrun__mutmut_3(self) -> int:
        """Strict independent floors never consult a suppressible baseline."""
        if self.branch_floor_pct is None:
            return super().run()
        failures = dict(None)
        if self.receipt_config is not None:
            from tc_fitness.coverage_admission import receipt_failures

            failures.update(receipt_failures(self._repo_root, self.receipt_config))
        for relative, message in failures.items():
            report_finding(self.name, relative, message)
            print(f"FAIL [{self.name}] {relative}: {message}")
        return int(bool(failures))

    def xǁCoverageFloorǁrun__mutmut_4(self) -> int:
        """Strict independent floors never consult a suppressible baseline."""
        if self.branch_floor_pct is None:
            return super().run()
        failures = dict(self._strict_failures)
        if self.receipt_config is None:
            from tc_fitness.coverage_admission import receipt_failures

            failures.update(receipt_failures(self._repo_root, self.receipt_config))
        for relative, message in failures.items():
            report_finding(self.name, relative, message)
            print(f"FAIL [{self.name}] {relative}: {message}")
        return int(bool(failures))

    def xǁCoverageFloorǁrun__mutmut_5(self) -> int:
        """Strict independent floors never consult a suppressible baseline."""
        if self.branch_floor_pct is None:
            return super().run()
        failures = dict(self._strict_failures)
        if self.receipt_config is not None:
            from tc_fitness.coverage_admission import receipt_failures

            failures.update(None)
        for relative, message in failures.items():
            report_finding(self.name, relative, message)
            print(f"FAIL [{self.name}] {relative}: {message}")
        return int(bool(failures))

    def xǁCoverageFloorǁrun__mutmut_6(self) -> int:
        """Strict independent floors never consult a suppressible baseline."""
        if self.branch_floor_pct is None:
            return super().run()
        failures = dict(self._strict_failures)
        if self.receipt_config is not None:
            from tc_fitness.coverage_admission import receipt_failures

            failures.update(receipt_failures(None, self.receipt_config))
        for relative, message in failures.items():
            report_finding(self.name, relative, message)
            print(f"FAIL [{self.name}] {relative}: {message}")
        return int(bool(failures))

    def xǁCoverageFloorǁrun__mutmut_7(self) -> int:
        """Strict independent floors never consult a suppressible baseline."""
        if self.branch_floor_pct is None:
            return super().run()
        failures = dict(self._strict_failures)
        if self.receipt_config is not None:
            from tc_fitness.coverage_admission import receipt_failures

            failures.update(receipt_failures(self._repo_root, None))
        for relative, message in failures.items():
            report_finding(self.name, relative, message)
            print(f"FAIL [{self.name}] {relative}: {message}")
        return int(bool(failures))

    def xǁCoverageFloorǁrun__mutmut_8(self) -> int:
        """Strict independent floors never consult a suppressible baseline."""
        if self.branch_floor_pct is None:
            return super().run()
        failures = dict(self._strict_failures)
        if self.receipt_config is not None:
            from tc_fitness.coverage_admission import receipt_failures

            failures.update(receipt_failures(self.receipt_config))
        for relative, message in failures.items():
            report_finding(self.name, relative, message)
            print(f"FAIL [{self.name}] {relative}: {message}")
        return int(bool(failures))

    def xǁCoverageFloorǁrun__mutmut_9(self) -> int:
        """Strict independent floors never consult a suppressible baseline."""
        if self.branch_floor_pct is None:
            return super().run()
        failures = dict(self._strict_failures)
        if self.receipt_config is not None:
            from tc_fitness.coverage_admission import receipt_failures

            failures.update(receipt_failures(self._repo_root, ))
        for relative, message in failures.items():
            report_finding(self.name, relative, message)
            print(f"FAIL [{self.name}] {relative}: {message}")
        return int(bool(failures))

    def xǁCoverageFloorǁrun__mutmut_10(self) -> int:
        """Strict independent floors never consult a suppressible baseline."""
        if self.branch_floor_pct is None:
            return super().run()
        failures = dict(self._strict_failures)
        if self.receipt_config is not None:
            from tc_fitness.coverage_admission import receipt_failures

            failures.update(receipt_failures(self._repo_root, self.receipt_config))
        for relative, message in failures.items():
            report_finding(None, relative, message)
            print(f"FAIL [{self.name}] {relative}: {message}")
        return int(bool(failures))

    def xǁCoverageFloorǁrun__mutmut_11(self) -> int:
        """Strict independent floors never consult a suppressible baseline."""
        if self.branch_floor_pct is None:
            return super().run()
        failures = dict(self._strict_failures)
        if self.receipt_config is not None:
            from tc_fitness.coverage_admission import receipt_failures

            failures.update(receipt_failures(self._repo_root, self.receipt_config))
        for relative, message in failures.items():
            report_finding(self.name, None, message)
            print(f"FAIL [{self.name}] {relative}: {message}")
        return int(bool(failures))

    def xǁCoverageFloorǁrun__mutmut_12(self) -> int:
        """Strict independent floors never consult a suppressible baseline."""
        if self.branch_floor_pct is None:
            return super().run()
        failures = dict(self._strict_failures)
        if self.receipt_config is not None:
            from tc_fitness.coverage_admission import receipt_failures

            failures.update(receipt_failures(self._repo_root, self.receipt_config))
        for relative, message in failures.items():
            report_finding(self.name, relative, None)
            print(f"FAIL [{self.name}] {relative}: {message}")
        return int(bool(failures))

    def xǁCoverageFloorǁrun__mutmut_13(self) -> int:
        """Strict independent floors never consult a suppressible baseline."""
        if self.branch_floor_pct is None:
            return super().run()
        failures = dict(self._strict_failures)
        if self.receipt_config is not None:
            from tc_fitness.coverage_admission import receipt_failures

            failures.update(receipt_failures(self._repo_root, self.receipt_config))
        for relative, message in failures.items():
            report_finding(relative, message)
            print(f"FAIL [{self.name}] {relative}: {message}")
        return int(bool(failures))

    def xǁCoverageFloorǁrun__mutmut_14(self) -> int:
        """Strict independent floors never consult a suppressible baseline."""
        if self.branch_floor_pct is None:
            return super().run()
        failures = dict(self._strict_failures)
        if self.receipt_config is not None:
            from tc_fitness.coverage_admission import receipt_failures

            failures.update(receipt_failures(self._repo_root, self.receipt_config))
        for relative, message in failures.items():
            report_finding(self.name, message)
            print(f"FAIL [{self.name}] {relative}: {message}")
        return int(bool(failures))

    def xǁCoverageFloorǁrun__mutmut_15(self) -> int:
        """Strict independent floors never consult a suppressible baseline."""
        if self.branch_floor_pct is None:
            return super().run()
        failures = dict(self._strict_failures)
        if self.receipt_config is not None:
            from tc_fitness.coverage_admission import receipt_failures

            failures.update(receipt_failures(self._repo_root, self.receipt_config))
        for relative, message in failures.items():
            report_finding(self.name, relative, )
            print(f"FAIL [{self.name}] {relative}: {message}")
        return int(bool(failures))

    def xǁCoverageFloorǁrun__mutmut_16(self) -> int:
        """Strict independent floors never consult a suppressible baseline."""
        if self.branch_floor_pct is None:
            return super().run()
        failures = dict(self._strict_failures)
        if self.receipt_config is not None:
            from tc_fitness.coverage_admission import receipt_failures

            failures.update(receipt_failures(self._repo_root, self.receipt_config))
        for relative, message in failures.items():
            report_finding(self.name, relative, message)
            print(None)
        return int(bool(failures))

    def xǁCoverageFloorǁrun__mutmut_17(self) -> int:
        """Strict independent floors never consult a suppressible baseline."""
        if self.branch_floor_pct is None:
            return super().run()
        failures = dict(self._strict_failures)
        if self.receipt_config is not None:
            from tc_fitness.coverage_admission import receipt_failures

            failures.update(receipt_failures(self._repo_root, self.receipt_config))
        for relative, message in failures.items():
            report_finding(self.name, relative, message)
            print(f"FAIL [{self.name}] {relative}: {message}")
        return int(None)

    def xǁCoverageFloorǁrun__mutmut_18(self) -> int:
        """Strict independent floors never consult a suppressible baseline."""
        if self.branch_floor_pct is None:
            return super().run()
        failures = dict(self._strict_failures)
        if self.receipt_config is not None:
            from tc_fitness.coverage_admission import receipt_failures

            failures.update(receipt_failures(self._repo_root, self.receipt_config))
        for relative, message in failures.items():
            report_finding(self.name, relative, message)
            print(f"FAIL [{self.name}] {relative}: {message}")
        return int(bool(None))

mutants_xǁCoverageFloorǁfrom_config__mutmut['_mutmut_orig'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_1'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_2'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_3'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_4'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_5'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_6'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_7'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_8'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_9'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_10'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_11'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_12'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_12 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_13'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_13 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_14'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_14 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_15'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_15 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_16'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_16 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_17'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_17 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_18'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_18 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_19'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_19 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_20'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_20 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_21'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_21 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_22'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_22 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_23'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_23 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_24'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_24 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_25'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_25 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_26'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_26 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_27'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_27 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_28'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_28 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_29'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_29 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_30'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_30 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_31'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_31 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_32'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_32 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_33'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_33 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_34'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_34 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_35'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_35 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_36'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_36 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_37'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_37 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_38'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_38 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_39'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_39 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_40'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_40 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_41'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_41 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_42'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_42 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_43'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_43 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_44'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_44 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_45'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_45 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_46'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_46 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_47'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_47 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_48'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_48 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_49'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_49 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_50'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_50 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_51'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_51 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_52'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_52 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_53'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_53 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_54'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_54 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_55'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_55 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_56'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_56 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_57'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_57 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_58'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_58 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_59'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_59 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_60'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_60 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_61'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_61 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_62'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_62 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_63'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_63 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_64'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_64 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_65'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_65 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_66'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_66 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_67'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_67 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_68'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_68 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_69'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_69 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_70'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_70 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_71'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_71 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_72'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_72 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_73'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_73 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_74'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_74 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_75'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_75 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_76'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_76 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_77'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_77 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_78'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_78 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_79'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_79 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_80'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_80 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_81'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_81 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_82'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_82 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_83'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_83 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_84'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_84 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_85'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_85 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_86'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_86 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_87'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_87 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_88'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_88 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_89'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_89 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_90'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_90 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_91'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_91 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_92'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_92 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_93'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_93 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_94'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_94 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_95'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_95 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_96'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_96 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_97'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_97 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_98'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_98 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_99'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_99 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_100'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_100 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_101'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_101 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_102'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_102 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_103'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_103 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_104'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_104 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_105'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_105 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_106'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_106 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_107'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_107 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_108'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_108 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_109'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_109 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_110'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_110 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_111'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_111 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_112'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_112 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_113'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_113 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_114'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_114 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_115'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_115 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_116'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_116 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_117'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_117 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_118'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_118 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_119'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_119 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_120'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_120 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_121'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_121 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_122'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_122 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_123'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_123 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_124'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_124 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_125'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_125 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_126'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_126 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_127'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_127 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_128'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_128 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_129'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_129 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_130'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_130 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_131'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_131 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfrom_config__mutmut['xǁCoverageFloorǁfrom_config__mutmut_132'] = CoverageFloor.xǁCoverageFloorǁfrom_config__mutmut_132 # type: ignore # mutmut generated

mutants_xǁCoverageFloorǁ_report_path__mutmut['_mutmut_orig'] = CoverageFloor.xǁCoverageFloorǁ_report_path__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁ_report_path__mutmut['xǁCoverageFloorǁ_report_path__mutmut_1'] = CoverageFloor.xǁCoverageFloorǁ_report_path__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁ_report_path__mutmut['xǁCoverageFloorǁ_report_path__mutmut_2'] = CoverageFloor.xǁCoverageFloorǁ_report_path__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁ_report_path__mutmut['xǁCoverageFloorǁ_report_path__mutmut_3'] = CoverageFloor.xǁCoverageFloorǁ_report_path__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁ_report_path__mutmut['xǁCoverageFloorǁ_report_path__mutmut_4'] = CoverageFloor.xǁCoverageFloorǁ_report_path__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁ_report_path__mutmut['xǁCoverageFloorǁ_report_path__mutmut_5'] = CoverageFloor.xǁCoverageFloorǁ_report_path__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁ_report_path__mutmut['xǁCoverageFloorǁ_report_path__mutmut_6'] = CoverageFloor.xǁCoverageFloorǁ_report_path__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁ_report_path__mutmut['xǁCoverageFloorǁ_report_path__mutmut_7'] = CoverageFloor.xǁCoverageFloorǁ_report_path__mutmut_7 # type: ignore # mutmut generated

mutants_xǁCoverageFloorǁenumerate_files__mutmut['_mutmut_orig'] = CoverageFloor.xǁCoverageFloorǁenumerate_files__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁenumerate_files__mutmut['xǁCoverageFloorǁenumerate_files__mutmut_1'] = CoverageFloor.xǁCoverageFloorǁenumerate_files__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁenumerate_files__mutmut['xǁCoverageFloorǁenumerate_files__mutmut_2'] = CoverageFloor.xǁCoverageFloorǁenumerate_files__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁenumerate_files__mutmut['xǁCoverageFloorǁenumerate_files__mutmut_3'] = CoverageFloor.xǁCoverageFloorǁenumerate_files__mutmut_3 # type: ignore # mutmut generated

mutants_xǁCoverageFloorǁis_in_scope__mutmut['_mutmut_orig'] = CoverageFloor.xǁCoverageFloorǁis_in_scope__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁis_in_scope__mutmut['xǁCoverageFloorǁis_in_scope__mutmut_1'] = CoverageFloor.xǁCoverageFloorǁis_in_scope__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁis_in_scope__mutmut['xǁCoverageFloorǁis_in_scope__mutmut_2'] = CoverageFloor.xǁCoverageFloorǁis_in_scope__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁis_in_scope__mutmut['xǁCoverageFloorǁis_in_scope__mutmut_3'] = CoverageFloor.xǁCoverageFloorǁis_in_scope__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁis_in_scope__mutmut['xǁCoverageFloorǁis_in_scope__mutmut_4'] = CoverageFloor.xǁCoverageFloorǁis_in_scope__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁis_in_scope__mutmut['xǁCoverageFloorǁis_in_scope__mutmut_5'] = CoverageFloor.xǁCoverageFloorǁis_in_scope__mutmut_5 # type: ignore # mutmut generated

mutants_xǁCoverageFloorǁfile_has_violation__mutmut['_mutmut_orig'] = CoverageFloor.xǁCoverageFloorǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfile_has_violation__mutmut['xǁCoverageFloorǁfile_has_violation__mutmut_1'] = CoverageFloor.xǁCoverageFloorǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfile_has_violation__mutmut['xǁCoverageFloorǁfile_has_violation__mutmut_2'] = CoverageFloor.xǁCoverageFloorǁfile_has_violation__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfile_has_violation__mutmut['xǁCoverageFloorǁfile_has_violation__mutmut_3'] = CoverageFloor.xǁCoverageFloorǁfile_has_violation__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfile_has_violation__mutmut['xǁCoverageFloorǁfile_has_violation__mutmut_4'] = CoverageFloor.xǁCoverageFloorǁfile_has_violation__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfile_has_violation__mutmut['xǁCoverageFloorǁfile_has_violation__mutmut_5'] = CoverageFloor.xǁCoverageFloorǁfile_has_violation__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfile_has_violation__mutmut['xǁCoverageFloorǁfile_has_violation__mutmut_6'] = CoverageFloor.xǁCoverageFloorǁfile_has_violation__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfile_has_violation__mutmut['xǁCoverageFloorǁfile_has_violation__mutmut_7'] = CoverageFloor.xǁCoverageFloorǁfile_has_violation__mutmut_7 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfile_has_violation__mutmut['xǁCoverageFloorǁfile_has_violation__mutmut_8'] = CoverageFloor.xǁCoverageFloorǁfile_has_violation__mutmut_8 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfile_has_violation__mutmut['xǁCoverageFloorǁfile_has_violation__mutmut_9'] = CoverageFloor.xǁCoverageFloorǁfile_has_violation__mutmut_9 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfile_has_violation__mutmut['xǁCoverageFloorǁfile_has_violation__mutmut_10'] = CoverageFloor.xǁCoverageFloorǁfile_has_violation__mutmut_10 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfile_has_violation__mutmut['xǁCoverageFloorǁfile_has_violation__mutmut_11'] = CoverageFloor.xǁCoverageFloorǁfile_has_violation__mutmut_11 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfile_has_violation__mutmut['xǁCoverageFloorǁfile_has_violation__mutmut_12'] = CoverageFloor.xǁCoverageFloorǁfile_has_violation__mutmut_12 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁfile_has_violation__mutmut['xǁCoverageFloorǁfile_has_violation__mutmut_13'] = CoverageFloor.xǁCoverageFloorǁfile_has_violation__mutmut_13 # type: ignore # mutmut generated

mutants_xǁCoverageFloorǁrun__mutmut['_mutmut_orig'] = CoverageFloor.xǁCoverageFloorǁrun__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁrun__mutmut['xǁCoverageFloorǁrun__mutmut_1'] = CoverageFloor.xǁCoverageFloorǁrun__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁrun__mutmut['xǁCoverageFloorǁrun__mutmut_2'] = CoverageFloor.xǁCoverageFloorǁrun__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁrun__mutmut['xǁCoverageFloorǁrun__mutmut_3'] = CoverageFloor.xǁCoverageFloorǁrun__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁrun__mutmut['xǁCoverageFloorǁrun__mutmut_4'] = CoverageFloor.xǁCoverageFloorǁrun__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁrun__mutmut['xǁCoverageFloorǁrun__mutmut_5'] = CoverageFloor.xǁCoverageFloorǁrun__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁrun__mutmut['xǁCoverageFloorǁrun__mutmut_6'] = CoverageFloor.xǁCoverageFloorǁrun__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁrun__mutmut['xǁCoverageFloorǁrun__mutmut_7'] = CoverageFloor.xǁCoverageFloorǁrun__mutmut_7 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁrun__mutmut['xǁCoverageFloorǁrun__mutmut_8'] = CoverageFloor.xǁCoverageFloorǁrun__mutmut_8 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁrun__mutmut['xǁCoverageFloorǁrun__mutmut_9'] = CoverageFloor.xǁCoverageFloorǁrun__mutmut_9 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁrun__mutmut['xǁCoverageFloorǁrun__mutmut_10'] = CoverageFloor.xǁCoverageFloorǁrun__mutmut_10 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁrun__mutmut['xǁCoverageFloorǁrun__mutmut_11'] = CoverageFloor.xǁCoverageFloorǁrun__mutmut_11 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁrun__mutmut['xǁCoverageFloorǁrun__mutmut_12'] = CoverageFloor.xǁCoverageFloorǁrun__mutmut_12 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁrun__mutmut['xǁCoverageFloorǁrun__mutmut_13'] = CoverageFloor.xǁCoverageFloorǁrun__mutmut_13 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁrun__mutmut['xǁCoverageFloorǁrun__mutmut_14'] = CoverageFloor.xǁCoverageFloorǁrun__mutmut_14 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁrun__mutmut['xǁCoverageFloorǁrun__mutmut_15'] = CoverageFloor.xǁCoverageFloorǁrun__mutmut_15 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁrun__mutmut['xǁCoverageFloorǁrun__mutmut_16'] = CoverageFloor.xǁCoverageFloorǁrun__mutmut_16 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁrun__mutmut['xǁCoverageFloorǁrun__mutmut_17'] = CoverageFloor.xǁCoverageFloorǁrun__mutmut_17 # type: ignore # mutmut generated
mutants_xǁCoverageFloorǁrun__mutmut['xǁCoverageFloorǁrun__mutmut_18'] = CoverageFloor.xǁCoverageFloorǁrun__mutmut_18 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> CoverageFloor:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CoverageFloor.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> CoverageFloor:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CoverageFloor.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> CoverageFloor:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CoverageFloor.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> CoverageFloor:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CoverageFloor.from_config(config, repo_root=None)


def x_build__mutmut_3(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> CoverageFloor:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CoverageFloor.from_config(repo_root=repo_root)


def x_build__mutmut_4(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> CoverageFloor:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CoverageFloor.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(CoverageFloor, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(CoverageFloor, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(CoverageFloor, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(CoverageFloor, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
