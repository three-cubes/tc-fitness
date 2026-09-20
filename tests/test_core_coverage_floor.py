"""Tests for the CORE check coverage_floor (v0.6.0)."""

from __future__ import annotations

import ast
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from tc_fitness.core_checks.coverage_floor import (
    build,
    parse_coverage_details,
    parse_coverage_report,
)

pytestmark = pytest.mark.integration


def _report(line_rates: dict[str, float], *, source: str = "src", sources: list[str] | None = None) -> str:
    classes = "\n".join(f'<class filename="{name}" line-rate="{rate}"/>' for name, rate in line_rates.items())
    source_values = sources if sources is not None else [source]
    source_xml = "".join(f"<source>{value}</source>" for value in source_values)
    return (
        '<?xml version="1.0" ?>\n'
        '<coverage line-rate="0.5">\n'
        f"  <sources>{source_xml}</sources>\n"
        f"  <packages><package><classes>\n{classes}\n"
        "  </classes></package></packages>\n"
        "</coverage>\n"
    )


def _seed(tmp_path: Path, rel: str, body: str) -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


def _strict_report(classes: dict[str, tuple[tuple[int, ...], tuple[int, int] | None]]) -> str:
    """Build count-consistent Cobertura detail for the files materialised by a test.

    Line numbers run from one, so a caller outside ``_strict_fixture`` must
    supply sources whose statements start at line one and run consecutively.
    """
    return _strict_document(
        {
            filename: (
                dict(enumerate(hits, start=1)),
                {1: branch} if branch is not None else {},
            )
            for filename, (hits, branch) in classes.items()
        }
    )


def _strict_document(classes: dict[str, tuple[dict[int, int], dict[int, tuple[int, int]]]]) -> str:
    """Render count-consistent Cobertura detail from explicit per-line counts."""
    line_total = line_covered = branch_total = branch_covered = 0
    rendered: list[str] = []
    for filename, (hits, branches) in classes.items():
        line_total += len(hits)
        line_covered += sum(hit > 0 for hit in hits.values())
        line_elements = []
        for number, hit in sorted(hits.items()):
            attributes = ""
            if number in branches:
                covered, total = branches[number]
                attributes = (
                    f' branch="true" condition-coverage="{100 * covered / total:g}% ({covered}/{total})"'
                )
            line_elements.append(f'<line number="{number}" hits="{hit}"{attributes}/>')
        taken = sum(covered for covered, _ in branches.values())
        exits = sum(total for _, total in branches.values())
        branch_covered += taken
        branch_total += exits
        rendered.append(
            f'<class filename="{filename}" '
            f'line-rate="{sum(hit > 0 for hit in hits.values()) / len(hits):.4g}" '
            f'branch-rate="{taken / exits if exits else 1:.4g}">'
            f"<lines>{''.join(line_elements)}</lines></class>"
        )
    line_rate = line_covered / line_total if line_total else 1
    branch_rate = branch_covered / branch_total if branch_total else 1
    return (
        f'<coverage line-rate="{line_rate:.4g}" branch-rate="{branch_rate:.4g}" '
        f'lines-valid="{line_total}" lines-covered="{line_covered}" '
        f'branches-valid="{branch_total}" branches-covered="{branch_covered}">'
        f"<sources><source>.</source></sources><packages><package><classes>{''.join(rendered)}"
        "</classes></package></packages></coverage>"
    )


def _strict_fixture(
    tmp_path: Path,
    classes: dict[str, tuple[str, tuple[int, ...], tuple[int, int] | None]],
) -> Path:
    """Materialise sources and a report whose inventory is Coverage.py's own.

    Statement lines and branch exit counts come from the file that was just
    written, so the fixture cannot declare an inventory the source does not
    have. Each test supplies only hit counts, one per statement in source
    order, and the taken/total pair for the file's single branching line.
    """
    import coverage

    from tc_fitness.coverage_measurement import source_branch_totals

    analyzer = coverage.Coverage(config_file=False, data_file=None)
    analyzer.set_option("report:exclude_lines", [])
    analyzer.set_option("report:partial_branches", [])
    document: dict[str, tuple[dict[int, int], dict[int, tuple[int, int]]]] = {}
    for filename, (source, hits, branch) in classes.items():
        path = _seed(tmp_path, filename, source)
        statements = sorted(analyzer.analysis2(str(path))[1])
        totals = source_branch_totals(path)
        assert len(statements) == len(hits), (filename, statements, hits)
        assert (branch is None) == (not totals), (filename, totals, branch)
        branches = {}
        if branch is not None:
            (line, total), (covered, declared) = next(iter(totals.items())), branch
            assert declared == total, (filename, declared, total)
            branches = {line: (covered, total)}
        document[filename] = (dict(zip(statements, hits, strict=True)), branches)
    return _seed(tmp_path, "coverage.xml", _strict_document(document))


def test_parse_joins_source_root(tmp_path: Path) -> None:
    p = _seed(tmp_path, "coverage.xml", _report({"a.py": 0.4, "b.py": 1.0}))
    parsed = parse_coverage_report(p)
    assert parsed == {"src/a.py": 40.0, "src/b.py": 100.0}


def test_absolute_source_root_is_normalised_to_repository_paths(tmp_path: Path) -> None:
    _seed(tmp_path, "src/tc_fitness/a.py", "value = 1\n")
    report = _seed(
        tmp_path,
        "coverage.xml",
        _report({"src/tc_fitness/a.py": 0.4}, source=str(tmp_path)),
    )

    assert parse_coverage_report(report, repo_root=tmp_path) == {"src/tc_fitness/a.py": 40.0}
    rule = build({"roots": ["src/tc_fitness"], "floor_pct": 95.0}, repo_root=tmp_path)
    assert rule.collect_violations() == {Path("src/tc_fitness/a.py")}


def test_multiple_absolute_source_roots_resolve_existing_files(tmp_path: Path) -> None:
    _seed(tmp_path, "src/tc_fitness/a.py", "value = 1\n")
    _seed(tmp_path, "scripts/helper.py", "value = 2\n")
    report = _seed(
        tmp_path,
        "coverage.xml",
        _report(
            {"a.py": 1.0, "helper.py": 0.4},
            sources=[str(tmp_path / "src" / "tc_fitness"), str(tmp_path / "scripts")],
        ),
    )

    assert parse_coverage_report(report, repo_root=tmp_path) == {
        "src/tc_fitness/a.py": 100.0,
        "scripts/helper.py": 40.0,
    }


def test_missing_report_is_a_violation(tmp_path: Path) -> None:
    _seed(tmp_path, "src/a.py", "value = 1\n")
    rule = build({"roots": ["src"], "floor_pct": 95.0}, repo_root=tmp_path)

    assert rule.collect_violations() == {Path("coverage.xml")}
    assert rule.run() == 1


def test_empty_report_is_a_violation(tmp_path: Path) -> None:
    _seed(tmp_path, "src/a.py", "value = 1\n")
    _seed(tmp_path, "coverage.xml", "<coverage><sources><source>src</source></sources></coverage>")
    rule = build({"roots": ["src"], "floor_pct": 95.0}, repo_root=tmp_path)

    assert rule.collect_violations() == {Path("coverage.xml")}


def test_source_file_omitted_from_report_is_a_violation(tmp_path: Path) -> None:
    _seed(tmp_path, "src/measured.py", "value = 1\n")
    _seed(tmp_path, "src/omitted.py", "value = 2\n")
    _seed(tmp_path, "coverage.xml", _report({"measured.py": 1.0}))
    rule = build({"roots": ["src"], "floor_pct": 95.0}, repo_root=tmp_path)

    assert rule.collect_violations() == {Path("src/omitted.py")}


def test_below_floor_is_violation(tmp_path: Path) -> None:
    _seed(tmp_path, "src/a.py", "a = 1\n")
    _seed(tmp_path, "src/b.py", "b = 1\n")
    _seed(tmp_path, "coverage.xml", _report({"a.py": 0.4, "b.py": 0.95}))
    rule = build({"roots": ["src"], "floor_pct": 90.0}, repo_root=tmp_path)
    assert {str(p) for p in rule.collect_violations()} == {"src/a.py"}


def test_floor_is_config_driven(tmp_path: Path) -> None:
    _seed(tmp_path, "src/a.py", "a = 1\n")
    _seed(tmp_path, "coverage.xml", _report({"a.py": 0.85}))
    # floor 90 → a.py violates; floor 80 → clean.
    assert {
        str(p) for p in build({"roots": ["src"], "floor_pct": 90.0}, repo_root=tmp_path).collect_violations()
    } == {"src/a.py"}
    assert build({"roots": ["src"], "floor_pct": 80.0}, repo_root=tmp_path).collect_violations() == set()


def test_roots_scope_the_violation_set(tmp_path: Path) -> None:
    _seed(tmp_path, "coverage.xml", _report({"a.py": 0.1}, source="vendor"))
    rule = build({"roots": ["src"], "floor_pct": 90.0}, repo_root=tmp_path)
    assert rule.collect_violations() == set()  # vendor/a.py is out of the src root


def test_unsafe_xml_rejected(tmp_path: Path) -> None:
    p = _seed(tmp_path, "coverage.xml", "<!DOCTYPE x>\n<coverage/>")
    try:
        parse_coverage_report(p)
    except ValueError as exc:
        assert "DTD/entity" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("expected ValueError for DTD declaration")


def test_parse_coverage_report_skips_invalid_entries_and_keeps_lowest_duplicate_rate(tmp_path: Path) -> None:
    report = _seed(
        tmp_path,
        "coverage.xml",
        """<coverage><sources><source>src</source></sources><packages><package><classes>
        <class filename="module.py" line-rate="0.9"/>
        <class filename="module.py" line-rate="0.4"/>
        <class filename="module.py" line-rate="0.6"/>
        <class filename="" line-rate="0.1"/>
        <class filename="broken.py" line-rate="not-a-rate"/>
        </classes></package></packages></coverage>""",
    )

    assert parse_coverage_report(report) == {"src/module.py": 40.0}


@pytest.mark.parametrize(
    ("document", "message"),
    [
        ("<other/>", "expected a Cobertura"),
        ("<coverage><class><lines/></class></coverage>", "missing its source filename"),
        (
            '<coverage><sources><source>.</source></sources><class filename="src/a.py" line-rate="1" branch-rate="1"><lines><line number="1" hits="1"/></lines></class><class filename="src/a.py" line-rate="1" branch-rate="1"><lines><line number="1" hits="1"/></lines></class></coverage>',
            "duplicate source file",
        ),
        ("<coverage><sources><source>.</source></sources></coverage>", "empty coverage report"),
    ],
)
def test_strict_report_rejects_incomplete_file_details(
    tmp_path: Path,
    document: str,
    message: str,
) -> None:
    _seed(tmp_path, "src/a.py", "value = 1\n")
    report = _seed(tmp_path, "coverage.xml", document)

    with pytest.raises(ValueError, match=message):
        parse_coverage_details(report, repo_root=tmp_path)


def test_stdlib_xml_fallback_reads_a_real_report_without_site_packages(tmp_path: Path) -> None:
    report = _seed(tmp_path, "coverage.xml", _report({"a.py": 0.75}))
    source_root = Path(__file__).parents[1] / "src"
    program = (
        "import json, sys; "
        "sys.path.insert(0, sys.argv[1]); "
        "from tc_fitness.core_checks.coverage_floor import parse_coverage_report; "
        "print(json.dumps(parse_coverage_report(__import__('pathlib').Path(sys.argv[2]))))"
    )
    result = subprocess.run(
        [sys.executable, "-S", "-c", program, str(source_root), str(report)],
        capture_output=True,
        check=False,
        text=True,
        env={**os.environ, "PYTHONPATH": ""},
    )

    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout) == {"src/a.py": 75.0}


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("floor_pct", True),
        ("floor_pct", "95"),
        ("floor_pct", -1),
        ("floor_pct", 101),
        ("branch_floor_pct", -1),
        ("branch_floor_pct", "95"),
    ],
)
def test_strict_config_rejects_non_numeric_or_out_of_range_floors(
    tmp_path: Path,
    field: str,
    value: object,
) -> None:
    _seed(tmp_path, "src/a.py", "value = 1\n")
    with pytest.raises(ValueError, match="finite percentage"):
        build({"roots": ["src"], "branch_floor_pct": 95, field: value}, repo_root=tmp_path)


def test_receipt_mode_resolves_report_and_rejects_missing_execution_identity(tmp_path: Path) -> None:
    _strict_fixture(tmp_path, {"src/a.py": ("value = 1\n", (1,), None)})
    rule = build(
        {
            "roots": ["src"],
            "branch_floor_pct": 95,
            "coverage_receipt": "receipt.json",
            "coverage_report": "coverage.xml",
        },
        repo_root=tmp_path,
    )

    with pytest.raises(ValueError, match="non-empty execution input"):
        rule.run()


def test_strict_noncritical_branch_floor_reports_partial_branch_paths(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _strict_fixture(
        tmp_path,
        {
            "src/ordinary.py": (
                "if enabled:\n    result = 1\nelse:\n    result = 0\n",
                (1, 1, 1),
                (1, 2),
            ),
        },
    )
    rule = build({"roots": ["src"], "floor_pct": 95, "branch_floor_pct": 95}, repo_root=tmp_path)

    assert rule.run() == 1
    assert "branch coverage 50% below 95%" in capsys.readouterr().out


def test_strict_coverage_requires_complete_line_and_critical_branch_measurement(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _strict_fixture(
        tmp_path,
        {
            "src/critical.py": (
                "extra = 2\nif enabled:\n    result = 1\nelse:\n    result = 0\n",
                (1, 1, 0, 0),
                (1, 2),
            ),
        },
    )
    rule = build(
        {
            "roots": ["src"],
            "floor_pct": 95,
            "branch_floor_pct": 95,
            "critical_branch_files": ["src/critical.py"],
        },
        repo_root=tmp_path,
    )

    assert rule.collect_violations() == {Path("src/critical.py")}
    assert rule.run() == 1
    output = capsys.readouterr().out
    assert "line coverage 50% below 95%" in output
    assert "critical branch coverage 50% below 100%" in output


def test_strict_coverage_accepts_complete_tree_with_all_critical_exits(tmp_path: Path) -> None:
    _strict_fixture(
        tmp_path,
        {
            "src/critical.py": (
                "if enabled:\n    result = 1\nelse:\n    result = 0\n",
                (1, 1, 1),
                (2, 2),
            ),
            "src/plain.py": ("value = 1\n", (1,), None),
        },
    )
    rule = build(
        {
            "roots": ["src"],
            "floor_pct": 95,
            "branch_floor_pct": 95,
            "critical_branch_files": ["src/critical.py"],
        },
        repo_root=tmp_path,
    )

    assert rule.run() == 0
    assert rule.collect_violations() == set()
    assert (
        parse_coverage_details(tmp_path / "coverage.xml", repo_root=tmp_path)["src/critical.py"].branch_pct
        == 100
    )


def test_strict_coverage_rejects_a_report_that_drops_a_branch_the_source_has(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """A self-consistent report is still not evidence if the source disagrees."""
    report = _strict_fixture(
        tmp_path,
        {
            "src/partial.py": (
                "if enabled:\n    result = 1\nelse:\n    result = 0\n",
                (1, 1, 1),
                (1, 2),
            ),
        },
    )
    report.write_text(
        report.read_text()
        .replace(' branch="true" condition-coverage="50% (1/2)"', "")
        .replace('branch-rate="0.5"', 'branch-rate="1"')
        .replace('branches-valid="2" branches-covered="1"', 'branches-valid="0" branches-covered="0"')
    )
    rule = build({"roots": ["src"], "floor_pct": 95, "branch_floor_pct": 95}, repo_root=tmp_path)

    assert rule.run() == 1
    assert "branch inventory disagrees with source opportunities" in capsys.readouterr().out


def test_strict_coverage_rejects_a_report_that_drops_an_executable_line(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Omitting an uncovered statement would otherwise raise the file's rate."""
    report = _strict_fixture(tmp_path, {"src/partial.py": ("a = 1\nb = 2\n", (1, 0), None)})
    report.write_text(
        report.read_text()
        .replace('<line number="2" hits="0"/>', "")
        .replace('line-rate="0.5"', 'line-rate="1"')
        .replace('lines-valid="2" lines-covered="1"', 'lines-valid="1" lines-covered="1"')
    )
    rule = build({"roots": ["src"], "floor_pct": 95, "branch_floor_pct": 95}, repo_root=tmp_path)

    assert rule.run() == 1
    assert "omits or invents executable source lines" in capsys.readouterr().out


def test_strict_coverage_reports_source_omitted_from_real_report(tmp_path: Path) -> None:
    _strict_fixture(
        tmp_path,
        {
            "src/measured.py": ("value = 1\n", (1,), None),
            "src/omitted.py": ("value = 2\n", (1,), None),
        },
    )
    report = _strict_report({"src/measured.py": ((1,), None)})
    _seed(tmp_path, "coverage.xml", report)
    rule = build({"roots": ["src"], "floor_pct": 95, "branch_floor_pct": 95}, repo_root=tmp_path)

    assert rule.collect_violations() == {Path("src/omitted.py")}
    assert rule.run() == 1


@pytest.mark.parametrize(
    ("config", "message"),
    [
        ({"roots": ["src"], "coverage_receipt": "receipt.json"}, "independent branch coverage"),
        ({"roots": ["src"], "branch_floor_pct": True}, "finite percentage"),
        ({"roots": ["src"], "branch_floor_pct": 101}, "finite percentage"),
        ({"roots": ["src"], "branch_floor_pct": float("nan")}, "finite percentage"),
        ({"roots": ["src"], "critical_branch_files": ["src/a.py"]}, "require branch_floor_pct"),
        ({"roots": ["src"], "branch_floor_pct": 95, "critical_branch_files": "src/a.py"}, "must be a list"),
        (
            {"roots": ["src"], "branch_floor_pct": 95, "critical_branch_files": ["../outside.py"]},
            "must exist within",
        ),
        (
            {"roots": ["src"], "branch_floor_pct": 95, "critical_branch_files": ["coverage.xml"]},
            "must exist within",
        ),
        (
            {"roots": ["src"], "branch_floor_pct": 95, "exempt_files": ["src/a.py"]},
            "exempt_files is not supported",
        ),
        ({"roots": ["/tmp"], "branch_floor_pct": 95}, "repository-relative source roots"),
        ({"roots": ["../outside"], "branch_floor_pct": 95}, "repository-relative source roots"),
        ({"roots": ["missing"], "branch_floor_pct": 95}, "repository-relative source roots"),
    ],
)
def test_strict_config_rejects_invalid_measurement_contracts(
    tmp_path: Path,
    config: dict[str, object],
    message: str,
) -> None:
    _seed(tmp_path, "src/a.py", "value = 1\n")
    with pytest.raises(ValueError, match=message):
        build(config, repo_root=tmp_path)


def test_strict_coverage_rejects_an_empty_source_root(tmp_path: Path) -> None:
    _seed(tmp_path, "src/.keep", "")
    _seed(tmp_path, "outside.py", "value = 1\n")
    _seed(tmp_path, "coverage.xml", _strict_report({"outside.py": ((1,), None)}))
    rule = build({"roots": ["src"], "floor_pct": 95, "branch_floor_pct": 95}, repo_root=tmp_path)

    with pytest.raises(ValueError, match="contain no Python files"):
        rule.collect_violations()


def test_strict_coverage_rejects_report_totals_that_disagree_with_file_detail(tmp_path: Path) -> None:
    source = _seed(tmp_path, "src/a.py", "value = 1\n")
    report = _seed(
        tmp_path,
        "coverage.xml",
        _strict_report({"src/a.py": ((1,), None)}).replace('lines-covered="1"', 'lines-covered="0"'),
    )

    with pytest.raises(ValueError, match="totals disagree"):
        parse_coverage_details(report, repo_root=source.parents[1])


def test_python_module_entrypoint_accepts_a_real_coverage_report(tmp_path: Path) -> None:
    _seed(tmp_path, "coverage.xml", _report({"a.py": 1.0}))
    source_root = Path(__file__).parents[1] / "src"
    result = subprocess.run(
        [sys.executable, "-m", "tc_fitness.core_checks.coverage_floor", "--repo-root", str(tmp_path)],
        capture_output=True,
        check=False,
        text=True,
        env={**os.environ, "PYTHONPATH": str(source_root)},
    )

    assert result.returncode == 0, result.stderr


def test_no_repo_strings_in_executable_code() -> None:
    import tc_fitness.core_checks.coverage_floor as mod

    _assert_no_repo_identity(Path(mod.__file__))


def _assert_no_repo_identity(module_file: Path) -> None:
    text = module_file.read_text(encoding="utf-8")
    tree = ast.parse(text)
    docstring_ids = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and node.body:
            first = node.body[0]
            if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant):
                docstring_ids.add(id(first.value))
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in docstring_ids:
            lowered = node.value.lower()
            for tok in ("kairix", "tc-agent-zone", "agent-zone", "kata"):
                assert tok not in lowered, f"repo identity leaked in a code literal: {tok}"


def test_an_external_coverage_report_is_keyed_inside_the_repository(tmp_path: Path) -> None:
    """An external report is legitimate; its finding still has to relativise."""
    external = tmp_path / "evidence" / "coverage.xml"
    external.parent.mkdir()
    repo = tmp_path / "repo"
    repo.mkdir()
    rule = build({"coverage_report": str(external)}, repo_root=repo)

    assert rule.enumerate_files() == [repo / "coverage.xml"]


def test_strict_mode_reads_exact_counts_not_the_rounded_summary(tmp_path: Path) -> None:
    """A file at 94.996% is written as 0.95 and would clear a 95% floor it misses."""
    source = tmp_path / "src" / "subject.py"
    source.parent.mkdir(parents=True)
    source.write_text("def f(x):\n    if x:\n        return 1\n    return 0\n", encoding="utf-8")
    (tmp_path / "coverage.xml").write_text(
        '<coverage lines-valid="4" lines-covered="4" branches-valid="2" branches-covered="2" '
        'line-rate="1.0" branch-rate="1.0"><sources><source>.</source></sources><packages><package>'
        '<classes><class filename="src/subject.py" line-rate="1.0" branch-rate="1.0"><lines>'
        '<line number="1" hits="1"/><line number="2" hits="1" branch="true" '
        'condition-coverage="100% (2/2)"/><line number="3" hits="1"/><line number="4" hits="1"/>'
        "</lines></class></classes></package></packages></coverage>\n",
        encoding="utf-8",
    )
    rule = build(
        {"roots": ["src"], "floor_pct": 95, "branch_floor_pct": 95, "coverage_report": "coverage.xml"},
        repo_root=tmp_path,
    )

    assert rule._coverage == {"src/subject.py": 100.0}


def test_a_report_inside_the_repository_keeps_its_relative_identity(tmp_path: Path) -> None:
    """The in-repository path is the ordinary case and must relativise unchanged."""
    rule = build({"coverage_report": "reports/coverage.xml"}, repo_root=tmp_path)

    assert rule._report_key() == Path("reports/coverage.xml")
