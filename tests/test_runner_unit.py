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

import re
import sys
from pathlib import Path

import pytest

from tc_fitness.catalogue import RuleEntry
from tc_fitness.runner import (
    Colours,
    Verdicts,
    print_aggregate,
    resolve_script,
    select_all,
    select_gate,
)

pytestmark = pytest.mark.unit

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


# --------------------------------------------------------------------------- #
# subprocess dispatch (sequential + parallel) for shell detectors
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
# mixed python + shell catalogue through the programmatic API
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
# run_all gating + --gate selection + dedup
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
# proposed entries are skipped
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
# conditional (runtime-arg) subprocess check — coverage-style
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
# main_cli thin-consumer surface
# --------------------------------------------------------------------------- #


def test_resolve_script_default_and_override() -> None:
    assert resolve_script(RuleEntry(id="X", gate="x", check="foo_bar")) == "check_foo_bar.py"
    assert resolve_script(RuleEntry(id="X", gate="x", check="foo", script="check-foo.sh")) == "check-foo.sh"


def test_verdicts_properties() -> None:
    assert Verdicts(ran=3, failures=[]).ok is True
    assert Verdicts(ran=3, failures=["A"]).ok is False
    assert Verdicts(ran=3, failures=[]).exit_code == 0
    assert Verdicts(ran=3, failures=["A"]).exit_code == 1


# --------------------------------------------------------------------------- #
# make_env_path_conditional_check — declarative ConditionalCheck factory (1.4)
#
# Generalises kairix's _make_conditional_check + _coverage_xml_path: resolve a
# runtime-arg path from an env var (else a repo-relative default), run with it
# appended when present, or skip with the consumer's EXACT skip lines when forced
# (--skip-coverage-style) or absent. The env-var name, default, force predicate,
# and both skip-line sets are all CONFIG.
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
# main_cli extra_flags + post_parse — consumer-specific flags (Task 1.4)
#
# Retires kairix's forked main()/--skip-coverage: a consumer declares its flag
# via extra_flags and maps the parsed Namespace to extra run() kwargs (e.g. a
# conditional_check built from the flag) via post_parse.
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
# RuleEntry argv-exception fields (Task 1.5)
#
# Generalises taz's _SCRIPT_PATH_OVERRIDES (hermetic smoke), _STATIC_EXTRA_ARGS
# (mutation ratchet --allow-missing-current), _orphan_files_extra
# (ORPHAN_FILES_STRICT → --strict). All declarative on the RuleEntry now.
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
# public subprocess-dispatch mode + promoted ledger primitives (Task 1.6)
#
# So taz drops its 7 private-symbol imports and reimplemented dispatch.
# --------------------------------------------------------------------------- #


# promoted ledger primitives -------------------------------------------------- #


def test_select_all_is_public_and_filters_run_all_and_proposed() -> None:
    rules = (
        RuleEntry(id="A", gate="a", check="a"),
        RuleEntry(id="B", gate="b", check="b", run_all=False),
        RuleEntry(id="C", gate="c", check="(proposed)", status="proposed"),
    )
    assert [e.id for e in select_all(rules)] == ["A"]


def test_select_gate_is_public_and_case_insensitive() -> None:
    rules = (RuleEntry(id="F26", gate="f26", check="x"),)
    assert [e.id for e in select_gate(rules, "f26")] == ["F26"]
    assert select_gate(rules, "nope") == []


def test_print_aggregate_is_public(capsys: pytest.CaptureFixture[str]) -> None:
    print_aggregate(Verdicts(ran=2, failures=[]))
    assert "All 2 architecture fitness functions passed" in _plain(capsys.readouterr().out)
    print_aggregate(Verdicts(ran=2, failures=["X"]))
    assert "1/2 rule(s) failed: X" in _plain(capsys.readouterr().out)


def test_colours_namespace_is_public() -> None:
    # The colours taz imports as private _GREEN/_RED/_RESET/_YELLOW are exposed
    # as a public namespace.
    assert Colours.GREEN == "\033[0;32m"
    assert Colours.RED == "\033[0;31m"
    assert Colours.YELLOW == "\033[0;33m"
    assert Colours.RESET == "\033[0m"


def test_underscore_aliases_still_re_exported() -> None:
    # Back-compat: taz's private imports keep resolving until it migrates.
    from tc_fitness.runner import (
        _GREEN,
        _RED,
        _RESET,
        _YELLOW,
        _print_aggregate,
        _select_all,
        _select_gate,
    )

    assert _print_aggregate is print_aggregate
    assert _select_all is select_all
    assert _select_gate is select_gate
    assert (_GREEN, _RED, _YELLOW, _RESET) == (
        Colours.GREEN,
        Colours.RED,
        Colours.YELLOW,
        Colours.RESET,
    )


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
