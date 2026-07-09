"""``tc-fitness run`` — the single runnable gate both CI and local invoke.

This is the load-bearing surface of "local == CI by construction". One binary,
reading one repo-local config (:mod:`tc_fitness.gate_config`), runs the repo's
WHOLE quality gate in order:

* CI's reusable ``python-quality-gate.yml`` shrinks to
  ``checkout → setup-uv → uv run tc-fitness run``.
* A repo's ``make check`` becomes ``uv run tc-fitness run``.

Because both shell out to the SAME command reading the SAME ``[tool.tc_fitness]``
declaration, the gate has exactly one definition. There is no hand-copied pytest
block to drift between ``scripts/ci/check.sh`` and ``ci.yml``.

What it does NOT do
-------------------
The engine orchestrates STEPS; it never owns a repo's specifics. The pytest
scope, the ``--cov`` roots, the ruff/bandit targets, the detect-secrets baseline,
and the consumer's fitness-check catalogue are all CONFIG (each a declared step),
never baked into this module. Adding a step is a config edit in the consumer,
not an engine change — that is the whole point (a reusable workflow that took
these as *inputs* would just relocate the per-repo coupling into YAML).

Step kinds
----------
* ``run`` — a command vector (argv), executed without a shell.
* ``shell`` — a shell command string (for pipelines / globs / ``$(...)``).
* ``catalogue`` — the consumer's ``module:attr`` RuleEntry catalogue, dispatched
  IN-PROCESS through :func:`tc_fitness.runner.main_cli` (no second python boot;
  the runner's own named ledger prints inline).

Output contract (gate-runner discipline)
----------------------------------------
A ``run [id]`` line and a ``PASS`` / ``FAIL`` / ``SKIP`` verdict per step, the
step's own stdout/stderr inline, then a final aggregate verdict. A FAILing step
prints its agent-actionable ``fix:`` / ``next:`` lines. The process exit is
non-zero iff any gating step failed (a ``continue_on_error`` step never gates).
"""

from __future__ import annotations

import argparse
import concurrent.futures
import contextlib
import io
import os
import shutil
import subprocess
import sys
from collections.abc import Sequence
from dataclasses import dataclass, field
from importlib import import_module
from pathlib import Path

from tc_fitness.gate_config import (
    GateConfig,
    GateConfigError,
    Stage,
    StepSpec,
    load_config,
    load_core_check_configs,
    plan_stages,
)
from tc_fitness.runner import Colours, main_cli, paths_from_file

_RED = Colours.RED
_GREEN = Colours.GREEN
_YELLOW = Colours.YELLOW
_RESET = Colours.RESET


@dataclass
class StepResult:
    """The outcome of one step: pass / fail / skip, plus whether it gates."""

    id: str
    status: str  # "pass" | "fail" | "skip"
    gating: bool = True  # a continue_on_error fail is non-gating

    @property
    def is_gating_failure(self) -> bool:
        return self.status == "fail" and self.gating


@dataclass
class GateOutcome:
    """The aggregate result of a ``tc-fitness run``."""

    results: list[StepResult] = field(default_factory=list)

    @property
    def ran(self) -> int:
        return sum(1 for r in self.results if r.status != "skip")

    @property
    def skipped(self) -> int:
        return sum(1 for r in self.results if r.status == "skip")

    @property
    def gating_failures(self) -> list[str]:
        return [r.id for r in self.results if r.is_gating_failure]

    @property
    def ok(self) -> bool:
        return not self.gating_failures

    @property
    def exit_code(self) -> int:
        return 0 if self.ok else 1


def _step_env(step: StepSpec) -> dict[str, str]:
    """The child environment: the inherited env overlaid with the step's env."""
    env = dict(os.environ)
    env.update(step.env)
    return env


def _program_on_path(argv0: str, env: dict[str, str]) -> bool:
    """Whether the step's program resolves on PATH (honouring the step env)."""
    return shutil.which(argv0, path=env.get("PATH")) is not None


def _fix_next_text(step: StepSpec) -> str:
    """The step's agent-actionable remediation lines as text (for buffered replay)."""
    lines = []
    if step.fix:
        lines.append(f"   fix: {step.fix}\n")
    if step.next:
        lines.append(f"   next: {step.next}\n")
    return "".join(lines)


def _print_fix_next(step: StepSpec) -> None:
    """Print the step's agent-actionable remediation under its FAIL, if declared."""
    text = _fix_next_text(step)
    if text:
        sys.stdout.write(text)


def _parse_shard(spec: str) -> tuple[int, int]:
    """Parse an ``i/N`` shard spec into ``(index, total)``; validate ``1 <= i <= N``.

    Raises ``ValueError`` (agent-actionable) on a malformed spec so ``main`` can map
    it to the same exit-2 config-error path ``--changed-files-from`` uses.
    """
    index_s, sep, total_s = spec.partition("/")
    if sep != "/" or not index_s.isdigit() or not total_s.isdigit():
        raise ValueError(
            f"--shard must be `i/N` with positive integers (got {spec!r}); "
            "fix: pass e.g. `--shard 2/4`; next: re-run tc-fitness run"
        )
    index, total = int(index_s), int(total_s)
    if total < 1 or not (1 <= index <= total):
        raise ValueError(
            f"--shard {spec}: need 1 <= i <= N and N >= 1; "
            "fix: pass e.g. `--shard 2/4`; next: re-run tc-fitness run"
        )
    return index, total


def _apply_shard(argv: list[str], env: dict[str, str], step: StepSpec, shard: tuple[int, int]) -> None:
    """Extend a run step's ``argv`` with its substituted ``shard_args`` and scope
    ``COVERAGE_FILE`` to this shard, IN PLACE.

    A no-op when the step declares no ``shard_args`` — so ``--shard`` only affects
    the step(s) that opt in, leaving every other command byte-identical. Uses a
    literal ``str.replace`` (not ``str.format``) so a stray brace in an argument
    cannot raise. ``env`` is the fresh per-step dict from :func:`_step_env`, so the
    ``COVERAGE_FILE`` override does not leak into the parent process.
    """
    if not step.shard_args:
        return
    index, total = shard
    argv.extend(arg.replace("{index}", str(index)).replace("{total}", str(total)) for arg in step.shard_args)
    env["COVERAGE_FILE"] = f".coverage.{index}"


def _run_command_step(step: StepSpec, repo_root: Path, *, shard: tuple[int, int] | None = None) -> StepResult:
    """Execute a ``run`` (argv) or ``shell`` (string) step as a child process.

    Inherits stdout/stderr so the child's output streams live (no capture) — the
    gate is a foreground command, not a log scraper. A missing program is a SKIP
    when ``allow_missing`` else a FAIL with an actionable hint.
    """
    env = _step_env(step)
    cwd = (repo_root / step.cwd).resolve()
    label = step.summary or step.id

    print(f"{_YELLOW}run [{step.id}]{_RESET} {label}")

    if step.kind == "run":
        # `kind == "run"` guarantees `run` is set (the loader enforces exactly
        # one action per step), so the `or ()` is unreachable — present only to
        # satisfy the type checker without an `assert` in shipped code.
        argv = list(step.run or ())
        if shard is not None:
            # No-op unless the step declares shard_args; keeps argv[0] (the
            # program) unchanged for the PATH lookup below.
            _apply_shard(argv, env, step, shard)
        if not _program_on_path(argv[0], env):
            if step.allow_missing:
                print(f"{_YELLOW}SKIP [{step.id}]{_RESET} {argv[0]} not on PATH (allow_missing)")
                return StepResult(step.id, "skip")
            print(f"{_RED}FAIL [{step.id}]{_RESET} {argv[0]} not on PATH")
            print(f"   fix: install {argv[0]} (or set allow_missing = true for this step)")
            _print_fix_next(step)
            return StepResult(step.id, "fail", gating=not step.continue_on_error)
        proc = subprocess.run(argv, cwd=cwd, env=env, check=False)  # noqa: S603 - argv is config, not user input
    else:  # shell
        # `kind == "shell"` guarantees `shell` is set (loader invariant).
        proc = subprocess.run(  # noqa: S602 - shell command is repo-owned config
            step.shell or "", cwd=cwd, env=env, shell=True, check=False
        )

    if proc.returncode == 0:
        print(f"{_GREEN}PASS [{step.id}]{_RESET} {label}")
        return StepResult(step.id, "pass")
    print(f"{_RED}FAIL [{step.id}]{_RESET} {label} (exit {proc.returncode})")
    _print_fix_next(step)
    return StepResult(step.id, "fail", gating=not step.continue_on_error)


def _resolve_catalogue(ref: str) -> tuple[object, ...]:
    """Import ``module.path:attr`` and return the ``tuple[RuleEntry, ...]``."""
    module_path, _, attr = ref.partition(":")
    module = import_module(module_path)
    rules = getattr(module, attr)
    return tuple(rules)


def _run_catalogue_step(
    step: StepSpec,
    repo_root: Path,
    gate_id: str | None,
    *,
    establish_baseline: bool = False,
    staged: bool = False,
    changed_files: list[str] | None = None,
) -> StepResult:
    """Dispatch the consumer's RuleEntry catalogue via the shared runner.

    Runs IN-PROCESS through :func:`tc_fitness.runner.main_cli` so the runner's own
    ``run [id]`` / ``PASS`` / ``FAIL`` ledger prints inline. The step PASSes iff
    ``main_cli`` returns 0. A ``--gate <id>`` from the CLI is threaded through so
    ``tc-fitness run --gate F26`` runs exactly one catalogue rule.

    ``staged`` routes the catalogue through the runner's sound per-rule
    ``--staged`` selection (the ``<60s`` smoke tier) — only the rules a staged
    change could trip run, narrowed to the staged files, with the no-false-
    negative guarantee :mod:`tc_fitness.staged` enforces. ``--gate`` wins over
    ``--staged`` when both are given (an explicit single-rule target is the
    narrower intent).

    Any ``core:<module>`` entry in the catalogue receives its
    ``[tool.tc_fitness.core_checks.<module>]`` config block (read from the SAME
    repo config the gate loaded) so the CORE check scans the consumer's
    configured tree. ``establish_baseline`` runs those entries in adoption mode.
    """
    # `kind == "catalogue"` guarantees `catalogue` is set (loader invariant).
    catalogue_ref = step.catalogue or ""
    label = step.summary or step.id
    print(f"{_YELLOW}run [{step.id}]{_RESET} {label}")

    repo_root_for_step = repo_root
    checks_dir = (repo_root / step.checks_dir).resolve() if step.checks_dir is not None else None

    # Make the catalogue module importable from the repo root (the consumer's
    # catalogue typically lives under scripts/checks/ alongside its checks).
    repo_root_str = str(repo_root)
    added = repo_root_str not in sys.path
    if added:
        sys.path.insert(0, repo_root_str)
    try:
        rules = _resolve_catalogue(catalogue_ref)
    except (ImportError, AttributeError) as exc:
        print(f"{_RED}FAIL [{step.id}]{_RESET} could not load catalogue {catalogue_ref!r}: {exc}")
        print(f'   fix: confirm the `catalogue = "module:attr"` ref resolves from {repo_root}')
        _print_fix_next(step)
        return StepResult(step.id, "fail", gating=not step.continue_on_error)
    finally:
        if added and repo_root_str in sys.path:
            sys.path.remove(repo_root_str)

    if gate_id:
        argv = ["--gate", gate_id]
    elif staged or changed_files is not None:
        argv = ["--staged"]
    else:
        argv = ["--all"]
    if establish_baseline:
        argv.append("--establish-baseline")
    core_check_configs = load_core_check_configs(repo_root)
    rc = main_cli(
        rules,  # type: ignore[arg-type]
        argv,
        repo_root=repo_root_for_step,
        checks_dir=checks_dir,
        dispatch=step.dispatch,
        parallel_subprocess=step.parallel,
        core_check_configs=core_check_configs,
        staged_files=changed_files,
    )
    if rc == 0:
        print(f"{_GREEN}PASS [{step.id}]{_RESET} {label}")
        return StepResult(step.id, "pass")
    print(f"{_RED}FAIL [{step.id}]{_RESET} {label} (exit {rc})")
    _print_fix_next(step)
    return StepResult(step.id, "fail", gating=not step.continue_on_error)


def _run_step(
    step: StepSpec,
    repo_root: Path,
    gate_id: str | None,
    *,
    establish_baseline: bool = False,
    staged: bool = False,
    changed_files: list[str] | None = None,
    shard: tuple[int, int] | None = None,
) -> StepResult:
    if step.kind == "catalogue":
        return _run_catalogue_step(
            step,
            repo_root,
            gate_id,
            establish_baseline=establish_baseline,
            staged=staged,
            changed_files=changed_files,
        )
    return _run_command_step(step, repo_root, shard=shard)


def _print_aggregate(cfg: GateConfig, outcome: GateOutcome) -> None:
    print()
    if outcome.ok:
        print(f"{_GREEN}=== {cfg.name}: PASS ==={_RESET} ({outcome.ran} ran, {outcome.skipped} skipped)")
        return
    failures = outcome.gating_failures
    print(
        f"{_RED}=== {cfg.name}: FAIL ==={_RESET} "
        f"({len(failures)}/{outcome.ran} step(s) failed: {', '.join(failures)})"
    )
    print("   fix: address the FAIL step(s) above — each carries its own fix:/next:")
    print("   next: re-run `tc-fitness run` (or `tc-fitness run --only <id>` to retry one step)")


def run_gate(
    cfg: GateConfig,
    repo_root: Path,
    *,
    only: list[str] | None = None,
    gate_id: str | None = None,
    establish_baseline: bool = False,
    staged: bool = False,
    changed_files: list[str] | None = None,
    shard: tuple[int, int] | None = None,
    tier: str | None = None,
) -> GateOutcome:
    """Run the configured steps in order; return the aggregate outcome.

    ``only`` restricts to the named step ids (in config order); ``gate_id`` is
    threaded into a catalogue step so a single fitness rule can be targeted.
    ``establish_baseline`` runs the catalogue step's ``core:`` entries in
    baseline-adoption mode (freeze today's offenders) instead of gating.

    ``staged`` selects the ``<60s`` smoke tier: catalogue steps run through the
    runner's sound per-rule ``--staged`` selection, and every step a repo has
    flagged ``skip_when_staged`` (its EXPENSIVE full-tree legs) is dropped with a
    transparent SKIP line. ``changed_files`` uses the same selection semantics
    with a caller-supplied PR diff list instead of the git index, which is the CI
    companion to the local staged smoke. The cheap legs (lint / format /
    branch-naming) run verbatim.

    ``fail_fast`` (from the config) stops at the first gating failure.
    """
    fast_mode = staged or changed_files is not None
    if changed_files is not None:
        banner = f"{cfg.name} (changed smoke)"
    elif staged:
        banner = f"{cfg.name} (staged smoke)"
    else:
        banner = cfg.name
    print(f"=== {banner} ===")
    if cfg.source is not None:
        print(f"    (config: {cfg.source})")

    selected = cfg.steps
    if only:
        wanted = set(only)
        selected = tuple(s for s in cfg.steps if s.id in wanted)
        unknown = wanted - {s.id for s in cfg.steps}
        if unknown:
            print(
                f"{_RED}unknown step id(s): {sorted(unknown)}{_RESET}; "
                f"fix: pass an id from {[s.id for s in cfg.steps]}"
            )
    if tier is not None:
        # Tier selector: keep only steps tagged `tier` (silently, like --only).
        selected = tuple(s for s in selected if tier in s.tags)

    runner = _run_scheduled if _has_stages(selected) else _run_sequential
    outcome = runner(
        cfg,
        repo_root,
        selected,
        gate_id=gate_id,
        establish_baseline=establish_baseline,
        staged=staged,
        changed_files=changed_files,
        shard=shard,
        fast_mode=fast_mode,
    )

    _print_aggregate(cfg, outcome)
    return outcome


def _has_stages(steps: Sequence[StepSpec]) -> bool:
    """True iff any step opts into the concern-parallel scheduler. A config with
    no ``stage`` / ``depends_on`` takes the untouched sequential path — the
    back-compat gate."""
    return any(s.stage is not None or s.depends_on for s in steps)


def _run_sequential(
    cfg: GateConfig,
    repo_root: Path,
    selected: Sequence[StepSpec],
    *,
    gate_id: str | None,
    establish_baseline: bool,
    staged: bool,
    changed_files: list[str] | None,
    shard: tuple[int, int] | None,
    fast_mode: bool,
) -> GateOutcome:
    """Today's path (v0.9.0): run ``selected`` sequentially, LIVE, in registration
    order. Physically preserved so a config without stages is byte-identical."""
    outcome = GateOutcome()
    for step in selected:
        if fast_mode and step.skip_when_staged:
            label = step.summary or step.id
            print(f"{_YELLOW}SKIP [{step.id}]{_RESET} {label} (skip_when_staged — not in the <60s smoke)")
            outcome.results.append(StepResult(step.id, "skip"))
            continue
        result = _run_step(
            step,
            repo_root,
            gate_id,
            establish_baseline=establish_baseline,
            staged=staged,
            changed_files=changed_files,
            shard=shard,
        )
        outcome.results.append(result)
        if cfg.fail_fast and result.is_gating_failure:
            print(f"{_YELLOW}fail_fast: stopping at first gating failure ({step.id}){_RESET}")
            break
    return outcome


@dataclass
class _StepOutcome:
    """A stage member's result plus its buffered output, for registration-order replay."""

    result: StepResult
    out: str = ""
    err: str = ""
    printed: bool = False  # True when already emitted live (singleton fast-path)


def _run_scheduled(
    cfg: GateConfig,
    repo_root: Path,
    selected: Sequence[StepSpec],
    *,
    gate_id: str | None,
    establish_baseline: bool,
    staged: bool,
    changed_files: list[str] | None,
    shard: tuple[int, int] | None,
    fast_mode: bool,
) -> GateOutcome:
    """Concern-parallel path: group ``selected`` into stages (dependency order),
    run each stage's members concurrently — subprocess legs on a bounded pool,
    in-process catalogue on the main thread — then replay each stage's output in
    registration order so the ledger stays byte-stable."""
    stages: tuple[Stage, ...] = plan_stages(selected, strict=False)
    outcome = GateOutcome()
    for stage in stages:
        runnable = [s for s in stage.steps if not (fast_mode and s.skip_when_staged)]
        outcomes = _execute_stage(
            runnable,
            repo_root,
            gate_id,
            shard=shard,
            establish_baseline=establish_baseline,
            staged=staged,
            changed_files=changed_files,
            max_workers=cfg.max_workers,
        )
        stage_failed = False
        for s in stage.steps:  # replay in registration order
            if fast_mode and s.skip_when_staged:
                label = s.summary or s.id
                print(f"{_YELLOW}SKIP [{s.id}]{_RESET} {label} (skip_when_staged — not in the <60s smoke)")
                outcome.results.append(StepResult(s.id, "skip"))
                continue
            oc = outcomes[s.id]
            if not oc.printed:
                if oc.out:
                    sys.stdout.write(oc.out)
                if oc.err:
                    sys.stderr.write(oc.err)
            outcome.results.append(oc.result)
            stage_failed = stage_failed or oc.result.is_gating_failure
        if cfg.fail_fast and stage_failed:
            print(f"{_YELLOW}fail_fast: stopping after the failing stage ({stage.name}){_RESET}")
            break
    return outcome


def _execute_stage(
    runnable: Sequence[StepSpec],
    repo_root: Path,
    gate_id: str | None,
    *,
    shard: tuple[int, int] | None,
    establish_baseline: bool,
    staged: bool,
    changed_files: list[str] | None,
    max_workers: int,
) -> dict[str, _StepOutcome]:
    """Run one stage's members concurrently, returning each by id. Subprocess
    (``run`` / ``shell``) steps go on a bounded ThreadPoolExecutor (captured via
    pipes); in-process ``catalogue`` steps run on the MAIN thread (they mutate
    ``sys.stdout`` / ``sys.path`` / the shared AST cache, so a worker thread would
    corrupt them) while overlapping the pool in wall-clock. One-member stages take
    a live fast-path — byte-identical to the sequential run."""
    if len(runnable) <= 1:
        out: dict[str, _StepOutcome] = {}
        for s in runnable:
            res = _run_step(
                s,
                repo_root,
                gate_id,
                establish_baseline=establish_baseline,
                staged=staged,
                changed_files=changed_files,
                shard=shard,
            )
            out[s.id] = _StepOutcome(result=res, printed=True)
        return out

    subprocess_steps = [s for s in runnable if s.kind in ("run", "shell")]
    catalogue_steps = [s for s in runnable if s.kind == "catalogue"]
    outcomes: dict[str, _StepOutcome] = {}
    workers = min(max_workers, max(1, len(subprocess_steps)))
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(_capture_command_step, s, repo_root, shard=shard): s.id for s in subprocess_steps
        }
        # Main thread: capture the in-process catalogue step(s) while the pool
        # drains the subprocess legs — genuine wall-clock overlap.
        for s in catalogue_steps:
            outcomes[s.id] = _capture_catalogue_step(
                s,
                repo_root,
                gate_id,
                establish_baseline=establish_baseline,
                staged=staged,
                changed_files=changed_files,
            )
        for fut in concurrent.futures.as_completed(futures):
            outcomes[futures[fut]] = fut.result()
    return outcomes


def _capture_command_step(step: StepSpec, repo_root: Path, *, shard: tuple[int, int] | None) -> _StepOutcome:
    """Buffered mirror of :func:`_run_command_step` — identical logic, but framing
    goes to a StringIO and the child is captured (``capture_output=True``) so a
    worker thread never writes to the process-global stdout the main thread may be
    redirecting for a concurrent catalogue step."""
    env = _step_env(step)
    cwd = (repo_root / step.cwd).resolve()
    label = step.summary or step.id
    out = io.StringIO()
    out.write(f"{_YELLOW}run [{step.id}]{_RESET} {label}\n")

    if step.kind == "run":
        argv = list(step.run or ())
        if shard is not None:
            _apply_shard(argv, env, step, shard)
        if not _program_on_path(argv[0], env):
            if step.allow_missing:
                out.write(f"{_YELLOW}SKIP [{step.id}]{_RESET} {argv[0]} not on PATH (allow_missing)\n")
                return _StepOutcome(StepResult(step.id, "skip"), out=out.getvalue())
            out.write(f"{_RED}FAIL [{step.id}]{_RESET} {argv[0]} not on PATH\n")
            out.write(f"   fix: install {argv[0]} (or set allow_missing = true for this step)\n")
            out.write(_fix_next_text(step))
            return _StepOutcome(
                StepResult(step.id, "fail", gating=not step.continue_on_error), out=out.getvalue()
            )
        proc = subprocess.run(  # noqa: S603 - argv is config, not user input
            argv, cwd=cwd, env=env, check=False, capture_output=True, text=True
        )
    else:  # shell
        proc = subprocess.run(  # noqa: S602 - shell command is repo-owned config
            step.shell or "", cwd=cwd, env=env, shell=True, check=False, capture_output=True, text=True
        )

    out.write(proc.stdout or "")
    if proc.returncode == 0:
        out.write(f"{_GREEN}PASS [{step.id}]{_RESET} {label}\n")
        return _StepOutcome(StepResult(step.id, "pass"), out=out.getvalue(), err=proc.stderr or "")
    out.write(f"{_RED}FAIL [{step.id}]{_RESET} {label} (exit {proc.returncode})\n")
    out.write(_fix_next_text(step))
    return _StepOutcome(
        StepResult(step.id, "fail", gating=not step.continue_on_error),
        out=out.getvalue(),
        err=proc.stderr or "",
    )


def _capture_catalogue_step(
    step: StepSpec,
    repo_root: Path,
    gate_id: str | None,
    *,
    establish_baseline: bool,
    staged: bool,
    changed_files: list[str] | None,
) -> _StepOutcome:
    """Run the in-process catalogue step under a main-thread stdout/stderr redirect
    so its ledger is buffered for registration-order replay."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        res = _run_catalogue_step(
            step,
            repo_root,
            gate_id,
            establish_baseline=establish_baseline,
            staged=staged,
            changed_files=changed_files,
        )
    return _StepOutcome(res, out=out.getvalue(), err=err.getvalue())


def main(argv: list[str] | None = None) -> int:
    """``tc-fitness`` console entrypoint.

    Subcommands:

    * ``run`` — load ``[tool.tc_fitness]`` and run the declared gate.
      ``--repo-root`` overrides CWD; ``--only ID`` runs a subset of steps;
      ``--gate ID`` targets a single fitness rule inside a catalogue step;
      ``--staged`` runs the ``<60s`` smoke tier (catalogue steps in sound
      per-rule ``--staged`` selection; ``skip_when_staged`` legs dropped);
      ``--changed-files-from PATH`` runs the same smoke tier against a CI
      supplied PR-diff file list.
    """
    parser = argparse.ArgumentParser(
        prog="tc-fitness",
        description="The single runnable quality gate — local == CI by construction.",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    run_p = sub.add_parser("run", help="run the repo's declared [tool.tc_fitness] gate")
    run_p.add_argument(
        "--repo-root",
        default=".",
        help="repo root holding the gate config (default: CWD)",
    )
    run_p.add_argument(
        "--only",
        action="append",
        metavar="ID",
        help="run only the named step id(s) (repeatable)",
    )
    run_p.add_argument(
        "--gate",
        metavar="ID",
        help="target one fitness rule by id inside the catalogue step",
    )
    run_p.add_argument(
        "--staged",
        action="store_true",
        help="the <60s smoke tier: run catalogue steps in sound per-rule --staged "
        "mode and drop steps flagged skip_when_staged (the expensive full-tree legs)",
    )
    run_p.add_argument(
        "--changed-files-from",
        metavar="PATH",
        help="the <60s CI smoke tier: run staged selection against a newline-delimited changed-file list",
    )
    run_p.add_argument(
        "--shard",
        metavar="I/N",
        help="run shard i of N (e.g. --shard 2/4): append each opted-in step's "
        "shard_args (with {index}/{total} substituted) to its command and set "
        "COVERAGE_FILE=.coverage.<i> so a downstream `coverage combine` merges the "
        "shards. Steps without shard_args are untouched.",
    )
    run_p.add_argument(
        "--tier",
        metavar="NAME",
        help="run only steps whose `tags` include NAME (e.g. smoke/full/nightly); "
        "composes with --only, --staged and --changed-files-from",
    )
    run_p.add_argument(
        "--establish-baseline",
        action="store_true",
        help="run the catalogue step's core: entries in baseline-adoption mode "
        "(freeze today's offenders), then exit",
    )
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    try:
        cfg = load_config(repo_root)
    except GateConfigError as exc:
        print(f"{_RED}FAIL tc-fitness run{_RESET} — {exc}", file=sys.stderr)
        return 2
    try:
        changed_files = (
            paths_from_file(Path(args.changed_files_from).resolve()) if args.changed_files_from else None
        )
    except OSError as exc:
        print(
            f"{_RED}FAIL --changed-files-from{_RESET} - cannot read {args.changed_files_from}: {exc}",
            file=sys.stderr,
        )
        return 2
    try:
        shard = _parse_shard(args.shard) if args.shard else None
    except ValueError as exc:
        print(f"{_RED}FAIL --shard{_RESET} - {exc}", file=sys.stderr)
        return 2

    outcome = run_gate(
        cfg,
        repo_root,
        only=args.only,
        gate_id=args.gate,
        establish_baseline=bool(args.establish_baseline),
        staged=bool(args.staged),
        changed_files=changed_files,
        shard=shard,
        tier=args.tier,
    )
    return outcome.exit_code


if __name__ == "__main__":
    sys.exit(main())


__all__ = [
    "GateOutcome",
    "StepResult",
    "main",
    "run_gate",
]
