"""Public runner and gate contracts exercised through real local collaborators."""

from __future__ import annotations

import importlib
import os
import shlex
import sys
import uuid
from pathlib import Path

import pytest

import tc_fitness
from tc_fitness.catalogue import RuleEntry
from tc_fitness.gate import run_gate
from tc_fitness.gate_config import load_config
from tc_fitness.runner import ConditionalResult, run
from tc_fitness.staged import make_binding_narrower

pytestmark = pytest.mark.contract


def test_runner_consumes_a_real_environment_selected_runtime_file(
    tmp_path: Path,
) -> None:
    checks_dir = tmp_path / "checks"
    checks_dir.mkdir()
    runtime_file = tmp_path / "coverage.xml"
    runtime_file.write_text("coverage evidence\n")
    consumed = tmp_path / "consumed.txt"
    script = checks_dir / "consume.sh"
    script.write_text(f'#!/usr/bin/env bash\ncat "$1" > {shlex.quote(str(consumed))}\n')
    script.chmod(0o755)
    env_var = f"TC_FITNESS_CONTRACT_INPUT_{uuid.uuid4().hex.upper()}"
    rule = RuleEntry(
        id="CONTRACT-INPUT",
        gate="contract-input",
        check="consume",
        script=script.name,
        subprocess_arg_env=env_var,
    )
    assert env_var not in os.environ
    os.environ[env_var] = str(runtime_file)
    try:
        verdict = run((rule,), repo_root=tmp_path, checks_dir=checks_dir)
    finally:
        del os.environ[env_var]

    assert verdict.ok
    assert consumed.read_text() == "coverage evidence\n"


def test_runner_delegates_to_a_real_default_runtime_file(
    tmp_path: Path,
) -> None:
    checks_dir = tmp_path / "checks"
    checks_dir.mkdir()
    runtime_file = tmp_path / "default-report.xml"
    runtime_file.write_text("default report consumed\n")
    consumed = tmp_path / "consumed-default.txt"
    script = checks_dir / "consume.sh"
    script.write_text(f'#!/usr/bin/env bash\ncat "$1" > {shlex.quote(str(consumed))}\n')
    script.chmod(0o755)
    env_var = f"TC_FITNESS_CONTRACT_DEFAULT_{uuid.uuid4().hex.upper()}"
    rule = RuleEntry(
        id="CONTRACT-DEFAULT",
        gate="contract-default",
        check="consume",
        script=script.name,
        subprocess_arg_env=env_var,
        subprocess_arg_default=runtime_file.name,
    )

    def defer_to_configured_file(entry: RuleEntry) -> ConditionalResult | None:
        assert entry.id == "CONTRACT-DEFAULT"
        return None if runtime_file.is_file() else ConditionalResult(run=False)

    verdict = run(
        (rule,),
        repo_root=tmp_path,
        checks_dir=checks_dir,
        conditional_check=defer_to_configured_file,
    )

    assert verdict.ok
    assert consumed.read_text() == "default report consumed\n"


def test_runner_skips_a_conditional_check_when_its_real_input_is_absent(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    checks_dir = tmp_path / "checks"
    checks_dir.mkdir()
    script = checks_dir / "requires-report.sh"
    script.write_text("#!/usr/bin/env bash\nexit 0\n")
    script.chmod(0o755)
    env_var = f"TC_FITNESS_CONTRACT_ABSENT_{uuid.uuid4().hex.upper()}"
    assert env_var not in os.environ
    rule = RuleEntry(
        id="CONTRACT-ABSENT",
        gate="contract-absent",
        check="requires-report",
        script=script.name,
        subprocess_arg_env=env_var,
    )

    verdict = run((rule,), repo_root=tmp_path, checks_dir=checks_dir)

    assert verdict.ok
    assert verdict.skipped == 1
    assert "runtime input not found" in capsys.readouterr().out


def test_runner_imports_a_local_python_check_from_its_resolved_script(
    tmp_path: Path,
) -> None:
    checks_dir = tmp_path / "checks"
    checks_dir.mkdir()
    check_name = "contract_" + uuid.uuid4().hex
    (checks_dir / f"check_{check_name}.py").write_text("def main():\n    return 0\n")
    rule = RuleEntry(id="CONTRACT-PYTHON", gate="contract-python", check=check_name)

    verdict = run((rule,), repo_root=tmp_path, checks_dir=checks_dir)

    assert verdict.ok
    assert verdict.ran == 1


def test_runner_composes_file_local_staging_with_a_real_consumer_binding(tmp_path: Path) -> None:
    checks_dir = tmp_path / "scripts" / "checks"
    checks_dir.mkdir(parents=True)
    sources = tmp_path / "sources"
    sources.mkdir()
    (sources / "changed.py").write_text("value = 1\n")
    (sources / "unchanged.py").write_text("value = 2\n")
    seen_count = tmp_path / "seen-count.txt"
    (checks_dir / "check_counter.py").write_text(
        "from pathlib import Path\n"
        "from tc_fitness import python_files\n"
        "def main():\n"
        f"    walked = python_files('sources', repo_root=Path({str(tmp_path)!r}))\n"
        f"    Path({str(seen_count)!r}).write_text(str(len(walked)))\n"
        "    return 0\n"
    )
    sys.path.insert(0, str(checks_dir))
    try:
        importlib.import_module("check_counter")
        rule = RuleEntry(
            id="CONTRACT-FILE-LOCAL",
            gate="contract-file-local",
            check="counter",
            staged_class="file-local",
            staged_scope=("sources",),
        )
        verdict = run(
            (rule,),
            mode="staged",
            staged_files=["sources/changed.py"],
            repo_root=tmp_path,
            checks_dir=checks_dir,
            enumeration_narrower=make_binding_narrower(),
        )
    finally:
        sys.modules.pop("check_counter", None)
        if str(checks_dir) in sys.path:
            sys.path.remove(str(checks_dir))

    assert verdict.ok
    assert verdict.ran == 1
    assert seen_count.read_text() == "1"
    assert len(tc_fitness.python_files("sources", repo_root=tmp_path)) == 2


def test_scheduled_gate_replays_captured_command_output_in_stage_order(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (tmp_path / ".tc-fitness.toml").write_text(
        'name = "public gate contract"\n'
        '[[steps]]\nid = "first"\nstage = "parallel"\nshell = "printf first-output"\n'
        '[[steps]]\nid = "second"\nstage = "parallel"\nshell = "printf second-output"\n'
    )

    outcome = run_gate(load_config(tmp_path), tmp_path)

    output = capsys.readouterr().out
    assert outcome.ok
    assert output.index("first-output") < output.index("second-output")
