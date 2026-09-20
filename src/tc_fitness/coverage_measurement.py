"""Cross-check bound Coverage.py JSON/XML against source-derived branch arcs."""

from __future__ import annotations

import importlib
import json
import re
from pathlib import Path
from typing import Any

from tc_fitness.core_checks._coverage_evidence import CoverageCounts, resolve_coverage_filename


def _integers(value: object) -> set[int]:
    if not isinstance(value, list) or any(type(item) is not int for item in value):
        raise ValueError("coverage JSON requires integer line detail")
    if len(value) != len(set(value)):
        raise ValueError("coverage JSON contains duplicate lines")
    return set(value)


def _arcs(value: object) -> set[tuple[int, int]]:
    if not isinstance(value, list) or any(
        not isinstance(arc, list) or len(arc) != 2 or any(type(line) is not int for line in arc)
        for arc in value
    ):
        raise ValueError("coverage JSON requires branch arc pairs")
    result = {(arc[0], arc[1]) for arc in value}
    if len(result) != len(value):
        raise ValueError("coverage JSON contains duplicate branch arcs")
    return result


def _summary(summary: dict[str, Any], counts: CoverageCounts) -> None:
    expected = {
        "num_statements": counts.lines,
        "covered_lines": counts.covered_lines,
        "missing_lines": counts.lines - counts.covered_lines,
        "excluded_lines": 0,
        "num_branches": counts.branches,
        "covered_branches": counts.covered_branches,
        "missing_branches": counts.branches - counts.covered_branches,
    }
    if any(type(summary.get(key)) is not int or summary[key] != value for key, value in expected.items()):
        raise ValueError("coverage JSON summary counts disagree with source detail")


def declared_branches(root: Path, report: Path) -> dict[str, dict[int, tuple[int, int]]]:
    """Per-file ``line -> (taken, total)`` branch detail an XML report declares."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    declared: dict[str, dict[int, tuple[int, int]]] = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        declared[relative] = branches
    return declared


def source_branch_totals(path: Path) -> dict[int, int]:
    """Branch opportunities Coverage.py derives from the source file itself."""
    parser_type = importlib.import_module("coverage.parser").PythonParser
    parser = parser_type(filename=str(path), exclude=None)
    parser.parse_source()
    return {start: total for start, total in parser.exit_counts().items() if total > 1}


def complete_branch_inventory(root: Path, report: Path, files: dict[str, Path]) -> None:
    """Refuse an XML report whose branch inventory is not the source's own.

    A report can drop a branching line's attributes, restate the summary to
    match, and read as fully covered. The source decides how many branch
    opportunities exist, so a floor is only meaningful once the report's
    inventory is shown to be exactly that set.
    """
    declared = declared_branches(root, report)
    if set(declared) != set(files):
        raise ValueError("coverage report does not measure the complete source set")
    for name, path in files.items():
        totals = {line: total for line, (_, total) in declared[name].items()}
        if totals != source_branch_totals(path):
            raise ValueError("coverage XML branch inventory disagrees with source opportunities: " + name)


def cross_check_branches(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml_branches = declared_branches(root, report)
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)
