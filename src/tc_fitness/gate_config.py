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

Fragments: gate configuration owned by the part of the repo it governs
-----------------------------------------------------------------------
``include`` names TOML fragments by repo-root-relative glob pattern (pathlib
glob semantics; ``**`` recurses, so prefer narrow patterns that never walk a
vendored or mirrored tree)::

    [tool.tc_fitness]
    include = ["capabilities/fitness.toml", "*/fitness.toml"]

A fragment holds only ``[[steps]]`` (the step schema above) and
``[core_checks.<module>]`` tables; ``include`` and the gate settings ``name`` /
``fail_fast`` / ``max_workers`` stay in the root config, and any other key is
rejected. Every path inside a fragment step (``run``, ``cwd``, ``paths``,
``checks_dir``) is repo-root-relative, exactly as in the root config; nothing is
resolved against the fragment's own directory.

:func:`load_config` and :func:`load_core_check_configs` return the resolved
configuration, so every consumer sees fragments transparently:

- steps: the root steps first, then each fragment's steps, fragments in sorted
  repo-relative path order. A step id declared twice anywhere is an error that
  names both files. Each :class:`StepSpec` records the file that declared it.
- ``core_checks.<module>``: a list value is the union of every declaration in
  the same order (root first, then fragments), later duplicates dropped; a
  non-list value declared in more than one place must be equal everywhere.
- a pattern that matches nothing is allowed (a part of the repo adopts
  fragments when it has steps to own); an absolute pattern, one containing
  ``..``, or a match that resolves outside the repo is an error.
"""

from __future__ import annotations

import heapq
import tomllib  # stdlib since 3.11, so always present under requires-python
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any


class GateConfigError(ValueError):
    """A malformed or missing ``[tool.tc_fitness]`` gate declaration.

    Carries an agent-actionable message (``<what>; fix: <fix>; next: <next>``)
    so a misconfiguration reads the same as any other gate failure."""


#: The two well-known config locations, in resolution order.
_DEDICATED_FILE = ".tc-fitness.toml"
_PYPROJECT = "pyproject.toml"

_DISPATCH_MODES = ("inprocess", "subprocess")

#: The root-only key naming fragment glob patterns, and the keys a fragment may hold.
_INCLUDE_KEY = "include"
_STEPS_KEY = "steps"
#: Gate-wide settings that only the root config may declare.
_ROOT_ONLY_SETTINGS = ("name", "fail_fast", "max_workers", _INCLUDE_KEY)

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
    #: The paths this step evaluates, as ``fnmatch`` patterns over repo-relative
    #: paths (``*`` crosses ``/``, so ``memory/*`` covers the whole subtree). When
    #: ``tc-fitness run --affected-from LIST`` supplies the change set, a step whose
    #: patterns match none of those files is skipped with its reason; without a
    #: change set (main, the nightly tier) every step runs. Empty (the default)
    #: means the step always runs.
    paths: tuple[str, ...] = ()
    #: The repo-root-relative file that declared this step: the root config
    #: (``pyproject.toml`` / ``.tc-fitness.toml``) or an included fragment. Set by
    #: :func:`load_config`; ``None`` when a step is built in memory.
    source: Path | None = None

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
    #: The repo-root-relative fragments ``include`` resolved to, in merge order.
    fragments: tuple[Path, ...] = ()
    #: The root ``include`` patterns, with `/` separators. A fragment deleted by
    #: the change under test is matched by them, though it no longer resolves.
    include: tuple[str, ...] = ()


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
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
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


def _parse_step(raw: Any, *, index: int, source: Path, declared_in: Path | None = None) -> StepSpec:
    # Name the file the step is written in: a fragment's, when it came from one.
    where = declared_in.as_posix() if declared_in is not None else source.name
    if not isinstance(raw, dict):
        raise GateConfigError(
            f"step #{index} in {where} is not a table; "
            "fix: declare each step as a [[tool.tc_fitness.steps]] table; "
            "next: re-run tc-fitness run"
        )
    step_id = raw.get("id")
    if not isinstance(step_id, str) or not step_id:
        raise GateConfigError(
            f"step #{index} in {where} is missing a string `id`; "
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

    if "baseline_free" in raw:
        raise GateConfigError(
            f"step {step_id!r} declares removed option `baseline_free`; "
            "fitness findings are always hard failures"
        )

    env = _coerce_env(raw["env"], step_id=step_id) if "env" in raw else {}
    shard_args = (
        _coerce_str_tuple(raw["shard_args"], field_name="shard_args", step_id=step_id)
        if "shard_args" in raw
        else ()
    )
    if shard_args and run is None:
        # Only a `run` step is split: gate.py applies the shard arguments inside
        # its `kind == "run"` branch, so a `shell` or `catalogue` step accepts
        # the key and ignores it. Left accepted, a repo can declare `shard_args`,
        # have its pipeline fan the step across N runners, pay N times the
        # compute, gain nothing because every runner did the whole job, and
        # still see the gate report green.
        kind = "catalogue" if catalogue is not None else "shell"
        raise GateConfigError(
            f"step {step_id!r} declares `shard_args` on a {kind} step, which the "
            "engine cannot split: every shard would run the ENTIRE step, costing "
            "N times the compute for no speedup while still passing. "
            "fix: remove `shard_args`, or express the step as `run = [...]` so "
            "the shard arguments reach the command; "
            "next: re-run tc-fitness run"
        )
    depends_on = (
        _coerce_str_tuple(raw["depends_on"], field_name="depends_on", step_id=step_id)
        if "depends_on" in raw
        else ()
    )
    tags = _coerce_str_tuple(raw["tags"], field_name="tags", step_id=step_id) if "tags" in raw else ()
    raw_paths = _coerce_str_tuple(raw["paths"], field_name="paths", step_id=step_id) if "paths" in raw else ()
    # Affected files are Git's repo-relative, `/`-separated paths, so a pattern
    # written with Windows separators is matched in the same form.
    paths = tuple(pattern.replace("\\", "/") for pattern in raw_paths)
    for raw_pattern, pattern in zip(raw_paths, paths, strict=True):
        # A pattern no repo-relative path can match would skip the step on every
        # --affected-from run while the gate still passes.
        posix = PurePosixPath(pattern)
        if not pattern or posix.is_absolute() or PureWindowsPath(raw_pattern).anchor or ".." in posix.parts:
            raise GateConfigError(
                f"step {step_id!r} `paths` entry {raw_pattern!r} is not a repo-relative glob, so no "
                "affected file can match it and the step would always be skipped; "
                'fix: write it relative to the repository root, e.g. `paths = ["src/**"]`; '
                "next: re-run tc-fitness run"
            )
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
        paths=paths,
        source=declared_in,
    )


def parse_config(
    table: dict[str, Any],
    *,
    source: Path,
    step_sources: Sequence[Path] | None = None,
    fragments: Sequence[Path] = (),
    include: Sequence[str] = (),
) -> GateConfig:
    """Validate a raw config table into a :class:`GateConfig`.

    Separated from the file read so tests can drive it from an in-memory dict.
    ``include`` is resolved only by :func:`load_config`, which reads the
    fragments from disk and passes the merged table here with ``step_sources``
    (one repo-relative declaring file per step) and the resolved ``fragments``.
    """
    if _INCLUDE_KEY in table:
        raise GateConfigError(
            f"gate config from {source.name} still carries `include`, which only "
            "load_config resolves; "
            "fix: load the config with load_config(repo_root) so the fragments are read and merged; "
            "next: re-run tc-fitness run"
        )
    steps_raw = table.get(_STEPS_KEY)
    if not isinstance(steps_raw, list) or not steps_raw:
        raise GateConfigError(
            f"gate config in {source.name} has no `steps`; "
            "fix: add at least one [[tool.tc_fitness.steps]] table; "
            "next: re-run tc-fitness run"
        )
    declared = list(step_sources) if step_sources is not None else [None] * len(steps_raw)
    steps = tuple(
        _parse_step(raw, index=i, source=source, declared_in=declared[i]) for i, raw in enumerate(steps_raw)
    )
    ids = [s.id for s in steps]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        where = ""
        if step_sources is not None:
            where = "; ".join(
                f"{d!r} in " + " and ".join(str(s.source) for s in steps if s.id == d) for d in dupes
            )
            where = f" ({where})"
        raise GateConfigError(
            f"duplicate step id(s) {dupes} in {source.name}{where}; "
            "fix: give every step a unique `id`, or keep one declaration and delete the other; "
            "next: re-run tc-fitness run"
        )
    plan_stages(steps, strict=True)  # validate stage references + reject dependency cycles at load time
    return GateConfig(
        steps=steps,
        name=str(table.get("name", "tc-fitness gate")),
        fail_fast=bool(table.get("fail_fast", False)),
        max_workers=int(table.get("max_workers", 8)),
        source=source,
        fragments=tuple(fragments),
        include=tuple(include),
    )


@dataclass(frozen=True)
class _Resolved:
    """The root config table with every included fragment merged in."""

    table: dict[str, Any]
    step_sources: tuple[Path, ...]
    fragments: tuple[Path, ...]
    include: tuple[str, ...] = ()


def _fragment_paths(patterns: Any, *, repo_root: Path, source: Path) -> tuple[Path, ...]:
    """Expand the root ``include`` patterns into sorted, de-duplicated fragment files."""
    if not isinstance(patterns, list) or not all(isinstance(p, str) for p in patterns):
        raise GateConfigError(
            f"`include` in {source.name} must be a list of glob patterns; "
            'fix: write `include = ["capabilities/fitness.toml"]`; '
            "next: re-run tc-fitness run"
        )
    root = repo_root.resolve()
    found: set[Path] = set()
    for pattern in patterns:
        if not pattern or PurePosixPath(pattern).is_absolute() or PureWindowsPath(pattern).anchor:
            raise GateConfigError(
                f"`include` pattern {pattern!r} in {source.name} is not repo-root-relative; "
                'fix: write the pattern relative to the repository root, e.g. "capabilities/fitness.toml"; '
                "next: re-run tc-fitness run"
            )
        if ".." in PurePosixPath(pattern.replace("\\", "/")).parts:
            raise GateConfigError(
                f"`include` pattern {pattern!r} in {source.name} escapes the repository with `..`; "
                "fix: name fragments inside the repository only; "
                "next: re-run tc-fitness run"
            )
        for match in root.glob(pattern):
            if not match.is_file():
                continue
            if not match.resolve().is_relative_to(root):
                raise GateConfigError(
                    f"`include` pattern {pattern!r} in {source.name} matched {match}, which resolves "
                    "outside the repository; "
                    "fix: replace the link with the fragment itself, inside the repository; "
                    "next: re-run tc-fitness run"
                )
            found.add(match.relative_to(root))
    return tuple(sorted(found, key=lambda p: p.as_posix()))


def _read_fragment(path: Path, rel: Path) -> dict[str, Any]:
    """Parse one fragment and reject keys a fragment may not declare."""
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
        raise GateConfigError(
            f"could not parse gate fragment {rel}: {exc}; "
            f"fix: correct the TOML syntax in {rel}; "
            "next: re-run tc-fitness run"
        ) from exc
    for key in data:
        if key in _ROOT_ONLY_SETTINGS:
            raise GateConfigError(
                f"gate fragment {rel} declares `{key}`, which only the root config may set; "
                f"fix: move `{key}` to the root [tool.tc_fitness] table, or delete it from {rel}; "
                "next: re-run tc-fitness run"
            )
        if key not in (_STEPS_KEY, _CORE_CHECKS_KEY):
            raise GateConfigError(
                f"gate fragment {rel} declares unknown key `{key}`; a fragment holds only "
                "[[steps]] and [core_checks.<module>] tables, written without a [tool.tc_fitness] prefix; "
                f"fix: rename or remove `{key}` in {rel}; "
                "next: re-run tc-fitness run"
            )
    steps = data.get(_STEPS_KEY, [])
    if not isinstance(steps, list):
        raise GateConfigError(
            f"`steps` in gate fragment {rel} must be an array of tables; "
            "fix: declare each step as a [[steps]] table; "
            "next: re-run tc-fitness run"
        )
    return data


def _is_ordered_list(key: str) -> bool:
    """A list read as a command line, whose order and duplicates are its meaning.

    Unioning two of them would build a third command neither file declared, so
    files that both declare one must agree, like a scalar.
    """
    return key.endswith(("command", "args", "argv"))


#: Lists of tables whose entries name one thing, keyed by these fields. Two
#: files may declare the same entry only identically: a check reads the first
#: matching entry, so a second, different one would be silently ignored.
_TABLE_IDENTITY: dict[str, tuple[str, ...]] = {"ratchets": ("path", "rule")}


def _check_table_entries(module_name: str, key: str, items: Any, where: str) -> None:
    """Reject a list of tables whose entries are not tables, or whose identity fields are not strings."""
    fields = _TABLE_IDENTITY[key]
    if not isinstance(items, list) or not all(isinstance(item, Mapping) for item in items):
        raise GateConfigError(
            f"core_checks.{module_name}.{key} must be an array of tables ({where}); "
            f"fix: declare each entry as a [[core_checks.{module_name}.{key}]] table; next: re-run tc-fitness run"
        )
    held: dict[tuple[Any, ...], Mapping[str, Any]] = {}
    for item in items:
        if not all(isinstance(item.get(f), str) for f in fields):
            raise GateConfigError(
                f"core_checks.{module_name}.{key} entry {dict(item)!r} ({where}) must name "
                + " and ".join(f"`{f}`" for f in fields)
                + " as strings; fix: write each as a quoted string; next: re-run tc-fitness run"
            )
        # A check reads the first entry for an identity, so a second, different
        # one in the same declaration would be silently ignored.
        identity = tuple(item.get(f) for f in fields)
        if identity in held and held[identity] != item:
            raise GateConfigError(
                f"core_checks.{module_name}.{key} declares {dict(zip(fields, identity, strict=True))} twice "
                f"with different values ({dict(held[identity])!r} and {dict(item)!r}, {where}); "
                "fix: keep one entry for it; next: re-run tc-fitness run"
            )
        held.setdefault(identity, item)


def _union_tables(module_name: str, key: str, current: list[Any], value: list[Any], where: str) -> None:
    """Append ``value``'s new entries to ``current``; a second, different entry for one identity is rejected."""
    _check_table_entries(module_name, key, [*current, *value], where)
    current.extend(item for item in value if item not in current)


def _merge_core_checks(
    merged: dict[str, dict[str, Any]],
    origin: dict[tuple[str, str], Path],
    blocks: Mapping[str, Mapping[str, Any]],
    rel: Path,
) -> None:
    """Merge one file's ``core_checks`` blocks into ``merged`` (set-like lists union; command lists and scalars agree)."""
    for module_name, block in blocks.items():
        target = merged.setdefault(module_name, {})
        for key, value in block.items():
            if key not in target:
                target[key] = list(value) if isinstance(value, list) else value
                origin[(module_name, key)] = rel
                continue
            current = target[key]
            if isinstance(current, list) and isinstance(value, list) and key in _TABLE_IDENTITY:
                _union_tables(module_name, key, current, value, f"in {origin[(module_name, key)]} and {rel}")
                continue
            if isinstance(current, list) and isinstance(value, list) and not _is_ordered_list(key):
                current.extend(item for item in value if item not in current)
                continue
            if current != value:
                raise GateConfigError(
                    f"core_checks.{module_name}.{key} is {current!r} in {origin[(module_name, key)]} "
                    f"but {value!r} in {rel}; "
                    "fix: declare the value in one file only, or make both declarations equal; "
                    "next: re-run tc-fitness run"
                )


def _resolve(source: Path, repo_root: Path) -> _Resolved:
    """Read the root config and merge every fragment its ``include`` names."""
    root_table = _raw_table(source)
    root_rel = Path(source.name)
    if _INCLUDE_KEY not in root_table:
        steps_raw = root_table.get(_STEPS_KEY)
        count = len(steps_raw) if isinstance(steps_raw, list) else 0
        return _Resolved(table=root_table, step_sources=(root_rel,) * count, fragments=())

    fragments = _fragment_paths(root_table[_INCLUDE_KEY], repo_root=repo_root, source=source)
    table = {k: v for k, v in root_table.items() if k != _INCLUDE_KEY}
    root_steps = root_table.get(_STEPS_KEY, [])
    if not isinstance(root_steps, list):
        raise GateConfigError(
            f"`steps` in {source.name} must be an array of tables; "
            "fix: declare each step as a [[tool.tc_fitness.steps]] table; "
            "next: re-run tc-fitness run"
        )
    steps: list[Any] = list(root_steps)
    step_sources: list[Path] = [root_rel] * len(steps)
    merged: dict[str, dict[str, Any]] = {}
    origin: dict[tuple[str, str], Path] = {}
    _merge_core_checks(merged, origin, parse_core_check_configs(root_table, source=source), root_rel)
    for rel in fragments:
        data = _read_fragment(repo_root / rel, rel)
        fragment_steps = data.get(_STEPS_KEY, [])
        steps.extend(fragment_steps)
        step_sources.extend([rel] * len(fragment_steps))
        _merge_core_checks(merged, origin, parse_core_check_configs(data, source=repo_root / rel), rel)
    table[_STEPS_KEY] = steps
    if merged:
        table[_CORE_CHECKS_KEY] = merged
    include = tuple(pattern.replace("\\", "/") for pattern in root_table[_INCLUDE_KEY])
    return _Resolved(table=table, step_sources=tuple(step_sources), fragments=fragments, include=include)


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
    resolved = _resolve(source, repo_root)
    return parse_config(
        resolved.table,
        source=source,
        step_sources=resolved.step_sources,
        fragments=resolved.fragments,
        include=resolved.include,
    )


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
    ``pyproject.toml``'s ``[tool.tc_fitness]``), merged with every fragment its
    ``include`` names, so a consumer's CORE-check config lives beside its gate
    declaration or in the part of the repo it scopes. Returns ``{}`` when no
    config file exists (a repo with no gate config binds no CORE check), so a
    caller can always treat the result as a plain mapping.
    """
    source = find_config_file(repo_root)
    if source is None:
        return {}
    configs = parse_core_check_configs(_resolve(source, repo_root).table, source=source)
    # A list of tables declared in one file only is never merged, so it is
    # validated here too: every declaration, merged or not, reaches a check valid.
    for module_name, block in configs.items():
        for key in _TABLE_IDENTITY.keys() & block.keys():
            _check_table_entries(module_name, key, block[key], f"in {source.name} or its fragments")
    return configs


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
