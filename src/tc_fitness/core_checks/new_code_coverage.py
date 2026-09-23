"""CORE check: new_code_coverage — coverage floor on the CHANGED lines only.

A repo-wide (or even per-file) coverage floor still lets a change land uncovered
so long as the file's *aggregate* rate stays above the bar: a well-covered file
absorbs a block of new, untested lines without dipping under the floor. The
merge gate SonarCloud enforces closes that gap by scoring "new code" in
isolation — the lines a branch ADDED or CHANGED versus the trunk — and blocking
when their coverage is below a floor (100% by default). This rule mirrors that
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

Hard floor, by design: new code that misses the threshold always fails.

Standard mode delegates changed-line calculation and report matching to
``diff-cover``. The floor, report path, trunk ref, and scan roots are CONFIG the
consumer supplies; nothing here names a repo, a source package, or a threshold
beyond the domain-intrinsic default. A configured remote-tracking trunk ref is
refreshed before the merge-base is resolved; failure is blocking so stale local
state cannot produce a false pass. The git invocation is a DI seam (a callable
defaulting to :func:`subprocess.run`) so the detector is testable without a real
repository.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any
from xml.etree import ElementTree

from tc_fitness.check_evidence import report_finding
from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: The domain-intrinsic default floor for new code — SonarCloud's own default
#: "Coverage on New Code" condition. Overridable per consumer via ``floor_pct``.
DEFAULT_FLOOR_PCT = 100.0

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
        "proves the new behaviour. The only way through is a real test."
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
    et = element_tree if element_tree is not None else ElementTree
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

    def file_has_violation(self, path: Path) -> bool:
        """Reject the per-file API: this rule is one atomic changed-line gate."""
        raise RuntimeError("new-code coverage must be evaluated with run(), not file_has_violation()")

    def _refresh_remote_base(self) -> bool:
        """Refresh a configured remote-tracking base before resolving it.

        Local refs and revisions are left untouched. A failed fetch is visible
        and blocking because a stale remote-tracking ref is not admissible
        changed-line evidence.
        """
        remotes = self.git_runner(["remote"], self._repo_root)
        if remotes.returncode != 0:
            return False
        names = sorted(_decode_git_output(remotes.stdout).splitlines(), key=len, reverse=True)
        remote = next((name for name in names if self.base_ref.startswith(f"{name}/")), None)
        if remote is None:
            return True
        branch = self.base_ref[len(remote) + 1 :]
        if not branch or not re.fullmatch(r"[A-Za-z0-9_./-]+", branch):
            return False
        refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
        fetched = self.git_runner(
            ["fetch", "--quiet", "--no-tags", "--", remote, refspec],
            self._repo_root,
        )
        if fetched.returncode == 0:
            return True
        detail = _decode_git_output(fetched.stderr).strip().splitlines()
        reason = detail[-1] if detail else f"git fetch exited {fetched.returncode}"
        print(
            f"warning [arch:{self._name}] — could not refresh {self.base_ref}: {reason}",
            file=sys.stderr,
        )
        return False

    def run(self) -> int:
        """Run the standard diff-cover changed-line gate, failing closed."""
        if self.exact_config is not None:
            from tc_fitness.coverage_admission import changed_line_failures

            failures = changed_line_failures(self._repo_root, self.exact_config)
            for relative, message in failures.items():
                report_finding(self.name, relative, message)
                print(f"FAIL [{self.name}] {relative}: {message}")
            return int(bool(failures))

        report = self._report_path()
        if not report.is_file():
            return self._fail(f"coverage report is missing: {report}")
        try:
            covered_paths = parse_line_coverage(report)
        except Exception as exc:
            return self._fail(f"coverage report is unreadable or invalid: {exc}")
        if not covered_paths:
            return self._fail(f"coverage report contains no source file data: {report}")

        if not _SAFE_REF_RE.fullmatch(self.base_ref):
            return self._fail(f"base ref is unsafe or invalid: {self.base_ref!r}")
        if not self._refresh_remote_base():
            return self._fail(f"base ref could not be fetched: {self.base_ref}")
        merge_base = self.git_runner(["merge-base", self.base_ref, "HEAD"], self._repo_root)
        if merge_base.returncode != 0 or not _decode_git_output(merge_base.stdout).strip():
            detail = _decode_git_output(merge_base.stderr).strip() or "git merge-base failed"
            return self._fail(f"base ref is unavailable: {self.base_ref} ({detail})")
        executable = shutil.which("diff-cover")
        if executable is None:
            return self._fail("diff-cover is not installed; sync the locked environment")
        argv = [
            executable,
            str(report),
            "--compare-branch",
            self.base_ref,
            "--fail-under",
            str(self.floor_pct),
            "--include-untracked",
        ]
        try:
            result = subprocess.run(argv, cwd=self._repo_root, capture_output=True, text=True, check=False)
        except Exception as exc:  # diff-cover errors are gate errors, never passes
            return self._fail(f"diff-cover could not evaluate changed Python coverage: {exc}")
        if result.stdout:
            print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, end="", file=sys.stderr)
        if result.returncode != 0:
            message = f"diff-cover changed Python coverage is below {self.floor_pct:g}%"
            report_finding(self._name, ".", message)
            print(f"FAIL [arch:{self._name}] — {message}.")
            print(self.remediation)
            return 1
        print(f"ok [arch:{self._name}] — changed Python coverage clears {self.floor_pct:g}%.")
        return 0

    def _fail(self, message: str) -> int:
        print(f"FAIL [arch:{self._name}] — {message}")
        report_finding(self._name, ".", message)
        print(self.remediation)
        return 1


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
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NewCodeCoverage, argv)


if __name__ == "__main__":
    import sys

    sys.exit(main())
