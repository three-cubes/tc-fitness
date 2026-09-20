"""CORE check: harness_canon_reference — the agent harness references ONE canon.

Every repo in the fleet MUST route its agents through a single central
engineering-standards canon, not a private fork. When a repo's agent harness
(its ``CLAUDE.md`` / ``AGENTS.md`` entrypoints and the sibling resolver/ethos
docs) stops pointing at the shared standards index, agents in that repo silently
converge on a drifted rule set — the exact failure this rule exists to catch.

The rule FAILS a repo whose harness has drifted from the shared canon on any of
three arms:

* **Presence** — a required harness entrypoint is missing at the repo root. A
  ``repo_type: product`` repo MUST carry the full harness set; a
  ``repo_type: core`` framework repo MUST carry only ``AGENTS.md``; an explicit
  ``required_files`` list overrides both with an "at least one present" contract.
* **Reference** — no harness file carries BOTH the canonical-standards marker AND
  a link matching the central standards index. This is what "references ONE
  canon" means operationally: some entrypoint MUST name the shared index.
* **Drift** (opt-in) — when ``banner_path`` names a pinned canonical banner, the
  banner inlined in the harness MUST match that pin (normalised compare). Leaving
  ``banner_path`` unset skips this arm, so a repo adopts presence + reference
  first and turns on drift enforcement once its banner is pinned.

This is a hard repo-level gate, so :meth:`run` drives the three proof arms
directly.

Repo-agnostic: every knob (the required set, the marker string, the reference
regex, the pinned-banner path) arrives through the consumer's
``[tool.tc_fitness.core_checks.harness_canon_reference]`` config block. The
engine bakes in no repo identity — only the shape every fleet harness shares.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path
from typing import Any

from tc_fitness.check_evidence import report_finding
from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: The full harness set a product repo must carry, and the universe of
#: entrypoints the reference/drift arms read. Domain-intrinsic shape (the files
#: every fleet harness shares), overridable via config.
STANDARD_HARNESS_FILES: tuple[str, ...] = (
    "CLAUDE.md",
    "AGENTS.md",
    "RESOLVER.md",
    "ETHOS.md",
    "SCORECARD.md",
    "CONTRIBUTING.md",
)

#: A framework/core repo (the gate engine, the CI templates) carries only the
#: runtime-neutral ``AGENTS.md`` entrypoint — no product-facing resolver/ethos.
CORE_REQUIRED_FILES: tuple[str, ...] = ("AGENTS.md",)

#: The "at least one present" fallback entrypoint set (used for an explicit
#: ``required_files`` default and any unrecognised ``repo_type``).
DEFAULT_REQUIRED_FILES: tuple[str, ...] = ("CLAUDE.md", "AGENTS.md")

#: The default ``repo_type`` — a full product harness unless a consumer relaxes.
DEFAULT_REPO_TYPE = "product"

#: The marker string a harness file must carry to count as naming the canon.
DEFAULT_BANNER_MARKER = "Canonical standards"

#: The regex a harness file must match to count as linking the central index.
DEFAULT_STANDARDS_REF_PATTERN = r"governance/STANDARDS"

REMEDIATION = _remediation(
    fix=(
        "point the agent harness at the shared engineering-standards canon: add "
        "the missing entrypoint file(s) at the repo root; ensure a harness file "
        "carries the canonical-standards marker AND a link to the central "
        "standards index; and, when a pinned banner is configured, re-inline the "
        "current pinned banner so it stops drifting. Do NOT fork a private "
        "standard — converge up to the one central canon."
    ),
    nxt="re-run this check to confirm the harness references the shared canon.",
    run="python -m tc_fitness.core_checks.harness_canon_reference",
    passing="CLAUDE.md → '## Canonical standards … see governance/STANDARDS.md'",
    forbidden="CLAUDE.md → (no canon marker, or a link to a repo-local fork)",
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x_missing_required_groups__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_missing_required_groups__mutmut)
def missing_required_groups(repo_root: Path, groups: Sequence[frozenset[str]]) -> list[str]:
    """Return a label per requirement group NOT satisfied at ``repo_root``.

    Each group is an "at least one of" set: it is satisfied when any member file
    exists at the repo root. A singleton group therefore expresses an
    all-of-these requirement, and a multi-member group an any-of-these one. The
    returned labels name the unsatisfied groups for the failure report.
    """
    unmet: list[str] = []
    for group in groups:
        if not any((repo_root / name).is_file() for name in group):
            unmet.append(" or ".join(sorted(group)))
    return unmet


def x_missing_required_groups__mutmut_orig(repo_root: Path, groups: Sequence[frozenset[str]]) -> list[str]:
    """Return a label per requirement group NOT satisfied at ``repo_root``.

    Each group is an "at least one of" set: it is satisfied when any member file
    exists at the repo root. A singleton group therefore expresses an
    all-of-these requirement, and a multi-member group an any-of-these one. The
    returned labels name the unsatisfied groups for the failure report.
    """
    unmet: list[str] = []
    for group in groups:
        if not any((repo_root / name).is_file() for name in group):
            unmet.append(" or ".join(sorted(group)))
    return unmet


def x_missing_required_groups__mutmut_1(repo_root: Path, groups: Sequence[frozenset[str]]) -> list[str]:
    """Return a label per requirement group NOT satisfied at ``repo_root``.

    Each group is an "at least one of" set: it is satisfied when any member file
    exists at the repo root. A singleton group therefore expresses an
    all-of-these requirement, and a multi-member group an any-of-these one. The
    returned labels name the unsatisfied groups for the failure report.
    """
    unmet: list[str] = None
    for group in groups:
        if not any((repo_root / name).is_file() for name in group):
            unmet.append(" or ".join(sorted(group)))
    return unmet


def x_missing_required_groups__mutmut_2(repo_root: Path, groups: Sequence[frozenset[str]]) -> list[str]:
    """Return a label per requirement group NOT satisfied at ``repo_root``.

    Each group is an "at least one of" set: it is satisfied when any member file
    exists at the repo root. A singleton group therefore expresses an
    all-of-these requirement, and a multi-member group an any-of-these one. The
    returned labels name the unsatisfied groups for the failure report.
    """
    unmet: list[str] = []
    for group in groups:
        if any((repo_root / name).is_file() for name in group):
            unmet.append(" or ".join(sorted(group)))
    return unmet


def x_missing_required_groups__mutmut_3(repo_root: Path, groups: Sequence[frozenset[str]]) -> list[str]:
    """Return a label per requirement group NOT satisfied at ``repo_root``.

    Each group is an "at least one of" set: it is satisfied when any member file
    exists at the repo root. A singleton group therefore expresses an
    all-of-these requirement, and a multi-member group an any-of-these one. The
    returned labels name the unsatisfied groups for the failure report.
    """
    unmet: list[str] = []
    for group in groups:
        if not any(None):
            unmet.append(" or ".join(sorted(group)))
    return unmet


def x_missing_required_groups__mutmut_4(repo_root: Path, groups: Sequence[frozenset[str]]) -> list[str]:
    """Return a label per requirement group NOT satisfied at ``repo_root``.

    Each group is an "at least one of" set: it is satisfied when any member file
    exists at the repo root. A singleton group therefore expresses an
    all-of-these requirement, and a multi-member group an any-of-these one. The
    returned labels name the unsatisfied groups for the failure report.
    """
    unmet: list[str] = []
    for group in groups:
        if not any((repo_root * name).is_file() for name in group):
            unmet.append(" or ".join(sorted(group)))
    return unmet


def x_missing_required_groups__mutmut_5(repo_root: Path, groups: Sequence[frozenset[str]]) -> list[str]:
    """Return a label per requirement group NOT satisfied at ``repo_root``.

    Each group is an "at least one of" set: it is satisfied when any member file
    exists at the repo root. A singleton group therefore expresses an
    all-of-these requirement, and a multi-member group an any-of-these one. The
    returned labels name the unsatisfied groups for the failure report.
    """
    unmet: list[str] = []
    for group in groups:
        if not any((repo_root / name).is_file() for name in group):
            unmet.append(None)
    return unmet


def x_missing_required_groups__mutmut_6(repo_root: Path, groups: Sequence[frozenset[str]]) -> list[str]:
    """Return a label per requirement group NOT satisfied at ``repo_root``.

    Each group is an "at least one of" set: it is satisfied when any member file
    exists at the repo root. A singleton group therefore expresses an
    all-of-these requirement, and a multi-member group an any-of-these one. The
    returned labels name the unsatisfied groups for the failure report.
    """
    unmet: list[str] = []
    for group in groups:
        if not any((repo_root / name).is_file() for name in group):
            unmet.append(" or ".join(None))
    return unmet


def x_missing_required_groups__mutmut_7(repo_root: Path, groups: Sequence[frozenset[str]]) -> list[str]:
    """Return a label per requirement group NOT satisfied at ``repo_root``.

    Each group is an "at least one of" set: it is satisfied when any member file
    exists at the repo root. A singleton group therefore expresses an
    all-of-these requirement, and a multi-member group an any-of-these one. The
    returned labels name the unsatisfied groups for the failure report.
    """
    unmet: list[str] = []
    for group in groups:
        if not any((repo_root / name).is_file() for name in group):
            unmet.append("XX or XX".join(sorted(group)))
    return unmet


def x_missing_required_groups__mutmut_8(repo_root: Path, groups: Sequence[frozenset[str]]) -> list[str]:
    """Return a label per requirement group NOT satisfied at ``repo_root``.

    Each group is an "at least one of" set: it is satisfied when any member file
    exists at the repo root. A singleton group therefore expresses an
    all-of-these requirement, and a multi-member group an any-of-these one. The
    returned labels name the unsatisfied groups for the failure report.
    """
    unmet: list[str] = []
    for group in groups:
        if not any((repo_root / name).is_file() for name in group):
            unmet.append(" OR ".join(sorted(group)))
    return unmet


def x_missing_required_groups__mutmut_9(repo_root: Path, groups: Sequence[frozenset[str]]) -> list[str]:
    """Return a label per requirement group NOT satisfied at ``repo_root``.

    Each group is an "at least one of" set: it is satisfied when any member file
    exists at the repo root. A singleton group therefore expresses an
    all-of-these requirement, and a multi-member group an any-of-these one. The
    returned labels name the unsatisfied groups for the failure report.
    """
    unmet: list[str] = []
    for group in groups:
        if not any((repo_root / name).is_file() for name in group):
            unmet.append(" or ".join(sorted(None)))
    return unmet

mutants_x_missing_required_groups__mutmut['_mutmut_orig'] = x_missing_required_groups__mutmut_orig # type: ignore # mutmut generated
mutants_x_missing_required_groups__mutmut['x_missing_required_groups__mutmut_1'] = x_missing_required_groups__mutmut_1 # type: ignore # mutmut generated
mutants_x_missing_required_groups__mutmut['x_missing_required_groups__mutmut_2'] = x_missing_required_groups__mutmut_2 # type: ignore # mutmut generated
mutants_x_missing_required_groups__mutmut['x_missing_required_groups__mutmut_3'] = x_missing_required_groups__mutmut_3 # type: ignore # mutmut generated
mutants_x_missing_required_groups__mutmut['x_missing_required_groups__mutmut_4'] = x_missing_required_groups__mutmut_4 # type: ignore # mutmut generated
mutants_x_missing_required_groups__mutmut['x_missing_required_groups__mutmut_5'] = x_missing_required_groups__mutmut_5 # type: ignore # mutmut generated
mutants_x_missing_required_groups__mutmut['x_missing_required_groups__mutmut_6'] = x_missing_required_groups__mutmut_6 # type: ignore # mutmut generated
mutants_x_missing_required_groups__mutmut['x_missing_required_groups__mutmut_7'] = x_missing_required_groups__mutmut_7 # type: ignore # mutmut generated
mutants_x_missing_required_groups__mutmut['x_missing_required_groups__mutmut_8'] = x_missing_required_groups__mutmut_8 # type: ignore # mutmut generated
mutants_x_missing_required_groups__mutmut['x_missing_required_groups__mutmut_9'] = x_missing_required_groups__mutmut_9 # type: ignore # mutmut generated
mutants_x_has_canon_reference__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_has_canon_reference__mutmut)
def has_canon_reference(texts: Iterable[str], *, marker: str, ref_pattern: re.Pattern[str]) -> bool:
    """True iff some text carries BOTH the canon marker AND a reference match.

    The marker and the reference link must co-occur in the SAME harness file — a
    stray marker in one file and a link in another does not prove that file names
    the canon.
    """
    return any(marker in text and ref_pattern.search(text) is not None for text in texts)


def x_has_canon_reference__mutmut_orig(texts: Iterable[str], *, marker: str, ref_pattern: re.Pattern[str]) -> bool:
    """True iff some text carries BOTH the canon marker AND a reference match.

    The marker and the reference link must co-occur in the SAME harness file — a
    stray marker in one file and a link in another does not prove that file names
    the canon.
    """
    return any(marker in text and ref_pattern.search(text) is not None for text in texts)


def x_has_canon_reference__mutmut_1(texts: Iterable[str], *, marker: str, ref_pattern: re.Pattern[str]) -> bool:
    """True iff some text carries BOTH the canon marker AND a reference match.

    The marker and the reference link must co-occur in the SAME harness file — a
    stray marker in one file and a link in another does not prove that file names
    the canon.
    """
    return any(None)


def x_has_canon_reference__mutmut_2(texts: Iterable[str], *, marker: str, ref_pattern: re.Pattern[str]) -> bool:
    """True iff some text carries BOTH the canon marker AND a reference match.

    The marker and the reference link must co-occur in the SAME harness file — a
    stray marker in one file and a link in another does not prove that file names
    the canon.
    """
    return any(marker in text or ref_pattern.search(text) is not None for text in texts)


def x_has_canon_reference__mutmut_3(texts: Iterable[str], *, marker: str, ref_pattern: re.Pattern[str]) -> bool:
    """True iff some text carries BOTH the canon marker AND a reference match.

    The marker and the reference link must co-occur in the SAME harness file — a
    stray marker in one file and a link in another does not prove that file names
    the canon.
    """
    return any(marker not in text and ref_pattern.search(text) is not None for text in texts)


def x_has_canon_reference__mutmut_4(texts: Iterable[str], *, marker: str, ref_pattern: re.Pattern[str]) -> bool:
    """True iff some text carries BOTH the canon marker AND a reference match.

    The marker and the reference link must co-occur in the SAME harness file — a
    stray marker in one file and a link in another does not prove that file names
    the canon.
    """
    return any(marker in text and ref_pattern.search(None) is not None for text in texts)


def x_has_canon_reference__mutmut_5(texts: Iterable[str], *, marker: str, ref_pattern: re.Pattern[str]) -> bool:
    """True iff some text carries BOTH the canon marker AND a reference match.

    The marker and the reference link must co-occur in the SAME harness file — a
    stray marker in one file and a link in another does not prove that file names
    the canon.
    """
    return any(marker in text and ref_pattern.search(text) is None for text in texts)

mutants_x_has_canon_reference__mutmut['_mutmut_orig'] = x_has_canon_reference__mutmut_orig # type: ignore # mutmut generated
mutants_x_has_canon_reference__mutmut['x_has_canon_reference__mutmut_1'] = x_has_canon_reference__mutmut_1 # type: ignore # mutmut generated
mutants_x_has_canon_reference__mutmut['x_has_canon_reference__mutmut_2'] = x_has_canon_reference__mutmut_2 # type: ignore # mutmut generated
mutants_x_has_canon_reference__mutmut['x_has_canon_reference__mutmut_3'] = x_has_canon_reference__mutmut_3 # type: ignore # mutmut generated
mutants_x_has_canon_reference__mutmut['x_has_canon_reference__mutmut_4'] = x_has_canon_reference__mutmut_4 # type: ignore # mutmut generated
mutants_x_has_canon_reference__mutmut['x_has_canon_reference__mutmut_5'] = x_has_canon_reference__mutmut_5 # type: ignore # mutmut generated
mutants_x_normalise_banner__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_normalise_banner__mutmut)
def normalise_banner(text: str) -> str:
    """Whitespace-normalise a banner block for a content (not layout) compare.

    Strips each line and drops blank lines, so indentation or blank-line reflow
    never reads as drift while a change to the banner's WORDS does.
    """
    return "\n".join(stripped for line in text.splitlines() if (stripped := line.strip()))


def x_normalise_banner__mutmut_orig(text: str) -> str:
    """Whitespace-normalise a banner block for a content (not layout) compare.

    Strips each line and drops blank lines, so indentation or blank-line reflow
    never reads as drift while a change to the banner's WORDS does.
    """
    return "\n".join(stripped for line in text.splitlines() if (stripped := line.strip()))


def x_normalise_banner__mutmut_1(text: str) -> str:
    """Whitespace-normalise a banner block for a content (not layout) compare.

    Strips each line and drops blank lines, so indentation or blank-line reflow
    never reads as drift while a change to the banner's WORDS does.
    """
    return "\n".join(None)


def x_normalise_banner__mutmut_2(text: str) -> str:
    """Whitespace-normalise a banner block for a content (not layout) compare.

    Strips each line and drops blank lines, so indentation or blank-line reflow
    never reads as drift while a change to the banner's WORDS does.
    """
    return "XX\nXX".join(stripped for line in text.splitlines() if (stripped := line.strip()))

mutants_x_normalise_banner__mutmut['_mutmut_orig'] = x_normalise_banner__mutmut_orig # type: ignore # mutmut generated
mutants_x_normalise_banner__mutmut['x_normalise_banner__mutmut_1'] = x_normalise_banner__mutmut_1 # type: ignore # mutmut generated
mutants_x_normalise_banner__mutmut['x_normalise_banner__mutmut_2'] = x_normalise_banner__mutmut_2 # type: ignore # mutmut generated
mutants_x_banner_present__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_banner_present__mutmut)
def banner_present(texts: Iterable[str], pinned: str) -> bool:
    """True iff the normalised pinned banner appears inside some harness text.

    An empty pin has nothing to drift from and is treated as present.
    """
    target = normalise_banner(pinned)
    if not target:
        return True
    return any(target in normalise_banner(text) for text in texts)


def x_banner_present__mutmut_orig(texts: Iterable[str], pinned: str) -> bool:
    """True iff the normalised pinned banner appears inside some harness text.

    An empty pin has nothing to drift from and is treated as present.
    """
    target = normalise_banner(pinned)
    if not target:
        return True
    return any(target in normalise_banner(text) for text in texts)


def x_banner_present__mutmut_1(texts: Iterable[str], pinned: str) -> bool:
    """True iff the normalised pinned banner appears inside some harness text.

    An empty pin has nothing to drift from and is treated as present.
    """
    target = None
    if not target:
        return True
    return any(target in normalise_banner(text) for text in texts)


def x_banner_present__mutmut_2(texts: Iterable[str], pinned: str) -> bool:
    """True iff the normalised pinned banner appears inside some harness text.

    An empty pin has nothing to drift from and is treated as present.
    """
    target = normalise_banner(None)
    if not target:
        return True
    return any(target in normalise_banner(text) for text in texts)


def x_banner_present__mutmut_3(texts: Iterable[str], pinned: str) -> bool:
    """True iff the normalised pinned banner appears inside some harness text.

    An empty pin has nothing to drift from and is treated as present.
    """
    target = normalise_banner(pinned)
    if target:
        return True
    return any(target in normalise_banner(text) for text in texts)


def x_banner_present__mutmut_4(texts: Iterable[str], pinned: str) -> bool:
    """True iff the normalised pinned banner appears inside some harness text.

    An empty pin has nothing to drift from and is treated as present.
    """
    target = normalise_banner(pinned)
    if not target:
        return False
    return any(target in normalise_banner(text) for text in texts)


def x_banner_present__mutmut_5(texts: Iterable[str], pinned: str) -> bool:
    """True iff the normalised pinned banner appears inside some harness text.

    An empty pin has nothing to drift from and is treated as present.
    """
    target = normalise_banner(pinned)
    if not target:
        return True
    return any(None)


def x_banner_present__mutmut_6(texts: Iterable[str], pinned: str) -> bool:
    """True iff the normalised pinned banner appears inside some harness text.

    An empty pin has nothing to drift from and is treated as present.
    """
    target = normalise_banner(pinned)
    if not target:
        return True
    return any(target not in normalise_banner(text) for text in texts)


def x_banner_present__mutmut_7(texts: Iterable[str], pinned: str) -> bool:
    """True iff the normalised pinned banner appears inside some harness text.

    An empty pin has nothing to drift from and is treated as present.
    """
    target = normalise_banner(pinned)
    if not target:
        return True
    return any(target in normalise_banner(None) for text in texts)

mutants_x_banner_present__mutmut['_mutmut_orig'] = x_banner_present__mutmut_orig # type: ignore # mutmut generated
mutants_x_banner_present__mutmut['x_banner_present__mutmut_1'] = x_banner_present__mutmut_1 # type: ignore # mutmut generated
mutants_x_banner_present__mutmut['x_banner_present__mutmut_2'] = x_banner_present__mutmut_2 # type: ignore # mutmut generated
mutants_x_banner_present__mutmut['x_banner_present__mutmut_3'] = x_banner_present__mutmut_3 # type: ignore # mutmut generated
mutants_x_banner_present__mutmut['x_banner_present__mutmut_4'] = x_banner_present__mutmut_4 # type: ignore # mutmut generated
mutants_x_banner_present__mutmut['x_banner_present__mutmut_5'] = x_banner_present__mutmut_5 # type: ignore # mutmut generated
mutants_x_banner_present__mutmut['x_banner_present__mutmut_6'] = x_banner_present__mutmut_6 # type: ignore # mutmut generated
mutants_x_banner_present__mutmut['x_banner_present__mutmut_7'] = x_banner_present__mutmut_7 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁHarnessCanonReferenceǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore
mutants_xǁHarnessCanonReferenceǁ_requirement_groups__mutmut: MutantDict = {}  # type: ignore
mutants_xǁHarnessCanonReferenceǁ_harness_texts__mutmut: MutantDict = {}  # type: ignore
mutants_xǁHarnessCanonReferenceǁ_reference_failure__mutmut: MutantDict = {}  # type: ignore
mutants_xǁHarnessCanonReferenceǁ_drift_failure__mutmut: MutantDict = {}  # type: ignore
mutants_xǁHarnessCanonReferenceǁrun__mutmut: MutantDict = {}  # type: ignore


class HarnessCanonReference(FitnessRule):
    """Gate that FAILS when a repo's agent harness has drifted from the canon.

    Drives three arms (presence, reference, drift) directly in :meth:`run`; the
    per-file scan hooks are inert because harness drift is a repo-level invariant.
    """

    name = "harness-canon-reference"
    remediation = REMEDIATION
    #: Not a file-scan rule — the enumeration hooks stay empty.
    extensions = ()

    #: Rule-specific config (instance attrs; from_config overrides per consumer).
    repo_type: str = DEFAULT_REPO_TYPE
    required_files: tuple[str, ...] | None = None
    banner_marker: str = DEFAULT_BANNER_MARKER
    standards_ref_pattern: str = DEFAULT_STANDARDS_REF_PATTERN
    banner_path: str | None = None

    @classmethod
    @_mutmut_mutated(mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("repo_type", DEFAULT_REPO_TYPE))
        required = config.get("required_files")
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(config.get("banner_marker", DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(config.get("standards_ref_pattern", DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get("banner_path")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("repo_type", DEFAULT_REPO_TYPE))
        required = config.get("required_files")
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(config.get("banner_marker", DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(config.get("standards_ref_pattern", DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get("banner_path")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = None
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("repo_type", DEFAULT_REPO_TYPE))
        required = config.get("required_files")
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(config.get("banner_marker", DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(config.get("standards_ref_pattern", DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get("banner_path")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("repo_type", DEFAULT_REPO_TYPE))
        required = config.get("required_files")
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(config.get("banner_marker", DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(config.get("standards_ref_pattern", DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get("banner_path")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("repo_type", DEFAULT_REPO_TYPE))
        required = config.get("required_files")
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(config.get("banner_marker", DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(config.get("standards_ref_pattern", DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get("banner_path")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("repo_type", DEFAULT_REPO_TYPE))
        required = config.get("required_files")
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(config.get("banner_marker", DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(config.get("standards_ref_pattern", DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get("banner_path")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, )
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("repo_type", DEFAULT_REPO_TYPE))
        required = config.get("required_files")
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(config.get("banner_marker", DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(config.get("standards_ref_pattern", DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get("banner_path")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = None
        required = config.get("required_files")
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(config.get("banner_marker", DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(config.get("standards_ref_pattern", DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get("banner_path")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(None)
        required = config.get("required_files")
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(config.get("banner_marker", DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(config.get("standards_ref_pattern", DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get("banner_path")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get(None, DEFAULT_REPO_TYPE))
        required = config.get("required_files")
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(config.get("banner_marker", DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(config.get("standards_ref_pattern", DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get("banner_path")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("repo_type", None))
        required = config.get("required_files")
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(config.get("banner_marker", DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(config.get("standards_ref_pattern", DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get("banner_path")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get(DEFAULT_REPO_TYPE))
        required = config.get("required_files")
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(config.get("banner_marker", DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(config.get("standards_ref_pattern", DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get("banner_path")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("repo_type", ))
        required = config.get("required_files")
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(config.get("banner_marker", DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(config.get("standards_ref_pattern", DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get("banner_path")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("XXrepo_typeXX", DEFAULT_REPO_TYPE))
        required = config.get("required_files")
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(config.get("banner_marker", DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(config.get("standards_ref_pattern", DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get("banner_path")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_13(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("REPO_TYPE", DEFAULT_REPO_TYPE))
        required = config.get("required_files")
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(config.get("banner_marker", DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(config.get("standards_ref_pattern", DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get("banner_path")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_14(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("repo_type", DEFAULT_REPO_TYPE))
        required = None
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(config.get("banner_marker", DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(config.get("standards_ref_pattern", DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get("banner_path")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_15(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("repo_type", DEFAULT_REPO_TYPE))
        required = config.get(None)
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(config.get("banner_marker", DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(config.get("standards_ref_pattern", DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get("banner_path")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_16(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("repo_type", DEFAULT_REPO_TYPE))
        required = config.get("XXrequired_filesXX")
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(config.get("banner_marker", DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(config.get("standards_ref_pattern", DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get("banner_path")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_17(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("repo_type", DEFAULT_REPO_TYPE))
        required = config.get("REQUIRED_FILES")
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(config.get("banner_marker", DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(config.get("standards_ref_pattern", DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get("banner_path")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_18(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("repo_type", DEFAULT_REPO_TYPE))
        required = config.get("required_files")
        rule.required_files = None
        rule.banner_marker = str(config.get("banner_marker", DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(config.get("standards_ref_pattern", DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get("banner_path")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_19(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("repo_type", DEFAULT_REPO_TYPE))
        required = config.get("required_files")
        rule.required_files = tuple(None) if required is not None else None
        rule.banner_marker = str(config.get("banner_marker", DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(config.get("standards_ref_pattern", DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get("banner_path")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_20(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("repo_type", DEFAULT_REPO_TYPE))
        required = config.get("required_files")
        rule.required_files = tuple(str(None) for f in required) if required is not None else None
        rule.banner_marker = str(config.get("banner_marker", DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(config.get("standards_ref_pattern", DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get("banner_path")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_21(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("repo_type", DEFAULT_REPO_TYPE))
        required = config.get("required_files")
        rule.required_files = tuple(str(f) for f in required) if required is None else None
        rule.banner_marker = str(config.get("banner_marker", DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(config.get("standards_ref_pattern", DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get("banner_path")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_22(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("repo_type", DEFAULT_REPO_TYPE))
        required = config.get("required_files")
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = None
        rule.standards_ref_pattern = str(config.get("standards_ref_pattern", DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get("banner_path")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_23(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("repo_type", DEFAULT_REPO_TYPE))
        required = config.get("required_files")
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(None)
        rule.standards_ref_pattern = str(config.get("standards_ref_pattern", DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get("banner_path")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_24(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("repo_type", DEFAULT_REPO_TYPE))
        required = config.get("required_files")
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(config.get(None, DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(config.get("standards_ref_pattern", DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get("banner_path")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_25(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("repo_type", DEFAULT_REPO_TYPE))
        required = config.get("required_files")
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(config.get("banner_marker", None))
        rule.standards_ref_pattern = str(config.get("standards_ref_pattern", DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get("banner_path")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_26(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("repo_type", DEFAULT_REPO_TYPE))
        required = config.get("required_files")
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(config.get(DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(config.get("standards_ref_pattern", DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get("banner_path")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_27(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("repo_type", DEFAULT_REPO_TYPE))
        required = config.get("required_files")
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(config.get("banner_marker", ))
        rule.standards_ref_pattern = str(config.get("standards_ref_pattern", DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get("banner_path")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_28(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("repo_type", DEFAULT_REPO_TYPE))
        required = config.get("required_files")
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(config.get("XXbanner_markerXX", DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(config.get("standards_ref_pattern", DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get("banner_path")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_29(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("repo_type", DEFAULT_REPO_TYPE))
        required = config.get("required_files")
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(config.get("BANNER_MARKER", DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(config.get("standards_ref_pattern", DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get("banner_path")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_30(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("repo_type", DEFAULT_REPO_TYPE))
        required = config.get("required_files")
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(config.get("banner_marker", DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = None
        banner_path = config.get("banner_path")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_31(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("repo_type", DEFAULT_REPO_TYPE))
        required = config.get("required_files")
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(config.get("banner_marker", DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(None)
        banner_path = config.get("banner_path")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_32(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("repo_type", DEFAULT_REPO_TYPE))
        required = config.get("required_files")
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(config.get("banner_marker", DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(config.get(None, DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get("banner_path")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_33(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("repo_type", DEFAULT_REPO_TYPE))
        required = config.get("required_files")
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(config.get("banner_marker", DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(config.get("standards_ref_pattern", None))
        banner_path = config.get("banner_path")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_34(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("repo_type", DEFAULT_REPO_TYPE))
        required = config.get("required_files")
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(config.get("banner_marker", DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(config.get(DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get("banner_path")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_35(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("repo_type", DEFAULT_REPO_TYPE))
        required = config.get("required_files")
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(config.get("banner_marker", DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(config.get("standards_ref_pattern", ))
        banner_path = config.get("banner_path")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_36(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("repo_type", DEFAULT_REPO_TYPE))
        required = config.get("required_files")
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(config.get("banner_marker", DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(config.get("XXstandards_ref_patternXX", DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get("banner_path")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_37(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("repo_type", DEFAULT_REPO_TYPE))
        required = config.get("required_files")
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(config.get("banner_marker", DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(config.get("STANDARDS_REF_PATTERN", DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get("banner_path")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_38(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("repo_type", DEFAULT_REPO_TYPE))
        required = config.get("required_files")
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(config.get("banner_marker", DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(config.get("standards_ref_pattern", DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = None
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_39(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("repo_type", DEFAULT_REPO_TYPE))
        required = config.get("required_files")
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(config.get("banner_marker", DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(config.get("standards_ref_pattern", DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get(None)
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_40(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("repo_type", DEFAULT_REPO_TYPE))
        required = config.get("required_files")
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(config.get("banner_marker", DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(config.get("standards_ref_pattern", DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get("XXbanner_pathXX")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_41(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("repo_type", DEFAULT_REPO_TYPE))
        required = config.get("required_files")
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(config.get("banner_marker", DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(config.get("standards_ref_pattern", DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get("BANNER_PATH")
        rule.banner_path = str(banner_path) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_42(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("repo_type", DEFAULT_REPO_TYPE))
        required = config.get("required_files")
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(config.get("banner_marker", DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(config.get("standards_ref_pattern", DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get("banner_path")
        rule.banner_path = None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_43(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("repo_type", DEFAULT_REPO_TYPE))
        required = config.get("required_files")
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(config.get("banner_marker", DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(config.get("standards_ref_pattern", DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get("banner_path")
        rule.banner_path = str(None) if banner_path is not None else None
        return rule

    @classmethod
    def xǁHarnessCanonReferenceǁfrom_config__mutmut_44(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> HarnessCanonReference:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, HarnessCanonReference)  # noqa: S101  # narrowing for mypy
        rule.repo_type = str(config.get("repo_type", DEFAULT_REPO_TYPE))
        required = config.get("required_files")
        rule.required_files = tuple(str(f) for f in required) if required is not None else None
        rule.banner_marker = str(config.get("banner_marker", DEFAULT_BANNER_MARKER))
        rule.standards_ref_pattern = str(config.get("standards_ref_pattern", DEFAULT_STANDARDS_REF_PATTERN))
        banner_path = config.get("banner_path")
        rule.banner_path = str(banner_path) if banner_path is None else None
        return rule

    @_mutmut_mutated(mutants_xǁHarnessCanonReferenceǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:  # pragma: no cover - not used
        """Unused: harness drift is a repo-level gate, not a per-file scan."""
        return False

    def xǁHarnessCanonReferenceǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:  # pragma: no cover - not used
        """Unused: harness drift is a repo-level gate, not a per-file scan."""
        return False

    def xǁHarnessCanonReferenceǁfile_has_violation__mutmut_1(self, path: Path) -> bool:  # pragma: no cover - not used
        """Unused: harness drift is a repo-level gate, not a per-file scan."""
        return True

    @_mutmut_mutated(mutants_xǁHarnessCanonReferenceǁ_requirement_groups__mutmut)
    def _requirement_groups(self) -> list[frozenset[str]]:
        """Resolve the presence requirement into "at least one of" groups.

        Precedence: an explicit ``required_files`` (one any-of group) wins; then
        the ``repo_type`` preset (product → the full set as singletons; core →
        ``AGENTS.md`` only); an unrecognised ``repo_type`` falls back to the
        any-of ``DEFAULT_REQUIRED_FILES`` entrypoint set.
        """
        if self.required_files is not None:
            return [frozenset(self.required_files)]
        if self.repo_type == "core":
            return [frozenset({name}) for name in CORE_REQUIRED_FILES]
        if self.repo_type == "product":
            return [frozenset({name}) for name in STANDARD_HARNESS_FILES]
        return [frozenset(DEFAULT_REQUIRED_FILES)]

    def xǁHarnessCanonReferenceǁ_requirement_groups__mutmut_orig(self) -> list[frozenset[str]]:
        """Resolve the presence requirement into "at least one of" groups.

        Precedence: an explicit ``required_files`` (one any-of group) wins; then
        the ``repo_type`` preset (product → the full set as singletons; core →
        ``AGENTS.md`` only); an unrecognised ``repo_type`` falls back to the
        any-of ``DEFAULT_REQUIRED_FILES`` entrypoint set.
        """
        if self.required_files is not None:
            return [frozenset(self.required_files)]
        if self.repo_type == "core":
            return [frozenset({name}) for name in CORE_REQUIRED_FILES]
        if self.repo_type == "product":
            return [frozenset({name}) for name in STANDARD_HARNESS_FILES]
        return [frozenset(DEFAULT_REQUIRED_FILES)]

    def xǁHarnessCanonReferenceǁ_requirement_groups__mutmut_1(self) -> list[frozenset[str]]:
        """Resolve the presence requirement into "at least one of" groups.

        Precedence: an explicit ``required_files`` (one any-of group) wins; then
        the ``repo_type`` preset (product → the full set as singletons; core →
        ``AGENTS.md`` only); an unrecognised ``repo_type`` falls back to the
        any-of ``DEFAULT_REQUIRED_FILES`` entrypoint set.
        """
        if self.required_files is None:
            return [frozenset(self.required_files)]
        if self.repo_type == "core":
            return [frozenset({name}) for name in CORE_REQUIRED_FILES]
        if self.repo_type == "product":
            return [frozenset({name}) for name in STANDARD_HARNESS_FILES]
        return [frozenset(DEFAULT_REQUIRED_FILES)]

    def xǁHarnessCanonReferenceǁ_requirement_groups__mutmut_2(self) -> list[frozenset[str]]:
        """Resolve the presence requirement into "at least one of" groups.

        Precedence: an explicit ``required_files`` (one any-of group) wins; then
        the ``repo_type`` preset (product → the full set as singletons; core →
        ``AGENTS.md`` only); an unrecognised ``repo_type`` falls back to the
        any-of ``DEFAULT_REQUIRED_FILES`` entrypoint set.
        """
        if self.required_files is not None:
            return [frozenset(None)]
        if self.repo_type == "core":
            return [frozenset({name}) for name in CORE_REQUIRED_FILES]
        if self.repo_type == "product":
            return [frozenset({name}) for name in STANDARD_HARNESS_FILES]
        return [frozenset(DEFAULT_REQUIRED_FILES)]

    def xǁHarnessCanonReferenceǁ_requirement_groups__mutmut_3(self) -> list[frozenset[str]]:
        """Resolve the presence requirement into "at least one of" groups.

        Precedence: an explicit ``required_files`` (one any-of group) wins; then
        the ``repo_type`` preset (product → the full set as singletons; core →
        ``AGENTS.md`` only); an unrecognised ``repo_type`` falls back to the
        any-of ``DEFAULT_REQUIRED_FILES`` entrypoint set.
        """
        if self.required_files is not None:
            return [frozenset(self.required_files)]
        if self.repo_type != "core":
            return [frozenset({name}) for name in CORE_REQUIRED_FILES]
        if self.repo_type == "product":
            return [frozenset({name}) for name in STANDARD_HARNESS_FILES]
        return [frozenset(DEFAULT_REQUIRED_FILES)]

    def xǁHarnessCanonReferenceǁ_requirement_groups__mutmut_4(self) -> list[frozenset[str]]:
        """Resolve the presence requirement into "at least one of" groups.

        Precedence: an explicit ``required_files`` (one any-of group) wins; then
        the ``repo_type`` preset (product → the full set as singletons; core →
        ``AGENTS.md`` only); an unrecognised ``repo_type`` falls back to the
        any-of ``DEFAULT_REQUIRED_FILES`` entrypoint set.
        """
        if self.required_files is not None:
            return [frozenset(self.required_files)]
        if self.repo_type == "XXcoreXX":
            return [frozenset({name}) for name in CORE_REQUIRED_FILES]
        if self.repo_type == "product":
            return [frozenset({name}) for name in STANDARD_HARNESS_FILES]
        return [frozenset(DEFAULT_REQUIRED_FILES)]

    def xǁHarnessCanonReferenceǁ_requirement_groups__mutmut_5(self) -> list[frozenset[str]]:
        """Resolve the presence requirement into "at least one of" groups.

        Precedence: an explicit ``required_files`` (one any-of group) wins; then
        the ``repo_type`` preset (product → the full set as singletons; core →
        ``AGENTS.md`` only); an unrecognised ``repo_type`` falls back to the
        any-of ``DEFAULT_REQUIRED_FILES`` entrypoint set.
        """
        if self.required_files is not None:
            return [frozenset(self.required_files)]
        if self.repo_type == "CORE":
            return [frozenset({name}) for name in CORE_REQUIRED_FILES]
        if self.repo_type == "product":
            return [frozenset({name}) for name in STANDARD_HARNESS_FILES]
        return [frozenset(DEFAULT_REQUIRED_FILES)]

    def xǁHarnessCanonReferenceǁ_requirement_groups__mutmut_6(self) -> list[frozenset[str]]:
        """Resolve the presence requirement into "at least one of" groups.

        Precedence: an explicit ``required_files`` (one any-of group) wins; then
        the ``repo_type`` preset (product → the full set as singletons; core →
        ``AGENTS.md`` only); an unrecognised ``repo_type`` falls back to the
        any-of ``DEFAULT_REQUIRED_FILES`` entrypoint set.
        """
        if self.required_files is not None:
            return [frozenset(self.required_files)]
        if self.repo_type == "core":
            return [frozenset(None) for name in CORE_REQUIRED_FILES]
        if self.repo_type == "product":
            return [frozenset({name}) for name in STANDARD_HARNESS_FILES]
        return [frozenset(DEFAULT_REQUIRED_FILES)]

    def xǁHarnessCanonReferenceǁ_requirement_groups__mutmut_7(self) -> list[frozenset[str]]:
        """Resolve the presence requirement into "at least one of" groups.

        Precedence: an explicit ``required_files`` (one any-of group) wins; then
        the ``repo_type`` preset (product → the full set as singletons; core →
        ``AGENTS.md`` only); an unrecognised ``repo_type`` falls back to the
        any-of ``DEFAULT_REQUIRED_FILES`` entrypoint set.
        """
        if self.required_files is not None:
            return [frozenset(self.required_files)]
        if self.repo_type == "core":
            return [frozenset({name}) for name in CORE_REQUIRED_FILES]
        if self.repo_type != "product":
            return [frozenset({name}) for name in STANDARD_HARNESS_FILES]
        return [frozenset(DEFAULT_REQUIRED_FILES)]

    def xǁHarnessCanonReferenceǁ_requirement_groups__mutmut_8(self) -> list[frozenset[str]]:
        """Resolve the presence requirement into "at least one of" groups.

        Precedence: an explicit ``required_files`` (one any-of group) wins; then
        the ``repo_type`` preset (product → the full set as singletons; core →
        ``AGENTS.md`` only); an unrecognised ``repo_type`` falls back to the
        any-of ``DEFAULT_REQUIRED_FILES`` entrypoint set.
        """
        if self.required_files is not None:
            return [frozenset(self.required_files)]
        if self.repo_type == "core":
            return [frozenset({name}) for name in CORE_REQUIRED_FILES]
        if self.repo_type == "XXproductXX":
            return [frozenset({name}) for name in STANDARD_HARNESS_FILES]
        return [frozenset(DEFAULT_REQUIRED_FILES)]

    def xǁHarnessCanonReferenceǁ_requirement_groups__mutmut_9(self) -> list[frozenset[str]]:
        """Resolve the presence requirement into "at least one of" groups.

        Precedence: an explicit ``required_files`` (one any-of group) wins; then
        the ``repo_type`` preset (product → the full set as singletons; core →
        ``AGENTS.md`` only); an unrecognised ``repo_type`` falls back to the
        any-of ``DEFAULT_REQUIRED_FILES`` entrypoint set.
        """
        if self.required_files is not None:
            return [frozenset(self.required_files)]
        if self.repo_type == "core":
            return [frozenset({name}) for name in CORE_REQUIRED_FILES]
        if self.repo_type == "PRODUCT":
            return [frozenset({name}) for name in STANDARD_HARNESS_FILES]
        return [frozenset(DEFAULT_REQUIRED_FILES)]

    def xǁHarnessCanonReferenceǁ_requirement_groups__mutmut_10(self) -> list[frozenset[str]]:
        """Resolve the presence requirement into "at least one of" groups.

        Precedence: an explicit ``required_files`` (one any-of group) wins; then
        the ``repo_type`` preset (product → the full set as singletons; core →
        ``AGENTS.md`` only); an unrecognised ``repo_type`` falls back to the
        any-of ``DEFAULT_REQUIRED_FILES`` entrypoint set.
        """
        if self.required_files is not None:
            return [frozenset(self.required_files)]
        if self.repo_type == "core":
            return [frozenset({name}) for name in CORE_REQUIRED_FILES]
        if self.repo_type == "product":
            return [frozenset(None) for name in STANDARD_HARNESS_FILES]
        return [frozenset(DEFAULT_REQUIRED_FILES)]

    def xǁHarnessCanonReferenceǁ_requirement_groups__mutmut_11(self) -> list[frozenset[str]]:
        """Resolve the presence requirement into "at least one of" groups.

        Precedence: an explicit ``required_files`` (one any-of group) wins; then
        the ``repo_type`` preset (product → the full set as singletons; core →
        ``AGENTS.md`` only); an unrecognised ``repo_type`` falls back to the
        any-of ``DEFAULT_REQUIRED_FILES`` entrypoint set.
        """
        if self.required_files is not None:
            return [frozenset(self.required_files)]
        if self.repo_type == "core":
            return [frozenset({name}) for name in CORE_REQUIRED_FILES]
        if self.repo_type == "product":
            return [frozenset({name}) for name in STANDARD_HARNESS_FILES]
        return [frozenset(None)]

    @_mutmut_mutated(mutants_xǁHarnessCanonReferenceǁ_harness_texts__mutmut)
    def _harness_texts(self) -> dict[str, str]:
        """Read the harness entrypoint files that exist at the repo root.

        The universe is the standard harness set plus any explicitly required
        files; the reference and drift arms scan whichever of these are present.
        """
        names = list(dict.fromkeys((*STANDARD_HARNESS_FILES, *(self.required_files or ()))))
        texts: dict[str, str] = {}
        for name in names:
            candidate = self._repo_root / name
            if not candidate.is_file():
                continue
            try:
                texts[name] = candidate.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
        return texts

    def xǁHarnessCanonReferenceǁ_harness_texts__mutmut_orig(self) -> dict[str, str]:
        """Read the harness entrypoint files that exist at the repo root.

        The universe is the standard harness set plus any explicitly required
        files; the reference and drift arms scan whichever of these are present.
        """
        names = list(dict.fromkeys((*STANDARD_HARNESS_FILES, *(self.required_files or ()))))
        texts: dict[str, str] = {}
        for name in names:
            candidate = self._repo_root / name
            if not candidate.is_file():
                continue
            try:
                texts[name] = candidate.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
        return texts

    def xǁHarnessCanonReferenceǁ_harness_texts__mutmut_1(self) -> dict[str, str]:
        """Read the harness entrypoint files that exist at the repo root.

        The universe is the standard harness set plus any explicitly required
        files; the reference and drift arms scan whichever of these are present.
        """
        names = None
        texts: dict[str, str] = {}
        for name in names:
            candidate = self._repo_root / name
            if not candidate.is_file():
                continue
            try:
                texts[name] = candidate.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
        return texts

    def xǁHarnessCanonReferenceǁ_harness_texts__mutmut_2(self) -> dict[str, str]:
        """Read the harness entrypoint files that exist at the repo root.

        The universe is the standard harness set plus any explicitly required
        files; the reference and drift arms scan whichever of these are present.
        """
        names = list(None)
        texts: dict[str, str] = {}
        for name in names:
            candidate = self._repo_root / name
            if not candidate.is_file():
                continue
            try:
                texts[name] = candidate.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
        return texts

    def xǁHarnessCanonReferenceǁ_harness_texts__mutmut_3(self) -> dict[str, str]:
        """Read the harness entrypoint files that exist at the repo root.

        The universe is the standard harness set plus any explicitly required
        files; the reference and drift arms scan whichever of these are present.
        """
        names = list(dict.fromkeys(None))
        texts: dict[str, str] = {}
        for name in names:
            candidate = self._repo_root / name
            if not candidate.is_file():
                continue
            try:
                texts[name] = candidate.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
        return texts

    def xǁHarnessCanonReferenceǁ_harness_texts__mutmut_4(self) -> dict[str, str]:
        """Read the harness entrypoint files that exist at the repo root.

        The universe is the standard harness set plus any explicitly required
        files; the reference and drift arms scan whichever of these are present.
        """
        names = list(dict.fromkeys((*STANDARD_HARNESS_FILES, *(self.required_files and ()))))
        texts: dict[str, str] = {}
        for name in names:
            candidate = self._repo_root / name
            if not candidate.is_file():
                continue
            try:
                texts[name] = candidate.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
        return texts

    def xǁHarnessCanonReferenceǁ_harness_texts__mutmut_5(self) -> dict[str, str]:
        """Read the harness entrypoint files that exist at the repo root.

        The universe is the standard harness set plus any explicitly required
        files; the reference and drift arms scan whichever of these are present.
        """
        names = list(dict.fromkeys((*STANDARD_HARNESS_FILES, *(self.required_files or ()))))
        texts: dict[str, str] = None
        for name in names:
            candidate = self._repo_root / name
            if not candidate.is_file():
                continue
            try:
                texts[name] = candidate.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
        return texts

    def xǁHarnessCanonReferenceǁ_harness_texts__mutmut_6(self) -> dict[str, str]:
        """Read the harness entrypoint files that exist at the repo root.

        The universe is the standard harness set plus any explicitly required
        files; the reference and drift arms scan whichever of these are present.
        """
        names = list(dict.fromkeys((*STANDARD_HARNESS_FILES, *(self.required_files or ()))))
        texts: dict[str, str] = {}
        for name in names:
            candidate = None
            if not candidate.is_file():
                continue
            try:
                texts[name] = candidate.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
        return texts

    def xǁHarnessCanonReferenceǁ_harness_texts__mutmut_7(self) -> dict[str, str]:
        """Read the harness entrypoint files that exist at the repo root.

        The universe is the standard harness set plus any explicitly required
        files; the reference and drift arms scan whichever of these are present.
        """
        names = list(dict.fromkeys((*STANDARD_HARNESS_FILES, *(self.required_files or ()))))
        texts: dict[str, str] = {}
        for name in names:
            candidate = self._repo_root * name
            if not candidate.is_file():
                continue
            try:
                texts[name] = candidate.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
        return texts

    def xǁHarnessCanonReferenceǁ_harness_texts__mutmut_8(self) -> dict[str, str]:
        """Read the harness entrypoint files that exist at the repo root.

        The universe is the standard harness set plus any explicitly required
        files; the reference and drift arms scan whichever of these are present.
        """
        names = list(dict.fromkeys((*STANDARD_HARNESS_FILES, *(self.required_files or ()))))
        texts: dict[str, str] = {}
        for name in names:
            candidate = self._repo_root / name
            if candidate.is_file():
                continue
            try:
                texts[name] = candidate.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
        return texts

    def xǁHarnessCanonReferenceǁ_harness_texts__mutmut_9(self) -> dict[str, str]:
        """Read the harness entrypoint files that exist at the repo root.

        The universe is the standard harness set plus any explicitly required
        files; the reference and drift arms scan whichever of these are present.
        """
        names = list(dict.fromkeys((*STANDARD_HARNESS_FILES, *(self.required_files or ()))))
        texts: dict[str, str] = {}
        for name in names:
            candidate = self._repo_root / name
            if not candidate.is_file():
                break
            try:
                texts[name] = candidate.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
        return texts

    def xǁHarnessCanonReferenceǁ_harness_texts__mutmut_10(self) -> dict[str, str]:
        """Read the harness entrypoint files that exist at the repo root.

        The universe is the standard harness set plus any explicitly required
        files; the reference and drift arms scan whichever of these are present.
        """
        names = list(dict.fromkeys((*STANDARD_HARNESS_FILES, *(self.required_files or ()))))
        texts: dict[str, str] = {}
        for name in names:
            candidate = self._repo_root / name
            if not candidate.is_file():
                continue
            try:
                texts[name] = None
            except (UnicodeDecodeError, OSError):
                continue
        return texts

    def xǁHarnessCanonReferenceǁ_harness_texts__mutmut_11(self) -> dict[str, str]:
        """Read the harness entrypoint files that exist at the repo root.

        The universe is the standard harness set plus any explicitly required
        files; the reference and drift arms scan whichever of these are present.
        """
        names = list(dict.fromkeys((*STANDARD_HARNESS_FILES, *(self.required_files or ()))))
        texts: dict[str, str] = {}
        for name in names:
            candidate = self._repo_root / name
            if not candidate.is_file():
                continue
            try:
                texts[name] = candidate.read_text(encoding=None)
            except (UnicodeDecodeError, OSError):
                continue
        return texts

    def xǁHarnessCanonReferenceǁ_harness_texts__mutmut_12(self) -> dict[str, str]:
        """Read the harness entrypoint files that exist at the repo root.

        The universe is the standard harness set plus any explicitly required
        files; the reference and drift arms scan whichever of these are present.
        """
        names = list(dict.fromkeys((*STANDARD_HARNESS_FILES, *(self.required_files or ()))))
        texts: dict[str, str] = {}
        for name in names:
            candidate = self._repo_root / name
            if not candidate.is_file():
                continue
            try:
                texts[name] = candidate.read_text(encoding="XXutf-8XX")
            except (UnicodeDecodeError, OSError):
                continue
        return texts

    def xǁHarnessCanonReferenceǁ_harness_texts__mutmut_13(self) -> dict[str, str]:
        """Read the harness entrypoint files that exist at the repo root.

        The universe is the standard harness set plus any explicitly required
        files; the reference and drift arms scan whichever of these are present.
        """
        names = list(dict.fromkeys((*STANDARD_HARNESS_FILES, *(self.required_files or ()))))
        texts: dict[str, str] = {}
        for name in names:
            candidate = self._repo_root / name
            if not candidate.is_file():
                continue
            try:
                texts[name] = candidate.read_text(encoding="UTF-8")
            except (UnicodeDecodeError, OSError):
                continue
        return texts

    def xǁHarnessCanonReferenceǁ_harness_texts__mutmut_14(self) -> dict[str, str]:
        """Read the harness entrypoint files that exist at the repo root.

        The universe is the standard harness set plus any explicitly required
        files; the reference and drift arms scan whichever of these are present.
        """
        names = list(dict.fromkeys((*STANDARD_HARNESS_FILES, *(self.required_files or ()))))
        texts: dict[str, str] = {}
        for name in names:
            candidate = self._repo_root / name
            if not candidate.is_file():
                continue
            try:
                texts[name] = candidate.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                break
        return texts

    @_mutmut_mutated(mutants_xǁHarnessCanonReferenceǁ_reference_failure__mutmut)
    def _reference_failure(self, harness_texts: Mapping[str, str]) -> str | None:
        """None when a harness file names the canon; else the failure label."""
        try:
            ref_pattern = re.compile(self.standards_ref_pattern)
        except re.error as exc:
            return f"standards_ref_pattern is not a valid regex ({exc})"
        if has_canon_reference(harness_texts.values(), marker=self.banner_marker, ref_pattern=ref_pattern):
            return None
        return (
            f"no harness file carries the canonical-standards reference "
            f"(marker {self.banner_marker!r} plus a link matching "
            f"{self.standards_ref_pattern!r})"
        )

    def xǁHarnessCanonReferenceǁ_reference_failure__mutmut_orig(self, harness_texts: Mapping[str, str]) -> str | None:
        """None when a harness file names the canon; else the failure label."""
        try:
            ref_pattern = re.compile(self.standards_ref_pattern)
        except re.error as exc:
            return f"standards_ref_pattern is not a valid regex ({exc})"
        if has_canon_reference(harness_texts.values(), marker=self.banner_marker, ref_pattern=ref_pattern):
            return None
        return (
            f"no harness file carries the canonical-standards reference "
            f"(marker {self.banner_marker!r} plus a link matching "
            f"{self.standards_ref_pattern!r})"
        )

    def xǁHarnessCanonReferenceǁ_reference_failure__mutmut_1(self, harness_texts: Mapping[str, str]) -> str | None:
        """None when a harness file names the canon; else the failure label."""
        try:
            ref_pattern = None
        except re.error as exc:
            return f"standards_ref_pattern is not a valid regex ({exc})"
        if has_canon_reference(harness_texts.values(), marker=self.banner_marker, ref_pattern=ref_pattern):
            return None
        return (
            f"no harness file carries the canonical-standards reference "
            f"(marker {self.banner_marker!r} plus a link matching "
            f"{self.standards_ref_pattern!r})"
        )

    def xǁHarnessCanonReferenceǁ_reference_failure__mutmut_2(self, harness_texts: Mapping[str, str]) -> str | None:
        """None when a harness file names the canon; else the failure label."""
        try:
            ref_pattern = re.compile(None)
        except re.error as exc:
            return f"standards_ref_pattern is not a valid regex ({exc})"
        if has_canon_reference(harness_texts.values(), marker=self.banner_marker, ref_pattern=ref_pattern):
            return None
        return (
            f"no harness file carries the canonical-standards reference "
            f"(marker {self.banner_marker!r} plus a link matching "
            f"{self.standards_ref_pattern!r})"
        )

    def xǁHarnessCanonReferenceǁ_reference_failure__mutmut_3(self, harness_texts: Mapping[str, str]) -> str | None:
        """None when a harness file names the canon; else the failure label."""
        try:
            ref_pattern = re.compile(self.standards_ref_pattern)
        except re.error as exc:
            return f"standards_ref_pattern is not a valid regex ({exc})"
        if has_canon_reference(None, marker=self.banner_marker, ref_pattern=ref_pattern):
            return None
        return (
            f"no harness file carries the canonical-standards reference "
            f"(marker {self.banner_marker!r} plus a link matching "
            f"{self.standards_ref_pattern!r})"
        )

    def xǁHarnessCanonReferenceǁ_reference_failure__mutmut_4(self, harness_texts: Mapping[str, str]) -> str | None:
        """None when a harness file names the canon; else the failure label."""
        try:
            ref_pattern = re.compile(self.standards_ref_pattern)
        except re.error as exc:
            return f"standards_ref_pattern is not a valid regex ({exc})"
        if has_canon_reference(harness_texts.values(), marker=None, ref_pattern=ref_pattern):
            return None
        return (
            f"no harness file carries the canonical-standards reference "
            f"(marker {self.banner_marker!r} plus a link matching "
            f"{self.standards_ref_pattern!r})"
        )

    def xǁHarnessCanonReferenceǁ_reference_failure__mutmut_5(self, harness_texts: Mapping[str, str]) -> str | None:
        """None when a harness file names the canon; else the failure label."""
        try:
            ref_pattern = re.compile(self.standards_ref_pattern)
        except re.error as exc:
            return f"standards_ref_pattern is not a valid regex ({exc})"
        if has_canon_reference(harness_texts.values(), marker=self.banner_marker, ref_pattern=None):
            return None
        return (
            f"no harness file carries the canonical-standards reference "
            f"(marker {self.banner_marker!r} plus a link matching "
            f"{self.standards_ref_pattern!r})"
        )

    def xǁHarnessCanonReferenceǁ_reference_failure__mutmut_6(self, harness_texts: Mapping[str, str]) -> str | None:
        """None when a harness file names the canon; else the failure label."""
        try:
            ref_pattern = re.compile(self.standards_ref_pattern)
        except re.error as exc:
            return f"standards_ref_pattern is not a valid regex ({exc})"
        if has_canon_reference(marker=self.banner_marker, ref_pattern=ref_pattern):
            return None
        return (
            f"no harness file carries the canonical-standards reference "
            f"(marker {self.banner_marker!r} plus a link matching "
            f"{self.standards_ref_pattern!r})"
        )

    def xǁHarnessCanonReferenceǁ_reference_failure__mutmut_7(self, harness_texts: Mapping[str, str]) -> str | None:
        """None when a harness file names the canon; else the failure label."""
        try:
            ref_pattern = re.compile(self.standards_ref_pattern)
        except re.error as exc:
            return f"standards_ref_pattern is not a valid regex ({exc})"
        if has_canon_reference(harness_texts.values(), ref_pattern=ref_pattern):
            return None
        return (
            f"no harness file carries the canonical-standards reference "
            f"(marker {self.banner_marker!r} plus a link matching "
            f"{self.standards_ref_pattern!r})"
        )

    def xǁHarnessCanonReferenceǁ_reference_failure__mutmut_8(self, harness_texts: Mapping[str, str]) -> str | None:
        """None when a harness file names the canon; else the failure label."""
        try:
            ref_pattern = re.compile(self.standards_ref_pattern)
        except re.error as exc:
            return f"standards_ref_pattern is not a valid regex ({exc})"
        if has_canon_reference(harness_texts.values(), marker=self.banner_marker, ):
            return None
        return (
            f"no harness file carries the canonical-standards reference "
            f"(marker {self.banner_marker!r} plus a link matching "
            f"{self.standards_ref_pattern!r})"
        )

    @_mutmut_mutated(mutants_xǁHarnessCanonReferenceǁ_drift_failure__mutmut)
    def _drift_failure(self, harness_texts: Mapping[str, str]) -> str | None:
        """None when the drift arm is off or the pinned banner is inlined."""
        if self.banner_path is None:
            return None
        pinned = self._repo_root / self.banner_path
        if not pinned.is_file():
            return (
                f"banner_path {self.banner_path!r} is configured but no pinned "
                f"banner file exists there to drift-compare against"
            )
        try:
            pinned_text = pinned.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as exc:
            return f"the pinned banner at {self.banner_path!r} could not be read ({exc})"
        if banner_present(harness_texts.values(), pinned_text):
            return None
        return f"the inlined canonical banner has drifted from the pinned copy at {self.banner_path!r}"

    def xǁHarnessCanonReferenceǁ_drift_failure__mutmut_orig(self, harness_texts: Mapping[str, str]) -> str | None:
        """None when the drift arm is off or the pinned banner is inlined."""
        if self.banner_path is None:
            return None
        pinned = self._repo_root / self.banner_path
        if not pinned.is_file():
            return (
                f"banner_path {self.banner_path!r} is configured but no pinned "
                f"banner file exists there to drift-compare against"
            )
        try:
            pinned_text = pinned.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as exc:
            return f"the pinned banner at {self.banner_path!r} could not be read ({exc})"
        if banner_present(harness_texts.values(), pinned_text):
            return None
        return f"the inlined canonical banner has drifted from the pinned copy at {self.banner_path!r}"

    def xǁHarnessCanonReferenceǁ_drift_failure__mutmut_1(self, harness_texts: Mapping[str, str]) -> str | None:
        """None when the drift arm is off or the pinned banner is inlined."""
        if self.banner_path is not None:
            return None
        pinned = self._repo_root / self.banner_path
        if not pinned.is_file():
            return (
                f"banner_path {self.banner_path!r} is configured but no pinned "
                f"banner file exists there to drift-compare against"
            )
        try:
            pinned_text = pinned.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as exc:
            return f"the pinned banner at {self.banner_path!r} could not be read ({exc})"
        if banner_present(harness_texts.values(), pinned_text):
            return None
        return f"the inlined canonical banner has drifted from the pinned copy at {self.banner_path!r}"

    def xǁHarnessCanonReferenceǁ_drift_failure__mutmut_2(self, harness_texts: Mapping[str, str]) -> str | None:
        """None when the drift arm is off or the pinned banner is inlined."""
        if self.banner_path is None:
            return None
        pinned = None
        if not pinned.is_file():
            return (
                f"banner_path {self.banner_path!r} is configured but no pinned "
                f"banner file exists there to drift-compare against"
            )
        try:
            pinned_text = pinned.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as exc:
            return f"the pinned banner at {self.banner_path!r} could not be read ({exc})"
        if banner_present(harness_texts.values(), pinned_text):
            return None
        return f"the inlined canonical banner has drifted from the pinned copy at {self.banner_path!r}"

    def xǁHarnessCanonReferenceǁ_drift_failure__mutmut_3(self, harness_texts: Mapping[str, str]) -> str | None:
        """None when the drift arm is off or the pinned banner is inlined."""
        if self.banner_path is None:
            return None
        pinned = self._repo_root * self.banner_path
        if not pinned.is_file():
            return (
                f"banner_path {self.banner_path!r} is configured but no pinned "
                f"banner file exists there to drift-compare against"
            )
        try:
            pinned_text = pinned.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as exc:
            return f"the pinned banner at {self.banner_path!r} could not be read ({exc})"
        if banner_present(harness_texts.values(), pinned_text):
            return None
        return f"the inlined canonical banner has drifted from the pinned copy at {self.banner_path!r}"

    def xǁHarnessCanonReferenceǁ_drift_failure__mutmut_4(self, harness_texts: Mapping[str, str]) -> str | None:
        """None when the drift arm is off or the pinned banner is inlined."""
        if self.banner_path is None:
            return None
        pinned = self._repo_root / self.banner_path
        if pinned.is_file():
            return (
                f"banner_path {self.banner_path!r} is configured but no pinned "
                f"banner file exists there to drift-compare against"
            )
        try:
            pinned_text = pinned.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as exc:
            return f"the pinned banner at {self.banner_path!r} could not be read ({exc})"
        if banner_present(harness_texts.values(), pinned_text):
            return None
        return f"the inlined canonical banner has drifted from the pinned copy at {self.banner_path!r}"

    def xǁHarnessCanonReferenceǁ_drift_failure__mutmut_5(self, harness_texts: Mapping[str, str]) -> str | None:
        """None when the drift arm is off or the pinned banner is inlined."""
        if self.banner_path is None:
            return None
        pinned = self._repo_root / self.banner_path
        if not pinned.is_file():
            return (
                f"banner_path {self.banner_path!r} is configured but no pinned "
                f"banner file exists there to drift-compare against"
            )
        try:
            pinned_text = None
        except (UnicodeDecodeError, OSError) as exc:
            return f"the pinned banner at {self.banner_path!r} could not be read ({exc})"
        if banner_present(harness_texts.values(), pinned_text):
            return None
        return f"the inlined canonical banner has drifted from the pinned copy at {self.banner_path!r}"

    def xǁHarnessCanonReferenceǁ_drift_failure__mutmut_6(self, harness_texts: Mapping[str, str]) -> str | None:
        """None when the drift arm is off or the pinned banner is inlined."""
        if self.banner_path is None:
            return None
        pinned = self._repo_root / self.banner_path
        if not pinned.is_file():
            return (
                f"banner_path {self.banner_path!r} is configured but no pinned "
                f"banner file exists there to drift-compare against"
            )
        try:
            pinned_text = pinned.read_text(encoding=None)
        except (UnicodeDecodeError, OSError) as exc:
            return f"the pinned banner at {self.banner_path!r} could not be read ({exc})"
        if banner_present(harness_texts.values(), pinned_text):
            return None
        return f"the inlined canonical banner has drifted from the pinned copy at {self.banner_path!r}"

    def xǁHarnessCanonReferenceǁ_drift_failure__mutmut_7(self, harness_texts: Mapping[str, str]) -> str | None:
        """None when the drift arm is off or the pinned banner is inlined."""
        if self.banner_path is None:
            return None
        pinned = self._repo_root / self.banner_path
        if not pinned.is_file():
            return (
                f"banner_path {self.banner_path!r} is configured but no pinned "
                f"banner file exists there to drift-compare against"
            )
        try:
            pinned_text = pinned.read_text(encoding="XXutf-8XX")
        except (UnicodeDecodeError, OSError) as exc:
            return f"the pinned banner at {self.banner_path!r} could not be read ({exc})"
        if banner_present(harness_texts.values(), pinned_text):
            return None
        return f"the inlined canonical banner has drifted from the pinned copy at {self.banner_path!r}"

    def xǁHarnessCanonReferenceǁ_drift_failure__mutmut_8(self, harness_texts: Mapping[str, str]) -> str | None:
        """None when the drift arm is off or the pinned banner is inlined."""
        if self.banner_path is None:
            return None
        pinned = self._repo_root / self.banner_path
        if not pinned.is_file():
            return (
                f"banner_path {self.banner_path!r} is configured but no pinned "
                f"banner file exists there to drift-compare against"
            )
        try:
            pinned_text = pinned.read_text(encoding="UTF-8")
        except (UnicodeDecodeError, OSError) as exc:
            return f"the pinned banner at {self.banner_path!r} could not be read ({exc})"
        if banner_present(harness_texts.values(), pinned_text):
            return None
        return f"the inlined canonical banner has drifted from the pinned copy at {self.banner_path!r}"

    def xǁHarnessCanonReferenceǁ_drift_failure__mutmut_9(self, harness_texts: Mapping[str, str]) -> str | None:
        """None when the drift arm is off or the pinned banner is inlined."""
        if self.banner_path is None:
            return None
        pinned = self._repo_root / self.banner_path
        if not pinned.is_file():
            return (
                f"banner_path {self.banner_path!r} is configured but no pinned "
                f"banner file exists there to drift-compare against"
            )
        try:
            pinned_text = pinned.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as exc:
            return f"the pinned banner at {self.banner_path!r} could not be read ({exc})"
        if banner_present(None, pinned_text):
            return None
        return f"the inlined canonical banner has drifted from the pinned copy at {self.banner_path!r}"

    def xǁHarnessCanonReferenceǁ_drift_failure__mutmut_10(self, harness_texts: Mapping[str, str]) -> str | None:
        """None when the drift arm is off or the pinned banner is inlined."""
        if self.banner_path is None:
            return None
        pinned = self._repo_root / self.banner_path
        if not pinned.is_file():
            return (
                f"banner_path {self.banner_path!r} is configured but no pinned "
                f"banner file exists there to drift-compare against"
            )
        try:
            pinned_text = pinned.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as exc:
            return f"the pinned banner at {self.banner_path!r} could not be read ({exc})"
        if banner_present(harness_texts.values(), None):
            return None
        return f"the inlined canonical banner has drifted from the pinned copy at {self.banner_path!r}"

    def xǁHarnessCanonReferenceǁ_drift_failure__mutmut_11(self, harness_texts: Mapping[str, str]) -> str | None:
        """None when the drift arm is off or the pinned banner is inlined."""
        if self.banner_path is None:
            return None
        pinned = self._repo_root / self.banner_path
        if not pinned.is_file():
            return (
                f"banner_path {self.banner_path!r} is configured but no pinned "
                f"banner file exists there to drift-compare against"
            )
        try:
            pinned_text = pinned.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as exc:
            return f"the pinned banner at {self.banner_path!r} could not be read ({exc})"
        if banner_present(pinned_text):
            return None
        return f"the inlined canonical banner has drifted from the pinned copy at {self.banner_path!r}"

    def xǁHarnessCanonReferenceǁ_drift_failure__mutmut_12(self, harness_texts: Mapping[str, str]) -> str | None:
        """None when the drift arm is off or the pinned banner is inlined."""
        if self.banner_path is None:
            return None
        pinned = self._repo_root / self.banner_path
        if not pinned.is_file():
            return (
                f"banner_path {self.banner_path!r} is configured but no pinned "
                f"banner file exists there to drift-compare against"
            )
        try:
            pinned_text = pinned.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as exc:
            return f"the pinned banner at {self.banner_path!r} could not be read ({exc})"
        if banner_present(harness_texts.values(), ):
            return None
        return f"the inlined canonical banner has drifted from the pinned copy at {self.banner_path!r}"

    @_mutmut_mutated(mutants_xǁHarnessCanonReferenceǁrun__mutmut)
    def run(self) -> int:
        """Drive the three arms; FAIL (1) on any drift, else PASS (0)."""
        failures: list[str] = []

        for label in missing_required_groups(self._repo_root, self._requirement_groups()):
            failures.append(f"missing required harness entrypoint: {label}")

        harness_texts = self._harness_texts()
        reference_failure = self._reference_failure(harness_texts)
        if reference_failure is not None:
            failures.append(reference_failure)

        drift_failure = self._drift_failure(harness_texts)
        if drift_failure is not None:
            failures.append(drift_failure)

        if failures:
            for failure in failures:
                report_finding(self.name, ".", failure)
            print(f"FAIL [{self._name}] — agent harness has drifted from the shared canon:")
            for failure in failures:
                print(f"  - {failure}")
            print()
            print(self.remediation)
            return 1

        arms = "presence, reference" + (", drift" if self.banner_path is not None else "")
        print(f"ok [{self._name}] — harness references the shared canon (arms checked: {arms}).")
        return 0

    def xǁHarnessCanonReferenceǁrun__mutmut_orig(self) -> int:
        """Drive the three arms; FAIL (1) on any drift, else PASS (0)."""
        failures: list[str] = []

        for label in missing_required_groups(self._repo_root, self._requirement_groups()):
            failures.append(f"missing required harness entrypoint: {label}")

        harness_texts = self._harness_texts()
        reference_failure = self._reference_failure(harness_texts)
        if reference_failure is not None:
            failures.append(reference_failure)

        drift_failure = self._drift_failure(harness_texts)
        if drift_failure is not None:
            failures.append(drift_failure)

        if failures:
            for failure in failures:
                report_finding(self.name, ".", failure)
            print(f"FAIL [{self._name}] — agent harness has drifted from the shared canon:")
            for failure in failures:
                print(f"  - {failure}")
            print()
            print(self.remediation)
            return 1

        arms = "presence, reference" + (", drift" if self.banner_path is not None else "")
        print(f"ok [{self._name}] — harness references the shared canon (arms checked: {arms}).")
        return 0

    def xǁHarnessCanonReferenceǁrun__mutmut_1(self) -> int:
        """Drive the three arms; FAIL (1) on any drift, else PASS (0)."""
        failures: list[str] = None

        for label in missing_required_groups(self._repo_root, self._requirement_groups()):
            failures.append(f"missing required harness entrypoint: {label}")

        harness_texts = self._harness_texts()
        reference_failure = self._reference_failure(harness_texts)
        if reference_failure is not None:
            failures.append(reference_failure)

        drift_failure = self._drift_failure(harness_texts)
        if drift_failure is not None:
            failures.append(drift_failure)

        if failures:
            for failure in failures:
                report_finding(self.name, ".", failure)
            print(f"FAIL [{self._name}] — agent harness has drifted from the shared canon:")
            for failure in failures:
                print(f"  - {failure}")
            print()
            print(self.remediation)
            return 1

        arms = "presence, reference" + (", drift" if self.banner_path is not None else "")
        print(f"ok [{self._name}] — harness references the shared canon (arms checked: {arms}).")
        return 0

    def xǁHarnessCanonReferenceǁrun__mutmut_2(self) -> int:
        """Drive the three arms; FAIL (1) on any drift, else PASS (0)."""
        failures: list[str] = []

        for label in missing_required_groups(None, self._requirement_groups()):
            failures.append(f"missing required harness entrypoint: {label}")

        harness_texts = self._harness_texts()
        reference_failure = self._reference_failure(harness_texts)
        if reference_failure is not None:
            failures.append(reference_failure)

        drift_failure = self._drift_failure(harness_texts)
        if drift_failure is not None:
            failures.append(drift_failure)

        if failures:
            for failure in failures:
                report_finding(self.name, ".", failure)
            print(f"FAIL [{self._name}] — agent harness has drifted from the shared canon:")
            for failure in failures:
                print(f"  - {failure}")
            print()
            print(self.remediation)
            return 1

        arms = "presence, reference" + (", drift" if self.banner_path is not None else "")
        print(f"ok [{self._name}] — harness references the shared canon (arms checked: {arms}).")
        return 0

    def xǁHarnessCanonReferenceǁrun__mutmut_3(self) -> int:
        """Drive the three arms; FAIL (1) on any drift, else PASS (0)."""
        failures: list[str] = []

        for label in missing_required_groups(self._repo_root, None):
            failures.append(f"missing required harness entrypoint: {label}")

        harness_texts = self._harness_texts()
        reference_failure = self._reference_failure(harness_texts)
        if reference_failure is not None:
            failures.append(reference_failure)

        drift_failure = self._drift_failure(harness_texts)
        if drift_failure is not None:
            failures.append(drift_failure)

        if failures:
            for failure in failures:
                report_finding(self.name, ".", failure)
            print(f"FAIL [{self._name}] — agent harness has drifted from the shared canon:")
            for failure in failures:
                print(f"  - {failure}")
            print()
            print(self.remediation)
            return 1

        arms = "presence, reference" + (", drift" if self.banner_path is not None else "")
        print(f"ok [{self._name}] — harness references the shared canon (arms checked: {arms}).")
        return 0

    def xǁHarnessCanonReferenceǁrun__mutmut_4(self) -> int:
        """Drive the three arms; FAIL (1) on any drift, else PASS (0)."""
        failures: list[str] = []

        for label in missing_required_groups(self._requirement_groups()):
            failures.append(f"missing required harness entrypoint: {label}")

        harness_texts = self._harness_texts()
        reference_failure = self._reference_failure(harness_texts)
        if reference_failure is not None:
            failures.append(reference_failure)

        drift_failure = self._drift_failure(harness_texts)
        if drift_failure is not None:
            failures.append(drift_failure)

        if failures:
            for failure in failures:
                report_finding(self.name, ".", failure)
            print(f"FAIL [{self._name}] — agent harness has drifted from the shared canon:")
            for failure in failures:
                print(f"  - {failure}")
            print()
            print(self.remediation)
            return 1

        arms = "presence, reference" + (", drift" if self.banner_path is not None else "")
        print(f"ok [{self._name}] — harness references the shared canon (arms checked: {arms}).")
        return 0

    def xǁHarnessCanonReferenceǁrun__mutmut_5(self) -> int:
        """Drive the three arms; FAIL (1) on any drift, else PASS (0)."""
        failures: list[str] = []

        for label in missing_required_groups(self._repo_root, ):
            failures.append(f"missing required harness entrypoint: {label}")

        harness_texts = self._harness_texts()
        reference_failure = self._reference_failure(harness_texts)
        if reference_failure is not None:
            failures.append(reference_failure)

        drift_failure = self._drift_failure(harness_texts)
        if drift_failure is not None:
            failures.append(drift_failure)

        if failures:
            for failure in failures:
                report_finding(self.name, ".", failure)
            print(f"FAIL [{self._name}] — agent harness has drifted from the shared canon:")
            for failure in failures:
                print(f"  - {failure}")
            print()
            print(self.remediation)
            return 1

        arms = "presence, reference" + (", drift" if self.banner_path is not None else "")
        print(f"ok [{self._name}] — harness references the shared canon (arms checked: {arms}).")
        return 0

    def xǁHarnessCanonReferenceǁrun__mutmut_6(self) -> int:
        """Drive the three arms; FAIL (1) on any drift, else PASS (0)."""
        failures: list[str] = []

        for label in missing_required_groups(self._repo_root, self._requirement_groups()):
            failures.append(None)

        harness_texts = self._harness_texts()
        reference_failure = self._reference_failure(harness_texts)
        if reference_failure is not None:
            failures.append(reference_failure)

        drift_failure = self._drift_failure(harness_texts)
        if drift_failure is not None:
            failures.append(drift_failure)

        if failures:
            for failure in failures:
                report_finding(self.name, ".", failure)
            print(f"FAIL [{self._name}] — agent harness has drifted from the shared canon:")
            for failure in failures:
                print(f"  - {failure}")
            print()
            print(self.remediation)
            return 1

        arms = "presence, reference" + (", drift" if self.banner_path is not None else "")
        print(f"ok [{self._name}] — harness references the shared canon (arms checked: {arms}).")
        return 0

    def xǁHarnessCanonReferenceǁrun__mutmut_7(self) -> int:
        """Drive the three arms; FAIL (1) on any drift, else PASS (0)."""
        failures: list[str] = []

        for label in missing_required_groups(self._repo_root, self._requirement_groups()):
            failures.append(f"missing required harness entrypoint: {label}")

        harness_texts = None
        reference_failure = self._reference_failure(harness_texts)
        if reference_failure is not None:
            failures.append(reference_failure)

        drift_failure = self._drift_failure(harness_texts)
        if drift_failure is not None:
            failures.append(drift_failure)

        if failures:
            for failure in failures:
                report_finding(self.name, ".", failure)
            print(f"FAIL [{self._name}] — agent harness has drifted from the shared canon:")
            for failure in failures:
                print(f"  - {failure}")
            print()
            print(self.remediation)
            return 1

        arms = "presence, reference" + (", drift" if self.banner_path is not None else "")
        print(f"ok [{self._name}] — harness references the shared canon (arms checked: {arms}).")
        return 0

    def xǁHarnessCanonReferenceǁrun__mutmut_8(self) -> int:
        """Drive the three arms; FAIL (1) on any drift, else PASS (0)."""
        failures: list[str] = []

        for label in missing_required_groups(self._repo_root, self._requirement_groups()):
            failures.append(f"missing required harness entrypoint: {label}")

        harness_texts = self._harness_texts()
        reference_failure = None
        if reference_failure is not None:
            failures.append(reference_failure)

        drift_failure = self._drift_failure(harness_texts)
        if drift_failure is not None:
            failures.append(drift_failure)

        if failures:
            for failure in failures:
                report_finding(self.name, ".", failure)
            print(f"FAIL [{self._name}] — agent harness has drifted from the shared canon:")
            for failure in failures:
                print(f"  - {failure}")
            print()
            print(self.remediation)
            return 1

        arms = "presence, reference" + (", drift" if self.banner_path is not None else "")
        print(f"ok [{self._name}] — harness references the shared canon (arms checked: {arms}).")
        return 0

    def xǁHarnessCanonReferenceǁrun__mutmut_9(self) -> int:
        """Drive the three arms; FAIL (1) on any drift, else PASS (0)."""
        failures: list[str] = []

        for label in missing_required_groups(self._repo_root, self._requirement_groups()):
            failures.append(f"missing required harness entrypoint: {label}")

        harness_texts = self._harness_texts()
        reference_failure = self._reference_failure(None)
        if reference_failure is not None:
            failures.append(reference_failure)

        drift_failure = self._drift_failure(harness_texts)
        if drift_failure is not None:
            failures.append(drift_failure)

        if failures:
            for failure in failures:
                report_finding(self.name, ".", failure)
            print(f"FAIL [{self._name}] — agent harness has drifted from the shared canon:")
            for failure in failures:
                print(f"  - {failure}")
            print()
            print(self.remediation)
            return 1

        arms = "presence, reference" + (", drift" if self.banner_path is not None else "")
        print(f"ok [{self._name}] — harness references the shared canon (arms checked: {arms}).")
        return 0

    def xǁHarnessCanonReferenceǁrun__mutmut_10(self) -> int:
        """Drive the three arms; FAIL (1) on any drift, else PASS (0)."""
        failures: list[str] = []

        for label in missing_required_groups(self._repo_root, self._requirement_groups()):
            failures.append(f"missing required harness entrypoint: {label}")

        harness_texts = self._harness_texts()
        reference_failure = self._reference_failure(harness_texts)
        if reference_failure is None:
            failures.append(reference_failure)

        drift_failure = self._drift_failure(harness_texts)
        if drift_failure is not None:
            failures.append(drift_failure)

        if failures:
            for failure in failures:
                report_finding(self.name, ".", failure)
            print(f"FAIL [{self._name}] — agent harness has drifted from the shared canon:")
            for failure in failures:
                print(f"  - {failure}")
            print()
            print(self.remediation)
            return 1

        arms = "presence, reference" + (", drift" if self.banner_path is not None else "")
        print(f"ok [{self._name}] — harness references the shared canon (arms checked: {arms}).")
        return 0

    def xǁHarnessCanonReferenceǁrun__mutmut_11(self) -> int:
        """Drive the three arms; FAIL (1) on any drift, else PASS (0)."""
        failures: list[str] = []

        for label in missing_required_groups(self._repo_root, self._requirement_groups()):
            failures.append(f"missing required harness entrypoint: {label}")

        harness_texts = self._harness_texts()
        reference_failure = self._reference_failure(harness_texts)
        if reference_failure is not None:
            failures.append(None)

        drift_failure = self._drift_failure(harness_texts)
        if drift_failure is not None:
            failures.append(drift_failure)

        if failures:
            for failure in failures:
                report_finding(self.name, ".", failure)
            print(f"FAIL [{self._name}] — agent harness has drifted from the shared canon:")
            for failure in failures:
                print(f"  - {failure}")
            print()
            print(self.remediation)
            return 1

        arms = "presence, reference" + (", drift" if self.banner_path is not None else "")
        print(f"ok [{self._name}] — harness references the shared canon (arms checked: {arms}).")
        return 0

    def xǁHarnessCanonReferenceǁrun__mutmut_12(self) -> int:
        """Drive the three arms; FAIL (1) on any drift, else PASS (0)."""
        failures: list[str] = []

        for label in missing_required_groups(self._repo_root, self._requirement_groups()):
            failures.append(f"missing required harness entrypoint: {label}")

        harness_texts = self._harness_texts()
        reference_failure = self._reference_failure(harness_texts)
        if reference_failure is not None:
            failures.append(reference_failure)

        drift_failure = None
        if drift_failure is not None:
            failures.append(drift_failure)

        if failures:
            for failure in failures:
                report_finding(self.name, ".", failure)
            print(f"FAIL [{self._name}] — agent harness has drifted from the shared canon:")
            for failure in failures:
                print(f"  - {failure}")
            print()
            print(self.remediation)
            return 1

        arms = "presence, reference" + (", drift" if self.banner_path is not None else "")
        print(f"ok [{self._name}] — harness references the shared canon (arms checked: {arms}).")
        return 0

    def xǁHarnessCanonReferenceǁrun__mutmut_13(self) -> int:
        """Drive the three arms; FAIL (1) on any drift, else PASS (0)."""
        failures: list[str] = []

        for label in missing_required_groups(self._repo_root, self._requirement_groups()):
            failures.append(f"missing required harness entrypoint: {label}")

        harness_texts = self._harness_texts()
        reference_failure = self._reference_failure(harness_texts)
        if reference_failure is not None:
            failures.append(reference_failure)

        drift_failure = self._drift_failure(None)
        if drift_failure is not None:
            failures.append(drift_failure)

        if failures:
            for failure in failures:
                report_finding(self.name, ".", failure)
            print(f"FAIL [{self._name}] — agent harness has drifted from the shared canon:")
            for failure in failures:
                print(f"  - {failure}")
            print()
            print(self.remediation)
            return 1

        arms = "presence, reference" + (", drift" if self.banner_path is not None else "")
        print(f"ok [{self._name}] — harness references the shared canon (arms checked: {arms}).")
        return 0

    def xǁHarnessCanonReferenceǁrun__mutmut_14(self) -> int:
        """Drive the three arms; FAIL (1) on any drift, else PASS (0)."""
        failures: list[str] = []

        for label in missing_required_groups(self._repo_root, self._requirement_groups()):
            failures.append(f"missing required harness entrypoint: {label}")

        harness_texts = self._harness_texts()
        reference_failure = self._reference_failure(harness_texts)
        if reference_failure is not None:
            failures.append(reference_failure)

        drift_failure = self._drift_failure(harness_texts)
        if drift_failure is None:
            failures.append(drift_failure)

        if failures:
            for failure in failures:
                report_finding(self.name, ".", failure)
            print(f"FAIL [{self._name}] — agent harness has drifted from the shared canon:")
            for failure in failures:
                print(f"  - {failure}")
            print()
            print(self.remediation)
            return 1

        arms = "presence, reference" + (", drift" if self.banner_path is not None else "")
        print(f"ok [{self._name}] — harness references the shared canon (arms checked: {arms}).")
        return 0

    def xǁHarnessCanonReferenceǁrun__mutmut_15(self) -> int:
        """Drive the three arms; FAIL (1) on any drift, else PASS (0)."""
        failures: list[str] = []

        for label in missing_required_groups(self._repo_root, self._requirement_groups()):
            failures.append(f"missing required harness entrypoint: {label}")

        harness_texts = self._harness_texts()
        reference_failure = self._reference_failure(harness_texts)
        if reference_failure is not None:
            failures.append(reference_failure)

        drift_failure = self._drift_failure(harness_texts)
        if drift_failure is not None:
            failures.append(None)

        if failures:
            for failure in failures:
                report_finding(self.name, ".", failure)
            print(f"FAIL [{self._name}] — agent harness has drifted from the shared canon:")
            for failure in failures:
                print(f"  - {failure}")
            print()
            print(self.remediation)
            return 1

        arms = "presence, reference" + (", drift" if self.banner_path is not None else "")
        print(f"ok [{self._name}] — harness references the shared canon (arms checked: {arms}).")
        return 0

    def xǁHarnessCanonReferenceǁrun__mutmut_16(self) -> int:
        """Drive the three arms; FAIL (1) on any drift, else PASS (0)."""
        failures: list[str] = []

        for label in missing_required_groups(self._repo_root, self._requirement_groups()):
            failures.append(f"missing required harness entrypoint: {label}")

        harness_texts = self._harness_texts()
        reference_failure = self._reference_failure(harness_texts)
        if reference_failure is not None:
            failures.append(reference_failure)

        drift_failure = self._drift_failure(harness_texts)
        if drift_failure is not None:
            failures.append(drift_failure)

        if failures:
            for failure in failures:
                report_finding(None, ".", failure)
            print(f"FAIL [{self._name}] — agent harness has drifted from the shared canon:")
            for failure in failures:
                print(f"  - {failure}")
            print()
            print(self.remediation)
            return 1

        arms = "presence, reference" + (", drift" if self.banner_path is not None else "")
        print(f"ok [{self._name}] — harness references the shared canon (arms checked: {arms}).")
        return 0

    def xǁHarnessCanonReferenceǁrun__mutmut_17(self) -> int:
        """Drive the three arms; FAIL (1) on any drift, else PASS (0)."""
        failures: list[str] = []

        for label in missing_required_groups(self._repo_root, self._requirement_groups()):
            failures.append(f"missing required harness entrypoint: {label}")

        harness_texts = self._harness_texts()
        reference_failure = self._reference_failure(harness_texts)
        if reference_failure is not None:
            failures.append(reference_failure)

        drift_failure = self._drift_failure(harness_texts)
        if drift_failure is not None:
            failures.append(drift_failure)

        if failures:
            for failure in failures:
                report_finding(self.name, None, failure)
            print(f"FAIL [{self._name}] — agent harness has drifted from the shared canon:")
            for failure in failures:
                print(f"  - {failure}")
            print()
            print(self.remediation)
            return 1

        arms = "presence, reference" + (", drift" if self.banner_path is not None else "")
        print(f"ok [{self._name}] — harness references the shared canon (arms checked: {arms}).")
        return 0

    def xǁHarnessCanonReferenceǁrun__mutmut_18(self) -> int:
        """Drive the three arms; FAIL (1) on any drift, else PASS (0)."""
        failures: list[str] = []

        for label in missing_required_groups(self._repo_root, self._requirement_groups()):
            failures.append(f"missing required harness entrypoint: {label}")

        harness_texts = self._harness_texts()
        reference_failure = self._reference_failure(harness_texts)
        if reference_failure is not None:
            failures.append(reference_failure)

        drift_failure = self._drift_failure(harness_texts)
        if drift_failure is not None:
            failures.append(drift_failure)

        if failures:
            for failure in failures:
                report_finding(self.name, ".", None)
            print(f"FAIL [{self._name}] — agent harness has drifted from the shared canon:")
            for failure in failures:
                print(f"  - {failure}")
            print()
            print(self.remediation)
            return 1

        arms = "presence, reference" + (", drift" if self.banner_path is not None else "")
        print(f"ok [{self._name}] — harness references the shared canon (arms checked: {arms}).")
        return 0

    def xǁHarnessCanonReferenceǁrun__mutmut_19(self) -> int:
        """Drive the three arms; FAIL (1) on any drift, else PASS (0)."""
        failures: list[str] = []

        for label in missing_required_groups(self._repo_root, self._requirement_groups()):
            failures.append(f"missing required harness entrypoint: {label}")

        harness_texts = self._harness_texts()
        reference_failure = self._reference_failure(harness_texts)
        if reference_failure is not None:
            failures.append(reference_failure)

        drift_failure = self._drift_failure(harness_texts)
        if drift_failure is not None:
            failures.append(drift_failure)

        if failures:
            for failure in failures:
                report_finding(".", failure)
            print(f"FAIL [{self._name}] — agent harness has drifted from the shared canon:")
            for failure in failures:
                print(f"  - {failure}")
            print()
            print(self.remediation)
            return 1

        arms = "presence, reference" + (", drift" if self.banner_path is not None else "")
        print(f"ok [{self._name}] — harness references the shared canon (arms checked: {arms}).")
        return 0

    def xǁHarnessCanonReferenceǁrun__mutmut_20(self) -> int:
        """Drive the three arms; FAIL (1) on any drift, else PASS (0)."""
        failures: list[str] = []

        for label in missing_required_groups(self._repo_root, self._requirement_groups()):
            failures.append(f"missing required harness entrypoint: {label}")

        harness_texts = self._harness_texts()
        reference_failure = self._reference_failure(harness_texts)
        if reference_failure is not None:
            failures.append(reference_failure)

        drift_failure = self._drift_failure(harness_texts)
        if drift_failure is not None:
            failures.append(drift_failure)

        if failures:
            for failure in failures:
                report_finding(self.name, failure)
            print(f"FAIL [{self._name}] — agent harness has drifted from the shared canon:")
            for failure in failures:
                print(f"  - {failure}")
            print()
            print(self.remediation)
            return 1

        arms = "presence, reference" + (", drift" if self.banner_path is not None else "")
        print(f"ok [{self._name}] — harness references the shared canon (arms checked: {arms}).")
        return 0

    def xǁHarnessCanonReferenceǁrun__mutmut_21(self) -> int:
        """Drive the three arms; FAIL (1) on any drift, else PASS (0)."""
        failures: list[str] = []

        for label in missing_required_groups(self._repo_root, self._requirement_groups()):
            failures.append(f"missing required harness entrypoint: {label}")

        harness_texts = self._harness_texts()
        reference_failure = self._reference_failure(harness_texts)
        if reference_failure is not None:
            failures.append(reference_failure)

        drift_failure = self._drift_failure(harness_texts)
        if drift_failure is not None:
            failures.append(drift_failure)

        if failures:
            for failure in failures:
                report_finding(self.name, ".", )
            print(f"FAIL [{self._name}] — agent harness has drifted from the shared canon:")
            for failure in failures:
                print(f"  - {failure}")
            print()
            print(self.remediation)
            return 1

        arms = "presence, reference" + (", drift" if self.banner_path is not None else "")
        print(f"ok [{self._name}] — harness references the shared canon (arms checked: {arms}).")
        return 0

    def xǁHarnessCanonReferenceǁrun__mutmut_22(self) -> int:
        """Drive the three arms; FAIL (1) on any drift, else PASS (0)."""
        failures: list[str] = []

        for label in missing_required_groups(self._repo_root, self._requirement_groups()):
            failures.append(f"missing required harness entrypoint: {label}")

        harness_texts = self._harness_texts()
        reference_failure = self._reference_failure(harness_texts)
        if reference_failure is not None:
            failures.append(reference_failure)

        drift_failure = self._drift_failure(harness_texts)
        if drift_failure is not None:
            failures.append(drift_failure)

        if failures:
            for failure in failures:
                report_finding(self.name, "XX.XX", failure)
            print(f"FAIL [{self._name}] — agent harness has drifted from the shared canon:")
            for failure in failures:
                print(f"  - {failure}")
            print()
            print(self.remediation)
            return 1

        arms = "presence, reference" + (", drift" if self.banner_path is not None else "")
        print(f"ok [{self._name}] — harness references the shared canon (arms checked: {arms}).")
        return 0

    def xǁHarnessCanonReferenceǁrun__mutmut_23(self) -> int:
        """Drive the three arms; FAIL (1) on any drift, else PASS (0)."""
        failures: list[str] = []

        for label in missing_required_groups(self._repo_root, self._requirement_groups()):
            failures.append(f"missing required harness entrypoint: {label}")

        harness_texts = self._harness_texts()
        reference_failure = self._reference_failure(harness_texts)
        if reference_failure is not None:
            failures.append(reference_failure)

        drift_failure = self._drift_failure(harness_texts)
        if drift_failure is not None:
            failures.append(drift_failure)

        if failures:
            for failure in failures:
                report_finding(self.name, ".", failure)
            print(None)
            for failure in failures:
                print(f"  - {failure}")
            print()
            print(self.remediation)
            return 1

        arms = "presence, reference" + (", drift" if self.banner_path is not None else "")
        print(f"ok [{self._name}] — harness references the shared canon (arms checked: {arms}).")
        return 0

    def xǁHarnessCanonReferenceǁrun__mutmut_24(self) -> int:
        """Drive the three arms; FAIL (1) on any drift, else PASS (0)."""
        failures: list[str] = []

        for label in missing_required_groups(self._repo_root, self._requirement_groups()):
            failures.append(f"missing required harness entrypoint: {label}")

        harness_texts = self._harness_texts()
        reference_failure = self._reference_failure(harness_texts)
        if reference_failure is not None:
            failures.append(reference_failure)

        drift_failure = self._drift_failure(harness_texts)
        if drift_failure is not None:
            failures.append(drift_failure)

        if failures:
            for failure in failures:
                report_finding(self.name, ".", failure)
            print(f"FAIL [{self._name}] — agent harness has drifted from the shared canon:")
            for failure in failures:
                print(None)
            print()
            print(self.remediation)
            return 1

        arms = "presence, reference" + (", drift" if self.banner_path is not None else "")
        print(f"ok [{self._name}] — harness references the shared canon (arms checked: {arms}).")
        return 0

    def xǁHarnessCanonReferenceǁrun__mutmut_25(self) -> int:
        """Drive the three arms; FAIL (1) on any drift, else PASS (0)."""
        failures: list[str] = []

        for label in missing_required_groups(self._repo_root, self._requirement_groups()):
            failures.append(f"missing required harness entrypoint: {label}")

        harness_texts = self._harness_texts()
        reference_failure = self._reference_failure(harness_texts)
        if reference_failure is not None:
            failures.append(reference_failure)

        drift_failure = self._drift_failure(harness_texts)
        if drift_failure is not None:
            failures.append(drift_failure)

        if failures:
            for failure in failures:
                report_finding(self.name, ".", failure)
            print(f"FAIL [{self._name}] — agent harness has drifted from the shared canon:")
            for failure in failures:
                print(f"  - {failure}")
            print()
            print(None)
            return 1

        arms = "presence, reference" + (", drift" if self.banner_path is not None else "")
        print(f"ok [{self._name}] — harness references the shared canon (arms checked: {arms}).")
        return 0

    def xǁHarnessCanonReferenceǁrun__mutmut_26(self) -> int:
        """Drive the three arms; FAIL (1) on any drift, else PASS (0)."""
        failures: list[str] = []

        for label in missing_required_groups(self._repo_root, self._requirement_groups()):
            failures.append(f"missing required harness entrypoint: {label}")

        harness_texts = self._harness_texts()
        reference_failure = self._reference_failure(harness_texts)
        if reference_failure is not None:
            failures.append(reference_failure)

        drift_failure = self._drift_failure(harness_texts)
        if drift_failure is not None:
            failures.append(drift_failure)

        if failures:
            for failure in failures:
                report_finding(self.name, ".", failure)
            print(f"FAIL [{self._name}] — agent harness has drifted from the shared canon:")
            for failure in failures:
                print(f"  - {failure}")
            print()
            print(self.remediation)
            return 2

        arms = "presence, reference" + (", drift" if self.banner_path is not None else "")
        print(f"ok [{self._name}] — harness references the shared canon (arms checked: {arms}).")
        return 0

    def xǁHarnessCanonReferenceǁrun__mutmut_27(self) -> int:
        """Drive the three arms; FAIL (1) on any drift, else PASS (0)."""
        failures: list[str] = []

        for label in missing_required_groups(self._repo_root, self._requirement_groups()):
            failures.append(f"missing required harness entrypoint: {label}")

        harness_texts = self._harness_texts()
        reference_failure = self._reference_failure(harness_texts)
        if reference_failure is not None:
            failures.append(reference_failure)

        drift_failure = self._drift_failure(harness_texts)
        if drift_failure is not None:
            failures.append(drift_failure)

        if failures:
            for failure in failures:
                report_finding(self.name, ".", failure)
            print(f"FAIL [{self._name}] — agent harness has drifted from the shared canon:")
            for failure in failures:
                print(f"  - {failure}")
            print()
            print(self.remediation)
            return 1

        arms = None
        print(f"ok [{self._name}] — harness references the shared canon (arms checked: {arms}).")
        return 0

    def xǁHarnessCanonReferenceǁrun__mutmut_28(self) -> int:
        """Drive the three arms; FAIL (1) on any drift, else PASS (0)."""
        failures: list[str] = []

        for label in missing_required_groups(self._repo_root, self._requirement_groups()):
            failures.append(f"missing required harness entrypoint: {label}")

        harness_texts = self._harness_texts()
        reference_failure = self._reference_failure(harness_texts)
        if reference_failure is not None:
            failures.append(reference_failure)

        drift_failure = self._drift_failure(harness_texts)
        if drift_failure is not None:
            failures.append(drift_failure)

        if failures:
            for failure in failures:
                report_finding(self.name, ".", failure)
            print(f"FAIL [{self._name}] — agent harness has drifted from the shared canon:")
            for failure in failures:
                print(f"  - {failure}")
            print()
            print(self.remediation)
            return 1

        arms = "presence, reference" - (", drift" if self.banner_path is not None else "")
        print(f"ok [{self._name}] — harness references the shared canon (arms checked: {arms}).")
        return 0

    def xǁHarnessCanonReferenceǁrun__mutmut_29(self) -> int:
        """Drive the three arms; FAIL (1) on any drift, else PASS (0)."""
        failures: list[str] = []

        for label in missing_required_groups(self._repo_root, self._requirement_groups()):
            failures.append(f"missing required harness entrypoint: {label}")

        harness_texts = self._harness_texts()
        reference_failure = self._reference_failure(harness_texts)
        if reference_failure is not None:
            failures.append(reference_failure)

        drift_failure = self._drift_failure(harness_texts)
        if drift_failure is not None:
            failures.append(drift_failure)

        if failures:
            for failure in failures:
                report_finding(self.name, ".", failure)
            print(f"FAIL [{self._name}] — agent harness has drifted from the shared canon:")
            for failure in failures:
                print(f"  - {failure}")
            print()
            print(self.remediation)
            return 1

        arms = "XXpresence, referenceXX" + (", drift" if self.banner_path is not None else "")
        print(f"ok [{self._name}] — harness references the shared canon (arms checked: {arms}).")
        return 0

    def xǁHarnessCanonReferenceǁrun__mutmut_30(self) -> int:
        """Drive the three arms; FAIL (1) on any drift, else PASS (0)."""
        failures: list[str] = []

        for label in missing_required_groups(self._repo_root, self._requirement_groups()):
            failures.append(f"missing required harness entrypoint: {label}")

        harness_texts = self._harness_texts()
        reference_failure = self._reference_failure(harness_texts)
        if reference_failure is not None:
            failures.append(reference_failure)

        drift_failure = self._drift_failure(harness_texts)
        if drift_failure is not None:
            failures.append(drift_failure)

        if failures:
            for failure in failures:
                report_finding(self.name, ".", failure)
            print(f"FAIL [{self._name}] — agent harness has drifted from the shared canon:")
            for failure in failures:
                print(f"  - {failure}")
            print()
            print(self.remediation)
            return 1

        arms = "PRESENCE, REFERENCE" + (", drift" if self.banner_path is not None else "")
        print(f"ok [{self._name}] — harness references the shared canon (arms checked: {arms}).")
        return 0

    def xǁHarnessCanonReferenceǁrun__mutmut_31(self) -> int:
        """Drive the three arms; FAIL (1) on any drift, else PASS (0)."""
        failures: list[str] = []

        for label in missing_required_groups(self._repo_root, self._requirement_groups()):
            failures.append(f"missing required harness entrypoint: {label}")

        harness_texts = self._harness_texts()
        reference_failure = self._reference_failure(harness_texts)
        if reference_failure is not None:
            failures.append(reference_failure)

        drift_failure = self._drift_failure(harness_texts)
        if drift_failure is not None:
            failures.append(drift_failure)

        if failures:
            for failure in failures:
                report_finding(self.name, ".", failure)
            print(f"FAIL [{self._name}] — agent harness has drifted from the shared canon:")
            for failure in failures:
                print(f"  - {failure}")
            print()
            print(self.remediation)
            return 1

        arms = "presence, reference" + ("XX, driftXX" if self.banner_path is not None else "")
        print(f"ok [{self._name}] — harness references the shared canon (arms checked: {arms}).")
        return 0

    def xǁHarnessCanonReferenceǁrun__mutmut_32(self) -> int:
        """Drive the three arms; FAIL (1) on any drift, else PASS (0)."""
        failures: list[str] = []

        for label in missing_required_groups(self._repo_root, self._requirement_groups()):
            failures.append(f"missing required harness entrypoint: {label}")

        harness_texts = self._harness_texts()
        reference_failure = self._reference_failure(harness_texts)
        if reference_failure is not None:
            failures.append(reference_failure)

        drift_failure = self._drift_failure(harness_texts)
        if drift_failure is not None:
            failures.append(drift_failure)

        if failures:
            for failure in failures:
                report_finding(self.name, ".", failure)
            print(f"FAIL [{self._name}] — agent harness has drifted from the shared canon:")
            for failure in failures:
                print(f"  - {failure}")
            print()
            print(self.remediation)
            return 1

        arms = "presence, reference" + (", DRIFT" if self.banner_path is not None else "")
        print(f"ok [{self._name}] — harness references the shared canon (arms checked: {arms}).")
        return 0

    def xǁHarnessCanonReferenceǁrun__mutmut_33(self) -> int:
        """Drive the three arms; FAIL (1) on any drift, else PASS (0)."""
        failures: list[str] = []

        for label in missing_required_groups(self._repo_root, self._requirement_groups()):
            failures.append(f"missing required harness entrypoint: {label}")

        harness_texts = self._harness_texts()
        reference_failure = self._reference_failure(harness_texts)
        if reference_failure is not None:
            failures.append(reference_failure)

        drift_failure = self._drift_failure(harness_texts)
        if drift_failure is not None:
            failures.append(drift_failure)

        if failures:
            for failure in failures:
                report_finding(self.name, ".", failure)
            print(f"FAIL [{self._name}] — agent harness has drifted from the shared canon:")
            for failure in failures:
                print(f"  - {failure}")
            print()
            print(self.remediation)
            return 1

        arms = "presence, reference" + (", drift" if self.banner_path is None else "")
        print(f"ok [{self._name}] — harness references the shared canon (arms checked: {arms}).")
        return 0

    def xǁHarnessCanonReferenceǁrun__mutmut_34(self) -> int:
        """Drive the three arms; FAIL (1) on any drift, else PASS (0)."""
        failures: list[str] = []

        for label in missing_required_groups(self._repo_root, self._requirement_groups()):
            failures.append(f"missing required harness entrypoint: {label}")

        harness_texts = self._harness_texts()
        reference_failure = self._reference_failure(harness_texts)
        if reference_failure is not None:
            failures.append(reference_failure)

        drift_failure = self._drift_failure(harness_texts)
        if drift_failure is not None:
            failures.append(drift_failure)

        if failures:
            for failure in failures:
                report_finding(self.name, ".", failure)
            print(f"FAIL [{self._name}] — agent harness has drifted from the shared canon:")
            for failure in failures:
                print(f"  - {failure}")
            print()
            print(self.remediation)
            return 1

        arms = "presence, reference" + (", drift" if self.banner_path is not None else "XXXX")
        print(f"ok [{self._name}] — harness references the shared canon (arms checked: {arms}).")
        return 0

    def xǁHarnessCanonReferenceǁrun__mutmut_35(self) -> int:
        """Drive the three arms; FAIL (1) on any drift, else PASS (0)."""
        failures: list[str] = []

        for label in missing_required_groups(self._repo_root, self._requirement_groups()):
            failures.append(f"missing required harness entrypoint: {label}")

        harness_texts = self._harness_texts()
        reference_failure = self._reference_failure(harness_texts)
        if reference_failure is not None:
            failures.append(reference_failure)

        drift_failure = self._drift_failure(harness_texts)
        if drift_failure is not None:
            failures.append(drift_failure)

        if failures:
            for failure in failures:
                report_finding(self.name, ".", failure)
            print(f"FAIL [{self._name}] — agent harness has drifted from the shared canon:")
            for failure in failures:
                print(f"  - {failure}")
            print()
            print(self.remediation)
            return 1

        arms = "presence, reference" + (", drift" if self.banner_path is not None else "")
        print(None)
        return 0

    def xǁHarnessCanonReferenceǁrun__mutmut_36(self) -> int:
        """Drive the three arms; FAIL (1) on any drift, else PASS (0)."""
        failures: list[str] = []

        for label in missing_required_groups(self._repo_root, self._requirement_groups()):
            failures.append(f"missing required harness entrypoint: {label}")

        harness_texts = self._harness_texts()
        reference_failure = self._reference_failure(harness_texts)
        if reference_failure is not None:
            failures.append(reference_failure)

        drift_failure = self._drift_failure(harness_texts)
        if drift_failure is not None:
            failures.append(drift_failure)

        if failures:
            for failure in failures:
                report_finding(self.name, ".", failure)
            print(f"FAIL [{self._name}] — agent harness has drifted from the shared canon:")
            for failure in failures:
                print(f"  - {failure}")
            print()
            print(self.remediation)
            return 1

        arms = "presence, reference" + (", drift" if self.banner_path is not None else "")
        print(f"ok [{self._name}] — harness references the shared canon (arms checked: {arms}).")
        return 1

mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['_mutmut_orig'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_1'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_2'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_3'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_4'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_5'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_6'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_7'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_8'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_9'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_10'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_11'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_12'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_12 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_13'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_13 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_14'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_14 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_15'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_15 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_16'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_16 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_17'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_17 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_18'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_18 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_19'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_19 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_20'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_20 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_21'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_21 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_22'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_22 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_23'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_23 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_24'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_24 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_25'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_25 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_26'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_26 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_27'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_27 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_28'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_28 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_29'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_29 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_30'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_30 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_31'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_31 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_32'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_32 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_33'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_33 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_34'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_34 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_35'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_35 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_36'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_36 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_37'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_37 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_38'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_38 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_39'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_39 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_40'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_40 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_41'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_41 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_42'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_42 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_43'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_43 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfrom_config__mutmut['xǁHarnessCanonReferenceǁfrom_config__mutmut_44'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfrom_config__mutmut_44 # type: ignore # mutmut generated

mutants_xǁHarnessCanonReferenceǁfile_has_violation__mutmut['_mutmut_orig'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁfile_has_violation__mutmut['xǁHarnessCanonReferenceǁfile_has_violation__mutmut_1'] = HarnessCanonReference.xǁHarnessCanonReferenceǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated

mutants_xǁHarnessCanonReferenceǁ_requirement_groups__mutmut['_mutmut_orig'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_requirement_groups__mutmut_orig # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_requirement_groups__mutmut['xǁHarnessCanonReferenceǁ_requirement_groups__mutmut_1'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_requirement_groups__mutmut_1 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_requirement_groups__mutmut['xǁHarnessCanonReferenceǁ_requirement_groups__mutmut_2'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_requirement_groups__mutmut_2 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_requirement_groups__mutmut['xǁHarnessCanonReferenceǁ_requirement_groups__mutmut_3'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_requirement_groups__mutmut_3 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_requirement_groups__mutmut['xǁHarnessCanonReferenceǁ_requirement_groups__mutmut_4'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_requirement_groups__mutmut_4 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_requirement_groups__mutmut['xǁHarnessCanonReferenceǁ_requirement_groups__mutmut_5'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_requirement_groups__mutmut_5 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_requirement_groups__mutmut['xǁHarnessCanonReferenceǁ_requirement_groups__mutmut_6'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_requirement_groups__mutmut_6 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_requirement_groups__mutmut['xǁHarnessCanonReferenceǁ_requirement_groups__mutmut_7'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_requirement_groups__mutmut_7 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_requirement_groups__mutmut['xǁHarnessCanonReferenceǁ_requirement_groups__mutmut_8'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_requirement_groups__mutmut_8 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_requirement_groups__mutmut['xǁHarnessCanonReferenceǁ_requirement_groups__mutmut_9'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_requirement_groups__mutmut_9 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_requirement_groups__mutmut['xǁHarnessCanonReferenceǁ_requirement_groups__mutmut_10'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_requirement_groups__mutmut_10 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_requirement_groups__mutmut['xǁHarnessCanonReferenceǁ_requirement_groups__mutmut_11'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_requirement_groups__mutmut_11 # type: ignore # mutmut generated

mutants_xǁHarnessCanonReferenceǁ_harness_texts__mutmut['_mutmut_orig'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_harness_texts__mutmut_orig # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_harness_texts__mutmut['xǁHarnessCanonReferenceǁ_harness_texts__mutmut_1'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_harness_texts__mutmut_1 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_harness_texts__mutmut['xǁHarnessCanonReferenceǁ_harness_texts__mutmut_2'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_harness_texts__mutmut_2 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_harness_texts__mutmut['xǁHarnessCanonReferenceǁ_harness_texts__mutmut_3'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_harness_texts__mutmut_3 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_harness_texts__mutmut['xǁHarnessCanonReferenceǁ_harness_texts__mutmut_4'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_harness_texts__mutmut_4 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_harness_texts__mutmut['xǁHarnessCanonReferenceǁ_harness_texts__mutmut_5'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_harness_texts__mutmut_5 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_harness_texts__mutmut['xǁHarnessCanonReferenceǁ_harness_texts__mutmut_6'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_harness_texts__mutmut_6 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_harness_texts__mutmut['xǁHarnessCanonReferenceǁ_harness_texts__mutmut_7'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_harness_texts__mutmut_7 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_harness_texts__mutmut['xǁHarnessCanonReferenceǁ_harness_texts__mutmut_8'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_harness_texts__mutmut_8 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_harness_texts__mutmut['xǁHarnessCanonReferenceǁ_harness_texts__mutmut_9'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_harness_texts__mutmut_9 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_harness_texts__mutmut['xǁHarnessCanonReferenceǁ_harness_texts__mutmut_10'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_harness_texts__mutmut_10 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_harness_texts__mutmut['xǁHarnessCanonReferenceǁ_harness_texts__mutmut_11'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_harness_texts__mutmut_11 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_harness_texts__mutmut['xǁHarnessCanonReferenceǁ_harness_texts__mutmut_12'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_harness_texts__mutmut_12 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_harness_texts__mutmut['xǁHarnessCanonReferenceǁ_harness_texts__mutmut_13'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_harness_texts__mutmut_13 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_harness_texts__mutmut['xǁHarnessCanonReferenceǁ_harness_texts__mutmut_14'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_harness_texts__mutmut_14 # type: ignore # mutmut generated

mutants_xǁHarnessCanonReferenceǁ_reference_failure__mutmut['_mutmut_orig'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_reference_failure__mutmut_orig # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_reference_failure__mutmut['xǁHarnessCanonReferenceǁ_reference_failure__mutmut_1'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_reference_failure__mutmut_1 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_reference_failure__mutmut['xǁHarnessCanonReferenceǁ_reference_failure__mutmut_2'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_reference_failure__mutmut_2 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_reference_failure__mutmut['xǁHarnessCanonReferenceǁ_reference_failure__mutmut_3'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_reference_failure__mutmut_3 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_reference_failure__mutmut['xǁHarnessCanonReferenceǁ_reference_failure__mutmut_4'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_reference_failure__mutmut_4 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_reference_failure__mutmut['xǁHarnessCanonReferenceǁ_reference_failure__mutmut_5'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_reference_failure__mutmut_5 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_reference_failure__mutmut['xǁHarnessCanonReferenceǁ_reference_failure__mutmut_6'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_reference_failure__mutmut_6 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_reference_failure__mutmut['xǁHarnessCanonReferenceǁ_reference_failure__mutmut_7'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_reference_failure__mutmut_7 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_reference_failure__mutmut['xǁHarnessCanonReferenceǁ_reference_failure__mutmut_8'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_reference_failure__mutmut_8 # type: ignore # mutmut generated

mutants_xǁHarnessCanonReferenceǁ_drift_failure__mutmut['_mutmut_orig'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_drift_failure__mutmut_orig # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_drift_failure__mutmut['xǁHarnessCanonReferenceǁ_drift_failure__mutmut_1'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_drift_failure__mutmut_1 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_drift_failure__mutmut['xǁHarnessCanonReferenceǁ_drift_failure__mutmut_2'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_drift_failure__mutmut_2 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_drift_failure__mutmut['xǁHarnessCanonReferenceǁ_drift_failure__mutmut_3'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_drift_failure__mutmut_3 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_drift_failure__mutmut['xǁHarnessCanonReferenceǁ_drift_failure__mutmut_4'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_drift_failure__mutmut_4 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_drift_failure__mutmut['xǁHarnessCanonReferenceǁ_drift_failure__mutmut_5'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_drift_failure__mutmut_5 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_drift_failure__mutmut['xǁHarnessCanonReferenceǁ_drift_failure__mutmut_6'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_drift_failure__mutmut_6 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_drift_failure__mutmut['xǁHarnessCanonReferenceǁ_drift_failure__mutmut_7'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_drift_failure__mutmut_7 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_drift_failure__mutmut['xǁHarnessCanonReferenceǁ_drift_failure__mutmut_8'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_drift_failure__mutmut_8 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_drift_failure__mutmut['xǁHarnessCanonReferenceǁ_drift_failure__mutmut_9'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_drift_failure__mutmut_9 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_drift_failure__mutmut['xǁHarnessCanonReferenceǁ_drift_failure__mutmut_10'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_drift_failure__mutmut_10 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_drift_failure__mutmut['xǁHarnessCanonReferenceǁ_drift_failure__mutmut_11'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_drift_failure__mutmut_11 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁ_drift_failure__mutmut['xǁHarnessCanonReferenceǁ_drift_failure__mutmut_12'] = HarnessCanonReference.xǁHarnessCanonReferenceǁ_drift_failure__mutmut_12 # type: ignore # mutmut generated

mutants_xǁHarnessCanonReferenceǁrun__mutmut['_mutmut_orig'] = HarnessCanonReference.xǁHarnessCanonReferenceǁrun__mutmut_orig # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁrun__mutmut['xǁHarnessCanonReferenceǁrun__mutmut_1'] = HarnessCanonReference.xǁHarnessCanonReferenceǁrun__mutmut_1 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁrun__mutmut['xǁHarnessCanonReferenceǁrun__mutmut_2'] = HarnessCanonReference.xǁHarnessCanonReferenceǁrun__mutmut_2 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁrun__mutmut['xǁHarnessCanonReferenceǁrun__mutmut_3'] = HarnessCanonReference.xǁHarnessCanonReferenceǁrun__mutmut_3 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁrun__mutmut['xǁHarnessCanonReferenceǁrun__mutmut_4'] = HarnessCanonReference.xǁHarnessCanonReferenceǁrun__mutmut_4 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁrun__mutmut['xǁHarnessCanonReferenceǁrun__mutmut_5'] = HarnessCanonReference.xǁHarnessCanonReferenceǁrun__mutmut_5 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁrun__mutmut['xǁHarnessCanonReferenceǁrun__mutmut_6'] = HarnessCanonReference.xǁHarnessCanonReferenceǁrun__mutmut_6 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁrun__mutmut['xǁHarnessCanonReferenceǁrun__mutmut_7'] = HarnessCanonReference.xǁHarnessCanonReferenceǁrun__mutmut_7 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁrun__mutmut['xǁHarnessCanonReferenceǁrun__mutmut_8'] = HarnessCanonReference.xǁHarnessCanonReferenceǁrun__mutmut_8 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁrun__mutmut['xǁHarnessCanonReferenceǁrun__mutmut_9'] = HarnessCanonReference.xǁHarnessCanonReferenceǁrun__mutmut_9 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁrun__mutmut['xǁHarnessCanonReferenceǁrun__mutmut_10'] = HarnessCanonReference.xǁHarnessCanonReferenceǁrun__mutmut_10 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁrun__mutmut['xǁHarnessCanonReferenceǁrun__mutmut_11'] = HarnessCanonReference.xǁHarnessCanonReferenceǁrun__mutmut_11 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁrun__mutmut['xǁHarnessCanonReferenceǁrun__mutmut_12'] = HarnessCanonReference.xǁHarnessCanonReferenceǁrun__mutmut_12 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁrun__mutmut['xǁHarnessCanonReferenceǁrun__mutmut_13'] = HarnessCanonReference.xǁHarnessCanonReferenceǁrun__mutmut_13 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁrun__mutmut['xǁHarnessCanonReferenceǁrun__mutmut_14'] = HarnessCanonReference.xǁHarnessCanonReferenceǁrun__mutmut_14 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁrun__mutmut['xǁHarnessCanonReferenceǁrun__mutmut_15'] = HarnessCanonReference.xǁHarnessCanonReferenceǁrun__mutmut_15 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁrun__mutmut['xǁHarnessCanonReferenceǁrun__mutmut_16'] = HarnessCanonReference.xǁHarnessCanonReferenceǁrun__mutmut_16 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁrun__mutmut['xǁHarnessCanonReferenceǁrun__mutmut_17'] = HarnessCanonReference.xǁHarnessCanonReferenceǁrun__mutmut_17 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁrun__mutmut['xǁHarnessCanonReferenceǁrun__mutmut_18'] = HarnessCanonReference.xǁHarnessCanonReferenceǁrun__mutmut_18 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁrun__mutmut['xǁHarnessCanonReferenceǁrun__mutmut_19'] = HarnessCanonReference.xǁHarnessCanonReferenceǁrun__mutmut_19 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁrun__mutmut['xǁHarnessCanonReferenceǁrun__mutmut_20'] = HarnessCanonReference.xǁHarnessCanonReferenceǁrun__mutmut_20 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁrun__mutmut['xǁHarnessCanonReferenceǁrun__mutmut_21'] = HarnessCanonReference.xǁHarnessCanonReferenceǁrun__mutmut_21 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁrun__mutmut['xǁHarnessCanonReferenceǁrun__mutmut_22'] = HarnessCanonReference.xǁHarnessCanonReferenceǁrun__mutmut_22 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁrun__mutmut['xǁHarnessCanonReferenceǁrun__mutmut_23'] = HarnessCanonReference.xǁHarnessCanonReferenceǁrun__mutmut_23 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁrun__mutmut['xǁHarnessCanonReferenceǁrun__mutmut_24'] = HarnessCanonReference.xǁHarnessCanonReferenceǁrun__mutmut_24 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁrun__mutmut['xǁHarnessCanonReferenceǁrun__mutmut_25'] = HarnessCanonReference.xǁHarnessCanonReferenceǁrun__mutmut_25 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁrun__mutmut['xǁHarnessCanonReferenceǁrun__mutmut_26'] = HarnessCanonReference.xǁHarnessCanonReferenceǁrun__mutmut_26 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁrun__mutmut['xǁHarnessCanonReferenceǁrun__mutmut_27'] = HarnessCanonReference.xǁHarnessCanonReferenceǁrun__mutmut_27 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁrun__mutmut['xǁHarnessCanonReferenceǁrun__mutmut_28'] = HarnessCanonReference.xǁHarnessCanonReferenceǁrun__mutmut_28 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁrun__mutmut['xǁHarnessCanonReferenceǁrun__mutmut_29'] = HarnessCanonReference.xǁHarnessCanonReferenceǁrun__mutmut_29 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁrun__mutmut['xǁHarnessCanonReferenceǁrun__mutmut_30'] = HarnessCanonReference.xǁHarnessCanonReferenceǁrun__mutmut_30 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁrun__mutmut['xǁHarnessCanonReferenceǁrun__mutmut_31'] = HarnessCanonReference.xǁHarnessCanonReferenceǁrun__mutmut_31 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁrun__mutmut['xǁHarnessCanonReferenceǁrun__mutmut_32'] = HarnessCanonReference.xǁHarnessCanonReferenceǁrun__mutmut_32 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁrun__mutmut['xǁHarnessCanonReferenceǁrun__mutmut_33'] = HarnessCanonReference.xǁHarnessCanonReferenceǁrun__mutmut_33 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁrun__mutmut['xǁHarnessCanonReferenceǁrun__mutmut_34'] = HarnessCanonReference.xǁHarnessCanonReferenceǁrun__mutmut_34 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁrun__mutmut['xǁHarnessCanonReferenceǁrun__mutmut_35'] = HarnessCanonReference.xǁHarnessCanonReferenceǁrun__mutmut_35 # type: ignore # mutmut generated
mutants_xǁHarnessCanonReferenceǁrun__mutmut['xǁHarnessCanonReferenceǁrun__mutmut_36'] = HarnessCanonReference.xǁHarnessCanonReferenceǁrun__mutmut_36 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> HarnessCanonReference:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return HarnessCanonReference.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> HarnessCanonReference:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return HarnessCanonReference.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> HarnessCanonReference:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return HarnessCanonReference.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> HarnessCanonReference:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return HarnessCanonReference.from_config(config, repo_root=None)


def x_build__mutmut_3(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> HarnessCanonReference:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return HarnessCanonReference.from_config(repo_root=repo_root)


def x_build__mutmut_4(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> HarnessCanonReference:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return HarnessCanonReference.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(HarnessCanonReference, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(HarnessCanonReference, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(HarnessCanonReference, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(HarnessCanonReference, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
