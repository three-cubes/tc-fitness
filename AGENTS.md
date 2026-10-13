# Fitness gate engine — `assurance/fitness/`

The `three-cubes-fitness` package: the gate orchestrator (`tc-fitness run`), the CORE checks every repository runs, and the coverage and ratchet machinery. It is generic across repositories and is exported one way to the public `three-cubes/tc-fitness` repository (ADR-0001 D6). Checks specific to agent-platform belong in `assurance/checks/`, not here.

## Read-only mirror — changes land in agent-platform (ADR-0001 D6)

The source of this code is `assurance/fitness/` in `three-cubes/agent-platform`. The `three-cubes/tc-fitness` repository is its one-way, read-only mirror. Make every change in agent-platform, under `assurance/fitness/`, with its tests; it reaches `three-cubes/tc-fitness` only through the export, which opens a pull request from the export identity. A pull request to `three-cubes/tc-fitness` from anyone else is closed and redone in agent-platform. The org ruleset `org-export-mirrors` admits only the export identity and the maintainers to create branches there. If the mirror holds a change agent-platform lacks, port it into `assurance/fitness/` with its tests first.

## Working here

- Add or improve a CORE check through [`CONTRIBUTING.md`](CONTRIBUTING.md): the check under `src/tc_fitness/core_checks/`, its contract test under `tests/`, and a `CHANGELOG.md` entry.
- Keep the package importable with the standard library alone; parse requirements lazily, as `pyproject.toml` documents.
- Reference only public paths and the standard library. The export to `three-cubes/tc-fitness` carries this directory alone.
- Run the engine's tests with the repository gate from the root (see the root `AGENTS.md`); the gate tags them for each tier.

## Code Review Rules

- Confirm a CORE check change keeps its output contract (`PASS`/`FAIL` lines with `fix:` / `next:` / `run:`), and that its contract test pins any change to it.
- Confirm a change to `tc-fitness run` configuration semantics is backward compatible for consumer `[tool.tc_fitness]` blocks, or carries a migration note in `CHANGELOG.md`.
