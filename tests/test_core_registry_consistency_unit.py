"""Engine CORE-check registry ↔ on-disk module consistency (the F92 keystone).

The v0.6.0 promotion ships ~35 CORE checks. ``CORE_CHECKS`` is the single
catalogue of what the engine claims to ship; the modules under
``tc_fitness.core_checks`` are what it actually ships. These tests lock the two
together BIDIRECTIONALLY (no orphan module, no dangling id) and prove the
``core:<module>`` namespace resolves to the importable module the runner
dispatches in-process.
"""

from __future__ import annotations

import pytest

from tc_fitness.catalogue import RuleEntry
from tc_fitness.core_checks import (
    CORE_CHECKS,
)
from tc_fitness.runner import core_module_name, is_core_check

pytestmark = pytest.mark.unit


def test_registry_is_sorted_and_namespaced() -> None:
    assert list(CORE_CHECKS) == sorted(CORE_CHECKS)
    assert all(cid.startswith("core:") for cid in CORE_CHECKS)


def test_core_module_name_resolution() -> None:
    entry = RuleEntry(id="x", gate="x", check="core:no_duplicate_string")
    assert is_core_check(entry)
    assert core_module_name(entry) == "tc_fitness.core_checks.no_duplicate_string"


def test_local_check_is_not_core() -> None:
    entry = RuleEntry(id="x", gate="x", check="provider_layer_imports")
    assert not is_core_check(entry)
