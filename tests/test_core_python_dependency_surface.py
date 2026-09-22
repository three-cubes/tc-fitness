"""Contract tests for the repo-agnostic Python dependency surface CORE check."""

from __future__ import annotations

import ast
import runpy
import sys
from pathlib import Path

import pytest

from tc_fitness.core_checks.python_dependency_surface import (
    RULE_ALTERNATIVE_MANIFEST,
    RULE_PRIVATE_INTERPRETER,
    RULE_RAW_PIP_INSTALL,
    RULE_VENV_BOOTSTRAP,
    _argv_findings,
    _iter_files,
    _string_sequence,
    _text_findings,
    build,
    main,
    scan_findings,
)
from tc_fitness.gate import run_gate
from tc_fitness.gate_config import load_config

pytestmark = pytest.mark.unit


def test_scans_argv_bootstrap_in_non_executable_python(tmp_path: Path) -> None:
    path = tmp_path / "tools" / "bootstrap.py"
    path.parent.mkdir()
    path.write_text(
        'subprocess.run([sys.executable, "-m", "venv", ".venv"])\n'
        'subprocess.run([sys.executable, "-m", "pip", "install", "demo"])\n',
        encoding="utf-8",
    )

    findings = scan_findings(tmp_path, roots=("tools",))

    assert {(finding.path, finding.rule) for finding in findings} == {
        ("tools/bootstrap.py", RULE_RAW_PIP_INSTALL),
        ("tools/bootstrap.py", RULE_VENV_BOOTSTRAP),
    }
    assert not path.stat().st_mode & 0o111


def test_approved_uv_pip_and_project_interpreter_are_not_findings(tmp_path: Path) -> None:
    path = tmp_path / "tools" / "run.py"
    path.parent.mkdir()
    path.write_text(
        'subprocess.run(["uv", "pip", "install", "demo"])\n'
        'subprocess.run(["uv", "run", "python", "-m", "demo"])\n',
        encoding="utf-8",
    )

    assert scan_findings(tmp_path, roots=("tools",)) == ()


def test_private_interpreter_and_alternative_manifest_are_findings(tmp_path: Path) -> None:
    script = tmp_path / "scripts" / "run.sh"
    script.parent.mkdir()
    script.write_text(".venv/bin/python -m demo\n", encoding="utf-8")
    lock = tmp_path / "scripts" / "requirements-prod.txt"
    lock.write_text("demo==1\n", encoding="utf-8")

    findings = scan_findings(tmp_path, roots=("scripts",))

    assert {(finding.path, finding.rule) for finding in findings} == {
        ("scripts/run.sh", RULE_PRIVATE_INTERPRETER),
        ("scripts/requirements-prod.txt", RULE_ALTERNATIVE_MANIFEST),
    }


def test_nested_project_manifests_are_findings(tmp_path: Path) -> None:
    nested = tmp_path / "packages" / "child"
    nested.mkdir(parents=True)
    (nested / "pyproject.toml").write_text("[project]\nname='child'\n", encoding="utf-8")
    (nested / "uv.lock").write_text("version = 1\n", encoding="utf-8")

    findings = scan_findings(tmp_path, roots=("packages",))

    assert {(finding.path, finding.rule) for finding in findings} == {
        ("packages/child/pyproject.toml", RULE_ALTERNATIVE_MANIFEST),
        ("packages/child/uv.lock", RULE_ALTERNATIVE_MANIFEST),
    }


def test_canonical_root_manifests_are_clean(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text("[project]\nname='x'\n", encoding="utf-8")
    (tmp_path / "uv.lock").write_text("version = 1\n", encoding="utf-8")
    rule = build({"roots": ["."]}, repo_root=tmp_path)

    assert rule.collect_violations() == set()


def test_ratchet_allows_only_shrink_and_known_content(tmp_path: Path) -> None:
    path = tmp_path / "tools" / "run.sh"
    path.parent.mkdir()
    path.write_text("pip install demo\n", encoding="utf-8")
    config = {
        "roots": ["tools"],
        "ratchets": [
            {
                "path": "tools/run.sh",
                "rule": RULE_RAW_PIP_INSTALL,
                "max_count": 1,
                "contents": ["pip install demo"],
            }
        ],
    }

    assert build(config, repo_root=tmp_path).collect_violations() == set()
    path.write_text("pip install replacement\n", encoding="utf-8")
    assert {str(item) for item in build(config, repo_root=tmp_path).collect_violations()} == {"tools/run.sh"}


def test_ratchet_must_track_current_count_and_exemptions_are_rejected(tmp_path: Path) -> None:
    path = tmp_path / "tools" / "run.sh"
    path.parent.mkdir()
    path.write_text("pip install one\npip install two\n", encoding="utf-8")
    config = {
        "roots": ["tools"],
        "ratchets": [{"path": "tools/run.sh", "rule": RULE_RAW_PIP_INSTALL, "max_count": 1}],
    }
    assert build(config, repo_root=tmp_path).collect_violations() == {Path("tools/run.sh")}
    with pytest.raises(ValueError, match="exempt_paths"):
        build({"roots": ["tools"], "exempt_paths": ["tools/"]}, repo_root=tmp_path)


def test_stale_ratchet_is_rejected_when_its_last_finding_disappears(tmp_path: Path) -> None:
    path = tmp_path / "tools" / "run.sh"
    path.parent.mkdir()
    path.write_text("pip install demo\n", encoding="utf-8")
    config = {
        "roots": ["tools"],
        "ratchets": [{"path": "tools/run.sh", "rule": RULE_RAW_PIP_INSTALL, "max_count": 1}],
    }
    path.write_text("#!/bin/sh\necho clean\n", encoding="utf-8")

    assert build(config, repo_root=tmp_path).run() == 1


def test_full_argv_global_options_launch_calls_and_nested_manifests(tmp_path: Path) -> None:
    path = tmp_path / "tools" / "run.py"
    path.parent.mkdir()
    path.write_text(
        'notify(["pip", "install", "not-a-process"])\n'
        'subprocess.run([sys.executable, "-m", "pip", "--isolated", "install", "demo"])\n',
        encoding="utf-8",
    )
    req = tmp_path / "tools" / "requirements" / "prod.txt"
    req.parent.mkdir()
    req.write_text("demo==1\n", encoding="utf-8")
    findings = scan_findings(tmp_path, roots=("tools",))
    assert {(finding.rule, finding.content) for finding in findings} == {
        (RULE_RAW_PIP_INSTALL, "<dynamic> -m pip --isolated install demo"),
        (RULE_ALTERNATIVE_MANIFEST, "prod.txt"),
    }


def test_argv_parser_skips_valued_options_and_nested_kwargs(tmp_path: Path) -> None:
    path = tmp_path / "tools" / "run.py"
    path.parent.mkdir()
    path.write_text(
        'subprocess.run(["pip", "--timeout", "10", "--trusted-host", "pypi.org", "install", "demo"])\n'
        'subprocess.run(["echo"], kwargs={"args": ["pip", "install", "not-a-process"]})\n',
        encoding="utf-8",
    )

    findings = scan_findings(tmp_path, roots=("tools",))

    assert [(finding.rule, finding.content) for finding in findings] == [
        (RULE_RAW_PIP_INSTALL, "pip --timeout 10 --trusted-host pypi.org install demo")
    ]


def test_argv_parser_requires_pip_executable_or_python_module(tmp_path: Path) -> None:
    path = tmp_path / "tools" / "run.py"
    path.parent.mkdir(parents=True)
    path.write_text(
        'subprocess.run(["echo", "pip", "install", "not-a-process"] )\n'
        'subprocess.run(["python", "-m", "pip", "install", "demo"])\n',
        encoding="utf-8",
    )

    findings = scan_findings(tmp_path, roots=("tools",))

    assert [(finding.rule, finding.content) for finding in findings] == [
        (RULE_RAW_PIP_INSTALL, "python -m pip install demo")
    ]


def test_argv_parser_covers_nonmatching_and_dynamic_process_sequences() -> None:
    findings = _argv_findings(
        "subprocess.run(dynamic)\n"
        'subprocess.run(["pip", "package", "install", "not-a-process"])\n'
        'subprocess.run(["pip", "--isolated"])\n',
        "tools/run.py",
    )

    assert findings == []


def test_argv_parser_rejects_non_python_module_interpreters() -> None:
    assert (
        _argv_findings(
            'subprocess.run(["pypy", "-m", "pip", "install", "demo"])\n',
            "tools/run.py",
        )
        == []
    )


def test_argv_parser_rejects_non_python_launcher_for_module_pip() -> None:
    assert (
        _argv_findings(
            'subprocess.run(["echo", "-m", "pip", "install", "demo"])\n',
            "tools/run.py",
        )
        == []
    )


def test_argv_parser_detects_private_interpreter(tmp_path: Path) -> None:
    path = tmp_path / "tools" / "run.py"
    path.parent.mkdir(parents=True)
    path.write_text(
        'subprocess.run([".venv/bin/python", "-m", "tool"])\n',
        encoding="utf-8",
    )

    findings = scan_findings(tmp_path, roots=("tools",))

    assert [(finding.rule, finding.content) for finding in findings] == [
        (RULE_PRIVATE_INTERPRETER, ".venv/bin/python -m tool")
    ]


def test_shell_parser_skips_valued_options(tmp_path: Path) -> None:
    path = tmp_path / "tools" / "run.sh"
    path.parent.mkdir()
    path.write_text("pip --timeout 10 --trusted-host pypi.org install demo\n", encoding="utf-8")

    findings = scan_findings(tmp_path, roots=("./tools/",))

    assert [(finding.rule, finding.content) for finding in findings] == [
        (RULE_RAW_PIP_INSTALL, "pip --timeout 10 --trusted-host pypi.org install demo")
    ]


def test_shell_parser_requires_pip_executable_or_python_module(tmp_path: Path) -> None:
    path = tmp_path / "tools" / "run.sh"
    path.parent.mkdir(parents=True)
    path.write_text("echo pip install not-a-process\npython -m pip install demo\n", encoding="utf-8")

    findings = scan_findings(tmp_path, roots=("tools",))

    assert [(finding.rule, finding.content) for finding in findings] == [
        (RULE_RAW_PIP_INSTALL, "python -m pip install demo")
    ]


def test_shell_parser_covers_equals_options_and_malformed_commands(tmp_path: Path) -> None:
    path = tmp_path / "tools" / "run.sh"
    path.parent.mkdir(parents=True)
    path.write_text(
        "pip --config-settings=foo=bar install demo\n"
        "pip package install not-a-process\n"
        "pip --isolated\n"
        'echo "unterminated\n',
        encoding="utf-8",
    )

    findings = _text_findings(path, "tools/run.sh")

    assert [(finding.rule, finding.content) for finding in findings] == [
        (RULE_RAW_PIP_INSTALL, "pip --config-settings=foo=bar install demo")
    ]


def test_scan_findings_deduplicates_repeated_literal_calls(tmp_path: Path) -> None:
    path = tmp_path / "tools" / "run.sh"
    path.parent.mkdir(parents=True)
    path.write_text("pip install demo; pip install demo\n", encoding="utf-8")

    findings = scan_findings(tmp_path, roots=("tools",))

    assert [(finding.rule, finding.path) for finding in findings] == [(RULE_RAW_PIP_INSTALL, "tools/run.sh")]


def test_tracked_enumeration_normalises_overlapping_dot_roots_and_ignores_untracked_files(
    tmp_path: Path,
) -> None:
    import subprocess

    tools = tmp_path / "tools"
    nested = tools / "nested"
    nested.mkdir(parents=True)
    tracked = tools / "tracked.sh"
    tracked.write_text("pip install demo\n", encoding="utf-8")
    ignored = nested / "ignored.sh"
    ignored.write_text("pip install ignored\n", encoding="utf-8")
    (tmp_path / ".gitignore").write_text("tools/nested/ignored.sh\n", encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "add", ".gitignore", "tools/tracked.sh"], cwd=tmp_path, check=True)

    findings = scan_findings(tmp_path, roots=(".", "./tools", "tools/nested/"))

    assert [(finding.path, finding.rule) for finding in findings] == [
        ("tools/tracked.sh", RULE_RAW_PIP_INSTALL)
    ]


def test_python_source_has_one_structural_finding_per_argv(tmp_path: Path) -> None:
    path = tmp_path / "tools" / "run.py"
    path.parent.mkdir()
    path.write_text('subprocess.run(["pip", "install", "demo"])\n', encoding="utf-8")
    findings = scan_findings(tmp_path, roots=("tools",))
    assert [(finding.rule, finding.content) for finding in findings] == [
        (RULE_RAW_PIP_INSTALL, "pip install demo")
    ]


def test_chained_uv_command_does_not_hide_second_install(tmp_path: Path) -> None:
    script = tmp_path / "tools" / "run.sh"
    script.parent.mkdir()
    script.write_text("uv pip install approved && pip install untracked\n", encoding="utf-8")
    findings = scan_findings(tmp_path, roots=("tools",))
    assert [(finding.rule, finding.content) for finding in findings] == [
        (RULE_RAW_PIP_INSTALL, "pip install untracked")
    ]


def test_rule_emits_actionable_output_for_unratcheted_finding(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "tools" / "run.sh"
    path.parent.mkdir()
    path.write_text("pip install demo\n", encoding="utf-8")

    assert build({"roots": ["tools"]}, repo_root=tmp_path).run() == 1
    output = capsys.readouterr().out
    assert all(marker in output for marker in ("fix:", "next:", "run:"))


def test_configured_core_entry_runs_through_gate(tmp_path: Path) -> None:
    """The published CORE check is consumable through a real gate catalogue."""
    checks = tmp_path / "scripts" / "checks"
    checks.mkdir(parents=True)
    (tmp_path / "scripts" / "__init__.py").write_text("", encoding="utf-8")
    (checks / "__init__.py").write_text("", encoding="utf-8")
    (checks / "surface_catalogue.py").write_text(
        "from tc_fitness.catalogue import RuleEntry\n"
        "ALL_ENTRIES = (RuleEntry(id='surface', gate='surface', "
        "check='core:python_dependency_surface'),)\n",
        encoding="utf-8",
    )
    (tmp_path / "tools").mkdir()
    (tmp_path / "tools" / "bootstrap.py").write_text(
        'subprocess.run([sys.executable, "-m", "pip", "install", "demo"])\n',
        encoding="utf-8",
    )
    (tmp_path / "pyproject.toml").write_text(
        "[project]\nname = 'consumer'\nversion = '0.0.0'\n\n"
        "[tool.tc_fitness]\nname = 'consumer gate'\n\n"
        "[[tool.tc_fitness.steps]]\n"
        "id = 'surface'\nsummary = 'dependency surface'\n"
        "catalogue = 'scripts.checks.surface_catalogue:ALL_ENTRIES'\n"
        "checks_dir = 'scripts/checks'\n\n"
        "[tool.tc_fitness.core_checks.python_dependency_surface]\n"
        "roots = ['tools']\n",
        encoding="utf-8",
    )

    try:
        outcome = run_gate(load_config(tmp_path), tmp_path)
        assert not outcome.ok
    finally:
        for name in list(sys.modules):
            if name == "scripts" or name.startswith("scripts."):
                del sys.modules[name]


def test_argv_parser_handles_dynamic_and_invalid_python(tmp_path: Path) -> None:
    assert _string_sequence(ast.parse("value = 1").body[0]) is None
    assert _argv_findings("not valid python(", "tools/bad.py") == []
    findings = _argv_findings(
        'subprocess.run(["pip", "install", "demo"])\n'
        'subprocess.run(["-m", "pip", "install", "demo"])\n'
        'subprocess.run([dynamic, "-m", "venv"])\n',
        "tools/run.py",
    )
    assert [finding.content for finding in findings] == [
        "pip install demo",
        "-m pip install demo",
        "<dynamic> -m venv",
    ]
    unreadable = tmp_path / "tools" / "broken.py"
    unreadable.parent.mkdir()
    unreadable.write_bytes(b"\xff")
    assert _text_findings(unreadable, "tools/broken.py") == []


def test_shell_findings_and_file_enumeration_cover_policy_boundaries(tmp_path: Path) -> None:
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    shell = scripts / "bootstrap.sh"
    shell.write_text(
        "# python -m venv ignored in a comment\n\n"
        "python -m venv .venv\n"
        "pip install demo\n"
        "uv pip install approved\n"
        ".venv/bin/python -m demo\n",
        encoding="utf-8",
    )
    executable = scripts / "tool"
    executable.write_text("pip install executable\n", encoding="utf-8")
    executable.chmod(0o755)
    (scripts / ".venv").mkdir()
    (scripts / ".venv" / "ignored.py").write_text("pip install ignored\n", encoding="utf-8")

    findings = _text_findings(shell, "scripts/bootstrap.sh")
    assert {finding.rule for finding in findings} == {
        RULE_RAW_PIP_INSTALL,
        RULE_VENV_BOOTSTRAP,
        RULE_PRIVATE_INTERPRETER,
    }
    paths = {
        path.relative_to(tmp_path).as_posix() for path in _iter_files(tmp_path, ("missing",), (".py",), ())
    }
    assert paths == set()
    paths = {path.relative_to(tmp_path).as_posix() for path in _iter_files(tmp_path, ("scripts",), (), ())}
    assert paths == {"scripts/tool"}


def test_invalid_ratchets_and_file_level_dispatch_are_explicit(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="array of tables"):
        build({"ratchets": "invalid"}, repo_root=tmp_path)
    with pytest.raises(ValueError, match="each ratchet"):
        build({"ratchets": ["invalid"]}, repo_root=tmp_path)
    with pytest.raises(ValueError, match="non-negative"):
        build({"ratchets": [{"path": "x", "rule": "x", "max_count": -1}]}, repo_root=tmp_path)

    path = tmp_path / "tools" / "run.sh"
    path.parent.mkdir()
    path.write_text("pip install demo\n", encoding="utf-8")
    rule = build({"roots": ["tools"]}, repo_root=tmp_path)
    assert rule.file_has_violation(path)
    assert not rule.file_has_violation(tmp_path / "other.sh")
    assert main([]) == 0


def test_module_main_guard_exits_cleanly() -> None:
    original_argv = sys.argv
    sys.argv = ["python-dependency-surface"]
    try:
        with pytest.raises(SystemExit) as raised:
            runpy.run_module("tc_fitness.core_checks.python_dependency_surface", run_name="__main__")
    finally:
        sys.argv = original_argv
    assert raised.value.code == 0
