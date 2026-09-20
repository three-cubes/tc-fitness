"""CORE check: deterministic_tests — test non-determinism is a GATE FAILURE.

A ~50% flake sat undetected in a consumer's coverage suite: the same commit
passed on some runs and failed on others, and the gate tolerated it because a
green-on-retry looked like a pass. This check converges that one-off lesson
INTO THE ENGINE so *every* repo inherits the same bite: a test whose outcome is
not stable is a failure the gate REFUSES to pass, surfaced with the offending
test id, not silently retried into green.

What it proves
==============
Given the (changed-scope) test roots a consumer configures, this check runs the
suite several times and FAILS if any test's outcome is not identical across all
runs. Two independent probes, both under one pinned hash seed
(``PYTHONHASHSEED``) so hash-ordering is held constant:

* **fixed-seed repeat** — run the suite ``repeats`` times in the SAME order.
  Any divergence here is pure non-determinism (wall-clock, unseeded ``random``,
  network, shared/leaked state, filesystem-order dependence) — the exact class
  the undetected coverage flake belonged to.

* **order stability** — re-run the SAME tests under one or more shuffled
  execution orders and require the SAME per-test verdicts. An outcome that
  flips when the order changes is an order-dependent test (state leaked between
  tests). Order is varied deterministically from an integer ``order_seed`` so a
  failure REPRODUCES exactly — non-determinism surfaced AS a deterministic
  failure. When a consumer has adopted ``pytest-randomly`` the same seed is
  handed to ``--randomly-seed`` (``use_randomly = true``); otherwise the check
  reorders the collected node ids itself, so it bites with core pytest alone.

Reconciliation with the loop determinism guardrail
==================================================
The loop state machine bans ``--reruns`` and the companion CORE check
``no_test_reruns`` fails any repo whose pytest/CI config enables flaky-retry
(``pytest-rerunfailures`` / ``--reruns`` / retry actions) — because a retry
MASKS the very flake this gate exists to catch. This check is the dynamic half
of the same standard and never contradicts it:

* it NEVER passes ``--reruns`` / enables a retry plugin, and
* it defensively blocks the retry plugin inside its own probe
  (``-p no:rerunfailures``) so a consumer's leftover ``addopts = "--reruns=N"``
  cannot mask a flake DURING the determinism run.

``no_test_reruns`` enforces the ban statically (the config may not ask for
retries); ``deterministic_tests`` proves the payoff dynamically (the suite is
actually stable). Spec (STANDARDS.md), gate (these two checks), and runtime
(the loop guardrail) therefore agree. See ``docs/STANDARDS.md`` §Deterministic
tests.

Repo-agnostic
=============
This module names no repo. The test roots, the pinned seed, the repeat count,
the order seeds, the per-run timeout, the base test command, and whether to
delegate ordering to ``pytest-randomly`` all arrive through the consumer's
``[tool.tc_fitness.core_checks.deterministic_tests]`` block. With NO config the
default ``roots = ()`` enumerates nothing and the check is a vacuous pass — the
same adoption contract every CORE check follows.
"""

from __future__ import annotations

import os
import random
import re
import subprocess
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tc_fitness.check_evidence import report_finding
from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: The pinned hash seed. Held CONSTANT across every run so hash-ordering is not
#: itself a variable — a divergence under a fixed seed is a real flake.
DEFAULT_SEED = 0
#: How many times the suite is run in the natural order. Two is enough to catch
#: a coin-flip flake most of the time; a consumer may raise it.
DEFAULT_REPEATS = 2
#: The order seeds probed for order-dependence. Each produces one extra run in a
#: distinct, reproducible order. Empty disables the order probe.
DEFAULT_ORDER_SEEDS: tuple[int, ...] = (1, 2)
#: The base command the runs are built on. ``python -m pytest`` by default; a
#: consumer on ``uv`` / a wrapper overrides it.
DEFAULT_TEST_COMMAND: tuple[str, ...] = ("python", "-m", "pytest")
#: Per-run wall-clock ceiling. A run that does not finish in this window is a
#: FAIL (the suite cannot be shown deterministic).
DEFAULT_TIMEOUT_SECONDS = 900

#: Sentinel outcome for a test that did not appear in a run at all (collection
#: non-determinism is itself instability).
_ABSENT = "<absent>"

# A verbose pytest progress line: ``<nodeid> <OUTCOME>  [ NN%]``. The trailing
# ``[ NN%]`` marker is present ONLY on the per-test progress lines, never on the
# terminal summary (``FAILED <nodeid> - <reason>``), so requiring it cleanly
# excludes the summary from the parse.
_OUTCOME_LINE = re.compile(
    r"^(?P<nodeid>.+?::.+?)\s+(?P<outcome>PASSED|FAILED|ERROR|SKIPPED|XFAIL|XPASS)\s+\[\s*\d+%\]\s*$"
)

REMEDIATION = _remediation(
    fix=(
        "a test whose verdict is not stable is a DEFECT, not noise: find the "
        "shared/leaked state, the unseeded random, the wall-clock or ordering "
        "dependence and fix the ROOT CAUSE so the test is stable in any order. "
        "Do NOT paper over it with --reruns / a retry plugin (that masks the "
        "flake and is banned by no_test_reruns + the loop guardrail). If it "
        "cannot be fixed now, open a must-fix Linear work-item and quarantine "
        "the test explicitly there — never leave it silently retried."
    ),
    nxt="re-run this check to confirm the suite is stable across seeds and orders.",
    run="python -m tc_fitness.core_checks.deterministic_tests",
    passing="isolate per-test state (fresh fixtures, seeded randomness) so order never changes a verdict",
    forbidden="enable pytest-rerunfailures / --reruns to retry a flaky test into green",
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


@dataclass(frozen=True)
class RunSpec:
    """One planned execution of the suite.

    ``order_seed`` is ``None`` for a natural-order run (the fixed-seed repeats)
    and an integer for an order-probe run. ``label`` is the human tag shown
    against a divergence so the reader sees WHICH probe caught it.
    """

    label: str
    order_seed: int | None


@dataclass(frozen=True)
class Divergence:
    """A test whose outcome was not identical across the planned runs."""

    test_id: str
    #: ``(label, outcome)`` for every run, in plan order.
    outcomes: tuple[tuple[str, str], ...]


class SuiteRunError(RuntimeError):
    """A run could not be completed (timeout / collection failure)."""
mutants_x_parse_outcomes__mutmut: MutantDict = {}  # type: ignore


# --------------------------------------------------------------------------- #
# Pure helpers — the detection core, unit-tested without a subprocess.
# --------------------------------------------------------------------------- #


@_mutmut_mutated(mutants_x_parse_outcomes__mutmut)
def parse_outcomes(stdout: str) -> dict[str, str]:
    """Map ``nodeid -> lowercased outcome`` from ``pytest -v --color=no`` output.

    Only the verbose per-test progress lines are read; the terminal summary and
    any captured output are ignored (they lack the ``[ NN%]`` progress marker).
    """
    out: dict[str, str] = {}
    for line in stdout.splitlines():
        match = _OUTCOME_LINE.match(line.rstrip())
        if match:
            out[match.group("nodeid").strip()] = match.group("outcome").lower()
    return out


# --------------------------------------------------------------------------- #
# Pure helpers — the detection core, unit-tested without a subprocess.
# --------------------------------------------------------------------------- #


def x_parse_outcomes__mutmut_orig(stdout: str) -> dict[str, str]:
    """Map ``nodeid -> lowercased outcome`` from ``pytest -v --color=no`` output.

    Only the verbose per-test progress lines are read; the terminal summary and
    any captured output are ignored (they lack the ``[ NN%]`` progress marker).
    """
    out: dict[str, str] = {}
    for line in stdout.splitlines():
        match = _OUTCOME_LINE.match(line.rstrip())
        if match:
            out[match.group("nodeid").strip()] = match.group("outcome").lower()
    return out


# --------------------------------------------------------------------------- #
# Pure helpers — the detection core, unit-tested without a subprocess.
# --------------------------------------------------------------------------- #


def x_parse_outcomes__mutmut_1(stdout: str) -> dict[str, str]:
    """Map ``nodeid -> lowercased outcome`` from ``pytest -v --color=no`` output.

    Only the verbose per-test progress lines are read; the terminal summary and
    any captured output are ignored (they lack the ``[ NN%]`` progress marker).
    """
    out: dict[str, str] = None
    for line in stdout.splitlines():
        match = _OUTCOME_LINE.match(line.rstrip())
        if match:
            out[match.group("nodeid").strip()] = match.group("outcome").lower()
    return out


# --------------------------------------------------------------------------- #
# Pure helpers — the detection core, unit-tested without a subprocess.
# --------------------------------------------------------------------------- #


def x_parse_outcomes__mutmut_2(stdout: str) -> dict[str, str]:
    """Map ``nodeid -> lowercased outcome`` from ``pytest -v --color=no`` output.

    Only the verbose per-test progress lines are read; the terminal summary and
    any captured output are ignored (they lack the ``[ NN%]`` progress marker).
    """
    out: dict[str, str] = {}
    for line in stdout.splitlines():
        match = None
        if match:
            out[match.group("nodeid").strip()] = match.group("outcome").lower()
    return out


# --------------------------------------------------------------------------- #
# Pure helpers — the detection core, unit-tested without a subprocess.
# --------------------------------------------------------------------------- #


def x_parse_outcomes__mutmut_3(stdout: str) -> dict[str, str]:
    """Map ``nodeid -> lowercased outcome`` from ``pytest -v --color=no`` output.

    Only the verbose per-test progress lines are read; the terminal summary and
    any captured output are ignored (they lack the ``[ NN%]`` progress marker).
    """
    out: dict[str, str] = {}
    for line in stdout.splitlines():
        match = _OUTCOME_LINE.match(None)
        if match:
            out[match.group("nodeid").strip()] = match.group("outcome").lower()
    return out


# --------------------------------------------------------------------------- #
# Pure helpers — the detection core, unit-tested without a subprocess.
# --------------------------------------------------------------------------- #


def x_parse_outcomes__mutmut_4(stdout: str) -> dict[str, str]:
    """Map ``nodeid -> lowercased outcome`` from ``pytest -v --color=no`` output.

    Only the verbose per-test progress lines are read; the terminal summary and
    any captured output are ignored (they lack the ``[ NN%]`` progress marker).
    """
    out: dict[str, str] = {}
    for line in stdout.splitlines():
        match = _OUTCOME_LINE.match(line.lstrip())
        if match:
            out[match.group("nodeid").strip()] = match.group("outcome").lower()
    return out


# --------------------------------------------------------------------------- #
# Pure helpers — the detection core, unit-tested without a subprocess.
# --------------------------------------------------------------------------- #


def x_parse_outcomes__mutmut_5(stdout: str) -> dict[str, str]:
    """Map ``nodeid -> lowercased outcome`` from ``pytest -v --color=no`` output.

    Only the verbose per-test progress lines are read; the terminal summary and
    any captured output are ignored (they lack the ``[ NN%]`` progress marker).
    """
    out: dict[str, str] = {}
    for line in stdout.splitlines():
        match = _OUTCOME_LINE.match(line.rstrip())
        if match:
            out[match.group("nodeid").strip()] = None
    return out


# --------------------------------------------------------------------------- #
# Pure helpers — the detection core, unit-tested without a subprocess.
# --------------------------------------------------------------------------- #


def x_parse_outcomes__mutmut_6(stdout: str) -> dict[str, str]:
    """Map ``nodeid -> lowercased outcome`` from ``pytest -v --color=no`` output.

    Only the verbose per-test progress lines are read; the terminal summary and
    any captured output are ignored (they lack the ``[ NN%]`` progress marker).
    """
    out: dict[str, str] = {}
    for line in stdout.splitlines():
        match = _OUTCOME_LINE.match(line.rstrip())
        if match:
            out[match.group(None).strip()] = match.group("outcome").lower()
    return out


# --------------------------------------------------------------------------- #
# Pure helpers — the detection core, unit-tested without a subprocess.
# --------------------------------------------------------------------------- #


def x_parse_outcomes__mutmut_7(stdout: str) -> dict[str, str]:
    """Map ``nodeid -> lowercased outcome`` from ``pytest -v --color=no`` output.

    Only the verbose per-test progress lines are read; the terminal summary and
    any captured output are ignored (they lack the ``[ NN%]`` progress marker).
    """
    out: dict[str, str] = {}
    for line in stdout.splitlines():
        match = _OUTCOME_LINE.match(line.rstrip())
        if match:
            out[match.group("XXnodeidXX").strip()] = match.group("outcome").lower()
    return out


# --------------------------------------------------------------------------- #
# Pure helpers — the detection core, unit-tested without a subprocess.
# --------------------------------------------------------------------------- #


def x_parse_outcomes__mutmut_8(stdout: str) -> dict[str, str]:
    """Map ``nodeid -> lowercased outcome`` from ``pytest -v --color=no`` output.

    Only the verbose per-test progress lines are read; the terminal summary and
    any captured output are ignored (they lack the ``[ NN%]`` progress marker).
    """
    out: dict[str, str] = {}
    for line in stdout.splitlines():
        match = _OUTCOME_LINE.match(line.rstrip())
        if match:
            out[match.group("NODEID").strip()] = match.group("outcome").lower()
    return out


# --------------------------------------------------------------------------- #
# Pure helpers — the detection core, unit-tested without a subprocess.
# --------------------------------------------------------------------------- #


def x_parse_outcomes__mutmut_9(stdout: str) -> dict[str, str]:
    """Map ``nodeid -> lowercased outcome`` from ``pytest -v --color=no`` output.

    Only the verbose per-test progress lines are read; the terminal summary and
    any captured output are ignored (they lack the ``[ NN%]`` progress marker).
    """
    out: dict[str, str] = {}
    for line in stdout.splitlines():
        match = _OUTCOME_LINE.match(line.rstrip())
        if match:
            out[match.group("nodeid").strip()] = match.group("outcome").upper()
    return out


# --------------------------------------------------------------------------- #
# Pure helpers — the detection core, unit-tested without a subprocess.
# --------------------------------------------------------------------------- #


def x_parse_outcomes__mutmut_10(stdout: str) -> dict[str, str]:
    """Map ``nodeid -> lowercased outcome`` from ``pytest -v --color=no`` output.

    Only the verbose per-test progress lines are read; the terminal summary and
    any captured output are ignored (they lack the ``[ NN%]`` progress marker).
    """
    out: dict[str, str] = {}
    for line in stdout.splitlines():
        match = _OUTCOME_LINE.match(line.rstrip())
        if match:
            out[match.group("nodeid").strip()] = match.group(None).lower()
    return out


# --------------------------------------------------------------------------- #
# Pure helpers — the detection core, unit-tested without a subprocess.
# --------------------------------------------------------------------------- #


def x_parse_outcomes__mutmut_11(stdout: str) -> dict[str, str]:
    """Map ``nodeid -> lowercased outcome`` from ``pytest -v --color=no`` output.

    Only the verbose per-test progress lines are read; the terminal summary and
    any captured output are ignored (they lack the ``[ NN%]`` progress marker).
    """
    out: dict[str, str] = {}
    for line in stdout.splitlines():
        match = _OUTCOME_LINE.match(line.rstrip())
        if match:
            out[match.group("nodeid").strip()] = match.group("XXoutcomeXX").lower()
    return out


# --------------------------------------------------------------------------- #
# Pure helpers — the detection core, unit-tested without a subprocess.
# --------------------------------------------------------------------------- #


def x_parse_outcomes__mutmut_12(stdout: str) -> dict[str, str]:
    """Map ``nodeid -> lowercased outcome`` from ``pytest -v --color=no`` output.

    Only the verbose per-test progress lines are read; the terminal summary and
    any captured output are ignored (they lack the ``[ NN%]`` progress marker).
    """
    out: dict[str, str] = {}
    for line in stdout.splitlines():
        match = _OUTCOME_LINE.match(line.rstrip())
        if match:
            out[match.group("nodeid").strip()] = match.group("OUTCOME").lower()
    return out

mutants_x_parse_outcomes__mutmut['_mutmut_orig'] = x_parse_outcomes__mutmut_orig # type: ignore # mutmut generated
mutants_x_parse_outcomes__mutmut['x_parse_outcomes__mutmut_1'] = x_parse_outcomes__mutmut_1 # type: ignore # mutmut generated
mutants_x_parse_outcomes__mutmut['x_parse_outcomes__mutmut_2'] = x_parse_outcomes__mutmut_2 # type: ignore # mutmut generated
mutants_x_parse_outcomes__mutmut['x_parse_outcomes__mutmut_3'] = x_parse_outcomes__mutmut_3 # type: ignore # mutmut generated
mutants_x_parse_outcomes__mutmut['x_parse_outcomes__mutmut_4'] = x_parse_outcomes__mutmut_4 # type: ignore # mutmut generated
mutants_x_parse_outcomes__mutmut['x_parse_outcomes__mutmut_5'] = x_parse_outcomes__mutmut_5 # type: ignore # mutmut generated
mutants_x_parse_outcomes__mutmut['x_parse_outcomes__mutmut_6'] = x_parse_outcomes__mutmut_6 # type: ignore # mutmut generated
mutants_x_parse_outcomes__mutmut['x_parse_outcomes__mutmut_7'] = x_parse_outcomes__mutmut_7 # type: ignore # mutmut generated
mutants_x_parse_outcomes__mutmut['x_parse_outcomes__mutmut_8'] = x_parse_outcomes__mutmut_8 # type: ignore # mutmut generated
mutants_x_parse_outcomes__mutmut['x_parse_outcomes__mutmut_9'] = x_parse_outcomes__mutmut_9 # type: ignore # mutmut generated
mutants_x_parse_outcomes__mutmut['x_parse_outcomes__mutmut_10'] = x_parse_outcomes__mutmut_10 # type: ignore # mutmut generated
mutants_x_parse_outcomes__mutmut['x_parse_outcomes__mutmut_11'] = x_parse_outcomes__mutmut_11 # type: ignore # mutmut generated
mutants_x_parse_outcomes__mutmut['x_parse_outcomes__mutmut_12'] = x_parse_outcomes__mutmut_12 # type: ignore # mutmut generated
mutants_x_parse_collected__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_parse_collected__mutmut)
def parse_collected(stdout: str) -> list[str]:
    """Return the node ids from ``pytest --collect-only -q`` output, in order.

    A collect line is any line naming a node id (contains ``::``); the trailing
    ``N tests collected`` summary carries no ``::`` and is dropped.
    """
    return [line.strip() for line in stdout.splitlines() if "::" in line and line.strip()]


def x_parse_collected__mutmut_orig(stdout: str) -> list[str]:
    """Return the node ids from ``pytest --collect-only -q`` output, in order.

    A collect line is any line naming a node id (contains ``::``); the trailing
    ``N tests collected`` summary carries no ``::`` and is dropped.
    """
    return [line.strip() for line in stdout.splitlines() if "::" in line and line.strip()]


def x_parse_collected__mutmut_1(stdout: str) -> list[str]:
    """Return the node ids from ``pytest --collect-only -q`` output, in order.

    A collect line is any line naming a node id (contains ``::``); the trailing
    ``N tests collected`` summary carries no ``::`` and is dropped.
    """
    return [line.strip() for line in stdout.splitlines() if "::" in line or line.strip()]


def x_parse_collected__mutmut_2(stdout: str) -> list[str]:
    """Return the node ids from ``pytest --collect-only -q`` output, in order.

    A collect line is any line naming a node id (contains ``::``); the trailing
    ``N tests collected`` summary carries no ``::`` and is dropped.
    """
    return [line.strip() for line in stdout.splitlines() if "XX::XX" in line and line.strip()]


def x_parse_collected__mutmut_3(stdout: str) -> list[str]:
    """Return the node ids from ``pytest --collect-only -q`` output, in order.

    A collect line is any line naming a node id (contains ``::``); the trailing
    ``N tests collected`` summary carries no ``::`` and is dropped.
    """
    return [line.strip() for line in stdout.splitlines() if "::" not in line and line.strip()]

mutants_x_parse_collected__mutmut['_mutmut_orig'] = x_parse_collected__mutmut_orig # type: ignore # mutmut generated
mutants_x_parse_collected__mutmut['x_parse_collected__mutmut_1'] = x_parse_collected__mutmut_1 # type: ignore # mutmut generated
mutants_x_parse_collected__mutmut['x_parse_collected__mutmut_2'] = x_parse_collected__mutmut_2 # type: ignore # mutmut generated
mutants_x_parse_collected__mutmut['x_parse_collected__mutmut_3'] = x_parse_collected__mutmut_3 # type: ignore # mutmut generated
mutants_x_shuffled_order__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_shuffled_order__mutmut)
def shuffled_order(node_ids: Sequence[str], seed: int) -> list[str]:
    """A reproducible reordering of ``node_ids`` under ``seed``.

    Deterministic in ``seed`` (its own ``random.Random``), so an order-dependent
    failure reproduces exactly rather than intermittently.
    """
    items = list(node_ids)
    # A REPRODUCIBLE shuffle is the whole point (a failing order must replay
    # exactly); this is not a security context, so the stdlib PRNG is correct.
    random.Random(seed).shuffle(items)  # noqa: S311  # reproducibility, not cryptography
    return items


def x_shuffled_order__mutmut_orig(node_ids: Sequence[str], seed: int) -> list[str]:
    """A reproducible reordering of ``node_ids`` under ``seed``.

    Deterministic in ``seed`` (its own ``random.Random``), so an order-dependent
    failure reproduces exactly rather than intermittently.
    """
    items = list(node_ids)
    # A REPRODUCIBLE shuffle is the whole point (a failing order must replay
    # exactly); this is not a security context, so the stdlib PRNG is correct.
    random.Random(seed).shuffle(items)  # noqa: S311  # reproducibility, not cryptography
    return items


def x_shuffled_order__mutmut_1(node_ids: Sequence[str], seed: int) -> list[str]:
    """A reproducible reordering of ``node_ids`` under ``seed``.

    Deterministic in ``seed`` (its own ``random.Random``), so an order-dependent
    failure reproduces exactly rather than intermittently.
    """
    items = None
    # A REPRODUCIBLE shuffle is the whole point (a failing order must replay
    # exactly); this is not a security context, so the stdlib PRNG is correct.
    random.Random(seed).shuffle(items)  # noqa: S311  # reproducibility, not cryptography
    return items


def x_shuffled_order__mutmut_2(node_ids: Sequence[str], seed: int) -> list[str]:
    """A reproducible reordering of ``node_ids`` under ``seed``.

    Deterministic in ``seed`` (its own ``random.Random``), so an order-dependent
    failure reproduces exactly rather than intermittently.
    """
    items = list(None)
    # A REPRODUCIBLE shuffle is the whole point (a failing order must replay
    # exactly); this is not a security context, so the stdlib PRNG is correct.
    random.Random(seed).shuffle(items)  # noqa: S311  # reproducibility, not cryptography
    return items


def x_shuffled_order__mutmut_3(node_ids: Sequence[str], seed: int) -> list[str]:
    """A reproducible reordering of ``node_ids`` under ``seed``.

    Deterministic in ``seed`` (its own ``random.Random``), so an order-dependent
    failure reproduces exactly rather than intermittently.
    """
    items = list(node_ids)
    # A REPRODUCIBLE shuffle is the whole point (a failing order must replay
    # exactly); this is not a security context, so the stdlib PRNG is correct.
    random.Random(seed).shuffle(None)  # noqa: S311  # reproducibility, not cryptography
    return items


def x_shuffled_order__mutmut_4(node_ids: Sequence[str], seed: int) -> list[str]:
    """A reproducible reordering of ``node_ids`` under ``seed``.

    Deterministic in ``seed`` (its own ``random.Random``), so an order-dependent
    failure reproduces exactly rather than intermittently.
    """
    items = list(node_ids)
    # A REPRODUCIBLE shuffle is the whole point (a failing order must replay
    # exactly); this is not a security context, so the stdlib PRNG is correct.
    random.Random(None).shuffle(items)  # noqa: S311  # reproducibility, not cryptography
    return items

mutants_x_shuffled_order__mutmut['_mutmut_orig'] = x_shuffled_order__mutmut_orig # type: ignore # mutmut generated
mutants_x_shuffled_order__mutmut['x_shuffled_order__mutmut_1'] = x_shuffled_order__mutmut_1 # type: ignore # mutmut generated
mutants_x_shuffled_order__mutmut['x_shuffled_order__mutmut_2'] = x_shuffled_order__mutmut_2 # type: ignore # mutmut generated
mutants_x_shuffled_order__mutmut['x_shuffled_order__mutmut_3'] = x_shuffled_order__mutmut_3 # type: ignore # mutmut generated
mutants_x_shuffled_order__mutmut['x_shuffled_order__mutmut_4'] = x_shuffled_order__mutmut_4 # type: ignore # mutmut generated
mutants_x_plan_runs__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_plan_runs__mutmut)
def plan_runs(repeats: int, order_seeds: Sequence[int]) -> list[RunSpec]:
    """Build the run plan: ``repeats`` natural-order runs + one per order seed."""
    plan = [RunSpec(label=f"fixed-seed:rep{i + 1}", order_seed=None) for i in range(max(repeats, 1))]
    plan += [RunSpec(label=f"order:seed{seed}", order_seed=seed) for seed in order_seeds]
    return plan


def x_plan_runs__mutmut_orig(repeats: int, order_seeds: Sequence[int]) -> list[RunSpec]:
    """Build the run plan: ``repeats`` natural-order runs + one per order seed."""
    plan = [RunSpec(label=f"fixed-seed:rep{i + 1}", order_seed=None) for i in range(max(repeats, 1))]
    plan += [RunSpec(label=f"order:seed{seed}", order_seed=seed) for seed in order_seeds]
    return plan


def x_plan_runs__mutmut_1(repeats: int, order_seeds: Sequence[int]) -> list[RunSpec]:
    """Build the run plan: ``repeats`` natural-order runs + one per order seed."""
    plan = None
    plan += [RunSpec(label=f"order:seed{seed}", order_seed=seed) for seed in order_seeds]
    return plan


def x_plan_runs__mutmut_2(repeats: int, order_seeds: Sequence[int]) -> list[RunSpec]:
    """Build the run plan: ``repeats`` natural-order runs + one per order seed."""
    plan = [RunSpec(label=None, order_seed=None) for i in range(max(repeats, 1))]
    plan += [RunSpec(label=f"order:seed{seed}", order_seed=seed) for seed in order_seeds]
    return plan


def x_plan_runs__mutmut_3(repeats: int, order_seeds: Sequence[int]) -> list[RunSpec]:
    """Build the run plan: ``repeats`` natural-order runs + one per order seed."""
    plan = [RunSpec(order_seed=None) for i in range(max(repeats, 1))]
    plan += [RunSpec(label=f"order:seed{seed}", order_seed=seed) for seed in order_seeds]
    return plan


def x_plan_runs__mutmut_4(repeats: int, order_seeds: Sequence[int]) -> list[RunSpec]:
    """Build the run plan: ``repeats`` natural-order runs + one per order seed."""
    plan = [RunSpec(label=f"fixed-seed:rep{i + 1}", ) for i in range(max(repeats, 1))]
    plan += [RunSpec(label=f"order:seed{seed}", order_seed=seed) for seed in order_seeds]
    return plan


def x_plan_runs__mutmut_5(repeats: int, order_seeds: Sequence[int]) -> list[RunSpec]:
    """Build the run plan: ``repeats`` natural-order runs + one per order seed."""
    plan = [RunSpec(label=f"fixed-seed:rep{i - 1}", order_seed=None) for i in range(max(repeats, 1))]
    plan += [RunSpec(label=f"order:seed{seed}", order_seed=seed) for seed in order_seeds]
    return plan


def x_plan_runs__mutmut_6(repeats: int, order_seeds: Sequence[int]) -> list[RunSpec]:
    """Build the run plan: ``repeats`` natural-order runs + one per order seed."""
    plan = [RunSpec(label=f"fixed-seed:rep{i + 2}", order_seed=None) for i in range(max(repeats, 1))]
    plan += [RunSpec(label=f"order:seed{seed}", order_seed=seed) for seed in order_seeds]
    return plan


def x_plan_runs__mutmut_7(repeats: int, order_seeds: Sequence[int]) -> list[RunSpec]:
    """Build the run plan: ``repeats`` natural-order runs + one per order seed."""
    plan = [RunSpec(label=f"fixed-seed:rep{i + 1}", order_seed=None) for i in range(None)]
    plan += [RunSpec(label=f"order:seed{seed}", order_seed=seed) for seed in order_seeds]
    return plan


def x_plan_runs__mutmut_8(repeats: int, order_seeds: Sequence[int]) -> list[RunSpec]:
    """Build the run plan: ``repeats`` natural-order runs + one per order seed."""
    plan = [RunSpec(label=f"fixed-seed:rep{i + 1}", order_seed=None) for i in range(max(None, 1))]
    plan += [RunSpec(label=f"order:seed{seed}", order_seed=seed) for seed in order_seeds]
    return plan


def x_plan_runs__mutmut_9(repeats: int, order_seeds: Sequence[int]) -> list[RunSpec]:
    """Build the run plan: ``repeats`` natural-order runs + one per order seed."""
    plan = [RunSpec(label=f"fixed-seed:rep{i + 1}", order_seed=None) for i in range(max(repeats, None))]
    plan += [RunSpec(label=f"order:seed{seed}", order_seed=seed) for seed in order_seeds]
    return plan


def x_plan_runs__mutmut_10(repeats: int, order_seeds: Sequence[int]) -> list[RunSpec]:
    """Build the run plan: ``repeats`` natural-order runs + one per order seed."""
    plan = [RunSpec(label=f"fixed-seed:rep{i + 1}", order_seed=None) for i in range(max(1))]
    plan += [RunSpec(label=f"order:seed{seed}", order_seed=seed) for seed in order_seeds]
    return plan


def x_plan_runs__mutmut_11(repeats: int, order_seeds: Sequence[int]) -> list[RunSpec]:
    """Build the run plan: ``repeats`` natural-order runs + one per order seed."""
    plan = [RunSpec(label=f"fixed-seed:rep{i + 1}", order_seed=None) for i in range(max(repeats, ))]
    plan += [RunSpec(label=f"order:seed{seed}", order_seed=seed) for seed in order_seeds]
    return plan


def x_plan_runs__mutmut_12(repeats: int, order_seeds: Sequence[int]) -> list[RunSpec]:
    """Build the run plan: ``repeats`` natural-order runs + one per order seed."""
    plan = [RunSpec(label=f"fixed-seed:rep{i + 1}", order_seed=None) for i in range(max(repeats, 2))]
    plan += [RunSpec(label=f"order:seed{seed}", order_seed=seed) for seed in order_seeds]
    return plan


def x_plan_runs__mutmut_13(repeats: int, order_seeds: Sequence[int]) -> list[RunSpec]:
    """Build the run plan: ``repeats`` natural-order runs + one per order seed."""
    plan = [RunSpec(label=f"fixed-seed:rep{i + 1}", order_seed=None) for i in range(max(repeats, 1))]
    plan = [RunSpec(label=f"order:seed{seed}", order_seed=seed) for seed in order_seeds]
    return plan


def x_plan_runs__mutmut_14(repeats: int, order_seeds: Sequence[int]) -> list[RunSpec]:
    """Build the run plan: ``repeats`` natural-order runs + one per order seed."""
    plan = [RunSpec(label=f"fixed-seed:rep{i + 1}", order_seed=None) for i in range(max(repeats, 1))]
    plan -= [RunSpec(label=f"order:seed{seed}", order_seed=seed) for seed in order_seeds]
    return plan


def x_plan_runs__mutmut_15(repeats: int, order_seeds: Sequence[int]) -> list[RunSpec]:
    """Build the run plan: ``repeats`` natural-order runs + one per order seed."""
    plan = [RunSpec(label=f"fixed-seed:rep{i + 1}", order_seed=None) for i in range(max(repeats, 1))]
    plan += [RunSpec(label=None, order_seed=seed) for seed in order_seeds]
    return plan


def x_plan_runs__mutmut_16(repeats: int, order_seeds: Sequence[int]) -> list[RunSpec]:
    """Build the run plan: ``repeats`` natural-order runs + one per order seed."""
    plan = [RunSpec(label=f"fixed-seed:rep{i + 1}", order_seed=None) for i in range(max(repeats, 1))]
    plan += [RunSpec(label=f"order:seed{seed}", order_seed=None) for seed in order_seeds]
    return plan


def x_plan_runs__mutmut_17(repeats: int, order_seeds: Sequence[int]) -> list[RunSpec]:
    """Build the run plan: ``repeats`` natural-order runs + one per order seed."""
    plan = [RunSpec(label=f"fixed-seed:rep{i + 1}", order_seed=None) for i in range(max(repeats, 1))]
    plan += [RunSpec(order_seed=seed) for seed in order_seeds]
    return plan


def x_plan_runs__mutmut_18(repeats: int, order_seeds: Sequence[int]) -> list[RunSpec]:
    """Build the run plan: ``repeats`` natural-order runs + one per order seed."""
    plan = [RunSpec(label=f"fixed-seed:rep{i + 1}", order_seed=None) for i in range(max(repeats, 1))]
    plan += [RunSpec(label=f"order:seed{seed}", ) for seed in order_seeds]
    return plan

mutants_x_plan_runs__mutmut['_mutmut_orig'] = x_plan_runs__mutmut_orig # type: ignore # mutmut generated
mutants_x_plan_runs__mutmut['x_plan_runs__mutmut_1'] = x_plan_runs__mutmut_1 # type: ignore # mutmut generated
mutants_x_plan_runs__mutmut['x_plan_runs__mutmut_2'] = x_plan_runs__mutmut_2 # type: ignore # mutmut generated
mutants_x_plan_runs__mutmut['x_plan_runs__mutmut_3'] = x_plan_runs__mutmut_3 # type: ignore # mutmut generated
mutants_x_plan_runs__mutmut['x_plan_runs__mutmut_4'] = x_plan_runs__mutmut_4 # type: ignore # mutmut generated
mutants_x_plan_runs__mutmut['x_plan_runs__mutmut_5'] = x_plan_runs__mutmut_5 # type: ignore # mutmut generated
mutants_x_plan_runs__mutmut['x_plan_runs__mutmut_6'] = x_plan_runs__mutmut_6 # type: ignore # mutmut generated
mutants_x_plan_runs__mutmut['x_plan_runs__mutmut_7'] = x_plan_runs__mutmut_7 # type: ignore # mutmut generated
mutants_x_plan_runs__mutmut['x_plan_runs__mutmut_8'] = x_plan_runs__mutmut_8 # type: ignore # mutmut generated
mutants_x_plan_runs__mutmut['x_plan_runs__mutmut_9'] = x_plan_runs__mutmut_9 # type: ignore # mutmut generated
mutants_x_plan_runs__mutmut['x_plan_runs__mutmut_10'] = x_plan_runs__mutmut_10 # type: ignore # mutmut generated
mutants_x_plan_runs__mutmut['x_plan_runs__mutmut_11'] = x_plan_runs__mutmut_11 # type: ignore # mutmut generated
mutants_x_plan_runs__mutmut['x_plan_runs__mutmut_12'] = x_plan_runs__mutmut_12 # type: ignore # mutmut generated
mutants_x_plan_runs__mutmut['x_plan_runs__mutmut_13'] = x_plan_runs__mutmut_13 # type: ignore # mutmut generated
mutants_x_plan_runs__mutmut['x_plan_runs__mutmut_14'] = x_plan_runs__mutmut_14 # type: ignore # mutmut generated
mutants_x_plan_runs__mutmut['x_plan_runs__mutmut_15'] = x_plan_runs__mutmut_15 # type: ignore # mutmut generated
mutants_x_plan_runs__mutmut['x_plan_runs__mutmut_16'] = x_plan_runs__mutmut_16 # type: ignore # mutmut generated
mutants_x_plan_runs__mutmut['x_plan_runs__mutmut_17'] = x_plan_runs__mutmut_17 # type: ignore # mutmut generated
mutants_x_plan_runs__mutmut['x_plan_runs__mutmut_18'] = x_plan_runs__mutmut_18 # type: ignore # mutmut generated
mutants_x_compare_runs__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_compare_runs__mutmut)
def compare_runs(runs: Sequence[tuple[str, Mapping[str, str]]]) -> list[Divergence]:
    """Return the tests whose outcome was not identical across ``runs``.

    ``runs`` is ``(label, {nodeid: outcome})`` in plan order. A test is a
    divergence when the set of outcomes it shows across the runs (with
    :data:`_ABSENT` standing in where a run never ran it) has more than one
    distinct value. The result is sorted by test id for a stable emit.
    """
    all_ids: set[str] = set()
    for _label, outcomes in runs:
        all_ids.update(outcomes)

    divergences: list[Divergence] = []
    for test_id in sorted(all_ids):
        per_run = tuple((label, outcomes.get(test_id, _ABSENT)) for label, outcomes in runs)
        if len({outcome for _label, outcome in per_run}) > 1:
            divergences.append(Divergence(test_id=test_id, outcomes=per_run))
    return divergences


def x_compare_runs__mutmut_orig(runs: Sequence[tuple[str, Mapping[str, str]]]) -> list[Divergence]:
    """Return the tests whose outcome was not identical across ``runs``.

    ``runs`` is ``(label, {nodeid: outcome})`` in plan order. A test is a
    divergence when the set of outcomes it shows across the runs (with
    :data:`_ABSENT` standing in where a run never ran it) has more than one
    distinct value. The result is sorted by test id for a stable emit.
    """
    all_ids: set[str] = set()
    for _label, outcomes in runs:
        all_ids.update(outcomes)

    divergences: list[Divergence] = []
    for test_id in sorted(all_ids):
        per_run = tuple((label, outcomes.get(test_id, _ABSENT)) for label, outcomes in runs)
        if len({outcome for _label, outcome in per_run}) > 1:
            divergences.append(Divergence(test_id=test_id, outcomes=per_run))
    return divergences


def x_compare_runs__mutmut_1(runs: Sequence[tuple[str, Mapping[str, str]]]) -> list[Divergence]:
    """Return the tests whose outcome was not identical across ``runs``.

    ``runs`` is ``(label, {nodeid: outcome})`` in plan order. A test is a
    divergence when the set of outcomes it shows across the runs (with
    :data:`_ABSENT` standing in where a run never ran it) has more than one
    distinct value. The result is sorted by test id for a stable emit.
    """
    all_ids: set[str] = None
    for _label, outcomes in runs:
        all_ids.update(outcomes)

    divergences: list[Divergence] = []
    for test_id in sorted(all_ids):
        per_run = tuple((label, outcomes.get(test_id, _ABSENT)) for label, outcomes in runs)
        if len({outcome for _label, outcome in per_run}) > 1:
            divergences.append(Divergence(test_id=test_id, outcomes=per_run))
    return divergences


def x_compare_runs__mutmut_2(runs: Sequence[tuple[str, Mapping[str, str]]]) -> list[Divergence]:
    """Return the tests whose outcome was not identical across ``runs``.

    ``runs`` is ``(label, {nodeid: outcome})`` in plan order. A test is a
    divergence when the set of outcomes it shows across the runs (with
    :data:`_ABSENT` standing in where a run never ran it) has more than one
    distinct value. The result is sorted by test id for a stable emit.
    """
    all_ids: set[str] = set()
    for _label, outcomes in runs:
        all_ids.update(None)

    divergences: list[Divergence] = []
    for test_id in sorted(all_ids):
        per_run = tuple((label, outcomes.get(test_id, _ABSENT)) for label, outcomes in runs)
        if len({outcome for _label, outcome in per_run}) > 1:
            divergences.append(Divergence(test_id=test_id, outcomes=per_run))
    return divergences


def x_compare_runs__mutmut_3(runs: Sequence[tuple[str, Mapping[str, str]]]) -> list[Divergence]:
    """Return the tests whose outcome was not identical across ``runs``.

    ``runs`` is ``(label, {nodeid: outcome})`` in plan order. A test is a
    divergence when the set of outcomes it shows across the runs (with
    :data:`_ABSENT` standing in where a run never ran it) has more than one
    distinct value. The result is sorted by test id for a stable emit.
    """
    all_ids: set[str] = set()
    for _label, outcomes in runs:
        all_ids.update(outcomes)

    divergences: list[Divergence] = None
    for test_id in sorted(all_ids):
        per_run = tuple((label, outcomes.get(test_id, _ABSENT)) for label, outcomes in runs)
        if len({outcome for _label, outcome in per_run}) > 1:
            divergences.append(Divergence(test_id=test_id, outcomes=per_run))
    return divergences


def x_compare_runs__mutmut_4(runs: Sequence[tuple[str, Mapping[str, str]]]) -> list[Divergence]:
    """Return the tests whose outcome was not identical across ``runs``.

    ``runs`` is ``(label, {nodeid: outcome})`` in plan order. A test is a
    divergence when the set of outcomes it shows across the runs (with
    :data:`_ABSENT` standing in where a run never ran it) has more than one
    distinct value. The result is sorted by test id for a stable emit.
    """
    all_ids: set[str] = set()
    for _label, outcomes in runs:
        all_ids.update(outcomes)

    divergences: list[Divergence] = []
    for test_id in sorted(None):
        per_run = tuple((label, outcomes.get(test_id, _ABSENT)) for label, outcomes in runs)
        if len({outcome for _label, outcome in per_run}) > 1:
            divergences.append(Divergence(test_id=test_id, outcomes=per_run))
    return divergences


def x_compare_runs__mutmut_5(runs: Sequence[tuple[str, Mapping[str, str]]]) -> list[Divergence]:
    """Return the tests whose outcome was not identical across ``runs``.

    ``runs`` is ``(label, {nodeid: outcome})`` in plan order. A test is a
    divergence when the set of outcomes it shows across the runs (with
    :data:`_ABSENT` standing in where a run never ran it) has more than one
    distinct value. The result is sorted by test id for a stable emit.
    """
    all_ids: set[str] = set()
    for _label, outcomes in runs:
        all_ids.update(outcomes)

    divergences: list[Divergence] = []
    for test_id in sorted(all_ids):
        per_run = None
        if len({outcome for _label, outcome in per_run}) > 1:
            divergences.append(Divergence(test_id=test_id, outcomes=per_run))
    return divergences


def x_compare_runs__mutmut_6(runs: Sequence[tuple[str, Mapping[str, str]]]) -> list[Divergence]:
    """Return the tests whose outcome was not identical across ``runs``.

    ``runs`` is ``(label, {nodeid: outcome})`` in plan order. A test is a
    divergence when the set of outcomes it shows across the runs (with
    :data:`_ABSENT` standing in where a run never ran it) has more than one
    distinct value. The result is sorted by test id for a stable emit.
    """
    all_ids: set[str] = set()
    for _label, outcomes in runs:
        all_ids.update(outcomes)

    divergences: list[Divergence] = []
    for test_id in sorted(all_ids):
        per_run = tuple(None)
        if len({outcome for _label, outcome in per_run}) > 1:
            divergences.append(Divergence(test_id=test_id, outcomes=per_run))
    return divergences


def x_compare_runs__mutmut_7(runs: Sequence[tuple[str, Mapping[str, str]]]) -> list[Divergence]:
    """Return the tests whose outcome was not identical across ``runs``.

    ``runs`` is ``(label, {nodeid: outcome})`` in plan order. A test is a
    divergence when the set of outcomes it shows across the runs (with
    :data:`_ABSENT` standing in where a run never ran it) has more than one
    distinct value. The result is sorted by test id for a stable emit.
    """
    all_ids: set[str] = set()
    for _label, outcomes in runs:
        all_ids.update(outcomes)

    divergences: list[Divergence] = []
    for test_id in sorted(all_ids):
        per_run = tuple((label, outcomes.get(None, _ABSENT)) for label, outcomes in runs)
        if len({outcome for _label, outcome in per_run}) > 1:
            divergences.append(Divergence(test_id=test_id, outcomes=per_run))
    return divergences


def x_compare_runs__mutmut_8(runs: Sequence[tuple[str, Mapping[str, str]]]) -> list[Divergence]:
    """Return the tests whose outcome was not identical across ``runs``.

    ``runs`` is ``(label, {nodeid: outcome})`` in plan order. A test is a
    divergence when the set of outcomes it shows across the runs (with
    :data:`_ABSENT` standing in where a run never ran it) has more than one
    distinct value. The result is sorted by test id for a stable emit.
    """
    all_ids: set[str] = set()
    for _label, outcomes in runs:
        all_ids.update(outcomes)

    divergences: list[Divergence] = []
    for test_id in sorted(all_ids):
        per_run = tuple((label, outcomes.get(test_id, None)) for label, outcomes in runs)
        if len({outcome for _label, outcome in per_run}) > 1:
            divergences.append(Divergence(test_id=test_id, outcomes=per_run))
    return divergences


def x_compare_runs__mutmut_9(runs: Sequence[tuple[str, Mapping[str, str]]]) -> list[Divergence]:
    """Return the tests whose outcome was not identical across ``runs``.

    ``runs`` is ``(label, {nodeid: outcome})`` in plan order. A test is a
    divergence when the set of outcomes it shows across the runs (with
    :data:`_ABSENT` standing in where a run never ran it) has more than one
    distinct value. The result is sorted by test id for a stable emit.
    """
    all_ids: set[str] = set()
    for _label, outcomes in runs:
        all_ids.update(outcomes)

    divergences: list[Divergence] = []
    for test_id in sorted(all_ids):
        per_run = tuple((label, outcomes.get(_ABSENT)) for label, outcomes in runs)
        if len({outcome for _label, outcome in per_run}) > 1:
            divergences.append(Divergence(test_id=test_id, outcomes=per_run))
    return divergences


def x_compare_runs__mutmut_10(runs: Sequence[tuple[str, Mapping[str, str]]]) -> list[Divergence]:
    """Return the tests whose outcome was not identical across ``runs``.

    ``runs`` is ``(label, {nodeid: outcome})`` in plan order. A test is a
    divergence when the set of outcomes it shows across the runs (with
    :data:`_ABSENT` standing in where a run never ran it) has more than one
    distinct value. The result is sorted by test id for a stable emit.
    """
    all_ids: set[str] = set()
    for _label, outcomes in runs:
        all_ids.update(outcomes)

    divergences: list[Divergence] = []
    for test_id in sorted(all_ids):
        per_run = tuple((label, outcomes.get(test_id, )) for label, outcomes in runs)
        if len({outcome for _label, outcome in per_run}) > 1:
            divergences.append(Divergence(test_id=test_id, outcomes=per_run))
    return divergences


def x_compare_runs__mutmut_11(runs: Sequence[tuple[str, Mapping[str, str]]]) -> list[Divergence]:
    """Return the tests whose outcome was not identical across ``runs``.

    ``runs`` is ``(label, {nodeid: outcome})`` in plan order. A test is a
    divergence when the set of outcomes it shows across the runs (with
    :data:`_ABSENT` standing in where a run never ran it) has more than one
    distinct value. The result is sorted by test id for a stable emit.
    """
    all_ids: set[str] = set()
    for _label, outcomes in runs:
        all_ids.update(outcomes)

    divergences: list[Divergence] = []
    for test_id in sorted(all_ids):
        per_run = tuple((label, outcomes.get(test_id, _ABSENT)) for label, outcomes in runs)
        if len({outcome for _label, outcome in per_run}) >= 1:
            divergences.append(Divergence(test_id=test_id, outcomes=per_run))
    return divergences


def x_compare_runs__mutmut_12(runs: Sequence[tuple[str, Mapping[str, str]]]) -> list[Divergence]:
    """Return the tests whose outcome was not identical across ``runs``.

    ``runs`` is ``(label, {nodeid: outcome})`` in plan order. A test is a
    divergence when the set of outcomes it shows across the runs (with
    :data:`_ABSENT` standing in where a run never ran it) has more than one
    distinct value. The result is sorted by test id for a stable emit.
    """
    all_ids: set[str] = set()
    for _label, outcomes in runs:
        all_ids.update(outcomes)

    divergences: list[Divergence] = []
    for test_id in sorted(all_ids):
        per_run = tuple((label, outcomes.get(test_id, _ABSENT)) for label, outcomes in runs)
        if len({outcome for _label, outcome in per_run}) > 2:
            divergences.append(Divergence(test_id=test_id, outcomes=per_run))
    return divergences


def x_compare_runs__mutmut_13(runs: Sequence[tuple[str, Mapping[str, str]]]) -> list[Divergence]:
    """Return the tests whose outcome was not identical across ``runs``.

    ``runs`` is ``(label, {nodeid: outcome})`` in plan order. A test is a
    divergence when the set of outcomes it shows across the runs (with
    :data:`_ABSENT` standing in where a run never ran it) has more than one
    distinct value. The result is sorted by test id for a stable emit.
    """
    all_ids: set[str] = set()
    for _label, outcomes in runs:
        all_ids.update(outcomes)

    divergences: list[Divergence] = []
    for test_id in sorted(all_ids):
        per_run = tuple((label, outcomes.get(test_id, _ABSENT)) for label, outcomes in runs)
        if len({outcome for _label, outcome in per_run}) > 1:
            divergences.append(None)
    return divergences


def x_compare_runs__mutmut_14(runs: Sequence[tuple[str, Mapping[str, str]]]) -> list[Divergence]:
    """Return the tests whose outcome was not identical across ``runs``.

    ``runs`` is ``(label, {nodeid: outcome})`` in plan order. A test is a
    divergence when the set of outcomes it shows across the runs (with
    :data:`_ABSENT` standing in where a run never ran it) has more than one
    distinct value. The result is sorted by test id for a stable emit.
    """
    all_ids: set[str] = set()
    for _label, outcomes in runs:
        all_ids.update(outcomes)

    divergences: list[Divergence] = []
    for test_id in sorted(all_ids):
        per_run = tuple((label, outcomes.get(test_id, _ABSENT)) for label, outcomes in runs)
        if len({outcome for _label, outcome in per_run}) > 1:
            divergences.append(Divergence(test_id=None, outcomes=per_run))
    return divergences


def x_compare_runs__mutmut_15(runs: Sequence[tuple[str, Mapping[str, str]]]) -> list[Divergence]:
    """Return the tests whose outcome was not identical across ``runs``.

    ``runs`` is ``(label, {nodeid: outcome})`` in plan order. A test is a
    divergence when the set of outcomes it shows across the runs (with
    :data:`_ABSENT` standing in where a run never ran it) has more than one
    distinct value. The result is sorted by test id for a stable emit.
    """
    all_ids: set[str] = set()
    for _label, outcomes in runs:
        all_ids.update(outcomes)

    divergences: list[Divergence] = []
    for test_id in sorted(all_ids):
        per_run = tuple((label, outcomes.get(test_id, _ABSENT)) for label, outcomes in runs)
        if len({outcome for _label, outcome in per_run}) > 1:
            divergences.append(Divergence(test_id=test_id, outcomes=None))
    return divergences


def x_compare_runs__mutmut_16(runs: Sequence[tuple[str, Mapping[str, str]]]) -> list[Divergence]:
    """Return the tests whose outcome was not identical across ``runs``.

    ``runs`` is ``(label, {nodeid: outcome})`` in plan order. A test is a
    divergence when the set of outcomes it shows across the runs (with
    :data:`_ABSENT` standing in where a run never ran it) has more than one
    distinct value. The result is sorted by test id for a stable emit.
    """
    all_ids: set[str] = set()
    for _label, outcomes in runs:
        all_ids.update(outcomes)

    divergences: list[Divergence] = []
    for test_id in sorted(all_ids):
        per_run = tuple((label, outcomes.get(test_id, _ABSENT)) for label, outcomes in runs)
        if len({outcome for _label, outcome in per_run}) > 1:
            divergences.append(Divergence(outcomes=per_run))
    return divergences


def x_compare_runs__mutmut_17(runs: Sequence[tuple[str, Mapping[str, str]]]) -> list[Divergence]:
    """Return the tests whose outcome was not identical across ``runs``.

    ``runs`` is ``(label, {nodeid: outcome})`` in plan order. A test is a
    divergence when the set of outcomes it shows across the runs (with
    :data:`_ABSENT` standing in where a run never ran it) has more than one
    distinct value. The result is sorted by test id for a stable emit.
    """
    all_ids: set[str] = set()
    for _label, outcomes in runs:
        all_ids.update(outcomes)

    divergences: list[Divergence] = []
    for test_id in sorted(all_ids):
        per_run = tuple((label, outcomes.get(test_id, _ABSENT)) for label, outcomes in runs)
        if len({outcome for _label, outcome in per_run}) > 1:
            divergences.append(Divergence(test_id=test_id, ))
    return divergences

mutants_x_compare_runs__mutmut['_mutmut_orig'] = x_compare_runs__mutmut_orig # type: ignore # mutmut generated
mutants_x_compare_runs__mutmut['x_compare_runs__mutmut_1'] = x_compare_runs__mutmut_1 # type: ignore # mutmut generated
mutants_x_compare_runs__mutmut['x_compare_runs__mutmut_2'] = x_compare_runs__mutmut_2 # type: ignore # mutmut generated
mutants_x_compare_runs__mutmut['x_compare_runs__mutmut_3'] = x_compare_runs__mutmut_3 # type: ignore # mutmut generated
mutants_x_compare_runs__mutmut['x_compare_runs__mutmut_4'] = x_compare_runs__mutmut_4 # type: ignore # mutmut generated
mutants_x_compare_runs__mutmut['x_compare_runs__mutmut_5'] = x_compare_runs__mutmut_5 # type: ignore # mutmut generated
mutants_x_compare_runs__mutmut['x_compare_runs__mutmut_6'] = x_compare_runs__mutmut_6 # type: ignore # mutmut generated
mutants_x_compare_runs__mutmut['x_compare_runs__mutmut_7'] = x_compare_runs__mutmut_7 # type: ignore # mutmut generated
mutants_x_compare_runs__mutmut['x_compare_runs__mutmut_8'] = x_compare_runs__mutmut_8 # type: ignore # mutmut generated
mutants_x_compare_runs__mutmut['x_compare_runs__mutmut_9'] = x_compare_runs__mutmut_9 # type: ignore # mutmut generated
mutants_x_compare_runs__mutmut['x_compare_runs__mutmut_10'] = x_compare_runs__mutmut_10 # type: ignore # mutmut generated
mutants_x_compare_runs__mutmut['x_compare_runs__mutmut_11'] = x_compare_runs__mutmut_11 # type: ignore # mutmut generated
mutants_x_compare_runs__mutmut['x_compare_runs__mutmut_12'] = x_compare_runs__mutmut_12 # type: ignore # mutmut generated
mutants_x_compare_runs__mutmut['x_compare_runs__mutmut_13'] = x_compare_runs__mutmut_13 # type: ignore # mutmut generated
mutants_x_compare_runs__mutmut['x_compare_runs__mutmut_14'] = x_compare_runs__mutmut_14 # type: ignore # mutmut generated
mutants_x_compare_runs__mutmut['x_compare_runs__mutmut_15'] = x_compare_runs__mutmut_15 # type: ignore # mutmut generated
mutants_x_compare_runs__mutmut['x_compare_runs__mutmut_16'] = x_compare_runs__mutmut_16 # type: ignore # mutmut generated
mutants_x_compare_runs__mutmut['x_compare_runs__mutmut_17'] = x_compare_runs__mutmut_17 # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build_pytest_argv__mutmut)
def build_pytest_argv(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "-v",
        "--color=no",
        "-p",
        "no:cacheprovider",
        "-p",
        "no:rerunfailures",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv += ["--randomly-seed", str(order_seed if order_seed is not None else DEFAULT_SEED)]
        argv += list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv += ["-p", "no:randomly"]
        if order_seed is None or not node_ids:
            argv += list(test_paths)
        else:
            argv += shuffled_order(node_ids, order_seed)
    return argv


def x_build_pytest_argv__mutmut_orig(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "-v",
        "--color=no",
        "-p",
        "no:cacheprovider",
        "-p",
        "no:rerunfailures",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv += ["--randomly-seed", str(order_seed if order_seed is not None else DEFAULT_SEED)]
        argv += list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv += ["-p", "no:randomly"]
        if order_seed is None or not node_ids:
            argv += list(test_paths)
        else:
            argv += shuffled_order(node_ids, order_seed)
    return argv


def x_build_pytest_argv__mutmut_1(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = None
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv += ["--randomly-seed", str(order_seed if order_seed is not None else DEFAULT_SEED)]
        argv += list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv += ["-p", "no:randomly"]
        if order_seed is None or not node_ids:
            argv += list(test_paths)
        else:
            argv += shuffled_order(node_ids, order_seed)
    return argv


def x_build_pytest_argv__mutmut_2(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "XX-vXX",
        "--color=no",
        "-p",
        "no:cacheprovider",
        "-p",
        "no:rerunfailures",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv += ["--randomly-seed", str(order_seed if order_seed is not None else DEFAULT_SEED)]
        argv += list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv += ["-p", "no:randomly"]
        if order_seed is None or not node_ids:
            argv += list(test_paths)
        else:
            argv += shuffled_order(node_ids, order_seed)
    return argv


def x_build_pytest_argv__mutmut_3(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "-V",
        "--color=no",
        "-p",
        "no:cacheprovider",
        "-p",
        "no:rerunfailures",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv += ["--randomly-seed", str(order_seed if order_seed is not None else DEFAULT_SEED)]
        argv += list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv += ["-p", "no:randomly"]
        if order_seed is None or not node_ids:
            argv += list(test_paths)
        else:
            argv += shuffled_order(node_ids, order_seed)
    return argv


def x_build_pytest_argv__mutmut_4(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "-v",
        "XX--color=noXX",
        "-p",
        "no:cacheprovider",
        "-p",
        "no:rerunfailures",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv += ["--randomly-seed", str(order_seed if order_seed is not None else DEFAULT_SEED)]
        argv += list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv += ["-p", "no:randomly"]
        if order_seed is None or not node_ids:
            argv += list(test_paths)
        else:
            argv += shuffled_order(node_ids, order_seed)
    return argv


def x_build_pytest_argv__mutmut_5(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "-v",
        "--COLOR=NO",
        "-p",
        "no:cacheprovider",
        "-p",
        "no:rerunfailures",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv += ["--randomly-seed", str(order_seed if order_seed is not None else DEFAULT_SEED)]
        argv += list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv += ["-p", "no:randomly"]
        if order_seed is None or not node_ids:
            argv += list(test_paths)
        else:
            argv += shuffled_order(node_ids, order_seed)
    return argv


def x_build_pytest_argv__mutmut_6(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "-v",
        "--color=no",
        "XX-pXX",
        "no:cacheprovider",
        "-p",
        "no:rerunfailures",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv += ["--randomly-seed", str(order_seed if order_seed is not None else DEFAULT_SEED)]
        argv += list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv += ["-p", "no:randomly"]
        if order_seed is None or not node_ids:
            argv += list(test_paths)
        else:
            argv += shuffled_order(node_ids, order_seed)
    return argv


def x_build_pytest_argv__mutmut_7(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "-v",
        "--color=no",
        "-P",
        "no:cacheprovider",
        "-p",
        "no:rerunfailures",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv += ["--randomly-seed", str(order_seed if order_seed is not None else DEFAULT_SEED)]
        argv += list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv += ["-p", "no:randomly"]
        if order_seed is None or not node_ids:
            argv += list(test_paths)
        else:
            argv += shuffled_order(node_ids, order_seed)
    return argv


def x_build_pytest_argv__mutmut_8(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "-v",
        "--color=no",
        "-p",
        "XXno:cacheproviderXX",
        "-p",
        "no:rerunfailures",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv += ["--randomly-seed", str(order_seed if order_seed is not None else DEFAULT_SEED)]
        argv += list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv += ["-p", "no:randomly"]
        if order_seed is None or not node_ids:
            argv += list(test_paths)
        else:
            argv += shuffled_order(node_ids, order_seed)
    return argv


def x_build_pytest_argv__mutmut_9(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "-v",
        "--color=no",
        "-p",
        "NO:CACHEPROVIDER",
        "-p",
        "no:rerunfailures",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv += ["--randomly-seed", str(order_seed if order_seed is not None else DEFAULT_SEED)]
        argv += list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv += ["-p", "no:randomly"]
        if order_seed is None or not node_ids:
            argv += list(test_paths)
        else:
            argv += shuffled_order(node_ids, order_seed)
    return argv


def x_build_pytest_argv__mutmut_10(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "-v",
        "--color=no",
        "-p",
        "no:cacheprovider",
        "XX-pXX",
        "no:rerunfailures",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv += ["--randomly-seed", str(order_seed if order_seed is not None else DEFAULT_SEED)]
        argv += list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv += ["-p", "no:randomly"]
        if order_seed is None or not node_ids:
            argv += list(test_paths)
        else:
            argv += shuffled_order(node_ids, order_seed)
    return argv


def x_build_pytest_argv__mutmut_11(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "-v",
        "--color=no",
        "-p",
        "no:cacheprovider",
        "-P",
        "no:rerunfailures",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv += ["--randomly-seed", str(order_seed if order_seed is not None else DEFAULT_SEED)]
        argv += list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv += ["-p", "no:randomly"]
        if order_seed is None or not node_ids:
            argv += list(test_paths)
        else:
            argv += shuffled_order(node_ids, order_seed)
    return argv


def x_build_pytest_argv__mutmut_12(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "-v",
        "--color=no",
        "-p",
        "no:cacheprovider",
        "-p",
        "XXno:rerunfailuresXX",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv += ["--randomly-seed", str(order_seed if order_seed is not None else DEFAULT_SEED)]
        argv += list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv += ["-p", "no:randomly"]
        if order_seed is None or not node_ids:
            argv += list(test_paths)
        else:
            argv += shuffled_order(node_ids, order_seed)
    return argv


def x_build_pytest_argv__mutmut_13(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "-v",
        "--color=no",
        "-p",
        "no:cacheprovider",
        "-p",
        "NO:RERUNFAILURES",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv += ["--randomly-seed", str(order_seed if order_seed is not None else DEFAULT_SEED)]
        argv += list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv += ["-p", "no:randomly"]
        if order_seed is None or not node_ids:
            argv += list(test_paths)
        else:
            argv += shuffled_order(node_ids, order_seed)
    return argv


def x_build_pytest_argv__mutmut_14(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "-v",
        "--color=no",
        "-p",
        "no:cacheprovider",
        "-p",
        "no:rerunfailures",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv = ["--randomly-seed", str(order_seed if order_seed is not None else DEFAULT_SEED)]
        argv += list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv += ["-p", "no:randomly"]
        if order_seed is None or not node_ids:
            argv += list(test_paths)
        else:
            argv += shuffled_order(node_ids, order_seed)
    return argv


def x_build_pytest_argv__mutmut_15(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "-v",
        "--color=no",
        "-p",
        "no:cacheprovider",
        "-p",
        "no:rerunfailures",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv -= ["--randomly-seed", str(order_seed if order_seed is not None else DEFAULT_SEED)]
        argv += list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv += ["-p", "no:randomly"]
        if order_seed is None or not node_ids:
            argv += list(test_paths)
        else:
            argv += shuffled_order(node_ids, order_seed)
    return argv


def x_build_pytest_argv__mutmut_16(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "-v",
        "--color=no",
        "-p",
        "no:cacheprovider",
        "-p",
        "no:rerunfailures",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv += ["XX--randomly-seedXX", str(order_seed if order_seed is not None else DEFAULT_SEED)]
        argv += list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv += ["-p", "no:randomly"]
        if order_seed is None or not node_ids:
            argv += list(test_paths)
        else:
            argv += shuffled_order(node_ids, order_seed)
    return argv


def x_build_pytest_argv__mutmut_17(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "-v",
        "--color=no",
        "-p",
        "no:cacheprovider",
        "-p",
        "no:rerunfailures",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv += ["--RANDOMLY-SEED", str(order_seed if order_seed is not None else DEFAULT_SEED)]
        argv += list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv += ["-p", "no:randomly"]
        if order_seed is None or not node_ids:
            argv += list(test_paths)
        else:
            argv += shuffled_order(node_ids, order_seed)
    return argv


def x_build_pytest_argv__mutmut_18(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "-v",
        "--color=no",
        "-p",
        "no:cacheprovider",
        "-p",
        "no:rerunfailures",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv += ["--randomly-seed", str(None)]
        argv += list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv += ["-p", "no:randomly"]
        if order_seed is None or not node_ids:
            argv += list(test_paths)
        else:
            argv += shuffled_order(node_ids, order_seed)
    return argv


def x_build_pytest_argv__mutmut_19(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "-v",
        "--color=no",
        "-p",
        "no:cacheprovider",
        "-p",
        "no:rerunfailures",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv += ["--randomly-seed", str(order_seed if order_seed is None else DEFAULT_SEED)]
        argv += list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv += ["-p", "no:randomly"]
        if order_seed is None or not node_ids:
            argv += list(test_paths)
        else:
            argv += shuffled_order(node_ids, order_seed)
    return argv


def x_build_pytest_argv__mutmut_20(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "-v",
        "--color=no",
        "-p",
        "no:cacheprovider",
        "-p",
        "no:rerunfailures",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv += ["--randomly-seed", str(order_seed if order_seed is not None else DEFAULT_SEED)]
        argv = list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv += ["-p", "no:randomly"]
        if order_seed is None or not node_ids:
            argv += list(test_paths)
        else:
            argv += shuffled_order(node_ids, order_seed)
    return argv


def x_build_pytest_argv__mutmut_21(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "-v",
        "--color=no",
        "-p",
        "no:cacheprovider",
        "-p",
        "no:rerunfailures",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv += ["--randomly-seed", str(order_seed if order_seed is not None else DEFAULT_SEED)]
        argv -= list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv += ["-p", "no:randomly"]
        if order_seed is None or not node_ids:
            argv += list(test_paths)
        else:
            argv += shuffled_order(node_ids, order_seed)
    return argv


def x_build_pytest_argv__mutmut_22(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "-v",
        "--color=no",
        "-p",
        "no:cacheprovider",
        "-p",
        "no:rerunfailures",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv += ["--randomly-seed", str(order_seed if order_seed is not None else DEFAULT_SEED)]
        argv += list(None)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv += ["-p", "no:randomly"]
        if order_seed is None or not node_ids:
            argv += list(test_paths)
        else:
            argv += shuffled_order(node_ids, order_seed)
    return argv


def x_build_pytest_argv__mutmut_23(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "-v",
        "--color=no",
        "-p",
        "no:cacheprovider",
        "-p",
        "no:rerunfailures",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv += ["--randomly-seed", str(order_seed if order_seed is not None else DEFAULT_SEED)]
        argv += list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv = ["-p", "no:randomly"]
        if order_seed is None or not node_ids:
            argv += list(test_paths)
        else:
            argv += shuffled_order(node_ids, order_seed)
    return argv


def x_build_pytest_argv__mutmut_24(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "-v",
        "--color=no",
        "-p",
        "no:cacheprovider",
        "-p",
        "no:rerunfailures",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv += ["--randomly-seed", str(order_seed if order_seed is not None else DEFAULT_SEED)]
        argv += list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv -= ["-p", "no:randomly"]
        if order_seed is None or not node_ids:
            argv += list(test_paths)
        else:
            argv += shuffled_order(node_ids, order_seed)
    return argv


def x_build_pytest_argv__mutmut_25(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "-v",
        "--color=no",
        "-p",
        "no:cacheprovider",
        "-p",
        "no:rerunfailures",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv += ["--randomly-seed", str(order_seed if order_seed is not None else DEFAULT_SEED)]
        argv += list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv += ["XX-pXX", "no:randomly"]
        if order_seed is None or not node_ids:
            argv += list(test_paths)
        else:
            argv += shuffled_order(node_ids, order_seed)
    return argv


def x_build_pytest_argv__mutmut_26(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "-v",
        "--color=no",
        "-p",
        "no:cacheprovider",
        "-p",
        "no:rerunfailures",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv += ["--randomly-seed", str(order_seed if order_seed is not None else DEFAULT_SEED)]
        argv += list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv += ["-P", "no:randomly"]
        if order_seed is None or not node_ids:
            argv += list(test_paths)
        else:
            argv += shuffled_order(node_ids, order_seed)
    return argv


def x_build_pytest_argv__mutmut_27(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "-v",
        "--color=no",
        "-p",
        "no:cacheprovider",
        "-p",
        "no:rerunfailures",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv += ["--randomly-seed", str(order_seed if order_seed is not None else DEFAULT_SEED)]
        argv += list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv += ["-p", "XXno:randomlyXX"]
        if order_seed is None or not node_ids:
            argv += list(test_paths)
        else:
            argv += shuffled_order(node_ids, order_seed)
    return argv


def x_build_pytest_argv__mutmut_28(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "-v",
        "--color=no",
        "-p",
        "no:cacheprovider",
        "-p",
        "no:rerunfailures",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv += ["--randomly-seed", str(order_seed if order_seed is not None else DEFAULT_SEED)]
        argv += list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv += ["-p", "NO:RANDOMLY"]
        if order_seed is None or not node_ids:
            argv += list(test_paths)
        else:
            argv += shuffled_order(node_ids, order_seed)
    return argv


def x_build_pytest_argv__mutmut_29(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "-v",
        "--color=no",
        "-p",
        "no:cacheprovider",
        "-p",
        "no:rerunfailures",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv += ["--randomly-seed", str(order_seed if order_seed is not None else DEFAULT_SEED)]
        argv += list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv += ["-p", "no:randomly"]
        if order_seed is None and not node_ids:
            argv += list(test_paths)
        else:
            argv += shuffled_order(node_ids, order_seed)
    return argv


def x_build_pytest_argv__mutmut_30(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "-v",
        "--color=no",
        "-p",
        "no:cacheprovider",
        "-p",
        "no:rerunfailures",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv += ["--randomly-seed", str(order_seed if order_seed is not None else DEFAULT_SEED)]
        argv += list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv += ["-p", "no:randomly"]
        if order_seed is not None or not node_ids:
            argv += list(test_paths)
        else:
            argv += shuffled_order(node_ids, order_seed)
    return argv


def x_build_pytest_argv__mutmut_31(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "-v",
        "--color=no",
        "-p",
        "no:cacheprovider",
        "-p",
        "no:rerunfailures",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv += ["--randomly-seed", str(order_seed if order_seed is not None else DEFAULT_SEED)]
        argv += list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv += ["-p", "no:randomly"]
        if order_seed is None or node_ids:
            argv += list(test_paths)
        else:
            argv += shuffled_order(node_ids, order_seed)
    return argv


def x_build_pytest_argv__mutmut_32(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "-v",
        "--color=no",
        "-p",
        "no:cacheprovider",
        "-p",
        "no:rerunfailures",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv += ["--randomly-seed", str(order_seed if order_seed is not None else DEFAULT_SEED)]
        argv += list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv += ["-p", "no:randomly"]
        if order_seed is None or not node_ids:
            argv = list(test_paths)
        else:
            argv += shuffled_order(node_ids, order_seed)
    return argv


def x_build_pytest_argv__mutmut_33(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "-v",
        "--color=no",
        "-p",
        "no:cacheprovider",
        "-p",
        "no:rerunfailures",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv += ["--randomly-seed", str(order_seed if order_seed is not None else DEFAULT_SEED)]
        argv += list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv += ["-p", "no:randomly"]
        if order_seed is None or not node_ids:
            argv -= list(test_paths)
        else:
            argv += shuffled_order(node_ids, order_seed)
    return argv


def x_build_pytest_argv__mutmut_34(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "-v",
        "--color=no",
        "-p",
        "no:cacheprovider",
        "-p",
        "no:rerunfailures",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv += ["--randomly-seed", str(order_seed if order_seed is not None else DEFAULT_SEED)]
        argv += list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv += ["-p", "no:randomly"]
        if order_seed is None or not node_ids:
            argv += list(None)
        else:
            argv += shuffled_order(node_ids, order_seed)
    return argv


def x_build_pytest_argv__mutmut_35(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "-v",
        "--color=no",
        "-p",
        "no:cacheprovider",
        "-p",
        "no:rerunfailures",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv += ["--randomly-seed", str(order_seed if order_seed is not None else DEFAULT_SEED)]
        argv += list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv += ["-p", "no:randomly"]
        if order_seed is None or not node_ids:
            argv += list(test_paths)
        else:
            argv = shuffled_order(node_ids, order_seed)
    return argv


def x_build_pytest_argv__mutmut_36(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "-v",
        "--color=no",
        "-p",
        "no:cacheprovider",
        "-p",
        "no:rerunfailures",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv += ["--randomly-seed", str(order_seed if order_seed is not None else DEFAULT_SEED)]
        argv += list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv += ["-p", "no:randomly"]
        if order_seed is None or not node_ids:
            argv += list(test_paths)
        else:
            argv -= shuffled_order(node_ids, order_seed)
    return argv


def x_build_pytest_argv__mutmut_37(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "-v",
        "--color=no",
        "-p",
        "no:cacheprovider",
        "-p",
        "no:rerunfailures",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv += ["--randomly-seed", str(order_seed if order_seed is not None else DEFAULT_SEED)]
        argv += list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv += ["-p", "no:randomly"]
        if order_seed is None or not node_ids:
            argv += list(test_paths)
        else:
            argv += shuffled_order(None, order_seed)
    return argv


def x_build_pytest_argv__mutmut_38(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "-v",
        "--color=no",
        "-p",
        "no:cacheprovider",
        "-p",
        "no:rerunfailures",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv += ["--randomly-seed", str(order_seed if order_seed is not None else DEFAULT_SEED)]
        argv += list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv += ["-p", "no:randomly"]
        if order_seed is None or not node_ids:
            argv += list(test_paths)
        else:
            argv += shuffled_order(node_ids, None)
    return argv


def x_build_pytest_argv__mutmut_39(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "-v",
        "--color=no",
        "-p",
        "no:cacheprovider",
        "-p",
        "no:rerunfailures",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv += ["--randomly-seed", str(order_seed if order_seed is not None else DEFAULT_SEED)]
        argv += list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv += ["-p", "no:randomly"]
        if order_seed is None or not node_ids:
            argv += list(test_paths)
        else:
            argv += shuffled_order(order_seed)
    return argv


def x_build_pytest_argv__mutmut_40(
    command: Sequence[str],
    *,
    test_paths: Sequence[str],
    node_ids: Sequence[str] | None,
    order_seed: int | None,
    use_randomly: bool,
) -> list[str]:
    """Assemble the pytest argv for one run.

    Invariants that make the probe trustworthy: verbose per-test reporting with
    no colour (so :func:`parse_outcomes` sees clean lines), the cache provider
    off (no run-to-run cache state), and the rerun plugin explicitly BLOCKED
    (``-p no:rerunfailures``) so a stray ``--reruns`` in the consumer's config
    can never mask a flake mid-probe. When ``use_randomly`` is off, the built-in
    ``pytest-randomly`` shuffle is disabled too so THIS check's ordering is the
    only variable.
    """
    argv = [
        *command,
        "-v",
        "--color=no",
        "-p",
        "no:cacheprovider",
        "-p",
        "no:rerunfailures",
    ]
    if use_randomly:
        # Delegate ordering to pytest-randomly: a natural run pins the base
        # seed (so repeats are identical); an order run uses the probe seed.
        argv += ["--randomly-seed", str(order_seed if order_seed is not None else DEFAULT_SEED)]
        argv += list(test_paths)
    else:
        # Own the ordering: block the randomly plugin, run the natural order by
        # path, or the explicit shuffled node ids for an order probe.
        argv += ["-p", "no:randomly"]
        if order_seed is None or not node_ids:
            argv += list(test_paths)
        else:
            argv += shuffled_order(node_ids, )
    return argv

mutants_x_build_pytest_argv__mutmut['_mutmut_orig'] = x_build_pytest_argv__mutmut_orig # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut['x_build_pytest_argv__mutmut_1'] = x_build_pytest_argv__mutmut_1 # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut['x_build_pytest_argv__mutmut_2'] = x_build_pytest_argv__mutmut_2 # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut['x_build_pytest_argv__mutmut_3'] = x_build_pytest_argv__mutmut_3 # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut['x_build_pytest_argv__mutmut_4'] = x_build_pytest_argv__mutmut_4 # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut['x_build_pytest_argv__mutmut_5'] = x_build_pytest_argv__mutmut_5 # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut['x_build_pytest_argv__mutmut_6'] = x_build_pytest_argv__mutmut_6 # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut['x_build_pytest_argv__mutmut_7'] = x_build_pytest_argv__mutmut_7 # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut['x_build_pytest_argv__mutmut_8'] = x_build_pytest_argv__mutmut_8 # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut['x_build_pytest_argv__mutmut_9'] = x_build_pytest_argv__mutmut_9 # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut['x_build_pytest_argv__mutmut_10'] = x_build_pytest_argv__mutmut_10 # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut['x_build_pytest_argv__mutmut_11'] = x_build_pytest_argv__mutmut_11 # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut['x_build_pytest_argv__mutmut_12'] = x_build_pytest_argv__mutmut_12 # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut['x_build_pytest_argv__mutmut_13'] = x_build_pytest_argv__mutmut_13 # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut['x_build_pytest_argv__mutmut_14'] = x_build_pytest_argv__mutmut_14 # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut['x_build_pytest_argv__mutmut_15'] = x_build_pytest_argv__mutmut_15 # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut['x_build_pytest_argv__mutmut_16'] = x_build_pytest_argv__mutmut_16 # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut['x_build_pytest_argv__mutmut_17'] = x_build_pytest_argv__mutmut_17 # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut['x_build_pytest_argv__mutmut_18'] = x_build_pytest_argv__mutmut_18 # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut['x_build_pytest_argv__mutmut_19'] = x_build_pytest_argv__mutmut_19 # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut['x_build_pytest_argv__mutmut_20'] = x_build_pytest_argv__mutmut_20 # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut['x_build_pytest_argv__mutmut_21'] = x_build_pytest_argv__mutmut_21 # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut['x_build_pytest_argv__mutmut_22'] = x_build_pytest_argv__mutmut_22 # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut['x_build_pytest_argv__mutmut_23'] = x_build_pytest_argv__mutmut_23 # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut['x_build_pytest_argv__mutmut_24'] = x_build_pytest_argv__mutmut_24 # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut['x_build_pytest_argv__mutmut_25'] = x_build_pytest_argv__mutmut_25 # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut['x_build_pytest_argv__mutmut_26'] = x_build_pytest_argv__mutmut_26 # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut['x_build_pytest_argv__mutmut_27'] = x_build_pytest_argv__mutmut_27 # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut['x_build_pytest_argv__mutmut_28'] = x_build_pytest_argv__mutmut_28 # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut['x_build_pytest_argv__mutmut_29'] = x_build_pytest_argv__mutmut_29 # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut['x_build_pytest_argv__mutmut_30'] = x_build_pytest_argv__mutmut_30 # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut['x_build_pytest_argv__mutmut_31'] = x_build_pytest_argv__mutmut_31 # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut['x_build_pytest_argv__mutmut_32'] = x_build_pytest_argv__mutmut_32 # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut['x_build_pytest_argv__mutmut_33'] = x_build_pytest_argv__mutmut_33 # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut['x_build_pytest_argv__mutmut_34'] = x_build_pytest_argv__mutmut_34 # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut['x_build_pytest_argv__mutmut_35'] = x_build_pytest_argv__mutmut_35 # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut['x_build_pytest_argv__mutmut_36'] = x_build_pytest_argv__mutmut_36 # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut['x_build_pytest_argv__mutmut_37'] = x_build_pytest_argv__mutmut_37 # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut['x_build_pytest_argv__mutmut_38'] = x_build_pytest_argv__mutmut_38 # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut['x_build_pytest_argv__mutmut_39'] = x_build_pytest_argv__mutmut_39 # type: ignore # mutmut generated
mutants_x_build_pytest_argv__mutmut['x_build_pytest_argv__mutmut_40'] = x_build_pytest_argv__mutmut_40 # type: ignore # mutmut generated
mutants_x__run_env__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__run_env__mutmut)
def _run_env(seed: int) -> dict[str, str]:
    """The child environment: the current env with ``PYTHONHASHSEED`` pinned."""
    env = dict(os.environ)
    env["PYTHONHASHSEED"] = str(seed)
    return env


def x__run_env__mutmut_orig(seed: int) -> dict[str, str]:
    """The child environment: the current env with ``PYTHONHASHSEED`` pinned."""
    env = dict(os.environ)
    env["PYTHONHASHSEED"] = str(seed)
    return env


def x__run_env__mutmut_1(seed: int) -> dict[str, str]:
    """The child environment: the current env with ``PYTHONHASHSEED`` pinned."""
    env = None
    env["PYTHONHASHSEED"] = str(seed)
    return env


def x__run_env__mutmut_2(seed: int) -> dict[str, str]:
    """The child environment: the current env with ``PYTHONHASHSEED`` pinned."""
    env = dict(None)
    env["PYTHONHASHSEED"] = str(seed)
    return env


def x__run_env__mutmut_3(seed: int) -> dict[str, str]:
    """The child environment: the current env with ``PYTHONHASHSEED`` pinned."""
    env = dict(os.environ)
    env["PYTHONHASHSEED"] = None
    return env


def x__run_env__mutmut_4(seed: int) -> dict[str, str]:
    """The child environment: the current env with ``PYTHONHASHSEED`` pinned."""
    env = dict(os.environ)
    env["XXPYTHONHASHSEEDXX"] = str(seed)
    return env


def x__run_env__mutmut_5(seed: int) -> dict[str, str]:
    """The child environment: the current env with ``PYTHONHASHSEED`` pinned."""
    env = dict(os.environ)
    env["pythonhashseed"] = str(seed)
    return env


def x__run_env__mutmut_6(seed: int) -> dict[str, str]:
    """The child environment: the current env with ``PYTHONHASHSEED`` pinned."""
    env = dict(os.environ)
    env["PYTHONHASHSEED"] = str(None)
    return env

mutants_x__run_env__mutmut['_mutmut_orig'] = x__run_env__mutmut_orig # type: ignore # mutmut generated
mutants_x__run_env__mutmut['x__run_env__mutmut_1'] = x__run_env__mutmut_1 # type: ignore # mutmut generated
mutants_x__run_env__mutmut['x__run_env__mutmut_2'] = x__run_env__mutmut_2 # type: ignore # mutmut generated
mutants_x__run_env__mutmut['x__run_env__mutmut_3'] = x__run_env__mutmut_3 # type: ignore # mutmut generated
mutants_x__run_env__mutmut['x__run_env__mutmut_4'] = x__run_env__mutmut_4 # type: ignore # mutmut generated
mutants_x__run_env__mutmut['x__run_env__mutmut_5'] = x__run_env__mutmut_5 # type: ignore # mutmut generated
mutants_x__run_env__mutmut['x__run_env__mutmut_6'] = x__run_env__mutmut_6 # type: ignore # mutmut generated
mutants_x_collect_node_ids__mutmut: MutantDict = {}  # type: ignore


# --------------------------------------------------------------------------- #
# The real subprocess runner (the dependency-injection seam).
# --------------------------------------------------------------------------- #


@_mutmut_mutated(mutants_x_collect_node_ids__mutmut)
def collect_node_ids(
    command: Sequence[str],
    test_paths: Sequence[str],
    *,
    repo_root: Path,
    seed: int,
    timeout: int,
) -> list[str]:
    """Collect the node ids under ``test_paths`` (for the order probe)."""
    argv = [*command, "--collect-only", "-q", "-p", "no:cacheprovider", "-p", "no:randomly", *test_paths]
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo paths
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:  # pragma: no cover - defensive
        raise SuiteRunError(f"collection timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    return parse_collected(result.stdout)


# --------------------------------------------------------------------------- #
# The real subprocess runner (the dependency-injection seam).
# --------------------------------------------------------------------------- #


def x_collect_node_ids__mutmut_orig(
    command: Sequence[str],
    test_paths: Sequence[str],
    *,
    repo_root: Path,
    seed: int,
    timeout: int,
) -> list[str]:
    """Collect the node ids under ``test_paths`` (for the order probe)."""
    argv = [*command, "--collect-only", "-q", "-p", "no:cacheprovider", "-p", "no:randomly", *test_paths]
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo paths
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:  # pragma: no cover - defensive
        raise SuiteRunError(f"collection timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    return parse_collected(result.stdout)


# --------------------------------------------------------------------------- #
# The real subprocess runner (the dependency-injection seam).
# --------------------------------------------------------------------------- #


def x_collect_node_ids__mutmut_1(
    command: Sequence[str],
    test_paths: Sequence[str],
    *,
    repo_root: Path,
    seed: int,
    timeout: int,
) -> list[str]:
    """Collect the node ids under ``test_paths`` (for the order probe)."""
    argv = None
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo paths
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:  # pragma: no cover - defensive
        raise SuiteRunError(f"collection timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    return parse_collected(result.stdout)


# --------------------------------------------------------------------------- #
# The real subprocess runner (the dependency-injection seam).
# --------------------------------------------------------------------------- #


def x_collect_node_ids__mutmut_2(
    command: Sequence[str],
    test_paths: Sequence[str],
    *,
    repo_root: Path,
    seed: int,
    timeout: int,
) -> list[str]:
    """Collect the node ids under ``test_paths`` (for the order probe)."""
    argv = [*command, "XX--collect-onlyXX", "-q", "-p", "no:cacheprovider", "-p", "no:randomly", *test_paths]
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo paths
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:  # pragma: no cover - defensive
        raise SuiteRunError(f"collection timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    return parse_collected(result.stdout)


# --------------------------------------------------------------------------- #
# The real subprocess runner (the dependency-injection seam).
# --------------------------------------------------------------------------- #


def x_collect_node_ids__mutmut_3(
    command: Sequence[str],
    test_paths: Sequence[str],
    *,
    repo_root: Path,
    seed: int,
    timeout: int,
) -> list[str]:
    """Collect the node ids under ``test_paths`` (for the order probe)."""
    argv = [*command, "--COLLECT-ONLY", "-q", "-p", "no:cacheprovider", "-p", "no:randomly", *test_paths]
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo paths
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:  # pragma: no cover - defensive
        raise SuiteRunError(f"collection timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    return parse_collected(result.stdout)


# --------------------------------------------------------------------------- #
# The real subprocess runner (the dependency-injection seam).
# --------------------------------------------------------------------------- #


def x_collect_node_ids__mutmut_4(
    command: Sequence[str],
    test_paths: Sequence[str],
    *,
    repo_root: Path,
    seed: int,
    timeout: int,
) -> list[str]:
    """Collect the node ids under ``test_paths`` (for the order probe)."""
    argv = [*command, "--collect-only", "XX-qXX", "-p", "no:cacheprovider", "-p", "no:randomly", *test_paths]
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo paths
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:  # pragma: no cover - defensive
        raise SuiteRunError(f"collection timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    return parse_collected(result.stdout)


# --------------------------------------------------------------------------- #
# The real subprocess runner (the dependency-injection seam).
# --------------------------------------------------------------------------- #


def x_collect_node_ids__mutmut_5(
    command: Sequence[str],
    test_paths: Sequence[str],
    *,
    repo_root: Path,
    seed: int,
    timeout: int,
) -> list[str]:
    """Collect the node ids under ``test_paths`` (for the order probe)."""
    argv = [*command, "--collect-only", "-Q", "-p", "no:cacheprovider", "-p", "no:randomly", *test_paths]
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo paths
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:  # pragma: no cover - defensive
        raise SuiteRunError(f"collection timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    return parse_collected(result.stdout)


# --------------------------------------------------------------------------- #
# The real subprocess runner (the dependency-injection seam).
# --------------------------------------------------------------------------- #


def x_collect_node_ids__mutmut_6(
    command: Sequence[str],
    test_paths: Sequence[str],
    *,
    repo_root: Path,
    seed: int,
    timeout: int,
) -> list[str]:
    """Collect the node ids under ``test_paths`` (for the order probe)."""
    argv = [*command, "--collect-only", "-q", "XX-pXX", "no:cacheprovider", "-p", "no:randomly", *test_paths]
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo paths
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:  # pragma: no cover - defensive
        raise SuiteRunError(f"collection timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    return parse_collected(result.stdout)


# --------------------------------------------------------------------------- #
# The real subprocess runner (the dependency-injection seam).
# --------------------------------------------------------------------------- #


def x_collect_node_ids__mutmut_7(
    command: Sequence[str],
    test_paths: Sequence[str],
    *,
    repo_root: Path,
    seed: int,
    timeout: int,
) -> list[str]:
    """Collect the node ids under ``test_paths`` (for the order probe)."""
    argv = [*command, "--collect-only", "-q", "-P", "no:cacheprovider", "-p", "no:randomly", *test_paths]
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo paths
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:  # pragma: no cover - defensive
        raise SuiteRunError(f"collection timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    return parse_collected(result.stdout)


# --------------------------------------------------------------------------- #
# The real subprocess runner (the dependency-injection seam).
# --------------------------------------------------------------------------- #


def x_collect_node_ids__mutmut_8(
    command: Sequence[str],
    test_paths: Sequence[str],
    *,
    repo_root: Path,
    seed: int,
    timeout: int,
) -> list[str]:
    """Collect the node ids under ``test_paths`` (for the order probe)."""
    argv = [*command, "--collect-only", "-q", "-p", "XXno:cacheproviderXX", "-p", "no:randomly", *test_paths]
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo paths
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:  # pragma: no cover - defensive
        raise SuiteRunError(f"collection timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    return parse_collected(result.stdout)


# --------------------------------------------------------------------------- #
# The real subprocess runner (the dependency-injection seam).
# --------------------------------------------------------------------------- #


def x_collect_node_ids__mutmut_9(
    command: Sequence[str],
    test_paths: Sequence[str],
    *,
    repo_root: Path,
    seed: int,
    timeout: int,
) -> list[str]:
    """Collect the node ids under ``test_paths`` (for the order probe)."""
    argv = [*command, "--collect-only", "-q", "-p", "NO:CACHEPROVIDER", "-p", "no:randomly", *test_paths]
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo paths
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:  # pragma: no cover - defensive
        raise SuiteRunError(f"collection timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    return parse_collected(result.stdout)


# --------------------------------------------------------------------------- #
# The real subprocess runner (the dependency-injection seam).
# --------------------------------------------------------------------------- #


def x_collect_node_ids__mutmut_10(
    command: Sequence[str],
    test_paths: Sequence[str],
    *,
    repo_root: Path,
    seed: int,
    timeout: int,
) -> list[str]:
    """Collect the node ids under ``test_paths`` (for the order probe)."""
    argv = [*command, "--collect-only", "-q", "-p", "no:cacheprovider", "XX-pXX", "no:randomly", *test_paths]
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo paths
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:  # pragma: no cover - defensive
        raise SuiteRunError(f"collection timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    return parse_collected(result.stdout)


# --------------------------------------------------------------------------- #
# The real subprocess runner (the dependency-injection seam).
# --------------------------------------------------------------------------- #


def x_collect_node_ids__mutmut_11(
    command: Sequence[str],
    test_paths: Sequence[str],
    *,
    repo_root: Path,
    seed: int,
    timeout: int,
) -> list[str]:
    """Collect the node ids under ``test_paths`` (for the order probe)."""
    argv = [*command, "--collect-only", "-q", "-p", "no:cacheprovider", "-P", "no:randomly", *test_paths]
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo paths
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:  # pragma: no cover - defensive
        raise SuiteRunError(f"collection timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    return parse_collected(result.stdout)


# --------------------------------------------------------------------------- #
# The real subprocess runner (the dependency-injection seam).
# --------------------------------------------------------------------------- #


def x_collect_node_ids__mutmut_12(
    command: Sequence[str],
    test_paths: Sequence[str],
    *,
    repo_root: Path,
    seed: int,
    timeout: int,
) -> list[str]:
    """Collect the node ids under ``test_paths`` (for the order probe)."""
    argv = [*command, "--collect-only", "-q", "-p", "no:cacheprovider", "-p", "XXno:randomlyXX", *test_paths]
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo paths
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:  # pragma: no cover - defensive
        raise SuiteRunError(f"collection timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    return parse_collected(result.stdout)


# --------------------------------------------------------------------------- #
# The real subprocess runner (the dependency-injection seam).
# --------------------------------------------------------------------------- #


def x_collect_node_ids__mutmut_13(
    command: Sequence[str],
    test_paths: Sequence[str],
    *,
    repo_root: Path,
    seed: int,
    timeout: int,
) -> list[str]:
    """Collect the node ids under ``test_paths`` (for the order probe)."""
    argv = [*command, "--collect-only", "-q", "-p", "no:cacheprovider", "-p", "NO:RANDOMLY", *test_paths]
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo paths
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:  # pragma: no cover - defensive
        raise SuiteRunError(f"collection timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    return parse_collected(result.stdout)


# --------------------------------------------------------------------------- #
# The real subprocess runner (the dependency-injection seam).
# --------------------------------------------------------------------------- #


def x_collect_node_ids__mutmut_14(
    command: Sequence[str],
    test_paths: Sequence[str],
    *,
    repo_root: Path,
    seed: int,
    timeout: int,
) -> list[str]:
    """Collect the node ids under ``test_paths`` (for the order probe)."""
    argv = [*command, "--collect-only", "-q", "-p", "no:cacheprovider", "-p", "no:randomly", *test_paths]
    try:
        result = None
    except subprocess.TimeoutExpired as exc:  # pragma: no cover - defensive
        raise SuiteRunError(f"collection timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    return parse_collected(result.stdout)


# --------------------------------------------------------------------------- #
# The real subprocess runner (the dependency-injection seam).
# --------------------------------------------------------------------------- #


def x_collect_node_ids__mutmut_15(
    command: Sequence[str],
    test_paths: Sequence[str],
    *,
    repo_root: Path,
    seed: int,
    timeout: int,
) -> list[str]:
    """Collect the node ids under ``test_paths`` (for the order probe)."""
    argv = [*command, "--collect-only", "-q", "-p", "no:cacheprovider", "-p", "no:randomly", *test_paths]
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo paths
            None,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:  # pragma: no cover - defensive
        raise SuiteRunError(f"collection timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    return parse_collected(result.stdout)


# --------------------------------------------------------------------------- #
# The real subprocess runner (the dependency-injection seam).
# --------------------------------------------------------------------------- #


def x_collect_node_ids__mutmut_16(
    command: Sequence[str],
    test_paths: Sequence[str],
    *,
    repo_root: Path,
    seed: int,
    timeout: int,
) -> list[str]:
    """Collect the node ids under ``test_paths`` (for the order probe)."""
    argv = [*command, "--collect-only", "-q", "-p", "no:cacheprovider", "-p", "no:randomly", *test_paths]
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo paths
            argv,
            cwd=None,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:  # pragma: no cover - defensive
        raise SuiteRunError(f"collection timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    return parse_collected(result.stdout)


# --------------------------------------------------------------------------- #
# The real subprocess runner (the dependency-injection seam).
# --------------------------------------------------------------------------- #


def x_collect_node_ids__mutmut_17(
    command: Sequence[str],
    test_paths: Sequence[str],
    *,
    repo_root: Path,
    seed: int,
    timeout: int,
) -> list[str]:
    """Collect the node ids under ``test_paths`` (for the order probe)."""
    argv = [*command, "--collect-only", "-q", "-p", "no:cacheprovider", "-p", "no:randomly", *test_paths]
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo paths
            argv,
            cwd=repo_root,
            env=None,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:  # pragma: no cover - defensive
        raise SuiteRunError(f"collection timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    return parse_collected(result.stdout)


# --------------------------------------------------------------------------- #
# The real subprocess runner (the dependency-injection seam).
# --------------------------------------------------------------------------- #


def x_collect_node_ids__mutmut_18(
    command: Sequence[str],
    test_paths: Sequence[str],
    *,
    repo_root: Path,
    seed: int,
    timeout: int,
) -> list[str]:
    """Collect the node ids under ``test_paths`` (for the order probe)."""
    argv = [*command, "--collect-only", "-q", "-p", "no:cacheprovider", "-p", "no:randomly", *test_paths]
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo paths
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=None,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:  # pragma: no cover - defensive
        raise SuiteRunError(f"collection timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    return parse_collected(result.stdout)


# --------------------------------------------------------------------------- #
# The real subprocess runner (the dependency-injection seam).
# --------------------------------------------------------------------------- #


def x_collect_node_ids__mutmut_19(
    command: Sequence[str],
    test_paths: Sequence[str],
    *,
    repo_root: Path,
    seed: int,
    timeout: int,
) -> list[str]:
    """Collect the node ids under ``test_paths`` (for the order probe)."""
    argv = [*command, "--collect-only", "-q", "-p", "no:cacheprovider", "-p", "no:randomly", *test_paths]
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo paths
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=None,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:  # pragma: no cover - defensive
        raise SuiteRunError(f"collection timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    return parse_collected(result.stdout)


# --------------------------------------------------------------------------- #
# The real subprocess runner (the dependency-injection seam).
# --------------------------------------------------------------------------- #


def x_collect_node_ids__mutmut_20(
    command: Sequence[str],
    test_paths: Sequence[str],
    *,
    repo_root: Path,
    seed: int,
    timeout: int,
) -> list[str]:
    """Collect the node ids under ``test_paths`` (for the order probe)."""
    argv = [*command, "--collect-only", "-q", "-p", "no:cacheprovider", "-p", "no:randomly", *test_paths]
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo paths
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=None,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:  # pragma: no cover - defensive
        raise SuiteRunError(f"collection timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    return parse_collected(result.stdout)


# --------------------------------------------------------------------------- #
# The real subprocess runner (the dependency-injection seam).
# --------------------------------------------------------------------------- #


def x_collect_node_ids__mutmut_21(
    command: Sequence[str],
    test_paths: Sequence[str],
    *,
    repo_root: Path,
    seed: int,
    timeout: int,
) -> list[str]:
    """Collect the node ids under ``test_paths`` (for the order probe)."""
    argv = [*command, "--collect-only", "-q", "-p", "no:cacheprovider", "-p", "no:randomly", *test_paths]
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo paths
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=None,
        )
    except subprocess.TimeoutExpired as exc:  # pragma: no cover - defensive
        raise SuiteRunError(f"collection timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    return parse_collected(result.stdout)


# --------------------------------------------------------------------------- #
# The real subprocess runner (the dependency-injection seam).
# --------------------------------------------------------------------------- #


def x_collect_node_ids__mutmut_22(
    command: Sequence[str],
    test_paths: Sequence[str],
    *,
    repo_root: Path,
    seed: int,
    timeout: int,
) -> list[str]:
    """Collect the node ids under ``test_paths`` (for the order probe)."""
    argv = [*command, "--collect-only", "-q", "-p", "no:cacheprovider", "-p", "no:randomly", *test_paths]
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo paths
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:  # pragma: no cover - defensive
        raise SuiteRunError(f"collection timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    return parse_collected(result.stdout)


# --------------------------------------------------------------------------- #
# The real subprocess runner (the dependency-injection seam).
# --------------------------------------------------------------------------- #


def x_collect_node_ids__mutmut_23(
    command: Sequence[str],
    test_paths: Sequence[str],
    *,
    repo_root: Path,
    seed: int,
    timeout: int,
) -> list[str]:
    """Collect the node ids under ``test_paths`` (for the order probe)."""
    argv = [*command, "--collect-only", "-q", "-p", "no:cacheprovider", "-p", "no:randomly", *test_paths]
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo paths
            argv,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:  # pragma: no cover - defensive
        raise SuiteRunError(f"collection timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    return parse_collected(result.stdout)


# --------------------------------------------------------------------------- #
# The real subprocess runner (the dependency-injection seam).
# --------------------------------------------------------------------------- #


def x_collect_node_ids__mutmut_24(
    command: Sequence[str],
    test_paths: Sequence[str],
    *,
    repo_root: Path,
    seed: int,
    timeout: int,
) -> list[str]:
    """Collect the node ids under ``test_paths`` (for the order probe)."""
    argv = [*command, "--collect-only", "-q", "-p", "no:cacheprovider", "-p", "no:randomly", *test_paths]
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo paths
            argv,
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:  # pragma: no cover - defensive
        raise SuiteRunError(f"collection timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    return parse_collected(result.stdout)


# --------------------------------------------------------------------------- #
# The real subprocess runner (the dependency-injection seam).
# --------------------------------------------------------------------------- #


def x_collect_node_ids__mutmut_25(
    command: Sequence[str],
    test_paths: Sequence[str],
    *,
    repo_root: Path,
    seed: int,
    timeout: int,
) -> list[str]:
    """Collect the node ids under ``test_paths`` (for the order probe)."""
    argv = [*command, "--collect-only", "-q", "-p", "no:cacheprovider", "-p", "no:randomly", *test_paths]
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo paths
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:  # pragma: no cover - defensive
        raise SuiteRunError(f"collection timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    return parse_collected(result.stdout)


# --------------------------------------------------------------------------- #
# The real subprocess runner (the dependency-injection seam).
# --------------------------------------------------------------------------- #


def x_collect_node_ids__mutmut_26(
    command: Sequence[str],
    test_paths: Sequence[str],
    *,
    repo_root: Path,
    seed: int,
    timeout: int,
) -> list[str]:
    """Collect the node ids under ``test_paths`` (for the order probe)."""
    argv = [*command, "--collect-only", "-q", "-p", "no:cacheprovider", "-p", "no:randomly", *test_paths]
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo paths
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:  # pragma: no cover - defensive
        raise SuiteRunError(f"collection timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    return parse_collected(result.stdout)


# --------------------------------------------------------------------------- #
# The real subprocess runner (the dependency-injection seam).
# --------------------------------------------------------------------------- #


def x_collect_node_ids__mutmut_27(
    command: Sequence[str],
    test_paths: Sequence[str],
    *,
    repo_root: Path,
    seed: int,
    timeout: int,
) -> list[str]:
    """Collect the node ids under ``test_paths`` (for the order probe)."""
    argv = [*command, "--collect-only", "-q", "-p", "no:cacheprovider", "-p", "no:randomly", *test_paths]
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo paths
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:  # pragma: no cover - defensive
        raise SuiteRunError(f"collection timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    return parse_collected(result.stdout)


# --------------------------------------------------------------------------- #
# The real subprocess runner (the dependency-injection seam).
# --------------------------------------------------------------------------- #


def x_collect_node_ids__mutmut_28(
    command: Sequence[str],
    test_paths: Sequence[str],
    *,
    repo_root: Path,
    seed: int,
    timeout: int,
) -> list[str]:
    """Collect the node ids under ``test_paths`` (for the order probe)."""
    argv = [*command, "--collect-only", "-q", "-p", "no:cacheprovider", "-p", "no:randomly", *test_paths]
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo paths
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            )
    except subprocess.TimeoutExpired as exc:  # pragma: no cover - defensive
        raise SuiteRunError(f"collection timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    return parse_collected(result.stdout)


# --------------------------------------------------------------------------- #
# The real subprocess runner (the dependency-injection seam).
# --------------------------------------------------------------------------- #


def x_collect_node_ids__mutmut_29(
    command: Sequence[str],
    test_paths: Sequence[str],
    *,
    repo_root: Path,
    seed: int,
    timeout: int,
) -> list[str]:
    """Collect the node ids under ``test_paths`` (for the order probe)."""
    argv = [*command, "--collect-only", "-q", "-p", "no:cacheprovider", "-p", "no:randomly", *test_paths]
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo paths
            argv,
            cwd=repo_root,
            env=_run_env(None),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:  # pragma: no cover - defensive
        raise SuiteRunError(f"collection timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    return parse_collected(result.stdout)


# --------------------------------------------------------------------------- #
# The real subprocess runner (the dependency-injection seam).
# --------------------------------------------------------------------------- #


def x_collect_node_ids__mutmut_30(
    command: Sequence[str],
    test_paths: Sequence[str],
    *,
    repo_root: Path,
    seed: int,
    timeout: int,
) -> list[str]:
    """Collect the node ids under ``test_paths`` (for the order probe)."""
    argv = [*command, "--collect-only", "-q", "-p", "no:cacheprovider", "-p", "no:randomly", *test_paths]
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo paths
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=False,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:  # pragma: no cover - defensive
        raise SuiteRunError(f"collection timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    return parse_collected(result.stdout)


# --------------------------------------------------------------------------- #
# The real subprocess runner (the dependency-injection seam).
# --------------------------------------------------------------------------- #


def x_collect_node_ids__mutmut_31(
    command: Sequence[str],
    test_paths: Sequence[str],
    *,
    repo_root: Path,
    seed: int,
    timeout: int,
) -> list[str]:
    """Collect the node ids under ``test_paths`` (for the order probe)."""
    argv = [*command, "--collect-only", "-q", "-p", "no:cacheprovider", "-p", "no:randomly", *test_paths]
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo paths
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=False,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:  # pragma: no cover - defensive
        raise SuiteRunError(f"collection timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    return parse_collected(result.stdout)


# --------------------------------------------------------------------------- #
# The real subprocess runner (the dependency-injection seam).
# --------------------------------------------------------------------------- #


def x_collect_node_ids__mutmut_32(
    command: Sequence[str],
    test_paths: Sequence[str],
    *,
    repo_root: Path,
    seed: int,
    timeout: int,
) -> list[str]:
    """Collect the node ids under ``test_paths`` (for the order probe)."""
    argv = [*command, "--collect-only", "-q", "-p", "no:cacheprovider", "-p", "no:randomly", *test_paths]
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo paths
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=True,
        )
    except subprocess.TimeoutExpired as exc:  # pragma: no cover - defensive
        raise SuiteRunError(f"collection timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    return parse_collected(result.stdout)


# --------------------------------------------------------------------------- #
# The real subprocess runner (the dependency-injection seam).
# --------------------------------------------------------------------------- #


def x_collect_node_ids__mutmut_33(
    command: Sequence[str],
    test_paths: Sequence[str],
    *,
    repo_root: Path,
    seed: int,
    timeout: int,
) -> list[str]:
    """Collect the node ids under ``test_paths`` (for the order probe)."""
    argv = [*command, "--collect-only", "-q", "-p", "no:cacheprovider", "-p", "no:randomly", *test_paths]
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo paths
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:  # pragma: no cover - defensive
        raise SuiteRunError(None) from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    return parse_collected(result.stdout)


# --------------------------------------------------------------------------- #
# The real subprocess runner (the dependency-injection seam).
# --------------------------------------------------------------------------- #


def x_collect_node_ids__mutmut_34(
    command: Sequence[str],
    test_paths: Sequence[str],
    *,
    repo_root: Path,
    seed: int,
    timeout: int,
) -> list[str]:
    """Collect the node ids under ``test_paths`` (for the order probe)."""
    argv = [*command, "--collect-only", "-q", "-p", "no:cacheprovider", "-p", "no:randomly", *test_paths]
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo paths
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:  # pragma: no cover - defensive
        raise SuiteRunError(f"collection timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(None) from exc
    return parse_collected(result.stdout)


# --------------------------------------------------------------------------- #
# The real subprocess runner (the dependency-injection seam).
# --------------------------------------------------------------------------- #


def x_collect_node_ids__mutmut_35(
    command: Sequence[str],
    test_paths: Sequence[str],
    *,
    repo_root: Path,
    seed: int,
    timeout: int,
) -> list[str]:
    """Collect the node ids under ``test_paths`` (for the order probe)."""
    argv = [*command, "--collect-only", "-q", "-p", "no:cacheprovider", "-p", "no:randomly", *test_paths]
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo paths
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:  # pragma: no cover - defensive
        raise SuiteRunError(f"collection timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[1]}") from exc
    return parse_collected(result.stdout)


# --------------------------------------------------------------------------- #
# The real subprocess runner (the dependency-injection seam).
# --------------------------------------------------------------------------- #


def x_collect_node_ids__mutmut_36(
    command: Sequence[str],
    test_paths: Sequence[str],
    *,
    repo_root: Path,
    seed: int,
    timeout: int,
) -> list[str]:
    """Collect the node ids under ``test_paths`` (for the order probe)."""
    argv = [*command, "--collect-only", "-q", "-p", "no:cacheprovider", "-p", "no:randomly", *test_paths]
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo paths
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:  # pragma: no cover - defensive
        raise SuiteRunError(f"collection timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    return parse_collected(None)

mutants_x_collect_node_ids__mutmut['_mutmut_orig'] = x_collect_node_ids__mutmut_orig # type: ignore # mutmut generated
mutants_x_collect_node_ids__mutmut['x_collect_node_ids__mutmut_1'] = x_collect_node_ids__mutmut_1 # type: ignore # mutmut generated
mutants_x_collect_node_ids__mutmut['x_collect_node_ids__mutmut_2'] = x_collect_node_ids__mutmut_2 # type: ignore # mutmut generated
mutants_x_collect_node_ids__mutmut['x_collect_node_ids__mutmut_3'] = x_collect_node_ids__mutmut_3 # type: ignore # mutmut generated
mutants_x_collect_node_ids__mutmut['x_collect_node_ids__mutmut_4'] = x_collect_node_ids__mutmut_4 # type: ignore # mutmut generated
mutants_x_collect_node_ids__mutmut['x_collect_node_ids__mutmut_5'] = x_collect_node_ids__mutmut_5 # type: ignore # mutmut generated
mutants_x_collect_node_ids__mutmut['x_collect_node_ids__mutmut_6'] = x_collect_node_ids__mutmut_6 # type: ignore # mutmut generated
mutants_x_collect_node_ids__mutmut['x_collect_node_ids__mutmut_7'] = x_collect_node_ids__mutmut_7 # type: ignore # mutmut generated
mutants_x_collect_node_ids__mutmut['x_collect_node_ids__mutmut_8'] = x_collect_node_ids__mutmut_8 # type: ignore # mutmut generated
mutants_x_collect_node_ids__mutmut['x_collect_node_ids__mutmut_9'] = x_collect_node_ids__mutmut_9 # type: ignore # mutmut generated
mutants_x_collect_node_ids__mutmut['x_collect_node_ids__mutmut_10'] = x_collect_node_ids__mutmut_10 # type: ignore # mutmut generated
mutants_x_collect_node_ids__mutmut['x_collect_node_ids__mutmut_11'] = x_collect_node_ids__mutmut_11 # type: ignore # mutmut generated
mutants_x_collect_node_ids__mutmut['x_collect_node_ids__mutmut_12'] = x_collect_node_ids__mutmut_12 # type: ignore # mutmut generated
mutants_x_collect_node_ids__mutmut['x_collect_node_ids__mutmut_13'] = x_collect_node_ids__mutmut_13 # type: ignore # mutmut generated
mutants_x_collect_node_ids__mutmut['x_collect_node_ids__mutmut_14'] = x_collect_node_ids__mutmut_14 # type: ignore # mutmut generated
mutants_x_collect_node_ids__mutmut['x_collect_node_ids__mutmut_15'] = x_collect_node_ids__mutmut_15 # type: ignore # mutmut generated
mutants_x_collect_node_ids__mutmut['x_collect_node_ids__mutmut_16'] = x_collect_node_ids__mutmut_16 # type: ignore # mutmut generated
mutants_x_collect_node_ids__mutmut['x_collect_node_ids__mutmut_17'] = x_collect_node_ids__mutmut_17 # type: ignore # mutmut generated
mutants_x_collect_node_ids__mutmut['x_collect_node_ids__mutmut_18'] = x_collect_node_ids__mutmut_18 # type: ignore # mutmut generated
mutants_x_collect_node_ids__mutmut['x_collect_node_ids__mutmut_19'] = x_collect_node_ids__mutmut_19 # type: ignore # mutmut generated
mutants_x_collect_node_ids__mutmut['x_collect_node_ids__mutmut_20'] = x_collect_node_ids__mutmut_20 # type: ignore # mutmut generated
mutants_x_collect_node_ids__mutmut['x_collect_node_ids__mutmut_21'] = x_collect_node_ids__mutmut_21 # type: ignore # mutmut generated
mutants_x_collect_node_ids__mutmut['x_collect_node_ids__mutmut_22'] = x_collect_node_ids__mutmut_22 # type: ignore # mutmut generated
mutants_x_collect_node_ids__mutmut['x_collect_node_ids__mutmut_23'] = x_collect_node_ids__mutmut_23 # type: ignore # mutmut generated
mutants_x_collect_node_ids__mutmut['x_collect_node_ids__mutmut_24'] = x_collect_node_ids__mutmut_24 # type: ignore # mutmut generated
mutants_x_collect_node_ids__mutmut['x_collect_node_ids__mutmut_25'] = x_collect_node_ids__mutmut_25 # type: ignore # mutmut generated
mutants_x_collect_node_ids__mutmut['x_collect_node_ids__mutmut_26'] = x_collect_node_ids__mutmut_26 # type: ignore # mutmut generated
mutants_x_collect_node_ids__mutmut['x_collect_node_ids__mutmut_27'] = x_collect_node_ids__mutmut_27 # type: ignore # mutmut generated
mutants_x_collect_node_ids__mutmut['x_collect_node_ids__mutmut_28'] = x_collect_node_ids__mutmut_28 # type: ignore # mutmut generated
mutants_x_collect_node_ids__mutmut['x_collect_node_ids__mutmut_29'] = x_collect_node_ids__mutmut_29 # type: ignore # mutmut generated
mutants_x_collect_node_ids__mutmut['x_collect_node_ids__mutmut_30'] = x_collect_node_ids__mutmut_30 # type: ignore # mutmut generated
mutants_x_collect_node_ids__mutmut['x_collect_node_ids__mutmut_31'] = x_collect_node_ids__mutmut_31 # type: ignore # mutmut generated
mutants_x_collect_node_ids__mutmut['x_collect_node_ids__mutmut_32'] = x_collect_node_ids__mutmut_32 # type: ignore # mutmut generated
mutants_x_collect_node_ids__mutmut['x_collect_node_ids__mutmut_33'] = x_collect_node_ids__mutmut_33 # type: ignore # mutmut generated
mutants_x_collect_node_ids__mutmut['x_collect_node_ids__mutmut_34'] = x_collect_node_ids__mutmut_34 # type: ignore # mutmut generated
mutants_x_collect_node_ids__mutmut['x_collect_node_ids__mutmut_35'] = x_collect_node_ids__mutmut_35 # type: ignore # mutmut generated
mutants_x_collect_node_ids__mutmut['x_collect_node_ids__mutmut_36'] = x_collect_node_ids__mutmut_36 # type: ignore # mutmut generated
mutants_x_run_suite__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_run_suite__mutmut)
def run_suite(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = build_pytest_argv(
        command,
        test_paths=test_paths,
        node_ids=node_ids,
        order_seed=spec.order_seed,
        use_randomly=use_randomly,
    )
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo node ids
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(f"run {spec.label!r} timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    outcomes = parse_outcomes(result.stdout)
    if not outcomes:
        raise SuiteRunError(
            f"run {spec.label!r} produced no per-test results (exit {result.returncode}); "
            "the suite did not run — check the configured test command and roots."
        )
    return outcomes


def x_run_suite__mutmut_orig(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = build_pytest_argv(
        command,
        test_paths=test_paths,
        node_ids=node_ids,
        order_seed=spec.order_seed,
        use_randomly=use_randomly,
    )
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo node ids
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(f"run {spec.label!r} timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    outcomes = parse_outcomes(result.stdout)
    if not outcomes:
        raise SuiteRunError(
            f"run {spec.label!r} produced no per-test results (exit {result.returncode}); "
            "the suite did not run — check the configured test command and roots."
        )
    return outcomes


def x_run_suite__mutmut_1(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = None
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo node ids
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(f"run {spec.label!r} timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    outcomes = parse_outcomes(result.stdout)
    if not outcomes:
        raise SuiteRunError(
            f"run {spec.label!r} produced no per-test results (exit {result.returncode}); "
            "the suite did not run — check the configured test command and roots."
        )
    return outcomes


def x_run_suite__mutmut_2(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = build_pytest_argv(
        None,
        test_paths=test_paths,
        node_ids=node_ids,
        order_seed=spec.order_seed,
        use_randomly=use_randomly,
    )
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo node ids
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(f"run {spec.label!r} timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    outcomes = parse_outcomes(result.stdout)
    if not outcomes:
        raise SuiteRunError(
            f"run {spec.label!r} produced no per-test results (exit {result.returncode}); "
            "the suite did not run — check the configured test command and roots."
        )
    return outcomes


def x_run_suite__mutmut_3(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = build_pytest_argv(
        command,
        test_paths=None,
        node_ids=node_ids,
        order_seed=spec.order_seed,
        use_randomly=use_randomly,
    )
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo node ids
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(f"run {spec.label!r} timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    outcomes = parse_outcomes(result.stdout)
    if not outcomes:
        raise SuiteRunError(
            f"run {spec.label!r} produced no per-test results (exit {result.returncode}); "
            "the suite did not run — check the configured test command and roots."
        )
    return outcomes


def x_run_suite__mutmut_4(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = build_pytest_argv(
        command,
        test_paths=test_paths,
        node_ids=None,
        order_seed=spec.order_seed,
        use_randomly=use_randomly,
    )
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo node ids
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(f"run {spec.label!r} timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    outcomes = parse_outcomes(result.stdout)
    if not outcomes:
        raise SuiteRunError(
            f"run {spec.label!r} produced no per-test results (exit {result.returncode}); "
            "the suite did not run — check the configured test command and roots."
        )
    return outcomes


def x_run_suite__mutmut_5(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = build_pytest_argv(
        command,
        test_paths=test_paths,
        node_ids=node_ids,
        order_seed=None,
        use_randomly=use_randomly,
    )
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo node ids
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(f"run {spec.label!r} timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    outcomes = parse_outcomes(result.stdout)
    if not outcomes:
        raise SuiteRunError(
            f"run {spec.label!r} produced no per-test results (exit {result.returncode}); "
            "the suite did not run — check the configured test command and roots."
        )
    return outcomes


def x_run_suite__mutmut_6(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = build_pytest_argv(
        command,
        test_paths=test_paths,
        node_ids=node_ids,
        order_seed=spec.order_seed,
        use_randomly=None,
    )
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo node ids
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(f"run {spec.label!r} timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    outcomes = parse_outcomes(result.stdout)
    if not outcomes:
        raise SuiteRunError(
            f"run {spec.label!r} produced no per-test results (exit {result.returncode}); "
            "the suite did not run — check the configured test command and roots."
        )
    return outcomes


def x_run_suite__mutmut_7(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = build_pytest_argv(
        test_paths=test_paths,
        node_ids=node_ids,
        order_seed=spec.order_seed,
        use_randomly=use_randomly,
    )
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo node ids
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(f"run {spec.label!r} timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    outcomes = parse_outcomes(result.stdout)
    if not outcomes:
        raise SuiteRunError(
            f"run {spec.label!r} produced no per-test results (exit {result.returncode}); "
            "the suite did not run — check the configured test command and roots."
        )
    return outcomes


def x_run_suite__mutmut_8(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = build_pytest_argv(
        command,
        node_ids=node_ids,
        order_seed=spec.order_seed,
        use_randomly=use_randomly,
    )
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo node ids
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(f"run {spec.label!r} timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    outcomes = parse_outcomes(result.stdout)
    if not outcomes:
        raise SuiteRunError(
            f"run {spec.label!r} produced no per-test results (exit {result.returncode}); "
            "the suite did not run — check the configured test command and roots."
        )
    return outcomes


def x_run_suite__mutmut_9(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = build_pytest_argv(
        command,
        test_paths=test_paths,
        order_seed=spec.order_seed,
        use_randomly=use_randomly,
    )
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo node ids
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(f"run {spec.label!r} timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    outcomes = parse_outcomes(result.stdout)
    if not outcomes:
        raise SuiteRunError(
            f"run {spec.label!r} produced no per-test results (exit {result.returncode}); "
            "the suite did not run — check the configured test command and roots."
        )
    return outcomes


def x_run_suite__mutmut_10(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = build_pytest_argv(
        command,
        test_paths=test_paths,
        node_ids=node_ids,
        use_randomly=use_randomly,
    )
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo node ids
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(f"run {spec.label!r} timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    outcomes = parse_outcomes(result.stdout)
    if not outcomes:
        raise SuiteRunError(
            f"run {spec.label!r} produced no per-test results (exit {result.returncode}); "
            "the suite did not run — check the configured test command and roots."
        )
    return outcomes


def x_run_suite__mutmut_11(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = build_pytest_argv(
        command,
        test_paths=test_paths,
        node_ids=node_ids,
        order_seed=spec.order_seed,
        )
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo node ids
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(f"run {spec.label!r} timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    outcomes = parse_outcomes(result.stdout)
    if not outcomes:
        raise SuiteRunError(
            f"run {spec.label!r} produced no per-test results (exit {result.returncode}); "
            "the suite did not run — check the configured test command and roots."
        )
    return outcomes


def x_run_suite__mutmut_12(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = build_pytest_argv(
        command,
        test_paths=test_paths,
        node_ids=node_ids,
        order_seed=spec.order_seed,
        use_randomly=use_randomly,
    )
    try:
        result = None
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(f"run {spec.label!r} timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    outcomes = parse_outcomes(result.stdout)
    if not outcomes:
        raise SuiteRunError(
            f"run {spec.label!r} produced no per-test results (exit {result.returncode}); "
            "the suite did not run — check the configured test command and roots."
        )
    return outcomes


def x_run_suite__mutmut_13(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = build_pytest_argv(
        command,
        test_paths=test_paths,
        node_ids=node_ids,
        order_seed=spec.order_seed,
        use_randomly=use_randomly,
    )
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo node ids
            None,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(f"run {spec.label!r} timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    outcomes = parse_outcomes(result.stdout)
    if not outcomes:
        raise SuiteRunError(
            f"run {spec.label!r} produced no per-test results (exit {result.returncode}); "
            "the suite did not run — check the configured test command and roots."
        )
    return outcomes


def x_run_suite__mutmut_14(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = build_pytest_argv(
        command,
        test_paths=test_paths,
        node_ids=node_ids,
        order_seed=spec.order_seed,
        use_randomly=use_randomly,
    )
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo node ids
            argv,
            cwd=None,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(f"run {spec.label!r} timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    outcomes = parse_outcomes(result.stdout)
    if not outcomes:
        raise SuiteRunError(
            f"run {spec.label!r} produced no per-test results (exit {result.returncode}); "
            "the suite did not run — check the configured test command and roots."
        )
    return outcomes


def x_run_suite__mutmut_15(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = build_pytest_argv(
        command,
        test_paths=test_paths,
        node_ids=node_ids,
        order_seed=spec.order_seed,
        use_randomly=use_randomly,
    )
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo node ids
            argv,
            cwd=repo_root,
            env=None,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(f"run {spec.label!r} timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    outcomes = parse_outcomes(result.stdout)
    if not outcomes:
        raise SuiteRunError(
            f"run {spec.label!r} produced no per-test results (exit {result.returncode}); "
            "the suite did not run — check the configured test command and roots."
        )
    return outcomes


def x_run_suite__mutmut_16(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = build_pytest_argv(
        command,
        test_paths=test_paths,
        node_ids=node_ids,
        order_seed=spec.order_seed,
        use_randomly=use_randomly,
    )
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo node ids
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=None,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(f"run {spec.label!r} timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    outcomes = parse_outcomes(result.stdout)
    if not outcomes:
        raise SuiteRunError(
            f"run {spec.label!r} produced no per-test results (exit {result.returncode}); "
            "the suite did not run — check the configured test command and roots."
        )
    return outcomes


def x_run_suite__mutmut_17(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = build_pytest_argv(
        command,
        test_paths=test_paths,
        node_ids=node_ids,
        order_seed=spec.order_seed,
        use_randomly=use_randomly,
    )
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo node ids
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=None,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(f"run {spec.label!r} timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    outcomes = parse_outcomes(result.stdout)
    if not outcomes:
        raise SuiteRunError(
            f"run {spec.label!r} produced no per-test results (exit {result.returncode}); "
            "the suite did not run — check the configured test command and roots."
        )
    return outcomes


def x_run_suite__mutmut_18(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = build_pytest_argv(
        command,
        test_paths=test_paths,
        node_ids=node_ids,
        order_seed=spec.order_seed,
        use_randomly=use_randomly,
    )
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo node ids
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=None,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(f"run {spec.label!r} timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    outcomes = parse_outcomes(result.stdout)
    if not outcomes:
        raise SuiteRunError(
            f"run {spec.label!r} produced no per-test results (exit {result.returncode}); "
            "the suite did not run — check the configured test command and roots."
        )
    return outcomes


def x_run_suite__mutmut_19(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = build_pytest_argv(
        command,
        test_paths=test_paths,
        node_ids=node_ids,
        order_seed=spec.order_seed,
        use_randomly=use_randomly,
    )
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo node ids
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=None,
        )
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(f"run {spec.label!r} timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    outcomes = parse_outcomes(result.stdout)
    if not outcomes:
        raise SuiteRunError(
            f"run {spec.label!r} produced no per-test results (exit {result.returncode}); "
            "the suite did not run — check the configured test command and roots."
        )
    return outcomes


def x_run_suite__mutmut_20(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = build_pytest_argv(
        command,
        test_paths=test_paths,
        node_ids=node_ids,
        order_seed=spec.order_seed,
        use_randomly=use_randomly,
    )
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo node ids
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(f"run {spec.label!r} timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    outcomes = parse_outcomes(result.stdout)
    if not outcomes:
        raise SuiteRunError(
            f"run {spec.label!r} produced no per-test results (exit {result.returncode}); "
            "the suite did not run — check the configured test command and roots."
        )
    return outcomes


def x_run_suite__mutmut_21(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = build_pytest_argv(
        command,
        test_paths=test_paths,
        node_ids=node_ids,
        order_seed=spec.order_seed,
        use_randomly=use_randomly,
    )
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo node ids
            argv,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(f"run {spec.label!r} timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    outcomes = parse_outcomes(result.stdout)
    if not outcomes:
        raise SuiteRunError(
            f"run {spec.label!r} produced no per-test results (exit {result.returncode}); "
            "the suite did not run — check the configured test command and roots."
        )
    return outcomes


def x_run_suite__mutmut_22(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = build_pytest_argv(
        command,
        test_paths=test_paths,
        node_ids=node_ids,
        order_seed=spec.order_seed,
        use_randomly=use_randomly,
    )
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo node ids
            argv,
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(f"run {spec.label!r} timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    outcomes = parse_outcomes(result.stdout)
    if not outcomes:
        raise SuiteRunError(
            f"run {spec.label!r} produced no per-test results (exit {result.returncode}); "
            "the suite did not run — check the configured test command and roots."
        )
    return outcomes


def x_run_suite__mutmut_23(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = build_pytest_argv(
        command,
        test_paths=test_paths,
        node_ids=node_ids,
        order_seed=spec.order_seed,
        use_randomly=use_randomly,
    )
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo node ids
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(f"run {spec.label!r} timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    outcomes = parse_outcomes(result.stdout)
    if not outcomes:
        raise SuiteRunError(
            f"run {spec.label!r} produced no per-test results (exit {result.returncode}); "
            "the suite did not run — check the configured test command and roots."
        )
    return outcomes


def x_run_suite__mutmut_24(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = build_pytest_argv(
        command,
        test_paths=test_paths,
        node_ids=node_ids,
        order_seed=spec.order_seed,
        use_randomly=use_randomly,
    )
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo node ids
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(f"run {spec.label!r} timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    outcomes = parse_outcomes(result.stdout)
    if not outcomes:
        raise SuiteRunError(
            f"run {spec.label!r} produced no per-test results (exit {result.returncode}); "
            "the suite did not run — check the configured test command and roots."
        )
    return outcomes


def x_run_suite__mutmut_25(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = build_pytest_argv(
        command,
        test_paths=test_paths,
        node_ids=node_ids,
        order_seed=spec.order_seed,
        use_randomly=use_randomly,
    )
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo node ids
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(f"run {spec.label!r} timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    outcomes = parse_outcomes(result.stdout)
    if not outcomes:
        raise SuiteRunError(
            f"run {spec.label!r} produced no per-test results (exit {result.returncode}); "
            "the suite did not run — check the configured test command and roots."
        )
    return outcomes


def x_run_suite__mutmut_26(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = build_pytest_argv(
        command,
        test_paths=test_paths,
        node_ids=node_ids,
        order_seed=spec.order_seed,
        use_randomly=use_randomly,
    )
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo node ids
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            )
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(f"run {spec.label!r} timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    outcomes = parse_outcomes(result.stdout)
    if not outcomes:
        raise SuiteRunError(
            f"run {spec.label!r} produced no per-test results (exit {result.returncode}); "
            "the suite did not run — check the configured test command and roots."
        )
    return outcomes


def x_run_suite__mutmut_27(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = build_pytest_argv(
        command,
        test_paths=test_paths,
        node_ids=node_ids,
        order_seed=spec.order_seed,
        use_randomly=use_randomly,
    )
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo node ids
            argv,
            cwd=repo_root,
            env=_run_env(None),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(f"run {spec.label!r} timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    outcomes = parse_outcomes(result.stdout)
    if not outcomes:
        raise SuiteRunError(
            f"run {spec.label!r} produced no per-test results (exit {result.returncode}); "
            "the suite did not run — check the configured test command and roots."
        )
    return outcomes


def x_run_suite__mutmut_28(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = build_pytest_argv(
        command,
        test_paths=test_paths,
        node_ids=node_ids,
        order_seed=spec.order_seed,
        use_randomly=use_randomly,
    )
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo node ids
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=False,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(f"run {spec.label!r} timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    outcomes = parse_outcomes(result.stdout)
    if not outcomes:
        raise SuiteRunError(
            f"run {spec.label!r} produced no per-test results (exit {result.returncode}); "
            "the suite did not run — check the configured test command and roots."
        )
    return outcomes


def x_run_suite__mutmut_29(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = build_pytest_argv(
        command,
        test_paths=test_paths,
        node_ids=node_ids,
        order_seed=spec.order_seed,
        use_randomly=use_randomly,
    )
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo node ids
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=False,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(f"run {spec.label!r} timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    outcomes = parse_outcomes(result.stdout)
    if not outcomes:
        raise SuiteRunError(
            f"run {spec.label!r} produced no per-test results (exit {result.returncode}); "
            "the suite did not run — check the configured test command and roots."
        )
    return outcomes


def x_run_suite__mutmut_30(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = build_pytest_argv(
        command,
        test_paths=test_paths,
        node_ids=node_ids,
        order_seed=spec.order_seed,
        use_randomly=use_randomly,
    )
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo node ids
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=True,
        )
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(f"run {spec.label!r} timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    outcomes = parse_outcomes(result.stdout)
    if not outcomes:
        raise SuiteRunError(
            f"run {spec.label!r} produced no per-test results (exit {result.returncode}); "
            "the suite did not run — check the configured test command and roots."
        )
    return outcomes


def x_run_suite__mutmut_31(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = build_pytest_argv(
        command,
        test_paths=test_paths,
        node_ids=node_ids,
        order_seed=spec.order_seed,
        use_randomly=use_randomly,
    )
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo node ids
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(None) from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    outcomes = parse_outcomes(result.stdout)
    if not outcomes:
        raise SuiteRunError(
            f"run {spec.label!r} produced no per-test results (exit {result.returncode}); "
            "the suite did not run — check the configured test command and roots."
        )
    return outcomes


def x_run_suite__mutmut_32(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = build_pytest_argv(
        command,
        test_paths=test_paths,
        node_ids=node_ids,
        order_seed=spec.order_seed,
        use_randomly=use_randomly,
    )
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo node ids
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(f"run {spec.label!r} timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(None) from exc
    outcomes = parse_outcomes(result.stdout)
    if not outcomes:
        raise SuiteRunError(
            f"run {spec.label!r} produced no per-test results (exit {result.returncode}); "
            "the suite did not run — check the configured test command and roots."
        )
    return outcomes


def x_run_suite__mutmut_33(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = build_pytest_argv(
        command,
        test_paths=test_paths,
        node_ids=node_ids,
        order_seed=spec.order_seed,
        use_randomly=use_randomly,
    )
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo node ids
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(f"run {spec.label!r} timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[1]}") from exc
    outcomes = parse_outcomes(result.stdout)
    if not outcomes:
        raise SuiteRunError(
            f"run {spec.label!r} produced no per-test results (exit {result.returncode}); "
            "the suite did not run — check the configured test command and roots."
        )
    return outcomes


def x_run_suite__mutmut_34(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = build_pytest_argv(
        command,
        test_paths=test_paths,
        node_ids=node_ids,
        order_seed=spec.order_seed,
        use_randomly=use_randomly,
    )
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo node ids
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(f"run {spec.label!r} timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    outcomes = None
    if not outcomes:
        raise SuiteRunError(
            f"run {spec.label!r} produced no per-test results (exit {result.returncode}); "
            "the suite did not run — check the configured test command and roots."
        )
    return outcomes


def x_run_suite__mutmut_35(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = build_pytest_argv(
        command,
        test_paths=test_paths,
        node_ids=node_ids,
        order_seed=spec.order_seed,
        use_randomly=use_randomly,
    )
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo node ids
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(f"run {spec.label!r} timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    outcomes = parse_outcomes(None)
    if not outcomes:
        raise SuiteRunError(
            f"run {spec.label!r} produced no per-test results (exit {result.returncode}); "
            "the suite did not run — check the configured test command and roots."
        )
    return outcomes


def x_run_suite__mutmut_36(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = build_pytest_argv(
        command,
        test_paths=test_paths,
        node_ids=node_ids,
        order_seed=spec.order_seed,
        use_randomly=use_randomly,
    )
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo node ids
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(f"run {spec.label!r} timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    outcomes = parse_outcomes(result.stdout)
    if outcomes:
        raise SuiteRunError(
            f"run {spec.label!r} produced no per-test results (exit {result.returncode}); "
            "the suite did not run — check the configured test command and roots."
        )
    return outcomes


def x_run_suite__mutmut_37(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = build_pytest_argv(
        command,
        test_paths=test_paths,
        node_ids=node_ids,
        order_seed=spec.order_seed,
        use_randomly=use_randomly,
    )
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo node ids
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(f"run {spec.label!r} timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    outcomes = parse_outcomes(result.stdout)
    if not outcomes:
        raise SuiteRunError(
            None
        )
    return outcomes


def x_run_suite__mutmut_38(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = build_pytest_argv(
        command,
        test_paths=test_paths,
        node_ids=node_ids,
        order_seed=spec.order_seed,
        use_randomly=use_randomly,
    )
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo node ids
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(f"run {spec.label!r} timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    outcomes = parse_outcomes(result.stdout)
    if not outcomes:
        raise SuiteRunError(
            f"run {spec.label!r} produced no per-test results (exit {result.returncode}); "
            "XXthe suite did not run — check the configured test command and roots.XX"
        )
    return outcomes


def x_run_suite__mutmut_39(
    spec: RunSpec,
    *,
    command: Sequence[str],
    test_paths: Sequence[str],
    node_ids: Sequence[str],
    repo_root: Path,
    seed: int,
    use_randomly: bool,
    timeout: int,
) -> dict[str, str]:
    """Execute one planned run and return its ``{nodeid: outcome}`` map."""
    argv = build_pytest_argv(
        command,
        test_paths=test_paths,
        node_ids=node_ids,
        order_seed=spec.order_seed,
        use_randomly=use_randomly,
    )
    try:
        result = subprocess.run(  # noqa: S603  # argv is the configured test command + repo node ids
            argv,
            cwd=repo_root,
            env=_run_env(seed),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise SuiteRunError(f"run {spec.label!r} timed out after {timeout}s") from exc
    except OSError as exc:
        raise SuiteRunError(f"configured test command unavailable: {command[0]}") from exc
    outcomes = parse_outcomes(result.stdout)
    if not outcomes:
        raise SuiteRunError(
            f"run {spec.label!r} produced no per-test results (exit {result.returncode}); "
            "THE SUITE DID NOT RUN — CHECK THE CONFIGURED TEST COMMAND AND ROOTS."
        )
    return outcomes

mutants_x_run_suite__mutmut['_mutmut_orig'] = x_run_suite__mutmut_orig # type: ignore # mutmut generated
mutants_x_run_suite__mutmut['x_run_suite__mutmut_1'] = x_run_suite__mutmut_1 # type: ignore # mutmut generated
mutants_x_run_suite__mutmut['x_run_suite__mutmut_2'] = x_run_suite__mutmut_2 # type: ignore # mutmut generated
mutants_x_run_suite__mutmut['x_run_suite__mutmut_3'] = x_run_suite__mutmut_3 # type: ignore # mutmut generated
mutants_x_run_suite__mutmut['x_run_suite__mutmut_4'] = x_run_suite__mutmut_4 # type: ignore # mutmut generated
mutants_x_run_suite__mutmut['x_run_suite__mutmut_5'] = x_run_suite__mutmut_5 # type: ignore # mutmut generated
mutants_x_run_suite__mutmut['x_run_suite__mutmut_6'] = x_run_suite__mutmut_6 # type: ignore # mutmut generated
mutants_x_run_suite__mutmut['x_run_suite__mutmut_7'] = x_run_suite__mutmut_7 # type: ignore # mutmut generated
mutants_x_run_suite__mutmut['x_run_suite__mutmut_8'] = x_run_suite__mutmut_8 # type: ignore # mutmut generated
mutants_x_run_suite__mutmut['x_run_suite__mutmut_9'] = x_run_suite__mutmut_9 # type: ignore # mutmut generated
mutants_x_run_suite__mutmut['x_run_suite__mutmut_10'] = x_run_suite__mutmut_10 # type: ignore # mutmut generated
mutants_x_run_suite__mutmut['x_run_suite__mutmut_11'] = x_run_suite__mutmut_11 # type: ignore # mutmut generated
mutants_x_run_suite__mutmut['x_run_suite__mutmut_12'] = x_run_suite__mutmut_12 # type: ignore # mutmut generated
mutants_x_run_suite__mutmut['x_run_suite__mutmut_13'] = x_run_suite__mutmut_13 # type: ignore # mutmut generated
mutants_x_run_suite__mutmut['x_run_suite__mutmut_14'] = x_run_suite__mutmut_14 # type: ignore # mutmut generated
mutants_x_run_suite__mutmut['x_run_suite__mutmut_15'] = x_run_suite__mutmut_15 # type: ignore # mutmut generated
mutants_x_run_suite__mutmut['x_run_suite__mutmut_16'] = x_run_suite__mutmut_16 # type: ignore # mutmut generated
mutants_x_run_suite__mutmut['x_run_suite__mutmut_17'] = x_run_suite__mutmut_17 # type: ignore # mutmut generated
mutants_x_run_suite__mutmut['x_run_suite__mutmut_18'] = x_run_suite__mutmut_18 # type: ignore # mutmut generated
mutants_x_run_suite__mutmut['x_run_suite__mutmut_19'] = x_run_suite__mutmut_19 # type: ignore # mutmut generated
mutants_x_run_suite__mutmut['x_run_suite__mutmut_20'] = x_run_suite__mutmut_20 # type: ignore # mutmut generated
mutants_x_run_suite__mutmut['x_run_suite__mutmut_21'] = x_run_suite__mutmut_21 # type: ignore # mutmut generated
mutants_x_run_suite__mutmut['x_run_suite__mutmut_22'] = x_run_suite__mutmut_22 # type: ignore # mutmut generated
mutants_x_run_suite__mutmut['x_run_suite__mutmut_23'] = x_run_suite__mutmut_23 # type: ignore # mutmut generated
mutants_x_run_suite__mutmut['x_run_suite__mutmut_24'] = x_run_suite__mutmut_24 # type: ignore # mutmut generated
mutants_x_run_suite__mutmut['x_run_suite__mutmut_25'] = x_run_suite__mutmut_25 # type: ignore # mutmut generated
mutants_x_run_suite__mutmut['x_run_suite__mutmut_26'] = x_run_suite__mutmut_26 # type: ignore # mutmut generated
mutants_x_run_suite__mutmut['x_run_suite__mutmut_27'] = x_run_suite__mutmut_27 # type: ignore # mutmut generated
mutants_x_run_suite__mutmut['x_run_suite__mutmut_28'] = x_run_suite__mutmut_28 # type: ignore # mutmut generated
mutants_x_run_suite__mutmut['x_run_suite__mutmut_29'] = x_run_suite__mutmut_29 # type: ignore # mutmut generated
mutants_x_run_suite__mutmut['x_run_suite__mutmut_30'] = x_run_suite__mutmut_30 # type: ignore # mutmut generated
mutants_x_run_suite__mutmut['x_run_suite__mutmut_31'] = x_run_suite__mutmut_31 # type: ignore # mutmut generated
mutants_x_run_suite__mutmut['x_run_suite__mutmut_32'] = x_run_suite__mutmut_32 # type: ignore # mutmut generated
mutants_x_run_suite__mutmut['x_run_suite__mutmut_33'] = x_run_suite__mutmut_33 # type: ignore # mutmut generated
mutants_x_run_suite__mutmut['x_run_suite__mutmut_34'] = x_run_suite__mutmut_34 # type: ignore # mutmut generated
mutants_x_run_suite__mutmut['x_run_suite__mutmut_35'] = x_run_suite__mutmut_35 # type: ignore # mutmut generated
mutants_x_run_suite__mutmut['x_run_suite__mutmut_36'] = x_run_suite__mutmut_36 # type: ignore # mutmut generated
mutants_x_run_suite__mutmut['x_run_suite__mutmut_37'] = x_run_suite__mutmut_37 # type: ignore # mutmut generated
mutants_x_run_suite__mutmut['x_run_suite__mutmut_38'] = x_run_suite__mutmut_38 # type: ignore # mutmut generated
mutants_x_run_suite__mutmut['x_run_suite__mutmut_39'] = x_run_suite__mutmut_39 # type: ignore # mutmut generated


#: The runner signature the orchestrator depends on (injectable for tests).
Runner = Callable[[RunSpec], Mapping[str, str]]
mutants_x_detect_nondeterminism__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_detect_nondeterminism__mutmut)
def detect_nondeterminism(
    plan: Sequence[RunSpec],
    runner: Runner,
) -> list[Divergence]:
    """Execute every planned run via ``runner`` and compare the outcomes.

    ``runner`` maps a :class:`RunSpec` to that run's ``{nodeid: outcome}``. The
    real path binds it to :func:`run_suite`; a test injects a fake to drive the
    comparison without a subprocess.
    """
    runs = [(spec.label, dict(runner(spec))) for spec in plan]
    return compare_runs(runs)


def x_detect_nondeterminism__mutmut_orig(
    plan: Sequence[RunSpec],
    runner: Runner,
) -> list[Divergence]:
    """Execute every planned run via ``runner`` and compare the outcomes.

    ``runner`` maps a :class:`RunSpec` to that run's ``{nodeid: outcome}``. The
    real path binds it to :func:`run_suite`; a test injects a fake to drive the
    comparison without a subprocess.
    """
    runs = [(spec.label, dict(runner(spec))) for spec in plan]
    return compare_runs(runs)


def x_detect_nondeterminism__mutmut_1(
    plan: Sequence[RunSpec],
    runner: Runner,
) -> list[Divergence]:
    """Execute every planned run via ``runner`` and compare the outcomes.

    ``runner`` maps a :class:`RunSpec` to that run's ``{nodeid: outcome}``. The
    real path binds it to :func:`run_suite`; a test injects a fake to drive the
    comparison without a subprocess.
    """
    runs = None
    return compare_runs(runs)


def x_detect_nondeterminism__mutmut_2(
    plan: Sequence[RunSpec],
    runner: Runner,
) -> list[Divergence]:
    """Execute every planned run via ``runner`` and compare the outcomes.

    ``runner`` maps a :class:`RunSpec` to that run's ``{nodeid: outcome}``. The
    real path binds it to :func:`run_suite`; a test injects a fake to drive the
    comparison without a subprocess.
    """
    runs = [(spec.label, dict(None)) for spec in plan]
    return compare_runs(runs)


def x_detect_nondeterminism__mutmut_3(
    plan: Sequence[RunSpec],
    runner: Runner,
) -> list[Divergence]:
    """Execute every planned run via ``runner`` and compare the outcomes.

    ``runner`` maps a :class:`RunSpec` to that run's ``{nodeid: outcome}``. The
    real path binds it to :func:`run_suite`; a test injects a fake to drive the
    comparison without a subprocess.
    """
    runs = [(spec.label, dict(runner(None))) for spec in plan]
    return compare_runs(runs)


def x_detect_nondeterminism__mutmut_4(
    plan: Sequence[RunSpec],
    runner: Runner,
) -> list[Divergence]:
    """Execute every planned run via ``runner`` and compare the outcomes.

    ``runner`` maps a :class:`RunSpec` to that run's ``{nodeid: outcome}``. The
    real path binds it to :func:`run_suite`; a test injects a fake to drive the
    comparison without a subprocess.
    """
    runs = [(spec.label, dict(runner(spec))) for spec in plan]
    return compare_runs(None)

mutants_x_detect_nondeterminism__mutmut['_mutmut_orig'] = x_detect_nondeterminism__mutmut_orig # type: ignore # mutmut generated
mutants_x_detect_nondeterminism__mutmut['x_detect_nondeterminism__mutmut_1'] = x_detect_nondeterminism__mutmut_1 # type: ignore # mutmut generated
mutants_x_detect_nondeterminism__mutmut['x_detect_nondeterminism__mutmut_2'] = x_detect_nondeterminism__mutmut_2 # type: ignore # mutmut generated
mutants_x_detect_nondeterminism__mutmut['x_detect_nondeterminism__mutmut_3'] = x_detect_nondeterminism__mutmut_3 # type: ignore # mutmut generated
mutants_x_detect_nondeterminism__mutmut['x_detect_nondeterminism__mutmut_4'] = x_detect_nondeterminism__mutmut_4 # type: ignore # mutmut generated
mutants_x_format_failure__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_format_failure__mutmut)
def format_failure(divergences: Sequence[Divergence]) -> str:
    """Render the FAIL block: each unstable test and its per-run verdicts."""
    lines = [
        f"FAIL [deterministic-tests] — {len(divergences)} test(s) with a non-deterministic outcome:",
    ]
    for div in divergences:
        detail = ", ".join(f"{label}={outcome}" for label, outcome in div.outcomes)
        lines.append(f"  {div.test_id}: {detail}")
    lines.append("")
    lines.append(REMEDIATION)
    return "\n".join(lines)


def x_format_failure__mutmut_orig(divergences: Sequence[Divergence]) -> str:
    """Render the FAIL block: each unstable test and its per-run verdicts."""
    lines = [
        f"FAIL [deterministic-tests] — {len(divergences)} test(s) with a non-deterministic outcome:",
    ]
    for div in divergences:
        detail = ", ".join(f"{label}={outcome}" for label, outcome in div.outcomes)
        lines.append(f"  {div.test_id}: {detail}")
    lines.append("")
    lines.append(REMEDIATION)
    return "\n".join(lines)


def x_format_failure__mutmut_1(divergences: Sequence[Divergence]) -> str:
    """Render the FAIL block: each unstable test and its per-run verdicts."""
    lines = None
    for div in divergences:
        detail = ", ".join(f"{label}={outcome}" for label, outcome in div.outcomes)
        lines.append(f"  {div.test_id}: {detail}")
    lines.append("")
    lines.append(REMEDIATION)
    return "\n".join(lines)


def x_format_failure__mutmut_2(divergences: Sequence[Divergence]) -> str:
    """Render the FAIL block: each unstable test and its per-run verdicts."""
    lines = [
        f"FAIL [deterministic-tests] — {len(divergences)} test(s) with a non-deterministic outcome:",
    ]
    for div in divergences:
        detail = None
        lines.append(f"  {div.test_id}: {detail}")
    lines.append("")
    lines.append(REMEDIATION)
    return "\n".join(lines)


def x_format_failure__mutmut_3(divergences: Sequence[Divergence]) -> str:
    """Render the FAIL block: each unstable test and its per-run verdicts."""
    lines = [
        f"FAIL [deterministic-tests] — {len(divergences)} test(s) with a non-deterministic outcome:",
    ]
    for div in divergences:
        detail = ", ".join(None)
        lines.append(f"  {div.test_id}: {detail}")
    lines.append("")
    lines.append(REMEDIATION)
    return "\n".join(lines)


def x_format_failure__mutmut_4(divergences: Sequence[Divergence]) -> str:
    """Render the FAIL block: each unstable test and its per-run verdicts."""
    lines = [
        f"FAIL [deterministic-tests] — {len(divergences)} test(s) with a non-deterministic outcome:",
    ]
    for div in divergences:
        detail = "XX, XX".join(f"{label}={outcome}" for label, outcome in div.outcomes)
        lines.append(f"  {div.test_id}: {detail}")
    lines.append("")
    lines.append(REMEDIATION)
    return "\n".join(lines)


def x_format_failure__mutmut_5(divergences: Sequence[Divergence]) -> str:
    """Render the FAIL block: each unstable test and its per-run verdicts."""
    lines = [
        f"FAIL [deterministic-tests] — {len(divergences)} test(s) with a non-deterministic outcome:",
    ]
    for div in divergences:
        detail = ", ".join(f"{label}={outcome}" for label, outcome in div.outcomes)
        lines.append(None)
    lines.append("")
    lines.append(REMEDIATION)
    return "\n".join(lines)


def x_format_failure__mutmut_6(divergences: Sequence[Divergence]) -> str:
    """Render the FAIL block: each unstable test and its per-run verdicts."""
    lines = [
        f"FAIL [deterministic-tests] — {len(divergences)} test(s) with a non-deterministic outcome:",
    ]
    for div in divergences:
        detail = ", ".join(f"{label}={outcome}" for label, outcome in div.outcomes)
        lines.append(f"  {div.test_id}: {detail}")
    lines.append(None)
    lines.append(REMEDIATION)
    return "\n".join(lines)


def x_format_failure__mutmut_7(divergences: Sequence[Divergence]) -> str:
    """Render the FAIL block: each unstable test and its per-run verdicts."""
    lines = [
        f"FAIL [deterministic-tests] — {len(divergences)} test(s) with a non-deterministic outcome:",
    ]
    for div in divergences:
        detail = ", ".join(f"{label}={outcome}" for label, outcome in div.outcomes)
        lines.append(f"  {div.test_id}: {detail}")
    lines.append("XXXX")
    lines.append(REMEDIATION)
    return "\n".join(lines)


def x_format_failure__mutmut_8(divergences: Sequence[Divergence]) -> str:
    """Render the FAIL block: each unstable test and its per-run verdicts."""
    lines = [
        f"FAIL [deterministic-tests] — {len(divergences)} test(s) with a non-deterministic outcome:",
    ]
    for div in divergences:
        detail = ", ".join(f"{label}={outcome}" for label, outcome in div.outcomes)
        lines.append(f"  {div.test_id}: {detail}")
    lines.append("")
    lines.append(None)
    return "\n".join(lines)


def x_format_failure__mutmut_9(divergences: Sequence[Divergence]) -> str:
    """Render the FAIL block: each unstable test and its per-run verdicts."""
    lines = [
        f"FAIL [deterministic-tests] — {len(divergences)} test(s) with a non-deterministic outcome:",
    ]
    for div in divergences:
        detail = ", ".join(f"{label}={outcome}" for label, outcome in div.outcomes)
        lines.append(f"  {div.test_id}: {detail}")
    lines.append("")
    lines.append(REMEDIATION)
    return "\n".join(None)


def x_format_failure__mutmut_10(divergences: Sequence[Divergence]) -> str:
    """Render the FAIL block: each unstable test and its per-run verdicts."""
    lines = [
        f"FAIL [deterministic-tests] — {len(divergences)} test(s) with a non-deterministic outcome:",
    ]
    for div in divergences:
        detail = ", ".join(f"{label}={outcome}" for label, outcome in div.outcomes)
        lines.append(f"  {div.test_id}: {detail}")
    lines.append("")
    lines.append(REMEDIATION)
    return "XX\nXX".join(lines)

mutants_x_format_failure__mutmut['_mutmut_orig'] = x_format_failure__mutmut_orig # type: ignore # mutmut generated
mutants_x_format_failure__mutmut['x_format_failure__mutmut_1'] = x_format_failure__mutmut_1 # type: ignore # mutmut generated
mutants_x_format_failure__mutmut['x_format_failure__mutmut_2'] = x_format_failure__mutmut_2 # type: ignore # mutmut generated
mutants_x_format_failure__mutmut['x_format_failure__mutmut_3'] = x_format_failure__mutmut_3 # type: ignore # mutmut generated
mutants_x_format_failure__mutmut['x_format_failure__mutmut_4'] = x_format_failure__mutmut_4 # type: ignore # mutmut generated
mutants_x_format_failure__mutmut['x_format_failure__mutmut_5'] = x_format_failure__mutmut_5 # type: ignore # mutmut generated
mutants_x_format_failure__mutmut['x_format_failure__mutmut_6'] = x_format_failure__mutmut_6 # type: ignore # mutmut generated
mutants_x_format_failure__mutmut['x_format_failure__mutmut_7'] = x_format_failure__mutmut_7 # type: ignore # mutmut generated
mutants_x_format_failure__mutmut['x_format_failure__mutmut_8'] = x_format_failure__mutmut_8 # type: ignore # mutmut generated
mutants_x_format_failure__mutmut['x_format_failure__mutmut_9'] = x_format_failure__mutmut_9 # type: ignore # mutmut generated
mutants_x_format_failure__mutmut['x_format_failure__mutmut_10'] = x_format_failure__mutmut_10 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁDeterministicTestsǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore
mutants_xǁDeterministicTestsǁ_test_paths__mutmut: MutantDict = {}  # type: ignore
mutants_xǁDeterministicTestsǁ_runner__mutmut: MutantDict = {}  # type: ignore
mutants_xǁDeterministicTestsǁrun__mutmut: MutantDict = {}  # type: ignore


# --------------------------------------------------------------------------- #
# The FitnessRule binding.
# --------------------------------------------------------------------------- #


class DeterministicTests(FitnessRule):
    """Gate that FAILS when a configured test suite is not run-to-run stable.

    Unlike a file-scan rule this drives the configured suite directly, so
    :meth:`run` is overridden to evaluate its process outcomes.
    """

    name = "deterministic-tests"
    remediation = REMEDIATION

    #: Rule-specific knobs (overridden from the consumer's config block).
    seed: int = DEFAULT_SEED
    repeats: int = DEFAULT_REPEATS
    order_seeds: tuple[int, ...] = DEFAULT_ORDER_SEEDS
    test_command: tuple[str, ...] = DEFAULT_TEST_COMMAND
    use_randomly: bool = False
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS

    @classmethod
    @_mutmut_mutated(mutants_xǁDeterministicTestsǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = None
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, )
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = None
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(None)
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get(None, DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", None))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get(DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", ))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("XXseedXX", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_13(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("SEED", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_14(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = None
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_15(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(None)
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_16(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get(None, DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_17(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", None))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_18(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get(DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_19(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", ))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_20(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("XXrepeatsXX", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_21(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("REPEATS", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_22(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = None
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_23(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get(None)
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_24(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("XXorder_seedsXX")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_25(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("ORDER_SEEDS")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_26(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = None
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_27(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(None) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_28(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(None) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_29(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_30(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = None
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_31(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get(None)
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_32(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("XXtest_commandXX")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_33(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("TEST_COMMAND")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_34(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = None
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_35(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(None) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_36(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(None) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_37(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = None
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_38(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(None)
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_39(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get(None, False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_40(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", None))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_41(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get(False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_42(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", ))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_43(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("XXuse_randomlyXX", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_44(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("USE_RANDOMLY", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_45(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", True))
        rule.timeout_seconds = int(config.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_46(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = None
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_47(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(None)
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_48(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get(None, DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_49(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", None))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_50(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get(DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_51(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("timeout_seconds", ))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_52(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("XXtimeout_secondsXX", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @classmethod
    def xǁDeterministicTestsǁfrom_config__mutmut_53(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> DeterministicTests:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, DeterministicTests)  # noqa: S101  # narrowing for mypy
        rule.seed = int(config.get("seed", DEFAULT_SEED))
        rule.repeats = int(config.get("repeats", DEFAULT_REPEATS))
        order_seeds = config.get("order_seeds")
        rule.order_seeds = (
            tuple(int(s) for s in order_seeds) if order_seeds is not None else DEFAULT_ORDER_SEEDS
        )
        command = config.get("test_command")
        rule.test_command = tuple(str(c) for c in command) if command else DEFAULT_TEST_COMMAND
        rule.use_randomly = bool(config.get("use_randomly", False))
        rule.timeout_seconds = int(config.get("TIMEOUT_SECONDS", DEFAULT_TIMEOUT_SECONDS))
        return rule

    @_mutmut_mutated(mutants_xǁDeterministicTestsǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:  # pragma: no cover - not used
        """Unused: determinism is a behavioural gate, not a per-file scan."""
        return False

    def xǁDeterministicTestsǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:  # pragma: no cover - not used
        """Unused: determinism is a behavioural gate, not a per-file scan."""
        return False

    def xǁDeterministicTestsǁfile_has_violation__mutmut_1(self, path: Path) -> bool:  # pragma: no cover - not used
        """Unused: determinism is a behavioural gate, not a per-file scan."""
        return True

    @_mutmut_mutated(mutants_xǁDeterministicTestsǁ_test_paths__mutmut)
    def _test_paths(self) -> list[str]:
        """The configured, on-disk test roots (repo-relative), or ``[]``."""
        return [root for root in self._roots if (self._repo_root / root).exists()]

    def xǁDeterministicTestsǁ_test_paths__mutmut_orig(self) -> list[str]:
        """The configured, on-disk test roots (repo-relative), or ``[]``."""
        return [root for root in self._roots if (self._repo_root / root).exists()]

    def xǁDeterministicTestsǁ_test_paths__mutmut_1(self) -> list[str]:
        """The configured, on-disk test roots (repo-relative), or ``[]``."""
        return [root for root in self._roots if (self._repo_root * root).exists()]

    @_mutmut_mutated(mutants_xǁDeterministicTestsǁ_runner__mutmut)
    def _runner(self, test_paths: Sequence[str], node_ids: Sequence[str]) -> Runner:
        """Bind :func:`run_suite` to this rule's config for the orchestrator."""

        def _run(spec: RunSpec) -> Mapping[str, str]:
            return run_suite(
                spec,
                command=self.test_command,
                test_paths=test_paths,
                node_ids=node_ids,
                repo_root=self._repo_root,
                seed=self.seed,
                use_randomly=self.use_randomly,
                timeout=self.timeout_seconds,
            )

        return _run

    def xǁDeterministicTestsǁ_runner__mutmut_orig(self, test_paths: Sequence[str], node_ids: Sequence[str]) -> Runner:
        """Bind :func:`run_suite` to this rule's config for the orchestrator."""

        def _run(spec: RunSpec) -> Mapping[str, str]:
            return run_suite(
                spec,
                command=self.test_command,
                test_paths=test_paths,
                node_ids=node_ids,
                repo_root=self._repo_root,
                seed=self.seed,
                use_randomly=self.use_randomly,
                timeout=self.timeout_seconds,
            )

        return _run

    def xǁDeterministicTestsǁ_runner__mutmut_1(self, test_paths: Sequence[str], node_ids: Sequence[str]) -> Runner:
        """Bind :func:`run_suite` to this rule's config for the orchestrator."""

        def _run(spec: RunSpec) -> Mapping[str, str]:
            return run_suite(
                None,
                command=self.test_command,
                test_paths=test_paths,
                node_ids=node_ids,
                repo_root=self._repo_root,
                seed=self.seed,
                use_randomly=self.use_randomly,
                timeout=self.timeout_seconds,
            )

        return _run

    def xǁDeterministicTestsǁ_runner__mutmut_2(self, test_paths: Sequence[str], node_ids: Sequence[str]) -> Runner:
        """Bind :func:`run_suite` to this rule's config for the orchestrator."""

        def _run(spec: RunSpec) -> Mapping[str, str]:
            return run_suite(
                spec,
                command=None,
                test_paths=test_paths,
                node_ids=node_ids,
                repo_root=self._repo_root,
                seed=self.seed,
                use_randomly=self.use_randomly,
                timeout=self.timeout_seconds,
            )

        return _run

    def xǁDeterministicTestsǁ_runner__mutmut_3(self, test_paths: Sequence[str], node_ids: Sequence[str]) -> Runner:
        """Bind :func:`run_suite` to this rule's config for the orchestrator."""

        def _run(spec: RunSpec) -> Mapping[str, str]:
            return run_suite(
                spec,
                command=self.test_command,
                test_paths=None,
                node_ids=node_ids,
                repo_root=self._repo_root,
                seed=self.seed,
                use_randomly=self.use_randomly,
                timeout=self.timeout_seconds,
            )

        return _run

    def xǁDeterministicTestsǁ_runner__mutmut_4(self, test_paths: Sequence[str], node_ids: Sequence[str]) -> Runner:
        """Bind :func:`run_suite` to this rule's config for the orchestrator."""

        def _run(spec: RunSpec) -> Mapping[str, str]:
            return run_suite(
                spec,
                command=self.test_command,
                test_paths=test_paths,
                node_ids=None,
                repo_root=self._repo_root,
                seed=self.seed,
                use_randomly=self.use_randomly,
                timeout=self.timeout_seconds,
            )

        return _run

    def xǁDeterministicTestsǁ_runner__mutmut_5(self, test_paths: Sequence[str], node_ids: Sequence[str]) -> Runner:
        """Bind :func:`run_suite` to this rule's config for the orchestrator."""

        def _run(spec: RunSpec) -> Mapping[str, str]:
            return run_suite(
                spec,
                command=self.test_command,
                test_paths=test_paths,
                node_ids=node_ids,
                repo_root=None,
                seed=self.seed,
                use_randomly=self.use_randomly,
                timeout=self.timeout_seconds,
            )

        return _run

    def xǁDeterministicTestsǁ_runner__mutmut_6(self, test_paths: Sequence[str], node_ids: Sequence[str]) -> Runner:
        """Bind :func:`run_suite` to this rule's config for the orchestrator."""

        def _run(spec: RunSpec) -> Mapping[str, str]:
            return run_suite(
                spec,
                command=self.test_command,
                test_paths=test_paths,
                node_ids=node_ids,
                repo_root=self._repo_root,
                seed=None,
                use_randomly=self.use_randomly,
                timeout=self.timeout_seconds,
            )

        return _run

    def xǁDeterministicTestsǁ_runner__mutmut_7(self, test_paths: Sequence[str], node_ids: Sequence[str]) -> Runner:
        """Bind :func:`run_suite` to this rule's config for the orchestrator."""

        def _run(spec: RunSpec) -> Mapping[str, str]:
            return run_suite(
                spec,
                command=self.test_command,
                test_paths=test_paths,
                node_ids=node_ids,
                repo_root=self._repo_root,
                seed=self.seed,
                use_randomly=None,
                timeout=self.timeout_seconds,
            )

        return _run

    def xǁDeterministicTestsǁ_runner__mutmut_8(self, test_paths: Sequence[str], node_ids: Sequence[str]) -> Runner:
        """Bind :func:`run_suite` to this rule's config for the orchestrator."""

        def _run(spec: RunSpec) -> Mapping[str, str]:
            return run_suite(
                spec,
                command=self.test_command,
                test_paths=test_paths,
                node_ids=node_ids,
                repo_root=self._repo_root,
                seed=self.seed,
                use_randomly=self.use_randomly,
                timeout=None,
            )

        return _run

    def xǁDeterministicTestsǁ_runner__mutmut_9(self, test_paths: Sequence[str], node_ids: Sequence[str]) -> Runner:
        """Bind :func:`run_suite` to this rule's config for the orchestrator."""

        def _run(spec: RunSpec) -> Mapping[str, str]:
            return run_suite(
                command=self.test_command,
                test_paths=test_paths,
                node_ids=node_ids,
                repo_root=self._repo_root,
                seed=self.seed,
                use_randomly=self.use_randomly,
                timeout=self.timeout_seconds,
            )

        return _run

    def xǁDeterministicTestsǁ_runner__mutmut_10(self, test_paths: Sequence[str], node_ids: Sequence[str]) -> Runner:
        """Bind :func:`run_suite` to this rule's config for the orchestrator."""

        def _run(spec: RunSpec) -> Mapping[str, str]:
            return run_suite(
                spec,
                test_paths=test_paths,
                node_ids=node_ids,
                repo_root=self._repo_root,
                seed=self.seed,
                use_randomly=self.use_randomly,
                timeout=self.timeout_seconds,
            )

        return _run

    def xǁDeterministicTestsǁ_runner__mutmut_11(self, test_paths: Sequence[str], node_ids: Sequence[str]) -> Runner:
        """Bind :func:`run_suite` to this rule's config for the orchestrator."""

        def _run(spec: RunSpec) -> Mapping[str, str]:
            return run_suite(
                spec,
                command=self.test_command,
                node_ids=node_ids,
                repo_root=self._repo_root,
                seed=self.seed,
                use_randomly=self.use_randomly,
                timeout=self.timeout_seconds,
            )

        return _run

    def xǁDeterministicTestsǁ_runner__mutmut_12(self, test_paths: Sequence[str], node_ids: Sequence[str]) -> Runner:
        """Bind :func:`run_suite` to this rule's config for the orchestrator."""

        def _run(spec: RunSpec) -> Mapping[str, str]:
            return run_suite(
                spec,
                command=self.test_command,
                test_paths=test_paths,
                repo_root=self._repo_root,
                seed=self.seed,
                use_randomly=self.use_randomly,
                timeout=self.timeout_seconds,
            )

        return _run

    def xǁDeterministicTestsǁ_runner__mutmut_13(self, test_paths: Sequence[str], node_ids: Sequence[str]) -> Runner:
        """Bind :func:`run_suite` to this rule's config for the orchestrator."""

        def _run(spec: RunSpec) -> Mapping[str, str]:
            return run_suite(
                spec,
                command=self.test_command,
                test_paths=test_paths,
                node_ids=node_ids,
                seed=self.seed,
                use_randomly=self.use_randomly,
                timeout=self.timeout_seconds,
            )

        return _run

    def xǁDeterministicTestsǁ_runner__mutmut_14(self, test_paths: Sequence[str], node_ids: Sequence[str]) -> Runner:
        """Bind :func:`run_suite` to this rule's config for the orchestrator."""

        def _run(spec: RunSpec) -> Mapping[str, str]:
            return run_suite(
                spec,
                command=self.test_command,
                test_paths=test_paths,
                node_ids=node_ids,
                repo_root=self._repo_root,
                use_randomly=self.use_randomly,
                timeout=self.timeout_seconds,
            )

        return _run

    def xǁDeterministicTestsǁ_runner__mutmut_15(self, test_paths: Sequence[str], node_ids: Sequence[str]) -> Runner:
        """Bind :func:`run_suite` to this rule's config for the orchestrator."""

        def _run(spec: RunSpec) -> Mapping[str, str]:
            return run_suite(
                spec,
                command=self.test_command,
                test_paths=test_paths,
                node_ids=node_ids,
                repo_root=self._repo_root,
                seed=self.seed,
                timeout=self.timeout_seconds,
            )

        return _run

    def xǁDeterministicTestsǁ_runner__mutmut_16(self, test_paths: Sequence[str], node_ids: Sequence[str]) -> Runner:
        """Bind :func:`run_suite` to this rule's config for the orchestrator."""

        def _run(spec: RunSpec) -> Mapping[str, str]:
            return run_suite(
                spec,
                command=self.test_command,
                test_paths=test_paths,
                node_ids=node_ids,
                repo_root=self._repo_root,
                seed=self.seed,
                use_randomly=self.use_randomly,
                )

        return _run

    @_mutmut_mutated(mutants_xǁDeterministicTestsǁrun__mutmut)
    def run(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_orig(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_1(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = None
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_2(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_3(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print(None)
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_4(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("XXok [deterministic-tests] — no test roots configured; nothing to check.XX")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_5(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("OK [DETERMINISTIC-TESTS] — NO TEST ROOTS CONFIGURED; NOTHING TO CHECK.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_6(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 1

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_7(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = None
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_8(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(None, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_9(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, None)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_10(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_11(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, )
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_12(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = None
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_13(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly or any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_14(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_15(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(None)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_16(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_17(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = None
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_18(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = None
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_19(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    None,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_20(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    None,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_21(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=None,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_22(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=None,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_23(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=None,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_24(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_25(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_26(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_27(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_28(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_29(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_30(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print(None)
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_31(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("XXok [deterministic-tests] — no tests collected under the configured roots.XX")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_32(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("OK [DETERMINISTIC-TESTS] — NO TESTS COLLECTED UNDER THE CONFIGURED ROOTS.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_33(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 1
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_34(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = None
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_35(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(None, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_36(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, None)
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_37(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_38(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, )
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_39(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(None, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_40(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, None))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_41(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_42(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, ))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_43(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith(None):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_44(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(None).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_45(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("XXconfigured test command unavailable:XX"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_46(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("CONFIGURED TEST COMMAND UNAVAILABLE:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_47(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding(None, ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_48(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", None, str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_49(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", None, status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_50(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status=None)
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_51(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding(".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_52(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_53(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_54(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), )
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_55(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("XXdependency-unavailableXX", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_56(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("DEPENDENCY-UNAVAILABLE", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_57(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", "XX.XX", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_58(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(None), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_59(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="XXerrorXX")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_60(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="ERROR")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_61(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(None)
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_62(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 3
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_63(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(None)
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_64(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(None)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_65(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 2

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_66(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding(None, divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_67(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", None, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_68(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, None)
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_69(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding(divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_70(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_71(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, )
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_72(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("XXnon-deterministic-testXX", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_73(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("NON-DETERMINISTIC-TEST", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_74(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[1][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_75(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][1])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_76(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(None)
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_77(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(None))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_78(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 2
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 0

    def xǁDeterministicTestsǁrun__mutmut_79(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(None)
        return 0

    def xǁDeterministicTestsǁrun__mutmut_80(self) -> int:
        """Run the plan; FAIL (1) on any non-determinism, else PASS (0).

        With no configured roots (the adoption default) there is nothing to run
        and the gate passes vacuously — identical to every other CORE check.
        """
        test_paths = self._test_paths()
        if not test_paths:
            print("ok [deterministic-tests] — no test roots configured; nothing to check.")
            return 0

        plan = plan_runs(self.repeats, self.order_seeds)
        need_node_ids = not self.use_randomly and any(spec.order_seed is not None for spec in plan)
        node_ids: list[str] = []
        try:
            if need_node_ids:
                node_ids = collect_node_ids(
                    self.test_command,
                    test_paths,
                    repo_root=self._repo_root,
                    seed=self.seed,
                    timeout=self.timeout_seconds,
                )
                if not node_ids:
                    print("ok [deterministic-tests] — no tests collected under the configured roots.")
                    return 0
            divergences = detect_nondeterminism(plan, self._runner(test_paths, node_ids))
        except SuiteRunError as exc:
            if str(exc).startswith("configured test command unavailable:"):
                report_finding("dependency-unavailable", ".", str(exc), status="error")
                print(f"ERROR [deterministic-tests] — {exc}")
                return 2
            print(f"FAIL [deterministic-tests] — could not establish determinism: {exc}")
            print()
            print(self.remediation)
            return 1

        if divergences:
            for divergence in divergences:
                report_finding("non-deterministic-test", divergence.test_id, divergence.outcomes[0][0])
            print(format_failure(divergences))
            return 1
        print(f"ok [deterministic-tests] — stable across {len(plan)} runs (seed={self.seed}).")
        return 1

mutants_xǁDeterministicTestsǁfrom_config__mutmut['_mutmut_orig'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_1'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_2'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_3'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_4'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_5'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_6'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_7'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_8'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_9'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_10'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_11'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_12'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_12 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_13'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_13 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_14'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_14 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_15'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_15 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_16'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_16 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_17'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_17 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_18'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_18 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_19'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_19 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_20'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_20 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_21'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_21 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_22'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_22 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_23'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_23 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_24'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_24 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_25'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_25 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_26'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_26 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_27'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_27 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_28'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_28 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_29'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_29 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_30'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_30 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_31'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_31 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_32'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_32 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_33'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_33 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_34'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_34 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_35'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_35 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_36'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_36 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_37'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_37 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_38'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_38 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_39'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_39 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_40'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_40 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_41'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_41 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_42'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_42 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_43'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_43 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_44'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_44 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_45'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_45 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_46'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_46 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_47'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_47 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_48'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_48 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_49'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_49 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_50'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_50 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_51'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_51 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_52'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_52 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfrom_config__mutmut['xǁDeterministicTestsǁfrom_config__mutmut_53'] = DeterministicTests.xǁDeterministicTestsǁfrom_config__mutmut_53 # type: ignore # mutmut generated

mutants_xǁDeterministicTestsǁfile_has_violation__mutmut['_mutmut_orig'] = DeterministicTests.xǁDeterministicTestsǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁfile_has_violation__mutmut['xǁDeterministicTestsǁfile_has_violation__mutmut_1'] = DeterministicTests.xǁDeterministicTestsǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated

mutants_xǁDeterministicTestsǁ_test_paths__mutmut['_mutmut_orig'] = DeterministicTests.xǁDeterministicTestsǁ_test_paths__mutmut_orig # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁ_test_paths__mutmut['xǁDeterministicTestsǁ_test_paths__mutmut_1'] = DeterministicTests.xǁDeterministicTestsǁ_test_paths__mutmut_1 # type: ignore # mutmut generated

mutants_xǁDeterministicTestsǁ_runner__mutmut['_mutmut_orig'] = DeterministicTests.xǁDeterministicTestsǁ_runner__mutmut_orig # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁ_runner__mutmut['xǁDeterministicTestsǁ_runner__mutmut_1'] = DeterministicTests.xǁDeterministicTestsǁ_runner__mutmut_1 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁ_runner__mutmut['xǁDeterministicTestsǁ_runner__mutmut_2'] = DeterministicTests.xǁDeterministicTestsǁ_runner__mutmut_2 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁ_runner__mutmut['xǁDeterministicTestsǁ_runner__mutmut_3'] = DeterministicTests.xǁDeterministicTestsǁ_runner__mutmut_3 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁ_runner__mutmut['xǁDeterministicTestsǁ_runner__mutmut_4'] = DeterministicTests.xǁDeterministicTestsǁ_runner__mutmut_4 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁ_runner__mutmut['xǁDeterministicTestsǁ_runner__mutmut_5'] = DeterministicTests.xǁDeterministicTestsǁ_runner__mutmut_5 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁ_runner__mutmut['xǁDeterministicTestsǁ_runner__mutmut_6'] = DeterministicTests.xǁDeterministicTestsǁ_runner__mutmut_6 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁ_runner__mutmut['xǁDeterministicTestsǁ_runner__mutmut_7'] = DeterministicTests.xǁDeterministicTestsǁ_runner__mutmut_7 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁ_runner__mutmut['xǁDeterministicTestsǁ_runner__mutmut_8'] = DeterministicTests.xǁDeterministicTestsǁ_runner__mutmut_8 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁ_runner__mutmut['xǁDeterministicTestsǁ_runner__mutmut_9'] = DeterministicTests.xǁDeterministicTestsǁ_runner__mutmut_9 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁ_runner__mutmut['xǁDeterministicTestsǁ_runner__mutmut_10'] = DeterministicTests.xǁDeterministicTestsǁ_runner__mutmut_10 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁ_runner__mutmut['xǁDeterministicTestsǁ_runner__mutmut_11'] = DeterministicTests.xǁDeterministicTestsǁ_runner__mutmut_11 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁ_runner__mutmut['xǁDeterministicTestsǁ_runner__mutmut_12'] = DeterministicTests.xǁDeterministicTestsǁ_runner__mutmut_12 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁ_runner__mutmut['xǁDeterministicTestsǁ_runner__mutmut_13'] = DeterministicTests.xǁDeterministicTestsǁ_runner__mutmut_13 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁ_runner__mutmut['xǁDeterministicTestsǁ_runner__mutmut_14'] = DeterministicTests.xǁDeterministicTestsǁ_runner__mutmut_14 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁ_runner__mutmut['xǁDeterministicTestsǁ_runner__mutmut_15'] = DeterministicTests.xǁDeterministicTestsǁ_runner__mutmut_15 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁ_runner__mutmut['xǁDeterministicTestsǁ_runner__mutmut_16'] = DeterministicTests.xǁDeterministicTestsǁ_runner__mutmut_16 # type: ignore # mutmut generated

mutants_xǁDeterministicTestsǁrun__mutmut['_mutmut_orig'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_orig # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_1'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_1 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_2'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_2 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_3'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_3 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_4'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_4 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_5'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_5 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_6'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_6 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_7'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_7 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_8'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_8 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_9'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_9 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_10'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_10 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_11'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_11 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_12'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_12 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_13'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_13 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_14'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_14 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_15'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_15 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_16'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_16 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_17'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_17 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_18'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_18 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_19'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_19 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_20'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_20 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_21'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_21 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_22'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_22 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_23'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_23 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_24'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_24 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_25'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_25 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_26'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_26 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_27'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_27 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_28'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_28 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_29'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_29 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_30'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_30 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_31'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_31 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_32'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_32 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_33'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_33 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_34'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_34 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_35'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_35 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_36'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_36 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_37'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_37 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_38'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_38 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_39'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_39 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_40'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_40 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_41'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_41 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_42'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_42 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_43'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_43 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_44'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_44 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_45'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_45 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_46'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_46 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_47'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_47 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_48'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_48 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_49'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_49 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_50'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_50 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_51'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_51 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_52'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_52 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_53'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_53 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_54'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_54 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_55'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_55 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_56'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_56 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_57'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_57 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_58'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_58 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_59'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_59 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_60'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_60 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_61'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_61 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_62'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_62 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_63'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_63 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_64'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_64 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_65'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_65 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_66'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_66 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_67'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_67 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_68'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_68 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_69'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_69 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_70'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_70 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_71'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_71 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_72'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_72 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_73'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_73 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_74'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_74 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_75'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_75 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_76'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_76 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_77'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_77 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_78'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_78 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_79'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_79 # type: ignore # mutmut generated
mutants_xǁDeterministicTestsǁrun__mutmut['xǁDeterministicTestsǁrun__mutmut_80'] = DeterministicTests.xǁDeterministicTestsǁrun__mutmut_80 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(config: Mapping[str, Any], *, repo_root: Path | None = None) -> DeterministicTests:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return DeterministicTests.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(config: Mapping[str, Any], *, repo_root: Path | None = None) -> DeterministicTests:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return DeterministicTests.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(config: Mapping[str, Any], *, repo_root: Path | None = None) -> DeterministicTests:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return DeterministicTests.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(config: Mapping[str, Any], *, repo_root: Path | None = None) -> DeterministicTests:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return DeterministicTests.from_config(config, repo_root=None)


def x_build__mutmut_3(config: Mapping[str, Any], *, repo_root: Path | None = None) -> DeterministicTests:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return DeterministicTests.from_config(repo_root=repo_root)


def x_build__mutmut_4(config: Mapping[str, Any], *, repo_root: Path | None = None) -> DeterministicTests:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return DeterministicTests.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(DeterministicTests, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(DeterministicTests, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(DeterministicTests, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(DeterministicTests, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
