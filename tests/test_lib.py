"""Behavioural tests for the merged lib surface.

Each test pins a behaviour a real call site in kairix or tc-agent-zone depends on,
so the merge is provably behaviour-preserving. Call patterns mirrored:

- kairix: ``gate(name, set, remediation)``, ``main_entry(fn, name, rem, *roots)``,
  ``python_files(*roots)``, ``repo_relative(path)``.
- tc-agent-zone: ``actionable(what, fix, nxt)``, ``emit_failures(name, fails)``,
  ``emit_pass(message)``, ``load_yaml(path) -> (data, err)``,
  ``missing_keys(parsed, required) -> list``.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tc_fitness import lib
from tc_fitness.lib import (
    gate,
    gate_keys,
    load_yaml,
    main_entry,
    python_files,
    repo_relative,
)

pytestmark = pytest.mark.integration

# --------------------------------------------------------------------------- #
# gate() — kairix baseline-gating contract
# --------------------------------------------------------------------------- #


def test_gate_clean_when_no_violations(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    rc = gate("rule-x", set(), "fix it", repo_root=tmp_path)
    assert rc == 0
    assert "clean" in capsys.readouterr().out


def test_gate_fails_on_net_new_violation(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    rc = gate("rule-x", {Path("kairix/bad.py")}, "REMEDIATION-TEXT", repo_root=tmp_path)
    out = capsys.readouterr().out
    assert rc == 1
    assert "kairix/bad.py" in out
    assert "REMEDIATION-TEXT" in out


def test_gate_grandfathers_baseline_files(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    baseline_dir = tmp_path / ".architecture" / "baseline"
    baseline_dir.mkdir(parents=True)
    (baseline_dir / "rule-x-files.txt").write_text("kairix/legacy.py\n")
    # The same file already in the baseline must NOT trip the gate.
    rc = gate("rule-x", {Path("kairix/legacy.py")}, "fix it", repo_root=tmp_path)
    out = capsys.readouterr().out
    assert rc == 0
    assert "grandfathered" in out
    assert "1 grandfathered" in out


def test_gate_new_violation_alongside_baseline(tmp_path: Path) -> None:
    baseline_dir = tmp_path / ".architecture" / "baseline"
    baseline_dir.mkdir(parents=True)
    (baseline_dir / "rule-x-files.txt").write_text("kairix/legacy.py\n")
    rc = gate("rule-x", {Path("kairix/legacy.py"), Path("kairix/new.py")}, "fix it", repo_root=tmp_path)
    assert rc == 1  # legacy grandfathered, new.py is net-new


def test_gate_baseline_skips_comment_lines(tmp_path: Path) -> None:
    baseline_dir = tmp_path / ".architecture" / "baseline"
    baseline_dir.mkdir(parents=True)
    (baseline_dir / "rule-x-files.txt").write_text("# a comment\nkairix/legacy.py\n")
    rc = gate("rule-x", {Path("kairix/legacy.py")}, "fix it", repo_root=tmp_path)
    assert rc == 0


def test_gate_relativises_absolute_paths(tmp_path: Path) -> None:
    abs_violation = tmp_path / "kairix" / "bad.py"
    abs_violation.parent.mkdir(parents=True)
    abs_violation.write_text("x = 1\n")
    rc = gate("rule-x", {abs_violation}, "fix it", repo_root=tmp_path)
    # Absolute path under repo_root is relativised; with no baseline it's net-new.
    assert rc == 1


# --------------------------------------------------------------------------- #
# gate(fail_on_stale=True) + counts banner — Task 1.7
#
# Generalises taz's per-check stale-baseline behaviour: a baseline entry no
# longer present in the current scan is STALE and FAILs (consumer supplies the
# remediation); on pass the banner reports new-vs-grandfathered counts. The
# default (fail_on_stale=False) preserves the v0.1.0 exit-code contract.
# --------------------------------------------------------------------------- #


def test_gate_fail_on_stale_fails_when_baseline_entry_no_longer_violates(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    baseline_dir = tmp_path / ".architecture" / "baseline"
    baseline_dir.mkdir(parents=True)
    (baseline_dir / "rule-x-files.txt").write_text("kairix/resolved.py\nkairix/still.py\n")
    # Only kairix/still.py still violates → kairix/resolved.py is STALE.
    rc = gate(
        "rule-x",
        {Path("kairix/still.py")},
        "fix it",
        repo_root=tmp_path,
        fail_on_stale=True,
        stale_remediation="REMOVE-STALE-LINE",
    )
    out = capsys.readouterr().out
    assert rc == 1
    assert "kairix/resolved.py" in out
    assert "REMOVE-STALE-LINE" in out
    assert "STALE" in out or "stale" in out


def test_gate_fail_on_stale_passes_and_prints_counts_when_no_stale(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    baseline_dir = tmp_path / ".architecture" / "baseline"
    baseline_dir.mkdir(parents=True)
    (baseline_dir / "rule-x-files.txt").write_text("kairix/a.py\nkairix/b.py\n")
    rc = gate(
        "rule-x",
        {Path("kairix/a.py"), Path("kairix/b.py")},
        "fix it",
        repo_root=tmp_path,
        fail_on_stale=True,
    )
    out = capsys.readouterr().out
    assert rc == 0
    # The counts banner reports new (0) vs grandfathered (2).
    assert "0" in out and "2" in out
    assert "grandfathered" in out


def test_gate_fail_on_stale_default_false_is_unchanged(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    # With the default (fail_on_stale=False), a baseline entry that no longer
    # violates is SILENTLY tolerated (the v0.1.0 shrinks-are-clean contract).
    baseline_dir = tmp_path / ".architecture" / "baseline"
    baseline_dir.mkdir(parents=True)
    (baseline_dir / "rule-x-files.txt").write_text("kairix/resolved.py\nkairix/still.py\n")
    rc = gate("rule-x", {Path("kairix/still.py")}, "fix it", repo_root=tmp_path)
    out = capsys.readouterr().out
    assert rc == 0  # stale entry tolerated, no FAIL
    assert "STALE" not in out


def test_gate_net_new_still_fails_under_fail_on_stale(tmp_path: Path) -> None:
    # A net-new violation FAILs regardless of fail_on_stale.
    baseline_dir = tmp_path / ".architecture" / "baseline"
    baseline_dir.mkdir(parents=True)
    (baseline_dir / "rule-x-files.txt").write_text("kairix/legacy.py\n")
    rc = gate(
        "rule-x",
        {Path("kairix/legacy.py"), Path("kairix/new.py")},
        "fix it",
        repo_root=tmp_path,
        fail_on_stale=True,
        stale_remediation="rem",
    )
    assert rc == 1


def test_gate_keys_fail_on_stale(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    baseline_dir = tmp_path / ".architecture" / "baseline"
    baseline_dir.mkdir(parents=True)
    (baseline_dir / "f30-ids.txt").write_text("F30:resolved\nF30:still\n")
    rc = gate_keys(
        "f30",
        {"F30:still"},
        "fix it",
        repo_root=tmp_path,
        fail_on_stale=True,
        stale_remediation="REMOVE-STALE-ID",
    )
    out = capsys.readouterr().out
    assert rc == 1
    assert "F30:resolved" in out
    assert "REMOVE-STALE-ID" in out


def test_gate_keys_fail_on_stale_default_false_unchanged(tmp_path: Path) -> None:
    baseline_dir = tmp_path / ".architecture" / "baseline"
    baseline_dir.mkdir(parents=True)
    (baseline_dir / "f30-ids.txt").write_text("F30:resolved\nF30:still\n")
    rc = gate_keys("f30", {"F30:still"}, "fix it", repo_root=tmp_path)
    assert rc == 0  # shrinks-are-clean by default


# --------------------------------------------------------------------------- #
# python_files() / repo_relative() / main_entry() — kairix enumeration
# --------------------------------------------------------------------------- #


def test_python_files_finds_py_skips_pycache(tmp_path: Path) -> None:
    (tmp_path / "kairix").mkdir()
    (tmp_path / "kairix" / "a.py").write_text("")
    (tmp_path / "kairix" / "nested").mkdir()
    (tmp_path / "kairix" / "nested" / "b.py").write_text("")
    (tmp_path / "kairix" / "__pycache__").mkdir()
    (tmp_path / "kairix" / "__pycache__" / "c.py").write_text("")
    (tmp_path / "kairix" / "notpy.txt").write_text("")

    found = {p.name for p in python_files("kairix", repo_root=tmp_path)}
    assert found == {"a.py", "b.py"}


def test_python_files_skips_missing_root(tmp_path: Path) -> None:
    assert python_files("does-not-exist", repo_root=tmp_path) == []


def test_repo_relative_strips_root(tmp_path: Path) -> None:
    target = tmp_path / "kairix" / "x.py"
    target.parent.mkdir(parents=True)
    target.write_text("")
    assert repo_relative(target, repo_root=tmp_path) == Path("kairix/x.py")


def test_main_entry_gates_on_check_fn(tmp_path: Path) -> None:
    (tmp_path / "kairix").mkdir()
    good = tmp_path / "kairix" / "good.py"
    bad = tmp_path / "kairix" / "bad.py"
    good.write_text("clean\n")
    bad.write_text("VIOLATION\n")

    def check_fn(path: Path) -> bool:
        return "VIOLATION" in path.read_text()

    rc = main_entry(check_fn, "rule-y", "fix it", "kairix", repo_root=tmp_path)
    assert rc == 1  # bad.py flagged, net-new


def test_main_entry_clean_when_check_fn_never_fires(tmp_path: Path) -> None:
    (tmp_path / "kairix").mkdir()
    (tmp_path / "kairix" / "good.py").write_text("clean\n")
    rc = main_entry(lambda p: False, "rule-y", "fix it", "kairix", repo_root=tmp_path)
    assert rc == 0


# --------------------------------------------------------------------------- #
# actionable() — tc-agent-zone canonical FAIL shape
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
# remediation() — taz multiline fix:/next:/run: (+ Pass/Forbidden) block
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
# gate_keys() — taz string-keyed baseline ratchet (-ids.txt / -paths.txt)
# --------------------------------------------------------------------------- #


def test_gate_keys_clean_when_no_violations(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    rc = gate_keys("rule-id", set(), "fix it", repo_root=tmp_path)
    assert rc == 0
    assert "clean" in capsys.readouterr().out


def test_gate_keys_fails_on_net_new_logical_id(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    rc = gate_keys("f30", {"F30:my_new_tool"}, "REMEDIATION-TEXT", repo_root=tmp_path)
    out = capsys.readouterr().out
    assert rc == 1
    assert "F30:my_new_tool" in out
    assert "REMEDIATION-TEXT" in out


def test_gate_keys_grandfathers_baseline_ids(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    baseline_dir = tmp_path / ".architecture" / "baseline"
    baseline_dir.mkdir(parents=True)
    (baseline_dir / "f30-ids.txt").write_text("F30:legacy_tool\n")
    rc = gate_keys("f30", {"F30:legacy_tool"}, "fix it", repo_root=tmp_path)
    out = capsys.readouterr().out
    assert rc == 0
    assert "1 grandfathered" in out


def test_gate_keys_new_id_alongside_baseline(tmp_path: Path) -> None:
    baseline_dir = tmp_path / ".architecture" / "baseline"
    baseline_dir.mkdir(parents=True)
    (baseline_dir / "f30-ids.txt").write_text("F30:legacy_tool\n")
    rc = gate_keys("f30", {"F30:legacy_tool", "F30:new_tool"}, "fix it", repo_root=tmp_path)
    assert rc == 1  # legacy grandfathered, new_tool is net-new


def test_gate_keys_baseline_skips_comment_lines(tmp_path: Path) -> None:
    baseline_dir = tmp_path / ".architecture" / "baseline"
    baseline_dir.mkdir(parents=True)
    (baseline_dir / "f30-ids.txt").write_text("# a comment\nF30:legacy_tool\n")
    rc = gate_keys("f30", {"F30:legacy_tool"}, "fix it", repo_root=tmp_path)
    assert rc == 0


def test_gate_keys_shrinks_only_is_clean(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    # Baseline has two ids; current has one (a resolved id). No net-new ⇒ clean pass.
    baseline_dir = tmp_path / ".architecture" / "baseline"
    baseline_dir.mkdir(parents=True)
    (baseline_dir / "f30-ids.txt").write_text("F30:a\nF30:b\n")
    rc = gate_keys("f30", {"F30:a"}, "fix it", repo_root=tmp_path)
    assert rc == 0
    assert "grandfathered" in capsys.readouterr().out


def test_gate_keys_paths_suffix_selects_paths_baseline(tmp_path: Path) -> None:
    # A path-glob key set ratchets against -paths.txt when the suffix is overridden.
    baseline_dir = tmp_path / ".architecture" / "baseline"
    baseline_dir.mkdir(parents=True)
    (baseline_dir / "f89-paths.txt").write_text("kairix/**/web/static/*\n")
    rc = gate_keys(
        "f89",
        {"kairix/**/web/static/*"},
        "fix it",
        repo_root=tmp_path,
        baseline_suffix="-paths.txt",
    )
    assert rc == 0


def test_gate_keys_does_not_relativise_keys(tmp_path: Path) -> None:
    # A key that looks like an absolute path must be treated as an OPAQUE string,
    # NOT relativised the way gate() relativises real Paths. Same string in the
    # baseline ⇒ grandfathered (proves no Path coercion happens).
    baseline_dir = tmp_path / ".architecture" / "baseline"
    baseline_dir.mkdir(parents=True)
    abs_like = "/abs/looking/key"
    (baseline_dir / "rule-ids.txt").write_text(f"{abs_like}\n")
    rc = gate_keys("rule", {abs_like}, "fix it", repo_root=tmp_path)
    assert rc == 0


# --------------------------------------------------------------------------- #
# emit_failures() / emit_pass() — tc-agent-zone banners
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
# load_yaml() — tc-agent-zone (data, error) contract
# --------------------------------------------------------------------------- #


def test_load_yaml_success(tmp_path: Path) -> None:
    pytest.importorskip("yaml")
    f = tmp_path / "ok.yaml"
    f.write_text("a: 1\nb: two\n")
    data, err = load_yaml(f)
    assert err is None
    assert data == {"a": 1, "b": "two"}


def test_load_yaml_empty_returns_empty_dict(tmp_path: Path) -> None:
    pytest.importorskip("yaml")
    f = tmp_path / "empty.yaml"
    f.write_text("")
    data, err = load_yaml(f)
    assert err is None
    assert data == {}


def test_load_yaml_malformed_returns_error(tmp_path: Path) -> None:
    pytest.importorskip("yaml")
    f = tmp_path / "bad.yaml"
    f.write_text("a: [unterminated\n")
    data, err = load_yaml(f)
    assert data is None
    assert err is not None
    assert "invalid YAML" in err


# --------------------------------------------------------------------------- #
# missing_keys() — tc-agent-zone required-key contract
# --------------------------------------------------------------------------- #


# -- pinned_version: the sanctioned alternative to restating a pin -----------


def test_pinned_version_returns_the_declared_exact_pin(monkeypatch) -> None:
    monkeypatch.setattr(lib, "metadata_requires", lambda _d: ["mutmut==3.6.0", "ruff>=0.15,<0.16"])
    assert lib.pinned_version("demo", "mutmut") == "3.6.0"


def test_pinned_version_normalises_the_package_name(monkeypatch) -> None:
    """PyPI treats `_` and `-` alike, so a caller spelling either must resolve."""
    monkeypatch.setattr(lib, "metadata_requires", lambda _d: ["My_Pkg==1.2.3"])
    assert lib.pinned_version("demo", "my-pkg") == "1.2.3"


def test_pinned_version_ignores_a_requirement_for_another_package(monkeypatch) -> None:
    monkeypatch.setattr(lib, "metadata_requires", lambda _d: ["other==9.9.9", "mutmut==3.6.0"])
    assert lib.pinned_version("demo", "mutmut") == "3.6.0"


def test_pinned_version_reads_an_extra_scoped_requirement(monkeypatch) -> None:
    """A dev-extra pin is still the manifest's declaration."""
    monkeypatch.setattr(lib, "metadata_requires", lambda _d: ['mutmut==3.6.0; extra == "dev"'])
    assert lib.pinned_version("demo", "mutmut") == "3.6.0"


def test_pinned_version_rejects_a_range_and_says_which_repair(monkeypatch) -> None:
    monkeypatch.setattr(lib, "metadata_requires", lambda _d: ["mutmut>=3.6"])
    with pytest.raises(lib.PinnedVersionError) as excinfo:
        lib.pinned_version("demo", "mutmut")
    message = str(excinfo.value)
    assert "not at an exact version" in message
    assert "fix:" in message and "next:" in message and "run:" in message


def test_pinned_version_rejects_an_undeclared_package_and_says_which_repair(monkeypatch) -> None:
    monkeypatch.setattr(lib, "metadata_requires", lambda _d: ["other==1.2.3"])
    with pytest.raises(lib.PinnedVersionError) as excinfo:
        lib.pinned_version("demo", "mutmut")
    message = str(excinfo.value)
    assert "does not require" in message
    assert "fix:" in message and "next:" in message and "run:" in message


def test_pinned_version_rejects_an_uninstalled_distribution_and_says_which_repair(monkeypatch) -> None:
    def _absent(_d: str) -> list[str]:
        raise lib.PackageNotFoundError("demo")

    monkeypatch.setattr(lib, "metadata_requires", _absent)
    with pytest.raises(lib.PinnedVersionError) as excinfo:
        lib.pinned_version("demo", "mutmut")
    message = str(excinfo.value)
    assert "is not installed" in message
    assert "fix:" in message and "next:" in message and "run:" in message


def test_a_wildcard_equality_is_not_an_exact_pin(monkeypatch: pytest.MonkeyPatch) -> None:
    """`foo==1.2.*` admits any 1.2 release, so it cannot be compared to an installed version."""
    monkeypatch.setattr(lib, "metadata_requires", lambda _d: ["foo==1.2.*"])

    with pytest.raises(lib.PinnedVersionError, match="not at an exact version"):
        lib.pinned_version("dist", "foo")


def test_package_names_compare_across_every_permitted_separator() -> None:
    """PEP 503 treats runs of -, _ and . as equivalent in a package name."""
    assert lib.canonical_package_name("zope.interface") == lib.canonical_package_name("zope-interface")
    assert lib.canonical_package_name("Zope_Interface") == "zope-interface"


def test_conflicting_conditional_pins_are_refused(monkeypatch: pytest.MonkeyPatch) -> None:
    """Choosing by metadata order would enforce the wrong version on some interpreters."""
    monkeypatch.setattr(
        lib,
        "metadata_requires",
        lambda _d: ['foo==1.2.3; python_version < "3.13"', 'foo==2.0.0; python_version >= "3.13"'],
    )

    with pytest.raises(lib.PinnedVersionError, match="more than one way"):
        lib.pinned_version("dist", "foo")


def test_a_mixed_exact_and_range_declaration_is_refused(monkeypatch: pytest.MonkeyPatch) -> None:
    """An exact pin beside a range means the version depends on who is asking."""
    monkeypatch.setattr(
        lib,
        "metadata_requires",
        lambda _d: ['foo==1.2.3; python_version < "3.12"', 'foo>=2; python_version >= "3.12"'],
    )

    with pytest.raises(lib.PinnedVersionError, match="more than one way"):
        lib.pinned_version("dist", "foo")


def test_a_parenthesised_pin_is_read_as_exact(monkeypatch: pytest.MonkeyPatch) -> None:
    """`foo (==1.2.3)` is valid PEP 508 and pins exactly as `foo==1.2.3` does."""
    monkeypatch.setattr(lib, "metadata_requires", lambda _d: ["foo (==1.2.3)"])

    assert lib.pinned_version("dist", "foo") == "1.2.3"


def test_a_direct_reference_url_is_not_mistaken_for_a_pin(monkeypatch: pytest.MonkeyPatch) -> None:
    """An `==` inside a URL query string is not an equality specifier."""
    monkeypatch.setattr(
        lib, "metadata_requires", lambda _d: ["foo @ https://example.invalid/foo.whl?build==1.2.3"]
    )

    with pytest.raises(lib.PinnedVersionError, match="not at an exact version"):
        lib.pinned_version("dist", "foo")
