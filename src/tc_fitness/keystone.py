"""Keystone drift-enders for catalogue integrity and Git change discovery.

:func:`catalogue_check_consistency` (lifted from kairix F92) ensures every
  ``RuleEntry`` in a consumer's catalogue resolves to a real check, AND every
  check the consumer ships is cataloged. Bidirectional: no orphan checks, no
  dangling entries.
"""

from __future__ import annotations

import subprocess
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from pathlib import Path


def staged_added_files(repo_root: Path) -> list[str]:
    """Repo-relative paths ADDED in the current staged diff (pre-commit mode)."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=A"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def added_since_tag(repo_root: Path, tag: str) -> list[str]:
    """Repo-relative paths ADDED between ``tag`` and HEAD (CI full-PR mode)."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=A", f"{tag}..HEAD"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def resolve_previous_tag(
    repo_root: Path,
    *,
    match_glob: str = "v[0-9]*.[0-9]*.[0-9]*",
) -> str | None:
    """Most recent release tag strictly older than HEAD, or ``None``.

    ``match_glob`` is CONFIG — a repo using ``v2026.5.18`` and a repo using
    ``v0.6.0`` both work by passing their own glob. ``None`` means "no prior
    tag" (first release → the shrink check is a clean skip).
    """
    result = subprocess.run(
        ["git", "describe", "--tags", "--abbrev=0", "--match", match_glob, "HEAD^"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


# ===========================================================================
# catalogue_check_consistency  (kairix F92, invariants a + b)
# ===========================================================================


@dataclass(frozen=True)
class CatalogueConsistencyReport:
    """Bidirectional catalogue ↔ checks reconciliation result."""

    orphan_checks: list[str]
    dangling_entries: list[tuple[str, str]]

    @property
    def ok(self) -> bool:
        return not self.orphan_checks and not self.dangling_entries


def reconcile_catalogue(
    *,
    cataloged_check_ids: Iterable[str],
    available_check_ids: Iterable[str],
) -> CatalogueConsistencyReport:
    """Reconcile the cataloged check ids against the checks that actually exist.

    * **orphan_checks** — a check the consumer ships that NO catalogue entry
      references (it runs but nothing documents what it protects).
    * **dangling_entries** — a catalogue entry referencing a check that does
      NOT exist (the runner would mis-dispatch).

    Both id sets are CONFIG: the consumer resolves "what does my catalogue
    reference" and "what checks exist" however its layout dictates (CORE
    ``core:<module>`` ids, local ``check_*.py`` filenames, …). The engine only
    diffs the two sets — fully repo-agnostic.
    """
    cataloged = set(cataloged_check_ids)
    available = set(available_check_ids)
    orphans = sorted(available - cataloged)
    dangling = sorted((cid, cid) for cid in (cataloged - available))
    return CatalogueConsistencyReport(
        orphan_checks=orphans,
        dangling_entries=[(eid, cid) for eid, cid in dangling],
    )


def catalogue_check_consistency(
    *,
    cataloged_check_ids: Iterable[str],
    available_check_ids: Iterable[str],
    remediation: str = "",
    print_fn: Callable[[str], None] = print,
) -> int:
    """Gate: catalogue ↔ checks agree bidirectionally. ``0`` ok, ``1`` drift.

    Thin printing wrapper over :func:`reconcile_catalogue`. The consumer
    supplies both id sets and the ``remediation`` text.
    """
    report = reconcile_catalogue(
        cataloged_check_ids=cataloged_check_ids,
        available_check_ids=available_check_ids,
    )
    if report.ok:
        print_fn("catalogue_check_consistency: catalogue and checks agree.")
        return 0
    if report.orphan_checks:
        print_fn("FAIL catalogue_check_consistency — check(s) with no catalogue entry:")
        for name in report.orphan_checks:
            print_fn(f"  {name}")
    if report.dangling_entries:
        print_fn("FAIL catalogue_check_consistency — catalogue entr(ies) naming a missing check:")
        for entry_id, check_id in report.dangling_entries:
            print_fn(f"  {entry_id} -> {check_id}")
    if remediation:
        print_fn("")
        print_fn(remediation)
    return 1


__all__ = [
    "staged_added_files",
    "added_since_tag",
    "resolve_previous_tag",
    # catalogue consistency
    "CatalogueConsistencyReport",
    "reconcile_catalogue",
    "catalogue_check_consistency",
]
