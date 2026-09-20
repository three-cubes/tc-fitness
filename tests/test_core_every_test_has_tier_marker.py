"""Tests for the CORE check every_test_has_tier_marker (v0.6.0)."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest
from _core_check_assertions import assert_no_repo_identity

from tc_fitness.core_checks.every_test_has_tier_marker import (
    EveryTestHasTierMarker,
    build,
    file_missing_tier_marker,
    main,
)

pytestmark = pytest.mark.integration

_UNTAGGED = """
def test_parser() -> None:
    assert True
"""

_MODULE_MARKER = """
import pytest

pytestmark = pytest.mark.unit

def test_parser() -> None:
    assert True
"""

_FUNCTION_MARKER = """
import pytest

@pytest.mark.contract
def test_parser() -> None:
    assert True
"""

_MODULE_AND_FUNCTION_MARKER = """
import pytest

pytestmark = pytest.mark.unit

@pytest.mark.integration
def test_parser() -> None:
    assert True
"""

_REASSIGNED_MODULE_MARKER = """
import pytest

pytestmark = pytest.mark.unit
pytestmark = [pytest.mark.unit, pytest.mark.integration]

def test_parser() -> None:
    assert True
"""

_REPEATED_MODULE_MARKER = """
import pytest

pytestmark = pytest.mark.unit
pytestmark = pytest.mark.unit

def test_parser() -> None:
    assert True
"""

_CONDITIONAL_AUGMENTATION = """
import pytest

pytestmark = pytest.mark.unit
if True:
    pytestmark += [pytest.mark.integration]

def test_parser() -> None:
    assert True
"""

_UNPACKED_REASSIGNMENT = """
import pytest

pytestmark = pytest.mark.unit
pytestmark, other = pytest.mark.unit, pytest.mark.integration

def test_parser() -> None:
    assert True
"""

_PYTESTMARK_MUTATION = """
import pytest

pytestmark = [pytest.mark.unit]
pytestmark.append(pytest.mark.integration)

def test_parser() -> None:
    assert True
"""

_STARRED_TIER_EXPRESSION = """
import pytest

pytestmark = [pytest.mark.unit, *[pytest.mark.integration]]

def test_parser() -> None:
    assert True
"""

_ALIASED_TIER_EXPRESSION = """
import pytest

other = pytest.mark.integration
pytestmark = [pytest.mark.unit, other]

def test_parser() -> None:
    assert True
"""

_CLASS_TIER_DECORATOR = """
import pytest

pytestmark = pytest.mark.unit

@pytest.mark.integration
class TestParser:
    def test_parser(self) -> None:
        assert True
"""

_CLASS_TIER_DECLARATION = """
import pytest

pytestmark = pytest.mark.unit

class TestParser:
    pytestmark = pytest.mark.integration

    def test_parser(self) -> None:
        assert True
"""

_TIER_ALIAS_DECORATOR = """
import pytest

pytestmark = pytest.mark.unit
tier = pytest.mark.integration

@tier
def test_parser() -> None:
    assert True
"""

_PYTEST_PARAM_TIER_MARK = """
import pytest

pytestmark = pytest.mark.unit
tier = pytest.mark.integration

@pytest.mark.parametrize("value", [pytest.param(1, marks=tier)])
def test_parser(value: int) -> None:
    assert value == 1
"""

_FUNCTION_PYTESTMARK_MUTATION = """
import pytest

pytestmark = pytest.mark.unit

def test_parser() -> None:
    assert True

test_parser.pytestmark = pytest.mark.integration
"""

_POST_DEFINITION_DECORATION = """
import pytest

pytestmark = pytest.mark.unit

def test_parser() -> None:
    assert True

test_parser = pytest.mark.integration(test_parser)
"""

_NAMED_EXPRESSION_BINDING = """
import pytest

pytestmark = pytest.mark.unit
if (pytestmark := pytest.mark.integration):
    pass

def test_parser() -> None:
    assert True
"""

_FOR_LOOP_BINDING = """
import pytest

pytestmark = pytest.mark.unit
for pytestmark in [pytest.mark.integration]:
    pass

def test_parser() -> None:
    assert True
"""

_OTHER_PYTESTMARK_BINDINGS = {
    "function-parameter": """
import pytest

pytestmark = pytest.mark.unit

def helper(pytestmark: object) -> object:
    return pytestmark

def test_parser() -> None:
    assert True
""",
    "definition-name": """
import pytest

pytestmark = pytest.mark.unit

def pytestmark() -> None:
    pass

def test_parser() -> None:
    assert True
""",
    "import-alias": """
import math as pytestmark
import pytest

pytestmark = pytest.mark.unit

def test_parser() -> None:
    assert True
""",
    "with-target": """
from contextlib import nullcontext
import pytest

pytestmark = pytest.mark.unit

with nullcontext() as pytestmark:
    pass

def test_parser() -> None:
    assert True
""",
    "except-target": """
import pytest

pytestmark = pytest.mark.unit

try:
    raise RuntimeError
except RuntimeError as pytestmark:
    pass

def test_parser() -> None:
    assert True
""",
    "match-capture": """
import pytest

pytestmark = pytest.mark.unit

match 1:
    case pytestmark:
        pass

def test_parser() -> None:
    assert True
""",
    "comprehension-target": """
import pytest

pytestmark = pytest.mark.unit
values = [pytestmark for pytestmark in range(1)]

def test_parser() -> None:
    assert True
""",
    "delete-target": """
import pytest

pytestmark = pytest.mark.unit
del pytestmark

def test_parser() -> None:
    assert True
""",
    "mapping-rest-capture": """
import pytest

pytestmark = pytest.mark.unit
match {}:
    case {**pytestmark}:
        pass

def test_parser() -> None:
    assert True
""",
}

_REUSED_OR_ALIASED_MARKERS = {
    "bare-decorator": "@pytestmark\ndef test_parser(): pass\n",
    "parameter-marker": (
        '@pytest.mark.parametrize("value", [pytest.param(1, marks=pytestmark)])\n'
        "def test_parser(value): pass\n"
    ),
    "import-mark": "from pytest import mark\n@mark.integration\ndef test_parser(): pass\n",
    "import-pytest-alias": "import pytest as pt\n@pt.mark.integration\ndef test_parser(): pass\n",
    "copy-mark": "mark = pytest.mark\n@mark.integration\ndef test_parser(): pass\n",
    "copy-pytest": "pt = pytest\n@pt.mark.integration\ndef test_parser(): pass\n",
    "getattr-mark": 'mark = getattr(pytest, "mark")\n@mark.integration\ndef test_parser(): pass\n',
    "post-definition-alias": (
        "from pytest import mark\ndef test_parser(): pass\ntest_parser = mark.integration(test_parser)\n"
    ),
}

_PYTEST_CONFIG = """[pytest]
markers =
    unit: unit tier
    contract: contract tier
    integration: integration tier
    e2e: e2e tier
"""

_NO_TESTS = """
import pytest

@pytest.fixture
def thing() -> int:
    return 1
"""

_TIERS = frozenset({"unit", "contract", "e2e"})


def _seed(tmp_path: Path, rel: str, body: str) -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


def _collect_tiers(tmp_path: Path, body: str, *args: str) -> subprocess.CompletedProcess[str]:
    """Exercise the shipped plugin in real pytest, never a synthetic item."""
    _seed(tmp_path, "pytest.ini", _PYTEST_CONFIG)
    _seed(tmp_path, "test_subject.py", body)
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "--collect-only",
            "--strict-markers",
            "-q",
            "-p",
            "tc_fitness.pytest_tiers",
            *args,
        ],
        check=False,
        capture_output=True,
        text=True,
        cwd=tmp_path,
        env=os.environ | {"PYTEST_ADDOPTS": "", "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1"},
        timeout=30,
    )


def _assert_canonical_rule_and_collection_reject(
    tmp_path: Path,
    body: str,
    *,
    expected_collection_exit: int = 0,
) -> None:
    path = _seed(tmp_path, "tests/test_x.py", body)
    _seed(tmp_path, "pytest.ini", _PYTEST_CONFIG)
    rule = EveryTestHasTierMarker.from_config(
        {"roots": ["tests"], "require_module_marker": True}, repo_root=tmp_path
    )
    assert rule.run() == 1
    collection = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "--strict-markers", "-q", str(path)],
        check=False,
        capture_output=True,
        text=True,
        cwd=tmp_path,
        env=os.environ | {"PYTEST_ADDOPTS": "", "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1"},
        timeout=30,
    )
    assert collection.returncode == expected_collection_exit, collection.stdout + collection.stderr


def test_untagged_is_violation(tmp_path: Path) -> None:
    p = _seed(tmp_path, "test_x.py", _UNTAGGED)
    assert file_missing_tier_marker(p, tiers=_TIERS) is True


def test_module_marker_passes(tmp_path: Path) -> None:
    p = _seed(tmp_path, "test_x.py", _MODULE_MARKER)
    assert file_missing_tier_marker(p, tiers=_TIERS) is False


def test_function_marker_passes(tmp_path: Path) -> None:
    p = _seed(tmp_path, "test_x.py", _FUNCTION_MARKER)
    assert file_missing_tier_marker(p, tiers=_TIERS) is False


def test_canonical_mode_rejects_function_only_module(tmp_path: Path) -> None:
    _seed(tmp_path, "tests/test_x.py", _FUNCTION_MARKER)
    rule = EveryTestHasTierMarker.from_config(
        {"roots": ["tests"], "require_module_marker": True}, repo_root=tmp_path
    )
    assert rule.collect_violations() == {Path("tests/test_x.py")}


def test_canonical_mode_rejects_module_and_function_tiers(tmp_path: Path) -> None:
    _seed(tmp_path, "tests/test_x.py", _MODULE_AND_FUNCTION_MARKER)
    rule = EveryTestHasTierMarker.from_config(
        {"roots": ["tests"], "require_module_marker": True}, repo_root=tmp_path
    )
    assert rule.collect_violations() == {Path("tests/test_x.py")}


def test_canonical_mode_rejects_reassigned_module_markers(tmp_path: Path) -> None:
    _seed(tmp_path, "tests/test_x.py", _REASSIGNED_MODULE_MARKER)
    rule = EveryTestHasTierMarker.from_config(
        {"roots": ["tests"], "require_module_marker": True}, repo_root=tmp_path
    )
    assert rule.collect_violations() == {Path("tests/test_x.py")}


def test_canonical_mode_rejects_repeated_module_markers(tmp_path: Path) -> None:
    _seed(tmp_path, "tests/test_x.py", _REPEATED_MODULE_MARKER)
    rule = EveryTestHasTierMarker.from_config(
        {"roots": ["tests"], "require_module_marker": True}, repo_root=tmp_path
    )
    assert rule.collect_violations() == {Path("tests/test_x.py")}


def test_canonical_mode_rejects_conditional_augmentation(tmp_path: Path) -> None:
    _assert_canonical_rule_and_collection_reject(
        tmp_path, _CONDITIONAL_AUGMENTATION, expected_collection_exit=2
    )


def test_canonical_mode_rejects_unpacked_reassignment(tmp_path: Path) -> None:
    _assert_canonical_rule_and_collection_reject(tmp_path, _UNPACKED_REASSIGNMENT)


def test_canonical_mode_rejects_pytestmark_mutation(tmp_path: Path) -> None:
    _assert_canonical_rule_and_collection_reject(tmp_path, _PYTESTMARK_MUTATION)


def test_canonical_mode_rejects_starred_tier_expression(tmp_path: Path) -> None:
    _assert_canonical_rule_and_collection_reject(tmp_path, _STARRED_TIER_EXPRESSION)


def test_canonical_mode_rejects_aliased_tier_expression(tmp_path: Path) -> None:
    _assert_canonical_rule_and_collection_reject(tmp_path, _ALIASED_TIER_EXPRESSION)


def test_canonical_mode_rejects_class_tier_decorator(tmp_path: Path) -> None:
    _assert_canonical_rule_and_collection_reject(tmp_path, _CLASS_TIER_DECORATOR)


def test_canonical_mode_rejects_class_tier_declaration(tmp_path: Path) -> None:
    _assert_canonical_rule_and_collection_reject(tmp_path, _CLASS_TIER_DECLARATION)


def test_canonical_mode_rejects_tier_alias_decorator(tmp_path: Path) -> None:
    _assert_canonical_rule_and_collection_reject(tmp_path, _TIER_ALIAS_DECORATOR)


def test_canonical_mode_rejects_pytest_param_tier_mark(tmp_path: Path) -> None:
    _assert_canonical_rule_and_collection_reject(tmp_path, _PYTEST_PARAM_TIER_MARK)


def test_canonical_mode_rejects_function_pytestmark_mutation(tmp_path: Path) -> None:
    _assert_canonical_rule_and_collection_reject(tmp_path, _FUNCTION_PYTESTMARK_MUTATION)


def test_canonical_mode_rejects_post_definition_decoration(tmp_path: Path) -> None:
    _assert_canonical_rule_and_collection_reject(tmp_path, _POST_DEFINITION_DECORATION)


def test_canonical_mode_rejects_named_expression_binding(tmp_path: Path) -> None:
    _assert_canonical_rule_and_collection_reject(tmp_path, _NAMED_EXPRESSION_BINDING)


def test_canonical_mode_rejects_for_loop_binding(tmp_path: Path) -> None:
    _assert_canonical_rule_and_collection_reject(tmp_path, _FOR_LOOP_BINDING)


@pytest.mark.parametrize("body", _OTHER_PYTESTMARK_BINDINGS.values(), ids=_OTHER_PYTESTMARK_BINDINGS)
def test_canonical_mode_rejects_other_pytestmark_binding_contexts(tmp_path: Path, body: str) -> None:
    path = _seed(tmp_path, "tests/test_x.py", body)
    rule = EveryTestHasTierMarker.from_config(
        {"roots": ["tests"], "require_module_marker": True}, repo_root=tmp_path
    )
    assert rule.collect_violations() == {path.relative_to(tmp_path)}


def test_file_without_tests_passes(tmp_path: Path) -> None:
    p = _seed(tmp_path, "test_x.py", _NO_TESTS)
    assert file_missing_tier_marker(p, tiers=_TIERS) is False


def test_tier_vocabulary_is_config_driven(tmp_path: Path) -> None:
    body = "import pytest\n\n@pytest.mark.fast\ndef test_x() -> None:\n    assert True\n"
    _seed(tmp_path, "tests/test_x.py", body)
    default = EveryTestHasTierMarker.from_config({"roots": ["tests"]}, repo_root=tmp_path)
    assert {str(p) for p in default.collect_violations()} == {"tests/test_x.py"}
    custom = EveryTestHasTierMarker.from_config(
        {"roots": ["tests"], "tier_markers": ["fast", "slow"]}, repo_root=tmp_path
    )
    assert custom.collect_violations() == set()


@pytest.mark.parametrize(
    "body,markers",
    [
        (_MODULE_AND_FUNCTION_MARKER, ["unit"]),
        (_MODULE_MARKER.replace("pytest.mark.unit", "pytest.mark.fast"), ["fast"]),
    ],
)
def test_generic_vocabulary_cannot_weaken_canonical_mode(
    tmp_path: Path, body: str, markers: list[str]
) -> None:
    path = _seed(tmp_path, "tests/test_x.py", body)
    rule = EveryTestHasTierMarker.from_config(
        {"roots": ["tests"], "tier_markers": markers, "require_module_marker": True}, repo_root=tmp_path
    )
    assert rule.collect_violations() == {path.relative_to(tmp_path)}


def test_scope_skips_non_test_files_and_excluded_parts(tmp_path: Path) -> None:
    _seed(tmp_path, "tests/helpers.py", _UNTAGGED)  # not test_*
    _seed(tmp_path, "tests/fixtures/test_x.py", _UNTAGGED)  # excluded part
    _seed(tmp_path, "tests/test_real.py", _UNTAGGED)
    rule = EveryTestHasTierMarker.from_config({"roots": ["tests"]}, repo_root=tmp_path)
    assert {str(p) for p in rule.collect_violations()} == {"tests/test_real.py"}


def test_run_then_establish_grandfathers(tmp_path: Path) -> None:
    _seed(tmp_path, "tests/test_x.py", _UNTAGGED)
    rule = EveryTestHasTierMarker.from_config({"roots": ["tests"]}, repo_root=tmp_path)
    assert rule.run() == 1
    rule.establish_baseline()
    assert rule.run() == 0


def test_main_establish_baseline_mode(tmp_path: Path) -> None:
    _seed(tmp_path, "test_x.py", _UNTAGGED)
    rc = main(["--establish-baseline", "--repo-root", str(tmp_path)])
    assert rc == 0
    assert (tmp_path / ".architecture" / "baseline" / "every-test-has-tier-marker-files.txt").exists()


def test_build_returns_rule() -> None:
    assert isinstance(build({}), EveryTestHasTierMarker)


def test_repository_tests_are_all_classified_by_tier() -> None:
    rule = EveryTestHasTierMarker.from_config(
        {
            "roots": ["tests"],
            "tier_markers": ["unit", "contract", "integration", "e2e"],
            "require_module_marker": True,
        },
        repo_root=Path(__file__).parent.parent,
    )
    # Self-assurance admits no baseline; ordinary consumer adoption still can.
    assert rule.collect_violations() == set()
    assert rule.run() == 0


def _contract_fixture_manifest(root: Path) -> None:
    _seed(
        root,
        "tests/check_contracts/every_test_has_tier_marker/contract.yaml",
        """schema: tc.fitness/check-contract/v1
check: core:every_test_has_tier_marker
config:
  roots: [tests]
  require_module_marker: true
cases:
  - id: compliant
    fixture: compliant
    expected: {status: pass, exit: zero, findings: []}
  - id: violation
    fixture: violation
    expected:
      status: fail
      exit: nonzero
      findings:
        - rule: every-test-has-tier-marker
          path: tests/test_subject.py
          message_contains: module-level tier
dependencies: []
""",
    )


def test_registered_contract_test_sources_are_data_not_authoring_tests(tmp_path: Path) -> None:
    _contract_fixture_manifest(tmp_path)
    _seed(
        tmp_path,
        "tests/check_contracts/every_test_has_tier_marker/compliant/tests/test_subject.py",
        "import pytest\npytestmark = pytest.mark.unit\ndef test_subject(): pass\n",
    )
    _seed(
        tmp_path,
        "tests/check_contracts/every_test_has_tier_marker/violation/tests/test_subject.py",
        "import pytest\n@pytest.mark.unit\ndef test_subject(): pass\n",
    )
    rule = EveryTestHasTierMarker.from_config(
        {"roots": ["tests"], "require_module_marker": True}, repo_root=tmp_path
    )

    assert rule.collect_violations() == set()


def test_unregistered_check_contracts_directory_cannot_hide_a_test(tmp_path: Path) -> None:
    path = _seed(
        tmp_path,
        "tests/check_contracts/unregistered/test_subject.py",
        "def test_subject(): pass\n",
    )
    rule = EveryTestHasTierMarker.from_config(
        {"roots": ["tests"], "require_module_marker": True}, repo_root=tmp_path
    )

    assert rule.collect_violations() == {path.relative_to(tmp_path)}


def test_copied_contract_manifest_cannot_hide_an_authoring_test(tmp_path: Path) -> None:
    _contract_fixture_manifest(tmp_path)
    manifest = tmp_path / "tests/check_contracts/every_test_has_tier_marker/contract.yaml"
    manifest.write_text(manifest.read_text().replace("core:every_test_has_tier_marker", "core:path_naming"))
    path = _seed(
        tmp_path,
        "tests/check_contracts/every_test_has_tier_marker/violation/tests/test_subject.py",
        "def test_subject(): pass\n",
    )
    rule = EveryTestHasTierMarker.from_config(
        {"roots": ["tests"], "require_module_marker": True}, repo_root=tmp_path
    )

    assert rule.collect_violations() == {path.relative_to(tmp_path)}


@pytest.mark.parametrize("suffix", _REUSED_OR_ALIASED_MARKERS.values(), ids=_REUSED_OR_ALIASED_MARKERS)
def test_canonical_source_rejects_reused_markers_and_namespaces(tmp_path: Path, suffix: str) -> None:
    body = "import pytest\npytestmark = pytest.mark.unit\n" + suffix
    path = _seed(tmp_path, "tests/test_subject.py", body)
    rule = EveryTestHasTierMarker.from_config(
        {"roots": ["tests"], "require_module_marker": True}, repo_root=tmp_path
    )
    assert rule.collect_violations() == {path.relative_to(tmp_path)}


def test_canonical_source_preserves_real_code_attributes(tmp_path: Path) -> None:
    body = """
from types import SimpleNamespace
import pytest
pytestmark = pytest.mark.unit
documents = SimpleNamespace(contract=lambda: 1)
@pytest.mark.parametrize("value", [pytest.param(1, marks=pytest.mark.xfail)])
def test_parser(value):
    assert documents.contract() == value
"""
    path = _seed(tmp_path, "test_subject.py", body)
    assert not file_missing_tier_marker(path, tiers=_TIERS, require_module_marker=True)
    collection = _collect_tiers(tmp_path, body)
    assert collection.returncode == 0, collection.stdout + collection.stderr


@pytest.mark.parametrize("suffix", _REUSED_OR_ALIASED_MARKERS.values(), ids=_REUSED_OR_ALIASED_MARKERS)
def test_runtime_rejects_reused_markers_and_namespaces(tmp_path: Path, suffix: str) -> None:
    collection = _collect_tiers(tmp_path, "import pytest\npytestmark = pytest.mark.unit\n" + suffix)
    assert collection.returncode == 4, collection.stdout + collection.stderr
    assert "test_subject.py::test_parser" in collection.stderr
    assert "exactly one effective tier" in collection.stderr
    expected = "['unit', 'unit']" if "pytestmark" in suffix else "['integration', 'unit']"
    assert expected in collection.stderr


@pytest.mark.parametrize(
    "body",
    [
        _MODULE_AND_FUNCTION_MARKER,
        _REASSIGNED_MODULE_MARKER,
        _UNPACKED_REASSIGNMENT.replace(
            "pytest.mark.unit, pytest.mark.integration", "[pytest.mark.unit, pytest.mark.integration], None"
        ),
        _PYTESTMARK_MUTATION,
        _STARRED_TIER_EXPRESSION,
        _ALIASED_TIER_EXPRESSION,
        _CLASS_TIER_DECORATOR,
        _CLASS_TIER_DECLARATION,
        _TIER_ALIAS_DECORATOR,
        _PYTEST_PARAM_TIER_MARK,
        _FUNCTION_PYTESTMARK_MUTATION,
        _POST_DEFINITION_DECORATION,
    ],
)
def test_runtime_rejects_previous_multiple_tier_controls(tmp_path: Path, body: str) -> None:
    collection = _collect_tiers(tmp_path, body)
    assert collection.returncode == 4, collection.stdout + collection.stderr
    assert "exactly one effective tier" in collection.stderr
    assert "unit" in collection.stderr and "integration" in collection.stderr


def test_runtime_rejects_missing_tier(tmp_path: Path) -> None:
    collection = _collect_tiers(tmp_path, _UNTAGGED)
    assert collection.returncode == 4, collection.stdout + collection.stderr
    assert "test_subject.py::test_parser: []" in collection.stderr


@pytest.mark.parametrize("selection", ["-m", "-k"])
def test_runtime_rejects_invalid_deselected_items(tmp_path: Path, selection: str) -> None:
    collection = _collect_tiers(tmp_path, _MODULE_AND_FUNCTION_MARKER, selection, "contract")
    assert collection.returncode == 4, collection.stdout + collection.stderr
    assert "test_subject.py::test_parser: ['integration', 'unit']" in collection.stderr


def test_runtime_rejects_invalid_item_created_then_deselected_by_collection_hook(tmp_path: Path) -> None:
    _seed(
        tmp_path,
        "conftest.py",
        "import pytest\ndef pytest_collection_modifyitems(config, items):\n"
        "    added = pytest.Function.from_parent(items[0].parent, name='test_hook_added', callobj=lambda: None)\n"
        "    added.add_marker(pytest.mark.contract)\n"
        "    items.append(added)\n"
        "    items.remove(added)\n"
        "    config.hook.pytest_deselected(items=[added])\n",
    )
    collection = _collect_tiers(tmp_path, _MODULE_MARKER)
    assert collection.returncode == 4, collection.stdout + collection.stderr
    assert "test_subject.py::test_hook_added: ['contract', 'unit']" in collection.stderr


def test_runtime_checks_markers_added_by_collection_hooks(tmp_path: Path) -> None:
    _seed(
        tmp_path,
        "conftest.py",
        "import pytest\ndef pytest_collection_modifyitems(items):\n"
        "    for item in items:\n        item.add_marker(pytest.mark.contract)\n",
    )
    collection = _collect_tiers(tmp_path, _MODULE_MARKER)
    assert collection.returncode == 4, collection.stdout + collection.stderr
    assert "test_subject.py::test_parser: ['contract', 'unit']" in collection.stderr


def test_runtime_catches_indirect_marking_beyond_source_grammar(tmp_path: Path) -> None:
    _seed(tmp_path, "helpers.py", "from pytest import mark\ndecorate = mark.integration\n")
    body = "import pytest\nfrom helpers import decorate\npytestmark = pytest.mark.unit\n@decorate\ndef test_parser(): pass\n"
    path = _seed(tmp_path, "test_subject.py", body)
    assert not file_missing_tier_marker(path, tiers=_TIERS, require_module_marker=True)
    collection = _collect_tiers(tmp_path, body)
    assert collection.returncode == 4, collection.stdout + collection.stderr
    assert "test_subject.py::test_parser: ['integration', 'unit']" in collection.stderr


def test_runtime_plugin_does_not_convert_empty_collection_to_pass(tmp_path: Path) -> None:
    collection = _collect_tiers(tmp_path, "import pytest\npytestmark = pytest.mark.unit\n")
    assert collection.returncode == 5, collection.stdout + collection.stderr


def test_no_repo_strings_in_executable_code() -> None:
    import tc_fitness.core_checks.every_test_has_tier_marker as mod

    assert_no_repo_identity(mod.__file__)


def test_a_camelcase_test_function_is_collected_and_must_declare_a_tier(tmp_path: Path) -> None:
    """pytest collects `testThing`, so a module holding only one is not tier-free."""
    module = tmp_path / "tests" / "test_camel.py"
    module.parent.mkdir(parents=True)
    module.write_text("def testThing():\n    assert True\n", encoding="utf-8")

    assert file_missing_tier_marker(module, tiers=frozenset({"unit", "contract", "integration", "e2e"}))
