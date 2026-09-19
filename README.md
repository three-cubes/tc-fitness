# tc-fitness (three-cubes-fitness)

**What this is:** the one quality check you run before your code can merge. You
run `tc-fitness run` and it runs your linters, type-check, tests, coverage,
security scan, and architecture rules, then gives you one pass or fail.

Supported platform evidence covers Linux on Python 3.12 and 3.13, plus macOS
CLI, Git and filesystem qualification on Python 3.12. Windows is unsupported
until it has an equivalent installed-distribution qualification lane.

**The tool knows HOW to run the checks. Your repo says WHAT to check** — you list
the checks in a `[tool.tc_fitness]` block in your `pyproject.toml`, and
tc-fitness runs them in order and gives you a single verdict.

## Why one shared check exists

Across many repos, the quality checks used to be hand-copied into each one. They
slowly drifted apart, so "passing" meant something different in every repo, and a
fix had to be re-applied by hand everywhere.

tc-fitness is the one check every repo uses instead of its own copy:

- You run it on your laptop and get the **same result CI will give**. No
  surprises, no "works on my machine".
- One fix to this check improves every repo at once.
- A new repo gets a proven setup instead of inventing its own.

## How to add it to a repo

1. **Install it.** Select an immutable release tag from
   [CHANGELOG.md](CHANGELOG.md) and pin it in your `pyproject.toml`:

   ```toml
   [project.optional-dependencies]
   dev = [
     "three-cubes-fitness @ git+https://github.com/three-cubes/tc-fitness.git@vX.Y.Z",
   ]
   ```

   Always pin a tag, never `@main` — the version is the contract your checks
   depend on, so a repo only moves when you bump the tag.

2. **List your checks.** Add a `[tool.tc_fitness]` block to your `pyproject.toml`
   (or a dedicated `.tc-fitness.toml`). Each entry is one step — a lint run, a
   test run, a security scan, your architecture rules. See
   [The `[tool.tc_fitness]` config](#the-tooltc_fitness-config) below for the
   full set of fields.

3. **Run it locally.** Install your full dev environment, then run the check the
   same way CI does:

   ```bash
   uv sync --all-extras --all-groups
   uv run tc-fitness run
   ```

   Get it green locally before you push.

4. **Point CI at it.** In your GitHub Actions, the CI job shrinks to: check out
   the code, set up `uv`, then run `uv run tc-fitness run`. The check you run
   locally is the exact same one CI runs. Call the reusable job from
   [tc-pipelines](https://github.com/three-cubes/tc-pipelines)
   (`uses: …/python-quality-gate.yml@<full-commit-sha> # vX.Y.Z`), pin it to the
   release commit, and SHA-pin every third-party `uses:` — improve the pipeline
   in tc-pipelines, never fork it into your repo.

## The daily loop

1. **Branch off `main`** named `<user>/<team>-<number>-<slug>` — the shape the
   engine's own `branch_naming` gate enforces (this repo dogfoods
   `tc_fitness.checks.branch_naming`).
2. **Run the gate before every push:** sync with
   `uv sync --locked --all-extras --all-groups`, run
   `uv run tc-fitness run`, and get it green.
   Local matches CI by construction — both run this same catalogue. Run your
   repo's own pytest separately where the gate does not.
3. **Set canonical commit metadata.** Git author and committer must be an
   allowlisted bot or human identity, with no AI/LLM attribution.
   `no_llm_attribution` and `canonical_commit_identity` inspect commit metadata;
   they do not authenticate a push, PR, or API request.
4. **Authenticate GitHub writes through the approved host broker.** The broker
   lives outside the writable checkout, obtains a short-lived repository-scoped
   credential for one operation, and passes it only to a validated `git` or `gh`
   child process. It must not print or persist the credential. tc-fitness owns
   the identity gate, not credentials or broker installation. The canonical
   pattern and consumer responsibilities live in the
   [Agent SDLC access + HITL standard](https://github.com/three-cubes/tc-pipelines/blob/main/governance/agent-sdlc-access-and-hitl.md).

The full branch / commit / PR / merge procedure is canon in
[tc-pipelines `governance/standards/development-workflow.md`](https://github.com/three-cubes/tc-pipelines/blob/main/governance/standards/development-workflow.md);
this repo's contributor specifics live in [CONTRIBUTING.md](CONTRIBUTING.md).

## What to expect

- **Green auto-merges — except here.** The platform default is auto-merge on a
  green gate: the App arms `gh pr merge --auto` and GitHub merges the moment every
  required check (the fan-in Quality gate + SonarCloud) passes, with no human
  running the merge. Because it IS the gate engine,
  [`.github/CODEOWNERS`](.github/CODEOWNERS) owns the control-plane paths — the
  engine source (`src/tc_fitness/`), its config and pins (`pyproject.toml`,
  `uv.lock`, `.python-version`, `.uv-version`), CI (`.github/`), and the licence
  — so a PR touching any of those **holds for a maintainer review and does not auto-merge**;
  a docs-, test-, or CHANGELOG-only PR auto-merges on green like any other. An
  agent must never be able to weaken the gate that gates it.
- **Red you fix.** A failing check is never bypassed. If it fails, you fix your
  change — you do not force it in. Green on your laptop but red in CI is a bug in
  the local setup; fix the setup, do not force the merge.
- **Merge mechanics.** Merges are a merge commit (squash and rebase are disabled
  at the repo level). `gh pr merge --admin` is an owner-only logged exception an
  agent requests and never self-authorises; a ruleset with no bypass actors
  blocks even an admin.

## Where to go next

- The canonical standard index: **[tc-pipelines/governance/STANDARDS.md](https://github.com/three-cubes/tc-pipelines/blob/main/governance/STANDARDS.md)**
  — links to everything authoritative. Improve the canonical standard; do not
  fork your own copy.
- The shared commit / PR / merge procedure: **[tc-pipelines `governance/standards/development-workflow.md`](https://github.com/three-cubes/tc-pipelines/blob/main/governance/standards/development-workflow.md)**
  — every repo follows it; the `harness_canon_reference` gate requires this
  reference to be present.
- The identity and authentication boundary: **[tc-pipelines `governance/agent-sdlc-access-and-hitl.md`](https://github.com/three-cubes/tc-pipelines/blob/main/governance/agent-sdlc-access-and-hitl.md)**
  — commit metadata is configured locally; authenticated GitHub writes use the
  approved host broker owned by the platform and consuming repo.
- **[CONTRIBUTING.md](CONTRIBUTING.md)** — how to author or improve a CORE check
  in this repo and prepare the feature PR that becomes the release.
- The canonical package-release workflow:
  **[tc-pipelines `governance/standards/sdlc-release-workflow.md`](https://github.com/three-cubes/tc-pipelines/blob/main/governance/standards/sdlc-release-workflow.md)**
  — preparation receipt, reviewed merge, immutable tag and replay behavior.
- **[tc-pipelines](https://github.com/three-cubes/tc-pipelines)** — the shared CI
  and deploy steps every repo's GitHub Actions calls
  (`uses: …/python-quality-gate.yml@<full-commit-sha> # vX.Y.Z`).
  These steps *run* this check.

---

The rest of this file is reference: the config schema, the step kinds, and the
library modules tc-fitness ships.

## The `[tool.tc_fitness]` config

Consumer repositories use `tc-fitness run` as the shared static gate. This
repository composes that gate with its own exact-commit coverage transaction:

```bash
make prepare       # sync the lock and apply deterministic formatting fixes
make smoke         # <60s staged feedback; never admissible coverage evidence
make check         # clean committed tree + static gate + fresh base/head coverage
```

```yaml
# Self CI: matrix check-static + one exact-base/head coverage-assurance job
```

`make check` runs preparation first and withholds evaluation if preparation
changes a file or any other working-tree change is present. Commit the exact
bytes to evaluate, then rerun it. Coverage evidence is written outside the
checkout. `make check-static` runs ruff, format verification, mypy and branch
naming without repeating the coverage transaction.

You declare the check **once**, in a `[tool.tc_fitness]` block in your
`pyproject.toml` (or a dedicated `.tc-fitness.toml`):

```toml
[tool.tc_fitness]
name = "tc-agent-zone quality gate"

[[tool.tc_fitness.steps]]
id = "deps"
run = ["uv", "sync", "--all-packages", "--locked"]

[[tool.tc_fitness.steps]]
id = "ruff"
run = ["ruff", "check", "scripts", "tests"]
fix = "run `ruff check --fix scripts tests`"
next = "re-run tc-fitness run"

[[tool.tc_fitness.steps]]
id = "bandit"
run = ["bandit", "-r", "scripts", "-ll", "-ii", "-c", "pyproject.toml"]

[[tool.tc_fitness.steps]]
id = "tests"
# A `shell` step is run through the shell — use it for the exact pytest line,
# with its test dirs, `--cov` roots, markers, and `-n auto`.
shell = "pytest -q tests -m 'not soak' -n auto --cov=scripts --cov=tools --cov-branch --cov-report=xml:coverage.xml"

[[tool.tc_fitness.steps]]
id = "secrets"
shell = "git diff --name-only origin/main...HEAD | xargs -r detect-secrets-hook --baseline .secrets.baseline"

# The architecture-rules catalogue is dispatched in-process via the shared
# runner — no second python boot. It names your repo's RuleEntry catalogue.
[[tool.tc_fitness.steps]]
id = "fitness"
summary = "architecture rules"
catalogue = "scripts.checks._rule_catalogue:ALL_ENTRIES"
checks_dir = "scripts/checks"
dispatch = "subprocess"
parallel = true
```

Each step is one of:

| Step kind | Field | Runs as |
|---|---|---|
| command vector | `run = ["prog", "arg"]` | a child process (no shell) |
| shell string | `shell = "a \| b"` | a child process through the shell (pipelines / globs / `$(...)`) |
| catalogue | `catalogue = "module:attr"` | your `RuleEntry` catalogue (your architecture rules), dispatched in-process via `tc_fitness.runner.main_cli` |

Per-step options: `summary`, `cwd`, `env`, `allow_missing` (skip when the program
isn't on PATH instead of failing), `continue_on_error` (record a FAIL but don't
fail the aggregate — informational steps), `shard_args` (argv appended to a `run`
step under `--shard i/N`, with `{index}`/`{total}` substituted — e.g.
`["--splits", "{total}", "--group", "{index}"]` for pytest-split), `stage` (steps
sharing a stage run **concurrently**), `depends_on` (stage names that must finish
first — a barrier), `tags` (membership for the `--tier` selector), and `fix:` /
`next:` lines printed under the step's FAIL. The full schema lives in
[`src/tc_fitness/gate_config.py`](src/tc_fitness/gate_config.py).

**Concurrency (v0.10.0).** Give steps a `stage` and they run at the same time —
subprocess `run`/`shell` legs on a bounded worker pool (`max_workers`, default 8),
an in-process `catalogue` step on the main thread, overlapping in wall-clock —
while their output is buffered and replayed in registration order so the ledger
stays byte-stable. `depends_on` makes one stage wait for another:

```toml
# lint ‖ type ‖ security run concurrently; the test stage waits for `checks`.
[[tool.tc_fitness.steps]]
id = "ruff"    ; stage = "checks" ; run = ["ruff", "check", "."]
[[tool.tc_fitness.steps]]
id = "mypy"    ; stage = "checks" ; run = ["mypy", "src"]
[[tool.tc_fitness.steps]]
id = "pytest"  ; stage = "test" ; depends_on = ["checks"] ; run = ["pytest"] ; tags = ["full"]
```

A config with no `stage`/`depends_on` runs the untouched sequential path,
byte-identical to earlier versions.

`tc-fitness run` flags: `--repo-root` (default CWD), `--only ID` (run a subset of
steps, repeatable), `--gate ID` (target one architecture rule inside a catalogue
step), `--staged` (the `<60s` fast tier — catalogue steps run through the *sound*
per-rule `--staged` selection, and any step flagged `skip_when_staged` in config,
e.g. a full `pytest`/`mypy` leg, is dropped), `--changed-files-from PATH`
(the CI fast tier — same selection semantics, but the changed paths come from a
newline-delimited PR-diff file instead of the git index), and `--shard I/N` (run
shard *i* of *N*: append each opted-in step's substituted `shard_args` and set
`COVERAGE_FILE=.coverage.<i>`, so a CI workflow can matrix `--shard 1/N … N/N`
across runners and `coverage combine` the shard files into one report — the
`skip_when_staged` full `pytest` leg is the intended target), and `--tier NAME`
(run only steps whose `tags` include NAME — e.g. `smoke`/`full`/`nightly` — which
composes with `--only`, `--staged` and `--changed-files-from`). This is the
fast-feedback entrypoint kairix's `safe-commit.sh --check` builds on, with
`--changed-files-from` as the GitHub Actions companion.

### CORE checks

The `[[tool.tc_fitness.steps]]` list above orchestrates a repo's own commands and
its `catalogue` of architecture rules. tc-fitness also **ships** a set of
repo-agnostic CORE checks — the `core:<name>` namespace (coverage, duplication,
determinism, commit-identity, and more; see [CHANGELOG.md](CHANGELOG.md) for the
full set). Bind one with a `[tool.tc_fitness.core_checks.<name>]` block that
scopes it plus a catalogue row that references it:

```toml
[tool.tc_fitness.core_checks.deterministic_tests]
roots = ["tests"]
```

```python
RuleEntry(id="deterministic-tests", check="core:deterministic_tests",
          category="test-integrity", summary="Tests are stable across seeds and orders.")
```

A CORE check with **no config block is a vacuous pass** — the standard adoption
contract, so repinning to a newer engine never breaks a build until the repo opts
in. [`docs/STANDARDS.md`](docs/STANDARDS.md) is the worked example
(`deterministic_tests`); every shipped check binds through the same
`[tool.tc_fitness.core_checks.<name>]` table.

For deployable surfaces, `core:behavioural_evidence` prevents a static
source-shape test from being credited as runtime proof. Consumers declare the
critical surface globs plus claims that bind each surface to its executable and
integration/E2E tests. The hard gate verifies that a named test invokes the
exact executable and asserts its result and produced output; it does not support
baselines.

### Check-contract execution

Execute a `tc.fitness/check-contract/v1` case through the same CORE dispatcher:

```sh
tc-fitness run --contract path/to/contract.yaml --case violation --ledger artifacts/violation.json
```

These three arguments are required together and cannot be combined with ordinary
gate options. The fixture is copied into a temporary repository; its declared
config and a single catalogue entry are passed to the existing runner. Fixtures
must be contained beneath the manifest and cannot contain symlinks.
Configuration must use fixture-relative paths and cannot select an external
rule name. Manifest bytes, parsed configuration, fixture digest and
candidate identity are captured before dispatch. A changed manifest, original
fixture or candidate source invalidates the run before a ledger can be published.
Every finding is a hard failure in contract and ordinary consumer execution;
there is no baseline or adoption mode.
Contract configuration also uses the reviewed per-CORE option inventory in
`tc_fitness.check_contract_policy`. Unknown options fail closed: new aliases
must be classified before assurance can use them. Adoption flags must be false,
exclusion lists must be empty, and cutover, informational-job and test-filename
exemption overrides are forbidden. OSV requires explicit `required: true`;
mutation-report contracts require explicit `allow_missing_current: false`.
Tier-marker contracts require explicit `require_module_marker: true` so
contract assurance cannot fall back to generic function-level classification.
Mutation `baseline_report` is a bound input report, not a suppression list.
Normal scope, thresholds and expected identities remain detector policy inputs.
The output directory must exist, and the ledger must be a new path outside the
fixture. Retries retain the previous ledger and use a new output path.

The command returns the observed result: 0 for pass, 1 for a check violation,
and 2 for an execution or dependency error. An expected violation therefore still
returns non-zero. To evaluate whether that observed result satisfies the case,
use the process runner, which invokes the installed `tc-fitness run` entrypoint
and validates its ledger:

```python
from pathlib import Path
from tc_fitness.check_contract_execution import run_contract_case

evidence = run_contract_case(
    Path("path/to/contract.yaml"), "violation", Path("artifacts/violation.json")
)
```

`CheckContractError` means the assurance case failed. Missing evidence, unexpected
findings or exits, stale timestamps, changed inputs, and digest mismatches are
failures. Each dependency-backed check reports its own unavailable executable as
an `error`; the contract harness never synthesises a dependency finding or skips
the check. That error satisfies only a case expecting its structured finding.

An unavailable case can remove PATH-resolved tools from its execution environment
without installing substitutes:

```yaml
environment:
  schema: tc.fitness/check-environment/v1
  path: empty
```

This optional per-case declaration accepts only `inherit` and `empty`. Omission
means `inherit`; only the `unavailable` case may use `empty`. Its PATH points to
an empty temporary directory during the same check dispatch and is then restored.
Compliant and violation cases use the ordinary environment. The declaration is
bound in the case digest and ledger. Absolute executable defaults remain absolute;
a PATH-absence case must configure the real check to resolve its declared tool
through PATH (for example, `python_executable: python3` for `script_help_smoke`).

The `tc.fitness/check-ledger/v1` JSON binds the check and case, manifest and case
digests, fixture contents and permissions, package version and source digest,
execution environment, UUID and timestamps, expected and actual outcomes, and structured
findings. `payload_digest` is SHA-256 over the UTF-8 JSON object with that field
removed, sorted keys, compact separators, unescaped Unicode and no NaN values.
The validator recomputes it; it is an integrity digest, not a signature.

Checks emit findings through `tc_fitness.check_evidence.report_finding` at the
actual decision point. `gate()`-based checks, including `license_present`, already
use this interface. Custom checks must emit their own structured findings;
console output is never parsed and detectors are never invoked twice.

### Independent coverage floors

The existing `core:coverage_floor` check supports strict, baseline-free admission
by configuring `branch_floor_pct` alongside its per-file line floor:

```toml
[tool.tc_fitness.core_checks.coverage_floor]
roots = ["src/tc_fitness"]
coverage_report = "coverage.xml"
floor_pct = 95
branch_floor_pct = 95
critical_branch_files = [
  "src/tc_fitness/gate.py",
  "src/tc_fitness/runner.py",
  "src/tc_fitness/gate_config.py",
  "src/tc_fitness/runtime_contract.py",
]
```

This mode requires complete Cobertura file and line detail, reconciles summary
counts, and calculates line and branch percentages independently. Critical files
require 100% branch coverage. Missing files/details, inconsistent counts, invalid
thresholds, exemptions and empty source scope cannot pass. Untracked Python files
within the declared roots are included. Existing line-only consumers remain
compatible when `branch_floor_pct` is absent.

The repository's self gate measures fresh branch-aware evidence for the exact
base and candidate commits. It enforces the absolute floors, exact-base
changed-line coverage and non-regression in one transaction. Missing or
uncommitted evidence is an error.

### Exact-base coverage and evidence handoff

The new self-assurance transaction measures both exact commits afresh:

```bash
tc-fitness assure-coverage --base-commit <full-base-sha> \
  --candidate-commit <full-head-sha> --evidence-dir /external/new-evidence \
  --output /external/path/result.json
```

It verifies HEAD and ancestry, creates two detached clean worktrees, runs the
fixed self-assurance test/profile in each, and immediately compares immutable
in-memory measurements. It enforces 95 percent line/branch floors, 100 percent
critical-predicate branches and changed executable lines, plus non-regression
from the fresh exact-base measurement. Neither accepted receipts/digests nor
candidate-configured roots, tests, floors or base selectors are inputs. The
optional JSON is output-only and cannot be imported for admission.

Each detached checkout gets its own external environment provisioned with
`uv sync --locked --all-extras`. Coverage and pytest run through that
environment's Python; provisioning or test failure is a terminal error, never
a fallback to the controller environment. Measurements retain the lock digest
and actual Python, Coverage.py, pytest and uv identities. The current trusted
engine independently parses and adjudicates the reports. Its fixed pytest
configuration registers tier names but does not load the candidate's tier
plugin or candidate-selected pytest configuration.

The evidence directory must be outside the checkout, new or empty and not a
symlink. Per-side provisioning logs, Python/pytest/Coverage output, XML/JSON
and `transaction.json` survive both success and failure; error output names
the failing side/phase and relative native log paths. Only detached worktrees
and their temporary environments are cleaned up. The controller recognises
complete registered contract-fixture directories using its own manifest
validator; those fixture cases run through their public contract tests rather
than being collected as outer pytest modules. Malformed or unregistered
directories remain subject to ordinary collection.

Possible branch arcs come from Coverage.py's analysis of bound Python source.
JSON executed/missing arcs must partition those opportunities, and XML must
agree on each branch's total and covered exits. Removing metadata from both
reports cannot turn a real branch into a zero-opportunity measurement.

The engine accepts full immutable IDs only. Trusted local and hosted wrappers
resolve the Git event or default-branch merge base. The self gate does not
select an accepted receipt or allow the candidate to choose its anchor.

`core:new_code_coverage` accepts `exact_base_commit` and `candidate_commit` as
full immutable Git object IDs (or explicit `env:NAME` bindings). This mode
requires `floor_pct = 100`, complete Python roots and no exemptions. It rejects
unavailable/non-ancestor bases, mismatched HEAD, dirty or untracked source,
missing reports and missing executable-line detail. Coverage.py's own source
analysis supplies the executable-line inventory; report omissions cannot turn
changed executable statements into non-code. Ordinary `base_ref` consumers keep
their existing behaviour when exact identities are absent.

The receipt producer remains available to consumer repositories that use the
receipt-admission API. It is not part of this repository's self gate:

```bash
uv run python -m tc_fitness.coverage_admission produce \
  --base-commit "$TC_FITNESS_BASE_COMMIT" \
  --candidate-commit "$TC_FITNESS_CANDIDATE_COMMIT" \
  --source src/tc_fitness --config pyproject.toml \
  --run-id "$TC_FITNESS_RUN_ID" --attempt-id "$TC_FITNESS_ATTEMPT_ID" \
  --output "$TC_FITNESS_COVERAGE_OUTPUT" \
  --digest-output "$TC_FITNESS_COVERAGE_DIGEST_FILE" -- -m pytest -q
```

The output directory and digest handoff must be new for each attempt; the digest
handoff is outside the candidate checkout. The producer never replaces previous
evidence or marks its own measurement accepted. It binds exact commits, complete
source bytes, tracked configuration, XML/JSON digests, integer counts, timestamps,
run/attempt identity, test command, Python and Coverage.py versions.

`coverage_receipt` activates receipt admission on the existing coverage checks.
Its configuration also supplies `coverage_receipt_digest`,
`accepted_coverage_receipt`, `accepted_coverage_digest`, `coverage_config`,
`run_id`, `attempt_id` and `max_age_seconds`. Digests may be literal `sha256:...`
or `file:/absolute/external/path` / `file:env:NAME` handoffs. A digest computed
from the receipt being checked is not an independent trust anchor.

Consumer CI/storage must select and protect the **latest accepted** digest. The
producer and validator do not implement an acceptance store, bootstrap waiver,
signature or hostile-process sandbox. Digest binding detects changed evidence;
it cannot authenticate an attacker who also controls the trusted handoff.

Catalogue steps are hard-gating by default. The removed `baseline_free` option
is rejected rather than silently accepted.

### Pytest tier assurance

Canonical pytest tier assurance uses two complementary checks. Configure
`core:every_test_has_tier_marker` with `require_module_marker = true` to require
one literal module declaration, `pytestmark = pytest.mark.<tier>`, using
`unit`, `contract`, `integration` or `e2e`. In this mode, `tier_markers` cannot
change the vocabulary. Reusing `pytestmark`, aliasing pytest's marker namespace,
and additional explicit tier applications fail; ordinary attributes and
non-tier marks remain valid. The generic default retains configurable tiers
and function-level markers for existing consumers.

Also run `pytest -p tc_fitness.pytest_tiers --strict-markers` (register the four
tiers in pytest configuration). This public plugin checks actual markers at
collection finish, including parametrised, inherited and deselected items.
Missing tiers, two identical tier marks and multiple different tiers fail with
the node ID and exact marker list. It catches dynamic decorators and hook-added
tiers without interpreting Python or starting another pytest process. tc-fitness
enables it in its own pytest `addopts`; its source self-check uses the unsuppressed
violation set. Collection assurance checks the items that pytest collects, not
the correctness of tier selection or code that changes markers after collection.

## Library modules

tc-fitness also ships these modules (the helpers `tc-fitness run` and a repo's
checks both build on):

- **`tc_fitness.lib`** — the merged check helpers:
  - **hard gating** (from kairix `scripts/checks/_arch_lib.py`):
    `gate()`, `python_files()`, `main_entry()`, `repo_relative()`, `REPO_ROOT`.
  - **agent-actionable emit / YAML** (from tc-agent-zone `scripts/checks/_lib/`):
    `actionable()`, `emit_failures()`, `emit_pass()`, `load_yaml()`, `missing_keys()`.
- **`tc_fitness.ratchet`** — the unified grammar for "can only improve, never get
  worse" gates: one override min-length, one marker parser, one suppression
  grammar (see *Drift reconciliation* below).
- **`tc_fitness.runner`** *(v0.3.0)* — the catalogue-driven, repo-agnostic check
  **runner**: in-process dispatch for python checks + guarded (optionally
  parallel) subprocess dispatch for shell checks, the named verdict ledger,
  `--all` / `--gate` / `--staged` modes, and the thin-consumer `main_cli` /
  programmatic `run` API. Supported by `tc_fitness.catalogue` (the `RuleEntry`
  schema), `tc_fitness.context` (the shared file-index + AST parse/walk cache),
  and `tc_fitness.staged` (the sound per-rule staged selection). See *The
  runner (v0.3.0)* below.

## What's in the box

```python
from tc_fitness import (
    # hard gating (kairix surface)
    gate, gate_keys, python_files, main_entry, repo_relative, REPO_ROOT,
    # agent-actionable emit / YAML (tc-agent-zone surface)
    actionable, remediation, emit_failures, emit_pass, load_yaml, missing_keys,
    # unified ratchet primitives
    OVERRIDE_MIN_REASON_LEN, make_override_re, parse_overrides, Override,
    COVERAGE_OVERRIDE_RE, MUTATION_OVERRIDE_RE,
    is_vague_reason, VAGUE_OVERRIDE_RE,
    SUPPRESSION_PATTERNS, BARE_SUPPRESSION_PATTERNS,
    contains_suppression, is_bare_suppression,
)
```

### Hard gating

```python
from pathlib import Path
from tc_fitness import gate, main_entry

# Low-level: fail on any current violation.
exit_code = gate("f26-core-no-provider-imports", violations, REMEDIATION)

# Convenience: scan roots, call a per-file predicate, gate the union.
def file_has_violation(path: Path) -> bool: ...
exit_code = main_entry(file_has_violation, "f26", REMEDIATION, "kairix")
```

`REPO_ROOT` defaults to the current working directory (the repo root when checks
run from `safe-commit.sh` / pre-commit / CI). Every gating helper also accepts an
explicit `repo_root=` keyword for test isolation or monorepo sub-trees.

### Agent-actionable output

```python
from tc_fitness import actionable, emit_failures, emit_pass

fails = [actionable("kairix/x.py:12 leaks a secret", "redact it", "re-run check_f15.py")]
if fails:
    emit_failures("f15-no-secret-logging", fails)  # → stderr
else:
    emit_pass("PASS f15-no-secret-logging")        # → stdout
```

### YAML loading

```python
from tc_fitness import load_yaml, missing_keys

data, err = load_yaml(Path("manifest.yaml"))   # (data, None) | (None, "error")
if err is None:
    absent = missing_keys(data, ("name", "version"))
```

`load_yaml` is available in every default installation. YAML-backed public
surfaces, including check-contract manifests, therefore do not require an
optional extra to parse their configuration.

## What v0.2.0 adds

v0.2.0 extends the surface to cover tc-agent-zone's 116-check fleet — additively,
so kairix's `@v0.1.0` pin needs no change. Four additions:

### `actionable(what, fix, nxt, run=None)` — optional 3-marker form

59 tc-agent-zone checks emit a `fix:/next:/run:` triple. `actionable` now takes an
optional fourth `run` argument; supplying it appends `; run: <run>`. With `run`
omitted (the default), the output is **byte-identical** to v0.1.0's 2-marker
`<what>; fix: <fix>; next: <nxt>`.

```python
actionable("X broke", "do Y", "rerun Z")                  # X broke; fix: do Y; next: rerun Z
actionable("X broke", "do Y", "rerun Z", "python check.py")  # ...; next: rerun Z; run: python check.py
```

### `remediation(fix, nxt, run, *, passing=None, forbidden=None)` — multiline block

30 tc-agent-zone checks emit a multiline F21-shape remediation block: the three
action markers on their own lines, optionally followed by a `Pass` and a
`Forbidden` example. `remediation` formats that block (no trailing newline),
ready to `print()`.

```python
print(remediation(
    "redact the secret", "re-run the check", "python scripts/checks/check_f15.py",
    passing='logger.info("token redacted")',
    forbidden='logger.info(f"token={token}")',
))
# fix: redact the secret
# next: re-run the check
# run: python scripts/checks/check_f15.py
# Pass: logger.info("token redacted")
# Forbidden: logger.info(f"token={token}")
```

### `gate_keys(name, current, remediation)` — string-keyed hard gate

`gate()` keys on `Path` objects and relativises absolute paths under
`repo_root`. `gate_keys()` is its sibling for opaque logical identifiers and
path globs: it does not coerce them to `Path` values. Both return `1` whenever
any current violation exists and `0` only for an empty set.

```python
exit_code = gate_keys("f30", {"F30:my_new_tool"}, REMEDIATION)
exit_code = gate_keys("f89", static_globs, REMEDIATION)
```

### `min_len` floor override on the ratchet vagueness check

`is_vague_reason` and `parse_overrides` now take an optional keyword-only
`min_len`, defaulting to `OVERRIDE_MIN_REASON_LEN` (=40). tc-agent-zone's shell
directives use a 10-char floor, so its checks call `min_len=10`. The constant is
unchanged and the default-arg behaviour is byte-identical to v0.1.0 — the lower
floor is a per-call choice, never a mutation of the shared default kairix depends
on.

```python
is_vague_reason("x" * 10)               # True  — vague at the default 40-floor
is_vague_reason("x" * 10, min_len=10)   # False — clears taz's 10-floor
```

### Discovery helpers (`REPO_ROOT` / `python_files` / `repo_relative`) cover taz unchanged

tc-agent-zone reimplements `REPO_ROOT = Path(__file__).resolve().parents[2]` inline
in each check. The package's CWD-anchored `REPO_ROOT = Path.cwd()` is the correct
shared replacement: it resolves to the consumer repo root in the `safe-commit.sh`
/ pre-commit / CI invocation paths (where checks run *from* the repo root), and
every gating helper accepts an explicit `repo_root=` for the rare case that
assumption doesn't hold. No additive gap was found here — `python_files`,
`repo_relative`, and `main_entry` already cover taz's `.py` discovery.

## How repositories consume it

To add tc-fitness to a repo, follow [How to add it to a repo](#how-to-add-it-to-a-repo)
above — pin the latest release tag (see [CHANGELOG.md](CHANGELOG.md)) in your
`pyproject.toml` and run `uv run tc-fitness run`. This section explains how the
version pin works.

Pin to a tag (git install — no PyPI publish); never `@main`. The version is the
contract your checks depend on, so a repo only moves when you bump the tag:

```toml
[project.optional-dependencies]
dev = [
  "three-cubes-fitness @ git+https://github.com/three-cubes/tc-fitness.git@v0.11.0",
]
```

or, equivalently, on the command line:

```bash
pip install "three-cubes-fitness @ git+https://github.com/three-cubes/tc-fitness.git@v0.11.0"
```

Each release is an additive, backward-compatible superset of the one before, so a
repo pinned to an older tag keeps working unchanged and bumps only when it needs
the newer surface — repin on your own schedule to adopt a newer CORE-check or
runner surface.

## The runner (v0.3.0)

v0.3.0 adds a **single, common, repo-agnostic check runner** that both kairix
and tc-agent-zone point their `run_checks.py` at — the structural keystone of
"one common fitness process for all repos". It is purely additive: the v0.1.0 /
v0.2.0 lib + ratchet surface is untouched.

### Thin-consumer API

A repo declares its own `tuple[RuleEntry, ...]` catalogue and its check modules,
then its `run_checks.py` collapses to:

```python
from tc_fitness.runner import main_cli
from .catalogue import RULES
raise SystemExit(main_cli(RULES))
```

`main_cli` parses `--all` / `--staged` / `--changed-files-from PATH` /
`--gate <id>` and returns the process exit code. For tests and embedding there
is a programmatic `run(rules, *, mode, staged_files=None, repo_root=None, ...) ->
Verdicts`.

### What the runner does

- **In-process dispatch** for python checks (`check_<x>.py` exposing
  `main() -> int`): the module is imported and `main()` is called inside one
  process, sharing a single `CheckContext` whose AST cache parses every file at
  most once. A check that raises is isolated into a FAIL — one crash never
  aborts the ledger.
- **Guarded subprocess dispatch** for `*.sh` shell detectors. Sequential by
  default (byte-identical interleaving with kairix's runner); pass
  `parallel_subprocess=True` to run them on a `ThreadPoolExecutor` with output
  buffered and replayed in catalogue order (tc-agent-zone's parallelism).
- **The named verdict ledger** — a `run [id]` line and a `PASS [id]` / `FAIL
  [id]` verdict per rule, then the aggregate verdict; the format kairix's F83
  gate-runner contract depends on.
- **`--all`** (dispatchable AND `run_all`), **`--gate <id>`** (one rule), and
  **`--staged`** / **`--changed-files-from PATH`** — the *sound* per-rule
  staged selection (file-local / relational / always-run), single-sourced on
  each `RuleEntry`. The hard invariant is **no false negative on a changed
  path**: when scope can't be resolved, the rule runs (fail-safe).
- A **footer hook** so a failing rule can point an agent at the repo's own query
  surface.

### Repo-agnostic by injection

The runner never imports `kairix` or `tc-agent-zone`. Repo-specific behaviour is
injected through `RunnerConfig` seams:

| Seam | Purpose |
|---|---|
| `repo_root` / `checks_dir` | where the repo + its check scripts live |
| `scope_resolver` | derive a rule's staged scope from its check script (the repo's FitnessRule-aware hook) when `staged_scope` is unset |
| `enumeration_narrower` | the repo's extra file-index narrowing for file-local staged runs, layered on top of the package-level `tc_fitness.python_files` narrowing |
| `conditional_check` | govern a `subprocess_arg_env` rule's runtime arg + exact skip text (e.g. a coverage check that needs a Cobertura XML) |
| `footer` | the line printed under a FAIL pointing at the repo's query surface |
| `parallel_subprocess` | run shell checks on a thread pool |

`RuleEntry.id` is id-agnostic — it accepts kairix's `"F26"` and tc-agent-zone's
`"no-duplicate-string"` style equally; the runner only uses it as a ledger label
and the `--gate` selector. `category` / `scope` are open `str` fields each repo
curates its own closed vocabulary for.

### Drop-in for kairix's local runner

The runner is byte-identical to kairix's current `scripts/checks/run_checks.py`:
wiring kairix's `_check_context` / `_staged_selection` / `_rule_catalogue` into
`main_cli` via the seams above reproduces the **same verdicts and the same
named-ledger text** for `--all`, `--gate`, and `--staged` (verified by diffing
the two runners' output over the full catalogue, including file-local staged
narrowing). kairix's migration is therefore mechanical: translate its `RuleEntry`
rows to the package schema, pass its three helper modules as hooks, and collapse
`run_checks.py` to the three-line form.

## Drift reconciliation

Both repos independently grew the same "can only improve, never get worse" gates
(coverage, mutation-survival, sonar-quality) and drifted on three details. This
package resolves each to one behaviour. The merged version is the
**superset-correct** choice — it satisfies every call pattern either repo relied
on.

### 1. Override-rationale minimum length → **40 chars, strictly-less-than**

tc-agent-zone's coverage ratchet treated a rationale as "vague" below **20**
chars; its mutation ratchet used **40**. The *remediation text both gates printed
to operators already said "≥40 chars"* — so the 20-char path was a latent bug
(code disagreed with its own message). Reconciled to `OVERRIDE_MIN_REASON_LEN =
40`, and `len(reason) < 40` is vague. Stricter of the two, and matches the
documented contract. **Mutation's behaviour won.**

### 2. Suppression-pattern list → **the superset, one grammar**

tc-agent-zone added `NOSONAR` (and the `//` C-style variants) to the marker set
kairix originally tracked, and the regex copies had possessive-quantifier
variations. Reconciled to the **union** of every marker any repo tracked:
`SUPPRESSION_PATTERNS` (substring markers for "flag any line containing one") and
`BARE_SUPPRESSION_PATTERNS` (end-of-line regexes for "bare suppression, no
rationale"). `NOSONAR` is in both. **The superset won** — dropping any marker
would silently un-gate a suppression one repo was catching.

### 3. Override-marker separator → **em-dash *and* hyphen both accepted**

tc-agent-zone's override-line regex accepted an em-dash **or** an ASCII hyphen as
the path↔reason separator (`[—-]++`); some kairix copies were em-dash-only.
Reconciled to **accept both** (`make_override_re` builds the parser; the
separator class is `[—-]++`, possessive to avoid backtracking). A commit that
wrote `coverage-ratchet-acknowledged: path - reason` with a plain hyphen must keep
clearing the ratchet, and so must the em-dash form. **The superset (tc-agent-zone's
looser parse) won.**

## Development

This repo IS the gate engine. Set up and run its own tests:

```bash
uv sync --all-extras --all-groups
uv run pytest tests/ -q
```

The package has one runtime dependency, PyYAML, for its YAML-backed public
surfaces. It must never import from `kairix` or `tc-agent-zone` — it is the
shared core both depend on. `tests/test_lib.py` pins the call patterns consumers'
checks depend on; `tests/test_ratchet.py` pins the reconciled ratchet grammar
(40-char threshold; em-dash and hyphen; `NOSONAR` in the suppression set).

### Author or improve a CORE check

1. **Add the check** at `src/tc_fitness/core_checks/<name>.py` as a config-driven
   `FitnessRule` subclass — bake in no repo identity; every knob (`roots`,
   `extensions`, thresholds) arrives from the consumer's config. Register it in
   the `CORE_CHECKS` registry so the catalogue exposes it.
2. **Pair it with a test** at `tests/test_core_<name>.py` — the convention every
   `core_checks/` module follows.
3. **Release additively.** Keep every existing public signature byte-identical and
   make the new surface opt-in with a safe default (a check with no config block
   is a vacuous pass). Add the release note under `Unreleased`, dispatch
   `Prepare release` on the feature branch, verify the generated receipt and
   gate, then merge that same reviewed PR. `release-on-merge.yml` creates the
   immutable tag and GitHub Release at the merge commit. The rule and its
   rationale are canon in [CHANGELOG.md](CHANGELOG.md); do not restate them.
4. **Consumers bind it** by repinning `three-cubes-fitness` on their own schedule
   and adding a `[tool.tc_fitness.core_checks.<name>]` block plus the catalogue
   row (see [CORE checks](#core-checks) above).

Gates live only in tc-fitness — converge up, never fork a parallel gate in a
consumer repo. To improve the **pipeline** rather than a gate, change the
tc-pipelines reusable (`python-quality-gate.yml`) or its composite action,
SHA-pin any third-party `uses:` (Sonar S7637), tag it, and move consumers to the
tag's full commit SHA with the tag retained as a comment. The full preparation,
reviewed-merge, publication and recovery procedure is in
[CONTRIBUTING.md](CONTRIBUTING.md).
