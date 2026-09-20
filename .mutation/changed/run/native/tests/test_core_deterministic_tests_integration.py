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
from _core_check_assertions import assert_no_repo_identity

from tc_fitness.core_checks.deterministic_tests import (
    DeterministicTests,
    RunSpec,
    SuiteRunError,
    build,
    collect_node_ids,
    run_suite,
    shuffled_order,
)

pytestmark = pytest.mark.integration

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


# --------------------------------------------------------------------------- #
# Config injection + conformance.
# --------------------------------------------------------------------------- #


def test_build_returns_rule_with_defaults() -> None:
    rule = build({})
    assert isinstance(rule, DeterministicTests)
    assert rule.repeats == 2
    assert rule.use_randomly is False


def test_from_config_reads_knobs() -> None:
    rule = build(
        {
            "roots": ["tests"],
            "seed": 42,
            "repeats": 3,
            "order_seeds": [9, 10],
            "test_command": ["uv", "run", "pytest"],
            "use_randomly": True,
            "timeout_seconds": 120,
        }
    )
    assert rule.seed == 42
    assert rule.repeats == 3
    assert rule.order_seeds == (9, 10)
    assert rule.test_command == ("uv", "run", "pytest")
    assert rule.use_randomly is True
    assert rule.timeout_seconds == 120


def test_no_config_is_vacuous_pass(tmp_path: Path, capsys: object) -> None:
    # No roots configured → nothing to run → vacuous pass (adoption default).
    assert build({}, repo_root=tmp_path).run() == 0


def test_no_repo_strings_in_executable_code() -> None:
    import tc_fitness.core_checks.deterministic_tests as mod

    assert_no_repo_identity(mod.__file__)


def test_suite_run_error_surfaces_as_fail(tmp_path: Path, capsys: object) -> None:
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_ok.py").write_text("def test_ok():\n    assert True\n", encoding="utf-8")

    class _Boom(DeterministicTests):
        def _runner(self, test_paths: object, node_ids: object) -> object:  # type: ignore[override]
            def _run(spec: RunSpec) -> dict[str, str]:
                raise SuiteRunError("boom")

            return _run

    rule = _Boom(repo_root=tmp_path, roots=("tests",))
    rule.order_seeds = ()
    assert rule.run() == 1


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


def test_fixed_seed_repeat_catches_flaky_test(tmp_path: Path, capsys: object) -> None:
    """A test that flips outcome each run is caught by the repeat probe."""
    counter = tmp_path / "counter.txt"
    tests = _seed_tests(tmp_path)
    (tests / "test_flaky.py").write_text(
        "from pathlib import Path\n"
        f"_C = Path(r'{counter}')\n"
        "def test_flaky_counter():\n"
        "    n = int(_C.read_text()) if _C.exists() else 0\n"
        "    _C.write_text(str(n + 1))\n"
        "    assert n % 2 == 0\n",
        encoding="utf-8",
    )
    # Repeat-only: run twice in natural order, no order probe needed.
    rule = _rule_for(tmp_path, repeats=2, order_seeds=())
    rc = rule.run()
    out = capsys.readouterr().out  # type: ignore[attr-defined]
    assert rc == 1, "a test that flips outcome across identical runs must FAIL the gate"
    assert "FAIL [deterministic-tests]" in out
    assert "test_flaky_counter" in out


def test_order_probe_catches_order_dependent_test(tmp_path: Path, capsys: object) -> None:
    """A pair leaking module state across tests is caught by the order probe."""
    tests = _seed_tests(tmp_path)
    # A shared, non-test module (no test_ prefix) both tests mutate/read. In
    # pytest's default prepend import mode the tests/ dir is on sys.path, so
    # `import _shared` resolves to one module instance shared within a run.
    (tests / "_shared.py").write_text("polluted = False\n", encoding="utf-8")
    (tests / "test_a_pollute.py").write_text(
        "import _shared\ndef test_pollute():\n    _shared.polluted = True\n    assert True\n",
        encoding="utf-8",
    )
    (tests / "test_z_depends.py").write_text(
        "import _shared\ndef test_depends_on_clean():\n    assert _shared.polluted is False\n",
        encoding="utf-8",
    )

    # Pick an order seed that puts the dependent test BEFORE the polluter (so it
    # passes), contrasting with the natural order (polluter first → it fails).
    node_ids = [
        "tests/test_a_pollute.py::test_pollute",
        "tests/test_z_depends.py::test_depends_on_clean",
    ]
    swap_seed = next(
        s for s in range(100) if shuffled_order(node_ids, s)[0].endswith("test_depends_on_clean")
    )

    # One natural run + one swapped-order run: the dependent test's verdict flips.
    rule = _rule_for(tmp_path, repeats=1, order_seeds=(swap_seed,))
    rc = rule.run()
    out = capsys.readouterr().out  # type: ignore[attr-defined]
    assert rc == 1, "an order-dependent test must FAIL the determinism gate"
    assert "FAIL [deterministic-tests]" in out
    assert "test_depends_on_clean" in out


def test_stable_suite_passes(tmp_path: Path, capsys: object) -> None:
    """A genuinely independent suite passes under repeats + order probes."""
    tests = _seed_tests(tmp_path)
    (tests / "test_indep.py").write_text(
        "def test_a():\n    assert 1 + 1 == 2\n\n\ndef test_b():\n    assert 'x' in 'xyz'\n",
        encoding="utf-8",
    )
    rule = _rule_for(tmp_path, repeats=2, order_seeds=(1, 2))
    rc = rule.run()
    out = capsys.readouterr().out  # type: ignore[attr-defined]
    assert rc == 0, "a deterministic suite must PASS"
    assert "ok [deterministic-tests]" in out


def test_existing_empty_root_is_reported_as_no_collected_tests(tmp_path: Path, capsys: object) -> None:
    _seed_tests(tmp_path)
    rule = build(
        {"roots": ["tests"], "test_command": [sys.executable, "-m", "pytest"]},
        repo_root=tmp_path,
    )

    assert rule.run() == 0
    assert "no tests collected" in capsys.readouterr().out  # type: ignore[attr-defined]


def test_unavailable_configured_runner_is_a_dependency_error(tmp_path: Path, capsys: object) -> None:
    _seed_tests(tmp_path)
    rule = build(
        {"roots": ["tests"], "test_command": [str(tmp_path / "missing-test-runner")]},
        repo_root=tmp_path,
    )

    assert rule.run() == 2
    assert "configured test command unavailable" in capsys.readouterr().out  # type: ignore[attr-defined]


def test_real_collection_timeout_is_a_suite_run_error(tmp_path: Path) -> None:
    with pytest.raises(SuiteRunError, match="collection timed out after"):
        collect_node_ids(
            [sys.executable, "-c", "import time; time.sleep(1)"],
            ["tests"],
            repo_root=tmp_path,
            seed=11,
            timeout=0.05,
        )


def test_real_suite_timeout_is_a_suite_run_error(tmp_path: Path) -> None:
    with pytest.raises(SuiteRunError, match="timed out after"):
        run_suite(
            RunSpec("timeout-probe", None),
            command=[sys.executable, "-c", "import time; time.sleep(1)"],
            test_paths=["tests"],
            node_ids=[],
            repo_root=tmp_path,
            seed=13,
            use_randomly=False,
            timeout=0.05,
        )


def test_real_process_without_pytest_outcomes_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(SuiteRunError, match="produced no per-test results"):
        run_suite(
            RunSpec("no-results", None),
            command=[sys.executable, "-c", "print('process started')"],
            test_paths=["tests"],
            node_ids=[],
            repo_root=tmp_path,
            seed=17,
            use_randomly=False,
            timeout=5,
        )
