"""Exact timestamp arithmetic behind the real-clock public admission boundary."""

from datetime import UTC, datetime, timedelta

import pytest

from tc_fitness.mutation_assurance import _validate_execution_timestamps
from tc_fitness.mutation_scope import MutationError

pytestmark = pytest.mark.unit


@pytest.mark.parametrize("age", [0, 86400])
def test_execution_accepts_exact_now_and_twenty_four_hour_boundaries(age: int) -> None:
    now = datetime(2026, 9, 19, tzinfo=UTC)
    stamp = (now - timedelta(seconds=age)).isoformat()
    _validate_execution_timestamps({"started_at": stamp, "finished_at": stamp}, now)


@pytest.mark.parametrize("age", [-0.000001, 86400.000001])
def test_execution_rejects_one_microsecond_outside_accepted_interval(age: float) -> None:
    now = datetime(2026, 9, 19, tzinfo=UTC)
    stamp = (now - timedelta(seconds=age)).isoformat()
    with pytest.raises(MutationError, match=r"^stale or reversed mutation execution timestamps$"):
        _validate_execution_timestamps({"started_at": stamp, "finished_at": stamp}, now)


def test_execution_rejects_reversed_interval_inside_fresh_window() -> None:
    now = datetime(2026, 9, 19, tzinfo=UTC)
    with pytest.raises(MutationError, match=r"^stale or reversed mutation execution timestamps$"):
        _validate_execution_timestamps(
            {"started_at": now.isoformat(), "finished_at": (now - timedelta(microseconds=1)).isoformat()},
            now,
        )
