"""Tests for the CORE check no_noop_test_scripts (v0.6.0)."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
from _core_check_assertions import assert_no_repo_identity

from tc_fitness.core_checks.no_noop_test_scripts import (
    NoNoopTestScripts,
    build,
    main,
)

pytestmark = pytest.mark.integration

_PLACEHOLDER = re.compile(
    r"(?:no tests? yet|todo|placeholder|not implemented|skip tests?|exit\s+0)", re.IGNORECASE
)
_REAL = re.compile(r"\b(vitest|jest|node\s+--test|tsx|mocha|tap|ava|playwright)\b")


def _seed_pkg(tmp_path: Path, rel: str, test_script: str) -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"scripts": {"test": test_script}}), encoding="utf-8")
    return p


def test_prod_prefix_scoping(tmp_path: Path) -> None:
    _seed_pkg(tmp_path, "agentic/pkg/package.json", "echo 'no tests yet'")
    _seed_pkg(tmp_path, "vendor/pkg/package.json", "echo 'no tests yet'")
    rule = NoNoopTestScripts.from_config({"prod_package_prefixes": ["agentic/"]}, repo_root=tmp_path)
    assert {str(p) for p in rule.collect_violations()} == {"agentic/pkg/package.json"}


def test_root_manifest_in_scope(tmp_path: Path) -> None:
    _seed_pkg(tmp_path, "package.json", "todo")
    rule = NoNoopTestScripts.from_config({}, repo_root=tmp_path)
    assert {str(p) for p in rule.collect_violations()} == {"package.json"}


def test_echoing_a_runner_name_does_not_execute_the_runner(tmp_path: Path) -> None:
    _seed_pkg(tmp_path, "agentic/pkg/package.json", "echo 'no tests yet; vitest run'")
    rule = build({"prod_package_prefixes": ["agentic/"]}, repo_root=tmp_path)

    assert rule.run() == 1


def test_real_runner_after_placeholder_echo_is_accepted(tmp_path: Path) -> None:
    _seed_pkg(tmp_path, "agentic/pkg/package.json", "echo 'no tests yet' && vitest run")
    rule = build({"prod_package_prefixes": ["agentic/"]}, repo_root=tmp_path)

    assert rule.run() == 0


def test_real_test_command_without_placeholder_is_clean(tmp_path: Path) -> None:
    _seed_pkg(tmp_path, "agentic/pkg/package.json", "vitest run")
    rule = build({"prod_package_prefixes": ["agentic/"]}, repo_root=tmp_path)

    assert rule.run() == 0


@pytest.mark.parametrize(
    "runner_command",
    [
        "npx --yes vitest run",
        "pnpm --silent exec vitest run",
        "pnpm exec -- vitest run",
        "env CI=true vitest run",
        "node --test tests/*.test.js",
    ],
)
def test_package_manager_runner_options_are_recognised(tmp_path: Path, runner_command: str) -> None:
    _seed_pkg(tmp_path, "agentic/pkg/package.json", f"echo 'no tests yet' && {runner_command}")
    rule = build({"prod_package_prefixes": ["agentic/"]}, repo_root=tmp_path)

    assert rule.run() == 0


def test_malformed_shell_command_is_a_placeholder_failure(tmp_path: Path) -> None:
    _seed_pkg(tmp_path, "agentic/pkg/package.json", "echo 'no tests yet")
    rule = build({"prod_package_prefixes": ["agentic/"]}, repo_root=tmp_path)

    assert rule.run() == 1


def test_non_runner_package_manager_command_is_not_accepted(tmp_path: Path) -> None:
    _seed_pkg(tmp_path, "agentic/pkg/package.json", "echo 'no tests yet' && pnpm test")
    rule = build({"prod_package_prefixes": ["agentic/"]}, repo_root=tmp_path)

    assert rule.run() == 1


@pytest.mark.parametrize("script", ["echo 'no tests yet' && npx", "echo 'no tests yet' &&"])
def test_runner_wrappers_without_an_executable_remain_noops(tmp_path: Path, script: str) -> None:
    _seed_pkg(tmp_path, "agentic/pkg/package.json", script)
    rule = build({"prod_package_prefixes": ["agentic/"]}, repo_root=tmp_path)

    assert rule.run() == 1


def test_missing_test_script_is_not_a_placeholder_test(tmp_path: Path) -> None:
    manifest = tmp_path / "agentic/pkg/package.json"
    manifest.parent.mkdir(parents=True)
    manifest.write_text('{"scripts": {"build": "tsc"}}', encoding="utf-8")
    rule = build({"prod_package_prefixes": ["agentic/"]}, repo_root=tmp_path)

    assert rule.run() == 0


def test_custom_placeholder_and_runner_patterns_are_respected(tmp_path: Path) -> None:
    _seed_pkg(tmp_path, "agentic/pkg/package.json", "echo waiting && custom-test execute")
    rule = build(
        {
            "prod_package_prefixes": ["agentic/"],
            "placeholder_pattern": "waiting",
            "real_runner_pattern": r"custom-test",
        },
        repo_root=tmp_path,
    )

    assert rule.run() == 0


def test_malformed_json_manifest_is_reported(tmp_path: Path) -> None:
    manifest = tmp_path / "agentic/pkg/package.json"
    manifest.parent.mkdir(parents=True)
    manifest.write_text('{"scripts":', encoding="utf-8")
    rule = build({"prod_package_prefixes": ["agentic/"]}, repo_root=tmp_path)

    assert rule.run() == 1


def test_malformed_scripts_section_is_incomplete_not_clean(tmp_path: Path) -> None:
    manifest = tmp_path / "agentic/pkg/package.json"
    manifest.parent.mkdir(parents=True)
    manifest.write_text('{"scripts": []}', encoding="utf-8")
    rule = build({"prod_package_prefixes": ["agentic/"]}, repo_root=tmp_path)

    assert rule.run() == 1


def test_non_object_manifest_is_incomplete_not_clean(tmp_path: Path) -> None:
    manifest = tmp_path / "agentic/pkg/package.json"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text('["scripts", "test"]', encoding="utf-8")
    rule = build({"prod_package_prefixes": ["agentic/"]}, repo_root=tmp_path)

    assert rule.run() == 1


def test_skip_parts_are_config_driven(tmp_path: Path) -> None:
    _seed_pkg(tmp_path, "agentic/pkg/node_modules/dep/package.json", "todo")
    _seed_pkg(tmp_path, "agentic/pkg/package.json", "todo")
    rule = NoNoopTestScripts.from_config({"prod_package_prefixes": ["agentic/"]}, repo_root=tmp_path)
    assert {str(p) for p in rule.collect_violations()} == {"agentic/pkg/package.json"}


def test_run_then_establish_grandfathers(tmp_path: Path) -> None:
    _seed_pkg(tmp_path, "agentic/pkg/package.json", "echo 'no tests yet'")
    rule = NoNoopTestScripts.from_config({"prod_package_prefixes": ["agentic/"]}, repo_root=tmp_path)
    assert rule.run() == 1
    rule.establish_baseline()
    assert rule.run() == 0


def test_main_establish_baseline_mode(tmp_path: Path) -> None:
    _seed_pkg(tmp_path, "package.json", "todo")
    rc = main(["--establish-baseline", "--repo-root", str(tmp_path)])
    assert rc == 0
    assert (tmp_path / ".architecture" / "baseline" / "no-noop-test-scripts-files.txt").exists()


def test_build_returns_rule() -> None:
    assert isinstance(build({}), NoNoopTestScripts)


def test_no_repo_strings_in_executable_code() -> None:
    import tc_fitness.core_checks.no_noop_test_scripts as mod

    assert_no_repo_identity(mod.__file__)
