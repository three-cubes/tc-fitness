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


def test_validator_rejects_a_check_without_reviewed_configuration(tmp_path: Path) -> None:
    manifest = contract_for(tmp_path, "core:unreviewed_check", {})
    with pytest.raises(CheckContractError, match="no reviewed contract configuration"):
        validate_contract_ledger(
            manifest, "compliant", tmp_path / "ledger.json", process_exit=0, started_after=datetime.now(UTC)
        )


def test_disabling_adoption_flags_keeps_the_real_ci_violation(tmp_path: Path) -> None:
    manifest = contract_for(
        tmp_path, "core:ci_consumes_shared_gate", {"warn_only": False, "baseline_ok": False}
    )
    workflow = tmp_path / "compliant" / ".github" / "workflows" / "ci.yml"
    workflow.parent.mkdir(parents=True)
    workflow.write_text("jobs:\n  quality:\n    steps:\n      - run: pytest\n")
    ledger = tmp_path / "ledger.json"
    assert invoke(manifest, "compliant", ledger, timeout=10).returncode == 1
    assert json.loads(ledger.read_text())["actual"]["status"] == "fail"


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


@pytest.mark.parametrize("option", ["warn_only", "baseline_ok"])
def test_ordinary_consumer_keeps_explicit_adoption_behaviour(tmp_path: Path, option: str) -> None:
    workflow = tmp_path / ".github" / "workflows" / "ci.yml"
    workflow.parent.mkdir(parents=True)
    workflow.write_text("jobs:\n  quality:\n    steps:\n      - run: pytest\n")
    (tmp_path / "consumer_checks.py").write_text(
        "from tc_fitness.catalogue import RuleEntry\n"
        "ENTRIES = (RuleEntry(id='ci', gate='ci', check='core:ci_consumes_shared_gate'),)\n"
    )
    config = tmp_path / ".tc-fitness.toml"
    header = (
        "[[steps]]\nid = 'ci'\ncatalogue = 'consumer_checks:ENTRIES'\n[core_checks.ci_consumes_shared_gate]\n"
    )
    command = [str(Path(sys.executable).with_name("tc-fitness")), "run", "--repo-root", str(tmp_path)]
    config.write_text(header + f"{option} = false\n")
    assert subprocess.run(command, capture_output=True, check=False, timeout=10).returncode == 1
    config.write_text(header + f"{option} = true\n")
    assert subprocess.run(command, capture_output=True, check=False, timeout=10).returncode == 0


def test_normal_scope_and_license_policy_still_detect_the_violation(tmp_path: Path) -> None:
    manifest = contract_for(
        tmp_path,
        "core:license_present",
        {"roots": ["src"], "markers": ["SPDX-License-Identifier:"], "header_lines": 5, "exempt_files": []},
    )
    for case, code in (("compliant", 0), ("violation", 1)):
        ledger = tmp_path / f"{case}.json"
        started = datetime.now(UTC)
        result = invoke(manifest, case, ledger, timeout=10)
        assert result.returncode == code
        validate_contract_ledger(manifest, case, ledger, process_exit=code, started_after=started)


@pytest.mark.parametrize("allow_missing", [True, None])
def test_mutation_contract_requires_explicit_strict_missing_input_policy(
    tmp_path: Path, allow_missing: bool | None
) -> None:
    config: dict[str, object] = {}
    if allow_missing is not None:
        config["allow_missing_current"] = allow_missing
    manifest = contract_for(tmp_path, "core:mutation_survival_ratchet", config)
    ledger = tmp_path / "ledger.json"
    assert invoke(manifest, "compliant", ledger, timeout=10).returncode == 2
    assert not ledger.exists()


def test_mutation_baseline_report_is_bound_input_not_suppression(tmp_path: Path) -> None:
    manifest = contract_for(
        tmp_path,
        "core:mutation_survival_ratchet",
        {"baseline_report": "before.json", "current_report": "after.json", "allow_missing_current": False},
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
