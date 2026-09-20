"""CORE check: new_code_coverage — coverage floor on the CHANGED lines only.

A repo-wide (or even per-file) coverage floor still lets a change land uncovered
so long as the file's *aggregate* rate stays above the bar: a well-covered file
absorbs a block of new, untested lines without dipping under the floor. The
merge gate SonarCloud enforces closes that gap by scoring "new code" in
isolation — the lines a branch ADDED or CHANGED versus the trunk — and blocking
when their coverage is below a floor (80% by default). This rule mirrors that
condition LOCALLY so an agent catches it before the CI round-trip, not after.

"New code" is the set of right-side lines between the merge base and the current
checkout. That includes committed, staged, unstaged, and untracked source, so a
local pre-push run and CI score the same source tree. For each in-scope changed
file present in the coverage report, the rule intersects those added lines with
the lines the report actually recorded (``coverable_changed``), counts those with
a non-zero hit (``covered_changed``), and FAILS the file when
``covered_changed / coverable_changed`` is below the floor. A file whose added
lines are all non-coverable (blank lines, comments, lines the report never
recorded) contributes no measurable new code and is not a violation.

That is the backwards-compatible consumer mode. Configuring
``exact_base_commit`` / ``candidate_commit`` instead uses strict immutable
coverage admission: complete source-derived executable detail, clean Git
identity, no exemptions and 100 percent changed lines. ``coverage_receipt``
additionally binds the fresh execution and accepted-base monotonic evidence.
Strict-mode missing inputs raise; they never enter the legacy soft-pass path.

Hard floor, by design. Unlike :mod:`coverage_floor`, this rule is baseline-free:
new code is inherently non-grandfatherable (see :meth:`NewCodeCoverage.establish_baseline`).

The floor, the report path, the trunk ref, and the scan roots are CONFIG the
consumer supplies; nothing here names a repo, a source package, or a threshold
beyond the domain-intrinsic default. A configured remote-tracking trunk ref is
refreshed before the merge-base is resolved; an offline refresh failure remains
visible while the cached ref supplies the best available local measurement. The
git invocation is a DI seam (a callable defaulting to :func:`subprocess.run`) so
the detector is testable without a real repository.
"""

from __future__ import annotations

import importlib
import os
import re
import stat
import subprocess
import sys
from collections.abc import Callable, Mapping
from functools import cached_property
from pathlib import Path
from types import ModuleType
from typing import Any

from tc_fitness.baseline import establish_baseline as _establish_baseline
from tc_fitness.check_evidence import report_finding
from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: The domain-intrinsic default floor for new code — SonarCloud's own default
#: "Coverage on New Code" condition. Overridable per consumer via ``floor_pct``.
DEFAULT_FLOOR_PCT = 80.0

#: Default coverage report location relative to the repo root. Overridable.
DEFAULT_COVERAGE_REPORT = "coverage.xml"

#: Default trunk ref the change set is measured against. The changed lines are
#: the right side of the diff from the merge-base of this ref and HEAD.
DEFAULT_BASE_REF = "origin/main"

#: A git ref must match this before it is interpolated into a git argv — a
#: conservative allow-list of the characters a legitimate ref/revision carries
#: (refname chars plus the revision operators ``~ ^ @ { }``). Anything else is
#: treated as unresolvable → the rule SKIPs rather than shell-interpolating it.
_SAFE_REF_RE = re.compile(r"^[A-Za-z0-9_./@{}~^-]+$")

#: ``@@ -old +new @@`` hunk header — capture the new-side start line and count.
_HUNK_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")

#: A git command runner: takes the git sub-arguments (argv0 ``git`` is fixed by
#: the runner, never the caller) and the working directory, returns the
#: completed process. The DI seam a test overrides to feed canned diff output.
GitResult = subprocess.CompletedProcess[str] | subprocess.CompletedProcess[bytes]
GitRunner = Callable[[list[str], Path], GitResult]

REMEDIATION = _remediation(
    fix=(
        "cover the lines this change ADDED — ask what DEFECT CLASS the uncovered "
        "new code proxies (a missing failure-mode test for the new branch, an "
        "unexercised boundary, an untested scale bound) and write the test that "
        "proves the new behaviour. New code is non-grandfatherable: there is no "
        "baseline to append to, so the only way through is a real test."
    ),
    nxt="re-run this check to confirm the changed lines clear the floor.",
    run="python -m tc_fitness.core_checks.new_code_coverage",
    passing="add a test that drives the new branch so its added lines report hits > 0",
    forbidden="pad coverage with a no-op call that executes the new lines without asserting",
)


def _reject_unsafe_xml(text: str, source: str) -> None:
    """Reject DTD/entity declarations before any parser runs (XXE guard)."""
    lowered = text.lower()
    if "<!doctype" in lowered or "<!entity" in lowered:
        raise ValueError(f"unsafe coverage XML at {source}: DTD/entity declarations are not allowed")


def _resolve_element_tree(
    import_module: Callable[[str], ModuleType] = importlib.import_module,
) -> Any:
    """Prefer defusedxml; fall back to stdlib after explicit DTD/entity rejection.

    ``import_module`` is a DI seam so a test can drive either path without
    monkeypatching the production module.
    """
    try:
        from defusedxml import ElementTree as DefusedET

        return DefusedET
    except ImportError:
        return import_module("xml.etree.ElementTree")


def parse_line_coverage(report_path: Path, *, element_tree: Any | None = None) -> dict[str, dict[int, int]]:
    """Return ``{<source>/<filename>: {line_no: hits}}`` from a Cobertura report.

    Cobertura declares ``<source>`` roots and emits ``<class filename=...>``
    with a nested ``<lines><line number=N hits=M/></lines>``. The returned keys
    join the first source root with each class filename so they read as
    repo-relative paths (the shape the changed-line paths and the scan roots
    filter against). When two classes resolve to one key, a line's hits are
    merged with ``max`` (covered anywhere ⇒ covered). A missing report yields an
    empty mapping — the caller decides whether that is in scope.
    """
    if not report_path.exists():
        return {}
    text = report_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(text, str(report_path))
    et = element_tree if element_tree is not None else _resolve_element_tree()
    root = et.parse(report_path).getroot()

    source_roots = [s.text.strip().strip("/") for s in root.iter("source") if s.text and s.text.strip()]
    source_prefix = source_roots[0] if source_roots else ""
    # A "." source root means the class filenames are ALREADY repo-relative — the
    # shape pytest-cov emits when coverage is normalised to a single repo-root
    # source (e.g. a multi-`--cov`-root report collapsed to `<source>.</source>`
    # so Sonar's Cobertura sensor resolves it). Treating "." as a prefix would
    # yield `./<path>` keys that never match the repo-relative changed-line paths,
    # so every changed file reads as "no measurable new code" and the hard floor
    # silently soft-PASSES. Normalise it to an empty prefix.
    if source_prefix == ".":
        source_prefix = ""

    out: dict[str, dict[int, int]] = {}
    for cls in root.iter("class"):
        filename = cls.get("filename") or ""
        if not filename:
            continue
        if source_prefix and not filename.startswith(source_prefix + "/"):
            full = f"{source_prefix}/{filename}"
        else:
            full = filename
        line_hits = out.setdefault(full, {})
        for line_el in cls.iter("line"):
            number = line_el.get("number")
            hits = line_el.get("hits")
            if number is None or hits is None:
                continue
            try:
                line_no = int(number)
                hit_count = int(hits)
            except ValueError:
                continue
            prev = line_hits.get(line_no)
            line_hits[line_no] = hit_count if prev is None else max(prev, hit_count)
    return out


def _strip_diff_prefix(target: str) -> str:
    """Drop git's ``a/`` / ``b/`` diff path prefix (default ``diff.prefix``)."""
    if target.startswith(("a/", "b/")):
        return target[2:]
    return target


def parse_added_lines(diff_text: str) -> dict[str, set[int]]:
    """Return ``{repo_relative_path: {added_line_no, ...}}`` from a unified diff.

    Parses ``git diff`` hunks for right-side (added) line numbers per file. A
    ``+++ /dev/null`` target (a deletion) contributes nothing; a ``+++ b/<path>``
    target starts a file. Within a hunk the new-side line counter starts at the
    header's new-start and advances on every added (``+``) or context (`` ``)
    line, so the rule works at any ``-U`` context width (``-U0`` simply has no
    context lines). Pure function — a test drives it with literal diff text.
    """
    added: dict[str, set[int]] = {}
    current: str | None = None
    new_line = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git"):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].split("\t", 1)[0].strip()
            current = None if target == "/dev/null" else _strip_diff_prefix(target)
            if current is not None:
                added.setdefault(current, set())
            continue
        if raw.startswith("--- "):
            continue
        if raw.startswith("@@"):
            match = _HUNK_RE.match(raw)
            if match:
                new_line = int(match.group(1))
            continue
        if current is None:
            continue
        if raw.startswith("+"):
            added[current].add(new_line)
            new_line += 1
        elif raw.startswith(" "):
            new_line += 1
        # '-' (removed) and '\' (no-newline marker) lines never advance the
        # new-side counter and are not added lines.
    return added


def _decode_git_output(output: str | bytes) -> str:
    """Decode Git's byte-preserving output without losing valid path bytes."""
    return output if isinstance(output, str) else output.decode("utf-8", "surrogateescape")


def _default_git_runner(args: list[str], cwd: Path) -> subprocess.CompletedProcess[bytes]:
    """Run ``git <args>`` in ``cwd`` and capture its output (the default seam).

    argv0 is the fixed literal ``git`` (never a caller-supplied path) and
    ``shell`` is never used; the only caller-controlled token is the ref, which
    the rule validates against :data:`_SAFE_REF_RE` before it reaches here.
    """
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        check=False,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0", "GCM_INTERACTIVE": "Never"},
    )


class NewCodeCoverage(FitnessRule):
    """Flags changed files whose ADDED lines are covered below the floor."""

    name = "new-code-coverage"
    remediation = REMEDIATION
    extensions = (".py",)

    #: Rule-specific knobs — instance attrs so ``from_config`` overrides them.
    floor_pct: float = DEFAULT_FLOOR_PCT
    coverage_report: str = DEFAULT_COVERAGE_REPORT
    base_ref: str = DEFAULT_BASE_REF
    #: The git command runner (DI seam) — set by ``from_config`` / ``build`` so a
    #: test can inject canned diff output without a real repo or monkeypatching.
    git_runner: GitRunner
    exact_config: dict[str, Any] | None = None

    @classmethod
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NewCodeCoverage:
        """Build from config, also reading ``floor_pct`` / ``coverage_report`` / ``base_ref``."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NewCodeCoverage)  # noqa: S101  # narrowing for mypy
        rule.floor_pct = float(config.get("floor_pct", DEFAULT_FLOOR_PCT))
        rule.coverage_report = str(config.get("coverage_report", DEFAULT_COVERAGE_REPORT))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.git_runner = _default_git_runner
        if any(key in config for key in ("exact_base_commit", "candidate_commit", "coverage_receipt")):
            rule.exact_config = dict(config)
        return rule

    def _report_path(self) -> Path:
        report = Path(self.coverage_report)
        return report if report.is_absolute() else self._repo_root / report

    def _refresh_remote_base(self) -> None:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        but non-blocking: the cached remote-tracking ref still gives an offline
        run the best available coverage measurement.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}; using cached ref: {reason}",
            file=sys.stderr,
        )

    def _changed_lines(self) -> dict[str, set[int]]:
        """Added lines from the merge-base through the current checkout.

        A remote-tracking base is refreshed first. Refresh failure warns and
        continues with the cached ref. Returns ``{}`` (→ a soft PASS) when the
        base ref is unsafe/unresolvable, the merge-base can't be computed, or
        the diff command fails — none of which is a coverage defect.
        """
        if not _SAFE_REF_RE.match(self.base_ref):
            return {}
        self._refresh_remote_base()
        merge_base = self.git_runner(["merge-base", self.base_ref, "HEAD"], self._repo_root)
        if merge_base.returncode != 0:
            return {}
        base = _decode_git_output(merge_base.stdout).strip()
        if not base:
            return {}
        # Comparing the base tree to the checkout includes committed, staged,
        # and unstaged changes. ``base...HEAD`` omits the latter two and made a
        # pre-commit local gate pass code that CI rejected after it was committed.
        diff = self.git_runner(["diff", "-U0", base, "--"], self._repo_root)
        if diff.returncode != 0:
            return {}
        changed = parse_added_lines(_decode_git_output(diff.stdout))
        changed.update(self._untracked_added_lines())
        return changed

    def _untracked_added_lines(self) -> dict[str, set[int]]:
        """All physical lines in untracked, non-ignored, in-scope source files."""
        result = self.git_runner(
            ["ls-files", "--others", "--exclude-standard", "-z", "--"],
            self._repo_root,
        )
        if result.returncode != 0:
            return {}

        added: dict[str, set[int]] = {}
        for rel in _decode_git_output(result.stdout).split("\0"):
            if not rel or Path(rel).is_absolute() or ".." in Path(rel).parts:
                continue
            if not self.is_in_scope(rel):
                continue
            path = self._repo_root / rel
            try:
                if not stat.S_ISREG(path.lstat().st_mode):
                    continue
                line_count = len(path.read_bytes().splitlines())
            except OSError:
                continue
            added[rel] = set(range(1, line_count + 1))
        return added

    @cached_property
    def _measured(self) -> dict[str, tuple[int, int]]:
        """``{repo_relative_path: (covered_changed, coverable_changed)}``.

        Only files with at least one *coverable* changed line (a changed line the
        report recorded) appear — a file with no measurable new code is omitted,
        so it is neither enumerated nor a violation. Cached: the git subprocess
        and the XML parse run once per rule instance.
        """
        changed = self._changed_lines()
        if not changed:
            return {}
        coverage = parse_line_coverage(self._report_path())
        if not coverage:
            return {}
        out: dict[str, tuple[int, int]] = {}
        for rel, lines in changed.items():
            line_hits = coverage.get(rel)
            if not line_hits:
                continue
            coverable = [ln for ln in lines if ln in line_hits]
            if not coverable:
                continue
            covered = sum(1 for ln in coverable if line_hits[ln] > 0)
            out[rel] = (covered, len(coverable))
        return out

    def enumerate_files(self) -> list[Path]:
        """The changed in-scope files with measurable new code, as repo-anchored paths.

        Overrides the default rglob walk: the rule's universe is the changed
        lines that landed in the coverage report, not the on-disk tree. The
        inherited scope predicate (extensions + roots) still applies via
        :meth:`FitnessRule.collect_violations`.
        """
        return [self._repo_root / rel for rel in self._measured]

    def file_has_violation(self, path: Path) -> bool:
        """True iff the file's covered/coverable changed-line ratio is below the floor."""
        rel = str(self._repo_relative(path))
        measured = self._measured.get(rel)
        if measured is None:
            return False
        covered, coverable = measured
        return covered / coverable * 100.0 < self.floor_pct

    def run(self) -> int:
        """Hard-floor gate: every below-floor changed file FAILs, none grandfathered.

        Modelling note: the base ``run()`` gates the violation set against a
        per-file baseline so a repo can freeze PRE-EXISTING offenders behind a
        ratchet. New-code coverage is different in KIND — the "new" line set is
        recomputed against the merge-base on every branch, so there is no stable
        offender to freeze, and an uncovered line ADDED on THIS branch is a fresh
        defect, never inherited debt. This override therefore consults NO
        baseline (not even a hand-crafted one) and gates the raw violation set: a
        HARD floor, mirroring SonarCloud's non-ratchetable "Coverage on New Code"
        merge condition. Returns ``0`` when the changed lines clear the floor (or
        there is no measurable new code), ``1`` otherwise.
        """
        if self.exact_config is not None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = changed_line_failures(self._repo_root, self.exact_config)
            for relative, message in failures.items():
                report_finding(self.name, relative, message)
                print(f"FAIL [{self.name}] {relative}: {message}")
            return int(bool(failures))
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — new code clears the {self.floor_pct:g}% coverage floor.")
            return 0
        print(f"FAIL [arch:{self._name}] — new code below the {self.floor_pct:g}% coverage floor:")
        finding = f"new code below the {self.floor_pct:g}% coverage floor"
        for path in violations:
            report_finding(self._name, self._repo_relative(path).as_posix(), finding)
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def establish_baseline(self) -> Path:
        """Freeze an EMPTY baseline — new-code coverage is non-grandfatherable.

        Modelling note: the base class freezes today's offenders so a repo can
        pay down PRE-EXISTING debt behind a ratchet. New-code coverage has no
        such notion — the "new" line set is recomputed against the merge-base on
        every branch, so a frozen path is meaningless on the next one, and a line
        ADDED on THIS branch that runs uncovered is a FRESH defect, never
        inherited debt. This override freezes the EMPTY set so ``--establish-baseline``
        writes a coherent (empty) file; the hard floor is enforced by
        :meth:`run`, which consults no baseline at all.
        """
        if self.exact_config is not None:
            raise ValueError("exact-base coverage cannot establish a baseline")
        return _establish_baseline(self._name, set(), self._repo_root)


def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
    git_runner: GitRunner | None = None,
) -> NewCodeCoverage:
    """Factory the engine calls to bind this CORE check to a consumer's config.

    ``git_runner`` is the DI seam: production leaves it ``None`` (the rule uses
    :func:`_default_git_runner`), a test passes a fake that returns canned
    ``merge-base`` / ``diff`` output so no real repository is required.
    """
    rule = NewCodeCoverage.from_config(config, repo_root=repo_root)
    if git_runner is not None:
        rule.git_runner = git_runner
    return rule


def main(argv: list[str] | None = None) -> int:
    """CLI entry — supports ``--establish-baseline`` and ``--repo-root``."""
    return run_core_check(NewCodeCoverage, argv)


if __name__ == "__main__":
    import sys

    sys.exit(main())
