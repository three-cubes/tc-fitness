"""Real public assurance admission and ordinary-consumer policy compatibility."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

import pytest
import yaml
from test_check_contract_execution import invoke, make_contract

from tc_fitness.check_contract_execution import validate_contract_ledger
from tc_fitness.check_contract_policy import validate_contract_configuration
from tc_fitness.check_contracts import CheckContractError
from tc_fitness.core_checks import CORE_CHECKS

pytestmark = pytest.mark.integration


def contract_for(root: Path, check: str, config: dict[str, object]) -> Path:
    manifest = make_contract(root)
    data = yaml.safe_load(manifest.read_text())
    data["check"] = check
    data["config"] = config
    manifest.write_text(yaml.safe_dump(data))
    return manifest


@pytest.mark.parametrize("option", ["warn_only", "baseline_ok"])
def test_real_forked_ci_cannot_be_admitted_using_adoption_alias(tmp_path: Path, option: str) -> None:
    manifest = contract_for(tmp_path, "core:ci_consumes_shared_gate", {option: True})
    workflow = tmp_path / "compliant" / ".github" / "workflows" / "ci.yml"
    workflow.parent.mkdir(parents=True)
    workflow.write_text("jobs:\n  quality:\n    steps:\n      - run: pytest\n")
    ledger = tmp_path / "ledger.json"
    started = datetime.now(UTC)
    result = invoke(manifest, "compliant", ledger, timeout=10)
    with pytest.raises(CheckContractError):
        validate_contract_ledger(
            manifest, "compliant", ledger, process_exit=result.returncode, started_after=started
        )
    assert result.returncode == 2
    assert not ledger.exists()


@pytest.mark.parametrize("check", CORE_CHECKS)
def test_every_core_check_rejects_an_unreviewed_advisory_alias(tmp_path: Path, check: str) -> None:
    manifest = contract_for(tmp_path, check, {"unreviewed_advisory": True})
    ledger = tmp_path / "ledger.json"
    result = invoke(manifest, "compliant", ledger, timeout=10)
    assert result.returncode == 2
    assert not ledger.exists()
    with pytest.raises(CheckContractError, match="unreviewed contract configuration"):
        validate_contract_ledger(
            manifest, "compliant", ledger, process_exit=2, started_after=datetime.now(UTC)
        )


@pytest.mark.parametrize(
    ("option", "value"),
    [("base_ref", "origin/main"), ("changed_files", ["infra/main.bicep"])],
)
def test_checkov_contract_accepts_its_reviewed_diff_scope_options(option: str, value: object) -> None:
    validate_contract_configuration("core:checkov_iac_security", {option: value})


@pytest.mark.parametrize(
    ("check", "option", "value"),
    [
        ("license_present", "exempt_files", ["src/example.py"]),
        ("no_internal_patches", "exempt_roots", ["app"]),
        ("no_internal_monkeypatch", "exempt_roots", ["app"]),
        ("no_internal_patches_ts", "exempt_specifiers", ["app"]),
        ("no_internal_patches_ts", "exempt_prefixes", ["app"]),
        ("no_production_suppressions", "exempt_prefixes", ["src"]),
        ("no_production_suppressions", "test_file_regex", ".*"),
        ("no_hardcoded_repo_paths", "exempt_prefixes", ["src"]),
        ("no_hardcoded_repo_paths", "exempt_extensions", [".py"]),
        ("path_naming", "allowed_names", ["bad_name.md"]),
        ("path_naming", "exempt_segments", ["src"]),
        ("no_test_only_kwargs", "exempt_keys", ["src/example.py::main::test_runner"]),
        ("readme_resolver_coverage", "exempt_dirs", ["src"]),
        ("posix_path_serialisation", "excluded_segments", ["src"]),
        ("every_test_has_tier_marker", "excluded_parts", ["src"]),
        ("no_noop_test_scripts", "skip_parts", ["src"]),
        ("script_help_smoke", "skip_dir_segments", ["src"]),
        ("mutation_survival_ratchet", "allow_missing_current", True),
        ("ci_fanin_parity", "informational_marker", "accepted debt"),
        ("canonical_commit_identity", "cutover_ref", "HEAD"),
        ("osv_scanner_sca", "required", False),
    ],
)
def test_each_audited_suppression_option_is_rejected_before_dispatch(
    tmp_path: Path, check: str, option: str, value: object
) -> None:
    manifest = contract_for(tmp_path, f"core:{check}", {option: value})
    ledger = tmp_path / "ledger.json"
    result = invoke(manifest, "compliant", ledger, timeout=10)
    assert result.returncode == 2
    assert not ledger.exists()
    with pytest.raises(CheckContractError, match=r"configuration|contract requires"):
        validate_contract_ledger(
            manifest, "compliant", ledger, process_exit=2, started_after=datetime.now(UTC)
        )


def test_osv_contract_requires_explicit_strict_scanning(tmp_path: Path) -> None:
    manifest = contract_for(tmp_path, "core:osv_scanner_sca", {})
    ledger = tmp_path / "ledger.json"
    assert invoke(manifest, "compliant", ledger, timeout=10).returncode == 2
    assert not ledger.exists()


def tier_contract(root: Path, config: dict[str, object]) -> Path:
    manifest = contract_for(root, "core:every_test_has_tier_marker", {"roots": ["tests"], **config})
    for case, declaration in (
        ("compliant", "pytestmark = pytest.mark.unit\n\n"),
        ("violation", "@pytest.mark.unit\n"),
    ):
        tests = root / case / "tests"
        tests.mkdir()
        (tests / "test_subject.py").write_text(
            "import pytest\n" + declaration + "def test_subject():\n    assert True\n"
        )
    data = yaml.safe_load(manifest.read_text())
    data["cases"][1]["expected"]["findings"] = [
        {"rule": "every-test-has-tier-marker", "path": "tests/test_subject.py", "message_contains": "fix:"}
    ]
    manifest.write_text(yaml.safe_dump(data))
    return manifest


@pytest.mark.parametrize("mode", [False, None, "true", 1])
def test_tier_contract_requires_explicit_canonical_mode(tmp_path: Path, mode: object) -> None:
    config = {} if mode is None else {"require_module_marker": mode}
    manifest = tier_contract(tmp_path, config)
    ledger = tmp_path / "ledger.json"
    result = invoke(manifest, "compliant", ledger, timeout=10)
    assert result.returncode == 2, result.stdout + result.stderr
    assert "tier contract requires require_module_marker=true" in result.stderr
    assert not ledger.exists()
    with pytest.raises(CheckContractError, match="tier contract requires require_module_marker=true"):
        validate_contract_ledger(
            manifest, "compliant", ledger, process_exit=2, started_after=datetime.now(UTC)
        )


def test_canonical_tier_contract_accepts_true_and_keeps_real_violation(tmp_path: Path) -> None:
    manifest = tier_contract(tmp_path, {"require_module_marker": True})
    for case, expected_exit in (("compliant", 0), ("violation", 1)):
        ledger = tmp_path / f"{case}.json"
        started = datetime.now(UTC)
        result = invoke(manifest, case, ledger, timeout=10)
        assert result.returncode == expected_exit, result.stdout + result.stderr
        validate_contract_ledger(manifest, case, ledger, process_exit=expected_exit, started_after=started)


@pytest.mark.parametrize("mode", [False, None])
def test_ordinary_consumer_keeps_generic_function_tiers(tmp_path: Path, mode: bool | None) -> None:
    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "test_subject.py").write_text(
        "import pytest\n@pytest.mark.unit\ndef test_subject():\n    assert True\n"
    )
    (tmp_path / "consumer_checks.py").write_text(
        "from tc_fitness.catalogue import RuleEntry\n"
        "ENTRIES = (RuleEntry(id='tiers', gate='tiers', check='core:every_test_has_tier_marker'),)\n"
    )
    config = (
        "[[steps]]\nid = 'tiers'\ncatalogue = 'consumer_checks:ENTRIES'\n"
        "[core_checks.every_test_has_tier_marker]\nroots = ['tests']\n"
    )
    if mode is False:
        config += "require_module_marker = false\n"
    (tmp_path / ".tc-fitness.toml").write_text(config)
    result = subprocess.run(
        [str(Path(sys.executable).with_name("tc-fitness")), "run", "--repo-root", str(tmp_path)],
        capture_output=True,
        text=True,
        check=False,
        timeout=10,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_validator_rejects_a_check_without_reviewed_configuration(tmp_path: Path) -> None:
    manifest = contract_for(tmp_path, "core:unreviewed_check", {})
    with pytest.raises(CheckContractError, match="no reviewed contract configuration"):
        validate_contract_ledger(
            manifest, "compliant", tmp_path / "ledger.json", process_exit=0, started_after=datetime.now(UTC)
        )


def test_test_filename_override_cannot_exempt_real_production_suppression(tmp_path: Path) -> None:
    manifest = contract_for(
        tmp_path, "core:no_production_suppressions", {"roots": ["src"], "test_file_regex": ".*"}
    )
    (tmp_path / "compliant" / "src" / "example.py").write_text("value = 1  # noqa\n")
    ledger = tmp_path / "ledger.json"
    assert invoke(manifest, "compliant", ledger, timeout=10).returncode == 2
    assert not ledger.exists()


def test_allowed_identity_policy_accepts_only_the_configured_real_git_identity(tmp_path: Path) -> None:
    manifest = contract_for(
        tmp_path,
        "core:canonical_commit_identity",
        {
            "allowed_emails": ["accepted@example.test"],
            "allowed_name_patterns": ["^Accepted$"],
            "base_ref": "HEAD~1",
            "head_ref": "HEAD",
        },
    )
    for case, identity, email, expected_exit in (
        ("compliant", "Accepted", "accepted@example.test", 0),
        ("violation", "Rejected", "rejected@example.test", 1),
    ):
        repo = tmp_path / case
        subprocess.run(["git", "init", "-q", str(repo)], check=True, capture_output=True, timeout=10)
        env = {
            **os.environ,
            "GIT_AUTHOR_NAME": identity,
            "GIT_AUTHOR_EMAIL": email,
            "GIT_COMMITTER_NAME": identity,
            "GIT_COMMITTER_EMAIL": email,
        }
        for message in ("base", "candidate"):
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(repo),
                    "-c",
                    "commit.gpgsign=false",
                    "-c",
                    "core.hooksPath=/dev/null",
                    "commit",
                    "--allow-empty",
                    "-qm",
                    message,
                ],
                env=env,
                check=True,
                capture_output=True,
                timeout=10,
            )
        if case == "violation":
            sha = subprocess.run(
                ["git", "-C", str(repo), "rev-parse", "HEAD"],
                text=True,
                capture_output=True,
                check=True,
                timeout=10,
            ).stdout.strip()
            data = yaml.safe_load(manifest.read_text())
            data["cases"][1]["expected"]["findings"] = [
                {
                    "rule": "canonical-commit-identity",
                    "path": f"{sha[:12]} author Rejected <rejected@example.test>; committer Rejected <rejected@example.test>",
                    "message_contains": "fix:",
                }
            ]
            manifest.write_text(yaml.safe_dump(data))
        ledger = tmp_path / f"{case}.json"
        started = datetime.now(UTC)
        assert invoke(manifest, case, ledger, timeout=10).returncode == expected_exit
        validate_contract_ledger(manifest, case, ledger, process_exit=expected_exit, started_after=started)


def test_real_complexity_threshold_remains_a_detector_policy_input(tmp_path: Path) -> None:
    manifest = contract_for(tmp_path, "core:cognitive_complexity", {"roots": ["src"], "threshold": 0})
    (tmp_path / "violation" / "src" / "example.py").write_text(
        "def check(value):\n    if value:\n        return 1\n    return 0\n"
    )
    data = yaml.safe_load(manifest.read_text())
    data["cases"][1]["expected"]["findings"] = [
        {"rule": "cognitive-complexity", "path": "src/example.py", "message_contains": "fix:"}
    ]
    manifest.write_text(yaml.safe_dump(data))
    for case, expected_exit in (("compliant", 0), ("violation", 1)):
        ledger = tmp_path / f"{case}.json"
        started = datetime.now(UTC)
        assert invoke(manifest, case, ledger, timeout=10).returncode == expected_exit
        validate_contract_ledger(manifest, case, ledger, process_exit=expected_exit, started_after=started)


def test_normal_scope_and_license_policy_still_detect_the_violation(tmp_path: Path) -> None:
    manifest = contract_for(
        tmp_path,
        "core:license_present",
        {"roots": ["src"], "markers": ["SPDX-License-Identifier:"], "header_lines": 5},
    )
    for case, code in (("compliant", 0), ("violation", 1)):
        ledger = tmp_path / f"{case}.json"
        started = datetime.now(UTC)
        result = invoke(manifest, case, ledger, timeout=10)
        assert result.returncode == code
        validate_contract_ledger(manifest, case, ledger, process_exit=code, started_after=started)


@pytest.mark.parametrize("allow_missing", [True, False, []])
def test_mutation_contract_rejects_removed_missing_input_override(
    tmp_path: Path, allow_missing: object
) -> None:
    manifest = contract_for(
        tmp_path, "core:mutation_survival_ratchet", {"allow_missing_current": allow_missing}
    )
    ledger = tmp_path / "ledger.json"
    assert invoke(manifest, "compliant", ledger, timeout=10).returncode == 2
    assert not ledger.exists()


def test_mutation_baseline_report_is_bound_input_not_suppression(tmp_path: Path) -> None:
    manifest = contract_for(
        tmp_path,
        "core:mutation_survival_ratchet",
        {"baseline_report": "before.json", "current_report": "after.json"},
    )
    report = json.dumps({"schema_version": 1, "packages": {"app": {"survived": 0, "killed": 3}}})
    for name in ("before.json", "after.json"):
        (tmp_path / "compliant" / name).write_text(report)
    ledger = tmp_path / "ledger.json"
    started = datetime.now(UTC)
    result = invoke(manifest, "compliant", ledger, timeout=10)
    assert result.returncode == 0
    validate_contract_ledger(manifest, "compliant", ledger, process_exit=0, started_after=started)
    (tmp_path / "compliant" / "before.json").write_text(report + "\n")
    with pytest.raises(CheckContractError, match="fixture_digest"):
        validate_contract_ledger(manifest, "compliant", ledger, process_exit=0, started_after=started)
