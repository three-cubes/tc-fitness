"""Exercise CORE check entrypoints as real Python module processes."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.integration

_MODULES = (
    "bicep_arm_lint",
    "canonical_commit_identity",
    "ci_consumes_shared_gate",
    "contract_change_has_test",
    "coverage_floor",
    "coverage_includes_branches",
    "deterministic_tests",
    "engine_version_floor",
    "harness_canon_reference",
    "mutation_survival_ratchet",
    "new_code_coverage",
    "osv_scanner_sca",
    "readme_resolver_coverage",
    "schema_conformance",
    "script_help_smoke",
)


def _seed(root: Path, relative: str, content: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


@pytest.mark.parametrize("module", _MODULES)
def test_core_check_module_entrypoint_uses_its_public_runtime_contract(tmp_path: Path, module: str) -> None:
    if module == "coverage_floor":
        _seed(
            tmp_path,
            "coverage.xml",
            '<coverage><sources><source>src</source></sources><class filename="a.py" line-rate="1"/></coverage>',
        )
    elif module == "coverage_includes_branches":
        _seed(tmp_path, "coverage.xml", '<coverage branch-rate="0.5" branches-valid="2"/>')
    elif module == "harness_canon_reference":
        for name in ("CLAUDE.md", "AGENTS.md", "RESOLVER.md", "ETHOS.md", "SCORECARD.md", "CONTRIBUTING.md"):
            content = (
                "Canonical standards are indexed at governance/STANDARDS.md\n"
                if name == "AGENTS.md"
                else "entrypoint\n"
            )
            _seed(tmp_path, name, content)

    arguments = [sys.executable, "-m", f"tc_fitness.core_checks.{module}", "--repo-root", str(tmp_path)]
    if module == "osv_scanner_sca":
        arguments.extend(("--scanner-version", "0.0.0", "--lockfile", "missing.lock"))
    result = subprocess.run(
        arguments,
        cwd=tmp_path,
        capture_output=True,
        check=False,
        text=True,
        env={**os.environ, "PYTHONPATH": str(Path(__file__).parents[1] / "src")},
    )

    if module == "new_code_coverage":
        assert result.returncode == 1
        assert "coverage report is missing" in result.stdout
    elif module in {"osv_scanner_sca", "mutation_survival_ratchet"}:
        if module == "mutation_survival_ratchet":
            assert result.returncode == 1
            assert "baseline" in result.stdout.lower()
            return
        assert result.returncode == 1
        assert "INCOMPLETE osv_scanner_sca" in result.stdout
    else:
        assert result.returncode == 0, result.stderr
