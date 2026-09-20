"""Soundness battery for the staged-selection logic.

The non-negotiable property is **no false negative on a staged change**: if
staging a file could newly violate rule R, ``--staged`` MUST run R. These tests
prove the three selection classes (file-local / relational / always-run), the
scope-derivation hook, the fail-safe "run when scope unresolved" residue, the
file-local narrowing through a real enumeration, and the transparent staged
ledger end-to-end through the runner.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from tc_fitness.catalogue import RuleEntry
from tc_fitness.runner import run
from tc_fitness.staged import (
    decide,
    resolve_staged_scope,
    staged_in_scope,
)

pytestmark = pytest.mark.unit

# --------------------------------------------------------------------------- #
# scope resolution: explicit wins, else resolver, else None (fail-safe)
# --------------------------------------------------------------------------- #


def test_explicit_staged_scope_wins() -> None:
    entry = RuleEntry(id="F", gate="f", check="x", staged_scope=("kairix",))
    # Resolver would say something else, but explicit scope is the source of truth.
    assert resolve_staged_scope(entry, "check_x.py", resolver=lambda _s: ("tests",)) == ("kairix",)


def test_derived_scope_via_resolver() -> None:
    entry = RuleEntry(id="F", gate="f", check="x")  # no explicit scope
    assert resolve_staged_scope(entry, "check_x.py", resolver=lambda _s: ("kairix/core",)) == ("kairix/core",)


def test_no_resolver_no_explicit_scope_is_none() -> None:
    entry = RuleEntry(id="F", gate="f", check="x")
    assert resolve_staged_scope(entry, "check_x.py", resolver=None) is None


# --------------------------------------------------------------------------- #
# staged_in_scope path-prefix matching
# --------------------------------------------------------------------------- #


def test_staged_in_scope_directory_prefix() -> None:
    scope = ("kairix",)
    staged = ["kairix/core/x.py", "tests/test_x.py", "kairixx/sneaky.py"]
    # "kairix" matches kairix/... but NOT kairixx (prefix boundary).
    assert staged_in_scope(scope, staged) == ["kairix/core/x.py"]


def test_staged_in_scope_exact_file_prefix() -> None:
    scope = ("kairix/cli.py",)
    assert staged_in_scope(scope, ["kairix/cli.py"]) == ["kairix/cli.py"]
    assert staged_in_scope(scope, ["kairix/cli_helpers.py"]) == []


def test_staged_in_scope_none_is_everything() -> None:
    staged = ["a", "b"]
    assert staged_in_scope(None, staged) == staged


# --------------------------------------------------------------------------- #
# decide() — the three classes, soundness
# --------------------------------------------------------------------------- #


def test_empty_staged_runs_everything() -> None:
    # The pre-commit --all-files quirk: no staged paths ⇒ run everything.
    entry = RuleEntry(id="F", gate="f", check="x", staged_class="file-local", staged_scope=("kairix",))
    assert decide(entry, "check_x.py", []).run is True


def test_always_run_always_dispatches() -> None:
    entry = RuleEntry(id="F50", gate="f50", check="x", staged_class="always-run")
    # Even a totally unrelated staged file runs an always-run rule.
    d = decide(entry, "check_x.py", ["totally/unrelated.txt"])
    assert d.run is True
    assert "always-run" in d.reason


def test_file_local_runs_only_on_in_scope_staged_file() -> None:
    entry = RuleEntry(id="F", gate="f", check="x", staged_class="file-local", staged_scope=("kairix",))
    # In scope → run, and the staged subset is handed back for narrowing.
    in_scope = decide(entry, "check_x.py", ["kairix/a.py", "docs/readme.md"])
    assert in_scope.run is True
    assert in_scope.scope_files == ("kairix/a.py",)
    # Out of scope → skip.
    out_scope = decide(entry, "check_x.py", ["docs/readme.md"])
    assert out_scope.run is False


def test_file_local_unresolved_scope_runs_fail_safe() -> None:
    # SOUNDNESS: a file-local rule whose scope can't be resolved must RUN
    # (never silently skip) when there ARE staged paths.
    entry = RuleEntry(id="F", gate="f", check="x", staged_class="file-local")
    d = decide(entry, "check_x.py", ["anything.py"], resolver=lambda _s: None)
    assert d.run is True
    assert "fail-safe" in d.reason


def test_relational_runs_full_scope_when_any_path_in_scope() -> None:
    entry = RuleEntry(
        id="F30",
        gate="f30",
        check="x",
        staged_class="relational",
        staged_scope=("kairix/cli.py", "tests"),
    )
    # A staged TEST deletion (relational trigger) runs the FULL scope — and
    # crucially returns NO scope_files, so the rule is NOT narrowed.
    d = decide(entry, "check_x.py", ["tests/test_thing.py"])
    assert d.run is True
    assert d.scope_files is None
    # A path outside the relational scope → skip.
    assert decide(entry, "check_x.py", ["docs/x.md"]).run is False


def test_relational_unresolved_scope_runs_when_touched() -> None:
    # A relational rule with an unresolved scope treats ALL staged paths as in
    # scope (staged_in_scope(None) returns everything) → runs.
    entry = RuleEntry(id="F", gate="f", check="x", staged_class="relational")
    d = decide(entry, "check_x.py", ["whatever.py"], resolver=lambda _s: None)
    assert d.run is True


# --------------------------------------------------------------------------- #
# file-local narrowing through a real enumeration
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
# make_module_roots_resolver — declarative ScopeResolver factory (Task 1.2)
#
# Generalises kairix's _kairix_scope_resolver / _roots_from_module. Synthetic
# check modules live in a tmp dir put on sys.path; the resolver imports them by
# name and reads roots in order of specificity. Repo-domain names ("RULE",
# the ABC, the location marker, the fallback roots) are ALL config args.
# --------------------------------------------------------------------------- #


@pytest.fixture
def roots_checks_dir(tmp_path: Path) -> Path:
    """A checks dir on sys.path holding synthetic check modules; cleaned up
    (path entry + imported modules) after the test."""
    d = tmp_path / "scripts" / "checks"
    d.mkdir(parents=True)
    before_path = list(sys.path)
    before_mods = set(sys.modules)
    sys.path.insert(0, str(d))  # mirror RunnerConfig putting the checks dir on path
    yield d
    sys.path[:] = before_path
    for name in set(sys.modules) - before_mods:
        if name.startswith("check_") or name.startswith("_engine_abc"):
            sys.modules.pop(name, None)


# --------------------------------------------------------------------------- #
# make_binding_narrower — declarative EnumerationNarrower factory (Task 1.3)
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
# end-to-end staged dispatch through the runner — the transparent ledger
# --------------------------------------------------------------------------- #


def _write_py_check(checks_dir: Path, name: str, body: str) -> None:
    (checks_dir / f"check_{name}.py").write_text(
        "def main():\n" + "\n".join(f"    {line}" for line in body.splitlines()) + "\n"
    )


# --------------------------------------------------------------------------- #
# staged-mode subprocess output is BYTE-STABLE — capturing format (v0.4.1)
#
# A shell detector's stdout is written to its own process's fd1. The OLD staged
# path routed subprocess checks through the NON-capturing _run_one_subprocess,
# which let the child's direct-fd stdout escape the parent's buffered print()
# (under redirection the child output races / merges with the parent ledger, or
# vanishes from a captured buffer entirely). The --all capturing path buffers
# the child output and replays it IN catalogue order between the run/PASS lines.
# Staged mode must use that SAME capturing format so its output is byte-stable.
# --------------------------------------------------------------------------- #


def _write_noisy_sh(checks_dir: Path, filename: str, exit_code: int, *lines: str) -> None:
    """A shell detector that echoes ``lines`` to its OWN stdout then exits."""
    script = "#!/usr/bin/env bash\n"
    for line in lines:
        script += f'echo "{line}"\n'
    script += f"exit {exit_code}\n"
    (checks_dir / filename).write_text(script)
    (checks_dir / filename).chmod(0o755)


def _staged_run_capturing(
    rules: tuple[RuleEntry, ...], *, repo_root: Path, checks_dir: Path, staged_files: list[str]
) -> str:
    """Run staged mode under redirect_stdout and return the colour-free buffer.

    Redirecting Python's ``sys.stdout`` (the way pre-commit / a CI pipe captures
    a run) is exactly where the non-capturing subprocess path leaks: a child
    writing to the inherited fd1 bypasses the StringIO buffer. So a child's
    detector output is only present in the buffer when the runner CAPTURES it.
    """
    import io
    import re
    from contextlib import redirect_stdout

    buf = io.StringIO()
    with redirect_stdout(buf):
        run(
            rules,
            mode="staged",
            staged_files=staged_files,
            repo_root=repo_root,
            checks_dir=checks_dir,
        )
    return re.sub(r"\x1b\[[0-9;]*m", "", buf.getvalue())
