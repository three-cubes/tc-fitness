"""Declarative gate config — the ``[tool.tc_fitness]`` block a consumer declares.

The ``tc-fitness run`` command (:mod:`tc_fitness.gate`) is the SINGLE runnable
gate both CI and local invoke. It runs no repo-specific logic of its own: every
repo-specific detail — which tests to run, with which ``--cov`` roots, which
ruff / bandit targets, the detect-secrets baseline, the consumer's own
fitness-check catalogue — is CONFIG, read from this block at run time. The engine
is a step ORCHESTRATOR; the steps themselves are the consumer's declaration.

Why config, not parameters
--------------------------
A reusable CI workflow that took ``pytest-args`` / ``cov-roots`` / ``ruff-paths``
as *workflow inputs* just relocates the per-repo logic into YAML — every caller
must still pass the right strings, and local and CI drift the moment one is
edited without the other. Declaring the gate ONCE, in a file the repo owns and
both surfaces read, is what makes ``local == CI`` true by construction. Nothing
in this module — or anywhere in the engine — may hard-code a consumer's pytest
scope, cov roots, or check-catalogue path.

Where the block lives
---------------------
Resolution order (first found wins):

1. ``.tc-fitness.toml`` at the repo root, whose top-level table IS the config
   (no ``[tool.tc_fitness]`` wrapper) — for a repo that prefers a dedicated file.
2. ``[tool.tc_fitness]`` inside the repo root ``pyproject.toml``.

The schema
----------
``[tool.tc_fitness]``::

    [tool.tc_fitness]
    # Optional: a label printed in the run banner.
    name = "tc-agent-zone quality gate"
    # Optional: stop at the first failing step instead of running them all and
    # aggregating (default false — run every step, report the full ledger).
    fail_fast = false

    # The ordered list of steps. Each is one table in this array. Order is the
    # array order; the engine runs them top to bottom.
    [[tool.tc_fitness.steps]]
    id = "ruff"                       # required — the ledger label + --only selector
    summary = "ruff lint"             # optional — one-line description in the ledger
    run = ["ruff", "check", "scripts", "tests"]   # a command vector (argv), OR…
    # shell = "ruff check $(git ls-files '*.py')" # …a shell string (run via the shell)
    cwd = "."                         # optional — relative to repo root (default ".")
    env = { RUFF_CACHE_DIR = ".ruff_cache" }  # optional — extra env for this step
    allow_missing = false             # optional — if the program isn't on PATH,
                                      #   skip (true) vs FAIL (false, default)
    fix = "run `ruff check --fix`"    # optional — the agent-actionable fix: line
    next = "re-run tc-fitness run"    #   shown under this step's FAIL
    continue_on_error = false         # optional — record FAIL but don't gate the
                                      #   aggregate (informational steps)

    # The catalogue step is special: instead of `run`/`shell` it names the
    # consumer's RuleEntry catalogue, and the engine dispatches it IN-PROCESS via
    # tc_fitness.runner.main_cli — no subprocess, no second python boot.
    [[tool.tc_fitness.steps]]
    id = "fitness-catalogue"
    summary = "architecture fitness functions"
    catalogue = "scripts.checks._rule_catalogue:ALL_ENTRIES"  # module:attr
    checks_dir = "scripts/checks"     # optional — where check_*.py / *.sh live
    dispatch = "subprocess"           # optional — "inprocess" (default) | "subprocess"
    parallel = true                   # optional — parallel subprocess dispatch

Exactly one of ``run`` / ``shell`` / ``catalogue`` is required per step.
"""

from __future__ import annotations

import heapq
import tomllib  # stdlib since 3.11; requires-python is >=3.12
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


class GateConfigError(ValueError):
    """A malformed or missing ``[tool.tc_fitness]`` gate declaration.

    Carries an agent-actionable message (``<what>; fix: <fix>; next: <next>``)
    so a misconfiguration reads the same as any other gate failure."""


#: The two well-known config locations, in resolution order.
_DEDICATED_FILE = ".tc-fitness.toml"
_PYPROJECT = "pyproject.toml"

_DISPATCH_MODES = ("inprocess", "subprocess")

#: The sub-table under ``[tool.tc_fitness]`` keyed by CORE-check module name that
#: carries each bound CORE check's config block. A consumer writes
#: ``[tool.tc_fitness.core_checks.no_duplicate_string]`` (in pyproject.toml) or
#: ``[core_checks.no_duplicate_string]`` (in a dedicated ``.tc-fitness.toml``);
#: the engine injects the matching block into the rule via
#: :meth:`tc_fitness.fitness_rule.FitnessRule.from_config` when it dispatches a
#: ``core:<module>`` catalogue entry.
_CORE_CHECKS_KEY = "core_checks"


@dataclass(frozen=True)
class StepSpec:
    """One declared gate step — a command vector, a shell string, OR a catalogue.

    Exactly one of ``run`` / ``shell`` / ``catalogue`` is set; the loader
    enforces this. Every other field is optional and defaults to a safe value, so
    a minimal step is just ``{id = "x", run = [...]}``.
    """

    id: str
    summary: str = ""
    #: A command vector (argv). Mutually exclusive with ``shell`` / ``catalogue``.
    run: tuple[str, ...] | None = None
    #: A shell command string, run through the shell. Mutually exclusive.
    shell: str | None = None
    #: A consumer catalogue reference ``module.path:attr`` — dispatched in-process
    #: via :func:`tc_fitness.runner.main_cli`. Mutually exclusive.
    catalogue: str | None = None
    #: Working dir relative to the repo root (default the repo root).
    cwd: str = "."
    #: Extra environment variables for this step (merged over the inherited env).
    env: dict[str, str] = field(default_factory=dict)
    #: When the program isn't on PATH: skip the step (True) or FAIL it (False).
    allow_missing: bool = False
    #: Record a FAIL but don't gate the aggregate exit (informational steps).
    continue_on_error: bool = False
    #: Agent-actionable remediation shown under this step's FAIL.
    fix: str = ""
    next: str = ""
    #: Catalogue-only: where the check_*.py / *.sh scripts live (repo-relative).
    checks_dir: str | None = None
    #: Catalogue-only: dispatch mode + parallelism (mirrors the runner kwargs).
    dispatch: str = "inprocess"
    parallel: bool = False
    #: Whether to drop this step from the ``--staged`` smoke tier. The ``<60s``
    #: smoke runs the catalogue step(s) in the sound per-rule ``--staged`` mode
    #: and the CHEAP legs (lint / format / branch-naming) verbatim; a repo sets
    #: ``skip_when_staged = true`` on its EXPENSIVE full-tree legs (a full
    #: ``pytest`` / ``mypy --strict`` over the whole tree) so the smoke stays
    #: fast. Default ``false`` (a step runs in the smoke unless it opts out) —
    #: the engine bakes in no policy about which legs are "expensive"; the repo
    #: declares it.
    skip_when_staged: bool = False
    #: Extra argv appended to a ``run`` step's command when ``tc-fitness run
    #: --shard i/N`` is passed, with ``{index}`` (the 1-based shard i) and
    #: ``{total}`` (N) substituted per token — e.g.
    #: ``["--splits", "{total}", "--group", "{index}"]`` for pytest-split. The
    #: engine also sets ``COVERAGE_FILE=.coverage.<i>`` on that step so a
    #: downstream ``coverage combine`` merges the shards. Empty (the default)
    #: means the step is shard-agnostic: ``--shard`` leaves it byte-identical.
    #: The engine hardcodes no splitter — the tokens are the consumer's
    #: declaration.
    shard_args: tuple[str, ...] = ()
    #: The concurrency group this step belongs to. Steps sharing one non-``None``
    #: ``stage`` value run CONCURRENTLY within that stage (subprocess ``run`` /
    #: ``shell`` steps on a bounded worker pool; an in-process ``catalogue`` step
    #: on the main thread, overlapping the pool). ``None`` (the default) makes the
    #: step its OWN singleton stage, so a config with no ``stage`` / ``depends_on``
    #: anywhere reduces to today's sequential registration-order run —
    #: byte-identically. See :func:`plan_stages`.
    stage: str | None = None
    #: Stage names that must fully complete before this step's stage starts (a
    #: barrier). Declared per-step but semantic at the stage level: a stage's
    #: predecessor set is the UNION of its members' ``depends_on``. Empty (the
    #: default) makes the stage implicitly depend on the stage immediately before
    #: it in first-appearance order — the chain that preserves sequential
    #: back-compat; a non-empty value OVERRIDES that implicit chain. An unknown
    #: target or a dependency cycle is a :class:`GateConfigError` at load time.
    depends_on: tuple[str, ...] = ()
    #: Tier membership for the ``--tier <name>`` selector. A step runs under
    #: ``--tier X`` iff ``X`` is in ``tags``. Empty (the default) = the step is in
    #: no named tier (it runs only in an untiered ``tc-fitness run``). Orthogonal
    #: to ``stage``: ``tags`` pick WHICH steps run; ``stage`` groups HOW they run.
    tags: tuple[str, ...] = ()

    @property
    def kind(self) -> str:
        """``"run"`` | ``"shell"`` | ``"catalogue"`` — which action this step is."""
        if self.run is not None:
            return "run"
        if self.shell is not None:
            return "shell"
        return "catalogue"


@dataclass(frozen=True)
class GateConfig:
    """The resolved ``[tool.tc_fitness]`` gate declaration."""

    steps: tuple[StepSpec, ...]
    name: str = "tc-fitness gate"
    fail_fast: bool = False
    #: Bound on the per-stage subprocess worker pool (concern-parallelism). Mirrors
    #: ``runner._DEFAULT_MAX_WORKERS``. Only relevant when steps declare ``stage``.
    max_workers: int = 8
    #: The file the config was read from (for the banner + error messages).
    source: Path | None = None


@dataclass(frozen=True)
class Stage:
    """One concurrency group + its predecessor stages, in execution position."""

    name: str
    steps: tuple[StepSpec, ...]
    depends_on: frozenset[str]


def plan_stages(steps: Sequence[StepSpec], *, strict: bool = True) -> tuple[Stage, ...]:
    """Group ``steps`` into stages in a deterministic topological execution order.

    Grouping: steps sharing a non-``None`` ``stage`` form one stage; a
    ``stage is None`` step is its own singleton stage keyed by position — so a
    config with no stages yields one singleton stage per step in registration
    order.

    Dependencies: a stage's predecessor set is the UNION of its members'
    ``depends_on``; when that union is empty the stage implicitly depends on the
    stage immediately before it in first-appearance order (the sequential chain).

    Order: Kahn's algorithm, ties broken by first-appearance index — so a
    singleton-only config topo-sorts to EXACTLY registration order.

    ``strict`` (config-load validation over the full step set): a ``depends_on``
    naming an unknown stage, or a self-dependency, raises :class:`GateConfigError`.
    Non-strict (run time, after ``--only`` / ``--tier`` filtering removed some
    stages): an absent dependency is dropped. A dependency cycle ALWAYS raises.
    """
    # 1. Bucket into stages, preserving first-appearance order. A stage-less step
    #    gets a unique positional key so it stays its own singleton stage.
    keys: list[str] = []
    members: dict[str, list[StepSpec]] = {}
    explicit: dict[str, set[str]] = {}
    named: set[str] = {s.stage for s in steps if s.stage is not None}
    for pos, s in enumerate(steps):
        key = s.stage if s.stage is not None else f"\x00{pos}"  # sentinel: unref-able name
        if key not in members:
            keys.append(key)
            members[key] = []
            explicit[key] = set()
        members[key].append(s)
        explicit[key].update(s.depends_on)

    first_index = {key: i for i, key in enumerate(keys)}

    # 2. Resolve each stage's predecessor set: explicit union, else the implicit
    #    "previous stage in first-appearance order" chain (sequential back-compat).
    deps: dict[str, set[str]] = {}
    for i, key in enumerate(keys):
        dep = set(explicit[key])
        if dep:
            for target in sorted(dep):
                if target == key:
                    raise GateConfigError(
                        f"stage {key!r} depends on itself; "
                        "fix: remove the self-reference from `depends_on`; next: re-run tc-fitness run"
                    )
                if target not in named:
                    if strict:
                        raise GateConfigError(
                            f"stage {key!r} depends_on unknown stage {target!r}; "
                            f"fix: reference a declared stage name (one of {sorted(named)}); "
                            "next: re-run tc-fitness run"
                        )
                    dep.discard(target)  # filtered out by --only/--tier: drop the dangling edge
        elif i > 0:
            dep = {keys[i - 1]}
        deps[key] = dep

    # 3. Kahn topo-sort, ties broken by first-appearance index (singleton-only ⇒
    #    registration order).
    indeg = {key: len(deps[key]) for key in keys}
    succ: dict[str, list[str]] = {key: [] for key in keys}
    for key in keys:
        for d in deps[key]:
            succ[d].append(key)
    ready = [first_index[key] for key in keys if indeg[key] == 0]
    heapq.heapify(ready)
    order: list[str] = []
    while ready:
        key = keys[heapq.heappop(ready)]
        order.append(key)
        for nxt in succ[key]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                heapq.heappush(ready, first_index[nxt])
    if len(order) != len(keys):
        unresolved = sorted(set(keys) - set(order), key=lambda k: first_index[k])
        cyc = [k for k in unresolved if not k.startswith("\x00")]
        raise GateConfigError(
            f"dependency cycle among stages {cyc}; "
            "fix: break the `depends_on` cycle; next: re-run tc-fitness run"
        )
    return tuple(Stage(name=key, steps=tuple(members[key]), depends_on=frozenset(deps[key])) for key in order)


def find_config_file(repo_root: Path) -> Path | None:
    """Return the gate-config file under ``repo_root``, or ``None`` if neither
    well-known location exists. ``.tc-fitness.toml`` wins over ``pyproject.toml``."""
    dedicated = repo_root / _DEDICATED_FILE
    if dedicated.is_file():
        return dedicated
    pyproject = repo_root / _PYPROJECT
    if pyproject.is_file():
        return pyproject
    return None


def _raw_table(path: Path) -> dict[str, Any]:
    """Parse ``path`` and return the tc_fitness config table.

    For ``.tc-fitness.toml`` the whole document is the config; for
    ``pyproject.toml`` it is the ``[tool.tc_fitness]`` sub-table."""
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise GateConfigError(
            f"could not parse gate config {path}: {exc}; "
            f"fix: correct the TOML syntax in {path.name}; "
            "next: re-run tc-fitness run"
        ) from exc
    if path.name == _DEDICATED_FILE:
        return data
    tool = data.get("tool")
    if not isinstance(tool, dict) or "tc_fitness" not in tool:
        raise GateConfigError(
            f"no [tool.tc_fitness] table in {path}; "
            f"fix: add a [tool.tc_fitness] block (or a {_DEDICATED_FILE} file) "
            "declaring the gate's steps; "
            "next: see tc_fitness.gate_config for the schema, then re-run tc-fitness run"
        )
    table = tool["tc_fitness"]
    if not isinstance(table, dict):
        raise GateConfigError(
            f"[tool.tc_fitness] in {path} must be a table; "
            "fix: make it a TOML table with a `steps` array; "
            "next: re-run tc-fitness run"
        )
    return table


def _coerce_str_tuple(value: Any, *, field_name: str, step_id: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
        raise GateConfigError(
            f"step {step_id!r} `{field_name}` must be a list of strings; "
            f'fix: write `{field_name} = ["prog", "arg"]`; '
            "next: re-run tc-fitness run"
        )
    return tuple(value)


def _coerce_env(value: Any, *, step_id: str) -> dict[str, str]:
    if not isinstance(value, dict) or not all(
        isinstance(k, str) and isinstance(v, str) for k, v in value.items()
    ):
        raise GateConfigError(
            f"step {step_id!r} `env` must be a table of string→string; "
            'fix: write `env = { KEY = "value" }`; '
            "next: re-run tc-fitness run"
        )
    return dict(value)


def _parse_step(raw: Any, *, index: int, source: Path) -> StepSpec:
    if not isinstance(raw, dict):
        raise GateConfigError(
            f"step #{index} in {source.name} is not a table; "
            "fix: declare each step as a [[tool.tc_fitness.steps]] table; "
            "next: re-run tc-fitness run"
        )
    step_id = raw.get("id")
    if not isinstance(step_id, str) or not step_id:
        raise GateConfigError(
            f"step #{index} in {source.name} is missing a string `id`; "
            'fix: add `id = "<short-label>"` to the step; '
            "next: re-run tc-fitness run"
        )

    action_keys = [k for k in ("run", "shell", "catalogue") if k in raw]
    if len(action_keys) != 1:
        raise GateConfigError(
            f"step {step_id!r} must declare EXACTLY ONE of run / shell / catalogue "
            f"(found {action_keys or 'none'}); "
            "fix: pick one action per step; "
            "next: re-run tc-fitness run"
        )

    run = _coerce_str_tuple(raw["run"], field_name="run", step_id=step_id) if "run" in raw else None
    shell = raw.get("shell")
    if shell is not None and not isinstance(shell, str):
        raise GateConfigError(
            f"step {step_id!r} `shell` must be a string; "
            'fix: write `shell = "cmd | filter"`; next: re-run tc-fitness run'
        )
    catalogue = raw.get("catalogue")
    if catalogue is not None and (not isinstance(catalogue, str) or ":" not in catalogue):
        raise GateConfigError(
            f"step {step_id!r} `catalogue` must be a `module.path:attr` string; "
            'fix: write `catalogue = "scripts.checks._rule_catalogue:ALL_ENTRIES"`; '
            "next: re-run tc-fitness run"
        )

    dispatch = raw.get("dispatch", "inprocess")
    if dispatch not in _DISPATCH_MODES:
        raise GateConfigError(
            f"step {step_id!r} `dispatch` must be one of {_DISPATCH_MODES}; "
            'fix: set `dispatch = "subprocess"` or omit for the default; '
            "next: re-run tc-fitness run"
        )

    env = _coerce_env(raw["env"], step_id=step_id) if "env" in raw else {}
    shard_args = (
        _coerce_str_tuple(raw["shard_args"], field_name="shard_args", step_id=step_id)
        if "shard_args" in raw
        else ()
    )
    depends_on = (
        _coerce_str_tuple(raw["depends_on"], field_name="depends_on", step_id=step_id)
        if "depends_on" in raw
        else ()
    )
    tags = _coerce_str_tuple(raw["tags"], field_name="tags", step_id=step_id) if "tags" in raw else ()
    stage = raw.get("stage")
    if stage is not None and (not isinstance(stage, str) or not stage):
        raise GateConfigError(
            f"step {step_id!r} `stage` must be a non-empty string; "
            'fix: write `stage = "lint"`; next: re-run tc-fitness run'
        )

    return StepSpec(
        id=step_id,
        summary=str(raw.get("summary", "")),
        run=run,
        shell=shell,
        catalogue=catalogue,
        cwd=str(raw.get("cwd", ".")),
        env=env,
        allow_missing=bool(raw.get("allow_missing", False)),
        continue_on_error=bool(raw.get("continue_on_error", False)),
        fix=str(raw.get("fix", "")),
        next=str(raw.get("next", "")),
        checks_dir=(str(raw["checks_dir"]) if "checks_dir" in raw else None),
        dispatch=dispatch,
        parallel=bool(raw.get("parallel", False)),
        skip_when_staged=bool(raw.get("skip_when_staged", False)),
        shard_args=shard_args,
        stage=stage,
        depends_on=depends_on,
        tags=tags,
    )


def parse_config(table: dict[str, Any], *, source: Path) -> GateConfig:
    """Validate a raw config table into a :class:`GateConfig`.

    Separated from the file read so tests can drive it from an in-memory dict.
    """
    steps_raw = table.get("steps")
    if not isinstance(steps_raw, list) or not steps_raw:
        raise GateConfigError(
            f"gate config in {source.name} has no `steps`; "
            "fix: add at least one [[tool.tc_fitness.steps]] table; "
            "next: re-run tc-fitness run"
        )
    steps = tuple(_parse_step(raw, index=i, source=source) for i, raw in enumerate(steps_raw))
    ids = [s.id for s in steps]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        raise GateConfigError(
            f"duplicate step id(s) {dupes} in {source.name}; "
            "fix: give every step a unique `id`; next: re-run tc-fitness run"
        )
    plan_stages(steps, strict=True)  # validate stage references + reject dependency cycles at load time
    return GateConfig(
        steps=steps,
        name=str(table.get("name", "tc-fitness gate")),
        fail_fast=bool(table.get("fail_fast", False)),
        max_workers=int(table.get("max_workers", 8)),
        source=source,
    )


def load_config(repo_root: Path) -> GateConfig:
    """Resolve + parse the gate config under ``repo_root``.

    Raises :class:`GateConfigError` (agent-actionable) when no config file exists
    or the declaration is malformed.
    """
    source = find_config_file(repo_root)
    if source is None:
        raise GateConfigError(
            f"no gate config found under {repo_root} "
            f"(looked for {_DEDICATED_FILE} and a [tool.tc_fitness] block in {_PYPROJECT}); "
            f"fix: add a [tool.tc_fitness] block declaring the gate's steps; "
            "next: see tc_fitness.gate_config for the schema, then re-run tc-fitness run"
        )
    table = _raw_table(source)
    return parse_config(table, source=source)


def parse_core_check_configs(table: Mapping[str, Any], *, source: Path) -> dict[str, Mapping[str, Any]]:
    """Extract the ``[tool.tc_fitness.core_checks.<module>]`` blocks from ``table``.

    ``table`` is the resolved tc_fitness config table (the ``[tool.tc_fitness]``
    sub-table for a ``pyproject.toml``, or the whole document for a
    ``.tc-fitness.toml``). Returns a mapping ``module_name -> config_block`` for
    every CORE check the consumer has supplied a config block for. A missing
    ``core_checks`` table yields an empty mapping (no consumer has bound a CORE
    check, or every bound check relies on the rule's class-attribute defaults).

    Separated from the file read (mirrors :func:`parse_config`) so a test can
    drive it from an in-memory dict.
    """
    raw = table.get(_CORE_CHECKS_KEY)
    if raw is None:
        return {}
    if not isinstance(raw, dict):
        raise GateConfigError(
            f"[tool.tc_fitness.{_CORE_CHECKS_KEY}] in {source.name} must be a table of "
            "per-module config blocks; "
            f"fix: write `[tool.tc_fitness.{_CORE_CHECKS_KEY}.<module>]` sub-tables; "
            "next: re-run tc-fitness run"
        )
    out: dict[str, Mapping[str, Any]] = {}
    for module_name, block in raw.items():
        if not isinstance(block, dict):
            raise GateConfigError(
                f"[tool.tc_fitness.{_CORE_CHECKS_KEY}.{module_name}] in {source.name} must be a "
                "table; "
                f"fix: write `[tool.tc_fitness.{_CORE_CHECKS_KEY}.{module_name}]` with the check's "
                "roots / extensions / thresholds; "
                "next: re-run tc-fitness run"
            )
        out[str(module_name)] = block
    return out


def load_core_check_configs(repo_root: Path) -> dict[str, Mapping[str, Any]]:
    """Resolve the ``[tool.tc_fitness.core_checks.<module>]`` config blocks.

    Reads the SAME config source the gate uses (``.tc-fitness.toml`` wins over
    ``pyproject.toml``'s ``[tool.tc_fitness]``), so a consumer's CORE-check config
    lives beside its gate declaration. Returns ``{}`` when no config file exists
    (a repo with no gate config binds no CORE check), so a caller can always
    treat the result as a plain mapping.
    """
    source = find_config_file(repo_root)
    if source is None:
        return {}
    table = _raw_table(source)
    return parse_core_check_configs(table, source=source)


__all__ = [
    "GateConfig",
    "GateConfigError",
    "Stage",
    "StepSpec",
    "find_config_file",
    "load_config",
    "load_core_check_configs",
    "parse_config",
    "parse_core_check_configs",
    "plan_stages",
]
