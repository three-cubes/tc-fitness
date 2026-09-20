"""Tests for the CORE check ci_silencers_have_rationale (v0.6.0)."""

from __future__ import annotations

import ast
import re
from pathlib import Path

import pytest

from tc_fitness.core_checks.ci_silencers_have_rationale import (
    DEFAULT_RATIONALE_TOKENS,
    DEFAULT_SILENCER_PATTERNS,
    DEFAULT_WINDOW,
    CiSilencersHaveRationale,
    build,
    file_has_unjustified_silencer,
)

pytestmark = pytest.mark.integration

_BARE = """\
jobs:
  lint:
    continue-on-error: true
    steps:
      - run: ruff check .
"""

_COMMENT_REASON = """\
jobs:
  lint:
    continue-on-error: true  # non-blocking: advisory lint job
    steps:
      - run: ruff check .
"""

_NEARBY_REASON = """\
jobs:
  lint:
    # intentional: this gate is advisory only
    continue-on-error: true
    steps:
      - run: ruff check .
"""

_SIL = re.compile("|".join(f"(?:{p})" for p in DEFAULT_SILENCER_PATTERNS))
_RAT = re.compile("|".join(re.escape(t) for t in DEFAULT_RATIONALE_TOKENS), re.IGNORECASE)


def _seed(tmp_path: Path, rel: str, body: str) -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


def _detect(p: Path) -> bool:
    return file_has_unjustified_silencer(p, silencer_re=_SIL, rationale_re=_RAT, window=DEFAULT_WINDOW)


def test_detection_core_flags_bare(tmp_path: Path) -> None:
    p = _seed(tmp_path, "ci.yml", _BARE)
    assert _detect(p) is True


def test_trailing_comment_satisfies(tmp_path: Path) -> None:
    p = _seed(tmp_path, "ci.yml", _COMMENT_REASON)
    assert _detect(p) is False


def test_nearby_token_satisfies(tmp_path: Path) -> None:
    p = _seed(tmp_path, "ci.yml", _NEARBY_REASON)
    assert _detect(p) is False


@pytest.mark.parametrize(
    "body",
    [
        "continue-on-error: true\n",
        "fail_ci_if_error: false\n",
        "command || true\n",
        "pytest --cov-fail-under=0\n",
        "if: ${{ always() }}\n",
    ],
)
def test_each_supported_silencer_requires_a_reason(tmp_path: Path, body: str) -> None:
    assert _detect(_seed(tmp_path, "ci.yml", body)) is True


def test_empty_inline_comment_does_not_explain_a_silencer(tmp_path: Path) -> None:
    assert _detect(_seed(tmp_path, "ci.yml", "continue-on-error: true  #\n")) is True


def test_nonempty_inline_comment_supplies_its_reason(tmp_path: Path) -> None:
    assert _detect(_seed(tmp_path, "ci.yml", "continue-on-error: true  # local lint is advisory\n")) is False


def test_rationale_outside_the_configured_window_does_not_apply(tmp_path: Path) -> None:
    path = _seed(tmp_path, "ci.yml", "# intentional legacy note\n\n\ncontinue-on-error: true\n")

    assert file_has_unjustified_silencer(path, silencer_re=_SIL, rationale_re=_RAT, window=1) is True


def test_read_failures_are_ignored_by_this_scanner(tmp_path: Path) -> None:
    missing = tmp_path / "missing.yml"
    invalid = tmp_path / "invalid.yml"
    invalid.write_bytes(b"continue-on-error: true\n\xff")

    assert _detect(missing) is False
    assert _detect(invalid) is False


def test_enumerates_workflow_dir(tmp_path: Path) -> None:
    _seed(tmp_path, ".github/workflows/ci.yml", _BARE)
    _seed(tmp_path, ".github/workflows/ok.yml", _COMMENT_REASON)
    rule = CiSilencersHaveRationale.from_config({}, repo_root=tmp_path)
    assert {str(p) for p in rule.collect_violations()} == {".github/workflows/ci.yml"}


def test_nonexistent_workflow_and_scan_files_produce_empty_inventory(tmp_path: Path) -> None:
    rule = build({"workflows_dir": "not-created", "scan_files": ["missing.sh"]}, repo_root=tmp_path)

    assert rule.enumerate_files() == []


def test_configured_patterns_tokens_and_window_are_used(tmp_path: Path) -> None:
    path = _seed(tmp_path, "pipeline.yml", "# checked by owner\ncontinue-on-error: true\n")
    rule = build(
        {
            "scan_files": ["pipeline.yml"],
            "rationale_tokens": ["checked by owner"],
            "silencer_patterns": [r"continue-on-error\s*:\s*true"],
            "window": 1,
        },
        repo_root=tmp_path,
    )

    assert rule.file_has_violation(path) is False


def test_scan_files_config_driven(tmp_path: Path) -> None:
    _seed(tmp_path, "scripts/check.sh", "pytest || true\n")
    rule = build({"scan_files": ["scripts/check.sh"]}, repo_root=tmp_path)
    assert {str(p) for p in rule.collect_violations()} == {"scripts/check.sh"}


def test_no_repo_strings_in_executable_code() -> None:
    import tc_fitness.core_checks.ci_silencers_have_rationale as mod

    text = Path(mod.__file__).read_text(encoding="utf-8")
    tree = ast.parse(text)
    docstring_ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            doc = ast.get_docstring(node, clean=False)
            if doc is not None and node.body:
                first = node.body[0]
                if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant):
                    docstring_ids.add(id(first.value))
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in docstring_ids:
            lowered = node.value.lower()
            for tok in ("kairix", "tc-agent-zone", "agent-zone", "kata"):
                assert tok not in lowered, f"repo identity leaked: {tok}"
