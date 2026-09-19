"""Tests for the CORE check no_internal_monkeypatch (v0.6.0)."""

from __future__ import annotations

from pathlib import Path

import pytest
from _core_check_assertions import assert_no_repo_identity

from tc_fitness.core_checks.no_internal_monkeypatch import (
    NoInternalMonkeypatch,
    build,
    file_has_internal_patch,
)

pytestmark = pytest.mark.integration

_PATCH_DECORATOR = """
from unittest.mock import patch

@patch("myapp.core.search.run")
def test_x(mock_run):
    assert True
"""

_PATCH_STDLIB = """
from unittest.mock import patch

@patch("os.environ")
def test_x(mock_env):
    assert True
"""

_MONKEYPATCH_REF = """
import myapp.paths as paths_mod

def test_x(monkeypatch):
    monkeypatch.setattr(paths_mod, "provider_name", lambda: "fake")
"""

_FROZEN_RAISES = """
import pytest
import myapp.config as cfg

def test_x():
    with pytest.raises(Exception):
        cfg.value = 3
"""

_PKGS = ("myapp",)
_EXEMPT = frozenset({"os", "sys", "httpx"})


def _seed(tmp_path: Path, rel: str, body: str) -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


def test_patch_decorator_on_internal_flagged(tmp_path: Path) -> None:
    p = _seed(tmp_path, "test_x.py", _PATCH_DECORATOR)
    assert file_has_internal_patch(p, internal_packages=_PKGS, exempt_roots=_EXEMPT) is True


def test_patch_on_stdlib_exempt(tmp_path: Path) -> None:
    p = _seed(tmp_path, "test_x.py", _PATCH_STDLIB)
    assert file_has_internal_patch(p, internal_packages=_PKGS, exempt_roots=_EXEMPT) is False


def test_monkeypatch_setattr_ref_flagged(tmp_path: Path) -> None:
    p = _seed(tmp_path, "test_x.py", _MONKEYPATCH_REF)
    assert file_has_internal_patch(p, internal_packages=_PKGS, exempt_roots=_EXEMPT) is True


def test_assignment_in_pytest_raises_is_exempt(tmp_path: Path) -> None:
    p = _seed(tmp_path, "test_x.py", _FROZEN_RAISES)
    assert file_has_internal_patch(p, internal_packages=_PKGS, exempt_roots=_EXEMPT) is False


def test_direct_internal_assignment_is_flagged_outside_raises(tmp_path: Path) -> None:
    p = _seed(
        tmp_path,
        "test_x.py",
        "import myapp.core.search\nmyapp.core.search.run = fake_run\n",
    )

    assert file_has_internal_patch(p, internal_packages=_PKGS, exempt_roots=_EXEMPT) is True


def test_patch_context_and_attribute_patch_decorator_are_detected(tmp_path: Path) -> None:
    context = _seed(
        tmp_path,
        "context.py",
        "from unittest.mock import patch\n\n"
        "def test_x():\n    with patch('myapp.core.search.run'):\n        pass\n",
    )
    decorator = _seed(
        tmp_path,
        "decorator.py",
        "import unittest.mock as mock\n\n@mock.patch('myapp.core.search.run')\ndef test_x():\n    pass\n",
    )

    assert file_has_internal_patch(context, internal_packages=_PKGS, exempt_roots=_EXEMPT) is True
    assert file_has_internal_patch(decorator, internal_packages=_PKGS, exempt_roots=_EXEMPT) is True


def test_import_aliases_and_string_target_monkeypatch_are_detected(tmp_path: Path) -> None:
    from_import = _seed(
        tmp_path,
        "from_import.py",
        "from myapp.paths import provider as paths_mod\npaths_mod.provider_name = fake_provider\n",
    )
    string_target = _seed(
        tmp_path,
        "string_target.py",
        "def test_x(monkeypatch):\n    monkeypatch.setattr('myapp.paths.provider_name', fake_provider)\n",
    )

    assert file_has_internal_patch(from_import, internal_packages=_PKGS, exempt_roots=_EXEMPT) is True
    assert file_has_internal_patch(string_target, internal_packages=_PKGS, exempt_roots=_EXEMPT) is True


def test_unreadable_sources_and_external_aliases_are_ignored(tmp_path: Path) -> None:
    syntax = _seed(tmp_path, "syntax.py", "value = (\n")
    binary = tmp_path / "binary.py"
    binary.write_bytes(b"import myapp.core\n\xff")
    external = _seed(
        tmp_path,
        "external.py",
        "import httpx as client\nclient.post = fake_post\n",
    )

    assert (
        file_has_internal_patch(tmp_path / "missing.py", internal_packages=_PKGS, exempt_roots=_EXEMPT)
        is False
    )
    assert file_has_internal_patch(syntax, internal_packages=_PKGS, exempt_roots=_EXEMPT) is False
    assert file_has_internal_patch(binary, internal_packages=_PKGS, exempt_roots=_EXEMPT) is False
    assert file_has_internal_patch(external, internal_packages=_PKGS, exempt_roots=_EXEMPT) is False


def test_package_root_and_imported_raises_context_are_recognised(tmp_path: Path) -> None:
    package_root = _seed(
        tmp_path,
        "root.py",
        "import myapp\ndef test_x(monkeypatch):\n    monkeypatch.setattr(myapp, 'client', fake_client)\n",
    )
    raises_context = _seed(
        tmp_path,
        "raises.py",
        "from pytest import raises\nimport myapp\n\ndef test_x():\n"
        "    with raises(RuntimeError):\n        myapp.client = 1\n",
    )

    assert file_has_internal_patch(package_root, internal_packages=_PKGS, exempt_roots=_EXEMPT) is True
    assert file_has_internal_patch(raises_context, internal_packages=_PKGS, exempt_roots=_EXEMPT) is False


def test_dynamic_and_exempt_monkeypatch_targets_are_not_classified_internal(tmp_path: Path) -> None:
    dynamic_attribute = _seed(
        tmp_path,
        "dynamic_attribute.py",
        "def test_x(monkeypatch):\n    monkeypatch.setattr(resolve_module().client, 'send', fake_send)\n",
    )
    dynamic_value = _seed(
        tmp_path,
        "dynamic_value.py",
        "def test_x(monkeypatch):\n    monkeypatch.setattr(resolve_target(), 'send', fake_send)\n",
    )
    exempt = _seed(
        tmp_path,
        "exempt.py",
        "import httpx\ndef test_x(monkeypatch):\n    monkeypatch.setattr(httpx, 'get', fake_get)\n",
    )
    no_target = _seed(tmp_path, "no_target.py", "def test_x(monkeypatch):\n    monkeypatch.setattr()\n")

    assert file_has_internal_patch(dynamic_attribute, internal_packages=_PKGS, exempt_roots=_EXEMPT) is False
    assert file_has_internal_patch(dynamic_value, internal_packages=_PKGS, exempt_roots=_EXEMPT) is False
    assert file_has_internal_patch(exempt, internal_packages=_PKGS, exempt_roots=_EXEMPT) is False
    assert file_has_internal_patch(no_target, internal_packages=_PKGS, exempt_roots=_EXEMPT) is False


def test_bare_patch_decorator_without_a_target_is_not_a_mock(tmp_path: Path) -> None:
    p = _seed(
        tmp_path,
        "bare.py",
        "from unittest.mock import patch\n\n@patch\ndef test_x():\n    pass\n",
    )

    assert file_has_internal_patch(p, internal_packages=_PKGS, exempt_roots=_EXEMPT) is False


def test_only_exception_assertion_context_exempts_internal_assignment(tmp_path: Path) -> None:
    direct_external = _seed(
        tmp_path,
        "direct_external.py",
        "import httpx\ndef test_x(monkeypatch):\n    monkeypatch.setattr(httpx, 'get', fake_get)\n",
    )
    unrelated_context = _seed(
        tmp_path,
        "unrelated_context.py",
        "from contextlib import nullcontext\nimport myapp\n\n"
        "def test_x():\n    with nullcontext():\n        myapp.client = 3\n",
    )
    patch_object = _seed(
        tmp_path,
        "patch_object.py",
        "from unittest.mock import patch\nimport os\n\n"
        "def test_x():\n    with patch.object(os, 'environ'):\n        pass\n",
    )

    assert file_has_internal_patch(direct_external, internal_packages=_PKGS, exempt_roots=_EXEMPT) is False
    assert file_has_internal_patch(unrelated_context, internal_packages=_PKGS, exempt_roots=_EXEMPT) is True
    assert file_has_internal_patch(patch_object, internal_packages=_PKGS, exempt_roots=_EXEMPT) is False


def test_no_internal_packages_matches_nothing(tmp_path: Path) -> None:
    p = _seed(tmp_path, "test_x.py", _PATCH_DECORATOR)
    assert file_has_internal_patch(p, internal_packages=(), exempt_roots=_EXEMPT) is False


def test_packages_are_config_driven(tmp_path: Path) -> None:
    _seed(tmp_path, "tests/test_x.py", _PATCH_DECORATOR)
    rule = NoInternalMonkeypatch.from_config(
        {"roots": ["tests"], "internal_packages": ["myapp"], "exempt_roots": ["os"]},
        repo_root=tmp_path,
    )
    assert {str(p) for p in rule.collect_violations()} == {"tests/test_x.py"}


def test_build_returns_rule() -> None:
    assert isinstance(build({}), NoInternalMonkeypatch)


def test_no_repo_strings_in_executable_code() -> None:
    import tc_fitness.core_checks.no_internal_monkeypatch as mod

    assert_no_repo_identity(mod.__file__)
