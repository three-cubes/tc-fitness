"""CORE check: ci_fanin_parity — every CI job gates the merge or says it doesn't.

Branch protection typically requires exactly ONE status context from the CI
workflow: the terminal aggregator job whose ``needs:`` fan-in aggregates every
blocking stage. A green merge is only as safe as that fan-in is COMPLETE. A job
defined in the workflow but NOT reachable from the aggregator's transitive
``needs:`` closure does not block the merge — it can run, fail, and the PR ships
green. This rule proves the workflow is INTERNALLY HONEST: every non-gating job
explicitly SAYS it is non-gating via an informational marker comment.

The check parses the configured workflow, finds the aggregator job (by its
``name:``), builds the transitive ``needs:`` closure, and flags the workflow when
any job is NEITHER in that closure, NOR the aggregator itself, NOR carrying an
``# fan-in: informational`` marker comment in the lines directly above its key.

Ported from kairix ``scripts/checks/check_f93_ci_fanin_parity.py`` (EPIC #499
Phase 2) and re-expressed as a configurable, repo-agnostic rule. The donor
hardcoded ``.github/workflows/ci.yml`` and the ``CI gate`` aggregator name; here
both are config:

* ``workflow`` — repo-relative path to the CI workflow file.
* ``aggregator_name`` — the ``name:`` of the job producing the required context.
* ``informational_marker`` — the comment prefix that marks a job non-gating.

Modelling note: the FitnessRule baseline is per-FILE, so a dishonest fan-in
surfaces as one violation (the workflow path). The remediation names the class;
the operator reads the workflow to find the specific dangling job(s).
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

import yaml

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: The job ``name:`` whose status context branch protection requires. Overridable.
DEFAULT_AGGREGATOR_NAME = "CI gate"

#: The comment prefix declaring a job legitimately outside the gate fan-in.
DEFAULT_INFORMATIONAL_MARKER = "# fan-in: informational"

#: The CI workflow this rule governs. Overridable via config.
DEFAULT_WORKFLOW = ".github/workflows/ci.yml"

REMEDIATION = _remediation(
    fix=(
        "decide whether the dangling job SHOULD gate the merge. If yes, add its "
        "id to the aggregator job's needs: list (and its result-evaluation "
        "loop). If no, add a marker comment on the lines directly above the "
        "job's key: '# fan-in: informational - <why it is non-gating>'."
    ),
    nxt="re-run this check to confirm the fan-in is honest.",
    run="python -m tc_fitness.core_checks.ci_fanin_parity",
    passing="check:\\n    name: CI gate\\n    needs: [unit, security, docker]",
    forbidden="license-scan defined but absent from the CI-gate needs: and unmarked",
)


def _load_jobs(workflow_text: str) -> dict[str, Any]:
    """Parse the workflow and return its non-empty ``jobs`` mapping.

    PyYAML is a required runtime dependency, so importing this enabled check
    fails immediately if its parser is unavailable.
    """
    try:
        data = yaml.safe_load(workflow_text)
    except yaml.YAMLError as exc:
        raise ValueError("workflow is not valid YAML") from exc
    if not isinstance(data, dict):
        raise ValueError("workflow root must be a mapping")
    jobs = data.get("jobs")
    if not isinstance(jobs, dict) or not jobs:
        raise ValueError("workflow must define a non-empty jobs mapping")
    return jobs


def _needs_of(job_spec: dict[str, Any]) -> list[str]:
    """Normalise a job's ``needs:`` (scalar or sequence) to a list of strings."""
    if "needs" not in job_spec:
        return []
    needs = job_spec["needs"]
    if isinstance(needs, str):
        return [needs]
    if isinstance(needs, list) and all(isinstance(node, str) for node in needs):
        return needs
    raise ValueError("job needs must be a job id or a list of job ids")


def _validate_jobs(jobs: dict[str, Any]) -> None:
    """Reject job definitions and dependency graphs that cannot be verified."""
    graph: dict[str, list[str]] = {}
    for job_id, job_spec in jobs.items():
        if not isinstance(job_id, str) or not job_id or not isinstance(job_spec, dict):
            raise ValueError("every workflow job must have an id and mapping definition")
        dependencies = _needs_of(job_spec)
        if any(not dependency for dependency in dependencies):
            raise ValueError("job needs cannot contain an empty job id")
        if any(dependency not in jobs for dependency in dependencies):
            raise ValueError("job needs references an undefined job")
        graph[job_id] = dependencies

    state: dict[str, int] = {}
    for job_id in graph:
        pending: list[tuple[str, bool]] = [(job_id, False)]
        while pending:
            node, leaving = pending.pop()
            if leaving:
                state[node] = 2
                continue
            status = state.get(node, 0)
            if status == 1:
                raise ValueError("workflow job dependencies contain a cycle")
            if status == 2:
                continue
            state[node] = 1
            pending.append((node, True))
            pending.extend((dependency, False) for dependency in graph[node])


def _find_aggregator(jobs: dict[str, Any], aggregator_name: str) -> str | None:
    """Return the job id whose ``name:`` is ``aggregator_name``, else None."""
    matches: list[str] = []
    for job_id, spec in jobs.items():
        if spec.get("name") == aggregator_name:
            matches.append(job_id)
    return matches[0] if len(matches) == 1 else None


def _closure(jobs: dict[str, Any], root: str) -> set[str]:
    """Transitive ``needs:`` closure rooted at ``root`` (root excluded)."""
    seen: set[str] = set()
    frontier = list(_needs_of(jobs[root]))
    while frontier:
        node = frontier.pop()
        if node in seen:
            continue
        seen.add(node)
        frontier.extend(_needs_of(jobs[node]))
    return seen


def _jobs_marked_informational(workflow_text: str, marker: str) -> set[str]:
    """Job ids carrying the informational ``marker`` in the comment block above.

    PyYAML discards comments, so this scans the raw text. A job key sits at
    exactly two-space indent under ``jobs:`` and ends in a bare colon.
    """
    lines = workflow_text.splitlines()
    marked: set[str] = set()
    for idx, raw in enumerate(lines):
        stripped = raw.strip()
        if not (raw.startswith("  ") and raw[2:3] != " "):
            continue
        if not stripped.endswith(":"):
            continue
        job_id = stripped[:-1].strip()
        for raw_above in reversed(lines[:idx]):
            above = raw_above.strip()
            if above.startswith("#"):
                if marker in raw_above:
                    marked.add(job_id)
                    break
                continue
            break
    return marked


def workflow_fanin_is_dishonest(
    path: Path,
    *,
    aggregator_name: str,
    informational_marker: str,
) -> bool:
    """True iff the workflow at ``path`` has a dangling (un-gated, un-marked) job.

    Pure helper (the detection core) so tests can assert on it directly. Returns
    True when the aggregator is missing entirely, or when any non-aggregator job
    is neither in the aggregator's needs-closure nor marked informational. An
    unreadable, malformed, or otherwise unverifiable configured workflow
    returns True so the gate cannot pass without validating its input.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return True
    try:
        jobs = _load_jobs(text)
        _validate_jobs(jobs)
    except ValueError:
        return True
    aggregator = _find_aggregator(jobs, aggregator_name)
    if aggregator is None:
        return True
    gated = _closure(jobs, aggregator)
    informational = _jobs_marked_informational(text, informational_marker)
    for job_id in jobs:
        if job_id == aggregator or job_id in gated or job_id in informational:
            continue
        return True
    return False


class CiFaninParity(FitnessRule):
    """Flags a CI workflow whose gate fan-in is dishonest."""

    name = "ci-fanin-parity"
    remediation = REMEDIATION
    extensions = (".yml", ".yaml")

    workflow: str = DEFAULT_WORKFLOW
    aggregator_name: str = DEFAULT_AGGREGATOR_NAME
    informational_marker: str = DEFAULT_INFORMATIONAL_MARKER

    @classmethod
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiFaninParity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiFaninParity)  # noqa: S101  # narrowing for mypy
        workflow = config.get("workflow")
        if workflow is not None:
            rule.workflow = str(workflow)
        aggregator = config.get("aggregator_name")
        if aggregator is not None:
            rule.aggregator_name = str(aggregator)
        marker = config.get("informational_marker")
        if marker is not None:
            rule.informational_marker = str(marker)
        return rule

    def is_in_scope(self, rel: str) -> bool:
        # Scope is the single configured workflow file.
        return True

    def enumerate_files(self) -> list[Path]:
        """Enumerate the configured workflow even when it is absent."""
        workflow_path = self._repo_root / self.workflow
        return [workflow_path]

    def file_has_violation(self, path: Path) -> bool:
        return workflow_fanin_is_dishonest(
            path,
            aggregator_name=self.aggregator_name,
            informational_marker=self.informational_marker,
        )


def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> CiFaninParity:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CiFaninParity.from_config(config, repo_root=repo_root)


def main(argv: list[str] | None = None) -> int:
    """CLI entry — supports ``--establish-baseline`` and ``--repo-root``."""
    return run_core_check(CiFaninParity, argv)


if __name__ == "__main__":
    import sys

    sys.exit(main())
