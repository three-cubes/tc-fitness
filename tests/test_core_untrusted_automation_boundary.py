"""Tests for the untrusted_automation_boundary CORE check."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from tc_fitness.core_checks.untrusted_automation_boundary import (
    build,
    workflow_has_untrusted_automation_boundary_violation,
)

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


@pytest.mark.integration
def test_separate_untrusted_and_privileged_jobs_are_clean(tmp_path: Path) -> None:
    assert _violates(_seed(tmp_path, _SAFE)) is False
    assert build(_CONFIG, repo_root=tmp_path).collect_violations() == set()


@pytest.mark.integration
def test_untrusted_job_with_write_permission_is_flagged(tmp_path: Path) -> None:
    body = _SAFE.replace(
        "contents: read\n    steps:\n      - uses: example/autonomous",
        "id-token: write\n    steps:\n      - uses: example/autonomous",
    )
    assert _violates(_seed(tmp_path, body)) is True


@pytest.mark.integration
def test_untrusted_job_with_write_all_permission_is_flagged(tmp_path: Path) -> None:
    body = _SAFE.replace("permissions:\n      contents: read", "permissions: write-all")
    assert _violates(_seed(tmp_path, body)) is True


@pytest.mark.integration
def test_untrusted_job_with_cloud_login_is_flagged(tmp_path: Path) -> None:
    body = _SAFE.replace(
        "prompt-file: agentic/skills/ops/remediate/SKILL.md",
        "prompt-file: agentic/skills/ops/remediate/SKILL.md\n      - uses: example/cloud-login@v1",
    )
    assert _violates(_seed(tmp_path, body)) is True


@pytest.mark.integration
def test_untrusted_job_with_credential_environment_is_flagged(tmp_path: Path) -> None:
    body = _SAFE.replace(
        "prompt-file: agentic/skills/ops/remediate/SKILL.md",
        "prompt-file: agentic/skills/ops/remediate/SKILL.md\n        env:\n          GH_TOKEN: ${{ secrets.token }}",
    )
    assert _violates(_seed(tmp_path, body)) is True


@pytest.mark.integration
def test_untrusted_job_inherits_workflow_credential_environment(tmp_path: Path) -> None:
    body = _SAFE.replace(
        "on: workflow_dispatch",
        "on: workflow_dispatch\nenv:\n  GH_TOKEN: ${{ secrets.token }}",
    )
    assert _violates(_seed(tmp_path, body)) is True


@pytest.mark.integration
def test_untrusted_job_with_publishing_command_is_flagged(tmp_path: Path) -> None:
    body = _SAFE.replace(
        "prompt-file: agentic/skills/ops/remediate/SKILL.md",
        "prompt-file: agentic/skills/ops/remediate/SKILL.md\n      - run: git push origin fix/bad",
    )
    assert _violates(_seed(tmp_path, body)) is True


@pytest.mark.integration
def test_untrusted_job_with_whitespace_obfuscated_publishing_command_is_flagged(tmp_path: Path) -> None:
    body = _SAFE.replace(
        "prompt-file: agentic/skills/ops/remediate/SKILL.md",
        "prompt-file: agentic/skills/ops/remediate/SKILL.md\n      - run: git\t  push origin fix/bad",
    )
    assert _violates(_seed(tmp_path, body)) is True


@pytest.mark.integration
def test_contract_outside_runtime_root_is_flagged(tmp_path: Path) -> None:
    body = _SAFE.replace("agentic/skills/ops/remediate/SKILL.md", ".github/prompts/remediate.md")
    assert _violates(_seed(tmp_path, body)) is True


@pytest.mark.integration
def test_contract_traversal_or_sibling_runtime_prefix_is_flagged(tmp_path: Path) -> None:
    traversal = _SAFE.replace(
        "agentic/skills/ops/remediate/SKILL.md", "agentic/../.github/prompts/remediate.md"
    )
    sibling = _SAFE.replace("agentic/skills/ops/remediate/SKILL.md", "agentic-other/prompts/remediate.md")
    assert _violates(_seed(tmp_path, traversal)) is True
    assert _violates(_seed(tmp_path, sibling)) is True


@pytest.mark.integration
def test_action_references_are_matched_case_insensitively(tmp_path: Path) -> None:
    body = _SAFE.replace("example/autonomous-action@v1", "EXAMPLE/AUTONOMOUS-ACTION@v1")
    assert _violates(_seed(tmp_path, body)) is False
    body = body.replace(
        "prompt-file: agentic/skills/ops/remediate/SKILL.md",
        "prompt-file: agentic/skills/ops/remediate/SKILL.md\n      - uses: EXAMPLE/CLOUD-LOGIN@v1",
    )
    assert _violates(_seed(tmp_path, body)) is True


@pytest.mark.integration
def test_absent_configured_workflow_is_vacuously_clean(tmp_path: Path) -> None:
    assert build(_CONFIG, repo_root=tmp_path).collect_violations() == set()


@pytest.mark.integration
def test_invalid_configured_workflow_is_flagged(tmp_path: Path) -> None:
    assert _violates(_seed(tmp_path, "jobs: [")) is True


@pytest.mark.integration
def test_existing_baseline_cannot_hide_a_boundary_violation(tmp_path: Path) -> None:
    _seed(tmp_path, _SAFE.replace("contents: read", "id-token: write"))
    baseline = tmp_path / ".architecture/baseline/untrusted-automation-boundary-files.txt"
    baseline.parent.mkdir(parents=True)
    baseline.write_text(".github/workflows/responder.yml\n", encoding="utf-8")
    assert build(_CONFIG, repo_root=tmp_path).run() == 1


@pytest.mark.integration
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
