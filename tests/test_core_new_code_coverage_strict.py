from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

import tc_fitness.core_checks.new_code_coverage as module

pytestmark = pytest.mark.unit


def _completed(
    args: list[str], returncode: int, stdout: str = "", stderr: str = ""
) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(args, returncode, stdout, stderr)


def test_default_is_strict_and_invokes_diff_cover(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    calls: list[list[str]] = []

    def run(args: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        calls.append(args)
        if args[:2] == ["git", "merge-base"]:
            return _completed(args, 0, "base-sha\n")
        return _completed(args, 0, "Passed all checks\n")

    (tmp_path / "coverage.xml").write_text(
        '<coverage><sources><source>.</source></sources><class filename="src/a.py">'
        '<lines><line number="1" hits="1"/></lines></class></coverage>',
        encoding="utf-8",
    )
    monkeypatch.setattr(module.subprocess, "run", run)
    rule = module.build({}, repo_root=tmp_path)
    assert rule.floor_pct == 100
    assert rule.run() == 0
    diff_cover_calls = [args for args in calls if args[0].endswith("/diff-cover")]
    assert diff_cover_calls and "--fail-under" in diff_cover_calls[0]
    assert "100.0" in diff_cover_calls[0]
    assert "--include-untracked" in diff_cover_calls[0]


def test_missing_report_fails_closed(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(
        module.subprocess, "run", lambda *args, **kwargs: _completed(list(args[0]), 0, "base\n")
    )
    rule = module.build({}, repo_root=tmp_path)
    assert rule.run() == 1
    assert "coverage report" in capsys.readouterr().out.lower()


def test_missing_base_ref_fails_closed(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (tmp_path / "coverage.xml").write_text(
        '<coverage><sources><source>.</source></sources><class filename="src/a.py">'
        '<lines><line number="1" hits="1"/></lines></class></coverage>',
        encoding="utf-8",
    )
    monkeypatch.setattr(
        module.subprocess, "run", lambda *args, **kwargs: _completed(list(args[0]), 1, "", "unknown ref")
    )
    rule = module.build({}, repo_root=tmp_path)
    assert rule.run() == 1
    assert "base" in capsys.readouterr().out.lower()


def test_exact_admission_mode_delegates_to_immutable_checker(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    called: list[tuple[Path, dict[str, object]]] = []

    def failures(root: Path, config: dict[str, object]) -> dict[str, str]:
        called.append((root, config))
        return {}

    monkeypatch.setattr("tc_fitness.coverage_admission.changed_line_failures", failures)
    config = {"floor_pct": 100, "exact_base_commit": "base", "candidate_commit": "head"}
    assert module.build(config, repo_root=tmp_path).run() == 0
    assert called == [(tmp_path, config)]


def test_changed_test_only_paths_do_not_trigger_mapping_precheck(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    (tmp_path / "coverage.xml").write_text(
        '<coverage><sources><source>.</source></sources><class filename="src/a.py">'
        '<lines><line number="1" hits="1"/></lines></class></coverage>',
        encoding="utf-8",
    )
    git_calls: list[list[str]] = []

    def git(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
        git_calls.append(args)
        return _completed(args, 0, "base\n")

    monkeypatch.setattr(
        module.subprocess,
        "run",
        lambda args, **kwargs: _completed(list(args), 0, "diff-cover passed\n"),
    )
    assert module.build({}, repo_root=tmp_path, git_runner=git).run() == 0
    assert not any(args[:1] == ["diff"] for args in git_calls)
