"""Tests for the CORE check no_noop_test_scripts (v0.6.0)."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from tc_fitness.core_checks.no_noop_test_scripts import (
    script_is_noop,
)

pytestmark = pytest.mark.unit

_PLACEHOLDER = re.compile(
    r"(?:no tests? yet|todo|placeholder|not implemented|skip tests?|exit\s+0)", re.IGNORECASE
)
_REAL = re.compile(r"\b(vitest|jest|node\s+--test|tsx|mocha|tap|ava|playwright)\b")


def _seed_pkg(tmp_path: Path, rel: str, test_script: str) -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"scripts": {"test": test_script}}), encoding="utf-8")
    return p


def test_placeholder_is_noop() -> None:
    assert (
        script_is_noop("echo 'no tests yet' && exit 0", placeholder=_PLACEHOLDER, real_runner=_REAL) is True
    )


def test_real_runner_is_not_noop() -> None:
    assert script_is_noop("vitest run src --coverage", placeholder=_PLACEHOLDER, real_runner=_REAL) is False


def test_placeholder_with_real_runner_passes() -> None:
    # mentions "exit 0" but also runs vitest → real
    assert script_is_noop("vitest run || exit 0", placeholder=_PLACEHOLDER, real_runner=_REAL) is False
