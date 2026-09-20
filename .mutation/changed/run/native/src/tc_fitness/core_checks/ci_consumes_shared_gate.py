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

The rule is a repo-level gate, so :meth:`run` drives both proof arms directly.

Repo-agnostic: every knob (the workflows directory, the reusable-reference
regex, and the engine-invocation regex) arrives through the
consumer's ``[tool.tc_fitness.core_checks.ci_consumes_shared_gate]`` config
block. The engine bakes in no consumer identity — only the shared-gate surface
every fleet CI is expected to reference.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tc_fitness.check_evidence import report_finding
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
        "governance/standards/improving-fitness-gates.md standard."
    ),
    nxt="re-run this check to confirm CI now consumes the shared gate.",
    run="python -m tc_fitness.core_checks.ci_consumes_shared_gate",
    passing="ci.yml → 'uses: …/python-quality-gate.yml@v1.13.0'  OR  'run: uv run tc-fitness run'",
    forbidden="ci.yml → a hand-rolled gate (no reusable reference, no `tc-fitness run` step)",
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x_workflow_files__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_workflow_files__mutmut)
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


def x_workflow_files__mutmut_orig(workflows_dir: Path) -> list[Path]:
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


def x_workflow_files__mutmut_1(workflows_dir: Path) -> list[Path]:
    """Return the workflow YAML files directly under ``workflows_dir``, sorted.

    Pure helper (the enumeration core) so tests can assert on it directly. Only
    the immediate children are considered — GitHub Actions reads workflow files
    from the top level of ``.github/workflows`` — and a non-existent directory
    yields the empty list (the SKIP signal).
    """
    if workflows_dir.is_dir():
        return []
    return [
        path
        for path in sorted(workflows_dir.iterdir())
        if path.is_file() and path.suffix in WORKFLOW_SUFFIXES
    ]


def x_workflow_files__mutmut_2(workflows_dir: Path) -> list[Path]:
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
        for path in sorted(None)
        if path.is_file() and path.suffix in WORKFLOW_SUFFIXES
    ]


def x_workflow_files__mutmut_3(workflows_dir: Path) -> list[Path]:
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
        if path.is_file() or path.suffix in WORKFLOW_SUFFIXES
    ]


def x_workflow_files__mutmut_4(workflows_dir: Path) -> list[Path]:
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
        if path.is_file() and path.suffix not in WORKFLOW_SUFFIXES
    ]

mutants_x_workflow_files__mutmut['_mutmut_orig'] = x_workflow_files__mutmut_orig # type: ignore # mutmut generated
mutants_x_workflow_files__mutmut['x_workflow_files__mutmut_1'] = x_workflow_files__mutmut_1 # type: ignore # mutmut generated
mutants_x_workflow_files__mutmut['x_workflow_files__mutmut_2'] = x_workflow_files__mutmut_2 # type: ignore # mutmut generated
mutants_x_workflow_files__mutmut['x_workflow_files__mutmut_3'] = x_workflow_files__mutmut_3 # type: ignore # mutmut generated
mutants_x_workflow_files__mutmut['x_workflow_files__mutmut_4'] = x_workflow_files__mutmut_4 # type: ignore # mutmut generated
mutants_x_satisfying_mechanism__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_satisfying_mechanism__mutmut)
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


def x_satisfying_mechanism__mutmut_orig(
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


def x_satisfying_mechanism__mutmut_1(
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
        for line_no, line in enumerate(None, start=1):
            if pattern.search(line):
                return (label, line_no, line.strip())
    return None


def x_satisfying_mechanism__mutmut_2(
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
        for line_no, line in enumerate(text.splitlines(), start=None):
            if pattern.search(line):
                return (label, line_no, line.strip())
    return None


def x_satisfying_mechanism__mutmut_3(
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
        for line_no, line in enumerate(start=1):
            if pattern.search(line):
                return (label, line_no, line.strip())
    return None


def x_satisfying_mechanism__mutmut_4(
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
        for line_no, line in enumerate(text.splitlines(), ):
            if pattern.search(line):
                return (label, line_no, line.strip())
    return None


def x_satisfying_mechanism__mutmut_5(
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
        for line_no, line in enumerate(text.splitlines(), start=2):
            if pattern.search(line):
                return (label, line_no, line.strip())
    return None


def x_satisfying_mechanism__mutmut_6(
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
            if pattern.search(None):
                return (label, line_no, line.strip())
    return None

mutants_x_satisfying_mechanism__mutmut['_mutmut_orig'] = x_satisfying_mechanism__mutmut_orig # type: ignore # mutmut generated
mutants_x_satisfying_mechanism__mutmut['x_satisfying_mechanism__mutmut_1'] = x_satisfying_mechanism__mutmut_1 # type: ignore # mutmut generated
mutants_x_satisfying_mechanism__mutmut['x_satisfying_mechanism__mutmut_2'] = x_satisfying_mechanism__mutmut_2 # type: ignore # mutmut generated
mutants_x_satisfying_mechanism__mutmut['x_satisfying_mechanism__mutmut_3'] = x_satisfying_mechanism__mutmut_3 # type: ignore # mutmut generated
mutants_x_satisfying_mechanism__mutmut['x_satisfying_mechanism__mutmut_4'] = x_satisfying_mechanism__mutmut_4 # type: ignore # mutmut generated
mutants_x_satisfying_mechanism__mutmut['x_satisfying_mechanism__mutmut_5'] = x_satisfying_mechanism__mutmut_5 # type: ignore # mutmut generated
mutants_x_satisfying_mechanism__mutmut['x_satisfying_mechanism__mutmut_6'] = x_satisfying_mechanism__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCiConsumesSharedGateǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCiConsumesSharedGateǁ_compile_patterns__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCiConsumesSharedGateǁ_first_satisfying__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCiConsumesSharedGateǁrun__mutmut: MutantDict = {}  # type: ignore


class CiConsumesSharedGate(FitnessRule):
    """Gate that FAILS when a repo's CI forks its own quality gate off the shared standard.

    Drives the two arms (reusable-reference, engine-invocation) directly in
    :meth:`run`; the per-file scan hooks are inert because a forked gate is a
    hard repo-level gate.
    """

    name = "ci-consumes-shared-gate"
    remediation = REMEDIATION
    #: Not a file-scan rule — the enumeration hooks stay empty.
    extensions = ()

    #: Rule-specific config (instance attrs; from_config overrides per consumer).
    workflows_dir: str = DEFAULT_WORKFLOWS_DIR
    reusable_pattern: str = DEFAULT_REUSABLE_PATTERN
    engine_pattern: str = DEFAULT_ENGINE_PATTERN

    @classmethod
    @_mutmut_mutated(mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted({"warn_only", "baseline_ok"} & set(config))
        if removed:
            raise ValueError(
                f"{', '.join(removed)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        rule.reusable_pattern = str(config.get("reusable_pattern", DEFAULT_REUSABLE_PATTERN))
        rule.engine_pattern = str(config.get("engine_pattern", DEFAULT_ENGINE_PATTERN))
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted({"warn_only", "baseline_ok"} & set(config))
        if removed:
            raise ValueError(
                f"{', '.join(removed)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        rule.reusable_pattern = str(config.get("reusable_pattern", DEFAULT_REUSABLE_PATTERN))
        rule.engine_pattern = str(config.get("engine_pattern", DEFAULT_ENGINE_PATTERN))
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = None
        if removed:
            raise ValueError(
                f"{', '.join(removed)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        rule.reusable_pattern = str(config.get("reusable_pattern", DEFAULT_REUSABLE_PATTERN))
        rule.engine_pattern = str(config.get("engine_pattern", DEFAULT_ENGINE_PATTERN))
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted(None)
        if removed:
            raise ValueError(
                f"{', '.join(removed)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        rule.reusable_pattern = str(config.get("reusable_pattern", DEFAULT_REUSABLE_PATTERN))
        rule.engine_pattern = str(config.get("engine_pattern", DEFAULT_ENGINE_PATTERN))
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted({"warn_only", "baseline_ok"} | set(config))
        if removed:
            raise ValueError(
                f"{', '.join(removed)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        rule.reusable_pattern = str(config.get("reusable_pattern", DEFAULT_REUSABLE_PATTERN))
        rule.engine_pattern = str(config.get("engine_pattern", DEFAULT_ENGINE_PATTERN))
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted({"XXwarn_onlyXX", "baseline_ok"} & set(config))
        if removed:
            raise ValueError(
                f"{', '.join(removed)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        rule.reusable_pattern = str(config.get("reusable_pattern", DEFAULT_REUSABLE_PATTERN))
        rule.engine_pattern = str(config.get("engine_pattern", DEFAULT_ENGINE_PATTERN))
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted({"WARN_ONLY", "baseline_ok"} & set(config))
        if removed:
            raise ValueError(
                f"{', '.join(removed)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        rule.reusable_pattern = str(config.get("reusable_pattern", DEFAULT_REUSABLE_PATTERN))
        rule.engine_pattern = str(config.get("engine_pattern", DEFAULT_ENGINE_PATTERN))
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted({"warn_only", "XXbaseline_okXX"} & set(config))
        if removed:
            raise ValueError(
                f"{', '.join(removed)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        rule.reusable_pattern = str(config.get("reusable_pattern", DEFAULT_REUSABLE_PATTERN))
        rule.engine_pattern = str(config.get("engine_pattern", DEFAULT_ENGINE_PATTERN))
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted({"warn_only", "BASELINE_OK"} & set(config))
        if removed:
            raise ValueError(
                f"{', '.join(removed)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        rule.reusable_pattern = str(config.get("reusable_pattern", DEFAULT_REUSABLE_PATTERN))
        rule.engine_pattern = str(config.get("engine_pattern", DEFAULT_ENGINE_PATTERN))
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted({"warn_only", "baseline_ok"} & set(None))
        if removed:
            raise ValueError(
                f"{', '.join(removed)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        rule.reusable_pattern = str(config.get("reusable_pattern", DEFAULT_REUSABLE_PATTERN))
        rule.engine_pattern = str(config.get("engine_pattern", DEFAULT_ENGINE_PATTERN))
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted({"warn_only", "baseline_ok"} & set(config))
        if removed:
            raise ValueError(
                None
            )
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        rule.reusable_pattern = str(config.get("reusable_pattern", DEFAULT_REUSABLE_PATTERN))
        rule.engine_pattern = str(config.get("engine_pattern", DEFAULT_ENGINE_PATTERN))
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted({"warn_only", "baseline_ok"} & set(config))
        if removed:
            raise ValueError(
                f"{', '.join(None)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        rule.reusable_pattern = str(config.get("reusable_pattern", DEFAULT_REUSABLE_PATTERN))
        rule.engine_pattern = str(config.get("engine_pattern", DEFAULT_ENGINE_PATTERN))
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted({"warn_only", "baseline_ok"} & set(config))
        if removed:
            raise ValueError(
                f"{'XX, XX'.join(removed)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        rule.reusable_pattern = str(config.get("reusable_pattern", DEFAULT_REUSABLE_PATTERN))
        rule.engine_pattern = str(config.get("engine_pattern", DEFAULT_ENGINE_PATTERN))
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted({"warn_only", "baseline_ok"} & set(config))
        if removed:
            raise ValueError(
                f"{', '.join(removed)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = None
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        rule.reusable_pattern = str(config.get("reusable_pattern", DEFAULT_REUSABLE_PATTERN))
        rule.engine_pattern = str(config.get("engine_pattern", DEFAULT_ENGINE_PATTERN))
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_13(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted({"warn_only", "baseline_ok"} & set(config))
        if removed:
            raise ValueError(
                f"{', '.join(removed)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        rule.reusable_pattern = str(config.get("reusable_pattern", DEFAULT_REUSABLE_PATTERN))
        rule.engine_pattern = str(config.get("engine_pattern", DEFAULT_ENGINE_PATTERN))
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_14(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted({"warn_only", "baseline_ok"} & set(config))
        if removed:
            raise ValueError(
                f"{', '.join(removed)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        rule.reusable_pattern = str(config.get("reusable_pattern", DEFAULT_REUSABLE_PATTERN))
        rule.engine_pattern = str(config.get("engine_pattern", DEFAULT_ENGINE_PATTERN))
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_15(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted({"warn_only", "baseline_ok"} & set(config))
        if removed:
            raise ValueError(
                f"{', '.join(removed)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        rule.reusable_pattern = str(config.get("reusable_pattern", DEFAULT_REUSABLE_PATTERN))
        rule.engine_pattern = str(config.get("engine_pattern", DEFAULT_ENGINE_PATTERN))
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_16(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted({"warn_only", "baseline_ok"} & set(config))
        if removed:
            raise ValueError(
                f"{', '.join(removed)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = super().from_config(config, )
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        rule.reusable_pattern = str(config.get("reusable_pattern", DEFAULT_REUSABLE_PATTERN))
        rule.engine_pattern = str(config.get("engine_pattern", DEFAULT_ENGINE_PATTERN))
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_17(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted({"warn_only", "baseline_ok"} & set(config))
        if removed:
            raise ValueError(
                f"{', '.join(removed)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = None
        rule.reusable_pattern = str(config.get("reusable_pattern", DEFAULT_REUSABLE_PATTERN))
        rule.engine_pattern = str(config.get("engine_pattern", DEFAULT_ENGINE_PATTERN))
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_18(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted({"warn_only", "baseline_ok"} & set(config))
        if removed:
            raise ValueError(
                f"{', '.join(removed)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(None)
        rule.reusable_pattern = str(config.get("reusable_pattern", DEFAULT_REUSABLE_PATTERN))
        rule.engine_pattern = str(config.get("engine_pattern", DEFAULT_ENGINE_PATTERN))
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_19(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted({"warn_only", "baseline_ok"} & set(config))
        if removed:
            raise ValueError(
                f"{', '.join(removed)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get(None, DEFAULT_WORKFLOWS_DIR))
        rule.reusable_pattern = str(config.get("reusable_pattern", DEFAULT_REUSABLE_PATTERN))
        rule.engine_pattern = str(config.get("engine_pattern", DEFAULT_ENGINE_PATTERN))
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_20(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted({"warn_only", "baseline_ok"} & set(config))
        if removed:
            raise ValueError(
                f"{', '.join(removed)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get("workflows_dir", None))
        rule.reusable_pattern = str(config.get("reusable_pattern", DEFAULT_REUSABLE_PATTERN))
        rule.engine_pattern = str(config.get("engine_pattern", DEFAULT_ENGINE_PATTERN))
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_21(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted({"warn_only", "baseline_ok"} & set(config))
        if removed:
            raise ValueError(
                f"{', '.join(removed)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get(DEFAULT_WORKFLOWS_DIR))
        rule.reusable_pattern = str(config.get("reusable_pattern", DEFAULT_REUSABLE_PATTERN))
        rule.engine_pattern = str(config.get("engine_pattern", DEFAULT_ENGINE_PATTERN))
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_22(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted({"warn_only", "baseline_ok"} & set(config))
        if removed:
            raise ValueError(
                f"{', '.join(removed)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get("workflows_dir", ))
        rule.reusable_pattern = str(config.get("reusable_pattern", DEFAULT_REUSABLE_PATTERN))
        rule.engine_pattern = str(config.get("engine_pattern", DEFAULT_ENGINE_PATTERN))
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_23(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted({"warn_only", "baseline_ok"} & set(config))
        if removed:
            raise ValueError(
                f"{', '.join(removed)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get("XXworkflows_dirXX", DEFAULT_WORKFLOWS_DIR))
        rule.reusable_pattern = str(config.get("reusable_pattern", DEFAULT_REUSABLE_PATTERN))
        rule.engine_pattern = str(config.get("engine_pattern", DEFAULT_ENGINE_PATTERN))
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_24(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted({"warn_only", "baseline_ok"} & set(config))
        if removed:
            raise ValueError(
                f"{', '.join(removed)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get("WORKFLOWS_DIR", DEFAULT_WORKFLOWS_DIR))
        rule.reusable_pattern = str(config.get("reusable_pattern", DEFAULT_REUSABLE_PATTERN))
        rule.engine_pattern = str(config.get("engine_pattern", DEFAULT_ENGINE_PATTERN))
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_25(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted({"warn_only", "baseline_ok"} & set(config))
        if removed:
            raise ValueError(
                f"{', '.join(removed)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        rule.reusable_pattern = None
        rule.engine_pattern = str(config.get("engine_pattern", DEFAULT_ENGINE_PATTERN))
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_26(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted({"warn_only", "baseline_ok"} & set(config))
        if removed:
            raise ValueError(
                f"{', '.join(removed)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        rule.reusable_pattern = str(None)
        rule.engine_pattern = str(config.get("engine_pattern", DEFAULT_ENGINE_PATTERN))
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_27(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted({"warn_only", "baseline_ok"} & set(config))
        if removed:
            raise ValueError(
                f"{', '.join(removed)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        rule.reusable_pattern = str(config.get(None, DEFAULT_REUSABLE_PATTERN))
        rule.engine_pattern = str(config.get("engine_pattern", DEFAULT_ENGINE_PATTERN))
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_28(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted({"warn_only", "baseline_ok"} & set(config))
        if removed:
            raise ValueError(
                f"{', '.join(removed)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        rule.reusable_pattern = str(config.get("reusable_pattern", None))
        rule.engine_pattern = str(config.get("engine_pattern", DEFAULT_ENGINE_PATTERN))
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_29(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted({"warn_only", "baseline_ok"} & set(config))
        if removed:
            raise ValueError(
                f"{', '.join(removed)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        rule.reusable_pattern = str(config.get(DEFAULT_REUSABLE_PATTERN))
        rule.engine_pattern = str(config.get("engine_pattern", DEFAULT_ENGINE_PATTERN))
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_30(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted({"warn_only", "baseline_ok"} & set(config))
        if removed:
            raise ValueError(
                f"{', '.join(removed)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        rule.reusable_pattern = str(config.get("reusable_pattern", ))
        rule.engine_pattern = str(config.get("engine_pattern", DEFAULT_ENGINE_PATTERN))
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_31(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted({"warn_only", "baseline_ok"} & set(config))
        if removed:
            raise ValueError(
                f"{', '.join(removed)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        rule.reusable_pattern = str(config.get("XXreusable_patternXX", DEFAULT_REUSABLE_PATTERN))
        rule.engine_pattern = str(config.get("engine_pattern", DEFAULT_ENGINE_PATTERN))
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_32(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted({"warn_only", "baseline_ok"} & set(config))
        if removed:
            raise ValueError(
                f"{', '.join(removed)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        rule.reusable_pattern = str(config.get("REUSABLE_PATTERN", DEFAULT_REUSABLE_PATTERN))
        rule.engine_pattern = str(config.get("engine_pattern", DEFAULT_ENGINE_PATTERN))
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_33(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted({"warn_only", "baseline_ok"} & set(config))
        if removed:
            raise ValueError(
                f"{', '.join(removed)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        rule.reusable_pattern = str(config.get("reusable_pattern", DEFAULT_REUSABLE_PATTERN))
        rule.engine_pattern = None
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_34(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted({"warn_only", "baseline_ok"} & set(config))
        if removed:
            raise ValueError(
                f"{', '.join(removed)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        rule.reusable_pattern = str(config.get("reusable_pattern", DEFAULT_REUSABLE_PATTERN))
        rule.engine_pattern = str(None)
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_35(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted({"warn_only", "baseline_ok"} & set(config))
        if removed:
            raise ValueError(
                f"{', '.join(removed)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        rule.reusable_pattern = str(config.get("reusable_pattern", DEFAULT_REUSABLE_PATTERN))
        rule.engine_pattern = str(config.get(None, DEFAULT_ENGINE_PATTERN))
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_36(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted({"warn_only", "baseline_ok"} & set(config))
        if removed:
            raise ValueError(
                f"{', '.join(removed)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        rule.reusable_pattern = str(config.get("reusable_pattern", DEFAULT_REUSABLE_PATTERN))
        rule.engine_pattern = str(config.get("engine_pattern", None))
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_37(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted({"warn_only", "baseline_ok"} & set(config))
        if removed:
            raise ValueError(
                f"{', '.join(removed)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        rule.reusable_pattern = str(config.get("reusable_pattern", DEFAULT_REUSABLE_PATTERN))
        rule.engine_pattern = str(config.get(DEFAULT_ENGINE_PATTERN))
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_38(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted({"warn_only", "baseline_ok"} & set(config))
        if removed:
            raise ValueError(
                f"{', '.join(removed)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        rule.reusable_pattern = str(config.get("reusable_pattern", DEFAULT_REUSABLE_PATTERN))
        rule.engine_pattern = str(config.get("engine_pattern", ))
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_39(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted({"warn_only", "baseline_ok"} & set(config))
        if removed:
            raise ValueError(
                f"{', '.join(removed)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        rule.reusable_pattern = str(config.get("reusable_pattern", DEFAULT_REUSABLE_PATTERN))
        rule.engine_pattern = str(config.get("XXengine_patternXX", DEFAULT_ENGINE_PATTERN))
        return rule

    @classmethod
    def xǁCiConsumesSharedGateǁfrom_config__mutmut_40(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiConsumesSharedGate:
        removed = sorted({"warn_only", "baseline_ok"} & set(config))
        if removed:
            raise ValueError(
                f"{', '.join(removed)} is not supported: a forked CI gate is always a hard failure"
            )
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiConsumesSharedGate)  # noqa: S101  # narrowing for mypy
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        rule.reusable_pattern = str(config.get("reusable_pattern", DEFAULT_REUSABLE_PATTERN))
        rule.engine_pattern = str(config.get("ENGINE_PATTERN", DEFAULT_ENGINE_PATTERN))
        return rule

    @_mutmut_mutated(mutants_xǁCiConsumesSharedGateǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:  # pragma: no cover - not used
        """Unused: a forked CI gate is a repo-level gate, not a per-file scan."""
        return False

    def xǁCiConsumesSharedGateǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:  # pragma: no cover - not used
        """Unused: a forked CI gate is a repo-level gate, not a per-file scan."""
        return False

    def xǁCiConsumesSharedGateǁfile_has_violation__mutmut_1(self, path: Path) -> bool:  # pragma: no cover - not used
        """Unused: a forked CI gate is a repo-level gate, not a per-file scan."""
        return True

    @_mutmut_mutated(mutants_xǁCiConsumesSharedGateǁ_compile_patterns__mutmut)
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

    def xǁCiConsumesSharedGateǁ_compile_patterns__mutmut_orig(self) -> tuple[re.Pattern[str], re.Pattern[str]] | str:
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

    def xǁCiConsumesSharedGateǁ_compile_patterns__mutmut_1(self) -> tuple[re.Pattern[str], re.Pattern[str]] | str:
        """Compile both configured regexes; return them, or an error label."""
        try:
            reusable_re = None
        except re.error as exc:
            return f"reusable_pattern is not a valid regex ({exc})"
        try:
            engine_re = re.compile(self.engine_pattern)
        except re.error as exc:
            return f"engine_pattern is not a valid regex ({exc})"
        return (reusable_re, engine_re)

    def xǁCiConsumesSharedGateǁ_compile_patterns__mutmut_2(self) -> tuple[re.Pattern[str], re.Pattern[str]] | str:
        """Compile both configured regexes; return them, or an error label."""
        try:
            reusable_re = re.compile(None)
        except re.error as exc:
            return f"reusable_pattern is not a valid regex ({exc})"
        try:
            engine_re = re.compile(self.engine_pattern)
        except re.error as exc:
            return f"engine_pattern is not a valid regex ({exc})"
        return (reusable_re, engine_re)

    def xǁCiConsumesSharedGateǁ_compile_patterns__mutmut_3(self) -> tuple[re.Pattern[str], re.Pattern[str]] | str:
        """Compile both configured regexes; return them, or an error label."""
        try:
            reusable_re = re.compile(self.reusable_pattern)
        except re.error as exc:
            return f"reusable_pattern is not a valid regex ({exc})"
        try:
            engine_re = None
        except re.error as exc:
            return f"engine_pattern is not a valid regex ({exc})"
        return (reusable_re, engine_re)

    def xǁCiConsumesSharedGateǁ_compile_patterns__mutmut_4(self) -> tuple[re.Pattern[str], re.Pattern[str]] | str:
        """Compile both configured regexes; return them, or an error label."""
        try:
            reusable_re = re.compile(self.reusable_pattern)
        except re.error as exc:
            return f"reusable_pattern is not a valid regex ({exc})"
        try:
            engine_re = re.compile(None)
        except re.error as exc:
            return f"engine_pattern is not a valid regex ({exc})"
        return (reusable_re, engine_re)

    @_mutmut_mutated(mutants_xǁCiConsumesSharedGateǁ_first_satisfying__mutmut)
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

    def xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_orig(
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

    def xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_1(
        self,
        files: list[Path],
        reusable_re: re.Pattern[str],
        engine_re: re.Pattern[str],
    ) -> tuple[Path, str, int, str] | None:
        """Return the first workflow that consumes the shared gate, else None."""
        for path in files:
            try:
                text = None
            except (UnicodeDecodeError, OSError):
                continue
            hit = satisfying_mechanism(text, reusable_pattern=reusable_re, engine_pattern=engine_re)
            if hit is not None:
                mechanism, line_no, line = hit
                return (path, mechanism, line_no, line)
        return None

    def xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_2(
        self,
        files: list[Path],
        reusable_re: re.Pattern[str],
        engine_re: re.Pattern[str],
    ) -> tuple[Path, str, int, str] | None:
        """Return the first workflow that consumes the shared gate, else None."""
        for path in files:
            try:
                text = path.read_text(encoding=None)
            except (UnicodeDecodeError, OSError):
                continue
            hit = satisfying_mechanism(text, reusable_pattern=reusable_re, engine_pattern=engine_re)
            if hit is not None:
                mechanism, line_no, line = hit
                return (path, mechanism, line_no, line)
        return None

    def xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_3(
        self,
        files: list[Path],
        reusable_re: re.Pattern[str],
        engine_re: re.Pattern[str],
    ) -> tuple[Path, str, int, str] | None:
        """Return the first workflow that consumes the shared gate, else None."""
        for path in files:
            try:
                text = path.read_text(encoding="XXutf-8XX")
            except (UnicodeDecodeError, OSError):
                continue
            hit = satisfying_mechanism(text, reusable_pattern=reusable_re, engine_pattern=engine_re)
            if hit is not None:
                mechanism, line_no, line = hit
                return (path, mechanism, line_no, line)
        return None

    def xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_4(
        self,
        files: list[Path],
        reusable_re: re.Pattern[str],
        engine_re: re.Pattern[str],
    ) -> tuple[Path, str, int, str] | None:
        """Return the first workflow that consumes the shared gate, else None."""
        for path in files:
            try:
                text = path.read_text(encoding="UTF-8")
            except (UnicodeDecodeError, OSError):
                continue
            hit = satisfying_mechanism(text, reusable_pattern=reusable_re, engine_pattern=engine_re)
            if hit is not None:
                mechanism, line_no, line = hit
                return (path, mechanism, line_no, line)
        return None

    def xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_5(
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
                break
            hit = satisfying_mechanism(text, reusable_pattern=reusable_re, engine_pattern=engine_re)
            if hit is not None:
                mechanism, line_no, line = hit
                return (path, mechanism, line_no, line)
        return None

    def xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_6(
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
            hit = None
            if hit is not None:
                mechanism, line_no, line = hit
                return (path, mechanism, line_no, line)
        return None

    def xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_7(
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
            hit = satisfying_mechanism(None, reusable_pattern=reusable_re, engine_pattern=engine_re)
            if hit is not None:
                mechanism, line_no, line = hit
                return (path, mechanism, line_no, line)
        return None

    def xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_8(
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
            hit = satisfying_mechanism(text, reusable_pattern=None, engine_pattern=engine_re)
            if hit is not None:
                mechanism, line_no, line = hit
                return (path, mechanism, line_no, line)
        return None

    def xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_9(
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
            hit = satisfying_mechanism(text, reusable_pattern=reusable_re, engine_pattern=None)
            if hit is not None:
                mechanism, line_no, line = hit
                return (path, mechanism, line_no, line)
        return None

    def xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_10(
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
            hit = satisfying_mechanism(reusable_pattern=reusable_re, engine_pattern=engine_re)
            if hit is not None:
                mechanism, line_no, line = hit
                return (path, mechanism, line_no, line)
        return None

    def xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_11(
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
            hit = satisfying_mechanism(text, engine_pattern=engine_re)
            if hit is not None:
                mechanism, line_no, line = hit
                return (path, mechanism, line_no, line)
        return None

    def xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_12(
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
            hit = satisfying_mechanism(text, reusable_pattern=reusable_re, )
            if hit is not None:
                mechanism, line_no, line = hit
                return (path, mechanism, line_no, line)
        return None

    def xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_13(
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
            if hit is None:
                mechanism, line_no, line = hit
                return (path, mechanism, line_no, line)
        return None

    def xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_14(
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
                mechanism, line_no, line = None
                return (path, mechanism, line_no, line)
        return None

    @_mutmut_mutated(mutants_xǁCiConsumesSharedGateǁrun__mutmut)
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
            report_finding(self.name, ".", compiled)
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
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_orig(self) -> int:
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
            report_finding(self.name, ".", compiled)
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
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_1(self) -> int:
        """Drive the two arms; SKIP when no CI, PASS on consumption, else FAIL."""
        workflows_dir = None
        files = workflow_files(workflows_dir)

        if not files:
            print(
                f"ok [{self._name}] — skipped: no CI workflows under "
                f"{self.workflows_dir!r} (nothing to enforce)."
            )
            return 0

        compiled = self._compile_patterns()
        if isinstance(compiled, str):
            report_finding(self.name, ".", compiled)
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
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_2(self) -> int:
        """Drive the two arms; SKIP when no CI, PASS on consumption, else FAIL."""
        workflows_dir = self._repo_root * self.workflows_dir
        files = workflow_files(workflows_dir)

        if not files:
            print(
                f"ok [{self._name}] — skipped: no CI workflows under "
                f"{self.workflows_dir!r} (nothing to enforce)."
            )
            return 0

        compiled = self._compile_patterns()
        if isinstance(compiled, str):
            report_finding(self.name, ".", compiled)
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
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_3(self) -> int:
        """Drive the two arms; SKIP when no CI, PASS on consumption, else FAIL."""
        workflows_dir = self._repo_root / self.workflows_dir
        files = None

        if not files:
            print(
                f"ok [{self._name}] — skipped: no CI workflows under "
                f"{self.workflows_dir!r} (nothing to enforce)."
            )
            return 0

        compiled = self._compile_patterns()
        if isinstance(compiled, str):
            report_finding(self.name, ".", compiled)
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
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_4(self) -> int:
        """Drive the two arms; SKIP when no CI, PASS on consumption, else FAIL."""
        workflows_dir = self._repo_root / self.workflows_dir
        files = workflow_files(None)

        if not files:
            print(
                f"ok [{self._name}] — skipped: no CI workflows under "
                f"{self.workflows_dir!r} (nothing to enforce)."
            )
            return 0

        compiled = self._compile_patterns()
        if isinstance(compiled, str):
            report_finding(self.name, ".", compiled)
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
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_5(self) -> int:
        """Drive the two arms; SKIP when no CI, PASS on consumption, else FAIL."""
        workflows_dir = self._repo_root / self.workflows_dir
        files = workflow_files(workflows_dir)

        if files:
            print(
                f"ok [{self._name}] — skipped: no CI workflows under "
                f"{self.workflows_dir!r} (nothing to enforce)."
            )
            return 0

        compiled = self._compile_patterns()
        if isinstance(compiled, str):
            report_finding(self.name, ".", compiled)
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
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_6(self) -> int:
        """Drive the two arms; SKIP when no CI, PASS on consumption, else FAIL."""
        workflows_dir = self._repo_root / self.workflows_dir
        files = workflow_files(workflows_dir)

        if not files:
            print(
                None
            )
            return 0

        compiled = self._compile_patterns()
        if isinstance(compiled, str):
            report_finding(self.name, ".", compiled)
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
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_7(self) -> int:
        """Drive the two arms; SKIP when no CI, PASS on consumption, else FAIL."""
        workflows_dir = self._repo_root / self.workflows_dir
        files = workflow_files(workflows_dir)

        if not files:
            print(
                f"ok [{self._name}] — skipped: no CI workflows under "
                f"{self.workflows_dir!r} (nothing to enforce)."
            )
            return 1

        compiled = self._compile_patterns()
        if isinstance(compiled, str):
            report_finding(self.name, ".", compiled)
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
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_8(self) -> int:
        """Drive the two arms; SKIP when no CI, PASS on consumption, else FAIL."""
        workflows_dir = self._repo_root / self.workflows_dir
        files = workflow_files(workflows_dir)

        if not files:
            print(
                f"ok [{self._name}] — skipped: no CI workflows under "
                f"{self.workflows_dir!r} (nothing to enforce)."
            )
            return 0

        compiled = None
        if isinstance(compiled, str):
            report_finding(self.name, ".", compiled)
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
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_9(self) -> int:
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
            report_finding(None, ".", compiled)
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
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_10(self) -> int:
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
            report_finding(self.name, None, compiled)
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
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_11(self) -> int:
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
            report_finding(self.name, ".", None)
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
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_12(self) -> int:
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
            report_finding(".", compiled)
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
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_13(self) -> int:
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
            report_finding(self.name, compiled)
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
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_14(self) -> int:
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
            report_finding(self.name, ".", )
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
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_15(self) -> int:
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
            report_finding(self.name, "XX.XX", compiled)
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
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_16(self) -> int:
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
            report_finding(self.name, ".", compiled)
            print(None)
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
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_17(self) -> int:
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
            report_finding(self.name, ".", compiled)
            print(f"FAIL [{self._name}] — a configured pattern is not a valid regex:")
            print(None)
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
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_18(self) -> int:
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
            report_finding(self.name, ".", compiled)
            print(f"FAIL [{self._name}] — a configured pattern is not a valid regex:")
            print(f"  - {compiled}")
            print()
            print(None)
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
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_19(self) -> int:
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
            report_finding(self.name, ".", compiled)
            print(f"FAIL [{self._name}] — a configured pattern is not a valid regex:")
            print(f"  - {compiled}")
            print()
            print(self.remediation)
            return 2
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
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_20(self) -> int:
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
            report_finding(self.name, ".", compiled)
            print(f"FAIL [{self._name}] — a configured pattern is not a valid regex:")
            print(f"  - {compiled}")
            print()
            print(self.remediation)
            return 1
        reusable_re, engine_re = None

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
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_21(self) -> int:
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
            report_finding(self.name, ".", compiled)
            print(f"FAIL [{self._name}] — a configured pattern is not a valid regex:")
            print(f"  - {compiled}")
            print()
            print(self.remediation)
            return 1
        reusable_re, engine_re = compiled

        satisfied = None
        if satisfied is not None:
            path, mechanism, line_no, line = satisfied
            rel = self._repo_relative(path)
            print(
                f"ok [{self._name}] — CI consumes the shared quality gate via "
                f"{mechanism}: {rel}:{line_no}  ({line})."
            )
            return 0

        scanned = ", ".join(sorted(path.name for path in files))
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_22(self) -> int:
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
            report_finding(self.name, ".", compiled)
            print(f"FAIL [{self._name}] — a configured pattern is not a valid regex:")
            print(f"  - {compiled}")
            print()
            print(self.remediation)
            return 1
        reusable_re, engine_re = compiled

        satisfied = self._first_satisfying(None, reusable_re, engine_re)
        if satisfied is not None:
            path, mechanism, line_no, line = satisfied
            rel = self._repo_relative(path)
            print(
                f"ok [{self._name}] — CI consumes the shared quality gate via "
                f"{mechanism}: {rel}:{line_no}  ({line})."
            )
            return 0

        scanned = ", ".join(sorted(path.name for path in files))
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_23(self) -> int:
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
            report_finding(self.name, ".", compiled)
            print(f"FAIL [{self._name}] — a configured pattern is not a valid regex:")
            print(f"  - {compiled}")
            print()
            print(self.remediation)
            return 1
        reusable_re, engine_re = compiled

        satisfied = self._first_satisfying(files, None, engine_re)
        if satisfied is not None:
            path, mechanism, line_no, line = satisfied
            rel = self._repo_relative(path)
            print(
                f"ok [{self._name}] — CI consumes the shared quality gate via "
                f"{mechanism}: {rel}:{line_no}  ({line})."
            )
            return 0

        scanned = ", ".join(sorted(path.name for path in files))
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_24(self) -> int:
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
            report_finding(self.name, ".", compiled)
            print(f"FAIL [{self._name}] — a configured pattern is not a valid regex:")
            print(f"  - {compiled}")
            print()
            print(self.remediation)
            return 1
        reusable_re, engine_re = compiled

        satisfied = self._first_satisfying(files, reusable_re, None)
        if satisfied is not None:
            path, mechanism, line_no, line = satisfied
            rel = self._repo_relative(path)
            print(
                f"ok [{self._name}] — CI consumes the shared quality gate via "
                f"{mechanism}: {rel}:{line_no}  ({line})."
            )
            return 0

        scanned = ", ".join(sorted(path.name for path in files))
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_25(self) -> int:
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
            report_finding(self.name, ".", compiled)
            print(f"FAIL [{self._name}] — a configured pattern is not a valid regex:")
            print(f"  - {compiled}")
            print()
            print(self.remediation)
            return 1
        reusable_re, engine_re = compiled

        satisfied = self._first_satisfying(reusable_re, engine_re)
        if satisfied is not None:
            path, mechanism, line_no, line = satisfied
            rel = self._repo_relative(path)
            print(
                f"ok [{self._name}] — CI consumes the shared quality gate via "
                f"{mechanism}: {rel}:{line_no}  ({line})."
            )
            return 0

        scanned = ", ".join(sorted(path.name for path in files))
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_26(self) -> int:
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
            report_finding(self.name, ".", compiled)
            print(f"FAIL [{self._name}] — a configured pattern is not a valid regex:")
            print(f"  - {compiled}")
            print()
            print(self.remediation)
            return 1
        reusable_re, engine_re = compiled

        satisfied = self._first_satisfying(files, engine_re)
        if satisfied is not None:
            path, mechanism, line_no, line = satisfied
            rel = self._repo_relative(path)
            print(
                f"ok [{self._name}] — CI consumes the shared quality gate via "
                f"{mechanism}: {rel}:{line_no}  ({line})."
            )
            return 0

        scanned = ", ".join(sorted(path.name for path in files))
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_27(self) -> int:
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
            report_finding(self.name, ".", compiled)
            print(f"FAIL [{self._name}] — a configured pattern is not a valid regex:")
            print(f"  - {compiled}")
            print()
            print(self.remediation)
            return 1
        reusable_re, engine_re = compiled

        satisfied = self._first_satisfying(files, reusable_re, )
        if satisfied is not None:
            path, mechanism, line_no, line = satisfied
            rel = self._repo_relative(path)
            print(
                f"ok [{self._name}] — CI consumes the shared quality gate via "
                f"{mechanism}: {rel}:{line_no}  ({line})."
            )
            return 0

        scanned = ", ".join(sorted(path.name for path in files))
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_28(self) -> int:
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
            report_finding(self.name, ".", compiled)
            print(f"FAIL [{self._name}] — a configured pattern is not a valid regex:")
            print(f"  - {compiled}")
            print()
            print(self.remediation)
            return 1
        reusable_re, engine_re = compiled

        satisfied = self._first_satisfying(files, reusable_re, engine_re)
        if satisfied is None:
            path, mechanism, line_no, line = satisfied
            rel = self._repo_relative(path)
            print(
                f"ok [{self._name}] — CI consumes the shared quality gate via "
                f"{mechanism}: {rel}:{line_no}  ({line})."
            )
            return 0

        scanned = ", ".join(sorted(path.name for path in files))
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_29(self) -> int:
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
            report_finding(self.name, ".", compiled)
            print(f"FAIL [{self._name}] — a configured pattern is not a valid regex:")
            print(f"  - {compiled}")
            print()
            print(self.remediation)
            return 1
        reusable_re, engine_re = compiled

        satisfied = self._first_satisfying(files, reusable_re, engine_re)
        if satisfied is not None:
            path, mechanism, line_no, line = None
            rel = self._repo_relative(path)
            print(
                f"ok [{self._name}] — CI consumes the shared quality gate via "
                f"{mechanism}: {rel}:{line_no}  ({line})."
            )
            return 0

        scanned = ", ".join(sorted(path.name for path in files))
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_30(self) -> int:
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
            report_finding(self.name, ".", compiled)
            print(f"FAIL [{self._name}] — a configured pattern is not a valid regex:")
            print(f"  - {compiled}")
            print()
            print(self.remediation)
            return 1
        reusable_re, engine_re = compiled

        satisfied = self._first_satisfying(files, reusable_re, engine_re)
        if satisfied is not None:
            path, mechanism, line_no, line = satisfied
            rel = None
            print(
                f"ok [{self._name}] — CI consumes the shared quality gate via "
                f"{mechanism}: {rel}:{line_no}  ({line})."
            )
            return 0

        scanned = ", ".join(sorted(path.name for path in files))
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_31(self) -> int:
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
            report_finding(self.name, ".", compiled)
            print(f"FAIL [{self._name}] — a configured pattern is not a valid regex:")
            print(f"  - {compiled}")
            print()
            print(self.remediation)
            return 1
        reusable_re, engine_re = compiled

        satisfied = self._first_satisfying(files, reusable_re, engine_re)
        if satisfied is not None:
            path, mechanism, line_no, line = satisfied
            rel = self._repo_relative(None)
            print(
                f"ok [{self._name}] — CI consumes the shared quality gate via "
                f"{mechanism}: {rel}:{line_no}  ({line})."
            )
            return 0

        scanned = ", ".join(sorted(path.name for path in files))
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_32(self) -> int:
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
            report_finding(self.name, ".", compiled)
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
                None
            )
            return 0

        scanned = ", ".join(sorted(path.name for path in files))
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_33(self) -> int:
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
            report_finding(self.name, ".", compiled)
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
            return 1

        scanned = ", ".join(sorted(path.name for path in files))
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_34(self) -> int:
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
            report_finding(self.name, ".", compiled)
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

        scanned = None
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_35(self) -> int:
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
            report_finding(self.name, ".", compiled)
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

        scanned = ", ".join(None)
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_36(self) -> int:
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
            report_finding(self.name, ".", compiled)
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

        scanned = "XX, XX".join(sorted(path.name for path in files))
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_37(self) -> int:
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
            report_finding(self.name, ".", compiled)
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

        scanned = ", ".join(sorted(None))
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_38(self) -> int:
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
            report_finding(self.name, ".", compiled)
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
        finding = None
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_39(self) -> int:
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
            report_finding(self.name, ".", compiled)
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
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(None, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_40(self) -> int:
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
            report_finding(self.name, ".", compiled)
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
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, None, finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_41(self) -> int:
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
            report_finding(self.name, ".", compiled)
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
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", None)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_42(self) -> int:
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
            report_finding(self.name, ".", compiled)
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
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_43(self) -> int:
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
            report_finding(self.name, ".", compiled)
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
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_44(self) -> int:
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
            report_finding(self.name, ".", compiled)
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
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", )
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_45(self) -> int:
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
            report_finding(self.name, ".", compiled)
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
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, "XX.XX", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_46(self) -> int:
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
            report_finding(self.name, ".", compiled)
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
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(None)
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_47(self) -> int:
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
            report_finding(self.name, ".", compiled)
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
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(None)
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_48(self) -> int:
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
            report_finding(self.name, ".", compiled)
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
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            None
        )
        print()
        print(self.remediation)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_49(self) -> int:
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
            report_finding(self.name, ".", compiled)
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
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(None)

        return 1

    def xǁCiConsumesSharedGateǁrun__mutmut_50(self) -> int:
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
            report_finding(self.name, ".", compiled)
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
        finding = f"{len(files)} workflow file(s) under {self.workflows_dir!r} ({scanned}), and NONE consumes the shared gate."
        report_finding(self.name, ".", finding)
        print(f"FAIL [{self._name}] — CI runs but forked its quality gate off the shared standard:")
        print(f"  - {finding}")
        print(
            f"  - no `uses:` reference matches {self.reusable_pattern!r} and no step "
            f"matches {self.engine_pattern!r}."
        )
        print()
        print(self.remediation)

        return 2

mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['_mutmut_orig'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['xǁCiConsumesSharedGateǁfrom_config__mutmut_1'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['xǁCiConsumesSharedGateǁfrom_config__mutmut_2'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['xǁCiConsumesSharedGateǁfrom_config__mutmut_3'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['xǁCiConsumesSharedGateǁfrom_config__mutmut_4'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['xǁCiConsumesSharedGateǁfrom_config__mutmut_5'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['xǁCiConsumesSharedGateǁfrom_config__mutmut_6'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['xǁCiConsumesSharedGateǁfrom_config__mutmut_7'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['xǁCiConsumesSharedGateǁfrom_config__mutmut_8'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['xǁCiConsumesSharedGateǁfrom_config__mutmut_9'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['xǁCiConsumesSharedGateǁfrom_config__mutmut_10'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['xǁCiConsumesSharedGateǁfrom_config__mutmut_11'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['xǁCiConsumesSharedGateǁfrom_config__mutmut_12'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_12 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['xǁCiConsumesSharedGateǁfrom_config__mutmut_13'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_13 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['xǁCiConsumesSharedGateǁfrom_config__mutmut_14'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_14 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['xǁCiConsumesSharedGateǁfrom_config__mutmut_15'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_15 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['xǁCiConsumesSharedGateǁfrom_config__mutmut_16'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_16 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['xǁCiConsumesSharedGateǁfrom_config__mutmut_17'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_17 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['xǁCiConsumesSharedGateǁfrom_config__mutmut_18'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_18 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['xǁCiConsumesSharedGateǁfrom_config__mutmut_19'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_19 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['xǁCiConsumesSharedGateǁfrom_config__mutmut_20'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_20 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['xǁCiConsumesSharedGateǁfrom_config__mutmut_21'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_21 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['xǁCiConsumesSharedGateǁfrom_config__mutmut_22'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_22 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['xǁCiConsumesSharedGateǁfrom_config__mutmut_23'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_23 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['xǁCiConsumesSharedGateǁfrom_config__mutmut_24'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_24 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['xǁCiConsumesSharedGateǁfrom_config__mutmut_25'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_25 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['xǁCiConsumesSharedGateǁfrom_config__mutmut_26'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_26 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['xǁCiConsumesSharedGateǁfrom_config__mutmut_27'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_27 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['xǁCiConsumesSharedGateǁfrom_config__mutmut_28'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_28 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['xǁCiConsumesSharedGateǁfrom_config__mutmut_29'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_29 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['xǁCiConsumesSharedGateǁfrom_config__mutmut_30'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_30 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['xǁCiConsumesSharedGateǁfrom_config__mutmut_31'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_31 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['xǁCiConsumesSharedGateǁfrom_config__mutmut_32'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_32 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['xǁCiConsumesSharedGateǁfrom_config__mutmut_33'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_33 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['xǁCiConsumesSharedGateǁfrom_config__mutmut_34'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_34 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['xǁCiConsumesSharedGateǁfrom_config__mutmut_35'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_35 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['xǁCiConsumesSharedGateǁfrom_config__mutmut_36'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_36 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['xǁCiConsumesSharedGateǁfrom_config__mutmut_37'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_37 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['xǁCiConsumesSharedGateǁfrom_config__mutmut_38'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_38 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['xǁCiConsumesSharedGateǁfrom_config__mutmut_39'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_39 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfrom_config__mutmut['xǁCiConsumesSharedGateǁfrom_config__mutmut_40'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfrom_config__mutmut_40 # type: ignore # mutmut generated

mutants_xǁCiConsumesSharedGateǁfile_has_violation__mutmut['_mutmut_orig'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁfile_has_violation__mutmut['xǁCiConsumesSharedGateǁfile_has_violation__mutmut_1'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated

mutants_xǁCiConsumesSharedGateǁ_compile_patterns__mutmut['_mutmut_orig'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁ_compile_patterns__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁ_compile_patterns__mutmut['xǁCiConsumesSharedGateǁ_compile_patterns__mutmut_1'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁ_compile_patterns__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁ_compile_patterns__mutmut['xǁCiConsumesSharedGateǁ_compile_patterns__mutmut_2'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁ_compile_patterns__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁ_compile_patterns__mutmut['xǁCiConsumesSharedGateǁ_compile_patterns__mutmut_3'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁ_compile_patterns__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁ_compile_patterns__mutmut['xǁCiConsumesSharedGateǁ_compile_patterns__mutmut_4'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁ_compile_patterns__mutmut_4 # type: ignore # mutmut generated

mutants_xǁCiConsumesSharedGateǁ_first_satisfying__mutmut['_mutmut_orig'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁ_first_satisfying__mutmut['xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_1'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁ_first_satisfying__mutmut['xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_2'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁ_first_satisfying__mutmut['xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_3'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁ_first_satisfying__mutmut['xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_4'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁ_first_satisfying__mutmut['xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_5'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁ_first_satisfying__mutmut['xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_6'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁ_first_satisfying__mutmut['xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_7'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_7 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁ_first_satisfying__mutmut['xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_8'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_8 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁ_first_satisfying__mutmut['xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_9'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_9 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁ_first_satisfying__mutmut['xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_10'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_10 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁ_first_satisfying__mutmut['xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_11'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_11 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁ_first_satisfying__mutmut['xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_12'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_12 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁ_first_satisfying__mutmut['xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_13'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_13 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁ_first_satisfying__mutmut['xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_14'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁ_first_satisfying__mutmut_14 # type: ignore # mutmut generated

mutants_xǁCiConsumesSharedGateǁrun__mutmut['_mutmut_orig'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_1'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_2'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_3'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_4'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_5'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_6'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_7'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_7 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_8'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_8 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_9'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_9 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_10'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_10 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_11'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_11 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_12'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_12 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_13'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_13 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_14'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_14 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_15'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_15 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_16'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_16 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_17'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_17 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_18'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_18 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_19'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_19 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_20'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_20 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_21'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_21 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_22'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_22 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_23'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_23 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_24'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_24 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_25'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_25 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_26'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_26 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_27'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_27 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_28'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_28 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_29'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_29 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_30'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_30 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_31'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_31 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_32'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_32 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_33'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_33 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_34'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_34 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_35'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_35 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_36'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_36 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_37'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_37 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_38'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_38 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_39'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_39 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_40'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_40 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_41'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_41 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_42'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_42 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_43'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_43 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_44'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_44 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_45'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_45 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_46'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_46 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_47'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_47 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_48'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_48 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_49'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_49 # type: ignore # mutmut generated
mutants_xǁCiConsumesSharedGateǁrun__mutmut['xǁCiConsumesSharedGateǁrun__mutmut_50'] = CiConsumesSharedGate.xǁCiConsumesSharedGateǁrun__mutmut_50 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> CiConsumesSharedGate:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CiConsumesSharedGate.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> CiConsumesSharedGate:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CiConsumesSharedGate.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> CiConsumesSharedGate:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CiConsumesSharedGate.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> CiConsumesSharedGate:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CiConsumesSharedGate.from_config(config, repo_root=None)


def x_build__mutmut_3(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> CiConsumesSharedGate:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CiConsumesSharedGate.from_config(repo_root=repo_root)


def x_build__mutmut_4(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> CiConsumesSharedGate:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CiConsumesSharedGate.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(CiConsumesSharedGate, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(CiConsumesSharedGate, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(CiConsumesSharedGate, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(CiConsumesSharedGate, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
