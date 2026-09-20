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

from collections.abc import Generator, Iterable, Sequence
from pathlib import Path

import pytest

from tc_fitness.check_contracts import registered_contract_directory
from tc_fitness.core_checks import CORE_CHECKS
from tc_fitness.core_checks.every_test_has_tier_marker import DEFAULT_TIER_MARKERS

_COLLECTED_ITEMS = pytest.StashKey[list[pytest.Item]]()


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x_pytest_ignore_collect__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_pytest_ignore_collect__mutmut)
def pytest_ignore_collect(collection_path: Path, config: pytest.Config) -> bool | None:
    """Exclude only complete manifest-bound fixture registries from outer discovery."""
    del config
    if registered_contract_directory(collection_path, CORE_CHECKS) is not None:
        return True
    return None


def x_pytest_ignore_collect__mutmut_orig(collection_path: Path, config: pytest.Config) -> bool | None:
    """Exclude only complete manifest-bound fixture registries from outer discovery."""
    del config
    if registered_contract_directory(collection_path, CORE_CHECKS) is not None:
        return True
    return None


def x_pytest_ignore_collect__mutmut_1(collection_path: Path, config: pytest.Config) -> bool | None:
    """Exclude only complete manifest-bound fixture registries from outer discovery."""
    del config
    if registered_contract_directory(None, CORE_CHECKS) is not None:
        return True
    return None


def x_pytest_ignore_collect__mutmut_2(collection_path: Path, config: pytest.Config) -> bool | None:
    """Exclude only complete manifest-bound fixture registries from outer discovery."""
    del config
    if registered_contract_directory(collection_path, None) is not None:
        return True
    return None


def x_pytest_ignore_collect__mutmut_3(collection_path: Path, config: pytest.Config) -> bool | None:
    """Exclude only complete manifest-bound fixture registries from outer discovery."""
    del config
    if registered_contract_directory(CORE_CHECKS) is not None:
        return True
    return None


def x_pytest_ignore_collect__mutmut_4(collection_path: Path, config: pytest.Config) -> bool | None:
    """Exclude only complete manifest-bound fixture registries from outer discovery."""
    del config
    if registered_contract_directory(collection_path, ) is not None:
        return True
    return None


def x_pytest_ignore_collect__mutmut_5(collection_path: Path, config: pytest.Config) -> bool | None:
    """Exclude only complete manifest-bound fixture registries from outer discovery."""
    del config
    if registered_contract_directory(collection_path, CORE_CHECKS) is None:
        return True
    return None


def x_pytest_ignore_collect__mutmut_6(collection_path: Path, config: pytest.Config) -> bool | None:
    """Exclude only complete manifest-bound fixture registries from outer discovery."""
    del config
    if registered_contract_directory(collection_path, CORE_CHECKS) is not None:
        return False
    return None

mutants_x_pytest_ignore_collect__mutmut['_mutmut_orig'] = x_pytest_ignore_collect__mutmut_orig # type: ignore # mutmut generated
mutants_x_pytest_ignore_collect__mutmut['x_pytest_ignore_collect__mutmut_1'] = x_pytest_ignore_collect__mutmut_1 # type: ignore # mutmut generated
mutants_x_pytest_ignore_collect__mutmut['x_pytest_ignore_collect__mutmut_2'] = x_pytest_ignore_collect__mutmut_2 # type: ignore # mutmut generated
mutants_x_pytest_ignore_collect__mutmut['x_pytest_ignore_collect__mutmut_3'] = x_pytest_ignore_collect__mutmut_3 # type: ignore # mutmut generated
mutants_x_pytest_ignore_collect__mutmut['x_pytest_ignore_collect__mutmut_4'] = x_pytest_ignore_collect__mutmut_4 # type: ignore # mutmut generated
mutants_x_pytest_ignore_collect__mutmut['x_pytest_ignore_collect__mutmut_5'] = x_pytest_ignore_collect__mutmut_5 # type: ignore # mutmut generated
mutants_x_pytest_ignore_collect__mutmut['x_pytest_ignore_collect__mutmut_6'] = x_pytest_ignore_collect__mutmut_6 # type: ignore # mutmut generated
mutants_x_effective_tier_violations__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_effective_tier_violations__mutmut)
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


def x_effective_tier_violations__mutmut_orig(items: Iterable[pytest.Item]) -> tuple[str, ...]:
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


def x_effective_tier_violations__mutmut_1(items: Iterable[pytest.Item]) -> tuple[str, ...]:
    """Return node IDs and exact tier lists for missing or repeated tiers.

    Count occurrences, not distinct names: two ``unit`` marks are a violation
    just as ``unit`` plus ``integration`` is.
    """
    violations = None
    for item in items:
        tiers = [mark.name for mark in item.iter_markers() if mark.name in DEFAULT_TIER_MARKERS]
        if len(tiers) != 1:
            violations.append(f"{item.nodeid}: {tiers!r}")
    return tuple(sorted(violations))


def x_effective_tier_violations__mutmut_2(items: Iterable[pytest.Item]) -> tuple[str, ...]:
    """Return node IDs and exact tier lists for missing or repeated tiers.

    Count occurrences, not distinct names: two ``unit`` marks are a violation
    just as ``unit`` plus ``integration`` is.
    """
    violations = []
    for item in items:
        tiers = None
        if len(tiers) != 1:
            violations.append(f"{item.nodeid}: {tiers!r}")
    return tuple(sorted(violations))


def x_effective_tier_violations__mutmut_3(items: Iterable[pytest.Item]) -> tuple[str, ...]:
    """Return node IDs and exact tier lists for missing or repeated tiers.

    Count occurrences, not distinct names: two ``unit`` marks are a violation
    just as ``unit`` plus ``integration`` is.
    """
    violations = []
    for item in items:
        tiers = [mark.name for mark in item.iter_markers() if mark.name not in DEFAULT_TIER_MARKERS]
        if len(tiers) != 1:
            violations.append(f"{item.nodeid}: {tiers!r}")
    return tuple(sorted(violations))


def x_effective_tier_violations__mutmut_4(items: Iterable[pytest.Item]) -> tuple[str, ...]:
    """Return node IDs and exact tier lists for missing or repeated tiers.

    Count occurrences, not distinct names: two ``unit`` marks are a violation
    just as ``unit`` plus ``integration`` is.
    """
    violations = []
    for item in items:
        tiers = [mark.name for mark in item.iter_markers() if mark.name in DEFAULT_TIER_MARKERS]
        if len(tiers) == 1:
            violations.append(f"{item.nodeid}: {tiers!r}")
    return tuple(sorted(violations))


def x_effective_tier_violations__mutmut_5(items: Iterable[pytest.Item]) -> tuple[str, ...]:
    """Return node IDs and exact tier lists for missing or repeated tiers.

    Count occurrences, not distinct names: two ``unit`` marks are a violation
    just as ``unit`` plus ``integration`` is.
    """
    violations = []
    for item in items:
        tiers = [mark.name for mark in item.iter_markers() if mark.name in DEFAULT_TIER_MARKERS]
        if len(tiers) != 2:
            violations.append(f"{item.nodeid}: {tiers!r}")
    return tuple(sorted(violations))


def x_effective_tier_violations__mutmut_6(items: Iterable[pytest.Item]) -> tuple[str, ...]:
    """Return node IDs and exact tier lists for missing or repeated tiers.

    Count occurrences, not distinct names: two ``unit`` marks are a violation
    just as ``unit`` plus ``integration`` is.
    """
    violations = []
    for item in items:
        tiers = [mark.name for mark in item.iter_markers() if mark.name in DEFAULT_TIER_MARKERS]
        if len(tiers) != 1:
            violations.append(None)
    return tuple(sorted(violations))


def x_effective_tier_violations__mutmut_7(items: Iterable[pytest.Item]) -> tuple[str, ...]:
    """Return node IDs and exact tier lists for missing or repeated tiers.

    Count occurrences, not distinct names: two ``unit`` marks are a violation
    just as ``unit`` plus ``integration`` is.
    """
    violations = []
    for item in items:
        tiers = [mark.name for mark in item.iter_markers() if mark.name in DEFAULT_TIER_MARKERS]
        if len(tiers) != 1:
            violations.append(f"{item.nodeid}: {tiers!r}")
    return tuple(None)


def x_effective_tier_violations__mutmut_8(items: Iterable[pytest.Item]) -> tuple[str, ...]:
    """Return node IDs and exact tier lists for missing or repeated tiers.

    Count occurrences, not distinct names: two ``unit`` marks are a violation
    just as ``unit`` plus ``integration`` is.
    """
    violations = []
    for item in items:
        tiers = [mark.name for mark in item.iter_markers() if mark.name in DEFAULT_TIER_MARKERS]
        if len(tiers) != 1:
            violations.append(f"{item.nodeid}: {tiers!r}")
    return tuple(sorted(None))

mutants_x_effective_tier_violations__mutmut['_mutmut_orig'] = x_effective_tier_violations__mutmut_orig # type: ignore # mutmut generated
mutants_x_effective_tier_violations__mutmut['x_effective_tier_violations__mutmut_1'] = x_effective_tier_violations__mutmut_1 # type: ignore # mutmut generated
mutants_x_effective_tier_violations__mutmut['x_effective_tier_violations__mutmut_2'] = x_effective_tier_violations__mutmut_2 # type: ignore # mutmut generated
mutants_x_effective_tier_violations__mutmut['x_effective_tier_violations__mutmut_3'] = x_effective_tier_violations__mutmut_3 # type: ignore # mutmut generated
mutants_x_effective_tier_violations__mutmut['x_effective_tier_violations__mutmut_4'] = x_effective_tier_violations__mutmut_4 # type: ignore # mutmut generated
mutants_x_effective_tier_violations__mutmut['x_effective_tier_violations__mutmut_5'] = x_effective_tier_violations__mutmut_5 # type: ignore # mutmut generated
mutants_x_effective_tier_violations__mutmut['x_effective_tier_violations__mutmut_6'] = x_effective_tier_violations__mutmut_6 # type: ignore # mutmut generated
mutants_x_effective_tier_violations__mutmut['x_effective_tier_violations__mutmut_7'] = x_effective_tier_violations__mutmut_7 # type: ignore # mutmut generated
mutants_x_effective_tier_violations__mutmut['x_effective_tier_violations__mutmut_8'] = x_effective_tier_violations__mutmut_8 # type: ignore # mutmut generated
mutants_x_pytest_itemcollected__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_pytest_itemcollected__mutmut)
def pytest_itemcollected(item: pytest.Item) -> None:
    """Keep item references before selection so deselection cannot hide debt."""
    item.session.stash.setdefault(_COLLECTED_ITEMS, []).append(item)


def x_pytest_itemcollected__mutmut_orig(item: pytest.Item) -> None:
    """Keep item references before selection so deselection cannot hide debt."""
    item.session.stash.setdefault(_COLLECTED_ITEMS, []).append(item)


def x_pytest_itemcollected__mutmut_1(item: pytest.Item) -> None:
    """Keep item references before selection so deselection cannot hide debt."""
    item.session.stash.setdefault(_COLLECTED_ITEMS, []).append(None)


def x_pytest_itemcollected__mutmut_2(item: pytest.Item) -> None:
    """Keep item references before selection so deselection cannot hide debt."""
    item.session.stash.setdefault(None, []).append(item)


def x_pytest_itemcollected__mutmut_3(item: pytest.Item) -> None:
    """Keep item references before selection so deselection cannot hide debt."""
    item.session.stash.setdefault(_COLLECTED_ITEMS, None).append(item)


def x_pytest_itemcollected__mutmut_4(item: pytest.Item) -> None:
    """Keep item references before selection so deselection cannot hide debt."""
    item.session.stash.setdefault([]).append(item)


def x_pytest_itemcollected__mutmut_5(item: pytest.Item) -> None:
    """Keep item references before selection so deselection cannot hide debt."""
    item.session.stash.setdefault(_COLLECTED_ITEMS, ).append(item)

mutants_x_pytest_itemcollected__mutmut['_mutmut_orig'] = x_pytest_itemcollected__mutmut_orig # type: ignore # mutmut generated
mutants_x_pytest_itemcollected__mutmut['x_pytest_itemcollected__mutmut_1'] = x_pytest_itemcollected__mutmut_1 # type: ignore # mutmut generated
mutants_x_pytest_itemcollected__mutmut['x_pytest_itemcollected__mutmut_2'] = x_pytest_itemcollected__mutmut_2 # type: ignore # mutmut generated
mutants_x_pytest_itemcollected__mutmut['x_pytest_itemcollected__mutmut_3'] = x_pytest_itemcollected__mutmut_3 # type: ignore # mutmut generated
mutants_x_pytest_itemcollected__mutmut['x_pytest_itemcollected__mutmut_4'] = x_pytest_itemcollected__mutmut_4 # type: ignore # mutmut generated
mutants_x_pytest_itemcollected__mutmut['x_pytest_itemcollected__mutmut_5'] = x_pytest_itemcollected__mutmut_5 # type: ignore # mutmut generated
mutants_x_pytest_deselected__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_pytest_deselected__mutmut)
def pytest_deselected(items: Sequence[pytest.Item]) -> None:
    """Retain hook-created items when a collection hook deselects them."""
    for item in items:
        item.session.stash.setdefault(_COLLECTED_ITEMS, []).append(item)


def x_pytest_deselected__mutmut_orig(items: Sequence[pytest.Item]) -> None:
    """Retain hook-created items when a collection hook deselects them."""
    for item in items:
        item.session.stash.setdefault(_COLLECTED_ITEMS, []).append(item)


def x_pytest_deselected__mutmut_1(items: Sequence[pytest.Item]) -> None:
    """Retain hook-created items when a collection hook deselects them."""
    for item in items:
        item.session.stash.setdefault(_COLLECTED_ITEMS, []).append(None)


def x_pytest_deselected__mutmut_2(items: Sequence[pytest.Item]) -> None:
    """Retain hook-created items when a collection hook deselects them."""
    for item in items:
        item.session.stash.setdefault(None, []).append(item)


def x_pytest_deselected__mutmut_3(items: Sequence[pytest.Item]) -> None:
    """Retain hook-created items when a collection hook deselects them."""
    for item in items:
        item.session.stash.setdefault(_COLLECTED_ITEMS, None).append(item)


def x_pytest_deselected__mutmut_4(items: Sequence[pytest.Item]) -> None:
    """Retain hook-created items when a collection hook deselects them."""
    for item in items:
        item.session.stash.setdefault([]).append(item)


def x_pytest_deselected__mutmut_5(items: Sequence[pytest.Item]) -> None:
    """Retain hook-created items when a collection hook deselects them."""
    for item in items:
        item.session.stash.setdefault(_COLLECTED_ITEMS, ).append(item)

mutants_x_pytest_deselected__mutmut['_mutmut_orig'] = x_pytest_deselected__mutmut_orig # type: ignore # mutmut generated
mutants_x_pytest_deselected__mutmut['x_pytest_deselected__mutmut_1'] = x_pytest_deselected__mutmut_1 # type: ignore # mutmut generated
mutants_x_pytest_deselected__mutmut['x_pytest_deselected__mutmut_2'] = x_pytest_deselected__mutmut_2 # type: ignore # mutmut generated
mutants_x_pytest_deselected__mutmut['x_pytest_deselected__mutmut_3'] = x_pytest_deselected__mutmut_3 # type: ignore # mutmut generated
mutants_x_pytest_deselected__mutmut['x_pytest_deselected__mutmut_4'] = x_pytest_deselected__mutmut_4 # type: ignore # mutmut generated
mutants_x_pytest_deselected__mutmut['x_pytest_deselected__mutmut_5'] = x_pytest_deselected__mutmut_5 # type: ignore # mutmut generated


@pytest.hookimpl(wrapper=True, tryfirst=True)
def pytest_collection_finish(session: pytest.Session) -> Generator[None, None, None]:
    """Check after ordinary collection hooks, without changing selected items."""
    yield
    # Include items introduced/replaced by collection hooks as well as originals.
    items = dict.fromkeys([*session.stash.get(_COLLECTED_ITEMS, []), *session.items])
    violations = effective_tier_violations(items)
    if violations:
        raise pytest.UsageError("items must have exactly one effective tier:\n" + "\n".join(violations))
