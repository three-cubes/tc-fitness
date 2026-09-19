"""Adversarial real-process tests for baseline-free, immutable contract proof."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml
from test_check_contract_execution import invoke, make_contract

pytestmark = pytest.mark.integration


def run_case(manifest: Path, ledger: Path, entrypoint: str) -> int:
    if entrypoint == "process":
        return invoke(manifest, "compliant", ledger).returncode
    from tc_fitness.gate import main

    return main(["run", "--contract", str(manifest), "--case", "compliant", "--ledger", str(ledger)])


@pytest.mark.parametrize(
    "environment",
    [
        {"schema": "unknown", "path": "empty"},
        {"schema": "tc.fitness/check-environment/v1", "path": "/host/tools"},
        {"schema": "tc.fitness/check-environment/v1", "path": []},
        {"schema": "tc.fitness/check-environment/v1", "path": {}},
        {"schema": "tc.fitness/check-environment/v1", "path": "empty", "other": "ignored"},
        "empty",
    ],
)
def test_case_environment_is_versioned_and_fail_closed(tmp_path: Path, environment: object) -> None:
    from tc_fitness.check_contracts import CheckContractError, load_check_contract

    manifest = make_contract(tmp_path, dependency=True)
    data = yaml.safe_load(manifest.read_text())
    data["cases"][-1]["environment"] = environment
    manifest.write_text(yaml.safe_dump(data))
    with pytest.raises(CheckContractError, match="environment"):
        load_check_contract(manifest)


def test_only_unavailable_case_may_change_the_process_search_path(tmp_path: Path) -> None:
    from tc_fitness.check_contracts import CheckContractError, load_check_contract

    manifest = make_contract(tmp_path)
    data = yaml.safe_load(manifest.read_text())
    data["cases"][0]["environment"] = {"schema": "tc.fitness/check-environment/v1", "path": "empty"}
    manifest.write_text(yaml.safe_dump(data))
    with pytest.raises(CheckContractError, match="unavailable"):
        load_check_contract(manifest)


def test_versioned_git_environment_accepts_bound_fast_import_history(tmp_path: Path) -> None:
    from tc_fitness.check_contracts import load_check_contract

    manifest = make_contract(tmp_path)
    data = yaml.safe_load(manifest.read_text())
    data["cases"][0]["environment"] = {
        "schema": "tc.fitness/check-environment/v2",
        "path": "inherit",
        "git": {
            "schema": "tc.fitness/git-fixture/v1",
            "history": ".contract/git.fast-import",
            "checkout": "refs/heads/candidate",
        },
    }
    manifest.write_text(yaml.safe_dump(data))

    environment = load_check_contract(manifest).cases[0].environment
    assert environment.schema == "tc.fitness/check-environment/v2"
    assert environment.git is not None
    assert environment.git.history == ".contract/git.fast-import"
    assert environment.git.checkout == "refs/heads/candidate"


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("history", "/tmp/history", "portable path"),
        ("history", "../history", "portable path"),
        ("history", "history.fast-import", ".contract"),
        ("checkout", "HEAD", "refs/heads"),
        ("checkout", "refs/heads/candidate;echo", "refs/heads"),
    ],
)
def test_versioned_git_environment_rejects_unsafe_materialisation(
    tmp_path: Path, field: str, value: str, message: str
) -> None:
    from tc_fitness.check_contracts import CheckContractError, load_check_contract

    manifest = make_contract(tmp_path)
    data = yaml.safe_load(manifest.read_text())
    git = {
        "schema": "tc.fitness/git-fixture/v1",
        "history": ".contract/git.fast-import",
        "checkout": "refs/heads/candidate",
    }
    git[field] = value
    data["cases"][0]["environment"] = {
        "schema": "tc.fitness/check-environment/v2",
        "path": "inherit",
        "git": git,
    }
    manifest.write_text(yaml.safe_dump(data))

    with pytest.raises(CheckContractError, match=message):
        load_check_contract(manifest)


@pytest.mark.parametrize("root", ["/outside", "../outside"])
def test_configured_scan_root_cannot_escape_the_bound_fixture(tmp_path: Path, root: str) -> None:
    manifest = make_contract(tmp_path)
    data = yaml.safe_load(manifest.read_text())
    data["config"]["roots"] = [root]
    manifest.write_text(yaml.safe_dump(data))
    assert run_case(manifest, tmp_path / "ledger.json", "embedded") == 2
    assert not (tmp_path / "ledger.json").exists()


def test_validator_reports_missing_manifest_snapshot_as_domain_error(tmp_path: Path) -> None:
    from datetime import UTC, datetime

    from tc_fitness.check_contract_execution import validate_contract_ledger
    from tc_fitness.check_contracts import CheckContractError

    with pytest.raises(CheckContractError, match="contract snapshot"):
        validate_contract_ledger(
            tmp_path / "missing.yaml",
            "compliant",
            tmp_path / "missing.json",
            process_exit=0,
            started_after=datetime.now(UTC),
        )


def script_contract(root: Path, body: str) -> Path:
    manifest = make_contract(root)
    data = yaml.safe_load(manifest.read_text())
    data["check"] = "core:script_help_smoke"
    data["config"] = {"roots": ["src"], "python_executable": "python3"}
    data["cases"][1]["expected"]["findings"] = [
        {
            "rule": "script-help-smoke",
            "path": "src/example.py",
            "message_contains": "--help",
        }
    ]
    manifest.write_text(yaml.safe_dump(data))
    script = (
        "import argparse\nfrom pathlib import Path\n\ndef main():\n    parser = argparse.ArgumentParser()\n"
        + body
    )
    (root / "compliant" / "src" / "example.py").write_text(script)
    return manifest


@pytest.mark.parametrize("entrypoint", ["process", "embedded"])
def test_real_help_script_cannot_change_manifest_and_attest_new_bytes(
    tmp_path: Path, entrypoint: str
) -> None:
    target = tmp_path / "contract.yaml"
    manifest = script_contract(
        tmp_path,
        f"""
manifest = Path({str(target)!r})
manifest.write_text(manifest.read_text() + '\\n# changed during execution\\n')
main()
""",
    )
    before = manifest.read_bytes()
    result = run_case(manifest, tmp_path / "ledger.json", entrypoint)
    assert manifest.read_bytes() != before
    assert result == 2
    assert not (tmp_path / "ledger.json").exists()


@pytest.mark.parametrize("entrypoint", ["process", "embedded"])
def test_real_help_script_cannot_change_original_fixture_during_execution(
    tmp_path: Path, entrypoint: str
) -> None:
    target = tmp_path / "compliant" / "src" / "example.py"
    manifest = script_contract(
        tmp_path,
        f"""
source = Path({str(target)!r})
source.write_text(source.read_text() + '\\n# changed original fixture\\n')
main()
""",
    )
    assert run_case(manifest, tmp_path / "ledger.json", entrypoint) == 2
    assert not (tmp_path / "ledger.json").exists()


def test_real_help_script_cannot_change_candidate_source_during_execution(tmp_path: Path) -> None:
    import tc_fitness

    candidate = tmp_path / "candidate" / "tc_fitness"
    shutil.copytree(Path(tc_fitness.__file__).parent, candidate, ignore=shutil.ignore_patterns("__pycache__"))
    target = candidate / "lib.py"
    manifest = script_contract(
        tmp_path,
        f"""
source = Path({str(target)!r})
source.write_text(source.read_text() + '\\n# changed candidate source\\n')
main()
""",
    )
    ledger = tmp_path / "ledger.json"
    result = subprocess.run(
        [
            str(Path(sys.executable).with_name("tc-fitness")),
            "run",
            "--contract",
            str(manifest),
            "--case",
            "compliant",
            "--ledger",
            str(ledger),
        ],
        env={**os.environ, "PYTHONPATH": str(candidate.parent)},
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 2
    assert not ledger.exists()


def test_generic_dependency_declaration_cannot_synthesize_unavailable_detector_evidence(
    tmp_path: Path,
) -> None:
    manifest = make_contract(tmp_path, dependency=True)
    data = yaml.safe_load(manifest.read_text())
    data["check"] = "core:license_present"
    data["config"] = {"roots": ["src"]}
    data["dependencies"] = ["tc-fitness-intentionally-unavailable-contract-tool"]
    manifest.write_text(yaml.safe_dump(data))
    (tmp_path / "unavailable" / "src" / "example.py").write_text("# SPDX-License-Identifier: MIT\n")
    result = invoke(manifest, "unavailable", tmp_path / "ledger.json")
    assert result.returncode == 0
    actual = json.loads((tmp_path / "ledger.json").read_text())["actual"]
    assert actual == {"status": "pass", "exit": "zero", "exit_code": 0, "findings": []}


def test_same_real_help_check_exercises_pass_violation_and_missing_interpreter(tmp_path: Path) -> None:
    manifest = script_contract(tmp_path, "main()\n")
    data = yaml.safe_load(manifest.read_text())
    data["dependencies"] = ["python3"]
    data["cases"].append(
        {
            "id": "unavailable",
            "fixture": "compliant",
            "environment": {"schema": "tc.fitness/check-environment/v1", "path": "empty"},
            "expected": {
                "status": "error",
                "exit": "nonzero",
                "findings": [
                    {
                        "rule": "dependency-unavailable",
                        "path": ".",
                        "message_contains": "python3",
                    }
                ],
            },
        }
    )
    (tmp_path / "violation" / "src" / "example.py").write_text(
        "import argparse\ndef main():\n    argparse.ArgumentParser()\nraise SystemExit(1)\n"
    )
    manifest.write_text(yaml.safe_dump(data))
    results = []
    for case in ("compliant", "violation", "unavailable"):
        ledger = tmp_path / f"{case}.json"
        result = invoke(manifest, case, ledger)
        results.append((result.returncode, json.loads(ledger.read_text())["actual"]["status"]))
    assert results == [(0, "pass"), (1, "fail"), (2, "error")]


@pytest.mark.parametrize("check", ["checkov_iac_security", "osv_scanner_sca"])
def test_real_required_scanner_reports_structured_error_with_empty_path(tmp_path: Path, check: str) -> None:
    manifest = make_contract(tmp_path)
    data = yaml.safe_load(manifest.read_text())
    data["check"] = f"core:{check}"
    data["config"] = (
        {"scan_dir": "src"}
        if check.startswith("checkov")
        else {"scanner_version": "2.3.0", "lockfiles": ["requirements.txt"], "required": True}
    )
    manifest.write_text(yaml.safe_dump(data))
    ledger = tmp_path / "ledger.json"
    result = subprocess.run(
        [
            str(Path(sys.executable).with_name("tc-fitness")),
            "run",
            "--contract",
            str(manifest),
            "--case",
            "compliant",
            "--ledger",
            str(ledger),
        ],
        env={**os.environ, "PATH": ""},
        capture_output=True,
        text=True,
        check=False,
    )
    actual = json.loads(ledger.read_text())["actual"]
    assert result.returncode == 2
    assert actual["status"] == "error"
    assert actual["findings"][0]["rule"] == "dependency-unavailable"
