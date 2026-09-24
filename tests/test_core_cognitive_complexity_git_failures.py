"""Failure-path coverage for cognitive-complexity Git snapshot handling."""

from __future__ import annotations

import subprocess
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

import tc_fitness.core_checks.cognitive_complexity as cognitive_complexity

pytestmark = pytest.mark.integration


def _rule(tmp_path: Path) -> cognitive_complexity.CognitiveComplexity:
    return cognitive_complexity.build({"roots": ["src"]}, repo_root=tmp_path)


def _completed(returncode: int, *, stdout: Any = b"", stderr: Any = b"") -> SimpleNamespace:
    return SimpleNamespace(returncode=returncode, stdout=stdout, stderr=stderr)


def test_missing_git_is_reported_as_an_error_and_fails_closed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(cognitive_complexity.shutil, "which", lambda _: None)
    rule = _rule(tmp_path)

    assert rule.enumerate_files() == []
    assert rule._scan_error and "git is unavailable" in rule._scan_error
    assert rule.file_has_violation(tmp_path / "src/module.py") is True
    assert rule.run() == 1
    assert "git is unavailable" in capsys.readouterr().out


@pytest.mark.parametrize(
    ("failure", "expected"),
    [
        (
            _completed(1, stderr="not related"),
            "could not establish one merge base",
        ),
        (
            _completed(0, stdout="base-a\nbase-b\n"),
            "could not establish one merge base",
        ),
    ],
)
def test_ref_and_merge_base_failures_include_actionable_errors(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    failure: SimpleNamespace,
    expected: str,
) -> None:
    monkeypatch.setattr(cognitive_complexity.shutil, "which", lambda _: "/usr/bin/git")
    calls = iter([_completed(0, stdout="commit\n"), failure])
    monkeypatch.setattr(cognitive_complexity.subprocess, "run", lambda *args, **kwargs: next(calls))

    result = _rule(tmp_path)._baseline_sources()

    assert isinstance(result, str)
    assert expected in result


def test_unavailable_base_ref_is_reported(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cognitive_complexity.shutil, "which", lambda _: "/usr/bin/git")
    monkeypatch.setattr(
        cognitive_complexity.subprocess,
        "run",
        lambda *args, **kwargs: _completed(128, stderr="unknown revision"),
    )

    result = _rule(tmp_path)._baseline_sources()

    assert isinstance(result, str)
    assert "base ref is unavailable" in result


def test_tree_listing_failure_includes_git_diagnostic(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(cognitive_complexity.shutil, "which", lambda _: "/usr/bin/git")
    calls = iter(
        [
            _completed(0, stdout="commit\n"),
            _completed(0, stdout="merge-base\n"),
            _completed(128, stderr=b"pathspec did not match"),
        ]
    )
    monkeypatch.setattr(cognitive_complexity.subprocess, "run", lambda *args, **kwargs: next(calls))

    result = _rule(tmp_path)._baseline_sources()

    assert isinstance(result, str)
    assert "could not enumerate files at merge base" in result
    assert "pathspec did not match" in result


def test_malformed_tree_output_is_rejected(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cognitive_complexity.shutil, "which", lambda _: "/usr/bin/git")
    calls = iter(
        [
            _completed(0, stdout="commit\n"),
            _completed(0, stdout="merge-base\n"),
            _completed(0, stdout=b"not a tree record"),
        ]
    )
    monkeypatch.setattr(cognitive_complexity.subprocess, "run", lambda *args, **kwargs: next(calls))

    result = _rule(tmp_path)._baseline_sources()

    assert isinstance(result, str)
    assert "could not decode the origin/main source tree" in result


def test_blob_read_failure_includes_git_diagnostic(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cognitive_complexity.shutil, "which", lambda _: "/usr/bin/git")
    tree = b"100644 blob abcdef\tsrc/example.py\x00"
    calls = iter(
        [
            _completed(0, stdout="commit\n"),
            _completed(0, stdout="merge-base\n"),
            _completed(0, stdout=tree),
            _completed(128, stderr=b"object unavailable"),
        ]
    )
    monkeypatch.setattr(cognitive_complexity.subprocess, "run", lambda *args, **kwargs: next(calls))

    result = _rule(tmp_path)._baseline_sources()

    assert isinstance(result, str)
    assert "could not read files at merge base" in result
    assert "object unavailable" in result


def test_malformed_blob_batch_is_rejected(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cognitive_complexity.shutil, "which", lambda _: "/usr/bin/git")
    tree = b"100644 blob abcdef\tsrc/example.py\x00"
    calls = iter(
        [
            _completed(0, stdout="commit\n"),
            _completed(0, stdout="merge-base\n"),
            _completed(0, stdout=tree),
            _completed(0, stdout=b"abcdef blob invalid-size\n"),
        ]
    )
    monkeypatch.setattr(cognitive_complexity.subprocess, "run", lambda *args, **kwargs: next(calls))

    result = _rule(tmp_path)._baseline_sources()

    assert isinstance(result, str)
    assert "could not decode the origin/main source tree" in result


def test_rename_diff_failure_includes_git_diagnostic(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cognitive_complexity.shutil, "which", lambda _: "/usr/bin/git")
    calls = iter(
        [
            _completed(0, stdout="commit\n"),
            _completed(0, stdout="merge-base\n"),
            _completed(0, stdout=b""),
            _completed(128, stderr=b"diff failed"),
        ]
    )
    monkeypatch.setattr(cognitive_complexity.subprocess, "run", lambda *args, **kwargs: next(calls))

    result = _rule(tmp_path)._baseline_sources()

    assert isinstance(result, str)
    assert "could not compare paths with merge base" in result


@pytest.mark.parametrize("failure", [OSError("git missing"), subprocess.TimeoutExpired("git", 30)])
def test_ls_files_operational_failures_fail_run_closed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    failure: Exception,
) -> None:
    monkeypatch.setattr(cognitive_complexity.shutil, "which", lambda _: "/usr/bin/git")
    rule = _rule(tmp_path)
    monkeypatch.setattr(rule, "_baseline_sources", lambda: {})
    findings: list[tuple[str, str, str]] = []
    monkeypatch.setattr(
        cognitive_complexity,
        "report_finding",
        lambda check, path, message, **kwargs: findings.append((check, path, message)),
    )

    def fail(*args: Any, **kwargs: Any) -> None:
        raise failure

    monkeypatch.setattr(cognitive_complexity.subprocess, "run", fail)

    assert rule.run() == 1
    output = capsys.readouterr().out
    assert "could not enumerate source files" in output
    assert findings and findings[0][1] == "source_inventory"
    assert "could not enumerate source files" in findings[0][2]


def test_ls_files_nonzero_exit_does_not_escape_enumeration(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(cognitive_complexity.shutil, "which", lambda _: "/usr/bin/git")
    rule = _rule(tmp_path)
    monkeypatch.setattr(rule, "_baseline_sources", lambda: {})
    findings: list[tuple[str, str, str]] = []
    monkeypatch.setattr(
        cognitive_complexity,
        "report_finding",
        lambda check, path, message, **kwargs: findings.append((check, path, message)),
    )
    monkeypatch.setattr(
        cognitive_complexity.subprocess,
        "run",
        lambda *args, **kwargs: _completed(128, stderr=b"not a repository"),
    )

    assert rule.run() == 1
    output = capsys.readouterr().out
    assert "not a repository" in output
    assert findings and findings[0][1] == "source_inventory"
