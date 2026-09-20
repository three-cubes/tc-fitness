"""Tests for the untrusted_automation_boundary CORE check."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from tc_fitness.core_checks.untrusted_automation_boundary import (
    build,
    workflow_has_untrusted_automation_boundary_violation,
)

pytestmark = pytest.mark.integration

_CONFIG = {
    "workflows": [".github/workflows/responder.yml"],
    "untrusted_action_prefixes": ["example/autonomous-action@"],
    "privileged_action_prefixes": ["example/cloud-login@"],
    "privileged_permissions": ["id-token"],
    "credential_env_names": ["GH_TOKEN"],
    "credential_command_markers": ["mint-token", "git push"],
    "runtime_contract_roots": ["agentic/"],
    "contract_keys": ["prompt-file"],
}

_SAFE = """
name: responder
on: workflow_dispatch
jobs:
  investigate:
    permissions:
      contents: read
    steps:
      - uses: example/autonomous-action@v1
        with:
          prompt-file: agentic/skills/ops/remediate/SKILL.md
  publish:
    permissions:
      id-token: write
    steps:
      - uses: example/cloud-login@v1
      - run: mint-token && git push origin fix/recover
"""


def _seed(tmp_path: Path, body: str) -> Path:
    path = tmp_path / ".github/workflows/responder.yml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    return path


def _violates(path: Path) -> bool:
    return workflow_has_untrusted_automation_boundary_violation(
        path,
        untrusted_action_prefixes=("example/autonomous-action@",),
        privileged_action_prefixes=("example/cloud-login@",),
        privileged_permissions=("id-token",),
        credential_env_names=("GH_TOKEN",),
        credential_command_markers=("mint-token", "git push"),
        runtime_contract_roots=("agentic/",),
        contract_keys=("prompt-file",),
    )


def test_separate_untrusted_and_privileged_jobs_are_clean(tmp_path: Path) -> None:
    assert _violates(_seed(tmp_path, _SAFE)) is False
    assert build(_CONFIG, repo_root=tmp_path).collect_violations() == set()


def test_single_workflow_string_config_is_supported(tmp_path: Path) -> None:
    _seed(tmp_path, _SAFE)

    assert build(dict(_CONFIG, workflows=".github/workflows/responder.yml"), repo_root=tmp_path).run() == 0


def test_none_workflow_config_selects_no_workflows(tmp_path: Path) -> None:
    assert build(dict(_CONFIG, workflows=None), repo_root=tmp_path).run() == 0


@pytest.mark.parametrize("invalid", [7, "", [".github/workflows/responder.yml", 7]])
def test_invalid_string_list_configuration_is_rejected(tmp_path: Path, invalid: object) -> None:
    with pytest.raises(ValueError, match="must be a string or a sequence of non-empty strings"):
        build(dict(_CONFIG, workflows=invalid), repo_root=tmp_path)


def test_untrusted_job_with_write_permission_is_flagged(tmp_path: Path) -> None:
    body = _SAFE.replace(
        "contents: read\n    steps:\n      - uses: example/autonomous",
        "id-token: write\n    steps:\n      - uses: example/autonomous",
    )
    assert _violates(_seed(tmp_path, body)) is True


def test_untrusted_job_with_write_all_permission_is_flagged(tmp_path: Path) -> None:
    body = _SAFE.replace("permissions:\n      contents: read", "permissions: write-all")
    assert _violates(_seed(tmp_path, body)) is True


def test_untrusted_job_with_cloud_login_is_flagged(tmp_path: Path) -> None:
    body = _SAFE.replace(
        "prompt-file: agentic/skills/ops/remediate/SKILL.md",
        "prompt-file: agentic/skills/ops/remediate/SKILL.md\n      - uses: example/cloud-login@v1",
    )
    assert _violates(_seed(tmp_path, body)) is True


def test_untrusted_job_with_credential_environment_is_flagged(tmp_path: Path) -> None:
    body = _SAFE.replace(
        "prompt-file: agentic/skills/ops/remediate/SKILL.md",
        "prompt-file: agentic/skills/ops/remediate/SKILL.md\n        env:\n          GH_TOKEN: ${{ secrets.token }}",
    )
    assert _violates(_seed(tmp_path, body)) is True


def test_untrusted_job_inherits_workflow_credential_environment(tmp_path: Path) -> None:
    body = _SAFE.replace(
        "on: workflow_dispatch",
        "on: workflow_dispatch\nenv:\n  GH_TOKEN: ${{ secrets.token }}",
    )
    assert _violates(_seed(tmp_path, body)) is True


def test_untrusted_job_with_publishing_command_is_flagged(tmp_path: Path) -> None:
    body = _SAFE.replace(
        "prompt-file: agentic/skills/ops/remediate/SKILL.md",
        "prompt-file: agentic/skills/ops/remediate/SKILL.md\n      - run: git push origin fix/bad",
    )
    assert _violates(_seed(tmp_path, body)) is True


def test_untrusted_job_with_whitespace_obfuscated_publishing_command_is_flagged(tmp_path: Path) -> None:
    body = _SAFE.replace(
        "prompt-file: agentic/skills/ops/remediate/SKILL.md",
        "prompt-file: agentic/skills/ops/remediate/SKILL.md\n      - run: git\t  push origin fix/bad",
    )
    assert _violates(_seed(tmp_path, body)) is True


def test_contract_outside_runtime_root_is_flagged(tmp_path: Path) -> None:
    body = _SAFE.replace("agentic/skills/ops/remediate/SKILL.md", ".github/prompts/remediate.md")
    assert _violates(_seed(tmp_path, body)) is True


def test_contract_traversal_or_sibling_runtime_prefix_is_flagged(tmp_path: Path) -> None:
    traversal = _SAFE.replace(
        "agentic/skills/ops/remediate/SKILL.md", "agentic/../.github/prompts/remediate.md"
    )
    sibling = _SAFE.replace("agentic/skills/ops/remediate/SKILL.md", "agentic-other/prompts/remediate.md")
    assert _violates(_seed(tmp_path, traversal)) is True
    assert _violates(_seed(tmp_path, sibling)) is True


def test_action_references_are_matched_case_insensitively(tmp_path: Path) -> None:
    body = _SAFE.replace("example/autonomous-action@v1", "EXAMPLE/AUTONOMOUS-ACTION@v1")
    assert _violates(_seed(tmp_path, body)) is False
    body = body.replace(
        "prompt-file: agentic/skills/ops/remediate/SKILL.md",
        "prompt-file: agentic/skills/ops/remediate/SKILL.md\n      - uses: EXAMPLE/CLOUD-LOGIN@v1",
    )
    assert _violates(_seed(tmp_path, body)) is True


def test_absent_configured_workflow_is_incomplete_evidence(tmp_path: Path) -> None:
    assert build(_CONFIG, repo_root=tmp_path).run() == 1


def test_invalid_configured_workflow_is_flagged(tmp_path: Path) -> None:
    assert _violates(_seed(tmp_path, "jobs: [")) is True


@pytest.mark.parametrize(
    "body", ["jobs: []\n", "jobs:\n  investigate: true\n", "jobs:\n  investigate:\n    steps: null\n"]
)
def test_workflow_shape_that_cannot_be_evaluated_is_reported(tmp_path: Path, body: str) -> None:
    _seed(tmp_path, body)

    assert build(_CONFIG, repo_root=tmp_path).run() == 1


@pytest.mark.parametrize(
    "steps",
    ["steps: [unstructured-step]", "steps: autonomous-action@v1"],
)
def test_malformed_step_entries_are_incomplete_not_clean(tmp_path: Path, steps: str) -> None:
    _seed(tmp_path, f"jobs:\n  investigate:\n    {steps}\n")

    assert build(_CONFIG, repo_root=tmp_path).run() == 1


def test_valid_empty_jobs_and_no_untrusted_action_are_clean(tmp_path: Path) -> None:
    body = "name: scheduled\njobs:\n  build:\n    steps:\n      - run: make check\n"
    _seed(tmp_path, body)

    assert build(_CONFIG, repo_root=tmp_path).run() == 0


def test_normalised_contract_path_inside_runtime_root_is_clean(tmp_path: Path) -> None:
    body = _SAFE.replace("agentic/skills/ops/remediate/SKILL.md", "./agentic/ops/../skills/remediate.md")
    _seed(tmp_path, body)

    assert build(_CONFIG, repo_root=tmp_path).run() == 0


def test_absolute_runtime_contract_path_is_rejected(tmp_path: Path) -> None:
    _seed(tmp_path, _SAFE.replace("agentic/skills/ops/remediate/SKILL.md", "/agentic/skills/remediate.md"))

    assert build(_CONFIG, repo_root=tmp_path).run() == 1


def test_contract_path_that_escapes_runtime_root_is_rejected(tmp_path: Path) -> None:
    _seed(tmp_path, _SAFE.replace("agentic/skills/ops/remediate/SKILL.md", "../../outside.md"))

    assert build(_CONFIG, repo_root=tmp_path).run() == 1


def test_untrusted_action_without_contract_input_is_rejected(tmp_path: Path) -> None:
    body = _SAFE.replace("        with:\n          prompt-file: agentic/skills/ops/remediate/SKILL.md\n", "")
    _seed(tmp_path, body)

    assert build(_CONFIG, repo_root=tmp_path).run() == 1


def test_workflow_level_write_permission_is_inherited_by_untrusted_job(tmp_path: Path) -> None:
    body = _SAFE.replace("on: workflow_dispatch", "on: workflow_dispatch\npermissions:\n  id-token: write")
    body = body.replace("    permissions:\n      contents: read\n", "")
    _seed(tmp_path, body)

    assert build(_CONFIG, repo_root=tmp_path).run() == 1


def test_step_credential_environment_is_flagged(tmp_path: Path) -> None:
    body = _SAFE.replace(
        "prompt-file: agentic/skills/ops/remediate/SKILL.md",
        "prompt-file: agentic/skills/ops/remediate/SKILL.md\n        env:\n          GH_TOKEN: ${{ secrets.token }}",
    )
    _seed(tmp_path, body)

    assert build(_CONFIG, repo_root=tmp_path).run() == 1


def test_no_contract_constraint_is_clean_when_not_configured(tmp_path: Path) -> None:
    _seed(tmp_path, "jobs:\n  investigate:\n    steps:\n      - uses: example/autonomous-action@v1\n")
    config = dict(_CONFIG, runtime_contract_roots=[], contract_keys=[])

    assert build(config, repo_root=tmp_path).run() == 0


def test_existing_baseline_cannot_hide_a_boundary_violation(tmp_path: Path) -> None:
    _seed(tmp_path, _SAFE.replace("contents: read", "id-token: write"))
    baseline = tmp_path / ".architecture/baseline/untrusted-automation-boundary-files.txt"
    baseline.parent.mkdir(parents=True)
    baseline.write_text(".github/workflows/responder.yml\n", encoding="utf-8")
    assert build(_CONFIG, repo_root=tmp_path).run() == 1


def test_no_repo_strings_in_executable_code() -> None:
    import tc_fitness.core_checks.untrusted_automation_boundary as mod

    text = Path(mod.__file__).read_text(encoding="utf-8")
    tree = ast.parse(text)
    docstring_ids = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            doc = ast.get_docstring(node, clean=False)
            if doc is not None and node.body:
                first = node.body[0]
                if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant):
                    docstring_ids.add(id(first.value))
    repo_tokens = ("kairix", "tc-agent-zone", "agent-zone", "kata")
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            if id(node) not in docstring_ids:
                assert all(token not in node.value.lower() for token in repo_tokens)
