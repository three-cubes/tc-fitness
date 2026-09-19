"""Public ``python -m`` contracts for config-driven CORE rules."""

from __future__ import annotations

import subprocess
import sys

import pytest

pytestmark = pytest.mark.integration

_CORE_MODULES = (
    "integrity_state_predicate",
    "license_present",
    "no_language_suffix_in_package_names",
    "no_noop_test_scripts",
    "no_test_only_kwargs",
    "posix_path_serialisation",
    "shellcheck_disable_with_reason",
    "sonar_ignore_rationale",
    "suppressions_have_rationale",
    "test_skip_rationale",
    "untrusted_automation_boundary",
    "unused_params_named",
)


@pytest.mark.parametrize("module", _CORE_MODULES)
def test_module_cli_exposes_repo_root_help(module: str) -> None:
    result = subprocess.run(
        [sys.executable, "-m", f"tc_fitness.core_checks.{module}", "--help"],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert result.returncode == 0, result.stderr
    assert "usage:" in result.stdout
    assert "--repo-root" in result.stdout
