"""Installed-package proof for check-contract manifest parsing."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.e2e


def test_default_wheel_install_parses_a_check_contract(tmp_path: Path) -> None:
    """A clean default install includes the YAML parser required by the contract API."""
    dist = tmp_path / "dist"
    build = subprocess.run(
        ["uv", "build", "--wheel", "--out-dir", str(dist)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert build.returncode == 0, build.stderr
    wheel = next(dist.glob("three_cubes_fitness-*.whl"))
    environment = tmp_path / "environment"
    create = subprocess.run(
        ["uv", "venv", "--python", sys.executable, str(environment)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert create.returncode == 0, create.stderr
    python = environment / "bin" / "python"
    install = subprocess.run(
        ["uv", "pip", "install", "--python", str(python), str(wheel)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert install.returncode == 0, install.stderr
    manifest = tmp_path / "contract.yaml"
    manifest.write_text(
        """
schema: tc.fitness/check-contract/v1
check: core:example_check
config: {}
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
        - rule: example-check
          path: src/broken.py
          message_contains: required behaviour is missing
dependencies: []
""",
        encoding="utf-8",
    )
    parse = subprocess.run(
        [
            str(python),
            "-c",
            "from pathlib import Path; from tc_fitness.check_contracts import load_check_contract; "
            "print(load_check_contract(Path(__import__('sys').argv[1])).check)",
            str(manifest),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert parse.returncode == 0, parse.stderr
    assert parse.stdout.strip() == "core:example_check"
