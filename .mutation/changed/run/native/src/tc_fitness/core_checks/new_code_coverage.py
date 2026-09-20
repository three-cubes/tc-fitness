"""CORE check: new_code_coverage — coverage floor on the CHANGED lines only.

A repo-wide (or even per-file) coverage floor still lets a change land uncovered
so long as the file's *aggregate* rate stays above the bar: a well-covered file
absorbs a block of new, untested lines without dipping under the floor. The
merge gate SonarCloud enforces closes that gap by scoring "new code" in
isolation — the lines a branch ADDED or CHANGED versus the trunk — and blocking
when their coverage is below a floor (80% by default). This rule mirrors that
condition LOCALLY so an agent catches it before the CI round-trip, not after.

"New code" is the set of right-side lines between the merge base and the current
checkout. That includes committed, staged, unstaged, and untracked source, so a
local pre-push run and CI score the same source tree. For each in-scope changed
file present in the coverage report, the rule intersects those added lines with
the lines the report actually recorded (``coverable_changed``), counts those with
a non-zero hit (``covered_changed``), and FAILS the file when
``covered_changed / coverable_changed`` is below the floor. A file whose added
lines are all non-coverable (blank lines, comments, lines the report never
recorded) contributes no measurable new code and is not a violation.

That is the backwards-compatible consumer mode. Configuring
``exact_base_commit`` / ``candidate_commit`` instead uses strict immutable
coverage admission: complete source-derived executable detail, clean Git
identity, no exemptions and 100 percent changed lines. ``coverage_receipt``
additionally binds the fresh execution and accepted-base monotonic evidence.
Strict-mode missing inputs raise; they never enter the legacy soft-pass path.

Hard floor, by design: new code that misses the threshold always fails.

The floor, the report path, the trunk ref, and the scan roots are CONFIG the
consumer supplies; nothing here names a repo, a source package, or a threshold
beyond the domain-intrinsic default. A configured remote-tracking trunk ref is
refreshed before the merge-base is resolved; an offline refresh failure remains
visible while the cached ref supplies the best available local measurement. The
git invocation is a DI seam (a callable defaulting to :func:`subprocess.run`) so
the detector is testable without a real repository.
"""

from __future__ import annotations

import importlib
import os
import re
import stat
import subprocess
import sys
from collections.abc import Callable, Mapping
from functools import cached_property
from pathlib import Path
from types import ModuleType
from typing import Any

from tc_fitness.check_evidence import report_finding
from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: The domain-intrinsic default floor for new code — SonarCloud's own default
#: "Coverage on New Code" condition. Overridable per consumer via ``floor_pct``.
DEFAULT_FLOOR_PCT = 80.0

#: Default coverage report location relative to the repo root. Overridable.
DEFAULT_COVERAGE_REPORT = "coverage.xml"

#: Default trunk ref the change set is measured against. The changed lines are
#: the right side of the diff from the merge-base of this ref and HEAD.
DEFAULT_BASE_REF = "origin/main"

#: A git ref must match this before it is interpolated into a git argv — a
#: conservative allow-list of the characters a legitimate ref/revision carries
#: (refname chars plus the revision operators ``~ ^ @ { }``). Anything else is
#: treated as unresolvable → the rule SKIPs rather than shell-interpolating it.
_SAFE_REF_RE = re.compile(r"^[A-Za-z0-9_./@{}~^-]+$")

#: ``@@ -old +new @@`` hunk header — capture the new-side start line and count.
_HUNK_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")

#: A git command runner: takes the git sub-arguments (argv0 ``git`` is fixed by
#: the runner, never the caller) and the working directory, returns the
#: completed process. The DI seam a test overrides to feed canned diff output.
GitResult = subprocess.CompletedProcess[str] | subprocess.CompletedProcess[bytes]
GitRunner = Callable[[list[str], Path], GitResult]

REMEDIATION = _remediation(
    fix=(
        "cover the lines this change ADDED — ask what DEFECT CLASS the uncovered "
        "new code proxies (a missing failure-mode test for the new branch, an "
        "unexercised boundary, an untested scale bound) and write the test that "
        "proves the new behaviour. The only way through is a real test."
    ),
    nxt="re-run this check to confirm the changed lines clear the floor.",
    run="python -m tc_fitness.core_checks.new_code_coverage",
    passing="add a test that drives the new branch so its added lines report hits > 0",
    forbidden="pad coverage with a no-op call that executes the new lines without asserting",
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
mutants_x_parse_line_coverage__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_parse_line_coverage__mutmut)
def parse_line_coverage(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_orig(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_1(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_2(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = None
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_3(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding=None)
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_4(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="XXutf-8XX")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_5(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="UTF-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_6(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(None, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_7(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, None)
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_8(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_9(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, )
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_10(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(None))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_11(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = None
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_12(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_13(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = None

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_14(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(None).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_15(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = None
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_16(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip(None) for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_17(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("XX/XX") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_18(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter(None) if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_19(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("XXsourceXX") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_20(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("SOURCE") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_21(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text or s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_22(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = None
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_23(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[1] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_24(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else "XXXX"
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_25(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix != ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_26(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == "XX.XX":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_27(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = None

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_28(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = "XXXX"

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_29(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = None
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_30(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter(None):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_31(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("XXclassXX"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_32(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("CLASS"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_33(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = None
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_34(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") and ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_35(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get(None) or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_36(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("XXfilenameXX") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_37(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("FILENAME") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_38(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or "XXXX"
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_39(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_40(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            break
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_41(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix or not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_42(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_43(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(None):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_44(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix - "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_45(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "XX/XX"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_46(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = None
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_47(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = None
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_48(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = None
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_49(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(None, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_50(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, None)
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_51(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault({})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_52(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, )
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_53(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter(None):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_54(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("XXlineXX"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_55(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("LINE"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_56(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = None
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_57(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get(None)
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_58(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("XXnumberXX")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_59(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("NUMBER")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_60(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = None
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_61(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get(None)
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_62(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("XXhitsXX")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_63(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("HITS")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_64(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None and hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_65(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is not None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_66(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is not None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_67(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                break
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_68(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = None
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_69(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(None)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_70(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = None
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_71(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(None)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_72(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                break
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_73(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = None
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_74(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(None)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_75(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = None
    return out


def x_parse_line_coverage__mutmut_76(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is not None else max(prev, hit_count)
    return out


def x_parse_line_coverage__mutmut_77(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(None, hit_count)
    return out


def x_parse_line_coverage__mutmut_78(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, None)
    return out


def x_parse_line_coverage__mutmut_79(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(hit_count)
    return out


def x_parse_line_coverage__mutmut_80(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, )
    return out

mutants_x_parse_line_coverage__mutmut['_mutmut_orig'] = x_parse_line_coverage__mutmut_orig # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_1'] = x_parse_line_coverage__mutmut_1 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_2'] = x_parse_line_coverage__mutmut_2 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_3'] = x_parse_line_coverage__mutmut_3 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_4'] = x_parse_line_coverage__mutmut_4 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_5'] = x_parse_line_coverage__mutmut_5 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_6'] = x_parse_line_coverage__mutmut_6 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_7'] = x_parse_line_coverage__mutmut_7 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_8'] = x_parse_line_coverage__mutmut_8 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_9'] = x_parse_line_coverage__mutmut_9 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_10'] = x_parse_line_coverage__mutmut_10 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_11'] = x_parse_line_coverage__mutmut_11 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_12'] = x_parse_line_coverage__mutmut_12 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_13'] = x_parse_line_coverage__mutmut_13 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_14'] = x_parse_line_coverage__mutmut_14 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_15'] = x_parse_line_coverage__mutmut_15 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_16'] = x_parse_line_coverage__mutmut_16 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_17'] = x_parse_line_coverage__mutmut_17 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_18'] = x_parse_line_coverage__mutmut_18 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_19'] = x_parse_line_coverage__mutmut_19 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_20'] = x_parse_line_coverage__mutmut_20 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_21'] = x_parse_line_coverage__mutmut_21 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_22'] = x_parse_line_coverage__mutmut_22 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_23'] = x_parse_line_coverage__mutmut_23 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_24'] = x_parse_line_coverage__mutmut_24 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_25'] = x_parse_line_coverage__mutmut_25 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_26'] = x_parse_line_coverage__mutmut_26 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_27'] = x_parse_line_coverage__mutmut_27 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_28'] = x_parse_line_coverage__mutmut_28 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_29'] = x_parse_line_coverage__mutmut_29 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_30'] = x_parse_line_coverage__mutmut_30 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_31'] = x_parse_line_coverage__mutmut_31 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_32'] = x_parse_line_coverage__mutmut_32 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_33'] = x_parse_line_coverage__mutmut_33 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_34'] = x_parse_line_coverage__mutmut_34 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_35'] = x_parse_line_coverage__mutmut_35 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_36'] = x_parse_line_coverage__mutmut_36 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_37'] = x_parse_line_coverage__mutmut_37 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_38'] = x_parse_line_coverage__mutmut_38 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_39'] = x_parse_line_coverage__mutmut_39 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_40'] = x_parse_line_coverage__mutmut_40 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_41'] = x_parse_line_coverage__mutmut_41 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_42'] = x_parse_line_coverage__mutmut_42 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_43'] = x_parse_line_coverage__mutmut_43 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_44'] = x_parse_line_coverage__mutmut_44 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_45'] = x_parse_line_coverage__mutmut_45 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_46'] = x_parse_line_coverage__mutmut_46 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_47'] = x_parse_line_coverage__mutmut_47 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_48'] = x_parse_line_coverage__mutmut_48 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_49'] = x_parse_line_coverage__mutmut_49 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_50'] = x_parse_line_coverage__mutmut_50 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_51'] = x_parse_line_coverage__mutmut_51 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_52'] = x_parse_line_coverage__mutmut_52 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_53'] = x_parse_line_coverage__mutmut_53 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_54'] = x_parse_line_coverage__mutmut_54 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_55'] = x_parse_line_coverage__mutmut_55 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_56'] = x_parse_line_coverage__mutmut_56 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_57'] = x_parse_line_coverage__mutmut_57 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_58'] = x_parse_line_coverage__mutmut_58 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_59'] = x_parse_line_coverage__mutmut_59 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_60'] = x_parse_line_coverage__mutmut_60 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_61'] = x_parse_line_coverage__mutmut_61 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_62'] = x_parse_line_coverage__mutmut_62 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_63'] = x_parse_line_coverage__mutmut_63 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_64'] = x_parse_line_coverage__mutmut_64 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_65'] = x_parse_line_coverage__mutmut_65 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_66'] = x_parse_line_coverage__mutmut_66 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_67'] = x_parse_line_coverage__mutmut_67 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_68'] = x_parse_line_coverage__mutmut_68 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_69'] = x_parse_line_coverage__mutmut_69 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_70'] = x_parse_line_coverage__mutmut_70 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_71'] = x_parse_line_coverage__mutmut_71 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_72'] = x_parse_line_coverage__mutmut_72 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_73'] = x_parse_line_coverage__mutmut_73 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_74'] = x_parse_line_coverage__mutmut_74 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_75'] = x_parse_line_coverage__mutmut_75 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_76'] = x_parse_line_coverage__mutmut_76 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_77'] = x_parse_line_coverage__mutmut_77 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_78'] = x_parse_line_coverage__mutmut_78 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_79'] = x_parse_line_coverage__mutmut_79 # type: ignore # mutmut generated
mutants_x_parse_line_coverage__mutmut['x_parse_line_coverage__mutmut_80'] = x_parse_line_coverage__mutmut_80 # type: ignore # mutmut generated
mutants_x__strip_diff_prefix__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__strip_diff_prefix__mutmut)
def _strip_diff_prefix(target: str) -> str:
    """Drop git's ``a/`` / ``b/`` diff path prefix (default ``diff.prefix``)."""
    if target.startswith(("a/", "b/")):
        return target[2:]
    return target


def x__strip_diff_prefix__mutmut_orig(target: str) -> str:
    """Drop git's ``a/`` / ``b/`` diff path prefix (default ``diff.prefix``)."""
    if target.startswith(("a/", "b/")):
        return target[2:]
    return target


def x__strip_diff_prefix__mutmut_1(target: str) -> str:
    """Drop git's ``a/`` / ``b/`` diff path prefix (default ``diff.prefix``)."""
    if target.startswith(None):
        return target[2:]
    return target


def x__strip_diff_prefix__mutmut_2(target: str) -> str:
    """Drop git's ``a/`` / ``b/`` diff path prefix (default ``diff.prefix``)."""
    if target.startswith(("XXa/XX", "b/")):
        return target[2:]
    return target


def x__strip_diff_prefix__mutmut_3(target: str) -> str:
    """Drop git's ``a/`` / ``b/`` diff path prefix (default ``diff.prefix``)."""
    if target.startswith(("A/", "b/")):
        return target[2:]
    return target


def x__strip_diff_prefix__mutmut_4(target: str) -> str:
    """Drop git's ``a/`` / ``b/`` diff path prefix (default ``diff.prefix``)."""
    if target.startswith(("a/", "XXb/XX")):
        return target[2:]
    return target


def x__strip_diff_prefix__mutmut_5(target: str) -> str:
    """Drop git's ``a/`` / ``b/`` diff path prefix (default ``diff.prefix``)."""
    if target.startswith(("a/", "B/")):
        return target[2:]
    return target


def x__strip_diff_prefix__mutmut_6(target: str) -> str:
    """Drop git's ``a/`` / ``b/`` diff path prefix (default ``diff.prefix``)."""
    if target.startswith(("a/", "b/")):
        return target[3:]
    return target

mutants_x__strip_diff_prefix__mutmut['_mutmut_orig'] = x__strip_diff_prefix__mutmut_orig # type: ignore # mutmut generated
mutants_x__strip_diff_prefix__mutmut['x__strip_diff_prefix__mutmut_1'] = x__strip_diff_prefix__mutmut_1 # type: ignore # mutmut generated
mutants_x__strip_diff_prefix__mutmut['x__strip_diff_prefix__mutmut_2'] = x__strip_diff_prefix__mutmut_2 # type: ignore # mutmut generated
mutants_x__strip_diff_prefix__mutmut['x__strip_diff_prefix__mutmut_3'] = x__strip_diff_prefix__mutmut_3 # type: ignore # mutmut generated
mutants_x__strip_diff_prefix__mutmut['x__strip_diff_prefix__mutmut_4'] = x__strip_diff_prefix__mutmut_4 # type: ignore # mutmut generated
mutants_x__strip_diff_prefix__mutmut['x__strip_diff_prefix__mutmut_5'] = x__strip_diff_prefix__mutmut_5 # type: ignore # mutmut generated
mutants_x__strip_diff_prefix__mutmut['x__strip_diff_prefix__mutmut_6'] = x__strip_diff_prefix__mutmut_6 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_parse_added_lines__mutmut)
def parse_added_lines(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_orig(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_1(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = None
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_2(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = ""
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_3(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = None
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_4(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 1
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_5(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith(None):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_6(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("XXdiff --gitXX"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_7(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("DIFF --GIT"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_8(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = ""
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_9(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            break
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_10(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith(None):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_11(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("XX+++ XX"):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_12(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = None
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_13(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split(None, 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_14(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", None)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_15(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split(1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_16(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", )[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_17(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].rsplit("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_18(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[5:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_19(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("XX\tXX", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_20(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 2)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_21(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[1].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_22(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_23(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target != "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_24(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "XX/dev/nullXX" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_25(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/DEV/NULL" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_26(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(None)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_27(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_28(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(None, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_29(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, None)
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_30(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_31(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, )
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_32(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            break
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_33(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith(None):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_34(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("XX--- XX"):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_35(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            break
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_36(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith(None):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_37(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("XX@@XX"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_38(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = None
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_39(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(None)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_40(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = None
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_41(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(None)
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_42(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(None))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_43(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(2))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_44(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            break
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_45(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is not None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_46(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            break
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_47(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith(None):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_48(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("XX+XX"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_49(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(None)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_50(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line = 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_51(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line -= 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_52(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 2
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_53(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(None):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_54(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith("XX XX"):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_55(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line = 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_56(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line -= 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def x_parse_added_lines__mutmut_57(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 2
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added

mutants_x_parse_added_lines__mutmut['_mutmut_orig'] = x_parse_added_lines__mutmut_orig # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_1'] = x_parse_added_lines__mutmut_1 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_2'] = x_parse_added_lines__mutmut_2 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_3'] = x_parse_added_lines__mutmut_3 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_4'] = x_parse_added_lines__mutmut_4 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_5'] = x_parse_added_lines__mutmut_5 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_6'] = x_parse_added_lines__mutmut_6 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_7'] = x_parse_added_lines__mutmut_7 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_8'] = x_parse_added_lines__mutmut_8 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_9'] = x_parse_added_lines__mutmut_9 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_10'] = x_parse_added_lines__mutmut_10 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_11'] = x_parse_added_lines__mutmut_11 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_12'] = x_parse_added_lines__mutmut_12 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_13'] = x_parse_added_lines__mutmut_13 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_14'] = x_parse_added_lines__mutmut_14 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_15'] = x_parse_added_lines__mutmut_15 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_16'] = x_parse_added_lines__mutmut_16 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_17'] = x_parse_added_lines__mutmut_17 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_18'] = x_parse_added_lines__mutmut_18 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_19'] = x_parse_added_lines__mutmut_19 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_20'] = x_parse_added_lines__mutmut_20 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_21'] = x_parse_added_lines__mutmut_21 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_22'] = x_parse_added_lines__mutmut_22 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_23'] = x_parse_added_lines__mutmut_23 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_24'] = x_parse_added_lines__mutmut_24 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_25'] = x_parse_added_lines__mutmut_25 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_26'] = x_parse_added_lines__mutmut_26 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_27'] = x_parse_added_lines__mutmut_27 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_28'] = x_parse_added_lines__mutmut_28 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_29'] = x_parse_added_lines__mutmut_29 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_30'] = x_parse_added_lines__mutmut_30 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_31'] = x_parse_added_lines__mutmut_31 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_32'] = x_parse_added_lines__mutmut_32 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_33'] = x_parse_added_lines__mutmut_33 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_34'] = x_parse_added_lines__mutmut_34 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_35'] = x_parse_added_lines__mutmut_35 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_36'] = x_parse_added_lines__mutmut_36 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_37'] = x_parse_added_lines__mutmut_37 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_38'] = x_parse_added_lines__mutmut_38 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_39'] = x_parse_added_lines__mutmut_39 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_40'] = x_parse_added_lines__mutmut_40 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_41'] = x_parse_added_lines__mutmut_41 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_42'] = x_parse_added_lines__mutmut_42 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_43'] = x_parse_added_lines__mutmut_43 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_44'] = x_parse_added_lines__mutmut_44 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_45'] = x_parse_added_lines__mutmut_45 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_46'] = x_parse_added_lines__mutmut_46 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_47'] = x_parse_added_lines__mutmut_47 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_48'] = x_parse_added_lines__mutmut_48 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_49'] = x_parse_added_lines__mutmut_49 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_50'] = x_parse_added_lines__mutmut_50 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_51'] = x_parse_added_lines__mutmut_51 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_52'] = x_parse_added_lines__mutmut_52 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_53'] = x_parse_added_lines__mutmut_53 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_54'] = x_parse_added_lines__mutmut_54 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_55'] = x_parse_added_lines__mutmut_55 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_56'] = x_parse_added_lines__mutmut_56 # type: ignore # mutmut generated
mutants_x_parse_added_lines__mutmut['x_parse_added_lines__mutmut_57'] = x_parse_added_lines__mutmut_57 # type: ignore # mutmut generated
mutants_x__decode_git_output__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__decode_git_output__mutmut)
def _decode_git_output(output: str | bytes) -> str:
    """Decode Git's byte-preserving output without losing valid path bytes."""
    return output if isinstance(output, str) else output.decode("utf-8", "surrogateescape")


def x__decode_git_output__mutmut_orig(output: str | bytes) -> str:
    """Decode Git's byte-preserving output without losing valid path bytes."""
    return output if isinstance(output, str) else output.decode("utf-8", "surrogateescape")


def x__decode_git_output__mutmut_1(output: str | bytes) -> str:
    """Decode Git's byte-preserving output without losing valid path bytes."""
    return output if isinstance(output, str) else output.decode(None, "surrogateescape")


def x__decode_git_output__mutmut_2(output: str | bytes) -> str:
    """Decode Git's byte-preserving output without losing valid path bytes."""
    return output if isinstance(output, str) else output.decode("utf-8", None)


def x__decode_git_output__mutmut_3(output: str | bytes) -> str:
    """Decode Git's byte-preserving output without losing valid path bytes."""
    return output if isinstance(output, str) else output.decode("surrogateescape")


def x__decode_git_output__mutmut_4(output: str | bytes) -> str:
    """Decode Git's byte-preserving output without losing valid path bytes."""
    return output if isinstance(output, str) else output.decode("utf-8", )


def x__decode_git_output__mutmut_5(output: str | bytes) -> str:
    """Decode Git's byte-preserving output without losing valid path bytes."""
    return output if isinstance(output, str) else output.decode("XXutf-8XX", "surrogateescape")


def x__decode_git_output__mutmut_6(output: str | bytes) -> str:
    """Decode Git's byte-preserving output without losing valid path bytes."""
    return output if isinstance(output, str) else output.decode("UTF-8", "surrogateescape")


def x__decode_git_output__mutmut_7(output: str | bytes) -> str:
    """Decode Git's byte-preserving output without losing valid path bytes."""
    return output if isinstance(output, str) else output.decode("utf-8", "XXsurrogateescapeXX")


def x__decode_git_output__mutmut_8(output: str | bytes) -> str:
    """Decode Git's byte-preserving output without losing valid path bytes."""
    return output if isinstance(output, str) else output.decode("utf-8", "SURROGATEESCAPE")

mutants_x__decode_git_output__mutmut['_mutmut_orig'] = x__decode_git_output__mutmut_orig # type: ignore # mutmut generated
mutants_x__decode_git_output__mutmut['x__decode_git_output__mutmut_1'] = x__decode_git_output__mutmut_1 # type: ignore # mutmut generated
mutants_x__decode_git_output__mutmut['x__decode_git_output__mutmut_2'] = x__decode_git_output__mutmut_2 # type: ignore # mutmut generated
mutants_x__decode_git_output__mutmut['x__decode_git_output__mutmut_3'] = x__decode_git_output__mutmut_3 # type: ignore # mutmut generated
mutants_x__decode_git_output__mutmut['x__decode_git_output__mutmut_4'] = x__decode_git_output__mutmut_4 # type: ignore # mutmut generated
mutants_x__decode_git_output__mutmut['x__decode_git_output__mutmut_5'] = x__decode_git_output__mutmut_5 # type: ignore # mutmut generated
mutants_x__decode_git_output__mutmut['x__decode_git_output__mutmut_6'] = x__decode_git_output__mutmut_6 # type: ignore # mutmut generated
mutants_x__decode_git_output__mutmut['x__decode_git_output__mutmut_7'] = x__decode_git_output__mutmut_7 # type: ignore # mutmut generated
mutants_x__decode_git_output__mutmut['x__decode_git_output__mutmut_8'] = x__decode_git_output__mutmut_8 # type: ignore # mutmut generated
mutants_x__default_git_runner__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__default_git_runner__mutmut)
def _default_git_runner(args: list[str], cwd: Path) -> subprocess.CompletedProcess[bytes]:
    """Run ``git <args>`` in ``cwd`` and capture its output (the default seam).

    argv0 is the fixed literal ``git`` (never a caller-supplied path) and
    ``shell`` is never used; the only caller-controlled token is the ref, which
    the rule validates against :data:`_SAFE_REF_RE` before it reaches here.
    """
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        check=False,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0", "GCM_INTERACTIVE": "Never"},
    )


def x__default_git_runner__mutmut_orig(args: list[str], cwd: Path) -> subprocess.CompletedProcess[bytes]:
    """Run ``git <args>`` in ``cwd`` and capture its output (the default seam).

    argv0 is the fixed literal ``git`` (never a caller-supplied path) and
    ``shell`` is never used; the only caller-controlled token is the ref, which
    the rule validates against :data:`_SAFE_REF_RE` before it reaches here.
    """
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        check=False,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0", "GCM_INTERACTIVE": "Never"},
    )


def x__default_git_runner__mutmut_1(args: list[str], cwd: Path) -> subprocess.CompletedProcess[bytes]:
    """Run ``git <args>`` in ``cwd`` and capture its output (the default seam).

    argv0 is the fixed literal ``git`` (never a caller-supplied path) and
    ``shell`` is never used; the only caller-controlled token is the ref, which
    the rule validates against :data:`_SAFE_REF_RE` before it reaches here.
    """
    return subprocess.run(
        None,
        cwd=cwd,
        capture_output=True,
        check=False,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0", "GCM_INTERACTIVE": "Never"},
    )


def x__default_git_runner__mutmut_2(args: list[str], cwd: Path) -> subprocess.CompletedProcess[bytes]:
    """Run ``git <args>`` in ``cwd`` and capture its output (the default seam).

    argv0 is the fixed literal ``git`` (never a caller-supplied path) and
    ``shell`` is never used; the only caller-controlled token is the ref, which
    the rule validates against :data:`_SAFE_REF_RE` before it reaches here.
    """
    return subprocess.run(
        ["git", *args],
        cwd=None,
        capture_output=True,
        check=False,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0", "GCM_INTERACTIVE": "Never"},
    )


def x__default_git_runner__mutmut_3(args: list[str], cwd: Path) -> subprocess.CompletedProcess[bytes]:
    """Run ``git <args>`` in ``cwd`` and capture its output (the default seam).

    argv0 is the fixed literal ``git`` (never a caller-supplied path) and
    ``shell`` is never used; the only caller-controlled token is the ref, which
    the rule validates against :data:`_SAFE_REF_RE` before it reaches here.
    """
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=None,
        check=False,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0", "GCM_INTERACTIVE": "Never"},
    )


def x__default_git_runner__mutmut_4(args: list[str], cwd: Path) -> subprocess.CompletedProcess[bytes]:
    """Run ``git <args>`` in ``cwd`` and capture its output (the default seam).

    argv0 is the fixed literal ``git`` (never a caller-supplied path) and
    ``shell`` is never used; the only caller-controlled token is the ref, which
    the rule validates against :data:`_SAFE_REF_RE` before it reaches here.
    """
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        check=None,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0", "GCM_INTERACTIVE": "Never"},
    )


def x__default_git_runner__mutmut_5(args: list[str], cwd: Path) -> subprocess.CompletedProcess[bytes]:
    """Run ``git <args>`` in ``cwd`` and capture its output (the default seam).

    argv0 is the fixed literal ``git`` (never a caller-supplied path) and
    ``shell`` is never used; the only caller-controlled token is the ref, which
    the rule validates against :data:`_SAFE_REF_RE` before it reaches here.
    """
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        check=False,
        env=None,
    )


def x__default_git_runner__mutmut_6(args: list[str], cwd: Path) -> subprocess.CompletedProcess[bytes]:
    """Run ``git <args>`` in ``cwd`` and capture its output (the default seam).

    argv0 is the fixed literal ``git`` (never a caller-supplied path) and
    ``shell`` is never used; the only caller-controlled token is the ref, which
    the rule validates against :data:`_SAFE_REF_RE` before it reaches here.
    """
    return subprocess.run(
        cwd=cwd,
        capture_output=True,
        check=False,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0", "GCM_INTERACTIVE": "Never"},
    )


def x__default_git_runner__mutmut_7(args: list[str], cwd: Path) -> subprocess.CompletedProcess[bytes]:
    """Run ``git <args>`` in ``cwd`` and capture its output (the default seam).

    argv0 is the fixed literal ``git`` (never a caller-supplied path) and
    ``shell`` is never used; the only caller-controlled token is the ref, which
    the rule validates against :data:`_SAFE_REF_RE` before it reaches here.
    """
    return subprocess.run(
        ["git", *args],
        capture_output=True,
        check=False,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0", "GCM_INTERACTIVE": "Never"},
    )


def x__default_git_runner__mutmut_8(args: list[str], cwd: Path) -> subprocess.CompletedProcess[bytes]:
    """Run ``git <args>`` in ``cwd`` and capture its output (the default seam).

    argv0 is the fixed literal ``git`` (never a caller-supplied path) and
    ``shell`` is never used; the only caller-controlled token is the ref, which
    the rule validates against :data:`_SAFE_REF_RE` before it reaches here.
    """
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=False,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0", "GCM_INTERACTIVE": "Never"},
    )


def x__default_git_runner__mutmut_9(args: list[str], cwd: Path) -> subprocess.CompletedProcess[bytes]:
    """Run ``git <args>`` in ``cwd`` and capture its output (the default seam).

    argv0 is the fixed literal ``git`` (never a caller-supplied path) and
    ``shell`` is never used; the only caller-controlled token is the ref, which
    the rule validates against :data:`_SAFE_REF_RE` before it reaches here.
    """
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0", "GCM_INTERACTIVE": "Never"},
    )


def x__default_git_runner__mutmut_10(args: list[str], cwd: Path) -> subprocess.CompletedProcess[bytes]:
    """Run ``git <args>`` in ``cwd`` and capture its output (the default seam).

    argv0 is the fixed literal ``git`` (never a caller-supplied path) and
    ``shell`` is never used; the only caller-controlled token is the ref, which
    the rule validates against :data:`_SAFE_REF_RE` before it reaches here.
    """
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        check=False,
        )


def x__default_git_runner__mutmut_11(args: list[str], cwd: Path) -> subprocess.CompletedProcess[bytes]:
    """Run ``git <args>`` in ``cwd`` and capture its output (the default seam).

    argv0 is the fixed literal ``git`` (never a caller-supplied path) and
    ``shell`` is never used; the only caller-controlled token is the ref, which
    the rule validates against :data:`_SAFE_REF_RE` before it reaches here.
    """
    return subprocess.run(
        ["XXgitXX", *args],
        cwd=cwd,
        capture_output=True,
        check=False,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0", "GCM_INTERACTIVE": "Never"},
    )


def x__default_git_runner__mutmut_12(args: list[str], cwd: Path) -> subprocess.CompletedProcess[bytes]:
    """Run ``git <args>`` in ``cwd`` and capture its output (the default seam).

    argv0 is the fixed literal ``git`` (never a caller-supplied path) and
    ``shell`` is never used; the only caller-controlled token is the ref, which
    the rule validates against :data:`_SAFE_REF_RE` before it reaches here.
    """
    return subprocess.run(
        ["GIT", *args],
        cwd=cwd,
        capture_output=True,
        check=False,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0", "GCM_INTERACTIVE": "Never"},
    )


def x__default_git_runner__mutmut_13(args: list[str], cwd: Path) -> subprocess.CompletedProcess[bytes]:
    """Run ``git <args>`` in ``cwd`` and capture its output (the default seam).

    argv0 is the fixed literal ``git`` (never a caller-supplied path) and
    ``shell`` is never used; the only caller-controlled token is the ref, which
    the rule validates against :data:`_SAFE_REF_RE` before it reaches here.
    """
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=False,
        check=False,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0", "GCM_INTERACTIVE": "Never"},
    )


def x__default_git_runner__mutmut_14(args: list[str], cwd: Path) -> subprocess.CompletedProcess[bytes]:
    """Run ``git <args>`` in ``cwd`` and capture its output (the default seam).

    argv0 is the fixed literal ``git`` (never a caller-supplied path) and
    ``shell`` is never used; the only caller-controlled token is the ref, which
    the rule validates against :data:`_SAFE_REF_RE` before it reaches here.
    """
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        check=True,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0", "GCM_INTERACTIVE": "Never"},
    )


def x__default_git_runner__mutmut_15(args: list[str], cwd: Path) -> subprocess.CompletedProcess[bytes]:
    """Run ``git <args>`` in ``cwd`` and capture its output (the default seam).

    argv0 is the fixed literal ``git`` (never a caller-supplied path) and
    ``shell`` is never used; the only caller-controlled token is the ref, which
    the rule validates against :data:`_SAFE_REF_RE` before it reaches here.
    """
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        check=False,
        env={**os.environ, "XXGIT_TERMINAL_PROMPTXX": "0", "GCM_INTERACTIVE": "Never"},
    )


def x__default_git_runner__mutmut_16(args: list[str], cwd: Path) -> subprocess.CompletedProcess[bytes]:
    """Run ``git <args>`` in ``cwd`` and capture its output (the default seam).

    argv0 is the fixed literal ``git`` (never a caller-supplied path) and
    ``shell`` is never used; the only caller-controlled token is the ref, which
    the rule validates against :data:`_SAFE_REF_RE` before it reaches here.
    """
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        check=False,
        env={**os.environ, "git_terminal_prompt": "0", "GCM_INTERACTIVE": "Never"},
    )


def x__default_git_runner__mutmut_17(args: list[str], cwd: Path) -> subprocess.CompletedProcess[bytes]:
    """Run ``git <args>`` in ``cwd`` and capture its output (the default seam).

    argv0 is the fixed literal ``git`` (never a caller-supplied path) and
    ``shell`` is never used; the only caller-controlled token is the ref, which
    the rule validates against :data:`_SAFE_REF_RE` before it reaches here.
    """
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        check=False,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "XX0XX", "GCM_INTERACTIVE": "Never"},
    )


def x__default_git_runner__mutmut_18(args: list[str], cwd: Path) -> subprocess.CompletedProcess[bytes]:
    """Run ``git <args>`` in ``cwd`` and capture its output (the default seam).

    argv0 is the fixed literal ``git`` (never a caller-supplied path) and
    ``shell`` is never used; the only caller-controlled token is the ref, which
    the rule validates against :data:`_SAFE_REF_RE` before it reaches here.
    """
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        check=False,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0", "XXGCM_INTERACTIVEXX": "Never"},
    )


def x__default_git_runner__mutmut_19(args: list[str], cwd: Path) -> subprocess.CompletedProcess[bytes]:
    """Run ``git <args>`` in ``cwd`` and capture its output (the default seam).

    argv0 is the fixed literal ``git`` (never a caller-supplied path) and
    ``shell`` is never used; the only caller-controlled token is the ref, which
    the rule validates against :data:`_SAFE_REF_RE` before it reaches here.
    """
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        check=False,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0", "gcm_interactive": "Never"},
    )


def x__default_git_runner__mutmut_20(args: list[str], cwd: Path) -> subprocess.CompletedProcess[bytes]:
    """Run ``git <args>`` in ``cwd`` and capture its output (the default seam).

    argv0 is the fixed literal ``git`` (never a caller-supplied path) and
    ``shell`` is never used; the only caller-controlled token is the ref, which
    the rule validates against :data:`_SAFE_REF_RE` before it reaches here.
    """
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        check=False,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0", "GCM_INTERACTIVE": "XXNeverXX"},
    )


def x__default_git_runner__mutmut_21(args: list[str], cwd: Path) -> subprocess.CompletedProcess[bytes]:
    """Run ``git <args>`` in ``cwd`` and capture its output (the default seam).

    argv0 is the fixed literal ``git`` (never a caller-supplied path) and
    ``shell`` is never used; the only caller-controlled token is the ref, which
    the rule validates against :data:`_SAFE_REF_RE` before it reaches here.
    """
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        check=False,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0", "GCM_INTERACTIVE": "never"},
    )


def x__default_git_runner__mutmut_22(args: list[str], cwd: Path) -> subprocess.CompletedProcess[bytes]:
    """Run ``git <args>`` in ``cwd`` and capture its output (the default seam).

    argv0 is the fixed literal ``git`` (never a caller-supplied path) and
    ``shell`` is never used; the only caller-controlled token is the ref, which
    the rule validates against :data:`_SAFE_REF_RE` before it reaches here.
    """
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        check=False,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0", "GCM_INTERACTIVE": "NEVER"},
    )

mutants_x__default_git_runner__mutmut['_mutmut_orig'] = x__default_git_runner__mutmut_orig # type: ignore # mutmut generated
mutants_x__default_git_runner__mutmut['x__default_git_runner__mutmut_1'] = x__default_git_runner__mutmut_1 # type: ignore # mutmut generated
mutants_x__default_git_runner__mutmut['x__default_git_runner__mutmut_2'] = x__default_git_runner__mutmut_2 # type: ignore # mutmut generated
mutants_x__default_git_runner__mutmut['x__default_git_runner__mutmut_3'] = x__default_git_runner__mutmut_3 # type: ignore # mutmut generated
mutants_x__default_git_runner__mutmut['x__default_git_runner__mutmut_4'] = x__default_git_runner__mutmut_4 # type: ignore # mutmut generated
mutants_x__default_git_runner__mutmut['x__default_git_runner__mutmut_5'] = x__default_git_runner__mutmut_5 # type: ignore # mutmut generated
mutants_x__default_git_runner__mutmut['x__default_git_runner__mutmut_6'] = x__default_git_runner__mutmut_6 # type: ignore # mutmut generated
mutants_x__default_git_runner__mutmut['x__default_git_runner__mutmut_7'] = x__default_git_runner__mutmut_7 # type: ignore # mutmut generated
mutants_x__default_git_runner__mutmut['x__default_git_runner__mutmut_8'] = x__default_git_runner__mutmut_8 # type: ignore # mutmut generated
mutants_x__default_git_runner__mutmut['x__default_git_runner__mutmut_9'] = x__default_git_runner__mutmut_9 # type: ignore # mutmut generated
mutants_x__default_git_runner__mutmut['x__default_git_runner__mutmut_10'] = x__default_git_runner__mutmut_10 # type: ignore # mutmut generated
mutants_x__default_git_runner__mutmut['x__default_git_runner__mutmut_11'] = x__default_git_runner__mutmut_11 # type: ignore # mutmut generated
mutants_x__default_git_runner__mutmut['x__default_git_runner__mutmut_12'] = x__default_git_runner__mutmut_12 # type: ignore # mutmut generated
mutants_x__default_git_runner__mutmut['x__default_git_runner__mutmut_13'] = x__default_git_runner__mutmut_13 # type: ignore # mutmut generated
mutants_x__default_git_runner__mutmut['x__default_git_runner__mutmut_14'] = x__default_git_runner__mutmut_14 # type: ignore # mutmut generated
mutants_x__default_git_runner__mutmut['x__default_git_runner__mutmut_15'] = x__default_git_runner__mutmut_15 # type: ignore # mutmut generated
mutants_x__default_git_runner__mutmut['x__default_git_runner__mutmut_16'] = x__default_git_runner__mutmut_16 # type: ignore # mutmut generated
mutants_x__default_git_runner__mutmut['x__default_git_runner__mutmut_17'] = x__default_git_runner__mutmut_17 # type: ignore # mutmut generated
mutants_x__default_git_runner__mutmut['x__default_git_runner__mutmut_18'] = x__default_git_runner__mutmut_18 # type: ignore # mutmut generated
mutants_x__default_git_runner__mutmut['x__default_git_runner__mutmut_19'] = x__default_git_runner__mutmut_19 # type: ignore # mutmut generated
mutants_x__default_git_runner__mutmut['x__default_git_runner__mutmut_20'] = x__default_git_runner__mutmut_20 # type: ignore # mutmut generated
mutants_x__default_git_runner__mutmut['x__default_git_runner__mutmut_21'] = x__default_git_runner__mutmut_21 # type: ignore # mutmut generated
mutants_x__default_git_runner__mutmut['x__default_git_runner__mutmut_22'] = x__default_git_runner__mutmut_22 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁNewCodeCoverageǁ_report_path__mutmut: MutantDict = {}  # type: ignore
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut: MutantDict = {}  # type: ignore
mutants_xǁNewCodeCoverageǁ_changed_lines__mutmut: MutantDict = {}  # type: ignore
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut: MutantDict = {}  # type: ignore
mutants_xǁNewCodeCoverageǁenumerate_files__mutmut: MutantDict = {}  # type: ignore
mutants_xǁNewCodeCoverageǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore
mutants_xǁNewCodeCoverageǁrun__mutmut: MutantDict = {}  # type: ignore


class NewCodeCoverage(FitnessRule):
    """Flags changed files whose ADDED lines are covered below the floor."""

    name = "new-code-coverage"
    remediation = REMEDIATION
    extensions = (".py",)

    #: Rule-specific knobs — instance attrs so ``from_config`` overrides them.
    floor_pct: float = DEFAULT_FLOOR_PCT
    coverage_report: str = DEFAULT_COVERAGE_REPORT
    base_ref: str = DEFAULT_BASE_REF
    #: The git command runner (DI seam) — set by ``from_config`` / ``build`` so a
    #: test can inject canned diff output without a real repo or monkeypatching.
    git_runner: GitRunner
    exact_config: dict[str, Any] | None = None

    @classmethod
    @_mutmut_mutated(mutants_xǁNewCodeCoverageǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        if any(key in config for key in ("exact_base_commit", "candidate_commit", "coverage_receipt")):
            rule.exact_config = dict(config)
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        if any(key in config for key in ("exact_base_commit", "candidate_commit", "coverage_receipt")):
            rule.exact_config = dict(config)
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = None
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        if any(key in config for key in ("exact_base_commit", "candidate_commit", "coverage_receipt")):
            rule.exact_config = dict(config)
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        if any(key in config for key in ("exact_base_commit", "candidate_commit", "coverage_receipt")):
            rule.exact_config = dict(config)
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        if any(key in config for key in ("exact_base_commit", "candidate_commit", "coverage_receipt")):
            rule.exact_config = dict(config)
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        if any(key in config for key in ("exact_base_commit", "candidate_commit", "coverage_receipt")):
            rule.exact_config = dict(config)
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(config, )
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        if any(key in config for key in ("exact_base_commit", "candidate_commit", "coverage_receipt")):
            rule.exact_config = dict(config)
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = None
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        if any(key in config for key in ("exact_base_commit", "candidate_commit", "coverage_receipt")):
            rule.exact_config = dict(config)
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(None)
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        if any(key in config for key in ("exact_base_commit", "candidate_commit", "coverage_receipt")):
            rule.exact_config = dict(config)
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get(None, DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        if any(key in config for key in ("exact_base_commit", "candidate_commit", "coverage_receipt")):
            rule.exact_config = dict(config)
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", None))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        if any(key in config for key in ("exact_base_commit", "candidate_commit", "coverage_receipt")):
            rule.exact_config = dict(config)
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get(DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        if any(key in config for key in ("exact_base_commit", "candidate_commit", "coverage_receipt")):
            rule.exact_config = dict(config)
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", ))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        if any(key in config for key in ("exact_base_commit", "candidate_commit", "coverage_receipt")):
            rule.exact_config = dict(config)
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("XXfloor_pctXX", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        if any(key in config for key in ("exact_base_commit", "candidate_commit", "coverage_receipt")):
            rule.exact_config = dict(config)
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_13(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("FLOOR_PCT", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        if any(key in config for key in ("exact_base_commit", "candidate_commit", "coverage_receipt")):
            rule.exact_config = dict(config)
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_14(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = None
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        if any(key in config for key in ("exact_base_commit", "candidate_commit", "coverage_receipt")):
            rule.exact_config = dict(config)
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_15(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(None)
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        if any(key in config for key in ("exact_base_commit", "candidate_commit", "coverage_receipt")):
            rule.exact_config = dict(config)
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_16(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get(None, DEFAULT_COVERAGE_REPORT))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        if any(key in config for key in ("exact_base_commit", "candidate_commit", "coverage_receipt")):
            rule.exact_config = dict(config)
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_17(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", None))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        if any(key in config for key in ("exact_base_commit", "candidate_commit", "coverage_receipt")):
            rule.exact_config = dict(config)
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_18(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get(DEFAULT_COVERAGE_REPORT))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        if any(key in config for key in ("exact_base_commit", "candidate_commit", "coverage_receipt")):
            rule.exact_config = dict(config)
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_19(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", ))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        if any(key in config for key in ("exact_base_commit", "candidate_commit", "coverage_receipt")):
            rule.exact_config = dict(config)
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_20(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("XXcoverage_reportXX", DEFAULT_COVERAGE_REPORT))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        if any(key in config for key in ("exact_base_commit", "candidate_commit", "coverage_receipt")):
            rule.exact_config = dict(config)
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_21(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("COVERAGE_REPORT", DEFAULT_COVERAGE_REPORT))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        if any(key in config for key in ("exact_base_commit", "candidate_commit", "coverage_receipt")):
            rule.exact_config = dict(config)
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_22(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        rule.base_ref = None
        rule.git_runner = _default_git_runner
        if any(key in config for key in ("exact_base_commit", "candidate_commit", "coverage_receipt")):
            rule.exact_config = dict(config)
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_23(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        rule.base_ref = str(None)
        rule.git_runner = _default_git_runner
        if any(key in config for key in ("exact_base_commit", "candidate_commit", "coverage_receipt")):
            rule.exact_config = dict(config)
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_24(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        rule.base_ref = str(config.get(None, DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        if any(key in config for key in ("exact_base_commit", "candidate_commit", "coverage_receipt")):
            rule.exact_config = dict(config)
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_25(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        rule.base_ref = str(config.get("base_ref", None))
        rule.git_runner = _default_git_runner
        if any(key in config for key in ("exact_base_commit", "candidate_commit", "coverage_receipt")):
            rule.exact_config = dict(config)
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_26(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        rule.base_ref = str(config.get(DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        if any(key in config for key in ("exact_base_commit", "candidate_commit", "coverage_receipt")):
            rule.exact_config = dict(config)
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_27(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        rule.base_ref = str(config.get("base_ref", ))
        rule.git_runner = _default_git_runner
        if any(key in config for key in ("exact_base_commit", "candidate_commit", "coverage_receipt")):
            rule.exact_config = dict(config)
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_28(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        rule.base_ref = str(config.get("XXbase_refXX", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        if any(key in config for key in ("exact_base_commit", "candidate_commit", "coverage_receipt")):
            rule.exact_config = dict(config)
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_29(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        rule.base_ref = str(config.get("BASE_REF", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        if any(key in config for key in ("exact_base_commit", "candidate_commit", "coverage_receipt")):
            rule.exact_config = dict(config)
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_30(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = None
        if any(key in config for key in ("exact_base_commit", "candidate_commit", "coverage_receipt")):
            rule.exact_config = dict(config)
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_31(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        if any(None):
            rule.exact_config = dict(config)
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_32(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        if any(key not in config for key in ("exact_base_commit", "candidate_commit", "coverage_receipt")):
            rule.exact_config = dict(config)
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_33(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        if any(key in config for key in ("XXexact_base_commitXX", "candidate_commit", "coverage_receipt")):
            rule.exact_config = dict(config)
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_34(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        if any(key in config for key in ("EXACT_BASE_COMMIT", "candidate_commit", "coverage_receipt")):
            rule.exact_config = dict(config)
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_35(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        if any(key in config for key in ("exact_base_commit", "XXcandidate_commitXX", "coverage_receipt")):
            rule.exact_config = dict(config)
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_36(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        if any(key in config for key in ("exact_base_commit", "CANDIDATE_COMMIT", "coverage_receipt")):
            rule.exact_config = dict(config)
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_37(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        if any(key in config for key in ("exact_base_commit", "candidate_commit", "XXcoverage_receiptXX")):
            rule.exact_config = dict(config)
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_38(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        if any(key in config for key in ("exact_base_commit", "candidate_commit", "COVERAGE_RECEIPT")):
            rule.exact_config = dict(config)
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_39(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        if any(key in config for key in ("exact_base_commit", "candidate_commit", "coverage_receipt")):
            rule.exact_config = None
        return rule

    @classmethod
    def xǁNewCodeCoverageǁfrom_config__mutmut_40(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        if any(key in config for key in ("exact_base_commit", "candidate_commit", "coverage_receipt")):
            rule.exact_config = dict(None)
        return rule

    @_mutmut_mutated(mutants_xǁNewCodeCoverageǁ_report_path__mutmut)
    def _report_path(self) -> Path:
        report = Path(self.coverage_report)
        return report if report.is_absolute() else self._repo_root / report

    def xǁNewCodeCoverageǁ_report_path__mutmut_orig(self) -> Path:
        report = Path(self.coverage_report)
        return report if report.is_absolute() else self._repo_root / report

    def xǁNewCodeCoverageǁ_report_path__mutmut_1(self) -> Path:
        report = None
        return report if report.is_absolute() else self._repo_root / report

    def xǁNewCodeCoverageǁ_report_path__mutmut_2(self) -> Path:
        report = Path(None)
        return report if report.is_absolute() else self._repo_root / report

    def xǁNewCodeCoverageǁ_report_path__mutmut_3(self) -> Path:
        report = Path(self.coverage_report)
        return report if report.is_absolute() else self._repo_root * report

    @_mutmut_mutated(mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut)
    def _refresh_remote_base(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_orig(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_1(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = None
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_2(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(None, self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_3(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], None)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_4(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_5(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], )
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_6(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["XXremoteXX"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_7(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["REMOTE"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_8(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode == 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_9(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 1:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_10(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = None
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_11(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(None, key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_12(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=None, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_13(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=None)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_14(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_15(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_16(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, )
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_17(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(None).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_18(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=False)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_19(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = None
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_20(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next(None, None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_21(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next(None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_22(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), )
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_23(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(None)), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_24(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is not None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_25(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = None
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_26(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) - 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_27(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 2 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_28(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch and not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_29(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_30(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_31(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(None, branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_32(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", None):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_33(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_34(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", ):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_35(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"XX[A-Za-z0-9_./-]+XX", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_36(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[a-za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_37(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-ZA-Z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_38(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = None
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_39(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = None
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_40(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            None,
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_41(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            None,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_42(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_43(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_44(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["XXfetchXX", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_45(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["FETCH", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_46(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "XX--quietXX", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_47(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--QUIET", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_48(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "XX--no-tagsXX", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_49(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--NO-TAGS", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_50(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "XX--XX", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_51(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode != 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_52(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 1:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_53(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = None
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_54(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(None).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_55(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = None
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_56(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[+1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_57(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-2] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_58(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            None,
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_59(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=None,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_60(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            file=sys.stderr,
        )

    def xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_61(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            )

    @_mutmut_mutated(mutants_xǁNewCodeCoverageǁ_changed_lines__mutmut)
    def _changed_lines(self) -> dict[str, set[int]]:
        """Added lines from the merge-base through the current checkout.

        A remote-tracking base is refreshed first. Refresh failure warns and
        continues with the cached ref. Returns ``{}`` (→ a soft PASS) when the
        base ref is unsafe/unresolvable, the merge-base can't be computed, or
        the diff command fails — none of which is a coverage defect.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return {}
        self._refresh_remote_base()
        merge_base = self.git_runner(["merge-base", self.base_ref, "HEAD"], self._repo_root)
        if merge_base.returncode != 0:
            return {}
        base = _decode_git_output(merge_base.stdout).strip()
        if not base:
            return {}
        # Comparing the base tree to the checkout includes committed, staged,
        # and unstaged changes. ``base...HEAD`` omits the latter two and made a
        # pre-commit local gate pass code that CI rejected after it was committed.
        diff = self.git_runner(["diff", "-U0", base, "--"], self._repo_root)
        if diff.returncode != 0:
            return {}
        changed = parse_added_lines(_decode_git_output(diff.stdout))
        changed.update(self._untracked_added_lines())
        return changed

    def xǁNewCodeCoverageǁ_changed_lines__mutmut_orig(self) -> dict[str, set[int]]:
        """Added lines from the merge-base through the current checkout.

        A remote-tracking base is refreshed first. Refresh failure warns and
        continues with the cached ref. Returns ``{}`` (→ a soft PASS) when the
        base ref is unsafe/unresolvable, the merge-base can't be computed, or
        the diff command fails — none of which is a coverage defect.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return {}
        self._refresh_remote_base()
        merge_base = self.git_runner(["merge-base", self.base_ref, "HEAD"], self._repo_root)
        if merge_base.returncode != 0:
            return {}
        base = _decode_git_output(merge_base.stdout).strip()
        if not base:
            return {}
        # Comparing the base tree to the checkout includes committed, staged,
        # and unstaged changes. ``base...HEAD`` omits the latter two and made a
        # pre-commit local gate pass code that CI rejected after it was committed.
        diff = self.git_runner(["diff", "-U0", base, "--"], self._repo_root)
        if diff.returncode != 0:
            return {}
        changed = parse_added_lines(_decode_git_output(diff.stdout))
        changed.update(self._untracked_added_lines())
        return changed

    def xǁNewCodeCoverageǁ_changed_lines__mutmut_1(self) -> dict[str, set[int]]:
        """Added lines from the merge-base through the current checkout.

        A remote-tracking base is refreshed first. Refresh failure warns and
        continues with the cached ref. Returns ``{}`` (→ a soft PASS) when the
        base ref is unsafe/unresolvable, the merge-base can't be computed, or
        the diff command fails — none of which is a coverage defect.
        """
        if _SAFE_REF_RE.match(self.base_ref):
            return {}
        self._refresh_remote_base()
        merge_base = self.git_runner(["merge-base", self.base_ref, "HEAD"], self._repo_root)
        if merge_base.returncode != 0:
            return {}
        base = _decode_git_output(merge_base.stdout).strip()
        if not base:
            return {}
        # Comparing the base tree to the checkout includes committed, staged,
        # and unstaged changes. ``base...HEAD`` omits the latter two and made a
        # pre-commit local gate pass code that CI rejected after it was committed.
        diff = self.git_runner(["diff", "-U0", base, "--"], self._repo_root)
        if diff.returncode != 0:
            return {}
        changed = parse_added_lines(_decode_git_output(diff.stdout))
        changed.update(self._untracked_added_lines())
        return changed

    def xǁNewCodeCoverageǁ_changed_lines__mutmut_2(self) -> dict[str, set[int]]:
        """Added lines from the merge-base through the current checkout.

        A remote-tracking base is refreshed first. Refresh failure warns and
        continues with the cached ref. Returns ``{}`` (→ a soft PASS) when the
        base ref is unsafe/unresolvable, the merge-base can't be computed, or
        the diff command fails — none of which is a coverage defect.
        """
        if not _SAFE_REF_RE.match(None):
            return {}
        self._refresh_remote_base()
        merge_base = self.git_runner(["merge-base", self.base_ref, "HEAD"], self._repo_root)
        if merge_base.returncode != 0:
            return {}
        base = _decode_git_output(merge_base.stdout).strip()
        if not base:
            return {}
        # Comparing the base tree to the checkout includes committed, staged,
        # and unstaged changes. ``base...HEAD`` omits the latter two and made a
        # pre-commit local gate pass code that CI rejected after it was committed.
        diff = self.git_runner(["diff", "-U0", base, "--"], self._repo_root)
        if diff.returncode != 0:
            return {}
        changed = parse_added_lines(_decode_git_output(diff.stdout))
        changed.update(self._untracked_added_lines())
        return changed

    def xǁNewCodeCoverageǁ_changed_lines__mutmut_3(self) -> dict[str, set[int]]:
        """Added lines from the merge-base through the current checkout.

        A remote-tracking base is refreshed first. Refresh failure warns and
        continues with the cached ref. Returns ``{}`` (→ a soft PASS) when the
        base ref is unsafe/unresolvable, the merge-base can't be computed, or
        the diff command fails — none of which is a coverage defect.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return {}
        self._refresh_remote_base()
        merge_base = None
        if merge_base.returncode != 0:
            return {}
        base = _decode_git_output(merge_base.stdout).strip()
        if not base:
            return {}
        # Comparing the base tree to the checkout includes committed, staged,
        # and unstaged changes. ``base...HEAD`` omits the latter two and made a
        # pre-commit local gate pass code that CI rejected after it was committed.
        diff = self.git_runner(["diff", "-U0", base, "--"], self._repo_root)
        if diff.returncode != 0:
            return {}
        changed = parse_added_lines(_decode_git_output(diff.stdout))
        changed.update(self._untracked_added_lines())
        return changed

    def xǁNewCodeCoverageǁ_changed_lines__mutmut_4(self) -> dict[str, set[int]]:
        """Added lines from the merge-base through the current checkout.

        A remote-tracking base is refreshed first. Refresh failure warns and
        continues with the cached ref. Returns ``{}`` (→ a soft PASS) when the
        base ref is unsafe/unresolvable, the merge-base can't be computed, or
        the diff command fails — none of which is a coverage defect.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return {}
        self._refresh_remote_base()
        merge_base = self.git_runner(None, self._repo_root)
        if merge_base.returncode != 0:
            return {}
        base = _decode_git_output(merge_base.stdout).strip()
        if not base:
            return {}
        # Comparing the base tree to the checkout includes committed, staged,
        # and unstaged changes. ``base...HEAD`` omits the latter two and made a
        # pre-commit local gate pass code that CI rejected after it was committed.
        diff = self.git_runner(["diff", "-U0", base, "--"], self._repo_root)
        if diff.returncode != 0:
            return {}
        changed = parse_added_lines(_decode_git_output(diff.stdout))
        changed.update(self._untracked_added_lines())
        return changed

    def xǁNewCodeCoverageǁ_changed_lines__mutmut_5(self) -> dict[str, set[int]]:
        """Added lines from the merge-base through the current checkout.

        A remote-tracking base is refreshed first. Refresh failure warns and
        continues with the cached ref. Returns ``{}`` (→ a soft PASS) when the
        base ref is unsafe/unresolvable, the merge-base can't be computed, or
        the diff command fails — none of which is a coverage defect.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return {}
        self._refresh_remote_base()
        merge_base = self.git_runner(["merge-base", self.base_ref, "HEAD"], None)
        if merge_base.returncode != 0:
            return {}
        base = _decode_git_output(merge_base.stdout).strip()
        if not base:
            return {}
        # Comparing the base tree to the checkout includes committed, staged,
        # and unstaged changes. ``base...HEAD`` omits the latter two and made a
        # pre-commit local gate pass code that CI rejected after it was committed.
        diff = self.git_runner(["diff", "-U0", base, "--"], self._repo_root)
        if diff.returncode != 0:
            return {}
        changed = parse_added_lines(_decode_git_output(diff.stdout))
        changed.update(self._untracked_added_lines())
        return changed

    def xǁNewCodeCoverageǁ_changed_lines__mutmut_6(self) -> dict[str, set[int]]:
        """Added lines from the merge-base through the current checkout.

        A remote-tracking base is refreshed first. Refresh failure warns and
        continues with the cached ref. Returns ``{}`` (→ a soft PASS) when the
        base ref is unsafe/unresolvable, the merge-base can't be computed, or
        the diff command fails — none of which is a coverage defect.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return {}
        self._refresh_remote_base()
        merge_base = self.git_runner(self._repo_root)
        if merge_base.returncode != 0:
            return {}
        base = _decode_git_output(merge_base.stdout).strip()
        if not base:
            return {}
        # Comparing the base tree to the checkout includes committed, staged,
        # and unstaged changes. ``base...HEAD`` omits the latter two and made a
        # pre-commit local gate pass code that CI rejected after it was committed.
        diff = self.git_runner(["diff", "-U0", base, "--"], self._repo_root)
        if diff.returncode != 0:
            return {}
        changed = parse_added_lines(_decode_git_output(diff.stdout))
        changed.update(self._untracked_added_lines())
        return changed

    def xǁNewCodeCoverageǁ_changed_lines__mutmut_7(self) -> dict[str, set[int]]:
        """Added lines from the merge-base through the current checkout.

        A remote-tracking base is refreshed first. Refresh failure warns and
        continues with the cached ref. Returns ``{}`` (→ a soft PASS) when the
        base ref is unsafe/unresolvable, the merge-base can't be computed, or
        the diff command fails — none of which is a coverage defect.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return {}
        self._refresh_remote_base()
        merge_base = self.git_runner(["merge-base", self.base_ref, "HEAD"], )
        if merge_base.returncode != 0:
            return {}
        base = _decode_git_output(merge_base.stdout).strip()
        if not base:
            return {}
        # Comparing the base tree to the checkout includes committed, staged,
        # and unstaged changes. ``base...HEAD`` omits the latter two and made a
        # pre-commit local gate pass code that CI rejected after it was committed.
        diff = self.git_runner(["diff", "-U0", base, "--"], self._repo_root)
        if diff.returncode != 0:
            return {}
        changed = parse_added_lines(_decode_git_output(diff.stdout))
        changed.update(self._untracked_added_lines())
        return changed

    def xǁNewCodeCoverageǁ_changed_lines__mutmut_8(self) -> dict[str, set[int]]:
        """Added lines from the merge-base through the current checkout.

        A remote-tracking base is refreshed first. Refresh failure warns and
        continues with the cached ref. Returns ``{}`` (→ a soft PASS) when the
        base ref is unsafe/unresolvable, the merge-base can't be computed, or
        the diff command fails — none of which is a coverage defect.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return {}
        self._refresh_remote_base()
        merge_base = self.git_runner(["XXmerge-baseXX", self.base_ref, "HEAD"], self._repo_root)
        if merge_base.returncode != 0:
            return {}
        base = _decode_git_output(merge_base.stdout).strip()
        if not base:
            return {}
        # Comparing the base tree to the checkout includes committed, staged,
        # and unstaged changes. ``base...HEAD`` omits the latter two and made a
        # pre-commit local gate pass code that CI rejected after it was committed.
        diff = self.git_runner(["diff", "-U0", base, "--"], self._repo_root)
        if diff.returncode != 0:
            return {}
        changed = parse_added_lines(_decode_git_output(diff.stdout))
        changed.update(self._untracked_added_lines())
        return changed

    def xǁNewCodeCoverageǁ_changed_lines__mutmut_9(self) -> dict[str, set[int]]:
        """Added lines from the merge-base through the current checkout.

        A remote-tracking base is refreshed first. Refresh failure warns and
        continues with the cached ref. Returns ``{}`` (→ a soft PASS) when the
        base ref is unsafe/unresolvable, the merge-base can't be computed, or
        the diff command fails — none of which is a coverage defect.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return {}
        self._refresh_remote_base()
        merge_base = self.git_runner(["MERGE-BASE", self.base_ref, "HEAD"], self._repo_root)
        if merge_base.returncode != 0:
            return {}
        base = _decode_git_output(merge_base.stdout).strip()
        if not base:
            return {}
        # Comparing the base tree to the checkout includes committed, staged,
        # and unstaged changes. ``base...HEAD`` omits the latter two and made a
        # pre-commit local gate pass code that CI rejected after it was committed.
        diff = self.git_runner(["diff", "-U0", base, "--"], self._repo_root)
        if diff.returncode != 0:
            return {}
        changed = parse_added_lines(_decode_git_output(diff.stdout))
        changed.update(self._untracked_added_lines())
        return changed

    def xǁNewCodeCoverageǁ_changed_lines__mutmut_10(self) -> dict[str, set[int]]:
        """Added lines from the merge-base through the current checkout.

        A remote-tracking base is refreshed first. Refresh failure warns and
        continues with the cached ref. Returns ``{}`` (→ a soft PASS) when the
        base ref is unsafe/unresolvable, the merge-base can't be computed, or
        the diff command fails — none of which is a coverage defect.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return {}
        self._refresh_remote_base()
        merge_base = self.git_runner(["merge-base", self.base_ref, "XXHEADXX"], self._repo_root)
        if merge_base.returncode != 0:
            return {}
        base = _decode_git_output(merge_base.stdout).strip()
        if not base:
            return {}
        # Comparing the base tree to the checkout includes committed, staged,
        # and unstaged changes. ``base...HEAD`` omits the latter two and made a
        # pre-commit local gate pass code that CI rejected after it was committed.
        diff = self.git_runner(["diff", "-U0", base, "--"], self._repo_root)
        if diff.returncode != 0:
            return {}
        changed = parse_added_lines(_decode_git_output(diff.stdout))
        changed.update(self._untracked_added_lines())
        return changed

    def xǁNewCodeCoverageǁ_changed_lines__mutmut_11(self) -> dict[str, set[int]]:
        """Added lines from the merge-base through the current checkout.

        A remote-tracking base is refreshed first. Refresh failure warns and
        continues with the cached ref. Returns ``{}`` (→ a soft PASS) when the
        base ref is unsafe/unresolvable, the merge-base can't be computed, or
        the diff command fails — none of which is a coverage defect.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return {}
        self._refresh_remote_base()
        merge_base = self.git_runner(["merge-base", self.base_ref, "head"], self._repo_root)
        if merge_base.returncode != 0:
            return {}
        base = _decode_git_output(merge_base.stdout).strip()
        if not base:
            return {}
        # Comparing the base tree to the checkout includes committed, staged,
        # and unstaged changes. ``base...HEAD`` omits the latter two and made a
        # pre-commit local gate pass code that CI rejected after it was committed.
        diff = self.git_runner(["diff", "-U0", base, "--"], self._repo_root)
        if diff.returncode != 0:
            return {}
        changed = parse_added_lines(_decode_git_output(diff.stdout))
        changed.update(self._untracked_added_lines())
        return changed

    def xǁNewCodeCoverageǁ_changed_lines__mutmut_12(self) -> dict[str, set[int]]:
        """Added lines from the merge-base through the current checkout.

        A remote-tracking base is refreshed first. Refresh failure warns and
        continues with the cached ref. Returns ``{}`` (→ a soft PASS) when the
        base ref is unsafe/unresolvable, the merge-base can't be computed, or
        the diff command fails — none of which is a coverage defect.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return {}
        self._refresh_remote_base()
        merge_base = self.git_runner(["merge-base", self.base_ref, "HEAD"], self._repo_root)
        if merge_base.returncode == 0:
            return {}
        base = _decode_git_output(merge_base.stdout).strip()
        if not base:
            return {}
        # Comparing the base tree to the checkout includes committed, staged,
        # and unstaged changes. ``base...HEAD`` omits the latter two and made a
        # pre-commit local gate pass code that CI rejected after it was committed.
        diff = self.git_runner(["diff", "-U0", base, "--"], self._repo_root)
        if diff.returncode != 0:
            return {}
        changed = parse_added_lines(_decode_git_output(diff.stdout))
        changed.update(self._untracked_added_lines())
        return changed

    def xǁNewCodeCoverageǁ_changed_lines__mutmut_13(self) -> dict[str, set[int]]:
        """Added lines from the merge-base through the current checkout.

        A remote-tracking base is refreshed first. Refresh failure warns and
        continues with the cached ref. Returns ``{}`` (→ a soft PASS) when the
        base ref is unsafe/unresolvable, the merge-base can't be computed, or
        the diff command fails — none of which is a coverage defect.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return {}
        self._refresh_remote_base()
        merge_base = self.git_runner(["merge-base", self.base_ref, "HEAD"], self._repo_root)
        if merge_base.returncode != 1:
            return {}
        base = _decode_git_output(merge_base.stdout).strip()
        if not base:
            return {}
        # Comparing the base tree to the checkout includes committed, staged,
        # and unstaged changes. ``base...HEAD`` omits the latter two and made a
        # pre-commit local gate pass code that CI rejected after it was committed.
        diff = self.git_runner(["diff", "-U0", base, "--"], self._repo_root)
        if diff.returncode != 0:
            return {}
        changed = parse_added_lines(_decode_git_output(diff.stdout))
        changed.update(self._untracked_added_lines())
        return changed

    def xǁNewCodeCoverageǁ_changed_lines__mutmut_14(self) -> dict[str, set[int]]:
        """Added lines from the merge-base through the current checkout.

        A remote-tracking base is refreshed first. Refresh failure warns and
        continues with the cached ref. Returns ``{}`` (→ a soft PASS) when the
        base ref is unsafe/unresolvable, the merge-base can't be computed, or
        the diff command fails — none of which is a coverage defect.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return {}
        self._refresh_remote_base()
        merge_base = self.git_runner(["merge-base", self.base_ref, "HEAD"], self._repo_root)
        if merge_base.returncode != 0:
            return {}
        base = None
        if not base:
            return {}
        # Comparing the base tree to the checkout includes committed, staged,
        # and unstaged changes. ``base...HEAD`` omits the latter two and made a
        # pre-commit local gate pass code that CI rejected after it was committed.
        diff = self.git_runner(["diff", "-U0", base, "--"], self._repo_root)
        if diff.returncode != 0:
            return {}
        changed = parse_added_lines(_decode_git_output(diff.stdout))
        changed.update(self._untracked_added_lines())
        return changed

    def xǁNewCodeCoverageǁ_changed_lines__mutmut_15(self) -> dict[str, set[int]]:
        """Added lines from the merge-base through the current checkout.

        A remote-tracking base is refreshed first. Refresh failure warns and
        continues with the cached ref. Returns ``{}`` (→ a soft PASS) when the
        base ref is unsafe/unresolvable, the merge-base can't be computed, or
        the diff command fails — none of which is a coverage defect.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return {}
        self._refresh_remote_base()
        merge_base = self.git_runner(["merge-base", self.base_ref, "HEAD"], self._repo_root)
        if merge_base.returncode != 0:
            return {}
        base = _decode_git_output(None).strip()
        if not base:
            return {}
        # Comparing the base tree to the checkout includes committed, staged,
        # and unstaged changes. ``base...HEAD`` omits the latter two and made a
        # pre-commit local gate pass code that CI rejected after it was committed.
        diff = self.git_runner(["diff", "-U0", base, "--"], self._repo_root)
        if diff.returncode != 0:
            return {}
        changed = parse_added_lines(_decode_git_output(diff.stdout))
        changed.update(self._untracked_added_lines())
        return changed

    def xǁNewCodeCoverageǁ_changed_lines__mutmut_16(self) -> dict[str, set[int]]:
        """Added lines from the merge-base through the current checkout.

        A remote-tracking base is refreshed first. Refresh failure warns and
        continues with the cached ref. Returns ``{}`` (→ a soft PASS) when the
        base ref is unsafe/unresolvable, the merge-base can't be computed, or
        the diff command fails — none of which is a coverage defect.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return {}
        self._refresh_remote_base()
        merge_base = self.git_runner(["merge-base", self.base_ref, "HEAD"], self._repo_root)
        if merge_base.returncode != 0:
            return {}
        base = _decode_git_output(merge_base.stdout).strip()
        if base:
            return {}
        # Comparing the base tree to the checkout includes committed, staged,
        # and unstaged changes. ``base...HEAD`` omits the latter two and made a
        # pre-commit local gate pass code that CI rejected after it was committed.
        diff = self.git_runner(["diff", "-U0", base, "--"], self._repo_root)
        if diff.returncode != 0:
            return {}
        changed = parse_added_lines(_decode_git_output(diff.stdout))
        changed.update(self._untracked_added_lines())
        return changed

    def xǁNewCodeCoverageǁ_changed_lines__mutmut_17(self) -> dict[str, set[int]]:
        """Added lines from the merge-base through the current checkout.

        A remote-tracking base is refreshed first. Refresh failure warns and
        continues with the cached ref. Returns ``{}`` (→ a soft PASS) when the
        base ref is unsafe/unresolvable, the merge-base can't be computed, or
        the diff command fails — none of which is a coverage defect.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return {}
        self._refresh_remote_base()
        merge_base = self.git_runner(["merge-base", self.base_ref, "HEAD"], self._repo_root)
        if merge_base.returncode != 0:
            return {}
        base = _decode_git_output(merge_base.stdout).strip()
        if not base:
            return {}
        # Comparing the base tree to the checkout includes committed, staged,
        # and unstaged changes. ``base...HEAD`` omits the latter two and made a
        # pre-commit local gate pass code that CI rejected after it was committed.
        diff = None
        if diff.returncode != 0:
            return {}
        changed = parse_added_lines(_decode_git_output(diff.stdout))
        changed.update(self._untracked_added_lines())
        return changed

    def xǁNewCodeCoverageǁ_changed_lines__mutmut_18(self) -> dict[str, set[int]]:
        """Added lines from the merge-base through the current checkout.

        A remote-tracking base is refreshed first. Refresh failure warns and
        continues with the cached ref. Returns ``{}`` (→ a soft PASS) when the
        base ref is unsafe/unresolvable, the merge-base can't be computed, or
        the diff command fails — none of which is a coverage defect.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return {}
        self._refresh_remote_base()
        merge_base = self.git_runner(["merge-base", self.base_ref, "HEAD"], self._repo_root)
        if merge_base.returncode != 0:
            return {}
        base = _decode_git_output(merge_base.stdout).strip()
        if not base:
            return {}
        # Comparing the base tree to the checkout includes committed, staged,
        # and unstaged changes. ``base...HEAD`` omits the latter two and made a
        # pre-commit local gate pass code that CI rejected after it was committed.
        diff = self.git_runner(None, self._repo_root)
        if diff.returncode != 0:
            return {}
        changed = parse_added_lines(_decode_git_output(diff.stdout))
        changed.update(self._untracked_added_lines())
        return changed

    def xǁNewCodeCoverageǁ_changed_lines__mutmut_19(self) -> dict[str, set[int]]:
        """Added lines from the merge-base through the current checkout.

        A remote-tracking base is refreshed first. Refresh failure warns and
        continues with the cached ref. Returns ``{}`` (→ a soft PASS) when the
        base ref is unsafe/unresolvable, the merge-base can't be computed, or
        the diff command fails — none of which is a coverage defect.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return {}
        self._refresh_remote_base()
        merge_base = self.git_runner(["merge-base", self.base_ref, "HEAD"], self._repo_root)
        if merge_base.returncode != 0:
            return {}
        base = _decode_git_output(merge_base.stdout).strip()
        if not base:
            return {}
        # Comparing the base tree to the checkout includes committed, staged,
        # and unstaged changes. ``base...HEAD`` omits the latter two and made a
        # pre-commit local gate pass code that CI rejected after it was committed.
        diff = self.git_runner(["diff", "-U0", base, "--"], None)
        if diff.returncode != 0:
            return {}
        changed = parse_added_lines(_decode_git_output(diff.stdout))
        changed.update(self._untracked_added_lines())
        return changed

    def xǁNewCodeCoverageǁ_changed_lines__mutmut_20(self) -> dict[str, set[int]]:
        """Added lines from the merge-base through the current checkout.

        A remote-tracking base is refreshed first. Refresh failure warns and
        continues with the cached ref. Returns ``{}`` (→ a soft PASS) when the
        base ref is unsafe/unresolvable, the merge-base can't be computed, or
        the diff command fails — none of which is a coverage defect.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return {}
        self._refresh_remote_base()
        merge_base = self.git_runner(["merge-base", self.base_ref, "HEAD"], self._repo_root)
        if merge_base.returncode != 0:
            return {}
        base = _decode_git_output(merge_base.stdout).strip()
        if not base:
            return {}
        # Comparing the base tree to the checkout includes committed, staged,
        # and unstaged changes. ``base...HEAD`` omits the latter two and made a
        # pre-commit local gate pass code that CI rejected after it was committed.
        diff = self.git_runner(self._repo_root)
        if diff.returncode != 0:
            return {}
        changed = parse_added_lines(_decode_git_output(diff.stdout))
        changed.update(self._untracked_added_lines())
        return changed

    def xǁNewCodeCoverageǁ_changed_lines__mutmut_21(self) -> dict[str, set[int]]:
        """Added lines from the merge-base through the current checkout.

        A remote-tracking base is refreshed first. Refresh failure warns and
        continues with the cached ref. Returns ``{}`` (→ a soft PASS) when the
        base ref is unsafe/unresolvable, the merge-base can't be computed, or
        the diff command fails — none of which is a coverage defect.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return {}
        self._refresh_remote_base()
        merge_base = self.git_runner(["merge-base", self.base_ref, "HEAD"], self._repo_root)
        if merge_base.returncode != 0:
            return {}
        base = _decode_git_output(merge_base.stdout).strip()
        if not base:
            return {}
        # Comparing the base tree to the checkout includes committed, staged,
        # and unstaged changes. ``base...HEAD`` omits the latter two and made a
        # pre-commit local gate pass code that CI rejected after it was committed.
        diff = self.git_runner(["diff", "-U0", base, "--"], )
        if diff.returncode != 0:
            return {}
        changed = parse_added_lines(_decode_git_output(diff.stdout))
        changed.update(self._untracked_added_lines())
        return changed

    def xǁNewCodeCoverageǁ_changed_lines__mutmut_22(self) -> dict[str, set[int]]:
        """Added lines from the merge-base through the current checkout.

        A remote-tracking base is refreshed first. Refresh failure warns and
        continues with the cached ref. Returns ``{}`` (→ a soft PASS) when the
        base ref is unsafe/unresolvable, the merge-base can't be computed, or
        the diff command fails — none of which is a coverage defect.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return {}
        self._refresh_remote_base()
        merge_base = self.git_runner(["merge-base", self.base_ref, "HEAD"], self._repo_root)
        if merge_base.returncode != 0:
            return {}
        base = _decode_git_output(merge_base.stdout).strip()
        if not base:
            return {}
        # Comparing the base tree to the checkout includes committed, staged,
        # and unstaged changes. ``base...HEAD`` omits the latter two and made a
        # pre-commit local gate pass code that CI rejected after it was committed.
        diff = self.git_runner(["XXdiffXX", "-U0", base, "--"], self._repo_root)
        if diff.returncode != 0:
            return {}
        changed = parse_added_lines(_decode_git_output(diff.stdout))
        changed.update(self._untracked_added_lines())
        return changed

    def xǁNewCodeCoverageǁ_changed_lines__mutmut_23(self) -> dict[str, set[int]]:
        """Added lines from the merge-base through the current checkout.

        A remote-tracking base is refreshed first. Refresh failure warns and
        continues with the cached ref. Returns ``{}`` (→ a soft PASS) when the
        base ref is unsafe/unresolvable, the merge-base can't be computed, or
        the diff command fails — none of which is a coverage defect.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return {}
        self._refresh_remote_base()
        merge_base = self.git_runner(["merge-base", self.base_ref, "HEAD"], self._repo_root)
        if merge_base.returncode != 0:
            return {}
        base = _decode_git_output(merge_base.stdout).strip()
        if not base:
            return {}
        # Comparing the base tree to the checkout includes committed, staged,
        # and unstaged changes. ``base...HEAD`` omits the latter two and made a
        # pre-commit local gate pass code that CI rejected after it was committed.
        diff = self.git_runner(["DIFF", "-U0", base, "--"], self._repo_root)
        if diff.returncode != 0:
            return {}
        changed = parse_added_lines(_decode_git_output(diff.stdout))
        changed.update(self._untracked_added_lines())
        return changed

    def xǁNewCodeCoverageǁ_changed_lines__mutmut_24(self) -> dict[str, set[int]]:
        """Added lines from the merge-base through the current checkout.

        A remote-tracking base is refreshed first. Refresh failure warns and
        continues with the cached ref. Returns ``{}`` (→ a soft PASS) when the
        base ref is unsafe/unresolvable, the merge-base can't be computed, or
        the diff command fails — none of which is a coverage defect.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return {}
        self._refresh_remote_base()
        merge_base = self.git_runner(["merge-base", self.base_ref, "HEAD"], self._repo_root)
        if merge_base.returncode != 0:
            return {}
        base = _decode_git_output(merge_base.stdout).strip()
        if not base:
            return {}
        # Comparing the base tree to the checkout includes committed, staged,
        # and unstaged changes. ``base...HEAD`` omits the latter two and made a
        # pre-commit local gate pass code that CI rejected after it was committed.
        diff = self.git_runner(["diff", "XX-U0XX", base, "--"], self._repo_root)
        if diff.returncode != 0:
            return {}
        changed = parse_added_lines(_decode_git_output(diff.stdout))
        changed.update(self._untracked_added_lines())
        return changed

    def xǁNewCodeCoverageǁ_changed_lines__mutmut_25(self) -> dict[str, set[int]]:
        """Added lines from the merge-base through the current checkout.

        A remote-tracking base is refreshed first. Refresh failure warns and
        continues with the cached ref. Returns ``{}`` (→ a soft PASS) when the
        base ref is unsafe/unresolvable, the merge-base can't be computed, or
        the diff command fails — none of which is a coverage defect.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return {}
        self._refresh_remote_base()
        merge_base = self.git_runner(["merge-base", self.base_ref, "HEAD"], self._repo_root)
        if merge_base.returncode != 0:
            return {}
        base = _decode_git_output(merge_base.stdout).strip()
        if not base:
            return {}
        # Comparing the base tree to the checkout includes committed, staged,
        # and unstaged changes. ``base...HEAD`` omits the latter two and made a
        # pre-commit local gate pass code that CI rejected after it was committed.
        diff = self.git_runner(["diff", "-u0", base, "--"], self._repo_root)
        if diff.returncode != 0:
            return {}
        changed = parse_added_lines(_decode_git_output(diff.stdout))
        changed.update(self._untracked_added_lines())
        return changed

    def xǁNewCodeCoverageǁ_changed_lines__mutmut_26(self) -> dict[str, set[int]]:
        """Added lines from the merge-base through the current checkout.

        A remote-tracking base is refreshed first. Refresh failure warns and
        continues with the cached ref. Returns ``{}`` (→ a soft PASS) when the
        base ref is unsafe/unresolvable, the merge-base can't be computed, or
        the diff command fails — none of which is a coverage defect.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return {}
        self._refresh_remote_base()
        merge_base = self.git_runner(["merge-base", self.base_ref, "HEAD"], self._repo_root)
        if merge_base.returncode != 0:
            return {}
        base = _decode_git_output(merge_base.stdout).strip()
        if not base:
            return {}
        # Comparing the base tree to the checkout includes committed, staged,
        # and unstaged changes. ``base...HEAD`` omits the latter two and made a
        # pre-commit local gate pass code that CI rejected after it was committed.
        diff = self.git_runner(["diff", "-U0", base, "XX--XX"], self._repo_root)
        if diff.returncode != 0:
            return {}
        changed = parse_added_lines(_decode_git_output(diff.stdout))
        changed.update(self._untracked_added_lines())
        return changed

    def xǁNewCodeCoverageǁ_changed_lines__mutmut_27(self) -> dict[str, set[int]]:
        """Added lines from the merge-base through the current checkout.

        A remote-tracking base is refreshed first. Refresh failure warns and
        continues with the cached ref. Returns ``{}`` (→ a soft PASS) when the
        base ref is unsafe/unresolvable, the merge-base can't be computed, or
        the diff command fails — none of which is a coverage defect.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return {}
        self._refresh_remote_base()
        merge_base = self.git_runner(["merge-base", self.base_ref, "HEAD"], self._repo_root)
        if merge_base.returncode != 0:
            return {}
        base = _decode_git_output(merge_base.stdout).strip()
        if not base:
            return {}
        # Comparing the base tree to the checkout includes committed, staged,
        # and unstaged changes. ``base...HEAD`` omits the latter two and made a
        # pre-commit local gate pass code that CI rejected after it was committed.
        diff = self.git_runner(["diff", "-U0", base, "--"], self._repo_root)
        if diff.returncode == 0:
            return {}
        changed = parse_added_lines(_decode_git_output(diff.stdout))
        changed.update(self._untracked_added_lines())
        return changed

    def xǁNewCodeCoverageǁ_changed_lines__mutmut_28(self) -> dict[str, set[int]]:
        """Added lines from the merge-base through the current checkout.

        A remote-tracking base is refreshed first. Refresh failure warns and
        continues with the cached ref. Returns ``{}`` (→ a soft PASS) when the
        base ref is unsafe/unresolvable, the merge-base can't be computed, or
        the diff command fails — none of which is a coverage defect.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return {}
        self._refresh_remote_base()
        merge_base = self.git_runner(["merge-base", self.base_ref, "HEAD"], self._repo_root)
        if merge_base.returncode != 0:
            return {}
        base = _decode_git_output(merge_base.stdout).strip()
        if not base:
            return {}
        # Comparing the base tree to the checkout includes committed, staged,
        # and unstaged changes. ``base...HEAD`` omits the latter two and made a
        # pre-commit local gate pass code that CI rejected after it was committed.
        diff = self.git_runner(["diff", "-U0", base, "--"], self._repo_root)
        if diff.returncode != 1:
            return {}
        changed = parse_added_lines(_decode_git_output(diff.stdout))
        changed.update(self._untracked_added_lines())
        return changed

    def xǁNewCodeCoverageǁ_changed_lines__mutmut_29(self) -> dict[str, set[int]]:
        """Added lines from the merge-base through the current checkout.

        A remote-tracking base is refreshed first. Refresh failure warns and
        continues with the cached ref. Returns ``{}`` (→ a soft PASS) when the
        base ref is unsafe/unresolvable, the merge-base can't be computed, or
        the diff command fails — none of which is a coverage defect.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return {}
        self._refresh_remote_base()
        merge_base = self.git_runner(["merge-base", self.base_ref, "HEAD"], self._repo_root)
        if merge_base.returncode != 0:
            return {}
        base = _decode_git_output(merge_base.stdout).strip()
        if not base:
            return {}
        # Comparing the base tree to the checkout includes committed, staged,
        # and unstaged changes. ``base...HEAD`` omits the latter two and made a
        # pre-commit local gate pass code that CI rejected after it was committed.
        diff = self.git_runner(["diff", "-U0", base, "--"], self._repo_root)
        if diff.returncode != 0:
            return {}
        changed = None
        changed.update(self._untracked_added_lines())
        return changed

    def xǁNewCodeCoverageǁ_changed_lines__mutmut_30(self) -> dict[str, set[int]]:
        """Added lines from the merge-base through the current checkout.

        A remote-tracking base is refreshed first. Refresh failure warns and
        continues with the cached ref. Returns ``{}`` (→ a soft PASS) when the
        base ref is unsafe/unresolvable, the merge-base can't be computed, or
        the diff command fails — none of which is a coverage defect.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return {}
        self._refresh_remote_base()
        merge_base = self.git_runner(["merge-base", self.base_ref, "HEAD"], self._repo_root)
        if merge_base.returncode != 0:
            return {}
        base = _decode_git_output(merge_base.stdout).strip()
        if not base:
            return {}
        # Comparing the base tree to the checkout includes committed, staged,
        # and unstaged changes. ``base...HEAD`` omits the latter two and made a
        # pre-commit local gate pass code that CI rejected after it was committed.
        diff = self.git_runner(["diff", "-U0", base, "--"], self._repo_root)
        if diff.returncode != 0:
            return {}
        changed = parse_added_lines(None)
        changed.update(self._untracked_added_lines())
        return changed

    def xǁNewCodeCoverageǁ_changed_lines__mutmut_31(self) -> dict[str, set[int]]:
        """Added lines from the merge-base through the current checkout.

        A remote-tracking base is refreshed first. Refresh failure warns and
        continues with the cached ref. Returns ``{}`` (→ a soft PASS) when the
        base ref is unsafe/unresolvable, the merge-base can't be computed, or
        the diff command fails — none of which is a coverage defect.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return {}
        self._refresh_remote_base()
        merge_base = self.git_runner(["merge-base", self.base_ref, "HEAD"], self._repo_root)
        if merge_base.returncode != 0:
            return {}
        base = _decode_git_output(merge_base.stdout).strip()
        if not base:
            return {}
        # Comparing the base tree to the checkout includes committed, staged,
        # and unstaged changes. ``base...HEAD`` omits the latter two and made a
        # pre-commit local gate pass code that CI rejected after it was committed.
        diff = self.git_runner(["diff", "-U0", base, "--"], self._repo_root)
        if diff.returncode != 0:
            return {}
        changed = parse_added_lines(_decode_git_output(None))
        changed.update(self._untracked_added_lines())
        return changed

    def xǁNewCodeCoverageǁ_changed_lines__mutmut_32(self) -> dict[str, set[int]]:
        """Added lines from the merge-base through the current checkout.

        A remote-tracking base is refreshed first. Refresh failure warns and
        continues with the cached ref. Returns ``{}`` (→ a soft PASS) when the
        base ref is unsafe/unresolvable, the merge-base can't be computed, or
        the diff command fails — none of which is a coverage defect.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return {}
        self._refresh_remote_base()
        merge_base = self.git_runner(["merge-base", self.base_ref, "HEAD"], self._repo_root)
        if merge_base.returncode != 0:
            return {}
        base = _decode_git_output(merge_base.stdout).strip()
        if not base:
            return {}
        # Comparing the base tree to the checkout includes committed, staged,
        # and unstaged changes. ``base...HEAD`` omits the latter two and made a
        # pre-commit local gate pass code that CI rejected after it was committed.
        diff = self.git_runner(["diff", "-U0", base, "--"], self._repo_root)
        if diff.returncode != 0:
            return {}
        changed = parse_added_lines(_decode_git_output(diff.stdout))
        changed.update(None)
        return changed

    @_mutmut_mutated(mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut)
    def _untracked_added_lines(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_orig(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_1(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = None
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_2(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            None,
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_3(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "-z", "--"],
            None,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_4(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_5(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "-z", "--"],
            )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_6(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["XXls-filesXX", "--others", "--exclude-standard", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_7(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["LS-FILES", "--others", "--exclude-standard", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_8(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "XX--othersXX", "--exclude-standard", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_9(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--OTHERS", "--exclude-standard", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_10(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "XX--exclude-standardXX", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_11(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--EXCLUDE-STANDARD", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_12(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "XX-zXX", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_13(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "-Z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_14(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "-z", "XX--XX"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_15(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "-z", "--"],
            self._repo_root,
        )
        if result.returncode == 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_16(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 1:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_17(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = None
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_18(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split(None):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_19(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(None).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_20(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("XX\0XX"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_21(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() and ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_22(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel and Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_23(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_24(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(None).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_25(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or "XX..XX" in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_26(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." not in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_27(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(None).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_28(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                break
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_29(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_30(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(None):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_31(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                break
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_32(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = None
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_33(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root * rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_34(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_35(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(None):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_36(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    break
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_37(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = None
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_38(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                break
            added[rel] = set(range(1, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_39(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = None
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_40(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(None)
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_41(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(None, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_42(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, None))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_43(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_44(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, ))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_45(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(2, line_count + 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_46(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count - 1))
        return added

    def xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_47(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 2))
        return added

    @cached_property
    def _measured(self) -> dict[str, tuple[int, int]]:
        """``{repo_relative_path: (covered_changed, coverable_changed)}``.

        Only files with at least one *coverable* changed line (a changed line the
        report recorded) appear — a file with no measurable new code is omitted,
        so it is neither enumerated nor a violation. Cached: the git subprocess
        and the XML parse run once per rule instance.
        """
        changed = self._changed_lines()
        if not changed:
            return {}
        coverage = parse_line_coverage(self._report_path())
        if not coverage:
            return {}
        out: dict[str, tuple[int, int]] = {}
        for rel, lines in changed.items():
            line_hits = coverage.get(rel)
            if not line_hits:
                continue
            coverable = [ln for ln in lines if ln in line_hits]
            if not coverable:
                continue
            covered = sum(1 for ln in coverable if line_hits[ln] > 0)
            out[rel] = (covered, len(coverable))
        return out

    @_mutmut_mutated(mutants_xǁNewCodeCoverageǁenumerate_files__mutmut)
    def enumerate_files(self) -> list[Path]:
        """The changed in-scope files with measurable new code, as repo-anchored paths.

        Overrides the default rglob walk: the rule's universe is the changed
        lines that landed in the coverage report, not the on-disk tree. The
        inherited scope predicate (extensions + roots) still applies via
        :meth:`FitnessRule.collect_violations`.
        """
        return [self._repo_root / rel for rel in self._measured]

    def xǁNewCodeCoverageǁenumerate_files__mutmut_orig(self) -> list[Path]:
        """The changed in-scope files with measurable new code, as repo-anchored paths.

        Overrides the default rglob walk: the rule's universe is the changed
        lines that landed in the coverage report, not the on-disk tree. The
        inherited scope predicate (extensions + roots) still applies via
        :meth:`FitnessRule.collect_violations`.
        """
        return [self._repo_root / rel for rel in self._measured]

    def xǁNewCodeCoverageǁenumerate_files__mutmut_1(self) -> list[Path]:
        """The changed in-scope files with measurable new code, as repo-anchored paths.

        Overrides the default rglob walk: the rule's universe is the changed
        lines that landed in the coverage report, not the on-disk tree. The
        inherited scope predicate (extensions + roots) still applies via
        :meth:`FitnessRule.collect_violations`.
        """
        return [self._repo_root * rel for rel in self._measured]

    @_mutmut_mutated(mutants_xǁNewCodeCoverageǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        """True iff the file's covered/coverable changed-line ratio is below the floor."""
        rel = str(self._repo_relative(path))
        measured = self._measured.get(rel)
        if measured is None:
            return False
        covered, coverable = measured
        return covered / coverable * 100.0 < self.floor_pct

    def xǁNewCodeCoverageǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        """True iff the file's covered/coverable changed-line ratio is below the floor."""
        rel = str(self._repo_relative(path))
        measured = self._measured.get(rel)
        if measured is None:
            return False
        covered, coverable = measured
        return covered / coverable * 100.0 < self.floor_pct

    def xǁNewCodeCoverageǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        """True iff the file's covered/coverable changed-line ratio is below the floor."""
        rel = None
        measured = self._measured.get(rel)
        if measured is None:
            return False
        covered, coverable = measured
        return covered / coverable * 100.0 < self.floor_pct

    def xǁNewCodeCoverageǁfile_has_violation__mutmut_2(self, path: Path) -> bool:
        """True iff the file's covered/coverable changed-line ratio is below the floor."""
        rel = str(None)
        measured = self._measured.get(rel)
        if measured is None:
            return False
        covered, coverable = measured
        return covered / coverable * 100.0 < self.floor_pct

    def xǁNewCodeCoverageǁfile_has_violation__mutmut_3(self, path: Path) -> bool:
        """True iff the file's covered/coverable changed-line ratio is below the floor."""
        rel = str(self._repo_relative(None))
        measured = self._measured.get(rel)
        if measured is None:
            return False
        covered, coverable = measured
        return covered / coverable * 100.0 < self.floor_pct

    def xǁNewCodeCoverageǁfile_has_violation__mutmut_4(self, path: Path) -> bool:
        """True iff the file's covered/coverable changed-line ratio is below the floor."""
        rel = str(self._repo_relative(path))
        measured = None
        if measured is None:
            return False
        covered, coverable = measured
        return covered / coverable * 100.0 < self.floor_pct

    def xǁNewCodeCoverageǁfile_has_violation__mutmut_5(self, path: Path) -> bool:
        """True iff the file's covered/coverable changed-line ratio is below the floor."""
        rel = str(self._repo_relative(path))
        measured = self._measured.get(None)
        if measured is None:
            return False
        covered, coverable = measured
        return covered / coverable * 100.0 < self.floor_pct

    def xǁNewCodeCoverageǁfile_has_violation__mutmut_6(self, path: Path) -> bool:
        """True iff the file's covered/coverable changed-line ratio is below the floor."""
        rel = str(self._repo_relative(path))
        measured = self._measured.get(rel)
        if measured is not None:
            return False
        covered, coverable = measured
        return covered / coverable * 100.0 < self.floor_pct

    def xǁNewCodeCoverageǁfile_has_violation__mutmut_7(self, path: Path) -> bool:
        """True iff the file's covered/coverable changed-line ratio is below the floor."""
        rel = str(self._repo_relative(path))
        measured = self._measured.get(rel)
        if measured is None:
            return True
        covered, coverable = measured
        return covered / coverable * 100.0 < self.floor_pct

    def xǁNewCodeCoverageǁfile_has_violation__mutmut_8(self, path: Path) -> bool:
        """True iff the file's covered/coverable changed-line ratio is below the floor."""
        rel = str(self._repo_relative(path))
        measured = self._measured.get(rel)
        if measured is None:
            return False
        covered, coverable = None
        return covered / coverable * 100.0 < self.floor_pct

    def xǁNewCodeCoverageǁfile_has_violation__mutmut_9(self, path: Path) -> bool:
        """True iff the file's covered/coverable changed-line ratio is below the floor."""
        rel = str(self._repo_relative(path))
        measured = self._measured.get(rel)
        if measured is None:
            return False
        covered, coverable = measured
        return covered / coverable / 100.0 < self.floor_pct

    def xǁNewCodeCoverageǁfile_has_violation__mutmut_10(self, path: Path) -> bool:
        """True iff the file's covered/coverable changed-line ratio is below the floor."""
        rel = str(self._repo_relative(path))
        measured = self._measured.get(rel)
        if measured is None:
            return False
        covered, coverable = measured
        return covered * coverable * 100.0 < self.floor_pct

    def xǁNewCodeCoverageǁfile_has_violation__mutmut_11(self, path: Path) -> bool:
        """True iff the file's covered/coverable changed-line ratio is below the floor."""
        rel = str(self._repo_relative(path))
        measured = self._measured.get(rel)
        if measured is None:
            return False
        covered, coverable = measured
        return covered / coverable * 101.0 < self.floor_pct

    def xǁNewCodeCoverageǁfile_has_violation__mutmut_12(self, path: Path) -> bool:
        """True iff the file's covered/coverable changed-line ratio is below the floor."""
        rel = str(self._repo_relative(path))
        measured = self._measured.get(rel)
        if measured is None:
            return False
        covered, coverable = measured
        return covered / coverable * 100.0 <= self.floor_pct

    @_mutmut_mutated(mutants_xǁNewCodeCoverageǁrun__mutmut)
    def run(self) -> int:
        """Hard-floor gate: every below-floor changed file fails.

        The "new" line set is recomputed against the merge-base on every branch,
        and an uncovered line added on this branch is a current defect. This
        method gates the raw violation set with a hard floor, mirroring
        SonarCloud's "Coverage on New Code"
        merge condition. Returns ``0`` when the changed lines clear the floor (or
        there is no measurable new code), ``1`` otherwise.
        """
        if self.exact_config is not None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = changed_line_failures(self._repo_root, self.exact_config)
            for relative, message in failures.items():
                report_finding(self.name, relative, message)
                print(f"FAIL [{self.name}] {relative}: {message}")
            return int(bool(failures))
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — new code clears the {self.floor_pct:g}% coverage floor.")
            return 0
        print(f"FAIL [arch:{self._name}] — new code below the {self.floor_pct:g}% coverage floor:")
        finding = f"new code below the {self.floor_pct:g}% coverage floor"
        for path in violations:
            report_finding(self.name, self._repo_relative(path).as_posix(), finding)
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁNewCodeCoverageǁrun__mutmut_orig(self) -> int:
        """Hard-floor gate: every below-floor changed file fails.

        The "new" line set is recomputed against the merge-base on every branch,
        and an uncovered line added on this branch is a current defect. This
        method gates the raw violation set with a hard floor, mirroring
        SonarCloud's "Coverage on New Code"
        merge condition. Returns ``0`` when the changed lines clear the floor (or
        there is no measurable new code), ``1`` otherwise.
        """
        if self.exact_config is not None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = changed_line_failures(self._repo_root, self.exact_config)
            for relative, message in failures.items():
                report_finding(self.name, relative, message)
                print(f"FAIL [{self.name}] {relative}: {message}")
            return int(bool(failures))
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — new code clears the {self.floor_pct:g}% coverage floor.")
            return 0
        print(f"FAIL [arch:{self._name}] — new code below the {self.floor_pct:g}% coverage floor:")
        finding = f"new code below the {self.floor_pct:g}% coverage floor"
        for path in violations:
            report_finding(self.name, self._repo_relative(path).as_posix(), finding)
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁNewCodeCoverageǁrun__mutmut_1(self) -> int:
        """Hard-floor gate: every below-floor changed file fails.

        The "new" line set is recomputed against the merge-base on every branch,
        and an uncovered line added on this branch is a current defect. This
        method gates the raw violation set with a hard floor, mirroring
        SonarCloud's "Coverage on New Code"
        merge condition. Returns ``0`` when the changed lines clear the floor (or
        there is no measurable new code), ``1`` otherwise.
        """
        if self.exact_config is None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = changed_line_failures(self._repo_root, self.exact_config)
            for relative, message in failures.items():
                report_finding(self.name, relative, message)
                print(f"FAIL [{self.name}] {relative}: {message}")
            return int(bool(failures))
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — new code clears the {self.floor_pct:g}% coverage floor.")
            return 0
        print(f"FAIL [arch:{self._name}] — new code below the {self.floor_pct:g}% coverage floor:")
        finding = f"new code below the {self.floor_pct:g}% coverage floor"
        for path in violations:
            report_finding(self.name, self._repo_relative(path).as_posix(), finding)
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁNewCodeCoverageǁrun__mutmut_2(self) -> int:
        """Hard-floor gate: every below-floor changed file fails.

        The "new" line set is recomputed against the merge-base on every branch,
        and an uncovered line added on this branch is a current defect. This
        method gates the raw violation set with a hard floor, mirroring
        SonarCloud's "Coverage on New Code"
        merge condition. Returns ``0`` when the changed lines clear the floor (or
        there is no measurable new code), ``1`` otherwise.
        """
        if self.exact_config is not None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = None
            for relative, message in failures.items():
                report_finding(self.name, relative, message)
                print(f"FAIL [{self.name}] {relative}: {message}")
            return int(bool(failures))
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — new code clears the {self.floor_pct:g}% coverage floor.")
            return 0
        print(f"FAIL [arch:{self._name}] — new code below the {self.floor_pct:g}% coverage floor:")
        finding = f"new code below the {self.floor_pct:g}% coverage floor"
        for path in violations:
            report_finding(self.name, self._repo_relative(path).as_posix(), finding)
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁNewCodeCoverageǁrun__mutmut_3(self) -> int:
        """Hard-floor gate: every below-floor changed file fails.

        The "new" line set is recomputed against the merge-base on every branch,
        and an uncovered line added on this branch is a current defect. This
        method gates the raw violation set with a hard floor, mirroring
        SonarCloud's "Coverage on New Code"
        merge condition. Returns ``0`` when the changed lines clear the floor (or
        there is no measurable new code), ``1`` otherwise.
        """
        if self.exact_config is not None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = changed_line_failures(None, self.exact_config)
            for relative, message in failures.items():
                report_finding(self.name, relative, message)
                print(f"FAIL [{self.name}] {relative}: {message}")
            return int(bool(failures))
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — new code clears the {self.floor_pct:g}% coverage floor.")
            return 0
        print(f"FAIL [arch:{self._name}] — new code below the {self.floor_pct:g}% coverage floor:")
        finding = f"new code below the {self.floor_pct:g}% coverage floor"
        for path in violations:
            report_finding(self.name, self._repo_relative(path).as_posix(), finding)
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁNewCodeCoverageǁrun__mutmut_4(self) -> int:
        """Hard-floor gate: every below-floor changed file fails.

        The "new" line set is recomputed against the merge-base on every branch,
        and an uncovered line added on this branch is a current defect. This
        method gates the raw violation set with a hard floor, mirroring
        SonarCloud's "Coverage on New Code"
        merge condition. Returns ``0`` when the changed lines clear the floor (or
        there is no measurable new code), ``1`` otherwise.
        """
        if self.exact_config is not None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = changed_line_failures(self._repo_root, None)
            for relative, message in failures.items():
                report_finding(self.name, relative, message)
                print(f"FAIL [{self.name}] {relative}: {message}")
            return int(bool(failures))
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — new code clears the {self.floor_pct:g}% coverage floor.")
            return 0
        print(f"FAIL [arch:{self._name}] — new code below the {self.floor_pct:g}% coverage floor:")
        finding = f"new code below the {self.floor_pct:g}% coverage floor"
        for path in violations:
            report_finding(self.name, self._repo_relative(path).as_posix(), finding)
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁNewCodeCoverageǁrun__mutmut_5(self) -> int:
        """Hard-floor gate: every below-floor changed file fails.

        The "new" line set is recomputed against the merge-base on every branch,
        and an uncovered line added on this branch is a current defect. This
        method gates the raw violation set with a hard floor, mirroring
        SonarCloud's "Coverage on New Code"
        merge condition. Returns ``0`` when the changed lines clear the floor (or
        there is no measurable new code), ``1`` otherwise.
        """
        if self.exact_config is not None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = changed_line_failures(self.exact_config)
            for relative, message in failures.items():
                report_finding(self.name, relative, message)
                print(f"FAIL [{self.name}] {relative}: {message}")
            return int(bool(failures))
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — new code clears the {self.floor_pct:g}% coverage floor.")
            return 0
        print(f"FAIL [arch:{self._name}] — new code below the {self.floor_pct:g}% coverage floor:")
        finding = f"new code below the {self.floor_pct:g}% coverage floor"
        for path in violations:
            report_finding(self.name, self._repo_relative(path).as_posix(), finding)
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁNewCodeCoverageǁrun__mutmut_6(self) -> int:
        """Hard-floor gate: every below-floor changed file fails.

        The "new" line set is recomputed against the merge-base on every branch,
        and an uncovered line added on this branch is a current defect. This
        method gates the raw violation set with a hard floor, mirroring
        SonarCloud's "Coverage on New Code"
        merge condition. Returns ``0`` when the changed lines clear the floor (or
        there is no measurable new code), ``1`` otherwise.
        """
        if self.exact_config is not None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = changed_line_failures(self._repo_root, )
            for relative, message in failures.items():
                report_finding(self.name, relative, message)
                print(f"FAIL [{self.name}] {relative}: {message}")
            return int(bool(failures))
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — new code clears the {self.floor_pct:g}% coverage floor.")
            return 0
        print(f"FAIL [arch:{self._name}] — new code below the {self.floor_pct:g}% coverage floor:")
        finding = f"new code below the {self.floor_pct:g}% coverage floor"
        for path in violations:
            report_finding(self.name, self._repo_relative(path).as_posix(), finding)
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁNewCodeCoverageǁrun__mutmut_7(self) -> int:
        """Hard-floor gate: every below-floor changed file fails.

        The "new" line set is recomputed against the merge-base on every branch,
        and an uncovered line added on this branch is a current defect. This
        method gates the raw violation set with a hard floor, mirroring
        SonarCloud's "Coverage on New Code"
        merge condition. Returns ``0`` when the changed lines clear the floor (or
        there is no measurable new code), ``1`` otherwise.
        """
        if self.exact_config is not None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = changed_line_failures(self._repo_root, self.exact_config)
            for relative, message in failures.items():
                report_finding(None, relative, message)
                print(f"FAIL [{self.name}] {relative}: {message}")
            return int(bool(failures))
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — new code clears the {self.floor_pct:g}% coverage floor.")
            return 0
        print(f"FAIL [arch:{self._name}] — new code below the {self.floor_pct:g}% coverage floor:")
        finding = f"new code below the {self.floor_pct:g}% coverage floor"
        for path in violations:
            report_finding(self.name, self._repo_relative(path).as_posix(), finding)
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁNewCodeCoverageǁrun__mutmut_8(self) -> int:
        """Hard-floor gate: every below-floor changed file fails.

        The "new" line set is recomputed against the merge-base on every branch,
        and an uncovered line added on this branch is a current defect. This
        method gates the raw violation set with a hard floor, mirroring
        SonarCloud's "Coverage on New Code"
        merge condition. Returns ``0`` when the changed lines clear the floor (or
        there is no measurable new code), ``1`` otherwise.
        """
        if self.exact_config is not None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = changed_line_failures(self._repo_root, self.exact_config)
            for relative, message in failures.items():
                report_finding(self.name, None, message)
                print(f"FAIL [{self.name}] {relative}: {message}")
            return int(bool(failures))
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — new code clears the {self.floor_pct:g}% coverage floor.")
            return 0
        print(f"FAIL [arch:{self._name}] — new code below the {self.floor_pct:g}% coverage floor:")
        finding = f"new code below the {self.floor_pct:g}% coverage floor"
        for path in violations:
            report_finding(self.name, self._repo_relative(path).as_posix(), finding)
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁNewCodeCoverageǁrun__mutmut_9(self) -> int:
        """Hard-floor gate: every below-floor changed file fails.

        The "new" line set is recomputed against the merge-base on every branch,
        and an uncovered line added on this branch is a current defect. This
        method gates the raw violation set with a hard floor, mirroring
        SonarCloud's "Coverage on New Code"
        merge condition. Returns ``0`` when the changed lines clear the floor (or
        there is no measurable new code), ``1`` otherwise.
        """
        if self.exact_config is not None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = changed_line_failures(self._repo_root, self.exact_config)
            for relative, message in failures.items():
                report_finding(self.name, relative, None)
                print(f"FAIL [{self.name}] {relative}: {message}")
            return int(bool(failures))
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — new code clears the {self.floor_pct:g}% coverage floor.")
            return 0
        print(f"FAIL [arch:{self._name}] — new code below the {self.floor_pct:g}% coverage floor:")
        finding = f"new code below the {self.floor_pct:g}% coverage floor"
        for path in violations:
            report_finding(self.name, self._repo_relative(path).as_posix(), finding)
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁNewCodeCoverageǁrun__mutmut_10(self) -> int:
        """Hard-floor gate: every below-floor changed file fails.

        The "new" line set is recomputed against the merge-base on every branch,
        and an uncovered line added on this branch is a current defect. This
        method gates the raw violation set with a hard floor, mirroring
        SonarCloud's "Coverage on New Code"
        merge condition. Returns ``0`` when the changed lines clear the floor (or
        there is no measurable new code), ``1`` otherwise.
        """
        if self.exact_config is not None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = changed_line_failures(self._repo_root, self.exact_config)
            for relative, message in failures.items():
                report_finding(relative, message)
                print(f"FAIL [{self.name}] {relative}: {message}")
            return int(bool(failures))
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — new code clears the {self.floor_pct:g}% coverage floor.")
            return 0
        print(f"FAIL [arch:{self._name}] — new code below the {self.floor_pct:g}% coverage floor:")
        finding = f"new code below the {self.floor_pct:g}% coverage floor"
        for path in violations:
            report_finding(self.name, self._repo_relative(path).as_posix(), finding)
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁNewCodeCoverageǁrun__mutmut_11(self) -> int:
        """Hard-floor gate: every below-floor changed file fails.

        The "new" line set is recomputed against the merge-base on every branch,
        and an uncovered line added on this branch is a current defect. This
        method gates the raw violation set with a hard floor, mirroring
        SonarCloud's "Coverage on New Code"
        merge condition. Returns ``0`` when the changed lines clear the floor (or
        there is no measurable new code), ``1`` otherwise.
        """
        if self.exact_config is not None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = changed_line_failures(self._repo_root, self.exact_config)
            for relative, message in failures.items():
                report_finding(self.name, message)
                print(f"FAIL [{self.name}] {relative}: {message}")
            return int(bool(failures))
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — new code clears the {self.floor_pct:g}% coverage floor.")
            return 0
        print(f"FAIL [arch:{self._name}] — new code below the {self.floor_pct:g}% coverage floor:")
        finding = f"new code below the {self.floor_pct:g}% coverage floor"
        for path in violations:
            report_finding(self.name, self._repo_relative(path).as_posix(), finding)
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁNewCodeCoverageǁrun__mutmut_12(self) -> int:
        """Hard-floor gate: every below-floor changed file fails.

        The "new" line set is recomputed against the merge-base on every branch,
        and an uncovered line added on this branch is a current defect. This
        method gates the raw violation set with a hard floor, mirroring
        SonarCloud's "Coverage on New Code"
        merge condition. Returns ``0`` when the changed lines clear the floor (or
        there is no measurable new code), ``1`` otherwise.
        """
        if self.exact_config is not None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = changed_line_failures(self._repo_root, self.exact_config)
            for relative, message in failures.items():
                report_finding(self.name, relative, )
                print(f"FAIL [{self.name}] {relative}: {message}")
            return int(bool(failures))
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — new code clears the {self.floor_pct:g}% coverage floor.")
            return 0
        print(f"FAIL [arch:{self._name}] — new code below the {self.floor_pct:g}% coverage floor:")
        finding = f"new code below the {self.floor_pct:g}% coverage floor"
        for path in violations:
            report_finding(self.name, self._repo_relative(path).as_posix(), finding)
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁNewCodeCoverageǁrun__mutmut_13(self) -> int:
        """Hard-floor gate: every below-floor changed file fails.

        The "new" line set is recomputed against the merge-base on every branch,
        and an uncovered line added on this branch is a current defect. This
        method gates the raw violation set with a hard floor, mirroring
        SonarCloud's "Coverage on New Code"
        merge condition. Returns ``0`` when the changed lines clear the floor (or
        there is no measurable new code), ``1`` otherwise.
        """
        if self.exact_config is not None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = changed_line_failures(self._repo_root, self.exact_config)
            for relative, message in failures.items():
                report_finding(self.name, relative, message)
                print(None)
            return int(bool(failures))
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — new code clears the {self.floor_pct:g}% coverage floor.")
            return 0
        print(f"FAIL [arch:{self._name}] — new code below the {self.floor_pct:g}% coverage floor:")
        finding = f"new code below the {self.floor_pct:g}% coverage floor"
        for path in violations:
            report_finding(self.name, self._repo_relative(path).as_posix(), finding)
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁNewCodeCoverageǁrun__mutmut_14(self) -> int:
        """Hard-floor gate: every below-floor changed file fails.

        The "new" line set is recomputed against the merge-base on every branch,
        and an uncovered line added on this branch is a current defect. This
        method gates the raw violation set with a hard floor, mirroring
        SonarCloud's "Coverage on New Code"
        merge condition. Returns ``0`` when the changed lines clear the floor (or
        there is no measurable new code), ``1`` otherwise.
        """
        if self.exact_config is not None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = changed_line_failures(self._repo_root, self.exact_config)
            for relative, message in failures.items():
                report_finding(self.name, relative, message)
                print(f"FAIL [{self.name}] {relative}: {message}")
            return int(None)
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — new code clears the {self.floor_pct:g}% coverage floor.")
            return 0
        print(f"FAIL [arch:{self._name}] — new code below the {self.floor_pct:g}% coverage floor:")
        finding = f"new code below the {self.floor_pct:g}% coverage floor"
        for path in violations:
            report_finding(self.name, self._repo_relative(path).as_posix(), finding)
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁNewCodeCoverageǁrun__mutmut_15(self) -> int:
        """Hard-floor gate: every below-floor changed file fails.

        The "new" line set is recomputed against the merge-base on every branch,
        and an uncovered line added on this branch is a current defect. This
        method gates the raw violation set with a hard floor, mirroring
        SonarCloud's "Coverage on New Code"
        merge condition. Returns ``0`` when the changed lines clear the floor (or
        there is no measurable new code), ``1`` otherwise.
        """
        if self.exact_config is not None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = changed_line_failures(self._repo_root, self.exact_config)
            for relative, message in failures.items():
                report_finding(self.name, relative, message)
                print(f"FAIL [{self.name}] {relative}: {message}")
            return int(bool(None))
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — new code clears the {self.floor_pct:g}% coverage floor.")
            return 0
        print(f"FAIL [arch:{self._name}] — new code below the {self.floor_pct:g}% coverage floor:")
        finding = f"new code below the {self.floor_pct:g}% coverage floor"
        for path in violations:
            report_finding(self.name, self._repo_relative(path).as_posix(), finding)
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁNewCodeCoverageǁrun__mutmut_16(self) -> int:
        """Hard-floor gate: every below-floor changed file fails.

        The "new" line set is recomputed against the merge-base on every branch,
        and an uncovered line added on this branch is a current defect. This
        method gates the raw violation set with a hard floor, mirroring
        SonarCloud's "Coverage on New Code"
        merge condition. Returns ``0`` when the changed lines clear the floor (or
        there is no measurable new code), ``1`` otherwise.
        """
        if self.exact_config is not None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = changed_line_failures(self._repo_root, self.exact_config)
            for relative, message in failures.items():
                report_finding(self.name, relative, message)
                print(f"FAIL [{self.name}] {relative}: {message}")
            return int(bool(failures))
        violations = None
        if not violations:
            print(f"ok [arch:{self._name}] — new code clears the {self.floor_pct:g}% coverage floor.")
            return 0
        print(f"FAIL [arch:{self._name}] — new code below the {self.floor_pct:g}% coverage floor:")
        finding = f"new code below the {self.floor_pct:g}% coverage floor"
        for path in violations:
            report_finding(self.name, self._repo_relative(path).as_posix(), finding)
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁNewCodeCoverageǁrun__mutmut_17(self) -> int:
        """Hard-floor gate: every below-floor changed file fails.

        The "new" line set is recomputed against the merge-base on every branch,
        and an uncovered line added on this branch is a current defect. This
        method gates the raw violation set with a hard floor, mirroring
        SonarCloud's "Coverage on New Code"
        merge condition. Returns ``0`` when the changed lines clear the floor (or
        there is no measurable new code), ``1`` otherwise.
        """
        if self.exact_config is not None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = changed_line_failures(self._repo_root, self.exact_config)
            for relative, message in failures.items():
                report_finding(self.name, relative, message)
                print(f"FAIL [{self.name}] {relative}: {message}")
            return int(bool(failures))
        violations = sorted(None, key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — new code clears the {self.floor_pct:g}% coverage floor.")
            return 0
        print(f"FAIL [arch:{self._name}] — new code below the {self.floor_pct:g}% coverage floor:")
        finding = f"new code below the {self.floor_pct:g}% coverage floor"
        for path in violations:
            report_finding(self.name, self._repo_relative(path).as_posix(), finding)
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁNewCodeCoverageǁrun__mutmut_18(self) -> int:
        """Hard-floor gate: every below-floor changed file fails.

        The "new" line set is recomputed against the merge-base on every branch,
        and an uncovered line added on this branch is a current defect. This
        method gates the raw violation set with a hard floor, mirroring
        SonarCloud's "Coverage on New Code"
        merge condition. Returns ``0`` when the changed lines clear the floor (or
        there is no measurable new code), ``1`` otherwise.
        """
        if self.exact_config is not None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = changed_line_failures(self._repo_root, self.exact_config)
            for relative, message in failures.items():
                report_finding(self.name, relative, message)
                print(f"FAIL [{self.name}] {relative}: {message}")
            return int(bool(failures))
        violations = sorted(self.collect_violations(), key=None)
        if not violations:
            print(f"ok [arch:{self._name}] — new code clears the {self.floor_pct:g}% coverage floor.")
            return 0
        print(f"FAIL [arch:{self._name}] — new code below the {self.floor_pct:g}% coverage floor:")
        finding = f"new code below the {self.floor_pct:g}% coverage floor"
        for path in violations:
            report_finding(self.name, self._repo_relative(path).as_posix(), finding)
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁNewCodeCoverageǁrun__mutmut_19(self) -> int:
        """Hard-floor gate: every below-floor changed file fails.

        The "new" line set is recomputed against the merge-base on every branch,
        and an uncovered line added on this branch is a current defect. This
        method gates the raw violation set with a hard floor, mirroring
        SonarCloud's "Coverage on New Code"
        merge condition. Returns ``0`` when the changed lines clear the floor (or
        there is no measurable new code), ``1`` otherwise.
        """
        if self.exact_config is not None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = changed_line_failures(self._repo_root, self.exact_config)
            for relative, message in failures.items():
                report_finding(self.name, relative, message)
                print(f"FAIL [{self.name}] {relative}: {message}")
            return int(bool(failures))
        violations = sorted(key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — new code clears the {self.floor_pct:g}% coverage floor.")
            return 0
        print(f"FAIL [arch:{self._name}] — new code below the {self.floor_pct:g}% coverage floor:")
        finding = f"new code below the {self.floor_pct:g}% coverage floor"
        for path in violations:
            report_finding(self.name, self._repo_relative(path).as_posix(), finding)
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁNewCodeCoverageǁrun__mutmut_20(self) -> int:
        """Hard-floor gate: every below-floor changed file fails.

        The "new" line set is recomputed against the merge-base on every branch,
        and an uncovered line added on this branch is a current defect. This
        method gates the raw violation set with a hard floor, mirroring
        SonarCloud's "Coverage on New Code"
        merge condition. Returns ``0`` when the changed lines clear the floor (or
        there is no measurable new code), ``1`` otherwise.
        """
        if self.exact_config is not None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = changed_line_failures(self._repo_root, self.exact_config)
            for relative, message in failures.items():
                report_finding(self.name, relative, message)
                print(f"FAIL [{self.name}] {relative}: {message}")
            return int(bool(failures))
        violations = sorted(self.collect_violations(), )
        if not violations:
            print(f"ok [arch:{self._name}] — new code clears the {self.floor_pct:g}% coverage floor.")
            return 0
        print(f"FAIL [arch:{self._name}] — new code below the {self.floor_pct:g}% coverage floor:")
        finding = f"new code below the {self.floor_pct:g}% coverage floor"
        for path in violations:
            report_finding(self.name, self._repo_relative(path).as_posix(), finding)
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁNewCodeCoverageǁrun__mutmut_21(self) -> int:
        """Hard-floor gate: every below-floor changed file fails.

        The "new" line set is recomputed against the merge-base on every branch,
        and an uncovered line added on this branch is a current defect. This
        method gates the raw violation set with a hard floor, mirroring
        SonarCloud's "Coverage on New Code"
        merge condition. Returns ``0`` when the changed lines clear the floor (or
        there is no measurable new code), ``1`` otherwise.
        """
        if self.exact_config is not None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = changed_line_failures(self._repo_root, self.exact_config)
            for relative, message in failures.items():
                report_finding(self.name, relative, message)
                print(f"FAIL [{self.name}] {relative}: {message}")
            return int(bool(failures))
        violations = sorted(self.collect_violations(), key=lambda path: None)
        if not violations:
            print(f"ok [arch:{self._name}] — new code clears the {self.floor_pct:g}% coverage floor.")
            return 0
        print(f"FAIL [arch:{self._name}] — new code below the {self.floor_pct:g}% coverage floor:")
        finding = f"new code below the {self.floor_pct:g}% coverage floor"
        for path in violations:
            report_finding(self.name, self._repo_relative(path).as_posix(), finding)
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁNewCodeCoverageǁrun__mutmut_22(self) -> int:
        """Hard-floor gate: every below-floor changed file fails.

        The "new" line set is recomputed against the merge-base on every branch,
        and an uncovered line added on this branch is a current defect. This
        method gates the raw violation set with a hard floor, mirroring
        SonarCloud's "Coverage on New Code"
        merge condition. Returns ``0`` when the changed lines clear the floor (or
        there is no measurable new code), ``1`` otherwise.
        """
        if self.exact_config is not None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = changed_line_failures(self._repo_root, self.exact_config)
            for relative, message in failures.items():
                report_finding(self.name, relative, message)
                print(f"FAIL [{self.name}] {relative}: {message}")
            return int(bool(failures))
        violations = sorted(self.collect_violations(), key=lambda path: str(None))
        if not violations:
            print(f"ok [arch:{self._name}] — new code clears the {self.floor_pct:g}% coverage floor.")
            return 0
        print(f"FAIL [arch:{self._name}] — new code below the {self.floor_pct:g}% coverage floor:")
        finding = f"new code below the {self.floor_pct:g}% coverage floor"
        for path in violations:
            report_finding(self.name, self._repo_relative(path).as_posix(), finding)
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁNewCodeCoverageǁrun__mutmut_23(self) -> int:
        """Hard-floor gate: every below-floor changed file fails.

        The "new" line set is recomputed against the merge-base on every branch,
        and an uncovered line added on this branch is a current defect. This
        method gates the raw violation set with a hard floor, mirroring
        SonarCloud's "Coverage on New Code"
        merge condition. Returns ``0`` when the changed lines clear the floor (or
        there is no measurable new code), ``1`` otherwise.
        """
        if self.exact_config is not None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = changed_line_failures(self._repo_root, self.exact_config)
            for relative, message in failures.items():
                report_finding(self.name, relative, message)
                print(f"FAIL [{self.name}] {relative}: {message}")
            return int(bool(failures))
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if violations:
            print(f"ok [arch:{self._name}] — new code clears the {self.floor_pct:g}% coverage floor.")
            return 0
        print(f"FAIL [arch:{self._name}] — new code below the {self.floor_pct:g}% coverage floor:")
        finding = f"new code below the {self.floor_pct:g}% coverage floor"
        for path in violations:
            report_finding(self.name, self._repo_relative(path).as_posix(), finding)
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁNewCodeCoverageǁrun__mutmut_24(self) -> int:
        """Hard-floor gate: every below-floor changed file fails.

        The "new" line set is recomputed against the merge-base on every branch,
        and an uncovered line added on this branch is a current defect. This
        method gates the raw violation set with a hard floor, mirroring
        SonarCloud's "Coverage on New Code"
        merge condition. Returns ``0`` when the changed lines clear the floor (or
        there is no measurable new code), ``1`` otherwise.
        """
        if self.exact_config is not None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = changed_line_failures(self._repo_root, self.exact_config)
            for relative, message in failures.items():
                report_finding(self.name, relative, message)
                print(f"FAIL [{self.name}] {relative}: {message}")
            return int(bool(failures))
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(None)
            return 0
        print(f"FAIL [arch:{self._name}] — new code below the {self.floor_pct:g}% coverage floor:")
        finding = f"new code below the {self.floor_pct:g}% coverage floor"
        for path in violations:
            report_finding(self.name, self._repo_relative(path).as_posix(), finding)
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁNewCodeCoverageǁrun__mutmut_25(self) -> int:
        """Hard-floor gate: every below-floor changed file fails.

        The "new" line set is recomputed against the merge-base on every branch,
        and an uncovered line added on this branch is a current defect. This
        method gates the raw violation set with a hard floor, mirroring
        SonarCloud's "Coverage on New Code"
        merge condition. Returns ``0`` when the changed lines clear the floor (or
        there is no measurable new code), ``1`` otherwise.
        """
        if self.exact_config is not None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = changed_line_failures(self._repo_root, self.exact_config)
            for relative, message in failures.items():
                report_finding(self.name, relative, message)
                print(f"FAIL [{self.name}] {relative}: {message}")
            return int(bool(failures))
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — new code clears the {self.floor_pct:g}% coverage floor.")
            return 1
        print(f"FAIL [arch:{self._name}] — new code below the {self.floor_pct:g}% coverage floor:")
        finding = f"new code below the {self.floor_pct:g}% coverage floor"
        for path in violations:
            report_finding(self.name, self._repo_relative(path).as_posix(), finding)
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁNewCodeCoverageǁrun__mutmut_26(self) -> int:
        """Hard-floor gate: every below-floor changed file fails.

        The "new" line set is recomputed against the merge-base on every branch,
        and an uncovered line added on this branch is a current defect. This
        method gates the raw violation set with a hard floor, mirroring
        SonarCloud's "Coverage on New Code"
        merge condition. Returns ``0`` when the changed lines clear the floor (or
        there is no measurable new code), ``1`` otherwise.
        """
        if self.exact_config is not None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = changed_line_failures(self._repo_root, self.exact_config)
            for relative, message in failures.items():
                report_finding(self.name, relative, message)
                print(f"FAIL [{self.name}] {relative}: {message}")
            return int(bool(failures))
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — new code clears the {self.floor_pct:g}% coverage floor.")
            return 0
        print(None)
        finding = f"new code below the {self.floor_pct:g}% coverage floor"
        for path in violations:
            report_finding(self.name, self._repo_relative(path).as_posix(), finding)
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁNewCodeCoverageǁrun__mutmut_27(self) -> int:
        """Hard-floor gate: every below-floor changed file fails.

        The "new" line set is recomputed against the merge-base on every branch,
        and an uncovered line added on this branch is a current defect. This
        method gates the raw violation set with a hard floor, mirroring
        SonarCloud's "Coverage on New Code"
        merge condition. Returns ``0`` when the changed lines clear the floor (or
        there is no measurable new code), ``1`` otherwise.
        """
        if self.exact_config is not None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = changed_line_failures(self._repo_root, self.exact_config)
            for relative, message in failures.items():
                report_finding(self.name, relative, message)
                print(f"FAIL [{self.name}] {relative}: {message}")
            return int(bool(failures))
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — new code clears the {self.floor_pct:g}% coverage floor.")
            return 0
        print(f"FAIL [arch:{self._name}] — new code below the {self.floor_pct:g}% coverage floor:")
        finding = None
        for path in violations:
            report_finding(self.name, self._repo_relative(path).as_posix(), finding)
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁNewCodeCoverageǁrun__mutmut_28(self) -> int:
        """Hard-floor gate: every below-floor changed file fails.

        The "new" line set is recomputed against the merge-base on every branch,
        and an uncovered line added on this branch is a current defect. This
        method gates the raw violation set with a hard floor, mirroring
        SonarCloud's "Coverage on New Code"
        merge condition. Returns ``0`` when the changed lines clear the floor (or
        there is no measurable new code), ``1`` otherwise.
        """
        if self.exact_config is not None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = changed_line_failures(self._repo_root, self.exact_config)
            for relative, message in failures.items():
                report_finding(self.name, relative, message)
                print(f"FAIL [{self.name}] {relative}: {message}")
            return int(bool(failures))
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — new code clears the {self.floor_pct:g}% coverage floor.")
            return 0
        print(f"FAIL [arch:{self._name}] — new code below the {self.floor_pct:g}% coverage floor:")
        finding = f"new code below the {self.floor_pct:g}% coverage floor"
        for path in violations:
            report_finding(None, self._repo_relative(path).as_posix(), finding)
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁNewCodeCoverageǁrun__mutmut_29(self) -> int:
        """Hard-floor gate: every below-floor changed file fails.

        The "new" line set is recomputed against the merge-base on every branch,
        and an uncovered line added on this branch is a current defect. This
        method gates the raw violation set with a hard floor, mirroring
        SonarCloud's "Coverage on New Code"
        merge condition. Returns ``0`` when the changed lines clear the floor (or
        there is no measurable new code), ``1`` otherwise.
        """
        if self.exact_config is not None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = changed_line_failures(self._repo_root, self.exact_config)
            for relative, message in failures.items():
                report_finding(self.name, relative, message)
                print(f"FAIL [{self.name}] {relative}: {message}")
            return int(bool(failures))
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — new code clears the {self.floor_pct:g}% coverage floor.")
            return 0
        print(f"FAIL [arch:{self._name}] — new code below the {self.floor_pct:g}% coverage floor:")
        finding = f"new code below the {self.floor_pct:g}% coverage floor"
        for path in violations:
            report_finding(self.name, None, finding)
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁNewCodeCoverageǁrun__mutmut_30(self) -> int:
        """Hard-floor gate: every below-floor changed file fails.

        The "new" line set is recomputed against the merge-base on every branch,
        and an uncovered line added on this branch is a current defect. This
        method gates the raw violation set with a hard floor, mirroring
        SonarCloud's "Coverage on New Code"
        merge condition. Returns ``0`` when the changed lines clear the floor (or
        there is no measurable new code), ``1`` otherwise.
        """
        if self.exact_config is not None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = changed_line_failures(self._repo_root, self.exact_config)
            for relative, message in failures.items():
                report_finding(self.name, relative, message)
                print(f"FAIL [{self.name}] {relative}: {message}")
            return int(bool(failures))
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — new code clears the {self.floor_pct:g}% coverage floor.")
            return 0
        print(f"FAIL [arch:{self._name}] — new code below the {self.floor_pct:g}% coverage floor:")
        finding = f"new code below the {self.floor_pct:g}% coverage floor"
        for path in violations:
            report_finding(self.name, self._repo_relative(path).as_posix(), None)
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁNewCodeCoverageǁrun__mutmut_31(self) -> int:
        """Hard-floor gate: every below-floor changed file fails.

        The "new" line set is recomputed against the merge-base on every branch,
        and an uncovered line added on this branch is a current defect. This
        method gates the raw violation set with a hard floor, mirroring
        SonarCloud's "Coverage on New Code"
        merge condition. Returns ``0`` when the changed lines clear the floor (or
        there is no measurable new code), ``1`` otherwise.
        """
        if self.exact_config is not None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = changed_line_failures(self._repo_root, self.exact_config)
            for relative, message in failures.items():
                report_finding(self.name, relative, message)
                print(f"FAIL [{self.name}] {relative}: {message}")
            return int(bool(failures))
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — new code clears the {self.floor_pct:g}% coverage floor.")
            return 0
        print(f"FAIL [arch:{self._name}] — new code below the {self.floor_pct:g}% coverage floor:")
        finding = f"new code below the {self.floor_pct:g}% coverage floor"
        for path in violations:
            report_finding(self._repo_relative(path).as_posix(), finding)
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁNewCodeCoverageǁrun__mutmut_32(self) -> int:
        """Hard-floor gate: every below-floor changed file fails.

        The "new" line set is recomputed against the merge-base on every branch,
        and an uncovered line added on this branch is a current defect. This
        method gates the raw violation set with a hard floor, mirroring
        SonarCloud's "Coverage on New Code"
        merge condition. Returns ``0`` when the changed lines clear the floor (or
        there is no measurable new code), ``1`` otherwise.
        """
        if self.exact_config is not None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = changed_line_failures(self._repo_root, self.exact_config)
            for relative, message in failures.items():
                report_finding(self.name, relative, message)
                print(f"FAIL [{self.name}] {relative}: {message}")
            return int(bool(failures))
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — new code clears the {self.floor_pct:g}% coverage floor.")
            return 0
        print(f"FAIL [arch:{self._name}] — new code below the {self.floor_pct:g}% coverage floor:")
        finding = f"new code below the {self.floor_pct:g}% coverage floor"
        for path in violations:
            report_finding(self.name, finding)
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁNewCodeCoverageǁrun__mutmut_33(self) -> int:
        """Hard-floor gate: every below-floor changed file fails.

        The "new" line set is recomputed against the merge-base on every branch,
        and an uncovered line added on this branch is a current defect. This
        method gates the raw violation set with a hard floor, mirroring
        SonarCloud's "Coverage on New Code"
        merge condition. Returns ``0`` when the changed lines clear the floor (or
        there is no measurable new code), ``1`` otherwise.
        """
        if self.exact_config is not None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = changed_line_failures(self._repo_root, self.exact_config)
            for relative, message in failures.items():
                report_finding(self.name, relative, message)
                print(f"FAIL [{self.name}] {relative}: {message}")
            return int(bool(failures))
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — new code clears the {self.floor_pct:g}% coverage floor.")
            return 0
        print(f"FAIL [arch:{self._name}] — new code below the {self.floor_pct:g}% coverage floor:")
        finding = f"new code below the {self.floor_pct:g}% coverage floor"
        for path in violations:
            report_finding(self.name, self._repo_relative(path).as_posix(), )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁNewCodeCoverageǁrun__mutmut_34(self) -> int:
        """Hard-floor gate: every below-floor changed file fails.

        The "new" line set is recomputed against the merge-base on every branch,
        and an uncovered line added on this branch is a current defect. This
        method gates the raw violation set with a hard floor, mirroring
        SonarCloud's "Coverage on New Code"
        merge condition. Returns ``0`` when the changed lines clear the floor (or
        there is no measurable new code), ``1`` otherwise.
        """
        if self.exact_config is not None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = changed_line_failures(self._repo_root, self.exact_config)
            for relative, message in failures.items():
                report_finding(self.name, relative, message)
                print(f"FAIL [{self.name}] {relative}: {message}")
            return int(bool(failures))
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — new code clears the {self.floor_pct:g}% coverage floor.")
            return 0
        print(f"FAIL [arch:{self._name}] — new code below the {self.floor_pct:g}% coverage floor:")
        finding = f"new code below the {self.floor_pct:g}% coverage floor"
        for path in violations:
            report_finding(self.name, self._repo_relative(None).as_posix(), finding)
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁNewCodeCoverageǁrun__mutmut_35(self) -> int:
        """Hard-floor gate: every below-floor changed file fails.

        The "new" line set is recomputed against the merge-base on every branch,
        and an uncovered line added on this branch is a current defect. This
        method gates the raw violation set with a hard floor, mirroring
        SonarCloud's "Coverage on New Code"
        merge condition. Returns ``0`` when the changed lines clear the floor (or
        there is no measurable new code), ``1`` otherwise.
        """
        if self.exact_config is not None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = changed_line_failures(self._repo_root, self.exact_config)
            for relative, message in failures.items():
                report_finding(self.name, relative, message)
                print(f"FAIL [{self.name}] {relative}: {message}")
            return int(bool(failures))
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — new code clears the {self.floor_pct:g}% coverage floor.")
            return 0
        print(f"FAIL [arch:{self._name}] — new code below the {self.floor_pct:g}% coverage floor:")
        finding = f"new code below the {self.floor_pct:g}% coverage floor"
        for path in violations:
            report_finding(self.name, self._repo_relative(path).as_posix(), finding)
            print(None)
        print()
        print(self.remediation)
        return 1

    def xǁNewCodeCoverageǁrun__mutmut_36(self) -> int:
        """Hard-floor gate: every below-floor changed file fails.

        The "new" line set is recomputed against the merge-base on every branch,
        and an uncovered line added on this branch is a current defect. This
        method gates the raw violation set with a hard floor, mirroring
        SonarCloud's "Coverage on New Code"
        merge condition. Returns ``0`` when the changed lines clear the floor (or
        there is no measurable new code), ``1`` otherwise.
        """
        if self.exact_config is not None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = changed_line_failures(self._repo_root, self.exact_config)
            for relative, message in failures.items():
                report_finding(self.name, relative, message)
                print(f"FAIL [{self.name}] {relative}: {message}")
            return int(bool(failures))
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — new code clears the {self.floor_pct:g}% coverage floor.")
            return 0
        print(f"FAIL [arch:{self._name}] — new code below the {self.floor_pct:g}% coverage floor:")
        finding = f"new code below the {self.floor_pct:g}% coverage floor"
        for path in violations:
            report_finding(self.name, self._repo_relative(path).as_posix(), finding)
            print(f"  {path}")
        print()
        print(None)
        return 1

    def xǁNewCodeCoverageǁrun__mutmut_37(self) -> int:
        """Hard-floor gate: every below-floor changed file fails.

        The "new" line set is recomputed against the merge-base on every branch,
        and an uncovered line added on this branch is a current defect. This
        method gates the raw violation set with a hard floor, mirroring
        SonarCloud's "Coverage on New Code"
        merge condition. Returns ``0`` when the changed lines clear the floor (or
        there is no measurable new code), ``1`` otherwise.
        """
        if self.exact_config is not None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = changed_line_failures(self._repo_root, self.exact_config)
            for relative, message in failures.items():
                report_finding(self.name, relative, message)
                print(f"FAIL [{self.name}] {relative}: {message}")
            return int(bool(failures))
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — new code clears the {self.floor_pct:g}% coverage floor.")
            return 0
        print(f"FAIL [arch:{self._name}] — new code below the {self.floor_pct:g}% coverage floor:")
        finding = f"new code below the {self.floor_pct:g}% coverage floor"
        for path in violations:
            report_finding(self.name, self._repo_relative(path).as_posix(), finding)
            print(f"  {path}")
        print()
        print(self.remediation)
        return 2

mutants_xǁNewCodeCoverageǁfrom_config__mutmut['_mutmut_orig'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut['xǁNewCodeCoverageǁfrom_config__mutmut_1'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut['xǁNewCodeCoverageǁfrom_config__mutmut_2'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut['xǁNewCodeCoverageǁfrom_config__mutmut_3'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut['xǁNewCodeCoverageǁfrom_config__mutmut_4'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut['xǁNewCodeCoverageǁfrom_config__mutmut_5'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut['xǁNewCodeCoverageǁfrom_config__mutmut_6'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut['xǁNewCodeCoverageǁfrom_config__mutmut_7'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut['xǁNewCodeCoverageǁfrom_config__mutmut_8'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut['xǁNewCodeCoverageǁfrom_config__mutmut_9'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut['xǁNewCodeCoverageǁfrom_config__mutmut_10'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut['xǁNewCodeCoverageǁfrom_config__mutmut_11'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut['xǁNewCodeCoverageǁfrom_config__mutmut_12'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_12 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut['xǁNewCodeCoverageǁfrom_config__mutmut_13'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_13 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut['xǁNewCodeCoverageǁfrom_config__mutmut_14'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_14 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut['xǁNewCodeCoverageǁfrom_config__mutmut_15'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_15 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut['xǁNewCodeCoverageǁfrom_config__mutmut_16'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_16 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut['xǁNewCodeCoverageǁfrom_config__mutmut_17'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_17 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut['xǁNewCodeCoverageǁfrom_config__mutmut_18'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_18 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut['xǁNewCodeCoverageǁfrom_config__mutmut_19'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_19 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut['xǁNewCodeCoverageǁfrom_config__mutmut_20'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_20 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut['xǁNewCodeCoverageǁfrom_config__mutmut_21'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_21 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut['xǁNewCodeCoverageǁfrom_config__mutmut_22'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_22 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut['xǁNewCodeCoverageǁfrom_config__mutmut_23'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_23 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut['xǁNewCodeCoverageǁfrom_config__mutmut_24'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_24 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut['xǁNewCodeCoverageǁfrom_config__mutmut_25'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_25 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut['xǁNewCodeCoverageǁfrom_config__mutmut_26'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_26 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut['xǁNewCodeCoverageǁfrom_config__mutmut_27'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_27 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut['xǁNewCodeCoverageǁfrom_config__mutmut_28'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_28 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut['xǁNewCodeCoverageǁfrom_config__mutmut_29'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_29 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut['xǁNewCodeCoverageǁfrom_config__mutmut_30'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_30 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut['xǁNewCodeCoverageǁfrom_config__mutmut_31'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_31 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut['xǁNewCodeCoverageǁfrom_config__mutmut_32'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_32 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut['xǁNewCodeCoverageǁfrom_config__mutmut_33'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_33 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut['xǁNewCodeCoverageǁfrom_config__mutmut_34'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_34 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut['xǁNewCodeCoverageǁfrom_config__mutmut_35'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_35 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut['xǁNewCodeCoverageǁfrom_config__mutmut_36'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_36 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut['xǁNewCodeCoverageǁfrom_config__mutmut_37'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_37 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut['xǁNewCodeCoverageǁfrom_config__mutmut_38'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_38 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut['xǁNewCodeCoverageǁfrom_config__mutmut_39'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_39 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfrom_config__mutmut['xǁNewCodeCoverageǁfrom_config__mutmut_40'] = NewCodeCoverage.xǁNewCodeCoverageǁfrom_config__mutmut_40 # type: ignore # mutmut generated

mutants_xǁNewCodeCoverageǁ_report_path__mutmut['_mutmut_orig'] = NewCodeCoverage.xǁNewCodeCoverageǁ_report_path__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_report_path__mutmut['xǁNewCodeCoverageǁ_report_path__mutmut_1'] = NewCodeCoverage.xǁNewCodeCoverageǁ_report_path__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_report_path__mutmut['xǁNewCodeCoverageǁ_report_path__mutmut_2'] = NewCodeCoverage.xǁNewCodeCoverageǁ_report_path__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_report_path__mutmut['xǁNewCodeCoverageǁ_report_path__mutmut_3'] = NewCodeCoverage.xǁNewCodeCoverageǁ_report_path__mutmut_3 # type: ignore # mutmut generated

mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['_mutmut_orig'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_1'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_2'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_3'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_4'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_4 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_5'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_5 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_6'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_6 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_7'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_7 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_8'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_8 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_9'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_9 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_10'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_10 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_11'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_11 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_12'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_12 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_13'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_13 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_14'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_14 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_15'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_15 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_16'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_16 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_17'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_17 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_18'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_18 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_19'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_19 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_20'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_20 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_21'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_21 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_22'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_22 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_23'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_23 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_24'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_24 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_25'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_25 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_26'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_26 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_27'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_27 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_28'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_28 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_29'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_29 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_30'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_30 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_31'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_31 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_32'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_32 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_33'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_33 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_34'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_34 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_35'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_35 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_36'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_36 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_37'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_37 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_38'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_38 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_39'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_39 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_40'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_40 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_41'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_41 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_42'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_42 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_43'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_43 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_44'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_44 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_45'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_45 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_46'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_46 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_47'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_47 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_48'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_48 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_49'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_49 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_50'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_50 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_51'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_51 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_52'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_52 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_53'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_53 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_54'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_54 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_55'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_55 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_56'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_56 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_57'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_57 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_58'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_58 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_59'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_59 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_60'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_60 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_refresh_remote_base__mutmut['xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_61'] = NewCodeCoverage.xǁNewCodeCoverageǁ_refresh_remote_base__mutmut_61 # type: ignore # mutmut generated

mutants_xǁNewCodeCoverageǁ_changed_lines__mutmut['_mutmut_orig'] = NewCodeCoverage.xǁNewCodeCoverageǁ_changed_lines__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_changed_lines__mutmut['xǁNewCodeCoverageǁ_changed_lines__mutmut_1'] = NewCodeCoverage.xǁNewCodeCoverageǁ_changed_lines__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_changed_lines__mutmut['xǁNewCodeCoverageǁ_changed_lines__mutmut_2'] = NewCodeCoverage.xǁNewCodeCoverageǁ_changed_lines__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_changed_lines__mutmut['xǁNewCodeCoverageǁ_changed_lines__mutmut_3'] = NewCodeCoverage.xǁNewCodeCoverageǁ_changed_lines__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_changed_lines__mutmut['xǁNewCodeCoverageǁ_changed_lines__mutmut_4'] = NewCodeCoverage.xǁNewCodeCoverageǁ_changed_lines__mutmut_4 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_changed_lines__mutmut['xǁNewCodeCoverageǁ_changed_lines__mutmut_5'] = NewCodeCoverage.xǁNewCodeCoverageǁ_changed_lines__mutmut_5 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_changed_lines__mutmut['xǁNewCodeCoverageǁ_changed_lines__mutmut_6'] = NewCodeCoverage.xǁNewCodeCoverageǁ_changed_lines__mutmut_6 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_changed_lines__mutmut['xǁNewCodeCoverageǁ_changed_lines__mutmut_7'] = NewCodeCoverage.xǁNewCodeCoverageǁ_changed_lines__mutmut_7 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_changed_lines__mutmut['xǁNewCodeCoverageǁ_changed_lines__mutmut_8'] = NewCodeCoverage.xǁNewCodeCoverageǁ_changed_lines__mutmut_8 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_changed_lines__mutmut['xǁNewCodeCoverageǁ_changed_lines__mutmut_9'] = NewCodeCoverage.xǁNewCodeCoverageǁ_changed_lines__mutmut_9 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_changed_lines__mutmut['xǁNewCodeCoverageǁ_changed_lines__mutmut_10'] = NewCodeCoverage.xǁNewCodeCoverageǁ_changed_lines__mutmut_10 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_changed_lines__mutmut['xǁNewCodeCoverageǁ_changed_lines__mutmut_11'] = NewCodeCoverage.xǁNewCodeCoverageǁ_changed_lines__mutmut_11 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_changed_lines__mutmut['xǁNewCodeCoverageǁ_changed_lines__mutmut_12'] = NewCodeCoverage.xǁNewCodeCoverageǁ_changed_lines__mutmut_12 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_changed_lines__mutmut['xǁNewCodeCoverageǁ_changed_lines__mutmut_13'] = NewCodeCoverage.xǁNewCodeCoverageǁ_changed_lines__mutmut_13 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_changed_lines__mutmut['xǁNewCodeCoverageǁ_changed_lines__mutmut_14'] = NewCodeCoverage.xǁNewCodeCoverageǁ_changed_lines__mutmut_14 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_changed_lines__mutmut['xǁNewCodeCoverageǁ_changed_lines__mutmut_15'] = NewCodeCoverage.xǁNewCodeCoverageǁ_changed_lines__mutmut_15 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_changed_lines__mutmut['xǁNewCodeCoverageǁ_changed_lines__mutmut_16'] = NewCodeCoverage.xǁNewCodeCoverageǁ_changed_lines__mutmut_16 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_changed_lines__mutmut['xǁNewCodeCoverageǁ_changed_lines__mutmut_17'] = NewCodeCoverage.xǁNewCodeCoverageǁ_changed_lines__mutmut_17 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_changed_lines__mutmut['xǁNewCodeCoverageǁ_changed_lines__mutmut_18'] = NewCodeCoverage.xǁNewCodeCoverageǁ_changed_lines__mutmut_18 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_changed_lines__mutmut['xǁNewCodeCoverageǁ_changed_lines__mutmut_19'] = NewCodeCoverage.xǁNewCodeCoverageǁ_changed_lines__mutmut_19 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_changed_lines__mutmut['xǁNewCodeCoverageǁ_changed_lines__mutmut_20'] = NewCodeCoverage.xǁNewCodeCoverageǁ_changed_lines__mutmut_20 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_changed_lines__mutmut['xǁNewCodeCoverageǁ_changed_lines__mutmut_21'] = NewCodeCoverage.xǁNewCodeCoverageǁ_changed_lines__mutmut_21 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_changed_lines__mutmut['xǁNewCodeCoverageǁ_changed_lines__mutmut_22'] = NewCodeCoverage.xǁNewCodeCoverageǁ_changed_lines__mutmut_22 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_changed_lines__mutmut['xǁNewCodeCoverageǁ_changed_lines__mutmut_23'] = NewCodeCoverage.xǁNewCodeCoverageǁ_changed_lines__mutmut_23 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_changed_lines__mutmut['xǁNewCodeCoverageǁ_changed_lines__mutmut_24'] = NewCodeCoverage.xǁNewCodeCoverageǁ_changed_lines__mutmut_24 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_changed_lines__mutmut['xǁNewCodeCoverageǁ_changed_lines__mutmut_25'] = NewCodeCoverage.xǁNewCodeCoverageǁ_changed_lines__mutmut_25 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_changed_lines__mutmut['xǁNewCodeCoverageǁ_changed_lines__mutmut_26'] = NewCodeCoverage.xǁNewCodeCoverageǁ_changed_lines__mutmut_26 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_changed_lines__mutmut['xǁNewCodeCoverageǁ_changed_lines__mutmut_27'] = NewCodeCoverage.xǁNewCodeCoverageǁ_changed_lines__mutmut_27 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_changed_lines__mutmut['xǁNewCodeCoverageǁ_changed_lines__mutmut_28'] = NewCodeCoverage.xǁNewCodeCoverageǁ_changed_lines__mutmut_28 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_changed_lines__mutmut['xǁNewCodeCoverageǁ_changed_lines__mutmut_29'] = NewCodeCoverage.xǁNewCodeCoverageǁ_changed_lines__mutmut_29 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_changed_lines__mutmut['xǁNewCodeCoverageǁ_changed_lines__mutmut_30'] = NewCodeCoverage.xǁNewCodeCoverageǁ_changed_lines__mutmut_30 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_changed_lines__mutmut['xǁNewCodeCoverageǁ_changed_lines__mutmut_31'] = NewCodeCoverage.xǁNewCodeCoverageǁ_changed_lines__mutmut_31 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_changed_lines__mutmut['xǁNewCodeCoverageǁ_changed_lines__mutmut_32'] = NewCodeCoverage.xǁNewCodeCoverageǁ_changed_lines__mutmut_32 # type: ignore # mutmut generated

mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['_mutmut_orig'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_1'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_2'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_3'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_4'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_4 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_5'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_5 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_6'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_6 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_7'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_7 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_8'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_8 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_9'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_9 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_10'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_10 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_11'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_11 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_12'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_12 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_13'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_13 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_14'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_14 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_15'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_15 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_16'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_16 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_17'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_17 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_18'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_18 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_19'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_19 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_20'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_20 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_21'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_21 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_22'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_22 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_23'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_23 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_24'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_24 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_25'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_25 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_26'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_26 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_27'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_27 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_28'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_28 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_29'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_29 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_30'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_30 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_31'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_31 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_32'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_32 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_33'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_33 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_34'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_34 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_35'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_35 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_36'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_36 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_37'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_37 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_38'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_38 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_39'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_39 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_40'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_40 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_41'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_41 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_42'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_42 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_43'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_43 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_44'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_44 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_45'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_45 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_46'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_46 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁ_untracked_added_lines__mutmut['xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_47'] = NewCodeCoverage.xǁNewCodeCoverageǁ_untracked_added_lines__mutmut_47 # type: ignore # mutmut generated

mutants_xǁNewCodeCoverageǁenumerate_files__mutmut['_mutmut_orig'] = NewCodeCoverage.xǁNewCodeCoverageǁenumerate_files__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁenumerate_files__mutmut['xǁNewCodeCoverageǁenumerate_files__mutmut_1'] = NewCodeCoverage.xǁNewCodeCoverageǁenumerate_files__mutmut_1 # type: ignore # mutmut generated

mutants_xǁNewCodeCoverageǁfile_has_violation__mutmut['_mutmut_orig'] = NewCodeCoverage.xǁNewCodeCoverageǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfile_has_violation__mutmut['xǁNewCodeCoverageǁfile_has_violation__mutmut_1'] = NewCodeCoverage.xǁNewCodeCoverageǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfile_has_violation__mutmut['xǁNewCodeCoverageǁfile_has_violation__mutmut_2'] = NewCodeCoverage.xǁNewCodeCoverageǁfile_has_violation__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfile_has_violation__mutmut['xǁNewCodeCoverageǁfile_has_violation__mutmut_3'] = NewCodeCoverage.xǁNewCodeCoverageǁfile_has_violation__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfile_has_violation__mutmut['xǁNewCodeCoverageǁfile_has_violation__mutmut_4'] = NewCodeCoverage.xǁNewCodeCoverageǁfile_has_violation__mutmut_4 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfile_has_violation__mutmut['xǁNewCodeCoverageǁfile_has_violation__mutmut_5'] = NewCodeCoverage.xǁNewCodeCoverageǁfile_has_violation__mutmut_5 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfile_has_violation__mutmut['xǁNewCodeCoverageǁfile_has_violation__mutmut_6'] = NewCodeCoverage.xǁNewCodeCoverageǁfile_has_violation__mutmut_6 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfile_has_violation__mutmut['xǁNewCodeCoverageǁfile_has_violation__mutmut_7'] = NewCodeCoverage.xǁNewCodeCoverageǁfile_has_violation__mutmut_7 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfile_has_violation__mutmut['xǁNewCodeCoverageǁfile_has_violation__mutmut_8'] = NewCodeCoverage.xǁNewCodeCoverageǁfile_has_violation__mutmut_8 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfile_has_violation__mutmut['xǁNewCodeCoverageǁfile_has_violation__mutmut_9'] = NewCodeCoverage.xǁNewCodeCoverageǁfile_has_violation__mutmut_9 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfile_has_violation__mutmut['xǁNewCodeCoverageǁfile_has_violation__mutmut_10'] = NewCodeCoverage.xǁNewCodeCoverageǁfile_has_violation__mutmut_10 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfile_has_violation__mutmut['xǁNewCodeCoverageǁfile_has_violation__mutmut_11'] = NewCodeCoverage.xǁNewCodeCoverageǁfile_has_violation__mutmut_11 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁfile_has_violation__mutmut['xǁNewCodeCoverageǁfile_has_violation__mutmut_12'] = NewCodeCoverage.xǁNewCodeCoverageǁfile_has_violation__mutmut_12 # type: ignore # mutmut generated

mutants_xǁNewCodeCoverageǁrun__mutmut['_mutmut_orig'] = NewCodeCoverage.xǁNewCodeCoverageǁrun__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁrun__mutmut['xǁNewCodeCoverageǁrun__mutmut_1'] = NewCodeCoverage.xǁNewCodeCoverageǁrun__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁrun__mutmut['xǁNewCodeCoverageǁrun__mutmut_2'] = NewCodeCoverage.xǁNewCodeCoverageǁrun__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁrun__mutmut['xǁNewCodeCoverageǁrun__mutmut_3'] = NewCodeCoverage.xǁNewCodeCoverageǁrun__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁrun__mutmut['xǁNewCodeCoverageǁrun__mutmut_4'] = NewCodeCoverage.xǁNewCodeCoverageǁrun__mutmut_4 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁrun__mutmut['xǁNewCodeCoverageǁrun__mutmut_5'] = NewCodeCoverage.xǁNewCodeCoverageǁrun__mutmut_5 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁrun__mutmut['xǁNewCodeCoverageǁrun__mutmut_6'] = NewCodeCoverage.xǁNewCodeCoverageǁrun__mutmut_6 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁrun__mutmut['xǁNewCodeCoverageǁrun__mutmut_7'] = NewCodeCoverage.xǁNewCodeCoverageǁrun__mutmut_7 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁrun__mutmut['xǁNewCodeCoverageǁrun__mutmut_8'] = NewCodeCoverage.xǁNewCodeCoverageǁrun__mutmut_8 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁrun__mutmut['xǁNewCodeCoverageǁrun__mutmut_9'] = NewCodeCoverage.xǁNewCodeCoverageǁrun__mutmut_9 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁrun__mutmut['xǁNewCodeCoverageǁrun__mutmut_10'] = NewCodeCoverage.xǁNewCodeCoverageǁrun__mutmut_10 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁrun__mutmut['xǁNewCodeCoverageǁrun__mutmut_11'] = NewCodeCoverage.xǁNewCodeCoverageǁrun__mutmut_11 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁrun__mutmut['xǁNewCodeCoverageǁrun__mutmut_12'] = NewCodeCoverage.xǁNewCodeCoverageǁrun__mutmut_12 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁrun__mutmut['xǁNewCodeCoverageǁrun__mutmut_13'] = NewCodeCoverage.xǁNewCodeCoverageǁrun__mutmut_13 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁrun__mutmut['xǁNewCodeCoverageǁrun__mutmut_14'] = NewCodeCoverage.xǁNewCodeCoverageǁrun__mutmut_14 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁrun__mutmut['xǁNewCodeCoverageǁrun__mutmut_15'] = NewCodeCoverage.xǁNewCodeCoverageǁrun__mutmut_15 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁrun__mutmut['xǁNewCodeCoverageǁrun__mutmut_16'] = NewCodeCoverage.xǁNewCodeCoverageǁrun__mutmut_16 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁrun__mutmut['xǁNewCodeCoverageǁrun__mutmut_17'] = NewCodeCoverage.xǁNewCodeCoverageǁrun__mutmut_17 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁrun__mutmut['xǁNewCodeCoverageǁrun__mutmut_18'] = NewCodeCoverage.xǁNewCodeCoverageǁrun__mutmut_18 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁrun__mutmut['xǁNewCodeCoverageǁrun__mutmut_19'] = NewCodeCoverage.xǁNewCodeCoverageǁrun__mutmut_19 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁrun__mutmut['xǁNewCodeCoverageǁrun__mutmut_20'] = NewCodeCoverage.xǁNewCodeCoverageǁrun__mutmut_20 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁrun__mutmut['xǁNewCodeCoverageǁrun__mutmut_21'] = NewCodeCoverage.xǁNewCodeCoverageǁrun__mutmut_21 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁrun__mutmut['xǁNewCodeCoverageǁrun__mutmut_22'] = NewCodeCoverage.xǁNewCodeCoverageǁrun__mutmut_22 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁrun__mutmut['xǁNewCodeCoverageǁrun__mutmut_23'] = NewCodeCoverage.xǁNewCodeCoverageǁrun__mutmut_23 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁrun__mutmut['xǁNewCodeCoverageǁrun__mutmut_24'] = NewCodeCoverage.xǁNewCodeCoverageǁrun__mutmut_24 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁrun__mutmut['xǁNewCodeCoverageǁrun__mutmut_25'] = NewCodeCoverage.xǁNewCodeCoverageǁrun__mutmut_25 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁrun__mutmut['xǁNewCodeCoverageǁrun__mutmut_26'] = NewCodeCoverage.xǁNewCodeCoverageǁrun__mutmut_26 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁrun__mutmut['xǁNewCodeCoverageǁrun__mutmut_27'] = NewCodeCoverage.xǁNewCodeCoverageǁrun__mutmut_27 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁrun__mutmut['xǁNewCodeCoverageǁrun__mutmut_28'] = NewCodeCoverage.xǁNewCodeCoverageǁrun__mutmut_28 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁrun__mutmut['xǁNewCodeCoverageǁrun__mutmut_29'] = NewCodeCoverage.xǁNewCodeCoverageǁrun__mutmut_29 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁrun__mutmut['xǁNewCodeCoverageǁrun__mutmut_30'] = NewCodeCoverage.xǁNewCodeCoverageǁrun__mutmut_30 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁrun__mutmut['xǁNewCodeCoverageǁrun__mutmut_31'] = NewCodeCoverage.xǁNewCodeCoverageǁrun__mutmut_31 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁrun__mutmut['xǁNewCodeCoverageǁrun__mutmut_32'] = NewCodeCoverage.xǁNewCodeCoverageǁrun__mutmut_32 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁrun__mutmut['xǁNewCodeCoverageǁrun__mutmut_33'] = NewCodeCoverage.xǁNewCodeCoverageǁrun__mutmut_33 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁrun__mutmut['xǁNewCodeCoverageǁrun__mutmut_34'] = NewCodeCoverage.xǁNewCodeCoverageǁrun__mutmut_34 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁrun__mutmut['xǁNewCodeCoverageǁrun__mutmut_35'] = NewCodeCoverage.xǁNewCodeCoverageǁrun__mutmut_35 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁrun__mutmut['xǁNewCodeCoverageǁrun__mutmut_36'] = NewCodeCoverage.xǁNewCodeCoverageǁrun__mutmut_36 # type: ignore # mutmut generated
mutants_xǁNewCodeCoverageǁrun__mutmut['xǁNewCodeCoverageǁrun__mutmut_37'] = NewCodeCoverage.xǁNewCodeCoverageǁrun__mutmut_37 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
    git_runner: GitRunner | None = None,
) -> NewCodeCoverage:
    """Factory the engine calls to bind this CORE check to a consumer's config.

    ``git_runner`` is the DI seam: production leaves it ``None`` (the rule uses
    :func:`_default_git_runner`), a test passes a fake that returns canned
    ``merge-base`` / ``diff`` output so no real repository is required.
    """
    rule = NewCodeCoverage.from_config(config, repo_root=repo_root)
    if git_runner is not None:
        rule.git_runner = git_runner
    return rule


def x_build__mutmut_orig(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
    git_runner: GitRunner | None = None,
) -> NewCodeCoverage:
    """Factory the engine calls to bind this CORE check to a consumer's config.

    ``git_runner`` is the DI seam: production leaves it ``None`` (the rule uses
    :func:`_default_git_runner`), a test passes a fake that returns canned
    ``merge-base`` / ``diff`` output so no real repository is required.
    """
    rule = NewCodeCoverage.from_config(config, repo_root=repo_root)
    if git_runner is not None:
        rule.git_runner = git_runner
    return rule


def x_build__mutmut_1(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
    git_runner: GitRunner | None = None,
) -> NewCodeCoverage:
    """Factory the engine calls to bind this CORE check to a consumer's config.

    ``git_runner`` is the DI seam: production leaves it ``None`` (the rule uses
    :func:`_default_git_runner`), a test passes a fake that returns canned
    ``merge-base`` / ``diff`` output so no real repository is required.
    """
    rule = None
    if git_runner is not None:
        rule.git_runner = git_runner
    return rule


def x_build__mutmut_2(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
    git_runner: GitRunner | None = None,
) -> NewCodeCoverage:
    """Factory the engine calls to bind this CORE check to a consumer's config.

    ``git_runner`` is the DI seam: production leaves it ``None`` (the rule uses
    :func:`_default_git_runner`), a test passes a fake that returns canned
    ``merge-base`` / ``diff`` output so no real repository is required.
    """
    rule = NewCodeCoverage.from_config(None, repo_root=repo_root)
    if git_runner is not None:
        rule.git_runner = git_runner
    return rule


def x_build__mutmut_3(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
    git_runner: GitRunner | None = None,
) -> NewCodeCoverage:
    """Factory the engine calls to bind this CORE check to a consumer's config.

    ``git_runner`` is the DI seam: production leaves it ``None`` (the rule uses
    :func:`_default_git_runner`), a test passes a fake that returns canned
    ``merge-base`` / ``diff`` output so no real repository is required.
    """
    rule = NewCodeCoverage.from_config(config, repo_root=None)
    if git_runner is not None:
        rule.git_runner = git_runner
    return rule


def x_build__mutmut_4(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
    git_runner: GitRunner | None = None,
) -> NewCodeCoverage:
    """Factory the engine calls to bind this CORE check to a consumer's config.

    ``git_runner`` is the DI seam: production leaves it ``None`` (the rule uses
    :func:`_default_git_runner`), a test passes a fake that returns canned
    ``merge-base`` / ``diff`` output so no real repository is required.
    """
    rule = NewCodeCoverage.from_config(repo_root=repo_root)
    if git_runner is not None:
        rule.git_runner = git_runner
    return rule


def x_build__mutmut_5(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
    git_runner: GitRunner | None = None,
) -> NewCodeCoverage:
    """Factory the engine calls to bind this CORE check to a consumer's config.

    ``git_runner`` is the DI seam: production leaves it ``None`` (the rule uses
    :func:`_default_git_runner`), a test passes a fake that returns canned
    ``merge-base`` / ``diff`` output so no real repository is required.
    """
    rule = NewCodeCoverage.from_config(config, )
    if git_runner is not None:
        rule.git_runner = git_runner
    return rule


def x_build__mutmut_6(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
    git_runner: GitRunner | None = None,
) -> NewCodeCoverage:
    """Factory the engine calls to bind this CORE check to a consumer's config.

    ``git_runner`` is the DI seam: production leaves it ``None`` (the rule uses
    :func:`_default_git_runner`), a test passes a fake that returns canned
    ``merge-base`` / ``diff`` output so no real repository is required.
    """
    rule = NewCodeCoverage.from_config(config, repo_root=repo_root)
    if git_runner is None:
        rule.git_runner = git_runner
    return rule


def x_build__mutmut_7(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
    git_runner: GitRunner | None = None,
) -> NewCodeCoverage:
    """Factory the engine calls to bind this CORE check to a consumer's config.

    ``git_runner`` is the DI seam: production leaves it ``None`` (the rule uses
    :func:`_default_git_runner`), a test passes a fake that returns canned
    ``merge-base`` / ``diff`` output so no real repository is required.
    """
    rule = NewCodeCoverage.from_config(config, repo_root=repo_root)
    if git_runner is not None:
        rule.git_runner = None
    return rule

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_5'] = x_build__mutmut_5 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_6'] = x_build__mutmut_6 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_7'] = x_build__mutmut_7 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NewCodeCoverage, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NewCodeCoverage, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NewCodeCoverage, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NewCodeCoverage, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
