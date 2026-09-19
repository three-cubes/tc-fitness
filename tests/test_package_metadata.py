"""Installed and source-checkout package-version behaviour."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.integration


def test_bare_source_checkout_reports_unknown_version_without_installed_metadata(tmp_path: Path) -> None:
    source = Path(__file__).resolve().parents[1] / "src"
    program = (
        "import sys\n"
        "sys.path[:] = [p for p in sys.path if not p.endswith(('site-packages', 'dist-packages'))]\n"
        f"sys.path.insert(0, {str(source)!r})\n"
        "import tc_fitness\n"
        "print(tc_fitness.__version__)\n"
    )

    result = subprocess.run(
        [sys.executable, "-c", program],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert result.stdout == "0+unknown\n"
