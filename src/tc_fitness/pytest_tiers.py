"""Opt-in pytest assurance for exactly one effective canonical tier per item.

Run ``pytest -p tc_fitness.pytest_tiers`` (or add it to pytest's ``addopts``).
This plugin complements the canonical source rule: actual collected markers,
including those supplied by imported decorators and collection hooks, decide
the runtime verdict. It neither launches pytest nor interprets source code.

The vocabulary is canonical and cannot be narrowed through consumer config.
Tests/plugins are trusted execution inputs; this is collection assurance, not
a sandbox against a plugin that disables assurance or changes markers later.
"""

from __future__ import annotations

from collections.abc import Generator, Iterable

import pytest

from tc_fitness.core_checks.every_test_has_tier_marker import DEFAULT_TIER_MARKERS

_COLLECTED_ITEMS = pytest.StashKey[list[pytest.Item]]()


def effective_tier_violations(items: Iterable[pytest.Item]) -> tuple[str, ...]:
    """Return node IDs and exact tier lists for missing or repeated tiers.

    Count occurrences, not distinct names: two ``unit`` marks are a violation
    just as ``unit`` plus ``integration`` is.
    """
    violations = []
    for item in items:
        tiers = [mark.name for mark in item.iter_markers() if mark.name in DEFAULT_TIER_MARKERS]
        if len(tiers) != 1:
            violations.append(f"{item.nodeid}: {tiers!r}")
    return tuple(sorted(violations))


def pytest_itemcollected(item: pytest.Item) -> None:
    """Keep item references before selection so deselection cannot hide debt."""
    item.session.stash.setdefault(_COLLECTED_ITEMS, []).append(item)


@pytest.hookimpl(wrapper=True, tryfirst=True)
def pytest_collection_finish(session: pytest.Session) -> Generator[None, None, None]:
    """Check after ordinary collection hooks, without changing selected items."""
    yield
    # Include items introduced/replaced by collection hooks as well as originals.
    items = dict.fromkeys([*session.stash.get(_COLLECTED_ITEMS, []), *session.items])
    violations = effective_tier_violations(items)
    if violations:
        raise pytest.UsageError("items must have exactly one effective tier:\n" + "\n".join(violations))
