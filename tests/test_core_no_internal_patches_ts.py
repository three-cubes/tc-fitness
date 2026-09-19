"""Tests for the CORE check no_internal_patches_ts (v0.6.0 security-freshness batch)."""

from __future__ import annotations

from pathlib import Path

import pytest

from tc_fitness.core_checks.no_internal_patches_ts import (
    build,
    file_mocks_internal_ts,
)

pytestmark = pytest.mark.integration

_INTERNAL = frozenset({"mcp-x", "mcp-kairix"})
_EXEMPT_EXACT = frozenset({"fs", "axios", "console"})
_EXEMPT_PREFIXES = ("node:", "@azure/")


def _seed(tmp_path: Path, rel: str, body: str) -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


def _flags(p: Path) -> bool:
    return file_mocks_internal_ts(
        p, internal_packages=_INTERNAL, exempt_exact=_EXEMPT_EXACT, exempt_prefixes=_EXEMPT_PREFIXES
    )


def test_flags_relative_mock(tmp_path: Path) -> None:
    p = _seed(tmp_path, "a.test.ts", "vi.mock('../../src/client.js', () => ({}));\n")
    assert _flags(p) is True


def test_flags_internal_workspace_package_mock(tmp_path: Path) -> None:
    p = _seed(tmp_path, "a.test.ts", "jest.mock('mcp-kairix/dist/x.js');\n")
    assert _flags(p) is True


def test_external_mock_is_clean(tmp_path: Path) -> None:
    p = _seed(tmp_path, "a.test.ts", "vi.mock('node:fs/promises');\nvi.mock('axios');\n")
    assert _flags(p) is False


def test_spyon_internal_namespace_flagged(tmp_path: Path) -> None:
    body = "import * as client from '../src/client.js';\nvi.spyOn(client, 'graphGet');\n"
    p = _seed(tmp_path, "a.test.ts", body)
    assert _flags(p) is True


def test_spyon_console_is_clean(tmp_path: Path) -> None:
    p = _seed(tmp_path, "a.test.ts", "vi.spyOn(console, 'log');\n")
    assert _flags(p) is False


def test_mock_in_comment_is_clean(tmp_path: Path) -> None:
    p = _seed(tmp_path, "a.test.ts", "// vi.mock('../src/x.js')\n/* vi.mock('../src/y.js') */\n")
    assert _flags(p) is False


def test_unknown_package_mock_and_unresolved_spy_are_not_internal(tmp_path: Path) -> None:
    p = _seed(
        tmp_path,
        "a.test.ts",
        "vi.mock('lodash/fp');\nvi.spyOn(unimported, 'map');\n",
    )

    assert _flags(p) is False


def test_named_import_alias_resolves_internal_spy_target(tmp_path: Path) -> None:
    p = _seed(
        tmp_path,
        "a.test.ts",
        "import { client as cli } from 'mcp-x/client';\nvi.spyOn(cli, 'send');\n",
    )

    assert _flags(p) is True


def test_default_and_namespace_imports_resolve_spy_sources(tmp_path: Path) -> None:
    internal = _seed(
        tmp_path,
        "default.test.ts",
        "import client from 'mcp-x/client';\nvi.spyOn(client, 'send');\n",
    )
    external = _seed(
        tmp_path,
        "namespace.test.ts",
        "import * as maps from 'lodash/fp';\nvi.spyOn(maps, 'map');\n",
    )
    exempt_prefix = _seed(
        tmp_path,
        "sdk.test.ts",
        "import * as sdk from '@azure/openai';\nvi.spyOn(sdk, 'send');\n",
    )

    assert _flags(internal) is True
    assert _flags(external) is False
    assert _flags(exempt_prefix) is False


def test_missing_source_is_ignored(tmp_path: Path) -> None:
    assert _flags(tmp_path / "missing.test.ts") is False


def test_non_test_ts_out_of_scope(tmp_path: Path) -> None:
    rule = build({"roots": ["."], "internal_packages": ["mcp-x"]}, repo_root=tmp_path)
    _seed(tmp_path, "src/x.ts", "vi.mock('../../src/client.js');\n")
    # .ts (not .test.ts) is out of scope via the default extensions.
    assert rule.collect_violations() == set()
