"""Real reports and public commands prove independent coverage admission."""

from __future__ import annotations

import json
import runpy
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from tc_fitness.core_checks._coverage_evidence import CoverageCounts
from tc_fitness.coverage_admission import complete_line_hits, exact_checkout
from tc_fitness.coverage_measurement import cross_check_branches
from tc_fitness.runner import run_contract_case

pytestmark = pytest.mark.integration


def seed(root: Path, path: str, text: str) -> Path:
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text)
    return target


def report(
    root: Path, *, lines: int = 100, covered: int = 100, branches: int = 100, branch_covered: int = 100
) -> str:
    """Materialised Cobertura inputs with hand-chosen, exact integer counts.

    The source is generated to hold exactly the statements and branch
    opportunities the report declares — ``branches // 2`` two-exit conditionals
    followed by plain assignments. Coverage.py decides which lines those are,
    so a case cannot assert against a report shape no real run could produce.
    """
    import coverage

    from tc_fitness.coverage_measurement import source_branch_totals

    conditionals = branches // 2
    source = "if value:\n    value = 1\n" * conditionals + "value = 1\n" * (lines - 2 * conditionals)
    path = seed(root, "src/subject.py", source)
    analyzer = coverage.Coverage(config_file=False, data_file=None)
    analyzer.set_option("report:exclude_lines", [])
    analyzer.set_option("report:partial_branches", [])
    statements = sorted(analyzer.analysis2(str(path))[1])
    exits = source_branch_totals(path)
    assert len(statements) == lines, (len(statements), lines)
    assert sum(exits.values()) == branches, (sum(exits.values()), branches)
    taken = {line: min(2, max(0, branch_covered - index * 2)) for index, line in enumerate(sorted(exits))}
    detail = []
    for index, number in enumerate(statements, start=1):
        branch = ""
        if number in exits:
            hits = taken[number]
            branch = f' branch="true" condition-coverage="{hits * 50}% ({hits}/2)"'
        detail.append(f'<line number="{number}" hits="{int(index <= covered)}"{branch}/>')
    return (
        f'<coverage lines-valid="{lines}" lines-covered="{covered}" '
        f'branches-valid="{branches}" branches-covered="{branch_covered}" '
        f'line-rate="{covered / lines}" branch-rate="{branch_covered / branches}">'
        "<sources><source>src</source></sources><packages><package><classes>"
        f'<class filename="subject.py" line-rate="{covered / lines}" '
        f'branch-rate="{branch_covered / branches}"><lines>{"".join(detail)}</lines></class>'
        "</classes></package></packages></coverage>"
    )


def consumer(root: Path, *, critical: bool = False) -> int:
    seed(
        root,
        "consumer_checks.py",
        "from tc_fitness.catalogue import RuleEntry\n"
        "ENTRIES = (RuleEntry(id='coverage', gate='coverage', check='core:coverage_floor'),)\n",
    )
    config = (
        "[[steps]]\nid = 'coverage'\ncatalogue = 'consumer_checks:ENTRIES'\n"
        "[core_checks.coverage_floor]\nroots = ['src']\nfloor_pct = 95\nbranch_floor_pct = 95\n"
    )
    if critical:
        config += "critical_branch_files = ['src/subject.py']\n"
    seed(root, ".tc-fitness.toml", config)
    return subprocess.run(
        [str(Path(sys.executable).with_name("tc-fitness")), "run", "--repo-root", str(root)],
        capture_output=True,
        check=False,
        timeout=15,
    ).returncode


def test_branch_floor_rejects_low_branches_despite_full_lines(tmp_path: Path) -> None:
    seed(tmp_path, "coverage.xml", report(tmp_path, branches=100, branch_covered=94))
    assert consumer(tmp_path) == 1


def test_exact_checkout_rejects_a_noncommit_base(tmp_path: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    seed(tmp_path, "tracked.txt", "value\n")
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(
        [
            "git",
            "-c",
            "user.name=Coverage",
            "-c",
            "user.email=coverage@example.invalid",
            "commit",
            "-qm",
            "candidate",
        ],
        cwd=tmp_path,
        check=True,
    )
    subprocess.run(
        [
            "git",
            "-c",
            "user.name=Coverage",
            "-c",
            "user.email=coverage@example.invalid",
            "tag",
            "-am",
            "annotated",
            "base-tag",
        ],
        cwd=tmp_path,
        check=True,
    )
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=tmp_path, check=True, capture_output=True, text=True
    ).stdout.strip()
    tag_object = subprocess.run(
        ["git", "rev-parse", "base-tag"], cwd=tmp_path, check=True, capture_output=True, text=True
    ).stdout.strip()
    with pytest.raises(ValueError, match="exact base is not a commit"):
        exact_checkout(tmp_path, tag_object, head)


def test_complete_line_hits_rejects_missing_source_document(tmp_path: Path) -> None:
    # One conditional is two statements, so this is the smallest report that
    # can carry a branch at all; the case only needs the measured file set to
    # differ from the source set.
    xml = seed(tmp_path, "coverage.xml", report(tmp_path, lines=2, covered=2, branches=2, branch_covered=2))
    extra = seed(tmp_path, "src/extra.py", "value = 2\n")
    files = {"src/subject.py": tmp_path / "src/subject.py", "src/extra.py": extra}
    with pytest.raises(ValueError, match="complete source set"):
        complete_line_hits(tmp_path, xml, files)


def test_complete_line_hits_rejects_invented_executable_line(tmp_path: Path) -> None:
    xml = seed(tmp_path, "coverage.xml", report(tmp_path, lines=2, covered=2, branches=2, branch_covered=2))
    source = tmp_path / "src/subject.py"
    source.write_text("value = 1\n# non-executable line\n")
    with pytest.raises(ValueError, match="omits or invents executable source lines"):
        complete_line_hits(tmp_path, xml, {"src/subject.py": source})


def test_branch_cross_check_rejects_malformed_xml_counts(tmp_path: Path) -> None:
    source = seed(tmp_path, "src/subject.py", "def choose(flag):\n    return 1 if flag else 0\n")
    xml = seed(
        tmp_path,
        "coverage.xml",
        "<coverage><sources><source>src</source></sources><packages><package><classes>"
        '<class filename="subject.py"><lines><line number="2" hits="1" branch="true" '
        'condition-coverage="malformed"/></lines></class></classes></package></packages></coverage>',
    )
    seed(
        tmp_path,
        "coverage.json",
        json.dumps(
            {
                "meta": {"branch_coverage": True},
                "files": {"src/subject.py": {}},
                "totals": {},
            }
        ),
    )
    with pytest.raises(ValueError, match="branch counts are malformed"):
        cross_check_branches(
            tmp_path,
            xml,
            {"src/subject.py": source},
            {"src/subject.py": {1: 1, 2: 1}},
            {"src/subject.py": CoverageCounts(2, 2, 2, 2)},
        )


def test_coverage_admission_module_entrypoint_exposes_help(capsys: pytest.CaptureFixture[str]) -> None:
    original = sys.argv
    sys.argv = ["coverage_admission", "--help"]
    try:
        with pytest.raises(SystemExit) as stopped:
            runpy.run_path(complete_line_hits.__code__.co_filename, run_name="__main__")
    finally:
        sys.argv = original
    assert stopped.value.code == 0
    assert "produce" in capsys.readouterr().out


@pytest.mark.parametrize("change", ["empty-roots", "exemption", "nan-line", "nan-branch", "missing-critical"])
def test_strict_configuration_cannot_make_measurement_vacuous(tmp_path: Path, change: str) -> None:
    seed(tmp_path, "coverage.xml", report(tmp_path))
    assert consumer(tmp_path) == 0
    path = tmp_path / ".tc-fitness.toml"
    config = path.read_text()
    if change == "empty-roots":
        config = config.replace("roots = ['src']", "roots = []")
    elif change == "exemption":
        config += "exempt_files = ['src/subject.py']\n"
    elif change == "nan-line":
        config = config.replace("floor_pct = 95", "floor_pct = nan", 1)
    elif change == "nan-branch":
        config = config.replace("branch_floor_pct = 95", "branch_floor_pct = nan")
    else:
        config += "critical_branch_files = ['src/missing.py']\n"
    path.write_text(config)
    result = subprocess.run(
        [str(Path(sys.executable).with_name("tc-fitness")), "run", "--repo-root", str(tmp_path)],
        capture_output=True,
        check=False,
        timeout=15,
    )
    assert result.returncode == 1


def test_strict_branch_admission_cannot_be_grandfathered(tmp_path: Path) -> None:
    seed(tmp_path, "coverage.xml", report(tmp_path, branch_covered=94))
    seed(tmp_path, ".architecture/baseline/coverage-floor-files.txt", "src/subject.py\n")
    assert consumer(tmp_path) == 1


def test_exact_95_percent_floors_are_inclusive(tmp_path: Path) -> None:
    seed(tmp_path, "coverage.xml", report(tmp_path, covered=95, branch_covered=95))
    assert consumer(tmp_path) == 0


@pytest.mark.parametrize("critical", ["./src/subject.py", "src2/subject.py"])
def test_critical_paths_cannot_escape_exact_source_membership(tmp_path: Path, critical: str) -> None:
    seed(tmp_path, "coverage.xml", report(tmp_path, branch_covered=99))
    seed(tmp_path, "src2/subject.py", "value = 1\n")
    assert consumer(tmp_path) == 0
    config = tmp_path / ".tc-fitness.toml"
    config.write_text(config.read_text() + f"critical_branch_files = ['{critical}']\n")
    result = subprocess.run(
        [str(Path(sys.executable).with_name("tc-fitness")), "run", "--repo-root", str(tmp_path)],
        capture_output=True,
        check=False,
        timeout=15,
    )
    assert result.returncode == 1


def contract(
    root: Path,
    bad_report: str,
    *,
    critical: bool = False,
    status: str = "fail",
    finding: str = "branch coverage",
) -> Path:
    good = root / "compliant"
    bad = root / "violation"
    seed(good, "coverage.xml", report(good))
    # report() has already materialised this case's source tree.
    seed(bad, "coverage.xml", bad_report)
    config: dict[str, object] = {"roots": ["src"], "floor_pct": 95, "branch_floor_pct": 95}
    if critical:
        config["critical_branch_files"] = ["src/subject.py"]
    cases = [
        {
            "id": "compliant",
            "fixture": "compliant",
            "expected": {"status": "pass", "exit": "zero", "findings": []},
        },
        {
            "id": "violation",
            "fixture": "violation",
            "expected": {
                "status": "fail",
                "exit": "nonzero",
                "findings": [
                    {"rule": "coverage-floor", "path": "src/subject.py", "message_contains": finding}
                ],
            },
        },
    ]
    if status == "error":
        cases.append(
            {
                "id": "malformed",
                "fixture": "violation",
                "expected": {
                    "status": "error",
                    "exit": "nonzero",
                    "findings": [
                        {"rule": "check-execution-error", "path": ".", "message_contains": "ValueError"}
                    ],
                },
            }
        )
    manifest = seed(
        root,
        "contract.yaml",
        yaml.safe_dump(
            {
                "schema": "tc.fitness/check-contract/v1",
                "check": "core:coverage_floor",
                "config": config,
                "dependencies": [],
                "cases": cases,
            }
        ),
    )
    return manifest


@pytest.mark.parametrize(("metric", "critical"), [("line", False), ("branch", False), ("critical", True)])
def test_exact_independent_floors_through_public_contract(
    tmp_path: Path, metric: str, critical: bool
) -> None:
    if metric == "line":
        xml = report(tmp_path / "violation", lines=10000, covered=9499)
        finding = "line coverage 94.99%"
    elif metric == "branch":
        xml = report(tmp_path / "violation", lines=10000, covered=10000, branches=10000, branch_covered=9499)
        finding = "branch coverage 94.99%"
    else:
        xml = report(tmp_path / "violation", branch_covered=99)
        finding = "critical branch coverage 99%"
    manifest = contract(tmp_path, xml, critical=critical, finding=finding)
    for case in ("compliant", "violation"):
        run_contract_case(manifest, case, tmp_path / f"{case}.json")


@pytest.mark.parametrize(
    "damage",
    [
        "no-lines",
        "no-condition",
        "bad-count",
        "nan-rate",
        "duplicate-line",
        "duplicate-class",
        "forged-total",
        "line-outside-source",
    ],
)
def test_missing_or_inconsistent_detail_is_an_error(tmp_path: Path, damage: str) -> None:
    xml = report(tmp_path / "violation")
    if damage == "no-lines":
        start, end = xml.index("<lines>"), xml.index("</lines>") + len("</lines>")
        xml = xml[:start] + xml[end:]
    elif damage == "no-condition":
        xml = xml.replace(' condition-coverage="100% (2/2)"', "", 1)
    elif damage == "bad-count":
        xml = xml.replace("100% (2/2)", "150% (3/2)", 1)
    elif damage == "nan-rate":
        xml = xml.replace('line-rate="1.0"', 'line-rate="NaN"')
    elif damage == "duplicate-line":
        xml = xml.replace('number="2"', 'number="1"', 1)
    elif damage == "duplicate-class":
        start, end = xml.index("<class "), xml.index("</class>") + len("</class>")
        xml = xml[:end] + xml[start:end] + xml[end:]
    elif damage == "forged-total":
        xml = xml.replace('branches-covered="100"', 'branches-covered="101"')
    else:
        xml = xml.replace('number="100"', 'number="101"')
    manifest = contract(tmp_path, xml, status="error")
    run_contract_case(manifest, "malformed", tmp_path / "ledger.json")


def test_incomplete_source_report_cannot_pass(tmp_path: Path) -> None:
    manifest = contract(tmp_path, report(tmp_path / "violation"))
    seed(tmp_path / "violation", "src/omitted.py", "missing = 1\n")
    value = yaml.safe_load(manifest.read_text())
    value["cases"][1]["expected"]["findings"] = [
        {"rule": "coverage-floor", "path": "src/omitted.py", "message_contains": "missing coverage detail"}
    ]
    manifest.write_text(yaml.safe_dump(value))
    run_contract_case(manifest, "violation", tmp_path / "ledger.json")


def test_real_branch_report_and_unimported_source_are_measured(tmp_path: Path) -> None:
    seed(tmp_path, "src/subject.py", "def choose(value):\n    if value:\n        return 1\n    return 0\n")
    seed(tmp_path, "src/unimported.py", "value = 1\n")
    seed(
        tmp_path,
        "exercise.py",
        "from src.subject import choose\nassert choose(True) == 1\nassert choose(False) == 0\n",
    )
    seed(
        tmp_path,
        ".coveragerc",
        "[run]\nbranch = true\nsource = src\n[report]\nexclude_lines =\npartial_branches =\n",
    )
    for arguments in (("run", "exercise.py"), ("xml",), ("json",)):
        subprocess.run(
            [sys.executable, "-m", "coverage", *arguments],
            cwd=tmp_path,
            check=True,
            capture_output=True,
            timeout=15,
        )
    data = json.loads((tmp_path / "coverage.json").read_text())
    assert data["meta"]["branch_coverage"] is True
    assert data["files"]["src/subject.py"]["summary"]["covered_branches"] == 2
    assert data["files"]["src/unimported.py"]["missing_lines"] == [1]
    assert consumer(tmp_path, critical=True) == 1
    seed(tmp_path, "exercise.py", (tmp_path / "exercise.py").read_text() + "import src.unimported\n")
    for arguments in (("run", "exercise.py"), ("xml",)):
        subprocess.run(
            [sys.executable, "-m", "coverage", *arguments],
            cwd=tmp_path,
            check=True,
            capture_output=True,
            timeout=15,
        )
    assert consumer(tmp_path, critical=True) == 0


def test_real_rounded_cobertura_rates_use_exact_detail(tmp_path: Path) -> None:
    fixture = tmp_path / "violation"
    seed(fixture, "src/subject.py", "def absent():\n    return 0\nvalue = 1\n")
    seed(fixture, "exercise.py", "import src.subject\n")
    seed(fixture, ".coveragerc", "[run]\nbranch = true\nsource = src\n")
    for arguments in (("run", "exercise.py"), ("xml",)):
        subprocess.run(
            [sys.executable, "-m", "coverage", *arguments],
            cwd=fixture,
            check=True,
            capture_output=True,
            timeout=15,
        )
    # Relocate the producer's source root for the contract execution snapshot;
    # retain its real integer detail and four-significant-digit summary rates.
    xml = (fixture / "coverage.xml").read_text().replace(str(fixture / "src"), "src")
    manifest = contract(tmp_path, xml, finding="line coverage 66.6667%")
    run_contract_case(manifest, "violation", tmp_path / "ledger.json")


@pytest.mark.parametrize("measure_branches", [False, True])
def test_line_only_report_cannot_satisfy_branch_admission(tmp_path: Path, measure_branches: bool) -> None:
    seed(tmp_path, "src/subject.py", "def choose(value):\n    if value:\n        return 1\n    return 0\n")
    seed(
        tmp_path,
        "exercise.py",
        "from src.subject import choose\nassert choose(True) == 1\nassert choose(False) == 0\n",
    )
    seed(tmp_path, ".coveragerc", f"[run]\nbranch = {str(measure_branches).lower()}\nsource = src\n")
    for arguments in (("run", "exercise.py"), ("xml",)):
        subprocess.run(
            [sys.executable, "-m", "coverage", *arguments],
            cwd=tmp_path,
            check=True,
            capture_output=True,
            timeout=15,
        )
    assert consumer(tmp_path) == (0 if measure_branches else 1)


def test_self_measurement_configuration_counts_suppressed_and_unimported_code(tmp_path: Path) -> None:
    # Exercise the real repository coverage config on a controlled package;
    # no assertion depends on a particular TOML line or command spelling.
    shutil.copyfile(Path(__file__).parents[1] / "pyproject.toml", tmp_path / "pyproject.toml")
    seed(tmp_path, "src/tc_fitness/__init__.py", "")
    seed(tmp_path, "src/tc_fitness/unimported.py", "value = 1\n")
    seed(
        tmp_path,
        "src/tc_fitness/subject.py",
        "def choose(value):\n    if value: # pragma: no branch\n        return 1\n    return 0 # pragma: no cover\n",
    )
    seed(tmp_path, "exercise.py", "from src.tc_fitness.subject import choose\nassert choose(True) == 1\n")
    for arguments in (("run", "exercise.py"), ("json",)):
        subprocess.run(
            [sys.executable, "-m", "coverage", *arguments],
            cwd=tmp_path,
            check=True,
            capture_output=True,
            timeout=15,
        )
    data = json.loads((tmp_path / "coverage.json").read_text())
    assert data["meta"]["branch_coverage"] is True
    assert data["files"]["src/tc_fitness/unimported.py"]["missing_lines"] == [1]
    subject = data["files"]["src/tc_fitness/subject.py"]
    assert subject["missing_lines"] == [4]
    assert subject["excluded_lines"] == []
    assert subject["summary"]["missing_branches"] == 1
