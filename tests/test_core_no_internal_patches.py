"""Tests for the CORE check no_internal_patches (v0.6.0 security-freshness batch)."""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

import pytest

from tc_fitness.core_checks.no_internal_patches import (
    NoInternalPatches,
    build,
    file_patches_internal,
    main,
)

pytestmark = pytest.mark.integration

_INTERNAL = frozenset({"scripts", "tools"})
_EXEMPT = frozenset({"os", "subprocess", "pytest"})


def _seed(tmp_path: Path, rel: str, body: str) -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


def test_flags_monkeypatch_string_target(tmp_path: Path) -> None:
    p = _seed(tmp_path, "t.py", "def test_x(monkeypatch):\n    monkeypatch.setattr('scripts.a.b', 1)\n")
    assert file_patches_internal(p, internal_roots=_INTERNAL, exempt_roots=_EXEMPT) is True


def test_flags_patch_decorator(tmp_path: Path) -> None:
    p = _seed(
        tmp_path, "t.py", "from unittest.mock import patch\n@patch('tools.x.y')\ndef test_x():\n    pass\n"
    )
    assert file_patches_internal(p, internal_roots=_INTERNAL, exempt_roots=_EXEMPT) is True


def test_stdlib_boundary_is_clean(tmp_path: Path) -> None:
    p = _seed(tmp_path, "t.py", "def test_x(monkeypatch):\n    monkeypatch.setattr('os.environ', {})\n")
    assert file_patches_internal(p, internal_roots=_INTERNAL, exempt_roots=_EXEMPT) is False


def test_pytest_raises_assign_not_flagged(tmp_path: Path) -> None:
    body = "import scripts\ndef test_x():\n    with pytest.raises(ValueError):\n        scripts.attr = 1\n"
    p = _seed(tmp_path, "t.py", body)
    assert file_patches_internal(p, internal_roots=_INTERNAL, exempt_roots=_EXEMPT) is False


@pytest.mark.parametrize(
    "body",
    [
        "import scripts.worker as worker\ndef test_x():\n    worker.value = 1\n",
        "from tools import worker as local\ndef test_x():\n    local.value = 1\n",
        "from unittest.mock import patch\n@patch('scripts.worker.value')\ndef test_x(): pass\n",
        "from unittest.mock import patch\ndef test_x():\n    with patch('tools.worker.value'):\n        pass\n",
        "module = _load()\ndef test_x(monkeypatch):\n    monkeypatch.setattr(module, 'value', 1)\n",
    ],
)
def test_flags_import_alias_dynamic_loader_and_context_patch_shapes(tmp_path: Path, body: str) -> None:
    assert (
        file_patches_internal(
            _seed(tmp_path, "tests/test_boundary.py", body),
            internal_roots=_INTERNAL,
            exempt_roots=_EXEMPT,
        )
        is True
    )


@pytest.mark.parametrize(
    "body",
    [
        "from unittest.mock import patch\n@patch('requests.get')\ndef test_x(): pass\n",
        "import os\ndef test_x():\n    os.environ = {}\n",
        "import scripts\ndef test_x():\n    with raises(ValueError):\n        scripts.value = 1\n",
        "def test_x(monkeypatch):\n    monkeypatch.setattr('requests.get', lambda: None)\n",
    ],
)
def test_allows_exempt_or_exception_assertion_shapes(tmp_path: Path, body: str) -> None:
    assert (
        file_patches_internal(
            _seed(tmp_path, "tests/test_boundary.py", body),
            internal_roots=_INTERNAL,
            exempt_roots=_EXEMPT,
        )
        is False
    )


@pytest.mark.parametrize(
    "body",
    [
        "import scripts\nmodule = 1\ndef test_x(monkeypatch):\n    monkeypatch.setattr(module, 'value', 1)\n",
        "from unittest.mock import patch\n@patch()\ndef test_x(): pass\n",
        "from unittest.mock import patch\n@patch\ndef test_x(): pass\n",
        "def test_x(monkeypatch):\n    monkeypatch.setattr(requests.api, 'get', None)\n",
        "def test_x(monkeypatch):\n    monkeypatch.setattr(factory().module, 'value', 1)\n",
        "import scripts\ndef test_x():\n    with pytest.raises(ValueError):\n        scripts.value = 1\n",
        "import os\ndef test_x():\n    with scripts.context:\n        os.environ = {}\n",
    ],
)
def test_unresolved_or_non_patch_shapes_remain_clean(tmp_path: Path, body: str) -> None:
    assert not file_patches_internal(
        _seed(tmp_path, "tests/test_boundary.py", body),
        internal_roots=_INTERNAL,
        exempt_roots=_EXEMPT,
    )


@pytest.mark.parametrize(
    "body",
    [
        "import importlib.util\nmodule = importlib.util.module_from_spec(spec)\n"
        "def test_x(monkeypatch):\n    monkeypatch.setattr(module, 'value', 1)\n",
        "import mock\n@mock.patch('scripts.worker.value')\ndef test_x(): pass\n",
        "import scripts\ndef test_x():\n    with object():\n        scripts.value = 1\n",
    ],
)
def test_flags_dynamic_module_load_attribute_patch_and_non_assertion_contexts(
    tmp_path: Path, body: str
) -> None:
    assert file_patches_internal(
        _seed(tmp_path, "tests/test_boundary.py", body),
        internal_roots=_INTERNAL,
        exempt_roots=_EXEMPT,
    )


def test_assignments_from_unrecognised_call_and_non_patch_decorator_stay_clean(tmp_path: Path) -> None:
    body = (
        "module = loader()\n"
        "@mock.decorator('scripts.worker.value')\n"
        "def test_x(monkeypatch):\n    monkeypatch.setattr(module, 'value', 1)\n"
    )
    assert not file_patches_internal(
        _seed(tmp_path, "tests/test_boundary.py", body),
        internal_roots=_INTERNAL,
        exempt_roots=_EXEMPT,
    )


def test_non_callable_ast_decorator_factory_is_not_a_patch_call(tmp_path: Path) -> None:
    body = "@build_decorator[0]('scripts.worker.value')\ndef test_x(): pass\n"
    assert not file_patches_internal(
        _seed(tmp_path, "tests/test_boundary.py", body),
        internal_roots=_INTERNAL,
        exempt_roots=_EXEMPT,
    )


def test_tuple_assignment_from_dynamic_module_load_is_not_mistaken_for_a_module(tmp_path: Path) -> None:
    body = "module, other = _load()\ndef test_x(monkeypatch):\n    monkeypatch.setattr(other, 'value', 1)\n"
    assert not file_patches_internal(
        _seed(tmp_path, "tests/test_boundary.py", body),
        internal_roots=_INTERNAL,
        exempt_roots=_EXEMPT,
    )


def test_invalid_syntax_and_missing_candidate_are_not_substitution_findings(tmp_path: Path) -> None:
    invalid = _seed(tmp_path, "tests/invalid.py", "def test_x(:\n")
    missing = tmp_path / "tests" / "missing.py"
    assert not file_patches_internal(invalid, internal_roots=_INTERNAL, exempt_roots=_EXEMPT)
    assert not file_patches_internal(missing, internal_roots=_INTERNAL, exempt_roots=_EXEMPT)


def test_unreadable_candidate_is_not_a_substitution_finding(tmp_path: Path) -> None:
    path = tmp_path / "tests" / "invalid.py"
    path.parent.mkdir()
    path.write_bytes(b"\xff")
    assert file_patches_internal(path, internal_roots=_INTERNAL, exempt_roots=_EXEMPT) is False


def test_empty_internal_roots_is_noop(tmp_path: Path) -> None:
    rule = build({"roots": ["."]}, repo_root=tmp_path)
    p = _seed(tmp_path, "t.py", "def test_x(monkeypatch):\n    monkeypatch.setattr('scripts.a.b', 1)\n")
    assert rule.file_has_violation(p) is False


def test_config_scopes_internal_roots(tmp_path: Path) -> None:
    rule = build(
        {"roots": ["tests"], "internal_roots": ["scripts"], "exempt_roots": ["os"]}, repo_root=tmp_path
    )
    _seed(tmp_path, "tests/t.py", "def test_x(monkeypatch):\n    monkeypatch.setattr('scripts.a.b', 1)\n")
    assert {str(x) for x in rule.collect_violations()} == {"tests/t.py"}


def test_run_fails_then_establish_grandfathers(tmp_path: Path) -> None:
    _seed(tmp_path, "tests/t.py", "def test_x(monkeypatch):\n    monkeypatch.setattr('scripts.a.b', 1)\n")
    rule = NoInternalPatches.from_config(
        {"roots": ["tests"], "internal_roots": ["scripts"]}, repo_root=tmp_path
    )
    assert rule.run() == 1
    rule.establish_baseline()
    assert rule.run() == 0


def test_main_establish_baseline_mode(tmp_path: Path) -> None:
    _seed(tmp_path, "t.py", "def test_x(monkeypatch):\n    monkeypatch.setattr('scripts.a.b', 1)\n")
    # internal_roots empty by default → no violations; establish writes empty baseline.
    rc = main(["--establish-baseline", "--repo-root", str(tmp_path)])
    assert rc == 0
    assert (tmp_path / ".architecture" / "baseline" / "no-internal-patches-files.txt").exists()


def test_module_entrypoint_accepts_repository_root(tmp_path: Path) -> None:
    import tc_fitness.core_checks.no_internal_patches as module

    original_argv = sys.argv
    sys.argv = ["no_internal_patches", "--repo-root", str(tmp_path)]
    try:
        with pytest.raises(SystemExit) as result:
            runpy.run_path(str(Path(module.__file__)), run_name="__main__")
    finally:
        sys.argv = original_argv
    assert result.value.code == 0
