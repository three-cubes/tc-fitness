"""CORE check: coverage_includes_branches — the report measures branches.

Pure line coverage proves "this line executed" but not "both sides of this
conditional were taken". A suite can show 100% line coverage and still miss
half the logic. This rule asserts the coverage report carries non-zero branch
coverage, so the floor it feeds (see :mod:`coverage_floor`) is measuring
branches, not just lines.

Shape note. This is a single-artifact assertion, so it overrides
:meth:`enumerate_files` to yield the one coverage report and
:meth:`is_in_scope` to admit it. The gate fails when the report records zero
branches.

Ported from tc-agent-zone ``scripts/checks/coverage_includes_branches.py``
(FEAT-150 G4) — re-expressed as a configurable, repo-agnostic rule. The report
path is CONFIG; nothing here names a repo.
"""

from __future__ import annotations

import importlib
from collections.abc import Callable, Mapping
from pathlib import Path
from types import ModuleType
from typing import Any

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: Default coverage report location relative to the repo root. Overridable.
DEFAULT_COVERAGE_REPORT = "coverage.xml"

REMEDIATION = _remediation(
    fix=(
        "enable branch coverage in the coverage config (for a Cobertura report "
        "from coverage.py, set branch = true under [tool.coverage.run], or pass "
        "--cov-branch). If the report is already branch-aware but reports zero "
        "branches, the suite exercises no conditionals — add tests that take "
        "both sides of a branch."
    ),
    nxt="re-run this check after the next coverage run emits the report.",
    run="python -m tc_fitness.core_checks.coverage_includes_branches",
    passing="branch = true so the report carries branch-rate > 0 and branches-valid > 0",
    forbidden="ship a report whose root reports branch-rate of 0 after a real run",
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
    """Prefer defusedxml; fall back to stdlib after explicit DTD/entity rejection."""
    try:
        from defusedxml import ElementTree as DefusedET

        return DefusedET
    except ImportError:
        return import_module("xml.etree.ElementTree")


def x__resolve_element_tree__mutmut_orig(
    import_module: Callable[[str], ModuleType] = importlib.import_module,
) -> Any:
    """Prefer defusedxml; fall back to stdlib after explicit DTD/entity rejection."""
    try:
        from defusedxml import ElementTree as DefusedET

        return DefusedET
    except ImportError:
        return import_module("xml.etree.ElementTree")


def x__resolve_element_tree__mutmut_1(
    import_module: Callable[[str], ModuleType] = importlib.import_module,
) -> Any:
    """Prefer defusedxml; fall back to stdlib after explicit DTD/entity rejection."""
    try:
        from defusedxml import ElementTree as DefusedET

        return DefusedET
    except ImportError:
        return import_module(None)


def x__resolve_element_tree__mutmut_2(
    import_module: Callable[[str], ModuleType] = importlib.import_module,
) -> Any:
    """Prefer defusedxml; fall back to stdlib after explicit DTD/entity rejection."""
    try:
        from defusedxml import ElementTree as DefusedET

        return DefusedET
    except ImportError:
        return import_module("XXxml.etree.ElementTreeXX")


def x__resolve_element_tree__mutmut_3(
    import_module: Callable[[str], ModuleType] = importlib.import_module,
) -> Any:
    """Prefer defusedxml; fall back to stdlib after explicit DTD/entity rejection."""
    try:
        from defusedxml import ElementTree as DefusedET

        return DefusedET
    except ImportError:
        return import_module("xml.etree.elementtree")


def x__resolve_element_tree__mutmut_4(
    import_module: Callable[[str], ModuleType] = importlib.import_module,
) -> Any:
    """Prefer defusedxml; fall back to stdlib after explicit DTD/entity rejection."""
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
mutants_x_report_lacks_branches__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_report_lacks_branches__mutmut)
def report_lacks_branches(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = float(root.attrib.get("branch-rate", "0") or "0")
    branches_valid = int(root.attrib.get("branches-valid", "0") or "0")
    return branch_rate <= 0.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_orig(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = float(root.attrib.get("branch-rate", "0") or "0")
    branches_valid = int(root.attrib.get("branches-valid", "0") or "0")
    return branch_rate <= 0.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_1(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if report_path.exists():
        return True
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = float(root.attrib.get("branch-rate", "0") or "0")
    branches_valid = int(root.attrib.get("branches-valid", "0") or "0")
    return branch_rate <= 0.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_2(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return False
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = float(root.attrib.get("branch-rate", "0") or "0")
    branches_valid = int(root.attrib.get("branches-valid", "0") or "0")
    return branch_rate <= 0.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_3(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = None
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = float(root.attrib.get("branch-rate", "0") or "0")
    branches_valid = int(root.attrib.get("branches-valid", "0") or "0")
    return branch_rate <= 0.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_4(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding=None)
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = float(root.attrib.get("branch-rate", "0") or "0")
    branches_valid = int(root.attrib.get("branches-valid", "0") or "0")
    return branch_rate <= 0.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_5(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding="XXutf-8XX")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = float(root.attrib.get("branch-rate", "0") or "0")
    branches_valid = int(root.attrib.get("branches-valid", "0") or "0")
    return branch_rate <= 0.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_6(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding="UTF-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = float(root.attrib.get("branch-rate", "0") or "0")
    branches_valid = int(root.attrib.get("branches-valid", "0") or "0")
    return branch_rate <= 0.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_7(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(None, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = float(root.attrib.get("branch-rate", "0") or "0")
    branches_valid = int(root.attrib.get("branches-valid", "0") or "0")
    return branch_rate <= 0.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_8(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, None)
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = float(root.attrib.get("branch-rate", "0") or "0")
    branches_valid = int(root.attrib.get("branches-valid", "0") or "0")
    return branch_rate <= 0.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_9(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = float(root.attrib.get("branch-rate", "0") or "0")
    branches_valid = int(root.attrib.get("branches-valid", "0") or "0")
    return branch_rate <= 0.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_10(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, )
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = float(root.attrib.get("branch-rate", "0") or "0")
    branches_valid = int(root.attrib.get("branches-valid", "0") or "0")
    return branch_rate <= 0.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_11(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(None))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = float(root.attrib.get("branch-rate", "0") or "0")
    branches_valid = int(root.attrib.get("branches-valid", "0") or "0")
    return branch_rate <= 0.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_12(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = None
    root = et.parse(report_path).getroot()
    branch_rate = float(root.attrib.get("branch-rate", "0") or "0")
    branches_valid = int(root.attrib.get("branches-valid", "0") or "0")
    return branch_rate <= 0.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_13(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = float(root.attrib.get("branch-rate", "0") or "0")
    branches_valid = int(root.attrib.get("branches-valid", "0") or "0")
    return branch_rate <= 0.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_14(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = None
    branch_rate = float(root.attrib.get("branch-rate", "0") or "0")
    branches_valid = int(root.attrib.get("branches-valid", "0") or "0")
    return branch_rate <= 0.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_15(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(None).getroot()
    branch_rate = float(root.attrib.get("branch-rate", "0") or "0")
    branches_valid = int(root.attrib.get("branches-valid", "0") or "0")
    return branch_rate <= 0.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_16(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = None
    branches_valid = int(root.attrib.get("branches-valid", "0") or "0")
    return branch_rate <= 0.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_17(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = float(None)
    branches_valid = int(root.attrib.get("branches-valid", "0") or "0")
    return branch_rate <= 0.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_18(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = float(root.attrib.get("branch-rate", "0") and "0")
    branches_valid = int(root.attrib.get("branches-valid", "0") or "0")
    return branch_rate <= 0.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_19(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = float(root.attrib.get(None, "0") or "0")
    branches_valid = int(root.attrib.get("branches-valid", "0") or "0")
    return branch_rate <= 0.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_20(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = float(root.attrib.get("branch-rate", None) or "0")
    branches_valid = int(root.attrib.get("branches-valid", "0") or "0")
    return branch_rate <= 0.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_21(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = float(root.attrib.get("0") or "0")
    branches_valid = int(root.attrib.get("branches-valid", "0") or "0")
    return branch_rate <= 0.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_22(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = float(root.attrib.get("branch-rate", ) or "0")
    branches_valid = int(root.attrib.get("branches-valid", "0") or "0")
    return branch_rate <= 0.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_23(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = float(root.attrib.get("XXbranch-rateXX", "0") or "0")
    branches_valid = int(root.attrib.get("branches-valid", "0") or "0")
    return branch_rate <= 0.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_24(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = float(root.attrib.get("BRANCH-RATE", "0") or "0")
    branches_valid = int(root.attrib.get("branches-valid", "0") or "0")
    return branch_rate <= 0.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_25(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = float(root.attrib.get("branch-rate", "XX0XX") or "0")
    branches_valid = int(root.attrib.get("branches-valid", "0") or "0")
    return branch_rate <= 0.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_26(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = float(root.attrib.get("branch-rate", "0") or "XX0XX")
    branches_valid = int(root.attrib.get("branches-valid", "0") or "0")
    return branch_rate <= 0.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_27(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = float(root.attrib.get("branch-rate", "0") or "0")
    branches_valid = None
    return branch_rate <= 0.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_28(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = float(root.attrib.get("branch-rate", "0") or "0")
    branches_valid = int(None)
    return branch_rate <= 0.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_29(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = float(root.attrib.get("branch-rate", "0") or "0")
    branches_valid = int(root.attrib.get("branches-valid", "0") and "0")
    return branch_rate <= 0.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_30(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = float(root.attrib.get("branch-rate", "0") or "0")
    branches_valid = int(root.attrib.get(None, "0") or "0")
    return branch_rate <= 0.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_31(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = float(root.attrib.get("branch-rate", "0") or "0")
    branches_valid = int(root.attrib.get("branches-valid", None) or "0")
    return branch_rate <= 0.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_32(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = float(root.attrib.get("branch-rate", "0") or "0")
    branches_valid = int(root.attrib.get("0") or "0")
    return branch_rate <= 0.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_33(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = float(root.attrib.get("branch-rate", "0") or "0")
    branches_valid = int(root.attrib.get("branches-valid", ) or "0")
    return branch_rate <= 0.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_34(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = float(root.attrib.get("branch-rate", "0") or "0")
    branches_valid = int(root.attrib.get("XXbranches-validXX", "0") or "0")
    return branch_rate <= 0.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_35(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = float(root.attrib.get("branch-rate", "0") or "0")
    branches_valid = int(root.attrib.get("BRANCHES-VALID", "0") or "0")
    return branch_rate <= 0.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_36(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = float(root.attrib.get("branch-rate", "0") or "0")
    branches_valid = int(root.attrib.get("branches-valid", "XX0XX") or "0")
    return branch_rate <= 0.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_37(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = float(root.attrib.get("branch-rate", "0") or "0")
    branches_valid = int(root.attrib.get("branches-valid", "0") or "XX0XX")
    return branch_rate <= 0.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_38(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = float(root.attrib.get("branch-rate", "0") or "0")
    branches_valid = int(root.attrib.get("branches-valid", "0") or "0")
    return branch_rate <= 0.0 and branches_valid <= 0


def x_report_lacks_branches__mutmut_39(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = float(root.attrib.get("branch-rate", "0") or "0")
    branches_valid = int(root.attrib.get("branches-valid", "0") or "0")
    return branch_rate < 0.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_40(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = float(root.attrib.get("branch-rate", "0") or "0")
    branches_valid = int(root.attrib.get("branches-valid", "0") or "0")
    return branch_rate <= 1.0 or branches_valid <= 0


def x_report_lacks_branches__mutmut_41(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = float(root.attrib.get("branch-rate", "0") or "0")
    branches_valid = int(root.attrib.get("branches-valid", "0") or "0")
    return branch_rate <= 0.0 or branches_valid < 0


def x_report_lacks_branches__mutmut_42(report_path: Path, *, element_tree: Any | None = None) -> bool:
    """True iff the coverage report exists but records no branch coverage.

    Reads the root ``<coverage>`` element's ``branch-rate`` and
    ``branches-valid`` attributes: a real branch-aware report carries both > 0.
    A missing report returns ``True``: absent evidence cannot satisfy branch
    assurance. A malformed/unsafe report raises rather than silently passing.
    """
    if not report_path.exists():
        return True
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()
    branch_rate = float(root.attrib.get("branch-rate", "0") or "0")
    branches_valid = int(root.attrib.get("branches-valid", "0") or "0")
    return branch_rate <= 0.0 or branches_valid <= 1

mutants_x_report_lacks_branches__mutmut['_mutmut_orig'] = x_report_lacks_branches__mutmut_orig # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_1'] = x_report_lacks_branches__mutmut_1 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_2'] = x_report_lacks_branches__mutmut_2 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_3'] = x_report_lacks_branches__mutmut_3 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_4'] = x_report_lacks_branches__mutmut_4 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_5'] = x_report_lacks_branches__mutmut_5 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_6'] = x_report_lacks_branches__mutmut_6 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_7'] = x_report_lacks_branches__mutmut_7 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_8'] = x_report_lacks_branches__mutmut_8 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_9'] = x_report_lacks_branches__mutmut_9 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_10'] = x_report_lacks_branches__mutmut_10 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_11'] = x_report_lacks_branches__mutmut_11 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_12'] = x_report_lacks_branches__mutmut_12 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_13'] = x_report_lacks_branches__mutmut_13 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_14'] = x_report_lacks_branches__mutmut_14 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_15'] = x_report_lacks_branches__mutmut_15 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_16'] = x_report_lacks_branches__mutmut_16 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_17'] = x_report_lacks_branches__mutmut_17 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_18'] = x_report_lacks_branches__mutmut_18 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_19'] = x_report_lacks_branches__mutmut_19 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_20'] = x_report_lacks_branches__mutmut_20 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_21'] = x_report_lacks_branches__mutmut_21 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_22'] = x_report_lacks_branches__mutmut_22 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_23'] = x_report_lacks_branches__mutmut_23 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_24'] = x_report_lacks_branches__mutmut_24 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_25'] = x_report_lacks_branches__mutmut_25 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_26'] = x_report_lacks_branches__mutmut_26 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_27'] = x_report_lacks_branches__mutmut_27 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_28'] = x_report_lacks_branches__mutmut_28 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_29'] = x_report_lacks_branches__mutmut_29 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_30'] = x_report_lacks_branches__mutmut_30 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_31'] = x_report_lacks_branches__mutmut_31 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_32'] = x_report_lacks_branches__mutmut_32 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_33'] = x_report_lacks_branches__mutmut_33 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_34'] = x_report_lacks_branches__mutmut_34 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_35'] = x_report_lacks_branches__mutmut_35 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_36'] = x_report_lacks_branches__mutmut_36 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_37'] = x_report_lacks_branches__mutmut_37 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_38'] = x_report_lacks_branches__mutmut_38 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_39'] = x_report_lacks_branches__mutmut_39 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_40'] = x_report_lacks_branches__mutmut_40 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_41'] = x_report_lacks_branches__mutmut_41 # type: ignore # mutmut generated
mutants_x_report_lacks_branches__mutmut['x_report_lacks_branches__mutmut_42'] = x_report_lacks_branches__mutmut_42 # type: ignore # mutmut generated
mutants_xǁCoverageIncludesBranchesǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCoverageIncludesBranchesǁ_report_path__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCoverageIncludesBranchesǁis_in_scope__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCoverageIncludesBranchesǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore


class CoverageIncludesBranches(FitnessRule):
    """Flags a coverage report that measures lines only, not branches."""

    name = "coverage-includes-branches"
    remediation = REMEDIATION
    extensions = (".xml",)

    #: Rule-specific knob — instance attr so ``from_config`` overrides it.
    coverage_report: str = DEFAULT_COVERAGE_REPORT

    @classmethod
    @_mutmut_mutated(mutants_xǁCoverageIncludesBranchesǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageIncludesBranches:
        """Build from config, also reading ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageIncludesBranches)  # noqa: S101  # narrowing for mypy
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        return rule

    @classmethod
    def xǁCoverageIncludesBranchesǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageIncludesBranches:
        """Build from config, also reading ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageIncludesBranches)  # noqa: S101  # narrowing for mypy
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        return rule

    @classmethod
    def xǁCoverageIncludesBranchesǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageIncludesBranches:
        """Build from config, also reading ``coverage_report``."""
        rule = None
        assert isinstance(rule, CoverageIncludesBranches)  # noqa: S101  # narrowing for mypy
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        return rule

    @classmethod
    def xǁCoverageIncludesBranchesǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageIncludesBranches:
        """Build from config, also reading ``coverage_report``."""
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, CoverageIncludesBranches)  # noqa: S101  # narrowing for mypy
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        return rule

    @classmethod
    def xǁCoverageIncludesBranchesǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageIncludesBranches:
        """Build from config, also reading ``coverage_report``."""
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, CoverageIncludesBranches)  # noqa: S101  # narrowing for mypy
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        return rule

    @classmethod
    def xǁCoverageIncludesBranchesǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageIncludesBranches:
        """Build from config, also reading ``coverage_report``."""
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, CoverageIncludesBranches)  # noqa: S101  # narrowing for mypy
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        return rule

    @classmethod
    def xǁCoverageIncludesBranchesǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageIncludesBranches:
        """Build from config, also reading ``coverage_report``."""
        rule = super().from_config(config, )
        assert isinstance(rule, CoverageIncludesBranches)  # noqa: S101  # narrowing for mypy
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        return rule

    @classmethod
    def xǁCoverageIncludesBranchesǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageIncludesBranches:
        """Build from config, also reading ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageIncludesBranches)  # noqa: S101  # narrowing for mypy
        rule.coverage_report = None
        return rule

    @classmethod
    def xǁCoverageIncludesBranchesǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageIncludesBranches:
        """Build from config, also reading ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageIncludesBranches)  # noqa: S101  # narrowing for mypy
        rule.coverage_report = str(None)
        return rule

    @classmethod
    def xǁCoverageIncludesBranchesǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageIncludesBranches:
        """Build from config, also reading ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageIncludesBranches)  # noqa: S101  # narrowing for mypy
        rule.coverage_report = str(config.get(None, DEFAULT_COVERAGE_REPORT))
        return rule

    @classmethod
    def xǁCoverageIncludesBranchesǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageIncludesBranches:
        """Build from config, also reading ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageIncludesBranches)  # noqa: S101  # narrowing for mypy
        rule.coverage_report = str(config.get("coverage_report", None))
        return rule

    @classmethod
    def xǁCoverageIncludesBranchesǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageIncludesBranches:
        """Build from config, also reading ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageIncludesBranches)  # noqa: S101  # narrowing for mypy
        rule.coverage_report = str(config.get(DEFAULT_COVERAGE_REPORT))
        return rule

    @classmethod
    def xǁCoverageIncludesBranchesǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageIncludesBranches:
        """Build from config, also reading ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageIncludesBranches)  # noqa: S101  # narrowing for mypy
        rule.coverage_report = str(config.get("coverage_report", ))
        return rule

    @classmethod
    def xǁCoverageIncludesBranchesǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageIncludesBranches:
        """Build from config, also reading ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageIncludesBranches)  # noqa: S101  # narrowing for mypy
        rule.coverage_report = str(config.get("XXcoverage_reportXX", DEFAULT_COVERAGE_REPORT))
        return rule

    @classmethod
    def xǁCoverageIncludesBranchesǁfrom_config__mutmut_13(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CoverageIncludesBranches:
        """Build from config, also reading ``coverage_report``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CoverageIncludesBranches)  # noqa: S101  # narrowing for mypy
        rule.coverage_report = str(config.get("COVERAGE_REPORT", DEFAULT_COVERAGE_REPORT))
        return rule

    @_mutmut_mutated(mutants_xǁCoverageIncludesBranchesǁ_report_path__mutmut)
    def _report_path(self) -> Path:
        if self.coverage_report.startswith("env:"):
            from tc_fitness.coverage_admission import configured

            report = Path(configured(self.coverage_report))
        else:
            report = Path(self.coverage_report)
        return report if report.is_absolute() else self._repo_root / report

    def xǁCoverageIncludesBranchesǁ_report_path__mutmut_orig(self) -> Path:
        if self.coverage_report.startswith("env:"):
            from tc_fitness.coverage_admission import configured

            report = Path(configured(self.coverage_report))
        else:
            report = Path(self.coverage_report)
        return report if report.is_absolute() else self._repo_root / report

    def xǁCoverageIncludesBranchesǁ_report_path__mutmut_1(self) -> Path:
        if self.coverage_report.startswith(None):
            from tc_fitness.coverage_admission import configured

            report = Path(configured(self.coverage_report))
        else:
            report = Path(self.coverage_report)
        return report if report.is_absolute() else self._repo_root / report

    def xǁCoverageIncludesBranchesǁ_report_path__mutmut_2(self) -> Path:
        if self.coverage_report.startswith("XXenv:XX"):
            from tc_fitness.coverage_admission import configured

            report = Path(configured(self.coverage_report))
        else:
            report = Path(self.coverage_report)
        return report if report.is_absolute() else self._repo_root / report

    def xǁCoverageIncludesBranchesǁ_report_path__mutmut_3(self) -> Path:
        if self.coverage_report.startswith("ENV:"):
            from tc_fitness.coverage_admission import configured

            report = Path(configured(self.coverage_report))
        else:
            report = Path(self.coverage_report)
        return report if report.is_absolute() else self._repo_root / report

    def xǁCoverageIncludesBranchesǁ_report_path__mutmut_4(self) -> Path:
        if self.coverage_report.startswith("env:"):
            from tc_fitness.coverage_admission import configured

            report = None
        else:
            report = Path(self.coverage_report)
        return report if report.is_absolute() else self._repo_root / report

    def xǁCoverageIncludesBranchesǁ_report_path__mutmut_5(self) -> Path:
        if self.coverage_report.startswith("env:"):
            from tc_fitness.coverage_admission import configured

            report = Path(None)
        else:
            report = Path(self.coverage_report)
        return report if report.is_absolute() else self._repo_root / report

    def xǁCoverageIncludesBranchesǁ_report_path__mutmut_6(self) -> Path:
        if self.coverage_report.startswith("env:"):
            from tc_fitness.coverage_admission import configured

            report = Path(configured(None))
        else:
            report = Path(self.coverage_report)
        return report if report.is_absolute() else self._repo_root / report

    def xǁCoverageIncludesBranchesǁ_report_path__mutmut_7(self) -> Path:
        if self.coverage_report.startswith("env:"):
            from tc_fitness.coverage_admission import configured

            report = Path(configured(self.coverage_report))
        else:
            report = None
        return report if report.is_absolute() else self._repo_root / report

    def xǁCoverageIncludesBranchesǁ_report_path__mutmut_8(self) -> Path:
        if self.coverage_report.startswith("env:"):
            from tc_fitness.coverage_admission import configured

            report = Path(configured(self.coverage_report))
        else:
            report = Path(None)
        return report if report.is_absolute() else self._repo_root / report

    def xǁCoverageIncludesBranchesǁ_report_path__mutmut_9(self) -> Path:
        if self.coverage_report.startswith("env:"):
            from tc_fitness.coverage_admission import configured

            report = Path(configured(self.coverage_report))
        else:
            report = Path(self.coverage_report)
        return report if report.is_absolute() else self._repo_root * report

    def enumerate_files(self) -> list[Path]:
        """The single artifact this rule judges: the coverage report itself."""
        return [self._report_path()]

    @_mutmut_mutated(mutants_xǁCoverageIncludesBranchesǁis_in_scope__mutmut)
    def is_in_scope(self, rel: str) -> bool:
        """Admit the configured report regardless of where it sits."""
        return True

    def xǁCoverageIncludesBranchesǁis_in_scope__mutmut_orig(self, rel: str) -> bool:
        """Admit the configured report regardless of where it sits."""
        return True

    def xǁCoverageIncludesBranchesǁis_in_scope__mutmut_1(self, rel: str) -> bool:
        """Admit the configured report regardless of where it sits."""
        return False

    @_mutmut_mutated(mutants_xǁCoverageIncludesBranchesǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        return report_lacks_branches(path)

    def xǁCoverageIncludesBranchesǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        return report_lacks_branches(path)

    def xǁCoverageIncludesBranchesǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        return report_lacks_branches(None)

mutants_xǁCoverageIncludesBranchesǁfrom_config__mutmut['_mutmut_orig'] = CoverageIncludesBranches.xǁCoverageIncludesBranchesǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCoverageIncludesBranchesǁfrom_config__mutmut['xǁCoverageIncludesBranchesǁfrom_config__mutmut_1'] = CoverageIncludesBranches.xǁCoverageIncludesBranchesǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCoverageIncludesBranchesǁfrom_config__mutmut['xǁCoverageIncludesBranchesǁfrom_config__mutmut_2'] = CoverageIncludesBranches.xǁCoverageIncludesBranchesǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCoverageIncludesBranchesǁfrom_config__mutmut['xǁCoverageIncludesBranchesǁfrom_config__mutmut_3'] = CoverageIncludesBranches.xǁCoverageIncludesBranchesǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCoverageIncludesBranchesǁfrom_config__mutmut['xǁCoverageIncludesBranchesǁfrom_config__mutmut_4'] = CoverageIncludesBranches.xǁCoverageIncludesBranchesǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCoverageIncludesBranchesǁfrom_config__mutmut['xǁCoverageIncludesBranchesǁfrom_config__mutmut_5'] = CoverageIncludesBranches.xǁCoverageIncludesBranchesǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCoverageIncludesBranchesǁfrom_config__mutmut['xǁCoverageIncludesBranchesǁfrom_config__mutmut_6'] = CoverageIncludesBranches.xǁCoverageIncludesBranchesǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCoverageIncludesBranchesǁfrom_config__mutmut['xǁCoverageIncludesBranchesǁfrom_config__mutmut_7'] = CoverageIncludesBranches.xǁCoverageIncludesBranchesǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁCoverageIncludesBranchesǁfrom_config__mutmut['xǁCoverageIncludesBranchesǁfrom_config__mutmut_8'] = CoverageIncludesBranches.xǁCoverageIncludesBranchesǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁCoverageIncludesBranchesǁfrom_config__mutmut['xǁCoverageIncludesBranchesǁfrom_config__mutmut_9'] = CoverageIncludesBranches.xǁCoverageIncludesBranchesǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁCoverageIncludesBranchesǁfrom_config__mutmut['xǁCoverageIncludesBranchesǁfrom_config__mutmut_10'] = CoverageIncludesBranches.xǁCoverageIncludesBranchesǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁCoverageIncludesBranchesǁfrom_config__mutmut['xǁCoverageIncludesBranchesǁfrom_config__mutmut_11'] = CoverageIncludesBranches.xǁCoverageIncludesBranchesǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁCoverageIncludesBranchesǁfrom_config__mutmut['xǁCoverageIncludesBranchesǁfrom_config__mutmut_12'] = CoverageIncludesBranches.xǁCoverageIncludesBranchesǁfrom_config__mutmut_12 # type: ignore # mutmut generated
mutants_xǁCoverageIncludesBranchesǁfrom_config__mutmut['xǁCoverageIncludesBranchesǁfrom_config__mutmut_13'] = CoverageIncludesBranches.xǁCoverageIncludesBranchesǁfrom_config__mutmut_13 # type: ignore # mutmut generated

mutants_xǁCoverageIncludesBranchesǁ_report_path__mutmut['_mutmut_orig'] = CoverageIncludesBranches.xǁCoverageIncludesBranchesǁ_report_path__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCoverageIncludesBranchesǁ_report_path__mutmut['xǁCoverageIncludesBranchesǁ_report_path__mutmut_1'] = CoverageIncludesBranches.xǁCoverageIncludesBranchesǁ_report_path__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCoverageIncludesBranchesǁ_report_path__mutmut['xǁCoverageIncludesBranchesǁ_report_path__mutmut_2'] = CoverageIncludesBranches.xǁCoverageIncludesBranchesǁ_report_path__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCoverageIncludesBranchesǁ_report_path__mutmut['xǁCoverageIncludesBranchesǁ_report_path__mutmut_3'] = CoverageIncludesBranches.xǁCoverageIncludesBranchesǁ_report_path__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCoverageIncludesBranchesǁ_report_path__mutmut['xǁCoverageIncludesBranchesǁ_report_path__mutmut_4'] = CoverageIncludesBranches.xǁCoverageIncludesBranchesǁ_report_path__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCoverageIncludesBranchesǁ_report_path__mutmut['xǁCoverageIncludesBranchesǁ_report_path__mutmut_5'] = CoverageIncludesBranches.xǁCoverageIncludesBranchesǁ_report_path__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCoverageIncludesBranchesǁ_report_path__mutmut['xǁCoverageIncludesBranchesǁ_report_path__mutmut_6'] = CoverageIncludesBranches.xǁCoverageIncludesBranchesǁ_report_path__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCoverageIncludesBranchesǁ_report_path__mutmut['xǁCoverageIncludesBranchesǁ_report_path__mutmut_7'] = CoverageIncludesBranches.xǁCoverageIncludesBranchesǁ_report_path__mutmut_7 # type: ignore # mutmut generated
mutants_xǁCoverageIncludesBranchesǁ_report_path__mutmut['xǁCoverageIncludesBranchesǁ_report_path__mutmut_8'] = CoverageIncludesBranches.xǁCoverageIncludesBranchesǁ_report_path__mutmut_8 # type: ignore # mutmut generated
mutants_xǁCoverageIncludesBranchesǁ_report_path__mutmut['xǁCoverageIncludesBranchesǁ_report_path__mutmut_9'] = CoverageIncludesBranches.xǁCoverageIncludesBranchesǁ_report_path__mutmut_9 # type: ignore # mutmut generated

mutants_xǁCoverageIncludesBranchesǁis_in_scope__mutmut['_mutmut_orig'] = CoverageIncludesBranches.xǁCoverageIncludesBranchesǁis_in_scope__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCoverageIncludesBranchesǁis_in_scope__mutmut['xǁCoverageIncludesBranchesǁis_in_scope__mutmut_1'] = CoverageIncludesBranches.xǁCoverageIncludesBranchesǁis_in_scope__mutmut_1 # type: ignore # mutmut generated

mutants_xǁCoverageIncludesBranchesǁfile_has_violation__mutmut['_mutmut_orig'] = CoverageIncludesBranches.xǁCoverageIncludesBranchesǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCoverageIncludesBranchesǁfile_has_violation__mutmut['xǁCoverageIncludesBranchesǁfile_has_violation__mutmut_1'] = CoverageIncludesBranches.xǁCoverageIncludesBranchesǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> CoverageIncludesBranches:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CoverageIncludesBranches.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> CoverageIncludesBranches:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CoverageIncludesBranches.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> CoverageIncludesBranches:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CoverageIncludesBranches.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> CoverageIncludesBranches:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CoverageIncludesBranches.from_config(config, repo_root=None)


def x_build__mutmut_3(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> CoverageIncludesBranches:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CoverageIncludesBranches.from_config(repo_root=repo_root)


def x_build__mutmut_4(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> CoverageIncludesBranches:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CoverageIncludesBranches.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(CoverageIncludesBranches, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(CoverageIncludesBranches, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(CoverageIncludesBranches, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(CoverageIncludesBranches, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
