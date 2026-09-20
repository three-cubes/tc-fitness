"""CORE check: mutation_survival_ratchet — the mutation report keeps its shape.

A mutation report records, per package, how many injected mutants the suite
KILLED versus how many SURVIVED. A rising survival rate means the suite is
getting weaker. This check binds both the accepted comparison report and the
current-run report as required evidence inputs.

What this CORE rule enforces:

* the baseline report exists and obeys the contract (``schema_version == 1`` and
  a ``packages`` object) — a malformed baseline is a violation;
* the current report exists and obeys the same contract.

The git-diff comparison + override grammar are deliberately NOT ported (they are
repo-coupled); a consumer that wants enforcement runs its own comparison on the
shape this rule guarantees.

Ported from tc-agent-zone ``scripts/checks/mutation_survival_ratchet.py`` —
re-expressed as a configurable, repo-agnostic rule. The two report paths are
CONFIG; nothing here names a repo.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: The schema version a mutation report MUST declare. Domain-intrinsic.
REQUIRED_SCHEMA_VERSION = 1

#: Default report locations relative to the repo root. Overridable per consumer.
DEFAULT_BASELINE_REPORT = ".architecture/baseline/mutation-survival-rates.json"
DEFAULT_CURRENT_REPORT = ".mutation/mutation-survival-rates.json"

REMEDIATION = _remediation(
    fix=(
        "make the mutation report obey its contract: valid JSON, "
        "schema_version of 1, and a packages object mapping each package to its "
        "survived/killed counts. Regenerate the report if it is stale or "
        "hand-edited into an invalid shape."
    ),
    nxt="re-run this check to confirm the report shape validates.",
    run="python -m tc_fitness.core_checks.mutation_survival_ratchet",
    passing='{"schema_version": 1, "packages": {"pkg": {"survived": 0, "killed": 9}}}',
    forbidden='{"schema_version": 2, "packages": []}  (wrong version, packages not an object)',
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x_report_is_malformed__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_report_is_malformed__mutmut)
def report_is_malformed(path: Path) -> bool:
    """True iff the report at ``path`` violates the shape contract.

    A non-existent file is reported by the caller. A present file must be valid JSON declaring
    ``schema_version == REQUIRED_SCHEMA_VERSION`` with a ``packages`` mapping;
    anything else is malformed.
    """
    if not path.exists():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return True
    if not isinstance(data, dict):
        return True
    if data.get("schema_version") != REQUIRED_SCHEMA_VERSION:
        return True
    return "packages" not in data or not isinstance(data["packages"], dict)


def x_report_is_malformed__mutmut_orig(path: Path) -> bool:
    """True iff the report at ``path`` violates the shape contract.

    A non-existent file is reported by the caller. A present file must be valid JSON declaring
    ``schema_version == REQUIRED_SCHEMA_VERSION`` with a ``packages`` mapping;
    anything else is malformed.
    """
    if not path.exists():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return True
    if not isinstance(data, dict):
        return True
    if data.get("schema_version") != REQUIRED_SCHEMA_VERSION:
        return True
    return "packages" not in data or not isinstance(data["packages"], dict)


def x_report_is_malformed__mutmut_1(path: Path) -> bool:
    """True iff the report at ``path`` violates the shape contract.

    A non-existent file is reported by the caller. A present file must be valid JSON declaring
    ``schema_version == REQUIRED_SCHEMA_VERSION`` with a ``packages`` mapping;
    anything else is malformed.
    """
    if path.exists():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return True
    if not isinstance(data, dict):
        return True
    if data.get("schema_version") != REQUIRED_SCHEMA_VERSION:
        return True
    return "packages" not in data or not isinstance(data["packages"], dict)


def x_report_is_malformed__mutmut_2(path: Path) -> bool:
    """True iff the report at ``path`` violates the shape contract.

    A non-existent file is reported by the caller. A present file must be valid JSON declaring
    ``schema_version == REQUIRED_SCHEMA_VERSION`` with a ``packages`` mapping;
    anything else is malformed.
    """
    if not path.exists():
        return True
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return True
    if not isinstance(data, dict):
        return True
    if data.get("schema_version") != REQUIRED_SCHEMA_VERSION:
        return True
    return "packages" not in data or not isinstance(data["packages"], dict)


def x_report_is_malformed__mutmut_3(path: Path) -> bool:
    """True iff the report at ``path`` violates the shape contract.

    A non-existent file is reported by the caller. A present file must be valid JSON declaring
    ``schema_version == REQUIRED_SCHEMA_VERSION`` with a ``packages`` mapping;
    anything else is malformed.
    """
    if not path.exists():
        return False
    try:
        data = None
    except (json.JSONDecodeError, UnicodeDecodeError):
        return True
    if not isinstance(data, dict):
        return True
    if data.get("schema_version") != REQUIRED_SCHEMA_VERSION:
        return True
    return "packages" not in data or not isinstance(data["packages"], dict)


def x_report_is_malformed__mutmut_4(path: Path) -> bool:
    """True iff the report at ``path`` violates the shape contract.

    A non-existent file is reported by the caller. A present file must be valid JSON declaring
    ``schema_version == REQUIRED_SCHEMA_VERSION`` with a ``packages`` mapping;
    anything else is malformed.
    """
    if not path.exists():
        return False
    try:
        data = json.loads(None)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return True
    if not isinstance(data, dict):
        return True
    if data.get("schema_version") != REQUIRED_SCHEMA_VERSION:
        return True
    return "packages" not in data or not isinstance(data["packages"], dict)


def x_report_is_malformed__mutmut_5(path: Path) -> bool:
    """True iff the report at ``path`` violates the shape contract.

    A non-existent file is reported by the caller. A present file must be valid JSON declaring
    ``schema_version == REQUIRED_SCHEMA_VERSION`` with a ``packages`` mapping;
    anything else is malformed.
    """
    if not path.exists():
        return False
    try:
        data = json.loads(path.read_text(encoding=None))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return True
    if not isinstance(data, dict):
        return True
    if data.get("schema_version") != REQUIRED_SCHEMA_VERSION:
        return True
    return "packages" not in data or not isinstance(data["packages"], dict)


def x_report_is_malformed__mutmut_6(path: Path) -> bool:
    """True iff the report at ``path`` violates the shape contract.

    A non-existent file is reported by the caller. A present file must be valid JSON declaring
    ``schema_version == REQUIRED_SCHEMA_VERSION`` with a ``packages`` mapping;
    anything else is malformed.
    """
    if not path.exists():
        return False
    try:
        data = json.loads(path.read_text(encoding="XXutf-8XX"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return True
    if not isinstance(data, dict):
        return True
    if data.get("schema_version") != REQUIRED_SCHEMA_VERSION:
        return True
    return "packages" not in data or not isinstance(data["packages"], dict)


def x_report_is_malformed__mutmut_7(path: Path) -> bool:
    """True iff the report at ``path`` violates the shape contract.

    A non-existent file is reported by the caller. A present file must be valid JSON declaring
    ``schema_version == REQUIRED_SCHEMA_VERSION`` with a ``packages`` mapping;
    anything else is malformed.
    """
    if not path.exists():
        return False
    try:
        data = json.loads(path.read_text(encoding="UTF-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return True
    if not isinstance(data, dict):
        return True
    if data.get("schema_version") != REQUIRED_SCHEMA_VERSION:
        return True
    return "packages" not in data or not isinstance(data["packages"], dict)


def x_report_is_malformed__mutmut_8(path: Path) -> bool:
    """True iff the report at ``path`` violates the shape contract.

    A non-existent file is reported by the caller. A present file must be valid JSON declaring
    ``schema_version == REQUIRED_SCHEMA_VERSION`` with a ``packages`` mapping;
    anything else is malformed.
    """
    if not path.exists():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return False
    if not isinstance(data, dict):
        return True
    if data.get("schema_version") != REQUIRED_SCHEMA_VERSION:
        return True
    return "packages" not in data or not isinstance(data["packages"], dict)


def x_report_is_malformed__mutmut_9(path: Path) -> bool:
    """True iff the report at ``path`` violates the shape contract.

    A non-existent file is reported by the caller. A present file must be valid JSON declaring
    ``schema_version == REQUIRED_SCHEMA_VERSION`` with a ``packages`` mapping;
    anything else is malformed.
    """
    if not path.exists():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return True
    if isinstance(data, dict):
        return True
    if data.get("schema_version") != REQUIRED_SCHEMA_VERSION:
        return True
    return "packages" not in data or not isinstance(data["packages"], dict)


def x_report_is_malformed__mutmut_10(path: Path) -> bool:
    """True iff the report at ``path`` violates the shape contract.

    A non-existent file is reported by the caller. A present file must be valid JSON declaring
    ``schema_version == REQUIRED_SCHEMA_VERSION`` with a ``packages`` mapping;
    anything else is malformed.
    """
    if not path.exists():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return True
    if not isinstance(data, dict):
        return False
    if data.get("schema_version") != REQUIRED_SCHEMA_VERSION:
        return True
    return "packages" not in data or not isinstance(data["packages"], dict)


def x_report_is_malformed__mutmut_11(path: Path) -> bool:
    """True iff the report at ``path`` violates the shape contract.

    A non-existent file is reported by the caller. A present file must be valid JSON declaring
    ``schema_version == REQUIRED_SCHEMA_VERSION`` with a ``packages`` mapping;
    anything else is malformed.
    """
    if not path.exists():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return True
    if not isinstance(data, dict):
        return True
    if data.get(None) != REQUIRED_SCHEMA_VERSION:
        return True
    return "packages" not in data or not isinstance(data["packages"], dict)


def x_report_is_malformed__mutmut_12(path: Path) -> bool:
    """True iff the report at ``path`` violates the shape contract.

    A non-existent file is reported by the caller. A present file must be valid JSON declaring
    ``schema_version == REQUIRED_SCHEMA_VERSION`` with a ``packages`` mapping;
    anything else is malformed.
    """
    if not path.exists():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return True
    if not isinstance(data, dict):
        return True
    if data.get("XXschema_versionXX") != REQUIRED_SCHEMA_VERSION:
        return True
    return "packages" not in data or not isinstance(data["packages"], dict)


def x_report_is_malformed__mutmut_13(path: Path) -> bool:
    """True iff the report at ``path`` violates the shape contract.

    A non-existent file is reported by the caller. A present file must be valid JSON declaring
    ``schema_version == REQUIRED_SCHEMA_VERSION`` with a ``packages`` mapping;
    anything else is malformed.
    """
    if not path.exists():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return True
    if not isinstance(data, dict):
        return True
    if data.get("SCHEMA_VERSION") != REQUIRED_SCHEMA_VERSION:
        return True
    return "packages" not in data or not isinstance(data["packages"], dict)


def x_report_is_malformed__mutmut_14(path: Path) -> bool:
    """True iff the report at ``path`` violates the shape contract.

    A non-existent file is reported by the caller. A present file must be valid JSON declaring
    ``schema_version == REQUIRED_SCHEMA_VERSION`` with a ``packages`` mapping;
    anything else is malformed.
    """
    if not path.exists():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return True
    if not isinstance(data, dict):
        return True
    if data.get("schema_version") == REQUIRED_SCHEMA_VERSION:
        return True
    return "packages" not in data or not isinstance(data["packages"], dict)


def x_report_is_malformed__mutmut_15(path: Path) -> bool:
    """True iff the report at ``path`` violates the shape contract.

    A non-existent file is reported by the caller. A present file must be valid JSON declaring
    ``schema_version == REQUIRED_SCHEMA_VERSION`` with a ``packages`` mapping;
    anything else is malformed.
    """
    if not path.exists():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return True
    if not isinstance(data, dict):
        return True
    if data.get("schema_version") != REQUIRED_SCHEMA_VERSION:
        return False
    return "packages" not in data or not isinstance(data["packages"], dict)


def x_report_is_malformed__mutmut_16(path: Path) -> bool:
    """True iff the report at ``path`` violates the shape contract.

    A non-existent file is reported by the caller. A present file must be valid JSON declaring
    ``schema_version == REQUIRED_SCHEMA_VERSION`` with a ``packages`` mapping;
    anything else is malformed.
    """
    if not path.exists():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return True
    if not isinstance(data, dict):
        return True
    if data.get("schema_version") != REQUIRED_SCHEMA_VERSION:
        return True
    return "packages" not in data and not isinstance(data["packages"], dict)


def x_report_is_malformed__mutmut_17(path: Path) -> bool:
    """True iff the report at ``path`` violates the shape contract.

    A non-existent file is reported by the caller. A present file must be valid JSON declaring
    ``schema_version == REQUIRED_SCHEMA_VERSION`` with a ``packages`` mapping;
    anything else is malformed.
    """
    if not path.exists():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return True
    if not isinstance(data, dict):
        return True
    if data.get("schema_version") != REQUIRED_SCHEMA_VERSION:
        return True
    return "XXpackagesXX" not in data or not isinstance(data["packages"], dict)


def x_report_is_malformed__mutmut_18(path: Path) -> bool:
    """True iff the report at ``path`` violates the shape contract.

    A non-existent file is reported by the caller. A present file must be valid JSON declaring
    ``schema_version == REQUIRED_SCHEMA_VERSION`` with a ``packages`` mapping;
    anything else is malformed.
    """
    if not path.exists():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return True
    if not isinstance(data, dict):
        return True
    if data.get("schema_version") != REQUIRED_SCHEMA_VERSION:
        return True
    return "PACKAGES" not in data or not isinstance(data["packages"], dict)


def x_report_is_malformed__mutmut_19(path: Path) -> bool:
    """True iff the report at ``path`` violates the shape contract.

    A non-existent file is reported by the caller. A present file must be valid JSON declaring
    ``schema_version == REQUIRED_SCHEMA_VERSION`` with a ``packages`` mapping;
    anything else is malformed.
    """
    if not path.exists():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return True
    if not isinstance(data, dict):
        return True
    if data.get("schema_version") != REQUIRED_SCHEMA_VERSION:
        return True
    return "packages" in data or not isinstance(data["packages"], dict)


def x_report_is_malformed__mutmut_20(path: Path) -> bool:
    """True iff the report at ``path`` violates the shape contract.

    A non-existent file is reported by the caller. A present file must be valid JSON declaring
    ``schema_version == REQUIRED_SCHEMA_VERSION`` with a ``packages`` mapping;
    anything else is malformed.
    """
    if not path.exists():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return True
    if not isinstance(data, dict):
        return True
    if data.get("schema_version") != REQUIRED_SCHEMA_VERSION:
        return True
    return "packages" not in data or isinstance(data["packages"], dict)

mutants_x_report_is_malformed__mutmut['_mutmut_orig'] = x_report_is_malformed__mutmut_orig # type: ignore # mutmut generated
mutants_x_report_is_malformed__mutmut['x_report_is_malformed__mutmut_1'] = x_report_is_malformed__mutmut_1 # type: ignore # mutmut generated
mutants_x_report_is_malformed__mutmut['x_report_is_malformed__mutmut_2'] = x_report_is_malformed__mutmut_2 # type: ignore # mutmut generated
mutants_x_report_is_malformed__mutmut['x_report_is_malformed__mutmut_3'] = x_report_is_malformed__mutmut_3 # type: ignore # mutmut generated
mutants_x_report_is_malformed__mutmut['x_report_is_malformed__mutmut_4'] = x_report_is_malformed__mutmut_4 # type: ignore # mutmut generated
mutants_x_report_is_malformed__mutmut['x_report_is_malformed__mutmut_5'] = x_report_is_malformed__mutmut_5 # type: ignore # mutmut generated
mutants_x_report_is_malformed__mutmut['x_report_is_malformed__mutmut_6'] = x_report_is_malformed__mutmut_6 # type: ignore # mutmut generated
mutants_x_report_is_malformed__mutmut['x_report_is_malformed__mutmut_7'] = x_report_is_malformed__mutmut_7 # type: ignore # mutmut generated
mutants_x_report_is_malformed__mutmut['x_report_is_malformed__mutmut_8'] = x_report_is_malformed__mutmut_8 # type: ignore # mutmut generated
mutants_x_report_is_malformed__mutmut['x_report_is_malformed__mutmut_9'] = x_report_is_malformed__mutmut_9 # type: ignore # mutmut generated
mutants_x_report_is_malformed__mutmut['x_report_is_malformed__mutmut_10'] = x_report_is_malformed__mutmut_10 # type: ignore # mutmut generated
mutants_x_report_is_malformed__mutmut['x_report_is_malformed__mutmut_11'] = x_report_is_malformed__mutmut_11 # type: ignore # mutmut generated
mutants_x_report_is_malformed__mutmut['x_report_is_malformed__mutmut_12'] = x_report_is_malformed__mutmut_12 # type: ignore # mutmut generated
mutants_x_report_is_malformed__mutmut['x_report_is_malformed__mutmut_13'] = x_report_is_malformed__mutmut_13 # type: ignore # mutmut generated
mutants_x_report_is_malformed__mutmut['x_report_is_malformed__mutmut_14'] = x_report_is_malformed__mutmut_14 # type: ignore # mutmut generated
mutants_x_report_is_malformed__mutmut['x_report_is_malformed__mutmut_15'] = x_report_is_malformed__mutmut_15 # type: ignore # mutmut generated
mutants_x_report_is_malformed__mutmut['x_report_is_malformed__mutmut_16'] = x_report_is_malformed__mutmut_16 # type: ignore # mutmut generated
mutants_x_report_is_malformed__mutmut['x_report_is_malformed__mutmut_17'] = x_report_is_malformed__mutmut_17 # type: ignore # mutmut generated
mutants_x_report_is_malformed__mutmut['x_report_is_malformed__mutmut_18'] = x_report_is_malformed__mutmut_18 # type: ignore # mutmut generated
mutants_x_report_is_malformed__mutmut['x_report_is_malformed__mutmut_19'] = x_report_is_malformed__mutmut_19 # type: ignore # mutmut generated
mutants_x_report_is_malformed__mutmut['x_report_is_malformed__mutmut_20'] = x_report_is_malformed__mutmut_20 # type: ignore # mutmut generated
mutants_xǁMutationSurvivalRatchetǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁMutationSurvivalRatchetǁ_abs__mutmut: MutantDict = {}  # type: ignore
mutants_xǁMutationSurvivalRatchetǁenumerate_files__mutmut: MutantDict = {}  # type: ignore
mutants_xǁMutationSurvivalRatchetǁis_in_scope__mutmut: MutantDict = {}  # type: ignore
mutants_xǁMutationSurvivalRatchetǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore


class MutationSurvivalRatchet(FitnessRule):
    """Flags a mutation report that breaks its file-shape contract."""

    name = "mutation-survival-ratchet"
    remediation = REMEDIATION
    extensions = (".json",)

    #: Rule-specific knobs — instance attrs so ``from_config`` overrides them.
    baseline_report: str = DEFAULT_BASELINE_REPORT
    current_report: str = DEFAULT_CURRENT_REPORT

    @classmethod
    @_mutmut_mutated(mutants_xǁMutationSurvivalRatchetǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> MutationSurvivalRatchet:
        """Build from config, reading both required report paths."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, MutationSurvivalRatchet)  # noqa: S101  # narrowing for mypy
        rule.baseline_report = str(config.get("baseline_report", DEFAULT_BASELINE_REPORT))
        rule.current_report = str(config.get("current_report", DEFAULT_CURRENT_REPORT))
        return rule

    @classmethod
    def xǁMutationSurvivalRatchetǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> MutationSurvivalRatchet:
        """Build from config, reading both required report paths."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, MutationSurvivalRatchet)  # noqa: S101  # narrowing for mypy
        rule.baseline_report = str(config.get("baseline_report", DEFAULT_BASELINE_REPORT))
        rule.current_report = str(config.get("current_report", DEFAULT_CURRENT_REPORT))
        return rule

    @classmethod
    def xǁMutationSurvivalRatchetǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> MutationSurvivalRatchet:
        """Build from config, reading both required report paths."""
        rule = None
        assert isinstance(rule, MutationSurvivalRatchet)  # noqa: S101  # narrowing for mypy
        rule.baseline_report = str(config.get("baseline_report", DEFAULT_BASELINE_REPORT))
        rule.current_report = str(config.get("current_report", DEFAULT_CURRENT_REPORT))
        return rule

    @classmethod
    def xǁMutationSurvivalRatchetǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> MutationSurvivalRatchet:
        """Build from config, reading both required report paths."""
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, MutationSurvivalRatchet)  # noqa: S101  # narrowing for mypy
        rule.baseline_report = str(config.get("baseline_report", DEFAULT_BASELINE_REPORT))
        rule.current_report = str(config.get("current_report", DEFAULT_CURRENT_REPORT))
        return rule

    @classmethod
    def xǁMutationSurvivalRatchetǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> MutationSurvivalRatchet:
        """Build from config, reading both required report paths."""
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, MutationSurvivalRatchet)  # noqa: S101  # narrowing for mypy
        rule.baseline_report = str(config.get("baseline_report", DEFAULT_BASELINE_REPORT))
        rule.current_report = str(config.get("current_report", DEFAULT_CURRENT_REPORT))
        return rule

    @classmethod
    def xǁMutationSurvivalRatchetǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> MutationSurvivalRatchet:
        """Build from config, reading both required report paths."""
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, MutationSurvivalRatchet)  # noqa: S101  # narrowing for mypy
        rule.baseline_report = str(config.get("baseline_report", DEFAULT_BASELINE_REPORT))
        rule.current_report = str(config.get("current_report", DEFAULT_CURRENT_REPORT))
        return rule

    @classmethod
    def xǁMutationSurvivalRatchetǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> MutationSurvivalRatchet:
        """Build from config, reading both required report paths."""
        rule = super().from_config(config, )
        assert isinstance(rule, MutationSurvivalRatchet)  # noqa: S101  # narrowing for mypy
        rule.baseline_report = str(config.get("baseline_report", DEFAULT_BASELINE_REPORT))
        rule.current_report = str(config.get("current_report", DEFAULT_CURRENT_REPORT))
        return rule

    @classmethod
    def xǁMutationSurvivalRatchetǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> MutationSurvivalRatchet:
        """Build from config, reading both required report paths."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, MutationSurvivalRatchet)  # noqa: S101  # narrowing for mypy
        rule.baseline_report = None
        rule.current_report = str(config.get("current_report", DEFAULT_CURRENT_REPORT))
        return rule

    @classmethod
    def xǁMutationSurvivalRatchetǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> MutationSurvivalRatchet:
        """Build from config, reading both required report paths."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, MutationSurvivalRatchet)  # noqa: S101  # narrowing for mypy
        rule.baseline_report = str(None)
        rule.current_report = str(config.get("current_report", DEFAULT_CURRENT_REPORT))
        return rule

    @classmethod
    def xǁMutationSurvivalRatchetǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> MutationSurvivalRatchet:
        """Build from config, reading both required report paths."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, MutationSurvivalRatchet)  # noqa: S101  # narrowing for mypy
        rule.baseline_report = str(config.get(None, DEFAULT_BASELINE_REPORT))
        rule.current_report = str(config.get("current_report", DEFAULT_CURRENT_REPORT))
        return rule

    @classmethod
    def xǁMutationSurvivalRatchetǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> MutationSurvivalRatchet:
        """Build from config, reading both required report paths."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, MutationSurvivalRatchet)  # noqa: S101  # narrowing for mypy
        rule.baseline_report = str(config.get("baseline_report", None))
        rule.current_report = str(config.get("current_report", DEFAULT_CURRENT_REPORT))
        return rule

    @classmethod
    def xǁMutationSurvivalRatchetǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> MutationSurvivalRatchet:
        """Build from config, reading both required report paths."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, MutationSurvivalRatchet)  # noqa: S101  # narrowing for mypy
        rule.baseline_report = str(config.get(DEFAULT_BASELINE_REPORT))
        rule.current_report = str(config.get("current_report", DEFAULT_CURRENT_REPORT))
        return rule

    @classmethod
    def xǁMutationSurvivalRatchetǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> MutationSurvivalRatchet:
        """Build from config, reading both required report paths."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, MutationSurvivalRatchet)  # noqa: S101  # narrowing for mypy
        rule.baseline_report = str(config.get("baseline_report", ))
        rule.current_report = str(config.get("current_report", DEFAULT_CURRENT_REPORT))
        return rule

    @classmethod
    def xǁMutationSurvivalRatchetǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> MutationSurvivalRatchet:
        """Build from config, reading both required report paths."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, MutationSurvivalRatchet)  # noqa: S101  # narrowing for mypy
        rule.baseline_report = str(config.get("XXbaseline_reportXX", DEFAULT_BASELINE_REPORT))
        rule.current_report = str(config.get("current_report", DEFAULT_CURRENT_REPORT))
        return rule

    @classmethod
    def xǁMutationSurvivalRatchetǁfrom_config__mutmut_13(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> MutationSurvivalRatchet:
        """Build from config, reading both required report paths."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, MutationSurvivalRatchet)  # noqa: S101  # narrowing for mypy
        rule.baseline_report = str(config.get("BASELINE_REPORT", DEFAULT_BASELINE_REPORT))
        rule.current_report = str(config.get("current_report", DEFAULT_CURRENT_REPORT))
        return rule

    @classmethod
    def xǁMutationSurvivalRatchetǁfrom_config__mutmut_14(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> MutationSurvivalRatchet:
        """Build from config, reading both required report paths."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, MutationSurvivalRatchet)  # noqa: S101  # narrowing for mypy
        rule.baseline_report = str(config.get("baseline_report", DEFAULT_BASELINE_REPORT))
        rule.current_report = None
        return rule

    @classmethod
    def xǁMutationSurvivalRatchetǁfrom_config__mutmut_15(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> MutationSurvivalRatchet:
        """Build from config, reading both required report paths."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, MutationSurvivalRatchet)  # noqa: S101  # narrowing for mypy
        rule.baseline_report = str(config.get("baseline_report", DEFAULT_BASELINE_REPORT))
        rule.current_report = str(None)
        return rule

    @classmethod
    def xǁMutationSurvivalRatchetǁfrom_config__mutmut_16(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> MutationSurvivalRatchet:
        """Build from config, reading both required report paths."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, MutationSurvivalRatchet)  # noqa: S101  # narrowing for mypy
        rule.baseline_report = str(config.get("baseline_report", DEFAULT_BASELINE_REPORT))
        rule.current_report = str(config.get(None, DEFAULT_CURRENT_REPORT))
        return rule

    @classmethod
    def xǁMutationSurvivalRatchetǁfrom_config__mutmut_17(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> MutationSurvivalRatchet:
        """Build from config, reading both required report paths."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, MutationSurvivalRatchet)  # noqa: S101  # narrowing for mypy
        rule.baseline_report = str(config.get("baseline_report", DEFAULT_BASELINE_REPORT))
        rule.current_report = str(config.get("current_report", None))
        return rule

    @classmethod
    def xǁMutationSurvivalRatchetǁfrom_config__mutmut_18(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> MutationSurvivalRatchet:
        """Build from config, reading both required report paths."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, MutationSurvivalRatchet)  # noqa: S101  # narrowing for mypy
        rule.baseline_report = str(config.get("baseline_report", DEFAULT_BASELINE_REPORT))
        rule.current_report = str(config.get(DEFAULT_CURRENT_REPORT))
        return rule

    @classmethod
    def xǁMutationSurvivalRatchetǁfrom_config__mutmut_19(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> MutationSurvivalRatchet:
        """Build from config, reading both required report paths."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, MutationSurvivalRatchet)  # noqa: S101  # narrowing for mypy
        rule.baseline_report = str(config.get("baseline_report", DEFAULT_BASELINE_REPORT))
        rule.current_report = str(config.get("current_report", ))
        return rule

    @classmethod
    def xǁMutationSurvivalRatchetǁfrom_config__mutmut_20(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> MutationSurvivalRatchet:
        """Build from config, reading both required report paths."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, MutationSurvivalRatchet)  # noqa: S101  # narrowing for mypy
        rule.baseline_report = str(config.get("baseline_report", DEFAULT_BASELINE_REPORT))
        rule.current_report = str(config.get("XXcurrent_reportXX", DEFAULT_CURRENT_REPORT))
        return rule

    @classmethod
    def xǁMutationSurvivalRatchetǁfrom_config__mutmut_21(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> MutationSurvivalRatchet:
        """Build from config, reading both required report paths."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, MutationSurvivalRatchet)  # noqa: S101  # narrowing for mypy
        rule.baseline_report = str(config.get("baseline_report", DEFAULT_BASELINE_REPORT))
        rule.current_report = str(config.get("CURRENT_REPORT", DEFAULT_CURRENT_REPORT))
        return rule

    @_mutmut_mutated(mutants_xǁMutationSurvivalRatchetǁ_abs__mutmut)
    def _abs(self, rel: str) -> Path:
        path = Path(rel)
        return path if path.is_absolute() else self._repo_root / path

    def xǁMutationSurvivalRatchetǁ_abs__mutmut_orig(self, rel: str) -> Path:
        path = Path(rel)
        return path if path.is_absolute() else self._repo_root / path

    def xǁMutationSurvivalRatchetǁ_abs__mutmut_1(self, rel: str) -> Path:
        path = None
        return path if path.is_absolute() else self._repo_root / path

    def xǁMutationSurvivalRatchetǁ_abs__mutmut_2(self, rel: str) -> Path:
        path = Path(None)
        return path if path.is_absolute() else self._repo_root / path

    def xǁMutationSurvivalRatchetǁ_abs__mutmut_3(self, rel: str) -> Path:
        path = Path(rel)
        return path if path.is_absolute() else self._repo_root * path

    @_mutmut_mutated(mutants_xǁMutationSurvivalRatchetǁenumerate_files__mutmut)
    def enumerate_files(self) -> list[Path]:
        """The two report artifacts this rule judges: baseline + current.

        Both are always enumerated because either absence is a violation.
        """
        return [self._abs(self.baseline_report), self._abs(self.current_report)]

    def xǁMutationSurvivalRatchetǁenumerate_files__mutmut_orig(self) -> list[Path]:
        """The two report artifacts this rule judges: baseline + current.

        Both are always enumerated because either absence is a violation.
        """
        return [self._abs(self.baseline_report), self._abs(self.current_report)]

    def xǁMutationSurvivalRatchetǁenumerate_files__mutmut_1(self) -> list[Path]:
        """The two report artifacts this rule judges: baseline + current.

        Both are always enumerated because either absence is a violation.
        """
        return [self._abs(None), self._abs(self.current_report)]

    def xǁMutationSurvivalRatchetǁenumerate_files__mutmut_2(self) -> list[Path]:
        """The two report artifacts this rule judges: baseline + current.

        Both are always enumerated because either absence is a violation.
        """
        return [self._abs(self.baseline_report), self._abs(None)]

    @_mutmut_mutated(mutants_xǁMutationSurvivalRatchetǁis_in_scope__mutmut)
    def is_in_scope(self, rel: str) -> bool:
        """Admit the configured report paths regardless of location."""
        return True

    def xǁMutationSurvivalRatchetǁis_in_scope__mutmut_orig(self, rel: str) -> bool:
        """Admit the configured report paths regardless of location."""
        return True

    def xǁMutationSurvivalRatchetǁis_in_scope__mutmut_1(self, rel: str) -> bool:
        """Admit the configured report paths regardless of location."""
        return False

    @_mutmut_mutated(mutants_xǁMutationSurvivalRatchetǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        # Both configured reports are required; a present one must validate.
        if not path.exists():
            return True
        return report_is_malformed(path)

    def xǁMutationSurvivalRatchetǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        # Both configured reports are required; a present one must validate.
        if not path.exists():
            return True
        return report_is_malformed(path)

    def xǁMutationSurvivalRatchetǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        # Both configured reports are required; a present one must validate.
        if path.exists():
            return True
        return report_is_malformed(path)

    def xǁMutationSurvivalRatchetǁfile_has_violation__mutmut_2(self, path: Path) -> bool:
        # Both configured reports are required; a present one must validate.
        if not path.exists():
            return False
        return report_is_malformed(path)

    def xǁMutationSurvivalRatchetǁfile_has_violation__mutmut_3(self, path: Path) -> bool:
        # Both configured reports are required; a present one must validate.
        if not path.exists():
            return True
        return report_is_malformed(None)

mutants_xǁMutationSurvivalRatchetǁfrom_config__mutmut['_mutmut_orig'] = MutationSurvivalRatchet.xǁMutationSurvivalRatchetǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁMutationSurvivalRatchetǁfrom_config__mutmut['xǁMutationSurvivalRatchetǁfrom_config__mutmut_1'] = MutationSurvivalRatchet.xǁMutationSurvivalRatchetǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁMutationSurvivalRatchetǁfrom_config__mutmut['xǁMutationSurvivalRatchetǁfrom_config__mutmut_2'] = MutationSurvivalRatchet.xǁMutationSurvivalRatchetǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁMutationSurvivalRatchetǁfrom_config__mutmut['xǁMutationSurvivalRatchetǁfrom_config__mutmut_3'] = MutationSurvivalRatchet.xǁMutationSurvivalRatchetǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁMutationSurvivalRatchetǁfrom_config__mutmut['xǁMutationSurvivalRatchetǁfrom_config__mutmut_4'] = MutationSurvivalRatchet.xǁMutationSurvivalRatchetǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁMutationSurvivalRatchetǁfrom_config__mutmut['xǁMutationSurvivalRatchetǁfrom_config__mutmut_5'] = MutationSurvivalRatchet.xǁMutationSurvivalRatchetǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁMutationSurvivalRatchetǁfrom_config__mutmut['xǁMutationSurvivalRatchetǁfrom_config__mutmut_6'] = MutationSurvivalRatchet.xǁMutationSurvivalRatchetǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁMutationSurvivalRatchetǁfrom_config__mutmut['xǁMutationSurvivalRatchetǁfrom_config__mutmut_7'] = MutationSurvivalRatchet.xǁMutationSurvivalRatchetǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁMutationSurvivalRatchetǁfrom_config__mutmut['xǁMutationSurvivalRatchetǁfrom_config__mutmut_8'] = MutationSurvivalRatchet.xǁMutationSurvivalRatchetǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁMutationSurvivalRatchetǁfrom_config__mutmut['xǁMutationSurvivalRatchetǁfrom_config__mutmut_9'] = MutationSurvivalRatchet.xǁMutationSurvivalRatchetǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁMutationSurvivalRatchetǁfrom_config__mutmut['xǁMutationSurvivalRatchetǁfrom_config__mutmut_10'] = MutationSurvivalRatchet.xǁMutationSurvivalRatchetǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁMutationSurvivalRatchetǁfrom_config__mutmut['xǁMutationSurvivalRatchetǁfrom_config__mutmut_11'] = MutationSurvivalRatchet.xǁMutationSurvivalRatchetǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁMutationSurvivalRatchetǁfrom_config__mutmut['xǁMutationSurvivalRatchetǁfrom_config__mutmut_12'] = MutationSurvivalRatchet.xǁMutationSurvivalRatchetǁfrom_config__mutmut_12 # type: ignore # mutmut generated
mutants_xǁMutationSurvivalRatchetǁfrom_config__mutmut['xǁMutationSurvivalRatchetǁfrom_config__mutmut_13'] = MutationSurvivalRatchet.xǁMutationSurvivalRatchetǁfrom_config__mutmut_13 # type: ignore # mutmut generated
mutants_xǁMutationSurvivalRatchetǁfrom_config__mutmut['xǁMutationSurvivalRatchetǁfrom_config__mutmut_14'] = MutationSurvivalRatchet.xǁMutationSurvivalRatchetǁfrom_config__mutmut_14 # type: ignore # mutmut generated
mutants_xǁMutationSurvivalRatchetǁfrom_config__mutmut['xǁMutationSurvivalRatchetǁfrom_config__mutmut_15'] = MutationSurvivalRatchet.xǁMutationSurvivalRatchetǁfrom_config__mutmut_15 # type: ignore # mutmut generated
mutants_xǁMutationSurvivalRatchetǁfrom_config__mutmut['xǁMutationSurvivalRatchetǁfrom_config__mutmut_16'] = MutationSurvivalRatchet.xǁMutationSurvivalRatchetǁfrom_config__mutmut_16 # type: ignore # mutmut generated
mutants_xǁMutationSurvivalRatchetǁfrom_config__mutmut['xǁMutationSurvivalRatchetǁfrom_config__mutmut_17'] = MutationSurvivalRatchet.xǁMutationSurvivalRatchetǁfrom_config__mutmut_17 # type: ignore # mutmut generated
mutants_xǁMutationSurvivalRatchetǁfrom_config__mutmut['xǁMutationSurvivalRatchetǁfrom_config__mutmut_18'] = MutationSurvivalRatchet.xǁMutationSurvivalRatchetǁfrom_config__mutmut_18 # type: ignore # mutmut generated
mutants_xǁMutationSurvivalRatchetǁfrom_config__mutmut['xǁMutationSurvivalRatchetǁfrom_config__mutmut_19'] = MutationSurvivalRatchet.xǁMutationSurvivalRatchetǁfrom_config__mutmut_19 # type: ignore # mutmut generated
mutants_xǁMutationSurvivalRatchetǁfrom_config__mutmut['xǁMutationSurvivalRatchetǁfrom_config__mutmut_20'] = MutationSurvivalRatchet.xǁMutationSurvivalRatchetǁfrom_config__mutmut_20 # type: ignore # mutmut generated
mutants_xǁMutationSurvivalRatchetǁfrom_config__mutmut['xǁMutationSurvivalRatchetǁfrom_config__mutmut_21'] = MutationSurvivalRatchet.xǁMutationSurvivalRatchetǁfrom_config__mutmut_21 # type: ignore # mutmut generated

mutants_xǁMutationSurvivalRatchetǁ_abs__mutmut['_mutmut_orig'] = MutationSurvivalRatchet.xǁMutationSurvivalRatchetǁ_abs__mutmut_orig # type: ignore # mutmut generated
mutants_xǁMutationSurvivalRatchetǁ_abs__mutmut['xǁMutationSurvivalRatchetǁ_abs__mutmut_1'] = MutationSurvivalRatchet.xǁMutationSurvivalRatchetǁ_abs__mutmut_1 # type: ignore # mutmut generated
mutants_xǁMutationSurvivalRatchetǁ_abs__mutmut['xǁMutationSurvivalRatchetǁ_abs__mutmut_2'] = MutationSurvivalRatchet.xǁMutationSurvivalRatchetǁ_abs__mutmut_2 # type: ignore # mutmut generated
mutants_xǁMutationSurvivalRatchetǁ_abs__mutmut['xǁMutationSurvivalRatchetǁ_abs__mutmut_3'] = MutationSurvivalRatchet.xǁMutationSurvivalRatchetǁ_abs__mutmut_3 # type: ignore # mutmut generated

mutants_xǁMutationSurvivalRatchetǁenumerate_files__mutmut['_mutmut_orig'] = MutationSurvivalRatchet.xǁMutationSurvivalRatchetǁenumerate_files__mutmut_orig # type: ignore # mutmut generated
mutants_xǁMutationSurvivalRatchetǁenumerate_files__mutmut['xǁMutationSurvivalRatchetǁenumerate_files__mutmut_1'] = MutationSurvivalRatchet.xǁMutationSurvivalRatchetǁenumerate_files__mutmut_1 # type: ignore # mutmut generated
mutants_xǁMutationSurvivalRatchetǁenumerate_files__mutmut['xǁMutationSurvivalRatchetǁenumerate_files__mutmut_2'] = MutationSurvivalRatchet.xǁMutationSurvivalRatchetǁenumerate_files__mutmut_2 # type: ignore # mutmut generated

mutants_xǁMutationSurvivalRatchetǁis_in_scope__mutmut['_mutmut_orig'] = MutationSurvivalRatchet.xǁMutationSurvivalRatchetǁis_in_scope__mutmut_orig # type: ignore # mutmut generated
mutants_xǁMutationSurvivalRatchetǁis_in_scope__mutmut['xǁMutationSurvivalRatchetǁis_in_scope__mutmut_1'] = MutationSurvivalRatchet.xǁMutationSurvivalRatchetǁis_in_scope__mutmut_1 # type: ignore # mutmut generated

mutants_xǁMutationSurvivalRatchetǁfile_has_violation__mutmut['_mutmut_orig'] = MutationSurvivalRatchet.xǁMutationSurvivalRatchetǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁMutationSurvivalRatchetǁfile_has_violation__mutmut['xǁMutationSurvivalRatchetǁfile_has_violation__mutmut_1'] = MutationSurvivalRatchet.xǁMutationSurvivalRatchetǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_xǁMutationSurvivalRatchetǁfile_has_violation__mutmut['xǁMutationSurvivalRatchetǁfile_has_violation__mutmut_2'] = MutationSurvivalRatchet.xǁMutationSurvivalRatchetǁfile_has_violation__mutmut_2 # type: ignore # mutmut generated
mutants_xǁMutationSurvivalRatchetǁfile_has_violation__mutmut['xǁMutationSurvivalRatchetǁfile_has_violation__mutmut_3'] = MutationSurvivalRatchet.xǁMutationSurvivalRatchetǁfile_has_violation__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> MutationSurvivalRatchet:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return MutationSurvivalRatchet.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> MutationSurvivalRatchet:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return MutationSurvivalRatchet.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> MutationSurvivalRatchet:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return MutationSurvivalRatchet.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> MutationSurvivalRatchet:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return MutationSurvivalRatchet.from_config(config, repo_root=None)


def x_build__mutmut_3(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> MutationSurvivalRatchet:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return MutationSurvivalRatchet.from_config(repo_root=repo_root)


def x_build__mutmut_4(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> MutationSurvivalRatchet:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return MutationSurvivalRatchet.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(MutationSurvivalRatchet, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(MutationSurvivalRatchet, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(MutationSurvivalRatchet, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(MutationSurvivalRatchet, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
