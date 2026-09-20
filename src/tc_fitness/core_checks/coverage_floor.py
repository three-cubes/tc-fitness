"""CORE check: coverage_floor — per-file line-coverage floor.

Repository-wide coverage averages hide files at 0%: a 91% repo mean can
conceal a source file with no tests at all. This rule enforces a PER-FILE
floor — every source file recorded in a coverage report must clear a minimum
line-coverage percentage — so the gap is surfaced file-by-file rather than
washed out in the mean.

The rule is the :class:`tc_fitness.fitness_rule.FitnessRule` expression of a
coverage *ratchet*: today's below-floor files are grandfathered into the
per-file baseline (``--establish-baseline``), and the gate FAILS only when a
file NOT in the baseline drops below the floor. The baseline may only shrink,
so coverage debt is paid down, never accreted.

Ported from kairix ``scripts/checks/check_per_file_coverage.py`` (F7/F9) and
the coverage.xml parsing in tc-agent-zone ``scripts/checks/coverage_ratchet.py``
— re-expressed as a configurable, repo-agnostic rule. The floor, the coverage
report path, and the scan roots are CONFIG the consumer supplies; nothing here
names a repo, a source package, or a hardcoded threshold beyond the
domain-intrinsic default.
"""

from __future__ import annotations

import importlib
from collections.abc import Callable, Mapping
from functools import cached_property
from pathlib import Path
from types import ModuleType
from typing import Any

from tc_fitness.core_checks import run_core_check
from tc_fitness.core_checks._coverage_evidence import (
    reject_external_report,
    resolve_coverage_filename,
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


def _reject_unsafe_xml(text: str, source: str) -> None:
    """Reject DTD/entity declarations before any parser runs (XXE guard)."""
    lowered = text.lower()
    if "<!doctype" in lowered or "<!entity" in lowered:
        raise ValueError(f"unsafe coverage XML at {source}: DTD/entity declarations are not allowed")


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


class CoverageFloor(FitnessRule):
    """Flags source files whose recorded line coverage is below the floor."""

    name = "coverage-floor"
    remediation = REMEDIATION
    extensions = (".py",)

    #: Rule-specific knobs — instance attrs so ``from_config`` overrides them.
    floor_pct: float = DEFAULT_FLOOR_PCT
    coverage_report: str = DEFAULT_COVERAGE_REPORT

    @classmethod
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
        reject_external_report(rule.coverage_report, rule._repo_root)
        return rule

    def establish_baseline(self) -> Path:
        """Refuse to freeze a state in which no evidence was measured at all.

        Absent evidence produces the same violation key as a measured report
        that falls short, so adopting a baseline while the report is missing
        would record that key and turn the check permanently green — exactly
        during onboarding, when the report is most likely not to have been
        produced yet. Debt that was measured can be ratcheted; evidence that
        was never produced cannot.
        """
        if not self._report_path().exists():
            raise ValueError(
                "cannot baseline absent coverage evidence: "
                f"{self.coverage_report} does not exist; produce the report, then adopt"
            )
        return super().establish_baseline()

    def _report_path(self) -> Path:
        report = Path(self.coverage_report)
        return report if report.is_absolute() else self._repo_root / report

    @cached_property
    def _coverage(self) -> dict[str, float]:
        return parse_coverage_report(self._report_path(), repo_root=self._repo_root)

    def _below_floor(self) -> dict[str, float]:
        """Map of report-relative path → coverage for files under the floor."""
        return {path: pct for path, pct in self._coverage.items() if pct < self.floor_pct}

    def enumerate_files(self) -> list[Path]:
        """Enumerate the below-floor files named in the coverage report.

        The source tree is authoritative. A report cannot hide an uncovered
        file by omitting it. A missing or empty report is represented by the
        report path itself so it produces an observable finding.
        """
        if not self._coverage:
            return [self._report_path()]
        return super().enumerate_files()

    def is_in_scope(self, rel: str) -> bool:
        report_rel = self._repo_relative(self._report_path()).as_posix()
        return rel == report_rel or super().is_in_scope(rel)

    def file_has_violation(self, path: Path) -> bool:
        """The report is absent/empty, or a source file is absent/below floor."""
        rel = self._repo_relative(path).as_posix()
        report_rel = self._repo_relative(self._report_path()).as_posix()
        if rel == report_rel:
            return not self._coverage
        measured = self._coverage.get(rel)
        return measured is None or measured < self.floor_pct


def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> CoverageFloor:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CoverageFloor.from_config(config, repo_root=repo_root)


def main(argv: list[str] | None = None) -> int:
    """CLI entry — supports ``--establish-baseline`` and ``--repo-root``."""
    return run_core_check(CoverageFloor, argv)


if __name__ == "__main__":
    import sys

    sys.exit(main())
