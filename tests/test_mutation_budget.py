"""The mutation campaign budget is derived from measurement, not declared.

An absolute bound conflates two independent things — how much work a change
demands, and how fast the machine running it is — so it can only ever be right
on the machine it was tuned on. Worse, it fails silently: a campaign cut off
before it evaluates a mutant reports the same way whether the number was too
small or the code untested.
"""

from __future__ import annotations

import os
import tomllib
from pathlib import Path

import pytest
import yaml

from tc_fitness import mutation_assurance, mutation_scope

pytestmark = pytest.mark.unit

_BUDGET = {
    "baseline_multiplier": 4,
    "per_function_multiplier": 1.5,
    "floor_seconds": 120,
    "ceiling_seconds": 2400,
}


def test_budget_scales_with_the_machine() -> None:
    """The same change on a slower runner legitimately needs longer."""
    fast = mutation_scope.derive_budget(_BUDGET, baseline_seconds=10, changed_functions=40, workers=1)
    slow = mutation_scope.derive_budget(_BUDGET, baseline_seconds=30, changed_functions=40, workers=1)
    assert slow > fast


def test_budget_scales_with_the_change() -> None:
    """A campaign's cost comes from the mutants, and those come from the scope."""
    small = mutation_scope.derive_budget(_BUDGET, baseline_seconds=20, changed_functions=5, workers=1)
    large = mutation_scope.derive_budget(_BUDGET, baseline_seconds=20, changed_functions=200, workers=1)
    assert large > small


def test_budget_never_falls_below_the_floor() -> None:
    """A fast machine and a tiny change must still get a usable budget."""
    assert mutation_scope.derive_budget(_BUDGET, baseline_seconds=0.1, changed_functions=1, workers=1) == 120


def test_budget_never_exceeds_the_ceiling() -> None:
    """The ceiling is what still catches a hang; scope cannot argue past it."""
    assert (
        mutation_scope.derive_budget(_BUDGET, baseline_seconds=60, changed_functions=5000, workers=1) == 2400
    )


def test_a_failed_baseline_measurement_falls_back_to_the_floor() -> None:
    """A zero baseline must not grant a zero budget."""
    assert mutation_scope.derive_budget(_BUDGET, baseline_seconds=0, changed_functions=10, workers=1) == 120


def test_policy_requires_every_budget_field() -> None:
    incomplete = {k: v for k, v in _BUDGET.items() if k != "floor_seconds"}
    with pytest.raises(mutation_scope.MutationError, match="budget requires exactly"):
        mutation_scope._validate_budget(incomplete)


def test_policy_rejects_a_non_positive_budget_term() -> None:
    with pytest.raises(mutation_scope.MutationError, match="positive number"):
        mutation_scope._validate_budget({**_BUDGET, "baseline_multiplier": 0})


def test_policy_rejects_an_inverted_clamp() -> None:
    """A floor above the ceiling is a contradiction, not a preference."""
    with pytest.raises(mutation_scope.MutationError, match="cannot exceed"):
        mutation_scope._validate_budget({**_BUDGET, "floor_seconds": 5000})


def test_policy_caps_the_ceiling() -> None:
    """An unbounded ceiling would retire hang detection entirely."""
    with pytest.raises(mutation_scope.MutationError, match="must not exceed"):
        mutation_scope._validate_budget({**_BUDGET, "ceiling_seconds": 99999})


def test_the_declared_policy_satisfies_its_own_schema() -> None:
    """The repository's own mutation.toml must be a valid budget."""
    import tomllib
    from pathlib import Path

    policy = tomllib.loads(
        (Path(__file__).resolve().parents[1] / "mutation.toml").read_text(encoding="utf-8")
    )
    mutation_scope._validate_budget(policy["budget"])


def test_the_baseline_times_the_same_tests_the_campaign_runs(tmp_path: Path) -> None:
    """A baseline over a wider selection would fund work the campaign never does."""
    files = {"pyproject.toml": b"[project]\nname = 'x'\n"}
    policy = {"source_roots": ["src"], "tests": ["tests"]}
    (tmp_path / "pyproject.toml").write_bytes(files["pyproject.toml"])
    mutation_assurance._native_config(tmp_path, files, policy)
    controls = tomllib.loads((tmp_path / "pyproject.toml").read_text())["tool"]["mutmut"]

    assert controls["pytest_add_cli_args"] == list(mutation_assurance.CAMPAIGN_TEST_ARGS)
    assert controls["pytest_add_cli_args_test_selection"] == policy["tests"]


def test_the_baseline_command_carries_the_campaign_selection(monkeypatch: pytest.MonkeyPatch) -> None:
    """The measured command is the campaign's selection, not the whole suite."""
    captured: dict[str, object] = {}

    def record(command: list[str], **kwargs: object) -> None:
        captured["command"] = command

    monkeypatch.setattr(mutation_assurance, "run_bounded_process", record)
    policy = {"tests": ["tests"], "budget": dict(_BUDGET)}
    mutation_assurance._measure_baseline(Path("."), {}, policy, Path("."))
    command = captured["command"]

    assert isinstance(command, list)
    for argument in mutation_assurance.CAMPAIGN_TEST_ARGS:
        assert argument in command


# -- the derived bound is only real if nothing outside it binds first ---------

#: Checkout and dependency install, measured from CI runs at roughly ninety
#: seconds. The margin is generous because being wrong the other way costs a
#: cancelled job with no receipt, which is the exact failure this ordering
#: exists to prevent.
SETUP_HEADROOM_SECONDS = 300

REPO_ROOT = Path(__file__).resolve().parent.parent


def _mutation_job() -> dict[str, object]:
    workflow = yaml.safe_load((REPO_ROOT / ".github/workflows/ci.yml").read_text())
    return dict(workflow["jobs"]["changed-mutation"])


def test_the_ci_job_outlasts_the_largest_budget_the_policy_can_grant() -> None:
    """A job that expires first cancels the campaign and leaves no receipt.

    The budget is only a budget if the campaign is what enforces it. When the
    runner's own timeout is the smaller number the campaign is killed mid-run,
    and the operator is told the job was cancelled rather than which bound was
    exhausted — the silent failure the derived budget replaced.
    """
    policy = tomllib.loads((REPO_ROOT / "mutation.toml").read_text())
    granted = policy["budget"]["ceiling_seconds"]
    job_seconds = int(_mutation_job()["timeout-minutes"]) * 60

    assert job_seconds >= granted + SETUP_HEADROOM_SECONDS


def test_the_policy_ceiling_cannot_exceed_the_schema_ceiling() -> None:
    """The schema bound is the outer limit any repository may declare."""
    policy = tomllib.loads((REPO_ROOT / "mutation.toml").read_text())

    assert policy["budget"]["ceiling_seconds"] <= mutation_scope.BUDGET_CEILING


def test_budget_scales_down_with_parallelism() -> None:
    """Four times the mutants at once is a quarter of the wall clock.

    Both grants sit inside the clamp by construction, so this tests the division
    rather than the floor and ceiling either side of it.
    """
    serial = mutation_scope.derive_budget(_BUDGET, baseline_seconds=10, changed_functions=50, workers=1)
    parallel = mutation_scope.derive_budget(_BUDGET, baseline_seconds=10, changed_functions=50, workers=4)

    assert _BUDGET["floor_seconds"] < parallel < serial < _BUDGET["ceiling_seconds"]
    assert parallel * 4 == pytest.approx(serial, abs=4)


def test_budget_refuses_a_campaign_with_no_workers() -> None:
    """Dividing work across no workers is not a budget, it is a crash."""
    with pytest.raises(mutation_scope.MutationError):
        mutation_scope.derive_budget(_BUDGET, baseline_seconds=20, changed_functions=10, workers=0)


def test_workers_come_from_the_machine_not_a_constant() -> None:
    """A fixed worker count describes the machine it was written on."""
    assert mutation_assurance.campaign_workers() == len(os.sched_getaffinity(0))


def test_workers_never_fall_below_one(monkeypatch: pytest.MonkeyPatch) -> None:
    """A campaign evaluating nothing in parallel still evaluates something."""
    monkeypatch.setattr(mutation_assurance.os, "sched_getaffinity", lambda _pid: set())

    assert mutation_assurance.campaign_workers() == 1
