"""CORE check: path_naming — repo paths follow the configured naming convention.

Consistent path naming is a discoverability contract: a reader who knows the
convention can predict where a file lives and what it is called. This rule flags
a path whose NAME violates the convention configured for the root it sits under —
``kebab-case`` for docs/dirs and ``snake_case`` for importable Python.

The check inspects path NAMES, never file content. It enumerates every in-scope
path and flags the ones whose stem/name fails the convention regex for its root,
unless the name is a fixed conventional repository filename (``README.md``,
``LICENSE``, …) or the path is generated dependency/cache output.

Ported from tc-agent-zone ``scripts/checks/path_naming.py`` and re-expressed as a
configurable, repo-agnostic rule. The donor hardcoded ``docs/``, ``scripts/checks``,
the ADR pattern and a fixed allow-list; here the governed roots are config:

* ``kebab_roots`` — repo-relative prefixes whose ``.md`` files must be kebab-case.
* ``snake_roots`` — repo-relative prefixes whose ``.py`` files must be snake_case
  (an importable module name).

A consumer with no roots configured flags nothing.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: A kebab-case stem: lowercase, digits, hyphens; no leading hyphen.
KEBAB_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
#: An importable Python module name: ``__init__`` or an optionally-underscored
#: lowercase snake stem with a ``.py`` suffix.
SNAKE_RE = re.compile(r"^(__init__|_?[a-z0-9][a-z0-9_]*)\.py$")

#: Filenames that are conventionally upper-case / fixed and exempt from the
#: kebab/snake rules. This is part of the rule definition, not consumer config.
DEFAULT_ALLOWED_NAMES: frozenset[str] = frozenset(
    {
        "README.md",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        "SECURITY.md",
        "LICENSE.md",
        "LICENSE",
        "AGENTS.md",
        "VERSION",
        "Makefile",
    }
)

#: Generated dependency/cache segments outside the authored-path domain.
DEFAULT_EXEMPT_SEGMENTS: tuple[str, ...] = (
    ".git",
    ".github",
    ".architecture",
    "node_modules",
    "__pycache__",
    ".venv",
    ".pytest_cache",
    ".ruff_cache",
)

REMEDIATION = _remediation(
    fix=("rename the path to lowercase kebab-case for docs/dirs or snake_case for importable Python."),
    nxt="re-run this check to confirm the rename cleared the violation.",
    run="python -m tc_fitness.core_checks.path_naming",
    passing="docs/my-design-note.md   scripts/checks/my_check.py",
    forbidden="docs/MyDesignNote.md    scripts/checks/My-Check.py",
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x_name_violates_convention__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_name_violates_convention__mutmut)
def name_violates_convention(
    rel: str,
    *,
    kebab_roots: tuple[str, ...],
    snake_roots: tuple[str, ...],
) -> bool:
    """True iff repo-relative ``rel`` breaks the convention for its root.

    Pure helper (the detection core) so tests can assert on it directly. A
    ``.md`` path under a kebab root must have a kebab-case stem; a ``.py`` path
    under a snake root must be an importable module name. Always-allowed
    filenames are never flagged. A path under no configured root is clean.
    """
    name = rel.rsplit("/", 1)[-1]
    if name in DEFAULT_ALLOWED_NAMES:
        return False
    if rel.endswith(".md") and rel.startswith(kebab_roots):
        stem = name[: -len(".md")]
        return KEBAB_RE.fullmatch(stem) is None
    if rel.endswith(".py") and rel.startswith(snake_roots):
        return SNAKE_RE.fullmatch(name) is None
    return False


def x_name_violates_convention__mutmut_orig(
    rel: str,
    *,
    kebab_roots: tuple[str, ...],
    snake_roots: tuple[str, ...],
) -> bool:
    """True iff repo-relative ``rel`` breaks the convention for its root.

    Pure helper (the detection core) so tests can assert on it directly. A
    ``.md`` path under a kebab root must have a kebab-case stem; a ``.py`` path
    under a snake root must be an importable module name. Always-allowed
    filenames are never flagged. A path under no configured root is clean.
    """
    name = rel.rsplit("/", 1)[-1]
    if name in DEFAULT_ALLOWED_NAMES:
        return False
    if rel.endswith(".md") and rel.startswith(kebab_roots):
        stem = name[: -len(".md")]
        return KEBAB_RE.fullmatch(stem) is None
    if rel.endswith(".py") and rel.startswith(snake_roots):
        return SNAKE_RE.fullmatch(name) is None
    return False


def x_name_violates_convention__mutmut_1(
    rel: str,
    *,
    kebab_roots: tuple[str, ...],
    snake_roots: tuple[str, ...],
) -> bool:
    """True iff repo-relative ``rel`` breaks the convention for its root.

    Pure helper (the detection core) so tests can assert on it directly. A
    ``.md`` path under a kebab root must have a kebab-case stem; a ``.py`` path
    under a snake root must be an importable module name. Always-allowed
    filenames are never flagged. A path under no configured root is clean.
    """
    name = None
    if name in DEFAULT_ALLOWED_NAMES:
        return False
    if rel.endswith(".md") and rel.startswith(kebab_roots):
        stem = name[: -len(".md")]
        return KEBAB_RE.fullmatch(stem) is None
    if rel.endswith(".py") and rel.startswith(snake_roots):
        return SNAKE_RE.fullmatch(name) is None
    return False


def x_name_violates_convention__mutmut_2(
    rel: str,
    *,
    kebab_roots: tuple[str, ...],
    snake_roots: tuple[str, ...],
) -> bool:
    """True iff repo-relative ``rel`` breaks the convention for its root.

    Pure helper (the detection core) so tests can assert on it directly. A
    ``.md`` path under a kebab root must have a kebab-case stem; a ``.py`` path
    under a snake root must be an importable module name. Always-allowed
    filenames are never flagged. A path under no configured root is clean.
    """
    name = rel.rsplit(None, 1)[-1]
    if name in DEFAULT_ALLOWED_NAMES:
        return False
    if rel.endswith(".md") and rel.startswith(kebab_roots):
        stem = name[: -len(".md")]
        return KEBAB_RE.fullmatch(stem) is None
    if rel.endswith(".py") and rel.startswith(snake_roots):
        return SNAKE_RE.fullmatch(name) is None
    return False


def x_name_violates_convention__mutmut_3(
    rel: str,
    *,
    kebab_roots: tuple[str, ...],
    snake_roots: tuple[str, ...],
) -> bool:
    """True iff repo-relative ``rel`` breaks the convention for its root.

    Pure helper (the detection core) so tests can assert on it directly. A
    ``.md`` path under a kebab root must have a kebab-case stem; a ``.py`` path
    under a snake root must be an importable module name. Always-allowed
    filenames are never flagged. A path under no configured root is clean.
    """
    name = rel.rsplit("/", None)[-1]
    if name in DEFAULT_ALLOWED_NAMES:
        return False
    if rel.endswith(".md") and rel.startswith(kebab_roots):
        stem = name[: -len(".md")]
        return KEBAB_RE.fullmatch(stem) is None
    if rel.endswith(".py") and rel.startswith(snake_roots):
        return SNAKE_RE.fullmatch(name) is None
    return False


def x_name_violates_convention__mutmut_4(
    rel: str,
    *,
    kebab_roots: tuple[str, ...],
    snake_roots: tuple[str, ...],
) -> bool:
    """True iff repo-relative ``rel`` breaks the convention for its root.

    Pure helper (the detection core) so tests can assert on it directly. A
    ``.md`` path under a kebab root must have a kebab-case stem; a ``.py`` path
    under a snake root must be an importable module name. Always-allowed
    filenames are never flagged. A path under no configured root is clean.
    """
    name = rel.rsplit(1)[-1]
    if name in DEFAULT_ALLOWED_NAMES:
        return False
    if rel.endswith(".md") and rel.startswith(kebab_roots):
        stem = name[: -len(".md")]
        return KEBAB_RE.fullmatch(stem) is None
    if rel.endswith(".py") and rel.startswith(snake_roots):
        return SNAKE_RE.fullmatch(name) is None
    return False


def x_name_violates_convention__mutmut_5(
    rel: str,
    *,
    kebab_roots: tuple[str, ...],
    snake_roots: tuple[str, ...],
) -> bool:
    """True iff repo-relative ``rel`` breaks the convention for its root.

    Pure helper (the detection core) so tests can assert on it directly. A
    ``.md`` path under a kebab root must have a kebab-case stem; a ``.py`` path
    under a snake root must be an importable module name. Always-allowed
    filenames are never flagged. A path under no configured root is clean.
    """
    name = rel.rsplit("/", )[-1]
    if name in DEFAULT_ALLOWED_NAMES:
        return False
    if rel.endswith(".md") and rel.startswith(kebab_roots):
        stem = name[: -len(".md")]
        return KEBAB_RE.fullmatch(stem) is None
    if rel.endswith(".py") and rel.startswith(snake_roots):
        return SNAKE_RE.fullmatch(name) is None
    return False


def x_name_violates_convention__mutmut_6(
    rel: str,
    *,
    kebab_roots: tuple[str, ...],
    snake_roots: tuple[str, ...],
) -> bool:
    """True iff repo-relative ``rel`` breaks the convention for its root.

    Pure helper (the detection core) so tests can assert on it directly. A
    ``.md`` path under a kebab root must have a kebab-case stem; a ``.py`` path
    under a snake root must be an importable module name. Always-allowed
    filenames are never flagged. A path under no configured root is clean.
    """
    name = rel.split("/", 1)[-1]
    if name in DEFAULT_ALLOWED_NAMES:
        return False
    if rel.endswith(".md") and rel.startswith(kebab_roots):
        stem = name[: -len(".md")]
        return KEBAB_RE.fullmatch(stem) is None
    if rel.endswith(".py") and rel.startswith(snake_roots):
        return SNAKE_RE.fullmatch(name) is None
    return False


def x_name_violates_convention__mutmut_7(
    rel: str,
    *,
    kebab_roots: tuple[str, ...],
    snake_roots: tuple[str, ...],
) -> bool:
    """True iff repo-relative ``rel`` breaks the convention for its root.

    Pure helper (the detection core) so tests can assert on it directly. A
    ``.md`` path under a kebab root must have a kebab-case stem; a ``.py`` path
    under a snake root must be an importable module name. Always-allowed
    filenames are never flagged. A path under no configured root is clean.
    """
    name = rel.rsplit("XX/XX", 1)[-1]
    if name in DEFAULT_ALLOWED_NAMES:
        return False
    if rel.endswith(".md") and rel.startswith(kebab_roots):
        stem = name[: -len(".md")]
        return KEBAB_RE.fullmatch(stem) is None
    if rel.endswith(".py") and rel.startswith(snake_roots):
        return SNAKE_RE.fullmatch(name) is None
    return False


def x_name_violates_convention__mutmut_8(
    rel: str,
    *,
    kebab_roots: tuple[str, ...],
    snake_roots: tuple[str, ...],
) -> bool:
    """True iff repo-relative ``rel`` breaks the convention for its root.

    Pure helper (the detection core) so tests can assert on it directly. A
    ``.md`` path under a kebab root must have a kebab-case stem; a ``.py`` path
    under a snake root must be an importable module name. Always-allowed
    filenames are never flagged. A path under no configured root is clean.
    """
    name = rel.rsplit("/", 2)[-1]
    if name in DEFAULT_ALLOWED_NAMES:
        return False
    if rel.endswith(".md") and rel.startswith(kebab_roots):
        stem = name[: -len(".md")]
        return KEBAB_RE.fullmatch(stem) is None
    if rel.endswith(".py") and rel.startswith(snake_roots):
        return SNAKE_RE.fullmatch(name) is None
    return False


def x_name_violates_convention__mutmut_9(
    rel: str,
    *,
    kebab_roots: tuple[str, ...],
    snake_roots: tuple[str, ...],
) -> bool:
    """True iff repo-relative ``rel`` breaks the convention for its root.

    Pure helper (the detection core) so tests can assert on it directly. A
    ``.md`` path under a kebab root must have a kebab-case stem; a ``.py`` path
    under a snake root must be an importable module name. Always-allowed
    filenames are never flagged. A path under no configured root is clean.
    """
    name = rel.rsplit("/", 1)[+1]
    if name in DEFAULT_ALLOWED_NAMES:
        return False
    if rel.endswith(".md") and rel.startswith(kebab_roots):
        stem = name[: -len(".md")]
        return KEBAB_RE.fullmatch(stem) is None
    if rel.endswith(".py") and rel.startswith(snake_roots):
        return SNAKE_RE.fullmatch(name) is None
    return False


def x_name_violates_convention__mutmut_10(
    rel: str,
    *,
    kebab_roots: tuple[str, ...],
    snake_roots: tuple[str, ...],
) -> bool:
    """True iff repo-relative ``rel`` breaks the convention for its root.

    Pure helper (the detection core) so tests can assert on it directly. A
    ``.md`` path under a kebab root must have a kebab-case stem; a ``.py`` path
    under a snake root must be an importable module name. Always-allowed
    filenames are never flagged. A path under no configured root is clean.
    """
    name = rel.rsplit("/", 1)[-2]
    if name in DEFAULT_ALLOWED_NAMES:
        return False
    if rel.endswith(".md") and rel.startswith(kebab_roots):
        stem = name[: -len(".md")]
        return KEBAB_RE.fullmatch(stem) is None
    if rel.endswith(".py") and rel.startswith(snake_roots):
        return SNAKE_RE.fullmatch(name) is None
    return False


def x_name_violates_convention__mutmut_11(
    rel: str,
    *,
    kebab_roots: tuple[str, ...],
    snake_roots: tuple[str, ...],
) -> bool:
    """True iff repo-relative ``rel`` breaks the convention for its root.

    Pure helper (the detection core) so tests can assert on it directly. A
    ``.md`` path under a kebab root must have a kebab-case stem; a ``.py`` path
    under a snake root must be an importable module name. Always-allowed
    filenames are never flagged. A path under no configured root is clean.
    """
    name = rel.rsplit("/", 1)[-1]
    if name not in DEFAULT_ALLOWED_NAMES:
        return False
    if rel.endswith(".md") and rel.startswith(kebab_roots):
        stem = name[: -len(".md")]
        return KEBAB_RE.fullmatch(stem) is None
    if rel.endswith(".py") and rel.startswith(snake_roots):
        return SNAKE_RE.fullmatch(name) is None
    return False


def x_name_violates_convention__mutmut_12(
    rel: str,
    *,
    kebab_roots: tuple[str, ...],
    snake_roots: tuple[str, ...],
) -> bool:
    """True iff repo-relative ``rel`` breaks the convention for its root.

    Pure helper (the detection core) so tests can assert on it directly. A
    ``.md`` path under a kebab root must have a kebab-case stem; a ``.py`` path
    under a snake root must be an importable module name. Always-allowed
    filenames are never flagged. A path under no configured root is clean.
    """
    name = rel.rsplit("/", 1)[-1]
    if name in DEFAULT_ALLOWED_NAMES:
        return True
    if rel.endswith(".md") and rel.startswith(kebab_roots):
        stem = name[: -len(".md")]
        return KEBAB_RE.fullmatch(stem) is None
    if rel.endswith(".py") and rel.startswith(snake_roots):
        return SNAKE_RE.fullmatch(name) is None
    return False


def x_name_violates_convention__mutmut_13(
    rel: str,
    *,
    kebab_roots: tuple[str, ...],
    snake_roots: tuple[str, ...],
) -> bool:
    """True iff repo-relative ``rel`` breaks the convention for its root.

    Pure helper (the detection core) so tests can assert on it directly. A
    ``.md`` path under a kebab root must have a kebab-case stem; a ``.py`` path
    under a snake root must be an importable module name. Always-allowed
    filenames are never flagged. A path under no configured root is clean.
    """
    name = rel.rsplit("/", 1)[-1]
    if name in DEFAULT_ALLOWED_NAMES:
        return False
    if rel.endswith(".md") or rel.startswith(kebab_roots):
        stem = name[: -len(".md")]
        return KEBAB_RE.fullmatch(stem) is None
    if rel.endswith(".py") and rel.startswith(snake_roots):
        return SNAKE_RE.fullmatch(name) is None
    return False


def x_name_violates_convention__mutmut_14(
    rel: str,
    *,
    kebab_roots: tuple[str, ...],
    snake_roots: tuple[str, ...],
) -> bool:
    """True iff repo-relative ``rel`` breaks the convention for its root.

    Pure helper (the detection core) so tests can assert on it directly. A
    ``.md`` path under a kebab root must have a kebab-case stem; a ``.py`` path
    under a snake root must be an importable module name. Always-allowed
    filenames are never flagged. A path under no configured root is clean.
    """
    name = rel.rsplit("/", 1)[-1]
    if name in DEFAULT_ALLOWED_NAMES:
        return False
    if rel.endswith(None) and rel.startswith(kebab_roots):
        stem = name[: -len(".md")]
        return KEBAB_RE.fullmatch(stem) is None
    if rel.endswith(".py") and rel.startswith(snake_roots):
        return SNAKE_RE.fullmatch(name) is None
    return False


def x_name_violates_convention__mutmut_15(
    rel: str,
    *,
    kebab_roots: tuple[str, ...],
    snake_roots: tuple[str, ...],
) -> bool:
    """True iff repo-relative ``rel`` breaks the convention for its root.

    Pure helper (the detection core) so tests can assert on it directly. A
    ``.md`` path under a kebab root must have a kebab-case stem; a ``.py`` path
    under a snake root must be an importable module name. Always-allowed
    filenames are never flagged. A path under no configured root is clean.
    """
    name = rel.rsplit("/", 1)[-1]
    if name in DEFAULT_ALLOWED_NAMES:
        return False
    if rel.endswith("XX.mdXX") and rel.startswith(kebab_roots):
        stem = name[: -len(".md")]
        return KEBAB_RE.fullmatch(stem) is None
    if rel.endswith(".py") and rel.startswith(snake_roots):
        return SNAKE_RE.fullmatch(name) is None
    return False


def x_name_violates_convention__mutmut_16(
    rel: str,
    *,
    kebab_roots: tuple[str, ...],
    snake_roots: tuple[str, ...],
) -> bool:
    """True iff repo-relative ``rel`` breaks the convention for its root.

    Pure helper (the detection core) so tests can assert on it directly. A
    ``.md`` path under a kebab root must have a kebab-case stem; a ``.py`` path
    under a snake root must be an importable module name. Always-allowed
    filenames are never flagged. A path under no configured root is clean.
    """
    name = rel.rsplit("/", 1)[-1]
    if name in DEFAULT_ALLOWED_NAMES:
        return False
    if rel.endswith(".MD") and rel.startswith(kebab_roots):
        stem = name[: -len(".md")]
        return KEBAB_RE.fullmatch(stem) is None
    if rel.endswith(".py") and rel.startswith(snake_roots):
        return SNAKE_RE.fullmatch(name) is None
    return False


def x_name_violates_convention__mutmut_17(
    rel: str,
    *,
    kebab_roots: tuple[str, ...],
    snake_roots: tuple[str, ...],
) -> bool:
    """True iff repo-relative ``rel`` breaks the convention for its root.

    Pure helper (the detection core) so tests can assert on it directly. A
    ``.md`` path under a kebab root must have a kebab-case stem; a ``.py`` path
    under a snake root must be an importable module name. Always-allowed
    filenames are never flagged. A path under no configured root is clean.
    """
    name = rel.rsplit("/", 1)[-1]
    if name in DEFAULT_ALLOWED_NAMES:
        return False
    if rel.endswith(".md") and rel.startswith(None):
        stem = name[: -len(".md")]
        return KEBAB_RE.fullmatch(stem) is None
    if rel.endswith(".py") and rel.startswith(snake_roots):
        return SNAKE_RE.fullmatch(name) is None
    return False


def x_name_violates_convention__mutmut_18(
    rel: str,
    *,
    kebab_roots: tuple[str, ...],
    snake_roots: tuple[str, ...],
) -> bool:
    """True iff repo-relative ``rel`` breaks the convention for its root.

    Pure helper (the detection core) so tests can assert on it directly. A
    ``.md`` path under a kebab root must have a kebab-case stem; a ``.py`` path
    under a snake root must be an importable module name. Always-allowed
    filenames are never flagged. A path under no configured root is clean.
    """
    name = rel.rsplit("/", 1)[-1]
    if name in DEFAULT_ALLOWED_NAMES:
        return False
    if rel.endswith(".md") and rel.startswith(kebab_roots):
        stem = None
        return KEBAB_RE.fullmatch(stem) is None
    if rel.endswith(".py") and rel.startswith(snake_roots):
        return SNAKE_RE.fullmatch(name) is None
    return False


def x_name_violates_convention__mutmut_19(
    rel: str,
    *,
    kebab_roots: tuple[str, ...],
    snake_roots: tuple[str, ...],
) -> bool:
    """True iff repo-relative ``rel`` breaks the convention for its root.

    Pure helper (the detection core) so tests can assert on it directly. A
    ``.md`` path under a kebab root must have a kebab-case stem; a ``.py`` path
    under a snake root must be an importable module name. Always-allowed
    filenames are never flagged. A path under no configured root is clean.
    """
    name = rel.rsplit("/", 1)[-1]
    if name in DEFAULT_ALLOWED_NAMES:
        return False
    if rel.endswith(".md") and rel.startswith(kebab_roots):
        stem = name[: +len(".md")]
        return KEBAB_RE.fullmatch(stem) is None
    if rel.endswith(".py") and rel.startswith(snake_roots):
        return SNAKE_RE.fullmatch(name) is None
    return False


def x_name_violates_convention__mutmut_20(
    rel: str,
    *,
    kebab_roots: tuple[str, ...],
    snake_roots: tuple[str, ...],
) -> bool:
    """True iff repo-relative ``rel`` breaks the convention for its root.

    Pure helper (the detection core) so tests can assert on it directly. A
    ``.md`` path under a kebab root must have a kebab-case stem; a ``.py`` path
    under a snake root must be an importable module name. Always-allowed
    filenames are never flagged. A path under no configured root is clean.
    """
    name = rel.rsplit("/", 1)[-1]
    if name in DEFAULT_ALLOWED_NAMES:
        return False
    if rel.endswith(".md") and rel.startswith(kebab_roots):
        stem = name[: -len(".md")]
        return KEBAB_RE.fullmatch(None) is None
    if rel.endswith(".py") and rel.startswith(snake_roots):
        return SNAKE_RE.fullmatch(name) is None
    return False


def x_name_violates_convention__mutmut_21(
    rel: str,
    *,
    kebab_roots: tuple[str, ...],
    snake_roots: tuple[str, ...],
) -> bool:
    """True iff repo-relative ``rel`` breaks the convention for its root.

    Pure helper (the detection core) so tests can assert on it directly. A
    ``.md`` path under a kebab root must have a kebab-case stem; a ``.py`` path
    under a snake root must be an importable module name. Always-allowed
    filenames are never flagged. A path under no configured root is clean.
    """
    name = rel.rsplit("/", 1)[-1]
    if name in DEFAULT_ALLOWED_NAMES:
        return False
    if rel.endswith(".md") and rel.startswith(kebab_roots):
        stem = name[: -len(".md")]
        return KEBAB_RE.fullmatch(stem) is not None
    if rel.endswith(".py") and rel.startswith(snake_roots):
        return SNAKE_RE.fullmatch(name) is None
    return False


def x_name_violates_convention__mutmut_22(
    rel: str,
    *,
    kebab_roots: tuple[str, ...],
    snake_roots: tuple[str, ...],
) -> bool:
    """True iff repo-relative ``rel`` breaks the convention for its root.

    Pure helper (the detection core) so tests can assert on it directly. A
    ``.md`` path under a kebab root must have a kebab-case stem; a ``.py`` path
    under a snake root must be an importable module name. Always-allowed
    filenames are never flagged. A path under no configured root is clean.
    """
    name = rel.rsplit("/", 1)[-1]
    if name in DEFAULT_ALLOWED_NAMES:
        return False
    if rel.endswith(".md") and rel.startswith(kebab_roots):
        stem = name[: -len(".md")]
        return KEBAB_RE.fullmatch(stem) is None
    if rel.endswith(".py") or rel.startswith(snake_roots):
        return SNAKE_RE.fullmatch(name) is None
    return False


def x_name_violates_convention__mutmut_23(
    rel: str,
    *,
    kebab_roots: tuple[str, ...],
    snake_roots: tuple[str, ...],
) -> bool:
    """True iff repo-relative ``rel`` breaks the convention for its root.

    Pure helper (the detection core) so tests can assert on it directly. A
    ``.md`` path under a kebab root must have a kebab-case stem; a ``.py`` path
    under a snake root must be an importable module name. Always-allowed
    filenames are never flagged. A path under no configured root is clean.
    """
    name = rel.rsplit("/", 1)[-1]
    if name in DEFAULT_ALLOWED_NAMES:
        return False
    if rel.endswith(".md") and rel.startswith(kebab_roots):
        stem = name[: -len(".md")]
        return KEBAB_RE.fullmatch(stem) is None
    if rel.endswith(None) and rel.startswith(snake_roots):
        return SNAKE_RE.fullmatch(name) is None
    return False


def x_name_violates_convention__mutmut_24(
    rel: str,
    *,
    kebab_roots: tuple[str, ...],
    snake_roots: tuple[str, ...],
) -> bool:
    """True iff repo-relative ``rel`` breaks the convention for its root.

    Pure helper (the detection core) so tests can assert on it directly. A
    ``.md`` path under a kebab root must have a kebab-case stem; a ``.py`` path
    under a snake root must be an importable module name. Always-allowed
    filenames are never flagged. A path under no configured root is clean.
    """
    name = rel.rsplit("/", 1)[-1]
    if name in DEFAULT_ALLOWED_NAMES:
        return False
    if rel.endswith(".md") and rel.startswith(kebab_roots):
        stem = name[: -len(".md")]
        return KEBAB_RE.fullmatch(stem) is None
    if rel.endswith("XX.pyXX") and rel.startswith(snake_roots):
        return SNAKE_RE.fullmatch(name) is None
    return False


def x_name_violates_convention__mutmut_25(
    rel: str,
    *,
    kebab_roots: tuple[str, ...],
    snake_roots: tuple[str, ...],
) -> bool:
    """True iff repo-relative ``rel`` breaks the convention for its root.

    Pure helper (the detection core) so tests can assert on it directly. A
    ``.md`` path under a kebab root must have a kebab-case stem; a ``.py`` path
    under a snake root must be an importable module name. Always-allowed
    filenames are never flagged. A path under no configured root is clean.
    """
    name = rel.rsplit("/", 1)[-1]
    if name in DEFAULT_ALLOWED_NAMES:
        return False
    if rel.endswith(".md") and rel.startswith(kebab_roots):
        stem = name[: -len(".md")]
        return KEBAB_RE.fullmatch(stem) is None
    if rel.endswith(".PY") and rel.startswith(snake_roots):
        return SNAKE_RE.fullmatch(name) is None
    return False


def x_name_violates_convention__mutmut_26(
    rel: str,
    *,
    kebab_roots: tuple[str, ...],
    snake_roots: tuple[str, ...],
) -> bool:
    """True iff repo-relative ``rel`` breaks the convention for its root.

    Pure helper (the detection core) so tests can assert on it directly. A
    ``.md`` path under a kebab root must have a kebab-case stem; a ``.py`` path
    under a snake root must be an importable module name. Always-allowed
    filenames are never flagged. A path under no configured root is clean.
    """
    name = rel.rsplit("/", 1)[-1]
    if name in DEFAULT_ALLOWED_NAMES:
        return False
    if rel.endswith(".md") and rel.startswith(kebab_roots):
        stem = name[: -len(".md")]
        return KEBAB_RE.fullmatch(stem) is None
    if rel.endswith(".py") and rel.startswith(None):
        return SNAKE_RE.fullmatch(name) is None
    return False


def x_name_violates_convention__mutmut_27(
    rel: str,
    *,
    kebab_roots: tuple[str, ...],
    snake_roots: tuple[str, ...],
) -> bool:
    """True iff repo-relative ``rel`` breaks the convention for its root.

    Pure helper (the detection core) so tests can assert on it directly. A
    ``.md`` path under a kebab root must have a kebab-case stem; a ``.py`` path
    under a snake root must be an importable module name. Always-allowed
    filenames are never flagged. A path under no configured root is clean.
    """
    name = rel.rsplit("/", 1)[-1]
    if name in DEFAULT_ALLOWED_NAMES:
        return False
    if rel.endswith(".md") and rel.startswith(kebab_roots):
        stem = name[: -len(".md")]
        return KEBAB_RE.fullmatch(stem) is None
    if rel.endswith(".py") and rel.startswith(snake_roots):
        return SNAKE_RE.fullmatch(None) is None
    return False


def x_name_violates_convention__mutmut_28(
    rel: str,
    *,
    kebab_roots: tuple[str, ...],
    snake_roots: tuple[str, ...],
) -> bool:
    """True iff repo-relative ``rel`` breaks the convention for its root.

    Pure helper (the detection core) so tests can assert on it directly. A
    ``.md`` path under a kebab root must have a kebab-case stem; a ``.py`` path
    under a snake root must be an importable module name. Always-allowed
    filenames are never flagged. A path under no configured root is clean.
    """
    name = rel.rsplit("/", 1)[-1]
    if name in DEFAULT_ALLOWED_NAMES:
        return False
    if rel.endswith(".md") and rel.startswith(kebab_roots):
        stem = name[: -len(".md")]
        return KEBAB_RE.fullmatch(stem) is None
    if rel.endswith(".py") and rel.startswith(snake_roots):
        return SNAKE_RE.fullmatch(name) is not None
    return False


def x_name_violates_convention__mutmut_29(
    rel: str,
    *,
    kebab_roots: tuple[str, ...],
    snake_roots: tuple[str, ...],
) -> bool:
    """True iff repo-relative ``rel`` breaks the convention for its root.

    Pure helper (the detection core) so tests can assert on it directly. A
    ``.md`` path under a kebab root must have a kebab-case stem; a ``.py`` path
    under a snake root must be an importable module name. Always-allowed
    filenames are never flagged. A path under no configured root is clean.
    """
    name = rel.rsplit("/", 1)[-1]
    if name in DEFAULT_ALLOWED_NAMES:
        return False
    if rel.endswith(".md") and rel.startswith(kebab_roots):
        stem = name[: -len(".md")]
        return KEBAB_RE.fullmatch(stem) is None
    if rel.endswith(".py") and rel.startswith(snake_roots):
        return SNAKE_RE.fullmatch(name) is None
    return True

mutants_x_name_violates_convention__mutmut['_mutmut_orig'] = x_name_violates_convention__mutmut_orig # type: ignore # mutmut generated
mutants_x_name_violates_convention__mutmut['x_name_violates_convention__mutmut_1'] = x_name_violates_convention__mutmut_1 # type: ignore # mutmut generated
mutants_x_name_violates_convention__mutmut['x_name_violates_convention__mutmut_2'] = x_name_violates_convention__mutmut_2 # type: ignore # mutmut generated
mutants_x_name_violates_convention__mutmut['x_name_violates_convention__mutmut_3'] = x_name_violates_convention__mutmut_3 # type: ignore # mutmut generated
mutants_x_name_violates_convention__mutmut['x_name_violates_convention__mutmut_4'] = x_name_violates_convention__mutmut_4 # type: ignore # mutmut generated
mutants_x_name_violates_convention__mutmut['x_name_violates_convention__mutmut_5'] = x_name_violates_convention__mutmut_5 # type: ignore # mutmut generated
mutants_x_name_violates_convention__mutmut['x_name_violates_convention__mutmut_6'] = x_name_violates_convention__mutmut_6 # type: ignore # mutmut generated
mutants_x_name_violates_convention__mutmut['x_name_violates_convention__mutmut_7'] = x_name_violates_convention__mutmut_7 # type: ignore # mutmut generated
mutants_x_name_violates_convention__mutmut['x_name_violates_convention__mutmut_8'] = x_name_violates_convention__mutmut_8 # type: ignore # mutmut generated
mutants_x_name_violates_convention__mutmut['x_name_violates_convention__mutmut_9'] = x_name_violates_convention__mutmut_9 # type: ignore # mutmut generated
mutants_x_name_violates_convention__mutmut['x_name_violates_convention__mutmut_10'] = x_name_violates_convention__mutmut_10 # type: ignore # mutmut generated
mutants_x_name_violates_convention__mutmut['x_name_violates_convention__mutmut_11'] = x_name_violates_convention__mutmut_11 # type: ignore # mutmut generated
mutants_x_name_violates_convention__mutmut['x_name_violates_convention__mutmut_12'] = x_name_violates_convention__mutmut_12 # type: ignore # mutmut generated
mutants_x_name_violates_convention__mutmut['x_name_violates_convention__mutmut_13'] = x_name_violates_convention__mutmut_13 # type: ignore # mutmut generated
mutants_x_name_violates_convention__mutmut['x_name_violates_convention__mutmut_14'] = x_name_violates_convention__mutmut_14 # type: ignore # mutmut generated
mutants_x_name_violates_convention__mutmut['x_name_violates_convention__mutmut_15'] = x_name_violates_convention__mutmut_15 # type: ignore # mutmut generated
mutants_x_name_violates_convention__mutmut['x_name_violates_convention__mutmut_16'] = x_name_violates_convention__mutmut_16 # type: ignore # mutmut generated
mutants_x_name_violates_convention__mutmut['x_name_violates_convention__mutmut_17'] = x_name_violates_convention__mutmut_17 # type: ignore # mutmut generated
mutants_x_name_violates_convention__mutmut['x_name_violates_convention__mutmut_18'] = x_name_violates_convention__mutmut_18 # type: ignore # mutmut generated
mutants_x_name_violates_convention__mutmut['x_name_violates_convention__mutmut_19'] = x_name_violates_convention__mutmut_19 # type: ignore # mutmut generated
mutants_x_name_violates_convention__mutmut['x_name_violates_convention__mutmut_20'] = x_name_violates_convention__mutmut_20 # type: ignore # mutmut generated
mutants_x_name_violates_convention__mutmut['x_name_violates_convention__mutmut_21'] = x_name_violates_convention__mutmut_21 # type: ignore # mutmut generated
mutants_x_name_violates_convention__mutmut['x_name_violates_convention__mutmut_22'] = x_name_violates_convention__mutmut_22 # type: ignore # mutmut generated
mutants_x_name_violates_convention__mutmut['x_name_violates_convention__mutmut_23'] = x_name_violates_convention__mutmut_23 # type: ignore # mutmut generated
mutants_x_name_violates_convention__mutmut['x_name_violates_convention__mutmut_24'] = x_name_violates_convention__mutmut_24 # type: ignore # mutmut generated
mutants_x_name_violates_convention__mutmut['x_name_violates_convention__mutmut_25'] = x_name_violates_convention__mutmut_25 # type: ignore # mutmut generated
mutants_x_name_violates_convention__mutmut['x_name_violates_convention__mutmut_26'] = x_name_violates_convention__mutmut_26 # type: ignore # mutmut generated
mutants_x_name_violates_convention__mutmut['x_name_violates_convention__mutmut_27'] = x_name_violates_convention__mutmut_27 # type: ignore # mutmut generated
mutants_x_name_violates_convention__mutmut['x_name_violates_convention__mutmut_28'] = x_name_violates_convention__mutmut_28 # type: ignore # mutmut generated
mutants_x_name_violates_convention__mutmut['x_name_violates_convention__mutmut_29'] = x_name_violates_convention__mutmut_29 # type: ignore # mutmut generated
mutants_xǁPathNamingǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁPathNamingǁis_in_scope__mutmut: MutantDict = {}  # type: ignore
mutants_xǁPathNamingǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore
mutants_xǁPathNamingǁenumerate_files__mutmut: MutantDict = {}  # type: ignore


class PathNaming(FitnessRule):
    """Flags paths whose name breaks the configured naming convention."""

    name = "path-naming"
    remediation = REMEDIATION
    #: Both doc and Python files are candidates; the root config decides which
    #: convention applies. A consumer narrows via ``extensions`` if desired.
    extensions = (".md", ".py")

    kebab_roots: tuple[str, ...] = ()
    snake_roots: tuple[str, ...] = ()

    @classmethod
    @_mutmut_mutated(mutants_xǁPathNamingǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PathNaming:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PathNaming)  # noqa: S101  # narrowing for mypy
        kebab = config.get("kebab_roots")
        if kebab is not None:
            rule.kebab_roots = tuple(kebab)
        snake = config.get("snake_roots")
        if snake is not None:
            rule.snake_roots = tuple(snake)
        return rule

    @classmethod
    def xǁPathNamingǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PathNaming:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PathNaming)  # noqa: S101  # narrowing for mypy
        kebab = config.get("kebab_roots")
        if kebab is not None:
            rule.kebab_roots = tuple(kebab)
        snake = config.get("snake_roots")
        if snake is not None:
            rule.snake_roots = tuple(snake)
        return rule

    @classmethod
    def xǁPathNamingǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PathNaming:
        rule = None
        assert isinstance(rule, PathNaming)  # noqa: S101  # narrowing for mypy
        kebab = config.get("kebab_roots")
        if kebab is not None:
            rule.kebab_roots = tuple(kebab)
        snake = config.get("snake_roots")
        if snake is not None:
            rule.snake_roots = tuple(snake)
        return rule

    @classmethod
    def xǁPathNamingǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PathNaming:
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, PathNaming)  # noqa: S101  # narrowing for mypy
        kebab = config.get("kebab_roots")
        if kebab is not None:
            rule.kebab_roots = tuple(kebab)
        snake = config.get("snake_roots")
        if snake is not None:
            rule.snake_roots = tuple(snake)
        return rule

    @classmethod
    def xǁPathNamingǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PathNaming:
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, PathNaming)  # noqa: S101  # narrowing for mypy
        kebab = config.get("kebab_roots")
        if kebab is not None:
            rule.kebab_roots = tuple(kebab)
        snake = config.get("snake_roots")
        if snake is not None:
            rule.snake_roots = tuple(snake)
        return rule

    @classmethod
    def xǁPathNamingǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PathNaming:
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, PathNaming)  # noqa: S101  # narrowing for mypy
        kebab = config.get("kebab_roots")
        if kebab is not None:
            rule.kebab_roots = tuple(kebab)
        snake = config.get("snake_roots")
        if snake is not None:
            rule.snake_roots = tuple(snake)
        return rule

    @classmethod
    def xǁPathNamingǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PathNaming:
        rule = super().from_config(config, )
        assert isinstance(rule, PathNaming)  # noqa: S101  # narrowing for mypy
        kebab = config.get("kebab_roots")
        if kebab is not None:
            rule.kebab_roots = tuple(kebab)
        snake = config.get("snake_roots")
        if snake is not None:
            rule.snake_roots = tuple(snake)
        return rule

    @classmethod
    def xǁPathNamingǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PathNaming:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PathNaming)  # noqa: S101  # narrowing for mypy
        kebab = None
        if kebab is not None:
            rule.kebab_roots = tuple(kebab)
        snake = config.get("snake_roots")
        if snake is not None:
            rule.snake_roots = tuple(snake)
        return rule

    @classmethod
    def xǁPathNamingǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PathNaming:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PathNaming)  # noqa: S101  # narrowing for mypy
        kebab = config.get(None)
        if kebab is not None:
            rule.kebab_roots = tuple(kebab)
        snake = config.get("snake_roots")
        if snake is not None:
            rule.snake_roots = tuple(snake)
        return rule

    @classmethod
    def xǁPathNamingǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PathNaming:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PathNaming)  # noqa: S101  # narrowing for mypy
        kebab = config.get("XXkebab_rootsXX")
        if kebab is not None:
            rule.kebab_roots = tuple(kebab)
        snake = config.get("snake_roots")
        if snake is not None:
            rule.snake_roots = tuple(snake)
        return rule

    @classmethod
    def xǁPathNamingǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PathNaming:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PathNaming)  # noqa: S101  # narrowing for mypy
        kebab = config.get("KEBAB_ROOTS")
        if kebab is not None:
            rule.kebab_roots = tuple(kebab)
        snake = config.get("snake_roots")
        if snake is not None:
            rule.snake_roots = tuple(snake)
        return rule

    @classmethod
    def xǁPathNamingǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PathNaming:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PathNaming)  # noqa: S101  # narrowing for mypy
        kebab = config.get("kebab_roots")
        if kebab is None:
            rule.kebab_roots = tuple(kebab)
        snake = config.get("snake_roots")
        if snake is not None:
            rule.snake_roots = tuple(snake)
        return rule

    @classmethod
    def xǁPathNamingǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PathNaming:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PathNaming)  # noqa: S101  # narrowing for mypy
        kebab = config.get("kebab_roots")
        if kebab is not None:
            rule.kebab_roots = None
        snake = config.get("snake_roots")
        if snake is not None:
            rule.snake_roots = tuple(snake)
        return rule

    @classmethod
    def xǁPathNamingǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PathNaming:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PathNaming)  # noqa: S101  # narrowing for mypy
        kebab = config.get("kebab_roots")
        if kebab is not None:
            rule.kebab_roots = tuple(None)
        snake = config.get("snake_roots")
        if snake is not None:
            rule.snake_roots = tuple(snake)
        return rule

    @classmethod
    def xǁPathNamingǁfrom_config__mutmut_13(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PathNaming:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PathNaming)  # noqa: S101  # narrowing for mypy
        kebab = config.get("kebab_roots")
        if kebab is not None:
            rule.kebab_roots = tuple(kebab)
        snake = None
        if snake is not None:
            rule.snake_roots = tuple(snake)
        return rule

    @classmethod
    def xǁPathNamingǁfrom_config__mutmut_14(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PathNaming:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PathNaming)  # noqa: S101  # narrowing for mypy
        kebab = config.get("kebab_roots")
        if kebab is not None:
            rule.kebab_roots = tuple(kebab)
        snake = config.get(None)
        if snake is not None:
            rule.snake_roots = tuple(snake)
        return rule

    @classmethod
    def xǁPathNamingǁfrom_config__mutmut_15(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PathNaming:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PathNaming)  # noqa: S101  # narrowing for mypy
        kebab = config.get("kebab_roots")
        if kebab is not None:
            rule.kebab_roots = tuple(kebab)
        snake = config.get("XXsnake_rootsXX")
        if snake is not None:
            rule.snake_roots = tuple(snake)
        return rule

    @classmethod
    def xǁPathNamingǁfrom_config__mutmut_16(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PathNaming:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PathNaming)  # noqa: S101  # narrowing for mypy
        kebab = config.get("kebab_roots")
        if kebab is not None:
            rule.kebab_roots = tuple(kebab)
        snake = config.get("SNAKE_ROOTS")
        if snake is not None:
            rule.snake_roots = tuple(snake)
        return rule

    @classmethod
    def xǁPathNamingǁfrom_config__mutmut_17(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PathNaming:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PathNaming)  # noqa: S101  # narrowing for mypy
        kebab = config.get("kebab_roots")
        if kebab is not None:
            rule.kebab_roots = tuple(kebab)
        snake = config.get("snake_roots")
        if snake is None:
            rule.snake_roots = tuple(snake)
        return rule

    @classmethod
    def xǁPathNamingǁfrom_config__mutmut_18(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PathNaming:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PathNaming)  # noqa: S101  # narrowing for mypy
        kebab = config.get("kebab_roots")
        if kebab is not None:
            rule.kebab_roots = tuple(kebab)
        snake = config.get("snake_roots")
        if snake is not None:
            rule.snake_roots = None
        return rule

    @classmethod
    def xǁPathNamingǁfrom_config__mutmut_19(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PathNaming:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PathNaming)  # noqa: S101  # narrowing for mypy
        kebab = config.get("kebab_roots")
        if kebab is not None:
            rule.kebab_roots = tuple(kebab)
        snake = config.get("snake_roots")
        if snake is not None:
            rule.snake_roots = tuple(None)
        return rule

    @_mutmut_mutated(mutants_xǁPathNamingǁis_in_scope__mutmut)
    def is_in_scope(self, rel: str) -> bool:
        if any(seg in DEFAULT_EXEMPT_SEGMENTS for seg in rel.split("/")):
            return False
        # Scope is governed by the per-root conventions, not by ``roots``;
        # a path under no convention-root is simply never a violation.
        return rel.endswith(self._extensions)

    def xǁPathNamingǁis_in_scope__mutmut_orig(self, rel: str) -> bool:
        if any(seg in DEFAULT_EXEMPT_SEGMENTS for seg in rel.split("/")):
            return False
        # Scope is governed by the per-root conventions, not by ``roots``;
        # a path under no convention-root is simply never a violation.
        return rel.endswith(self._extensions)

    def xǁPathNamingǁis_in_scope__mutmut_1(self, rel: str) -> bool:
        if any(None):
            return False
        # Scope is governed by the per-root conventions, not by ``roots``;
        # a path under no convention-root is simply never a violation.
        return rel.endswith(self._extensions)

    def xǁPathNamingǁis_in_scope__mutmut_2(self, rel: str) -> bool:
        if any(seg not in DEFAULT_EXEMPT_SEGMENTS for seg in rel.split("/")):
            return False
        # Scope is governed by the per-root conventions, not by ``roots``;
        # a path under no convention-root is simply never a violation.
        return rel.endswith(self._extensions)

    def xǁPathNamingǁis_in_scope__mutmut_3(self, rel: str) -> bool:
        if any(seg in DEFAULT_EXEMPT_SEGMENTS for seg in rel.split(None)):
            return False
        # Scope is governed by the per-root conventions, not by ``roots``;
        # a path under no convention-root is simply never a violation.
        return rel.endswith(self._extensions)

    def xǁPathNamingǁis_in_scope__mutmut_4(self, rel: str) -> bool:
        if any(seg in DEFAULT_EXEMPT_SEGMENTS for seg in rel.split("XX/XX")):
            return False
        # Scope is governed by the per-root conventions, not by ``roots``;
        # a path under no convention-root is simply never a violation.
        return rel.endswith(self._extensions)

    def xǁPathNamingǁis_in_scope__mutmut_5(self, rel: str) -> bool:
        if any(seg in DEFAULT_EXEMPT_SEGMENTS for seg in rel.split("/")):
            return True
        # Scope is governed by the per-root conventions, not by ``roots``;
        # a path under no convention-root is simply never a violation.
        return rel.endswith(self._extensions)

    def xǁPathNamingǁis_in_scope__mutmut_6(self, rel: str) -> bool:
        if any(seg in DEFAULT_EXEMPT_SEGMENTS for seg in rel.split("/")):
            return False
        # Scope is governed by the per-root conventions, not by ``roots``;
        # a path under no convention-root is simply never a violation.
        return rel.endswith(None)

    @_mutmut_mutated(mutants_xǁPathNamingǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        rel = str(self._repo_relative(path)).replace("\\", "/")
        return name_violates_convention(
            rel,
            kebab_roots=self.kebab_roots,
            snake_roots=self.snake_roots,
        )

    def xǁPathNamingǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        rel = str(self._repo_relative(path)).replace("\\", "/")
        return name_violates_convention(
            rel,
            kebab_roots=self.kebab_roots,
            snake_roots=self.snake_roots,
        )

    def xǁPathNamingǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        rel = None
        return name_violates_convention(
            rel,
            kebab_roots=self.kebab_roots,
            snake_roots=self.snake_roots,
        )

    def xǁPathNamingǁfile_has_violation__mutmut_2(self, path: Path) -> bool:
        rel = str(self._repo_relative(path)).replace(None, "/")
        return name_violates_convention(
            rel,
            kebab_roots=self.kebab_roots,
            snake_roots=self.snake_roots,
        )

    def xǁPathNamingǁfile_has_violation__mutmut_3(self, path: Path) -> bool:
        rel = str(self._repo_relative(path)).replace("\\", None)
        return name_violates_convention(
            rel,
            kebab_roots=self.kebab_roots,
            snake_roots=self.snake_roots,
        )

    def xǁPathNamingǁfile_has_violation__mutmut_4(self, path: Path) -> bool:
        rel = str(self._repo_relative(path)).replace("/")
        return name_violates_convention(
            rel,
            kebab_roots=self.kebab_roots,
            snake_roots=self.snake_roots,
        )

    def xǁPathNamingǁfile_has_violation__mutmut_5(self, path: Path) -> bool:
        rel = str(self._repo_relative(path)).replace("\\", )
        return name_violates_convention(
            rel,
            kebab_roots=self.kebab_roots,
            snake_roots=self.snake_roots,
        )

    def xǁPathNamingǁfile_has_violation__mutmut_6(self, path: Path) -> bool:
        rel = str(None).replace("\\", "/")
        return name_violates_convention(
            rel,
            kebab_roots=self.kebab_roots,
            snake_roots=self.snake_roots,
        )

    def xǁPathNamingǁfile_has_violation__mutmut_7(self, path: Path) -> bool:
        rel = str(self._repo_relative(None)).replace("\\", "/")
        return name_violates_convention(
            rel,
            kebab_roots=self.kebab_roots,
            snake_roots=self.snake_roots,
        )

    def xǁPathNamingǁfile_has_violation__mutmut_8(self, path: Path) -> bool:
        rel = str(self._repo_relative(path)).replace("XX\\XX", "/")
        return name_violates_convention(
            rel,
            kebab_roots=self.kebab_roots,
            snake_roots=self.snake_roots,
        )

    def xǁPathNamingǁfile_has_violation__mutmut_9(self, path: Path) -> bool:
        rel = str(self._repo_relative(path)).replace("\\", "XX/XX")
        return name_violates_convention(
            rel,
            kebab_roots=self.kebab_roots,
            snake_roots=self.snake_roots,
        )

    def xǁPathNamingǁfile_has_violation__mutmut_10(self, path: Path) -> bool:
        rel = str(self._repo_relative(path)).replace("\\", "/")
        return name_violates_convention(
            None,
            kebab_roots=self.kebab_roots,
            snake_roots=self.snake_roots,
        )

    def xǁPathNamingǁfile_has_violation__mutmut_11(self, path: Path) -> bool:
        rel = str(self._repo_relative(path)).replace("\\", "/")
        return name_violates_convention(
            rel,
            kebab_roots=None,
            snake_roots=self.snake_roots,
        )

    def xǁPathNamingǁfile_has_violation__mutmut_12(self, path: Path) -> bool:
        rel = str(self._repo_relative(path)).replace("\\", "/")
        return name_violates_convention(
            rel,
            kebab_roots=self.kebab_roots,
            snake_roots=None,
        )

    def xǁPathNamingǁfile_has_violation__mutmut_13(self, path: Path) -> bool:
        rel = str(self._repo_relative(path)).replace("\\", "/")
        return name_violates_convention(
            kebab_roots=self.kebab_roots,
            snake_roots=self.snake_roots,
        )

    def xǁPathNamingǁfile_has_violation__mutmut_14(self, path: Path) -> bool:
        rel = str(self._repo_relative(path)).replace("\\", "/")
        return name_violates_convention(
            rel,
            snake_roots=self.snake_roots,
        )

    def xǁPathNamingǁfile_has_violation__mutmut_15(self, path: Path) -> bool:
        rel = str(self._repo_relative(path)).replace("\\", "/")
        return name_violates_convention(
            rel,
            kebab_roots=self.kebab_roots,
            )

    @_mutmut_mutated(mutants_xǁPathNamingǁenumerate_files__mutmut)
    def enumerate_files(self) -> list[Path]:
        """Enumerate under the union of the convention roots.

        ``path_naming`` scopes by ``kebab_roots`` / ``snake_roots`` rather than
        the base ``roots`` knob, so enumeration walks those prefixes. When none
        are configured the rule enumerates nothing (flags nothing).
        """
        out: list[Path] = []
        for root in (*self.kebab_roots, *self.snake_roots):
            root_path = self._repo_root / root
            if not root_path.exists():
                continue
            for path in root_path.rglob("*"):
                if not path.is_file() or "__pycache__" in path.parts:
                    continue
                if path.name.endswith(self._extensions):
                    out.append(path)
        return out

    def xǁPathNamingǁenumerate_files__mutmut_orig(self) -> list[Path]:
        """Enumerate under the union of the convention roots.

        ``path_naming`` scopes by ``kebab_roots`` / ``snake_roots`` rather than
        the base ``roots`` knob, so enumeration walks those prefixes. When none
        are configured the rule enumerates nothing (flags nothing).
        """
        out: list[Path] = []
        for root in (*self.kebab_roots, *self.snake_roots):
            root_path = self._repo_root / root
            if not root_path.exists():
                continue
            for path in root_path.rglob("*"):
                if not path.is_file() or "__pycache__" in path.parts:
                    continue
                if path.name.endswith(self._extensions):
                    out.append(path)
        return out

    def xǁPathNamingǁenumerate_files__mutmut_1(self) -> list[Path]:
        """Enumerate under the union of the convention roots.

        ``path_naming`` scopes by ``kebab_roots`` / ``snake_roots`` rather than
        the base ``roots`` knob, so enumeration walks those prefixes. When none
        are configured the rule enumerates nothing (flags nothing).
        """
        out: list[Path] = None
        for root in (*self.kebab_roots, *self.snake_roots):
            root_path = self._repo_root / root
            if not root_path.exists():
                continue
            for path in root_path.rglob("*"):
                if not path.is_file() or "__pycache__" in path.parts:
                    continue
                if path.name.endswith(self._extensions):
                    out.append(path)
        return out

    def xǁPathNamingǁenumerate_files__mutmut_2(self) -> list[Path]:
        """Enumerate under the union of the convention roots.

        ``path_naming`` scopes by ``kebab_roots`` / ``snake_roots`` rather than
        the base ``roots`` knob, so enumeration walks those prefixes. When none
        are configured the rule enumerates nothing (flags nothing).
        """
        out: list[Path] = []
        for root in (*self.kebab_roots, *self.snake_roots):
            root_path = None
            if not root_path.exists():
                continue
            for path in root_path.rglob("*"):
                if not path.is_file() or "__pycache__" in path.parts:
                    continue
                if path.name.endswith(self._extensions):
                    out.append(path)
        return out

    def xǁPathNamingǁenumerate_files__mutmut_3(self) -> list[Path]:
        """Enumerate under the union of the convention roots.

        ``path_naming`` scopes by ``kebab_roots`` / ``snake_roots`` rather than
        the base ``roots`` knob, so enumeration walks those prefixes. When none
        are configured the rule enumerates nothing (flags nothing).
        """
        out: list[Path] = []
        for root in (*self.kebab_roots, *self.snake_roots):
            root_path = self._repo_root * root
            if not root_path.exists():
                continue
            for path in root_path.rglob("*"):
                if not path.is_file() or "__pycache__" in path.parts:
                    continue
                if path.name.endswith(self._extensions):
                    out.append(path)
        return out

    def xǁPathNamingǁenumerate_files__mutmut_4(self) -> list[Path]:
        """Enumerate under the union of the convention roots.

        ``path_naming`` scopes by ``kebab_roots`` / ``snake_roots`` rather than
        the base ``roots`` knob, so enumeration walks those prefixes. When none
        are configured the rule enumerates nothing (flags nothing).
        """
        out: list[Path] = []
        for root in (*self.kebab_roots, *self.snake_roots):
            root_path = self._repo_root / root
            if root_path.exists():
                continue
            for path in root_path.rglob("*"):
                if not path.is_file() or "__pycache__" in path.parts:
                    continue
                if path.name.endswith(self._extensions):
                    out.append(path)
        return out

    def xǁPathNamingǁenumerate_files__mutmut_5(self) -> list[Path]:
        """Enumerate under the union of the convention roots.

        ``path_naming`` scopes by ``kebab_roots`` / ``snake_roots`` rather than
        the base ``roots`` knob, so enumeration walks those prefixes. When none
        are configured the rule enumerates nothing (flags nothing).
        """
        out: list[Path] = []
        for root in (*self.kebab_roots, *self.snake_roots):
            root_path = self._repo_root / root
            if not root_path.exists():
                break
            for path in root_path.rglob("*"):
                if not path.is_file() or "__pycache__" in path.parts:
                    continue
                if path.name.endswith(self._extensions):
                    out.append(path)
        return out

    def xǁPathNamingǁenumerate_files__mutmut_6(self) -> list[Path]:
        """Enumerate under the union of the convention roots.

        ``path_naming`` scopes by ``kebab_roots`` / ``snake_roots`` rather than
        the base ``roots`` knob, so enumeration walks those prefixes. When none
        are configured the rule enumerates nothing (flags nothing).
        """
        out: list[Path] = []
        for root in (*self.kebab_roots, *self.snake_roots):
            root_path = self._repo_root / root
            if not root_path.exists():
                continue
            for path in root_path.rglob(None):
                if not path.is_file() or "__pycache__" in path.parts:
                    continue
                if path.name.endswith(self._extensions):
                    out.append(path)
        return out

    def xǁPathNamingǁenumerate_files__mutmut_7(self) -> list[Path]:
        """Enumerate under the union of the convention roots.

        ``path_naming`` scopes by ``kebab_roots`` / ``snake_roots`` rather than
        the base ``roots`` knob, so enumeration walks those prefixes. When none
        are configured the rule enumerates nothing (flags nothing).
        """
        out: list[Path] = []
        for root in (*self.kebab_roots, *self.snake_roots):
            root_path = self._repo_root / root
            if not root_path.exists():
                continue
            for path in root_path.rglob("XX*XX"):
                if not path.is_file() or "__pycache__" in path.parts:
                    continue
                if path.name.endswith(self._extensions):
                    out.append(path)
        return out

    def xǁPathNamingǁenumerate_files__mutmut_8(self) -> list[Path]:
        """Enumerate under the union of the convention roots.

        ``path_naming`` scopes by ``kebab_roots`` / ``snake_roots`` rather than
        the base ``roots`` knob, so enumeration walks those prefixes. When none
        are configured the rule enumerates nothing (flags nothing).
        """
        out: list[Path] = []
        for root in (*self.kebab_roots, *self.snake_roots):
            root_path = self._repo_root / root
            if not root_path.exists():
                continue
            for path in root_path.rglob("*"):
                if not path.is_file() and "__pycache__" in path.parts:
                    continue
                if path.name.endswith(self._extensions):
                    out.append(path)
        return out

    def xǁPathNamingǁenumerate_files__mutmut_9(self) -> list[Path]:
        """Enumerate under the union of the convention roots.

        ``path_naming`` scopes by ``kebab_roots`` / ``snake_roots`` rather than
        the base ``roots`` knob, so enumeration walks those prefixes. When none
        are configured the rule enumerates nothing (flags nothing).
        """
        out: list[Path] = []
        for root in (*self.kebab_roots, *self.snake_roots):
            root_path = self._repo_root / root
            if not root_path.exists():
                continue
            for path in root_path.rglob("*"):
                if path.is_file() or "__pycache__" in path.parts:
                    continue
                if path.name.endswith(self._extensions):
                    out.append(path)
        return out

    def xǁPathNamingǁenumerate_files__mutmut_10(self) -> list[Path]:
        """Enumerate under the union of the convention roots.

        ``path_naming`` scopes by ``kebab_roots`` / ``snake_roots`` rather than
        the base ``roots`` knob, so enumeration walks those prefixes. When none
        are configured the rule enumerates nothing (flags nothing).
        """
        out: list[Path] = []
        for root in (*self.kebab_roots, *self.snake_roots):
            root_path = self._repo_root / root
            if not root_path.exists():
                continue
            for path in root_path.rglob("*"):
                if not path.is_file() or "XX__pycache__XX" in path.parts:
                    continue
                if path.name.endswith(self._extensions):
                    out.append(path)
        return out

    def xǁPathNamingǁenumerate_files__mutmut_11(self) -> list[Path]:
        """Enumerate under the union of the convention roots.

        ``path_naming`` scopes by ``kebab_roots`` / ``snake_roots`` rather than
        the base ``roots`` knob, so enumeration walks those prefixes. When none
        are configured the rule enumerates nothing (flags nothing).
        """
        out: list[Path] = []
        for root in (*self.kebab_roots, *self.snake_roots):
            root_path = self._repo_root / root
            if not root_path.exists():
                continue
            for path in root_path.rglob("*"):
                if not path.is_file() or "__PYCACHE__" in path.parts:
                    continue
                if path.name.endswith(self._extensions):
                    out.append(path)
        return out

    def xǁPathNamingǁenumerate_files__mutmut_12(self) -> list[Path]:
        """Enumerate under the union of the convention roots.

        ``path_naming`` scopes by ``kebab_roots`` / ``snake_roots`` rather than
        the base ``roots`` knob, so enumeration walks those prefixes. When none
        are configured the rule enumerates nothing (flags nothing).
        """
        out: list[Path] = []
        for root in (*self.kebab_roots, *self.snake_roots):
            root_path = self._repo_root / root
            if not root_path.exists():
                continue
            for path in root_path.rglob("*"):
                if not path.is_file() or "__pycache__" not in path.parts:
                    continue
                if path.name.endswith(self._extensions):
                    out.append(path)
        return out

    def xǁPathNamingǁenumerate_files__mutmut_13(self) -> list[Path]:
        """Enumerate under the union of the convention roots.

        ``path_naming`` scopes by ``kebab_roots`` / ``snake_roots`` rather than
        the base ``roots`` knob, so enumeration walks those prefixes. When none
        are configured the rule enumerates nothing (flags nothing).
        """
        out: list[Path] = []
        for root in (*self.kebab_roots, *self.snake_roots):
            root_path = self._repo_root / root
            if not root_path.exists():
                continue
            for path in root_path.rglob("*"):
                if not path.is_file() or "__pycache__" in path.parts:
                    break
                if path.name.endswith(self._extensions):
                    out.append(path)
        return out

    def xǁPathNamingǁenumerate_files__mutmut_14(self) -> list[Path]:
        """Enumerate under the union of the convention roots.

        ``path_naming`` scopes by ``kebab_roots`` / ``snake_roots`` rather than
        the base ``roots`` knob, so enumeration walks those prefixes. When none
        are configured the rule enumerates nothing (flags nothing).
        """
        out: list[Path] = []
        for root in (*self.kebab_roots, *self.snake_roots):
            root_path = self._repo_root / root
            if not root_path.exists():
                continue
            for path in root_path.rglob("*"):
                if not path.is_file() or "__pycache__" in path.parts:
                    continue
                if path.name.endswith(None):
                    out.append(path)
        return out

    def xǁPathNamingǁenumerate_files__mutmut_15(self) -> list[Path]:
        """Enumerate under the union of the convention roots.

        ``path_naming`` scopes by ``kebab_roots`` / ``snake_roots`` rather than
        the base ``roots`` knob, so enumeration walks those prefixes. When none
        are configured the rule enumerates nothing (flags nothing).
        """
        out: list[Path] = []
        for root in (*self.kebab_roots, *self.snake_roots):
            root_path = self._repo_root / root
            if not root_path.exists():
                continue
            for path in root_path.rglob("*"):
                if not path.is_file() or "__pycache__" in path.parts:
                    continue
                if path.name.endswith(self._extensions):
                    out.append(None)
        return out

mutants_xǁPathNamingǁfrom_config__mutmut['_mutmut_orig'] = PathNaming.xǁPathNamingǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁPathNamingǁfrom_config__mutmut['xǁPathNamingǁfrom_config__mutmut_1'] = PathNaming.xǁPathNamingǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁPathNamingǁfrom_config__mutmut['xǁPathNamingǁfrom_config__mutmut_2'] = PathNaming.xǁPathNamingǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁPathNamingǁfrom_config__mutmut['xǁPathNamingǁfrom_config__mutmut_3'] = PathNaming.xǁPathNamingǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁPathNamingǁfrom_config__mutmut['xǁPathNamingǁfrom_config__mutmut_4'] = PathNaming.xǁPathNamingǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁPathNamingǁfrom_config__mutmut['xǁPathNamingǁfrom_config__mutmut_5'] = PathNaming.xǁPathNamingǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁPathNamingǁfrom_config__mutmut['xǁPathNamingǁfrom_config__mutmut_6'] = PathNaming.xǁPathNamingǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁPathNamingǁfrom_config__mutmut['xǁPathNamingǁfrom_config__mutmut_7'] = PathNaming.xǁPathNamingǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁPathNamingǁfrom_config__mutmut['xǁPathNamingǁfrom_config__mutmut_8'] = PathNaming.xǁPathNamingǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁPathNamingǁfrom_config__mutmut['xǁPathNamingǁfrom_config__mutmut_9'] = PathNaming.xǁPathNamingǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁPathNamingǁfrom_config__mutmut['xǁPathNamingǁfrom_config__mutmut_10'] = PathNaming.xǁPathNamingǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁPathNamingǁfrom_config__mutmut['xǁPathNamingǁfrom_config__mutmut_11'] = PathNaming.xǁPathNamingǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁPathNamingǁfrom_config__mutmut['xǁPathNamingǁfrom_config__mutmut_12'] = PathNaming.xǁPathNamingǁfrom_config__mutmut_12 # type: ignore # mutmut generated
mutants_xǁPathNamingǁfrom_config__mutmut['xǁPathNamingǁfrom_config__mutmut_13'] = PathNaming.xǁPathNamingǁfrom_config__mutmut_13 # type: ignore # mutmut generated
mutants_xǁPathNamingǁfrom_config__mutmut['xǁPathNamingǁfrom_config__mutmut_14'] = PathNaming.xǁPathNamingǁfrom_config__mutmut_14 # type: ignore # mutmut generated
mutants_xǁPathNamingǁfrom_config__mutmut['xǁPathNamingǁfrom_config__mutmut_15'] = PathNaming.xǁPathNamingǁfrom_config__mutmut_15 # type: ignore # mutmut generated
mutants_xǁPathNamingǁfrom_config__mutmut['xǁPathNamingǁfrom_config__mutmut_16'] = PathNaming.xǁPathNamingǁfrom_config__mutmut_16 # type: ignore # mutmut generated
mutants_xǁPathNamingǁfrom_config__mutmut['xǁPathNamingǁfrom_config__mutmut_17'] = PathNaming.xǁPathNamingǁfrom_config__mutmut_17 # type: ignore # mutmut generated
mutants_xǁPathNamingǁfrom_config__mutmut['xǁPathNamingǁfrom_config__mutmut_18'] = PathNaming.xǁPathNamingǁfrom_config__mutmut_18 # type: ignore # mutmut generated
mutants_xǁPathNamingǁfrom_config__mutmut['xǁPathNamingǁfrom_config__mutmut_19'] = PathNaming.xǁPathNamingǁfrom_config__mutmut_19 # type: ignore # mutmut generated

mutants_xǁPathNamingǁis_in_scope__mutmut['_mutmut_orig'] = PathNaming.xǁPathNamingǁis_in_scope__mutmut_orig # type: ignore # mutmut generated
mutants_xǁPathNamingǁis_in_scope__mutmut['xǁPathNamingǁis_in_scope__mutmut_1'] = PathNaming.xǁPathNamingǁis_in_scope__mutmut_1 # type: ignore # mutmut generated
mutants_xǁPathNamingǁis_in_scope__mutmut['xǁPathNamingǁis_in_scope__mutmut_2'] = PathNaming.xǁPathNamingǁis_in_scope__mutmut_2 # type: ignore # mutmut generated
mutants_xǁPathNamingǁis_in_scope__mutmut['xǁPathNamingǁis_in_scope__mutmut_3'] = PathNaming.xǁPathNamingǁis_in_scope__mutmut_3 # type: ignore # mutmut generated
mutants_xǁPathNamingǁis_in_scope__mutmut['xǁPathNamingǁis_in_scope__mutmut_4'] = PathNaming.xǁPathNamingǁis_in_scope__mutmut_4 # type: ignore # mutmut generated
mutants_xǁPathNamingǁis_in_scope__mutmut['xǁPathNamingǁis_in_scope__mutmut_5'] = PathNaming.xǁPathNamingǁis_in_scope__mutmut_5 # type: ignore # mutmut generated
mutants_xǁPathNamingǁis_in_scope__mutmut['xǁPathNamingǁis_in_scope__mutmut_6'] = PathNaming.xǁPathNamingǁis_in_scope__mutmut_6 # type: ignore # mutmut generated

mutants_xǁPathNamingǁfile_has_violation__mutmut['_mutmut_orig'] = PathNaming.xǁPathNamingǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁPathNamingǁfile_has_violation__mutmut['xǁPathNamingǁfile_has_violation__mutmut_1'] = PathNaming.xǁPathNamingǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_xǁPathNamingǁfile_has_violation__mutmut['xǁPathNamingǁfile_has_violation__mutmut_2'] = PathNaming.xǁPathNamingǁfile_has_violation__mutmut_2 # type: ignore # mutmut generated
mutants_xǁPathNamingǁfile_has_violation__mutmut['xǁPathNamingǁfile_has_violation__mutmut_3'] = PathNaming.xǁPathNamingǁfile_has_violation__mutmut_3 # type: ignore # mutmut generated
mutants_xǁPathNamingǁfile_has_violation__mutmut['xǁPathNamingǁfile_has_violation__mutmut_4'] = PathNaming.xǁPathNamingǁfile_has_violation__mutmut_4 # type: ignore # mutmut generated
mutants_xǁPathNamingǁfile_has_violation__mutmut['xǁPathNamingǁfile_has_violation__mutmut_5'] = PathNaming.xǁPathNamingǁfile_has_violation__mutmut_5 # type: ignore # mutmut generated
mutants_xǁPathNamingǁfile_has_violation__mutmut['xǁPathNamingǁfile_has_violation__mutmut_6'] = PathNaming.xǁPathNamingǁfile_has_violation__mutmut_6 # type: ignore # mutmut generated
mutants_xǁPathNamingǁfile_has_violation__mutmut['xǁPathNamingǁfile_has_violation__mutmut_7'] = PathNaming.xǁPathNamingǁfile_has_violation__mutmut_7 # type: ignore # mutmut generated
mutants_xǁPathNamingǁfile_has_violation__mutmut['xǁPathNamingǁfile_has_violation__mutmut_8'] = PathNaming.xǁPathNamingǁfile_has_violation__mutmut_8 # type: ignore # mutmut generated
mutants_xǁPathNamingǁfile_has_violation__mutmut['xǁPathNamingǁfile_has_violation__mutmut_9'] = PathNaming.xǁPathNamingǁfile_has_violation__mutmut_9 # type: ignore # mutmut generated
mutants_xǁPathNamingǁfile_has_violation__mutmut['xǁPathNamingǁfile_has_violation__mutmut_10'] = PathNaming.xǁPathNamingǁfile_has_violation__mutmut_10 # type: ignore # mutmut generated
mutants_xǁPathNamingǁfile_has_violation__mutmut['xǁPathNamingǁfile_has_violation__mutmut_11'] = PathNaming.xǁPathNamingǁfile_has_violation__mutmut_11 # type: ignore # mutmut generated
mutants_xǁPathNamingǁfile_has_violation__mutmut['xǁPathNamingǁfile_has_violation__mutmut_12'] = PathNaming.xǁPathNamingǁfile_has_violation__mutmut_12 # type: ignore # mutmut generated
mutants_xǁPathNamingǁfile_has_violation__mutmut['xǁPathNamingǁfile_has_violation__mutmut_13'] = PathNaming.xǁPathNamingǁfile_has_violation__mutmut_13 # type: ignore # mutmut generated
mutants_xǁPathNamingǁfile_has_violation__mutmut['xǁPathNamingǁfile_has_violation__mutmut_14'] = PathNaming.xǁPathNamingǁfile_has_violation__mutmut_14 # type: ignore # mutmut generated
mutants_xǁPathNamingǁfile_has_violation__mutmut['xǁPathNamingǁfile_has_violation__mutmut_15'] = PathNaming.xǁPathNamingǁfile_has_violation__mutmut_15 # type: ignore # mutmut generated

mutants_xǁPathNamingǁenumerate_files__mutmut['_mutmut_orig'] = PathNaming.xǁPathNamingǁenumerate_files__mutmut_orig # type: ignore # mutmut generated
mutants_xǁPathNamingǁenumerate_files__mutmut['xǁPathNamingǁenumerate_files__mutmut_1'] = PathNaming.xǁPathNamingǁenumerate_files__mutmut_1 # type: ignore # mutmut generated
mutants_xǁPathNamingǁenumerate_files__mutmut['xǁPathNamingǁenumerate_files__mutmut_2'] = PathNaming.xǁPathNamingǁenumerate_files__mutmut_2 # type: ignore # mutmut generated
mutants_xǁPathNamingǁenumerate_files__mutmut['xǁPathNamingǁenumerate_files__mutmut_3'] = PathNaming.xǁPathNamingǁenumerate_files__mutmut_3 # type: ignore # mutmut generated
mutants_xǁPathNamingǁenumerate_files__mutmut['xǁPathNamingǁenumerate_files__mutmut_4'] = PathNaming.xǁPathNamingǁenumerate_files__mutmut_4 # type: ignore # mutmut generated
mutants_xǁPathNamingǁenumerate_files__mutmut['xǁPathNamingǁenumerate_files__mutmut_5'] = PathNaming.xǁPathNamingǁenumerate_files__mutmut_5 # type: ignore # mutmut generated
mutants_xǁPathNamingǁenumerate_files__mutmut['xǁPathNamingǁenumerate_files__mutmut_6'] = PathNaming.xǁPathNamingǁenumerate_files__mutmut_6 # type: ignore # mutmut generated
mutants_xǁPathNamingǁenumerate_files__mutmut['xǁPathNamingǁenumerate_files__mutmut_7'] = PathNaming.xǁPathNamingǁenumerate_files__mutmut_7 # type: ignore # mutmut generated
mutants_xǁPathNamingǁenumerate_files__mutmut['xǁPathNamingǁenumerate_files__mutmut_8'] = PathNaming.xǁPathNamingǁenumerate_files__mutmut_8 # type: ignore # mutmut generated
mutants_xǁPathNamingǁenumerate_files__mutmut['xǁPathNamingǁenumerate_files__mutmut_9'] = PathNaming.xǁPathNamingǁenumerate_files__mutmut_9 # type: ignore # mutmut generated
mutants_xǁPathNamingǁenumerate_files__mutmut['xǁPathNamingǁenumerate_files__mutmut_10'] = PathNaming.xǁPathNamingǁenumerate_files__mutmut_10 # type: ignore # mutmut generated
mutants_xǁPathNamingǁenumerate_files__mutmut['xǁPathNamingǁenumerate_files__mutmut_11'] = PathNaming.xǁPathNamingǁenumerate_files__mutmut_11 # type: ignore # mutmut generated
mutants_xǁPathNamingǁenumerate_files__mutmut['xǁPathNamingǁenumerate_files__mutmut_12'] = PathNaming.xǁPathNamingǁenumerate_files__mutmut_12 # type: ignore # mutmut generated
mutants_xǁPathNamingǁenumerate_files__mutmut['xǁPathNamingǁenumerate_files__mutmut_13'] = PathNaming.xǁPathNamingǁenumerate_files__mutmut_13 # type: ignore # mutmut generated
mutants_xǁPathNamingǁenumerate_files__mutmut['xǁPathNamingǁenumerate_files__mutmut_14'] = PathNaming.xǁPathNamingǁenumerate_files__mutmut_14 # type: ignore # mutmut generated
mutants_xǁPathNamingǁenumerate_files__mutmut['xǁPathNamingǁenumerate_files__mutmut_15'] = PathNaming.xǁPathNamingǁenumerate_files__mutmut_15 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> PathNaming:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return PathNaming.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> PathNaming:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return PathNaming.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> PathNaming:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return PathNaming.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> PathNaming:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return PathNaming.from_config(config, repo_root=None)


def x_build__mutmut_3(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> PathNaming:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return PathNaming.from_config(repo_root=repo_root)


def x_build__mutmut_4(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> PathNaming:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return PathNaming.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(PathNaming, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(PathNaming, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(PathNaming, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(PathNaming, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
