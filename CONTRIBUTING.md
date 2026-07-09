# Contributing to tc-fitness

tc-fitness is the gate engine of the Three Cubes Golden Path — the CORE checks
every consumer repo inherits instead of hand-copying. Because this repo IS the
control plane, its contribution rules are stricter than a product repo's. The
shared branch / commit / PR / merge procedure is canon in
[tc-pipelines `governance/standards/development-workflow.md`](https://github.com/three-cubes/tc-pipelines/blob/main/governance/standards/development-workflow.md);
this file adds only the tc-fitness specifics.

## Branch

Branch off `main` named `<user>/<team>-<number>-<slug>` (the Linear
`gitBranchName` shape). The engine's own `branch_naming` gate enforces it, so a
non-conforming name fails the gate.

## Commit identity

Author and commit as the canonical `three-cubes-agent` GitHub App
(`295831460+three-cubes-agent[bot]@users.noreply.github.com`). Keep authorship
clean of AI/LLM self-attribution — no `Co-Authored-By: <model>` trailer, no
"Generated with <tool>" credit, no robot emoji. The `no_llm_attribution` and
`canonical_commit_identity` CORE checks enforce this.

## Run the gate before every push

Run `uv run tc-fitness run` and get it green. Local matches CI by construction —
both run this same catalogue. Run the repo's own pytest where the gate does not:

```bash
uv sync --all-extras --all-groups
uv run tc-fitness run
uv run pytest tests/ -q
```

## Open the PR and merge

Open the PR from the `three-cubes-agent` App (short-lived installation token via
WIF / Key Vault `kv-tc-agents`), never a human account — a PR author cannot
approve their own PR, so bot-authorship is what lets a human maintainer review.
CI runs the fan-in Quality gate plus SonarCloud; the required contexts gate the
merge.

Because tc-fitness is the gate engine, [`.github/CODEOWNERS`](.github/CODEOWNERS)
owns the control-plane paths — the engine source (`src/tc_fitness/`), its config
and pins (`pyproject.toml`, `uv.lock`, `.python-version`), CI (`.github/`), and
the licence. A PR touching any owned path **holds for a maintainer review and
does not auto-merge**; a docs-, test-, or CHANGELOG-only PR auto-merges on green
like any product repo. Merges are a merge commit (squash and rebase are disabled
at the repo level). `gh pr merge --admin`
is an owner-only logged exception an agent requests and never self-authorises; a
ruleset with no bypass actors blocks even an admin.

## Author or improve a CORE check

1. Add the check at `src/tc_fitness/core_checks/<name>.py` as a config-driven
   `FitnessRule` subclass — bake in no repo identity; every knob (`roots`,
   `extensions`, thresholds) arrives from the consumer's config. Register it in
   the `CORE_CHECKS` registry.
2. Pair it with a contract/unit test at `tests/test_core_<name>.py` — the
   convention every `core_checks/` module follows.
3. Bind the consumer surface: a check reads its scope from a
   `[tool.tc_fitness.core_checks.<name>]` block and a catalogue
   `RuleEntry(check="core:<name>")` row. A check with no config block is a vacuous
   pass, so adopting it never breaks a build until the repo opts in.

## Release a tag (this repo's deploy analog)

tc-fitness is a pinned library, not a VM service — its "deploy" is a release tag,
so no VM deploy or runbook applies. Release **additively**: keep every existing
public signature byte-identical and make new surface opt-in with a safe default,
then cut a new immutable tag `vX.Y.Z` and record it in
[CHANGELOG.md](CHANGELOG.md). Consumers repin `three-cubes-fitness` on their own
schedule. The release procedure is canon in
[tc-pipelines `governance/standards/sdlc-release-workflow.md`](https://github.com/three-cubes/tc-pipelines/blob/main/governance/standards/sdlc-release-workflow.md).

## Converge up — one home each

Gates live only in tc-fitness; pipelines live only in tc-pipelines. Improve a gate
here and a pipeline there — never fork a parallel gate or pipeline into a consumer
repo. To change the pipeline, edit the tc-pipelines reusable
(`python-quality-gate.yml`) or its composite action, SHA-pin any third-party
`uses:` (Sonar S7637), tag it, and move consumers to the tag. The canonical
engineering-standards index is
[tc-pipelines `governance/STANDARDS.md`](https://github.com/three-cubes/tc-pipelines/blob/main/governance/STANDARDS.md).
