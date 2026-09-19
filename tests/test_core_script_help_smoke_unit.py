"""Tests for the CORE check script_help_smoke (v0.6.0)."""

from __future__ import annotations

from pathlib import Path

import pytest

from tc_fitness.core_checks.script_help_smoke import (
    extract_declared_flags,
)

pytestmark = pytest.mark.unit

_GOOD_CLI = """
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent")
    parser.add_argument("--out-dir")
    parser.parse_args()
    return 0

if __name__ == "__main__":
    main()
"""

# Missing flag in help: argparse renders all add_argument flags, so the only
# way --help omits a declared flag is a parser that fails to build. We emulate
# the broken case with a script that crashes before printing help.
_BROKEN_CLI = """
import argparse

raise SystemExit(2)  # work at import time before argparse fires

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent")
    return 0
"""

_NOT_A_CLI = """
def helper():
    return 1
"""


def _seed(tmp_path: Path, rel: str, body: str) -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


def test_extract_declared_flags() -> None:
    import ast

    tree = ast.parse(_GOOD_CLI)
    assert extract_declared_flags(tree) == ("--agent", "--out-dir")
