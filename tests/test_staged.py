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

import tc_fitness
from tc_fitness.catalogue import RuleEntry
from tc_fitness.runner import run
from tc_fitness.staged import (
    decide,
    filter_to_staged,
    make_binding_narrower,
    make_module_roots_resolver,
    resolve_staged_scope,
    restrict_python_files,
    staged_abs_set,
    staged_in_scope,
)

# --------------------------------------------------------------------------- #
# scope resolution: explicit wins, else resolver, else None (fail-safe)
# --------------------------------------------------------------------------- #


def test_explicit_staged_scope_wins() -> None:
    entry = RuleEntry(id="F", gate="f", check="x", staged_scope=("kairix",))
    # Resolver would say something else, but explicit scope is the source of truth.
    assert resolve_staged_scope(entry, "check_x.py", resolver=lambda _s: ("tests",)) == ("kairix",)


def test_derived_scope_via_resolver() -> None:
    entry = RuleEntry(id="F", gate="f", check="x")  # no explicit scope
    assert resolve_staged_scope(entry, "check_x.py", resolver=lambda _s: ("kairix/core",)) == (
        "kairix/core",
    )


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


def test_restrict_python_files_narrows_to_staged(tmp_path: Path) -> None:
    (tmp_path / "kairix").mkdir()
    a = tmp_path / "kairix" / "a.py"
    b = tmp_path / "kairix" / "b.py"
    a.write_text("")
    b.write_text("")

    # Outside the context: both files enumerate.
    full = tc_fitness.python_files("kairix", repo_root=tmp_path)
    assert {p.name for p in full} == {"a.py", "b.py"}

    # Inside the context: only the staged file (a.py) enumerates.
    with restrict_python_files(tmp_path, ["kairix/a.py"]):
        narrowed = tc_fitness.python_files("kairix", repo_root=tmp_path)
    assert {p.name for p in narrowed} == {"a.py"}

    # Restored on exit.
    assert {p.name for p in tc_fitness.python_files("kairix", repo_root=tmp_path)} == {"a.py", "b.py"}


def test_filter_to_staged_keeps_only_staged(tmp_path: Path) -> None:
    a = tmp_path / "a.py"
    b = tmp_path / "b.py"
    a.write_text("")
    b.write_text("")
    staged_abs = staged_abs_set(tmp_path, ["a.py"])
    assert filter_to_staged([a, b], staged_abs) == [a]


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


def test_module_roots_from_boundary_rule_attr(roots_checks_dir: Path) -> None:
    # A module-level boundary-rule object carrying a roots tuple → that tuple.
    # The attr name is CONFIG — passed explicitly (the engine privileges no
    # repo's convention, so "RULE" is not the default; DEFECT-3).
    (roots_checks_dir / "check_boundary.py").write_text(
        "class _R:\n    roots = ('pkg', 'pkg/sub')\nRULE = _R()\n"
    )
    resolver = make_module_roots_resolver(
        checks_dir=roots_checks_dir, boundary_rule_attr="RULE"
    )
    assert resolver("check_boundary.py") == ("pkg", "pkg/sub")


def test_module_roots_boundary_branch_off_by_default(roots_checks_dir: Path) -> None:
    # DEFECT-3 regression: with NO boundary_rule_attr configured, the engine must
    # NOT consult kairix's "RULE" convention — that would privilege one repo's
    # attribute name as the engine default. A module carrying a `RULE` object
    # with roots is IGNORED; nothing else resolves → None (fail-safe).
    (roots_checks_dir / "check_unconfigured.py").write_text(
        "class _R:\n    roots = ('PRIVILEGED',)\nRULE = _R()\n"
    )
    resolver = make_module_roots_resolver(checks_dir=roots_checks_dir)
    assert resolver("check_unconfigured.py") is None


def test_module_roots_from_abc_subclass_classvar(roots_checks_dir: Path) -> None:
    # An ABC subclass declared IN the module exposes a `roots` ClassVar → that.
    # The ABC type is config — the engine bakes in no particular ABC.
    (roots_checks_dir / "_engine_abc.py").write_text(
        "class EngineRule:\n    roots = ()\n"
    )
    (roots_checks_dir / "check_abc.py").write_text(
        "from _engine_abc import EngineRule\n"
        "class MyRule(EngineRule):\n    roots = ('engine/scope',)\n"
    )
    import importlib

    abc_mod = importlib.import_module("_engine_abc")
    resolver = make_module_roots_resolver(
        checks_dir=roots_checks_dir, abc_type=abc_mod.EngineRule
    )
    assert resolver("check_abc.py") == ("engine/scope",)


def test_module_roots_skips_imported_abc_itself(roots_checks_dir: Path) -> None:
    # The imported ABC base (whose __module__ is NOT the check module) must be
    # skipped — only the check's OWN subclass roots count. The base here has
    # non-empty roots that must be ignored.
    (roots_checks_dir / "_engine_abc2.py").write_text(
        "class EngineRule2:\n    roots = ('WRONG',)\n"
    )
    (roots_checks_dir / "check_owns_no_subclass.py").write_text(
        "from _engine_abc2 import EngineRule2\n"  # imports base, declares none
    )
    import importlib

    base = importlib.import_module("_engine_abc2").EngineRule2
    resolver = make_module_roots_resolver(
        checks_dir=roots_checks_dir, abc_type=base, fallback_roots=None
    )
    # No own subclass → the imported base's roots are ignored → None.
    assert resolver("check_owns_no_subclass.py") is None


def test_module_roots_location_marker_fallback(roots_checks_dir: Path) -> None:
    # The optional location-marker hook generalises kairix's "imports the
    # location engine → walk the production package" branch.
    (roots_checks_dir / "check_located.py").write_text("MARKER = True\n")

    def location_marker(module: object) -> tuple[str, ...] | None:
        return ("prod_pkg",) if getattr(module, "MARKER", False) else None

    resolver = make_module_roots_resolver(
        checks_dir=roots_checks_dir, location_marker=location_marker
    )
    assert resolver("check_located.py") == ("prod_pkg",)


def test_module_roots_fallback_roots_when_nothing_resolves(roots_checks_dir: Path) -> None:
    (roots_checks_dir / "check_bare.py").write_text("x = 1\n")
    resolver = make_module_roots_resolver(
        checks_dir=roots_checks_dir, fallback_roots=("default_scope",)
    )
    assert resolver("check_bare.py") == ("default_scope",)


def test_module_roots_none_for_shell_script(roots_checks_dir: Path) -> None:
    # A .sh detector can't be introspected → None (caller runs fail-safe).
    resolver = make_module_roots_resolver(checks_dir=roots_checks_dir)
    assert resolver("check-shell.sh") is None


def test_module_roots_import_failure_is_fail_safe_none(roots_checks_dir: Path) -> None:
    (roots_checks_dir / "check_broken.py").write_text("import does_not_exist_xyz\n")
    resolver = make_module_roots_resolver(checks_dir=roots_checks_dir)
    assert resolver("check_broken.py") is None


def test_module_roots_boundary_attr_is_configurable(roots_checks_dir: Path) -> None:
    # The attr name is config — a repo using a different module-level name works.
    (roots_checks_dir / "check_renamed.py").write_text(
        "class _R:\n    paths = ('aaa',)\nBOUNDARY = _R()\n"
    )
    resolver = make_module_roots_resolver(
        checks_dir=roots_checks_dir, boundary_rule_attr="BOUNDARY", roots_attr="paths"
    )
    assert resolver("check_renamed.py") == ("aaa",)


# --------------------------------------------------------------------------- #
# make_binding_narrower — declarative EnumerationNarrower factory (Task 1.3)
# --------------------------------------------------------------------------- #


def test_binding_narrower_narrows_check_module_python_files_binding(
    roots_checks_dir: Path, tmp_path: Path
) -> None:
    # A check module that bound `python_files` BY VALUE at import time has its
    # local name narrowed inside the context, restored on exit.
    (roots_checks_dir / "check_binder.py").write_text(
        "from tc_fitness import python_files\n"
    )
    import importlib

    mod = importlib.import_module("check_binder")
    (tmp_path / "kairix").mkdir()
    (tmp_path / "kairix" / "a.py").write_text("")
    (tmp_path / "kairix" / "b.py").write_text("")

    narrower = make_binding_narrower()
    # Outside: the module's binding walks both files.
    assert {p.name for p in mod.python_files("kairix", repo_root=tmp_path)} == {"a.py", "b.py"}
    with narrower(tmp_path, ["kairix/a.py"]):
        narrowed = {p.name for p in mod.python_files("kairix", repo_root=tmp_path)}
    assert narrowed == {"a.py"}
    # Restored on exit (the original free function is back).
    assert {p.name for p in mod.python_files("kairix", repo_root=tmp_path)} == {"a.py", "b.py"}


def test_binding_narrower_package_level_via_runner_composition(tmp_path: Path) -> None:
    # The package-level tc_fitness.python_files surface is the RUNNER's job
    # (restrict_python_files), NOT the binding narrower's — the narrower handles
    # only the by-value bindings (DEFECT-2: no redundant internal restrict wrap).
    # Composed exactly as the runner's _run_staged_one does (restrict outer,
    # narrower inner), the package attribute IS narrowed.
    from contextlib import ExitStack

    (tmp_path / "kairix").mkdir()
    (tmp_path / "kairix" / "a.py").write_text("")
    (tmp_path / "kairix" / "b.py").write_text("")
    narrower = make_binding_narrower()
    with ExitStack() as stack:
        stack.enter_context(restrict_python_files(tmp_path, ["kairix/a.py"]))
        stack.enter_context(narrower(tmp_path, ["kairix/a.py"]))
        narrowed = {p.name for p in tc_fitness.python_files("kairix", repo_root=tmp_path)}
    assert narrowed == {"a.py"}
    assert {p.name for p in tc_fitness.python_files("kairix", repo_root=tmp_path)} == {"a.py", "b.py"}


def test_binding_narrower_extra_method_patches_and_restores(tmp_path: Path) -> None:
    # The kairix-specific residue: patch THIS ABC's enumerate_files. The
    # (type, method-name) pair is config; the engine bakes in no ABC.
    captured: dict[str, object] = {}

    class _ABC:
        def enumerate_files(self) -> list[Path]:
            return [tmp_path / "kairix" / "a.py", tmp_path / "kairix" / "b.py"]

    (tmp_path / "kairix").mkdir()
    (tmp_path / "kairix" / "a.py").write_text("")
    (tmp_path / "kairix" / "b.py").write_text("")

    original = _ABC.enumerate_files
    narrower = make_binding_narrower(extra_method=(_ABC, "enumerate_files"))
    inst = _ABC()
    with narrower(tmp_path, ["kairix/a.py"]):
        captured["narrowed"] = [p.name for p in inst.enumerate_files()]
        captured["patched_is_not_original"] = _ABC.enumerate_files is not original
    assert captured["narrowed"] == ["a.py"]
    assert captured["patched_is_not_original"] is True
    # Restored exactly.
    assert _ABC.enumerate_files is original
    assert [p.name for p in inst.enumerate_files()] == ["a.py", "b.py"]


def test_binding_narrower_narrows_under_runner_restrict_composition(
    roots_checks_dir: Path, tmp_path: Path
) -> None:
    # DEFECT-2 regression: the SHIPPING path. The runner's _run_staged_one wraps
    # restrict_python_files(repo_root, staged) AROUND the consumer's narrower
    # (restrict + narrower nested). Under that composition the package attribute
    # tc_fitness.python_files is ALREADY rebound to the scoped function before the
    # narrower captures its "original", so the per-check by-value binding identity
    # test `bound is real_python_files` never matches → the ~16 kairix check
    # modules that `from tc_fitness import python_files` are NEVER re-narrowed.
    # This test composes exactly as the runner does and asserts a real check_*
    # module binding IS narrowed.
    (roots_checks_dir / "check_composed_binder.py").write_text(
        "from tc_fitness import python_files\n"
    )
    import importlib

    mod = importlib.import_module("check_composed_binder")
    (tmp_path / "kairix").mkdir()
    (tmp_path / "kairix" / "a.py").write_text("")
    (tmp_path / "kairix" / "b.py").write_text("")

    narrower = make_binding_narrower()
    # Compose EXACTLY as runner._run_staged_one: restrict_python_files (outer)
    # then the consumer narrower (inner) — both for the same staged subset.
    from contextlib import ExitStack

    with ExitStack() as stack:
        stack.enter_context(restrict_python_files(tmp_path, ["kairix/a.py"]))
        stack.enter_context(narrower(tmp_path, ["kairix/a.py"]))
        # The check module's BY-VALUE binding must walk ONLY the staged file.
        narrowed = {p.name for p in mod.python_files("kairix", repo_root=tmp_path)}
    assert narrowed == {"a.py"}, (
        "check module by-value python_files binding was NOT narrowed under the "
        "runner's restrict+narrower composition (DEFECT-2: stale real_python_files)"
    )
    # Restored exactly after both contexts exit.
    assert {p.name for p in mod.python_files("kairix", repo_root=tmp_path)} == {"a.py", "b.py"}


def test_binding_narrower_full_staged_run_narrows_real_check_module(tmp_path: Path) -> None:
    # DEFECT-2 end-to-end through run(mode="staged"): a check module enumerates
    # via its by-value python_files binding and records how many files it saw.
    # With two kairix files on disk but only ONE staged, the narrowed run must
    # see exactly one file — proving the staged-mode optimisation actually fires
    # through the real runner composition (and the PASS/FAIL verdict is unchanged:
    # the check passes either way, so the optimisation is verdict-safe).
    checks_dir = tmp_path / "scripts" / "checks"
    checks_dir.mkdir(parents=True)
    (tmp_path / "kairix").mkdir()
    (tmp_path / "kairix" / "touched.py").write_text("")
    (tmp_path / "kairix" / "untouched.py").write_text("")
    seen_file = tmp_path / "seen_count.txt"
    (checks_dir / "check_counter.py").write_text(
        "from pathlib import Path\n"
        "from tc_fitness import python_files\n"
        "def main():\n"
        f"    walked = python_files('kairix', repo_root=Path({str(tmp_path)!r}))\n"
        f"    Path({str(seen_file)!r}).write_text(str(len(walked)))\n"
        "    return 0\n"
    )
    # Pre-import the check module BEFORE the staged run so its `from tc_fitness
    # import python_files` binds the ORIGINAL by value — exactly the state the
    # ~16 already-imported kairix check modules are in when staged mode starts.
    # (Importing it lazily inside the run would bind the already-scoped function
    # by import-timing luck and would NOT exercise the binding-narrower defect.)
    import importlib
    import sys

    sys.path.insert(0, str(checks_dir))
    try:
        importlib.import_module("check_counter")
        rules = (
            RuleEntry(
                id="CNT", gate="cnt", check="counter", summary="counter rule",
                staged_class="file-local", staged_scope=("kairix",),
            ),
        )
        verdict = run(
            rules,
            mode="staged",
            staged_files=["kairix/touched.py"],
            repo_root=tmp_path,
            checks_dir=checks_dir,
            enumeration_narrower=make_binding_narrower(),
        )
    finally:
        sys.modules.pop("check_counter", None)
        if str(checks_dir) in sys.path:
            sys.path.remove(str(checks_dir))
    assert verdict.ok  # verdict-safe: the check passes regardless of narrowing
    assert verdict.ran == 1
    # The narrowed run walked ONLY the one staged file, not both on disk.
    assert seen_file.read_text() == "1", (
        "the staged-mode binding-narrowing optimisation did not fire through the "
        "real runner — the check walked both files instead of just the staged one"
    )


# --------------------------------------------------------------------------- #
# end-to-end staged dispatch through the runner — the transparent ledger
# --------------------------------------------------------------------------- #


def _write_py_check(checks_dir: Path, name: str, body: str) -> None:
    (checks_dir / f"check_{name}.py").write_text(
        "def main():\n" + "\n".join(f"    {line}" for line in body.splitlines()) + "\n"
    )


def test_staged_dispatch_skips_out_of_scope_transparently(tmp_path: Path) -> None:
    checks_dir = tmp_path / "scripts" / "checks"
    checks_dir.mkdir(parents=True)
    _write_py_check(checks_dir, "kairix_rule", "return 0")
    _write_py_check(checks_dir, "tests_rule", "return 1")  # would FAIL if dispatched

    rules = (
        RuleEntry(
            id="K", gate="k", check="kairix_rule", summary="kairix rule",
            staged_class="file-local", staged_scope=("kairix",),
        ),
        RuleEntry(
            id="T", gate="t", check="tests_rule", summary="tests rule",
            staged_class="file-local", staged_scope=("tests",),
        ),
    )

    # Only a kairix file is staged → the tests rule must be skipped (so its FAIL
    # never registers), the kairix rule runs.
    import io
    import re
    from contextlib import redirect_stdout

    buf = io.StringIO()
    with redirect_stdout(buf):
        verdict = run(
            rules,
            mode="staged",
            staged_files=["kairix/a.py"],
            repo_root=tmp_path,
            checks_dir=checks_dir,
        )
    out = re.sub(r"\x1b\[[0-9;]*m", "", buf.getvalue())

    assert verdict.ok  # tests_rule (which would fail) was correctly skipped
    assert verdict.ran == 1
    assert verdict.skipped == 1
    assert "run [K]" in out
    assert "skip [T]" in out
    assert "no staged file in scope" in out
    assert "staged selection: 1 ran, 1 skipped" in out


def test_staged_dispatch_no_false_negative(tmp_path: Path) -> None:
    # SOUNDNESS end-to-end: a staged file IN a failing rule's scope MUST run the
    # rule and surface the failure (the property that makes --staged trustworthy).
    checks_dir = tmp_path / "scripts" / "checks"
    checks_dir.mkdir(parents=True)
    _write_py_check(checks_dir, "guard", "return 1")  # always fails when run

    rules = (
        RuleEntry(
            id="GUARD", gate="guard", check="guard", summary="guard rule",
            staged_class="file-local", staged_scope=("kairix",),
        ),
    )
    verdict = run(
        rules,
        mode="staged",
        staged_files=["kairix/touched.py"],
        repo_root=tmp_path,
        checks_dir=checks_dir,
    )
    assert verdict.failures == ["GUARD"]  # the staged change tripped the rule


def test_staged_empty_runs_everything_through_runner(tmp_path: Path) -> None:
    checks_dir = tmp_path / "scripts" / "checks"
    checks_dir.mkdir(parents=True)
    _write_py_check(checks_dir, "any", "return 1")
    rules = (
        RuleEntry(
            id="ANY", gate="any", check="any", summary="any",
            staged_class="file-local", staged_scope=("nowhere",),
        ),
    )
    # No staged files at all → fail-safe: the rule runs even though its scope
    # doesn't match (the pre-commit --all-files quirk).
    verdict = run(
        rules, mode="staged", staged_files=[], repo_root=tmp_path, checks_dir=checks_dir
    )
    assert verdict.failures == ["ANY"]
