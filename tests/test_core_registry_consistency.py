"""Engine CORE-check registry ↔ on-disk module consistency (the F92 keystone).

The v0.6.0 promotion ships ~35 CORE checks. ``CORE_CHECKS`` is the single
catalogue of what the engine claims to ship; the modules under
``tc_fitness.core_checks`` are what it actually ships. These tests lock the two
together BIDIRECTIONALLY (no orphan module, no dangling id) and prove the
``core:<module>`` namespace resolves to the importable module the runner
dispatches in-process.
"""

from __future__ import annotations

import importlib

import pytest

from tc_fitness.catalogue import RuleEntry
from tc_fitness.core_checks import (
    CORE_CHECKS,
    core_check_consistency,
    discover_core_check_modules,
)
from tc_fitness.runner import core_module_name, is_core_check

pytestmark = pytest.mark.integration


def test_registry_matches_disk_bidirectionally() -> None:
    registry = set(CORE_CHECKS)
    on_disk = set(discover_core_check_modules())
    assert registry - on_disk == set(), "dangling registry id with no module"
    assert on_disk - registry == set(), "orphan module with no registry id"


def test_core_check_consistency_passes() -> None:
    assert core_check_consistency() == 0


@pytest.mark.parametrize("check_id", CORE_CHECKS)
def test_every_core_check_module_is_conformant(check_id: str) -> None:
    """Each registered check resolves to a module exposing build() + main()."""
    entry = RuleEntry(id=check_id, gate=check_id.split(":", 1)[1], check=check_id)
    assert is_core_check(entry)
    module = importlib.import_module(core_module_name(entry))
    assert callable(module.build)
    assert callable(module.main)


def test_runner_dispatches_core_check_in_process(tmp_path: object) -> None:
    """A ``core:`` catalogue entry resolves + runs in-process via the runner.

    With no config and an empty tree the CORE check finds no violations and the
    runner returns 0 — proving the ``core:<module>`` namespace dispatches to the
    engine module rather than a (non-existent) ``check_core:<module>.py``.
    """
    from pathlib import Path

    from tc_fitness.runner import main_cli

    repo_root = Path(str(tmp_path))
    (repo_root / "scripts" / "checks").mkdir(parents=True)
    rules = (
        RuleEntry(
            id="no-duplicate-string",
            gate="no-duplicate-string",
            check="core:no_duplicate_string",
            summary="exemplar core check",
        ),
    )
    rc = main_cli(rules, ["--all"], repo_root=repo_root, checks_dir=repo_root / "scripts" / "checks")
    assert rc == 0
