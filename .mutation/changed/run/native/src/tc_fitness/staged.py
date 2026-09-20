"""Precise per-rule staged selection for the fitness runner.

``run_checks.py --staged`` must give fast feedback that the STAGED CHANGE
introduced no fitness violation. The non-negotiable property is **no false
negative on staged changes**: if staging file(s) introduces a violation of rule
R, staged mode MUST run R. Speed is the goal, but a fast path that silently
MISSES a violation is worse than a slow one. When in doubt, run the rule — the
full ``--all`` gate is the merge bar, so over-running is cheap and under-running
is the only real danger.

This module turns each rule's catalogue metadata into a concrete decision:

* **scope predicate** — the repo-relative path prefixes whose staged change
  could trip the rule. Single-sourced: the explicit ``RuleEntry.staged_scope``
  wins; otherwise it is DERIVED from the rule's own detector via an injected
  :class:`ScopeResolver` (the consumer repo's hook — e.g. kairix reads a check
  module's ``RULE.roots`` / ``FitnessRule.roots``). When no scope resolves, the
  predicate is ``None`` → the rule is treated as always-in-scope (fail-safe).

* **selection class** — from :data:`~tc_fitness.catalogue.StagedClass`:
    - ``file-local`` — run over ``staged ∩ scope`` (and the runner scopes the
      shared file index to the staged files so an in-process check walks ONLY
      them). Skipped when that intersection is empty.
    - ``relational`` — if any staged path is within ``scope``, run over the
      FULL scope (a deletion of the paired artefact, or a new surface file, can
      break a cross-file invariant even when the obvious file isn't staged).
    - ``always-run`` — run unconditionally (net-new-file / catalogue-currency /
      README / path-naming — the trigger is "any change at all").

Repo-agnostic scope derivation
------------------------------
Deriving a scope from a check module is repo-specific: kairix introspects its
``FitnessRule`` ABC and import-boundary shims. To stay agnostic, this module
accepts a :class:`ScopeResolver` callable. The runner threads the consumer's
resolver through ``decide``; when none is supplied, only the explicit
``staged_scope`` is honoured and everything else falls back to "run"
(fail-safe). That keeps the common path sound for any repo while letting kairix
supply its FitnessRule-aware resolver to stay byte-identical.
"""

from __future__ import annotations

import importlib
import inspect
import sys
from collections.abc import Callable, Iterable, Iterator
from contextlib import AbstractContextManager, contextmanager
from dataclasses import dataclass
from pathlib import Path

from tc_fitness.catalogue import RuleEntry, StagedClass

# A scope resolver maps a check ``script`` filename to the rule's repo-relative
# scan roots, or ``None`` when it can't be derived (→ fail-safe run). The
# consumer repo supplies this so the shared module never needs to know the
# repo's check-module internals.
ScopeResolver = Callable[[str], "tuple[str, ...] | None"]


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x_resolve_staged_scope__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_resolve_staged_scope__mutmut)
def resolve_staged_scope(
    entry: RuleEntry,
    script: str,
    resolver: ScopeResolver | None = None,
) -> tuple[str, ...] | None:
    """The repo-relative path-prefix scope for ``entry`` under ``script``.

    Explicit ``entry.staged_scope`` always wins (single source of truth for
    rules whose scope can't be derived — shell detectors, multi-tree standalone
    checks, relational rules with a BROADER trigger than their scan roots).
    Otherwise the scope is derived from the check's own detector via the
    injected ``resolver``. ``None`` means "no resolvable scope" → the caller
    runs the rule unconditionally (fail-safe).
    """
    if entry.staged_scope is not None:
        return entry.staged_scope
    if resolver is None:
        return None
    return resolver(script)


def x_resolve_staged_scope__mutmut_orig(
    entry: RuleEntry,
    script: str,
    resolver: ScopeResolver | None = None,
) -> tuple[str, ...] | None:
    """The repo-relative path-prefix scope for ``entry`` under ``script``.

    Explicit ``entry.staged_scope`` always wins (single source of truth for
    rules whose scope can't be derived — shell detectors, multi-tree standalone
    checks, relational rules with a BROADER trigger than their scan roots).
    Otherwise the scope is derived from the check's own detector via the
    injected ``resolver``. ``None`` means "no resolvable scope" → the caller
    runs the rule unconditionally (fail-safe).
    """
    if entry.staged_scope is not None:
        return entry.staged_scope
    if resolver is None:
        return None
    return resolver(script)


def x_resolve_staged_scope__mutmut_1(
    entry: RuleEntry,
    script: str,
    resolver: ScopeResolver | None = None,
) -> tuple[str, ...] | None:
    """The repo-relative path-prefix scope for ``entry`` under ``script``.

    Explicit ``entry.staged_scope`` always wins (single source of truth for
    rules whose scope can't be derived — shell detectors, multi-tree standalone
    checks, relational rules with a BROADER trigger than their scan roots).
    Otherwise the scope is derived from the check's own detector via the
    injected ``resolver``. ``None`` means "no resolvable scope" → the caller
    runs the rule unconditionally (fail-safe).
    """
    if entry.staged_scope is None:
        return entry.staged_scope
    if resolver is None:
        return None
    return resolver(script)


def x_resolve_staged_scope__mutmut_2(
    entry: RuleEntry,
    script: str,
    resolver: ScopeResolver | None = None,
) -> tuple[str, ...] | None:
    """The repo-relative path-prefix scope for ``entry`` under ``script``.

    Explicit ``entry.staged_scope`` always wins (single source of truth for
    rules whose scope can't be derived — shell detectors, multi-tree standalone
    checks, relational rules with a BROADER trigger than their scan roots).
    Otherwise the scope is derived from the check's own detector via the
    injected ``resolver``. ``None`` means "no resolvable scope" → the caller
    runs the rule unconditionally (fail-safe).
    """
    if entry.staged_scope is not None:
        return entry.staged_scope
    if resolver is not None:
        return None
    return resolver(script)


def x_resolve_staged_scope__mutmut_3(
    entry: RuleEntry,
    script: str,
    resolver: ScopeResolver | None = None,
) -> tuple[str, ...] | None:
    """The repo-relative path-prefix scope for ``entry`` under ``script``.

    Explicit ``entry.staged_scope`` always wins (single source of truth for
    rules whose scope can't be derived — shell detectors, multi-tree standalone
    checks, relational rules with a BROADER trigger than their scan roots).
    Otherwise the scope is derived from the check's own detector via the
    injected ``resolver``. ``None`` means "no resolvable scope" → the caller
    runs the rule unconditionally (fail-safe).
    """
    if entry.staged_scope is not None:
        return entry.staged_scope
    if resolver is None:
        return None
    return resolver(None)

mutants_x_resolve_staged_scope__mutmut['_mutmut_orig'] = x_resolve_staged_scope__mutmut_orig # type: ignore # mutmut generated
mutants_x_resolve_staged_scope__mutmut['x_resolve_staged_scope__mutmut_1'] = x_resolve_staged_scope__mutmut_1 # type: ignore # mutmut generated
mutants_x_resolve_staged_scope__mutmut['x_resolve_staged_scope__mutmut_2'] = x_resolve_staged_scope__mutmut_2 # type: ignore # mutmut generated
mutants_x_resolve_staged_scope__mutmut['x_resolve_staged_scope__mutmut_3'] = x_resolve_staged_scope__mutmut_3 # type: ignore # mutmut generated
mutants_x__path_under__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__path_under__mutmut)
def _path_under(path: str, prefix: str) -> bool:
    """True if repo-relative ``path`` is the file ``prefix`` or sits under the
    directory ``prefix``. A ``prefix`` ending in a file suffix (``.py`` etc.)
    matches that exact file only."""
    if path == prefix:
        return True
    # Directory prefix: ``kairix`` matches ``kairix/...`` but not ``kairixx``.
    return path.startswith(prefix + "/")


def x__path_under__mutmut_orig(path: str, prefix: str) -> bool:
    """True if repo-relative ``path`` is the file ``prefix`` or sits under the
    directory ``prefix``. A ``prefix`` ending in a file suffix (``.py`` etc.)
    matches that exact file only."""
    if path == prefix:
        return True
    # Directory prefix: ``kairix`` matches ``kairix/...`` but not ``kairixx``.
    return path.startswith(prefix + "/")


def x__path_under__mutmut_1(path: str, prefix: str) -> bool:
    """True if repo-relative ``path`` is the file ``prefix`` or sits under the
    directory ``prefix``. A ``prefix`` ending in a file suffix (``.py`` etc.)
    matches that exact file only."""
    if path != prefix:
        return True
    # Directory prefix: ``kairix`` matches ``kairix/...`` but not ``kairixx``.
    return path.startswith(prefix + "/")


def x__path_under__mutmut_2(path: str, prefix: str) -> bool:
    """True if repo-relative ``path`` is the file ``prefix`` or sits under the
    directory ``prefix``. A ``prefix`` ending in a file suffix (``.py`` etc.)
    matches that exact file only."""
    if path == prefix:
        return False
    # Directory prefix: ``kairix`` matches ``kairix/...`` but not ``kairixx``.
    return path.startswith(prefix + "/")


def x__path_under__mutmut_3(path: str, prefix: str) -> bool:
    """True if repo-relative ``path`` is the file ``prefix`` or sits under the
    directory ``prefix``. A ``prefix`` ending in a file suffix (``.py`` etc.)
    matches that exact file only."""
    if path == prefix:
        return True
    # Directory prefix: ``kairix`` matches ``kairix/...`` but not ``kairixx``.
    return path.startswith(None)


def x__path_under__mutmut_4(path: str, prefix: str) -> bool:
    """True if repo-relative ``path`` is the file ``prefix`` or sits under the
    directory ``prefix``. A ``prefix`` ending in a file suffix (``.py`` etc.)
    matches that exact file only."""
    if path == prefix:
        return True
    # Directory prefix: ``kairix`` matches ``kairix/...`` but not ``kairixx``.
    return path.startswith(prefix - "/")


def x__path_under__mutmut_5(path: str, prefix: str) -> bool:
    """True if repo-relative ``path`` is the file ``prefix`` or sits under the
    directory ``prefix``. A ``prefix`` ending in a file suffix (``.py`` etc.)
    matches that exact file only."""
    if path == prefix:
        return True
    # Directory prefix: ``kairix`` matches ``kairix/...`` but not ``kairixx``.
    return path.startswith(prefix + "XX/XX")

mutants_x__path_under__mutmut['_mutmut_orig'] = x__path_under__mutmut_orig # type: ignore # mutmut generated
mutants_x__path_under__mutmut['x__path_under__mutmut_1'] = x__path_under__mutmut_1 # type: ignore # mutmut generated
mutants_x__path_under__mutmut['x__path_under__mutmut_2'] = x__path_under__mutmut_2 # type: ignore # mutmut generated
mutants_x__path_under__mutmut['x__path_under__mutmut_3'] = x__path_under__mutmut_3 # type: ignore # mutmut generated
mutants_x__path_under__mutmut['x__path_under__mutmut_4'] = x__path_under__mutmut_4 # type: ignore # mutmut generated
mutants_x__path_under__mutmut['x__path_under__mutmut_5'] = x__path_under__mutmut_5 # type: ignore # mutmut generated
mutants_x_staged_in_scope__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_staged_in_scope__mutmut)
def staged_in_scope(scope: tuple[str, ...] | None, staged: list[str]) -> list[str]:
    """The staged paths that fall within ``scope``.

    ``scope is None`` → every staged path is "in scope" (conservative). A
    concrete scope intersects each staged path against its prefixes.
    """
    if scope is None:
        return list(staged)
    return [p for p in staged if any(_path_under(p, prefix) for prefix in scope)]


def x_staged_in_scope__mutmut_orig(scope: tuple[str, ...] | None, staged: list[str]) -> list[str]:
    """The staged paths that fall within ``scope``.

    ``scope is None`` → every staged path is "in scope" (conservative). A
    concrete scope intersects each staged path against its prefixes.
    """
    if scope is None:
        return list(staged)
    return [p for p in staged if any(_path_under(p, prefix) for prefix in scope)]


def x_staged_in_scope__mutmut_1(scope: tuple[str, ...] | None, staged: list[str]) -> list[str]:
    """The staged paths that fall within ``scope``.

    ``scope is None`` → every staged path is "in scope" (conservative). A
    concrete scope intersects each staged path against its prefixes.
    """
    if scope is not None:
        return list(staged)
    return [p for p in staged if any(_path_under(p, prefix) for prefix in scope)]


def x_staged_in_scope__mutmut_2(scope: tuple[str, ...] | None, staged: list[str]) -> list[str]:
    """The staged paths that fall within ``scope``.

    ``scope is None`` → every staged path is "in scope" (conservative). A
    concrete scope intersects each staged path against its prefixes.
    """
    if scope is None:
        return list(None)
    return [p for p in staged if any(_path_under(p, prefix) for prefix in scope)]


def x_staged_in_scope__mutmut_3(scope: tuple[str, ...] | None, staged: list[str]) -> list[str]:
    """The staged paths that fall within ``scope``.

    ``scope is None`` → every staged path is "in scope" (conservative). A
    concrete scope intersects each staged path against its prefixes.
    """
    if scope is None:
        return list(staged)
    return [p for p in staged if any(None)]


def x_staged_in_scope__mutmut_4(scope: tuple[str, ...] | None, staged: list[str]) -> list[str]:
    """The staged paths that fall within ``scope``.

    ``scope is None`` → every staged path is "in scope" (conservative). A
    concrete scope intersects each staged path against its prefixes.
    """
    if scope is None:
        return list(staged)
    return [p for p in staged if any(_path_under(None, prefix) for prefix in scope)]


def x_staged_in_scope__mutmut_5(scope: tuple[str, ...] | None, staged: list[str]) -> list[str]:
    """The staged paths that fall within ``scope``.

    ``scope is None`` → every staged path is "in scope" (conservative). A
    concrete scope intersects each staged path against its prefixes.
    """
    if scope is None:
        return list(staged)
    return [p for p in staged if any(_path_under(p, None) for prefix in scope)]


def x_staged_in_scope__mutmut_6(scope: tuple[str, ...] | None, staged: list[str]) -> list[str]:
    """The staged paths that fall within ``scope``.

    ``scope is None`` → every staged path is "in scope" (conservative). A
    concrete scope intersects each staged path against its prefixes.
    """
    if scope is None:
        return list(staged)
    return [p for p in staged if any(_path_under(prefix) for prefix in scope)]


def x_staged_in_scope__mutmut_7(scope: tuple[str, ...] | None, staged: list[str]) -> list[str]:
    """The staged paths that fall within ``scope``.

    ``scope is None`` → every staged path is "in scope" (conservative). A
    concrete scope intersects each staged path against its prefixes.
    """
    if scope is None:
        return list(staged)
    return [p for p in staged if any(_path_under(p, ) for prefix in scope)]

mutants_x_staged_in_scope__mutmut['_mutmut_orig'] = x_staged_in_scope__mutmut_orig # type: ignore # mutmut generated
mutants_x_staged_in_scope__mutmut['x_staged_in_scope__mutmut_1'] = x_staged_in_scope__mutmut_1 # type: ignore # mutmut generated
mutants_x_staged_in_scope__mutmut['x_staged_in_scope__mutmut_2'] = x_staged_in_scope__mutmut_2 # type: ignore # mutmut generated
mutants_x_staged_in_scope__mutmut['x_staged_in_scope__mutmut_3'] = x_staged_in_scope__mutmut_3 # type: ignore # mutmut generated
mutants_x_staged_in_scope__mutmut['x_staged_in_scope__mutmut_4'] = x_staged_in_scope__mutmut_4 # type: ignore # mutmut generated
mutants_x_staged_in_scope__mutmut['x_staged_in_scope__mutmut_5'] = x_staged_in_scope__mutmut_5 # type: ignore # mutmut generated
mutants_x_staged_in_scope__mutmut['x_staged_in_scope__mutmut_6'] = x_staged_in_scope__mutmut_6 # type: ignore # mutmut generated
mutants_x_staged_in_scope__mutmut['x_staged_in_scope__mutmut_7'] = x_staged_in_scope__mutmut_7 # type: ignore # mutmut generated


@dataclass(frozen=True)
class StagedDecision:
    """The runner's decision for one rule against the staged set.

    Attributes:
        run: whether to dispatch the rule at all.
        reason: a short human-readable why (printed in the transparent staged
            ledger so narrowing is auditable, never silent).
        scope_files: for a ``file-local`` rule that should run, the staged
            files to restrict the shared file index to (so the in-process check
            walks ONLY them). Empty/``None`` for relational / always-run (those
            run over their full natural scope).
    """

    run: bool
    reason: str
    scope_files: tuple[str, ...] | None = None
mutants_x_decide__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_decide__mutmut)
def decide(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_orig(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_1(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = None

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_2(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_3(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=None, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_4(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason=None)

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_5(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_6(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, )

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_7(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=False, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_8(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="XXno staged paths — run everything (fail-safe)XX")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_9(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="NO STAGED PATHS — RUN EVERYTHING (FAIL-SAFE)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_10(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass != "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_11(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "XXalways-runXX":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_12(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "ALWAYS-RUN":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_13(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=None, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_14(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason=None)

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_15(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_16(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, )

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_17(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=False, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_18(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="XXalways-run (trigger is any change)XX")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_19(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="ALWAYS-RUN (TRIGGER IS ANY CHANGE)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_20(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = None
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_21(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(None, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_22(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, None, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_23(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, None)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_24(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_25(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_26(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, )
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_27(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = None

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_28(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(None, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_29(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, None)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_30(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_31(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, )

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_32(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass != "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_33(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "XXrelationalXX":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_34(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "RELATIONAL":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_35(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = None
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_36(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "XXunresolved scopeXX" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_37(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "UNRESOLVED SCOPE" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_38(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is not None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_39(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(None)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_40(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else "XX, XX".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_41(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=None, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_42(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=None)
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_43(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_44(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, )
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_45(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=False, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_46(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=None, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_47(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason=None)

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_48(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_49(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, )

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_50(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=True, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_51(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="XXrelational — no staged path in scopeXX")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_52(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="RELATIONAL — NO STAGED PATH IN SCOPE")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_53(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is not None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_54(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=None, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_55(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason=None)
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_56(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_57(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, )
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_58(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=False, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_59(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="XXfile-local — scope unresolved; run (fail-safe)XX")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_60(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="FILE-LOCAL — SCOPE UNRESOLVED; RUN (FAIL-SAFE)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_61(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=None,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_62(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=None,
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_63(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=None,
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_64(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_65(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_66(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_67(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=False,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_68(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(None),
        )
    return StagedDecision(run=False, reason="file-local — no staged file in scope")


def x_decide__mutmut_69(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=None, reason="file-local — no staged file in scope")


def x_decide__mutmut_70(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason=None)


def x_decide__mutmut_71(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(reason="file-local — no staged file in scope")


def x_decide__mutmut_72(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, )


def x_decide__mutmut_73(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=True, reason="file-local — no staged file in scope")


def x_decide__mutmut_74(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="XXfile-local — no staged file in scopeXX")


def x_decide__mutmut_75(
    entry: RuleEntry,
    script: str,
    staged: list[str],
    resolver: ScopeResolver | None = None,
) -> StagedDecision:
    """Decide whether — and over what — to run ``entry`` given ``staged``.

    The three classes:

    * ``always-run`` → always dispatch (full scope).
    * ``relational`` → dispatch over full scope iff any staged path is within
      the rule's scope; else skip.
    * ``file-local`` → dispatch over ``staged ∩ scope`` iff that intersection
      is non-empty (and hand those files back so the runner scopes the file
      index); else skip.

    With no staged paths at all (``staged == []``), every rule runs — the
    pre-commit ``--all-files`` quirk must never silently pass.
    """
    klass: StagedClass = entry.staged_class

    if not staged:
        return StagedDecision(run=True, reason="no staged paths — run everything (fail-safe)")

    if klass == "always-run":
        return StagedDecision(run=True, reason="always-run (trigger is any change)")

    scope = resolve_staged_scope(entry, script, resolver)
    matched = staged_in_scope(scope, staged)

    if klass == "relational":
        if matched:
            where = "unresolved scope" if scope is None else ", ".join(scope)
            return StagedDecision(run=True, reason=f"relational — staged path in scope ({where}); full scope")
        return StagedDecision(run=False, reason="relational — no staged path in scope")

    # file-local
    if scope is None:
        # No resolvable scope → can't narrow soundly; run unconditionally.
        return StagedDecision(run=True, reason="file-local — scope unresolved; run (fail-safe)")
    if matched:
        return StagedDecision(
            run=True,
            reason=f"file-local — {len(matched)} staged file(s) in scope",
            scope_files=tuple(matched),
        )
    return StagedDecision(run=False, reason="FILE-LOCAL — NO STAGED FILE IN SCOPE")

mutants_x_decide__mutmut['_mutmut_orig'] = x_decide__mutmut_orig # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_1'] = x_decide__mutmut_1 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_2'] = x_decide__mutmut_2 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_3'] = x_decide__mutmut_3 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_4'] = x_decide__mutmut_4 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_5'] = x_decide__mutmut_5 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_6'] = x_decide__mutmut_6 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_7'] = x_decide__mutmut_7 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_8'] = x_decide__mutmut_8 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_9'] = x_decide__mutmut_9 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_10'] = x_decide__mutmut_10 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_11'] = x_decide__mutmut_11 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_12'] = x_decide__mutmut_12 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_13'] = x_decide__mutmut_13 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_14'] = x_decide__mutmut_14 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_15'] = x_decide__mutmut_15 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_16'] = x_decide__mutmut_16 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_17'] = x_decide__mutmut_17 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_18'] = x_decide__mutmut_18 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_19'] = x_decide__mutmut_19 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_20'] = x_decide__mutmut_20 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_21'] = x_decide__mutmut_21 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_22'] = x_decide__mutmut_22 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_23'] = x_decide__mutmut_23 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_24'] = x_decide__mutmut_24 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_25'] = x_decide__mutmut_25 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_26'] = x_decide__mutmut_26 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_27'] = x_decide__mutmut_27 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_28'] = x_decide__mutmut_28 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_29'] = x_decide__mutmut_29 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_30'] = x_decide__mutmut_30 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_31'] = x_decide__mutmut_31 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_32'] = x_decide__mutmut_32 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_33'] = x_decide__mutmut_33 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_34'] = x_decide__mutmut_34 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_35'] = x_decide__mutmut_35 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_36'] = x_decide__mutmut_36 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_37'] = x_decide__mutmut_37 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_38'] = x_decide__mutmut_38 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_39'] = x_decide__mutmut_39 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_40'] = x_decide__mutmut_40 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_41'] = x_decide__mutmut_41 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_42'] = x_decide__mutmut_42 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_43'] = x_decide__mutmut_43 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_44'] = x_decide__mutmut_44 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_45'] = x_decide__mutmut_45 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_46'] = x_decide__mutmut_46 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_47'] = x_decide__mutmut_47 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_48'] = x_decide__mutmut_48 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_49'] = x_decide__mutmut_49 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_50'] = x_decide__mutmut_50 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_51'] = x_decide__mutmut_51 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_52'] = x_decide__mutmut_52 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_53'] = x_decide__mutmut_53 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_54'] = x_decide__mutmut_54 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_55'] = x_decide__mutmut_55 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_56'] = x_decide__mutmut_56 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_57'] = x_decide__mutmut_57 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_58'] = x_decide__mutmut_58 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_59'] = x_decide__mutmut_59 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_60'] = x_decide__mutmut_60 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_61'] = x_decide__mutmut_61 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_62'] = x_decide__mutmut_62 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_63'] = x_decide__mutmut_63 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_64'] = x_decide__mutmut_64 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_65'] = x_decide__mutmut_65 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_66'] = x_decide__mutmut_66 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_67'] = x_decide__mutmut_67 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_68'] = x_decide__mutmut_68 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_69'] = x_decide__mutmut_69 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_70'] = x_decide__mutmut_70 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_71'] = x_decide__mutmut_71 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_72'] = x_decide__mutmut_72 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_73'] = x_decide__mutmut_73 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_74'] = x_decide__mutmut_74 # type: ignore # mutmut generated
mutants_x_decide__mutmut['x_decide__mutmut_75'] = x_decide__mutmut_75 # type: ignore # mutmut generated


# ── file-index narrowing for a file-local rule ──────────────────────────
#
# When a file-local rule runs in staged mode, it only needs to RE-CHECK the
# staged files — every other in-scope file was clean at the previous commit and
# its content is unchanged, so its file-local verdict is unchanged. Narrowing
# the rule's file enumeration to the staged set turns a full-tree walk into a
# handful of files. Soundness note: this only narrows FILE-LOCAL rules, where a
# each file's verdict is independent of the other files. Relational and always-run
# rules are NEVER narrowed.
#
# WHICH enumeration surfaces to narrow is repo-specific (kairix patches its
# ``FitnessRule.enumerate_files`` ABC method plus the ``tc_fitness.python_files``
# free function plus each check module's bound copy). To stay agnostic, the
# runner is handed an ``EnumerationNarrower`` — a context-manager factory the
# consumer supplies. The common runner narrows the package-level
# ``tc_fitness.python_files`` itself; the consumer's narrower layers any
# repo-specific surfaces (its ABC method, its per-check bindings) on top.

# An enumeration narrower takes (repo_root, staged-paths) and returns a context
# manager that, for its duration, restricts every relevant file-enumeration
# surface to the staged files.
EnumerationNarrower = Callable[[Path, list[str]], "AbstractContextManager[None]"]
mutants_x_filter_to_staged__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_filter_to_staged__mutmut)
def filter_to_staged(paths: list[Path], staged_abs: frozenset[Path]) -> list[Path]:
    """Keep only the ``paths`` that are in the staged set (by resolved path).

    A reusable helper for a consumer's own :data:`EnumerationNarrower`: the
    set a narrowed enumeration should yield is exactly ``what-it-would-walk ∩
    staged``.
    """
    out: list[Path] = []
    for p in paths:
        try:
            resolved = p.resolve()
        except OSError:  # pragma: no cover - resolve hiccup → drop conservatively only if not staged
            resolved = p
        if resolved in staged_abs:
            out.append(p)
    return out


def x_filter_to_staged__mutmut_orig(paths: list[Path], staged_abs: frozenset[Path]) -> list[Path]:
    """Keep only the ``paths`` that are in the staged set (by resolved path).

    A reusable helper for a consumer's own :data:`EnumerationNarrower`: the
    set a narrowed enumeration should yield is exactly ``what-it-would-walk ∩
    staged``.
    """
    out: list[Path] = []
    for p in paths:
        try:
            resolved = p.resolve()
        except OSError:  # pragma: no cover - resolve hiccup → drop conservatively only if not staged
            resolved = p
        if resolved in staged_abs:
            out.append(p)
    return out


def x_filter_to_staged__mutmut_1(paths: list[Path], staged_abs: frozenset[Path]) -> list[Path]:
    """Keep only the ``paths`` that are in the staged set (by resolved path).

    A reusable helper for a consumer's own :data:`EnumerationNarrower`: the
    set a narrowed enumeration should yield is exactly ``what-it-would-walk ∩
    staged``.
    """
    out: list[Path] = None
    for p in paths:
        try:
            resolved = p.resolve()
        except OSError:  # pragma: no cover - resolve hiccup → drop conservatively only if not staged
            resolved = p
        if resolved in staged_abs:
            out.append(p)
    return out


def x_filter_to_staged__mutmut_2(paths: list[Path], staged_abs: frozenset[Path]) -> list[Path]:
    """Keep only the ``paths`` that are in the staged set (by resolved path).

    A reusable helper for a consumer's own :data:`EnumerationNarrower`: the
    set a narrowed enumeration should yield is exactly ``what-it-would-walk ∩
    staged``.
    """
    out: list[Path] = []
    for p in paths:
        try:
            resolved = None
        except OSError:  # pragma: no cover - resolve hiccup → drop conservatively only if not staged
            resolved = p
        if resolved in staged_abs:
            out.append(p)
    return out


def x_filter_to_staged__mutmut_3(paths: list[Path], staged_abs: frozenset[Path]) -> list[Path]:
    """Keep only the ``paths`` that are in the staged set (by resolved path).

    A reusable helper for a consumer's own :data:`EnumerationNarrower`: the
    set a narrowed enumeration should yield is exactly ``what-it-would-walk ∩
    staged``.
    """
    out: list[Path] = []
    for p in paths:
        try:
            resolved = p.resolve()
        except OSError:  # pragma: no cover - resolve hiccup → drop conservatively only if not staged
            resolved = None
        if resolved in staged_abs:
            out.append(p)
    return out


def x_filter_to_staged__mutmut_4(paths: list[Path], staged_abs: frozenset[Path]) -> list[Path]:
    """Keep only the ``paths`` that are in the staged set (by resolved path).

    A reusable helper for a consumer's own :data:`EnumerationNarrower`: the
    set a narrowed enumeration should yield is exactly ``what-it-would-walk ∩
    staged``.
    """
    out: list[Path] = []
    for p in paths:
        try:
            resolved = p.resolve()
        except OSError:  # pragma: no cover - resolve hiccup → drop conservatively only if not staged
            resolved = p
        if resolved not in staged_abs:
            out.append(p)
    return out


def x_filter_to_staged__mutmut_5(paths: list[Path], staged_abs: frozenset[Path]) -> list[Path]:
    """Keep only the ``paths`` that are in the staged set (by resolved path).

    A reusable helper for a consumer's own :data:`EnumerationNarrower`: the
    set a narrowed enumeration should yield is exactly ``what-it-would-walk ∩
    staged``.
    """
    out: list[Path] = []
    for p in paths:
        try:
            resolved = p.resolve()
        except OSError:  # pragma: no cover - resolve hiccup → drop conservatively only if not staged
            resolved = p
        if resolved in staged_abs:
            out.append(None)
    return out

mutants_x_filter_to_staged__mutmut['_mutmut_orig'] = x_filter_to_staged__mutmut_orig # type: ignore # mutmut generated
mutants_x_filter_to_staged__mutmut['x_filter_to_staged__mutmut_1'] = x_filter_to_staged__mutmut_1 # type: ignore # mutmut generated
mutants_x_filter_to_staged__mutmut['x_filter_to_staged__mutmut_2'] = x_filter_to_staged__mutmut_2 # type: ignore # mutmut generated
mutants_x_filter_to_staged__mutmut['x_filter_to_staged__mutmut_3'] = x_filter_to_staged__mutmut_3 # type: ignore # mutmut generated
mutants_x_filter_to_staged__mutmut['x_filter_to_staged__mutmut_4'] = x_filter_to_staged__mutmut_4 # type: ignore # mutmut generated
mutants_x_filter_to_staged__mutmut['x_filter_to_staged__mutmut_5'] = x_filter_to_staged__mutmut_5 # type: ignore # mutmut generated
mutants_x_staged_abs_set__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_staged_abs_set__mutmut)
def staged_abs_set(repo_root: Path, staged: list[str]) -> frozenset[Path]:
    """The staged repo-relative paths resolved to absolute paths under
    ``repo_root`` — the membership set :func:`filter_to_staged` keys on."""
    return frozenset((repo_root / s).resolve() for s in staged)


def x_staged_abs_set__mutmut_orig(repo_root: Path, staged: list[str]) -> frozenset[Path]:
    """The staged repo-relative paths resolved to absolute paths under
    ``repo_root`` — the membership set :func:`filter_to_staged` keys on."""
    return frozenset((repo_root / s).resolve() for s in staged)


def x_staged_abs_set__mutmut_1(repo_root: Path, staged: list[str]) -> frozenset[Path]:
    """The staged repo-relative paths resolved to absolute paths under
    ``repo_root`` — the membership set :func:`filter_to_staged` keys on."""
    return frozenset(None)


def x_staged_abs_set__mutmut_2(repo_root: Path, staged: list[str]) -> frozenset[Path]:
    """The staged repo-relative paths resolved to absolute paths under
    ``repo_root`` — the membership set :func:`filter_to_staged` keys on."""
    return frozenset((repo_root * s).resolve() for s in staged)

mutants_x_staged_abs_set__mutmut['_mutmut_orig'] = x_staged_abs_set__mutmut_orig # type: ignore # mutmut generated
mutants_x_staged_abs_set__mutmut['x_staged_abs_set__mutmut_1'] = x_staged_abs_set__mutmut_1 # type: ignore # mutmut generated
mutants_x_staged_abs_set__mutmut['x_staged_abs_set__mutmut_2'] = x_staged_abs_set__mutmut_2 # type: ignore # mutmut generated


@contextmanager
def restrict_python_files(repo_root: Path, staged: list[str]) -> Iterator[None]:
    """Narrow the package-level :func:`tc_fitness.python_files` to ``staged``.

    The repo-agnostic half of the enumeration narrowing: any check that
    enumerates through ``tc_fitness.python_files`` (directly or via
    :func:`tc_fitness.main_entry`) yields only the staged files for the
    duration of the ``with`` block. A consumer with additional enumeration
    surfaces (a ``FitnessRule.enumerate_files`` ABC, per-check ``from
    tc_fitness import python_files`` bindings) supplies its own
    :data:`EnumerationNarrower` that layers those on top of this one.
    """
    import tc_fitness

    staged_abs = staged_abs_set(repo_root, staged)
    real_python_files = tc_fitness.python_files

    def _scoped_python_files(*roots: str, repo_root: Path | None = None, **kwargs: object) -> list[Path]:
        full = real_python_files(*roots, repo_root=repo_root, **kwargs)
        return filter_to_staged(full, staged_abs)

    tc_fitness.python_files = _scoped_python_files
    try:
        yield
    finally:
        tc_fitness.python_files = real_python_files


# ── declarative factories (v0.4.0 seam absorption) ───────────────────────────
#
# Two factories that turn the consumer-side ``ScopeResolver`` /
# ``EnumerationNarrower`` callables kairix hand-codes into declarative engine
# config. They reproduce kairix's behaviour EXACTLY when the consumer passes its
# own attr names / ABC type / fallback roots — but the engine bakes in NO
# repo-domain default (no ``"RULE"``, no ``"kairix"``, no particular ABC). Shared
# machinery, per-repo domain.

# A location marker generalises kairix's "this check imports the location /
# singleton engine → walk the production package" branch. Given the imported
# check module, it returns the scan roots to use, or ``None`` if the marker
# doesn't apply. The engine never assumes what the marker is.
LocationMarker = Callable[[object], "tuple[str, ...] | None"]
mutants_x_make_module_roots_resolver__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_make_module_roots_resolver__mutmut)
def make_module_roots_resolver(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_orig(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_1(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "XXrootsXX",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_2(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "ROOTS",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_3(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = False,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_4(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = None
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_5(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_6(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None or checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_7(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_8(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = None
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_9(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(None)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_10(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_11(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(None, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_12(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, None)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_13(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_14(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, )

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_15(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(1, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_16(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_17(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(None):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_18(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith("XX.pyXX"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_19(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".PY"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_20(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: +len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_21(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = None
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_22(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(None)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_23(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_24(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = None
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_25(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(None, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_26(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, None, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_27(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_28(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_29(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, )
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_30(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = None
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_31(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(None, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_32(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, None, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_33(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_34(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_35(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, )
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_36(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) or boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_37(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_38(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(None, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_39(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, None):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_40(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_41(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, ):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_42(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type and not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_43(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is not abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_44(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_45(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(None, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_46(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, None):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_47(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_48(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, ):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_49(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    break
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_50(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ == module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_51(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    break
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_52(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = None
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_53(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(None, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_54(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, None, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_55(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_56(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_57(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, )
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_58(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) or roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_59(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_60(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = None
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_61(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(None)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_62(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_63(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = None
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_64(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(None)
        if module_name is None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_65(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is not None:
            return None
        return _roots_from_module(module_name)

    return _resolver


def x_make_module_roots_resolver__mutmut_66(
    *,
    boundary_rule_attr: str | None = None,
    roots_attr: str = "roots",
    abc_type: type | None = None,
    abc_roots_attr: str | None = None,
    location_marker: LocationMarker | None = None,
    fallback_roots: tuple[str, ...] | None = None,
    checks_dir: Path | None = None,
    checks_dir_on_path: bool = True,
) -> ScopeResolver:
    """Build a :data:`ScopeResolver` that derives a check module's scan roots.

    Generalises kairix's ``_kairix_scope_resolver`` / ``_roots_from_module``
    into declarative config. The returned resolver maps a check ``script``
    filename to the rule's repo-relative scan roots, reading — in order of
    specificity:

    1. when ``boundary_rule_attr`` is given, a module-level object named by it
       (kairix passes ``"RULE"``) carrying a non-empty tuple under ``roots_attr``
       (default ``"roots"``);
    2. when ``abc_type`` is given, the check module's OWN subclass of
       ``abc_type`` (one whose ``__module__`` is the check module — the imported
       base and re-exports are skipped) and its non-empty ``abc_roots_attr``
       tuple (defaults to ``roots_attr``);
    3. when ``location_marker`` is given, whatever roots it returns for the
       imported module (its way of expressing "this kind of check walks the
       production package");
    4. otherwise ``fallback_roots`` (default ``None``).

    A ``.sh`` detector (no python module to introspect) and an un-importable
    module both resolve to ``None`` — the caller treats that as
    always-in-scope (fail-safe, never a silent skip).

    Every attribute name, the ABC type, the location marker, and the fallback
    roots are CONFIG — the engine bakes in NO repo-specific default. In
    particular ``boundary_rule_attr`` defaults to ``None`` (the boundary-rule
    branch is OFF unless configured), so kairix's ``"RULE"`` convention is not
    privileged as the engine default; kairix passes ``boundary_rule_attr="RULE"``
    / ``abc_type=FitnessRule`` / its location marker / ``fallback_roots`` and
    another repo passes its own.

    Args:
        boundary_rule_attr: module-level attribute holding the boundary-rule
            object (kairix passes ``"RULE"``); ``None`` (default) disables the
            boundary-rule branch — no repo's convention is privileged.
        roots_attr: attribute on the boundary-rule object holding the roots
            tuple (kairix: ``"roots"``).
        abc_type: the ABC whose in-module subclass declares ``roots``; ``None``
            disables the ABC branch.
        abc_roots_attr: the roots attribute on the ABC subclass; defaults to
            ``roots_attr``.
        location_marker: a ``(module) -> tuple[str, ...] | None`` hook for the
            "walks the production package" branch; ``None`` disables it.
        fallback_roots: the roots when nothing else resolves.
        checks_dir: directory holding the check modules; put on ``sys.path`` for
            ``import_module`` when ``checks_dir_on_path`` (default).
        checks_dir_on_path: whether to insert ``checks_dir`` onto ``sys.path``.
    """
    effective_abc_roots_attr = abc_roots_attr if abc_roots_attr is not None else roots_attr
    if checks_dir is not None and checks_dir_on_path:
        checks_dir_str = str(checks_dir)
        if checks_dir_str not in sys.path:
            sys.path.insert(0, checks_dir_str)

    def _module_name_for(script: str) -> str | None:
        if not script.endswith(".py"):
            return None
        return script[: -len(".py")]

    def _roots_from_module(module_name: str) -> tuple[str, ...] | None:
        try:
            module = importlib.import_module(module_name)
        except BaseException:  # pragma: no cover - import hiccup → fail-safe None
            return None

        if boundary_rule_attr is not None:
            rule = getattr(module, boundary_rule_attr, None)
            boundary_roots = getattr(rule, roots_attr, None)
            if isinstance(boundary_roots, tuple) and boundary_roots:
                return boundary_roots

        if abc_type is not None:
            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if obj is abc_type or not issubclass(obj, abc_type):
                    continue
                if obj.__module__ != module.__name__:
                    # The imported base / re-exports — only the check's OWN
                    # subclass declares its scan roots.
                    continue
                roots = getattr(obj, effective_abc_roots_attr, None)
                if isinstance(roots, tuple) and roots:
                    return roots

        if location_marker is not None:
            marked = location_marker(module)
            if marked is not None:
                return marked

        return fallback_roots

    def _resolver(script: str) -> tuple[str, ...] | None:
        module_name = _module_name_for(script)
        if module_name is None:
            return None
        return _roots_from_module(None)

    return _resolver

mutants_x_make_module_roots_resolver__mutmut['_mutmut_orig'] = x_make_module_roots_resolver__mutmut_orig # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_1'] = x_make_module_roots_resolver__mutmut_1 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_2'] = x_make_module_roots_resolver__mutmut_2 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_3'] = x_make_module_roots_resolver__mutmut_3 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_4'] = x_make_module_roots_resolver__mutmut_4 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_5'] = x_make_module_roots_resolver__mutmut_5 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_6'] = x_make_module_roots_resolver__mutmut_6 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_7'] = x_make_module_roots_resolver__mutmut_7 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_8'] = x_make_module_roots_resolver__mutmut_8 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_9'] = x_make_module_roots_resolver__mutmut_9 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_10'] = x_make_module_roots_resolver__mutmut_10 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_11'] = x_make_module_roots_resolver__mutmut_11 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_12'] = x_make_module_roots_resolver__mutmut_12 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_13'] = x_make_module_roots_resolver__mutmut_13 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_14'] = x_make_module_roots_resolver__mutmut_14 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_15'] = x_make_module_roots_resolver__mutmut_15 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_16'] = x_make_module_roots_resolver__mutmut_16 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_17'] = x_make_module_roots_resolver__mutmut_17 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_18'] = x_make_module_roots_resolver__mutmut_18 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_19'] = x_make_module_roots_resolver__mutmut_19 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_20'] = x_make_module_roots_resolver__mutmut_20 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_21'] = x_make_module_roots_resolver__mutmut_21 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_22'] = x_make_module_roots_resolver__mutmut_22 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_23'] = x_make_module_roots_resolver__mutmut_23 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_24'] = x_make_module_roots_resolver__mutmut_24 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_25'] = x_make_module_roots_resolver__mutmut_25 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_26'] = x_make_module_roots_resolver__mutmut_26 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_27'] = x_make_module_roots_resolver__mutmut_27 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_28'] = x_make_module_roots_resolver__mutmut_28 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_29'] = x_make_module_roots_resolver__mutmut_29 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_30'] = x_make_module_roots_resolver__mutmut_30 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_31'] = x_make_module_roots_resolver__mutmut_31 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_32'] = x_make_module_roots_resolver__mutmut_32 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_33'] = x_make_module_roots_resolver__mutmut_33 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_34'] = x_make_module_roots_resolver__mutmut_34 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_35'] = x_make_module_roots_resolver__mutmut_35 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_36'] = x_make_module_roots_resolver__mutmut_36 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_37'] = x_make_module_roots_resolver__mutmut_37 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_38'] = x_make_module_roots_resolver__mutmut_38 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_39'] = x_make_module_roots_resolver__mutmut_39 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_40'] = x_make_module_roots_resolver__mutmut_40 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_41'] = x_make_module_roots_resolver__mutmut_41 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_42'] = x_make_module_roots_resolver__mutmut_42 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_43'] = x_make_module_roots_resolver__mutmut_43 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_44'] = x_make_module_roots_resolver__mutmut_44 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_45'] = x_make_module_roots_resolver__mutmut_45 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_46'] = x_make_module_roots_resolver__mutmut_46 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_47'] = x_make_module_roots_resolver__mutmut_47 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_48'] = x_make_module_roots_resolver__mutmut_48 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_49'] = x_make_module_roots_resolver__mutmut_49 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_50'] = x_make_module_roots_resolver__mutmut_50 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_51'] = x_make_module_roots_resolver__mutmut_51 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_52'] = x_make_module_roots_resolver__mutmut_52 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_53'] = x_make_module_roots_resolver__mutmut_53 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_54'] = x_make_module_roots_resolver__mutmut_54 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_55'] = x_make_module_roots_resolver__mutmut_55 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_56'] = x_make_module_roots_resolver__mutmut_56 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_57'] = x_make_module_roots_resolver__mutmut_57 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_58'] = x_make_module_roots_resolver__mutmut_58 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_59'] = x_make_module_roots_resolver__mutmut_59 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_60'] = x_make_module_roots_resolver__mutmut_60 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_61'] = x_make_module_roots_resolver__mutmut_61 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_62'] = x_make_module_roots_resolver__mutmut_62 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_63'] = x_make_module_roots_resolver__mutmut_63 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_64'] = x_make_module_roots_resolver__mutmut_64 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_65'] = x_make_module_roots_resolver__mutmut_65 # type: ignore # mutmut generated
mutants_x_make_module_roots_resolver__mutmut['x_make_module_roots_resolver__mutmut_66'] = x_make_module_roots_resolver__mutmut_66 # type: ignore # mutmut generated


def make_binding_narrower(
    *,
    extra_method: tuple[type, str] | None = None,
) -> EnumerationNarrower:
    """Build an :data:`EnumerationNarrower` that narrows by-value bindings.

    Generalises the repo-agnostic half of kairix's
    ``_kairix_enumeration_narrower``. For the duration of the ``with`` block the
    returned context manager narrows — to the staged set, intersected with what
    each surface would otherwise walk:

    * every already-imported ``check_*`` module's local ``python_files`` name
      (bound BY VALUE at import, so re-patching the package attribute alone
      doesn't reach the local binding);
    * optionally, the bound method named by ``extra_method`` on the given type —
      the one kairix-specific residue (its ``FitnessRule.enumerate_files`` ABC
      method). The ``(type, method_name)`` pair is CONFIG; the engine bakes in no
      ABC. ``None`` (the default) narrows only the ``python_files`` surfaces.

    Composition with the runner's outer restrict
    --------------------------------------------
    The runner's ``_run_staged_one`` ALREADY wraps
    :func:`restrict_python_files` around this narrower, so this factory narrows
    ONLY the by-value bindings (no redundant internal restrict — that would
    double-wrap the package surface). Crucially, under that composition the
    package attribute ``tc_fitness.python_files`` has ALREADY been rebound to the
    outer restrict's scoped wrapper, so it can NOT be used as the
    original-binding identity reference: the pre-imported ``check_*`` modules
    bound the GENUINE original by value, and that no longer equals the package
    attribute. This factory therefore discovers the genuine original FROM the
    check modules themselves (the by-value bindings every pre-imported check
    shares) before patching, so the per-check narrowing fires under runner
    composition — the staged-mode optimisation the bug silently no-op'd.

    Everything is restored exactly on exit (each patched binding records its
    original). Correctness-preserving for file-local rules: the set a rule
    inspects becomes ``what-it-would-walk ∩ staged`` and the per-file verdict is
    identical to the full run.
    """

    @contextmanager
    def _narrower(repo_root: Path, staged: list[str]) -> Iterator[None]:
        import tc_fitness

        staged_abs = staged_abs_set(repo_root, staged)

        # Discover the genuine ORIGINAL ``python_files`` binding(s) up-front. The
        # package attribute may already be the outer restrict's scoped wrapper
        # (the runner wraps restrict_python_files around us), so capture the
        # by-value binding every pre-imported ``check_*`` module holds — that is
        # the genuine original, untouched by the outer restrict. We narrow any
        # check module bound to one of these original references; each scoped
        # wrapper closes over its own captured original so narrowing stays
        # ``original(...) ∩ staged``.
        check_modules = [
            module
            for module in list(sys.modules.values())
            if getattr(module, "__name__", "").startswith("check_")
            and getattr(module, "python_files", None) is not None
        ]
        original_bindings: set[object] = {m.python_files for m in check_modules}
        # The current package attribute is also an "original" worth narrowing
        # when no outer restrict is active (standalone use of this narrower).
        original_bindings.add(tc_fitness.python_files)

        def _make_scoped(real: Callable[..., list[Path]]) -> Callable[..., list[Path]]:
            def _scoped_python_files(
                *roots: str, repo_root: Path | None = None, **kwargs: object
            ) -> list[Path]:
                full = real(*roots, repo_root=repo_root, **kwargs)
                return filter_to_staged(full, staged_abs)

            return _scoped_python_files

        # Patch every already-imported check module that bound python_files BY
        # VALUE so its local reference also narrows. Each scoped wrapper closes
        # over the module's OWN original binding; record originals to restore.
        patched_modules: list[tuple[object, object]] = []
        for module in check_modules:
            bound = module.python_files
            if bound in original_bindings:
                patched_modules.append((module, bound))
                module.python_files = _make_scoped(bound)  # type: ignore[attr-defined]

        extra_original: Callable[..., Iterable[Path]] | None = None
        extra_owner: type | None = None
        extra_name = ""
        if extra_method is not None:
            extra_owner, extra_name = extra_method
            extra_original = getattr(extra_owner, extra_name)
            real_extra: Callable[..., Iterable[Path]] = extra_original

            def _scoped_extra(self: object, *a: object, **k: object) -> list[Path]:
                full = list(real_extra(self, *a, **k))
                return filter_to_staged(full, staged_abs)

            setattr(extra_owner, extra_name, _scoped_extra)

        try:
            yield
        finally:
            for patched, original in patched_modules:
                patched.python_files = original  # type: ignore[attr-defined]
            if extra_owner is not None and extra_original is not None:
                setattr(extra_owner, extra_name, extra_original)

    return _narrower


__all__ = [
    "ScopeResolver",
    "EnumerationNarrower",
    "LocationMarker",
    "StagedDecision",
    "decide",
    "resolve_staged_scope",
    "staged_in_scope",
    "filter_to_staged",
    "staged_abs_set",
    "restrict_python_files",
    "make_module_roots_resolver",
    "make_binding_narrower",
]
