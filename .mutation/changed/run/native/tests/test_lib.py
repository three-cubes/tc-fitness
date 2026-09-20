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


def test_gate_keys_does_not_relativise_keys(tmp_path: Path) -> None:
    # A key that looks like an absolute path must be treated as an OPAQUE string,
    # NOT relativised the way gate() relativises real Paths.
    abs_like = "/abs/looking/key"
    rc = gate_keys("rule", {abs_like}, "fix it", repo_root=tmp_path)
    assert rc == 1


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
