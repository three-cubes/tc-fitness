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

Hard floor, by design. A contract change landed without its proving test is a
fresh defect recomputed against the merge-base on every branch and always fails.

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

from tc_fitness.check_evidence import report_finding
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


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x__matches_any__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__matches_any__mutmut)
def _matches_any(rel: str, globs: tuple[str, ...]) -> bool:
    """True iff ``rel`` matches any glob in ``globs`` (case-sensitive, path-aware).

    Uses :func:`fnmatch.fnmatchcase` — deterministic across platforms (no
    ``os.path.normcase`` fold). ``*``/``**`` both match path separators, so a
    prefix glob such as ``tests/**`` matches every nested path under the tree.
    """
    return any(fnmatchcase(rel, pattern) for pattern in globs)


def x__matches_any__mutmut_orig(rel: str, globs: tuple[str, ...]) -> bool:
    """True iff ``rel`` matches any glob in ``globs`` (case-sensitive, path-aware).

    Uses :func:`fnmatch.fnmatchcase` — deterministic across platforms (no
    ``os.path.normcase`` fold). ``*``/``**`` both match path separators, so a
    prefix glob such as ``tests/**`` matches every nested path under the tree.
    """
    return any(fnmatchcase(rel, pattern) for pattern in globs)


def x__matches_any__mutmut_1(rel: str, globs: tuple[str, ...]) -> bool:
    """True iff ``rel`` matches any glob in ``globs`` (case-sensitive, path-aware).

    Uses :func:`fnmatch.fnmatchcase` — deterministic across platforms (no
    ``os.path.normcase`` fold). ``*``/``**`` both match path separators, so a
    prefix glob such as ``tests/**`` matches every nested path under the tree.
    """
    return any(None)


def x__matches_any__mutmut_2(rel: str, globs: tuple[str, ...]) -> bool:
    """True iff ``rel`` matches any glob in ``globs`` (case-sensitive, path-aware).

    Uses :func:`fnmatch.fnmatchcase` — deterministic across platforms (no
    ``os.path.normcase`` fold). ``*``/``**`` both match path separators, so a
    prefix glob such as ``tests/**`` matches every nested path under the tree.
    """
    return any(fnmatchcase(None, pattern) for pattern in globs)


def x__matches_any__mutmut_3(rel: str, globs: tuple[str, ...]) -> bool:
    """True iff ``rel`` matches any glob in ``globs`` (case-sensitive, path-aware).

    Uses :func:`fnmatch.fnmatchcase` — deterministic across platforms (no
    ``os.path.normcase`` fold). ``*``/``**`` both match path separators, so a
    prefix glob such as ``tests/**`` matches every nested path under the tree.
    """
    return any(fnmatchcase(rel, None) for pattern in globs)


def x__matches_any__mutmut_4(rel: str, globs: tuple[str, ...]) -> bool:
    """True iff ``rel`` matches any glob in ``globs`` (case-sensitive, path-aware).

    Uses :func:`fnmatch.fnmatchcase` — deterministic across platforms (no
    ``os.path.normcase`` fold). ``*``/``**`` both match path separators, so a
    prefix glob such as ``tests/**`` matches every nested path under the tree.
    """
    return any(fnmatchcase(pattern) for pattern in globs)


def x__matches_any__mutmut_5(rel: str, globs: tuple[str, ...]) -> bool:
    """True iff ``rel`` matches any glob in ``globs`` (case-sensitive, path-aware).

    Uses :func:`fnmatch.fnmatchcase` — deterministic across platforms (no
    ``os.path.normcase`` fold). ``*``/``**`` both match path separators, so a
    prefix glob such as ``tests/**`` matches every nested path under the tree.
    """
    return any(fnmatchcase(rel, ) for pattern in globs)

mutants_x__matches_any__mutmut['_mutmut_orig'] = x__matches_any__mutmut_orig # type: ignore # mutmut generated
mutants_x__matches_any__mutmut['x__matches_any__mutmut_1'] = x__matches_any__mutmut_1 # type: ignore # mutmut generated
mutants_x__matches_any__mutmut['x__matches_any__mutmut_2'] = x__matches_any__mutmut_2 # type: ignore # mutmut generated
mutants_x__matches_any__mutmut['x__matches_any__mutmut_3'] = x__matches_any__mutmut_3 # type: ignore # mutmut generated
mutants_x__matches_any__mutmut['x__matches_any__mutmut_4'] = x__matches_any__mutmut_4 # type: ignore # mutmut generated
mutants_x__matches_any__mutmut['x__matches_any__mutmut_5'] = x__matches_any__mutmut_5 # type: ignore # mutmut generated
mutants_x__default_git_runner__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__default_git_runner__mutmut)
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


def x__default_git_runner__mutmut_orig(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
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


def x__default_git_runner__mutmut_1(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    """Run ``git <args>`` in ``cwd`` and capture its output (the default seam).

    argv0 is the fixed literal ``git`` (never a caller-supplied path) and
    ``shell`` is never used; the only caller-controlled token is the ref, which
    the rule validates against :data:`_SAFE_REF_RE` before it reaches here.
    """
    return subprocess.run(
        None,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )


def x__default_git_runner__mutmut_2(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    """Run ``git <args>`` in ``cwd`` and capture its output (the default seam).

    argv0 is the fixed literal ``git`` (never a caller-supplied path) and
    ``shell`` is never used; the only caller-controlled token is the ref, which
    the rule validates against :data:`_SAFE_REF_RE` before it reaches here.
    """
    return subprocess.run(
        ["git", *args],
        cwd=None,
        capture_output=True,
        text=True,
        check=False,
    )


def x__default_git_runner__mutmut_3(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    """Run ``git <args>`` in ``cwd`` and capture its output (the default seam).

    argv0 is the fixed literal ``git`` (never a caller-supplied path) and
    ``shell`` is never used; the only caller-controlled token is the ref, which
    the rule validates against :data:`_SAFE_REF_RE` before it reaches here.
    """
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=None,
        text=True,
        check=False,
    )


def x__default_git_runner__mutmut_4(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    """Run ``git <args>`` in ``cwd`` and capture its output (the default seam).

    argv0 is the fixed literal ``git`` (never a caller-supplied path) and
    ``shell`` is never used; the only caller-controlled token is the ref, which
    the rule validates against :data:`_SAFE_REF_RE` before it reaches here.
    """
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=None,
        check=False,
    )


def x__default_git_runner__mutmut_5(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
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
        check=None,
    )


def x__default_git_runner__mutmut_6(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    """Run ``git <args>`` in ``cwd`` and capture its output (the default seam).

    argv0 is the fixed literal ``git`` (never a caller-supplied path) and
    ``shell`` is never used; the only caller-controlled token is the ref, which
    the rule validates against :data:`_SAFE_REF_RE` before it reaches here.
    """
    return subprocess.run(
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )


def x__default_git_runner__mutmut_7(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    """Run ``git <args>`` in ``cwd`` and capture its output (the default seam).

    argv0 is the fixed literal ``git`` (never a caller-supplied path) and
    ``shell`` is never used; the only caller-controlled token is the ref, which
    the rule validates against :data:`_SAFE_REF_RE` before it reaches here.
    """
    return subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        check=False,
    )


def x__default_git_runner__mutmut_8(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    """Run ``git <args>`` in ``cwd`` and capture its output (the default seam).

    argv0 is the fixed literal ``git`` (never a caller-supplied path) and
    ``shell`` is never used; the only caller-controlled token is the ref, which
    the rule validates against :data:`_SAFE_REF_RE` before it reaches here.
    """
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        text=True,
        check=False,
    )


def x__default_git_runner__mutmut_9(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
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


def x__default_git_runner__mutmut_10(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
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
        )


def x__default_git_runner__mutmut_11(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    """Run ``git <args>`` in ``cwd`` and capture its output (the default seam).

    argv0 is the fixed literal ``git`` (never a caller-supplied path) and
    ``shell`` is never used; the only caller-controlled token is the ref, which
    the rule validates against :data:`_SAFE_REF_RE` before it reaches here.
    """
    return subprocess.run(
        ["XXgitXX", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )


def x__default_git_runner__mutmut_12(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    """Run ``git <args>`` in ``cwd`` and capture its output (the default seam).

    argv0 is the fixed literal ``git`` (never a caller-supplied path) and
    ``shell`` is never used; the only caller-controlled token is the ref, which
    the rule validates against :data:`_SAFE_REF_RE` before it reaches here.
    """
    return subprocess.run(
        ["GIT", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )


def x__default_git_runner__mutmut_13(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    """Run ``git <args>`` in ``cwd`` and capture its output (the default seam).

    argv0 is the fixed literal ``git`` (never a caller-supplied path) and
    ``shell`` is never used; the only caller-controlled token is the ref, which
    the rule validates against :data:`_SAFE_REF_RE` before it reaches here.
    """
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=False,
        text=True,
        check=False,
    )


def x__default_git_runner__mutmut_14(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    """Run ``git <args>`` in ``cwd`` and capture its output (the default seam).

    argv0 is the fixed literal ``git`` (never a caller-supplied path) and
    ``shell`` is never used; the only caller-controlled token is the ref, which
    the rule validates against :data:`_SAFE_REF_RE` before it reaches here.
    """
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=False,
        check=False,
    )


def x__default_git_runner__mutmut_15(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
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
        check=True,
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
mutants_xǁContractChangeHasTestǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁContractChangeHasTestǁ_changed_files__mutmut: MutantDict = {}  # type: ignore
mutants_xǁContractChangeHasTestǁis_in_scope__mutmut: MutantDict = {}  # type: ignore
mutants_xǁContractChangeHasTestǁenumerate_files__mutmut: MutantDict = {}  # type: ignore
mutants_xǁContractChangeHasTestǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore
mutants_xǁContractChangeHasTestǁrun__mutmut: MutantDict = {}  # type: ignore


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
    @_mutmut_mutated(mutants_xǁContractChangeHasTestǁfrom_config__mutmut, is_classmethod = True)
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

    @classmethod
    def xǁContractChangeHasTestǁfrom_config__mutmut_orig(
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

    @classmethod
    def xǁContractChangeHasTestǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ContractChangeHasTest:
        """Build from config, also reading ``contract_surface`` / ``test_globs`` / ``base_ref``."""
        rule = None
        assert isinstance(rule, ContractChangeHasTest)  # noqa: S101  # narrowing for mypy
        surface = config.get("contract_surface")
        globs = config.get("test_globs")
        rule.contract_surface = tuple(surface) if surface is not None else DEFAULT_CONTRACT_SURFACE
        rule.test_globs = tuple(globs) if globs is not None else DEFAULT_TEST_GLOBS
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        return rule

    @classmethod
    def xǁContractChangeHasTestǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ContractChangeHasTest:
        """Build from config, also reading ``contract_surface`` / ``test_globs`` / ``base_ref``."""
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, ContractChangeHasTest)  # noqa: S101  # narrowing for mypy
        surface = config.get("contract_surface")
        globs = config.get("test_globs")
        rule.contract_surface = tuple(surface) if surface is not None else DEFAULT_CONTRACT_SURFACE
        rule.test_globs = tuple(globs) if globs is not None else DEFAULT_TEST_GLOBS
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        return rule

    @classmethod
    def xǁContractChangeHasTestǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ContractChangeHasTest:
        """Build from config, also reading ``contract_surface`` / ``test_globs`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, ContractChangeHasTest)  # noqa: S101  # narrowing for mypy
        surface = config.get("contract_surface")
        globs = config.get("test_globs")
        rule.contract_surface = tuple(surface) if surface is not None else DEFAULT_CONTRACT_SURFACE
        rule.test_globs = tuple(globs) if globs is not None else DEFAULT_TEST_GLOBS
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        return rule

    @classmethod
    def xǁContractChangeHasTestǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ContractChangeHasTest:
        """Build from config, also reading ``contract_surface`` / ``test_globs`` / ``base_ref``."""
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, ContractChangeHasTest)  # noqa: S101  # narrowing for mypy
        surface = config.get("contract_surface")
        globs = config.get("test_globs")
        rule.contract_surface = tuple(surface) if surface is not None else DEFAULT_CONTRACT_SURFACE
        rule.test_globs = tuple(globs) if globs is not None else DEFAULT_TEST_GLOBS
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        return rule

    @classmethod
    def xǁContractChangeHasTestǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ContractChangeHasTest:
        """Build from config, also reading ``contract_surface`` / ``test_globs`` / ``base_ref``."""
        rule = super().from_config(config, )
        assert isinstance(rule, ContractChangeHasTest)  # noqa: S101  # narrowing for mypy
        surface = config.get("contract_surface")
        globs = config.get("test_globs")
        rule.contract_surface = tuple(surface) if surface is not None else DEFAULT_CONTRACT_SURFACE
        rule.test_globs = tuple(globs) if globs is not None else DEFAULT_TEST_GLOBS
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        return rule

    @classmethod
    def xǁContractChangeHasTestǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ContractChangeHasTest:
        """Build from config, also reading ``contract_surface`` / ``test_globs`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ContractChangeHasTest)  # noqa: S101  # narrowing for mypy
        surface = None
        globs = config.get("test_globs")
        rule.contract_surface = tuple(surface) if surface is not None else DEFAULT_CONTRACT_SURFACE
        rule.test_globs = tuple(globs) if globs is not None else DEFAULT_TEST_GLOBS
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        return rule

    @classmethod
    def xǁContractChangeHasTestǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ContractChangeHasTest:
        """Build from config, also reading ``contract_surface`` / ``test_globs`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ContractChangeHasTest)  # noqa: S101  # narrowing for mypy
        surface = config.get(None)
        globs = config.get("test_globs")
        rule.contract_surface = tuple(surface) if surface is not None else DEFAULT_CONTRACT_SURFACE
        rule.test_globs = tuple(globs) if globs is not None else DEFAULT_TEST_GLOBS
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        return rule

    @classmethod
    def xǁContractChangeHasTestǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ContractChangeHasTest:
        """Build from config, also reading ``contract_surface`` / ``test_globs`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ContractChangeHasTest)  # noqa: S101  # narrowing for mypy
        surface = config.get("XXcontract_surfaceXX")
        globs = config.get("test_globs")
        rule.contract_surface = tuple(surface) if surface is not None else DEFAULT_CONTRACT_SURFACE
        rule.test_globs = tuple(globs) if globs is not None else DEFAULT_TEST_GLOBS
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        return rule

    @classmethod
    def xǁContractChangeHasTestǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ContractChangeHasTest:
        """Build from config, also reading ``contract_surface`` / ``test_globs`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ContractChangeHasTest)  # noqa: S101  # narrowing for mypy
        surface = config.get("CONTRACT_SURFACE")
        globs = config.get("test_globs")
        rule.contract_surface = tuple(surface) if surface is not None else DEFAULT_CONTRACT_SURFACE
        rule.test_globs = tuple(globs) if globs is not None else DEFAULT_TEST_GLOBS
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        return rule

    @classmethod
    def xǁContractChangeHasTestǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ContractChangeHasTest:
        """Build from config, also reading ``contract_surface`` / ``test_globs`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ContractChangeHasTest)  # noqa: S101  # narrowing for mypy
        surface = config.get("contract_surface")
        globs = None
        rule.contract_surface = tuple(surface) if surface is not None else DEFAULT_CONTRACT_SURFACE
        rule.test_globs = tuple(globs) if globs is not None else DEFAULT_TEST_GLOBS
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        return rule

    @classmethod
    def xǁContractChangeHasTestǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ContractChangeHasTest:
        """Build from config, also reading ``contract_surface`` / ``test_globs`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ContractChangeHasTest)  # noqa: S101  # narrowing for mypy
        surface = config.get("contract_surface")
        globs = config.get(None)
        rule.contract_surface = tuple(surface) if surface is not None else DEFAULT_CONTRACT_SURFACE
        rule.test_globs = tuple(globs) if globs is not None else DEFAULT_TEST_GLOBS
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        return rule

    @classmethod
    def xǁContractChangeHasTestǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ContractChangeHasTest:
        """Build from config, also reading ``contract_surface`` / ``test_globs`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ContractChangeHasTest)  # noqa: S101  # narrowing for mypy
        surface = config.get("contract_surface")
        globs = config.get("XXtest_globsXX")
        rule.contract_surface = tuple(surface) if surface is not None else DEFAULT_CONTRACT_SURFACE
        rule.test_globs = tuple(globs) if globs is not None else DEFAULT_TEST_GLOBS
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        return rule

    @classmethod
    def xǁContractChangeHasTestǁfrom_config__mutmut_13(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ContractChangeHasTest:
        """Build from config, also reading ``contract_surface`` / ``test_globs`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ContractChangeHasTest)  # noqa: S101  # narrowing for mypy
        surface = config.get("contract_surface")
        globs = config.get("TEST_GLOBS")
        rule.contract_surface = tuple(surface) if surface is not None else DEFAULT_CONTRACT_SURFACE
        rule.test_globs = tuple(globs) if globs is not None else DEFAULT_TEST_GLOBS
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        return rule

    @classmethod
    def xǁContractChangeHasTestǁfrom_config__mutmut_14(
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
        rule.contract_surface = None
        rule.test_globs = tuple(globs) if globs is not None else DEFAULT_TEST_GLOBS
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        return rule

    @classmethod
    def xǁContractChangeHasTestǁfrom_config__mutmut_15(
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
        rule.contract_surface = tuple(None) if surface is not None else DEFAULT_CONTRACT_SURFACE
        rule.test_globs = tuple(globs) if globs is not None else DEFAULT_TEST_GLOBS
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        return rule

    @classmethod
    def xǁContractChangeHasTestǁfrom_config__mutmut_16(
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
        rule.contract_surface = tuple(surface) if surface is None else DEFAULT_CONTRACT_SURFACE
        rule.test_globs = tuple(globs) if globs is not None else DEFAULT_TEST_GLOBS
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        return rule

    @classmethod
    def xǁContractChangeHasTestǁfrom_config__mutmut_17(
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
        rule.test_globs = None
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        return rule

    @classmethod
    def xǁContractChangeHasTestǁfrom_config__mutmut_18(
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
        rule.test_globs = tuple(None) if globs is not None else DEFAULT_TEST_GLOBS
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        return rule

    @classmethod
    def xǁContractChangeHasTestǁfrom_config__mutmut_19(
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
        rule.test_globs = tuple(globs) if globs is None else DEFAULT_TEST_GLOBS
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        return rule

    @classmethod
    def xǁContractChangeHasTestǁfrom_config__mutmut_20(
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
        rule.base_ref = None
        rule.git_runner = _default_git_runner
        return rule

    @classmethod
    def xǁContractChangeHasTestǁfrom_config__mutmut_21(
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
        rule.base_ref = str(None)
        rule.git_runner = _default_git_runner
        return rule

    @classmethod
    def xǁContractChangeHasTestǁfrom_config__mutmut_22(
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
        rule.base_ref = str(config.get(None, DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        return rule

    @classmethod
    def xǁContractChangeHasTestǁfrom_config__mutmut_23(
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
        rule.base_ref = str(config.get("base_ref", None))
        rule.git_runner = _default_git_runner
        return rule

    @classmethod
    def xǁContractChangeHasTestǁfrom_config__mutmut_24(
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
        rule.base_ref = str(config.get(DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        return rule

    @classmethod
    def xǁContractChangeHasTestǁfrom_config__mutmut_25(
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
        rule.base_ref = str(config.get("base_ref", ))
        rule.git_runner = _default_git_runner
        return rule

    @classmethod
    def xǁContractChangeHasTestǁfrom_config__mutmut_26(
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
        rule.base_ref = str(config.get("XXbase_refXX", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        return rule

    @classmethod
    def xǁContractChangeHasTestǁfrom_config__mutmut_27(
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
        rule.base_ref = str(config.get("BASE_REF", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        return rule

    @classmethod
    def xǁContractChangeHasTestǁfrom_config__mutmut_28(
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
        rule.git_runner = None
        return rule

    @_mutmut_mutated(mutants_xǁContractChangeHasTestǁ_changed_files__mutmut)
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

    def xǁContractChangeHasTestǁ_changed_files__mutmut_orig(self) -> list[str]:
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

    def xǁContractChangeHasTestǁ_changed_files__mutmut_1(self) -> list[str]:
        """Repo-relative paths changed since the merge-base of ``base_ref`` and HEAD.

        Returns ``[]`` (→ a soft PASS) when the base ref is unsafe/unresolvable,
        the merge-base can't be computed, or the diff command fails — none of
        which is a contract-coverage defect, so the gate stays quiet.
        """
        if _SAFE_REF_RE.match(self.base_ref):
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

    def xǁContractChangeHasTestǁ_changed_files__mutmut_2(self) -> list[str]:
        """Repo-relative paths changed since the merge-base of ``base_ref`` and HEAD.

        Returns ``[]`` (→ a soft PASS) when the base ref is unsafe/unresolvable,
        the merge-base can't be computed, or the diff command fails — none of
        which is a contract-coverage defect, so the gate stays quiet.
        """
        if not _SAFE_REF_RE.match(None):
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

    def xǁContractChangeHasTestǁ_changed_files__mutmut_3(self) -> list[str]:
        """Repo-relative paths changed since the merge-base of ``base_ref`` and HEAD.

        Returns ``[]`` (→ a soft PASS) when the base ref is unsafe/unresolvable,
        the merge-base can't be computed, or the diff command fails — none of
        which is a contract-coverage defect, so the gate stays quiet.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return []
        merge_base = None
        if merge_base.returncode != 0:
            return []
        base = merge_base.stdout.strip()
        if not base:
            return []
        diff = self.git_runner(["diff", "--name-only", f"{base}...HEAD"], self._repo_root)
        if diff.returncode != 0:
            return []
        return [line.strip() for line in diff.stdout.splitlines() if line.strip()]

    def xǁContractChangeHasTestǁ_changed_files__mutmut_4(self) -> list[str]:
        """Repo-relative paths changed since the merge-base of ``base_ref`` and HEAD.

        Returns ``[]`` (→ a soft PASS) when the base ref is unsafe/unresolvable,
        the merge-base can't be computed, or the diff command fails — none of
        which is a contract-coverage defect, so the gate stays quiet.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return []
        merge_base = self.git_runner(None, self._repo_root)
        if merge_base.returncode != 0:
            return []
        base = merge_base.stdout.strip()
        if not base:
            return []
        diff = self.git_runner(["diff", "--name-only", f"{base}...HEAD"], self._repo_root)
        if diff.returncode != 0:
            return []
        return [line.strip() for line in diff.stdout.splitlines() if line.strip()]

    def xǁContractChangeHasTestǁ_changed_files__mutmut_5(self) -> list[str]:
        """Repo-relative paths changed since the merge-base of ``base_ref`` and HEAD.

        Returns ``[]`` (→ a soft PASS) when the base ref is unsafe/unresolvable,
        the merge-base can't be computed, or the diff command fails — none of
        which is a contract-coverage defect, so the gate stays quiet.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return []
        merge_base = self.git_runner(["merge-base", self.base_ref, "HEAD"], None)
        if merge_base.returncode != 0:
            return []
        base = merge_base.stdout.strip()
        if not base:
            return []
        diff = self.git_runner(["diff", "--name-only", f"{base}...HEAD"], self._repo_root)
        if diff.returncode != 0:
            return []
        return [line.strip() for line in diff.stdout.splitlines() if line.strip()]

    def xǁContractChangeHasTestǁ_changed_files__mutmut_6(self) -> list[str]:
        """Repo-relative paths changed since the merge-base of ``base_ref`` and HEAD.

        Returns ``[]`` (→ a soft PASS) when the base ref is unsafe/unresolvable,
        the merge-base can't be computed, or the diff command fails — none of
        which is a contract-coverage defect, so the gate stays quiet.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return []
        merge_base = self.git_runner(self._repo_root)
        if merge_base.returncode != 0:
            return []
        base = merge_base.stdout.strip()
        if not base:
            return []
        diff = self.git_runner(["diff", "--name-only", f"{base}...HEAD"], self._repo_root)
        if diff.returncode != 0:
            return []
        return [line.strip() for line in diff.stdout.splitlines() if line.strip()]

    def xǁContractChangeHasTestǁ_changed_files__mutmut_7(self) -> list[str]:
        """Repo-relative paths changed since the merge-base of ``base_ref`` and HEAD.

        Returns ``[]`` (→ a soft PASS) when the base ref is unsafe/unresolvable,
        the merge-base can't be computed, or the diff command fails — none of
        which is a contract-coverage defect, so the gate stays quiet.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return []
        merge_base = self.git_runner(["merge-base", self.base_ref, "HEAD"], )
        if merge_base.returncode != 0:
            return []
        base = merge_base.stdout.strip()
        if not base:
            return []
        diff = self.git_runner(["diff", "--name-only", f"{base}...HEAD"], self._repo_root)
        if diff.returncode != 0:
            return []
        return [line.strip() for line in diff.stdout.splitlines() if line.strip()]

    def xǁContractChangeHasTestǁ_changed_files__mutmut_8(self) -> list[str]:
        """Repo-relative paths changed since the merge-base of ``base_ref`` and HEAD.

        Returns ``[]`` (→ a soft PASS) when the base ref is unsafe/unresolvable,
        the merge-base can't be computed, or the diff command fails — none of
        which is a contract-coverage defect, so the gate stays quiet.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return []
        merge_base = self.git_runner(["XXmerge-baseXX", self.base_ref, "HEAD"], self._repo_root)
        if merge_base.returncode != 0:
            return []
        base = merge_base.stdout.strip()
        if not base:
            return []
        diff = self.git_runner(["diff", "--name-only", f"{base}...HEAD"], self._repo_root)
        if diff.returncode != 0:
            return []
        return [line.strip() for line in diff.stdout.splitlines() if line.strip()]

    def xǁContractChangeHasTestǁ_changed_files__mutmut_9(self) -> list[str]:
        """Repo-relative paths changed since the merge-base of ``base_ref`` and HEAD.

        Returns ``[]`` (→ a soft PASS) when the base ref is unsafe/unresolvable,
        the merge-base can't be computed, or the diff command fails — none of
        which is a contract-coverage defect, so the gate stays quiet.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return []
        merge_base = self.git_runner(["MERGE-BASE", self.base_ref, "HEAD"], self._repo_root)
        if merge_base.returncode != 0:
            return []
        base = merge_base.stdout.strip()
        if not base:
            return []
        diff = self.git_runner(["diff", "--name-only", f"{base}...HEAD"], self._repo_root)
        if diff.returncode != 0:
            return []
        return [line.strip() for line in diff.stdout.splitlines() if line.strip()]

    def xǁContractChangeHasTestǁ_changed_files__mutmut_10(self) -> list[str]:
        """Repo-relative paths changed since the merge-base of ``base_ref`` and HEAD.

        Returns ``[]`` (→ a soft PASS) when the base ref is unsafe/unresolvable,
        the merge-base can't be computed, or the diff command fails — none of
        which is a contract-coverage defect, so the gate stays quiet.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return []
        merge_base = self.git_runner(["merge-base", self.base_ref, "XXHEADXX"], self._repo_root)
        if merge_base.returncode != 0:
            return []
        base = merge_base.stdout.strip()
        if not base:
            return []
        diff = self.git_runner(["diff", "--name-only", f"{base}...HEAD"], self._repo_root)
        if diff.returncode != 0:
            return []
        return [line.strip() for line in diff.stdout.splitlines() if line.strip()]

    def xǁContractChangeHasTestǁ_changed_files__mutmut_11(self) -> list[str]:
        """Repo-relative paths changed since the merge-base of ``base_ref`` and HEAD.

        Returns ``[]`` (→ a soft PASS) when the base ref is unsafe/unresolvable,
        the merge-base can't be computed, or the diff command fails — none of
        which is a contract-coverage defect, so the gate stays quiet.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return []
        merge_base = self.git_runner(["merge-base", self.base_ref, "head"], self._repo_root)
        if merge_base.returncode != 0:
            return []
        base = merge_base.stdout.strip()
        if not base:
            return []
        diff = self.git_runner(["diff", "--name-only", f"{base}...HEAD"], self._repo_root)
        if diff.returncode != 0:
            return []
        return [line.strip() for line in diff.stdout.splitlines() if line.strip()]

    def xǁContractChangeHasTestǁ_changed_files__mutmut_12(self) -> list[str]:
        """Repo-relative paths changed since the merge-base of ``base_ref`` and HEAD.

        Returns ``[]`` (→ a soft PASS) when the base ref is unsafe/unresolvable,
        the merge-base can't be computed, or the diff command fails — none of
        which is a contract-coverage defect, so the gate stays quiet.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return []
        merge_base = self.git_runner(["merge-base", self.base_ref, "HEAD"], self._repo_root)
        if merge_base.returncode == 0:
            return []
        base = merge_base.stdout.strip()
        if not base:
            return []
        diff = self.git_runner(["diff", "--name-only", f"{base}...HEAD"], self._repo_root)
        if diff.returncode != 0:
            return []
        return [line.strip() for line in diff.stdout.splitlines() if line.strip()]

    def xǁContractChangeHasTestǁ_changed_files__mutmut_13(self) -> list[str]:
        """Repo-relative paths changed since the merge-base of ``base_ref`` and HEAD.

        Returns ``[]`` (→ a soft PASS) when the base ref is unsafe/unresolvable,
        the merge-base can't be computed, or the diff command fails — none of
        which is a contract-coverage defect, so the gate stays quiet.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return []
        merge_base = self.git_runner(["merge-base", self.base_ref, "HEAD"], self._repo_root)
        if merge_base.returncode != 1:
            return []
        base = merge_base.stdout.strip()
        if not base:
            return []
        diff = self.git_runner(["diff", "--name-only", f"{base}...HEAD"], self._repo_root)
        if diff.returncode != 0:
            return []
        return [line.strip() for line in diff.stdout.splitlines() if line.strip()]

    def xǁContractChangeHasTestǁ_changed_files__mutmut_14(self) -> list[str]:
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
        base = None
        if not base:
            return []
        diff = self.git_runner(["diff", "--name-only", f"{base}...HEAD"], self._repo_root)
        if diff.returncode != 0:
            return []
        return [line.strip() for line in diff.stdout.splitlines() if line.strip()]

    def xǁContractChangeHasTestǁ_changed_files__mutmut_15(self) -> list[str]:
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
        if base:
            return []
        diff = self.git_runner(["diff", "--name-only", f"{base}...HEAD"], self._repo_root)
        if diff.returncode != 0:
            return []
        return [line.strip() for line in diff.stdout.splitlines() if line.strip()]

    def xǁContractChangeHasTestǁ_changed_files__mutmut_16(self) -> list[str]:
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
        diff = None
        if diff.returncode != 0:
            return []
        return [line.strip() for line in diff.stdout.splitlines() if line.strip()]

    def xǁContractChangeHasTestǁ_changed_files__mutmut_17(self) -> list[str]:
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
        diff = self.git_runner(None, self._repo_root)
        if diff.returncode != 0:
            return []
        return [line.strip() for line in diff.stdout.splitlines() if line.strip()]

    def xǁContractChangeHasTestǁ_changed_files__mutmut_18(self) -> list[str]:
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
        diff = self.git_runner(["diff", "--name-only", f"{base}...HEAD"], None)
        if diff.returncode != 0:
            return []
        return [line.strip() for line in diff.stdout.splitlines() if line.strip()]

    def xǁContractChangeHasTestǁ_changed_files__mutmut_19(self) -> list[str]:
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
        diff = self.git_runner(self._repo_root)
        if diff.returncode != 0:
            return []
        return [line.strip() for line in diff.stdout.splitlines() if line.strip()]

    def xǁContractChangeHasTestǁ_changed_files__mutmut_20(self) -> list[str]:
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
        diff = self.git_runner(["diff", "--name-only", f"{base}...HEAD"], )
        if diff.returncode != 0:
            return []
        return [line.strip() for line in diff.stdout.splitlines() if line.strip()]

    def xǁContractChangeHasTestǁ_changed_files__mutmut_21(self) -> list[str]:
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
        diff = self.git_runner(["XXdiffXX", "--name-only", f"{base}...HEAD"], self._repo_root)
        if diff.returncode != 0:
            return []
        return [line.strip() for line in diff.stdout.splitlines() if line.strip()]

    def xǁContractChangeHasTestǁ_changed_files__mutmut_22(self) -> list[str]:
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
        diff = self.git_runner(["DIFF", "--name-only", f"{base}...HEAD"], self._repo_root)
        if diff.returncode != 0:
            return []
        return [line.strip() for line in diff.stdout.splitlines() if line.strip()]

    def xǁContractChangeHasTestǁ_changed_files__mutmut_23(self) -> list[str]:
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
        diff = self.git_runner(["diff", "XX--name-onlyXX", f"{base}...HEAD"], self._repo_root)
        if diff.returncode != 0:
            return []
        return [line.strip() for line in diff.stdout.splitlines() if line.strip()]

    def xǁContractChangeHasTestǁ_changed_files__mutmut_24(self) -> list[str]:
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
        diff = self.git_runner(["diff", "--NAME-ONLY", f"{base}...HEAD"], self._repo_root)
        if diff.returncode != 0:
            return []
        return [line.strip() for line in diff.stdout.splitlines() if line.strip()]

    def xǁContractChangeHasTestǁ_changed_files__mutmut_25(self) -> list[str]:
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
        if diff.returncode == 0:
            return []
        return [line.strip() for line in diff.stdout.splitlines() if line.strip()]

    def xǁContractChangeHasTestǁ_changed_files__mutmut_26(self) -> list[str]:
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
        if diff.returncode != 1:
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

    @_mutmut_mutated(mutants_xǁContractChangeHasTestǁis_in_scope__mutmut)
    def is_in_scope(self, rel: str) -> bool:
        """Scope IS the contract-surface glob set — not an extension/root prefix.

        Overrides the default extension+root predicate: this rule's universe is
        the contract-surface globs the consumer declares, matched against the
        changed-file set, so scope is decided by :func:`_matches_any` alone.
        """
        return _matches_any(rel, self.contract_surface)

    def xǁContractChangeHasTestǁis_in_scope__mutmut_orig(self, rel: str) -> bool:
        """Scope IS the contract-surface glob set — not an extension/root prefix.

        Overrides the default extension+root predicate: this rule's universe is
        the contract-surface globs the consumer declares, matched against the
        changed-file set, so scope is decided by :func:`_matches_any` alone.
        """
        return _matches_any(rel, self.contract_surface)

    def xǁContractChangeHasTestǁis_in_scope__mutmut_1(self, rel: str) -> bool:
        """Scope IS the contract-surface glob set — not an extension/root prefix.

        Overrides the default extension+root predicate: this rule's universe is
        the contract-surface globs the consumer declares, matched against the
        changed-file set, so scope is decided by :func:`_matches_any` alone.
        """
        return _matches_any(None, self.contract_surface)

    def xǁContractChangeHasTestǁis_in_scope__mutmut_2(self, rel: str) -> bool:
        """Scope IS the contract-surface glob set — not an extension/root prefix.

        Overrides the default extension+root predicate: this rule's universe is
        the contract-surface globs the consumer declares, matched against the
        changed-file set, so scope is decided by :func:`_matches_any` alone.
        """
        return _matches_any(rel, None)

    def xǁContractChangeHasTestǁis_in_scope__mutmut_3(self, rel: str) -> bool:
        """Scope IS the contract-surface glob set — not an extension/root prefix.

        Overrides the default extension+root predicate: this rule's universe is
        the contract-surface globs the consumer declares, matched against the
        changed-file set, so scope is decided by :func:`_matches_any` alone.
        """
        return _matches_any(self.contract_surface)

    def xǁContractChangeHasTestǁis_in_scope__mutmut_4(self, rel: str) -> bool:
        """Scope IS the contract-surface glob set — not an extension/root prefix.

        Overrides the default extension+root predicate: this rule's universe is
        the contract-surface globs the consumer declares, matched against the
        changed-file set, so scope is decided by :func:`_matches_any` alone.
        """
        return _matches_any(rel, )

    @_mutmut_mutated(mutants_xǁContractChangeHasTestǁenumerate_files__mutmut)
    def enumerate_files(self) -> list[Path]:
        """The changed contract-surface files, as repo-anchored paths.

        Overrides the default git-tracked walk: the rule's universe is the
        changed files (from the diff), not the on-disk tree. The contract-surface
        scope predicate is applied here and again in
        :meth:`FitnessRule.collect_violations` via :meth:`is_in_scope`.
        """
        return [self._repo_root / rel for rel in self._changed if self.is_in_scope(rel)]

    def xǁContractChangeHasTestǁenumerate_files__mutmut_orig(self) -> list[Path]:
        """The changed contract-surface files, as repo-anchored paths.

        Overrides the default git-tracked walk: the rule's universe is the
        changed files (from the diff), not the on-disk tree. The contract-surface
        scope predicate is applied here and again in
        :meth:`FitnessRule.collect_violations` via :meth:`is_in_scope`.
        """
        return [self._repo_root / rel for rel in self._changed if self.is_in_scope(rel)]

    def xǁContractChangeHasTestǁenumerate_files__mutmut_1(self) -> list[Path]:
        """The changed contract-surface files, as repo-anchored paths.

        Overrides the default git-tracked walk: the rule's universe is the
        changed files (from the diff), not the on-disk tree. The contract-surface
        scope predicate is applied here and again in
        :meth:`FitnessRule.collect_violations` via :meth:`is_in_scope`.
        """
        return [self._repo_root * rel for rel in self._changed if self.is_in_scope(rel)]

    def xǁContractChangeHasTestǁenumerate_files__mutmut_2(self) -> list[Path]:
        """The changed contract-surface files, as repo-anchored paths.

        Overrides the default git-tracked walk: the rule's universe is the
        changed files (from the diff), not the on-disk tree. The contract-surface
        scope predicate is applied here and again in
        :meth:`FitnessRule.collect_violations` via :meth:`is_in_scope`.
        """
        return [self._repo_root / rel for rel in self._changed if self.is_in_scope(None)]

    @_mutmut_mutated(mutants_xǁContractChangeHasTestǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        """True iff this contract file was changed with NO test file in the change set."""
        rel = str(self._repo_relative(path))
        if not self.is_in_scope(rel):
            return False
        return not self._test_touched

    def xǁContractChangeHasTestǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        """True iff this contract file was changed with NO test file in the change set."""
        rel = str(self._repo_relative(path))
        if not self.is_in_scope(rel):
            return False
        return not self._test_touched

    def xǁContractChangeHasTestǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        """True iff this contract file was changed with NO test file in the change set."""
        rel = None
        if not self.is_in_scope(rel):
            return False
        return not self._test_touched

    def xǁContractChangeHasTestǁfile_has_violation__mutmut_2(self, path: Path) -> bool:
        """True iff this contract file was changed with NO test file in the change set."""
        rel = str(None)
        if not self.is_in_scope(rel):
            return False
        return not self._test_touched

    def xǁContractChangeHasTestǁfile_has_violation__mutmut_3(self, path: Path) -> bool:
        """True iff this contract file was changed with NO test file in the change set."""
        rel = str(self._repo_relative(None))
        if not self.is_in_scope(rel):
            return False
        return not self._test_touched

    def xǁContractChangeHasTestǁfile_has_violation__mutmut_4(self, path: Path) -> bool:
        """True iff this contract file was changed with NO test file in the change set."""
        rel = str(self._repo_relative(path))
        if self.is_in_scope(rel):
            return False
        return not self._test_touched

    def xǁContractChangeHasTestǁfile_has_violation__mutmut_5(self, path: Path) -> bool:
        """True iff this contract file was changed with NO test file in the change set."""
        rel = str(self._repo_relative(path))
        if not self.is_in_scope(None):
            return False
        return not self._test_touched

    def xǁContractChangeHasTestǁfile_has_violation__mutmut_6(self, path: Path) -> bool:
        """True iff this contract file was changed with NO test file in the change set."""
        rel = str(self._repo_relative(path))
        if not self.is_in_scope(rel):
            return True
        return not self._test_touched

    def xǁContractChangeHasTestǁfile_has_violation__mutmut_7(self, path: Path) -> bool:
        """True iff this contract file was changed with NO test file in the change set."""
        rel = str(self._repo_relative(path))
        if not self.is_in_scope(rel):
            return False
        return self._test_touched

    @_mutmut_mutated(mutants_xǁContractChangeHasTestǁrun__mutmut)
    def run(self) -> int:
        """Hard gate: a contract change with no companion test change FAILs.

        The change set is recomputed against the merge-base on every branch. A
        contract file touched on this branch without a test is therefore a
        current defect. This method gates the raw violation set and returns
        ``0`` when the change set is clean (or there is no contract change),
        ``1`` otherwise.
        """
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — every contract-surface change carries a test change.")
            return 0
        print(f"FAIL [arch:{self._name}] — contract surface changed with no test change:")
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(path).as_posix(),
                "contract surface changed with no test change",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁContractChangeHasTestǁrun__mutmut_orig(self) -> int:
        """Hard gate: a contract change with no companion test change FAILs.

        The change set is recomputed against the merge-base on every branch. A
        contract file touched on this branch without a test is therefore a
        current defect. This method gates the raw violation set and returns
        ``0`` when the change set is clean (or there is no contract change),
        ``1`` otherwise.
        """
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — every contract-surface change carries a test change.")
            return 0
        print(f"FAIL [arch:{self._name}] — contract surface changed with no test change:")
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(path).as_posix(),
                "contract surface changed with no test change",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁContractChangeHasTestǁrun__mutmut_1(self) -> int:
        """Hard gate: a contract change with no companion test change FAILs.

        The change set is recomputed against the merge-base on every branch. A
        contract file touched on this branch without a test is therefore a
        current defect. This method gates the raw violation set and returns
        ``0`` when the change set is clean (or there is no contract change),
        ``1`` otherwise.
        """
        violations = None
        if not violations:
            print(f"ok [arch:{self._name}] — every contract-surface change carries a test change.")
            return 0
        print(f"FAIL [arch:{self._name}] — contract surface changed with no test change:")
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(path).as_posix(),
                "contract surface changed with no test change",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁContractChangeHasTestǁrun__mutmut_2(self) -> int:
        """Hard gate: a contract change with no companion test change FAILs.

        The change set is recomputed against the merge-base on every branch. A
        contract file touched on this branch without a test is therefore a
        current defect. This method gates the raw violation set and returns
        ``0`` when the change set is clean (or there is no contract change),
        ``1`` otherwise.
        """
        violations = sorted(None, key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — every contract-surface change carries a test change.")
            return 0
        print(f"FAIL [arch:{self._name}] — contract surface changed with no test change:")
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(path).as_posix(),
                "contract surface changed with no test change",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁContractChangeHasTestǁrun__mutmut_3(self) -> int:
        """Hard gate: a contract change with no companion test change FAILs.

        The change set is recomputed against the merge-base on every branch. A
        contract file touched on this branch without a test is therefore a
        current defect. This method gates the raw violation set and returns
        ``0`` when the change set is clean (or there is no contract change),
        ``1`` otherwise.
        """
        violations = sorted(self.collect_violations(), key=None)
        if not violations:
            print(f"ok [arch:{self._name}] — every contract-surface change carries a test change.")
            return 0
        print(f"FAIL [arch:{self._name}] — contract surface changed with no test change:")
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(path).as_posix(),
                "contract surface changed with no test change",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁContractChangeHasTestǁrun__mutmut_4(self) -> int:
        """Hard gate: a contract change with no companion test change FAILs.

        The change set is recomputed against the merge-base on every branch. A
        contract file touched on this branch without a test is therefore a
        current defect. This method gates the raw violation set and returns
        ``0`` when the change set is clean (or there is no contract change),
        ``1`` otherwise.
        """
        violations = sorted(key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — every contract-surface change carries a test change.")
            return 0
        print(f"FAIL [arch:{self._name}] — contract surface changed with no test change:")
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(path).as_posix(),
                "contract surface changed with no test change",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁContractChangeHasTestǁrun__mutmut_5(self) -> int:
        """Hard gate: a contract change with no companion test change FAILs.

        The change set is recomputed against the merge-base on every branch. A
        contract file touched on this branch without a test is therefore a
        current defect. This method gates the raw violation set and returns
        ``0`` when the change set is clean (or there is no contract change),
        ``1`` otherwise.
        """
        violations = sorted(self.collect_violations(), )
        if not violations:
            print(f"ok [arch:{self._name}] — every contract-surface change carries a test change.")
            return 0
        print(f"FAIL [arch:{self._name}] — contract surface changed with no test change:")
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(path).as_posix(),
                "contract surface changed with no test change",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁContractChangeHasTestǁrun__mutmut_6(self) -> int:
        """Hard gate: a contract change with no companion test change FAILs.

        The change set is recomputed against the merge-base on every branch. A
        contract file touched on this branch without a test is therefore a
        current defect. This method gates the raw violation set and returns
        ``0`` when the change set is clean (or there is no contract change),
        ``1`` otherwise.
        """
        violations = sorted(self.collect_violations(), key=lambda path: None)
        if not violations:
            print(f"ok [arch:{self._name}] — every contract-surface change carries a test change.")
            return 0
        print(f"FAIL [arch:{self._name}] — contract surface changed with no test change:")
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(path).as_posix(),
                "contract surface changed with no test change",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁContractChangeHasTestǁrun__mutmut_7(self) -> int:
        """Hard gate: a contract change with no companion test change FAILs.

        The change set is recomputed against the merge-base on every branch. A
        contract file touched on this branch without a test is therefore a
        current defect. This method gates the raw violation set and returns
        ``0`` when the change set is clean (or there is no contract change),
        ``1`` otherwise.
        """
        violations = sorted(self.collect_violations(), key=lambda path: str(None))
        if not violations:
            print(f"ok [arch:{self._name}] — every contract-surface change carries a test change.")
            return 0
        print(f"FAIL [arch:{self._name}] — contract surface changed with no test change:")
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(path).as_posix(),
                "contract surface changed with no test change",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁContractChangeHasTestǁrun__mutmut_8(self) -> int:
        """Hard gate: a contract change with no companion test change FAILs.

        The change set is recomputed against the merge-base on every branch. A
        contract file touched on this branch without a test is therefore a
        current defect. This method gates the raw violation set and returns
        ``0`` when the change set is clean (or there is no contract change),
        ``1`` otherwise.
        """
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if violations:
            print(f"ok [arch:{self._name}] — every contract-surface change carries a test change.")
            return 0
        print(f"FAIL [arch:{self._name}] — contract surface changed with no test change:")
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(path).as_posix(),
                "contract surface changed with no test change",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁContractChangeHasTestǁrun__mutmut_9(self) -> int:
        """Hard gate: a contract change with no companion test change FAILs.

        The change set is recomputed against the merge-base on every branch. A
        contract file touched on this branch without a test is therefore a
        current defect. This method gates the raw violation set and returns
        ``0`` when the change set is clean (or there is no contract change),
        ``1`` otherwise.
        """
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(None)
            return 0
        print(f"FAIL [arch:{self._name}] — contract surface changed with no test change:")
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(path).as_posix(),
                "contract surface changed with no test change",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁContractChangeHasTestǁrun__mutmut_10(self) -> int:
        """Hard gate: a contract change with no companion test change FAILs.

        The change set is recomputed against the merge-base on every branch. A
        contract file touched on this branch without a test is therefore a
        current defect. This method gates the raw violation set and returns
        ``0`` when the change set is clean (or there is no contract change),
        ``1`` otherwise.
        """
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — every contract-surface change carries a test change.")
            return 1
        print(f"FAIL [arch:{self._name}] — contract surface changed with no test change:")
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(path).as_posix(),
                "contract surface changed with no test change",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁContractChangeHasTestǁrun__mutmut_11(self) -> int:
        """Hard gate: a contract change with no companion test change FAILs.

        The change set is recomputed against the merge-base on every branch. A
        contract file touched on this branch without a test is therefore a
        current defect. This method gates the raw violation set and returns
        ``0`` when the change set is clean (or there is no contract change),
        ``1`` otherwise.
        """
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — every contract-surface change carries a test change.")
            return 0
        print(None)
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(path).as_posix(),
                "contract surface changed with no test change",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁContractChangeHasTestǁrun__mutmut_12(self) -> int:
        """Hard gate: a contract change with no companion test change FAILs.

        The change set is recomputed against the merge-base on every branch. A
        contract file touched on this branch without a test is therefore a
        current defect. This method gates the raw violation set and returns
        ``0`` when the change set is clean (or there is no contract change),
        ``1`` otherwise.
        """
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — every contract-surface change carries a test change.")
            return 0
        print(f"FAIL [arch:{self._name}] — contract surface changed with no test change:")
        for path in violations:
            report_finding(
                None,
                self._repo_relative(path).as_posix(),
                "contract surface changed with no test change",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁContractChangeHasTestǁrun__mutmut_13(self) -> int:
        """Hard gate: a contract change with no companion test change FAILs.

        The change set is recomputed against the merge-base on every branch. A
        contract file touched on this branch without a test is therefore a
        current defect. This method gates the raw violation set and returns
        ``0`` when the change set is clean (or there is no contract change),
        ``1`` otherwise.
        """
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — every contract-surface change carries a test change.")
            return 0
        print(f"FAIL [arch:{self._name}] — contract surface changed with no test change:")
        for path in violations:
            report_finding(
                self.name,
                None,
                "contract surface changed with no test change",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁContractChangeHasTestǁrun__mutmut_14(self) -> int:
        """Hard gate: a contract change with no companion test change FAILs.

        The change set is recomputed against the merge-base on every branch. A
        contract file touched on this branch without a test is therefore a
        current defect. This method gates the raw violation set and returns
        ``0`` when the change set is clean (or there is no contract change),
        ``1`` otherwise.
        """
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — every contract-surface change carries a test change.")
            return 0
        print(f"FAIL [arch:{self._name}] — contract surface changed with no test change:")
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(path).as_posix(),
                None,
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁContractChangeHasTestǁrun__mutmut_15(self) -> int:
        """Hard gate: a contract change with no companion test change FAILs.

        The change set is recomputed against the merge-base on every branch. A
        contract file touched on this branch without a test is therefore a
        current defect. This method gates the raw violation set and returns
        ``0`` when the change set is clean (or there is no contract change),
        ``1`` otherwise.
        """
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — every contract-surface change carries a test change.")
            return 0
        print(f"FAIL [arch:{self._name}] — contract surface changed with no test change:")
        for path in violations:
            report_finding(
                self._repo_relative(path).as_posix(),
                "contract surface changed with no test change",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁContractChangeHasTestǁrun__mutmut_16(self) -> int:
        """Hard gate: a contract change with no companion test change FAILs.

        The change set is recomputed against the merge-base on every branch. A
        contract file touched on this branch without a test is therefore a
        current defect. This method gates the raw violation set and returns
        ``0`` when the change set is clean (or there is no contract change),
        ``1`` otherwise.
        """
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — every contract-surface change carries a test change.")
            return 0
        print(f"FAIL [arch:{self._name}] — contract surface changed with no test change:")
        for path in violations:
            report_finding(
                self.name,
                "contract surface changed with no test change",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁContractChangeHasTestǁrun__mutmut_17(self) -> int:
        """Hard gate: a contract change with no companion test change FAILs.

        The change set is recomputed against the merge-base on every branch. A
        contract file touched on this branch without a test is therefore a
        current defect. This method gates the raw violation set and returns
        ``0`` when the change set is clean (or there is no contract change),
        ``1`` otherwise.
        """
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — every contract-surface change carries a test change.")
            return 0
        print(f"FAIL [arch:{self._name}] — contract surface changed with no test change:")
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(path).as_posix(),
                )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁContractChangeHasTestǁrun__mutmut_18(self) -> int:
        """Hard gate: a contract change with no companion test change FAILs.

        The change set is recomputed against the merge-base on every branch. A
        contract file touched on this branch without a test is therefore a
        current defect. This method gates the raw violation set and returns
        ``0`` when the change set is clean (or there is no contract change),
        ``1`` otherwise.
        """
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — every contract-surface change carries a test change.")
            return 0
        print(f"FAIL [arch:{self._name}] — contract surface changed with no test change:")
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(None).as_posix(),
                "contract surface changed with no test change",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁContractChangeHasTestǁrun__mutmut_19(self) -> int:
        """Hard gate: a contract change with no companion test change FAILs.

        The change set is recomputed against the merge-base on every branch. A
        contract file touched on this branch without a test is therefore a
        current defect. This method gates the raw violation set and returns
        ``0`` when the change set is clean (or there is no contract change),
        ``1`` otherwise.
        """
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — every contract-surface change carries a test change.")
            return 0
        print(f"FAIL [arch:{self._name}] — contract surface changed with no test change:")
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(path).as_posix(),
                "XXcontract surface changed with no test changeXX",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁContractChangeHasTestǁrun__mutmut_20(self) -> int:
        """Hard gate: a contract change with no companion test change FAILs.

        The change set is recomputed against the merge-base on every branch. A
        contract file touched on this branch without a test is therefore a
        current defect. This method gates the raw violation set and returns
        ``0`` when the change set is clean (or there is no contract change),
        ``1`` otherwise.
        """
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — every contract-surface change carries a test change.")
            return 0
        print(f"FAIL [arch:{self._name}] — contract surface changed with no test change:")
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(path).as_posix(),
                "CONTRACT SURFACE CHANGED WITH NO TEST CHANGE",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁContractChangeHasTestǁrun__mutmut_21(self) -> int:
        """Hard gate: a contract change with no companion test change FAILs.

        The change set is recomputed against the merge-base on every branch. A
        contract file touched on this branch without a test is therefore a
        current defect. This method gates the raw violation set and returns
        ``0`` when the change set is clean (or there is no contract change),
        ``1`` otherwise.
        """
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — every contract-surface change carries a test change.")
            return 0
        print(f"FAIL [arch:{self._name}] — contract surface changed with no test change:")
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(path).as_posix(),
                "contract surface changed with no test change",
            )
            print(None)
        print()
        print(self.remediation)
        return 1

    def xǁContractChangeHasTestǁrun__mutmut_22(self) -> int:
        """Hard gate: a contract change with no companion test change FAILs.

        The change set is recomputed against the merge-base on every branch. A
        contract file touched on this branch without a test is therefore a
        current defect. This method gates the raw violation set and returns
        ``0`` when the change set is clean (or there is no contract change),
        ``1`` otherwise.
        """
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — every contract-surface change carries a test change.")
            return 0
        print(f"FAIL [arch:{self._name}] — contract surface changed with no test change:")
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(path).as_posix(),
                "contract surface changed with no test change",
            )
            print(f"  {path}")
        print()
        print(None)
        return 1

    def xǁContractChangeHasTestǁrun__mutmut_23(self) -> int:
        """Hard gate: a contract change with no companion test change FAILs.

        The change set is recomputed against the merge-base on every branch. A
        contract file touched on this branch without a test is therefore a
        current defect. This method gates the raw violation set and returns
        ``0`` when the change set is clean (or there is no contract change),
        ``1`` otherwise.
        """
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — every contract-surface change carries a test change.")
            return 0
        print(f"FAIL [arch:{self._name}] — contract surface changed with no test change:")
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(path).as_posix(),
                "contract surface changed with no test change",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 2

mutants_xǁContractChangeHasTestǁfrom_config__mutmut['_mutmut_orig'] = ContractChangeHasTest.xǁContractChangeHasTestǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁfrom_config__mutmut['xǁContractChangeHasTestǁfrom_config__mutmut_1'] = ContractChangeHasTest.xǁContractChangeHasTestǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁfrom_config__mutmut['xǁContractChangeHasTestǁfrom_config__mutmut_2'] = ContractChangeHasTest.xǁContractChangeHasTestǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁfrom_config__mutmut['xǁContractChangeHasTestǁfrom_config__mutmut_3'] = ContractChangeHasTest.xǁContractChangeHasTestǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁfrom_config__mutmut['xǁContractChangeHasTestǁfrom_config__mutmut_4'] = ContractChangeHasTest.xǁContractChangeHasTestǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁfrom_config__mutmut['xǁContractChangeHasTestǁfrom_config__mutmut_5'] = ContractChangeHasTest.xǁContractChangeHasTestǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁfrom_config__mutmut['xǁContractChangeHasTestǁfrom_config__mutmut_6'] = ContractChangeHasTest.xǁContractChangeHasTestǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁfrom_config__mutmut['xǁContractChangeHasTestǁfrom_config__mutmut_7'] = ContractChangeHasTest.xǁContractChangeHasTestǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁfrom_config__mutmut['xǁContractChangeHasTestǁfrom_config__mutmut_8'] = ContractChangeHasTest.xǁContractChangeHasTestǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁfrom_config__mutmut['xǁContractChangeHasTestǁfrom_config__mutmut_9'] = ContractChangeHasTest.xǁContractChangeHasTestǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁfrom_config__mutmut['xǁContractChangeHasTestǁfrom_config__mutmut_10'] = ContractChangeHasTest.xǁContractChangeHasTestǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁfrom_config__mutmut['xǁContractChangeHasTestǁfrom_config__mutmut_11'] = ContractChangeHasTest.xǁContractChangeHasTestǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁfrom_config__mutmut['xǁContractChangeHasTestǁfrom_config__mutmut_12'] = ContractChangeHasTest.xǁContractChangeHasTestǁfrom_config__mutmut_12 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁfrom_config__mutmut['xǁContractChangeHasTestǁfrom_config__mutmut_13'] = ContractChangeHasTest.xǁContractChangeHasTestǁfrom_config__mutmut_13 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁfrom_config__mutmut['xǁContractChangeHasTestǁfrom_config__mutmut_14'] = ContractChangeHasTest.xǁContractChangeHasTestǁfrom_config__mutmut_14 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁfrom_config__mutmut['xǁContractChangeHasTestǁfrom_config__mutmut_15'] = ContractChangeHasTest.xǁContractChangeHasTestǁfrom_config__mutmut_15 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁfrom_config__mutmut['xǁContractChangeHasTestǁfrom_config__mutmut_16'] = ContractChangeHasTest.xǁContractChangeHasTestǁfrom_config__mutmut_16 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁfrom_config__mutmut['xǁContractChangeHasTestǁfrom_config__mutmut_17'] = ContractChangeHasTest.xǁContractChangeHasTestǁfrom_config__mutmut_17 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁfrom_config__mutmut['xǁContractChangeHasTestǁfrom_config__mutmut_18'] = ContractChangeHasTest.xǁContractChangeHasTestǁfrom_config__mutmut_18 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁfrom_config__mutmut['xǁContractChangeHasTestǁfrom_config__mutmut_19'] = ContractChangeHasTest.xǁContractChangeHasTestǁfrom_config__mutmut_19 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁfrom_config__mutmut['xǁContractChangeHasTestǁfrom_config__mutmut_20'] = ContractChangeHasTest.xǁContractChangeHasTestǁfrom_config__mutmut_20 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁfrom_config__mutmut['xǁContractChangeHasTestǁfrom_config__mutmut_21'] = ContractChangeHasTest.xǁContractChangeHasTestǁfrom_config__mutmut_21 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁfrom_config__mutmut['xǁContractChangeHasTestǁfrom_config__mutmut_22'] = ContractChangeHasTest.xǁContractChangeHasTestǁfrom_config__mutmut_22 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁfrom_config__mutmut['xǁContractChangeHasTestǁfrom_config__mutmut_23'] = ContractChangeHasTest.xǁContractChangeHasTestǁfrom_config__mutmut_23 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁfrom_config__mutmut['xǁContractChangeHasTestǁfrom_config__mutmut_24'] = ContractChangeHasTest.xǁContractChangeHasTestǁfrom_config__mutmut_24 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁfrom_config__mutmut['xǁContractChangeHasTestǁfrom_config__mutmut_25'] = ContractChangeHasTest.xǁContractChangeHasTestǁfrom_config__mutmut_25 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁfrom_config__mutmut['xǁContractChangeHasTestǁfrom_config__mutmut_26'] = ContractChangeHasTest.xǁContractChangeHasTestǁfrom_config__mutmut_26 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁfrom_config__mutmut['xǁContractChangeHasTestǁfrom_config__mutmut_27'] = ContractChangeHasTest.xǁContractChangeHasTestǁfrom_config__mutmut_27 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁfrom_config__mutmut['xǁContractChangeHasTestǁfrom_config__mutmut_28'] = ContractChangeHasTest.xǁContractChangeHasTestǁfrom_config__mutmut_28 # type: ignore # mutmut generated

mutants_xǁContractChangeHasTestǁ_changed_files__mutmut['_mutmut_orig'] = ContractChangeHasTest.xǁContractChangeHasTestǁ_changed_files__mutmut_orig # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁ_changed_files__mutmut['xǁContractChangeHasTestǁ_changed_files__mutmut_1'] = ContractChangeHasTest.xǁContractChangeHasTestǁ_changed_files__mutmut_1 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁ_changed_files__mutmut['xǁContractChangeHasTestǁ_changed_files__mutmut_2'] = ContractChangeHasTest.xǁContractChangeHasTestǁ_changed_files__mutmut_2 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁ_changed_files__mutmut['xǁContractChangeHasTestǁ_changed_files__mutmut_3'] = ContractChangeHasTest.xǁContractChangeHasTestǁ_changed_files__mutmut_3 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁ_changed_files__mutmut['xǁContractChangeHasTestǁ_changed_files__mutmut_4'] = ContractChangeHasTest.xǁContractChangeHasTestǁ_changed_files__mutmut_4 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁ_changed_files__mutmut['xǁContractChangeHasTestǁ_changed_files__mutmut_5'] = ContractChangeHasTest.xǁContractChangeHasTestǁ_changed_files__mutmut_5 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁ_changed_files__mutmut['xǁContractChangeHasTestǁ_changed_files__mutmut_6'] = ContractChangeHasTest.xǁContractChangeHasTestǁ_changed_files__mutmut_6 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁ_changed_files__mutmut['xǁContractChangeHasTestǁ_changed_files__mutmut_7'] = ContractChangeHasTest.xǁContractChangeHasTestǁ_changed_files__mutmut_7 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁ_changed_files__mutmut['xǁContractChangeHasTestǁ_changed_files__mutmut_8'] = ContractChangeHasTest.xǁContractChangeHasTestǁ_changed_files__mutmut_8 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁ_changed_files__mutmut['xǁContractChangeHasTestǁ_changed_files__mutmut_9'] = ContractChangeHasTest.xǁContractChangeHasTestǁ_changed_files__mutmut_9 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁ_changed_files__mutmut['xǁContractChangeHasTestǁ_changed_files__mutmut_10'] = ContractChangeHasTest.xǁContractChangeHasTestǁ_changed_files__mutmut_10 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁ_changed_files__mutmut['xǁContractChangeHasTestǁ_changed_files__mutmut_11'] = ContractChangeHasTest.xǁContractChangeHasTestǁ_changed_files__mutmut_11 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁ_changed_files__mutmut['xǁContractChangeHasTestǁ_changed_files__mutmut_12'] = ContractChangeHasTest.xǁContractChangeHasTestǁ_changed_files__mutmut_12 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁ_changed_files__mutmut['xǁContractChangeHasTestǁ_changed_files__mutmut_13'] = ContractChangeHasTest.xǁContractChangeHasTestǁ_changed_files__mutmut_13 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁ_changed_files__mutmut['xǁContractChangeHasTestǁ_changed_files__mutmut_14'] = ContractChangeHasTest.xǁContractChangeHasTestǁ_changed_files__mutmut_14 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁ_changed_files__mutmut['xǁContractChangeHasTestǁ_changed_files__mutmut_15'] = ContractChangeHasTest.xǁContractChangeHasTestǁ_changed_files__mutmut_15 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁ_changed_files__mutmut['xǁContractChangeHasTestǁ_changed_files__mutmut_16'] = ContractChangeHasTest.xǁContractChangeHasTestǁ_changed_files__mutmut_16 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁ_changed_files__mutmut['xǁContractChangeHasTestǁ_changed_files__mutmut_17'] = ContractChangeHasTest.xǁContractChangeHasTestǁ_changed_files__mutmut_17 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁ_changed_files__mutmut['xǁContractChangeHasTestǁ_changed_files__mutmut_18'] = ContractChangeHasTest.xǁContractChangeHasTestǁ_changed_files__mutmut_18 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁ_changed_files__mutmut['xǁContractChangeHasTestǁ_changed_files__mutmut_19'] = ContractChangeHasTest.xǁContractChangeHasTestǁ_changed_files__mutmut_19 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁ_changed_files__mutmut['xǁContractChangeHasTestǁ_changed_files__mutmut_20'] = ContractChangeHasTest.xǁContractChangeHasTestǁ_changed_files__mutmut_20 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁ_changed_files__mutmut['xǁContractChangeHasTestǁ_changed_files__mutmut_21'] = ContractChangeHasTest.xǁContractChangeHasTestǁ_changed_files__mutmut_21 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁ_changed_files__mutmut['xǁContractChangeHasTestǁ_changed_files__mutmut_22'] = ContractChangeHasTest.xǁContractChangeHasTestǁ_changed_files__mutmut_22 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁ_changed_files__mutmut['xǁContractChangeHasTestǁ_changed_files__mutmut_23'] = ContractChangeHasTest.xǁContractChangeHasTestǁ_changed_files__mutmut_23 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁ_changed_files__mutmut['xǁContractChangeHasTestǁ_changed_files__mutmut_24'] = ContractChangeHasTest.xǁContractChangeHasTestǁ_changed_files__mutmut_24 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁ_changed_files__mutmut['xǁContractChangeHasTestǁ_changed_files__mutmut_25'] = ContractChangeHasTest.xǁContractChangeHasTestǁ_changed_files__mutmut_25 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁ_changed_files__mutmut['xǁContractChangeHasTestǁ_changed_files__mutmut_26'] = ContractChangeHasTest.xǁContractChangeHasTestǁ_changed_files__mutmut_26 # type: ignore # mutmut generated

mutants_xǁContractChangeHasTestǁis_in_scope__mutmut['_mutmut_orig'] = ContractChangeHasTest.xǁContractChangeHasTestǁis_in_scope__mutmut_orig # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁis_in_scope__mutmut['xǁContractChangeHasTestǁis_in_scope__mutmut_1'] = ContractChangeHasTest.xǁContractChangeHasTestǁis_in_scope__mutmut_1 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁis_in_scope__mutmut['xǁContractChangeHasTestǁis_in_scope__mutmut_2'] = ContractChangeHasTest.xǁContractChangeHasTestǁis_in_scope__mutmut_2 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁis_in_scope__mutmut['xǁContractChangeHasTestǁis_in_scope__mutmut_3'] = ContractChangeHasTest.xǁContractChangeHasTestǁis_in_scope__mutmut_3 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁis_in_scope__mutmut['xǁContractChangeHasTestǁis_in_scope__mutmut_4'] = ContractChangeHasTest.xǁContractChangeHasTestǁis_in_scope__mutmut_4 # type: ignore # mutmut generated

mutants_xǁContractChangeHasTestǁenumerate_files__mutmut['_mutmut_orig'] = ContractChangeHasTest.xǁContractChangeHasTestǁenumerate_files__mutmut_orig # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁenumerate_files__mutmut['xǁContractChangeHasTestǁenumerate_files__mutmut_1'] = ContractChangeHasTest.xǁContractChangeHasTestǁenumerate_files__mutmut_1 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁenumerate_files__mutmut['xǁContractChangeHasTestǁenumerate_files__mutmut_2'] = ContractChangeHasTest.xǁContractChangeHasTestǁenumerate_files__mutmut_2 # type: ignore # mutmut generated

mutants_xǁContractChangeHasTestǁfile_has_violation__mutmut['_mutmut_orig'] = ContractChangeHasTest.xǁContractChangeHasTestǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁfile_has_violation__mutmut['xǁContractChangeHasTestǁfile_has_violation__mutmut_1'] = ContractChangeHasTest.xǁContractChangeHasTestǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁfile_has_violation__mutmut['xǁContractChangeHasTestǁfile_has_violation__mutmut_2'] = ContractChangeHasTest.xǁContractChangeHasTestǁfile_has_violation__mutmut_2 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁfile_has_violation__mutmut['xǁContractChangeHasTestǁfile_has_violation__mutmut_3'] = ContractChangeHasTest.xǁContractChangeHasTestǁfile_has_violation__mutmut_3 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁfile_has_violation__mutmut['xǁContractChangeHasTestǁfile_has_violation__mutmut_4'] = ContractChangeHasTest.xǁContractChangeHasTestǁfile_has_violation__mutmut_4 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁfile_has_violation__mutmut['xǁContractChangeHasTestǁfile_has_violation__mutmut_5'] = ContractChangeHasTest.xǁContractChangeHasTestǁfile_has_violation__mutmut_5 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁfile_has_violation__mutmut['xǁContractChangeHasTestǁfile_has_violation__mutmut_6'] = ContractChangeHasTest.xǁContractChangeHasTestǁfile_has_violation__mutmut_6 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁfile_has_violation__mutmut['xǁContractChangeHasTestǁfile_has_violation__mutmut_7'] = ContractChangeHasTest.xǁContractChangeHasTestǁfile_has_violation__mutmut_7 # type: ignore # mutmut generated

mutants_xǁContractChangeHasTestǁrun__mutmut['_mutmut_orig'] = ContractChangeHasTest.xǁContractChangeHasTestǁrun__mutmut_orig # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁrun__mutmut['xǁContractChangeHasTestǁrun__mutmut_1'] = ContractChangeHasTest.xǁContractChangeHasTestǁrun__mutmut_1 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁrun__mutmut['xǁContractChangeHasTestǁrun__mutmut_2'] = ContractChangeHasTest.xǁContractChangeHasTestǁrun__mutmut_2 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁrun__mutmut['xǁContractChangeHasTestǁrun__mutmut_3'] = ContractChangeHasTest.xǁContractChangeHasTestǁrun__mutmut_3 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁrun__mutmut['xǁContractChangeHasTestǁrun__mutmut_4'] = ContractChangeHasTest.xǁContractChangeHasTestǁrun__mutmut_4 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁrun__mutmut['xǁContractChangeHasTestǁrun__mutmut_5'] = ContractChangeHasTest.xǁContractChangeHasTestǁrun__mutmut_5 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁrun__mutmut['xǁContractChangeHasTestǁrun__mutmut_6'] = ContractChangeHasTest.xǁContractChangeHasTestǁrun__mutmut_6 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁrun__mutmut['xǁContractChangeHasTestǁrun__mutmut_7'] = ContractChangeHasTest.xǁContractChangeHasTestǁrun__mutmut_7 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁrun__mutmut['xǁContractChangeHasTestǁrun__mutmut_8'] = ContractChangeHasTest.xǁContractChangeHasTestǁrun__mutmut_8 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁrun__mutmut['xǁContractChangeHasTestǁrun__mutmut_9'] = ContractChangeHasTest.xǁContractChangeHasTestǁrun__mutmut_9 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁrun__mutmut['xǁContractChangeHasTestǁrun__mutmut_10'] = ContractChangeHasTest.xǁContractChangeHasTestǁrun__mutmut_10 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁrun__mutmut['xǁContractChangeHasTestǁrun__mutmut_11'] = ContractChangeHasTest.xǁContractChangeHasTestǁrun__mutmut_11 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁrun__mutmut['xǁContractChangeHasTestǁrun__mutmut_12'] = ContractChangeHasTest.xǁContractChangeHasTestǁrun__mutmut_12 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁrun__mutmut['xǁContractChangeHasTestǁrun__mutmut_13'] = ContractChangeHasTest.xǁContractChangeHasTestǁrun__mutmut_13 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁrun__mutmut['xǁContractChangeHasTestǁrun__mutmut_14'] = ContractChangeHasTest.xǁContractChangeHasTestǁrun__mutmut_14 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁrun__mutmut['xǁContractChangeHasTestǁrun__mutmut_15'] = ContractChangeHasTest.xǁContractChangeHasTestǁrun__mutmut_15 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁrun__mutmut['xǁContractChangeHasTestǁrun__mutmut_16'] = ContractChangeHasTest.xǁContractChangeHasTestǁrun__mutmut_16 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁrun__mutmut['xǁContractChangeHasTestǁrun__mutmut_17'] = ContractChangeHasTest.xǁContractChangeHasTestǁrun__mutmut_17 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁrun__mutmut['xǁContractChangeHasTestǁrun__mutmut_18'] = ContractChangeHasTest.xǁContractChangeHasTestǁrun__mutmut_18 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁrun__mutmut['xǁContractChangeHasTestǁrun__mutmut_19'] = ContractChangeHasTest.xǁContractChangeHasTestǁrun__mutmut_19 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁrun__mutmut['xǁContractChangeHasTestǁrun__mutmut_20'] = ContractChangeHasTest.xǁContractChangeHasTestǁrun__mutmut_20 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁrun__mutmut['xǁContractChangeHasTestǁrun__mutmut_21'] = ContractChangeHasTest.xǁContractChangeHasTestǁrun__mutmut_21 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁrun__mutmut['xǁContractChangeHasTestǁrun__mutmut_22'] = ContractChangeHasTest.xǁContractChangeHasTestǁrun__mutmut_22 # type: ignore # mutmut generated
mutants_xǁContractChangeHasTestǁrun__mutmut['xǁContractChangeHasTestǁrun__mutmut_23'] = ContractChangeHasTest.xǁContractChangeHasTestǁrun__mutmut_23 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
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


def x_build__mutmut_orig(
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


def x_build__mutmut_1(
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
    rule = None
    if git_runner is not None:
        rule.git_runner = git_runner
    return rule


def x_build__mutmut_2(
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
    rule = ContractChangeHasTest.from_config(None, repo_root=repo_root)
    if git_runner is not None:
        rule.git_runner = git_runner
    return rule


def x_build__mutmut_3(
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
    rule = ContractChangeHasTest.from_config(config, repo_root=None)
    if git_runner is not None:
        rule.git_runner = git_runner
    return rule


def x_build__mutmut_4(
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
    rule = ContractChangeHasTest.from_config(repo_root=repo_root)
    if git_runner is not None:
        rule.git_runner = git_runner
    return rule


def x_build__mutmut_5(
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
    rule = ContractChangeHasTest.from_config(config, )
    if git_runner is not None:
        rule.git_runner = git_runner
    return rule


def x_build__mutmut_6(
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
    if git_runner is None:
        rule.git_runner = git_runner
    return rule


def x_build__mutmut_7(
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
    return run_core_check(ContractChangeHasTest, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(ContractChangeHasTest, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(ContractChangeHasTest, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(ContractChangeHasTest, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
