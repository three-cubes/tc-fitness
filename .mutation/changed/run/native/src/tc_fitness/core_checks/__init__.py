"""CORE check modules — the canonical fitness checks every repo INHERITS.

The v0.6.0 promotion (interrogation wss0rcfdr): ~45 checks that every Three
Cubes repo would otherwise reimplement become ENGINE CORE, so a consumer
INHERITS them via its catalogue instead of porting Python. Each CORE check is
a single module under this package exposing:

* a :class:`tc_fitness.fitness_rule.FitnessRule` subclass (the detector), and
* a ``main(argv=None) -> int`` entry point that runs the rule.

The CORE-check-module convention
================================

**Location.** One module per check at
``src/tc_fitness/core_checks/<canonical-name>.py`` (canonical name in
``snake_case``; the rule's ``name`` attribute uses the same name in
``kebab-case`` for findings). Tests live at
``tests/core_checks/test_<canonical-name>.py``.

**Module shape.** Copy the exemplar (:mod:`tc_fitness.core_checks.no_duplicate_string`):

.. code-block:: python

    class MyRule(FitnessRule):
        name = "my-rule"
        remediation = REMEDIATION        # built with tc_fitness.remediation(...)
        extensions = (".py",)            # repo-NEUTRAL default; roots come from config

        def file_has_violation(self, path: Path) -> bool:
            ...

    def build(config, repo_root=None) -> MyRule:
        return MyRule.from_config(config, repo_root=repo_root)

    def main(argv=None) -> int:
        return run_core_check(MyRule, argv)

**Repo-agnostic.** A CORE module contains ZERO repo strings — no ``kairix`` /
``taz`` / ``kata`` paths, globs, or thresholds. Everything repo-specific
(``roots``, ``extensions``, thresholds)
arrives through the consumer's ``[tool.tc_fitness]`` catalogue entry and is
applied via :meth:`FitnessRule.from_config`.

**The catalogue-entry shape a consumer writes.** To bind a CORE check, a
consumer adds a row to its catalogue (``tuple[RuleEntry, ...]``) AND a config
block keyed by the check name. The ``RuleEntry`` points at the CORE module via
its ``check`` field using the ``core:`` namespace:

.. code-block:: python

    # in the consumer's catalogue.py
    RuleEntry(
        id="no-duplicate-string",
        gate="no-duplicate-string",
        check="core:no_duplicate_string",    # resolves to tc_fitness.core_checks.no_duplicate_string
        category="maintainability",
        summary="No string literal duplicated 3+ times in one module.",
    )

.. code-block:: toml

    # in the consumer's pyproject.toml [tool.tc_fitness]
    [tool.tc_fitness.core_checks.no_duplicate_string]
    roots = ["scripts", "tools", "src"]
    extensions = [".py"]
    min_length = 10        # rule-specific knob the subclass reads from config
    min_occurrences = 3

The engine resolves the ``core:<module>`` check to
``tc_fitness.core_checks.<module>``, calls its ``build(config, repo_root=...)``
with the matching config block, and runs the returned rule. A consumer pinned
to ``@v0.5.0`` that never adds a ``core:`` row is unaffected (purely additive).

**The shared entry-point helper.** :func:`run_core_check` gives every CORE
module an identical ``main()`` that parses the optional ``--repo-root``, so no
module re-implements argv handling.
"""

from __future__ import annotations

import argparse
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tc_fitness.fitness_rule import FitnessRule


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x_run_core_check__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_run_core_check__mutmut)
def run_core_check(
    rule_cls: type[FitnessRule],
    argv: list[str] | None = None,
    *,
    config: Mapping[str, Any] | None = None,
) -> int:
    """Shared ``main()`` body for a CORE check module.

    Parses the universal ``--repo-root PATH`` flag to gate a tree other than the CWD (tests / monorepo
      sub-trees).

    ``config`` is the consumer's config block for this check (from
    ``[tool.tc_fitness]``); when ``None`` the rule's class-attribute defaults
    apply. Returns the rule's exit code (or ``0`` after establishing).
    """
    parser = argparse.ArgumentParser(prog=rule_cls.name)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="repo root to scan (default: current working directory).",
    )
    args = parser.parse_args(argv)

    cfg: Mapping[str, Any] = config if config is not None else {}
    rule = rule_cls.from_config(cfg, repo_root=args.repo_root)

    return rule.run()


def x_run_core_check__mutmut_orig(
    rule_cls: type[FitnessRule],
    argv: list[str] | None = None,
    *,
    config: Mapping[str, Any] | None = None,
) -> int:
    """Shared ``main()`` body for a CORE check module.

    Parses the universal ``--repo-root PATH`` flag to gate a tree other than the CWD (tests / monorepo
      sub-trees).

    ``config`` is the consumer's config block for this check (from
    ``[tool.tc_fitness]``); when ``None`` the rule's class-attribute defaults
    apply. Returns the rule's exit code (or ``0`` after establishing).
    """
    parser = argparse.ArgumentParser(prog=rule_cls.name)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="repo root to scan (default: current working directory).",
    )
    args = parser.parse_args(argv)

    cfg: Mapping[str, Any] = config if config is not None else {}
    rule = rule_cls.from_config(cfg, repo_root=args.repo_root)

    return rule.run()


def x_run_core_check__mutmut_1(
    rule_cls: type[FitnessRule],
    argv: list[str] | None = None,
    *,
    config: Mapping[str, Any] | None = None,
) -> int:
    """Shared ``main()`` body for a CORE check module.

    Parses the universal ``--repo-root PATH`` flag to gate a tree other than the CWD (tests / monorepo
      sub-trees).

    ``config`` is the consumer's config block for this check (from
    ``[tool.tc_fitness]``); when ``None`` the rule's class-attribute defaults
    apply. Returns the rule's exit code (or ``0`` after establishing).
    """
    parser = None
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="repo root to scan (default: current working directory).",
    )
    args = parser.parse_args(argv)

    cfg: Mapping[str, Any] = config if config is not None else {}
    rule = rule_cls.from_config(cfg, repo_root=args.repo_root)

    return rule.run()


def x_run_core_check__mutmut_2(
    rule_cls: type[FitnessRule],
    argv: list[str] | None = None,
    *,
    config: Mapping[str, Any] | None = None,
) -> int:
    """Shared ``main()`` body for a CORE check module.

    Parses the universal ``--repo-root PATH`` flag to gate a tree other than the CWD (tests / monorepo
      sub-trees).

    ``config`` is the consumer's config block for this check (from
    ``[tool.tc_fitness]``); when ``None`` the rule's class-attribute defaults
    apply. Returns the rule's exit code (or ``0`` after establishing).
    """
    parser = argparse.ArgumentParser(prog=None)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="repo root to scan (default: current working directory).",
    )
    args = parser.parse_args(argv)

    cfg: Mapping[str, Any] = config if config is not None else {}
    rule = rule_cls.from_config(cfg, repo_root=args.repo_root)

    return rule.run()


def x_run_core_check__mutmut_3(
    rule_cls: type[FitnessRule],
    argv: list[str] | None = None,
    *,
    config: Mapping[str, Any] | None = None,
) -> int:
    """Shared ``main()`` body for a CORE check module.

    Parses the universal ``--repo-root PATH`` flag to gate a tree other than the CWD (tests / monorepo
      sub-trees).

    ``config`` is the consumer's config block for this check (from
    ``[tool.tc_fitness]``); when ``None`` the rule's class-attribute defaults
    apply. Returns the rule's exit code (or ``0`` after establishing).
    """
    parser = argparse.ArgumentParser(prog=rule_cls.name)
    parser.add_argument(
        None,
        type=Path,
        default=None,
        help="repo root to scan (default: current working directory).",
    )
    args = parser.parse_args(argv)

    cfg: Mapping[str, Any] = config if config is not None else {}
    rule = rule_cls.from_config(cfg, repo_root=args.repo_root)

    return rule.run()


def x_run_core_check__mutmut_4(
    rule_cls: type[FitnessRule],
    argv: list[str] | None = None,
    *,
    config: Mapping[str, Any] | None = None,
) -> int:
    """Shared ``main()`` body for a CORE check module.

    Parses the universal ``--repo-root PATH`` flag to gate a tree other than the CWD (tests / monorepo
      sub-trees).

    ``config`` is the consumer's config block for this check (from
    ``[tool.tc_fitness]``); when ``None`` the rule's class-attribute defaults
    apply. Returns the rule's exit code (or ``0`` after establishing).
    """
    parser = argparse.ArgumentParser(prog=rule_cls.name)
    parser.add_argument(
        "--repo-root",
        type=None,
        default=None,
        help="repo root to scan (default: current working directory).",
    )
    args = parser.parse_args(argv)

    cfg: Mapping[str, Any] = config if config is not None else {}
    rule = rule_cls.from_config(cfg, repo_root=args.repo_root)

    return rule.run()


def x_run_core_check__mutmut_5(
    rule_cls: type[FitnessRule],
    argv: list[str] | None = None,
    *,
    config: Mapping[str, Any] | None = None,
) -> int:
    """Shared ``main()`` body for a CORE check module.

    Parses the universal ``--repo-root PATH`` flag to gate a tree other than the CWD (tests / monorepo
      sub-trees).

    ``config`` is the consumer's config block for this check (from
    ``[tool.tc_fitness]``); when ``None`` the rule's class-attribute defaults
    apply. Returns the rule's exit code (or ``0`` after establishing).
    """
    parser = argparse.ArgumentParser(prog=rule_cls.name)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help=None,
    )
    args = parser.parse_args(argv)

    cfg: Mapping[str, Any] = config if config is not None else {}
    rule = rule_cls.from_config(cfg, repo_root=args.repo_root)

    return rule.run()


def x_run_core_check__mutmut_6(
    rule_cls: type[FitnessRule],
    argv: list[str] | None = None,
    *,
    config: Mapping[str, Any] | None = None,
) -> int:
    """Shared ``main()`` body for a CORE check module.

    Parses the universal ``--repo-root PATH`` flag to gate a tree other than the CWD (tests / monorepo
      sub-trees).

    ``config`` is the consumer's config block for this check (from
    ``[tool.tc_fitness]``); when ``None`` the rule's class-attribute defaults
    apply. Returns the rule's exit code (or ``0`` after establishing).
    """
    parser = argparse.ArgumentParser(prog=rule_cls.name)
    parser.add_argument(
        type=Path,
        default=None,
        help="repo root to scan (default: current working directory).",
    )
    args = parser.parse_args(argv)

    cfg: Mapping[str, Any] = config if config is not None else {}
    rule = rule_cls.from_config(cfg, repo_root=args.repo_root)

    return rule.run()


def x_run_core_check__mutmut_7(
    rule_cls: type[FitnessRule],
    argv: list[str] | None = None,
    *,
    config: Mapping[str, Any] | None = None,
) -> int:
    """Shared ``main()`` body for a CORE check module.

    Parses the universal ``--repo-root PATH`` flag to gate a tree other than the CWD (tests / monorepo
      sub-trees).

    ``config`` is the consumer's config block for this check (from
    ``[tool.tc_fitness]``); when ``None`` the rule's class-attribute defaults
    apply. Returns the rule's exit code (or ``0`` after establishing).
    """
    parser = argparse.ArgumentParser(prog=rule_cls.name)
    parser.add_argument(
        "--repo-root",
        default=None,
        help="repo root to scan (default: current working directory).",
    )
    args = parser.parse_args(argv)

    cfg: Mapping[str, Any] = config if config is not None else {}
    rule = rule_cls.from_config(cfg, repo_root=args.repo_root)

    return rule.run()


def x_run_core_check__mutmut_8(
    rule_cls: type[FitnessRule],
    argv: list[str] | None = None,
    *,
    config: Mapping[str, Any] | None = None,
) -> int:
    """Shared ``main()`` body for a CORE check module.

    Parses the universal ``--repo-root PATH`` flag to gate a tree other than the CWD (tests / monorepo
      sub-trees).

    ``config`` is the consumer's config block for this check (from
    ``[tool.tc_fitness]``); when ``None`` the rule's class-attribute defaults
    apply. Returns the rule's exit code (or ``0`` after establishing).
    """
    parser = argparse.ArgumentParser(prog=rule_cls.name)
    parser.add_argument(
        "--repo-root",
        type=Path,
        help="repo root to scan (default: current working directory).",
    )
    args = parser.parse_args(argv)

    cfg: Mapping[str, Any] = config if config is not None else {}
    rule = rule_cls.from_config(cfg, repo_root=args.repo_root)

    return rule.run()


def x_run_core_check__mutmut_9(
    rule_cls: type[FitnessRule],
    argv: list[str] | None = None,
    *,
    config: Mapping[str, Any] | None = None,
) -> int:
    """Shared ``main()`` body for a CORE check module.

    Parses the universal ``--repo-root PATH`` flag to gate a tree other than the CWD (tests / monorepo
      sub-trees).

    ``config`` is the consumer's config block for this check (from
    ``[tool.tc_fitness]``); when ``None`` the rule's class-attribute defaults
    apply. Returns the rule's exit code (or ``0`` after establishing).
    """
    parser = argparse.ArgumentParser(prog=rule_cls.name)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        )
    args = parser.parse_args(argv)

    cfg: Mapping[str, Any] = config if config is not None else {}
    rule = rule_cls.from_config(cfg, repo_root=args.repo_root)

    return rule.run()


def x_run_core_check__mutmut_10(
    rule_cls: type[FitnessRule],
    argv: list[str] | None = None,
    *,
    config: Mapping[str, Any] | None = None,
) -> int:
    """Shared ``main()`` body for a CORE check module.

    Parses the universal ``--repo-root PATH`` flag to gate a tree other than the CWD (tests / monorepo
      sub-trees).

    ``config`` is the consumer's config block for this check (from
    ``[tool.tc_fitness]``); when ``None`` the rule's class-attribute defaults
    apply. Returns the rule's exit code (or ``0`` after establishing).
    """
    parser = argparse.ArgumentParser(prog=rule_cls.name)
    parser.add_argument(
        "XX--repo-rootXX",
        type=Path,
        default=None,
        help="repo root to scan (default: current working directory).",
    )
    args = parser.parse_args(argv)

    cfg: Mapping[str, Any] = config if config is not None else {}
    rule = rule_cls.from_config(cfg, repo_root=args.repo_root)

    return rule.run()


def x_run_core_check__mutmut_11(
    rule_cls: type[FitnessRule],
    argv: list[str] | None = None,
    *,
    config: Mapping[str, Any] | None = None,
) -> int:
    """Shared ``main()`` body for a CORE check module.

    Parses the universal ``--repo-root PATH`` flag to gate a tree other than the CWD (tests / monorepo
      sub-trees).

    ``config`` is the consumer's config block for this check (from
    ``[tool.tc_fitness]``); when ``None`` the rule's class-attribute defaults
    apply. Returns the rule's exit code (or ``0`` after establishing).
    """
    parser = argparse.ArgumentParser(prog=rule_cls.name)
    parser.add_argument(
        "--REPO-ROOT",
        type=Path,
        default=None,
        help="repo root to scan (default: current working directory).",
    )
    args = parser.parse_args(argv)

    cfg: Mapping[str, Any] = config if config is not None else {}
    rule = rule_cls.from_config(cfg, repo_root=args.repo_root)

    return rule.run()


def x_run_core_check__mutmut_12(
    rule_cls: type[FitnessRule],
    argv: list[str] | None = None,
    *,
    config: Mapping[str, Any] | None = None,
) -> int:
    """Shared ``main()`` body for a CORE check module.

    Parses the universal ``--repo-root PATH`` flag to gate a tree other than the CWD (tests / monorepo
      sub-trees).

    ``config`` is the consumer's config block for this check (from
    ``[tool.tc_fitness]``); when ``None`` the rule's class-attribute defaults
    apply. Returns the rule's exit code (or ``0`` after establishing).
    """
    parser = argparse.ArgumentParser(prog=rule_cls.name)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="XXrepo root to scan (default: current working directory).XX",
    )
    args = parser.parse_args(argv)

    cfg: Mapping[str, Any] = config if config is not None else {}
    rule = rule_cls.from_config(cfg, repo_root=args.repo_root)

    return rule.run()


def x_run_core_check__mutmut_13(
    rule_cls: type[FitnessRule],
    argv: list[str] | None = None,
    *,
    config: Mapping[str, Any] | None = None,
) -> int:
    """Shared ``main()`` body for a CORE check module.

    Parses the universal ``--repo-root PATH`` flag to gate a tree other than the CWD (tests / monorepo
      sub-trees).

    ``config`` is the consumer's config block for this check (from
    ``[tool.tc_fitness]``); when ``None`` the rule's class-attribute defaults
    apply. Returns the rule's exit code (or ``0`` after establishing).
    """
    parser = argparse.ArgumentParser(prog=rule_cls.name)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="REPO ROOT TO SCAN (DEFAULT: CURRENT WORKING DIRECTORY).",
    )
    args = parser.parse_args(argv)

    cfg: Mapping[str, Any] = config if config is not None else {}
    rule = rule_cls.from_config(cfg, repo_root=args.repo_root)

    return rule.run()


def x_run_core_check__mutmut_14(
    rule_cls: type[FitnessRule],
    argv: list[str] | None = None,
    *,
    config: Mapping[str, Any] | None = None,
) -> int:
    """Shared ``main()`` body for a CORE check module.

    Parses the universal ``--repo-root PATH`` flag to gate a tree other than the CWD (tests / monorepo
      sub-trees).

    ``config`` is the consumer's config block for this check (from
    ``[tool.tc_fitness]``); when ``None`` the rule's class-attribute defaults
    apply. Returns the rule's exit code (or ``0`` after establishing).
    """
    parser = argparse.ArgumentParser(prog=rule_cls.name)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="repo root to scan (default: current working directory).",
    )
    args = None

    cfg: Mapping[str, Any] = config if config is not None else {}
    rule = rule_cls.from_config(cfg, repo_root=args.repo_root)

    return rule.run()


def x_run_core_check__mutmut_15(
    rule_cls: type[FitnessRule],
    argv: list[str] | None = None,
    *,
    config: Mapping[str, Any] | None = None,
) -> int:
    """Shared ``main()`` body for a CORE check module.

    Parses the universal ``--repo-root PATH`` flag to gate a tree other than the CWD (tests / monorepo
      sub-trees).

    ``config`` is the consumer's config block for this check (from
    ``[tool.tc_fitness]``); when ``None`` the rule's class-attribute defaults
    apply. Returns the rule's exit code (or ``0`` after establishing).
    """
    parser = argparse.ArgumentParser(prog=rule_cls.name)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="repo root to scan (default: current working directory).",
    )
    args = parser.parse_args(None)

    cfg: Mapping[str, Any] = config if config is not None else {}
    rule = rule_cls.from_config(cfg, repo_root=args.repo_root)

    return rule.run()


def x_run_core_check__mutmut_16(
    rule_cls: type[FitnessRule],
    argv: list[str] | None = None,
    *,
    config: Mapping[str, Any] | None = None,
) -> int:
    """Shared ``main()`` body for a CORE check module.

    Parses the universal ``--repo-root PATH`` flag to gate a tree other than the CWD (tests / monorepo
      sub-trees).

    ``config`` is the consumer's config block for this check (from
    ``[tool.tc_fitness]``); when ``None`` the rule's class-attribute defaults
    apply. Returns the rule's exit code (or ``0`` after establishing).
    """
    parser = argparse.ArgumentParser(prog=rule_cls.name)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="repo root to scan (default: current working directory).",
    )
    args = parser.parse_args(argv)

    cfg: Mapping[str, Any] = None
    rule = rule_cls.from_config(cfg, repo_root=args.repo_root)

    return rule.run()


def x_run_core_check__mutmut_17(
    rule_cls: type[FitnessRule],
    argv: list[str] | None = None,
    *,
    config: Mapping[str, Any] | None = None,
) -> int:
    """Shared ``main()`` body for a CORE check module.

    Parses the universal ``--repo-root PATH`` flag to gate a tree other than the CWD (tests / monorepo
      sub-trees).

    ``config`` is the consumer's config block for this check (from
    ``[tool.tc_fitness]``); when ``None`` the rule's class-attribute defaults
    apply. Returns the rule's exit code (or ``0`` after establishing).
    """
    parser = argparse.ArgumentParser(prog=rule_cls.name)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="repo root to scan (default: current working directory).",
    )
    args = parser.parse_args(argv)

    cfg: Mapping[str, Any] = config if config is None else {}
    rule = rule_cls.from_config(cfg, repo_root=args.repo_root)

    return rule.run()


def x_run_core_check__mutmut_18(
    rule_cls: type[FitnessRule],
    argv: list[str] | None = None,
    *,
    config: Mapping[str, Any] | None = None,
) -> int:
    """Shared ``main()`` body for a CORE check module.

    Parses the universal ``--repo-root PATH`` flag to gate a tree other than the CWD (tests / monorepo
      sub-trees).

    ``config`` is the consumer's config block for this check (from
    ``[tool.tc_fitness]``); when ``None`` the rule's class-attribute defaults
    apply. Returns the rule's exit code (or ``0`` after establishing).
    """
    parser = argparse.ArgumentParser(prog=rule_cls.name)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="repo root to scan (default: current working directory).",
    )
    args = parser.parse_args(argv)

    cfg: Mapping[str, Any] = config if config is not None else {}
    rule = None

    return rule.run()


def x_run_core_check__mutmut_19(
    rule_cls: type[FitnessRule],
    argv: list[str] | None = None,
    *,
    config: Mapping[str, Any] | None = None,
) -> int:
    """Shared ``main()`` body for a CORE check module.

    Parses the universal ``--repo-root PATH`` flag to gate a tree other than the CWD (tests / monorepo
      sub-trees).

    ``config`` is the consumer's config block for this check (from
    ``[tool.tc_fitness]``); when ``None`` the rule's class-attribute defaults
    apply. Returns the rule's exit code (or ``0`` after establishing).
    """
    parser = argparse.ArgumentParser(prog=rule_cls.name)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="repo root to scan (default: current working directory).",
    )
    args = parser.parse_args(argv)

    cfg: Mapping[str, Any] = config if config is not None else {}
    rule = rule_cls.from_config(None, repo_root=args.repo_root)

    return rule.run()


def x_run_core_check__mutmut_20(
    rule_cls: type[FitnessRule],
    argv: list[str] | None = None,
    *,
    config: Mapping[str, Any] | None = None,
) -> int:
    """Shared ``main()`` body for a CORE check module.

    Parses the universal ``--repo-root PATH`` flag to gate a tree other than the CWD (tests / monorepo
      sub-trees).

    ``config`` is the consumer's config block for this check (from
    ``[tool.tc_fitness]``); when ``None`` the rule's class-attribute defaults
    apply. Returns the rule's exit code (or ``0`` after establishing).
    """
    parser = argparse.ArgumentParser(prog=rule_cls.name)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="repo root to scan (default: current working directory).",
    )
    args = parser.parse_args(argv)

    cfg: Mapping[str, Any] = config if config is not None else {}
    rule = rule_cls.from_config(cfg, repo_root=None)

    return rule.run()


def x_run_core_check__mutmut_21(
    rule_cls: type[FitnessRule],
    argv: list[str] | None = None,
    *,
    config: Mapping[str, Any] | None = None,
) -> int:
    """Shared ``main()`` body for a CORE check module.

    Parses the universal ``--repo-root PATH`` flag to gate a tree other than the CWD (tests / monorepo
      sub-trees).

    ``config`` is the consumer's config block for this check (from
    ``[tool.tc_fitness]``); when ``None`` the rule's class-attribute defaults
    apply. Returns the rule's exit code (or ``0`` after establishing).
    """
    parser = argparse.ArgumentParser(prog=rule_cls.name)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="repo root to scan (default: current working directory).",
    )
    args = parser.parse_args(argv)

    cfg: Mapping[str, Any] = config if config is not None else {}
    rule = rule_cls.from_config(repo_root=args.repo_root)

    return rule.run()


def x_run_core_check__mutmut_22(
    rule_cls: type[FitnessRule],
    argv: list[str] | None = None,
    *,
    config: Mapping[str, Any] | None = None,
) -> int:
    """Shared ``main()`` body for a CORE check module.

    Parses the universal ``--repo-root PATH`` flag to gate a tree other than the CWD (tests / monorepo
      sub-trees).

    ``config`` is the consumer's config block for this check (from
    ``[tool.tc_fitness]``); when ``None`` the rule's class-attribute defaults
    apply. Returns the rule's exit code (or ``0`` after establishing).
    """
    parser = argparse.ArgumentParser(prog=rule_cls.name)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="repo root to scan (default: current working directory).",
    )
    args = parser.parse_args(argv)

    cfg: Mapping[str, Any] = config if config is not None else {}
    rule = rule_cls.from_config(cfg, )

    return rule.run()

mutants_x_run_core_check__mutmut['_mutmut_orig'] = x_run_core_check__mutmut_orig # type: ignore # mutmut generated
mutants_x_run_core_check__mutmut['x_run_core_check__mutmut_1'] = x_run_core_check__mutmut_1 # type: ignore # mutmut generated
mutants_x_run_core_check__mutmut['x_run_core_check__mutmut_2'] = x_run_core_check__mutmut_2 # type: ignore # mutmut generated
mutants_x_run_core_check__mutmut['x_run_core_check__mutmut_3'] = x_run_core_check__mutmut_3 # type: ignore # mutmut generated
mutants_x_run_core_check__mutmut['x_run_core_check__mutmut_4'] = x_run_core_check__mutmut_4 # type: ignore # mutmut generated
mutants_x_run_core_check__mutmut['x_run_core_check__mutmut_5'] = x_run_core_check__mutmut_5 # type: ignore # mutmut generated
mutants_x_run_core_check__mutmut['x_run_core_check__mutmut_6'] = x_run_core_check__mutmut_6 # type: ignore # mutmut generated
mutants_x_run_core_check__mutmut['x_run_core_check__mutmut_7'] = x_run_core_check__mutmut_7 # type: ignore # mutmut generated
mutants_x_run_core_check__mutmut['x_run_core_check__mutmut_8'] = x_run_core_check__mutmut_8 # type: ignore # mutmut generated
mutants_x_run_core_check__mutmut['x_run_core_check__mutmut_9'] = x_run_core_check__mutmut_9 # type: ignore # mutmut generated
mutants_x_run_core_check__mutmut['x_run_core_check__mutmut_10'] = x_run_core_check__mutmut_10 # type: ignore # mutmut generated
mutants_x_run_core_check__mutmut['x_run_core_check__mutmut_11'] = x_run_core_check__mutmut_11 # type: ignore # mutmut generated
mutants_x_run_core_check__mutmut['x_run_core_check__mutmut_12'] = x_run_core_check__mutmut_12 # type: ignore # mutmut generated
mutants_x_run_core_check__mutmut['x_run_core_check__mutmut_13'] = x_run_core_check__mutmut_13 # type: ignore # mutmut generated
mutants_x_run_core_check__mutmut['x_run_core_check__mutmut_14'] = x_run_core_check__mutmut_14 # type: ignore # mutmut generated
mutants_x_run_core_check__mutmut['x_run_core_check__mutmut_15'] = x_run_core_check__mutmut_15 # type: ignore # mutmut generated
mutants_x_run_core_check__mutmut['x_run_core_check__mutmut_16'] = x_run_core_check__mutmut_16 # type: ignore # mutmut generated
mutants_x_run_core_check__mutmut['x_run_core_check__mutmut_17'] = x_run_core_check__mutmut_17 # type: ignore # mutmut generated
mutants_x_run_core_check__mutmut['x_run_core_check__mutmut_18'] = x_run_core_check__mutmut_18 # type: ignore # mutmut generated
mutants_x_run_core_check__mutmut['x_run_core_check__mutmut_19'] = x_run_core_check__mutmut_19 # type: ignore # mutmut generated
mutants_x_run_core_check__mutmut['x_run_core_check__mutmut_20'] = x_run_core_check__mutmut_20 # type: ignore # mutmut generated
mutants_x_run_core_check__mutmut['x_run_core_check__mutmut_21'] = x_run_core_check__mutmut_21 # type: ignore # mutmut generated
mutants_x_run_core_check__mutmut['x_run_core_check__mutmut_22'] = x_run_core_check__mutmut_22 # type: ignore # mutmut generated


# ===========================================================================
# The engine CORE-check registry — the single catalogue of shippable checks
# ===========================================================================
#
# ``CORE_CHECKS`` is the canonical, hand-maintained list of every CORE check
# the engine ships, named in the consumer-facing ``core:<module>`` namespace.
# A consumer binds a subset of these from its own catalogue; the engine
# guarantees (via :func:`core_check_consistency`, exercised in the engine test
# suite) that this registry and the modules ON DISK agree BIDIRECTIONALLY —
# no registry id without a module, no module without a registry id. That is the
# engine-side expression of the F92 ``catalogue_check_consistency`` keystone:
# the catalogue can never silently drift from the checks it claims to ship.
#
# Adding a CORE check is a two-line edit: drop the module under this package and
# add its ``core:<module>`` id here. The consistency test fails otherwise,
# pointing at the orphan module or the dangling id.
CORE_CHECKS: tuple[str, ...] = (
    "core:actionable_feedback",
    "core:adr_number_unique",
    "core:behavioural_evidence",
    "core:bicep_arm_lint",
    "core:canonical_commit_identity",
    "core:checkov_iac_security",
    "core:ci_consumes_shared_gate",
    "core:ci_fanin_parity",
    "core:ci_silencers_have_rationale",
    "core:cognitive_complexity",
    "core:contract_change_has_test",
    "core:coverage_floor",
    "core:coverage_includes_branches",
    "core:deterministic_tests",
    "core:empty_body_intent",
    "core:engine_version_floor",
    "core:every_test_has_tier_marker",
    "core:harness_canon_reference",
    "core:integrity_state_predicate",
    "core:license_present",
    "core:mutation_survival_ratchet",
    "core:new_code_coverage",
    "core:no_commented_out_code",
    "core:no_duplicate_string",
    "core:no_env_monkeypatch",
    "core:no_hardcoded_repo_paths",
    "core:no_internal_monkeypatch",
    "core:no_internal_patches",
    "core:no_internal_patches_ts",
    "core:no_language_suffix_in_package_names",
    "core:no_llm_attribution",
    "core:no_logging_secrets",
    "core:no_noop_test_scripts",
    "core:no_production_suppressions",
    "core:no_real_names",
    "core:no_test_doubles_in_runtime_tiers",
    "core:no_test_imports_in_prod",
    "core:no_test_only_kwargs",
    "core:osv_scanner_sca",
    "core:path_naming",
    "core:pattern_chokepoint",
    "core:posix_path_serialisation",
    "core:readme_resolver_coverage",
    "core:runtime_evidence_contract",
    "core:runtime_filesystem_contract",
    "core:schema_conformance",
    "core:script_help_smoke",
    "core:shellcheck_disable_with_reason",
    "core:sonar_ignore_rationale",
    "core:suppressions_have_rationale",
    "core:test_skip_rationale",
    "core:untrusted_automation_boundary",
    "core:unused_params_named",
)

_CORE_NAMESPACE = "core:"
mutants_x_discover_core_check_modules__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_discover_core_check_modules__mutmut)
def discover_core_check_modules() -> tuple[str, ...]:
    """Enumerate the CORE-check modules present on disk, ``core:``-namespaced.

    Walks this package directory for ``<module>.py`` files (excluding dunder
    modules) and returns each as a ``core:<module>`` id — the same namespace
    :data:`CORE_CHECKS` declares. The discovery source of truth for the
    bidirectional :func:`core_check_consistency` reconciliation.
    """
    here = Path(__file__).parent
    out: list[str] = []
    for path in sorted(here.glob("*.py")):
        stem = path.stem
        if stem.startswith("_"):
            continue
        out.append(f"{_CORE_NAMESPACE}{stem}")
    return tuple(out)


def x_discover_core_check_modules__mutmut_orig() -> tuple[str, ...]:
    """Enumerate the CORE-check modules present on disk, ``core:``-namespaced.

    Walks this package directory for ``<module>.py`` files (excluding dunder
    modules) and returns each as a ``core:<module>`` id — the same namespace
    :data:`CORE_CHECKS` declares. The discovery source of truth for the
    bidirectional :func:`core_check_consistency` reconciliation.
    """
    here = Path(__file__).parent
    out: list[str] = []
    for path in sorted(here.glob("*.py")):
        stem = path.stem
        if stem.startswith("_"):
            continue
        out.append(f"{_CORE_NAMESPACE}{stem}")
    return tuple(out)


def x_discover_core_check_modules__mutmut_1() -> tuple[str, ...]:
    """Enumerate the CORE-check modules present on disk, ``core:``-namespaced.

    Walks this package directory for ``<module>.py`` files (excluding dunder
    modules) and returns each as a ``core:<module>`` id — the same namespace
    :data:`CORE_CHECKS` declares. The discovery source of truth for the
    bidirectional :func:`core_check_consistency` reconciliation.
    """
    here = None
    out: list[str] = []
    for path in sorted(here.glob("*.py")):
        stem = path.stem
        if stem.startswith("_"):
            continue
        out.append(f"{_CORE_NAMESPACE}{stem}")
    return tuple(out)


def x_discover_core_check_modules__mutmut_2() -> tuple[str, ...]:
    """Enumerate the CORE-check modules present on disk, ``core:``-namespaced.

    Walks this package directory for ``<module>.py`` files (excluding dunder
    modules) and returns each as a ``core:<module>`` id — the same namespace
    :data:`CORE_CHECKS` declares. The discovery source of truth for the
    bidirectional :func:`core_check_consistency` reconciliation.
    """
    here = Path(None).parent
    out: list[str] = []
    for path in sorted(here.glob("*.py")):
        stem = path.stem
        if stem.startswith("_"):
            continue
        out.append(f"{_CORE_NAMESPACE}{stem}")
    return tuple(out)


def x_discover_core_check_modules__mutmut_3() -> tuple[str, ...]:
    """Enumerate the CORE-check modules present on disk, ``core:``-namespaced.

    Walks this package directory for ``<module>.py`` files (excluding dunder
    modules) and returns each as a ``core:<module>`` id — the same namespace
    :data:`CORE_CHECKS` declares. The discovery source of truth for the
    bidirectional :func:`core_check_consistency` reconciliation.
    """
    here = Path(__file__).parent
    out: list[str] = None
    for path in sorted(here.glob("*.py")):
        stem = path.stem
        if stem.startswith("_"):
            continue
        out.append(f"{_CORE_NAMESPACE}{stem}")
    return tuple(out)


def x_discover_core_check_modules__mutmut_4() -> tuple[str, ...]:
    """Enumerate the CORE-check modules present on disk, ``core:``-namespaced.

    Walks this package directory for ``<module>.py`` files (excluding dunder
    modules) and returns each as a ``core:<module>`` id — the same namespace
    :data:`CORE_CHECKS` declares. The discovery source of truth for the
    bidirectional :func:`core_check_consistency` reconciliation.
    """
    here = Path(__file__).parent
    out: list[str] = []
    for path in sorted(None):
        stem = path.stem
        if stem.startswith("_"):
            continue
        out.append(f"{_CORE_NAMESPACE}{stem}")
    return tuple(out)


def x_discover_core_check_modules__mutmut_5() -> tuple[str, ...]:
    """Enumerate the CORE-check modules present on disk, ``core:``-namespaced.

    Walks this package directory for ``<module>.py`` files (excluding dunder
    modules) and returns each as a ``core:<module>`` id — the same namespace
    :data:`CORE_CHECKS` declares. The discovery source of truth for the
    bidirectional :func:`core_check_consistency` reconciliation.
    """
    here = Path(__file__).parent
    out: list[str] = []
    for path in sorted(here.glob(None)):
        stem = path.stem
        if stem.startswith("_"):
            continue
        out.append(f"{_CORE_NAMESPACE}{stem}")
    return tuple(out)


def x_discover_core_check_modules__mutmut_6() -> tuple[str, ...]:
    """Enumerate the CORE-check modules present on disk, ``core:``-namespaced.

    Walks this package directory for ``<module>.py`` files (excluding dunder
    modules) and returns each as a ``core:<module>`` id — the same namespace
    :data:`CORE_CHECKS` declares. The discovery source of truth for the
    bidirectional :func:`core_check_consistency` reconciliation.
    """
    here = Path(__file__).parent
    out: list[str] = []
    for path in sorted(here.glob("XX*.pyXX")):
        stem = path.stem
        if stem.startswith("_"):
            continue
        out.append(f"{_CORE_NAMESPACE}{stem}")
    return tuple(out)


def x_discover_core_check_modules__mutmut_7() -> tuple[str, ...]:
    """Enumerate the CORE-check modules present on disk, ``core:``-namespaced.

    Walks this package directory for ``<module>.py`` files (excluding dunder
    modules) and returns each as a ``core:<module>`` id — the same namespace
    :data:`CORE_CHECKS` declares. The discovery source of truth for the
    bidirectional :func:`core_check_consistency` reconciliation.
    """
    here = Path(__file__).parent
    out: list[str] = []
    for path in sorted(here.glob("*.PY")):
        stem = path.stem
        if stem.startswith("_"):
            continue
        out.append(f"{_CORE_NAMESPACE}{stem}")
    return tuple(out)


def x_discover_core_check_modules__mutmut_8() -> tuple[str, ...]:
    """Enumerate the CORE-check modules present on disk, ``core:``-namespaced.

    Walks this package directory for ``<module>.py`` files (excluding dunder
    modules) and returns each as a ``core:<module>`` id — the same namespace
    :data:`CORE_CHECKS` declares. The discovery source of truth for the
    bidirectional :func:`core_check_consistency` reconciliation.
    """
    here = Path(__file__).parent
    out: list[str] = []
    for path in sorted(here.glob("*.py")):
        stem = None
        if stem.startswith("_"):
            continue
        out.append(f"{_CORE_NAMESPACE}{stem}")
    return tuple(out)


def x_discover_core_check_modules__mutmut_9() -> tuple[str, ...]:
    """Enumerate the CORE-check modules present on disk, ``core:``-namespaced.

    Walks this package directory for ``<module>.py`` files (excluding dunder
    modules) and returns each as a ``core:<module>`` id — the same namespace
    :data:`CORE_CHECKS` declares. The discovery source of truth for the
    bidirectional :func:`core_check_consistency` reconciliation.
    """
    here = Path(__file__).parent
    out: list[str] = []
    for path in sorted(here.glob("*.py")):
        stem = path.stem
        if stem.startswith(None):
            continue
        out.append(f"{_CORE_NAMESPACE}{stem}")
    return tuple(out)


def x_discover_core_check_modules__mutmut_10() -> tuple[str, ...]:
    """Enumerate the CORE-check modules present on disk, ``core:``-namespaced.

    Walks this package directory for ``<module>.py`` files (excluding dunder
    modules) and returns each as a ``core:<module>`` id — the same namespace
    :data:`CORE_CHECKS` declares. The discovery source of truth for the
    bidirectional :func:`core_check_consistency` reconciliation.
    """
    here = Path(__file__).parent
    out: list[str] = []
    for path in sorted(here.glob("*.py")):
        stem = path.stem
        if stem.startswith("XX_XX"):
            continue
        out.append(f"{_CORE_NAMESPACE}{stem}")
    return tuple(out)


def x_discover_core_check_modules__mutmut_11() -> tuple[str, ...]:
    """Enumerate the CORE-check modules present on disk, ``core:``-namespaced.

    Walks this package directory for ``<module>.py`` files (excluding dunder
    modules) and returns each as a ``core:<module>`` id — the same namespace
    :data:`CORE_CHECKS` declares. The discovery source of truth for the
    bidirectional :func:`core_check_consistency` reconciliation.
    """
    here = Path(__file__).parent
    out: list[str] = []
    for path in sorted(here.glob("*.py")):
        stem = path.stem
        if stem.startswith("_"):
            break
        out.append(f"{_CORE_NAMESPACE}{stem}")
    return tuple(out)


def x_discover_core_check_modules__mutmut_12() -> tuple[str, ...]:
    """Enumerate the CORE-check modules present on disk, ``core:``-namespaced.

    Walks this package directory for ``<module>.py`` files (excluding dunder
    modules) and returns each as a ``core:<module>`` id — the same namespace
    :data:`CORE_CHECKS` declares. The discovery source of truth for the
    bidirectional :func:`core_check_consistency` reconciliation.
    """
    here = Path(__file__).parent
    out: list[str] = []
    for path in sorted(here.glob("*.py")):
        stem = path.stem
        if stem.startswith("_"):
            continue
        out.append(None)
    return tuple(out)


def x_discover_core_check_modules__mutmut_13() -> tuple[str, ...]:
    """Enumerate the CORE-check modules present on disk, ``core:``-namespaced.

    Walks this package directory for ``<module>.py`` files (excluding dunder
    modules) and returns each as a ``core:<module>`` id — the same namespace
    :data:`CORE_CHECKS` declares. The discovery source of truth for the
    bidirectional :func:`core_check_consistency` reconciliation.
    """
    here = Path(__file__).parent
    out: list[str] = []
    for path in sorted(here.glob("*.py")):
        stem = path.stem
        if stem.startswith("_"):
            continue
        out.append(f"{_CORE_NAMESPACE}{stem}")
    return tuple(None)

mutants_x_discover_core_check_modules__mutmut['_mutmut_orig'] = x_discover_core_check_modules__mutmut_orig # type: ignore # mutmut generated
mutants_x_discover_core_check_modules__mutmut['x_discover_core_check_modules__mutmut_1'] = x_discover_core_check_modules__mutmut_1 # type: ignore # mutmut generated
mutants_x_discover_core_check_modules__mutmut['x_discover_core_check_modules__mutmut_2'] = x_discover_core_check_modules__mutmut_2 # type: ignore # mutmut generated
mutants_x_discover_core_check_modules__mutmut['x_discover_core_check_modules__mutmut_3'] = x_discover_core_check_modules__mutmut_3 # type: ignore # mutmut generated
mutants_x_discover_core_check_modules__mutmut['x_discover_core_check_modules__mutmut_4'] = x_discover_core_check_modules__mutmut_4 # type: ignore # mutmut generated
mutants_x_discover_core_check_modules__mutmut['x_discover_core_check_modules__mutmut_5'] = x_discover_core_check_modules__mutmut_5 # type: ignore # mutmut generated
mutants_x_discover_core_check_modules__mutmut['x_discover_core_check_modules__mutmut_6'] = x_discover_core_check_modules__mutmut_6 # type: ignore # mutmut generated
mutants_x_discover_core_check_modules__mutmut['x_discover_core_check_modules__mutmut_7'] = x_discover_core_check_modules__mutmut_7 # type: ignore # mutmut generated
mutants_x_discover_core_check_modules__mutmut['x_discover_core_check_modules__mutmut_8'] = x_discover_core_check_modules__mutmut_8 # type: ignore # mutmut generated
mutants_x_discover_core_check_modules__mutmut['x_discover_core_check_modules__mutmut_9'] = x_discover_core_check_modules__mutmut_9 # type: ignore # mutmut generated
mutants_x_discover_core_check_modules__mutmut['x_discover_core_check_modules__mutmut_10'] = x_discover_core_check_modules__mutmut_10 # type: ignore # mutmut generated
mutants_x_discover_core_check_modules__mutmut['x_discover_core_check_modules__mutmut_11'] = x_discover_core_check_modules__mutmut_11 # type: ignore # mutmut generated
mutants_x_discover_core_check_modules__mutmut['x_discover_core_check_modules__mutmut_12'] = x_discover_core_check_modules__mutmut_12 # type: ignore # mutmut generated
mutants_x_discover_core_check_modules__mutmut['x_discover_core_check_modules__mutmut_13'] = x_discover_core_check_modules__mutmut_13 # type: ignore # mutmut generated
mutants_x_core_check_consistency__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_core_check_consistency__mutmut)
def core_check_consistency() -> int:
    """Gate: :data:`CORE_CHECKS` ↔ on-disk modules agree bidirectionally.

    Reuses the engine keystone :func:`tc_fitness.catalogue_check_consistency`
    over the declared registry and the discovered modules, so a CORE module
    added without a registry id (orphan) OR a registry id with no module
    (dangling) FAILS. Returns ``0`` when consistent, ``1`` on drift.
    """
    from tc_fitness.keystone import catalogue_check_consistency
    from tc_fitness.lib import remediation as _remediation

    return catalogue_check_consistency(
        cataloged_check_ids=CORE_CHECKS,
        available_check_ids=discover_core_check_modules(),
        remediation=_remediation(
            fix=(
                "reconcile CORE_CHECKS (in tc_fitness.core_checks) with the modules "
                "on disk: add the missing core:<module> id for a new check module, "
                "or remove the dangling id for a module that no longer exists."
            ),
            nxt="re-run the engine test suite to confirm the registry is consistent.",
            run="python -c 'from tc_fitness.core_checks import core_check_consistency as c; raise SystemExit(c())'",
        ),
    )


def x_core_check_consistency__mutmut_orig() -> int:
    """Gate: :data:`CORE_CHECKS` ↔ on-disk modules agree bidirectionally.

    Reuses the engine keystone :func:`tc_fitness.catalogue_check_consistency`
    over the declared registry and the discovered modules, so a CORE module
    added without a registry id (orphan) OR a registry id with no module
    (dangling) FAILS. Returns ``0`` when consistent, ``1`` on drift.
    """
    from tc_fitness.keystone import catalogue_check_consistency
    from tc_fitness.lib import remediation as _remediation

    return catalogue_check_consistency(
        cataloged_check_ids=CORE_CHECKS,
        available_check_ids=discover_core_check_modules(),
        remediation=_remediation(
            fix=(
                "reconcile CORE_CHECKS (in tc_fitness.core_checks) with the modules "
                "on disk: add the missing core:<module> id for a new check module, "
                "or remove the dangling id for a module that no longer exists."
            ),
            nxt="re-run the engine test suite to confirm the registry is consistent.",
            run="python -c 'from tc_fitness.core_checks import core_check_consistency as c; raise SystemExit(c())'",
        ),
    )


def x_core_check_consistency__mutmut_1() -> int:
    """Gate: :data:`CORE_CHECKS` ↔ on-disk modules agree bidirectionally.

    Reuses the engine keystone :func:`tc_fitness.catalogue_check_consistency`
    over the declared registry and the discovered modules, so a CORE module
    added without a registry id (orphan) OR a registry id with no module
    (dangling) FAILS. Returns ``0`` when consistent, ``1`` on drift.
    """
    from tc_fitness.keystone import catalogue_check_consistency
    from tc_fitness.lib import remediation as _remediation

    return catalogue_check_consistency(
        cataloged_check_ids=None,
        available_check_ids=discover_core_check_modules(),
        remediation=_remediation(
            fix=(
                "reconcile CORE_CHECKS (in tc_fitness.core_checks) with the modules "
                "on disk: add the missing core:<module> id for a new check module, "
                "or remove the dangling id for a module that no longer exists."
            ),
            nxt="re-run the engine test suite to confirm the registry is consistent.",
            run="python -c 'from tc_fitness.core_checks import core_check_consistency as c; raise SystemExit(c())'",
        ),
    )


def x_core_check_consistency__mutmut_2() -> int:
    """Gate: :data:`CORE_CHECKS` ↔ on-disk modules agree bidirectionally.

    Reuses the engine keystone :func:`tc_fitness.catalogue_check_consistency`
    over the declared registry and the discovered modules, so a CORE module
    added without a registry id (orphan) OR a registry id with no module
    (dangling) FAILS. Returns ``0`` when consistent, ``1`` on drift.
    """
    from tc_fitness.keystone import catalogue_check_consistency
    from tc_fitness.lib import remediation as _remediation

    return catalogue_check_consistency(
        cataloged_check_ids=CORE_CHECKS,
        available_check_ids=None,
        remediation=_remediation(
            fix=(
                "reconcile CORE_CHECKS (in tc_fitness.core_checks) with the modules "
                "on disk: add the missing core:<module> id for a new check module, "
                "or remove the dangling id for a module that no longer exists."
            ),
            nxt="re-run the engine test suite to confirm the registry is consistent.",
            run="python -c 'from tc_fitness.core_checks import core_check_consistency as c; raise SystemExit(c())'",
        ),
    )


def x_core_check_consistency__mutmut_3() -> int:
    """Gate: :data:`CORE_CHECKS` ↔ on-disk modules agree bidirectionally.

    Reuses the engine keystone :func:`tc_fitness.catalogue_check_consistency`
    over the declared registry and the discovered modules, so a CORE module
    added without a registry id (orphan) OR a registry id with no module
    (dangling) FAILS. Returns ``0`` when consistent, ``1`` on drift.
    """
    from tc_fitness.keystone import catalogue_check_consistency
    from tc_fitness.lib import remediation as _remediation

    return catalogue_check_consistency(
        cataloged_check_ids=CORE_CHECKS,
        available_check_ids=discover_core_check_modules(),
        remediation=None,
    )


def x_core_check_consistency__mutmut_4() -> int:
    """Gate: :data:`CORE_CHECKS` ↔ on-disk modules agree bidirectionally.

    Reuses the engine keystone :func:`tc_fitness.catalogue_check_consistency`
    over the declared registry and the discovered modules, so a CORE module
    added without a registry id (orphan) OR a registry id with no module
    (dangling) FAILS. Returns ``0`` when consistent, ``1`` on drift.
    """
    from tc_fitness.keystone import catalogue_check_consistency
    from tc_fitness.lib import remediation as _remediation

    return catalogue_check_consistency(
        available_check_ids=discover_core_check_modules(),
        remediation=_remediation(
            fix=(
                "reconcile CORE_CHECKS (in tc_fitness.core_checks) with the modules "
                "on disk: add the missing core:<module> id for a new check module, "
                "or remove the dangling id for a module that no longer exists."
            ),
            nxt="re-run the engine test suite to confirm the registry is consistent.",
            run="python -c 'from tc_fitness.core_checks import core_check_consistency as c; raise SystemExit(c())'",
        ),
    )


def x_core_check_consistency__mutmut_5() -> int:
    """Gate: :data:`CORE_CHECKS` ↔ on-disk modules agree bidirectionally.

    Reuses the engine keystone :func:`tc_fitness.catalogue_check_consistency`
    over the declared registry and the discovered modules, so a CORE module
    added without a registry id (orphan) OR a registry id with no module
    (dangling) FAILS. Returns ``0`` when consistent, ``1`` on drift.
    """
    from tc_fitness.keystone import catalogue_check_consistency
    from tc_fitness.lib import remediation as _remediation

    return catalogue_check_consistency(
        cataloged_check_ids=CORE_CHECKS,
        remediation=_remediation(
            fix=(
                "reconcile CORE_CHECKS (in tc_fitness.core_checks) with the modules "
                "on disk: add the missing core:<module> id for a new check module, "
                "or remove the dangling id for a module that no longer exists."
            ),
            nxt="re-run the engine test suite to confirm the registry is consistent.",
            run="python -c 'from tc_fitness.core_checks import core_check_consistency as c; raise SystemExit(c())'",
        ),
    )


def x_core_check_consistency__mutmut_6() -> int:
    """Gate: :data:`CORE_CHECKS` ↔ on-disk modules agree bidirectionally.

    Reuses the engine keystone :func:`tc_fitness.catalogue_check_consistency`
    over the declared registry and the discovered modules, so a CORE module
    added without a registry id (orphan) OR a registry id with no module
    (dangling) FAILS. Returns ``0`` when consistent, ``1`` on drift.
    """
    from tc_fitness.keystone import catalogue_check_consistency
    from tc_fitness.lib import remediation as _remediation

    return catalogue_check_consistency(
        cataloged_check_ids=CORE_CHECKS,
        available_check_ids=discover_core_check_modules(),
        )


def x_core_check_consistency__mutmut_7() -> int:
    """Gate: :data:`CORE_CHECKS` ↔ on-disk modules agree bidirectionally.

    Reuses the engine keystone :func:`tc_fitness.catalogue_check_consistency`
    over the declared registry and the discovered modules, so a CORE module
    added without a registry id (orphan) OR a registry id with no module
    (dangling) FAILS. Returns ``0`` when consistent, ``1`` on drift.
    """
    from tc_fitness.keystone import catalogue_check_consistency
    from tc_fitness.lib import remediation as _remediation

    return catalogue_check_consistency(
        cataloged_check_ids=CORE_CHECKS,
        available_check_ids=discover_core_check_modules(),
        remediation=_remediation(
            fix=None,
            nxt="re-run the engine test suite to confirm the registry is consistent.",
            run="python -c 'from tc_fitness.core_checks import core_check_consistency as c; raise SystemExit(c())'",
        ),
    )


def x_core_check_consistency__mutmut_8() -> int:
    """Gate: :data:`CORE_CHECKS` ↔ on-disk modules agree bidirectionally.

    Reuses the engine keystone :func:`tc_fitness.catalogue_check_consistency`
    over the declared registry and the discovered modules, so a CORE module
    added without a registry id (orphan) OR a registry id with no module
    (dangling) FAILS. Returns ``0`` when consistent, ``1`` on drift.
    """
    from tc_fitness.keystone import catalogue_check_consistency
    from tc_fitness.lib import remediation as _remediation

    return catalogue_check_consistency(
        cataloged_check_ids=CORE_CHECKS,
        available_check_ids=discover_core_check_modules(),
        remediation=_remediation(
            fix=(
                "reconcile CORE_CHECKS (in tc_fitness.core_checks) with the modules "
                "on disk: add the missing core:<module> id for a new check module, "
                "or remove the dangling id for a module that no longer exists."
            ),
            nxt=None,
            run="python -c 'from tc_fitness.core_checks import core_check_consistency as c; raise SystemExit(c())'",
        ),
    )


def x_core_check_consistency__mutmut_9() -> int:
    """Gate: :data:`CORE_CHECKS` ↔ on-disk modules agree bidirectionally.

    Reuses the engine keystone :func:`tc_fitness.catalogue_check_consistency`
    over the declared registry and the discovered modules, so a CORE module
    added without a registry id (orphan) OR a registry id with no module
    (dangling) FAILS. Returns ``0`` when consistent, ``1`` on drift.
    """
    from tc_fitness.keystone import catalogue_check_consistency
    from tc_fitness.lib import remediation as _remediation

    return catalogue_check_consistency(
        cataloged_check_ids=CORE_CHECKS,
        available_check_ids=discover_core_check_modules(),
        remediation=_remediation(
            fix=(
                "reconcile CORE_CHECKS (in tc_fitness.core_checks) with the modules "
                "on disk: add the missing core:<module> id for a new check module, "
                "or remove the dangling id for a module that no longer exists."
            ),
            nxt="re-run the engine test suite to confirm the registry is consistent.",
            run=None,
        ),
    )


def x_core_check_consistency__mutmut_10() -> int:
    """Gate: :data:`CORE_CHECKS` ↔ on-disk modules agree bidirectionally.

    Reuses the engine keystone :func:`tc_fitness.catalogue_check_consistency`
    over the declared registry and the discovered modules, so a CORE module
    added without a registry id (orphan) OR a registry id with no module
    (dangling) FAILS. Returns ``0`` when consistent, ``1`` on drift.
    """
    from tc_fitness.keystone import catalogue_check_consistency
    from tc_fitness.lib import remediation as _remediation

    return catalogue_check_consistency(
        cataloged_check_ids=CORE_CHECKS,
        available_check_ids=discover_core_check_modules(),
        remediation=_remediation(
            nxt="re-run the engine test suite to confirm the registry is consistent.",
            run="python -c 'from tc_fitness.core_checks import core_check_consistency as c; raise SystemExit(c())'",
        ),
    )


def x_core_check_consistency__mutmut_11() -> int:
    """Gate: :data:`CORE_CHECKS` ↔ on-disk modules agree bidirectionally.

    Reuses the engine keystone :func:`tc_fitness.catalogue_check_consistency`
    over the declared registry and the discovered modules, so a CORE module
    added without a registry id (orphan) OR a registry id with no module
    (dangling) FAILS. Returns ``0`` when consistent, ``1`` on drift.
    """
    from tc_fitness.keystone import catalogue_check_consistency
    from tc_fitness.lib import remediation as _remediation

    return catalogue_check_consistency(
        cataloged_check_ids=CORE_CHECKS,
        available_check_ids=discover_core_check_modules(),
        remediation=_remediation(
            fix=(
                "reconcile CORE_CHECKS (in tc_fitness.core_checks) with the modules "
                "on disk: add the missing core:<module> id for a new check module, "
                "or remove the dangling id for a module that no longer exists."
            ),
            run="python -c 'from tc_fitness.core_checks import core_check_consistency as c; raise SystemExit(c())'",
        ),
    )


def x_core_check_consistency__mutmut_12() -> int:
    """Gate: :data:`CORE_CHECKS` ↔ on-disk modules agree bidirectionally.

    Reuses the engine keystone :func:`tc_fitness.catalogue_check_consistency`
    over the declared registry and the discovered modules, so a CORE module
    added without a registry id (orphan) OR a registry id with no module
    (dangling) FAILS. Returns ``0`` when consistent, ``1`` on drift.
    """
    from tc_fitness.keystone import catalogue_check_consistency
    from tc_fitness.lib import remediation as _remediation

    return catalogue_check_consistency(
        cataloged_check_ids=CORE_CHECKS,
        available_check_ids=discover_core_check_modules(),
        remediation=_remediation(
            fix=(
                "reconcile CORE_CHECKS (in tc_fitness.core_checks) with the modules "
                "on disk: add the missing core:<module> id for a new check module, "
                "or remove the dangling id for a module that no longer exists."
            ),
            nxt="re-run the engine test suite to confirm the registry is consistent.",
            ),
    )


def x_core_check_consistency__mutmut_13() -> int:
    """Gate: :data:`CORE_CHECKS` ↔ on-disk modules agree bidirectionally.

    Reuses the engine keystone :func:`tc_fitness.catalogue_check_consistency`
    over the declared registry and the discovered modules, so a CORE module
    added without a registry id (orphan) OR a registry id with no module
    (dangling) FAILS. Returns ``0`` when consistent, ``1`` on drift.
    """
    from tc_fitness.keystone import catalogue_check_consistency
    from tc_fitness.lib import remediation as _remediation

    return catalogue_check_consistency(
        cataloged_check_ids=CORE_CHECKS,
        available_check_ids=discover_core_check_modules(),
        remediation=_remediation(
            fix=(
                "XXreconcile CORE_CHECKS (in tc_fitness.core_checks) with the modules XX"
                "on disk: add the missing core:<module> id for a new check module, "
                "or remove the dangling id for a module that no longer exists."
            ),
            nxt="re-run the engine test suite to confirm the registry is consistent.",
            run="python -c 'from tc_fitness.core_checks import core_check_consistency as c; raise SystemExit(c())'",
        ),
    )


def x_core_check_consistency__mutmut_14() -> int:
    """Gate: :data:`CORE_CHECKS` ↔ on-disk modules agree bidirectionally.

    Reuses the engine keystone :func:`tc_fitness.catalogue_check_consistency`
    over the declared registry and the discovered modules, so a CORE module
    added without a registry id (orphan) OR a registry id with no module
    (dangling) FAILS. Returns ``0`` when consistent, ``1`` on drift.
    """
    from tc_fitness.keystone import catalogue_check_consistency
    from tc_fitness.lib import remediation as _remediation

    return catalogue_check_consistency(
        cataloged_check_ids=CORE_CHECKS,
        available_check_ids=discover_core_check_modules(),
        remediation=_remediation(
            fix=(
                "reconcile core_checks (in tc_fitness.core_checks) with the modules "
                "on disk: add the missing core:<module> id for a new check module, "
                "or remove the dangling id for a module that no longer exists."
            ),
            nxt="re-run the engine test suite to confirm the registry is consistent.",
            run="python -c 'from tc_fitness.core_checks import core_check_consistency as c; raise SystemExit(c())'",
        ),
    )


def x_core_check_consistency__mutmut_15() -> int:
    """Gate: :data:`CORE_CHECKS` ↔ on-disk modules agree bidirectionally.

    Reuses the engine keystone :func:`tc_fitness.catalogue_check_consistency`
    over the declared registry and the discovered modules, so a CORE module
    added without a registry id (orphan) OR a registry id with no module
    (dangling) FAILS. Returns ``0`` when consistent, ``1`` on drift.
    """
    from tc_fitness.keystone import catalogue_check_consistency
    from tc_fitness.lib import remediation as _remediation

    return catalogue_check_consistency(
        cataloged_check_ids=CORE_CHECKS,
        available_check_ids=discover_core_check_modules(),
        remediation=_remediation(
            fix=(
                "RECONCILE CORE_CHECKS (IN TC_FITNESS.CORE_CHECKS) WITH THE MODULES "
                "on disk: add the missing core:<module> id for a new check module, "
                "or remove the dangling id for a module that no longer exists."
            ),
            nxt="re-run the engine test suite to confirm the registry is consistent.",
            run="python -c 'from tc_fitness.core_checks import core_check_consistency as c; raise SystemExit(c())'",
        ),
    )


def x_core_check_consistency__mutmut_16() -> int:
    """Gate: :data:`CORE_CHECKS` ↔ on-disk modules agree bidirectionally.

    Reuses the engine keystone :func:`tc_fitness.catalogue_check_consistency`
    over the declared registry and the discovered modules, so a CORE module
    added without a registry id (orphan) OR a registry id with no module
    (dangling) FAILS. Returns ``0`` when consistent, ``1`` on drift.
    """
    from tc_fitness.keystone import catalogue_check_consistency
    from tc_fitness.lib import remediation as _remediation

    return catalogue_check_consistency(
        cataloged_check_ids=CORE_CHECKS,
        available_check_ids=discover_core_check_modules(),
        remediation=_remediation(
            fix=(
                "reconcile CORE_CHECKS (in tc_fitness.core_checks) with the modules "
                "XXon disk: add the missing core:<module> id for a new check module, XX"
                "or remove the dangling id for a module that no longer exists."
            ),
            nxt="re-run the engine test suite to confirm the registry is consistent.",
            run="python -c 'from tc_fitness.core_checks import core_check_consistency as c; raise SystemExit(c())'",
        ),
    )


def x_core_check_consistency__mutmut_17() -> int:
    """Gate: :data:`CORE_CHECKS` ↔ on-disk modules agree bidirectionally.

    Reuses the engine keystone :func:`tc_fitness.catalogue_check_consistency`
    over the declared registry and the discovered modules, so a CORE module
    added without a registry id (orphan) OR a registry id with no module
    (dangling) FAILS. Returns ``0`` when consistent, ``1`` on drift.
    """
    from tc_fitness.keystone import catalogue_check_consistency
    from tc_fitness.lib import remediation as _remediation

    return catalogue_check_consistency(
        cataloged_check_ids=CORE_CHECKS,
        available_check_ids=discover_core_check_modules(),
        remediation=_remediation(
            fix=(
                "reconcile CORE_CHECKS (in tc_fitness.core_checks) with the modules "
                "ON DISK: ADD THE MISSING CORE:<MODULE> ID FOR A NEW CHECK MODULE, "
                "or remove the dangling id for a module that no longer exists."
            ),
            nxt="re-run the engine test suite to confirm the registry is consistent.",
            run="python -c 'from tc_fitness.core_checks import core_check_consistency as c; raise SystemExit(c())'",
        ),
    )


def x_core_check_consistency__mutmut_18() -> int:
    """Gate: :data:`CORE_CHECKS` ↔ on-disk modules agree bidirectionally.

    Reuses the engine keystone :func:`tc_fitness.catalogue_check_consistency`
    over the declared registry and the discovered modules, so a CORE module
    added without a registry id (orphan) OR a registry id with no module
    (dangling) FAILS. Returns ``0`` when consistent, ``1`` on drift.
    """
    from tc_fitness.keystone import catalogue_check_consistency
    from tc_fitness.lib import remediation as _remediation

    return catalogue_check_consistency(
        cataloged_check_ids=CORE_CHECKS,
        available_check_ids=discover_core_check_modules(),
        remediation=_remediation(
            fix=(
                "reconcile CORE_CHECKS (in tc_fitness.core_checks) with the modules "
                "on disk: add the missing core:<module> id for a new check module, "
                "XXor remove the dangling id for a module that no longer exists.XX"
            ),
            nxt="re-run the engine test suite to confirm the registry is consistent.",
            run="python -c 'from tc_fitness.core_checks import core_check_consistency as c; raise SystemExit(c())'",
        ),
    )


def x_core_check_consistency__mutmut_19() -> int:
    """Gate: :data:`CORE_CHECKS` ↔ on-disk modules agree bidirectionally.

    Reuses the engine keystone :func:`tc_fitness.catalogue_check_consistency`
    over the declared registry and the discovered modules, so a CORE module
    added without a registry id (orphan) OR a registry id with no module
    (dangling) FAILS. Returns ``0`` when consistent, ``1`` on drift.
    """
    from tc_fitness.keystone import catalogue_check_consistency
    from tc_fitness.lib import remediation as _remediation

    return catalogue_check_consistency(
        cataloged_check_ids=CORE_CHECKS,
        available_check_ids=discover_core_check_modules(),
        remediation=_remediation(
            fix=(
                "reconcile CORE_CHECKS (in tc_fitness.core_checks) with the modules "
                "on disk: add the missing core:<module> id for a new check module, "
                "OR REMOVE THE DANGLING ID FOR A MODULE THAT NO LONGER EXISTS."
            ),
            nxt="re-run the engine test suite to confirm the registry is consistent.",
            run="python -c 'from tc_fitness.core_checks import core_check_consistency as c; raise SystemExit(c())'",
        ),
    )


def x_core_check_consistency__mutmut_20() -> int:
    """Gate: :data:`CORE_CHECKS` ↔ on-disk modules agree bidirectionally.

    Reuses the engine keystone :func:`tc_fitness.catalogue_check_consistency`
    over the declared registry and the discovered modules, so a CORE module
    added without a registry id (orphan) OR a registry id with no module
    (dangling) FAILS. Returns ``0`` when consistent, ``1`` on drift.
    """
    from tc_fitness.keystone import catalogue_check_consistency
    from tc_fitness.lib import remediation as _remediation

    return catalogue_check_consistency(
        cataloged_check_ids=CORE_CHECKS,
        available_check_ids=discover_core_check_modules(),
        remediation=_remediation(
            fix=(
                "reconcile CORE_CHECKS (in tc_fitness.core_checks) with the modules "
                "on disk: add the missing core:<module> id for a new check module, "
                "or remove the dangling id for a module that no longer exists."
            ),
            nxt="XXre-run the engine test suite to confirm the registry is consistent.XX",
            run="python -c 'from tc_fitness.core_checks import core_check_consistency as c; raise SystemExit(c())'",
        ),
    )


def x_core_check_consistency__mutmut_21() -> int:
    """Gate: :data:`CORE_CHECKS` ↔ on-disk modules agree bidirectionally.

    Reuses the engine keystone :func:`tc_fitness.catalogue_check_consistency`
    over the declared registry and the discovered modules, so a CORE module
    added without a registry id (orphan) OR a registry id with no module
    (dangling) FAILS. Returns ``0`` when consistent, ``1`` on drift.
    """
    from tc_fitness.keystone import catalogue_check_consistency
    from tc_fitness.lib import remediation as _remediation

    return catalogue_check_consistency(
        cataloged_check_ids=CORE_CHECKS,
        available_check_ids=discover_core_check_modules(),
        remediation=_remediation(
            fix=(
                "reconcile CORE_CHECKS (in tc_fitness.core_checks) with the modules "
                "on disk: add the missing core:<module> id for a new check module, "
                "or remove the dangling id for a module that no longer exists."
            ),
            nxt="RE-RUN THE ENGINE TEST SUITE TO CONFIRM THE REGISTRY IS CONSISTENT.",
            run="python -c 'from tc_fitness.core_checks import core_check_consistency as c; raise SystemExit(c())'",
        ),
    )


def x_core_check_consistency__mutmut_22() -> int:
    """Gate: :data:`CORE_CHECKS` ↔ on-disk modules agree bidirectionally.

    Reuses the engine keystone :func:`tc_fitness.catalogue_check_consistency`
    over the declared registry and the discovered modules, so a CORE module
    added without a registry id (orphan) OR a registry id with no module
    (dangling) FAILS. Returns ``0`` when consistent, ``1`` on drift.
    """
    from tc_fitness.keystone import catalogue_check_consistency
    from tc_fitness.lib import remediation as _remediation

    return catalogue_check_consistency(
        cataloged_check_ids=CORE_CHECKS,
        available_check_ids=discover_core_check_modules(),
        remediation=_remediation(
            fix=(
                "reconcile CORE_CHECKS (in tc_fitness.core_checks) with the modules "
                "on disk: add the missing core:<module> id for a new check module, "
                "or remove the dangling id for a module that no longer exists."
            ),
            nxt="re-run the engine test suite to confirm the registry is consistent.",
            run="XXpython -c 'from tc_fitness.core_checks import core_check_consistency as c; raise SystemExit(c())'XX",
        ),
    )


def x_core_check_consistency__mutmut_23() -> int:
    """Gate: :data:`CORE_CHECKS` ↔ on-disk modules agree bidirectionally.

    Reuses the engine keystone :func:`tc_fitness.catalogue_check_consistency`
    over the declared registry and the discovered modules, so a CORE module
    added without a registry id (orphan) OR a registry id with no module
    (dangling) FAILS. Returns ``0`` when consistent, ``1`` on drift.
    """
    from tc_fitness.keystone import catalogue_check_consistency
    from tc_fitness.lib import remediation as _remediation

    return catalogue_check_consistency(
        cataloged_check_ids=CORE_CHECKS,
        available_check_ids=discover_core_check_modules(),
        remediation=_remediation(
            fix=(
                "reconcile CORE_CHECKS (in tc_fitness.core_checks) with the modules "
                "on disk: add the missing core:<module> id for a new check module, "
                "or remove the dangling id for a module that no longer exists."
            ),
            nxt="re-run the engine test suite to confirm the registry is consistent.",
            run="python -c 'from tc_fitness.core_checks import core_check_consistency as c; raise systemexit(c())'",
        ),
    )


def x_core_check_consistency__mutmut_24() -> int:
    """Gate: :data:`CORE_CHECKS` ↔ on-disk modules agree bidirectionally.

    Reuses the engine keystone :func:`tc_fitness.catalogue_check_consistency`
    over the declared registry and the discovered modules, so a CORE module
    added without a registry id (orphan) OR a registry id with no module
    (dangling) FAILS. Returns ``0`` when consistent, ``1`` on drift.
    """
    from tc_fitness.keystone import catalogue_check_consistency
    from tc_fitness.lib import remediation as _remediation

    return catalogue_check_consistency(
        cataloged_check_ids=CORE_CHECKS,
        available_check_ids=discover_core_check_modules(),
        remediation=_remediation(
            fix=(
                "reconcile CORE_CHECKS (in tc_fitness.core_checks) with the modules "
                "on disk: add the missing core:<module> id for a new check module, "
                "or remove the dangling id for a module that no longer exists."
            ),
            nxt="re-run the engine test suite to confirm the registry is consistent.",
            run="PYTHON -C 'FROM TC_FITNESS.CORE_CHECKS IMPORT CORE_CHECK_CONSISTENCY AS C; RAISE SYSTEMEXIT(C())'",
        ),
    )

mutants_x_core_check_consistency__mutmut['_mutmut_orig'] = x_core_check_consistency__mutmut_orig # type: ignore # mutmut generated
mutants_x_core_check_consistency__mutmut['x_core_check_consistency__mutmut_1'] = x_core_check_consistency__mutmut_1 # type: ignore # mutmut generated
mutants_x_core_check_consistency__mutmut['x_core_check_consistency__mutmut_2'] = x_core_check_consistency__mutmut_2 # type: ignore # mutmut generated
mutants_x_core_check_consistency__mutmut['x_core_check_consistency__mutmut_3'] = x_core_check_consistency__mutmut_3 # type: ignore # mutmut generated
mutants_x_core_check_consistency__mutmut['x_core_check_consistency__mutmut_4'] = x_core_check_consistency__mutmut_4 # type: ignore # mutmut generated
mutants_x_core_check_consistency__mutmut['x_core_check_consistency__mutmut_5'] = x_core_check_consistency__mutmut_5 # type: ignore # mutmut generated
mutants_x_core_check_consistency__mutmut['x_core_check_consistency__mutmut_6'] = x_core_check_consistency__mutmut_6 # type: ignore # mutmut generated
mutants_x_core_check_consistency__mutmut['x_core_check_consistency__mutmut_7'] = x_core_check_consistency__mutmut_7 # type: ignore # mutmut generated
mutants_x_core_check_consistency__mutmut['x_core_check_consistency__mutmut_8'] = x_core_check_consistency__mutmut_8 # type: ignore # mutmut generated
mutants_x_core_check_consistency__mutmut['x_core_check_consistency__mutmut_9'] = x_core_check_consistency__mutmut_9 # type: ignore # mutmut generated
mutants_x_core_check_consistency__mutmut['x_core_check_consistency__mutmut_10'] = x_core_check_consistency__mutmut_10 # type: ignore # mutmut generated
mutants_x_core_check_consistency__mutmut['x_core_check_consistency__mutmut_11'] = x_core_check_consistency__mutmut_11 # type: ignore # mutmut generated
mutants_x_core_check_consistency__mutmut['x_core_check_consistency__mutmut_12'] = x_core_check_consistency__mutmut_12 # type: ignore # mutmut generated
mutants_x_core_check_consistency__mutmut['x_core_check_consistency__mutmut_13'] = x_core_check_consistency__mutmut_13 # type: ignore # mutmut generated
mutants_x_core_check_consistency__mutmut['x_core_check_consistency__mutmut_14'] = x_core_check_consistency__mutmut_14 # type: ignore # mutmut generated
mutants_x_core_check_consistency__mutmut['x_core_check_consistency__mutmut_15'] = x_core_check_consistency__mutmut_15 # type: ignore # mutmut generated
mutants_x_core_check_consistency__mutmut['x_core_check_consistency__mutmut_16'] = x_core_check_consistency__mutmut_16 # type: ignore # mutmut generated
mutants_x_core_check_consistency__mutmut['x_core_check_consistency__mutmut_17'] = x_core_check_consistency__mutmut_17 # type: ignore # mutmut generated
mutants_x_core_check_consistency__mutmut['x_core_check_consistency__mutmut_18'] = x_core_check_consistency__mutmut_18 # type: ignore # mutmut generated
mutants_x_core_check_consistency__mutmut['x_core_check_consistency__mutmut_19'] = x_core_check_consistency__mutmut_19 # type: ignore # mutmut generated
mutants_x_core_check_consistency__mutmut['x_core_check_consistency__mutmut_20'] = x_core_check_consistency__mutmut_20 # type: ignore # mutmut generated
mutants_x_core_check_consistency__mutmut['x_core_check_consistency__mutmut_21'] = x_core_check_consistency__mutmut_21 # type: ignore # mutmut generated
mutants_x_core_check_consistency__mutmut['x_core_check_consistency__mutmut_22'] = x_core_check_consistency__mutmut_22 # type: ignore # mutmut generated
mutants_x_core_check_consistency__mutmut['x_core_check_consistency__mutmut_23'] = x_core_check_consistency__mutmut_23 # type: ignore # mutmut generated
mutants_x_core_check_consistency__mutmut['x_core_check_consistency__mutmut_24'] = x_core_check_consistency__mutmut_24 # type: ignore # mutmut generated


__all__ = [
    "run_core_check",
    "CORE_CHECKS",
    "discover_core_check_modules",
    "core_check_consistency",
]
