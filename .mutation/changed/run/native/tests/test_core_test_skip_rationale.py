"""Tests for the CORE check test_skip_rationale (v0.6.0)."""

from __future__ import annotations

from pathlib import Path

import pytest
from _core_check_assertions import assert_no_repo_identity

from tc_fitness.core_checks.test_skip_rationale import (
    TestSkipRationale,
    build,
    file_has_skip_without_reason,
)

pytestmark = pytest.mark.integration

_BARE_SKIP = """
import pytest

@pytest.mark.skip
def test_a() -> None:
    assert True
"""

_SKIP_WITH_REASON = """
import pytest

@pytest.mark.skip(reason="re-enabled once the upstream fix lands")
def test_a() -> None:
    assert True
"""

_IMPORTORSKIP_NO_COMMENT = """
import pytest

docx = pytest.importorskip("docx")
"""

_IMPORTORSKIP_WITH_COMMENT = """
import pytest

# docx is an optional runtime dep — skip if missing
docx = pytest.importorskip("docx")
"""


def _seed(tmp_path: Path, rel: str, body: str) -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


def test_detection_flags_bare_skip(tmp_path: Path) -> None:
    p = _seed(tmp_path, "test_x.py", _BARE_SKIP)
    assert file_has_skip_without_reason(p, importorskip_lookback=3) is True


def test_detection_passes_skip_with_reason(tmp_path: Path) -> None:
    p = _seed(tmp_path, "test_x.py", _SKIP_WITH_REASON)
    assert file_has_skip_without_reason(p, importorskip_lookback=3) is False


def test_importorskip_needs_comment(tmp_path: Path) -> None:
    bad = _seed(tmp_path, "test_bad.py", _IMPORTORSKIP_NO_COMMENT)
    good = _seed(tmp_path, "test_good.py", _IMPORTORSKIP_WITH_COMMENT)
    assert file_has_skip_without_reason(bad, importorskip_lookback=3) is True
    assert file_has_skip_without_reason(good, importorskip_lookback=3) is False


def test_lookback_is_config_driven(tmp_path: Path) -> None:
    # Comment two blank-free lines above; lookback=1 cannot see it, lookback=3 can.
    body = "import pytest\n# the reason\nx = 1\ndocx = pytest.importorskip('docx')\n"
    p = _seed(tmp_path, "test_lb.py", body)
    assert file_has_skip_without_reason(p, importorskip_lookback=1) is True
    assert file_has_skip_without_reason(p, importorskip_lookback=3) is False


def test_unparseable_configured_test_file_is_reported(tmp_path: Path) -> None:
    _seed(tmp_path, "tests/test_broken.py", "def test_broken(:\n")
    rule = build({"roots": ["tests"]}, repo_root=tmp_path)

    assert rule.run() == 1


def test_annotated_importorskip_assignment_is_checked(tmp_path: Path) -> None:
    body = "import pytest\nmodule: object = pytest.importorskip('optional_dep')\n"
    _seed(tmp_path, "tests/test_annotated.py", body)
    rule = build({"roots": ["tests"]}, repo_root=tmp_path)

    assert rule.run() == 1


def test_import_alias_does_not_bypass_skip_rationale(tmp_path: Path) -> None:
    body = "import pytest as pt\n\n@pt.mark.skip\ndef test_feature():\n    assert True\n"
    _seed(tmp_path, "tests/test_alias.py", body)
    rule = build({"roots": ["tests"]}, repo_root=tmp_path)

    assert rule.run() == 1


def test_import_alias_does_not_bypass_importorskip_rationale(tmp_path: Path) -> None:
    body = "import pytest as pt\noptional = pt.importorskip('optional_dep')\n"
    _seed(tmp_path, "tests/test_alias_import.py", body)
    rule = build({"roots": ["tests"]}, repo_root=tmp_path)

    assert rule.run() == 1


def test_reasoned_skip_mark_and_importorskip_are_clean(tmp_path: Path) -> None:
    body = "import pytest as pt\n"
    body += "pytestmark = [pt.mark.skipif(True, reason='upstream unavailable')]\n"
    body += "optional = pt.importorskip('optional_dep', reason='optional dependency')\n"
    _seed(tmp_path, "tests/test_reasoned.py", body)
    rule = build({"roots": ["tests"]}, repo_root=tmp_path)

    assert rule.run() == 0


def test_non_pytest_mark_namespace_is_not_treated_as_skip(tmp_path: Path) -> None:
    body = "from domain import mark as custom_mark\n@custom_mark.skip\ndef test_feature():\n    assert True\n"
    _seed(tmp_path, "tests/test_custom_mark.py", body)
    rule = build({"roots": ["tests"]}, repo_root=tmp_path)

    assert rule.run() == 0


def test_custom_object_named_pytest_is_not_assumed_to_be_the_framework(tmp_path: Path) -> None:
    body = "pytest = domain\n@pytest.mark.skip\ndef test_feature():\n    assert True\n"
    _seed(tmp_path, "tests/test_shadowed_name.py", body)
    rule = build({"roots": ["tests"]}, repo_root=tmp_path)

    assert rule.run() == 0


def test_importing_only_a_pytest_submodule_does_not_bind_the_framework_alias(tmp_path: Path) -> None:
    body = "import pytest.plugin\n@pytest.mark.skip\ndef test_feature():\n    assert True\n"
    _seed(tmp_path, "tests/test_submodule_import.py", body)
    rule = build({"roots": ["tests"]}, repo_root=tmp_path)

    assert rule.run() == 0


def test_non_pytest_importorskip_attribute_is_not_treated_as_a_skip(tmp_path: Path) -> None:
    _seed(tmp_path, "tests/test_custom_importorskip.py", "domain.importorskip('optional_dep')\n")
    rule = build({"roots": ["tests"]}, repo_root=tmp_path)

    assert rule.run() == 0


def test_reference_to_importorskip_without_call_is_not_a_skip(tmp_path: Path) -> None:
    _seed(tmp_path, "tests/test_importorskip_reference.py", "import pytest\noptional = pytest.importorskip\n")
    rule = build({"roots": ["tests"]}, repo_root=tmp_path)

    assert rule.run() == 0


def test_from_pytest_aliases_for_marks_and_importorskip_are_recognised(tmp_path: Path) -> None:
    body = "from pytest import mark as pm, importorskip as optional\n"
    body += "@pm.xfail\ndef test_known_failure():\n    assert False\n"
    _seed(tmp_path, "tests/test_from_import.py", body)
    rule = build({"roots": ["tests"]}, repo_root=tmp_path)

    assert rule.run() == 1


def test_reasoned_from_import_skip_mark_is_clean(tmp_path: Path) -> None:
    body = "from pytest import mark as pm, importorskip as optional\n"
    body += "pytestmark: object = [pm.skipif(True, reason='unsupported runtime')]\n"
    body += "module = optional('optional_dep', reason='not installed')\n"
    _seed(tmp_path, "tests/test_from_import_clean.py", body)
    rule = build({"roots": ["tests"]}, repo_root=tmp_path)

    assert rule.run() == 0


def test_empty_reason_skip_marker_is_rejected(tmp_path: Path) -> None:
    body = "import pytest\n@pytest.mark.skipif(True, reason='')\ndef test_a():\n    pass\n"
    _seed(tmp_path, "tests/test_empty_reason.py", body)
    rule = build({"roots": ["tests"], "importorskip_lookback": 0}, repo_root=tmp_path)

    assert rule.run() == 1


def test_expression_importorskip_without_reason_is_rejected(tmp_path: Path) -> None:
    _seed(tmp_path, "tests/test_expr_import.py", "import pytest\npytest.importorskip('optional_dep')\n")
    rule = build({"roots": ["tests"], "importorskip_lookback": 0}, repo_root=tmp_path)

    assert rule.run() == 1


def test_reasoned_standalone_importorskip_is_clean(tmp_path: Path) -> None:
    body = "import pytest\npytest.importorskip('optional_dep', reason='not installed')\n"
    _seed(tmp_path, "tests/test_standalone_import.py", body)
    rule = build({"roots": ["tests"]}, repo_root=tmp_path)

    assert rule.run() == 0


def test_unrelated_pytest_mark_does_not_require_skip_reason(tmp_path: Path) -> None:
    body = "import pytest\n@pytest.mark.slow\ndef test_long_job():\n    pass\n"
    _seed(tmp_path, "tests/test_non_skip_mark.py", body)
    rule = build({"roots": ["tests"]}, repo_root=tmp_path)

    assert rule.run() == 0


def test_tuple_pytestmark_with_undocumented_skip_is_rejected(tmp_path: Path) -> None:
    body = "import pytest\npytestmark = (pytest.mark.skip, pytest.mark.slow)\n"
    _seed(tmp_path, "tests/test_tuple_mark.py", body)
    rule = build({"roots": ["tests"]}, repo_root=tmp_path)

    assert rule.run() == 1


def test_single_pytestmark_with_undocumented_skip_is_rejected(tmp_path: Path) -> None:
    body = "import pytest\npytestmark = pytest.mark.skip\n"
    _seed(tmp_path, "tests/test_single_mark.py", body)
    rule = build({"roots": ["tests"]}, repo_root=tmp_path)

    assert rule.run() == 1


def test_pytestmark_annotation_without_value_is_clean(tmp_path: Path) -> None:
    _seed(tmp_path, "tests/test_annotated_empty.py", "pytestmark: object\n")
    rule = build({"roots": ["tests"]}, repo_root=tmp_path)

    assert rule.run() == 0


def test_same_line_importorskip_comment_is_accepted(tmp_path: Path) -> None:
    body = "import pytest\noptional = pytest.importorskip('optional_dep')  # optional integration\n"
    _seed(tmp_path, "tests/test_inline_importorskip.py", body)
    rule = build({"roots": ["tests"]}, repo_root=tmp_path)

    assert rule.run() == 0


def test_empty_same_line_importorskip_comment_does_not_explain_skip(tmp_path: Path) -> None:
    body = "import pytest\noptional = pytest.importorskip('optional_dep')  #\n"
    _seed(tmp_path, "tests/test_empty_inline_importorskip.py", body)
    rule = build({"roots": ["tests"], "importorskip_lookback": 0}, repo_root=tmp_path)

    assert rule.run() == 1


def test_non_comment_lookback_does_not_explain_importorskip(tmp_path: Path) -> None:
    body = "from pytest import importorskip\nvalue = True\nmodule = importorskip('optional_dep')\n"
    _seed(tmp_path, "tests/test_unexplained_importorskip.py", body)
    rule = build({"roots": ["tests"], "importorskip_lookback": 5}, repo_root=tmp_path)

    assert rule.run() == 1


def test_rule_from_config_scopes_roots(tmp_path: Path) -> None:
    _seed(tmp_path, "tests/test_a.py", _BARE_SKIP)
    _seed(tmp_path, "vendor/test_b.py", _BARE_SKIP)
    rule = TestSkipRationale.from_config({"roots": ["tests"]}, repo_root=tmp_path)
    assert {str(p) for p in rule.collect_violations()} == {"tests/test_a.py"}


def test_build_returns_rule() -> None:
    assert isinstance(build({}), TestSkipRationale)


def test_no_repo_strings_in_executable_code() -> None:
    import tc_fitness.core_checks.test_skip_rationale as mod

    assert_no_repo_identity(mod.__file__)
