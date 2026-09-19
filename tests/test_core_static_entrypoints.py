"""Installed module entrypoints retain their command-line help contract."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.integration

_MODULES = (
    "actionable_feedback",
    "adr_number_unique",
    "behavioural_evidence",
    "ci_fanin_parity",
    "ci_silencers_have_rationale",
    "empty_body_intent",
    "every_test_has_tier_marker",
    "no_commented_out_code",
    "no_duplicate_string",
    "no_env_monkeypatch",
    "no_hardcoded_repo_paths",
    "no_internal_monkeypatch",
    "no_internal_patches_ts",
    "no_llm_attribution",
    "no_logging_secrets",
    "no_production_suppressions",
    "no_real_names",
    "no_test_doubles_in_runtime_tiers",
    "no_test_imports_in_prod",
)


@pytest.mark.parametrize("module", _MODULES)
def test_module_entrypoint_exposes_its_supported_cli(tmp_path: Path, module: str) -> None:
    args = [] if module == "behavioural_evidence" else ["--help"]
    result = subprocess.run(
        [sys.executable, "-m", f"tc_fitness.core_checks.{module}", *args],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    if args:
        assert "usage:" in result.stdout.lower()
