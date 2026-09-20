"""Behavioural tests for the catalogue-driven runner.

Each test builds a SYNTHETIC catalogue + check modules in a tmp checks dir, so
the runner's dispatch is exercised end-to-end without depending on any consumer
repo's rules. The fixtures prove:

- in-process dispatch (a ``check_<x>.py`` with ``main() -> int`` runs in-process,
  sharing one CheckContext; a crashing check is isolated into a FAIL);
- guarded subprocess dispatch for ``*.sh`` shell detectors (sequential AND the
  parallel ThreadPoolExecutor path);
- the named verdict ledger shape (``run [id]`` / ``PASS [id]`` / ``FAIL [id]``
  + the aggregate line) — the format kairix's F83 + verdict tests depend on;
- staged-selection soundness (no false-negative on a staged change; the
  transparent skip ledger; file-local narrowing);
- ``--gate <id>`` selection;
- ``run_all=False`` exclusion from ``--all``;
- the programmatic ``run(...) -> Verdicts`` over a mixed python+shell catalogue.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import uuid
from pathlib import Path

import pytest

from tc_fitness.catalogue import RuleEntry
from tc_fitness.runner import (
    SKIP_EXIT_CODE,
    ConditionalResult,
    RunnerConfig,
    Verdicts,
    declared_skip_reason,
    dispatches_in_process,
    main_cli,
    make_env_path_conditional_check,
    run,
    run_bounded_process,
    staged_paths,
    write_skip_report,
)

pytestmark = pytest.mark.integration

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def _plain(text: str) -> str:
    """Strip ANSI colour codes so a ledger assertion reads the bare text.

    The runner wraps the ``run``/``PASS``/``FAIL`` markers in colour codes
    (byte-identical to kairix's runner), which puts a reset escape between
    ``run [id]`` and the script name. Tests assert on the colour-free form."""
    return _ANSI_RE.sub("", text)


# --------------------------------------------------------------------------- #
# fixture helpers — write synthetic check modules + a catalogue into tmp_path
# --------------------------------------------------------------------------- #


def _write_py_check(checks_dir: Path, name: str, body: str) -> None:
    """Write a ``check_<name>.py`` whose ``main()`` body is ``body`` (must
    ``return`` an int)."""
    (checks_dir / f"check_{name}.py").write_text(
        "def main():\n" + "\n".join(f"    {line}" for line in body.splitlines()) + "\n"
    )


def _write_sh_check(checks_dir: Path, filename: str, exit_code: int, echo: str = "") -> None:
    """Write a ``*.sh`` detector exiting ``exit_code``."""
    script = "#!/usr/bin/env bash\n"
    if echo:
        script += f'echo "{echo}"\n'
    script += f"exit {exit_code}\n"
    (checks_dir / filename).write_text(script)
    (checks_dir / filename).chmod(0o755)


@pytest.fixture
def checks_dir(tmp_path: Path) -> Path:
    d = tmp_path / "scripts" / "checks"
    d.mkdir(parents=True)
    return d


@pytest.fixture
def repo_root(tmp_path: Path) -> Path:
    return tmp_path


@pytest.fixture(autouse=True)
def _clean_sys_modules() -> object:
    """Drop synthetic ``check_*`` modules from ``sys.modules`` after each test so
    a re-used module name across tests can't serve a stale import."""
    before = set(sys.modules)
    yield
    for name in set(sys.modules) - before:
        if name.startswith("check_"):
            del sys.modules[name]


# --------------------------------------------------------------------------- #
# in-process dispatch + ledger shape
# --------------------------------------------------------------------------- #


def test_inprocess_pass_emits_run_and_pass_lines(
    checks_dir: Path, repo_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _write_py_check(checks_dir, "alpha", "return 0")
    rules = (RuleEntry(id="A1", gate="a1", check="alpha", summary="alpha rule"),)

    verdict = run(rules, mode="all", repo_root=repo_root, checks_dir=checks_dir)
    out = _plain(capsys.readouterr().out)

    assert verdict.ok
    assert verdict.ran == 1
    assert "run [A1] check_alpha.py" in out
    assert "PASS [A1] alpha rule" in out
    assert "=== All 1 architecture fitness functions passed ===" in out


def test_main_cli_changed_files_from_uses_explicit_diff_scope(
    checks_dir: Path, repo_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _write_py_check(checks_dir, "src_rule", "return 0")
    _write_py_check(checks_dir, "tests_rule", "return 1")  # would FAIL if dispatched
    changed = repo_root / "changed-files.txt"
    changed.write_text("src/service.py\n", encoding="utf-8")
    rules = (
        RuleEntry(
            id="SRC",
            gate="src",
            check="src_rule",
            summary="src rule",
            staged_class="file-local",
            staged_scope=("src",),
        ),
        RuleEntry(
            id="TESTS",
            gate="tests",
            check="tests_rule",
            summary="tests rule",
            staged_class="file-local",
            staged_scope=("tests",),
        ),
    )

    rc = main_cli(
        rules,
        ["--changed-files-from", str(changed)],
        repo_root=repo_root,
        checks_dir=checks_dir,
    )
    out = _plain(capsys.readouterr().out)

    assert rc == 0
    assert "run [SRC]" in out
    assert "skip [TESTS]" in out
    assert "staged selection: 1 ran, 1 skipped" in out


def test_main_cli_changed_files_from_missing_file_fails_closed(
    checks_dir: Path, repo_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _write_py_check(checks_dir, "src_rule", "return 0")
    rules = (
        RuleEntry(
            id="SRC",
            gate="src",
            check="src_rule",
            summary="src rule",
            staged_class="file-local",
            staged_scope=("src",),
        ),
    )

    rc = main_cli(
        rules,
        ["--changed-files-from", str(repo_root / "missing-files.txt")],
        repo_root=repo_root,
        checks_dir=checks_dir,
    )
    err = _plain(capsys.readouterr().err)

    assert rc == 2
    assert "FAIL --changed-files-from" in err
    assert "missing-files.txt" in err


def test_inprocess_fail_records_failure_and_exit_code(
    checks_dir: Path, repo_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _write_py_check(checks_dir, "beta", "return 1")
    rules = (RuleEntry(id="B1", gate="b1", check="beta", summary="beta rule"),)

    verdict = run(rules, mode="all", repo_root=repo_root, checks_dir=checks_dir)
    out = _plain(capsys.readouterr().out)

    assert not verdict.ok
    assert verdict.exit_code == 1
    assert verdict.failures == ["B1"]
    assert "FAIL [B1] beta rule (exit 1)" in out
    assert "Architecture fitness functions FAILED" in out


def test_inprocess_crash_is_isolated_into_a_fail(
    checks_dir: Path, repo_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    # A check that RAISES must be converted to a FAIL, never abort the ledger:
    # the SECOND rule still runs and the aggregate counts both.
    _write_py_check(checks_dir, "boom", 'raise RuntimeError("kaboom")')
    _write_py_check(checks_dir, "ok", "return 0")
    rules = (
        RuleEntry(id="C1", gate="c1", check="boom", summary="crashy rule"),
        RuleEntry(id="C2", gate="c2", check="ok", summary="fine rule"),
    )

    verdict = run(rules, mode="all", repo_root=repo_root, checks_dir=checks_dir)
    captured = capsys.readouterr()
    out = _plain(captured.out)

    assert verdict.failures == ["C1"]
    assert verdict.ran == 2  # the crash did NOT abort the ledger
    assert "FAIL [C1] crashy rule" in out  # no "(exit N)" suffix for a crash
    assert "PASS [C2] fine rule" in out
    assert "kaboom" in captured.err  # traceback replayed to stderr


def test_inprocess_check_stdout_is_replayed_inline(
    checks_dir: Path, repo_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _write_py_check(checks_dir, "talky", 'print("hello from the check"); return 0')
    rules = (RuleEntry(id="T1", gate="t1", check="talky", summary="talky"),)

    run(rules, mode="all", repo_root=repo_root, checks_dir=checks_dir)
    out = _plain(capsys.readouterr().out)

    # The check's own stdout lands between its run and PASS lines.
    assert "hello from the check" in out


def test_inprocess_main_accepting_argv_is_called_with_empty_list(checks_dir: Path, repo_root: Path) -> None:
    # A check declaring main(argv) must be called with [] (the no-args
    # subprocess shape), NOT the runner's own sys.argv.
    (checks_dir / "check_argvy.py").write_text(
        "def main(argv=None):\n    assert argv == [], f'expected [], got {argv!r}'\n    return 0\n"
    )
    rules = (RuleEntry(id="AV", gate="av", check="argvy", summary="argv check"),)
    verdict = run(rules, mode="all", repo_root=repo_root, checks_dir=checks_dir)
    assert verdict.ok


# --------------------------------------------------------------------------- #
# subprocess dispatch (sequential + parallel) for shell detectors
# --------------------------------------------------------------------------- #


def test_shell_detector_runs_as_subprocess(
    checks_dir: Path, repo_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _write_sh_check(checks_dir, "check-shellgate.sh", exit_code=0)
    rules = (
        RuleEntry(id="S1", gate="s1", check="shellgate", summary="shell rule", script="check-shellgate.sh"),
    )
    verdict = run(rules, mode="all", repo_root=repo_root, checks_dir=checks_dir)
    out = _plain(capsys.readouterr().out)
    assert verdict.ok
    assert "run [S1] check-shellgate.sh" in out
    assert "PASS [S1] shell rule" in out


def test_shell_detector_nonzero_exit_is_a_fail(checks_dir: Path, repo_root: Path) -> None:
    _write_sh_check(checks_dir, "check-bad.sh", exit_code=3)
    rules = (RuleEntry(id="S2", gate="s2", check="bad", summary="bad shell", script="check-bad.sh"),)
    verdict = run(rules, mode="all", repo_root=repo_root, checks_dir=checks_dir)
    assert verdict.failures == ["S2"]


def test_missing_shell_script_is_a_fail_not_a_crash(checks_dir: Path, repo_root: Path) -> None:
    rules = (RuleEntry(id="S3", gate="s3", check="absent", summary="missing", script="check-absent.sh"),)
    verdict = run(rules, mode="all", repo_root=repo_root, checks_dir=checks_dir)
    assert verdict.failures == ["S3"]


def test_parallel_subprocess_dispatch_matches_sequential_verdicts(
    checks_dir: Path, repo_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _write_sh_check(checks_dir, "check-p1.sh", exit_code=0)
    _write_sh_check(checks_dir, "check-p2.sh", exit_code=1)
    _write_sh_check(checks_dir, "check-p3.sh", exit_code=0)
    rules = (
        RuleEntry(id="P1", gate="p1", check="p1", summary="p1", script="check-p1.sh"),
        RuleEntry(id="P2", gate="p2", check="p2", summary="p2", script="check-p2.sh"),
        RuleEntry(id="P3", gate="p3", check="p3", summary="p3", script="check-p3.sh"),
    )

    verdict = run(rules, mode="all", repo_root=repo_root, checks_dir=checks_dir, parallel_subprocess=True)
    out = _plain(capsys.readouterr().out)

    assert verdict.failures == ["P2"]
    assert verdict.ran == 3
    # The named ledger is replayed in CATALOGUE order regardless of completion
    # order — P1 before P2 before P3.
    assert out.index("run [P1]") < out.index("run [P2]") < out.index("run [P3]")
    assert "PASS [P1] p1" in out
    assert "FAIL [P2] p2 (exit 1)" in out
    assert "PASS [P3] p3" in out


def test_parallel_replays_subprocess_output(
    checks_dir: Path, repo_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _write_sh_check(checks_dir, "check-loud.sh", exit_code=0, echo="DETECTOR-OUTPUT-MARKER")
    rules = (RuleEntry(id="L1", gate="l1", check="loud", summary="loud", script="check-loud.sh"),)
    run(rules, mode="all", repo_root=repo_root, checks_dir=checks_dir, parallel_subprocess=True)
    out = _plain(capsys.readouterr().out)
    assert "DETECTOR-OUTPUT-MARKER" in out


def test_parallel_mode_with_only_python_checks_needs_no_worker_results(
    checks_dir: Path, repo_root: Path
) -> None:
    _write_py_check(checks_dir, "parallel_python", "return 0")
    rules = (RuleEntry(id="PY", gate="py", check="parallel_python"),)

    verdict = run(rules, repo_root=repo_root, checks_dir=checks_dir, parallel_subprocess=True)

    assert verdict.ok
    assert verdict.ran == 1


def test_engine_core_rules_dispatch_inprocess_by_default() -> None:
    entry = RuleEntry(id="CORE", gate="core", check="core:coverage_floor")

    assert dispatches_in_process(entry)


def test_parallel_replay_captures_stderr_from_a_real_subprocess(
    checks_dir: Path, repo_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    script = checks_dir / "stderr-only.sh"
    script.write_text("#!/usr/bin/env bash\nprintf 'captured diagnostic\\n' >&2\n")
    script.chmod(0o755)
    rules = (RuleEntry(id="ERR", gate="err", check="err", script=script.name),)

    verdict = run(rules, repo_root=repo_root, checks_dir=checks_dir, parallel_subprocess=True)

    captured = capsys.readouterr()
    assert verdict.ok
    assert "captured diagnostic" in captured.err


def test_parallel_replay_reports_a_missing_script_as_a_failure(
    checks_dir: Path, repo_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    rules = (RuleEntry(id="MISSING", gate="missing", check="missing", script="missing.sh"),)

    verdict = run(rules, repo_root=repo_root, checks_dir=checks_dir, parallel_subprocess=True)

    assert verdict.failures == ["MISSING"]
    assert "check script not found: missing.sh" in _plain(capsys.readouterr().err)


def test_parallel_replay_reports_a_real_child_launch_error(
    checks_dir: Path, repo_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    script = checks_dir / "missing-interpreter.sh"
    script.write_text("#!/usr/bin/env bash\nexit 0\n")
    script.chmod(0o755)
    rules = (RuleEntry(id="BAD-INTERPRETER", gate="bad-interpreter", check="bad", script=script.name),)

    path = os.environ["PATH"]
    os.environ["PATH"] = ""
    try:
        verdict = run(rules, repo_root=repo_root, checks_dir=checks_dir, parallel_subprocess=True)
    finally:
        os.environ["PATH"] = path

    assert verdict.failures == ["BAD-INTERPRETER"]
    assert "could not launch missing-interpreter.sh" in _plain(capsys.readouterr().err)


def test_parallel_replay_preserves_empty_skip_lines_from_the_conditional_factory(
    checks_dir: Path, repo_root: Path
) -> None:
    env_var = f"TC_FITNESS_EMPTY_SKIP_{uuid.uuid4().hex.upper()}"
    assert env_var not in os.environ
    (checks_dir / "conditional.sh").write_text("#!/usr/bin/env bash\nexit 0\n")
    (checks_dir / "conditional.sh").chmod(0o755)
    rules = (
        RuleEntry(
            id="EMPTY-SKIP",
            gate="empty-skip",
            check="conditional",
            script="conditional.sh",
            subprocess_arg_env=env_var,
        ),
    )
    hook = make_env_path_conditional_check(
        env_var=env_var,
        default_rel="absent-report.xml",
        repo_root=repo_root,
    )

    verdict = run(
        rules,
        repo_root=repo_root,
        checks_dir=checks_dir,
        parallel_subprocess=True,
        conditional_check=hook,
    )

    assert verdict.ok
    assert verdict.skipped == 1


def test_parallel_conditional_subprocess_uses_a_real_environment_path(
    checks_dir: Path, repo_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env_var = f"TC_FITNESS_RUNTIME_PATH_{uuid.uuid4().hex.upper()}"
    runtime_input = repo_root / "runtime-input.txt"
    runtime_input.write_text("runtime input consumed\n")
    script = checks_dir / "read-input.sh"
    script.write_text('#!/usr/bin/env bash\ncat "$1"\n')
    script.chmod(0o755)
    rules = (
        RuleEntry(
            id="RUNTIME-PATH",
            gate="runtime-path",
            check="read-input",
            script=script.name,
            subprocess_arg_env=env_var,
        ),
    )
    assert env_var not in os.environ
    os.environ[env_var] = str(runtime_input)
    try:
        verdict = run(rules, repo_root=repo_root, checks_dir=checks_dir, parallel_subprocess=True)
    finally:
        del os.environ[env_var]

    assert verdict.ok
    assert "runtime input consumed" in _plain(capsys.readouterr().out)


def test_parallel_replay_classifies_a_subprocess_skip_exit_code(
    checks_dir: Path, repo_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The buffer-and-replay path has its own ``SKIP_EXIT_CODE`` check to cover.

    ``_run_one_subprocess`` (streamed straight to fd1) already proves exit 77
    is classified as a skip; ``--parallel``/``--staged`` route through the
    SEPARATE capturing replay function instead, which re-implements the same
    classification over the buffered output and needs its own test.
    """
    _write_sh_check(checks_dir, "check-skip.sh", SKIP_EXIT_CODE, echo="SKIP skip1: no input")
    rules = (RuleEntry(id="SKIP1", gate="skip1", check="skip1", script="check-skip.sh"),)

    verdict = run(rules, repo_root=repo_root, checks_dir=checks_dir, parallel_subprocess=True)

    assert verdict.ran == 0
    assert verdict.skipped == 1
    assert "PASS [SKIP1]" not in _plain(capsys.readouterr().out)


def test_parallel_replay_classifies_a_declared_skip_marker_on_a_zero_exit(
    checks_dir: Path, repo_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A detector that exits 0 but prints its own ``SKIP <id>: reason`` marker
    must be recognised on the replay path too, reading the reason from the
    BUFFERED stdout rather than being counted as an ordinary pass."""
    _write_sh_check(checks_dir, "check-marker.sh", 0, echo="SKIP marker1: tool not installed")
    rules = (RuleEntry(id="marker1", gate="marker1", check="marker1", script="check-marker.sh"),)

    verdict = run(rules, repo_root=repo_root, checks_dir=checks_dir, parallel_subprocess=True)
    out = _plain(capsys.readouterr().out)

    assert verdict.ran == 0
    assert verdict.skipped == 1
    assert verdict.skips == {"marker1": "tool not installed"}
    assert "PASS [marker1]" not in out


@pytest.mark.parametrize(("footer_contents", "printed"), [("fix path from a file", True), ("", False)])
def test_failed_check_uses_the_consumer_footer_file_when_nonempty(
    checks_dir: Path,
    repo_root: Path,
    capsys: pytest.CaptureFixture[str],
    footer_contents: str,
    printed: bool,
) -> None:
    footer_path = repo_root / "paved-road.txt"
    footer_path.write_text(footer_contents)
    _write_py_check(checks_dir, "footer_failure", "return 1")
    rules = (RuleEntry(id="FOOTER", gate="footer", check="footer_failure"),)

    def read_consumer_footer(entry: RuleEntry) -> str | None:
        assert entry.id == "FOOTER"
        return footer_path.read_text()

    verdict = run(
        rules,
        repo_root=repo_root,
        checks_dir=checks_dir,
        paved_road_footer=read_consumer_footer,
    )

    out = _plain(capsys.readouterr().out)
    assert verdict.failures == ["FOOTER"]
    assert ("fix path from a file" in out) is printed


def test_staged_mode_counts_a_builtin_conditional_skip(
    checks_dir: Path, repo_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    env_var = f"TC_FITNESS_STAGED_SKIP_{uuid.uuid4().hex.upper()}"
    assert env_var not in os.environ
    script = checks_dir / "conditional.sh"
    script.write_text("#!/usr/bin/env bash\nexit 0\n")
    script.chmod(0o755)
    rules = (
        RuleEntry(
            id="STAGED-SKIP",
            gate="staged-skip",
            check="conditional",
            script=script.name,
            subprocess_arg_env=env_var,
            staged_class="always-run",
        ),
    )
    hook = make_env_path_conditional_check(
        env_var=env_var,
        default_rel="absent-report.xml",
        repo_root=repo_root,
        absent_skip_lines=("skip [STAGED-SKIP] report absent",),
    )

    verdict = run(
        rules,
        mode="staged",
        staged_files=["any-change.txt"],
        repo_root=repo_root,
        checks_dir=checks_dir,
        conditional_check=hook,
    )

    assert verdict.ok
    assert verdict.skipped == 1
    assert "staged selection: 0 ran, 1 skipped" in _plain(capsys.readouterr().out)


def test_staged_mode_deduplicates_two_rules_for_one_real_script(checks_dir: Path, repo_root: Path) -> None:
    _write_py_check(checks_dir, "staged_shared", "return 0")
    rules = (
        RuleEntry(id="STAGED-FIRST", gate="staged-first", check="staged_shared", staged_class="always-run"),
        RuleEntry(id="STAGED-SECOND", gate="staged-second", check="staged_shared", staged_class="always-run"),
    )

    verdict = run(
        rules, mode="staged", staged_files=["changed.py"], repo_root=repo_root, checks_dir=checks_dir
    )

    assert verdict.ok
    assert verdict.ran == 1


def test_staged_mode_records_a_real_failing_python_check(checks_dir: Path, repo_root: Path) -> None:
    _write_py_check(checks_dir, "staged_failure", "return 1")
    rules = (
        RuleEntry(id="STAGED-FAIL", gate="staged-fail", check="staged_failure", staged_class="always-run"),
    )

    verdict = run(
        rules, mode="staged", staged_files=["changed.py"], repo_root=repo_root, checks_dir=checks_dir
    )

    assert verdict.failures == ["STAGED-FAIL"]


def test_staged_paths_reads_a_real_staged_git_change(tmp_path: Path) -> None:
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    staged = tmp_path / "staged.txt"
    staged.write_text("ready\n")
    subprocess.run(["git", "add", "staged.txt"], cwd=tmp_path, check=True)

    assert staged_paths(tmp_path) == ["staged.txt"]


def test_staged_paths_fails_safe_outside_a_git_repository(tmp_path: Path) -> None:
    assert staged_paths(tmp_path) == []


def test_staged_paths_fails_safe_when_git_is_not_on_path(tmp_path: Path) -> None:
    original_path = os.environ["PATH"]
    os.environ["PATH"] = ""
    try:
        assert staged_paths(tmp_path) == []
    finally:
        os.environ["PATH"] = original_path


def test_gate_mode_requires_an_identifier(repo_root: Path) -> None:
    with pytest.raises(ValueError, match="requires gate_id"):
        run((), mode="gate", repo_root=repo_root)


# --------------------------------------------------------------------------- #
# mixed python + shell catalogue through the programmatic API
# --------------------------------------------------------------------------- #


def test_mixed_python_and_shell_catalogue(
    checks_dir: Path, repo_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _write_py_check(checks_dir, "py_pass", "return 0")
    _write_py_check(checks_dir, "py_fail", "return 1")
    _write_sh_check(checks_dir, "check-sh-pass.sh", exit_code=0)
    _write_sh_check(checks_dir, "check-sh-fail.sh", exit_code=1)
    rules = (
        RuleEntry(id="M1", gate="m1", check="py_pass", summary="py pass"),
        RuleEntry(id="M2", gate="m2", check="sh_pass", summary="sh pass", script="check-sh-pass.sh"),
        RuleEntry(id="M3", gate="m3", check="py_fail", summary="py fail"),
        RuleEntry(id="M4", gate="m4", check="sh_fail", summary="sh fail", script="check-sh-fail.sh"),
    )

    verdict = run(rules, mode="all", repo_root=repo_root, checks_dir=checks_dir)
    out = _plain(capsys.readouterr().out)

    assert verdict.ran == 4
    assert sorted(verdict.failures) == ["M3", "M4"]
    assert "2/4 rule(s) failed: M3, M4" in out


# --------------------------------------------------------------------------- #
# run_all gating + --gate selection + dedup
# --------------------------------------------------------------------------- #


def test_run_all_false_is_excluded_from_all(checks_dir: Path, repo_root: Path) -> None:
    _write_py_check(checks_dir, "always", "return 0")
    _write_py_check(checks_dir, "elsewhere", "return 1")  # would FAIL if dispatched
    rules = (
        RuleEntry(id="R1", gate="r1", check="always", summary="always"),
        RuleEntry(id="R2", gate="r2", check="elsewhere", summary="out-of-band", run_all=False),
    )
    verdict = run(rules, mode="all", repo_root=repo_root, checks_dir=checks_dir)
    # R2 is run_all=False → not dispatched, so its FAIL never registers.
    assert verdict.ok
    assert verdict.ran == 1


def test_gate_selects_one_rule_by_id(
    checks_dir: Path, repo_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _write_py_check(checks_dir, "one", "return 0")
    _write_py_check(checks_dir, "two", "return 1")
    rules = (
        RuleEntry(id="G1", gate="g1", check="one", summary="one"),
        RuleEntry(id="G2", gate="g2", check="two", summary="two"),
    )
    verdict = run(rules, mode="gate", gate_id="g1", repo_root=repo_root, checks_dir=checks_dir)
    out = _plain(capsys.readouterr().out)
    assert verdict.ok
    assert verdict.ran == 1
    assert "=== Architecture fitness function: g1 ===" in out
    assert "G2" not in out


def test_gate_unknown_id_returns_exit_2_via_main_cli(checks_dir: Path, repo_root: Path) -> None:
    rules = (RuleEntry(id="X1", gate="x1", check="one", summary="one"),)
    rc = main_cli(rules, ["--gate", "nope"], repo_root=repo_root, checks_dir=checks_dir)
    assert rc == 2


def test_duplicate_resolved_script_runs_once(checks_dir: Path, repo_root: Path) -> None:
    # Two entries resolving to the SAME script dispatch that script once
    # (kairix's F7/F9-style shared-script dedup).
    _write_py_check(checks_dir, "shared", "return 0")
    rules = (
        RuleEntry(id="D1", gate="d1", check="shared", summary="first"),
        RuleEntry(id="D2", gate="d2", check="shared", summary="second"),
    )
    verdict = run(rules, mode="all", repo_root=repo_root, checks_dir=checks_dir)
    assert verdict.ran == 1  # deduped


# --------------------------------------------------------------------------- #
# proposed entries are skipped
# --------------------------------------------------------------------------- #


def test_proposed_entry_is_not_dispatched(checks_dir: Path, repo_root: Path) -> None:
    _write_py_check(checks_dir, "real", "return 0")
    rules = (
        RuleEntry(id="PR1", gate="pr1", check="real", summary="real"),
        RuleEntry(id="PR2", gate="pr2", check="(proposed)", summary="future", status="proposed"),
    )
    verdict = run(rules, mode="all", repo_root=repo_root, checks_dir=checks_dir)
    assert verdict.ran == 1  # the proposed rule contributed nothing


# --------------------------------------------------------------------------- #
# conditional (runtime-arg) subprocess check — coverage-style
# --------------------------------------------------------------------------- #


def test_conditional_check_skips_when_input_absent_with_custom_text(
    checks_dir: Path, repo_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _write_sh_check(checks_dir, "check-cov.sh", exit_code=0)
    rules = (
        RuleEntry(
            id="COV",
            gate="cov",
            check="cov",
            summary="coverage",
            script="check-cov.sh",
            subprocess_arg_env="NONEXISTENT_COVERAGE_XML",
        ),
    )

    def conditional(entry: RuleEntry) -> ConditionalResult:
        # The consumer's exact skip text — proves the byte-identical skip-line hook.
        return ConditionalResult(run=False, skip_lines=(f"skip [{entry.id}] — coverage report not found",))

    verdict = run(
        rules,
        mode="all",
        repo_root=repo_root,
        checks_dir=checks_dir,
        conditional_check=conditional,
    )
    out = _plain(capsys.readouterr().out)
    assert verdict.skipped == 1
    assert verdict.ran == 0
    assert "skip [COV] — coverage report not found" in out


def test_conditional_check_runs_with_extra_args(checks_dir: Path, repo_root: Path) -> None:
    # The shell detector asserts it received the runtime arg.
    (checks_dir / "check-cov2.sh").write_text(
        '#!/usr/bin/env bash\n[ "$1" = "/tmp/the-report.xml" ] && exit 0 || exit 9\n'
    )
    (checks_dir / "check-cov2.sh").chmod(0o755)
    rules = (
        RuleEntry(
            id="COV2",
            gate="cov2",
            check="cov2",
            summary="coverage2",
            script="check-cov2.sh",
            subprocess_arg_env="X",
        ),
    )

    def conditional(_entry: RuleEntry) -> ConditionalResult:
        return ConditionalResult(run=True, extra_args=("/tmp/the-report.xml",))

    verdict = run(
        rules, mode="all", repo_root=repo_root, checks_dir=checks_dir, conditional_check=conditional
    )
    assert verdict.ok  # detector saw the arg


def test_conditional_builtin_env_resolution(
    checks_dir: Path, repo_root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # With NO conditional hook, the runner falls back to env-var resolution:
    # the arg path is read from the declared env var; absent → skip.
    report = repo_root / "coverage.xml"
    report.write_text("<coverage/>")
    (checks_dir / "check-cov3.sh").write_text(
        f'#!/usr/bin/env bash\n[ "$1" = "{report}" ] && exit 0 || exit 9\n'
    )
    (checks_dir / "check-cov3.sh").chmod(0o755)
    rules = (
        RuleEntry(
            id="COV3",
            gate="cov3",
            check="cov3",
            summary="cov3",
            script="check-cov3.sh",
            subprocess_arg_env="MY_COVERAGE_XML",
            subprocess_arg_default="coverage.xml",
        ),
    )
    monkeypatch.delenv("MY_COVERAGE_XML", raising=False)
    verdict = run(rules, mode="all", repo_root=repo_root, checks_dir=checks_dir)
    assert verdict.ok  # default path resolved + exists


def test_conditional_check_hook_declining_a_rule_falls_back_to_builtin_resolution(
    checks_dir: Path, repo_root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A ``conditional_check`` hook may return ``None`` to decline a rule.

    The docstring on :data:`ConditionalCheck` promises the built-in env-var
    resolution then applies, exactly as if no hook were installed at all —
    this is what lets a consumer's hook narrow itself to the rules it cares
    about and let every other ``subprocess_arg_env`` rule through unmodified.
    """
    report = repo_root / "coverage.xml"
    report.write_text("<coverage/>")
    (checks_dir / "check-cov4.sh").write_text(
        f'#!/usr/bin/env bash\n[ "$1" = "{report}" ] && exit 0 || exit 9\n'
    )
    (checks_dir / "check-cov4.sh").chmod(0o755)
    rules = (
        RuleEntry(
            id="COV4",
            gate="cov4",
            check="cov4",
            summary="cov4",
            script="check-cov4.sh",
            subprocess_arg_env="MY_COVERAGE_XML_4",
            subprocess_arg_default="coverage.xml",
        ),
    )
    monkeypatch.delenv("MY_COVERAGE_XML_4", raising=False)

    def declining_hook(_entry: RuleEntry) -> ConditionalResult | None:
        return None

    verdict = run(
        rules, mode="all", repo_root=repo_root, checks_dir=checks_dir, conditional_check=declining_hook
    )
    assert verdict.ok  # the hook declined; the built-in default path resolved + exists


# --------------------------------------------------------------------------- #
# main_cli thin-consumer surface
# --------------------------------------------------------------------------- #


def test_main_cli_default_is_all(checks_dir: Path, repo_root: Path) -> None:
    _write_py_check(checks_dir, "cli_pass", "return 0")
    rules = (RuleEntry(id="CLI1", gate="cli1", check="cli_pass", summary="cli"),)
    rc = main_cli(rules, [], repo_root=repo_root, checks_dir=checks_dir)
    assert rc == 0


def test_main_cli_returns_1_on_failure(checks_dir: Path, repo_root: Path) -> None:
    _write_py_check(checks_dir, "cli_fail", "return 1")
    rules = (RuleEntry(id="CLI2", gate="cli2", check="cli_fail", summary="cli"),)
    rc = main_cli(rules, ["--all"], repo_root=repo_root, checks_dir=checks_dir)
    assert rc == 1


def test_runner_config_puts_checks_dir_on_sys_path(checks_dir: Path, repo_root: Path) -> None:
    before = list(sys.path)
    try:
        RunnerConfig(repo_root=repo_root, checks_dir=checks_dir)
        assert str(checks_dir) in sys.path
    finally:
        sys.path[:] = before


# --------------------------------------------------------------------------- #
# make_env_path_conditional_check — declarative ConditionalCheck factory (1.4)
#
# Generalises kairix's _make_conditional_check + _coverage_xml_path: resolve a
# runtime-arg path from an env var (else a repo-relative default), run with it
# appended when present, or skip with the consumer's EXACT skip lines when forced
# (--skip-coverage-style) or absent. The env-var name, default, force predicate,
# and both skip-line sets are all CONFIG.
# --------------------------------------------------------------------------- #


def test_conditional_factory_runs_with_resolved_default_path(tmp_path: Path) -> None:
    report = tmp_path / "coverage.xml"
    report.write_text("<coverage/>")
    hook = make_env_path_conditional_check(
        env_var="MY_COV_XML",
        default_rel="coverage.xml",
        repo_root=tmp_path,
    )
    entry = RuleEntry(id="F7", gate="f7", check="cov", subprocess_arg_env="MY_COV_XML")
    result = hook(entry)
    assert result is not None
    assert result.run is True
    assert result.extra_args == (str(report),)


def test_conditional_factory_env_var_wins_over_default(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    env_report = tmp_path / "from-env.xml"
    env_report.write_text("<coverage/>")
    (tmp_path / "coverage.xml").write_text("<coverage/>")  # default also present
    monkeypatch.setenv("MY_COV_XML", str(env_report))
    hook = make_env_path_conditional_check(
        env_var="MY_COV_XML", default_rel="coverage.xml", repo_root=tmp_path
    )
    result = hook(RuleEntry(id="F7", gate="f7", check="cov", subprocess_arg_env="MY_COV_XML"))
    assert result is not None
    assert result.extra_args == (str(env_report),)


def test_conditional_factory_skips_when_path_absent_with_exact_lines(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("MY_COV_XML", raising=False)
    hook = make_env_path_conditional_check(
        env_var="MY_COV_XML",
        default_rel="coverage.xml",  # does not exist
        repo_root=tmp_path,
        absent_skip_lines=(
            "skip [F7] check_cov.py — coverage report not found",
            "   run: pytest --cov first",
        ),
    )
    result = hook(RuleEntry(id="F7", gate="f7", check="cov", subprocess_arg_env="MY_COV_XML"))
    assert result is not None
    assert result.run is False
    assert result.skip_lines == (
        "skip [F7] check_cov.py — coverage report not found",
        "   run: pytest --cov first",
    )


def test_conditional_factory_force_skip_short_circuits_with_exact_lines(tmp_path: Path) -> None:
    # The --skip-coverage path: force_skip() True ⇒ skip with force_skip_lines,
    # even if the report exists.
    (tmp_path / "coverage.xml").write_text("<coverage/>")
    hook = make_env_path_conditional_check(
        env_var="MY_COV_XML",
        default_rel="coverage.xml",
        repo_root=tmp_path,
        force_skip=lambda: True,
        force_skip_lines=("skip [F7] check_cov.py — --skip-coverage",),
    )
    result = hook(RuleEntry(id="F7", gate="f7", check="cov", subprocess_arg_env="MY_COV_XML"))
    assert result is not None
    assert result.run is False
    assert result.skip_lines == ("skip [F7] check_cov.py — --skip-coverage",)


def test_conditional_factory_force_skip_false_falls_through_to_run(tmp_path: Path) -> None:
    (tmp_path / "coverage.xml").write_text("<coverage/>")
    hook = make_env_path_conditional_check(
        env_var="MY_COV_XML",
        default_rel="coverage.xml",
        repo_root=tmp_path,
        force_skip=lambda: False,
        force_skip_lines=("unused",),
    )
    result = hook(RuleEntry(id="F7", gate="f7", check="cov", subprocess_arg_env="MY_COV_XML"))
    assert result is not None
    assert result.run is True


def test_conditional_factory_wires_into_runner_skip(
    checks_dir: Path, repo_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    # End-to-end: the factory hook passed as conditional_check skips the rule and
    # prints the consumer's exact lines.
    _write_sh_check(checks_dir, "check-cov.sh", exit_code=0)
    rules = (
        RuleEntry(
            id="COVE",
            gate="cove",
            check="cov",
            summary="coverage",
            script="check-cov.sh",
            subprocess_arg_env="MY_COV_XML",
        ),
    )
    hook = make_env_path_conditional_check(
        env_var="MY_COV_XML",
        default_rel="nope.xml",
        repo_root=repo_root,
        absent_skip_lines=("skip [COVE] check-cov.sh — coverage report not found",),
    )
    verdict = run(rules, mode="all", repo_root=repo_root, checks_dir=checks_dir, conditional_check=hook)
    out = _plain(capsys.readouterr().out)
    assert verdict.skipped == 1
    assert "skip [COVE] check-cov.sh — coverage report not found" in out


def test_conditional_factory_per_entry_skip_line_differs_by_id(tmp_path: Path) -> None:
    # DEFECT-1 regression: F7 and F9 share ONE script (check_per_file_coverage.py)
    # and differ ONLY by entry.id. A static skip tuple emits IDENTICAL text for
    # both; the per-entry callable interpolates `skip [{entry.id}]` so the two
    # produced lines differ — the byte-identity ledger contract for shared-script
    # rules. The fn form must win, receive the RuleEntry, and resolve per id.
    hook = make_env_path_conditional_check(
        env_var="MY_COV_XML",
        default_rel="nope.xml",  # absent → exercise the absent-skip path
        repo_root=tmp_path,
        absent_skip_line_fn=lambda e: (
            f"skip [{e.id}] check_per_file_coverage.py — coverage report not found",
            f"   run: pytest --cov first ({e.id})",
        ),
    )
    f7 = RuleEntry(
        id="F7",
        gate="f7",
        check="per_file_coverage",
        script="check_per_file_coverage.py",
        subprocess_arg_env="MY_COV_XML",
    )
    f9 = RuleEntry(
        id="F9",
        gate="f9",
        check="per_file_coverage",
        script="check_per_file_coverage.py",
        subprocess_arg_env="MY_COV_XML",
    )
    r7 = hook(f7)
    r9 = hook(f9)
    assert r7 is not None and r9 is not None
    assert r7.run is False and r9.run is False
    assert r7.skip_lines == (
        "skip [F7] check_per_file_coverage.py — coverage report not found",
        "   run: pytest --cov first (F7)",
    )
    assert r9.skip_lines == (
        "skip [F9] check_per_file_coverage.py — coverage report not found",
        "   run: pytest --cov first (F9)",
    )
    # The two skip ledgers are DISTINCT despite sharing one script.
    assert r7.skip_lines != r9.skip_lines


def test_conditional_factory_force_skip_line_fn_receives_entry(tmp_path: Path) -> None:
    # DEFECT-1: the forced-skip path also accepts a per-entry callable that wins
    # over the static tuple and interpolates the id.
    (tmp_path / "coverage.xml").write_text("<coverage/>")  # present, but forced
    hook = make_env_path_conditional_check(
        env_var="MY_COV_XML",
        default_rel="coverage.xml",
        repo_root=tmp_path,
        force_skip=lambda: True,
        force_skip_line_fn=lambda e: (f"skip [{e.id}] check_per_file_coverage.py — --skip-coverage",),
    )
    r7 = hook(RuleEntry(id="F7", gate="f7", check="cov", subprocess_arg_env="MY_COV_XML"))
    r9 = hook(RuleEntry(id="F9", gate="f9", check="cov", subprocess_arg_env="MY_COV_XML"))
    assert r7 is not None and r9 is not None
    assert r7.skip_lines == ("skip [F7] check_per_file_coverage.py — --skip-coverage",)
    assert r9.skip_lines == ("skip [F9] check_per_file_coverage.py — --skip-coverage",)


def test_conditional_factory_fn_wins_over_static_tuple(tmp_path: Path) -> None:
    # DEFECT-1: precedence — when both the static tuple and the fn are supplied,
    # the fn wins (per-entry interpolation supersedes the fixed text).
    hook = make_env_path_conditional_check(
        env_var="MY_COV_XML",
        default_rel="nope.xml",
        repo_root=tmp_path,
        absent_skip_lines=("static — WRONG",),
        absent_skip_line_fn=lambda e: (f"skip [{e.id}] — dynamic wins",),
    )
    r = hook(RuleEntry(id="F7", gate="f7", check="cov", subprocess_arg_env="MY_COV_XML"))
    assert r is not None
    assert r.skip_lines == ("skip [F7] — dynamic wins",)


# --------------------------------------------------------------------------- #
# main_cli extra_flags + post_parse — consumer-specific flags (Task 1.4)
#
# Retires kairix's forked main()/--skip-coverage: a consumer declares its flag
# via extra_flags and maps the parsed Namespace to extra run() kwargs (e.g. a
# conditional_check built from the flag) via post_parse.
# --------------------------------------------------------------------------- #


def test_main_cli_extra_flag_is_parsed_and_threaded_via_post_parse(
    checks_dir: Path, repo_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    # The coverage rule would FAIL if dispatched; --skip-coverage must skip it.
    _write_sh_check(checks_dir, "check-covx.sh", exit_code=1)
    rules = (
        RuleEntry(
            id="CX",
            gate="cx",
            check="covx",
            summary="cov",
            script="check-covx.sh",
            subprocess_arg_env="MY_COV_XML",
        ),
    )

    seen: dict[str, object] = {}

    def post_parse(ns: object) -> dict[str, object]:
        seen["skip_coverage"] = ns.skip_coverage  # type: ignore[attr-defined]
        hook = make_env_path_conditional_check(
            env_var="MY_COV_XML",
            default_rel="coverage.xml",
            repo_root=repo_root,
            force_skip=lambda: ns.skip_coverage,  # type: ignore[attr-defined]
            force_skip_lines=("skip [CX] check-covx.sh — --skip-coverage",),
        )
        return {"conditional_check": hook}

    rc = main_cli(
        rules,
        ["--all", "--skip-coverage"],
        repo_root=repo_root,
        checks_dir=checks_dir,
        extra_flags=[("--skip-coverage", {"action": "store_true"})],
        post_parse=post_parse,
    )
    out = _plain(capsys.readouterr().out)
    assert seen["skip_coverage"] is True
    assert rc == 0  # the failing rule was skipped
    assert "skip [CX] check-covx.sh — --skip-coverage" in out


def test_main_cli_extra_flag_absent_defaults_and_dispatches(checks_dir: Path, repo_root: Path) -> None:
    # Without --skip-coverage the post_parse hook lets the rule run (and here the
    # report is absent → the factory skips on absence, not on force).
    _write_sh_check(checks_dir, "check-covy.sh", exit_code=0)
    rules = (
        RuleEntry(
            id="CY",
            gate="cy",
            check="covy",
            summary="cov",
            script="check-covy.sh",
            subprocess_arg_env="MY_COV_XML",
        ),
    )

    def post_parse(ns: object) -> dict[str, object]:
        hook = make_env_path_conditional_check(
            env_var="MY_COV_XML",
            default_rel="nope.xml",
            repo_root=repo_root,
            force_skip=lambda: ns.skip_coverage,  # type: ignore[attr-defined]
            force_skip_lines=("forced",),
            absent_skip_lines=("absent",),
        )
        return {"conditional_check": hook}

    rc = main_cli(
        rules,
        ["--all"],
        repo_root=repo_root,
        checks_dir=checks_dir,
        extra_flags=[("--skip-coverage", {"action": "store_true"})],
        post_parse=post_parse,
    )
    assert rc == 0  # skipped on absence (not forced); no failure registered


def test_main_cli_without_extra_flags_is_byte_identical(checks_dir: Path, repo_root: Path) -> None:
    # The default (no extra_flags / post_parse) is unchanged from v0.3.0.
    _write_py_check(checks_dir, "plain", "return 0")
    rules = (RuleEntry(id="PL", gate="pl", check="plain", summary="plain"),)
    assert main_cli(rules, ["--all"], repo_root=repo_root, checks_dir=checks_dir) == 0


# --------------------------------------------------------------------------- #
# RuleEntry argv-exception fields (Task 1.5)
#
# Generalises taz's _SCRIPT_PATH_OVERRIDES (hermetic smoke), _STATIC_EXTRA_ARGS
# (mutation ratchet --allow-missing-current), _orphan_files_extra
# (ORPHAN_FILES_STRICT → --strict). All declarative on the RuleEntry now.
# --------------------------------------------------------------------------- #


def test_script_path_override_resolves_outside_checks_dir(tmp_path: Path, repo_root: Path) -> None:
    # The override path is resolved relative to the REPO ROOT, not the checks
    # dir — taz's hermetic smoke lives at tests/smoke/hermetic.sh.
    checks_dir = repo_root / "scripts" / "checks"
    checks_dir.mkdir(parents=True)
    smoke_dir = repo_root / "tests" / "smoke"
    smoke_dir.mkdir(parents=True)
    (smoke_dir / "hermetic.sh").write_text("#!/usr/bin/env bash\nexit 0\n")
    (smoke_dir / "hermetic.sh").chmod(0o755)
    rules = (
        RuleEntry(
            id="HSMOKE",
            gate="hsmoke",
            check="hermetic",
            summary="hermetic smoke",
            script="hermetic.sh",
            script_path_override="tests/smoke/hermetic.sh",
        ),
    )
    verdict = run(rules, mode="all", repo_root=repo_root, checks_dir=checks_dir)
    assert verdict.ok
    assert verdict.ran == 1


def test_static_extra_args_always_appended(repo_root: Path) -> None:
    checks_dir = repo_root / "scripts" / "checks"
    checks_dir.mkdir(parents=True)
    # The detector passes only if it sees the static arg.
    (checks_dir / "check-mut.sh").write_text(
        '#!/usr/bin/env bash\n[ "$1" = "--allow-missing-current" ] && exit 0 || exit 7\n'
    )
    (checks_dir / "check-mut.sh").chmod(0o755)
    rules = (
        RuleEntry(
            id="MUT",
            gate="mut",
            check="mut",
            summary="mutation ratchet",
            script="check-mut.sh",
            static_extra_args=("--allow-missing-current",),
        ),
    )
    verdict = run(rules, mode="all", repo_root=repo_root, checks_dir=checks_dir)
    assert verdict.ok


def test_env_gated_extra_arg_present_only_when_env_set(
    repo_root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    checks_dir = repo_root / "scripts" / "checks"
    checks_dir.mkdir(parents=True)
    # Detector exits 0 IFF it sees --strict as $1.
    (checks_dir / "check-orphan.sh").write_text(
        '#!/usr/bin/env bash\n[ "$1" = "--strict" ] && exit 0 || exit 5\n'
    )
    (checks_dir / "check-orphan.sh").chmod(0o755)
    rules = (
        RuleEntry(
            id="ORPH",
            gate="orph",
            check="orphan",
            summary="orphan files",
            script="check-orphan.sh",
            env_gated_extra_args=(("ORPHAN_FILES_STRICT", "--strict"),),
        ),
    )
    # Env set → the gated arg appears → detector passes.
    monkeypatch.setenv("ORPHAN_FILES_STRICT", "1")
    assert run(rules, mode="all", repo_root=repo_root, checks_dir=checks_dir).ok

    # Env unset → the gated arg is absent → detector FAILs (proves gating).
    monkeypatch.delenv("ORPHAN_FILES_STRICT", raising=False)
    assert not run(rules, mode="all", repo_root=repo_root, checks_dir=checks_dir).ok


def test_static_and_env_gated_args_order(repo_root: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # static args come before env-gated args, both after any conditional arg.
    checks_dir = repo_root / "scripts" / "checks"
    checks_dir.mkdir(parents=True)
    (checks_dir / "check-both.sh").write_text(
        '#!/usr/bin/env bash\n[ "$1" = "--static" ] && [ "$2" = "--gated" ] && exit 0 || exit 4\n'
    )
    (checks_dir / "check-both.sh").chmod(0o755)
    rules = (
        RuleEntry(
            id="BOTH",
            gate="both",
            check="both",
            summary="both",
            script="check-both.sh",
            static_extra_args=("--static",),
            env_gated_extra_args=(("GATE_ENV", "--gated"),),
        ),
    )
    monkeypatch.setenv("GATE_ENV", "1")
    assert run(rules, mode="all", repo_root=repo_root, checks_dir=checks_dir).ok


# --------------------------------------------------------------------------- #
# public subprocess-dispatch mode + promoted ledger primitives (Task 1.6)
#
# So taz drops its 7 private-symbol imports and reimplemented dispatch.
# --------------------------------------------------------------------------- #


def test_dispatch_subprocess_routes_python_checks_through_subprocess(
    checks_dir: Path, repo_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    # A pure-python check that would run IN-PROCESS by default is routed through
    # the guarded subprocess path when dispatch="subprocess". It writes a marker
    # to a file from its OWN process so we can prove it ran out-of-process.
    marker = repo_root / "ran_in_subprocess.txt"
    (checks_dir / "check_subp.py").write_text(
        "import os, sys\n"
        "def main():\n"
        f"    open(r'{marker}', 'w').write(str(os.getpid()))\n"
        "    return 0\n"
        "if __name__ == '__main__':\n"
        "    sys.exit(main())\n"
    )
    rules = (RuleEntry(id="SUBP", gate="subp", check="subp", summary="subp"),)
    verdict = run(rules, mode="all", repo_root=repo_root, checks_dir=checks_dir, dispatch="subprocess")
    out = _plain(capsys.readouterr().out)
    assert verdict.ok
    assert verdict.ran == 1
    assert marker.exists()  # ran as a real child process
    child_pid = int(marker.read_text())
    import os as _os

    assert child_pid != _os.getpid()  # genuinely a different process
    assert "PASS [SUBP] subp" in out


def test_dispatch_subprocess_produces_same_aggregate_banner(
    checks_dir: Path, repo_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    # Run-as-a-file needs a main guard (subprocess invokes the script directly).
    (checks_dir / "check_sp_ok.py").write_text(
        "import sys\ndef main():\n    return 0\nif __name__ == '__main__':\n    sys.exit(main())\n"
    )
    (checks_dir / "check_sp_bad.py").write_text(
        "import sys\ndef main():\n    return 1\nif __name__ == '__main__':\n    sys.exit(main())\n"
    )
    rules = (
        RuleEntry(id="SO", gate="so", check="sp_ok", summary="ok"),
        RuleEntry(id="SB", gate="sb", check="sp_bad", summary="bad"),
    )
    verdict = run(rules, mode="all", repo_root=repo_root, checks_dir=checks_dir, dispatch="subprocess")
    out = _plain(capsys.readouterr().out)
    assert verdict.failures == ["SB"]
    assert "1/2 rule(s) failed: SB" in out


def test_main_cli_dispatch_subprocess_kwarg(checks_dir: Path, repo_root: Path) -> None:
    _write_py_check(checks_dir, "cli_subp", "import sys; sys.exit(0)")
    rules = (RuleEntry(id="CS", gate="cs", check="cli_subp", summary="cs"),)
    rc = main_cli(rules, ["--all"], repo_root=repo_root, checks_dir=checks_dir, dispatch="subprocess")
    assert rc == 0


def test_default_dispatch_is_inprocess(checks_dir: Path, repo_root: Path) -> None:
    # The v0.3.0 default: pure-python checks run in-process (no dispatch kwarg).
    marker = repo_root / "should_not_exist.txt"
    (checks_dir / "check_ip.py").write_text("import os\ndef main():\n    return 0\n")
    rules = (RuleEntry(id="IP", gate="ip", check="ip", summary="ip"),)
    verdict = run(rules, mode="all", repo_root=repo_root, checks_dir=checks_dir)
    assert verdict.ok
    assert not marker.exists()


# promoted ledger primitives -------------------------------------------------- #


def test_argv_exception_fields_work_in_parallel_dispatch(
    repo_root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # The same argv assembly must hold on the parallel subprocess path.
    checks_dir = repo_root / "scripts" / "checks"
    checks_dir.mkdir(parents=True)
    (checks_dir / "check-par.sh").write_text('#!/usr/bin/env bash\n[ "$1" = "--s" ] && exit 0 || exit 6\n')
    (checks_dir / "check-par.sh").chmod(0o755)
    rules = (
        RuleEntry(
            id="PAR",
            gate="par",
            check="par",
            summary="par",
            script="check-par.sh",
            static_extra_args=("--s",),
        ),
    )
    assert run(rules, mode="all", repo_root=repo_root, checks_dir=checks_dir, parallel_subprocess=True).ok


# --------------------------------------------------------------------------- #
# core: entries — config injection + in-process dispatch (v0.6.1)
# --------------------------------------------------------------------------- #

_CORE_DUP_FIXTURE = '''"""docstring."""


def a() -> None:
    raise ValueError("a repeated long literal")


def b() -> None:
    raise ValueError("a repeated long literal")


def c() -> None:
    raise ValueError("a repeated long literal")
'''


def _core_rule() -> tuple[RuleEntry, ...]:
    return (
        RuleEntry(
            id="no-duplicate-string",
            gate="no-duplicate-string",
            check="core:no_duplicate_string",
            summary="no duplicated literal",
        ),
    )


def test_core_entry_injects_config_and_flags(repo_root: Path, capsys: pytest.CaptureFixture[str]) -> None:
    (repo_root / "src").mkdir()
    (repo_root / "src" / "dup.py").write_text(_CORE_DUP_FIXTURE, encoding="utf-8")
    verdict = run(
        _core_rule(),
        mode="all",
        repo_root=repo_root,
        core_check_configs={"no_duplicate_string": {"roots": ["src"], "min_occurrences": 3}},
    )
    out = _plain(capsys.readouterr().out)
    assert not verdict.ok
    assert "FAIL [no-duplicate-string]" in out
    assert "dup.py" in out


def test_core_entry_without_config_is_vacuous(repo_root: Path) -> None:
    (repo_root / "src").mkdir()
    (repo_root / "src" / "dup.py").write_text(_CORE_DUP_FIXTURE, encoding="utf-8")
    # No config block → roots=() → nothing enumerated → vacuous pass.
    assert run(_core_rule(), mode="all", repo_root=repo_root).ok


def test_core_entry_in_process_even_under_subprocess_dispatch(
    repo_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (repo_root / "src").mkdir()
    (repo_root / "src" / "dup.py").write_text(_CORE_DUP_FIXTURE, encoding="utf-8")
    verdict = run(
        _core_rule(),
        mode="all",
        repo_root=repo_root,
        dispatch="subprocess",
        core_check_configs={"no_duplicate_string": {"roots": ["src"]}},
    )
    out = _plain(capsys.readouterr().out)
    assert not verdict.ok
    assert "FAIL [no-duplicate-string]" in out
    assert "check script not found" not in out


def test_core_entry_establish_baseline_then_passes(repo_root: Path) -> None:
    (repo_root / "src").mkdir()
    (repo_root / "src" / "dup.py").write_text(_CORE_DUP_FIXTURE, encoding="utf-8")
    cfg_kwargs = {
        "repo_root": repo_root,
        "core_check_configs": {"no_duplicate_string": {"roots": ["src"]}},
    }
    # Establish writes the baseline and passes…
    assert run(_core_rule(), mode="all", establish_baseline=True, **cfg_kwargs).ok  # type: ignore[arg-type]
    baseline = repo_root / ".architecture" / "baseline" / "no-duplicate-string-files.txt"
    assert baseline.exists()
    assert "src/dup.py" in baseline.read_text(encoding="utf-8")
    # …and the subsequent gate run passes (offender grandfathered).
    assert run(_core_rule(), mode="all", **cfg_kwargs).ok  # type: ignore[arg-type]


# --------------------------------------------------------------------------- #
# detector-declared skips — a rule that did not examine its subject
# --------------------------------------------------------------------------- #


def test_declared_skip_reason_reads_a_colon_form() -> None:
    entry = RuleEntry(id="S1", gate="s1", check="osv_scanner_sca", summary="sca")
    assert declared_skip_reason(entry, "SKIP osv_scanner_sca: binary not on PATH\n") == "binary not on PATH"


def test_declared_skip_reason_reads_a_parenthesised_form() -> None:
    entry = RuleEntry(id="S2", gate="s2", check="coverage_includes_branches", summary="cov")
    out = "SKIP coverage_includes_branches (coverage.xml not present)\n"
    assert declared_skip_reason(entry, out) == "coverage.xml not present"


def test_declared_skip_reason_matches_the_rule_id_too() -> None:
    entry = RuleEntry(id="branch_naming", gate="bn", check="branch_naming", summary="bn")
    assert declared_skip_reason(entry, "SKIP branch_naming: detached HEAD") == "detached HEAD"


def test_declared_skip_reason_ignores_a_rule_reporting_about_other_skips() -> None:
    """A check whose SUBJECT is skipping must not classify itself as skipped.

    taz ships ``test_skip_rationale``, which reports on skipped tests. Matching a
    bare ``SKIP`` substring would delete it from the ledger — turning a fix for
    invisible skips into a new invisible skip.
    """
    entry = RuleEntry(id="TSR", gate="tsr", check="test_skip_rationale", summary="skip rationale")
    out = "SKIP without rationale: tests/test_a.py::test_b\nFound 1 offender\n"
    assert declared_skip_reason(entry, out) is None


def test_declared_skip_reason_returns_none_for_ordinary_output() -> None:
    entry = RuleEntry(id="S3", gate="s3", check="alpha", summary="alpha")
    assert declared_skip_reason(entry, "checked 12 files\n") is None


def test_inprocess_detector_printing_skip_is_not_counted_as_passed(
    checks_dir: Path, repo_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _write_py_check(checks_dir, "alpha", "print('SKIP alpha: tool not installed')\nreturn 0")
    rules = (RuleEntry(id="A1", gate="a1", check="alpha", summary="alpha rule"),)

    verdict = run(rules, mode="all", repo_root=repo_root, checks_dir=checks_dir)
    out = _plain(capsys.readouterr().out)

    assert verdict.ran == 0, "a rule that examined nothing must not count as having run"
    assert verdict.skipped == 1
    assert verdict.skips == {"A1": "tool not installed"}
    assert "PASS [A1]" not in out
    assert "SKIP [A1]" in out
    assert "tool not installed" in out


def test_inprocess_skip_exit_code_is_classified_without_any_marker(
    checks_dir: Path, repo_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _write_py_check(checks_dir, "alpha", f"return {SKIP_EXIT_CODE}")
    rules = (RuleEntry(id="A1", gate="a1", check="alpha", summary="alpha rule"),)

    verdict = run(rules, mode="all", repo_root=repo_root, checks_dir=checks_dir)

    assert verdict.ran == 0
    assert verdict.skipped == 1
    assert "A1" in verdict.skips
    assert "PASS [A1]" not in _plain(capsys.readouterr().out)


def test_subprocess_skip_exit_code_is_classified_on_the_noncapturing_path(
    checks_dir: Path, repo_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The default dispatch streams child output straight to fd1, so the exit
    code is the only signal available there."""
    _write_sh_check(checks_dir, "beta.sh", SKIP_EXIT_CODE, echo="SKIP beta: no input")
    rules = (RuleEntry(id="B1", gate="b1", check="beta", script="beta.sh", summary="beta rule"),)

    verdict = run(rules, mode="all", repo_root=repo_root, checks_dir=checks_dir, dispatch="subprocess")

    assert verdict.ran == 0
    assert verdict.skipped == 1
    assert "PASS [B1]" not in _plain(capsys.readouterr().out)


def test_aggregate_banner_names_the_rules_that_did_not_run(
    checks_dir: Path, repo_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _write_py_check(checks_dir, "alpha", "return 0")
    _write_py_check(checks_dir, "beta", "print('SKIP beta: no coverage.xml')\nreturn 0")
    rules = (
        RuleEntry(id="A1", gate="a1", check="alpha", summary="alpha rule"),
        RuleEntry(id="B1", gate="b1", check="beta", summary="beta rule"),
    )

    run(rules, mode="all", repo_root=repo_root, checks_dir=checks_dir)
    out = _plain(capsys.readouterr().out)

    assert "=== All 1 architecture fitness functions passed ===" in out
    assert "1 rule(s) declared themselves skipped" in out
    assert "B1: no coverage.xml" in out


def test_write_skip_report_records_the_gap(tmp_path: Path) -> None:
    verdict = Verdicts(ran=3, skipped=1, skips={"B1": "no coverage.xml"})
    target = tmp_path / "nested" / "skips.json"

    write_skip_report(target, verdict)

    payload = json.loads(target.read_text(encoding="utf-8"))
    assert payload["ran"] == 3
    assert payload["declared_skips"] == [{"rule": "B1", "reason": "no coverage.xml"}]


def test_write_skip_report_is_written_even_when_nothing_skipped(tmp_path: Path) -> None:
    """ "No rule skipped" and "the report never ran" must not look identical —
    that conflation is the defect this contract exists to remove."""
    target = tmp_path / "skips.json"

    write_skip_report(target, Verdicts(ran=2))

    assert json.loads(target.read_text(encoding="utf-8"))["declared_skips"] == []


def test_write_skip_report_without_a_path_writes_nothing(tmp_path: Path) -> None:
    write_skip_report(None, Verdicts(ran=1, skipped=1, skips={"B1": "why"}))
    assert list(tmp_path.iterdir()) == []


def test_a_bounded_process_that_outruns_its_deadline_reports_the_timeout_code(tmp_path: Path) -> None:
    """A deadline must kill the whole group and be distinguishable from a test failure."""
    result = run_bounded_process(
        [sys.executable, "-c", "import time; time.sleep(30)"],
        cwd=tmp_path,
        timeout=0.5,
    )

    assert result.returncode == 124
