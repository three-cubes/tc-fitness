# Fitness gate engine — `assurance/fitness/`

The `three-cubes-fitness` package: the gate orchestrator (`tc-fitness run`), the CORE checks every repository runs, and the coverage and ratchet machinery. It is generic across repositories and is exported one way to the public `three-cubes/tc-fitness` repository (ADR-0001 D6). Checks specific to agent-platform belong in `assurance/checks/`, not here.

## Working here

- Add or improve a CORE check through [`CONTRIBUTING.md`](CONTRIBUTING.md): the check under `src/tc_fitness/core_checks/`, its contract test under `tests/`, and a `CHANGELOG.md` entry.
- Keep the package importable with the standard library alone; parse requirements lazily, as `pyproject.toml` documents.
- Reference only public paths and the standard library. The export to `three-cubes/tc-fitness` carries this directory alone.
- Run the engine's tests with the repository gate from the root (see the root `AGENTS.md`); the gate tags them for each tier.

## Code Review Rules

- Confirm a CORE check change keeps its output contract (`PASS`/`FAIL` lines with `fix:` / `next:` / `run:`), and that its contract test pins any change to it.
- Confirm a change to `tc-fitness run` configuration semantics is backward compatible for consumer `[tool.tc_fitness]` blocks, or carries a migration note in `CHANGELOG.md`.
