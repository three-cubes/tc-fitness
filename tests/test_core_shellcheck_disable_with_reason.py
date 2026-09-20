"""Tests for the CORE check shellcheck_disable_with_reason (v0.6.0)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from tc_fitness.core_checks.shellcheck_disable_with_reason import (
    DEFAULT_MIN_RATIONALE_LEN,
    DEFAULT_RATIONALE_MARKERS,
    ShellcheckDisableWithReason,
    build,
    file_has_unjustified_disable,
    is_shell_file,
)

pytestmark = pytest.mark.integration

_BARE = """\
#!/usr/bin/env bash
# shellcheck disable=SC1090
. "$SECRETS_FILE"
"""

_INLINE_REASON = """\
#!/usr/bin/env bash
# shellcheck disable=SC2034  # exported via process substitution below
x=1
"""

_PRECEDING_REASON = """\
#!/usr/bin/env bash
# safe -- sourced path computed from a controlled config var
# shellcheck disable=SC1090
. "$SECRETS_FILE"
"""


def _seed(tmp_path: Path, rel: str, body: str) -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


def _kw() -> dict:
    return {"markers": DEFAULT_RATIONALE_MARKERS, "min_len": DEFAULT_MIN_RATIONALE_LEN}


def test_detection_core_flags_bare(tmp_path: Path) -> None:
    p = _seed(tmp_path, "x.sh", _BARE)
    assert file_has_unjustified_disable(p, **_kw()) is True


def test_inline_reason_satisfies(tmp_path: Path) -> None:
    p = _seed(tmp_path, "x.sh", _INLINE_REASON)
    assert file_has_unjustified_disable(p, **_kw()) is False


def test_preceding_reason_satisfies(tmp_path: Path) -> None:
    p = _seed(tmp_path, "x.sh", _PRECEDING_REASON)
    assert file_has_unjustified_disable(p, **_kw()) is False


def test_clean_shell_without_directives_and_non_shell_text_are_ignored(tmp_path: Path) -> None:
    _seed(tmp_path, "src/clean.sh", "#!/bin/sh\necho ready\n")
    _seed(tmp_path, "src/notes.txt", "# shellcheck disable=SC1090\n")
    rule = build({"roots": ["src"]}, repo_root=tmp_path)

    assert rule.run() == 0


def test_each_disable_needs_its_own_rationale(tmp_path: Path) -> None:
    body = "#!/bin/sh\n# shellcheck disable=SC2034 -- declared for child shells\n"
    body += "# shellcheck disable=SC1090\n"
    _seed(tmp_path, "src/multiple.sh", body)
    rule = build({"roots": ["src"]}, repo_root=tmp_path)

    assert rule.run() == 1


def test_blank_lines_do_not_separate_preceding_reason(tmp_path: Path) -> None:
    body = "#!/bin/sh\n# why: this path is dynamically assembled\n\n"
    body += "# shellcheck disable=SC1090\n"
    source = _seed(tmp_path, "src/sourced.sh", body)
    rule = build({"roots": ["src"]}, repo_root=tmp_path)

    assert rule.file_has_violation(source) is False


def test_noncomment_preceding_line_and_short_inline_text_do_not_justify(tmp_path: Path) -> None:
    body = "echo ready\n# shellcheck disable=SC1090 # ok\n"
    _seed(tmp_path, "src/unjustified.sh", body)
    rule = build({"roots": ["src"], "min_rationale_len": 12}, repo_root=tmp_path)

    assert rule.run() == 1


def test_custom_rationale_marker_is_case_insensitive(tmp_path: Path) -> None:
    body = "#!/bin/sh\n# shellcheck disable=SC1090 # NEEDS-REASON because shell exports it\n"
    _seed(tmp_path, "src/custom.sh", body)
    rule = build({"roots": ["src"], "rationale_markers": ["needs-reason"]}, repo_root=tmp_path)

    assert rule.run() == 0


def test_inline_marker_explains_disable_even_when_short(tmp_path: Path) -> None:
    source = _seed(tmp_path, "scripts/short.sh", "# shellcheck disable=SC1090 # reason: dynamic source\n")
    rule = build({"roots": ["scripts"]}, repo_root=tmp_path)

    assert rule.file_has_violation(source) is False


def test_empty_preceding_comment_does_not_explain_disable(tmp_path: Path) -> None:
    _seed(tmp_path, "scripts/empty-comment.sh", "#\n# shellcheck disable=SC1090\n")
    rule = build({"roots": ["scripts"]}, repo_root=tmp_path)

    assert rule.run() == 1


def test_disable_at_first_line_without_preceding_rationale_is_flagged(tmp_path: Path) -> None:
    _seed(tmp_path, "scripts/first-line.sh", "# shellcheck disable=SC1090\n")
    rule = build({"roots": ["scripts"]}, repo_root=tmp_path)

    assert rule.run() == 1


def test_shellcheck_words_cannot_justify_themselves(tmp_path: Path) -> None:
    _seed(tmp_path, "scripts/self-reference.sh", "# shellcheck disable=SC1090 # shellcheck disable\n")
    rule = build({"roots": ["scripts"]}, repo_root=tmp_path)

    assert rule.run() == 1


def test_shebang_probe_treats_missing_file_as_non_shell(tmp_path: Path) -> None:
    from tc_fitness.core_checks.shellcheck_disable_with_reason import is_shell_file

    assert is_shell_file(tmp_path / "missing-script") is False


def test_discovery_ignores_cache_directories(tmp_path: Path) -> None:
    _seed(tmp_path, "scripts/__pycache__/ignored.sh", _BARE)
    rule = build({"roots": ["scripts"]}, repo_root=tmp_path)

    assert rule.run() == 0


def test_missing_configured_shell_root_is_reported(tmp_path: Path) -> None:
    rule = build({"roots": ["scripts"]}, repo_root=tmp_path)

    assert rule.run() == 1


def test_invalid_utf8_in_configured_shell_file_is_not_clean(tmp_path: Path) -> None:
    source = tmp_path / "src" / "broken.sh"
    source.parent.mkdir()
    source.write_bytes(b"# shellcheck disable=SC1090 \xff\n")
    rule = build({"roots": ["src"]}, repo_root=tmp_path)

    assert rule.run() == 1


def test_shebang_file_without_sh_ext_detected(tmp_path: Path) -> None:
    p = _seed(tmp_path, "src/deploy", _BARE)
    assert is_shell_file(p) is True
    rule = ShellcheckDisableWithReason.from_config({"roots": ["src"]}, repo_root=tmp_path)
    assert {str(x) for x in rule.collect_violations()} == {"src/deploy"}


def test_rule_from_config_scopes_roots(tmp_path: Path) -> None:
    _seed(tmp_path, "src/a.sh", _BARE)
    _seed(tmp_path, "vendor/a.sh", _BARE)
    rule = ShellcheckDisableWithReason.from_config({"roots": ["src"]}, repo_root=tmp_path)
    assert {str(p) for p in rule.collect_violations()} == {"src/a.sh"}


def test_no_repo_strings_in_executable_code() -> None:
    import tc_fitness.core_checks.shellcheck_disable_with_reason as mod

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
