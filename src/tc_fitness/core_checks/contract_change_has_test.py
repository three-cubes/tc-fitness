"""CORE check: contract_change_has_test — a contract-surface change needs a test.

A shared *contract-surface* file is the base every consumer INHERITS: its public
behaviour is depended on unseen across repos, so a change to it that no test
proves is the highest-blast-radius edit in the codebase. The v0.13.0 empty-roots
regression is the exact shape — the shared base changed, no test asserted the new
enumeration contract, and the break reached ``main`` and every consumer. This
rule mirrors that merge condition LOCALLY: given the PR's changed-file set, a
change that touches a contract-surface file but touches NO test file FAILs, so an
agent catches the missing-proof edit before the CI round-trip, not after.

The verdict is a property of the CHANGE SET, not of any file on disk:

* a changed file matches ``contract_surface`` AND no changed file matches
  ``test_globs`` → VIOLATION (each touched contract file is reported);
* a contract file changed AND a test changed → clean;
* no contract file changed → clean (a no-op — nothing to enforce).

Hard floor, by design. Like :mod:`new_code_coverage`, this rule is baseline-free:
a contract change landed without its proving test is a FRESH defect recomputed
against the merge-base on every branch, never inherited debt, so there is no
stable offender to grandfather (see :meth:`ContractChangeHasTest.establish_baseline`).

``contract_surface`` (globs; default the shared base), ``test_globs`` (globs;
default the test tree), and ``base_ref`` are CONFIG the consumer supplies;
nothing here names a repo or a threshold. The changed-file list is sourced the
same way :mod:`new_code_coverage` sources it — a ``git merge-base`` + ``git diff``
DI seam (a callable defaulting to :func:`subprocess.run`) — so the detector is
testable without a real repository.
"""

from __future__ import annotations

import re
import subprocess
from collections.abc import Callable, Mapping
from fnmatch import fnmatchcase
from functools import cached_property
from pathlib import Path
from typing import Any

from tc_fitness.baseline import establish_baseline as _establish_baseline
from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: The domain-intrinsic default contract surface — the shared config-driven base
#: every consumer inherits. Overridable per consumer via ``contract_surface``.
DEFAULT_CONTRACT_SURFACE: tuple[str, ...] = ("src/tc_fitness/fitness_rule.py",)

#: Default test-file globs. A change matching any of these is a companion test
#: touch that discharges the requirement. Overridable via ``test_globs``.
DEFAULT_TEST_GLOBS: tuple[str, ...] = ("tests/**",)

#: Default trunk ref the change set is measured against. The changed files are
#: the union of paths on the diff from the merge-base of this ref and HEAD.
DEFAULT_BASE_REF = "origin/main"

#: A git ref must match this before it is interpolated into a git argv — a
#: conservative allow-list of the characters a legitimate ref/revision carries
#: (refname chars plus the revision operators ``~ ^ @ { }``). Anything else is
#: treated as unresolvable → the rule SKIPs rather than shell-interpolating it.
_SAFE_REF_RE = re.compile(r"^[A-Za-z0-9_./@{}~^-]+$")

#: A git command runner: takes the git sub-arguments (argv0 ``git`` is fixed by
#: the runner, never the caller) and the working directory, returns the
#: completed process. The DI seam a test overrides to feed canned diff output.
GitRunner = Callable[[list[str], Path], "subprocess.CompletedProcess[str]"]

REMEDIATION = _remediation(
    fix=(
        "add or change a test alongside the contract-surface change — a shared base "
        "the whole fleet inherits must not shift its behaviour with nothing asserting "
        "the new contract. Ask what BEHAVIOUR the edit changes and write the test that "
        "pins it (the empty-roots regression was a one-line enumeration change no test "
        "covered). If the change is a pure comment/docstring edit with no behavioural "
        "surface, still touch the contract's test file to record that it was reviewed."
    ),
    nxt="re-run this check to confirm the change set carries a companion test change.",
    run="python -m tc_fitness.core_checks.contract_change_has_test",
    passing="edit fitness_rule.py AND its tests/test_fitness_rule.py in the same change",
    forbidden="change the shared contract surface with no test in the change set",
)


def _matches_any(rel: str, globs: tuple[str, ...]) -> bool:
    """True iff ``rel`` matches any glob in ``globs`` (case-sensitive, path-aware).

    Uses :func:`fnmatch.fnmatchcase` — deterministic across platforms (no
    ``os.path.normcase`` fold). ``*``/``**`` both match path separators, so a
    prefix glob such as ``tests/**`` matches every nested path under the tree.
    """
    return any(fnmatchcase(rel, pattern) for pattern in globs)


def _default_git_runner(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    """Run ``git <args>`` in ``cwd`` and capture its output (the default seam).

    argv0 is the fixed literal ``git`` (never a caller-supplied path) and
    ``shell`` is never used; the only caller-controlled token is the ref, which
    the rule validates against :data:`_SAFE_REF_RE` before it reaches here.
    """
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )


class ContractChangeHasTest(FitnessRule):
    """Flags a change that touches a contract surface but touches no test file."""

    name = "contract-change-has-test"
    remediation = REMEDIATION

    #: Rule-specific knobs — instance attrs so ``from_config`` overrides them.
    contract_surface: tuple[str, ...] = DEFAULT_CONTRACT_SURFACE
    test_globs: tuple[str, ...] = DEFAULT_TEST_GLOBS
    base_ref: str = DEFAULT_BASE_REF
    #: The git command runner (DI seam) — set by ``from_config`` / ``build`` so a
    #: test can inject canned diff output without a real repo or monkeypatching.
    git_runner: GitRunner

    @classmethod
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ContractChangeHasTest:
        """Build from config, also reading ``contract_surface`` / ``test_globs`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ContractChangeHasTest)  # noqa: S101  # narrowing for mypy
        surface = config.get("contract_surface")
        globs = config.get("test_globs")
        rule.contract_surface = tuple(surface) if surface is not None else DEFAULT_CONTRACT_SURFACE
        rule.test_globs = tuple(globs) if globs is not None else DEFAULT_TEST_GLOBS
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        return rule

    def _changed_files(self) -> list[str]:
        """Repo-relative paths changed since the merge-base of ``base_ref`` and HEAD.

        Returns ``[]`` (→ a soft PASS) when the base ref is unsafe/unresolvable,
        the merge-base can't be computed, or the diff command fails — none of
        which is a contract-coverage defect, so the gate stays quiet.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return []
        merge_base = self.git_runner(["merge-base", self.base_ref, "HEAD"], self._repo_root)
        if merge_base.returncode != 0:
            return []
        base = merge_base.stdout.strip()
        if not base:
            return []
        diff = self.git_runner(["diff", "--name-only", f"{base}...HEAD"], self._repo_root)
        if diff.returncode != 0:
            return []
        return [line.strip() for line in diff.stdout.splitlines() if line.strip()]

    @cached_property
    def _changed(self) -> list[str]:
        """The changed-file set, computed once per rule instance."""
        return self._changed_files()

    @cached_property
    def _test_touched(self) -> bool:
        """True iff at least one changed file matches ``test_globs``."""
        return any(_matches_any(rel, self.test_globs) for rel in self._changed)

    def is_in_scope(self, rel: str) -> bool:
        """Scope IS the contract-surface glob set — not an extension/root prefix.

        Overrides the default extension+root predicate: this rule's universe is
        the contract-surface globs the consumer declares, matched against the
        changed-file set, so scope is decided by :func:`_matches_any` alone.
        """
        return _matches_any(rel, self.contract_surface)

    def enumerate_files(self) -> list[Path]:
        """The changed contract-surface files, as repo-anchored paths.

        Overrides the default git-tracked walk: the rule's universe is the
        changed files (from the diff), not the on-disk tree. The contract-surface
        scope predicate is applied here and again in
        :meth:`FitnessRule.collect_violations` via :meth:`is_in_scope`.
        """
        return [self._repo_root / rel for rel in self._changed if self.is_in_scope(rel)]

    def file_has_violation(self, path: Path) -> bool:
        """True iff this contract file was changed with NO test file in the change set."""
        rel = str(self._repo_relative(path))
        if not self.is_in_scope(rel):
            return False
        return not self._test_touched

    def run(self) -> int:
        """Hard gate: a contract change with no companion test change FAILs.

        Modelling note: the base ``run()`` gates the violation set against a
        per-file baseline so a repo can freeze PRE-EXISTING offenders behind a
        ratchet. A missing-test-for-a-contract-change is different in KIND — the
        change set is recomputed against the merge-base on every branch, so there
        is no stable offender to freeze, and a contract file touched on THIS
        branch with no test is a fresh defect, never inherited debt. This
        override consults NO baseline and gates the raw violation set. Returns
        ``0`` when the change set is clean (or there is no contract change),
        ``1`` otherwise.
        """
        violations = sorted(str(p) for p in self.collect_violations())
        if not violations:
            print(f"ok [arch:{self._name}] — every contract-surface change carries a test change.")
            return 0
        print(f"FAIL [arch:{self._name}] — contract surface changed with no test change:")
        for rel in violations:
            print(f"  {rel}")
        print()
        print(self.remediation)
        return 1

    def establish_baseline(self) -> Path:
        """Freeze an EMPTY baseline — a missing test is non-grandfatherable.

        Mirrors :mod:`new_code_coverage`: the "changed" set is recomputed against
        the merge-base on every branch, so a frozen path is meaningless on the
        next one, and a contract change ADDED on THIS branch with no test is a
        FRESH defect, never inherited debt. This override freezes the EMPTY set so
        ``--establish-baseline`` writes a coherent (empty) file; the hard gate is
        enforced by :meth:`run`, which consults no baseline at all.
        """
        return _establish_baseline(self._name, set(), self._repo_root)


def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
    git_runner: GitRunner | None = None,
) -> ContractChangeHasTest:
    """Factory the engine calls to bind this CORE check to a consumer's config.

    ``git_runner`` is the DI seam: production leaves it ``None`` (the rule uses
    :func:`_default_git_runner`), a test passes a fake that returns canned
    ``merge-base`` / ``diff`` output so no real repository is required.
    """
    rule = ContractChangeHasTest.from_config(config, repo_root=repo_root)
    if git_runner is not None:
        rule.git_runner = git_runner
    return rule


def main(argv: list[str] | None = None) -> int:
    """CLI entry — supports ``--establish-baseline`` and ``--repo-root``."""
    return run_core_check(ContractChangeHasTest, argv)


if __name__ == "__main__":
    import sys

    sys.exit(main())
