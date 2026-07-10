"""CORE check: ci_consumes_shared_gate — CI MUST run the ONE shared quality gate.

Every repo in the fleet MUST route its CI quality gate through the single shared
standard, so "green" means the same thing everywhere and a repo can never drift
onto a privately-forked gate that quietly enforces a weaker bar. A repo satisfies
this by doing at least one of two things in its workflows:

* **Consume the canonical reusable** — a workflow ``uses:`` the shared
  ``three-cubes/tc-pipelines/.github/workflows/python-quality-gate.yml@<ref>``
  reusable (the pinned org quality gate), OR
* **Invoke the shared engine** — a workflow job runs ``tc-fitness run`` (the same
  binary the reusable runs), so the repo drives the shared engine directly.

The rule FAILS a repo that HAS CI workflows but whose workflows do NEITHER — i.e.
the repo runs CI yet forked its own quality gate off the shared standard. It
PASSES a repo whose CI does at least one of the two, and it SKIPS (vacuous pass)
a repo with no CI workflows at all, because there is nothing to enforce.

Non-grandfatherable: a forked gate is a hard repo-level gate, not a per-file
debt, so :meth:`run` drives the two arms directly rather than ratcheting a
violation set against a baseline (the same posture as the harness_canon_reference
and deterministic_tests CORE checks).

Warn → hard adoption path
=========================
A repo mid-onboarding — one that has not yet converged its CI onto the shared
gate — adopts the check in WARN mode first: set ``warn_only = true`` (its alias
``baseline_ok = true`` has the identical effect) in the check's config block. In
WARN mode the check STILL reports the fork loudly but exits ``0``, so the repo
lands the check in its catalogue without a day-one red build, converges its CI,
then flips the flag off to hard-enforce. The default is HARD: a fork exits ``1``.

Repo-agnostic: every knob (the workflows directory, the reusable-reference
regex, the engine-invocation regex, the warn flag) arrives through the
consumer's ``[tool.tc_fitness.core_checks.ci_consumes_shared_gate]`` config
block. The engine bakes in no consumer identity — only the shared-gate surface
every fleet CI is expected to reference.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: The directory (repo-relative) whose workflow files carry the CI definition.
#: Domain-intrinsic default, overridable via config.
DEFAULT_WORKFLOWS_DIR = ".github/workflows"

#: The filename suffixes a GitHub Actions workflow file may carry.
WORKFLOW_SUFFIXES: frozenset[str] = frozenset({".yml", ".yaml"})

#: The regex that identifies a ``uses:`` reference to the canonical reusable
#: quality gate. Matches the pinned-ref form (``…python-quality-gate.yml@<ref>``)
#: so a workflow that consumes the shared reusable at any tag/sha satisfies it.
DEFAULT_REUSABLE_PATTERN = r"three-cubes/tc-pipelines/\.github/workflows/python-quality-gate\.yml@"

#: The regex that identifies an invocation of the shared engine. Matches a step
#: that runs ``tc-fitness run`` (however wrapped, e.g. ``uv run tc-fitness run``).
DEFAULT_ENGINE_PATTERN = r"\btc-fitness run\b"

#: The label reported when the reusable arm proves consumption.
_REUSABLE_LABEL = "reusable-workflow (python-quality-gate.yml)"

#: The label reported when the engine arm proves consumption.
_ENGINE_LABEL = "shared-engine (tc-fitness run)"

REMEDIATION = _remediation(
    fix=(
        "make CI consume the ONE shared quality gate via either acceptable path: "
        "(a) add a workflow job that `uses:` the canonical reusable "
        "`three-cubes/tc-pipelines/.github/workflows/python-quality-gate.yml@<tag>` "
        "(pin a tag, never @main), OR (b) add a job step that runs `tc-fitness run` "
        "(the shared engine). Do NOT fork a private quality gate — converge up to "
        "the shared standard. See the tc-pipelines "
        "governance/standards/improving-fitness-gates.md standard for the "
        "converge-up + adoption path; onboard in WARN mode first with "
        "`warn_only = true`."
    ),
    nxt="re-run this check to confirm CI now consumes the shared gate.",
    run="python -m tc_fitness.core_checks.ci_consumes_shared_gate",
    passing="ci.yml → 'uses: …/python-quality-gate.yml@v1.13.0'  OR  'run: uv run tc-fitness run'",
    forbidden="ci.yml → a hand-rolled gate (no reusable reference, no `tc-fitness run` step)",
)


def workflow_files(workflows_dir: Path) -> list[Path]:
    """Return the workflow YAML files directly under ``workflows_dir``, sorted.

    Pure helper (the enumeration core) so tests can assert on it directly. Only
    the immediate children are considered — GitHub Actions reads workflow files
    from the top level of ``.github/workflows`` — and a non-existent directory
    yields the empty list (the SKIP signal).
    """
    if not workflows_dir.is_dir():
        return []
    return [
        path
        for path in sorted(workflows_dir.iterdir())
        if path.is_file() and path.suffix in WORKFLOW_SUFFIXES
    ]


def satisfying_mechanism(
    text: str,
    *,
    reusable_pattern: re.Pattern[str],
    engine_pattern: re.Pattern[str],
) -> tuple[str, int, str] | None:
    """Return ``(mechanism, line_no, line)`` proving ``text`` consumes the gate.

    Pure helper (the detection core). Scans for the reusable-reference arm first
    (the stronger ``uses:`` signal), then the engine-invocation arm, so a
    workflow that carries both reports the reusable path. Returns ``None`` when
    the workflow proves NEITHER — the fork signal.
    """
    for label, pattern in ((_REUSABLE_LABEL, reusable_pattern), (_ENGINE_LABEL, engine_pattern)):
        for line_no, line in enumerate(text.splitlines(), start=1):
            if pattern.search(line):
                return (label, line_no, line.strip())
    return None


class CiConsumesSharedGate(FitnessRule):
    """Gate that FAILS when a repo's CI forks its own quality gate off the shared standard.

    Drives the two arms (reusable-reference, engine-invocation) directly in
    :meth:`run`; the per-file scan hooks are inert because a forked gate is a
    hard repo-level gate, not a grandfatherable per-file debt.
    """

    name = "ci-consumes-shared-gate"
    remediation = REMEDIATION
    #: Not a file-scan rule — the enumeration hooks stay empty so the base
    #: --establish-baseline mode writes an empty baseline harmlessly.
    extensions = ()

    #: Rule-specific config (instance attrs; from_config overrides per consumer).
    workflows_dir: str = DEFAULT_WORKFLOWS_DIR
    reusable_pattern: str = DEFAULT_REUSABLE_PATTERN
    engine_pattern: str = DEFAULT_ENGINE_PATTERN
    warn_only: bool = False

    @classmethod
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        rule.reusable_pattern = str(config.get("reusable_pattern", DEFAULT_REUSABLE_PATTERN))
        rule.engine_pattern = str(config.get("engine_pattern", DEFAULT_ENGINE_PATTERN))
        # WARN mode: either flag name puts the check in report-but-pass mode.
        # `warn_only` is canonical; `baseline_ok` is its accepted alias so a repo
        # that has "baselined" its current forked CI adopts the same soft mode.
        rule.warn_only = bool(config.get("warn_only", False)) or bool(config.get("baseline_ok", False))
        return rule

    def file_has_violation(self, path: Path) -> bool:  # pragma: no cover - not used
        """Unused: a forked CI gate is a repo-level gate, not a per-file scan."""
        return False

    def _compile_patterns(self) -> tuple[re.Pattern[str], re.Pattern[str]] | str:
        """Compile both configured regexes; return them, or an error label."""
        try:
            reusable_re = re.compile(self.reusable_pattern)
        except re.error as exc:
            return f"reusable_pattern is not a valid regex ({exc})"
        try:
            engine_re = re.compile(self.engine_pattern)
        except re.error as exc:
            return f"engine_pattern is not a valid regex ({exc})"
        return (reusable_re, engine_re)

    def _first_satisfying(
        self,
        files: list[Path],
        reusable_re: re.Pattern[str],
        engine_re: re.Pattern[str],
    ) -> tuple[Path, str, int, str] | None:
        """Return the first workflow that consumes the shared gate, else None."""
        for path in files:
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            hit = satisfying_mechanism(text, reusable_pattern=reusable_re, engine_pattern=engine_re)
            if hit is not None:
                mechanism, line_no, line = hit
                return (path, mechanism, line_no, line)
        return None

    def run(self) -> int:
        """Drive the two arms; SKIP when no CI, PASS on consumption, else FAIL."""
        workflows_dir = self._repo_root / self.workflows_dir
        files = workflow_files(workflows_dir)

        if not files:
            print(
                f"ok [{self._name}] — skipped: no CI workflows under "
                f"{self.workflows_dir!r} (nothing to enforce)."
            )
            return 0

        compiled = self._compile_patterns()
        if isinstance(compiled, str):
            print(f"FAIL [{self._name}] — a configured pattern is not a valid regex:")
            print(f"  - {compiled}")
            print()
            print(self.remediation)
            return 1
        reusable_re, engine_re = compiled

        satisfied = self._first_satisfying(files, reusable_re, engine_re)
        if satisfied is not None:
            path, mechanism, line_no, line = satisfied
            rel = self._repo_relative(path)
            print(
                f"ok [{self._name}] — CI consumes the shared quality gate via "
                f"{mechanism}: {rel}:{line_no}  ({line})."
            )
            return 0

        scanned = ", ".join(sorted(path.name for path in files))
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(
            f"  - {len(files)} workflow file(s) under {self.workflows_dir!r} "
            f"({scanned}), and NONE consumes the shared gate."
        )
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        if self.warn_only:
            print()
            print(
                f"warn-only [{self._name}] — reported above but NOT failing the build "
                f"(warn_only adoption mode). Converge CI onto the shared gate, then "
                f"remove warn_only to hard-enforce."
            )
            return 0
        return 1


def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> CiConsumesSharedGate:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CiConsumesSharedGate.from_config(config, repo_root=repo_root)


def main(argv: list[str] | None = None) -> int:
    """CLI entry — supports ``--establish-baseline`` and ``--repo-root``."""
    return run_core_check(CiConsumesSharedGate, argv)


if __name__ == "__main__":
    import sys

    sys.exit(main())
