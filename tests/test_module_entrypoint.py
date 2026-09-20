"""Tests for `python -m tc_fitness` and the candidate binding it exists to serve.

The module entry point is not a convenience alias for the console script. The
script is resolved from the environment's bin directory and runs whatever is
*installed*; the module resolves through the caller's import path and therefore
runs the candidate the caller is testing. Contract evidence is bound to the
candidate's source digest, so which of the two executes decides whether the
evidence describes the thing under test.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

from tc_fitness import runner

pytestmark = pytest.mark.unit

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_module_entrypoint_exposes_the_same_cli_as_the_console_script() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "tc_fitness", "--help"],
        capture_output=True,
        text=True,
        check=False,
        cwd=REPO_ROOT,
    )
    assert result.returncode == 0, result.stderr
    assert "tc-fitness" in result.stdout


def test_module_entrypoint_resolves_through_the_callers_import_path(tmp_path: Path) -> None:
    """A PYTHONPATH entry wins, which is what carries a relocated candidate.

    This is the property `run_contract_case` depends on: a mutation run executes
    from a copied tree, and the child must import that tree rather than the
    installed copy, or the ledger it writes describes a candidate nobody is
    testing.
    """
    shadow = tmp_path / "shadow"
    (shadow / "tc_fitness").mkdir(parents=True)
    (shadow / "tc_fitness" / "__init__.py").write_text("", encoding="utf-8")
    (shadow / "tc_fitness" / "__main__.py").write_text("print('shadow candidate')\n", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "tc_fitness"],
        capture_output=True,
        text=True,
        check=False,
        cwd=tmp_path,
        env={**os.environ, "PYTHONPATH": str(shadow)},
    )
    assert "shadow candidate" in result.stdout, result.stderr


def test_contract_case_hands_the_callers_search_path_to_the_child(monkeypatch) -> None:
    """Runtime sys.path additions are not inherited, so PYTHONPATH carries them."""
    captured: dict[str, object] = {}

    class _Completed:
        returncode = 0

    def _fake_run(argv, **kwargs):
        captured["argv"] = argv
        captured["env"] = kwargs.get("env")
        return _Completed()

    monkeypatch.setattr(runner.subprocess, "run", _fake_run)
    monkeypatch.setattr(
        "tc_fitness.check_contract_execution.validate_contract_ledger",
        lambda *a, **k: {"ok": True},
    )
    monkeypatch.syspath_prepend("/tmp/candidate-under-test")

    runner.run_contract_case(Path("manifest.yaml"), "case-1", Path("ledger.json"))

    argv = captured["argv"]
    assert argv[:3] == [sys.executable, "-m", "tc_fitness"], argv
    search_path = (captured["env"] or {})["PYTHONPATH"].split(os.pathsep)
    assert "/tmp/candidate-under-test" in search_path


def test_contract_case_preserves_an_inherited_pythonpath(monkeypatch) -> None:
    """An operator's PYTHONPATH must survive, after the caller's own entries."""
    captured: dict[str, object] = {}

    class _Completed:
        returncode = 0

    monkeypatch.setattr(
        runner.subprocess,
        "run",
        lambda argv, **kwargs: (captured.update(env=kwargs.get("env")), _Completed())[1],
    )
    monkeypatch.setattr(
        "tc_fitness.check_contract_execution.validate_contract_ledger",
        lambda *a, **k: {"ok": True},
    )
    monkeypatch.setenv("PYTHONPATH", "/operator/entry")

    runner.run_contract_case(Path("manifest.yaml"), "case-1", Path("ledger.json"))

    search_path = (captured["env"] or {})["PYTHONPATH"].split(os.pathsep)
    assert "/operator/entry" in search_path
    assert search_path.index("/operator/entry") == len(search_path) - 1
