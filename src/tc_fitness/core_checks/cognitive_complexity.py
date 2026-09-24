"""CORE check: cognitive_complexity — Sonar S3776 (Campbell).

Cognitive complexity measures how hard a function is to *read*, not how hard
it is to test. The score climbs with each branch (``if`` / ``elif`` / ``else``
/ ``for`` / ``while`` / ``try`` / ``except`` / ternary / boolean operator) and
is amplified by nesting depth — a triple-nested ``if`` is harder to follow
than three sequential ones. The merge gate compares qualified function scores
with the merge base: a new over-threshold function or an existing function that
worsens above the threshold is flagged, while unchanged legacy debt does not
need a stored exception list. The file is the unit reported.

Ported from kairix ``scripts/checks/check_cognitive_complexity.py`` (F16) and
re-expressed as a configurable, repo-agnostic rule: the only domain-intrinsic
number is S3776's own default ceiling (15), exposed as a ``threshold`` knob the
consumer overrides via ``[tool.tc_fitness]``. The comparison ref is also
configurable. No repo paths or globs are baked in — the consumer supplies
``roots``.
"""

from __future__ import annotations

import ast
import io
import re
import shutil
import subprocess
import tarfile
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tc_fitness.check_evidence import report_finding
from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import gate
from tc_fitness.lib import remediation as _remediation

#: S3776's own default ceiling — domain-intrinsic, not repo identity. Overridable.
DEFAULT_THRESHOLD = 15
DEFAULT_BASE_REF = "origin/main"
_SAFE_REF_RE = re.compile(r"^[A-Za-z0-9_./@{}~^-]+$")

REMEDIATION = _remediation(
    fix=(
        "pick the most-nested branch in the flagged function and extract it "
        "into a named helper; or replace an if/elif chain with a dispatch "
        "dict; or invert a guard so the happy path returns early."
    ),
    nxt="re-run this check to confirm the gate goes green.",
    run="python -m tc_fitness.core_checks.cognitive_complexity",
    passing="handler = _HANDLERS.get(cmd, _default); return handler(args)",
    forbidden="nested if/elif chains scoring above the cognitive-complexity ceiling",
)


class _Scorer(ast.NodeVisitor):
    """Accumulate a cognitive-complexity score for one function body.

    The ``nesting`` counter rises on every branch construct and is added to
    each subsequent branch encountered inside it (the nesting amplifier).
    """

    def __init__(self) -> None:
        self.score = 0
        self.nesting = 0

    def _bump(self) -> None:
        self.score += 1 + self.nesting

    def _walk_nested(self, body: list[ast.stmt]) -> None:
        self.nesting += 1
        for child in body:
            self.visit(child)
        self.nesting -= 1

    def visit_If(self, node: ast.If) -> None:
        self._bump()
        self.visit(node.test)
        self._walk_nested(node.body)
        if node.orelse:
            # An ``elif`` is a single nested If in orelse — recurse so it is
            # counted once; a plain ``else`` body bumps and nests.
            if len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If):
                self.visit(node.orelse[0])
            else:
                self._bump()
                self._walk_nested(node.orelse)

    def visit_For(self, node: ast.For) -> None:
        self._bump()
        self._walk_nested(node.body)
        if node.orelse:
            self._walk_nested(node.orelse)

    def visit_AsyncFor(self, node: ast.AsyncFor) -> None:
        self._bump()
        self._walk_nested(node.body)
        if node.orelse:
            self._walk_nested(node.orelse)

    def visit_While(self, node: ast.While) -> None:
        self._bump()
        self.visit(node.test)
        self._walk_nested(node.body)
        if node.orelse:
            self._walk_nested(node.orelse)

    def visit_Try(self, node: ast.Try) -> None:
        self._bump()
        self._walk_nested(node.body)
        for handler in node.handlers:
            self._bump()
            self._walk_nested(handler.body)
        if node.orelse:
            self._walk_nested(node.orelse)
        if node.finalbody:
            self._walk_nested(node.finalbody)

    def visit_With(self, node: ast.With) -> None:
        # ``with`` does not branch, so it adds nothing to the score.
        self.generic_visit(node)

    def visit_AsyncWith(self, node: ast.AsyncWith) -> None:
        self.generic_visit(node)

    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        # A chain ``a and b and c`` has two operators → +2 (flat, no amplifier).
        self.score += max(len(node.values) - 1, 0)
        self.generic_visit(node)

    def visit_IfExp(self, node: ast.IfExp) -> None:
        self._bump()
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self.generic_visit(node)


def _score_function(func: ast.FunctionDef | ast.AsyncFunctionDef) -> int:
    scorer = _Scorer()
    for stmt in func.body:
        scorer.visit(stmt)
    return scorer.score


def _function_scores(source: str, *, filename: str = "<source>") -> dict[str, int]:
    """Return complexity by qualified lexical function identity."""
    try:
        tree = ast.parse(source, filename=filename)
    except (SyntaxError, UnicodeDecodeError):
        return {}

    scores: dict[str, int] = {}

    def visit_definition(child: ast.AST, prefix: str, counts: dict[str, int]) -> None:
        if isinstance(child, ast.ClassDef):
            ordinal = counts.get(child.name, 0)
            counts[child.name] = ordinal + 1
            class_name = f"{child.name}#{ordinal}"
            visit_scope(child, f"{prefix}.{class_name}" if prefix else class_name)
            return
        if isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef):
            ordinal = counts.get(child.name, 0)
            counts[child.name] = ordinal + 1
            function_name = f"{child.name}#{ordinal}"
            identity = f"{prefix}.{function_name}" if prefix else function_name
            scores[identity] = _score_function(child)
            visit_scope(child, identity)
            return
        for descendant in ast.iter_child_nodes(child):
            visit_definition(descendant, prefix, counts)

    def visit_scope(
        node: ast.Module | ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef, prefix: str
    ) -> None:
        counts: dict[str, int] = {}
        for child in node.body:
            visit_definition(child, prefix, counts)

    visit_scope(tree, "")
    return scores


def _regressed_functions(previous: dict[str, int], current: dict[str, int], *, threshold: int) -> bool:
    """Return whether current source adds or worsens an over-threshold function."""
    return any(
        score > threshold
        and (identity not in previous or previous[identity] <= threshold or score > previous[identity])
        for identity, score in current.items()
    )


def module_over_threshold(path: Path, *, threshold: int) -> bool:
    """True iff any function in ``path`` scores above ``threshold``.

    Pure helper (the detection core) so tests assert on it directly. A syntax /
    decode error is treated as "no violation" — another check owns unparseable
    files.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _score_function(node) > threshold:
            return True
    return False


class CognitiveComplexity(FitnessRule):
    """Fail only when this change adds or worsens an over-threshold function."""

    name = "cognitive-complexity"
    remediation = REMEDIATION
    extensions = (".py",)

    #: Rule-specific knob — S3776's own ceiling; overridable per consumer.
    threshold: int = DEFAULT_THRESHOLD
    base_ref: str = DEFAULT_BASE_REF
    _base_error: str | None = None
    _scan_error: str | None = None

    @classmethod
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CognitiveComplexity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CognitiveComplexity)  # noqa: S101  # narrowing for mypy
        rule.threshold = int(config.get("threshold", DEFAULT_THRESHOLD))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule._base_error = None
        rule._scan_error = None
        return rule

    def file_has_violation(self, path: Path) -> bool:
        baseline = self._baseline_sources()
        if isinstance(baseline, str):
            self._base_error = baseline
            return True
        relative = self._repo_relative(path).as_posix()
        previous = _function_scores(baseline.get(relative, ""), filename=relative)
        current = _function_scores(path.read_text(encoding="utf-8"), filename=relative)
        return _regressed_functions(previous, current, threshold=self.threshold)

    def enumerate_files(self) -> list[Path]:
        """Enumerate tracked and nonignored untracked source from the index view."""
        self._scan_error = None
        git = shutil.which("git")
        if git is None:
            self._scan_error = "git is unavailable; install git to enumerate source files"
            return []
        try:
            result = subprocess.run(  # noqa: S603  # executable is resolved; fixed argv
                [git, "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
                cwd=self._repo_root,
                capture_output=True,
                check=False,
                timeout=30,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            self._scan_error = f"could not enumerate source files with git ls-files: {exc}"
            return []
        if result.returncode:
            detail = result.stderr.decode("utf-8", "replace").strip() or "git ls-files failed"
            self._scan_error = f"could not enumerate source files with git ls-files: {detail}"
            return []
        paths: set[Path] = set()
        for raw_path in result.stdout.split(b"\x00"):
            if not raw_path:
                continue
            relative = raw_path.decode("utf-8", "surrogateescape")
            if not relative.endswith(self._extensions) or not self.is_in_scope(relative):
                continue
            path = self._repo_root / relative
            if not path.is_file() or path.is_symlink():
                continue
            resolved = path.resolve()
            if resolved.is_relative_to(self._repo_root):
                paths.add(resolved)
        return sorted(paths)

    def _baseline_sources(self) -> dict[str, str] | str:
        """Read scoped source from one immutable merge-base archive or return its error."""
        if not _SAFE_REF_RE.fullmatch(self.base_ref) or self.base_ref.startswith("-"):
            return f"base ref is unsafe or invalid: {self.base_ref!r}; set a valid base_ref"
        git = shutil.which("git")
        if git is None:
            return (
                "git is unavailable; install git to compare cognitive complexity with the configured base_ref"
            )
        verified = subprocess.run(  # noqa: S603  # validated git ref; argv, not shell
            [git, "rev-parse", "--verify", "--end-of-options", f"{self.base_ref}^{{commit}}"],
            cwd=self._repo_root,
            capture_output=True,
            text=True,
            check=False,
        )
        if verified.returncode:
            detail = verified.stderr.strip() or "git could not resolve the configured ref"
            return f"base ref is unavailable: {self.base_ref} ({detail}); fetch or configure base_ref"
        merge_base = subprocess.run(  # noqa: S603  # resolved commit; argv, not shell
            [git, "merge-base", "--all", verified.stdout.strip(), "HEAD"],
            cwd=self._repo_root,
            capture_output=True,
            text=True,
            check=False,
        )
        bases = merge_base.stdout.splitlines()
        if merge_base.returncode or len(bases) != 1:
            detail = merge_base.stderr.strip() or "merge base is missing or ambiguous"
            return f"could not establish one merge base with {self.base_ref}: {detail}"
        command = [git, "archive", "--format=tar", bases[0], *self._roots]
        archive = subprocess.run(command, cwd=self._repo_root, capture_output=True, check=False)  # noqa: S603  # resolved commit and configured repo paths
        if archive.returncode:
            detail = archive.stderr.decode("utf-8", "replace").strip() or "git archive failed"
            return f"could not read files at merge base with {self.base_ref}: {detail}"
        try:
            with tarfile.open(fileobj=io.BytesIO(archive.stdout), mode="r:") as snapshot:
                return {
                    member.name: extracted.read().decode("utf-8")
                    for member in snapshot.getmembers()
                    if member.isfile()
                    and member.name.endswith(self._extensions)
                    and (extracted := snapshot.extractfile(member)) is not None
                }
        except (tarfile.TarError, UnicodeDecodeError) as exc:
            return f"could not decode the {self.base_ref} source snapshot: {exc}"

    def collect_violations(self) -> set[Path]:
        """Compare working-tree files, including staged and untracked content."""
        baseline = self._baseline_sources()
        if isinstance(baseline, str):
            self._base_error = baseline
            return {Path("base_ref")}
        self._base_error = None
        violations: set[Path] = set()
        paths = self.enumerate_files()
        if self._scan_error:
            return {Path("source_inventory")}
        for path in paths:
            relative = self._repo_relative(path).as_posix()
            try:
                current_text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            previous = _function_scores(baseline.get(relative, ""), filename=relative)
            current = _function_scores(current_text, filename=relative)
            if _regressed_functions(previous, current, threshold=self.threshold):
                violations.add(self._repo_relative(path))
        return violations

    def run(self) -> int:
        violations = self.collect_violations()
        if self._base_error:
            report_finding(self._name, "base_ref", self._base_error, status="error")
            print(f"FAIL [arch:{self._name}] — {self._base_error}")
            return 1
        if self._scan_error:
            report_finding(self._name, "source_inventory", self._scan_error, status="error")
            print(f"FAIL [arch:{self._name}] — {self._scan_error}")
            return 1
        return gate(self._name, violations, self.remediation, repo_root=self._repo_root)


def build(config: Mapping[str, Any], *, repo_root: Path | None = None) -> CognitiveComplexity:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CognitiveComplexity.from_config(config, repo_root=repo_root)


def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(CognitiveComplexity, argv)


if __name__ == "__main__":
    import sys

    sys.exit(main())
