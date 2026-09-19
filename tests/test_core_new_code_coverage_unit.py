"""Tests for the CORE check new_code_coverage.

Mirrors SonarCloud's "Coverage on New Code >= floor" merge condition locally:
for each changed file, the ADDED lines (right side of the diff vs the merge-base)
must clear a coverage floor. The git invocation is a DI seam, so these tests feed
canned ``merge-base`` / ``diff`` output — no real repository, no monkeypatching.
"""

from __future__ import annotations

import subprocess
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import pytest

import tc_fitness.core_checks.new_code_coverage as new_code_coverage
from tc_fitness.core_checks.new_code_coverage import (
    parse_added_lines,
)

pytestmark = pytest.mark.unit

# --------------------------------------------------------------------------- #
# Fixtures: a Cobertura report with per-line hits + a canned git runner.
# --------------------------------------------------------------------------- #


def _report(files: dict[str, dict[int, int]], *, source: str = "src") -> str:
    """Render a Cobertura report: ``{filename: {line_no: hits}}``."""
    blocks = []
    for name, lines in files.items():
        line_els = "".join(f'<line number="{n}" hits="{h}"/>' for n, h in lines.items())
        blocks.append(f'<class filename="{name}" line-rate="0.5"><lines>{line_els}</lines></class>')
    classes = "\n".join(blocks)
    return (
        '<?xml version="1.0" ?>\n'
        '<coverage line-rate="0.5" branch-rate="0.5">\n'
        f"  <sources><source>{source}</source></sources>\n"
        f"  <packages><package><classes>\n{classes}\n"
        "  </classes></package></packages>\n"
        "</coverage>\n"
    )


def _seed(tmp_path: Path, rel: str, body: str) -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


def _completed(args: list[str], rc: int, out: str, err: str = "") -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(args=["git", *args], returncode=rc, stdout=out, stderr=err)


def _fake_git(
    *,
    merge_base: str = "0123abc",
    diff: str = "",
    mb_rc: int = 0,
    diff_rc: int = 0,
):
    """A canned git runner returning fixed ``merge-base`` / ``diff`` output."""

    def runner(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
        if args and args[0] == "merge-base":
            return _completed(args, mb_rc, merge_base + "\n")
        if args and args[0] == "diff":
            return _completed(args, diff_rc, diff)
        return _completed(args, 0, "")

    return runner


def _diff(path: str, new_start: int, added: list[str], *, new_file: bool = False) -> str:
    """A minimal ``git diff -U0`` for one file adding ``added`` lines at ``new_start``."""
    old = "--- /dev/null" if new_file else f"--- a/{path}"
    header = (
        f"@@ -0,0 +{new_start},{len(added)} @@"
        if new_file
        else f"@@ -{new_start - 1},0 +{new_start},{len(added)} @@"
    )
    body = "".join(f"+{line}\n" for line in added)
    mode = "new file mode 100644\n" if new_file else ""
    return (
        f"diff --git a/{path} b/{path}\n"
        f"{mode}index 1111111..2222222 100644\n"
        f"{old}\n"
        f"+++ b/{path}\n"
        f"{header}\n"
        f"{body}"
    )


def _cfg(**extra: Any) -> Mapping[str, Any]:
    base: dict[str, Any] = {"roots": ["src"], "floor_pct": 80.0, "base_ref": "origin/main"}
    base.update(extra)
    return base


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    """Run real git against a disposable repository."""
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )


def _git_repo(tmp_path: Path) -> Path:
    """Create a repository whose current commit is also ``origin/main``."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "--quiet")
    _git(repo, "config", "user.name", "Coverage Test")
    _git(repo, "config", "user.email", "coverage-test@example.invalid")
    _seed(repo, "src/a.py", "existing = 1\n")
    _git(repo, "add", "src/a.py")
    _git(repo, "commit", "--quiet", "-m", "base")
    _git(repo, "update-ref", "refs/remotes/origin/main", "HEAD")
    return repo


# --------------------------------------------------------------------------- #
# Pure parser: per-line Cobertura coverage.
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
# Pure parser: added lines from a unified diff.
# --------------------------------------------------------------------------- #


def test_parse_added_lines_basic_hunk() -> None:
    diff = _diff("src/a.py", 10, ["x = 1", "y = 2", "z = 3"])
    assert parse_added_lines(diff) == {"src/a.py": {10, 11, 12}}


def test_parse_added_lines_new_file_whole_body_is_added() -> None:
    diff = _diff("src/new.py", 1, ["a = 1", "b = 2"], new_file=True)
    assert parse_added_lines(diff) == {"src/new.py": {1, 2}}


def test_parse_added_lines_deleted_file_contributes_nothing() -> None:
    diff = (
        "diff --git a/src/gone.py b/src/gone.py\n"
        "deleted file mode 100644\n"
        "index 1111111..0000000 100644\n"
        "--- a/src/gone.py\n"
        "+++ /dev/null\n"
        "@@ -1,2 +0,0 @@\n"
        "-was = 1\n"
        "-here = 2\n"
    )
    assert parse_added_lines(diff) == {}


def test_parse_added_lines_context_lines_advance_counter() -> None:
    # A -U1 hunk: context lines advance the new-side counter so the added line
    # lands on its true number (11), not the hunk start (10).
    diff = (
        "diff --git a/src/c.py b/src/c.py\n"
        "index aaa..bbb 100644\n"
        "--- a/src/c.py\n"
        "+++ b/src/c.py\n"
        "@@ -10,2 +10,3 @@ def f():\n"
        " keep = 0\n"
        "+added = 1\n"
        " tail = 2\n"
    )
    assert parse_added_lines(diff) == {"src/c.py": {11}}


def test_parse_added_lines_multiple_hunks_one_file() -> None:
    diff = (
        "diff --git a/src/m.py b/src/m.py\n"
        "index aaa..bbb 100644\n"
        "--- a/src/m.py\n"
        "+++ b/src/m.py\n"
        "@@ -0,0 +1,1 @@\n"
        "+first\n"
        "@@ -10,0 +12,2 @@\n"
        "+twelfth\n"
        "+thirteenth\n"
    )
    assert parse_added_lines(diff) == {"src/m.py": {1, 12, 13}}


# --------------------------------------------------------------------------- #
# Rule end-to-end via the injected git seam.
# --------------------------------------------------------------------------- #


def test_git_output_decodes_non_utf8_bytes_losslessly() -> None:
    raw = b"src/bad_\xff.py\0"
    decoder = getattr(new_code_coverage, "_decode_git_output", None)

    assert decoder is not None
    assert decoder(raw) == "src/bad_\udcff.py\0"


# --------------------------------------------------------------------------- #
# Soft-skip paths: no report / no changes / git unavailable / unsafe ref.
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
# Hard floor: new code is non-grandfatherable.
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
# Design law: the CORE module carries zero repo identity in executable code.
# --------------------------------------------------------------------------- #
