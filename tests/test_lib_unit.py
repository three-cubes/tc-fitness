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

import io

import pytest

from tc_fitness.lib import (
    actionable,
    emit_failures,
    emit_pass,
    missing_keys,
    remediation,
)

pytestmark = pytest.mark.unit

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


def test_actionable_shape() -> None:
    assert actionable("X broke", "do Y", "rerun Z") == "X broke; fix: do Y; next: rerun Z"


def test_actionable_v01_default_is_byte_identical_two_marker() -> None:
    # v0.1.0 contract: with run omitted the output is EXACTLY the 2-marker form.
    # Proves the new optional param did not perturb existing call sites.
    assert actionable("kairix/x.py leaks", "redact it", "re-run check") == (
        "kairix/x.py leaks; fix: redact it; next: re-run check"
    )
    # The positional call shape kairix uses everywhere still emits no run: marker.
    assert "; run:" not in actionable("a", "b", "c")


def test_actionable_run_appends_third_marker() -> None:
    # taz's 59 fix/next/run checks: the third marker is appended verbatim.
    assert actionable("X broke", "do Y", "rerun Z", "python check.py") == (
        "X broke; fix: do Y; next: rerun Z; run: python check.py"
    )


def test_actionable_run_can_be_keyword() -> None:
    assert actionable("X", "Y", "Z", run="cmd") == "X; fix: Y; next: Z; run: cmd"


def test_actionable_run_explicit_none_matches_default() -> None:
    assert actionable("X", "Y", "Z", run=None) == actionable("X", "Y", "Z")


# --------------------------------------------------------------------------- #
# remediation() — taz multiline fix:/next:/run: (+ Pass/Forbidden) block
# --------------------------------------------------------------------------- #


def test_remediation_three_markers_on_own_lines() -> None:
    block = remediation("redact it", "re-run check", "python check.py")
    assert block == "fix: redact it\nnext: re-run check\nrun: python check.py"


def test_remediation_with_pass_and_forbidden_examples() -> None:
    block = remediation(
        "redact the secret",
        "re-run the check",
        "python scripts/checks/check_f15.py",
        passing='logger.info("token redacted")',
        forbidden='logger.info(f"token={token}")',
    )
    assert block == (
        "fix: redact the secret\n"
        "next: re-run the check\n"
        "run: python scripts/checks/check_f15.py\n"
        'Pass: logger.info("token redacted")\n'
        'Forbidden: logger.info(f"token={token}")'
    )


def test_remediation_pass_only_omits_forbidden() -> None:
    block = remediation("a", "b", "c", passing="good")
    assert block == "fix: a\nnext: b\nrun: c\nPass: good"
    assert "Forbidden:" not in block


def test_remediation_forbidden_only_omits_pass() -> None:
    block = remediation("a", "b", "c", forbidden="bad")
    assert block == "fix: a\nnext: b\nrun: c\nForbidden: bad"
    assert "Pass:" not in block


# --------------------------------------------------------------------------- #
# gate_keys() — taz string-keyed baseline ratchet (-ids.txt / -paths.txt)
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
# emit_failures() / emit_pass() — tc-agent-zone banners
# --------------------------------------------------------------------------- #


def test_emit_failures_banner_and_bullets() -> None:
    buf = io.StringIO()
    emit_failures("my_check", ["first fail", "second fail"], stream=buf)
    text = buf.getvalue()
    assert "FAIL my_check (2 violations)" in text
    assert "  - first fail" in text
    assert "  - second fail" in text


def test_emit_pass_writes_message() -> None:
    buf = io.StringIO()
    emit_pass("PASS my_check", stream=buf)
    assert buf.getvalue().strip() == "PASS my_check"


# --------------------------------------------------------------------------- #
# load_yaml() — tc-agent-zone (data, error) contract
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
# missing_keys() — tc-agent-zone required-key contract
# --------------------------------------------------------------------------- #


def test_missing_keys_reports_absent() -> None:
    assert missing_keys({"a": 1}, ("a", "b", "c")) == ["b", "c"]


def test_missing_keys_empty_when_all_present() -> None:
    assert missing_keys({"a": 1, "b": 2}, ("a", "b")) == []


def test_missing_keys_preserves_required_order() -> None:
    assert missing_keys({}, ("z", "a", "m")) == ["z", "a", "m"]
