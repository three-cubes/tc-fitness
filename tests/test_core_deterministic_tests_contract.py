"""Tests for the CORE check deterministic_tests (SGO-200).

Two layers of proof:

* the pure detection core (parse / plan / compare / argv) driven directly and
  with an injected fake runner — no subprocess, fast and hermetic;
* end-to-end FIXTURES that prove the gate BITES: a genuinely non-deterministic
  test (a counter that flips even/odd each run) is caught by the fixed-seed
  repeat probe, and a deliberately order-dependent pair (shared module state)
  is caught by the order probe — both surfacing the offending test id.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from tc_fitness.core_checks.deterministic_tests import (
    DeterministicTests,
    RunSpec,
    build,
    detect_nondeterminism,
)

pytestmark = pytest.mark.contract

# --------------------------------------------------------------------------- #
# Pure helpers.
# --------------------------------------------------------------------------- #

_PYTEST_V_OUTPUT = """\
tests/test_a.py::test_one PASSED                                         [ 25%]
tests/test_a.py::TestCls::test_m FAILED                                  [ 50%]
tests/test_b.py::test_p[1] PASSED                                        [ 75%]
tests/test_b.py::test_p[2] SKIPPED                                       [100%]
=========================== short test summary info ============================
FAILED tests/test_a.py::TestCls::test_m - assert True is False
"""


# The terminal-summary "FAILED <nodeid> - ..." line is NOT double-counted as
# a result (it carries no [ NN%] progress marker).


def test_detect_nondeterminism_with_injected_runner() -> None:
    # rep1/rep2 identical; the order run flips "b" — the order probe bites.
    scripted = {
        "fixed-seed:rep1": {"a": "passed", "b": "passed"},
        "fixed-seed:rep2": {"a": "passed", "b": "passed"},
        "order:seed1": {"a": "passed", "b": "failed"},
    }
    plan = [RunSpec("fixed-seed:rep1", None), RunSpec("fixed-seed:rep2", None), RunSpec("order:seed1", 1)]
    diffs = detect_nondeterminism(plan, lambda spec: scripted[spec.label])
    assert [d.test_id for d in diffs] == ["b"]


# --------------------------------------------------------------------------- #
# Config injection + conformance.
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
# End-to-end fixtures: the gate BITES on a real subprocess pytest run.
# --------------------------------------------------------------------------- #


def _seed_tests(tmp_path: Path) -> Path:
    tests = tmp_path / "tests"
    tests.mkdir()
    return tests


def _rule_for(tmp_path: Path, *, repeats: int, order_seeds: tuple[int, ...]) -> DeterministicTests:
    rule = build(
        {
            "roots": ["tests"],
            "repeats": repeats,
            "order_seeds": list(order_seeds),
            # Use THIS interpreter's pytest so the subprocess is hermetic.
            "test_command": [sys.executable, "-m", "pytest"],
            "timeout_seconds": 120,
        },
        repo_root=tmp_path,
    )
    return rule
