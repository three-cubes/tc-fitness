"""Shared Cobertura path resolution for coverage assurance.

Coverage producers may emit repository-relative source roots, absolute source
roots, or several roots. Assurance resolves every class filename back to one
repository-relative file and rejects ambiguous or out-of-repository evidence.
"""

from __future__ import annotations

import ast
import math
import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class CoverageCounts:
    """Independent executable-line and branch-exit counts, never combined."""

    lines: int
    covered_lines: int
    branches: int
    covered_branches: int

    @property
    def line_pct(self) -> float:
        return 100 * self.covered_lines / self.lines if self.lines else 100.0

    @property
    def branch_pct(self) -> float:
        return 100 * self.covered_branches / self.branches if self.branches else 100.0


def coverage_integer(value: str | None) -> int:
    """Require explicit non-negative integer evidence rather than defaults."""
    if value is None or re.fullmatch(r"0|[1-9][0-9]*", value) is None:
        raise ValueError("coverage detail requires non-negative integer counts")
    return int(value)


def validate_coverage_rate(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("missing coverage rate")
    rate = float(value)
    if not math.isfinite(rate) or not 0 <= rate <= 1:
        raise ValueError("coverage rate must be finite and between zero and one")
    if not total and rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("zero-opportunity coverage must be measured, not disabled")
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") and not math.isclose(rate, exact, abs_tol=0.000001):
            raise ValueError("coverage rate disagrees with detailed counts")


def count_class_coverage(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def _relative_to_repository(candidate: Path, repo_root: Path) -> str:
    try:
        return candidate.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError as exc:
        raise ValueError(f"coverage path is outside the repository: {candidate}") from exc


def resolve_coverage_filename(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


__all__ = ["resolve_coverage_filename"]
