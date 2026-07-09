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

Non-grandfatherable: a harness that references the wrong canon or omits an
entrypoint is a hard gate, not a per-file debt, so :meth:`run` drives the three
arms directly rather than ratcheting a violation set against a baseline (the
same posture as the deterministic-tests CORE check).

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


def has_canon_reference(texts: Iterable[str], *, marker: str, ref_pattern: re.Pattern[str]) -> bool:
    """True iff some text carries BOTH the canon marker AND a reference match.

    The marker and the reference link must co-occur in the SAME harness file — a
    stray marker in one file and a link in another does not prove that file names
    the canon.
    """
    return any(marker in text and ref_pattern.search(text) is not None for text in texts)


def normalise_banner(text: str) -> str:
    """Whitespace-normalise a banner block for a content (not layout) compare.

    Strips each line and drops blank lines, so indentation or blank-line reflow
    never reads as drift while a change to the banner's WORDS does.
    """
    return "\n".join(stripped for line in text.splitlines() if (stripped := line.strip()))


def banner_present(texts: Iterable[str], pinned: str) -> bool:
    """True iff the normalised pinned banner appears inside some harness text.

    An empty pin has nothing to drift from and is treated as present.
    """
    target = normalise_banner(pinned)
    if not target:
        return True
    return any(target in normalise_banner(text) for text in texts)


class HarnessCanonReference(FitnessRule):
    """Gate that FAILS when a repo's agent harness has drifted from the canon.

    Drives three arms (presence, reference, drift) directly in :meth:`run`; the
    per-file scan hooks are inert because harness drift is a hard repo-level gate,
    not a grandfatherable per-file debt.
    """

    name = "harness-canon-reference"
    remediation = REMEDIATION
    #: Not a file-scan rule — the enumeration hooks stay empty so the base
    #: --establish-baseline mode writes an empty baseline harmlessly.
    extensions = ()

    #: Rule-specific config (instance attrs; from_config overrides per consumer).
    repo_type: str = DEFAULT_REPO_TYPE
    required_files: tuple[str, ...] | None = None
    banner_marker: str = DEFAULT_BANNER_MARKER
    standards_ref_pattern: str = DEFAULT_STANDARDS_REF_PATTERN
    banner_path: str | None = None

    @classmethod
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

    def file_has_violation(self, path: Path) -> bool:  # pragma: no cover - not used
        """Unused: harness drift is a repo-level gate, not a per-file scan."""
        return False

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
            print(f"FAIL [{self._name}] — agent harness has drifted from the shared canon:")
            for failure in failures:
                print(f"  - {failure}")
            print()
            print(self.remediation)
            return 1

        arms = "presence, reference" + (", drift" if self.banner_path is not None else "")
        print(f"ok [{self._name}] — harness references the shared canon (arms checked: {arms}).")
        return 0


def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> HarnessCanonReference:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return HarnessCanonReference.from_config(config, repo_root=repo_root)


def main(argv: list[str] | None = None) -> int:
    """CLI entry — supports ``--establish-baseline`` and ``--repo-root``."""
    return run_core_check(HarnessCanonReference, argv)


if __name__ == "__main__":
    import sys

    sys.exit(main())
