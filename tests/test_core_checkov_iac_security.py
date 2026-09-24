"""Real Checkov contract tests for the absolute IaC security gate."""

from __future__ import annotations

import json
import os
import runpy
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from tc_fitness.catalogue import RuleEntry
from tc_fitness.core_checks.checkov_iac_security import (
    CheckovIacSecurity,
    CheckovScanError,
    _finding_line,
    _finding_path,
    _parse_report,
    build,
    checkov_binary,
    main,
    run_checkov,
)
from tc_fitness.runner import run

pytestmark = pytest.mark.integration
CONTRACT_ROOT = Path(__file__).parent / "check_contracts" / "checkov_iac_security"


def _iac_repo(tmp_path: Path) -> Path:
    infra = tmp_path / "infra"
    infra.mkdir(parents=True)
    for name, fixture in (("safe.bicep", "compliant"), ("unsafe.bicep", "violation")):
        shutil.copyfile(CONTRACT_ROOT / fixture / "infra" / "main.bicep", infra / name)
    return tmp_path


def test_compliant_storage_fixture_passes_real_checkov() -> None:
    rule = CheckovIacSecurity(CONTRACT_ROOT / "compliant", scan_dir="infra")

    passed, errors, meta = rule.evaluate()

    assert checkov_binary()
    assert (passed, errors) == (True, [])
    assert meta == {
        "unavailable": False,
        "execution_error": False,
        "exit_code": 0,
        "failed": 0,
        "parsing_errors": 0,
        "findings": [],
    }


def test_network_open_storage_fails_real_checkov_with_actionable_finding() -> None:
    rule = CheckovIacSecurity(CONTRACT_ROOT / "violation", scan_dir="infra")

    passed, errors, meta = rule.evaluate()

    assert not passed
    assert meta["failed"] >= 1
    assert meta["parsing_errors"] == 0
    assert any("CKV_AZURE_35" in line for line in errors)
    assert any("network access" in line.lower() for line in errors)


def test_violation_run_returns_failure_and_emits_structured_checkov_finding(
    capsys: pytest.CaptureFixture[str],
) -> None:
    rule = CheckovIacSecurity(CONTRACT_ROOT / "violation", scan_dir="infra")

    assert rule.run() == 1
    output = capsys.readouterr().out
    assert "CKV_AZURE_35" in output
    assert "FAIL checkov_iac_security" in output


def test_config_factory_and_public_run_use_the_configured_fixture(capsys: pytest.CaptureFixture[str]) -> None:
    rule = build(
        {"scan_dir": "compliant/infra", "framework": "bicep", "timeout": 60},
        repo_root=CONTRACT_ROOT,
    )

    assert rule.scan_path == (CONTRACT_ROOT / "compliant" / "infra").resolve()
    assert rule.run() == 0
    assert "PASS checkov_iac_security" in capsys.readouterr().out


def test_affected_scan_rejects_changed_vulnerable_file(tmp_path: Path) -> None:
    repo = _iac_repo(tmp_path)

    passed, errors, meta = CheckovIacSecurity(
        repo, scan_dir="infra", changed_files=["infra/unsafe.bicep"]
    ).evaluate()

    assert not passed
    assert meta["failed"] >= 1
    assert any("CKV_AZURE_35" in error for error in errors)


def test_affected_scan_excludes_unchanged_vulnerable_file_but_full_scan_finds_it(
    tmp_path: Path,
) -> None:
    repo = _iac_repo(tmp_path)

    affected_passed, _, affected_meta = CheckovIacSecurity(
        repo, scan_dir="infra", changed_files=["infra/safe.bicep"]
    ).evaluate()
    full_passed, _, full_meta = CheckovIacSecurity(repo, scan_dir="infra").evaluate()

    assert affected_passed
    assert affected_meta["failed"] == 0
    assert not full_passed
    assert full_meta["failed"] >= 1


def test_affected_scan_includes_local_module_dependency_closure(tmp_path: Path) -> None:
    repo = _iac_repo(tmp_path)
    (repo / "infra" / "safe.bicep").write_text(
        "module storage './unsafe.bicep' = {\n  name: 'storage'\n}\n", encoding="utf-8"
    )

    passed, errors, meta = CheckovIacSecurity(
        repo, scan_dir="infra", changed_files=["infra/safe.bicep"]
    ).evaluate()

    assert not passed
    assert meta["failed"] >= 1
    assert any("CKV_AZURE_35" in error for error in errors)


def test_module_outside_scan_directory_is_reported_at_repository_path(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    repo = _iac_repo(tmp_path)
    modules = repo / "modules"
    modules.mkdir()
    (repo / "infra" / "unsafe.bicep").rename(modules / "unsafe.bicep")
    (repo / "infra" / "safe.bicep").write_text(
        "module storage '../modules/unsafe.bicep' = {\n  name: 'storage'\n}\n",
        encoding="utf-8",
    )

    assert CheckovIacSecurity(repo, scan_dir="infra", changed_files=["infra/safe.bicep"]).run() == 1
    assert "at /modules/unsafe.bicep:" in capsys.readouterr().out
    result = run_checkov(modules, files=[modules / "unsafe.bicep"])
    assert result is not None
    finding = result[1]["results"]["failed_checks"][0]
    assert (
        _finding_path(finding, scan_path=repo / "infra", scan_dir="infra", repo_root=repo)
        == "modules/unsafe.bicep"
    )


def test_changed_external_module_scans_unchanged_in_scope_importer(tmp_path: Path) -> None:
    repo = _iac_repo(tmp_path)
    modules = repo / "modules"
    modules.mkdir()
    (repo / "infra" / "unsafe.bicep").rename(modules / "unsafe.bicep")
    (repo / "infra" / "safe.bicep").write_text(
        "module storage '../modules/unsafe.bicep' = {\n  name: 'storage'\n}\n",
        encoding="utf-8",
    )

    passed, errors, meta = CheckovIacSecurity(
        repo, scan_dir="infra", changed_files=["modules/unsafe.bicep"]
    ).evaluate()

    assert not passed
    assert meta["failed"] >= 1
    assert any("CKV_AZURE_35" in error for error in errors)


def test_deleted_external_module_imported_by_unchanged_template_fails_closed(
    tmp_path: Path,
) -> None:
    repo = _iac_repo(tmp_path)
    modules = repo / "modules"
    modules.mkdir()
    (repo / "infra" / "unsafe.bicep").rename(modules / "unsafe.bicep")
    (repo / "infra" / "safe.bicep").write_text(
        "module storage '../modules/unsafe.bicep' = {\n  name: 'storage'\n}\n",
        encoding="utf-8",
    )
    (modules / "unsafe.bicep").unlink()

    passed, errors, meta = CheckovIacSecurity(
        repo, scan_dir="infra", changed_files=["modules/unsafe.bicep"]
    ).evaluate()

    assert not passed
    assert meta["execution_error"] is True
    assert errors and "missing" in errors[0].lower()


def test_affected_scan_ignores_deleted_bicep_and_scans_rename_destination(tmp_path: Path) -> None:
    repo = _iac_repo(tmp_path)
    (repo / "infra" / "safe.bicep").unlink()
    (repo / "infra" / "unsafe.bicep").rename(repo / "infra" / "renamed.bicep")

    deleted_passed, _, deleted_meta = CheckovIacSecurity(
        repo, scan_dir="infra", changed_files=["infra/safe.bicep"]
    ).evaluate()
    renamed_passed, errors, renamed_meta = CheckovIacSecurity(
        repo, scan_dir="infra", changed_files=["infra/unsafe.bicep", "infra/renamed.bicep"]
    ).evaluate()

    assert deleted_passed
    assert deleted_meta["failed"] == 0
    assert not renamed_passed
    assert renamed_meta["failed"] >= 1
    assert any("CKV_AZURE_35" in error for error in errors)


def test_unresolvable_diff_base_fails_closed(tmp_path: Path) -> None:
    repo = _iac_repo(tmp_path)

    passed, errors, meta = CheckovIacSecurity(
        repo, scan_dir="infra", base_ref="refs/heads/does-not-exist"
    ).evaluate()

    assert not passed
    assert meta["execution_error"] is True
    assert errors and "base" in errors[0].lower()


def test_missing_configured_scan_directory_fails_affected_scan(tmp_path: Path) -> None:
    passed, errors, meta = CheckovIacSecurity(
        tmp_path, scan_dir="infra", changed_files=["infra/missing.bicep"]
    ).evaluate()

    assert not passed
    assert meta["execution_error"] is True
    assert errors and "scan directory" in errors[0].lower()


def test_ambient_checkov_skip_setting_cannot_hide_a_changed_finding(tmp_path: Path) -> None:
    repo = _iac_repo(tmp_path)
    (repo / ".checkov.yaml").write_text("skip-check: CKV_AZURE_35\n", encoding="utf-8")
    process = subprocess.run(
        [
            sys.executable,
            "-c",
            "from pathlib import Path; import json, sys; "
            "from tc_fitness.core_checks.checkov_iac_security import CheckovIacSecurity; "
            "print(json.dumps(CheckovIacSecurity(Path(sys.argv[1]), scan_dir='infra', "
            "changed_files=['infra/unsafe.bicep']).evaluate()))",
            str(repo),
        ],
        cwd=repo,
        env={**os.environ, "CKV_SKIP_CHECK": "CKV_AZURE_35"},
        capture_output=True,
        text=True,
        check=False,
    )

    assert process.returncode == 0
    passed, errors, meta = json.loads(process.stdout)
    assert not passed
    assert meta["failed"] >= 1
    assert any("CKV_AZURE_35" in error for error in errors)


def test_explicit_changed_files_manifest_is_used_by_direct_cli(tmp_path: Path) -> None:
    repo = _iac_repo(tmp_path)
    changed = repo / "changed-files.txt"
    changed.write_text("infra/safe.bicep\n", encoding="utf-8")

    assert main(["--repo-root", str(repo), "--changed-files-from", str(changed)]) == 0


def test_full_catalogue_mode_can_use_diff_scoped_checkov_config(tmp_path: Path) -> None:
    repo = _iac_repo(tmp_path)
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    subprocess.run(["git", "add", "infra"], cwd=repo, check=True)
    commit = [
        "git",
        "-c",
        "user.name=three-cubes-agent[bot]",
        "-c",
        "user.email=295831460+three-cubes-agent[bot]@users.noreply.github.com",
        "commit",
        "-qm",
        "fixture base",
    ]
    subprocess.run(commit, cwd=repo, check=True)
    base = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True, check=True
    ).stdout.strip()
    safe = repo / "infra" / "safe.bicep"
    safe.write_text(safe.read_text(encoding="utf-8") + "\n// changed\n", encoding="utf-8")
    subprocess.run(["git", "add", "infra/safe.bicep"], cwd=repo, check=True)
    subprocess.run(commit, cwd=repo, check=True)
    rules = (
        RuleEntry(
            id="checkov_iac_security",
            gate="checkov",
            check="core:checkov_iac_security",
            summary="IaC security",
        ),
    )

    verdict = run(
        rules,
        mode="all",
        repo_root=repo,
        core_check_configs={"checkov_iac_security": {"scan_dir": "infra", "base_ref": base}},
    )

    assert verdict.ok
    assert verdict.ran == 1


def test_base_ref_rename_detects_unchanged_importer_of_old_module_path(tmp_path: Path) -> None:
    repo = _iac_repo(tmp_path)
    modules = repo / "modules"
    modules.mkdir()
    (repo / "infra" / "unsafe.bicep").rename(modules / "old.bicep")
    (repo / "infra" / "safe.bicep").write_text(
        "module storage '../modules/old.bicep' = {\n  name: 'storage'\n}\n",
        encoding="utf-8",
    )
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    subprocess.run(["git", "add", "infra", "modules"], cwd=repo, check=True)
    commit = [
        "git",
        "-c",
        "user.name=three-cubes-agent[bot]",
        "-c",
        "user.email=295831460+three-cubes-agent[bot]@users.noreply.github.com",
        "commit",
        "-qm",
        "fixture",
    ]
    subprocess.run(commit, cwd=repo, check=True)
    base = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True, check=True
    ).stdout.strip()
    (modules / "old.bicep").rename(modules / "new.bicep")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    subprocess.run(commit, cwd=repo, check=True)

    passed, errors, meta = CheckovIacSecurity(repo, scan_dir="infra", base_ref=base).evaluate()

    assert not passed
    assert meta["execution_error"] is True
    assert errors and "missing" in errors[0].lower()


def test_staged_runner_passes_its_changed_files_to_checkov(tmp_path: Path) -> None:
    repo = _iac_repo(tmp_path)
    rules = (
        RuleEntry(
            id="checkov_iac_security",
            gate="checkov",
            check="core:checkov_iac_security",
            summary="IaC security",
            staged_class="file-local",
            staged_scope=("infra",),
        ),
    )

    verdict = run(
        rules,
        mode="staged",
        staged_files=["infra/safe.bicep"],
        repo_root=repo,
        core_check_configs={"checkov_iac_security": {"scan_dir": "infra"}},
    )

    assert verdict.ok
    assert verdict.ran == 1


def test_staged_runner_does_not_drop_changed_external_checkov_module(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    repo = _iac_repo(tmp_path)
    modules = repo / "modules"
    modules.mkdir()
    (repo / "infra" / "unsafe.bicep").rename(modules / "unsafe.bicep")
    (repo / "infra" / "safe.bicep").write_text(
        "module storage '../modules/unsafe.bicep' = {\n  name: 'storage'\n}\n",
        encoding="utf-8",
    )
    rules = (
        RuleEntry(
            id="checkov_iac_security",
            gate="checkov",
            check="core:checkov_iac_security",
            summary="IaC security",
            staged_class="file-local",
            staged_scope=("infra",),
        ),
    )

    verdict = run(
        rules,
        mode="staged",
        staged_files=["modules/unsafe.bicep"],
        repo_root=repo,
        core_check_configs={"checkov_iac_security": {"scan_dir": "infra"}},
    )

    assert checkov_binary()
    assert verdict.ran == 1
    assert verdict.failures == ["checkov_iac_security"]
    assert "CKV_AZURE_35" in capsys.readouterr().out


def test_staged_runner_with_no_paths_runs_full_checkov_scan_fail_safe(tmp_path: Path) -> None:
    repo = _iac_repo(tmp_path)
    rules = (
        RuleEntry(
            id="checkov_iac_security",
            gate="checkov",
            check="core:checkov_iac_security",
            summary="IaC security",
            staged_class="file-local",
            staged_scope=("infra",),
        ),
    )

    verdict = run(
        rules,
        mode="staged",
        staged_files=[],
        repo_root=repo,
        core_check_configs={"checkov_iac_security": {"scan_dir": "infra"}},
    )

    assert verdict.ran == 1
    assert verdict.failures == ["checkov_iac_security"]


def test_direct_cli_runs_the_real_scan_from_repository_root() -> None:
    assert main(["--repo-root", str(CONTRACT_ROOT / "compliant")]) == 0


def test_python_module_entrypoint_runs_the_real_scan() -> None:
    from tc_fitness.core_checks import checkov_iac_security

    original_argv = sys.argv
    sys.argv = [
        str(Path(checkov_iac_security.__file__)),
        "--repo-root",
        str(CONTRACT_ROOT / "compliant"),
    ]
    try:
        with pytest.raises(SystemExit) as result:
            runpy.run_path(str(Path(checkov_iac_security.__file__)), run_name="__main__")
        assert result.value.code == 0
    finally:
        sys.argv = original_argv


def test_missing_scanner_is_an_error_not_a_clean_result(tmp_path: Path) -> None:
    process = subprocess.run(
        [
            sys.executable,
            "-c",
            "from pathlib import Path; import json, sys; "
            "from tc_fitness.core_checks.checkov_iac_security import CheckovIacSecurity; "
            "print(json.dumps(CheckovIacSecurity(Path(sys.argv[1])).evaluate()))",
            str(tmp_path),
        ],
        env={**os.environ, "PATH": ""},
        capture_output=True,
        text=True,
        check=False,
    )

    assert process.returncode == 0
    passed, errors, meta = json.loads(process.stdout)
    assert not passed
    assert errors == []
    assert meta["unavailable"] is True


def test_missing_scanner_blocks_changed_scope_with_no_bicep_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = _iac_repo(tmp_path)
    monkeypatch.setenv("PATH", "")

    passed, errors, meta = CheckovIacSecurity(repo, scan_dir="infra", changed_files=["README.md"]).evaluate()

    assert not passed
    assert errors == []
    assert meta["unavailable"] is True


def test_run_checkov_reports_missing_scanner_directly(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("PATH", "")

    assert run_checkov(tmp_path) is None


def test_missing_scanner_run_reports_structured_error_without_test_doubles(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    previous_path = os.environ.get("PATH")
    os.environ["PATH"] = ""
    try:
        rule = CheckovIacSecurity(tmp_path)
        passed, errors, meta = rule.evaluate()
        assert not passed
        assert errors == []
        assert meta["unavailable"] is True
        assert rule.run() == 2
        assert "checkov is unavailable" in capsys.readouterr().out
    finally:
        if previous_path is None:
            os.environ.pop("PATH", None)
        else:
            os.environ["PATH"] = previous_path


def test_malformed_scanner_report_is_rejected() -> None:
    with pytest.raises(CheckovScanError, match="invalid JSON"):
        _parse_report("not-json")


def test_incomplete_scanner_report_is_rejected() -> None:
    with pytest.raises(CheckovScanError, match="missing results or summary"):
        _parse_report("{}")


@pytest.mark.parametrize(
    ("payload", "message"),
    [
        ("[]", "report list is empty"),
        ("[1]", "must be an object"),
        ('{"results": [], "summary": {}}', "missing results or summary"),
        (
            '{"results": {"failed_checks": [null]}, "summary": {"parsing_errors": 0}}',
            "invalid failed_checks",
        ),
        (
            '{"results": {"failed_checks": []}, "summary": {"parsing_errors": "0"}}',
            "invalid parsing_errors",
        ),
        (
            '{"results": {"failed_checks": []}, "summary": {"parsing_errors": true}}',
            "invalid parsing_errors",
        ),
        (
            '{"results": {"failed_checks": []}, "summary": {"parsing_errors": -1}}',
            "invalid parsing_errors",
        ),
    ],
)
def test_malformed_checkov_report_shapes_are_rejected(payload: str, message: str) -> None:
    with pytest.raises(CheckovScanError, match=message):
        _parse_report(payload)


def test_multi_framework_report_list_is_aggregated() -> None:
    payload = json.dumps(
        [
            {
                "results": {"failed_checks": [{"check_id": "CKV_1"}]},
                "summary": {"parsing_errors": 1},
            },
            {
                "results": {"failed_checks": [{"check_id": "CKV_2"}]},
                "summary": {"parsing_errors": 2},
            },
        ]
    )

    report = _parse_report(payload)

    assert [item["check_id"] for item in report["results"]["failed_checks"]] == ["CKV_1", "CKV_2"]
    assert report["summary"]["parsing_errors"] == 3


def test_one_malformed_report_in_a_list_is_rejected() -> None:
    payload = json.dumps([{"results": {"failed_checks": []}, "summary": {"parsing_errors": 0}}, {}])

    with pytest.raises(CheckovScanError, match="missing results or summary"):
        _parse_report(payload)


def test_invalid_framework_cannot_turn_missing_report_into_a_pass() -> None:
    rule = CheckovIacSecurity(
        CONTRACT_ROOT / "compliant",
        scan_dir="infra",
        framework="not-a-framework",
    )

    passed, errors, meta = rule.evaluate()

    assert not passed
    assert meta["execution_error"] is True
    assert errors == ["Checkov exited with unexpected status 2"]


def test_checkov_timeout_fails_closed() -> None:
    rule = CheckovIacSecurity(CONTRACT_ROOT / "compliant", scan_dir="infra", timeout=0)

    passed, errors, meta = rule.evaluate()

    assert not passed
    assert meta["execution_error"] is True
    assert errors and "execution failed" in errors[0]


def test_checkov_timeout_is_reported_as_execution_error(
    capsys: pytest.CaptureFixture[str],
) -> None:
    rule = CheckovIacSecurity(CONTRACT_ROOT / "compliant", scan_dir="infra", timeout=0)

    assert rule.run() == 2
    assert "ERROR checkov_iac_security" in capsys.readouterr().out


def test_actual_parser_failure_fails_the_scan(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    source = tmp_path / "infra" / "main.bicep"
    source.parent.mkdir()
    source.write_text("resource broken 'Microsoft.Storage/storageAccounts@2023-01-01' = {\n  name: }\n")
    rule = CheckovIacSecurity(tmp_path, scan_dir="infra")

    passed, errors, meta = rule.evaluate()

    assert not passed
    assert meta["parsing_errors"] == 1
    assert any("could not parse" in error for error in errors)
    assert rule.run() == 1
    assert "Checkov could not parse 1 IaC file(s)" in capsys.readouterr().out


def test_finding_path_and_text_are_rendered_for_minimal_scanner_records() -> None:
    finding = {"check_id": "CKV_TEST_1", "resource": "resource", "file_path": "/nested/main.bicep"}

    assert _finding_line(finding) == (
        "  - [CKV_TEST_1] Checkov policy violation: resource at /nested/main.bicep."
    )
    assert _finding_path(finding, scan_path=CONTRACT_ROOT / "compliant" / "infra", scan_dir="infra") == (
        "infra/main.bicep"
    )


def test_checkov_report_paths_are_mapped_from_the_real_scan_root() -> None:
    scan_path = (CONTRACT_ROOT / "violation" / "infra").resolve()
    result = run_checkov(scan_path)
    assert result is not None
    _, report = result
    finding = report["results"]["failed_checks"][0]
    assert _finding_path(finding, scan_path=scan_path, scan_dir="infra") == "infra/main.bicep"
    outside_scan_root = {**finding, "file_abs_path": "/outside/tree/main.bicep"}
    assert _finding_path(outside_scan_root, scan_path=scan_path, scan_dir="infra") == "infra/main.bicep"
    assert (
        _finding_path(
            outside_scan_root,
            scan_path=scan_path,
            scan_dir="infra",
            repo_root=CONTRACT_ROOT / "violation",
        )
        == "infra/main.bicep"
    )


@pytest.mark.parametrize("base_ref", ["", "--bad", "HEAD other"])
def test_invalid_diff_base_fails_closed(tmp_path: Path, base_ref: str) -> None:
    repo = _iac_repo(tmp_path)

    passed, errors, meta = CheckovIacSecurity(repo, scan_dir="infra", base_ref=base_ref).evaluate()

    assert not passed
    assert meta["execution_error"] is True
    assert errors == ["diff base is invalid"]


def test_missing_git_fails_closed_before_scanning(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    repo = _iac_repo(tmp_path)
    monkeypatch.setenv("PATH", "")

    passed, errors, meta = CheckovIacSecurity(repo, scan_dir="infra", base_ref="HEAD").evaluate()

    assert not passed
    assert meta["execution_error"] is True
    assert errors == ["diff cannot be computed: git is unavailable"]


def test_unrelated_git_history_fails_closed(tmp_path: Path) -> None:
    repo = _iac_repo(tmp_path)
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    subprocess.run(["git", "add", "infra"], cwd=repo, check=True)
    commit = [
        "git",
        "-c",
        "user.name=fixture",
        "-c",
        "user.email=fixture@example.invalid",
        "commit",
        "-qm",
        "fixture",
    ]
    subprocess.run(commit, cwd=repo, check=True)
    base = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True, check=True
    ).stdout.strip()
    subprocess.run(["git", "checkout", "-q", "--orphan", "unrelated"], cwd=repo, check=True)
    (repo / "infra" / "safe.bicep").write_text(
        (repo / "infra" / "safe.bicep").read_text(encoding="utf-8") + "\n// unrelated\n",
        encoding="utf-8",
    )
    subprocess.run(["git", "add", "infra"], cwd=repo, check=True)
    subprocess.run(commit, cwd=repo, check=True)

    passed, errors, meta = CheckovIacSecurity(repo, scan_dir="infra", base_ref=base).evaluate()

    assert not passed
    assert meta["execution_error"] is True
    assert errors == ["diff base is missing or ambiguous"]


def test_nonexistent_repository_fails_closed_on_git_process_error(tmp_path: Path) -> None:
    missing = tmp_path / "missing"

    passed, errors, meta = CheckovIacSecurity(missing, scan_dir="infra", base_ref="HEAD").evaluate()

    assert not passed
    assert meta["execution_error"] is True
    assert errors and errors[0].startswith("diff cannot be computed:")


@pytest.mark.parametrize(
    ("changed_files", "scan_dir", "message"),
    [
        (["infra/safe.bicep"], "../", "scan directory escapes the repository"),
        ([""], "infra", "changed file path is invalid"),
        (["/absolute.bicep"], "infra", "changed file path is invalid"),
        (["../outside.bicep"], "infra", "changed file escapes the repository"),
    ],
)
def test_affected_scan_rejects_unsafe_scope_inputs(
    tmp_path: Path, changed_files: list[str], scan_dir: str, message: str
) -> None:
    repo = _iac_repo(tmp_path)

    passed, errors, meta = CheckovIacSecurity(repo, scan_dir=scan_dir, changed_files=changed_files).evaluate()

    assert not passed
    assert meta["execution_error"] is True
    assert errors and message in errors[0]


def test_affected_scan_rejects_conflicting_or_malformed_config(tmp_path: Path) -> None:
    repo = _iac_repo(tmp_path)
    conflicting = CheckovIacSecurity(
        repo, scan_dir="infra", changed_files=["infra/safe.bicep"], base_ref="HEAD"
    )
    malformed = build({"scan_dir": "infra", "changed_files": "infra/safe.bicep"}, repo_root=repo)

    for rule, message in (
        (conflicting, "changed files and diff base cannot both be set"),
        (malformed, "changed files must be a list"),
    ):
        passed, errors, meta = rule.evaluate()
        assert not passed
        assert meta["execution_error"] is True
        assert errors and message in errors[0]


def test_affected_scan_with_no_changed_bicep_files_excludes_unchanged_findings(
    tmp_path: Path,
) -> None:
    repo = _iac_repo(tmp_path)

    passed, errors, meta = CheckovIacSecurity(repo, scan_dir="infra", changed_files=["README.md"]).evaluate()

    assert passed
    assert errors == []
    assert meta["failed"] == 0


def test_affected_scan_rejects_symlinked_bicep_outside_repository(tmp_path: Path) -> None:
    repo = _iac_repo(tmp_path / "repo")
    outside = tmp_path / "outside.bicep"
    outside.write_text("param name string\n", encoding="utf-8")
    (repo / "infra" / "linked.bicep").symlink_to(outside)

    passed, errors, meta = CheckovIacSecurity(
        repo, scan_dir="infra", changed_files=["infra/safe.bicep"]
    ).evaluate()

    assert not passed
    assert meta["execution_error"] is True
    assert errors and "escapes the repository" in errors[0]


def test_affected_scan_rejects_directory_disguised_as_bicep_file(tmp_path: Path) -> None:
    repo = _iac_repo(tmp_path)
    (repo / "infra" / "not-a-file.bicep").mkdir()

    passed, errors, meta = CheckovIacSecurity(
        repo, scan_dir="infra", changed_files=["infra/safe.bicep"]
    ).evaluate()

    assert not passed
    assert meta["execution_error"] is True
    assert errors and "not a file" in errors[0]


def test_affected_scan_rejects_local_module_outside_repository(tmp_path: Path) -> None:
    repo = _iac_repo(tmp_path / "repo")
    (repo / "infra" / "safe.bicep").write_text(
        "module outside '../../outside.bicep' = {\n  name: 'outside'\n}\n", encoding="utf-8"
    )

    passed, errors, meta = CheckovIacSecurity(
        repo, scan_dir="infra", changed_files=["infra/safe.bicep"]
    ).evaluate()

    assert not passed
    assert meta["execution_error"] is True
    assert errors and "module escapes the repository" in errors[0]


def test_unreadable_changed_file_manifest_fails_closed(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    repo = _iac_repo(tmp_path)

    assert main(["--repo-root", str(repo), "--changed-files-from", str(repo / "missing.txt")]) == 2
    assert "changed-file input cannot be read" in capsys.readouterr().out


def test_changed_bicep_parser_failure_fails_closed(tmp_path: Path) -> None:
    repo = _iac_repo(tmp_path)
    (repo / "infra" / "safe.bicep").write_text("module broken", encoding="utf-8")

    passed, errors, meta = CheckovIacSecurity(
        repo, scan_dir="infra", changed_files=["infra/safe.bicep"]
    ).evaluate()

    assert not passed
    assert meta["execution_error"] is True
    assert errors and "Bicep dependency parsing failed" in errors[0]


def test_remote_module_reference_is_not_treated_as_missing_local_dependency(
    tmp_path: Path,
) -> None:
    repo = _iac_repo(tmp_path)
    (repo / "infra" / "remote.bicep").write_text(
        "module remote 'br/public:avm/res/storage/storage-account:0.1.0' = {\n"
        "  name: 'remote'\n"
        "  params: {}\n"
        "}\n",
        encoding="utf-8",
    )

    passed, errors, meta = CheckovIacSecurity(
        repo, scan_dir="infra", changed_files=["infra/safe.bicep"]
    ).evaluate()

    assert passed
    assert errors == []
    assert meta["execution_error"] is False


def test_cyclic_local_module_references_terminate_and_fail_closed(tmp_path: Path) -> None:
    repo = _iac_repo(tmp_path)
    (repo / "infra" / "safe.bicep").write_text(
        "module unsafe './unsafe.bicep' = {\n  name: 'unsafe'\n}\n",
        encoding="utf-8",
    )
    (repo / "infra" / "unsafe.bicep").write_text(
        "module safe './safe.bicep' = {\n  name: 'safe'\n}\n",
        encoding="utf-8",
    )

    passed, errors, meta = CheckovIacSecurity(
        repo, scan_dir="infra", changed_files=["infra/safe.bicep"]
    ).evaluate()

    assert not passed
    assert meta["execution_error"] is True
    assert errors and "Checkov JSON report is missing results or summary" in errors[0]


def test_diff_command_failure_after_valid_base_fails_closed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = _iac_repo(tmp_path / "repo")
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    git = bin_dir / "git"
    git.write_text(
        "#!/bin/sh\n"
        'case "$1" in\n'
        "  rev-parse|merge-base) echo aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa ;;\n"
        "  diff) exit 1 ;;\n"
        "  *) exit 2 ;;\n"
        "esac\n",
        encoding="utf-8",
    )
    git.chmod(0o755)
    monkeypatch.setenv("PATH", str(bin_dir))

    passed, errors, meta = CheckovIacSecurity(repo, scan_dir="infra", base_ref="main").evaluate()

    assert not passed
    assert meta["execution_error"] is True
    assert errors == ["diff cannot be computed"]


def test_malformed_external_parser_module_path_fails_closed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from pycep import BicepParser

    repo = _iac_repo(tmp_path)
    (repo / "infra" / "safe.bicep").write_text(
        "module storage './unsafe.bicep' = {\n  name: 'storage'\n}\n",
        encoding="utf-8",
    )
    real_parse = BicepParser.parse

    def malformed_parse(
        parser: BicepParser, *, text: str | None = None, file_path: Path | None = None
    ) -> dict[str, object]:
        report = real_parse(parser, text=text, file_path=file_path)
        for module in report.get("modules", {}).values():
            if module["type"] == "local":
                module["detail"]["path"] = None
        return report

    monkeypatch.setattr(BicepParser, "parse", malformed_parse)

    passed, errors, meta = CheckovIacSecurity(
        repo, scan_dir="infra", changed_files=["infra/safe.bicep"]
    ).evaluate()

    assert not passed
    assert meta["execution_error"] is True
    assert errors and "local Bicep module path is invalid" in errors[0]
