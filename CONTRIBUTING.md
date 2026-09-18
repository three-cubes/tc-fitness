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

## Commit metadata

Set Git author and committer metadata to the canonical `three-cubes-agent[bot]`
identity (`295831460+three-cubes-agent[bot]@users.noreply.github.com`). This is
local commit metadata: set it through repo-local Git configuration or the
commit process. It needs no GitHub token and does not authenticate a network
write. Keep authorship clean of AI/LLM self-attribution — no
`Co-Authored-By: <model>` trailer, no "Generated with <tool>" credit, no robot
emoji. The `no_llm_attribution` and `canonical_commit_identity` CORE checks
enforce this metadata contract.

## Run the gate before every push

Run `uv run tc-fitness run` and get it green. Local matches CI by construction —
both run this same catalogue. Run the repo's own pytest where the gate does not:

```bash
uv sync --locked --all-extras --all-groups
uv run tc-fitness run
uv run pytest tests/ -q
```

## Open the PR and merge

Use the approved host credential broker for each push, PR, or GitHub API write.
It must live outside the writable checkout, obtain a short-lived
repository-scoped credential for one operation, and pass it only to a validated
child process without printing or persisting it. The broker pattern belongs to
tc-pipelines; broker deployment and credential storage belong to the consuming
environment. tc-fitness does not own either. See the canonical
[Agent SDLC access + HITL standard](https://github.com/three-cubes/tc-pipelines/blob/main/governance/agent-sdlc-access-and-hitl.md).

Open the PR as the `three-cubes-agent` App, never a human account — a PR author
cannot approve their own PR, so App-authorship lets a human maintainer review.
CI runs the fan-in Quality gate plus SonarCloud; the required contexts gate the
merge.

Because tc-fitness is the gate engine, [`.github/CODEOWNERS`](.github/CODEOWNERS)
owns the control-plane paths — the engine source (`src/tc_fitness/`), its config
and pins (`pyproject.toml`, `uv.lock`, `.python-version`, `.uv-version`), CI
(`.github/`), and the licence. A PR touching any owned path **holds for a
maintainer review and does not auto-merge**; a docs-, test-, or CHANGELOG-only
PR auto-merges on green like any product repo. Merges are a merge commit (squash and rebase are disabled
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

## Release the reviewed feature PR

tc-fitness is a pinned library. Its release output is an immutable tag and
GitHub Release at the reviewed merge commit.

1. Add the release notes under `Unreleased` in [CHANGELOG.md](CHANGELOG.md).
2. Dispatch `Prepare release` on the feature branch with one exact `vX.Y.Z`
   value or one semantic bump. The pinned tc-pipelines action updates the
   project version, `uv.lock`, dated CHANGELOG section and
   `.release-prepared.json`, then commits those generated outputs to the same
   branch as `three-cubes-agent[bot]`.
3. Sync from the updated lockfile and run the local gate and pytest commands
   above. Record the tested commit and terminal results in the PR.
4. Merge the reviewed feature PR with a merge commit. The receipt-filtered
   `release-on-merge.yml` caller validates the preparation receipt at the exact
   merge SHA, then creates or confirms the annotated tag and GitHub Release.
5. Consumers repin `three-cubes-fitness` on their own schedule and run their
   full gate against the new engine.

Preparation failure stays on the feature branch for correction. Release
failure records the merge SHA and receipt validation error. Rerun the failed job
only when its immutable workflow revision is still correct and the failure was
transient. A correction to tc-pipelines or this repository's pinned caller
cannot change an old run: open a new tc-fitness PR that pins the corrected
tc-pipelines release commit, prepare the next version on that branch, run the
gate, and merge it. That reviewed merge creates the replacement release
coordinate while preserving the failed merge and any existing tag as evidence.
An existing tag at another SHA remains a hard conflict.

Keep releases additive: preserve existing public signatures and make new
surface opt-in with a safe default. The canonical procedure and evidence
contract live in
[tc-pipelines `governance/standards/sdlc-release-workflow.md`](https://github.com/three-cubes/tc-pipelines/blob/main/governance/standards/sdlc-release-workflow.md)
and
[`ci-release-deployment-architecture.md`](https://github.com/three-cubes/tc-pipelines/blob/main/governance/standards/ci-release-deployment-architecture.md).

## Converge up — one home each

Gates live only in tc-fitness; pipelines live only in tc-pipelines. Improve a gate
here and a pipeline there — never fork a parallel gate or pipeline into a consumer
repo. To change the pipeline, edit the tc-pipelines reusable
(`python-quality-gate.yml`) or its composite action, SHA-pin any third-party
`uses:` (Sonar S7637), publish its release tag, and move consumers to that
tag's full commit SHA with the tag retained as a comment. The canonical
engineering-standards index is
[tc-pipelines `governance/STANDARDS.md`](https://github.com/three-cubes/tc-pipelines/blob/main/governance/STANDARDS.md).
