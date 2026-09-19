"""Real filesystem and process proof of public check-contract execution."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
import yaml

pytestmark = pytest.mark.integration


def make_contract(root: Path, *, dependency: bool = False) -> Path:
    finding = {"rule": "license-present", "path": "src/example.py", "message_contains": "license header"}
    cases = [
        {
            "id": "compliant",
            "fixture": "compliant",
            "expected": {"status": "pass", "exit": "zero", "findings": []},
        },
        {
            "id": "violation",
            "fixture": "violation",
            "expected": {"status": "fail", "exit": "nonzero", "findings": [finding]},
        },
    ]
    dependencies = []
    if dependency:
        dependencies = ["python3"]
        cases.append(
            {
                "id": "unavailable",
                "fixture": "unavailable",
                "environment": {"schema": "tc.fitness/check-environment/v1", "path": "empty"},
                "expected": {
                    "status": "error",
                    "exit": "nonzero",
                    "findings": [
                        {
                            "rule": "dependency-unavailable",
                            "path": ".",
                            "message_contains": dependencies[0],
                        }
                    ],
                },
            }
        )
    for case in cases:
        folder = root / case["fixture"] / "src"
        folder.mkdir(parents=True)
        text = "value = 1\n" if case["id"] == "violation" else "# SPDX-License-Identifier: MIT\nvalue = 1\n"
        if dependency:
            text = "import argparse\ndef main():\n    argparse.ArgumentParser()\n"
            text += "raise SystemExit(1)\n" if case["id"] == "violation" else "main()\n"
        (folder / "example.py").write_text(text)
    if dependency:
        cases[1]["expected"]["findings"] = [
            {"rule": "script-help-smoke", "path": "src/example.py", "message_contains": "--help"}
        ]
    manifest = root / "contract.yaml"
    manifest.write_text(
        yaml.safe_dump(
            {
                "schema": "tc.fitness/check-contract/v1",
                "check": "core:script_help_smoke" if dependency else "core:license_present",
                "config": {"roots": ["src"], "python_executable": "python3"}
                if dependency
                else {"roots": ["src"]},
                "cases": cases,
                "dependencies": dependencies,
            }
        )
    )
    return manifest


def invoke(
    manifest: Path, case: str, ledger: Path, *extra: str, timeout: float | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            str(Path(sys.executable).with_name("tc-fitness")),
            "run",
            "--contract",
            str(manifest),
            "--case",
            case,
            "--ledger",
            str(ledger),
            *extra,
        ],
        text=True,
        capture_output=True,
        check=False,
        env=dict(os.environ),
        timeout=timeout,
    )


def _fast_import_single_file(path: str, content: bytes) -> bytes:
    """One deterministic commit plus a remote base ref for a real Git fixture."""
    return (
        b"blob\nmark :1\ndata "
        + str(len(content)).encode()
        + b"\n"
        + content
        + b"\ncommit refs/heads/candidate\nmark :2\n"
        + b"author Contract Fixture <fixture@example.invalid> 0 +0000\n"
        + b"committer Contract Fixture <fixture@example.invalid> 0 +0000\n"
        + b"data 7\ninitial\n"
        + f"M 100644 :1 {path}\n\n".encode()
        + b"reset refs/remotes/origin/main\nfrom :2\n\n"
    )


def test_public_contract_materialises_bound_git_history(tmp_path: Path) -> None:
    manifest = make_contract(tmp_path)
    fixture = tmp_path / "compliant"
    for path in sorted((fixture / "src").rglob("*"), reverse=True):
        if path.is_file():
            path.unlink()
        else:
            path.rmdir()
    (fixture / "src").rmdir()
    history = fixture / ".contract" / "git.fast-import"
    history.parent.mkdir()
    history.write_bytes(
        _fast_import_single_file("src/example.py", b"# SPDX-License-Identifier: MIT\nvalue = 1\n")
    )
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
    ledger = tmp_path / "git-ledger.json"

    result = invoke(manifest, "compliant", ledger)

    assert result.returncode == 0, result.stderr
    evidence = json.loads(ledger.read_text())
    assert evidence["actual"] == {"exit": "zero", "exit_code": 0, "findings": [], "status": "pass"}
    assert evidence["environment"]["git"] == {
        "checkout": "refs/heads/candidate",
        "history": ".contract/git.fast-import",
        "schema": "tc.fitness/git-fixture/v1",
    }


@pytest.mark.parametrize(
    ("case", "status", "exit_code"),
    [("compliant", "pass", 0), ("violation", "fail", 1), ("unavailable", "error", 2)],
)
def test_public_command_emits_real_case_evidence(
    tmp_path: Path, case: str, status: str, exit_code: int
) -> None:
    manifest = make_contract(tmp_path, dependency=case == "unavailable")
    ledger = tmp_path / "ledger.json"
    result = invoke(manifest, case, ledger)
    assert ledger.is_file(), result.stderr
    evidence = json.loads(ledger.read_text())
    assert result.returncode == exit_code
    assert evidence["schema"] == "tc.fitness/check-ledger/v1"
    assert evidence["check"] == (
        "core:script_help_smoke" if case == "unavailable" else "core:license_present"
    )
    assert evidence["case_id"] == case
    assert evidence["actual"]["status"] == status
    assert evidence["actual"]["exit_code"] == exit_code
    if case == "compliant":
        assert evidence["actual"]["findings"] == []
    elif case == "violation":
        assert evidence["actual"]["findings"][0]["rule"] == "license-present"
        assert evidence["actual"]["findings"][0]["path"] == "src/example.py"
        assert "license header" in evidence["actual"]["findings"][0]["message"]
    else:
        assert evidence["actual"]["findings"][0]["rule"] == "dependency-unavailable"
    assert evidence["candidate"]["package_version"]
    assert evidence["candidate"]["source_digest"].startswith("sha256:")
    assert evidence["fixture_digest"].startswith("sha256:")
    assert evidence["payload_digest"].startswith("sha256:")
    assert evidence["started_at"] <= evidence["finished_at"]


def validate(manifest: Path, case: str, ledger: Path, exit_code: int, started: datetime) -> object:
    from tc_fitness import check_contract_execution

    validator = getattr(check_contract_execution, "validate_contract_ledger", None)
    assert callable(validator), "structured ledger validator is missing"
    return validator(manifest, case, ledger, process_exit=exit_code, started_after=started)


def rewrite_ledger(ledger: Path, evidence: dict) -> None:
    evidence.pop("payload_digest", None)
    encoded = json.dumps(evidence, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    evidence["payload_digest"] = "sha256:" + hashlib.sha256(encoded).hexdigest()
    ledger.write_text(json.dumps(evidence))


@pytest.mark.parametrize("case", ["compliant", "violation", "unavailable"])
def test_validator_accepts_only_the_expected_terminal_outcome(tmp_path: Path, case: str) -> None:
    manifest = make_contract(tmp_path, dependency=case == "unavailable")
    ledger = tmp_path / "ledger.json"
    started = datetime.now(UTC)
    result = invoke(manifest, case, ledger)
    assert validate(manifest, case, ledger, result.returncode, started)["case_id"] == case


@pytest.mark.parametrize(
    "sabotage",
    [
        "missing-ledger",
        "wrong-process-exit",
        "wrong-exit-code",
        "wrong-exit-class",
        "wrong-status",
        "wrong-rule",
        "wrong-path",
        "wrong-message",
        "missing-finding",
        "extra-finding",
        "wrong-check",
        "wrong-case",
        "wrong-fixture",
        "wrong-contract",
        "wrong-candidate",
        "wrong-version",
        "wrong-expectation",
        "stale",
        "future",
        "reversed-time",
        "digest-mismatch",
        "invalid-json",
        "wrong-schema",
        "wrong-case-digest",
    ],
)
def test_validator_rejects_sabotaged_real_command_evidence(tmp_path: Path, sabotage: str) -> None:
    from tc_fitness.check_contracts import CheckContractError

    manifest = make_contract(tmp_path)
    ledger = tmp_path / "ledger.json"
    started = datetime.now(UTC)
    result = invoke(manifest, "violation", ledger)
    assert result.returncode == 1
    evidence = json.loads(ledger.read_text())
    actual = evidence["actual"]
    exit_code = result.returncode
    if sabotage == "missing-ledger":
        ledger.unlink()
    elif sabotage == "invalid-json":
        ledger.write_text("[")
    else:
        if sabotage == "wrong-process-exit":
            exit_code = 0
        elif sabotage == "wrong-exit-code":
            actual["exit_code"] = 2
        elif sabotage == "wrong-exit-class":
            actual["exit"] = "zero"
        elif sabotage == "wrong-status":
            actual["status"] = "error"
        elif sabotage in {"wrong-rule", "wrong-path", "wrong-message"}:
            actual["findings"][0][sabotage.removeprefix("wrong-")] = "unrelated"
        elif sabotage == "missing-finding":
            actual["findings"] = []
        elif sabotage == "extra-finding":
            actual["findings"].append(
                {"rule": "unrelated", "path": ".", "message": "unrelated failure", "status": "fail"}
            )
        elif sabotage == "wrong-check":
            evidence["check"] = "core:deterministic_tests"
        elif sabotage == "wrong-case":
            evidence["case_id"] = "compliant"
        elif sabotage in {"wrong-fixture", "wrong-contract", "wrong-case-digest"}:
            field = {
                "wrong-fixture": "fixture_digest",
                "wrong-contract": "contract_digest",
                "wrong-case-digest": "case_digest",
            }[sabotage]
            evidence[field] = "sha256:" + "0" * 64
        elif sabotage == "wrong-candidate":
            evidence["candidate"]["source_digest"] = "sha256:" + "0" * 64
        elif sabotage == "wrong-version":
            evidence["candidate"]["package_version"] = "0.0.0"
        elif sabotage == "wrong-expectation":
            evidence["expected"]["status"] = "pass"
        elif sabotage == "stale":
            evidence["started_at"] = (started - timedelta(days=1)).isoformat()
        elif sabotage == "future":
            evidence["finished_at"] = (started + timedelta(days=1)).isoformat()
        elif sabotage == "reversed-time":
            evidence["finished_at"] = (started - timedelta(days=1)).isoformat()
        elif sabotage == "wrong-schema":
            evidence["schema"] = "unrecognised"
        rewrite_ledger(ledger, evidence)
        if sabotage == "digest-mismatch":
            evidence = json.loads(ledger.read_text())
            evidence["payload_digest"] = "sha256:" + "0" * 64
            ledger.write_text(json.dumps(evidence))
    with pytest.raises(CheckContractError):
        validate(manifest, "violation", ledger, exit_code, started)


def test_unrelated_check_crash_does_not_satisfy_violation(tmp_path: Path) -> None:
    from tc_fitness.check_contracts import CheckContractError

    manifest = make_contract(tmp_path)
    config = yaml.safe_load(manifest.read_text())
    config["config"]["header_lines"] = "not an integer"
    manifest.write_text(yaml.safe_dump(config))
    ledger = tmp_path / "ledger.json"
    started = datetime.now(UTC)
    result = invoke(manifest, "violation", ledger)
    evidence = json.loads(ledger.read_text())
    assert result.returncode == 2
    assert evidence["actual"]["status"] == "error"
    assert evidence["actual"]["findings"][0]["rule"] == "check-execution-error"
    with pytest.raises(CheckContractError):
        validate(manifest, "violation", ledger, result.returncode, started)


@pytest.mark.parametrize("case", ["compliant", "violation", "unavailable"])
def test_case_runner_invokes_and_validates_the_public_command(tmp_path: Path, case: str) -> None:
    from tc_fitness import check_contract_execution

    manifest = make_contract(tmp_path, dependency=case == "unavailable")
    runner = getattr(check_contract_execution, "run_contract_case", None)
    assert callable(runner), "public process contract runner is missing"
    evidence = runner(manifest, case, tmp_path / "ledger.json")
    assert evidence["case_id"] == case


@pytest.mark.parametrize(
    "extra",
    [
        ["--repo-root", "."],
        ["--only", "ruff"],
        ["--gate", "anything"],
        ["--staged"],
        ["--changed-files-from", "paths.txt"],
        ["--shard", "1/2"],
        ["--tier", "smoke"],
        ["--establish-baseline"],
    ],
)
def test_contract_mode_rejects_normal_gate_selectors(tmp_path: Path, extra: list[str]) -> None:
    manifest = make_contract(tmp_path)
    ledger = tmp_path / "ledger.json"
    result = invoke(manifest, "compliant", ledger, *extra)
    assert result.returncode == 2
    assert not ledger.exists()


@pytest.mark.parametrize("omitted", ["--contract", "--case", "--ledger"])
def test_contract_arguments_are_required_together(tmp_path: Path, omitted: str) -> None:
    manifest = make_contract(tmp_path)
    arguments = {
        "--contract": str(manifest),
        "--case": "compliant",
        "--ledger": str(tmp_path / "ledger.json"),
    }
    args = [value for flag, arg in arguments.items() if flag != omitted for value in (flag, arg)]
    (tmp_path / ".tc-fitness.toml").write_text(
        '[[steps]]\nid = "minimal"\nrun = ' + json.dumps([sys.executable, "-c", "pass"]) + "\n"
    )
    result = subprocess.run(
        [str(Path(sys.executable).with_name("tc-fitness")), "run", *args],
        cwd=tmp_path,
        check=False,
        capture_output=True,
    )
    assert result.returncode == 2
    assert not (tmp_path / "ledger.json").exists()


def test_existing_ledger_is_preserved_for_retry(tmp_path: Path) -> None:
    manifest = make_contract(tmp_path)
    ledger = tmp_path / "ledger.json"
    assert invoke(manifest, "compliant", ledger).returncode == 0
    original = ledger.read_bytes()
    assert invoke(manifest, "violation", ledger).returncode == 2
    assert ledger.read_bytes() == original


@pytest.mark.parametrize("sabotage", ["outside-fixture", "symlink", "baseline", "unregistered-check"])
def test_case_setup_rejects_unbound_or_suppressed_inputs(tmp_path: Path, sabotage: str) -> None:
    manifest = make_contract(tmp_path)
    data = yaml.safe_load(manifest.read_text())
    if sabotage == "outside-fixture":
        data["cases"][0]["fixture"] = str(tmp_path / "compliant")
    elif sabotage == "symlink":
        (tmp_path / "compliant" / "src" / "external.py").symlink_to(
            tmp_path / "violation" / "src" / "example.py"
        )
    elif sabotage == "baseline":
        baseline = tmp_path / "compliant" / ".architecture" / "baseline"
        baseline.mkdir(parents=True)
        (baseline / "license-present-files.txt").write_text("src/example.py\n")
    else:
        data["check"] = "core:__init__"
    manifest.write_text(yaml.safe_dump(data))
    ledger = tmp_path / "ledger.json"
    result = invoke(manifest, "compliant", ledger)
    assert result.returncode == 2
    assert not ledger.exists()


def test_changed_fixture_invalidates_an_otherwise_valid_ledger(tmp_path: Path) -> None:
    from tc_fitness.check_contracts import CheckContractError

    manifest = make_contract(tmp_path)
    ledger = tmp_path / "ledger.json"
    started = datetime.now(UTC)
    result = invoke(manifest, "compliant", ledger)
    (tmp_path / "compliant" / "src" / "example.py").write_text("value = 2\n")
    with pytest.raises(CheckContractError, match="fixture_digest"):
        validate(manifest, "compliant", ledger, result.returncode, started)


def test_duplicate_json_keys_cannot_disguise_ledger_identity(tmp_path: Path) -> None:
    from tc_fitness.check_contracts import CheckContractError

    manifest = make_contract(tmp_path)
    ledger = tmp_path / "ledger.json"
    started = datetime.now(UTC)
    result = invoke(manifest, "compliant", ledger)
    ledger.write_text(ledger.read_text().replace("{", '{"check": "core:unrelated",', 1))
    with pytest.raises(CheckContractError, match="duplicate"):
        validate(manifest, "compliant", ledger, result.returncode, started)


def test_ledger_cannot_be_written_inside_the_fixture(tmp_path: Path) -> None:
    manifest = make_contract(tmp_path)
    ledger = tmp_path / "compliant" / "evidence.json"
    result = invoke(manifest, "compliant", ledger)
    assert result.returncode == 2
    assert not ledger.exists()


def test_fixture_cannot_traverse_a_symlinked_parent(tmp_path: Path) -> None:
    manifest = make_contract(tmp_path)
    (tmp_path / "shortcut").symlink_to(tmp_path, target_is_directory=True)
    data = yaml.safe_load(manifest.read_text())
    data["cases"][0]["fixture"] = "shortcut/compliant"
    manifest.write_text(yaml.safe_dump(data))
    result = invoke(manifest, "compliant", tmp_path / "ledger.json")
    assert result.returncode == 2
    assert not (tmp_path / "ledger.json").exists()


def test_fixture_permission_changes_invalidate_evidence(tmp_path: Path) -> None:
    from tc_fitness.check_contracts import CheckContractError

    manifest = make_contract(tmp_path)
    ledger = tmp_path / "ledger.json"
    started = datetime.now(UTC)
    result = invoke(manifest, "compliant", ledger)
    source = tmp_path / "compliant" / "src" / "example.py"
    source.chmod(source.stat().st_mode ^ 0o100)
    with pytest.raises(CheckContractError, match="fixture_digest"):
        validate(manifest, "compliant", ledger, result.returncode, started)


@pytest.mark.parametrize("case", ["compliant", "violation", "unavailable", "crash"])
def test_embedded_public_entrypoint_retains_evidence_and_restores_outer_capture(
    tmp_path: Path, case: str
) -> None:
    from tc_fitness.check_evidence import capture_check_evidence, report_finding
    from tc_fitness.gate import main

    manifest = make_contract(tmp_path, dependency=case == "unavailable")
    if case == "crash":
        data = yaml.safe_load(manifest.read_text())
        data["config"]["header_lines"] = "invalid"
        manifest.write_text(yaml.safe_dump(data))
    ledger = tmp_path / "ledger.json"
    original_path = os.environ.get("PATH")
    with capture_check_evidence() as outer:
        exit_code = main(
            [
                "run",
                "--contract",
                str(manifest),
                "--case",
                "violation" if case == "crash" else case,
                "--ledger",
                str(ledger),
            ]
        )
        report_finding("outer", ".", "outer context restored")
    evidence = json.loads(ledger.read_text())
    assert (
        evidence["actual"]["status"]
        == {"compliant": "pass", "violation": "fail", "unavailable": "error", "crash": "error"}[case]
    )
    assert evidence["actual"]["exit_code"] == exit_code
    assert [finding.rule for finding in outer.findings] == ["outer"]
    assert outer.results == []
    assert os.environ.get("PATH") == original_path


@pytest.mark.parametrize(
    "sabotage",
    [
        "unknown-case",
        "unregistered-check",
        "missing-fixture",
        "absolute-fixture",
        "symlink",
        "baseline",
        "existing-ledger",
        "ledger-in-fixture",
    ],
)
def test_embedded_public_entrypoint_fails_closed_on_invalid_setup(tmp_path: Path, sabotage: str) -> None:
    from tc_fitness.gate import main

    manifest = make_contract(tmp_path)
    data = yaml.safe_load(manifest.read_text())
    case = "compliant"
    ledger = tmp_path / "ledger.json"
    if sabotage == "unknown-case":
        case = "absent"
    elif sabotage == "unregistered-check":
        data["check"] = "core:absent"
    elif sabotage in {"missing-fixture", "absolute-fixture"}:
        data["cases"][0]["fixture"] = (
            "absent" if sabotage == "missing-fixture" else str(tmp_path / "compliant")
        )
    elif sabotage == "symlink":
        (tmp_path / "compliant" / "linked").symlink_to(tmp_path / "violation")
    elif sabotage == "baseline":
        (tmp_path / "compliant" / ".architecture" / "baseline").mkdir(parents=True)
    elif sabotage == "existing-ledger":
        ledger.write_text("retained evidence")
    else:
        ledger = tmp_path / "compliant" / "ledger.json"
    manifest.write_text(yaml.safe_dump(data))
    assert main(["run", "--contract", str(manifest), "--case", case, "--ledger", str(ledger)]) == 2


@pytest.mark.parametrize(
    "damage",
    [
        "bad-findings-list",
        "bad-finding-type",
        "bad-field-type",
        "bad-finding-status",
        "invalid-id",
        "invalid-timestamp",
        "missing-field",
        "array-root",
        "boolean-exit",
    ],
)
def test_malformed_signed_evidence_has_a_domain_error(tmp_path: Path, damage: str) -> None:
    from tc_fitness.check_contracts import CheckContractError

    manifest = make_contract(tmp_path)
    ledger = tmp_path / "ledger.json"
    started = datetime.now(UTC)
    result = invoke(manifest, "violation", ledger)
    evidence = json.loads(ledger.read_text())
    if damage == "bad-findings-list":
        evidence["actual"]["findings"] = "not a list"
    elif damage == "bad-finding-type":
        evidence["actual"]["findings"] = [1]
    elif damage == "bad-field-type":
        evidence["actual"]["findings"][0]["message"] = 1
    elif damage == "bad-finding-status":
        evidence["actual"]["findings"][0]["status"] = "error"
    elif damage == "invalid-id":
        evidence["execution_id"] = "invalid"
    elif damage == "invalid-timestamp":
        evidence["started_at"] = "invalid"
    elif damage == "boolean-exit":
        evidence["actual"]["exit_code"] = True
    elif damage == "missing-field":
        del evidence["candidate"]
    rewrite_ledger(ledger, evidence)
    if damage == "array-root":
        ledger.write_text("[]")
    with pytest.raises(CheckContractError):
        validate(manifest, "violation", ledger, result.returncode, started)


def test_validator_rejects_unknown_case(tmp_path: Path) -> None:
    from tc_fitness.check_contracts import CheckContractError

    manifest = make_contract(tmp_path)
    with pytest.raises(CheckContractError, match="unknown contract case"):
        validate(manifest, "absent", tmp_path / "absent.json", 0, datetime.now(UTC))
