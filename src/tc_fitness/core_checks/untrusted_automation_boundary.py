"""CORE check: untrusted_automation_boundary — isolate autonomous analysis.

An autonomous workflow may read untrusted incident material, repository content,
or issue comments. It must not run in the same GitHub Actions job as cloud
login, token minting, or publishing credentials: prompt injection in the
analysis surface would otherwise have a direct route to those credentials.

Consumers opt in by naming the workflow paths and the action and credential
surfaces relevant to their platform. The check is repository-agnostic: no
workflow, action, secret, or runtime path is built in. For each configured
workflow it rejects a job that invokes a configured untrusted automation action
and also has any configured privileged capability. It also requires that the
automation action's configured contract input points at a configured runtime
contract root, keeping behaviour portable and runtime-verifiable.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path, PurePosixPath
from typing import Any

from tc_fitness.baseline import establish_baseline as _establish_baseline
from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

REMEDIATION = _remediation(
    fix=(
        "split autonomous analysis from privileged publishing into separate jobs. "
        "The analysis job may use only read-only permissions and no cloud login, "
        "token, or publishing command. Move its contract to the configured runtime "
        "contract root; make a separately validated publisher own privileged access."
    ),
    nxt="re-run this check and the workflow contract tests before opening the PR.",
    run="tc-fitness run",
    passing=(
        "investigate job: autonomous action + runtime contract + read-only permissions; "
        "publish job: validated output + cloud login or token minting"
    ),
    forbidden=(
        "one job combines an autonomous action with id-token write, cloud login, "
        "a credential environment variable, or a token/publish command"
    ),
)


def _as_strings(value: object) -> tuple[str, ...]:
    """Return string members of a scalar-or-sequence config value."""
    if isinstance(value, str):
        return (value,)
    if isinstance(value, Sequence):
        return tuple(item for item in value if isinstance(item, str))
    return ()


def _load_workflow(path: Path) -> Mapping[str, Any] | None:
    """Parse one workflow, returning ``None`` for unreadable or invalid YAML."""
    try:
        import yaml
    except ImportError:
        return None
    try:
        loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        return None
    return loaded if isinstance(loaded, Mapping) else None


def _step_uses(step: object, prefixes: tuple[str, ...]) -> bool:
    """Whether ``step`` invokes an action with a configured prefix."""
    if not isinstance(step, Mapping):
        return False
    uses = step.get("uses")
    return isinstance(uses, str) and any(uses.casefold().startswith(prefix.casefold()) for prefix in prefixes)


def _mapping_has_credential_env(value: object, names: tuple[str, ...]) -> bool:
    """Whether an ``env`` mapping names a configured credential variable."""
    return isinstance(value, Mapping) and any(name in value for name in names)


def _has_privileged_permission(value: object, names: tuple[str, ...]) -> bool:
    """Whether a GitHub permissions mapping grants a configured write capability."""
    if isinstance(value, str):
        return value.casefold() == "write-all" and bool(names)
    if not isinstance(value, Mapping):
        return False
    return any(str(value.get(name, "")).lower() == "write" for name in names)


def _normalise_relative_path(value: str) -> tuple[str, ...] | None:
    """Return normalised relative POSIX components, rejecting root escape."""
    path = PurePosixPath(value)
    if path.is_absolute():
        return None
    parts: list[str] = []
    for part in path.parts:
        if part in ("", "."):
            continue
        if part == "..":
            if not parts:
                return None
            parts.pop()
            continue
        parts.append(part)
    return tuple(parts)


def _is_at_runtime_root(contract_path: str, runtime_contract_roots: tuple[str, ...]) -> bool:
    """Whether a normalised contract path is within one configured root."""
    contract_parts = _normalise_relative_path(contract_path)
    if contract_parts is None:
        return False
    for root in runtime_contract_roots:
        root_parts = _normalise_relative_path(root)
        if root_parts and contract_parts[: len(root_parts)] == root_parts:
            return True
    return False


def _has_contract_at_runtime_root(
    step: Mapping[str, Any],
    *,
    contract_keys: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
) -> bool:
    """Whether the autonomous action reads a configured contract from runtime scope."""
    if not contract_keys or not runtime_contract_roots:
        return True
    with_value = step.get("with")
    if not isinstance(with_value, Mapping):
        return False
    for key in contract_keys:
        contract_path = with_value.get(key)
        if isinstance(contract_path, str) and _is_at_runtime_root(contract_path, runtime_contract_roots):
            return True
    return False


def workflow_has_untrusted_automation_boundary_violation(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            continue
        steps = job.get("steps")
        if not isinstance(steps, Sequence):
            continue
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if not isinstance(step, Mapping):
                continue
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


class UntrustedAutomationBoundary(FitnessRule):
    """Flags an autonomous workflow job that can reach privileged credentials."""

    name = "untrusted-automation-boundary"
    remediation = REMEDIATION
    extensions = (".yml", ".yaml")

    workflows: tuple[str, ...] = ()
    untrusted_action_prefixes: tuple[str, ...] = ()
    privileged_action_prefixes: tuple[str, ...] = ()
    privileged_permissions: tuple[str, ...] = ()
    credential_env_names: tuple[str, ...] = ()
    credential_command_markers: tuple[str, ...] = ()
    runtime_contract_roots: tuple[str, ...] = ()
    contract_keys: tuple[str, ...] = ()

    @classmethod
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    def enumerate_files(self) -> list[Path]:
        """Enumerate only existing consumer-configured workflow files."""
        return [
            self._repo_root / workflow
            for workflow in self.workflows
            if (self._repo_root / workflow).is_file()
        ]

    def is_in_scope(self, rel: str) -> bool:
        return rel in self.workflows

    def file_has_violation(self, path: Path) -> bool:
        return workflow_has_untrusted_automation_boundary_violation(
            path,
            untrusted_action_prefixes=self.untrusted_action_prefixes,
            privileged_action_prefixes=self.privileged_action_prefixes,
            privileged_permissions=self.privileged_permissions,
            credential_env_names=self.credential_env_names,
            credential_command_markers=self.credential_command_markers,
            runtime_contract_roots=self.runtime_contract_roots,
            contract_keys=self.contract_keys,
        )

    def run(self) -> int:
        """Hard gate: a credential boundary violation is never grandfathered.

        A workflow may change without changing its filename, so a per-file
        baseline would hide a fresh credential path added to a previously known
        workflow. This check therefore evaluates the current workflow state on
        every run and deliberately does not consult a baseline.
        """
        violations = sorted(str(path) for path in self.collect_violations())
        if not violations:
            print(f"ok [arch:{self._name}] — autonomous workflows are isolated from credentials.")
            return 0
        print(f"FAIL [arch:{self._name}] — autonomous workflow crosses a credential boundary:")
        for path in violations:
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def establish_baseline(self) -> Path:
        """Write an empty baseline; this security boundary is not grandfathered."""
        return _establish_baseline(self._name, set(), self._repo_root)


def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> UntrustedAutomationBoundary:
    """Factory the engine calls to bind this CORE check to consumer config."""
    return UntrustedAutomationBoundary.from_config(config, repo_root=repo_root)


def main(argv: list[str] | None = None) -> int:
    """CLI entry — supports ``--establish-baseline`` and ``--repo-root``."""
    return run_core_check(UntrustedAutomationBoundary, argv)


if __name__ == "__main__":
    import sys

    sys.exit(main())
