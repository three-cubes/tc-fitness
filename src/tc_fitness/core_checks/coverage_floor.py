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

    def _report_path(self) -> Path:
        if self.receipt_config is not None:
            from tc_fitness.coverage_admission import configured

            report = Path(configured(self.coverage_report))
        else:
            report = Path(self.coverage_report)
        return report if report.is_absolute() else self._repo_root / report

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

    def is_in_scope(self, rel: str) -> bool:
        report_rel = self._repo_relative(self._report_path()).as_posix()
        return rel == report_rel or super().is_in_scope(rel)

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


def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> CoverageFloor:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CoverageFloor.from_config(config, repo_root=repo_root)


def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(CoverageFloor, argv)


if __name__ == "__main__":
    import sys

    sys.exit(main())
