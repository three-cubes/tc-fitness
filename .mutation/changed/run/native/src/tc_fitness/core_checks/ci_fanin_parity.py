"""CORE check: ci_fanin_parity — every CI job gates the merge.

Branch protection typically requires exactly ONE status context from the CI
workflow: the terminal aggregator job whose ``needs:`` fan-in aggregates every
blocking stage. A green merge is only as safe as that fan-in is COMPLETE. A job
defined in the workflow but NOT reachable from the aggregator's transitive
``needs:`` closure does not block the merge — it can run, fail, and the PR ships
green. This rule proves the workflow is INTERNALLY HONEST: every job is in the
terminal gate's dependency closure.

The check parses the configured workflow, finds the aggregator job (by its
``name:``), builds the transitive ``needs:`` closure, and flags the workflow when
any job is neither in that closure nor the aggregator itself.

Ported from kairix ``scripts/checks/check_f93_ci_fanin_parity.py`` (EPIC #499
Phase 2) and re-expressed as a configurable, repo-agnostic rule. The donor
hardcoded ``.github/workflows/ci.yml`` and the ``CI gate`` aggregator name; here
both are config:

* ``workflow`` — repo-relative path to the CI workflow file.
* ``aggregator_name`` — the ``name:`` of the job producing the required context.

The workflow path is the finding unit for a dishonest fan-in. The remediation names the class;
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

#: The CI workflow this rule governs. Overridable via config.
DEFAULT_WORKFLOW = ".github/workflows/ci.yml"

REMEDIATION = _remediation(
    fix=(
        "add the dangling job id to the aggregator job's needs: list and its "
        "result-evaluation loop. Move jobs that do not belong in merge CI to "
        "a separate workflow with an explicit trigger."
    ),
    nxt="re-run this check to confirm the fan-in is honest.",
    run="python -m tc_fitness.core_checks.ci_fanin_parity",
    passing="check:\\n    name: CI gate\\n    needs: [unit, security, docker]",
    forbidden="license-scan defined but absent from the CI-gate needs:",
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x__load_jobs__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__load_jobs__mutmut)
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


def x__load_jobs__mutmut_orig(workflow_text: str) -> dict[str, Any]:
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


def x__load_jobs__mutmut_1(workflow_text: str) -> dict[str, Any]:
    """Parse the workflow and return its non-empty ``jobs`` mapping.

    PyYAML is a required runtime dependency, so importing this enabled check
    fails immediately if its parser is unavailable.
    """
    try:
        data = None
    except yaml.YAMLError as exc:
        raise ValueError("workflow is not valid YAML") from exc
    if not isinstance(data, dict):
        raise ValueError("workflow root must be a mapping")
    jobs = data.get("jobs")
    if not isinstance(jobs, dict) or not jobs:
        raise ValueError("workflow must define a non-empty jobs mapping")
    return jobs


def x__load_jobs__mutmut_2(workflow_text: str) -> dict[str, Any]:
    """Parse the workflow and return its non-empty ``jobs`` mapping.

    PyYAML is a required runtime dependency, so importing this enabled check
    fails immediately if its parser is unavailable.
    """
    try:
        data = yaml.safe_load(None)
    except yaml.YAMLError as exc:
        raise ValueError("workflow is not valid YAML") from exc
    if not isinstance(data, dict):
        raise ValueError("workflow root must be a mapping")
    jobs = data.get("jobs")
    if not isinstance(jobs, dict) or not jobs:
        raise ValueError("workflow must define a non-empty jobs mapping")
    return jobs


def x__load_jobs__mutmut_3(workflow_text: str) -> dict[str, Any]:
    """Parse the workflow and return its non-empty ``jobs`` mapping.

    PyYAML is a required runtime dependency, so importing this enabled check
    fails immediately if its parser is unavailable.
    """
    try:
        data = yaml.safe_load(workflow_text)
    except yaml.YAMLError as exc:
        raise ValueError(None) from exc
    if not isinstance(data, dict):
        raise ValueError("workflow root must be a mapping")
    jobs = data.get("jobs")
    if not isinstance(jobs, dict) or not jobs:
        raise ValueError("workflow must define a non-empty jobs mapping")
    return jobs


def x__load_jobs__mutmut_4(workflow_text: str) -> dict[str, Any]:
    """Parse the workflow and return its non-empty ``jobs`` mapping.

    PyYAML is a required runtime dependency, so importing this enabled check
    fails immediately if its parser is unavailable.
    """
    try:
        data = yaml.safe_load(workflow_text)
    except yaml.YAMLError as exc:
        raise ValueError("XXworkflow is not valid YAMLXX") from exc
    if not isinstance(data, dict):
        raise ValueError("workflow root must be a mapping")
    jobs = data.get("jobs")
    if not isinstance(jobs, dict) or not jobs:
        raise ValueError("workflow must define a non-empty jobs mapping")
    return jobs


def x__load_jobs__mutmut_5(workflow_text: str) -> dict[str, Any]:
    """Parse the workflow and return its non-empty ``jobs`` mapping.

    PyYAML is a required runtime dependency, so importing this enabled check
    fails immediately if its parser is unavailable.
    """
    try:
        data = yaml.safe_load(workflow_text)
    except yaml.YAMLError as exc:
        raise ValueError("workflow is not valid yaml") from exc
    if not isinstance(data, dict):
        raise ValueError("workflow root must be a mapping")
    jobs = data.get("jobs")
    if not isinstance(jobs, dict) or not jobs:
        raise ValueError("workflow must define a non-empty jobs mapping")
    return jobs


def x__load_jobs__mutmut_6(workflow_text: str) -> dict[str, Any]:
    """Parse the workflow and return its non-empty ``jobs`` mapping.

    PyYAML is a required runtime dependency, so importing this enabled check
    fails immediately if its parser is unavailable.
    """
    try:
        data = yaml.safe_load(workflow_text)
    except yaml.YAMLError as exc:
        raise ValueError("WORKFLOW IS NOT VALID YAML") from exc
    if not isinstance(data, dict):
        raise ValueError("workflow root must be a mapping")
    jobs = data.get("jobs")
    if not isinstance(jobs, dict) or not jobs:
        raise ValueError("workflow must define a non-empty jobs mapping")
    return jobs


def x__load_jobs__mutmut_7(workflow_text: str) -> dict[str, Any]:
    """Parse the workflow and return its non-empty ``jobs`` mapping.

    PyYAML is a required runtime dependency, so importing this enabled check
    fails immediately if its parser is unavailable.
    """
    try:
        data = yaml.safe_load(workflow_text)
    except yaml.YAMLError as exc:
        raise ValueError("workflow is not valid YAML") from exc
    if isinstance(data, dict):
        raise ValueError("workflow root must be a mapping")
    jobs = data.get("jobs")
    if not isinstance(jobs, dict) or not jobs:
        raise ValueError("workflow must define a non-empty jobs mapping")
    return jobs


def x__load_jobs__mutmut_8(workflow_text: str) -> dict[str, Any]:
    """Parse the workflow and return its non-empty ``jobs`` mapping.

    PyYAML is a required runtime dependency, so importing this enabled check
    fails immediately if its parser is unavailable.
    """
    try:
        data = yaml.safe_load(workflow_text)
    except yaml.YAMLError as exc:
        raise ValueError("workflow is not valid YAML") from exc
    if not isinstance(data, dict):
        raise ValueError(None)
    jobs = data.get("jobs")
    if not isinstance(jobs, dict) or not jobs:
        raise ValueError("workflow must define a non-empty jobs mapping")
    return jobs


def x__load_jobs__mutmut_9(workflow_text: str) -> dict[str, Any]:
    """Parse the workflow and return its non-empty ``jobs`` mapping.

    PyYAML is a required runtime dependency, so importing this enabled check
    fails immediately if its parser is unavailable.
    """
    try:
        data = yaml.safe_load(workflow_text)
    except yaml.YAMLError as exc:
        raise ValueError("workflow is not valid YAML") from exc
    if not isinstance(data, dict):
        raise ValueError("XXworkflow root must be a mappingXX")
    jobs = data.get("jobs")
    if not isinstance(jobs, dict) or not jobs:
        raise ValueError("workflow must define a non-empty jobs mapping")
    return jobs


def x__load_jobs__mutmut_10(workflow_text: str) -> dict[str, Any]:
    """Parse the workflow and return its non-empty ``jobs`` mapping.

    PyYAML is a required runtime dependency, so importing this enabled check
    fails immediately if its parser is unavailable.
    """
    try:
        data = yaml.safe_load(workflow_text)
    except yaml.YAMLError as exc:
        raise ValueError("workflow is not valid YAML") from exc
    if not isinstance(data, dict):
        raise ValueError("WORKFLOW ROOT MUST BE A MAPPING")
    jobs = data.get("jobs")
    if not isinstance(jobs, dict) or not jobs:
        raise ValueError("workflow must define a non-empty jobs mapping")
    return jobs


def x__load_jobs__mutmut_11(workflow_text: str) -> dict[str, Any]:
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
    jobs = None
    if not isinstance(jobs, dict) or not jobs:
        raise ValueError("workflow must define a non-empty jobs mapping")
    return jobs


def x__load_jobs__mutmut_12(workflow_text: str) -> dict[str, Any]:
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
    jobs = data.get(None)
    if not isinstance(jobs, dict) or not jobs:
        raise ValueError("workflow must define a non-empty jobs mapping")
    return jobs


def x__load_jobs__mutmut_13(workflow_text: str) -> dict[str, Any]:
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
    jobs = data.get("XXjobsXX")
    if not isinstance(jobs, dict) or not jobs:
        raise ValueError("workflow must define a non-empty jobs mapping")
    return jobs


def x__load_jobs__mutmut_14(workflow_text: str) -> dict[str, Any]:
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
    jobs = data.get("JOBS")
    if not isinstance(jobs, dict) or not jobs:
        raise ValueError("workflow must define a non-empty jobs mapping")
    return jobs


def x__load_jobs__mutmut_15(workflow_text: str) -> dict[str, Any]:
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
    if not isinstance(jobs, dict) and not jobs:
        raise ValueError("workflow must define a non-empty jobs mapping")
    return jobs


def x__load_jobs__mutmut_16(workflow_text: str) -> dict[str, Any]:
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
    if isinstance(jobs, dict) or not jobs:
        raise ValueError("workflow must define a non-empty jobs mapping")
    return jobs


def x__load_jobs__mutmut_17(workflow_text: str) -> dict[str, Any]:
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
    if not isinstance(jobs, dict) or jobs:
        raise ValueError("workflow must define a non-empty jobs mapping")
    return jobs


def x__load_jobs__mutmut_18(workflow_text: str) -> dict[str, Any]:
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
        raise ValueError(None)
    return jobs


def x__load_jobs__mutmut_19(workflow_text: str) -> dict[str, Any]:
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
        raise ValueError("XXworkflow must define a non-empty jobs mappingXX")
    return jobs


def x__load_jobs__mutmut_20(workflow_text: str) -> dict[str, Any]:
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
        raise ValueError("WORKFLOW MUST DEFINE A NON-EMPTY JOBS MAPPING")
    return jobs

mutants_x__load_jobs__mutmut['_mutmut_orig'] = x__load_jobs__mutmut_orig # type: ignore # mutmut generated
mutants_x__load_jobs__mutmut['x__load_jobs__mutmut_1'] = x__load_jobs__mutmut_1 # type: ignore # mutmut generated
mutants_x__load_jobs__mutmut['x__load_jobs__mutmut_2'] = x__load_jobs__mutmut_2 # type: ignore # mutmut generated
mutants_x__load_jobs__mutmut['x__load_jobs__mutmut_3'] = x__load_jobs__mutmut_3 # type: ignore # mutmut generated
mutants_x__load_jobs__mutmut['x__load_jobs__mutmut_4'] = x__load_jobs__mutmut_4 # type: ignore # mutmut generated
mutants_x__load_jobs__mutmut['x__load_jobs__mutmut_5'] = x__load_jobs__mutmut_5 # type: ignore # mutmut generated
mutants_x__load_jobs__mutmut['x__load_jobs__mutmut_6'] = x__load_jobs__mutmut_6 # type: ignore # mutmut generated
mutants_x__load_jobs__mutmut['x__load_jobs__mutmut_7'] = x__load_jobs__mutmut_7 # type: ignore # mutmut generated
mutants_x__load_jobs__mutmut['x__load_jobs__mutmut_8'] = x__load_jobs__mutmut_8 # type: ignore # mutmut generated
mutants_x__load_jobs__mutmut['x__load_jobs__mutmut_9'] = x__load_jobs__mutmut_9 # type: ignore # mutmut generated
mutants_x__load_jobs__mutmut['x__load_jobs__mutmut_10'] = x__load_jobs__mutmut_10 # type: ignore # mutmut generated
mutants_x__load_jobs__mutmut['x__load_jobs__mutmut_11'] = x__load_jobs__mutmut_11 # type: ignore # mutmut generated
mutants_x__load_jobs__mutmut['x__load_jobs__mutmut_12'] = x__load_jobs__mutmut_12 # type: ignore # mutmut generated
mutants_x__load_jobs__mutmut['x__load_jobs__mutmut_13'] = x__load_jobs__mutmut_13 # type: ignore # mutmut generated
mutants_x__load_jobs__mutmut['x__load_jobs__mutmut_14'] = x__load_jobs__mutmut_14 # type: ignore # mutmut generated
mutants_x__load_jobs__mutmut['x__load_jobs__mutmut_15'] = x__load_jobs__mutmut_15 # type: ignore # mutmut generated
mutants_x__load_jobs__mutmut['x__load_jobs__mutmut_16'] = x__load_jobs__mutmut_16 # type: ignore # mutmut generated
mutants_x__load_jobs__mutmut['x__load_jobs__mutmut_17'] = x__load_jobs__mutmut_17 # type: ignore # mutmut generated
mutants_x__load_jobs__mutmut['x__load_jobs__mutmut_18'] = x__load_jobs__mutmut_18 # type: ignore # mutmut generated
mutants_x__load_jobs__mutmut['x__load_jobs__mutmut_19'] = x__load_jobs__mutmut_19 # type: ignore # mutmut generated
mutants_x__load_jobs__mutmut['x__load_jobs__mutmut_20'] = x__load_jobs__mutmut_20 # type: ignore # mutmut generated
mutants_x__needs_of__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__needs_of__mutmut)
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


def x__needs_of__mutmut_orig(job_spec: dict[str, Any]) -> list[str]:
    """Normalise a job's ``needs:`` (scalar or sequence) to a list of strings."""
    if "needs" not in job_spec:
        return []
    needs = job_spec["needs"]
    if isinstance(needs, str):
        return [needs]
    if isinstance(needs, list) and all(isinstance(node, str) for node in needs):
        return needs
    raise ValueError("job needs must be a job id or a list of job ids")


def x__needs_of__mutmut_1(job_spec: dict[str, Any]) -> list[str]:
    """Normalise a job's ``needs:`` (scalar or sequence) to a list of strings."""
    if "XXneedsXX" not in job_spec:
        return []
    needs = job_spec["needs"]
    if isinstance(needs, str):
        return [needs]
    if isinstance(needs, list) and all(isinstance(node, str) for node in needs):
        return needs
    raise ValueError("job needs must be a job id or a list of job ids")


def x__needs_of__mutmut_2(job_spec: dict[str, Any]) -> list[str]:
    """Normalise a job's ``needs:`` (scalar or sequence) to a list of strings."""
    if "NEEDS" not in job_spec:
        return []
    needs = job_spec["needs"]
    if isinstance(needs, str):
        return [needs]
    if isinstance(needs, list) and all(isinstance(node, str) for node in needs):
        return needs
    raise ValueError("job needs must be a job id or a list of job ids")


def x__needs_of__mutmut_3(job_spec: dict[str, Any]) -> list[str]:
    """Normalise a job's ``needs:`` (scalar or sequence) to a list of strings."""
    if "needs" in job_spec:
        return []
    needs = job_spec["needs"]
    if isinstance(needs, str):
        return [needs]
    if isinstance(needs, list) and all(isinstance(node, str) for node in needs):
        return needs
    raise ValueError("job needs must be a job id or a list of job ids")


def x__needs_of__mutmut_4(job_spec: dict[str, Any]) -> list[str]:
    """Normalise a job's ``needs:`` (scalar or sequence) to a list of strings."""
    if "needs" not in job_spec:
        return []
    needs = None
    if isinstance(needs, str):
        return [needs]
    if isinstance(needs, list) and all(isinstance(node, str) for node in needs):
        return needs
    raise ValueError("job needs must be a job id or a list of job ids")


def x__needs_of__mutmut_5(job_spec: dict[str, Any]) -> list[str]:
    """Normalise a job's ``needs:`` (scalar or sequence) to a list of strings."""
    if "needs" not in job_spec:
        return []
    needs = job_spec["XXneedsXX"]
    if isinstance(needs, str):
        return [needs]
    if isinstance(needs, list) and all(isinstance(node, str) for node in needs):
        return needs
    raise ValueError("job needs must be a job id or a list of job ids")


def x__needs_of__mutmut_6(job_spec: dict[str, Any]) -> list[str]:
    """Normalise a job's ``needs:`` (scalar or sequence) to a list of strings."""
    if "needs" not in job_spec:
        return []
    needs = job_spec["NEEDS"]
    if isinstance(needs, str):
        return [needs]
    if isinstance(needs, list) and all(isinstance(node, str) for node in needs):
        return needs
    raise ValueError("job needs must be a job id or a list of job ids")


def x__needs_of__mutmut_7(job_spec: dict[str, Any]) -> list[str]:
    """Normalise a job's ``needs:`` (scalar or sequence) to a list of strings."""
    if "needs" not in job_spec:
        return []
    needs = job_spec["needs"]
    if isinstance(needs, str):
        return [needs]
    if isinstance(needs, list) or all(isinstance(node, str) for node in needs):
        return needs
    raise ValueError("job needs must be a job id or a list of job ids")


def x__needs_of__mutmut_8(job_spec: dict[str, Any]) -> list[str]:
    """Normalise a job's ``needs:`` (scalar or sequence) to a list of strings."""
    if "needs" not in job_spec:
        return []
    needs = job_spec["needs"]
    if isinstance(needs, str):
        return [needs]
    if isinstance(needs, list) and all(None):
        return needs
    raise ValueError("job needs must be a job id or a list of job ids")


def x__needs_of__mutmut_9(job_spec: dict[str, Any]) -> list[str]:
    """Normalise a job's ``needs:`` (scalar or sequence) to a list of strings."""
    if "needs" not in job_spec:
        return []
    needs = job_spec["needs"]
    if isinstance(needs, str):
        return [needs]
    if isinstance(needs, list) and all(isinstance(node, str) for node in needs):
        return needs
    raise ValueError(None)


def x__needs_of__mutmut_10(job_spec: dict[str, Any]) -> list[str]:
    """Normalise a job's ``needs:`` (scalar or sequence) to a list of strings."""
    if "needs" not in job_spec:
        return []
    needs = job_spec["needs"]
    if isinstance(needs, str):
        return [needs]
    if isinstance(needs, list) and all(isinstance(node, str) for node in needs):
        return needs
    raise ValueError("XXjob needs must be a job id or a list of job idsXX")


def x__needs_of__mutmut_11(job_spec: dict[str, Any]) -> list[str]:
    """Normalise a job's ``needs:`` (scalar or sequence) to a list of strings."""
    if "needs" not in job_spec:
        return []
    needs = job_spec["needs"]
    if isinstance(needs, str):
        return [needs]
    if isinstance(needs, list) and all(isinstance(node, str) for node in needs):
        return needs
    raise ValueError("JOB NEEDS MUST BE A JOB ID OR A LIST OF JOB IDS")

mutants_x__needs_of__mutmut['_mutmut_orig'] = x__needs_of__mutmut_orig # type: ignore # mutmut generated
mutants_x__needs_of__mutmut['x__needs_of__mutmut_1'] = x__needs_of__mutmut_1 # type: ignore # mutmut generated
mutants_x__needs_of__mutmut['x__needs_of__mutmut_2'] = x__needs_of__mutmut_2 # type: ignore # mutmut generated
mutants_x__needs_of__mutmut['x__needs_of__mutmut_3'] = x__needs_of__mutmut_3 # type: ignore # mutmut generated
mutants_x__needs_of__mutmut['x__needs_of__mutmut_4'] = x__needs_of__mutmut_4 # type: ignore # mutmut generated
mutants_x__needs_of__mutmut['x__needs_of__mutmut_5'] = x__needs_of__mutmut_5 # type: ignore # mutmut generated
mutants_x__needs_of__mutmut['x__needs_of__mutmut_6'] = x__needs_of__mutmut_6 # type: ignore # mutmut generated
mutants_x__needs_of__mutmut['x__needs_of__mutmut_7'] = x__needs_of__mutmut_7 # type: ignore # mutmut generated
mutants_x__needs_of__mutmut['x__needs_of__mutmut_8'] = x__needs_of__mutmut_8 # type: ignore # mutmut generated
mutants_x__needs_of__mutmut['x__needs_of__mutmut_9'] = x__needs_of__mutmut_9 # type: ignore # mutmut generated
mutants_x__needs_of__mutmut['x__needs_of__mutmut_10'] = x__needs_of__mutmut_10 # type: ignore # mutmut generated
mutants_x__needs_of__mutmut['x__needs_of__mutmut_11'] = x__needs_of__mutmut_11 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__validate_jobs__mutmut)
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


def x__validate_jobs__mutmut_orig(jobs: dict[str, Any]) -> None:
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


def x__validate_jobs__mutmut_1(jobs: dict[str, Any]) -> None:
    """Reject job definitions and dependency graphs that cannot be verified."""
    graph: dict[str, list[str]] = None
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


def x__validate_jobs__mutmut_2(jobs: dict[str, Any]) -> None:
    """Reject job definitions and dependency graphs that cannot be verified."""
    graph: dict[str, list[str]] = {}
    for job_id, job_spec in jobs.items():
        if not isinstance(job_id, str) or not job_id and not isinstance(job_spec, dict):
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


def x__validate_jobs__mutmut_3(jobs: dict[str, Any]) -> None:
    """Reject job definitions and dependency graphs that cannot be verified."""
    graph: dict[str, list[str]] = {}
    for job_id, job_spec in jobs.items():
        if not isinstance(job_id, str) and not job_id or not isinstance(job_spec, dict):
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


def x__validate_jobs__mutmut_4(jobs: dict[str, Any]) -> None:
    """Reject job definitions and dependency graphs that cannot be verified."""
    graph: dict[str, list[str]] = {}
    for job_id, job_spec in jobs.items():
        if isinstance(job_id, str) or not job_id or not isinstance(job_spec, dict):
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


def x__validate_jobs__mutmut_5(jobs: dict[str, Any]) -> None:
    """Reject job definitions and dependency graphs that cannot be verified."""
    graph: dict[str, list[str]] = {}
    for job_id, job_spec in jobs.items():
        if not isinstance(job_id, str) or job_id or not isinstance(job_spec, dict):
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


def x__validate_jobs__mutmut_6(jobs: dict[str, Any]) -> None:
    """Reject job definitions and dependency graphs that cannot be verified."""
    graph: dict[str, list[str]] = {}
    for job_id, job_spec in jobs.items():
        if not isinstance(job_id, str) or not job_id or isinstance(job_spec, dict):
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


def x__validate_jobs__mutmut_7(jobs: dict[str, Any]) -> None:
    """Reject job definitions and dependency graphs that cannot be verified."""
    graph: dict[str, list[str]] = {}
    for job_id, job_spec in jobs.items():
        if not isinstance(job_id, str) or not job_id or not isinstance(job_spec, dict):
            raise ValueError(None)
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


def x__validate_jobs__mutmut_8(jobs: dict[str, Any]) -> None:
    """Reject job definitions and dependency graphs that cannot be verified."""
    graph: dict[str, list[str]] = {}
    for job_id, job_spec in jobs.items():
        if not isinstance(job_id, str) or not job_id or not isinstance(job_spec, dict):
            raise ValueError("XXevery workflow job must have an id and mapping definitionXX")
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


def x__validate_jobs__mutmut_9(jobs: dict[str, Any]) -> None:
    """Reject job definitions and dependency graphs that cannot be verified."""
    graph: dict[str, list[str]] = {}
    for job_id, job_spec in jobs.items():
        if not isinstance(job_id, str) or not job_id or not isinstance(job_spec, dict):
            raise ValueError("EVERY WORKFLOW JOB MUST HAVE AN ID AND MAPPING DEFINITION")
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


def x__validate_jobs__mutmut_10(jobs: dict[str, Any]) -> None:
    """Reject job definitions and dependency graphs that cannot be verified."""
    graph: dict[str, list[str]] = {}
    for job_id, job_spec in jobs.items():
        if not isinstance(job_id, str) or not job_id or not isinstance(job_spec, dict):
            raise ValueError("every workflow job must have an id and mapping definition")
        dependencies = None
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


def x__validate_jobs__mutmut_11(jobs: dict[str, Any]) -> None:
    """Reject job definitions and dependency graphs that cannot be verified."""
    graph: dict[str, list[str]] = {}
    for job_id, job_spec in jobs.items():
        if not isinstance(job_id, str) or not job_id or not isinstance(job_spec, dict):
            raise ValueError("every workflow job must have an id and mapping definition")
        dependencies = _needs_of(None)
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


def x__validate_jobs__mutmut_12(jobs: dict[str, Any]) -> None:
    """Reject job definitions and dependency graphs that cannot be verified."""
    graph: dict[str, list[str]] = {}
    for job_id, job_spec in jobs.items():
        if not isinstance(job_id, str) or not job_id or not isinstance(job_spec, dict):
            raise ValueError("every workflow job must have an id and mapping definition")
        dependencies = _needs_of(job_spec)
        if any(None):
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


def x__validate_jobs__mutmut_13(jobs: dict[str, Any]) -> None:
    """Reject job definitions and dependency graphs that cannot be verified."""
    graph: dict[str, list[str]] = {}
    for job_id, job_spec in jobs.items():
        if not isinstance(job_id, str) or not job_id or not isinstance(job_spec, dict):
            raise ValueError("every workflow job must have an id and mapping definition")
        dependencies = _needs_of(job_spec)
        if any(dependency for dependency in dependencies):
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


def x__validate_jobs__mutmut_14(jobs: dict[str, Any]) -> None:
    """Reject job definitions and dependency graphs that cannot be verified."""
    graph: dict[str, list[str]] = {}
    for job_id, job_spec in jobs.items():
        if not isinstance(job_id, str) or not job_id or not isinstance(job_spec, dict):
            raise ValueError("every workflow job must have an id and mapping definition")
        dependencies = _needs_of(job_spec)
        if any(not dependency for dependency in dependencies):
            raise ValueError(None)
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


def x__validate_jobs__mutmut_15(jobs: dict[str, Any]) -> None:
    """Reject job definitions and dependency graphs that cannot be verified."""
    graph: dict[str, list[str]] = {}
    for job_id, job_spec in jobs.items():
        if not isinstance(job_id, str) or not job_id or not isinstance(job_spec, dict):
            raise ValueError("every workflow job must have an id and mapping definition")
        dependencies = _needs_of(job_spec)
        if any(not dependency for dependency in dependencies):
            raise ValueError("XXjob needs cannot contain an empty job idXX")
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


def x__validate_jobs__mutmut_16(jobs: dict[str, Any]) -> None:
    """Reject job definitions and dependency graphs that cannot be verified."""
    graph: dict[str, list[str]] = {}
    for job_id, job_spec in jobs.items():
        if not isinstance(job_id, str) or not job_id or not isinstance(job_spec, dict):
            raise ValueError("every workflow job must have an id and mapping definition")
        dependencies = _needs_of(job_spec)
        if any(not dependency for dependency in dependencies):
            raise ValueError("JOB NEEDS CANNOT CONTAIN AN EMPTY JOB ID")
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


def x__validate_jobs__mutmut_17(jobs: dict[str, Any]) -> None:
    """Reject job definitions and dependency graphs that cannot be verified."""
    graph: dict[str, list[str]] = {}
    for job_id, job_spec in jobs.items():
        if not isinstance(job_id, str) or not job_id or not isinstance(job_spec, dict):
            raise ValueError("every workflow job must have an id and mapping definition")
        dependencies = _needs_of(job_spec)
        if any(not dependency for dependency in dependencies):
            raise ValueError("job needs cannot contain an empty job id")
        if any(None):
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


def x__validate_jobs__mutmut_18(jobs: dict[str, Any]) -> None:
    """Reject job definitions and dependency graphs that cannot be verified."""
    graph: dict[str, list[str]] = {}
    for job_id, job_spec in jobs.items():
        if not isinstance(job_id, str) or not job_id or not isinstance(job_spec, dict):
            raise ValueError("every workflow job must have an id and mapping definition")
        dependencies = _needs_of(job_spec)
        if any(not dependency for dependency in dependencies):
            raise ValueError("job needs cannot contain an empty job id")
        if any(dependency in jobs for dependency in dependencies):
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


def x__validate_jobs__mutmut_19(jobs: dict[str, Any]) -> None:
    """Reject job definitions and dependency graphs that cannot be verified."""
    graph: dict[str, list[str]] = {}
    for job_id, job_spec in jobs.items():
        if not isinstance(job_id, str) or not job_id or not isinstance(job_spec, dict):
            raise ValueError("every workflow job must have an id and mapping definition")
        dependencies = _needs_of(job_spec)
        if any(not dependency for dependency in dependencies):
            raise ValueError("job needs cannot contain an empty job id")
        if any(dependency not in jobs for dependency in dependencies):
            raise ValueError(None)
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


def x__validate_jobs__mutmut_20(jobs: dict[str, Any]) -> None:
    """Reject job definitions and dependency graphs that cannot be verified."""
    graph: dict[str, list[str]] = {}
    for job_id, job_spec in jobs.items():
        if not isinstance(job_id, str) or not job_id or not isinstance(job_spec, dict):
            raise ValueError("every workflow job must have an id and mapping definition")
        dependencies = _needs_of(job_spec)
        if any(not dependency for dependency in dependencies):
            raise ValueError("job needs cannot contain an empty job id")
        if any(dependency not in jobs for dependency in dependencies):
            raise ValueError("XXjob needs references an undefined jobXX")
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


def x__validate_jobs__mutmut_21(jobs: dict[str, Any]) -> None:
    """Reject job definitions and dependency graphs that cannot be verified."""
    graph: dict[str, list[str]] = {}
    for job_id, job_spec in jobs.items():
        if not isinstance(job_id, str) or not job_id or not isinstance(job_spec, dict):
            raise ValueError("every workflow job must have an id and mapping definition")
        dependencies = _needs_of(job_spec)
        if any(not dependency for dependency in dependencies):
            raise ValueError("job needs cannot contain an empty job id")
        if any(dependency not in jobs for dependency in dependencies):
            raise ValueError("JOB NEEDS REFERENCES AN UNDEFINED JOB")
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


def x__validate_jobs__mutmut_22(jobs: dict[str, Any]) -> None:
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
        graph[job_id] = None

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


def x__validate_jobs__mutmut_23(jobs: dict[str, Any]) -> None:
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

    state: dict[str, int] = None
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


def x__validate_jobs__mutmut_24(jobs: dict[str, Any]) -> None:
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
        pending: list[tuple[str, bool]] = None
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


def x__validate_jobs__mutmut_25(jobs: dict[str, Any]) -> None:
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
        pending: list[tuple[str, bool]] = [(job_id, True)]
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


def x__validate_jobs__mutmut_26(jobs: dict[str, Any]) -> None:
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
            node, leaving = None
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


def x__validate_jobs__mutmut_27(jobs: dict[str, Any]) -> None:
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
                state[node] = None
                continue
            status = state.get(node, 0)
            if status == 1:
                raise ValueError("workflow job dependencies contain a cycle")
            if status == 2:
                continue
            state[node] = 1
            pending.append((node, True))
            pending.extend((dependency, False) for dependency in graph[node])


def x__validate_jobs__mutmut_28(jobs: dict[str, Any]) -> None:
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
                state[node] = 3
                continue
            status = state.get(node, 0)
            if status == 1:
                raise ValueError("workflow job dependencies contain a cycle")
            if status == 2:
                continue
            state[node] = 1
            pending.append((node, True))
            pending.extend((dependency, False) for dependency in graph[node])


def x__validate_jobs__mutmut_29(jobs: dict[str, Any]) -> None:
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
                break
            status = state.get(node, 0)
            if status == 1:
                raise ValueError("workflow job dependencies contain a cycle")
            if status == 2:
                continue
            state[node] = 1
            pending.append((node, True))
            pending.extend((dependency, False) for dependency in graph[node])


def x__validate_jobs__mutmut_30(jobs: dict[str, Any]) -> None:
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
            status = None
            if status == 1:
                raise ValueError("workflow job dependencies contain a cycle")
            if status == 2:
                continue
            state[node] = 1
            pending.append((node, True))
            pending.extend((dependency, False) for dependency in graph[node])


def x__validate_jobs__mutmut_31(jobs: dict[str, Any]) -> None:
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
            status = state.get(None, 0)
            if status == 1:
                raise ValueError("workflow job dependencies contain a cycle")
            if status == 2:
                continue
            state[node] = 1
            pending.append((node, True))
            pending.extend((dependency, False) for dependency in graph[node])


def x__validate_jobs__mutmut_32(jobs: dict[str, Any]) -> None:
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
            status = state.get(node, None)
            if status == 1:
                raise ValueError("workflow job dependencies contain a cycle")
            if status == 2:
                continue
            state[node] = 1
            pending.append((node, True))
            pending.extend((dependency, False) for dependency in graph[node])


def x__validate_jobs__mutmut_33(jobs: dict[str, Any]) -> None:
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
            status = state.get(0)
            if status == 1:
                raise ValueError("workflow job dependencies contain a cycle")
            if status == 2:
                continue
            state[node] = 1
            pending.append((node, True))
            pending.extend((dependency, False) for dependency in graph[node])


def x__validate_jobs__mutmut_34(jobs: dict[str, Any]) -> None:
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
            status = state.get(node, )
            if status == 1:
                raise ValueError("workflow job dependencies contain a cycle")
            if status == 2:
                continue
            state[node] = 1
            pending.append((node, True))
            pending.extend((dependency, False) for dependency in graph[node])


def x__validate_jobs__mutmut_35(jobs: dict[str, Any]) -> None:
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
            status = state.get(node, 1)
            if status == 1:
                raise ValueError("workflow job dependencies contain a cycle")
            if status == 2:
                continue
            state[node] = 1
            pending.append((node, True))
            pending.extend((dependency, False) for dependency in graph[node])


def x__validate_jobs__mutmut_36(jobs: dict[str, Any]) -> None:
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
            if status != 1:
                raise ValueError("workflow job dependencies contain a cycle")
            if status == 2:
                continue
            state[node] = 1
            pending.append((node, True))
            pending.extend((dependency, False) for dependency in graph[node])


def x__validate_jobs__mutmut_37(jobs: dict[str, Any]) -> None:
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
            if status == 2:
                raise ValueError("workflow job dependencies contain a cycle")
            if status == 2:
                continue
            state[node] = 1
            pending.append((node, True))
            pending.extend((dependency, False) for dependency in graph[node])


def x__validate_jobs__mutmut_38(jobs: dict[str, Any]) -> None:
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
                raise ValueError(None)
            if status == 2:
                continue
            state[node] = 1
            pending.append((node, True))
            pending.extend((dependency, False) for dependency in graph[node])


def x__validate_jobs__mutmut_39(jobs: dict[str, Any]) -> None:
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
                raise ValueError("XXworkflow job dependencies contain a cycleXX")
            if status == 2:
                continue
            state[node] = 1
            pending.append((node, True))
            pending.extend((dependency, False) for dependency in graph[node])


def x__validate_jobs__mutmut_40(jobs: dict[str, Any]) -> None:
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
                raise ValueError("WORKFLOW JOB DEPENDENCIES CONTAIN A CYCLE")
            if status == 2:
                continue
            state[node] = 1
            pending.append((node, True))
            pending.extend((dependency, False) for dependency in graph[node])


def x__validate_jobs__mutmut_41(jobs: dict[str, Any]) -> None:
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
            if status != 2:
                continue
            state[node] = 1
            pending.append((node, True))
            pending.extend((dependency, False) for dependency in graph[node])


def x__validate_jobs__mutmut_42(jobs: dict[str, Any]) -> None:
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
            if status == 3:
                continue
            state[node] = 1
            pending.append((node, True))
            pending.extend((dependency, False) for dependency in graph[node])


def x__validate_jobs__mutmut_43(jobs: dict[str, Any]) -> None:
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
                break
            state[node] = 1
            pending.append((node, True))
            pending.extend((dependency, False) for dependency in graph[node])


def x__validate_jobs__mutmut_44(jobs: dict[str, Any]) -> None:
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
            state[node] = None
            pending.append((node, True))
            pending.extend((dependency, False) for dependency in graph[node])


def x__validate_jobs__mutmut_45(jobs: dict[str, Any]) -> None:
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
            state[node] = 2
            pending.append((node, True))
            pending.extend((dependency, False) for dependency in graph[node])


def x__validate_jobs__mutmut_46(jobs: dict[str, Any]) -> None:
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
            pending.append(None)
            pending.extend((dependency, False) for dependency in graph[node])


def x__validate_jobs__mutmut_47(jobs: dict[str, Any]) -> None:
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
            pending.append((node, False))
            pending.extend((dependency, False) for dependency in graph[node])


def x__validate_jobs__mutmut_48(jobs: dict[str, Any]) -> None:
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
            pending.extend(None)


def x__validate_jobs__mutmut_49(jobs: dict[str, Any]) -> None:
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
            pending.extend((dependency, True) for dependency in graph[node])

mutants_x__validate_jobs__mutmut['_mutmut_orig'] = x__validate_jobs__mutmut_orig # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_1'] = x__validate_jobs__mutmut_1 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_2'] = x__validate_jobs__mutmut_2 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_3'] = x__validate_jobs__mutmut_3 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_4'] = x__validate_jobs__mutmut_4 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_5'] = x__validate_jobs__mutmut_5 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_6'] = x__validate_jobs__mutmut_6 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_7'] = x__validate_jobs__mutmut_7 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_8'] = x__validate_jobs__mutmut_8 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_9'] = x__validate_jobs__mutmut_9 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_10'] = x__validate_jobs__mutmut_10 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_11'] = x__validate_jobs__mutmut_11 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_12'] = x__validate_jobs__mutmut_12 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_13'] = x__validate_jobs__mutmut_13 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_14'] = x__validate_jobs__mutmut_14 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_15'] = x__validate_jobs__mutmut_15 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_16'] = x__validate_jobs__mutmut_16 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_17'] = x__validate_jobs__mutmut_17 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_18'] = x__validate_jobs__mutmut_18 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_19'] = x__validate_jobs__mutmut_19 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_20'] = x__validate_jobs__mutmut_20 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_21'] = x__validate_jobs__mutmut_21 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_22'] = x__validate_jobs__mutmut_22 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_23'] = x__validate_jobs__mutmut_23 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_24'] = x__validate_jobs__mutmut_24 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_25'] = x__validate_jobs__mutmut_25 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_26'] = x__validate_jobs__mutmut_26 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_27'] = x__validate_jobs__mutmut_27 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_28'] = x__validate_jobs__mutmut_28 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_29'] = x__validate_jobs__mutmut_29 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_30'] = x__validate_jobs__mutmut_30 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_31'] = x__validate_jobs__mutmut_31 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_32'] = x__validate_jobs__mutmut_32 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_33'] = x__validate_jobs__mutmut_33 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_34'] = x__validate_jobs__mutmut_34 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_35'] = x__validate_jobs__mutmut_35 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_36'] = x__validate_jobs__mutmut_36 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_37'] = x__validate_jobs__mutmut_37 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_38'] = x__validate_jobs__mutmut_38 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_39'] = x__validate_jobs__mutmut_39 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_40'] = x__validate_jobs__mutmut_40 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_41'] = x__validate_jobs__mutmut_41 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_42'] = x__validate_jobs__mutmut_42 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_43'] = x__validate_jobs__mutmut_43 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_44'] = x__validate_jobs__mutmut_44 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_45'] = x__validate_jobs__mutmut_45 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_46'] = x__validate_jobs__mutmut_46 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_47'] = x__validate_jobs__mutmut_47 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_48'] = x__validate_jobs__mutmut_48 # type: ignore # mutmut generated
mutants_x__validate_jobs__mutmut['x__validate_jobs__mutmut_49'] = x__validate_jobs__mutmut_49 # type: ignore # mutmut generated
mutants_x__find_aggregator__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__find_aggregator__mutmut)
def _find_aggregator(jobs: dict[str, Any], aggregator_name: str) -> str | None:
    """Return the job id whose ``name:`` is ``aggregator_name``, else None."""
    matches: list[str] = []
    for job_id, spec in jobs.items():
        if spec.get("name") == aggregator_name:
            matches.append(job_id)
    return matches[0] if len(matches) == 1 else None


def x__find_aggregator__mutmut_orig(jobs: dict[str, Any], aggregator_name: str) -> str | None:
    """Return the job id whose ``name:`` is ``aggregator_name``, else None."""
    matches: list[str] = []
    for job_id, spec in jobs.items():
        if spec.get("name") == aggregator_name:
            matches.append(job_id)
    return matches[0] if len(matches) == 1 else None


def x__find_aggregator__mutmut_1(jobs: dict[str, Any], aggregator_name: str) -> str | None:
    """Return the job id whose ``name:`` is ``aggregator_name``, else None."""
    matches: list[str] = None
    for job_id, spec in jobs.items():
        if spec.get("name") == aggregator_name:
            matches.append(job_id)
    return matches[0] if len(matches) == 1 else None


def x__find_aggregator__mutmut_2(jobs: dict[str, Any], aggregator_name: str) -> str | None:
    """Return the job id whose ``name:`` is ``aggregator_name``, else None."""
    matches: list[str] = []
    for job_id, spec in jobs.items():
        if spec.get(None) == aggregator_name:
            matches.append(job_id)
    return matches[0] if len(matches) == 1 else None


def x__find_aggregator__mutmut_3(jobs: dict[str, Any], aggregator_name: str) -> str | None:
    """Return the job id whose ``name:`` is ``aggregator_name``, else None."""
    matches: list[str] = []
    for job_id, spec in jobs.items():
        if spec.get("XXnameXX") == aggregator_name:
            matches.append(job_id)
    return matches[0] if len(matches) == 1 else None


def x__find_aggregator__mutmut_4(jobs: dict[str, Any], aggregator_name: str) -> str | None:
    """Return the job id whose ``name:`` is ``aggregator_name``, else None."""
    matches: list[str] = []
    for job_id, spec in jobs.items():
        if spec.get("NAME") == aggregator_name:
            matches.append(job_id)
    return matches[0] if len(matches) == 1 else None


def x__find_aggregator__mutmut_5(jobs: dict[str, Any], aggregator_name: str) -> str | None:
    """Return the job id whose ``name:`` is ``aggregator_name``, else None."""
    matches: list[str] = []
    for job_id, spec in jobs.items():
        if spec.get("name") != aggregator_name:
            matches.append(job_id)
    return matches[0] if len(matches) == 1 else None


def x__find_aggregator__mutmut_6(jobs: dict[str, Any], aggregator_name: str) -> str | None:
    """Return the job id whose ``name:`` is ``aggregator_name``, else None."""
    matches: list[str] = []
    for job_id, spec in jobs.items():
        if spec.get("name") == aggregator_name:
            matches.append(None)
    return matches[0] if len(matches) == 1 else None


def x__find_aggregator__mutmut_7(jobs: dict[str, Any], aggregator_name: str) -> str | None:
    """Return the job id whose ``name:`` is ``aggregator_name``, else None."""
    matches: list[str] = []
    for job_id, spec in jobs.items():
        if spec.get("name") == aggregator_name:
            matches.append(job_id)
    return matches[1] if len(matches) == 1 else None


def x__find_aggregator__mutmut_8(jobs: dict[str, Any], aggregator_name: str) -> str | None:
    """Return the job id whose ``name:`` is ``aggregator_name``, else None."""
    matches: list[str] = []
    for job_id, spec in jobs.items():
        if spec.get("name") == aggregator_name:
            matches.append(job_id)
    return matches[0] if len(matches) != 1 else None


def x__find_aggregator__mutmut_9(jobs: dict[str, Any], aggregator_name: str) -> str | None:
    """Return the job id whose ``name:`` is ``aggregator_name``, else None."""
    matches: list[str] = []
    for job_id, spec in jobs.items():
        if spec.get("name") == aggregator_name:
            matches.append(job_id)
    return matches[0] if len(matches) == 2 else None

mutants_x__find_aggregator__mutmut['_mutmut_orig'] = x__find_aggregator__mutmut_orig # type: ignore # mutmut generated
mutants_x__find_aggregator__mutmut['x__find_aggregator__mutmut_1'] = x__find_aggregator__mutmut_1 # type: ignore # mutmut generated
mutants_x__find_aggregator__mutmut['x__find_aggregator__mutmut_2'] = x__find_aggregator__mutmut_2 # type: ignore # mutmut generated
mutants_x__find_aggregator__mutmut['x__find_aggregator__mutmut_3'] = x__find_aggregator__mutmut_3 # type: ignore # mutmut generated
mutants_x__find_aggregator__mutmut['x__find_aggregator__mutmut_4'] = x__find_aggregator__mutmut_4 # type: ignore # mutmut generated
mutants_x__find_aggregator__mutmut['x__find_aggregator__mutmut_5'] = x__find_aggregator__mutmut_5 # type: ignore # mutmut generated
mutants_x__find_aggregator__mutmut['x__find_aggregator__mutmut_6'] = x__find_aggregator__mutmut_6 # type: ignore # mutmut generated
mutants_x__find_aggregator__mutmut['x__find_aggregator__mutmut_7'] = x__find_aggregator__mutmut_7 # type: ignore # mutmut generated
mutants_x__find_aggregator__mutmut['x__find_aggregator__mutmut_8'] = x__find_aggregator__mutmut_8 # type: ignore # mutmut generated
mutants_x__find_aggregator__mutmut['x__find_aggregator__mutmut_9'] = x__find_aggregator__mutmut_9 # type: ignore # mutmut generated
mutants_x__closure__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__closure__mutmut)
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


def x__closure__mutmut_orig(jobs: dict[str, Any], root: str) -> set[str]:
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


def x__closure__mutmut_1(jobs: dict[str, Any], root: str) -> set[str]:
    """Transitive ``needs:`` closure rooted at ``root`` (root excluded)."""
    seen: set[str] = None
    frontier = list(_needs_of(jobs[root]))
    while frontier:
        node = frontier.pop()
        if node in seen:
            continue
        seen.add(node)
        frontier.extend(_needs_of(jobs[node]))
    return seen


def x__closure__mutmut_2(jobs: dict[str, Any], root: str) -> set[str]:
    """Transitive ``needs:`` closure rooted at ``root`` (root excluded)."""
    seen: set[str] = set()
    frontier = None
    while frontier:
        node = frontier.pop()
        if node in seen:
            continue
        seen.add(node)
        frontier.extend(_needs_of(jobs[node]))
    return seen


def x__closure__mutmut_3(jobs: dict[str, Any], root: str) -> set[str]:
    """Transitive ``needs:`` closure rooted at ``root`` (root excluded)."""
    seen: set[str] = set()
    frontier = list(None)
    while frontier:
        node = frontier.pop()
        if node in seen:
            continue
        seen.add(node)
        frontier.extend(_needs_of(jobs[node]))
    return seen


def x__closure__mutmut_4(jobs: dict[str, Any], root: str) -> set[str]:
    """Transitive ``needs:`` closure rooted at ``root`` (root excluded)."""
    seen: set[str] = set()
    frontier = list(_needs_of(None))
    while frontier:
        node = frontier.pop()
        if node in seen:
            continue
        seen.add(node)
        frontier.extend(_needs_of(jobs[node]))
    return seen


def x__closure__mutmut_5(jobs: dict[str, Any], root: str) -> set[str]:
    """Transitive ``needs:`` closure rooted at ``root`` (root excluded)."""
    seen: set[str] = set()
    frontier = list(_needs_of(jobs[root]))
    while frontier:
        node = None
        if node in seen:
            continue
        seen.add(node)
        frontier.extend(_needs_of(jobs[node]))
    return seen


def x__closure__mutmut_6(jobs: dict[str, Any], root: str) -> set[str]:
    """Transitive ``needs:`` closure rooted at ``root`` (root excluded)."""
    seen: set[str] = set()
    frontier = list(_needs_of(jobs[root]))
    while frontier:
        node = frontier.pop()
        if node not in seen:
            continue
        seen.add(node)
        frontier.extend(_needs_of(jobs[node]))
    return seen


def x__closure__mutmut_7(jobs: dict[str, Any], root: str) -> set[str]:
    """Transitive ``needs:`` closure rooted at ``root`` (root excluded)."""
    seen: set[str] = set()
    frontier = list(_needs_of(jobs[root]))
    while frontier:
        node = frontier.pop()
        if node in seen:
            break
        seen.add(node)
        frontier.extend(_needs_of(jobs[node]))
    return seen


def x__closure__mutmut_8(jobs: dict[str, Any], root: str) -> set[str]:
    """Transitive ``needs:`` closure rooted at ``root`` (root excluded)."""
    seen: set[str] = set()
    frontier = list(_needs_of(jobs[root]))
    while frontier:
        node = frontier.pop()
        if node in seen:
            continue
        seen.add(None)
        frontier.extend(_needs_of(jobs[node]))
    return seen


def x__closure__mutmut_9(jobs: dict[str, Any], root: str) -> set[str]:
    """Transitive ``needs:`` closure rooted at ``root`` (root excluded)."""
    seen: set[str] = set()
    frontier = list(_needs_of(jobs[root]))
    while frontier:
        node = frontier.pop()
        if node in seen:
            continue
        seen.add(node)
        frontier.extend(None)
    return seen


def x__closure__mutmut_10(jobs: dict[str, Any], root: str) -> set[str]:
    """Transitive ``needs:`` closure rooted at ``root`` (root excluded)."""
    seen: set[str] = set()
    frontier = list(_needs_of(jobs[root]))
    while frontier:
        node = frontier.pop()
        if node in seen:
            continue
        seen.add(node)
        frontier.extend(_needs_of(None))
    return seen

mutants_x__closure__mutmut['_mutmut_orig'] = x__closure__mutmut_orig # type: ignore # mutmut generated
mutants_x__closure__mutmut['x__closure__mutmut_1'] = x__closure__mutmut_1 # type: ignore # mutmut generated
mutants_x__closure__mutmut['x__closure__mutmut_2'] = x__closure__mutmut_2 # type: ignore # mutmut generated
mutants_x__closure__mutmut['x__closure__mutmut_3'] = x__closure__mutmut_3 # type: ignore # mutmut generated
mutants_x__closure__mutmut['x__closure__mutmut_4'] = x__closure__mutmut_4 # type: ignore # mutmut generated
mutants_x__closure__mutmut['x__closure__mutmut_5'] = x__closure__mutmut_5 # type: ignore # mutmut generated
mutants_x__closure__mutmut['x__closure__mutmut_6'] = x__closure__mutmut_6 # type: ignore # mutmut generated
mutants_x__closure__mutmut['x__closure__mutmut_7'] = x__closure__mutmut_7 # type: ignore # mutmut generated
mutants_x__closure__mutmut['x__closure__mutmut_8'] = x__closure__mutmut_8 # type: ignore # mutmut generated
mutants_x__closure__mutmut['x__closure__mutmut_9'] = x__closure__mutmut_9 # type: ignore # mutmut generated
mutants_x__closure__mutmut['x__closure__mutmut_10'] = x__closure__mutmut_10 # type: ignore # mutmut generated
mutants_x_workflow_fanin_is_dishonest__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_workflow_fanin_is_dishonest__mutmut)
def workflow_fanin_is_dishonest(
    path: Path,
    *,
    aggregator_name: str,
) -> bool:
    """True iff the workflow at ``path`` has a dangling job.

    Pure helper (the detection core) so tests can assert on it directly. Returns
    True when the aggregator is missing entirely, or when any non-aggregator job
    is not in the aggregator's needs-closure. An
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
    for job_id in jobs:
        if job_id == aggregator or job_id in gated:
            continue
        return True
    return False


def x_workflow_fanin_is_dishonest__mutmut_orig(
    path: Path,
    *,
    aggregator_name: str,
) -> bool:
    """True iff the workflow at ``path`` has a dangling job.

    Pure helper (the detection core) so tests can assert on it directly. Returns
    True when the aggregator is missing entirely, or when any non-aggregator job
    is not in the aggregator's needs-closure. An
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
    for job_id in jobs:
        if job_id == aggregator or job_id in gated:
            continue
        return True
    return False


def x_workflow_fanin_is_dishonest__mutmut_1(
    path: Path,
    *,
    aggregator_name: str,
) -> bool:
    """True iff the workflow at ``path`` has a dangling job.

    Pure helper (the detection core) so tests can assert on it directly. Returns
    True when the aggregator is missing entirely, or when any non-aggregator job
    is not in the aggregator's needs-closure. An
    unreadable, malformed, or otherwise unverifiable configured workflow
    returns True so the gate cannot pass without validating its input.
    """
    try:
        text = None
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
    for job_id in jobs:
        if job_id == aggregator or job_id in gated:
            continue
        return True
    return False


def x_workflow_fanin_is_dishonest__mutmut_2(
    path: Path,
    *,
    aggregator_name: str,
) -> bool:
    """True iff the workflow at ``path`` has a dangling job.

    Pure helper (the detection core) so tests can assert on it directly. Returns
    True when the aggregator is missing entirely, or when any non-aggregator job
    is not in the aggregator's needs-closure. An
    unreadable, malformed, or otherwise unverifiable configured workflow
    returns True so the gate cannot pass without validating its input.
    """
    try:
        text = path.read_text(encoding=None)
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
    for job_id in jobs:
        if job_id == aggregator or job_id in gated:
            continue
        return True
    return False


def x_workflow_fanin_is_dishonest__mutmut_3(
    path: Path,
    *,
    aggregator_name: str,
) -> bool:
    """True iff the workflow at ``path`` has a dangling job.

    Pure helper (the detection core) so tests can assert on it directly. Returns
    True when the aggregator is missing entirely, or when any non-aggregator job
    is not in the aggregator's needs-closure. An
    unreadable, malformed, or otherwise unverifiable configured workflow
    returns True so the gate cannot pass without validating its input.
    """
    try:
        text = path.read_text(encoding="XXutf-8XX")
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
    for job_id in jobs:
        if job_id == aggregator or job_id in gated:
            continue
        return True
    return False


def x_workflow_fanin_is_dishonest__mutmut_4(
    path: Path,
    *,
    aggregator_name: str,
) -> bool:
    """True iff the workflow at ``path`` has a dangling job.

    Pure helper (the detection core) so tests can assert on it directly. Returns
    True when the aggregator is missing entirely, or when any non-aggregator job
    is not in the aggregator's needs-closure. An
    unreadable, malformed, or otherwise unverifiable configured workflow
    returns True so the gate cannot pass without validating its input.
    """
    try:
        text = path.read_text(encoding="UTF-8")
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
    for job_id in jobs:
        if job_id == aggregator or job_id in gated:
            continue
        return True
    return False


def x_workflow_fanin_is_dishonest__mutmut_5(
    path: Path,
    *,
    aggregator_name: str,
) -> bool:
    """True iff the workflow at ``path`` has a dangling job.

    Pure helper (the detection core) so tests can assert on it directly. Returns
    True when the aggregator is missing entirely, or when any non-aggregator job
    is not in the aggregator's needs-closure. An
    unreadable, malformed, or otherwise unverifiable configured workflow
    returns True so the gate cannot pass without validating its input.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    try:
        jobs = _load_jobs(text)
        _validate_jobs(jobs)
    except ValueError:
        return True
    aggregator = _find_aggregator(jobs, aggregator_name)
    if aggregator is None:
        return True
    gated = _closure(jobs, aggregator)
    for job_id in jobs:
        if job_id == aggregator or job_id in gated:
            continue
        return True
    return False


def x_workflow_fanin_is_dishonest__mutmut_6(
    path: Path,
    *,
    aggregator_name: str,
) -> bool:
    """True iff the workflow at ``path`` has a dangling job.

    Pure helper (the detection core) so tests can assert on it directly. Returns
    True when the aggregator is missing entirely, or when any non-aggregator job
    is not in the aggregator's needs-closure. An
    unreadable, malformed, or otherwise unverifiable configured workflow
    returns True so the gate cannot pass without validating its input.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return True
    try:
        jobs = None
        _validate_jobs(jobs)
    except ValueError:
        return True
    aggregator = _find_aggregator(jobs, aggregator_name)
    if aggregator is None:
        return True
    gated = _closure(jobs, aggregator)
    for job_id in jobs:
        if job_id == aggregator or job_id in gated:
            continue
        return True
    return False


def x_workflow_fanin_is_dishonest__mutmut_7(
    path: Path,
    *,
    aggregator_name: str,
) -> bool:
    """True iff the workflow at ``path`` has a dangling job.

    Pure helper (the detection core) so tests can assert on it directly. Returns
    True when the aggregator is missing entirely, or when any non-aggregator job
    is not in the aggregator's needs-closure. An
    unreadable, malformed, or otherwise unverifiable configured workflow
    returns True so the gate cannot pass without validating its input.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return True
    try:
        jobs = _load_jobs(None)
        _validate_jobs(jobs)
    except ValueError:
        return True
    aggregator = _find_aggregator(jobs, aggregator_name)
    if aggregator is None:
        return True
    gated = _closure(jobs, aggregator)
    for job_id in jobs:
        if job_id == aggregator or job_id in gated:
            continue
        return True
    return False


def x_workflow_fanin_is_dishonest__mutmut_8(
    path: Path,
    *,
    aggregator_name: str,
) -> bool:
    """True iff the workflow at ``path`` has a dangling job.

    Pure helper (the detection core) so tests can assert on it directly. Returns
    True when the aggregator is missing entirely, or when any non-aggregator job
    is not in the aggregator's needs-closure. An
    unreadable, malformed, or otherwise unverifiable configured workflow
    returns True so the gate cannot pass without validating its input.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return True
    try:
        jobs = _load_jobs(text)
        _validate_jobs(None)
    except ValueError:
        return True
    aggregator = _find_aggregator(jobs, aggregator_name)
    if aggregator is None:
        return True
    gated = _closure(jobs, aggregator)
    for job_id in jobs:
        if job_id == aggregator or job_id in gated:
            continue
        return True
    return False


def x_workflow_fanin_is_dishonest__mutmut_9(
    path: Path,
    *,
    aggregator_name: str,
) -> bool:
    """True iff the workflow at ``path`` has a dangling job.

    Pure helper (the detection core) so tests can assert on it directly. Returns
    True when the aggregator is missing entirely, or when any non-aggregator job
    is not in the aggregator's needs-closure. An
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
        return False
    aggregator = _find_aggregator(jobs, aggregator_name)
    if aggregator is None:
        return True
    gated = _closure(jobs, aggregator)
    for job_id in jobs:
        if job_id == aggregator or job_id in gated:
            continue
        return True
    return False


def x_workflow_fanin_is_dishonest__mutmut_10(
    path: Path,
    *,
    aggregator_name: str,
) -> bool:
    """True iff the workflow at ``path`` has a dangling job.

    Pure helper (the detection core) so tests can assert on it directly. Returns
    True when the aggregator is missing entirely, or when any non-aggregator job
    is not in the aggregator's needs-closure. An
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
    aggregator = None
    if aggregator is None:
        return True
    gated = _closure(jobs, aggregator)
    for job_id in jobs:
        if job_id == aggregator or job_id in gated:
            continue
        return True
    return False


def x_workflow_fanin_is_dishonest__mutmut_11(
    path: Path,
    *,
    aggregator_name: str,
) -> bool:
    """True iff the workflow at ``path`` has a dangling job.

    Pure helper (the detection core) so tests can assert on it directly. Returns
    True when the aggregator is missing entirely, or when any non-aggregator job
    is not in the aggregator's needs-closure. An
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
    aggregator = _find_aggregator(None, aggregator_name)
    if aggregator is None:
        return True
    gated = _closure(jobs, aggregator)
    for job_id in jobs:
        if job_id == aggregator or job_id in gated:
            continue
        return True
    return False


def x_workflow_fanin_is_dishonest__mutmut_12(
    path: Path,
    *,
    aggregator_name: str,
) -> bool:
    """True iff the workflow at ``path`` has a dangling job.

    Pure helper (the detection core) so tests can assert on it directly. Returns
    True when the aggregator is missing entirely, or when any non-aggregator job
    is not in the aggregator's needs-closure. An
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
    aggregator = _find_aggregator(jobs, None)
    if aggregator is None:
        return True
    gated = _closure(jobs, aggregator)
    for job_id in jobs:
        if job_id == aggregator or job_id in gated:
            continue
        return True
    return False


def x_workflow_fanin_is_dishonest__mutmut_13(
    path: Path,
    *,
    aggregator_name: str,
) -> bool:
    """True iff the workflow at ``path`` has a dangling job.

    Pure helper (the detection core) so tests can assert on it directly. Returns
    True when the aggregator is missing entirely, or when any non-aggregator job
    is not in the aggregator's needs-closure. An
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
    aggregator = _find_aggregator(aggregator_name)
    if aggregator is None:
        return True
    gated = _closure(jobs, aggregator)
    for job_id in jobs:
        if job_id == aggregator or job_id in gated:
            continue
        return True
    return False


def x_workflow_fanin_is_dishonest__mutmut_14(
    path: Path,
    *,
    aggregator_name: str,
) -> bool:
    """True iff the workflow at ``path`` has a dangling job.

    Pure helper (the detection core) so tests can assert on it directly. Returns
    True when the aggregator is missing entirely, or when any non-aggregator job
    is not in the aggregator's needs-closure. An
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
    aggregator = _find_aggregator(jobs, )
    if aggregator is None:
        return True
    gated = _closure(jobs, aggregator)
    for job_id in jobs:
        if job_id == aggregator or job_id in gated:
            continue
        return True
    return False


def x_workflow_fanin_is_dishonest__mutmut_15(
    path: Path,
    *,
    aggregator_name: str,
) -> bool:
    """True iff the workflow at ``path`` has a dangling job.

    Pure helper (the detection core) so tests can assert on it directly. Returns
    True when the aggregator is missing entirely, or when any non-aggregator job
    is not in the aggregator's needs-closure. An
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
    if aggregator is not None:
        return True
    gated = _closure(jobs, aggregator)
    for job_id in jobs:
        if job_id == aggregator or job_id in gated:
            continue
        return True
    return False


def x_workflow_fanin_is_dishonest__mutmut_16(
    path: Path,
    *,
    aggregator_name: str,
) -> bool:
    """True iff the workflow at ``path`` has a dangling job.

    Pure helper (the detection core) so tests can assert on it directly. Returns
    True when the aggregator is missing entirely, or when any non-aggregator job
    is not in the aggregator's needs-closure. An
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
        return False
    gated = _closure(jobs, aggregator)
    for job_id in jobs:
        if job_id == aggregator or job_id in gated:
            continue
        return True
    return False


def x_workflow_fanin_is_dishonest__mutmut_17(
    path: Path,
    *,
    aggregator_name: str,
) -> bool:
    """True iff the workflow at ``path`` has a dangling job.

    Pure helper (the detection core) so tests can assert on it directly. Returns
    True when the aggregator is missing entirely, or when any non-aggregator job
    is not in the aggregator's needs-closure. An
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
    gated = None
    for job_id in jobs:
        if job_id == aggregator or job_id in gated:
            continue
        return True
    return False


def x_workflow_fanin_is_dishonest__mutmut_18(
    path: Path,
    *,
    aggregator_name: str,
) -> bool:
    """True iff the workflow at ``path`` has a dangling job.

    Pure helper (the detection core) so tests can assert on it directly. Returns
    True when the aggregator is missing entirely, or when any non-aggregator job
    is not in the aggregator's needs-closure. An
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
    gated = _closure(None, aggregator)
    for job_id in jobs:
        if job_id == aggregator or job_id in gated:
            continue
        return True
    return False


def x_workflow_fanin_is_dishonest__mutmut_19(
    path: Path,
    *,
    aggregator_name: str,
) -> bool:
    """True iff the workflow at ``path`` has a dangling job.

    Pure helper (the detection core) so tests can assert on it directly. Returns
    True when the aggregator is missing entirely, or when any non-aggregator job
    is not in the aggregator's needs-closure. An
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
    gated = _closure(jobs, None)
    for job_id in jobs:
        if job_id == aggregator or job_id in gated:
            continue
        return True
    return False


def x_workflow_fanin_is_dishonest__mutmut_20(
    path: Path,
    *,
    aggregator_name: str,
) -> bool:
    """True iff the workflow at ``path`` has a dangling job.

    Pure helper (the detection core) so tests can assert on it directly. Returns
    True when the aggregator is missing entirely, or when any non-aggregator job
    is not in the aggregator's needs-closure. An
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
    gated = _closure(aggregator)
    for job_id in jobs:
        if job_id == aggregator or job_id in gated:
            continue
        return True
    return False


def x_workflow_fanin_is_dishonest__mutmut_21(
    path: Path,
    *,
    aggregator_name: str,
) -> bool:
    """True iff the workflow at ``path`` has a dangling job.

    Pure helper (the detection core) so tests can assert on it directly. Returns
    True when the aggregator is missing entirely, or when any non-aggregator job
    is not in the aggregator's needs-closure. An
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
    gated = _closure(jobs, )
    for job_id in jobs:
        if job_id == aggregator or job_id in gated:
            continue
        return True
    return False


def x_workflow_fanin_is_dishonest__mutmut_22(
    path: Path,
    *,
    aggregator_name: str,
) -> bool:
    """True iff the workflow at ``path`` has a dangling job.

    Pure helper (the detection core) so tests can assert on it directly. Returns
    True when the aggregator is missing entirely, or when any non-aggregator job
    is not in the aggregator's needs-closure. An
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
    for job_id in jobs:
        if job_id == aggregator and job_id in gated:
            continue
        return True
    return False


def x_workflow_fanin_is_dishonest__mutmut_23(
    path: Path,
    *,
    aggregator_name: str,
) -> bool:
    """True iff the workflow at ``path`` has a dangling job.

    Pure helper (the detection core) so tests can assert on it directly. Returns
    True when the aggregator is missing entirely, or when any non-aggregator job
    is not in the aggregator's needs-closure. An
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
    for job_id in jobs:
        if job_id != aggregator or job_id in gated:
            continue
        return True
    return False


def x_workflow_fanin_is_dishonest__mutmut_24(
    path: Path,
    *,
    aggregator_name: str,
) -> bool:
    """True iff the workflow at ``path`` has a dangling job.

    Pure helper (the detection core) so tests can assert on it directly. Returns
    True when the aggregator is missing entirely, or when any non-aggregator job
    is not in the aggregator's needs-closure. An
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
    for job_id in jobs:
        if job_id == aggregator or job_id not in gated:
            continue
        return True
    return False


def x_workflow_fanin_is_dishonest__mutmut_25(
    path: Path,
    *,
    aggregator_name: str,
) -> bool:
    """True iff the workflow at ``path`` has a dangling job.

    Pure helper (the detection core) so tests can assert on it directly. Returns
    True when the aggregator is missing entirely, or when any non-aggregator job
    is not in the aggregator's needs-closure. An
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
    for job_id in jobs:
        if job_id == aggregator or job_id in gated:
            break
        return True
    return False


def x_workflow_fanin_is_dishonest__mutmut_26(
    path: Path,
    *,
    aggregator_name: str,
) -> bool:
    """True iff the workflow at ``path`` has a dangling job.

    Pure helper (the detection core) so tests can assert on it directly. Returns
    True when the aggregator is missing entirely, or when any non-aggregator job
    is not in the aggregator's needs-closure. An
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
    for job_id in jobs:
        if job_id == aggregator or job_id in gated:
            continue
        return False
    return False


def x_workflow_fanin_is_dishonest__mutmut_27(
    path: Path,
    *,
    aggregator_name: str,
) -> bool:
    """True iff the workflow at ``path`` has a dangling job.

    Pure helper (the detection core) so tests can assert on it directly. Returns
    True when the aggregator is missing entirely, or when any non-aggregator job
    is not in the aggregator's needs-closure. An
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
    for job_id in jobs:
        if job_id == aggregator or job_id in gated:
            continue
        return True
    return True

mutants_x_workflow_fanin_is_dishonest__mutmut['_mutmut_orig'] = x_workflow_fanin_is_dishonest__mutmut_orig # type: ignore # mutmut generated
mutants_x_workflow_fanin_is_dishonest__mutmut['x_workflow_fanin_is_dishonest__mutmut_1'] = x_workflow_fanin_is_dishonest__mutmut_1 # type: ignore # mutmut generated
mutants_x_workflow_fanin_is_dishonest__mutmut['x_workflow_fanin_is_dishonest__mutmut_2'] = x_workflow_fanin_is_dishonest__mutmut_2 # type: ignore # mutmut generated
mutants_x_workflow_fanin_is_dishonest__mutmut['x_workflow_fanin_is_dishonest__mutmut_3'] = x_workflow_fanin_is_dishonest__mutmut_3 # type: ignore # mutmut generated
mutants_x_workflow_fanin_is_dishonest__mutmut['x_workflow_fanin_is_dishonest__mutmut_4'] = x_workflow_fanin_is_dishonest__mutmut_4 # type: ignore # mutmut generated
mutants_x_workflow_fanin_is_dishonest__mutmut['x_workflow_fanin_is_dishonest__mutmut_5'] = x_workflow_fanin_is_dishonest__mutmut_5 # type: ignore # mutmut generated
mutants_x_workflow_fanin_is_dishonest__mutmut['x_workflow_fanin_is_dishonest__mutmut_6'] = x_workflow_fanin_is_dishonest__mutmut_6 # type: ignore # mutmut generated
mutants_x_workflow_fanin_is_dishonest__mutmut['x_workflow_fanin_is_dishonest__mutmut_7'] = x_workflow_fanin_is_dishonest__mutmut_7 # type: ignore # mutmut generated
mutants_x_workflow_fanin_is_dishonest__mutmut['x_workflow_fanin_is_dishonest__mutmut_8'] = x_workflow_fanin_is_dishonest__mutmut_8 # type: ignore # mutmut generated
mutants_x_workflow_fanin_is_dishonest__mutmut['x_workflow_fanin_is_dishonest__mutmut_9'] = x_workflow_fanin_is_dishonest__mutmut_9 # type: ignore # mutmut generated
mutants_x_workflow_fanin_is_dishonest__mutmut['x_workflow_fanin_is_dishonest__mutmut_10'] = x_workflow_fanin_is_dishonest__mutmut_10 # type: ignore # mutmut generated
mutants_x_workflow_fanin_is_dishonest__mutmut['x_workflow_fanin_is_dishonest__mutmut_11'] = x_workflow_fanin_is_dishonest__mutmut_11 # type: ignore # mutmut generated
mutants_x_workflow_fanin_is_dishonest__mutmut['x_workflow_fanin_is_dishonest__mutmut_12'] = x_workflow_fanin_is_dishonest__mutmut_12 # type: ignore # mutmut generated
mutants_x_workflow_fanin_is_dishonest__mutmut['x_workflow_fanin_is_dishonest__mutmut_13'] = x_workflow_fanin_is_dishonest__mutmut_13 # type: ignore # mutmut generated
mutants_x_workflow_fanin_is_dishonest__mutmut['x_workflow_fanin_is_dishonest__mutmut_14'] = x_workflow_fanin_is_dishonest__mutmut_14 # type: ignore # mutmut generated
mutants_x_workflow_fanin_is_dishonest__mutmut['x_workflow_fanin_is_dishonest__mutmut_15'] = x_workflow_fanin_is_dishonest__mutmut_15 # type: ignore # mutmut generated
mutants_x_workflow_fanin_is_dishonest__mutmut['x_workflow_fanin_is_dishonest__mutmut_16'] = x_workflow_fanin_is_dishonest__mutmut_16 # type: ignore # mutmut generated
mutants_x_workflow_fanin_is_dishonest__mutmut['x_workflow_fanin_is_dishonest__mutmut_17'] = x_workflow_fanin_is_dishonest__mutmut_17 # type: ignore # mutmut generated
mutants_x_workflow_fanin_is_dishonest__mutmut['x_workflow_fanin_is_dishonest__mutmut_18'] = x_workflow_fanin_is_dishonest__mutmut_18 # type: ignore # mutmut generated
mutants_x_workflow_fanin_is_dishonest__mutmut['x_workflow_fanin_is_dishonest__mutmut_19'] = x_workflow_fanin_is_dishonest__mutmut_19 # type: ignore # mutmut generated
mutants_x_workflow_fanin_is_dishonest__mutmut['x_workflow_fanin_is_dishonest__mutmut_20'] = x_workflow_fanin_is_dishonest__mutmut_20 # type: ignore # mutmut generated
mutants_x_workflow_fanin_is_dishonest__mutmut['x_workflow_fanin_is_dishonest__mutmut_21'] = x_workflow_fanin_is_dishonest__mutmut_21 # type: ignore # mutmut generated
mutants_x_workflow_fanin_is_dishonest__mutmut['x_workflow_fanin_is_dishonest__mutmut_22'] = x_workflow_fanin_is_dishonest__mutmut_22 # type: ignore # mutmut generated
mutants_x_workflow_fanin_is_dishonest__mutmut['x_workflow_fanin_is_dishonest__mutmut_23'] = x_workflow_fanin_is_dishonest__mutmut_23 # type: ignore # mutmut generated
mutants_x_workflow_fanin_is_dishonest__mutmut['x_workflow_fanin_is_dishonest__mutmut_24'] = x_workflow_fanin_is_dishonest__mutmut_24 # type: ignore # mutmut generated
mutants_x_workflow_fanin_is_dishonest__mutmut['x_workflow_fanin_is_dishonest__mutmut_25'] = x_workflow_fanin_is_dishonest__mutmut_25 # type: ignore # mutmut generated
mutants_x_workflow_fanin_is_dishonest__mutmut['x_workflow_fanin_is_dishonest__mutmut_26'] = x_workflow_fanin_is_dishonest__mutmut_26 # type: ignore # mutmut generated
mutants_x_workflow_fanin_is_dishonest__mutmut['x_workflow_fanin_is_dishonest__mutmut_27'] = x_workflow_fanin_is_dishonest__mutmut_27 # type: ignore # mutmut generated
mutants_xǁCiFaninParityǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCiFaninParityǁis_in_scope__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCiFaninParityǁenumerate_files__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCiFaninParityǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore


class CiFaninParity(FitnessRule):
    """Flags a CI workflow whose gate fan-in is dishonest."""

    name = "ci-fanin-parity"
    remediation = REMEDIATION
    extensions = (".yml", ".yaml")

    workflow: str = DEFAULT_WORKFLOW
    aggregator_name: str = DEFAULT_AGGREGATOR_NAME

    @classmethod
    @_mutmut_mutated(mutants_xǁCiFaninParityǁfrom_config__mutmut, is_classmethod = True)
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
        return rule

    @classmethod
    def xǁCiFaninParityǁfrom_config__mutmut_orig(
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
        return rule

    @classmethod
    def xǁCiFaninParityǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiFaninParity:
        rule = None
        assert isinstance(rule, CiFaninParity)  # noqa: S101  # narrowing for mypy
        workflow = config.get("workflow")
        if workflow is not None:
            rule.workflow = str(workflow)
        aggregator = config.get("aggregator_name")
        if aggregator is not None:
            rule.aggregator_name = str(aggregator)
        return rule

    @classmethod
    def xǁCiFaninParityǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiFaninParity:
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, CiFaninParity)  # noqa: S101  # narrowing for mypy
        workflow = config.get("workflow")
        if workflow is not None:
            rule.workflow = str(workflow)
        aggregator = config.get("aggregator_name")
        if aggregator is not None:
            rule.aggregator_name = str(aggregator)
        return rule

    @classmethod
    def xǁCiFaninParityǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiFaninParity:
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, CiFaninParity)  # noqa: S101  # narrowing for mypy
        workflow = config.get("workflow")
        if workflow is not None:
            rule.workflow = str(workflow)
        aggregator = config.get("aggregator_name")
        if aggregator is not None:
            rule.aggregator_name = str(aggregator)
        return rule

    @classmethod
    def xǁCiFaninParityǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiFaninParity:
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, CiFaninParity)  # noqa: S101  # narrowing for mypy
        workflow = config.get("workflow")
        if workflow is not None:
            rule.workflow = str(workflow)
        aggregator = config.get("aggregator_name")
        if aggregator is not None:
            rule.aggregator_name = str(aggregator)
        return rule

    @classmethod
    def xǁCiFaninParityǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiFaninParity:
        rule = super().from_config(config, )
        assert isinstance(rule, CiFaninParity)  # noqa: S101  # narrowing for mypy
        workflow = config.get("workflow")
        if workflow is not None:
            rule.workflow = str(workflow)
        aggregator = config.get("aggregator_name")
        if aggregator is not None:
            rule.aggregator_name = str(aggregator)
        return rule

    @classmethod
    def xǁCiFaninParityǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiFaninParity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiFaninParity)  # noqa: S101  # narrowing for mypy
        workflow = None
        if workflow is not None:
            rule.workflow = str(workflow)
        aggregator = config.get("aggregator_name")
        if aggregator is not None:
            rule.aggregator_name = str(aggregator)
        return rule

    @classmethod
    def xǁCiFaninParityǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiFaninParity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiFaninParity)  # noqa: S101  # narrowing for mypy
        workflow = config.get(None)
        if workflow is not None:
            rule.workflow = str(workflow)
        aggregator = config.get("aggregator_name")
        if aggregator is not None:
            rule.aggregator_name = str(aggregator)
        return rule

    @classmethod
    def xǁCiFaninParityǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiFaninParity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiFaninParity)  # noqa: S101  # narrowing for mypy
        workflow = config.get("XXworkflowXX")
        if workflow is not None:
            rule.workflow = str(workflow)
        aggregator = config.get("aggregator_name")
        if aggregator is not None:
            rule.aggregator_name = str(aggregator)
        return rule

    @classmethod
    def xǁCiFaninParityǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiFaninParity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiFaninParity)  # noqa: S101  # narrowing for mypy
        workflow = config.get("WORKFLOW")
        if workflow is not None:
            rule.workflow = str(workflow)
        aggregator = config.get("aggregator_name")
        if aggregator is not None:
            rule.aggregator_name = str(aggregator)
        return rule

    @classmethod
    def xǁCiFaninParityǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiFaninParity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiFaninParity)  # noqa: S101  # narrowing for mypy
        workflow = config.get("workflow")
        if workflow is None:
            rule.workflow = str(workflow)
        aggregator = config.get("aggregator_name")
        if aggregator is not None:
            rule.aggregator_name = str(aggregator)
        return rule

    @classmethod
    def xǁCiFaninParityǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiFaninParity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiFaninParity)  # noqa: S101  # narrowing for mypy
        workflow = config.get("workflow")
        if workflow is not None:
            rule.workflow = None
        aggregator = config.get("aggregator_name")
        if aggregator is not None:
            rule.aggregator_name = str(aggregator)
        return rule

    @classmethod
    def xǁCiFaninParityǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiFaninParity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiFaninParity)  # noqa: S101  # narrowing for mypy
        workflow = config.get("workflow")
        if workflow is not None:
            rule.workflow = str(None)
        aggregator = config.get("aggregator_name")
        if aggregator is not None:
            rule.aggregator_name = str(aggregator)
        return rule

    @classmethod
    def xǁCiFaninParityǁfrom_config__mutmut_13(
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
        aggregator = None
        if aggregator is not None:
            rule.aggregator_name = str(aggregator)
        return rule

    @classmethod
    def xǁCiFaninParityǁfrom_config__mutmut_14(
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
        aggregator = config.get(None)
        if aggregator is not None:
            rule.aggregator_name = str(aggregator)
        return rule

    @classmethod
    def xǁCiFaninParityǁfrom_config__mutmut_15(
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
        aggregator = config.get("XXaggregator_nameXX")
        if aggregator is not None:
            rule.aggregator_name = str(aggregator)
        return rule

    @classmethod
    def xǁCiFaninParityǁfrom_config__mutmut_16(
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
        aggregator = config.get("AGGREGATOR_NAME")
        if aggregator is not None:
            rule.aggregator_name = str(aggregator)
        return rule

    @classmethod
    def xǁCiFaninParityǁfrom_config__mutmut_17(
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
        if aggregator is None:
            rule.aggregator_name = str(aggregator)
        return rule

    @classmethod
    def xǁCiFaninParityǁfrom_config__mutmut_18(
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
            rule.aggregator_name = None
        return rule

    @classmethod
    def xǁCiFaninParityǁfrom_config__mutmut_19(
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
            rule.aggregator_name = str(None)
        return rule

    @_mutmut_mutated(mutants_xǁCiFaninParityǁis_in_scope__mutmut)
    def is_in_scope(self, rel: str) -> bool:
        # Scope is the single configured workflow file.
        return True

    def xǁCiFaninParityǁis_in_scope__mutmut_orig(self, rel: str) -> bool:
        # Scope is the single configured workflow file.
        return True

    def xǁCiFaninParityǁis_in_scope__mutmut_1(self, rel: str) -> bool:
        # Scope is the single configured workflow file.
        return False

    @_mutmut_mutated(mutants_xǁCiFaninParityǁenumerate_files__mutmut)
    def enumerate_files(self) -> list[Path]:
        """Enumerate the configured workflow even when it is absent."""
        workflow_path = self._repo_root / self.workflow
        return [workflow_path]

    def xǁCiFaninParityǁenumerate_files__mutmut_orig(self) -> list[Path]:
        """Enumerate the configured workflow even when it is absent."""
        workflow_path = self._repo_root / self.workflow
        return [workflow_path]

    def xǁCiFaninParityǁenumerate_files__mutmut_1(self) -> list[Path]:
        """Enumerate the configured workflow even when it is absent."""
        workflow_path = None
        return [workflow_path]

    def xǁCiFaninParityǁenumerate_files__mutmut_2(self) -> list[Path]:
        """Enumerate the configured workflow even when it is absent."""
        workflow_path = self._repo_root * self.workflow
        return [workflow_path]

    @_mutmut_mutated(mutants_xǁCiFaninParityǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        return workflow_fanin_is_dishonest(
            path,
            aggregator_name=self.aggregator_name,
        )

    def xǁCiFaninParityǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        return workflow_fanin_is_dishonest(
            path,
            aggregator_name=self.aggregator_name,
        )

    def xǁCiFaninParityǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        return workflow_fanin_is_dishonest(
            None,
            aggregator_name=self.aggregator_name,
        )

    def xǁCiFaninParityǁfile_has_violation__mutmut_2(self, path: Path) -> bool:
        return workflow_fanin_is_dishonest(
            path,
            aggregator_name=None,
        )

    def xǁCiFaninParityǁfile_has_violation__mutmut_3(self, path: Path) -> bool:
        return workflow_fanin_is_dishonest(
            aggregator_name=self.aggregator_name,
        )

    def xǁCiFaninParityǁfile_has_violation__mutmut_4(self, path: Path) -> bool:
        return workflow_fanin_is_dishonest(
            path,
            )

mutants_xǁCiFaninParityǁfrom_config__mutmut['_mutmut_orig'] = CiFaninParity.xǁCiFaninParityǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCiFaninParityǁfrom_config__mutmut['xǁCiFaninParityǁfrom_config__mutmut_1'] = CiFaninParity.xǁCiFaninParityǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCiFaninParityǁfrom_config__mutmut['xǁCiFaninParityǁfrom_config__mutmut_2'] = CiFaninParity.xǁCiFaninParityǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCiFaninParityǁfrom_config__mutmut['xǁCiFaninParityǁfrom_config__mutmut_3'] = CiFaninParity.xǁCiFaninParityǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCiFaninParityǁfrom_config__mutmut['xǁCiFaninParityǁfrom_config__mutmut_4'] = CiFaninParity.xǁCiFaninParityǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCiFaninParityǁfrom_config__mutmut['xǁCiFaninParityǁfrom_config__mutmut_5'] = CiFaninParity.xǁCiFaninParityǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCiFaninParityǁfrom_config__mutmut['xǁCiFaninParityǁfrom_config__mutmut_6'] = CiFaninParity.xǁCiFaninParityǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCiFaninParityǁfrom_config__mutmut['xǁCiFaninParityǁfrom_config__mutmut_7'] = CiFaninParity.xǁCiFaninParityǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁCiFaninParityǁfrom_config__mutmut['xǁCiFaninParityǁfrom_config__mutmut_8'] = CiFaninParity.xǁCiFaninParityǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁCiFaninParityǁfrom_config__mutmut['xǁCiFaninParityǁfrom_config__mutmut_9'] = CiFaninParity.xǁCiFaninParityǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁCiFaninParityǁfrom_config__mutmut['xǁCiFaninParityǁfrom_config__mutmut_10'] = CiFaninParity.xǁCiFaninParityǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁCiFaninParityǁfrom_config__mutmut['xǁCiFaninParityǁfrom_config__mutmut_11'] = CiFaninParity.xǁCiFaninParityǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁCiFaninParityǁfrom_config__mutmut['xǁCiFaninParityǁfrom_config__mutmut_12'] = CiFaninParity.xǁCiFaninParityǁfrom_config__mutmut_12 # type: ignore # mutmut generated
mutants_xǁCiFaninParityǁfrom_config__mutmut['xǁCiFaninParityǁfrom_config__mutmut_13'] = CiFaninParity.xǁCiFaninParityǁfrom_config__mutmut_13 # type: ignore # mutmut generated
mutants_xǁCiFaninParityǁfrom_config__mutmut['xǁCiFaninParityǁfrom_config__mutmut_14'] = CiFaninParity.xǁCiFaninParityǁfrom_config__mutmut_14 # type: ignore # mutmut generated
mutants_xǁCiFaninParityǁfrom_config__mutmut['xǁCiFaninParityǁfrom_config__mutmut_15'] = CiFaninParity.xǁCiFaninParityǁfrom_config__mutmut_15 # type: ignore # mutmut generated
mutants_xǁCiFaninParityǁfrom_config__mutmut['xǁCiFaninParityǁfrom_config__mutmut_16'] = CiFaninParity.xǁCiFaninParityǁfrom_config__mutmut_16 # type: ignore # mutmut generated
mutants_xǁCiFaninParityǁfrom_config__mutmut['xǁCiFaninParityǁfrom_config__mutmut_17'] = CiFaninParity.xǁCiFaninParityǁfrom_config__mutmut_17 # type: ignore # mutmut generated
mutants_xǁCiFaninParityǁfrom_config__mutmut['xǁCiFaninParityǁfrom_config__mutmut_18'] = CiFaninParity.xǁCiFaninParityǁfrom_config__mutmut_18 # type: ignore # mutmut generated
mutants_xǁCiFaninParityǁfrom_config__mutmut['xǁCiFaninParityǁfrom_config__mutmut_19'] = CiFaninParity.xǁCiFaninParityǁfrom_config__mutmut_19 # type: ignore # mutmut generated

mutants_xǁCiFaninParityǁis_in_scope__mutmut['_mutmut_orig'] = CiFaninParity.xǁCiFaninParityǁis_in_scope__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCiFaninParityǁis_in_scope__mutmut['xǁCiFaninParityǁis_in_scope__mutmut_1'] = CiFaninParity.xǁCiFaninParityǁis_in_scope__mutmut_1 # type: ignore # mutmut generated

mutants_xǁCiFaninParityǁenumerate_files__mutmut['_mutmut_orig'] = CiFaninParity.xǁCiFaninParityǁenumerate_files__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCiFaninParityǁenumerate_files__mutmut['xǁCiFaninParityǁenumerate_files__mutmut_1'] = CiFaninParity.xǁCiFaninParityǁenumerate_files__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCiFaninParityǁenumerate_files__mutmut['xǁCiFaninParityǁenumerate_files__mutmut_2'] = CiFaninParity.xǁCiFaninParityǁenumerate_files__mutmut_2 # type: ignore # mutmut generated

mutants_xǁCiFaninParityǁfile_has_violation__mutmut['_mutmut_orig'] = CiFaninParity.xǁCiFaninParityǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCiFaninParityǁfile_has_violation__mutmut['xǁCiFaninParityǁfile_has_violation__mutmut_1'] = CiFaninParity.xǁCiFaninParityǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCiFaninParityǁfile_has_violation__mutmut['xǁCiFaninParityǁfile_has_violation__mutmut_2'] = CiFaninParity.xǁCiFaninParityǁfile_has_violation__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCiFaninParityǁfile_has_violation__mutmut['xǁCiFaninParityǁfile_has_violation__mutmut_3'] = CiFaninParity.xǁCiFaninParityǁfile_has_violation__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCiFaninParityǁfile_has_violation__mutmut['xǁCiFaninParityǁfile_has_violation__mutmut_4'] = CiFaninParity.xǁCiFaninParityǁfile_has_violation__mutmut_4 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> CiFaninParity:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CiFaninParity.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> CiFaninParity:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CiFaninParity.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> CiFaninParity:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CiFaninParity.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> CiFaninParity:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CiFaninParity.from_config(config, repo_root=None)


def x_build__mutmut_3(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> CiFaninParity:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CiFaninParity.from_config(repo_root=repo_root)


def x_build__mutmut_4(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> CiFaninParity:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CiFaninParity.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(CiFaninParity, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(CiFaninParity, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(CiFaninParity, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(CiFaninParity, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
