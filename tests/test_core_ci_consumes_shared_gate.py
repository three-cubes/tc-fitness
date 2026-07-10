"""Tests for the CORE check ci_consumes_shared_gate (CI runs the shared gate)."""

from __future__ import annotations

import ast
import re
from pathlib import Path

from tc_fitness.core_checks.ci_consumes_shared_gate import (
    CiConsumesSharedGate,
    build,
    main,
    satisfying_mechanism,
    workflow_files,
)

# A workflow that satisfies the reusable arm: a `uses:` reference to the pinned
# canonical python-quality-gate reusable.
_VIA_REUSABLE = (
    "name: Quality gate\n"
    "on: [pull_request]\n"
    "jobs:\n"
    "  quality:\n"
    "    uses: three-cubes/tc-pipelines/.github/workflows/python-quality-gate.yml@v1.13.0\n"
)

# A workflow that satisfies the engine arm: a step that runs `tc-fitness run`.
_VIA_ENGINE = (
    "name: Quality gate\n"
    "on: [pull_request]\n"
    "jobs:\n"
    "  quality:\n"
    "    runs-on: ubuntu-latest\n"
    "    steps:\n"
    "      - run: uv run tc-fitness run\n"
)

# A workflow that consumes NEITHER — a hand-rolled gate forked off the standard.
_FORKED_GATE = (
    "name: Quality gate\n"
    "on: [pull_request]\n"
    "jobs:\n"
    "  quality:\n"
    "    runs-on: ubuntu-latest\n"
    "    steps:\n"
    "      - run: ruff check . && pytest\n"
)


def _write_workflow(tmp_path: Path, name: str, body: str) -> Path:
    p = tmp_path / ".github" / "workflows" / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


# --------------------------------------------------------------------------- #
# Pure-helper unit tests (the detection + enumeration cores).
# --------------------------------------------------------------------------- #


def test_workflow_files_enumerates_only_yaml(tmp_path: Path) -> None:
    _write_workflow(tmp_path, "ci.yml", _VIA_REUSABLE)
    _write_workflow(tmp_path, "release.yaml", _VIA_ENGINE)
    _write_workflow(tmp_path, "notes.md", "not a workflow\n")
    found = {p.name for p in workflow_files(tmp_path / ".github" / "workflows")}
    assert found == {"ci.yml", "release.yaml"}


def test_workflow_files_missing_dir_is_empty(tmp_path: Path) -> None:
    assert workflow_files(tmp_path / ".github" / "workflows") == []


def test_satisfying_mechanism_prefers_reusable() -> None:
    reusable = re.compile(r"three-cubes/tc-pipelines/\.github/workflows/python-quality-gate\.yml@")
    engine = re.compile(r"\btc-fitness run\b")
    # Carries BOTH: a comment mentioning `tc-fitness run` above the `uses:` line.
    both = "# runs tc-fitness run under the hood\n" + _VIA_REUSABLE
    hit = satisfying_mechanism(both, reusable_pattern=reusable, engine_pattern=engine)
    assert hit is not None
    mechanism, _line_no, _line = hit
    assert "reusable-workflow" in mechanism


def test_satisfying_mechanism_none_on_fork() -> None:
    reusable = re.compile(r"three-cubes/tc-pipelines/\.github/workflows/python-quality-gate\.yml@")
    engine = re.compile(r"\btc-fitness run\b")
    assert satisfying_mechanism(_FORKED_GATE, reusable_pattern=reusable, engine_pattern=engine) is None


# --------------------------------------------------------------------------- #
# PASS arms.
# --------------------------------------------------------------------------- #


def test_pass_via_reusable(tmp_path: Path) -> None:
    _write_workflow(tmp_path, "ci.yml", _VIA_REUSABLE)
    assert build({}, repo_root=tmp_path).run() == 0


def test_pass_via_engine(tmp_path: Path) -> None:
    _write_workflow(tmp_path, "ci.yml", _VIA_ENGINE)
    assert build({}, repo_root=tmp_path).run() == 0


def test_pass_when_one_of_several_workflows_satisfies(tmp_path: Path) -> None:
    # A repo with several workflows passes when ANY of them consumes the gate.
    _write_workflow(tmp_path, "docs.yml", _FORKED_GATE)
    _write_workflow(tmp_path, "ci.yml", _VIA_REUSABLE)
    assert build({}, repo_root=tmp_path).run() == 0


# --------------------------------------------------------------------------- #
# FAIL arm — CI present, but the gate is forked off the shared standard.
# --------------------------------------------------------------------------- #


def test_fail_on_fork(tmp_path: Path) -> None:
    _write_workflow(tmp_path, "ci.yml", _FORKED_GATE)
    assert build({}, repo_root=tmp_path).run() == 1


def test_fail_on_multiple_forked_workflows(tmp_path: Path) -> None:
    _write_workflow(tmp_path, "ci.yml", _FORKED_GATE)
    _write_workflow(tmp_path, "nightly.yml", "name: nightly\non: schedule\n")
    assert build({}, repo_root=tmp_path).run() == 1


# --------------------------------------------------------------------------- #
# SKIP arm — no CI workflows to enforce.
# --------------------------------------------------------------------------- #


def test_skip_on_no_workflows_dir(tmp_path: Path) -> None:
    # No .github/workflows at all → vacuous pass (nothing to enforce).
    assert build({}, repo_root=tmp_path).run() == 0


def test_skip_on_empty_workflows_dir(tmp_path: Path) -> None:
    # Directory exists but holds no yaml → vacuous pass.
    (tmp_path / ".github" / "workflows").mkdir(parents=True)
    (tmp_path / ".github" / "workflows" / "README.md").write_text("no workflows here\n", encoding="utf-8")
    assert build({}, repo_root=tmp_path).run() == 0


# --------------------------------------------------------------------------- #
# WARN mode — a fork is reported but does NOT fail the build (adoption).
# --------------------------------------------------------------------------- #


def test_warn_only_reports_but_passes(tmp_path: Path, capsys) -> None:  # type: ignore[no-untyped-def]
    _write_workflow(tmp_path, "ci.yml", _FORKED_GATE)
    assert build({"warn_only": True}, repo_root=tmp_path).run() == 0
    out = capsys.readouterr().out
    assert "FAIL" in out  # the fork is still reported loudly
    assert "warn-only" in out


def test_baseline_ok_alias_is_warn_mode(tmp_path: Path) -> None:
    # `baseline_ok` is the accepted alias for `warn_only` — same soft-mode effect.
    _write_workflow(tmp_path, "ci.yml", _FORKED_GATE)
    assert build({"baseline_ok": True}, repo_root=tmp_path).run() == 0


# --------------------------------------------------------------------------- #
# Config knobs.
# --------------------------------------------------------------------------- #


def test_config_workflows_dir_knob(tmp_path: Path) -> None:
    # A repo whose CI lives elsewhere binds `workflows_dir`; the default dir is
    # empty (skip) but the configured dir holds a forked gate (fail).
    other = tmp_path / "ci"
    other.mkdir()
    (other / "pipeline.yml").write_text(_FORKED_GATE, encoding="utf-8")
    assert build({"workflows_dir": "ci"}, repo_root=tmp_path).run() == 1


def test_config_custom_engine_pattern(tmp_path: Path) -> None:
    # A consumer can point the engine arm at a different invocation token.
    body = "name: gate\non: [pull_request]\njobs:\n  q:\n    steps:\n      - run: make org-quality-gate\n"
    _write_workflow(tmp_path, "ci.yml", body)
    # Default patterns do not match → fork.
    assert build({}, repo_root=tmp_path).run() == 1
    # Custom engine pattern matches → pass.
    cfg = {"engine_pattern": r"\bmake org-quality-gate\b"}
    assert build(cfg, repo_root=tmp_path).run() == 0


def test_config_custom_reusable_pattern(tmp_path: Path) -> None:
    body = (
        "name: gate\non: [pull_request]\njobs:\n  q:\n"
        "    uses: my-org/pipelines/.github/workflows/quality.yml@v2\n"
    )
    _write_workflow(tmp_path, "ci.yml", body)
    assert build({}, repo_root=tmp_path).run() == 1
    cfg = {"reusable_pattern": r"my-org/pipelines/\.github/workflows/quality\.yml@"}
    assert build(cfg, repo_root=tmp_path).run() == 0


def test_invalid_pattern_fails_actionably(tmp_path: Path) -> None:
    _write_workflow(tmp_path, "ci.yml", _VIA_REUSABLE)
    # A broken regex is a config error → hard fail regardless of would-be match.
    assert build({"reusable_pattern": "["}, repo_root=tmp_path).run() == 1


def test_from_config_binds_all_knobs(tmp_path: Path) -> None:
    rule = CiConsumesSharedGate.from_config(
        {
            "workflows_dir": "ci",
            "reusable_pattern": r"acme/pipe\.yml@",
            "engine_pattern": r"\bacme-gate\b",
            "warn_only": True,
        },
        repo_root=tmp_path,
    )
    assert rule.workflows_dir == "ci"
    assert rule.reusable_pattern == r"acme/pipe\.yml@"
    assert rule.engine_pattern == r"\bacme-gate\b"
    assert rule.warn_only is True


# --------------------------------------------------------------------------- #
# CLI + engine-conformance parity with the sibling CORE checks.
# --------------------------------------------------------------------------- #


def test_main_establish_baseline_mode(tmp_path: Path) -> None:
    _write_workflow(tmp_path, "ci.yml", _VIA_REUSABLE)
    rc = main(["--establish-baseline", "--repo-root", str(tmp_path)])
    assert rc == 0
    assert (tmp_path / ".architecture" / "baseline" / "ci-consumes-shared-gate-files.txt").exists()


def test_no_repo_strings_in_executable_code() -> None:
    import tc_fitness.core_checks.ci_consumes_shared_gate as mod

    text = Path(mod.__file__).read_text(encoding="utf-8")
    tree = ast.parse(text)
    docstring_ids = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            doc = ast.get_docstring(node, clean=False)
            if doc is not None and node.body:
                first = node.body[0]
                if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant):
                    docstring_ids.add(id(first.value))
    repo_tokens = ("kairix", "tc-agent-zone", "agent-zone", "kata")
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            if id(node) in docstring_ids:
                continue
            lowered = node.value.lower()
            for tok in repo_tokens:
                assert tok not in lowered, f"repo identity leaked in a code literal: {tok}"
