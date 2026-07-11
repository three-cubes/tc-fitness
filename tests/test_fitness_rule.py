"""Tests for the repo-agnostic, config-driven FitnessRule ABC (v0.6.0)."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from tc_fitness.core_checks.no_llm_attribution import NoLlmAttribution
from tc_fitness.fitness_rule import FitnessRule

#: An attribution signature `scan_text` flags — the kind of residue vendored test
#: fixtures and pnpm trash dirs legitimately carry (the issue-25 repro).
_ATTRIBUTION = "Co-Authored-By: Claude <noreply@anthropic.com>\n"


class _BadWord(FitnessRule):
    """A trivial concrete rule: a ``.py`` file containing the token ``BADWORD``."""

    name = "bad-word"
    remediation = "fix: remove BADWORD; next: re-run; run: pytest"
    extensions = (".py",)

    def file_has_violation(self, path: Path) -> bool:
        return "BADWORD" in path.read_text(encoding="utf-8")


def _seed(tmp_path: Path, rel: str, body: str) -> None:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")


def _git_init_and_add(repo: Path, *tracked: str) -> None:
    """Init a git repo at ``repo`` and stage ``tracked`` so ``git ls-files`` sees them.

    Staging (``git add``) is enough — ``git ls-files`` reads the index, so no
    commit (and thus no user identity) is required.
    """
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "add", *tracked], cwd=repo, check=True, capture_output=True)


def test_abstract_cannot_instantiate() -> None:
    with pytest.raises(TypeError):
        FitnessRule()  # type: ignore[abstract]


def test_collect_violations_respects_config_roots(tmp_path: Path) -> None:
    _seed(tmp_path, "src/bad.py", "x = 'BADWORD'\n")
    _seed(tmp_path, "other/bad.py", "x = 'BADWORD'\n")
    rule = _BadWord(repo_root=tmp_path, roots=("src",))
    violations = {str(p) for p in rule.collect_violations()}
    assert violations == {"src/bad.py"}  # 'other/' is out of configured scope


def test_from_config_overrides_roots_and_exempt(tmp_path: Path) -> None:
    _seed(tmp_path, "src/a.py", "x = 'BADWORD'\n")
    _seed(tmp_path, "src/b.py", "x = 'BADWORD'\n")
    rule = _BadWord.from_config(
        {"roots": ["src"], "exempt_files": ["src/b.py"]},
        repo_root=tmp_path,
    )
    assert {str(p) for p in rule.collect_violations()} == {"src/a.py"}


def test_extension_filter(tmp_path: Path) -> None:
    _seed(tmp_path, "src/a.py", "BADWORD")
    _seed(tmp_path, "src/a.txt", "BADWORD")
    rule = _BadWord(repo_root=tmp_path, roots=("src",))
    assert {str(p) for p in rule.collect_violations()} == {"src/a.py"}


def test_run_clean_when_no_baseline_and_no_violation(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _seed(tmp_path, "src/ok.py", "x = 1\n")
    rule = _BadWord(repo_root=tmp_path, roots=("src",))
    assert rule.run() == 0


def test_run_fails_on_net_new_violation(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    _seed(tmp_path, "src/bad.py", "BADWORD\n")
    rule = _BadWord(repo_root=tmp_path, roots=("src",))
    assert rule.run() == 1


def test_establish_then_violation_is_grandfathered(tmp_path: Path) -> None:
    _seed(tmp_path, "src/bad.py", "BADWORD\n")
    rule = _BadWord(repo_root=tmp_path, roots=("src",))
    rule.establish_baseline()
    # Same offender is now grandfathered → clean.
    assert rule.run() == 0
    assert rule.load_baseline() == {"src/bad.py"}


def test_grandfathered_does_not_mask_a_new_offender(tmp_path: Path) -> None:
    _seed(tmp_path, "src/old.py", "BADWORD\n")
    rule = _BadWord(repo_root=tmp_path, roots=("src",))
    rule.establish_baseline()
    _seed(tmp_path, "src/new.py", "BADWORD\n")
    assert rule.run() == 1  # net-new offender still fails


def test_name_override_via_config(tmp_path: Path) -> None:
    rule = _BadWord.from_config({"name": "renamed"}, repo_root=tmp_path)
    rule.establish_baseline()
    assert (tmp_path / ".architecture" / "baseline" / "renamed-files.txt").exists()


def test_symlinked_repo_root_still_scopes(tmp_path: Path) -> None:
    # A symlinked repo root (e.g. macOS /tmp → /private/tmp) must not break
    # scoping: enumerated paths resolve symlinks, so the root must too, else
    # _repo_relative falls back to the absolute path and every is_in_scope
    # prefix test fails — a silent always-pass. Regression guard.
    real = tmp_path / "real"
    (real / "src").mkdir(parents=True)
    (real / "src" / "bad.py").write_text("BADWORD\n", encoding="utf-8")
    link = tmp_path / "link"
    link.symlink_to(real)
    rule = _BadWord(repo_root=link, roots=("src",))
    assert {str(p) for p in rule.collect_violations()} == {"src/bad.py"}
    assert rule.run() == 1  # the net-new offender is detected through the symlink


def test_empty_roots_enumerate_nothing(tmp_path: Path) -> None:
    # The empty-roots guard: with NO configured root, the default enumeration
    # yields nothing even when the git repo has tracked in-scope files. Scanning
    # by extension alone requires an explicit root (``roots=("",)``) or an
    # ``enumerate_files`` override — an unconfigured check scans no files, so a
    # check dispatched against the class-default config never scans the whole repo.
    _seed(tmp_path, "src/tracked.py", "x = 'BADWORD'\n")
    _git_init_and_add(tmp_path, "src/tracked.py")
    rule = _BadWord(repo_root=tmp_path)  # class-default empty roots
    assert rule.enumerate_files() == []
    assert rule.collect_violations() == set()  # nothing enumerated → nothing flagged


def test_untracked_vendor_residue_is_not_scanned(tmp_path: Path) -> None:
    # The issue-25 parity fix: a fresh CI checkout sees only tracked files, so a
    # local run must too. A gitignored pnpm/vendor trash file carrying an
    # attribution signature must NOT be enumerated — only `git ls-files` does.
    # ``roots=("",)`` is the explicit scan-all root (every path starts with the
    # empty prefix), so the whole tracked tree is enumerated by extension.
    _seed(tmp_path, "src/clean.py", "x = 1\n")
    _seed(tmp_path, ".gitignore", "node_modules/\n")
    _seed(tmp_path, "node_modules/.ignored/x.py", _ATTRIBUTION)
    _git_init_and_add(tmp_path, "src/clean.py", ".gitignore")  # residue left unstaged
    rule = NoLlmAttribution(repo_root=tmp_path, roots=("",))
    violations = {str(p) for p in rule.collect_violations()}
    assert violations == set()  # the untracked residue is invisible to the scan


def test_tracked_file_with_violation_is_still_flagged(tmp_path: Path) -> None:
    # The fix narrows enumeration to tracked files without weakening detection: a
    # tracked file that genuinely carries residue is still flagged. ``roots=("",)``
    # is the explicit scan-all root (the whole tracked tree, by extension).
    _seed(tmp_path, "src/bad.py", _ATTRIBUTION)
    _git_init_and_add(tmp_path, "src/bad.py")
    rule = NoLlmAttribution(repo_root=tmp_path, roots=("",))
    assert {str(p) for p in rule.collect_violations()} == {"src/bad.py"}


def test_non_git_fallback_skips_node_modules(tmp_path: Path) -> None:
    # An unpacked source tarball (no git tree) falls back to a working-tree walk;
    # that walk must still exclude `node_modules` so untracked vendor residue
    # cannot trip a non-git scan either. tmp_path is not a git repo → fallback.
    _seed(tmp_path, "src/real.py", "BADWORD\n")
    _seed(tmp_path, "src/node_modules/dep.py", "BADWORD\n")
    rule = _BadWord(repo_root=tmp_path, roots=("src",))
    assert {str(p) for p in rule.collect_violations()} == {"src/real.py"}


def test_run_core_check_with_no_config_scans_nothing(tmp_path: Path) -> None:
    # Consumer contract at the engine↔consumer boundary: a CORE check dispatched
    # with NO config (`run_core_check` with `config=None` → the rule's empty-roots
    # class defaults) — the path a consumer's subprocess dispatch takes — must
    # scan NOTHING, not the whole repo. This is the exact boundary the v0.13.0
    # empty-roots regression escaped through: a tracked file carrying attribution
    # residue must NOT be flagged when the check runs with defaults (rc 0). Under
    # the regression this scanned the whole tree, found the residue, and returned
    # rc 1 — so this test goes red on v0.13.0 and green on the restored contract.
    from tc_fitness.core_checks import run_core_check

    _seed(tmp_path, "app/mod.py", _ATTRIBUTION)
    _git_init_and_add(tmp_path, "app/mod.py")
    assert run_core_check(NoLlmAttribution, ["--repo-root", str(tmp_path)]) == 0
