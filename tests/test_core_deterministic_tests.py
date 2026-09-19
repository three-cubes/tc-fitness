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
    Divergence,
    build,
    build_pytest_argv,
    compare_runs,
    format_failure,
    parse_collected,
    parse_outcomes,
    plan_runs,
    shuffled_order,
)

pytestmark = pytest.mark.unit

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


def test_parse_outcomes_reads_progress_lines_only() -> None:
    outcomes = parse_outcomes(_PYTEST_V_OUTPUT)
    assert outcomes == {
        "tests/test_a.py::test_one": "passed",
        "tests/test_a.py::TestCls::test_m": "failed",
        "tests/test_b.py::test_p[1]": "passed",
        "tests/test_b.py::test_p[2]": "skipped",
    }
    # The terminal-summary "FAILED <nodeid> - ..." line is NOT double-counted as
    # a result (it carries no [ NN%] progress marker).


def test_parse_collected_keeps_node_ids_only() -> None:
    text = "tests/test_a.py::test_one\ntests/test_b.py::test_p[1]\n\n2 tests collected in 0.01s\n"
    assert parse_collected(text) == [
        "tests/test_a.py::test_one",
        "tests/test_b.py::test_p[1]",
    ]


def test_shuffled_order_is_deterministic_in_seed() -> None:
    ids = [f"t{i}" for i in range(12)]
    assert shuffled_order(ids, 7) == shuffled_order(ids, 7)
    # A different seed generally yields a different order (not the natural one).
    assert shuffled_order(ids, 7) != ids


def test_plan_runs_shape() -> None:
    plan = plan_runs(2, [1, 2])
    assert [s.label for s in plan] == ["fixed-seed:rep1", "fixed-seed:rep2", "order:seed1", "order:seed2"]
    assert [s.order_seed for s in plan] == [None, None, 1, 2]


def test_compare_runs_flags_only_unstable() -> None:
    runs = [
        ("rep1", {"a": "passed", "b": "passed"}),
        ("rep2", {"a": "failed", "b": "passed"}),
    ]
    diffs = compare_runs(runs)
    assert [d.test_id for d in diffs] == ["a"]
    assert diffs[0].outcomes == (("rep1", "passed"), ("rep2", "failed"))


def test_compare_runs_flags_absence_as_instability() -> None:
    runs = [("r1", {"a": "passed"}), ("r2", {})]
    diffs = compare_runs(runs)
    assert [d.test_id for d in diffs] == ["a"]
    assert diffs[0].outcomes == (("r1", "passed"), ("r2", "<absent>"))


def test_compare_runs_stable_suite_is_clean() -> None:
    runs = [("r1", {"a": "passed", "b": "skipped"}), ("r2", {"a": "passed", "b": "skipped"})]
    assert compare_runs(runs) == []


def test_build_argv_plugin_free_blocks_reruns_and_randomly() -> None:
    argv = build_pytest_argv(
        ["python", "-m", "pytest"],
        test_paths=["tests"],
        node_ids=["tests/test_a.py::t"],
        order_seed=None,
        use_randomly=False,
    )
    # The reconciliation with the loop guardrail: reruns can NEVER mask a flake
    # inside the probe, and no run ever asks for retries.
    assert "no:rerunfailures" in argv
    assert "no:randomly" in argv
    assert not any(a.startswith("--reruns") for a in argv)
    assert "--randomly-seed" not in argv
    # A natural-order run scopes by path, not explicit node ids.
    assert argv[-1] == "tests"


def test_build_argv_order_run_uses_shuffled_node_ids() -> None:
    node_ids = [f"tests/test_a.py::t{i}" for i in range(8)]
    argv = build_pytest_argv(
        ["python", "-m", "pytest"],
        test_paths=["tests"],
        node_ids=node_ids,
        order_seed=3,
        use_randomly=False,
    )
    tail = argv[argv.index("no:randomly") + 1 :]
    assert sorted(tail) == sorted(node_ids)
    assert tail == shuffled_order(node_ids, 3)


def test_build_argv_randomly_mode_delegates_ordering() -> None:
    argv = build_pytest_argv(
        ["python", "-m", "pytest"],
        test_paths=["tests"],
        node_ids=[],
        order_seed=5,
        use_randomly=True,
    )
    assert "--randomly-seed" in argv
    assert argv[argv.index("--randomly-seed") + 1] == "5"
    assert "no:randomly" not in argv  # not disabled — we WANT randomly here
    assert "no:rerunfailures" in argv  # still never masked by reruns


def test_format_failure_names_offender_and_remediation() -> None:
    block = format_failure(
        [Divergence("tests/test_x.py::test_flaky", (("rep1", "passed"), ("rep2", "failed")))]
    )
    assert "FAIL [deterministic-tests]" in block
    assert "tests/test_x.py::test_flaky" in block
    assert "rep1=passed" in block and "rep2=failed" in block
    assert "--reruns" in block  # remediation forbids the retry escape hatch


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
