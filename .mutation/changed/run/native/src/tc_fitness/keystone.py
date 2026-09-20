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


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x_staged_added_files__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_staged_added_files__mutmut)
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


def x_staged_added_files__mutmut_orig(repo_root: Path) -> list[str]:
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


def x_staged_added_files__mutmut_1(repo_root: Path) -> list[str]:
    """Repo-relative paths ADDED in the current staged diff (pre-commit mode)."""
    result = None
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_staged_added_files__mutmut_2(repo_root: Path) -> list[str]:
    """Repo-relative paths ADDED in the current staged diff (pre-commit mode)."""
    result = subprocess.run(
        None,
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_staged_added_files__mutmut_3(repo_root: Path) -> list[str]:
    """Repo-relative paths ADDED in the current staged diff (pre-commit mode)."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=A"],
        cwd=None,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_staged_added_files__mutmut_4(repo_root: Path) -> list[str]:
    """Repo-relative paths ADDED in the current staged diff (pre-commit mode)."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=A"],
        cwd=repo_root,
        capture_output=None,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_staged_added_files__mutmut_5(repo_root: Path) -> list[str]:
    """Repo-relative paths ADDED in the current staged diff (pre-commit mode)."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=A"],
        cwd=repo_root,
        capture_output=True,
        text=None,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_staged_added_files__mutmut_6(repo_root: Path) -> list[str]:
    """Repo-relative paths ADDED in the current staged diff (pre-commit mode)."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=A"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=None,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_staged_added_files__mutmut_7(repo_root: Path) -> list[str]:
    """Repo-relative paths ADDED in the current staged diff (pre-commit mode)."""
    result = subprocess.run(
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_staged_added_files__mutmut_8(repo_root: Path) -> list[str]:
    """Repo-relative paths ADDED in the current staged diff (pre-commit mode)."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=A"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_staged_added_files__mutmut_9(repo_root: Path) -> list[str]:
    """Repo-relative paths ADDED in the current staged diff (pre-commit mode)."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=A"],
        cwd=repo_root,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_staged_added_files__mutmut_10(repo_root: Path) -> list[str]:
    """Repo-relative paths ADDED in the current staged diff (pre-commit mode)."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=A"],
        cwd=repo_root,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_staged_added_files__mutmut_11(repo_root: Path) -> list[str]:
    """Repo-relative paths ADDED in the current staged diff (pre-commit mode)."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=A"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_staged_added_files__mutmut_12(repo_root: Path) -> list[str]:
    """Repo-relative paths ADDED in the current staged diff (pre-commit mode)."""
    result = subprocess.run(
        ["XXgitXX", "diff", "--cached", "--name-only", "--diff-filter=A"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_staged_added_files__mutmut_13(repo_root: Path) -> list[str]:
    """Repo-relative paths ADDED in the current staged diff (pre-commit mode)."""
    result = subprocess.run(
        ["GIT", "diff", "--cached", "--name-only", "--diff-filter=A"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_staged_added_files__mutmut_14(repo_root: Path) -> list[str]:
    """Repo-relative paths ADDED in the current staged diff (pre-commit mode)."""
    result = subprocess.run(
        ["git", "XXdiffXX", "--cached", "--name-only", "--diff-filter=A"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_staged_added_files__mutmut_15(repo_root: Path) -> list[str]:
    """Repo-relative paths ADDED in the current staged diff (pre-commit mode)."""
    result = subprocess.run(
        ["git", "DIFF", "--cached", "--name-only", "--diff-filter=A"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_staged_added_files__mutmut_16(repo_root: Path) -> list[str]:
    """Repo-relative paths ADDED in the current staged diff (pre-commit mode)."""
    result = subprocess.run(
        ["git", "diff", "XX--cachedXX", "--name-only", "--diff-filter=A"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_staged_added_files__mutmut_17(repo_root: Path) -> list[str]:
    """Repo-relative paths ADDED in the current staged diff (pre-commit mode)."""
    result = subprocess.run(
        ["git", "diff", "--CACHED", "--name-only", "--diff-filter=A"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_staged_added_files__mutmut_18(repo_root: Path) -> list[str]:
    """Repo-relative paths ADDED in the current staged diff (pre-commit mode)."""
    result = subprocess.run(
        ["git", "diff", "--cached", "XX--name-onlyXX", "--diff-filter=A"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_staged_added_files__mutmut_19(repo_root: Path) -> list[str]:
    """Repo-relative paths ADDED in the current staged diff (pre-commit mode)."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--NAME-ONLY", "--diff-filter=A"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_staged_added_files__mutmut_20(repo_root: Path) -> list[str]:
    """Repo-relative paths ADDED in the current staged diff (pre-commit mode)."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "XX--diff-filter=AXX"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_staged_added_files__mutmut_21(repo_root: Path) -> list[str]:
    """Repo-relative paths ADDED in the current staged diff (pre-commit mode)."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=a"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_staged_added_files__mutmut_22(repo_root: Path) -> list[str]:
    """Repo-relative paths ADDED in the current staged diff (pre-commit mode)."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--DIFF-FILTER=A"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_staged_added_files__mutmut_23(repo_root: Path) -> list[str]:
    """Repo-relative paths ADDED in the current staged diff (pre-commit mode)."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=A"],
        cwd=repo_root,
        capture_output=False,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_staged_added_files__mutmut_24(repo_root: Path) -> list[str]:
    """Repo-relative paths ADDED in the current staged diff (pre-commit mode)."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=A"],
        cwd=repo_root,
        capture_output=True,
        text=False,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_staged_added_files__mutmut_25(repo_root: Path) -> list[str]:
    """Repo-relative paths ADDED in the current staged diff (pre-commit mode)."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=A"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_staged_added_files__mutmut_26(repo_root: Path) -> list[str]:
    """Repo-relative paths ADDED in the current staged diff (pre-commit mode)."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=A"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_staged_added_files__mutmut_27(repo_root: Path) -> list[str]:
    """Repo-relative paths ADDED in the current staged diff (pre-commit mode)."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=A"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 1:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]

mutants_x_staged_added_files__mutmut['_mutmut_orig'] = x_staged_added_files__mutmut_orig # type: ignore # mutmut generated
mutants_x_staged_added_files__mutmut['x_staged_added_files__mutmut_1'] = x_staged_added_files__mutmut_1 # type: ignore # mutmut generated
mutants_x_staged_added_files__mutmut['x_staged_added_files__mutmut_2'] = x_staged_added_files__mutmut_2 # type: ignore # mutmut generated
mutants_x_staged_added_files__mutmut['x_staged_added_files__mutmut_3'] = x_staged_added_files__mutmut_3 # type: ignore # mutmut generated
mutants_x_staged_added_files__mutmut['x_staged_added_files__mutmut_4'] = x_staged_added_files__mutmut_4 # type: ignore # mutmut generated
mutants_x_staged_added_files__mutmut['x_staged_added_files__mutmut_5'] = x_staged_added_files__mutmut_5 # type: ignore # mutmut generated
mutants_x_staged_added_files__mutmut['x_staged_added_files__mutmut_6'] = x_staged_added_files__mutmut_6 # type: ignore # mutmut generated
mutants_x_staged_added_files__mutmut['x_staged_added_files__mutmut_7'] = x_staged_added_files__mutmut_7 # type: ignore # mutmut generated
mutants_x_staged_added_files__mutmut['x_staged_added_files__mutmut_8'] = x_staged_added_files__mutmut_8 # type: ignore # mutmut generated
mutants_x_staged_added_files__mutmut['x_staged_added_files__mutmut_9'] = x_staged_added_files__mutmut_9 # type: ignore # mutmut generated
mutants_x_staged_added_files__mutmut['x_staged_added_files__mutmut_10'] = x_staged_added_files__mutmut_10 # type: ignore # mutmut generated
mutants_x_staged_added_files__mutmut['x_staged_added_files__mutmut_11'] = x_staged_added_files__mutmut_11 # type: ignore # mutmut generated
mutants_x_staged_added_files__mutmut['x_staged_added_files__mutmut_12'] = x_staged_added_files__mutmut_12 # type: ignore # mutmut generated
mutants_x_staged_added_files__mutmut['x_staged_added_files__mutmut_13'] = x_staged_added_files__mutmut_13 # type: ignore # mutmut generated
mutants_x_staged_added_files__mutmut['x_staged_added_files__mutmut_14'] = x_staged_added_files__mutmut_14 # type: ignore # mutmut generated
mutants_x_staged_added_files__mutmut['x_staged_added_files__mutmut_15'] = x_staged_added_files__mutmut_15 # type: ignore # mutmut generated
mutants_x_staged_added_files__mutmut['x_staged_added_files__mutmut_16'] = x_staged_added_files__mutmut_16 # type: ignore # mutmut generated
mutants_x_staged_added_files__mutmut['x_staged_added_files__mutmut_17'] = x_staged_added_files__mutmut_17 # type: ignore # mutmut generated
mutants_x_staged_added_files__mutmut['x_staged_added_files__mutmut_18'] = x_staged_added_files__mutmut_18 # type: ignore # mutmut generated
mutants_x_staged_added_files__mutmut['x_staged_added_files__mutmut_19'] = x_staged_added_files__mutmut_19 # type: ignore # mutmut generated
mutants_x_staged_added_files__mutmut['x_staged_added_files__mutmut_20'] = x_staged_added_files__mutmut_20 # type: ignore # mutmut generated
mutants_x_staged_added_files__mutmut['x_staged_added_files__mutmut_21'] = x_staged_added_files__mutmut_21 # type: ignore # mutmut generated
mutants_x_staged_added_files__mutmut['x_staged_added_files__mutmut_22'] = x_staged_added_files__mutmut_22 # type: ignore # mutmut generated
mutants_x_staged_added_files__mutmut['x_staged_added_files__mutmut_23'] = x_staged_added_files__mutmut_23 # type: ignore # mutmut generated
mutants_x_staged_added_files__mutmut['x_staged_added_files__mutmut_24'] = x_staged_added_files__mutmut_24 # type: ignore # mutmut generated
mutants_x_staged_added_files__mutmut['x_staged_added_files__mutmut_25'] = x_staged_added_files__mutmut_25 # type: ignore # mutmut generated
mutants_x_staged_added_files__mutmut['x_staged_added_files__mutmut_26'] = x_staged_added_files__mutmut_26 # type: ignore # mutmut generated
mutants_x_staged_added_files__mutmut['x_staged_added_files__mutmut_27'] = x_staged_added_files__mutmut_27 # type: ignore # mutmut generated
mutants_x_added_since_tag__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_added_since_tag__mutmut)
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


def x_added_since_tag__mutmut_orig(repo_root: Path, tag: str) -> list[str]:
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


def x_added_since_tag__mutmut_1(repo_root: Path, tag: str) -> list[str]:
    """Repo-relative paths ADDED between ``tag`` and HEAD (CI full-PR mode)."""
    result = None
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_added_since_tag__mutmut_2(repo_root: Path, tag: str) -> list[str]:
    """Repo-relative paths ADDED between ``tag`` and HEAD (CI full-PR mode)."""
    result = subprocess.run(
        None,
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_added_since_tag__mutmut_3(repo_root: Path, tag: str) -> list[str]:
    """Repo-relative paths ADDED between ``tag`` and HEAD (CI full-PR mode)."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=A", f"{tag}..HEAD"],
        cwd=None,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_added_since_tag__mutmut_4(repo_root: Path, tag: str) -> list[str]:
    """Repo-relative paths ADDED between ``tag`` and HEAD (CI full-PR mode)."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=A", f"{tag}..HEAD"],
        cwd=repo_root,
        capture_output=None,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_added_since_tag__mutmut_5(repo_root: Path, tag: str) -> list[str]:
    """Repo-relative paths ADDED between ``tag`` and HEAD (CI full-PR mode)."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=A", f"{tag}..HEAD"],
        cwd=repo_root,
        capture_output=True,
        text=None,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_added_since_tag__mutmut_6(repo_root: Path, tag: str) -> list[str]:
    """Repo-relative paths ADDED between ``tag`` and HEAD (CI full-PR mode)."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=A", f"{tag}..HEAD"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=None,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_added_since_tag__mutmut_7(repo_root: Path, tag: str) -> list[str]:
    """Repo-relative paths ADDED between ``tag`` and HEAD (CI full-PR mode)."""
    result = subprocess.run(
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_added_since_tag__mutmut_8(repo_root: Path, tag: str) -> list[str]:
    """Repo-relative paths ADDED between ``tag`` and HEAD (CI full-PR mode)."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=A", f"{tag}..HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_added_since_tag__mutmut_9(repo_root: Path, tag: str) -> list[str]:
    """Repo-relative paths ADDED between ``tag`` and HEAD (CI full-PR mode)."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=A", f"{tag}..HEAD"],
        cwd=repo_root,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_added_since_tag__mutmut_10(repo_root: Path, tag: str) -> list[str]:
    """Repo-relative paths ADDED between ``tag`` and HEAD (CI full-PR mode)."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=A", f"{tag}..HEAD"],
        cwd=repo_root,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_added_since_tag__mutmut_11(repo_root: Path, tag: str) -> list[str]:
    """Repo-relative paths ADDED between ``tag`` and HEAD (CI full-PR mode)."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=A", f"{tag}..HEAD"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_added_since_tag__mutmut_12(repo_root: Path, tag: str) -> list[str]:
    """Repo-relative paths ADDED between ``tag`` and HEAD (CI full-PR mode)."""
    result = subprocess.run(
        ["XXgitXX", "diff", "--name-only", "--diff-filter=A", f"{tag}..HEAD"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_added_since_tag__mutmut_13(repo_root: Path, tag: str) -> list[str]:
    """Repo-relative paths ADDED between ``tag`` and HEAD (CI full-PR mode)."""
    result = subprocess.run(
        ["GIT", "diff", "--name-only", "--diff-filter=A", f"{tag}..HEAD"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_added_since_tag__mutmut_14(repo_root: Path, tag: str) -> list[str]:
    """Repo-relative paths ADDED between ``tag`` and HEAD (CI full-PR mode)."""
    result = subprocess.run(
        ["git", "XXdiffXX", "--name-only", "--diff-filter=A", f"{tag}..HEAD"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_added_since_tag__mutmut_15(repo_root: Path, tag: str) -> list[str]:
    """Repo-relative paths ADDED between ``tag`` and HEAD (CI full-PR mode)."""
    result = subprocess.run(
        ["git", "DIFF", "--name-only", "--diff-filter=A", f"{tag}..HEAD"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_added_since_tag__mutmut_16(repo_root: Path, tag: str) -> list[str]:
    """Repo-relative paths ADDED between ``tag`` and HEAD (CI full-PR mode)."""
    result = subprocess.run(
        ["git", "diff", "XX--name-onlyXX", "--diff-filter=A", f"{tag}..HEAD"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_added_since_tag__mutmut_17(repo_root: Path, tag: str) -> list[str]:
    """Repo-relative paths ADDED between ``tag`` and HEAD (CI full-PR mode)."""
    result = subprocess.run(
        ["git", "diff", "--NAME-ONLY", "--diff-filter=A", f"{tag}..HEAD"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_added_since_tag__mutmut_18(repo_root: Path, tag: str) -> list[str]:
    """Repo-relative paths ADDED between ``tag`` and HEAD (CI full-PR mode)."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "XX--diff-filter=AXX", f"{tag}..HEAD"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_added_since_tag__mutmut_19(repo_root: Path, tag: str) -> list[str]:
    """Repo-relative paths ADDED between ``tag`` and HEAD (CI full-PR mode)."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=a", f"{tag}..HEAD"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_added_since_tag__mutmut_20(repo_root: Path, tag: str) -> list[str]:
    """Repo-relative paths ADDED between ``tag`` and HEAD (CI full-PR mode)."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "--DIFF-FILTER=A", f"{tag}..HEAD"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_added_since_tag__mutmut_21(repo_root: Path, tag: str) -> list[str]:
    """Repo-relative paths ADDED between ``tag`` and HEAD (CI full-PR mode)."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=A", f"{tag}..HEAD"],
        cwd=repo_root,
        capture_output=False,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_added_since_tag__mutmut_22(repo_root: Path, tag: str) -> list[str]:
    """Repo-relative paths ADDED between ``tag`` and HEAD (CI full-PR mode)."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=A", f"{tag}..HEAD"],
        cwd=repo_root,
        capture_output=True,
        text=False,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_added_since_tag__mutmut_23(repo_root: Path, tag: str) -> list[str]:
    """Repo-relative paths ADDED between ``tag`` and HEAD (CI full-PR mode)."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=A", f"{tag}..HEAD"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_added_since_tag__mutmut_24(repo_root: Path, tag: str) -> list[str]:
    """Repo-relative paths ADDED between ``tag`` and HEAD (CI full-PR mode)."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=A", f"{tag}..HEAD"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def x_added_since_tag__mutmut_25(repo_root: Path, tag: str) -> list[str]:
    """Repo-relative paths ADDED between ``tag`` and HEAD (CI full-PR mode)."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=A", f"{tag}..HEAD"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 1:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]

mutants_x_added_since_tag__mutmut['_mutmut_orig'] = x_added_since_tag__mutmut_orig # type: ignore # mutmut generated
mutants_x_added_since_tag__mutmut['x_added_since_tag__mutmut_1'] = x_added_since_tag__mutmut_1 # type: ignore # mutmut generated
mutants_x_added_since_tag__mutmut['x_added_since_tag__mutmut_2'] = x_added_since_tag__mutmut_2 # type: ignore # mutmut generated
mutants_x_added_since_tag__mutmut['x_added_since_tag__mutmut_3'] = x_added_since_tag__mutmut_3 # type: ignore # mutmut generated
mutants_x_added_since_tag__mutmut['x_added_since_tag__mutmut_4'] = x_added_since_tag__mutmut_4 # type: ignore # mutmut generated
mutants_x_added_since_tag__mutmut['x_added_since_tag__mutmut_5'] = x_added_since_tag__mutmut_5 # type: ignore # mutmut generated
mutants_x_added_since_tag__mutmut['x_added_since_tag__mutmut_6'] = x_added_since_tag__mutmut_6 # type: ignore # mutmut generated
mutants_x_added_since_tag__mutmut['x_added_since_tag__mutmut_7'] = x_added_since_tag__mutmut_7 # type: ignore # mutmut generated
mutants_x_added_since_tag__mutmut['x_added_since_tag__mutmut_8'] = x_added_since_tag__mutmut_8 # type: ignore # mutmut generated
mutants_x_added_since_tag__mutmut['x_added_since_tag__mutmut_9'] = x_added_since_tag__mutmut_9 # type: ignore # mutmut generated
mutants_x_added_since_tag__mutmut['x_added_since_tag__mutmut_10'] = x_added_since_tag__mutmut_10 # type: ignore # mutmut generated
mutants_x_added_since_tag__mutmut['x_added_since_tag__mutmut_11'] = x_added_since_tag__mutmut_11 # type: ignore # mutmut generated
mutants_x_added_since_tag__mutmut['x_added_since_tag__mutmut_12'] = x_added_since_tag__mutmut_12 # type: ignore # mutmut generated
mutants_x_added_since_tag__mutmut['x_added_since_tag__mutmut_13'] = x_added_since_tag__mutmut_13 # type: ignore # mutmut generated
mutants_x_added_since_tag__mutmut['x_added_since_tag__mutmut_14'] = x_added_since_tag__mutmut_14 # type: ignore # mutmut generated
mutants_x_added_since_tag__mutmut['x_added_since_tag__mutmut_15'] = x_added_since_tag__mutmut_15 # type: ignore # mutmut generated
mutants_x_added_since_tag__mutmut['x_added_since_tag__mutmut_16'] = x_added_since_tag__mutmut_16 # type: ignore # mutmut generated
mutants_x_added_since_tag__mutmut['x_added_since_tag__mutmut_17'] = x_added_since_tag__mutmut_17 # type: ignore # mutmut generated
mutants_x_added_since_tag__mutmut['x_added_since_tag__mutmut_18'] = x_added_since_tag__mutmut_18 # type: ignore # mutmut generated
mutants_x_added_since_tag__mutmut['x_added_since_tag__mutmut_19'] = x_added_since_tag__mutmut_19 # type: ignore # mutmut generated
mutants_x_added_since_tag__mutmut['x_added_since_tag__mutmut_20'] = x_added_since_tag__mutmut_20 # type: ignore # mutmut generated
mutants_x_added_since_tag__mutmut['x_added_since_tag__mutmut_21'] = x_added_since_tag__mutmut_21 # type: ignore # mutmut generated
mutants_x_added_since_tag__mutmut['x_added_since_tag__mutmut_22'] = x_added_since_tag__mutmut_22 # type: ignore # mutmut generated
mutants_x_added_since_tag__mutmut['x_added_since_tag__mutmut_23'] = x_added_since_tag__mutmut_23 # type: ignore # mutmut generated
mutants_x_added_since_tag__mutmut['x_added_since_tag__mutmut_24'] = x_added_since_tag__mutmut_24 # type: ignore # mutmut generated
mutants_x_added_since_tag__mutmut['x_added_since_tag__mutmut_25'] = x_added_since_tag__mutmut_25 # type: ignore # mutmut generated
mutants_x_resolve_previous_tag__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_resolve_previous_tag__mutmut)
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


def x_resolve_previous_tag__mutmut_orig(
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


def x_resolve_previous_tag__mutmut_1(
    repo_root: Path,
    *,
    match_glob: str = "XXv[0-9]*.[0-9]*.[0-9]*XX",
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


def x_resolve_previous_tag__mutmut_2(
    repo_root: Path,
    *,
    match_glob: str = "V[0-9]*.[0-9]*.[0-9]*",
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


def x_resolve_previous_tag__mutmut_3(
    repo_root: Path,
    *,
    match_glob: str = "v[0-9]*.[0-9]*.[0-9]*",
) -> str | None:
    """Most recent release tag strictly older than HEAD, or ``None``.

    ``match_glob`` is CONFIG — a repo using ``v2026.5.18`` and a repo using
    ``v0.6.0`` both work by passing their own glob. ``None`` means "no prior
    tag" (first release → the shrink check is a clean skip).
    """
    result = None
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def x_resolve_previous_tag__mutmut_4(
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
        None,
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def x_resolve_previous_tag__mutmut_5(
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
        cwd=None,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def x_resolve_previous_tag__mutmut_6(
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
        capture_output=None,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def x_resolve_previous_tag__mutmut_7(
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
        text=None,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def x_resolve_previous_tag__mutmut_8(
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
        check=None,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def x_resolve_previous_tag__mutmut_9(
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
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def x_resolve_previous_tag__mutmut_10(
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
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def x_resolve_previous_tag__mutmut_11(
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
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def x_resolve_previous_tag__mutmut_12(
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
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def x_resolve_previous_tag__mutmut_13(
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
        )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def x_resolve_previous_tag__mutmut_14(
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
        ["XXgitXX", "describe", "--tags", "--abbrev=0", "--match", match_glob, "HEAD^"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def x_resolve_previous_tag__mutmut_15(
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
        ["GIT", "describe", "--tags", "--abbrev=0", "--match", match_glob, "HEAD^"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def x_resolve_previous_tag__mutmut_16(
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
        ["git", "XXdescribeXX", "--tags", "--abbrev=0", "--match", match_glob, "HEAD^"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def x_resolve_previous_tag__mutmut_17(
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
        ["git", "DESCRIBE", "--tags", "--abbrev=0", "--match", match_glob, "HEAD^"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def x_resolve_previous_tag__mutmut_18(
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
        ["git", "describe", "XX--tagsXX", "--abbrev=0", "--match", match_glob, "HEAD^"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def x_resolve_previous_tag__mutmut_19(
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
        ["git", "describe", "--TAGS", "--abbrev=0", "--match", match_glob, "HEAD^"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def x_resolve_previous_tag__mutmut_20(
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
        ["git", "describe", "--tags", "XX--abbrev=0XX", "--match", match_glob, "HEAD^"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def x_resolve_previous_tag__mutmut_21(
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
        ["git", "describe", "--tags", "--ABBREV=0", "--match", match_glob, "HEAD^"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def x_resolve_previous_tag__mutmut_22(
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
        ["git", "describe", "--tags", "--abbrev=0", "XX--matchXX", match_glob, "HEAD^"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def x_resolve_previous_tag__mutmut_23(
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
        ["git", "describe", "--tags", "--abbrev=0", "--MATCH", match_glob, "HEAD^"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def x_resolve_previous_tag__mutmut_24(
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
        ["git", "describe", "--tags", "--abbrev=0", "--match", match_glob, "XXHEAD^XX"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def x_resolve_previous_tag__mutmut_25(
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
        ["git", "describe", "--tags", "--abbrev=0", "--match", match_glob, "head^"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def x_resolve_previous_tag__mutmut_26(
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
        capture_output=False,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def x_resolve_previous_tag__mutmut_27(
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
        text=False,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def x_resolve_previous_tag__mutmut_28(
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
        check=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def x_resolve_previous_tag__mutmut_29(
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
    if result.returncode == 0:
        return None
    return result.stdout.strip() or None


def x_resolve_previous_tag__mutmut_30(
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
    if result.returncode != 1:
        return None
    return result.stdout.strip() or None


def x_resolve_previous_tag__mutmut_31(
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
    return result.stdout.strip() and None

mutants_x_resolve_previous_tag__mutmut['_mutmut_orig'] = x_resolve_previous_tag__mutmut_orig # type: ignore # mutmut generated
mutants_x_resolve_previous_tag__mutmut['x_resolve_previous_tag__mutmut_1'] = x_resolve_previous_tag__mutmut_1 # type: ignore # mutmut generated
mutants_x_resolve_previous_tag__mutmut['x_resolve_previous_tag__mutmut_2'] = x_resolve_previous_tag__mutmut_2 # type: ignore # mutmut generated
mutants_x_resolve_previous_tag__mutmut['x_resolve_previous_tag__mutmut_3'] = x_resolve_previous_tag__mutmut_3 # type: ignore # mutmut generated
mutants_x_resolve_previous_tag__mutmut['x_resolve_previous_tag__mutmut_4'] = x_resolve_previous_tag__mutmut_4 # type: ignore # mutmut generated
mutants_x_resolve_previous_tag__mutmut['x_resolve_previous_tag__mutmut_5'] = x_resolve_previous_tag__mutmut_5 # type: ignore # mutmut generated
mutants_x_resolve_previous_tag__mutmut['x_resolve_previous_tag__mutmut_6'] = x_resolve_previous_tag__mutmut_6 # type: ignore # mutmut generated
mutants_x_resolve_previous_tag__mutmut['x_resolve_previous_tag__mutmut_7'] = x_resolve_previous_tag__mutmut_7 # type: ignore # mutmut generated
mutants_x_resolve_previous_tag__mutmut['x_resolve_previous_tag__mutmut_8'] = x_resolve_previous_tag__mutmut_8 # type: ignore # mutmut generated
mutants_x_resolve_previous_tag__mutmut['x_resolve_previous_tag__mutmut_9'] = x_resolve_previous_tag__mutmut_9 # type: ignore # mutmut generated
mutants_x_resolve_previous_tag__mutmut['x_resolve_previous_tag__mutmut_10'] = x_resolve_previous_tag__mutmut_10 # type: ignore # mutmut generated
mutants_x_resolve_previous_tag__mutmut['x_resolve_previous_tag__mutmut_11'] = x_resolve_previous_tag__mutmut_11 # type: ignore # mutmut generated
mutants_x_resolve_previous_tag__mutmut['x_resolve_previous_tag__mutmut_12'] = x_resolve_previous_tag__mutmut_12 # type: ignore # mutmut generated
mutants_x_resolve_previous_tag__mutmut['x_resolve_previous_tag__mutmut_13'] = x_resolve_previous_tag__mutmut_13 # type: ignore # mutmut generated
mutants_x_resolve_previous_tag__mutmut['x_resolve_previous_tag__mutmut_14'] = x_resolve_previous_tag__mutmut_14 # type: ignore # mutmut generated
mutants_x_resolve_previous_tag__mutmut['x_resolve_previous_tag__mutmut_15'] = x_resolve_previous_tag__mutmut_15 # type: ignore # mutmut generated
mutants_x_resolve_previous_tag__mutmut['x_resolve_previous_tag__mutmut_16'] = x_resolve_previous_tag__mutmut_16 # type: ignore # mutmut generated
mutants_x_resolve_previous_tag__mutmut['x_resolve_previous_tag__mutmut_17'] = x_resolve_previous_tag__mutmut_17 # type: ignore # mutmut generated
mutants_x_resolve_previous_tag__mutmut['x_resolve_previous_tag__mutmut_18'] = x_resolve_previous_tag__mutmut_18 # type: ignore # mutmut generated
mutants_x_resolve_previous_tag__mutmut['x_resolve_previous_tag__mutmut_19'] = x_resolve_previous_tag__mutmut_19 # type: ignore # mutmut generated
mutants_x_resolve_previous_tag__mutmut['x_resolve_previous_tag__mutmut_20'] = x_resolve_previous_tag__mutmut_20 # type: ignore # mutmut generated
mutants_x_resolve_previous_tag__mutmut['x_resolve_previous_tag__mutmut_21'] = x_resolve_previous_tag__mutmut_21 # type: ignore # mutmut generated
mutants_x_resolve_previous_tag__mutmut['x_resolve_previous_tag__mutmut_22'] = x_resolve_previous_tag__mutmut_22 # type: ignore # mutmut generated
mutants_x_resolve_previous_tag__mutmut['x_resolve_previous_tag__mutmut_23'] = x_resolve_previous_tag__mutmut_23 # type: ignore # mutmut generated
mutants_x_resolve_previous_tag__mutmut['x_resolve_previous_tag__mutmut_24'] = x_resolve_previous_tag__mutmut_24 # type: ignore # mutmut generated
mutants_x_resolve_previous_tag__mutmut['x_resolve_previous_tag__mutmut_25'] = x_resolve_previous_tag__mutmut_25 # type: ignore # mutmut generated
mutants_x_resolve_previous_tag__mutmut['x_resolve_previous_tag__mutmut_26'] = x_resolve_previous_tag__mutmut_26 # type: ignore # mutmut generated
mutants_x_resolve_previous_tag__mutmut['x_resolve_previous_tag__mutmut_27'] = x_resolve_previous_tag__mutmut_27 # type: ignore # mutmut generated
mutants_x_resolve_previous_tag__mutmut['x_resolve_previous_tag__mutmut_28'] = x_resolve_previous_tag__mutmut_28 # type: ignore # mutmut generated
mutants_x_resolve_previous_tag__mutmut['x_resolve_previous_tag__mutmut_29'] = x_resolve_previous_tag__mutmut_29 # type: ignore # mutmut generated
mutants_x_resolve_previous_tag__mutmut['x_resolve_previous_tag__mutmut_30'] = x_resolve_previous_tag__mutmut_30 # type: ignore # mutmut generated
mutants_x_resolve_previous_tag__mutmut['x_resolve_previous_tag__mutmut_31'] = x_resolve_previous_tag__mutmut_31 # type: ignore # mutmut generated


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
mutants_x_reconcile_catalogue__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_reconcile_catalogue__mutmut)
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


def x_reconcile_catalogue__mutmut_orig(
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


def x_reconcile_catalogue__mutmut_1(
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
    cataloged = None
    available = set(available_check_ids)
    orphans = sorted(available - cataloged)
    dangling = sorted((cid, cid) for cid in (cataloged - available))
    return CatalogueConsistencyReport(
        orphan_checks=orphans,
        dangling_entries=[(eid, cid) for eid, cid in dangling],
    )


def x_reconcile_catalogue__mutmut_2(
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
    cataloged = set(None)
    available = set(available_check_ids)
    orphans = sorted(available - cataloged)
    dangling = sorted((cid, cid) for cid in (cataloged - available))
    return CatalogueConsistencyReport(
        orphan_checks=orphans,
        dangling_entries=[(eid, cid) for eid, cid in dangling],
    )


def x_reconcile_catalogue__mutmut_3(
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
    available = None
    orphans = sorted(available - cataloged)
    dangling = sorted((cid, cid) for cid in (cataloged - available))
    return CatalogueConsistencyReport(
        orphan_checks=orphans,
        dangling_entries=[(eid, cid) for eid, cid in dangling],
    )


def x_reconcile_catalogue__mutmut_4(
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
    available = set(None)
    orphans = sorted(available - cataloged)
    dangling = sorted((cid, cid) for cid in (cataloged - available))
    return CatalogueConsistencyReport(
        orphan_checks=orphans,
        dangling_entries=[(eid, cid) for eid, cid in dangling],
    )


def x_reconcile_catalogue__mutmut_5(
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
    orphans = None
    dangling = sorted((cid, cid) for cid in (cataloged - available))
    return CatalogueConsistencyReport(
        orphan_checks=orphans,
        dangling_entries=[(eid, cid) for eid, cid in dangling],
    )


def x_reconcile_catalogue__mutmut_6(
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
    orphans = sorted(None)
    dangling = sorted((cid, cid) for cid in (cataloged - available))
    return CatalogueConsistencyReport(
        orphan_checks=orphans,
        dangling_entries=[(eid, cid) for eid, cid in dangling],
    )


def x_reconcile_catalogue__mutmut_7(
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
    orphans = sorted(available + cataloged)
    dangling = sorted((cid, cid) for cid in (cataloged - available))
    return CatalogueConsistencyReport(
        orphan_checks=orphans,
        dangling_entries=[(eid, cid) for eid, cid in dangling],
    )


def x_reconcile_catalogue__mutmut_8(
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
    dangling = None
    return CatalogueConsistencyReport(
        orphan_checks=orphans,
        dangling_entries=[(eid, cid) for eid, cid in dangling],
    )


def x_reconcile_catalogue__mutmut_9(
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
    dangling = sorted(None)
    return CatalogueConsistencyReport(
        orphan_checks=orphans,
        dangling_entries=[(eid, cid) for eid, cid in dangling],
    )


def x_reconcile_catalogue__mutmut_10(
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
    dangling = sorted((cid, cid) for cid in (cataloged + available))
    return CatalogueConsistencyReport(
        orphan_checks=orphans,
        dangling_entries=[(eid, cid) for eid, cid in dangling],
    )


def x_reconcile_catalogue__mutmut_11(
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
        orphan_checks=None,
        dangling_entries=[(eid, cid) for eid, cid in dangling],
    )


def x_reconcile_catalogue__mutmut_12(
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
        dangling_entries=None,
    )


def x_reconcile_catalogue__mutmut_13(
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
        dangling_entries=[(eid, cid) for eid, cid in dangling],
    )


def x_reconcile_catalogue__mutmut_14(
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
        )

mutants_x_reconcile_catalogue__mutmut['_mutmut_orig'] = x_reconcile_catalogue__mutmut_orig # type: ignore # mutmut generated
mutants_x_reconcile_catalogue__mutmut['x_reconcile_catalogue__mutmut_1'] = x_reconcile_catalogue__mutmut_1 # type: ignore # mutmut generated
mutants_x_reconcile_catalogue__mutmut['x_reconcile_catalogue__mutmut_2'] = x_reconcile_catalogue__mutmut_2 # type: ignore # mutmut generated
mutants_x_reconcile_catalogue__mutmut['x_reconcile_catalogue__mutmut_3'] = x_reconcile_catalogue__mutmut_3 # type: ignore # mutmut generated
mutants_x_reconcile_catalogue__mutmut['x_reconcile_catalogue__mutmut_4'] = x_reconcile_catalogue__mutmut_4 # type: ignore # mutmut generated
mutants_x_reconcile_catalogue__mutmut['x_reconcile_catalogue__mutmut_5'] = x_reconcile_catalogue__mutmut_5 # type: ignore # mutmut generated
mutants_x_reconcile_catalogue__mutmut['x_reconcile_catalogue__mutmut_6'] = x_reconcile_catalogue__mutmut_6 # type: ignore # mutmut generated
mutants_x_reconcile_catalogue__mutmut['x_reconcile_catalogue__mutmut_7'] = x_reconcile_catalogue__mutmut_7 # type: ignore # mutmut generated
mutants_x_reconcile_catalogue__mutmut['x_reconcile_catalogue__mutmut_8'] = x_reconcile_catalogue__mutmut_8 # type: ignore # mutmut generated
mutants_x_reconcile_catalogue__mutmut['x_reconcile_catalogue__mutmut_9'] = x_reconcile_catalogue__mutmut_9 # type: ignore # mutmut generated
mutants_x_reconcile_catalogue__mutmut['x_reconcile_catalogue__mutmut_10'] = x_reconcile_catalogue__mutmut_10 # type: ignore # mutmut generated
mutants_x_reconcile_catalogue__mutmut['x_reconcile_catalogue__mutmut_11'] = x_reconcile_catalogue__mutmut_11 # type: ignore # mutmut generated
mutants_x_reconcile_catalogue__mutmut['x_reconcile_catalogue__mutmut_12'] = x_reconcile_catalogue__mutmut_12 # type: ignore # mutmut generated
mutants_x_reconcile_catalogue__mutmut['x_reconcile_catalogue__mutmut_13'] = x_reconcile_catalogue__mutmut_13 # type: ignore # mutmut generated
mutants_x_reconcile_catalogue__mutmut['x_reconcile_catalogue__mutmut_14'] = x_reconcile_catalogue__mutmut_14 # type: ignore # mutmut generated
mutants_x_catalogue_check_consistency__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_catalogue_check_consistency__mutmut)
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


def x_catalogue_check_consistency__mutmut_orig(
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


def x_catalogue_check_consistency__mutmut_1(
    *,
    cataloged_check_ids: Iterable[str],
    available_check_ids: Iterable[str],
    remediation: str = "XXXX",
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


def x_catalogue_check_consistency__mutmut_2(
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
    report = None
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


def x_catalogue_check_consistency__mutmut_3(
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
        cataloged_check_ids=None,
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


def x_catalogue_check_consistency__mutmut_4(
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
        available_check_ids=None,
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


def x_catalogue_check_consistency__mutmut_5(
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


def x_catalogue_check_consistency__mutmut_6(
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


def x_catalogue_check_consistency__mutmut_7(
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
        print_fn(None)
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


def x_catalogue_check_consistency__mutmut_8(
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
        print_fn("XXcatalogue_check_consistency: catalogue and checks agree.XX")
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


def x_catalogue_check_consistency__mutmut_9(
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
        print_fn("CATALOGUE_CHECK_CONSISTENCY: CATALOGUE AND CHECKS AGREE.")
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


def x_catalogue_check_consistency__mutmut_10(
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
        return 1
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


def x_catalogue_check_consistency__mutmut_11(
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
        print_fn(None)
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


def x_catalogue_check_consistency__mutmut_12(
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
        print_fn("XXFAIL catalogue_check_consistency — check(s) with no catalogue entry:XX")
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


def x_catalogue_check_consistency__mutmut_13(
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
        print_fn("fail catalogue_check_consistency — check(s) with no catalogue entry:")
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


def x_catalogue_check_consistency__mutmut_14(
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
        print_fn("FAIL CATALOGUE_CHECK_CONSISTENCY — CHECK(S) WITH NO CATALOGUE ENTRY:")
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


def x_catalogue_check_consistency__mutmut_15(
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
            print_fn(None)
    if report.dangling_entries:
        print_fn("FAIL catalogue_check_consistency — catalogue entr(ies) naming a missing check:")
        for entry_id, check_id in report.dangling_entries:
            print_fn(f"  {entry_id} -> {check_id}")
    if remediation:
        print_fn("")
        print_fn(remediation)
    return 1


def x_catalogue_check_consistency__mutmut_16(
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
        print_fn(None)
        for entry_id, check_id in report.dangling_entries:
            print_fn(f"  {entry_id} -> {check_id}")
    if remediation:
        print_fn("")
        print_fn(remediation)
    return 1


def x_catalogue_check_consistency__mutmut_17(
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
        print_fn("XXFAIL catalogue_check_consistency — catalogue entr(ies) naming a missing check:XX")
        for entry_id, check_id in report.dangling_entries:
            print_fn(f"  {entry_id} -> {check_id}")
    if remediation:
        print_fn("")
        print_fn(remediation)
    return 1


def x_catalogue_check_consistency__mutmut_18(
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
        print_fn("fail catalogue_check_consistency — catalogue entr(ies) naming a missing check:")
        for entry_id, check_id in report.dangling_entries:
            print_fn(f"  {entry_id} -> {check_id}")
    if remediation:
        print_fn("")
        print_fn(remediation)
    return 1


def x_catalogue_check_consistency__mutmut_19(
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
        print_fn("FAIL CATALOGUE_CHECK_CONSISTENCY — CATALOGUE ENTR(IES) NAMING A MISSING CHECK:")
        for entry_id, check_id in report.dangling_entries:
            print_fn(f"  {entry_id} -> {check_id}")
    if remediation:
        print_fn("")
        print_fn(remediation)
    return 1


def x_catalogue_check_consistency__mutmut_20(
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
            print_fn(None)
    if remediation:
        print_fn("")
        print_fn(remediation)
    return 1


def x_catalogue_check_consistency__mutmut_21(
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
        print_fn(None)
        print_fn(remediation)
    return 1


def x_catalogue_check_consistency__mutmut_22(
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
        print_fn("XXXX")
        print_fn(remediation)
    return 1


def x_catalogue_check_consistency__mutmut_23(
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
        print_fn(None)
    return 1


def x_catalogue_check_consistency__mutmut_24(
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
    return 2

mutants_x_catalogue_check_consistency__mutmut['_mutmut_orig'] = x_catalogue_check_consistency__mutmut_orig # type: ignore # mutmut generated
mutants_x_catalogue_check_consistency__mutmut['x_catalogue_check_consistency__mutmut_1'] = x_catalogue_check_consistency__mutmut_1 # type: ignore # mutmut generated
mutants_x_catalogue_check_consistency__mutmut['x_catalogue_check_consistency__mutmut_2'] = x_catalogue_check_consistency__mutmut_2 # type: ignore # mutmut generated
mutants_x_catalogue_check_consistency__mutmut['x_catalogue_check_consistency__mutmut_3'] = x_catalogue_check_consistency__mutmut_3 # type: ignore # mutmut generated
mutants_x_catalogue_check_consistency__mutmut['x_catalogue_check_consistency__mutmut_4'] = x_catalogue_check_consistency__mutmut_4 # type: ignore # mutmut generated
mutants_x_catalogue_check_consistency__mutmut['x_catalogue_check_consistency__mutmut_5'] = x_catalogue_check_consistency__mutmut_5 # type: ignore # mutmut generated
mutants_x_catalogue_check_consistency__mutmut['x_catalogue_check_consistency__mutmut_6'] = x_catalogue_check_consistency__mutmut_6 # type: ignore # mutmut generated
mutants_x_catalogue_check_consistency__mutmut['x_catalogue_check_consistency__mutmut_7'] = x_catalogue_check_consistency__mutmut_7 # type: ignore # mutmut generated
mutants_x_catalogue_check_consistency__mutmut['x_catalogue_check_consistency__mutmut_8'] = x_catalogue_check_consistency__mutmut_8 # type: ignore # mutmut generated
mutants_x_catalogue_check_consistency__mutmut['x_catalogue_check_consistency__mutmut_9'] = x_catalogue_check_consistency__mutmut_9 # type: ignore # mutmut generated
mutants_x_catalogue_check_consistency__mutmut['x_catalogue_check_consistency__mutmut_10'] = x_catalogue_check_consistency__mutmut_10 # type: ignore # mutmut generated
mutants_x_catalogue_check_consistency__mutmut['x_catalogue_check_consistency__mutmut_11'] = x_catalogue_check_consistency__mutmut_11 # type: ignore # mutmut generated
mutants_x_catalogue_check_consistency__mutmut['x_catalogue_check_consistency__mutmut_12'] = x_catalogue_check_consistency__mutmut_12 # type: ignore # mutmut generated
mutants_x_catalogue_check_consistency__mutmut['x_catalogue_check_consistency__mutmut_13'] = x_catalogue_check_consistency__mutmut_13 # type: ignore # mutmut generated
mutants_x_catalogue_check_consistency__mutmut['x_catalogue_check_consistency__mutmut_14'] = x_catalogue_check_consistency__mutmut_14 # type: ignore # mutmut generated
mutants_x_catalogue_check_consistency__mutmut['x_catalogue_check_consistency__mutmut_15'] = x_catalogue_check_consistency__mutmut_15 # type: ignore # mutmut generated
mutants_x_catalogue_check_consistency__mutmut['x_catalogue_check_consistency__mutmut_16'] = x_catalogue_check_consistency__mutmut_16 # type: ignore # mutmut generated
mutants_x_catalogue_check_consistency__mutmut['x_catalogue_check_consistency__mutmut_17'] = x_catalogue_check_consistency__mutmut_17 # type: ignore # mutmut generated
mutants_x_catalogue_check_consistency__mutmut['x_catalogue_check_consistency__mutmut_18'] = x_catalogue_check_consistency__mutmut_18 # type: ignore # mutmut generated
mutants_x_catalogue_check_consistency__mutmut['x_catalogue_check_consistency__mutmut_19'] = x_catalogue_check_consistency__mutmut_19 # type: ignore # mutmut generated
mutants_x_catalogue_check_consistency__mutmut['x_catalogue_check_consistency__mutmut_20'] = x_catalogue_check_consistency__mutmut_20 # type: ignore # mutmut generated
mutants_x_catalogue_check_consistency__mutmut['x_catalogue_check_consistency__mutmut_21'] = x_catalogue_check_consistency__mutmut_21 # type: ignore # mutmut generated
mutants_x_catalogue_check_consistency__mutmut['x_catalogue_check_consistency__mutmut_22'] = x_catalogue_check_consistency__mutmut_22 # type: ignore # mutmut generated
mutants_x_catalogue_check_consistency__mutmut['x_catalogue_check_consistency__mutmut_23'] = x_catalogue_check_consistency__mutmut_23 # type: ignore # mutmut generated
mutants_x_catalogue_check_consistency__mutmut['x_catalogue_check_consistency__mutmut_24'] = x_catalogue_check_consistency__mutmut_24 # type: ignore # mutmut generated


__all__ = [
    "staged_added_files",
    "added_since_tag",
    "resolve_previous_tag",
    # catalogue consistency
    "CatalogueConsistencyReport",
    "reconcile_catalogue",
    "catalogue_check_consistency",
]
