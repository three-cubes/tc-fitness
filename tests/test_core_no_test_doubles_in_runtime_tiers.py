"""Tests for the CORE check that protects declared runtime test tiers."""

from __future__ import annotations

from pathlib import Path

import pytest
from _core_check_assertions import assert_no_repo_identity

from tc_fitness.core_checks.no_test_doubles_in_runtime_tiers import (
    NoTestDoublesInRuntimeTiers,
    build,
    file_has_runtime_tier_test_double,
)


def _seed(tmp_path: Path, content: str) -> Path:
    path = tmp_path / "test_subject.py"
    path.write_text(content, encoding="utf-8")
    return path


@pytest.mark.integration
def test_rejects_monkeypatch_in_module_marked_runtime_tier(tmp_path: Path) -> None:
    path = _seed(
        tmp_path,
        "import pytest\npytestmark = pytest.mark.e2e\n\ndef test_live(monkeypatch):\n"
        "    monkeypatch.setattr('vendor.client.send', lambda: None)\n",
    )

    assert file_has_runtime_tier_test_double(path, runtime_markers=("e2e",)) is True


@pytest.mark.integration
def test_rejects_mock_in_individually_marked_runtime_tier(tmp_path: Path) -> None:
    path = _seed(
        tmp_path,
        "import pytest\nfrom unittest.mock import Mock\n\n@pytest.mark.pvt\ndef test_live():\n"
        "    client = Mock()\n",
    )

    assert file_has_runtime_tier_test_double(path, runtime_markers=("pvt",)) is True


@pytest.mark.integration
def test_allows_real_http_patch_method_in_runtime_tier(tmp_path: Path) -> None:
    path = _seed(
        tmp_path,
        "import pytest\npytestmark = pytest.mark.e2e\n\ndef test_live(client):\n"
        "    assert client.patch('/health').status_code == 200\n",
    )

    assert file_has_runtime_tier_test_double(path, runtime_markers=("e2e",)) is False


@pytest.mark.integration
def test_rejects_mock_in_runtime_marked_test_class(tmp_path: Path) -> None:
    path = _seed(
        tmp_path,
        "import pytest\nfrom unittest.mock import Mock\n\n@pytest.mark.e2e\nclass TestJourney:\n"
        "    def test_live(self):\n        client = Mock()\n",
    )

    assert file_has_runtime_tier_test_double(path, runtime_markers=("e2e",)) is True


@pytest.mark.integration
def test_rejects_fixture_double_used_by_individually_marked_test(tmp_path: Path) -> None:
    path = _seed(
        tmp_path,
        "import pytest\nfrom unittest.mock import Mock\n\n@pytest.fixture\ndef client():\n"
        "    return Mock()\n\n@pytest.mark.e2e\ndef test_live(client):\n    assert client\n",
    )

    assert file_has_runtime_tier_test_double(path, runtime_markers=("e2e",)) is True


@pytest.mark.integration
def test_rejects_double_in_in_file_helper_called_by_runtime_test(tmp_path: Path) -> None:
    path = _seed(
        tmp_path,
        "import pytest\npytestmark = pytest.mark.e2e\n\ndef _configure_client(monkeypatch):\n"
        "    monkeypatch.setattr('vendor.client.send', lambda: None)\n\ndef test_live(monkeypatch):\n"
        "    _configure_client(monkeypatch)\n",
    )

    assert file_has_runtime_tier_test_double(path, runtime_markers=("e2e",)) is True


@pytest.mark.integration
def test_rejects_double_in_transitive_in_file_helper_called_by_runtime_test(tmp_path: Path) -> None:
    path = _seed(
        tmp_path,
        "import pytest\npytestmark = pytest.mark.e2e\n\ndef _patch_client(monkeypatch):\n"
        "    monkeypatch.setattr('vendor.client.send', lambda: None)\n\ndef _configure_client(monkeypatch):\n"
        "    _patch_client(monkeypatch)\n\ndef test_live(monkeypatch):\n"
        "    _configure_client(monkeypatch)\n",
    )

    assert file_has_runtime_tier_test_double(path, runtime_markers=("e2e",)) is True


@pytest.mark.integration
def test_rejects_monkeypatch_passed_to_a_renamed_helper_parameter(tmp_path: Path) -> None:
    path = _seed(
        tmp_path,
        "import pytest\npytestmark = pytest.mark.e2e\n\ndef _configure_client(mp):\n"
        "    mp.setattr('vendor.client.send', lambda: None)\n\ndef test_live(monkeypatch):\n"
        "    _configure_client(monkeypatch)\n",
    )

    assert file_has_runtime_tier_test_double(path, runtime_markers=("e2e",)) is True


@pytest.mark.integration
def test_allows_restoring_a_real_module_in_runtime_tier(tmp_path: Path) -> None:
    path = _seed(
        tmp_path,
        "import sys\nimport pytest\npytestmark = pytest.mark.e2e\n\n"
        "saved_module = sys.modules.get('vendor.client')\n\ndef test_live():\n"
        "    sys.modules['vendor.client'] = saved_module\n",
    )

    assert file_has_runtime_tier_test_double(path, runtime_markers=("e2e",)) is False


@pytest.mark.integration
def test_ignores_module_helper_shadowed_by_a_local_binding(tmp_path: Path) -> None:
    path = _seed(
        tmp_path,
        "import pytest\nfrom unittest.mock import Mock\npytestmark = pytest.mark.e2e\n\n"
        "def check():\n    return Mock()\n\ndef test_live(live_client):\n"
        "    check = live_client.check\n    check()\n",
    )

    assert file_has_runtime_tier_test_double(path, runtime_markers=("e2e",)) is False


@pytest.mark.integration
def test_rejects_monkeypatch_in_a_runtime_test_class_helper_method(tmp_path: Path) -> None:
    path = _seed(
        tmp_path,
        "import pytest\n\n@pytest.mark.e2e\nclass TestJourney:\n"
        "    def _configure(self, mp):\n"
        "        mp.setattr('vendor.client.send', lambda: None)\n\n"
        "    def test_live(self, monkeypatch):\n"
        "        self._configure(monkeypatch)\n",
    )

    assert file_has_runtime_tier_test_double(path, runtime_markers=("e2e",)) is True


@pytest.mark.integration
def test_rejects_underscore_prefixed_fake_in_runtime_tier(tmp_path: Path) -> None:
    path = _seed(
        tmp_path,
        "import pytest\npytestmark = pytest.mark.e2e\n\nclass _FakeClient:\n    pass\n\ndef test_live():\n"
        "    assert _FakeClient()\n",
    )

    assert file_has_runtime_tier_test_double(path, runtime_markers=("e2e",)) is True


@pytest.mark.integration
def test_rejects_synthetic_module_injection_in_runtime_tier(tmp_path: Path) -> None:
    path = _seed(
        tmp_path,
        "import sys\nimport types\nimport pytest\npytestmark = pytest.mark.e2e\n\ndef test_live():\n"
        "    sys.modules['vendor.client'] = types.ModuleType('vendor.client')\n",
    )

    assert file_has_runtime_tier_test_double(path, runtime_markers=("e2e",)) is True


@pytest.mark.integration
def test_rejects_all_monkeypatch_mutation_methods_in_runtime_tier(tmp_path: Path) -> None:
    path = _seed(
        tmp_path,
        "import pytest\npytestmark = pytest.mark.e2e\n\ndef test_live(monkeypatch):\n"
        "    monkeypatch.setitem(registry, 'client', fake_client)\n",
    )

    assert file_has_runtime_tier_test_double(path, runtime_markers=("e2e",)) is True


@pytest.mark.integration
def test_resolves_pytest_import_aliases(tmp_path: Path) -> None:
    path = _seed(
        tmp_path,
        "import pytest as pt\nfrom unittest.mock import Mock\n\n@pt.mark.e2e\ndef test_live():\n"
        "    client = Mock()\n",
    )

    assert file_has_runtime_tier_test_double(path, runtime_markers=("e2e",)) is True


@pytest.mark.integration
def test_rejects_imported_unittest_patch_object(tmp_path: Path) -> None:
    path = _seed(
        tmp_path,
        "import pytest\nfrom unittest.mock import patch\n\n@pytest.mark.e2e\ndef test_live():\n"
        "    with patch.object(client, 'send'):\n        assert True\n",
    )

    assert file_has_runtime_tier_test_double(path, runtime_markers=("e2e",)) is True


@pytest.mark.integration
def test_resolves_imported_pytest_mark_alias(tmp_path: Path) -> None:
    path = _seed(
        tmp_path,
        "from pytest import mark as m\nfrom unittest.mock import Mock\n\n@m.e2e\ndef test_live():\n"
        "    assert Mock()\n",
    )

    assert file_has_runtime_tier_test_double(path, runtime_markers=("e2e",)) is True


@pytest.mark.integration
def test_rejects_configured_simulation_seam_in_runtime_tier(tmp_path: Path) -> None:
    path = _seed(
        tmp_path,
        "import pytest\n\n@pytest.mark.e2e\ndef test_live():\n    produce(request, runner=fake_runner)\n",
    )

    assert (
        file_has_runtime_tier_test_double(
            path,
            runtime_markers=("e2e",),
            forbidden_keyword_arguments=("runner",),
        )
        is True
    )


@pytest.mark.integration
def test_allows_test_double_in_contract_tier(tmp_path: Path) -> None:
    path = _seed(
        tmp_path,
        "from unittest.mock import Mock\n\ndef test_contract():\n    client = Mock()\n",
    )

    assert file_has_runtime_tier_test_double(path, runtime_markers=("e2e", "pvt")) is False


@pytest.mark.integration
def test_allows_live_runtime_test_without_a_test_double(tmp_path: Path) -> None:
    path = _seed(
        tmp_path,
        "import pytest\n\n@pytest.mark.journey\ndef test_live():\n    assert True\n",
    )

    assert file_has_runtime_tier_test_double(path, runtime_markers=("journey",)) is False


@pytest.mark.integration
def test_runtime_markers_are_consumer_configured(tmp_path: Path) -> None:
    path = _seed(
        tmp_path,
        "import pytest\npytestmark = pytest.mark.live\n\ndef test_live(monkeypatch):\n"
        "    monkeypatch.setattr('vendor.client.send', lambda: None)\n",
    )
    rule = NoTestDoublesInRuntimeTiers.from_config(
        {"roots": ["."], "runtime_markers": ["live"]},
        repo_root=tmp_path,
    )

    assert rule.file_has_violation(path) is True


@pytest.mark.integration
def test_build_returns_rule() -> None:
    assert isinstance(build({}), NoTestDoublesInRuntimeTiers)


@pytest.mark.integration
def test_no_repo_strings_in_executable_code() -> None:
    import tc_fitness.core_checks.no_test_doubles_in_runtime_tiers as mod

    assert_no_repo_identity(mod.__file__)
