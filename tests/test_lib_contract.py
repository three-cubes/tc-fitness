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

import pytest

from tc_fitness.lib import (
    emit_failures,
    emit_pass,
)

pytestmark = pytest.mark.contract

# --------------------------------------------------------------------------- #
# gate() — kairix baseline-gating contract
# --------------------------------------------------------------------------- #


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


# --------------------------------------------------------------------------- #
# actionable() — tc-agent-zone canonical FAIL shape
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
# remediation() — taz multiline fix:/next:/run: (+ Pass/Forbidden) block
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
# gate_keys() — taz string-keyed baseline ratchet (-ids.txt / -paths.txt)
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
# emit_failures() / emit_pass() — tc-agent-zone banners
# --------------------------------------------------------------------------- #


def test_emit_failures_defaults_to_stderr(capsys: pytest.CaptureFixture[str]) -> None:
    emit_failures("my_check", ["boom"])
    captured = capsys.readouterr()
    assert "FAIL my_check (1 violations)" in captured.err
    assert captured.out == ""


def test_emit_pass_defaults_to_stdout(capsys: pytest.CaptureFixture[str]) -> None:
    emit_pass("PASS my_check")
    captured = capsys.readouterr()
    assert "PASS my_check" in captured.out
    assert captured.err == ""


# --------------------------------------------------------------------------- #
# load_yaml() — tc-agent-zone (data, error) contract
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
# missing_keys() — tc-agent-zone required-key contract
# --------------------------------------------------------------------------- #
