"""Shared helpers for architecture-fitness checks across Three Cubes repos.

This module unions two independently-grown libraries into one source:

- **kairix** ``scripts/checks/_arch_lib.py`` — hard-gating helpers:
  :func:`gate`, :func:`python_files`, :func:`main_entry`, :func:`repo_relative`,
  and the :data:`REPO_ROOT` anchor. Each check reports a set of offending
  paths and fails whenever violations exist.

- **tc-agent-zone** ``scripts/checks/_lib/__init__.py`` — agent-actionable
  emit/YAML helpers: :func:`actionable`, :func:`emit_failures`, :func:`emit_pass`,
  :func:`load_yaml`, :func:`missing_keys`. These shape FAIL/PASS output per the
  canonical ``<what>; fix: <fix>; next: <nxt>`` form and load YAML with a
  ``(data, error)`` contract.

Both call patterns are preserved exactly so the ~80 kairix checks and ~95
tc-agent-zone checks can adopt this package without rewriting their call sites.

REPO_ROOT note
--------------
The original kairix module derived ``REPO_ROOT`` from its own file location
(``parent.parent.parent``). Inside an installed package that anchor is wrong,
so :data:`REPO_ROOT` here resolves from the current working directory, which is
the repo root when checks run from ``scripts/safe-commit.sh`` / pre-commit / CI.
Every gating helper also accepts an explicit ``repo_root`` argument; callers that
need isolation (tests, monorepo sub-trees) pass it directly rather than relying
on the default.
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# kairix _arch_lib surface — hard gating
# ---------------------------------------------------------------------------

# Anchored to CWD so an installed package gates the *consumer* repo, not the
# site-packages tree. Checks run from the repo root, so this is correct in the
# pre-commit / safe-commit / CI invocation paths. Pass repo_root= explicitly
# anywhere that assumption does not hold.
REPO_ROOT = Path.cwd()

_RED = "\033[0;31m"
_GREEN = "\033[0;32m"
_RESET = "\033[0m"


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x_gate__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_gate__mutmut)
def gate(
    name: str,
    current: set[Path],
    remediation: str,
    *,
    repo_root: Path | None = None,
) -> int:
    """Fail when any current path violates the rule; print + return exit code.

    Args:
        name: short rule name used in messages.
        current: set of repo-relative (or absolute under ``repo_root``) Paths
            with the violation.
        remediation: operator-actionable remediation hint.
        repo_root: repo root used to relativise
            absolute paths. Defaults to :data:`REPO_ROOT` (the CWD).

    Returns:
        ``0`` if there are no violations; ``1`` otherwise.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    current_rel = {p.relative_to(root) if p.is_absolute() else p for p in current}
    violations = sorted(current_rel)

    if violations:
        from tc_fitness.check_evidence import report_finding

        for path in violations:
            report_finding(name, path.as_posix(), remediation)
        print(f"{_RED}FAIL [arch:{name}]{_RESET} — violation(s) found:")
        for p in violations:
            print(f"  {p}")
        print()
        print(remediation)
        return 1
    print(f"{_GREEN}ok [arch:{name}]{_RESET} — clean.")
    return 0


def x_gate__mutmut_orig(
    name: str,
    current: set[Path],
    remediation: str,
    *,
    repo_root: Path | None = None,
) -> int:
    """Fail when any current path violates the rule; print + return exit code.

    Args:
        name: short rule name used in messages.
        current: set of repo-relative (or absolute under ``repo_root``) Paths
            with the violation.
        remediation: operator-actionable remediation hint.
        repo_root: repo root used to relativise
            absolute paths. Defaults to :data:`REPO_ROOT` (the CWD).

    Returns:
        ``0`` if there are no violations; ``1`` otherwise.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    current_rel = {p.relative_to(root) if p.is_absolute() else p for p in current}
    violations = sorted(current_rel)

    if violations:
        from tc_fitness.check_evidence import report_finding

        for path in violations:
            report_finding(name, path.as_posix(), remediation)
        print(f"{_RED}FAIL [arch:{name}]{_RESET} — violation(s) found:")
        for p in violations:
            print(f"  {p}")
        print()
        print(remediation)
        return 1
    print(f"{_GREEN}ok [arch:{name}]{_RESET} — clean.")
    return 0


def x_gate__mutmut_1(
    name: str,
    current: set[Path],
    remediation: str,
    *,
    repo_root: Path | None = None,
) -> int:
    """Fail when any current path violates the rule; print + return exit code.

    Args:
        name: short rule name used in messages.
        current: set of repo-relative (or absolute under ``repo_root``) Paths
            with the violation.
        remediation: operator-actionable remediation hint.
        repo_root: repo root used to relativise
            absolute paths. Defaults to :data:`REPO_ROOT` (the CWD).

    Returns:
        ``0`` if there are no violations; ``1`` otherwise.
    """
    root = None
    current_rel = {p.relative_to(root) if p.is_absolute() else p for p in current}
    violations = sorted(current_rel)

    if violations:
        from tc_fitness.check_evidence import report_finding

        for path in violations:
            report_finding(name, path.as_posix(), remediation)
        print(f"{_RED}FAIL [arch:{name}]{_RESET} — violation(s) found:")
        for p in violations:
            print(f"  {p}")
        print()
        print(remediation)
        return 1
    print(f"{_GREEN}ok [arch:{name}]{_RESET} — clean.")
    return 0


def x_gate__mutmut_2(
    name: str,
    current: set[Path],
    remediation: str,
    *,
    repo_root: Path | None = None,
) -> int:
    """Fail when any current path violates the rule; print + return exit code.

    Args:
        name: short rule name used in messages.
        current: set of repo-relative (or absolute under ``repo_root``) Paths
            with the violation.
        remediation: operator-actionable remediation hint.
        repo_root: repo root used to relativise
            absolute paths. Defaults to :data:`REPO_ROOT` (the CWD).

    Returns:
        ``0`` if there are no violations; ``1`` otherwise.
    """
    root = repo_root if repo_root is None else REPO_ROOT
    current_rel = {p.relative_to(root) if p.is_absolute() else p for p in current}
    violations = sorted(current_rel)

    if violations:
        from tc_fitness.check_evidence import report_finding

        for path in violations:
            report_finding(name, path.as_posix(), remediation)
        print(f"{_RED}FAIL [arch:{name}]{_RESET} — violation(s) found:")
        for p in violations:
            print(f"  {p}")
        print()
        print(remediation)
        return 1
    print(f"{_GREEN}ok [arch:{name}]{_RESET} — clean.")
    return 0


def x_gate__mutmut_3(
    name: str,
    current: set[Path],
    remediation: str,
    *,
    repo_root: Path | None = None,
) -> int:
    """Fail when any current path violates the rule; print + return exit code.

    Args:
        name: short rule name used in messages.
        current: set of repo-relative (or absolute under ``repo_root``) Paths
            with the violation.
        remediation: operator-actionable remediation hint.
        repo_root: repo root used to relativise
            absolute paths. Defaults to :data:`REPO_ROOT` (the CWD).

    Returns:
        ``0`` if there are no violations; ``1`` otherwise.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    current_rel = None
    violations = sorted(current_rel)

    if violations:
        from tc_fitness.check_evidence import report_finding

        for path in violations:
            report_finding(name, path.as_posix(), remediation)
        print(f"{_RED}FAIL [arch:{name}]{_RESET} — violation(s) found:")
        for p in violations:
            print(f"  {p}")
        print()
        print(remediation)
        return 1
    print(f"{_GREEN}ok [arch:{name}]{_RESET} — clean.")
    return 0


def x_gate__mutmut_4(
    name: str,
    current: set[Path],
    remediation: str,
    *,
    repo_root: Path | None = None,
) -> int:
    """Fail when any current path violates the rule; print + return exit code.

    Args:
        name: short rule name used in messages.
        current: set of repo-relative (or absolute under ``repo_root``) Paths
            with the violation.
        remediation: operator-actionable remediation hint.
        repo_root: repo root used to relativise
            absolute paths. Defaults to :data:`REPO_ROOT` (the CWD).

    Returns:
        ``0`` if there are no violations; ``1`` otherwise.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    current_rel = {p.relative_to(None) if p.is_absolute() else p for p in current}
    violations = sorted(current_rel)

    if violations:
        from tc_fitness.check_evidence import report_finding

        for path in violations:
            report_finding(name, path.as_posix(), remediation)
        print(f"{_RED}FAIL [arch:{name}]{_RESET} — violation(s) found:")
        for p in violations:
            print(f"  {p}")
        print()
        print(remediation)
        return 1
    print(f"{_GREEN}ok [arch:{name}]{_RESET} — clean.")
    return 0


def x_gate__mutmut_5(
    name: str,
    current: set[Path],
    remediation: str,
    *,
    repo_root: Path | None = None,
) -> int:
    """Fail when any current path violates the rule; print + return exit code.

    Args:
        name: short rule name used in messages.
        current: set of repo-relative (or absolute under ``repo_root``) Paths
            with the violation.
        remediation: operator-actionable remediation hint.
        repo_root: repo root used to relativise
            absolute paths. Defaults to :data:`REPO_ROOT` (the CWD).

    Returns:
        ``0`` if there are no violations; ``1`` otherwise.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    current_rel = {p.relative_to(root) if p.is_absolute() else p for p in current}
    violations = None

    if violations:
        from tc_fitness.check_evidence import report_finding

        for path in violations:
            report_finding(name, path.as_posix(), remediation)
        print(f"{_RED}FAIL [arch:{name}]{_RESET} — violation(s) found:")
        for p in violations:
            print(f"  {p}")
        print()
        print(remediation)
        return 1
    print(f"{_GREEN}ok [arch:{name}]{_RESET} — clean.")
    return 0


def x_gate__mutmut_6(
    name: str,
    current: set[Path],
    remediation: str,
    *,
    repo_root: Path | None = None,
) -> int:
    """Fail when any current path violates the rule; print + return exit code.

    Args:
        name: short rule name used in messages.
        current: set of repo-relative (or absolute under ``repo_root``) Paths
            with the violation.
        remediation: operator-actionable remediation hint.
        repo_root: repo root used to relativise
            absolute paths. Defaults to :data:`REPO_ROOT` (the CWD).

    Returns:
        ``0`` if there are no violations; ``1`` otherwise.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    current_rel = {p.relative_to(root) if p.is_absolute() else p for p in current}
    violations = sorted(None)

    if violations:
        from tc_fitness.check_evidence import report_finding

        for path in violations:
            report_finding(name, path.as_posix(), remediation)
        print(f"{_RED}FAIL [arch:{name}]{_RESET} — violation(s) found:")
        for p in violations:
            print(f"  {p}")
        print()
        print(remediation)
        return 1
    print(f"{_GREEN}ok [arch:{name}]{_RESET} — clean.")
    return 0


def x_gate__mutmut_7(
    name: str,
    current: set[Path],
    remediation: str,
    *,
    repo_root: Path | None = None,
) -> int:
    """Fail when any current path violates the rule; print + return exit code.

    Args:
        name: short rule name used in messages.
        current: set of repo-relative (or absolute under ``repo_root``) Paths
            with the violation.
        remediation: operator-actionable remediation hint.
        repo_root: repo root used to relativise
            absolute paths. Defaults to :data:`REPO_ROOT` (the CWD).

    Returns:
        ``0`` if there are no violations; ``1`` otherwise.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    current_rel = {p.relative_to(root) if p.is_absolute() else p for p in current}
    violations = sorted(current_rel)

    if violations:
        from tc_fitness.check_evidence import report_finding

        for path in violations:
            report_finding(None, path.as_posix(), remediation)
        print(f"{_RED}FAIL [arch:{name}]{_RESET} — violation(s) found:")
        for p in violations:
            print(f"  {p}")
        print()
        print(remediation)
        return 1
    print(f"{_GREEN}ok [arch:{name}]{_RESET} — clean.")
    return 0


def x_gate__mutmut_8(
    name: str,
    current: set[Path],
    remediation: str,
    *,
    repo_root: Path | None = None,
) -> int:
    """Fail when any current path violates the rule; print + return exit code.

    Args:
        name: short rule name used in messages.
        current: set of repo-relative (or absolute under ``repo_root``) Paths
            with the violation.
        remediation: operator-actionable remediation hint.
        repo_root: repo root used to relativise
            absolute paths. Defaults to :data:`REPO_ROOT` (the CWD).

    Returns:
        ``0`` if there are no violations; ``1`` otherwise.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    current_rel = {p.relative_to(root) if p.is_absolute() else p for p in current}
    violations = sorted(current_rel)

    if violations:
        from tc_fitness.check_evidence import report_finding

        for path in violations:
            report_finding(name, None, remediation)
        print(f"{_RED}FAIL [arch:{name}]{_RESET} — violation(s) found:")
        for p in violations:
            print(f"  {p}")
        print()
        print(remediation)
        return 1
    print(f"{_GREEN}ok [arch:{name}]{_RESET} — clean.")
    return 0


def x_gate__mutmut_9(
    name: str,
    current: set[Path],
    remediation: str,
    *,
    repo_root: Path | None = None,
) -> int:
    """Fail when any current path violates the rule; print + return exit code.

    Args:
        name: short rule name used in messages.
        current: set of repo-relative (or absolute under ``repo_root``) Paths
            with the violation.
        remediation: operator-actionable remediation hint.
        repo_root: repo root used to relativise
            absolute paths. Defaults to :data:`REPO_ROOT` (the CWD).

    Returns:
        ``0`` if there are no violations; ``1`` otherwise.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    current_rel = {p.relative_to(root) if p.is_absolute() else p for p in current}
    violations = sorted(current_rel)

    if violations:
        from tc_fitness.check_evidence import report_finding

        for path in violations:
            report_finding(name, path.as_posix(), None)
        print(f"{_RED}FAIL [arch:{name}]{_RESET} — violation(s) found:")
        for p in violations:
            print(f"  {p}")
        print()
        print(remediation)
        return 1
    print(f"{_GREEN}ok [arch:{name}]{_RESET} — clean.")
    return 0


def x_gate__mutmut_10(
    name: str,
    current: set[Path],
    remediation: str,
    *,
    repo_root: Path | None = None,
) -> int:
    """Fail when any current path violates the rule; print + return exit code.

    Args:
        name: short rule name used in messages.
        current: set of repo-relative (or absolute under ``repo_root``) Paths
            with the violation.
        remediation: operator-actionable remediation hint.
        repo_root: repo root used to relativise
            absolute paths. Defaults to :data:`REPO_ROOT` (the CWD).

    Returns:
        ``0`` if there are no violations; ``1`` otherwise.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    current_rel = {p.relative_to(root) if p.is_absolute() else p for p in current}
    violations = sorted(current_rel)

    if violations:
        from tc_fitness.check_evidence import report_finding

        for path in violations:
            report_finding(path.as_posix(), remediation)
        print(f"{_RED}FAIL [arch:{name}]{_RESET} — violation(s) found:")
        for p in violations:
            print(f"  {p}")
        print()
        print(remediation)
        return 1
    print(f"{_GREEN}ok [arch:{name}]{_RESET} — clean.")
    return 0


def x_gate__mutmut_11(
    name: str,
    current: set[Path],
    remediation: str,
    *,
    repo_root: Path | None = None,
) -> int:
    """Fail when any current path violates the rule; print + return exit code.

    Args:
        name: short rule name used in messages.
        current: set of repo-relative (or absolute under ``repo_root``) Paths
            with the violation.
        remediation: operator-actionable remediation hint.
        repo_root: repo root used to relativise
            absolute paths. Defaults to :data:`REPO_ROOT` (the CWD).

    Returns:
        ``0`` if there are no violations; ``1`` otherwise.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    current_rel = {p.relative_to(root) if p.is_absolute() else p for p in current}
    violations = sorted(current_rel)

    if violations:
        from tc_fitness.check_evidence import report_finding

        for path in violations:
            report_finding(name, remediation)
        print(f"{_RED}FAIL [arch:{name}]{_RESET} — violation(s) found:")
        for p in violations:
            print(f"  {p}")
        print()
        print(remediation)
        return 1
    print(f"{_GREEN}ok [arch:{name}]{_RESET} — clean.")
    return 0


def x_gate__mutmut_12(
    name: str,
    current: set[Path],
    remediation: str,
    *,
    repo_root: Path | None = None,
) -> int:
    """Fail when any current path violates the rule; print + return exit code.

    Args:
        name: short rule name used in messages.
        current: set of repo-relative (or absolute under ``repo_root``) Paths
            with the violation.
        remediation: operator-actionable remediation hint.
        repo_root: repo root used to relativise
            absolute paths. Defaults to :data:`REPO_ROOT` (the CWD).

    Returns:
        ``0`` if there are no violations; ``1`` otherwise.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    current_rel = {p.relative_to(root) if p.is_absolute() else p for p in current}
    violations = sorted(current_rel)

    if violations:
        from tc_fitness.check_evidence import report_finding

        for path in violations:
            report_finding(name, path.as_posix(), )
        print(f"{_RED}FAIL [arch:{name}]{_RESET} — violation(s) found:")
        for p in violations:
            print(f"  {p}")
        print()
        print(remediation)
        return 1
    print(f"{_GREEN}ok [arch:{name}]{_RESET} — clean.")
    return 0


def x_gate__mutmut_13(
    name: str,
    current: set[Path],
    remediation: str,
    *,
    repo_root: Path | None = None,
) -> int:
    """Fail when any current path violates the rule; print + return exit code.

    Args:
        name: short rule name used in messages.
        current: set of repo-relative (or absolute under ``repo_root``) Paths
            with the violation.
        remediation: operator-actionable remediation hint.
        repo_root: repo root used to relativise
            absolute paths. Defaults to :data:`REPO_ROOT` (the CWD).

    Returns:
        ``0`` if there are no violations; ``1`` otherwise.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    current_rel = {p.relative_to(root) if p.is_absolute() else p for p in current}
    violations = sorted(current_rel)

    if violations:
        from tc_fitness.check_evidence import report_finding

        for path in violations:
            report_finding(name, path.as_posix(), remediation)
        print(None)
        for p in violations:
            print(f"  {p}")
        print()
        print(remediation)
        return 1
    print(f"{_GREEN}ok [arch:{name}]{_RESET} — clean.")
    return 0


def x_gate__mutmut_14(
    name: str,
    current: set[Path],
    remediation: str,
    *,
    repo_root: Path | None = None,
) -> int:
    """Fail when any current path violates the rule; print + return exit code.

    Args:
        name: short rule name used in messages.
        current: set of repo-relative (or absolute under ``repo_root``) Paths
            with the violation.
        remediation: operator-actionable remediation hint.
        repo_root: repo root used to relativise
            absolute paths. Defaults to :data:`REPO_ROOT` (the CWD).

    Returns:
        ``0`` if there are no violations; ``1`` otherwise.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    current_rel = {p.relative_to(root) if p.is_absolute() else p for p in current}
    violations = sorted(current_rel)

    if violations:
        from tc_fitness.check_evidence import report_finding

        for path in violations:
            report_finding(name, path.as_posix(), remediation)
        print(f"{_RED}FAIL [arch:{name}]{_RESET} — violation(s) found:")
        for p in violations:
            print(None)
        print()
        print(remediation)
        return 1
    print(f"{_GREEN}ok [arch:{name}]{_RESET} — clean.")
    return 0


def x_gate__mutmut_15(
    name: str,
    current: set[Path],
    remediation: str,
    *,
    repo_root: Path | None = None,
) -> int:
    """Fail when any current path violates the rule; print + return exit code.

    Args:
        name: short rule name used in messages.
        current: set of repo-relative (or absolute under ``repo_root``) Paths
            with the violation.
        remediation: operator-actionable remediation hint.
        repo_root: repo root used to relativise
            absolute paths. Defaults to :data:`REPO_ROOT` (the CWD).

    Returns:
        ``0`` if there are no violations; ``1`` otherwise.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    current_rel = {p.relative_to(root) if p.is_absolute() else p for p in current}
    violations = sorted(current_rel)

    if violations:
        from tc_fitness.check_evidence import report_finding

        for path in violations:
            report_finding(name, path.as_posix(), remediation)
        print(f"{_RED}FAIL [arch:{name}]{_RESET} — violation(s) found:")
        for p in violations:
            print(f"  {p}")
        print()
        print(None)
        return 1
    print(f"{_GREEN}ok [arch:{name}]{_RESET} — clean.")
    return 0


def x_gate__mutmut_16(
    name: str,
    current: set[Path],
    remediation: str,
    *,
    repo_root: Path | None = None,
) -> int:
    """Fail when any current path violates the rule; print + return exit code.

    Args:
        name: short rule name used in messages.
        current: set of repo-relative (or absolute under ``repo_root``) Paths
            with the violation.
        remediation: operator-actionable remediation hint.
        repo_root: repo root used to relativise
            absolute paths. Defaults to :data:`REPO_ROOT` (the CWD).

    Returns:
        ``0`` if there are no violations; ``1`` otherwise.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    current_rel = {p.relative_to(root) if p.is_absolute() else p for p in current}
    violations = sorted(current_rel)

    if violations:
        from tc_fitness.check_evidence import report_finding

        for path in violations:
            report_finding(name, path.as_posix(), remediation)
        print(f"{_RED}FAIL [arch:{name}]{_RESET} — violation(s) found:")
        for p in violations:
            print(f"  {p}")
        print()
        print(remediation)
        return 2
    print(f"{_GREEN}ok [arch:{name}]{_RESET} — clean.")
    return 0


def x_gate__mutmut_17(
    name: str,
    current: set[Path],
    remediation: str,
    *,
    repo_root: Path | None = None,
) -> int:
    """Fail when any current path violates the rule; print + return exit code.

    Args:
        name: short rule name used in messages.
        current: set of repo-relative (or absolute under ``repo_root``) Paths
            with the violation.
        remediation: operator-actionable remediation hint.
        repo_root: repo root used to relativise
            absolute paths. Defaults to :data:`REPO_ROOT` (the CWD).

    Returns:
        ``0`` if there are no violations; ``1`` otherwise.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    current_rel = {p.relative_to(root) if p.is_absolute() else p for p in current}
    violations = sorted(current_rel)

    if violations:
        from tc_fitness.check_evidence import report_finding

        for path in violations:
            report_finding(name, path.as_posix(), remediation)
        print(f"{_RED}FAIL [arch:{name}]{_RESET} — violation(s) found:")
        for p in violations:
            print(f"  {p}")
        print()
        print(remediation)
        return 1
    print(None)
    return 0


def x_gate__mutmut_18(
    name: str,
    current: set[Path],
    remediation: str,
    *,
    repo_root: Path | None = None,
) -> int:
    """Fail when any current path violates the rule; print + return exit code.

    Args:
        name: short rule name used in messages.
        current: set of repo-relative (or absolute under ``repo_root``) Paths
            with the violation.
        remediation: operator-actionable remediation hint.
        repo_root: repo root used to relativise
            absolute paths. Defaults to :data:`REPO_ROOT` (the CWD).

    Returns:
        ``0`` if there are no violations; ``1`` otherwise.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    current_rel = {p.relative_to(root) if p.is_absolute() else p for p in current}
    violations = sorted(current_rel)

    if violations:
        from tc_fitness.check_evidence import report_finding

        for path in violations:
            report_finding(name, path.as_posix(), remediation)
        print(f"{_RED}FAIL [arch:{name}]{_RESET} — violation(s) found:")
        for p in violations:
            print(f"  {p}")
        print()
        print(remediation)
        return 1
    print(f"{_GREEN}ok [arch:{name}]{_RESET} — clean.")
    return 1

mutants_x_gate__mutmut['_mutmut_orig'] = x_gate__mutmut_orig # type: ignore # mutmut generated
mutants_x_gate__mutmut['x_gate__mutmut_1'] = x_gate__mutmut_1 # type: ignore # mutmut generated
mutants_x_gate__mutmut['x_gate__mutmut_2'] = x_gate__mutmut_2 # type: ignore # mutmut generated
mutants_x_gate__mutmut['x_gate__mutmut_3'] = x_gate__mutmut_3 # type: ignore # mutmut generated
mutants_x_gate__mutmut['x_gate__mutmut_4'] = x_gate__mutmut_4 # type: ignore # mutmut generated
mutants_x_gate__mutmut['x_gate__mutmut_5'] = x_gate__mutmut_5 # type: ignore # mutmut generated
mutants_x_gate__mutmut['x_gate__mutmut_6'] = x_gate__mutmut_6 # type: ignore # mutmut generated
mutants_x_gate__mutmut['x_gate__mutmut_7'] = x_gate__mutmut_7 # type: ignore # mutmut generated
mutants_x_gate__mutmut['x_gate__mutmut_8'] = x_gate__mutmut_8 # type: ignore # mutmut generated
mutants_x_gate__mutmut['x_gate__mutmut_9'] = x_gate__mutmut_9 # type: ignore # mutmut generated
mutants_x_gate__mutmut['x_gate__mutmut_10'] = x_gate__mutmut_10 # type: ignore # mutmut generated
mutants_x_gate__mutmut['x_gate__mutmut_11'] = x_gate__mutmut_11 # type: ignore # mutmut generated
mutants_x_gate__mutmut['x_gate__mutmut_12'] = x_gate__mutmut_12 # type: ignore # mutmut generated
mutants_x_gate__mutmut['x_gate__mutmut_13'] = x_gate__mutmut_13 # type: ignore # mutmut generated
mutants_x_gate__mutmut['x_gate__mutmut_14'] = x_gate__mutmut_14 # type: ignore # mutmut generated
mutants_x_gate__mutmut['x_gate__mutmut_15'] = x_gate__mutmut_15 # type: ignore # mutmut generated
mutants_x_gate__mutmut['x_gate__mutmut_16'] = x_gate__mutmut_16 # type: ignore # mutmut generated
mutants_x_gate__mutmut['x_gate__mutmut_17'] = x_gate__mutmut_17 # type: ignore # mutmut generated
mutants_x_gate__mutmut['x_gate__mutmut_18'] = x_gate__mutmut_18 # type: ignore # mutmut generated
mutants_x_gate_keys__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_gate_keys__mutmut)
def gate_keys(
    name: str,
    current: set[str],
    remediation: str,
    *,
    repo_root: Path | None = None,
) -> int:
    """Fail when any current opaque key violates the rule."""
    del repo_root
    violations = sorted(current)
    if violations:
        print(f"{_RED}FAIL [arch:{name}]{_RESET} — violation(s) found:")
        for key in violations:
            print(f"  {key}")
        print()
        print(remediation)
        return 1
    print(f"{_GREEN}ok [arch:{name}]{_RESET} — clean.")
    return 0


def x_gate_keys__mutmut_orig(
    name: str,
    current: set[str],
    remediation: str,
    *,
    repo_root: Path | None = None,
) -> int:
    """Fail when any current opaque key violates the rule."""
    del repo_root
    violations = sorted(current)
    if violations:
        print(f"{_RED}FAIL [arch:{name}]{_RESET} — violation(s) found:")
        for key in violations:
            print(f"  {key}")
        print()
        print(remediation)
        return 1
    print(f"{_GREEN}ok [arch:{name}]{_RESET} — clean.")
    return 0


def x_gate_keys__mutmut_1(
    name: str,
    current: set[str],
    remediation: str,
    *,
    repo_root: Path | None = None,
) -> int:
    """Fail when any current opaque key violates the rule."""
    del repo_root
    violations = None
    if violations:
        print(f"{_RED}FAIL [arch:{name}]{_RESET} — violation(s) found:")
        for key in violations:
            print(f"  {key}")
        print()
        print(remediation)
        return 1
    print(f"{_GREEN}ok [arch:{name}]{_RESET} — clean.")
    return 0


def x_gate_keys__mutmut_2(
    name: str,
    current: set[str],
    remediation: str,
    *,
    repo_root: Path | None = None,
) -> int:
    """Fail when any current opaque key violates the rule."""
    del repo_root
    violations = sorted(None)
    if violations:
        print(f"{_RED}FAIL [arch:{name}]{_RESET} — violation(s) found:")
        for key in violations:
            print(f"  {key}")
        print()
        print(remediation)
        return 1
    print(f"{_GREEN}ok [arch:{name}]{_RESET} — clean.")
    return 0


def x_gate_keys__mutmut_3(
    name: str,
    current: set[str],
    remediation: str,
    *,
    repo_root: Path | None = None,
) -> int:
    """Fail when any current opaque key violates the rule."""
    del repo_root
    violations = sorted(current)
    if violations:
        print(None)
        for key in violations:
            print(f"  {key}")
        print()
        print(remediation)
        return 1
    print(f"{_GREEN}ok [arch:{name}]{_RESET} — clean.")
    return 0


def x_gate_keys__mutmut_4(
    name: str,
    current: set[str],
    remediation: str,
    *,
    repo_root: Path | None = None,
) -> int:
    """Fail when any current opaque key violates the rule."""
    del repo_root
    violations = sorted(current)
    if violations:
        print(f"{_RED}FAIL [arch:{name}]{_RESET} — violation(s) found:")
        for key in violations:
            print(None)
        print()
        print(remediation)
        return 1
    print(f"{_GREEN}ok [arch:{name}]{_RESET} — clean.")
    return 0


def x_gate_keys__mutmut_5(
    name: str,
    current: set[str],
    remediation: str,
    *,
    repo_root: Path | None = None,
) -> int:
    """Fail when any current opaque key violates the rule."""
    del repo_root
    violations = sorted(current)
    if violations:
        print(f"{_RED}FAIL [arch:{name}]{_RESET} — violation(s) found:")
        for key in violations:
            print(f"  {key}")
        print()
        print(None)
        return 1
    print(f"{_GREEN}ok [arch:{name}]{_RESET} — clean.")
    return 0


def x_gate_keys__mutmut_6(
    name: str,
    current: set[str],
    remediation: str,
    *,
    repo_root: Path | None = None,
) -> int:
    """Fail when any current opaque key violates the rule."""
    del repo_root
    violations = sorted(current)
    if violations:
        print(f"{_RED}FAIL [arch:{name}]{_RESET} — violation(s) found:")
        for key in violations:
            print(f"  {key}")
        print()
        print(remediation)
        return 2
    print(f"{_GREEN}ok [arch:{name}]{_RESET} — clean.")
    return 0


def x_gate_keys__mutmut_7(
    name: str,
    current: set[str],
    remediation: str,
    *,
    repo_root: Path | None = None,
) -> int:
    """Fail when any current opaque key violates the rule."""
    del repo_root
    violations = sorted(current)
    if violations:
        print(f"{_RED}FAIL [arch:{name}]{_RESET} — violation(s) found:")
        for key in violations:
            print(f"  {key}")
        print()
        print(remediation)
        return 1
    print(None)
    return 0


def x_gate_keys__mutmut_8(
    name: str,
    current: set[str],
    remediation: str,
    *,
    repo_root: Path | None = None,
) -> int:
    """Fail when any current opaque key violates the rule."""
    del repo_root
    violations = sorted(current)
    if violations:
        print(f"{_RED}FAIL [arch:{name}]{_RESET} — violation(s) found:")
        for key in violations:
            print(f"  {key}")
        print()
        print(remediation)
        return 1
    print(f"{_GREEN}ok [arch:{name}]{_RESET} — clean.")
    return 1

mutants_x_gate_keys__mutmut['_mutmut_orig'] = x_gate_keys__mutmut_orig # type: ignore # mutmut generated
mutants_x_gate_keys__mutmut['x_gate_keys__mutmut_1'] = x_gate_keys__mutmut_1 # type: ignore # mutmut generated
mutants_x_gate_keys__mutmut['x_gate_keys__mutmut_2'] = x_gate_keys__mutmut_2 # type: ignore # mutmut generated
mutants_x_gate_keys__mutmut['x_gate_keys__mutmut_3'] = x_gate_keys__mutmut_3 # type: ignore # mutmut generated
mutants_x_gate_keys__mutmut['x_gate_keys__mutmut_4'] = x_gate_keys__mutmut_4 # type: ignore # mutmut generated
mutants_x_gate_keys__mutmut['x_gate_keys__mutmut_5'] = x_gate_keys__mutmut_5 # type: ignore # mutmut generated
mutants_x_gate_keys__mutmut['x_gate_keys__mutmut_6'] = x_gate_keys__mutmut_6 # type: ignore # mutmut generated
mutants_x_gate_keys__mutmut['x_gate_keys__mutmut_7'] = x_gate_keys__mutmut_7 # type: ignore # mutmut generated
mutants_x_gate_keys__mutmut['x_gate_keys__mutmut_8'] = x_gate_keys__mutmut_8 # type: ignore # mutmut generated
mutants_x_repo_relative__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_repo_relative__mutmut)
def repo_relative(path: Path, *, repo_root: Path | None = None) -> Path:
    """Convert an absolute path under the repo root to a repo-relative Path."""
    root = repo_root if repo_root is not None else REPO_ROOT
    return path.resolve().relative_to(root)


def x_repo_relative__mutmut_orig(path: Path, *, repo_root: Path | None = None) -> Path:
    """Convert an absolute path under the repo root to a repo-relative Path."""
    root = repo_root if repo_root is not None else REPO_ROOT
    return path.resolve().relative_to(root)


def x_repo_relative__mutmut_1(path: Path, *, repo_root: Path | None = None) -> Path:
    """Convert an absolute path under the repo root to a repo-relative Path."""
    root = None
    return path.resolve().relative_to(root)


def x_repo_relative__mutmut_2(path: Path, *, repo_root: Path | None = None) -> Path:
    """Convert an absolute path under the repo root to a repo-relative Path."""
    root = repo_root if repo_root is None else REPO_ROOT
    return path.resolve().relative_to(root)


def x_repo_relative__mutmut_3(path: Path, *, repo_root: Path | None = None) -> Path:
    """Convert an absolute path under the repo root to a repo-relative Path."""
    root = repo_root if repo_root is not None else REPO_ROOT
    return path.resolve().relative_to(None)

mutants_x_repo_relative__mutmut['_mutmut_orig'] = x_repo_relative__mutmut_orig # type: ignore # mutmut generated
mutants_x_repo_relative__mutmut['x_repo_relative__mutmut_1'] = x_repo_relative__mutmut_1 # type: ignore # mutmut generated
mutants_x_repo_relative__mutmut['x_repo_relative__mutmut_2'] = x_repo_relative__mutmut_2 # type: ignore # mutmut generated
mutants_x_repo_relative__mutmut['x_repo_relative__mutmut_3'] = x_repo_relative__mutmut_3 # type: ignore # mutmut generated
mutants_x_python_files__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_python_files__mutmut)
def python_files(*roots: str, repo_root: Path | None = None) -> list[Path]:
    """Return all ``.py`` files under the given relative roots, skipping ``__pycache__``."""
    root = repo_root if repo_root is not None else REPO_ROOT
    out: list[Path] = []
    for rel in roots:
        root_path = root / rel
        if not root_path.exists():
            continue
        for p in root_path.rglob("*.py"):
            if "__pycache__" in p.parts:
                continue
            out.append(p)
    return out


def x_python_files__mutmut_orig(*roots: str, repo_root: Path | None = None) -> list[Path]:
    """Return all ``.py`` files under the given relative roots, skipping ``__pycache__``."""
    root = repo_root if repo_root is not None else REPO_ROOT
    out: list[Path] = []
    for rel in roots:
        root_path = root / rel
        if not root_path.exists():
            continue
        for p in root_path.rglob("*.py"):
            if "__pycache__" in p.parts:
                continue
            out.append(p)
    return out


def x_python_files__mutmut_1(*roots: str, repo_root: Path | None = None) -> list[Path]:
    """Return all ``.py`` files under the given relative roots, skipping ``__pycache__``."""
    root = None
    out: list[Path] = []
    for rel in roots:
        root_path = root / rel
        if not root_path.exists():
            continue
        for p in root_path.rglob("*.py"):
            if "__pycache__" in p.parts:
                continue
            out.append(p)
    return out


def x_python_files__mutmut_2(*roots: str, repo_root: Path | None = None) -> list[Path]:
    """Return all ``.py`` files under the given relative roots, skipping ``__pycache__``."""
    root = repo_root if repo_root is None else REPO_ROOT
    out: list[Path] = []
    for rel in roots:
        root_path = root / rel
        if not root_path.exists():
            continue
        for p in root_path.rglob("*.py"):
            if "__pycache__" in p.parts:
                continue
            out.append(p)
    return out


def x_python_files__mutmut_3(*roots: str, repo_root: Path | None = None) -> list[Path]:
    """Return all ``.py`` files under the given relative roots, skipping ``__pycache__``."""
    root = repo_root if repo_root is not None else REPO_ROOT
    out: list[Path] = None
    for rel in roots:
        root_path = root / rel
        if not root_path.exists():
            continue
        for p in root_path.rglob("*.py"):
            if "__pycache__" in p.parts:
                continue
            out.append(p)
    return out


def x_python_files__mutmut_4(*roots: str, repo_root: Path | None = None) -> list[Path]:
    """Return all ``.py`` files under the given relative roots, skipping ``__pycache__``."""
    root = repo_root if repo_root is not None else REPO_ROOT
    out: list[Path] = []
    for rel in roots:
        root_path = None
        if not root_path.exists():
            continue
        for p in root_path.rglob("*.py"):
            if "__pycache__" in p.parts:
                continue
            out.append(p)
    return out


def x_python_files__mutmut_5(*roots: str, repo_root: Path | None = None) -> list[Path]:
    """Return all ``.py`` files under the given relative roots, skipping ``__pycache__``."""
    root = repo_root if repo_root is not None else REPO_ROOT
    out: list[Path] = []
    for rel in roots:
        root_path = root * rel
        if not root_path.exists():
            continue
        for p in root_path.rglob("*.py"):
            if "__pycache__" in p.parts:
                continue
            out.append(p)
    return out


def x_python_files__mutmut_6(*roots: str, repo_root: Path | None = None) -> list[Path]:
    """Return all ``.py`` files under the given relative roots, skipping ``__pycache__``."""
    root = repo_root if repo_root is not None else REPO_ROOT
    out: list[Path] = []
    for rel in roots:
        root_path = root / rel
        if root_path.exists():
            continue
        for p in root_path.rglob("*.py"):
            if "__pycache__" in p.parts:
                continue
            out.append(p)
    return out


def x_python_files__mutmut_7(*roots: str, repo_root: Path | None = None) -> list[Path]:
    """Return all ``.py`` files under the given relative roots, skipping ``__pycache__``."""
    root = repo_root if repo_root is not None else REPO_ROOT
    out: list[Path] = []
    for rel in roots:
        root_path = root / rel
        if not root_path.exists():
            break
        for p in root_path.rglob("*.py"):
            if "__pycache__" in p.parts:
                continue
            out.append(p)
    return out


def x_python_files__mutmut_8(*roots: str, repo_root: Path | None = None) -> list[Path]:
    """Return all ``.py`` files under the given relative roots, skipping ``__pycache__``."""
    root = repo_root if repo_root is not None else REPO_ROOT
    out: list[Path] = []
    for rel in roots:
        root_path = root / rel
        if not root_path.exists():
            continue
        for p in root_path.rglob(None):
            if "__pycache__" in p.parts:
                continue
            out.append(p)
    return out


def x_python_files__mutmut_9(*roots: str, repo_root: Path | None = None) -> list[Path]:
    """Return all ``.py`` files under the given relative roots, skipping ``__pycache__``."""
    root = repo_root if repo_root is not None else REPO_ROOT
    out: list[Path] = []
    for rel in roots:
        root_path = root / rel
        if not root_path.exists():
            continue
        for p in root_path.rglob("XX*.pyXX"):
            if "__pycache__" in p.parts:
                continue
            out.append(p)
    return out


def x_python_files__mutmut_10(*roots: str, repo_root: Path | None = None) -> list[Path]:
    """Return all ``.py`` files under the given relative roots, skipping ``__pycache__``."""
    root = repo_root if repo_root is not None else REPO_ROOT
    out: list[Path] = []
    for rel in roots:
        root_path = root / rel
        if not root_path.exists():
            continue
        for p in root_path.rglob("*.PY"):
            if "__pycache__" in p.parts:
                continue
            out.append(p)
    return out


def x_python_files__mutmut_11(*roots: str, repo_root: Path | None = None) -> list[Path]:
    """Return all ``.py`` files under the given relative roots, skipping ``__pycache__``."""
    root = repo_root if repo_root is not None else REPO_ROOT
    out: list[Path] = []
    for rel in roots:
        root_path = root / rel
        if not root_path.exists():
            continue
        for p in root_path.rglob("*.py"):
            if "XX__pycache__XX" in p.parts:
                continue
            out.append(p)
    return out


def x_python_files__mutmut_12(*roots: str, repo_root: Path | None = None) -> list[Path]:
    """Return all ``.py`` files under the given relative roots, skipping ``__pycache__``."""
    root = repo_root if repo_root is not None else REPO_ROOT
    out: list[Path] = []
    for rel in roots:
        root_path = root / rel
        if not root_path.exists():
            continue
        for p in root_path.rglob("*.py"):
            if "__PYCACHE__" in p.parts:
                continue
            out.append(p)
    return out


def x_python_files__mutmut_13(*roots: str, repo_root: Path | None = None) -> list[Path]:
    """Return all ``.py`` files under the given relative roots, skipping ``__pycache__``."""
    root = repo_root if repo_root is not None else REPO_ROOT
    out: list[Path] = []
    for rel in roots:
        root_path = root / rel
        if not root_path.exists():
            continue
        for p in root_path.rglob("*.py"):
            if "__pycache__" not in p.parts:
                continue
            out.append(p)
    return out


def x_python_files__mutmut_14(*roots: str, repo_root: Path | None = None) -> list[Path]:
    """Return all ``.py`` files under the given relative roots, skipping ``__pycache__``."""
    root = repo_root if repo_root is not None else REPO_ROOT
    out: list[Path] = []
    for rel in roots:
        root_path = root / rel
        if not root_path.exists():
            continue
        for p in root_path.rglob("*.py"):
            if "__pycache__" in p.parts:
                break
            out.append(p)
    return out


def x_python_files__mutmut_15(*roots: str, repo_root: Path | None = None) -> list[Path]:
    """Return all ``.py`` files under the given relative roots, skipping ``__pycache__``."""
    root = repo_root if repo_root is not None else REPO_ROOT
    out: list[Path] = []
    for rel in roots:
        root_path = root / rel
        if not root_path.exists():
            continue
        for p in root_path.rglob("*.py"):
            if "__pycache__" in p.parts:
                continue
            out.append(None)
    return out

mutants_x_python_files__mutmut['_mutmut_orig'] = x_python_files__mutmut_orig # type: ignore # mutmut generated
mutants_x_python_files__mutmut['x_python_files__mutmut_1'] = x_python_files__mutmut_1 # type: ignore # mutmut generated
mutants_x_python_files__mutmut['x_python_files__mutmut_2'] = x_python_files__mutmut_2 # type: ignore # mutmut generated
mutants_x_python_files__mutmut['x_python_files__mutmut_3'] = x_python_files__mutmut_3 # type: ignore # mutmut generated
mutants_x_python_files__mutmut['x_python_files__mutmut_4'] = x_python_files__mutmut_4 # type: ignore # mutmut generated
mutants_x_python_files__mutmut['x_python_files__mutmut_5'] = x_python_files__mutmut_5 # type: ignore # mutmut generated
mutants_x_python_files__mutmut['x_python_files__mutmut_6'] = x_python_files__mutmut_6 # type: ignore # mutmut generated
mutants_x_python_files__mutmut['x_python_files__mutmut_7'] = x_python_files__mutmut_7 # type: ignore # mutmut generated
mutants_x_python_files__mutmut['x_python_files__mutmut_8'] = x_python_files__mutmut_8 # type: ignore # mutmut generated
mutants_x_python_files__mutmut['x_python_files__mutmut_9'] = x_python_files__mutmut_9 # type: ignore # mutmut generated
mutants_x_python_files__mutmut['x_python_files__mutmut_10'] = x_python_files__mutmut_10 # type: ignore # mutmut generated
mutants_x_python_files__mutmut['x_python_files__mutmut_11'] = x_python_files__mutmut_11 # type: ignore # mutmut generated
mutants_x_python_files__mutmut['x_python_files__mutmut_12'] = x_python_files__mutmut_12 # type: ignore # mutmut generated
mutants_x_python_files__mutmut['x_python_files__mutmut_13'] = x_python_files__mutmut_13 # type: ignore # mutmut generated
mutants_x_python_files__mutmut['x_python_files__mutmut_14'] = x_python_files__mutmut_14 # type: ignore # mutmut generated
mutants_x_python_files__mutmut['x_python_files__mutmut_15'] = x_python_files__mutmut_15 # type: ignore # mutmut generated
mutants_x_main_entry__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main_entry__mutmut)
def main_entry(
    check_fn: Callable[[Path], object] | object,
    name: str,
    remediation: str,
    *roots: str,
    repo_root: Path | None = None,
) -> int:
    """Scan ``roots``, call ``check_fn(path)`` on each ``.py`` file, gate on the union.

    ``check_fn`` returns either ``True`` (file has a violation) or a falsy value.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    violations: set[Path] = set()
    for path in python_files(*roots, repo_root=root):
        if callable(check_fn) and check_fn(path):
            violations.add(repo_relative(path, repo_root=root))
    return gate(name, violations, remediation, repo_root=root)


def x_main_entry__mutmut_orig(
    check_fn: Callable[[Path], object] | object,
    name: str,
    remediation: str,
    *roots: str,
    repo_root: Path | None = None,
) -> int:
    """Scan ``roots``, call ``check_fn(path)`` on each ``.py`` file, gate on the union.

    ``check_fn`` returns either ``True`` (file has a violation) or a falsy value.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    violations: set[Path] = set()
    for path in python_files(*roots, repo_root=root):
        if callable(check_fn) and check_fn(path):
            violations.add(repo_relative(path, repo_root=root))
    return gate(name, violations, remediation, repo_root=root)


def x_main_entry__mutmut_1(
    check_fn: Callable[[Path], object] | object,
    name: str,
    remediation: str,
    *roots: str,
    repo_root: Path | None = None,
) -> int:
    """Scan ``roots``, call ``check_fn(path)`` on each ``.py`` file, gate on the union.

    ``check_fn`` returns either ``True`` (file has a violation) or a falsy value.
    """
    root = None
    violations: set[Path] = set()
    for path in python_files(*roots, repo_root=root):
        if callable(check_fn) and check_fn(path):
            violations.add(repo_relative(path, repo_root=root))
    return gate(name, violations, remediation, repo_root=root)


def x_main_entry__mutmut_2(
    check_fn: Callable[[Path], object] | object,
    name: str,
    remediation: str,
    *roots: str,
    repo_root: Path | None = None,
) -> int:
    """Scan ``roots``, call ``check_fn(path)`` on each ``.py`` file, gate on the union.

    ``check_fn`` returns either ``True`` (file has a violation) or a falsy value.
    """
    root = repo_root if repo_root is None else REPO_ROOT
    violations: set[Path] = set()
    for path in python_files(*roots, repo_root=root):
        if callable(check_fn) and check_fn(path):
            violations.add(repo_relative(path, repo_root=root))
    return gate(name, violations, remediation, repo_root=root)


def x_main_entry__mutmut_3(
    check_fn: Callable[[Path], object] | object,
    name: str,
    remediation: str,
    *roots: str,
    repo_root: Path | None = None,
) -> int:
    """Scan ``roots``, call ``check_fn(path)`` on each ``.py`` file, gate on the union.

    ``check_fn`` returns either ``True`` (file has a violation) or a falsy value.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    violations: set[Path] = None
    for path in python_files(*roots, repo_root=root):
        if callable(check_fn) and check_fn(path):
            violations.add(repo_relative(path, repo_root=root))
    return gate(name, violations, remediation, repo_root=root)


def x_main_entry__mutmut_4(
    check_fn: Callable[[Path], object] | object,
    name: str,
    remediation: str,
    *roots: str,
    repo_root: Path | None = None,
) -> int:
    """Scan ``roots``, call ``check_fn(path)`` on each ``.py`` file, gate on the union.

    ``check_fn`` returns either ``True`` (file has a violation) or a falsy value.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    violations: set[Path] = set()
    for path in python_files(*roots, repo_root=None):
        if callable(check_fn) and check_fn(path):
            violations.add(repo_relative(path, repo_root=root))
    return gate(name, violations, remediation, repo_root=root)


def x_main_entry__mutmut_5(
    check_fn: Callable[[Path], object] | object,
    name: str,
    remediation: str,
    *roots: str,
    repo_root: Path | None = None,
) -> int:
    """Scan ``roots``, call ``check_fn(path)`` on each ``.py`` file, gate on the union.

    ``check_fn`` returns either ``True`` (file has a violation) or a falsy value.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    violations: set[Path] = set()
    for path in python_files(repo_root=root):
        if callable(check_fn) and check_fn(path):
            violations.add(repo_relative(path, repo_root=root))
    return gate(name, violations, remediation, repo_root=root)


def x_main_entry__mutmut_6(
    check_fn: Callable[[Path], object] | object,
    name: str,
    remediation: str,
    *roots: str,
    repo_root: Path | None = None,
) -> int:
    """Scan ``roots``, call ``check_fn(path)`` on each ``.py`` file, gate on the union.

    ``check_fn`` returns either ``True`` (file has a violation) or a falsy value.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    violations: set[Path] = set()
    for path in python_files(*roots, ):
        if callable(check_fn) and check_fn(path):
            violations.add(repo_relative(path, repo_root=root))
    return gate(name, violations, remediation, repo_root=root)


def x_main_entry__mutmut_7(
    check_fn: Callable[[Path], object] | object,
    name: str,
    remediation: str,
    *roots: str,
    repo_root: Path | None = None,
) -> int:
    """Scan ``roots``, call ``check_fn(path)`` on each ``.py`` file, gate on the union.

    ``check_fn`` returns either ``True`` (file has a violation) or a falsy value.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    violations: set[Path] = set()
    for path in python_files(*roots, repo_root=root):
        if callable(check_fn) or check_fn(path):
            violations.add(repo_relative(path, repo_root=root))
    return gate(name, violations, remediation, repo_root=root)


def x_main_entry__mutmut_8(
    check_fn: Callable[[Path], object] | object,
    name: str,
    remediation: str,
    *roots: str,
    repo_root: Path | None = None,
) -> int:
    """Scan ``roots``, call ``check_fn(path)`` on each ``.py`` file, gate on the union.

    ``check_fn`` returns either ``True`` (file has a violation) or a falsy value.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    violations: set[Path] = set()
    for path in python_files(*roots, repo_root=root):
        if callable(None) and check_fn(path):
            violations.add(repo_relative(path, repo_root=root))
    return gate(name, violations, remediation, repo_root=root)


def x_main_entry__mutmut_9(
    check_fn: Callable[[Path], object] | object,
    name: str,
    remediation: str,
    *roots: str,
    repo_root: Path | None = None,
) -> int:
    """Scan ``roots``, call ``check_fn(path)`` on each ``.py`` file, gate on the union.

    ``check_fn`` returns either ``True`` (file has a violation) or a falsy value.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    violations: set[Path] = set()
    for path in python_files(*roots, repo_root=root):
        if callable(check_fn) and check_fn(None):
            violations.add(repo_relative(path, repo_root=root))
    return gate(name, violations, remediation, repo_root=root)


def x_main_entry__mutmut_10(
    check_fn: Callable[[Path], object] | object,
    name: str,
    remediation: str,
    *roots: str,
    repo_root: Path | None = None,
) -> int:
    """Scan ``roots``, call ``check_fn(path)`` on each ``.py`` file, gate on the union.

    ``check_fn`` returns either ``True`` (file has a violation) or a falsy value.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    violations: set[Path] = set()
    for path in python_files(*roots, repo_root=root):
        if callable(check_fn) and check_fn(path):
            violations.add(None)
    return gate(name, violations, remediation, repo_root=root)


def x_main_entry__mutmut_11(
    check_fn: Callable[[Path], object] | object,
    name: str,
    remediation: str,
    *roots: str,
    repo_root: Path | None = None,
) -> int:
    """Scan ``roots``, call ``check_fn(path)`` on each ``.py`` file, gate on the union.

    ``check_fn`` returns either ``True`` (file has a violation) or a falsy value.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    violations: set[Path] = set()
    for path in python_files(*roots, repo_root=root):
        if callable(check_fn) and check_fn(path):
            violations.add(repo_relative(None, repo_root=root))
    return gate(name, violations, remediation, repo_root=root)


def x_main_entry__mutmut_12(
    check_fn: Callable[[Path], object] | object,
    name: str,
    remediation: str,
    *roots: str,
    repo_root: Path | None = None,
) -> int:
    """Scan ``roots``, call ``check_fn(path)`` on each ``.py`` file, gate on the union.

    ``check_fn`` returns either ``True`` (file has a violation) or a falsy value.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    violations: set[Path] = set()
    for path in python_files(*roots, repo_root=root):
        if callable(check_fn) and check_fn(path):
            violations.add(repo_relative(path, repo_root=None))
    return gate(name, violations, remediation, repo_root=root)


def x_main_entry__mutmut_13(
    check_fn: Callable[[Path], object] | object,
    name: str,
    remediation: str,
    *roots: str,
    repo_root: Path | None = None,
) -> int:
    """Scan ``roots``, call ``check_fn(path)`` on each ``.py`` file, gate on the union.

    ``check_fn`` returns either ``True`` (file has a violation) or a falsy value.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    violations: set[Path] = set()
    for path in python_files(*roots, repo_root=root):
        if callable(check_fn) and check_fn(path):
            violations.add(repo_relative(repo_root=root))
    return gate(name, violations, remediation, repo_root=root)


def x_main_entry__mutmut_14(
    check_fn: Callable[[Path], object] | object,
    name: str,
    remediation: str,
    *roots: str,
    repo_root: Path | None = None,
) -> int:
    """Scan ``roots``, call ``check_fn(path)`` on each ``.py`` file, gate on the union.

    ``check_fn`` returns either ``True`` (file has a violation) or a falsy value.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    violations: set[Path] = set()
    for path in python_files(*roots, repo_root=root):
        if callable(check_fn) and check_fn(path):
            violations.add(repo_relative(path, ))
    return gate(name, violations, remediation, repo_root=root)


def x_main_entry__mutmut_15(
    check_fn: Callable[[Path], object] | object,
    name: str,
    remediation: str,
    *roots: str,
    repo_root: Path | None = None,
) -> int:
    """Scan ``roots``, call ``check_fn(path)`` on each ``.py`` file, gate on the union.

    ``check_fn`` returns either ``True`` (file has a violation) or a falsy value.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    violations: set[Path] = set()
    for path in python_files(*roots, repo_root=root):
        if callable(check_fn) and check_fn(path):
            violations.add(repo_relative(path, repo_root=root))
    return gate(None, violations, remediation, repo_root=root)


def x_main_entry__mutmut_16(
    check_fn: Callable[[Path], object] | object,
    name: str,
    remediation: str,
    *roots: str,
    repo_root: Path | None = None,
) -> int:
    """Scan ``roots``, call ``check_fn(path)`` on each ``.py`` file, gate on the union.

    ``check_fn`` returns either ``True`` (file has a violation) or a falsy value.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    violations: set[Path] = set()
    for path in python_files(*roots, repo_root=root):
        if callable(check_fn) and check_fn(path):
            violations.add(repo_relative(path, repo_root=root))
    return gate(name, None, remediation, repo_root=root)


def x_main_entry__mutmut_17(
    check_fn: Callable[[Path], object] | object,
    name: str,
    remediation: str,
    *roots: str,
    repo_root: Path | None = None,
) -> int:
    """Scan ``roots``, call ``check_fn(path)`` on each ``.py`` file, gate on the union.

    ``check_fn`` returns either ``True`` (file has a violation) or a falsy value.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    violations: set[Path] = set()
    for path in python_files(*roots, repo_root=root):
        if callable(check_fn) and check_fn(path):
            violations.add(repo_relative(path, repo_root=root))
    return gate(name, violations, None, repo_root=root)


def x_main_entry__mutmut_18(
    check_fn: Callable[[Path], object] | object,
    name: str,
    remediation: str,
    *roots: str,
    repo_root: Path | None = None,
) -> int:
    """Scan ``roots``, call ``check_fn(path)`` on each ``.py`` file, gate on the union.

    ``check_fn`` returns either ``True`` (file has a violation) or a falsy value.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    violations: set[Path] = set()
    for path in python_files(*roots, repo_root=root):
        if callable(check_fn) and check_fn(path):
            violations.add(repo_relative(path, repo_root=root))
    return gate(name, violations, remediation, repo_root=None)


def x_main_entry__mutmut_19(
    check_fn: Callable[[Path], object] | object,
    name: str,
    remediation: str,
    *roots: str,
    repo_root: Path | None = None,
) -> int:
    """Scan ``roots``, call ``check_fn(path)`` on each ``.py`` file, gate on the union.

    ``check_fn`` returns either ``True`` (file has a violation) or a falsy value.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    violations: set[Path] = set()
    for path in python_files(*roots, repo_root=root):
        if callable(check_fn) and check_fn(path):
            violations.add(repo_relative(path, repo_root=root))
    return gate(violations, remediation, repo_root=root)


def x_main_entry__mutmut_20(
    check_fn: Callable[[Path], object] | object,
    name: str,
    remediation: str,
    *roots: str,
    repo_root: Path | None = None,
) -> int:
    """Scan ``roots``, call ``check_fn(path)`` on each ``.py`` file, gate on the union.

    ``check_fn`` returns either ``True`` (file has a violation) or a falsy value.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    violations: set[Path] = set()
    for path in python_files(*roots, repo_root=root):
        if callable(check_fn) and check_fn(path):
            violations.add(repo_relative(path, repo_root=root))
    return gate(name, remediation, repo_root=root)


def x_main_entry__mutmut_21(
    check_fn: Callable[[Path], object] | object,
    name: str,
    remediation: str,
    *roots: str,
    repo_root: Path | None = None,
) -> int:
    """Scan ``roots``, call ``check_fn(path)`` on each ``.py`` file, gate on the union.

    ``check_fn`` returns either ``True`` (file has a violation) or a falsy value.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    violations: set[Path] = set()
    for path in python_files(*roots, repo_root=root):
        if callable(check_fn) and check_fn(path):
            violations.add(repo_relative(path, repo_root=root))
    return gate(name, violations, repo_root=root)


def x_main_entry__mutmut_22(
    check_fn: Callable[[Path], object] | object,
    name: str,
    remediation: str,
    *roots: str,
    repo_root: Path | None = None,
) -> int:
    """Scan ``roots``, call ``check_fn(path)`` on each ``.py`` file, gate on the union.

    ``check_fn`` returns either ``True`` (file has a violation) or a falsy value.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    violations: set[Path] = set()
    for path in python_files(*roots, repo_root=root):
        if callable(check_fn) and check_fn(path):
            violations.add(repo_relative(path, repo_root=root))
    return gate(name, violations, remediation, )

mutants_x_main_entry__mutmut['_mutmut_orig'] = x_main_entry__mutmut_orig # type: ignore # mutmut generated
mutants_x_main_entry__mutmut['x_main_entry__mutmut_1'] = x_main_entry__mutmut_1 # type: ignore # mutmut generated
mutants_x_main_entry__mutmut['x_main_entry__mutmut_2'] = x_main_entry__mutmut_2 # type: ignore # mutmut generated
mutants_x_main_entry__mutmut['x_main_entry__mutmut_3'] = x_main_entry__mutmut_3 # type: ignore # mutmut generated
mutants_x_main_entry__mutmut['x_main_entry__mutmut_4'] = x_main_entry__mutmut_4 # type: ignore # mutmut generated
mutants_x_main_entry__mutmut['x_main_entry__mutmut_5'] = x_main_entry__mutmut_5 # type: ignore # mutmut generated
mutants_x_main_entry__mutmut['x_main_entry__mutmut_6'] = x_main_entry__mutmut_6 # type: ignore # mutmut generated
mutants_x_main_entry__mutmut['x_main_entry__mutmut_7'] = x_main_entry__mutmut_7 # type: ignore # mutmut generated
mutants_x_main_entry__mutmut['x_main_entry__mutmut_8'] = x_main_entry__mutmut_8 # type: ignore # mutmut generated
mutants_x_main_entry__mutmut['x_main_entry__mutmut_9'] = x_main_entry__mutmut_9 # type: ignore # mutmut generated
mutants_x_main_entry__mutmut['x_main_entry__mutmut_10'] = x_main_entry__mutmut_10 # type: ignore # mutmut generated
mutants_x_main_entry__mutmut['x_main_entry__mutmut_11'] = x_main_entry__mutmut_11 # type: ignore # mutmut generated
mutants_x_main_entry__mutmut['x_main_entry__mutmut_12'] = x_main_entry__mutmut_12 # type: ignore # mutmut generated
mutants_x_main_entry__mutmut['x_main_entry__mutmut_13'] = x_main_entry__mutmut_13 # type: ignore # mutmut generated
mutants_x_main_entry__mutmut['x_main_entry__mutmut_14'] = x_main_entry__mutmut_14 # type: ignore # mutmut generated
mutants_x_main_entry__mutmut['x_main_entry__mutmut_15'] = x_main_entry__mutmut_15 # type: ignore # mutmut generated
mutants_x_main_entry__mutmut['x_main_entry__mutmut_16'] = x_main_entry__mutmut_16 # type: ignore # mutmut generated
mutants_x_main_entry__mutmut['x_main_entry__mutmut_17'] = x_main_entry__mutmut_17 # type: ignore # mutmut generated
mutants_x_main_entry__mutmut['x_main_entry__mutmut_18'] = x_main_entry__mutmut_18 # type: ignore # mutmut generated
mutants_x_main_entry__mutmut['x_main_entry__mutmut_19'] = x_main_entry__mutmut_19 # type: ignore # mutmut generated
mutants_x_main_entry__mutmut['x_main_entry__mutmut_20'] = x_main_entry__mutmut_20 # type: ignore # mutmut generated
mutants_x_main_entry__mutmut['x_main_entry__mutmut_21'] = x_main_entry__mutmut_21 # type: ignore # mutmut generated
mutants_x_main_entry__mutmut['x_main_entry__mutmut_22'] = x_main_entry__mutmut_22 # type: ignore # mutmut generated
mutants_x_actionable__mutmut: MutantDict = {}  # type: ignore


# ---------------------------------------------------------------------------
# tc-agent-zone _lib surface — agent-actionable emit / YAML
# ---------------------------------------------------------------------------


@_mutmut_mutated(mutants_x_actionable__mutmut)
def actionable(what: str, fix: str, nxt: str, run: str | None = None) -> str:
    """Format an agent-actionable single-line failure.

    Shape (default): ``<what>; fix: <fix>; next: <nxt>``. Standardising the shape
    lets the actionable-feedback parser keep up without chasing each call site's
    bespoke formatting.

    When ``run`` is supplied, a third ``; run: <run>`` marker is appended,
    yielding the 3-marker ``<what>; fix: <fix>; next: <nxt>; run: <run>`` form
    that tc-agent-zone's 59 fix/next/run checks emit. ``run`` defaults to
    ``None``, so the 2-marker v0.1.0 output is byte-identical for every existing
    call site.
    """
    base = f"{what}; fix: {fix}; next: {nxt}"
    if run is None:
        return base
    return f"{base}; run: {run}"


# ---------------------------------------------------------------------------
# tc-agent-zone _lib surface — agent-actionable emit / YAML
# ---------------------------------------------------------------------------


def x_actionable__mutmut_orig(what: str, fix: str, nxt: str, run: str | None = None) -> str:
    """Format an agent-actionable single-line failure.

    Shape (default): ``<what>; fix: <fix>; next: <nxt>``. Standardising the shape
    lets the actionable-feedback parser keep up without chasing each call site's
    bespoke formatting.

    When ``run`` is supplied, a third ``; run: <run>`` marker is appended,
    yielding the 3-marker ``<what>; fix: <fix>; next: <nxt>; run: <run>`` form
    that tc-agent-zone's 59 fix/next/run checks emit. ``run`` defaults to
    ``None``, so the 2-marker v0.1.0 output is byte-identical for every existing
    call site.
    """
    base = f"{what}; fix: {fix}; next: {nxt}"
    if run is None:
        return base
    return f"{base}; run: {run}"


# ---------------------------------------------------------------------------
# tc-agent-zone _lib surface — agent-actionable emit / YAML
# ---------------------------------------------------------------------------


def x_actionable__mutmut_1(what: str, fix: str, nxt: str, run: str | None = None) -> str:
    """Format an agent-actionable single-line failure.

    Shape (default): ``<what>; fix: <fix>; next: <nxt>``. Standardising the shape
    lets the actionable-feedback parser keep up without chasing each call site's
    bespoke formatting.

    When ``run`` is supplied, a third ``; run: <run>`` marker is appended,
    yielding the 3-marker ``<what>; fix: <fix>; next: <nxt>; run: <run>`` form
    that tc-agent-zone's 59 fix/next/run checks emit. ``run`` defaults to
    ``None``, so the 2-marker v0.1.0 output is byte-identical for every existing
    call site.
    """
    base = None
    if run is None:
        return base
    return f"{base}; run: {run}"


# ---------------------------------------------------------------------------
# tc-agent-zone _lib surface — agent-actionable emit / YAML
# ---------------------------------------------------------------------------


def x_actionable__mutmut_2(what: str, fix: str, nxt: str, run: str | None = None) -> str:
    """Format an agent-actionable single-line failure.

    Shape (default): ``<what>; fix: <fix>; next: <nxt>``. Standardising the shape
    lets the actionable-feedback parser keep up without chasing each call site's
    bespoke formatting.

    When ``run`` is supplied, a third ``; run: <run>`` marker is appended,
    yielding the 3-marker ``<what>; fix: <fix>; next: <nxt>; run: <run>`` form
    that tc-agent-zone's 59 fix/next/run checks emit. ``run`` defaults to
    ``None``, so the 2-marker v0.1.0 output is byte-identical for every existing
    call site.
    """
    base = f"{what}; fix: {fix}; next: {nxt}"
    if run is not None:
        return base
    return f"{base}; run: {run}"

mutants_x_actionable__mutmut['_mutmut_orig'] = x_actionable__mutmut_orig # type: ignore # mutmut generated
mutants_x_actionable__mutmut['x_actionable__mutmut_1'] = x_actionable__mutmut_1 # type: ignore # mutmut generated
mutants_x_actionable__mutmut['x_actionable__mutmut_2'] = x_actionable__mutmut_2 # type: ignore # mutmut generated
mutants_x_remediation__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_remediation__mutmut)
def remediation(
    fix: str,
    nxt: str,
    run: str,
    *,
    passing: str | None = None,
    forbidden: str | None = None,
) -> str:
    """Format the multiline ``fix:`` / ``next:`` / ``run:`` remediation block.

    The F21-shape block tc-agent-zone's 30 checks emit alongside a failure: the
    three action markers on their own lines, optionally followed by a ``Pass``
    example and a ``Forbidden`` example. Returns the joined block as one string
    (no trailing newline), ready to ``print()``.

    Example output::

        fix: redact the secret before logging
        next: re-run the check
        run: python scripts/checks/check_f15.py
        Pass: logger.info("token redacted")
        Forbidden: logger.info(f"token={token}")

    Args:
        fix: the corrective action.
        nxt: the follow-up step after fixing.
        run: the exact command to re-verify.
        passing: optional Pass-example line (omitted when ``None``).
        forbidden: optional Forbidden-example line (omitted when ``None``).
    """
    lines = [f"fix: {fix}", f"next: {nxt}", f"run: {run}"]
    if passing is not None:
        lines.append(f"Pass: {passing}")
    if forbidden is not None:
        lines.append(f"Forbidden: {forbidden}")
    return "\n".join(lines)


def x_remediation__mutmut_orig(
    fix: str,
    nxt: str,
    run: str,
    *,
    passing: str | None = None,
    forbidden: str | None = None,
) -> str:
    """Format the multiline ``fix:`` / ``next:`` / ``run:`` remediation block.

    The F21-shape block tc-agent-zone's 30 checks emit alongside a failure: the
    three action markers on their own lines, optionally followed by a ``Pass``
    example and a ``Forbidden`` example. Returns the joined block as one string
    (no trailing newline), ready to ``print()``.

    Example output::

        fix: redact the secret before logging
        next: re-run the check
        run: python scripts/checks/check_f15.py
        Pass: logger.info("token redacted")
        Forbidden: logger.info(f"token={token}")

    Args:
        fix: the corrective action.
        nxt: the follow-up step after fixing.
        run: the exact command to re-verify.
        passing: optional Pass-example line (omitted when ``None``).
        forbidden: optional Forbidden-example line (omitted when ``None``).
    """
    lines = [f"fix: {fix}", f"next: {nxt}", f"run: {run}"]
    if passing is not None:
        lines.append(f"Pass: {passing}")
    if forbidden is not None:
        lines.append(f"Forbidden: {forbidden}")
    return "\n".join(lines)


def x_remediation__mutmut_1(
    fix: str,
    nxt: str,
    run: str,
    *,
    passing: str | None = None,
    forbidden: str | None = None,
) -> str:
    """Format the multiline ``fix:`` / ``next:`` / ``run:`` remediation block.

    The F21-shape block tc-agent-zone's 30 checks emit alongside a failure: the
    three action markers on their own lines, optionally followed by a ``Pass``
    example and a ``Forbidden`` example. Returns the joined block as one string
    (no trailing newline), ready to ``print()``.

    Example output::

        fix: redact the secret before logging
        next: re-run the check
        run: python scripts/checks/check_f15.py
        Pass: logger.info("token redacted")
        Forbidden: logger.info(f"token={token}")

    Args:
        fix: the corrective action.
        nxt: the follow-up step after fixing.
        run: the exact command to re-verify.
        passing: optional Pass-example line (omitted when ``None``).
        forbidden: optional Forbidden-example line (omitted when ``None``).
    """
    lines = None
    if passing is not None:
        lines.append(f"Pass: {passing}")
    if forbidden is not None:
        lines.append(f"Forbidden: {forbidden}")
    return "\n".join(lines)


def x_remediation__mutmut_2(
    fix: str,
    nxt: str,
    run: str,
    *,
    passing: str | None = None,
    forbidden: str | None = None,
) -> str:
    """Format the multiline ``fix:`` / ``next:`` / ``run:`` remediation block.

    The F21-shape block tc-agent-zone's 30 checks emit alongside a failure: the
    three action markers on their own lines, optionally followed by a ``Pass``
    example and a ``Forbidden`` example. Returns the joined block as one string
    (no trailing newline), ready to ``print()``.

    Example output::

        fix: redact the secret before logging
        next: re-run the check
        run: python scripts/checks/check_f15.py
        Pass: logger.info("token redacted")
        Forbidden: logger.info(f"token={token}")

    Args:
        fix: the corrective action.
        nxt: the follow-up step after fixing.
        run: the exact command to re-verify.
        passing: optional Pass-example line (omitted when ``None``).
        forbidden: optional Forbidden-example line (omitted when ``None``).
    """
    lines = [f"fix: {fix}", f"next: {nxt}", f"run: {run}"]
    if passing is None:
        lines.append(f"Pass: {passing}")
    if forbidden is not None:
        lines.append(f"Forbidden: {forbidden}")
    return "\n".join(lines)


def x_remediation__mutmut_3(
    fix: str,
    nxt: str,
    run: str,
    *,
    passing: str | None = None,
    forbidden: str | None = None,
) -> str:
    """Format the multiline ``fix:`` / ``next:`` / ``run:`` remediation block.

    The F21-shape block tc-agent-zone's 30 checks emit alongside a failure: the
    three action markers on their own lines, optionally followed by a ``Pass``
    example and a ``Forbidden`` example. Returns the joined block as one string
    (no trailing newline), ready to ``print()``.

    Example output::

        fix: redact the secret before logging
        next: re-run the check
        run: python scripts/checks/check_f15.py
        Pass: logger.info("token redacted")
        Forbidden: logger.info(f"token={token}")

    Args:
        fix: the corrective action.
        nxt: the follow-up step after fixing.
        run: the exact command to re-verify.
        passing: optional Pass-example line (omitted when ``None``).
        forbidden: optional Forbidden-example line (omitted when ``None``).
    """
    lines = [f"fix: {fix}", f"next: {nxt}", f"run: {run}"]
    if passing is not None:
        lines.append(None)
    if forbidden is not None:
        lines.append(f"Forbidden: {forbidden}")
    return "\n".join(lines)


def x_remediation__mutmut_4(
    fix: str,
    nxt: str,
    run: str,
    *,
    passing: str | None = None,
    forbidden: str | None = None,
) -> str:
    """Format the multiline ``fix:`` / ``next:`` / ``run:`` remediation block.

    The F21-shape block tc-agent-zone's 30 checks emit alongside a failure: the
    three action markers on their own lines, optionally followed by a ``Pass``
    example and a ``Forbidden`` example. Returns the joined block as one string
    (no trailing newline), ready to ``print()``.

    Example output::

        fix: redact the secret before logging
        next: re-run the check
        run: python scripts/checks/check_f15.py
        Pass: logger.info("token redacted")
        Forbidden: logger.info(f"token={token}")

    Args:
        fix: the corrective action.
        nxt: the follow-up step after fixing.
        run: the exact command to re-verify.
        passing: optional Pass-example line (omitted when ``None``).
        forbidden: optional Forbidden-example line (omitted when ``None``).
    """
    lines = [f"fix: {fix}", f"next: {nxt}", f"run: {run}"]
    if passing is not None:
        lines.append(f"Pass: {passing}")
    if forbidden is None:
        lines.append(f"Forbidden: {forbidden}")
    return "\n".join(lines)


def x_remediation__mutmut_5(
    fix: str,
    nxt: str,
    run: str,
    *,
    passing: str | None = None,
    forbidden: str | None = None,
) -> str:
    """Format the multiline ``fix:`` / ``next:`` / ``run:`` remediation block.

    The F21-shape block tc-agent-zone's 30 checks emit alongside a failure: the
    three action markers on their own lines, optionally followed by a ``Pass``
    example and a ``Forbidden`` example. Returns the joined block as one string
    (no trailing newline), ready to ``print()``.

    Example output::

        fix: redact the secret before logging
        next: re-run the check
        run: python scripts/checks/check_f15.py
        Pass: logger.info("token redacted")
        Forbidden: logger.info(f"token={token}")

    Args:
        fix: the corrective action.
        nxt: the follow-up step after fixing.
        run: the exact command to re-verify.
        passing: optional Pass-example line (omitted when ``None``).
        forbidden: optional Forbidden-example line (omitted when ``None``).
    """
    lines = [f"fix: {fix}", f"next: {nxt}", f"run: {run}"]
    if passing is not None:
        lines.append(f"Pass: {passing}")
    if forbidden is not None:
        lines.append(None)
    return "\n".join(lines)


def x_remediation__mutmut_6(
    fix: str,
    nxt: str,
    run: str,
    *,
    passing: str | None = None,
    forbidden: str | None = None,
) -> str:
    """Format the multiline ``fix:`` / ``next:`` / ``run:`` remediation block.

    The F21-shape block tc-agent-zone's 30 checks emit alongside a failure: the
    three action markers on their own lines, optionally followed by a ``Pass``
    example and a ``Forbidden`` example. Returns the joined block as one string
    (no trailing newline), ready to ``print()``.

    Example output::

        fix: redact the secret before logging
        next: re-run the check
        run: python scripts/checks/check_f15.py
        Pass: logger.info("token redacted")
        Forbidden: logger.info(f"token={token}")

    Args:
        fix: the corrective action.
        nxt: the follow-up step after fixing.
        run: the exact command to re-verify.
        passing: optional Pass-example line (omitted when ``None``).
        forbidden: optional Forbidden-example line (omitted when ``None``).
    """
    lines = [f"fix: {fix}", f"next: {nxt}", f"run: {run}"]
    if passing is not None:
        lines.append(f"Pass: {passing}")
    if forbidden is not None:
        lines.append(f"Forbidden: {forbidden}")
    return "\n".join(None)


def x_remediation__mutmut_7(
    fix: str,
    nxt: str,
    run: str,
    *,
    passing: str | None = None,
    forbidden: str | None = None,
) -> str:
    """Format the multiline ``fix:`` / ``next:`` / ``run:`` remediation block.

    The F21-shape block tc-agent-zone's 30 checks emit alongside a failure: the
    three action markers on their own lines, optionally followed by a ``Pass``
    example and a ``Forbidden`` example. Returns the joined block as one string
    (no trailing newline), ready to ``print()``.

    Example output::

        fix: redact the secret before logging
        next: re-run the check
        run: python scripts/checks/check_f15.py
        Pass: logger.info("token redacted")
        Forbidden: logger.info(f"token={token}")

    Args:
        fix: the corrective action.
        nxt: the follow-up step after fixing.
        run: the exact command to re-verify.
        passing: optional Pass-example line (omitted when ``None``).
        forbidden: optional Forbidden-example line (omitted when ``None``).
    """
    lines = [f"fix: {fix}", f"next: {nxt}", f"run: {run}"]
    if passing is not None:
        lines.append(f"Pass: {passing}")
    if forbidden is not None:
        lines.append(f"Forbidden: {forbidden}")
    return "XX\nXX".join(lines)

mutants_x_remediation__mutmut['_mutmut_orig'] = x_remediation__mutmut_orig # type: ignore # mutmut generated
mutants_x_remediation__mutmut['x_remediation__mutmut_1'] = x_remediation__mutmut_1 # type: ignore # mutmut generated
mutants_x_remediation__mutmut['x_remediation__mutmut_2'] = x_remediation__mutmut_2 # type: ignore # mutmut generated
mutants_x_remediation__mutmut['x_remediation__mutmut_3'] = x_remediation__mutmut_3 # type: ignore # mutmut generated
mutants_x_remediation__mutmut['x_remediation__mutmut_4'] = x_remediation__mutmut_4 # type: ignore # mutmut generated
mutants_x_remediation__mutmut['x_remediation__mutmut_5'] = x_remediation__mutmut_5 # type: ignore # mutmut generated
mutants_x_remediation__mutmut['x_remediation__mutmut_6'] = x_remediation__mutmut_6 # type: ignore # mutmut generated
mutants_x_remediation__mutmut['x_remediation__mutmut_7'] = x_remediation__mutmut_7 # type: ignore # mutmut generated
mutants_x_emit_failures__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_emit_failures__mutmut)
def emit_failures(check_name: str, fails: list[str], stream: Any = None) -> None:
    """Emit the canonical FAIL banner + bulleted failure list.

    Defaults to ``sys.stderr`` (resolved at call time so tests can capture it).
    """
    out = stream if stream is not None else sys.stderr
    print(f"FAIL {check_name} ({len(fails)} violations)", file=out)
    for f in fails:
        print(f"  - {f}", file=out)


def x_emit_failures__mutmut_orig(check_name: str, fails: list[str], stream: Any = None) -> None:
    """Emit the canonical FAIL banner + bulleted failure list.

    Defaults to ``sys.stderr`` (resolved at call time so tests can capture it).
    """
    out = stream if stream is not None else sys.stderr
    print(f"FAIL {check_name} ({len(fails)} violations)", file=out)
    for f in fails:
        print(f"  - {f}", file=out)


def x_emit_failures__mutmut_1(check_name: str, fails: list[str], stream: Any = None) -> None:
    """Emit the canonical FAIL banner + bulleted failure list.

    Defaults to ``sys.stderr`` (resolved at call time so tests can capture it).
    """
    out = None
    print(f"FAIL {check_name} ({len(fails)} violations)", file=out)
    for f in fails:
        print(f"  - {f}", file=out)


def x_emit_failures__mutmut_2(check_name: str, fails: list[str], stream: Any = None) -> None:
    """Emit the canonical FAIL banner + bulleted failure list.

    Defaults to ``sys.stderr`` (resolved at call time so tests can capture it).
    """
    out = stream if stream is None else sys.stderr
    print(f"FAIL {check_name} ({len(fails)} violations)", file=out)
    for f in fails:
        print(f"  - {f}", file=out)


def x_emit_failures__mutmut_3(check_name: str, fails: list[str], stream: Any = None) -> None:
    """Emit the canonical FAIL banner + bulleted failure list.

    Defaults to ``sys.stderr`` (resolved at call time so tests can capture it).
    """
    out = stream if stream is not None else sys.stderr
    print(None, file=out)
    for f in fails:
        print(f"  - {f}", file=out)


def x_emit_failures__mutmut_4(check_name: str, fails: list[str], stream: Any = None) -> None:
    """Emit the canonical FAIL banner + bulleted failure list.

    Defaults to ``sys.stderr`` (resolved at call time so tests can capture it).
    """
    out = stream if stream is not None else sys.stderr
    print(f"FAIL {check_name} ({len(fails)} violations)", file=None)
    for f in fails:
        print(f"  - {f}", file=out)


def x_emit_failures__mutmut_5(check_name: str, fails: list[str], stream: Any = None) -> None:
    """Emit the canonical FAIL banner + bulleted failure list.

    Defaults to ``sys.stderr`` (resolved at call time so tests can capture it).
    """
    out = stream if stream is not None else sys.stderr
    print(file=out)
    for f in fails:
        print(f"  - {f}", file=out)


def x_emit_failures__mutmut_6(check_name: str, fails: list[str], stream: Any = None) -> None:
    """Emit the canonical FAIL banner + bulleted failure list.

    Defaults to ``sys.stderr`` (resolved at call time so tests can capture it).
    """
    out = stream if stream is not None else sys.stderr
    print(f"FAIL {check_name} ({len(fails)} violations)", )
    for f in fails:
        print(f"  - {f}", file=out)


def x_emit_failures__mutmut_7(check_name: str, fails: list[str], stream: Any = None) -> None:
    """Emit the canonical FAIL banner + bulleted failure list.

    Defaults to ``sys.stderr`` (resolved at call time so tests can capture it).
    """
    out = stream if stream is not None else sys.stderr
    print(f"FAIL {check_name} ({len(fails)} violations)", file=out)
    for f in fails:
        print(None, file=out)


def x_emit_failures__mutmut_8(check_name: str, fails: list[str], stream: Any = None) -> None:
    """Emit the canonical FAIL banner + bulleted failure list.

    Defaults to ``sys.stderr`` (resolved at call time so tests can capture it).
    """
    out = stream if stream is not None else sys.stderr
    print(f"FAIL {check_name} ({len(fails)} violations)", file=out)
    for f in fails:
        print(f"  - {f}", file=None)


def x_emit_failures__mutmut_9(check_name: str, fails: list[str], stream: Any = None) -> None:
    """Emit the canonical FAIL banner + bulleted failure list.

    Defaults to ``sys.stderr`` (resolved at call time so tests can capture it).
    """
    out = stream if stream is not None else sys.stderr
    print(f"FAIL {check_name} ({len(fails)} violations)", file=out)
    for f in fails:
        print(file=out)


def x_emit_failures__mutmut_10(check_name: str, fails: list[str], stream: Any = None) -> None:
    """Emit the canonical FAIL banner + bulleted failure list.

    Defaults to ``sys.stderr`` (resolved at call time so tests can capture it).
    """
    out = stream if stream is not None else sys.stderr
    print(f"FAIL {check_name} ({len(fails)} violations)", file=out)
    for f in fails:
        print(f"  - {f}", )

mutants_x_emit_failures__mutmut['_mutmut_orig'] = x_emit_failures__mutmut_orig # type: ignore # mutmut generated
mutants_x_emit_failures__mutmut['x_emit_failures__mutmut_1'] = x_emit_failures__mutmut_1 # type: ignore # mutmut generated
mutants_x_emit_failures__mutmut['x_emit_failures__mutmut_2'] = x_emit_failures__mutmut_2 # type: ignore # mutmut generated
mutants_x_emit_failures__mutmut['x_emit_failures__mutmut_3'] = x_emit_failures__mutmut_3 # type: ignore # mutmut generated
mutants_x_emit_failures__mutmut['x_emit_failures__mutmut_4'] = x_emit_failures__mutmut_4 # type: ignore # mutmut generated
mutants_x_emit_failures__mutmut['x_emit_failures__mutmut_5'] = x_emit_failures__mutmut_5 # type: ignore # mutmut generated
mutants_x_emit_failures__mutmut['x_emit_failures__mutmut_6'] = x_emit_failures__mutmut_6 # type: ignore # mutmut generated
mutants_x_emit_failures__mutmut['x_emit_failures__mutmut_7'] = x_emit_failures__mutmut_7 # type: ignore # mutmut generated
mutants_x_emit_failures__mutmut['x_emit_failures__mutmut_8'] = x_emit_failures__mutmut_8 # type: ignore # mutmut generated
mutants_x_emit_failures__mutmut['x_emit_failures__mutmut_9'] = x_emit_failures__mutmut_9 # type: ignore # mutmut generated
mutants_x_emit_failures__mutmut['x_emit_failures__mutmut_10'] = x_emit_failures__mutmut_10 # type: ignore # mutmut generated
mutants_x_emit_pass__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_emit_pass__mutmut)
def emit_pass(message: str, stream: Any = None) -> None:
    """Emit the canonical PASS line for a check (defaults to ``sys.stdout``)."""
    out = stream if stream is not None else sys.stdout
    print(message, file=out)


def x_emit_pass__mutmut_orig(message: str, stream: Any = None) -> None:
    """Emit the canonical PASS line for a check (defaults to ``sys.stdout``)."""
    out = stream if stream is not None else sys.stdout
    print(message, file=out)


def x_emit_pass__mutmut_1(message: str, stream: Any = None) -> None:
    """Emit the canonical PASS line for a check (defaults to ``sys.stdout``)."""
    out = None
    print(message, file=out)


def x_emit_pass__mutmut_2(message: str, stream: Any = None) -> None:
    """Emit the canonical PASS line for a check (defaults to ``sys.stdout``)."""
    out = stream if stream is None else sys.stdout
    print(message, file=out)


def x_emit_pass__mutmut_3(message: str, stream: Any = None) -> None:
    """Emit the canonical PASS line for a check (defaults to ``sys.stdout``)."""
    out = stream if stream is not None else sys.stdout
    print(None, file=out)


def x_emit_pass__mutmut_4(message: str, stream: Any = None) -> None:
    """Emit the canonical PASS line for a check (defaults to ``sys.stdout``)."""
    out = stream if stream is not None else sys.stdout
    print(message, file=None)


def x_emit_pass__mutmut_5(message: str, stream: Any = None) -> None:
    """Emit the canonical PASS line for a check (defaults to ``sys.stdout``)."""
    out = stream if stream is not None else sys.stdout
    print(file=out)


def x_emit_pass__mutmut_6(message: str, stream: Any = None) -> None:
    """Emit the canonical PASS line for a check (defaults to ``sys.stdout``)."""
    out = stream if stream is not None else sys.stdout
    print(message, )

mutants_x_emit_pass__mutmut['_mutmut_orig'] = x_emit_pass__mutmut_orig # type: ignore # mutmut generated
mutants_x_emit_pass__mutmut['x_emit_pass__mutmut_1'] = x_emit_pass__mutmut_1 # type: ignore # mutmut generated
mutants_x_emit_pass__mutmut['x_emit_pass__mutmut_2'] = x_emit_pass__mutmut_2 # type: ignore # mutmut generated
mutants_x_emit_pass__mutmut['x_emit_pass__mutmut_3'] = x_emit_pass__mutmut_3 # type: ignore # mutmut generated
mutants_x_emit_pass__mutmut['x_emit_pass__mutmut_4'] = x_emit_pass__mutmut_4 # type: ignore # mutmut generated
mutants_x_emit_pass__mutmut['x_emit_pass__mutmut_5'] = x_emit_pass__mutmut_5 # type: ignore # mutmut generated
mutants_x_emit_pass__mutmut['x_emit_pass__mutmut_6'] = x_emit_pass__mutmut_6 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_load_yaml__mutmut)
def load_yaml(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_orig(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_1(
    path: Path, *, reject_duplicate_keys: bool = True, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_2(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "XXPyYAML missingXX"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_3(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "pyyaml missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_4(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PYYAML MISSING"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_5(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = None
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_6(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is not None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_7(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode(None)
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_8(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("XXutf-8XX")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_9(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("UTF-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_10(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_11(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) and {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_12(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(None) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_13(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = True) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_14(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(None)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_15(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = None
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_16(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = None
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_17(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(None, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_18(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=None)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_19(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_20(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, )
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_21(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = None
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_22(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key not in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_23(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        None,
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_24(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        None,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_25(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        None,
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_26(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        None,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_27(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_28(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_29(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_30(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_31(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "XXwhile constructing a mappingXX",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_32(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "WHILE CONSTRUCTING A MAPPING",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_33(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        None,
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_34(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        None,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_35(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        None,
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_36(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        None,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_37(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_38(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_39(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_40(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_41(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "XXwhile constructing a mappingXX",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_42(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "WHILE CONSTRUCTING A MAPPING",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_43(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = None
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_44(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(None, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_45(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=None)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_46(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_47(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, )
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_48(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = None
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_49(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            None,
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_50(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            None,
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_51(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            None,
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_52(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_53(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_54(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_55(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "XXStrictLoaderXX",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_56(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "strictloader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_57(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "STRICTLOADER",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_58(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"XXconstruct_mappingXX": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_59(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"CONSTRUCT_MAPPING": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_60(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = None
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_61(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(None)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def x_load_yaml__mutmut_62(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() and {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"

mutants_x_load_yaml__mutmut['_mutmut_orig'] = x_load_yaml__mutmut_orig # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_1'] = x_load_yaml__mutmut_1 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_2'] = x_load_yaml__mutmut_2 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_3'] = x_load_yaml__mutmut_3 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_4'] = x_load_yaml__mutmut_4 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_5'] = x_load_yaml__mutmut_5 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_6'] = x_load_yaml__mutmut_6 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_7'] = x_load_yaml__mutmut_7 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_8'] = x_load_yaml__mutmut_8 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_9'] = x_load_yaml__mutmut_9 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_10'] = x_load_yaml__mutmut_10 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_11'] = x_load_yaml__mutmut_11 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_12'] = x_load_yaml__mutmut_12 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_13'] = x_load_yaml__mutmut_13 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_14'] = x_load_yaml__mutmut_14 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_15'] = x_load_yaml__mutmut_15 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_16'] = x_load_yaml__mutmut_16 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_17'] = x_load_yaml__mutmut_17 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_18'] = x_load_yaml__mutmut_18 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_19'] = x_load_yaml__mutmut_19 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_20'] = x_load_yaml__mutmut_20 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_21'] = x_load_yaml__mutmut_21 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_22'] = x_load_yaml__mutmut_22 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_23'] = x_load_yaml__mutmut_23 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_24'] = x_load_yaml__mutmut_24 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_25'] = x_load_yaml__mutmut_25 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_26'] = x_load_yaml__mutmut_26 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_27'] = x_load_yaml__mutmut_27 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_28'] = x_load_yaml__mutmut_28 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_29'] = x_load_yaml__mutmut_29 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_30'] = x_load_yaml__mutmut_30 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_31'] = x_load_yaml__mutmut_31 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_32'] = x_load_yaml__mutmut_32 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_33'] = x_load_yaml__mutmut_33 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_34'] = x_load_yaml__mutmut_34 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_35'] = x_load_yaml__mutmut_35 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_36'] = x_load_yaml__mutmut_36 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_37'] = x_load_yaml__mutmut_37 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_38'] = x_load_yaml__mutmut_38 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_39'] = x_load_yaml__mutmut_39 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_40'] = x_load_yaml__mutmut_40 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_41'] = x_load_yaml__mutmut_41 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_42'] = x_load_yaml__mutmut_42 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_43'] = x_load_yaml__mutmut_43 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_44'] = x_load_yaml__mutmut_44 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_45'] = x_load_yaml__mutmut_45 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_46'] = x_load_yaml__mutmut_46 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_47'] = x_load_yaml__mutmut_47 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_48'] = x_load_yaml__mutmut_48 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_49'] = x_load_yaml__mutmut_49 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_50'] = x_load_yaml__mutmut_50 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_51'] = x_load_yaml__mutmut_51 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_52'] = x_load_yaml__mutmut_52 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_53'] = x_load_yaml__mutmut_53 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_54'] = x_load_yaml__mutmut_54 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_55'] = x_load_yaml__mutmut_55 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_56'] = x_load_yaml__mutmut_56 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_57'] = x_load_yaml__mutmut_57 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_58'] = x_load_yaml__mutmut_58 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_59'] = x_load_yaml__mutmut_59 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_60'] = x_load_yaml__mutmut_60 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_61'] = x_load_yaml__mutmut_61 # type: ignore # mutmut generated
mutants_x_load_yaml__mutmut['x_load_yaml__mutmut_62'] = x_load_yaml__mutmut_62 # type: ignore # mutmut generated
mutants_x_missing_keys__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_missing_keys__mutmut)
def missing_keys(parsed: dict[str, Any], required: tuple[str, ...]) -> list[str]:
    """Return the subset of ``required`` keys that are absent in ``parsed``."""
    return [k for k in required if k not in parsed]


def x_missing_keys__mutmut_orig(parsed: dict[str, Any], required: tuple[str, ...]) -> list[str]:
    """Return the subset of ``required`` keys that are absent in ``parsed``."""
    return [k for k in required if k not in parsed]


def x_missing_keys__mutmut_1(parsed: dict[str, Any], required: tuple[str, ...]) -> list[str]:
    """Return the subset of ``required`` keys that are absent in ``parsed``."""
    return [k for k in required if k in parsed]

mutants_x_missing_keys__mutmut['_mutmut_orig'] = x_missing_keys__mutmut_orig # type: ignore # mutmut generated
mutants_x_missing_keys__mutmut['x_missing_keys__mutmut_1'] = x_missing_keys__mutmut_1 # type: ignore # mutmut generated


__all__ = [
    "REPO_ROOT",
    "actionable",
    "emit_failures",
    "emit_pass",
    "gate",
    "gate_keys",
    "load_yaml",
    "main_entry",
    "missing_keys",
    "python_files",
    "remediation",
    "repo_relative",
]
