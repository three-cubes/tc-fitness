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


def consumer(root: Path, *, strict: bool = True, extra: str = "") -> None:
    seed(
        root,
        "checks.py",
        "from tc_fitness.catalogue import RuleEntry\nENTRIES = (RuleEntry(id='branches', gate='branches', check='core:coverage_includes_branches'),)\n",
    )
    seed(
        root,
        ".tc-fitness.toml",
        "[[steps]]\nid='coverage'\ncatalogue='checks:ENTRIES'\n"
        + ("baseline_free=true\n" if strict else "")
        + extra,
    )
    seed(root, "coverage.xml", '<coverage branch-rate="0" branches-valid="0"/>')


def test_catalogue_does_not_consume_baseline_debt(tmp_path: Path) -> None:
    consumer(tmp_path, strict=False)
    seed(tmp_path, ".architecture/baseline/coverage-includes-branches-files.txt", "coverage.xml\n")
    assert invoke(tmp_path) == 0
    consumer(tmp_path)
    assert invoke(tmp_path) == 1


def test_catalogue_rejects_public_establish_baseline(tmp_path: Path) -> None:
    consumer(tmp_path)
    assert invoke(tmp_path, "--establish-baseline") == 1
    assert not (tmp_path / ".architecture/baseline").exists()


def test_dispatched_python_check_cannot_write_a_baseline(tmp_path: Path) -> None:
    consumer(tmp_path)
    seed(
        tmp_path,
        "checks.py",
        "from tc_fitness.catalogue import RuleEntry\nENTRIES = (RuleEntry(id='escape', gate='escape', check='escape'),)\n",
    )
    seed(
        tmp_path,
        "scripts/checks/check_escape.py",
        "from pathlib import Path\nfrom tc_fitness.baseline import establish_baseline\ndef main():\n    establish_baseline('escape', ['coverage.xml'], Path("
        + repr(str(tmp_path))
        + "))\n    return 0\n",
    )
    assert invoke(tmp_path) == 1
    assert not (tmp_path / ".architecture/baseline").exists()


def test_baseline_free_step_rejects_conditional_python_subprocess(tmp_path: Path) -> None:
    consumer(tmp_path)
    seed(
        tmp_path,
        "checks.py",
        "from tc_fitness.catalogue import RuleEntry\n"
        "ENTRIES = (RuleEntry(id='escape', gate='escape', check='escape', "
        "subprocess_arg_env='COVERAGE_EVIDENCE', "
        "subprocess_arg_default='coverage.xml'),)\n",
    )
    seed(
        tmp_path,
        "scripts/checks/check_escape.py",
        "from pathlib import Path\n"
        "from tc_fitness.baseline import establish_baseline\n"
        "def main():\n"
        "    establish_baseline('escape', ['coverage.xml'], Path(" + repr(str(tmp_path)) + "))\n"
        "    return 0\n",
    )

    assert invoke(tmp_path) != 0
    assert not (tmp_path / ".architecture/baseline").exists()


@pytest.mark.parametrize(
    "extra",
    ['dispatch="subprocess"\n', "continue_on_error=true\n", "allow_missing=true\n", "parallel=true\n"],
)
def test_baseline_free_step_rejects_execution_escape_configuration(tmp_path: Path, extra: str) -> None:
    consumer(tmp_path, extra=extra)
    seed(tmp_path, "coverage.xml", '<coverage branch-rate="1" branches-valid="2"/>')
    assert invoke(tmp_path) != 0


def test_catalogue_import_cannot_write_a_baseline_before_dispatch(tmp_path: Path) -> None:
    consumer(tmp_path)
    path = tmp_path / "checks.py"
    path.write_text(
        "from pathlib import Path\nfrom tc_fitness.baseline import establish_baseline\nestablish_baseline('escape', [], Path("
        + repr(str(tmp_path))
        + "))\n"
        + path.read_text()
    )
    assert invoke(tmp_path) == 1
    assert not (tmp_path / ".architecture/baseline").exists()
