"""The installed public gate cannot suppress its coverage catalogue."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from tc_fitness.coverage_catalogue import ENTRIES

pytestmark = pytest.mark.integration


def test_coverage_catalogue_declares_the_actual_coverage_checks() -> None:
    assert tuple((entry.id, entry.check) for entry in ENTRIES) == (
        ("coverage_includes_branches", "core:coverage_includes_branches"),
        ("coverage_floor", "core:coverage_floor"),
        ("new_code_coverage", "core:new_code_coverage"),
    )


def seed(root: Path, relative: str, body: str) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body)
    return path


def invoke(root: Path, *args: str) -> int:
    return subprocess.run(
        [str(Path(sys.executable).with_name("tc-fitness")), "run", "--repo-root", str(root), *args],
        capture_output=True,
        timeout=15,
        check=False,
    ).returncode


def consumer(root: Path, *, extra: str = "") -> None:
    seed(
        root,
        "checks.py",
        "from tc_fitness.catalogue import RuleEntry\nENTRIES = (RuleEntry(id='branches', gate='branches', check='core:coverage_includes_branches'),)\n",
    )
    seed(
        root,
        ".tc-fitness.toml",
        "[[steps]]\nid='coverage'\ncatalogue='checks:ENTRIES'\n" + extra,
    )
    seed(root, "coverage.xml", '<coverage branch-rate="0" branches-valid="0"/>')


def test_catalogue_does_not_consume_legacy_baseline_debt(tmp_path: Path) -> None:
    consumer(tmp_path)
    seed(tmp_path, ".architecture/baseline/coverage-includes-branches-files.txt", "coverage.xml\n")
    assert invoke(tmp_path) == 1
