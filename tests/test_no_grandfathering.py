"""Public contracts: fitness findings are never adopted or suppressed."""

from __future__ import annotations

from pathlib import Path

import pytest

import tc_fitness
from tc_fitness.catalogue import RuleEntry
from tc_fitness.check_contract_policy import validate_contract_configuration
from tc_fitness.check_contracts import CheckContractError
from tc_fitness.core_checks import run_core_check
from tc_fitness.core_checks.ci_consumes_shared_gate import build as build_ci_gate
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.gate_config import GateConfigError, parse_config
from tc_fitness.lib import gate, gate_keys
from tc_fitness.runner import main_cli, run

pytestmark = pytest.mark.integration


class _AlwaysFails(FitnessRule):
    name = "always-fails"
    remediation = "fix: remove the violation; next: retry; run: tc-fitness run"
    extensions = (".txt",)

    def file_has_violation(self, path: Path) -> bool:
        return True


def _write_violation(root: Path) -> None:
    source = root / "src" / "bad.txt"
    source.parent.mkdir(parents=True)
    source.write_text("bad\n", encoding="utf-8")


def _write_legacy_baseline(root: Path, name: str, entry: str) -> Path:
    path = root / ".architecture" / "baseline" / f"{name}-files.txt"
    path.parent.mkdir(parents=True)
    path.write_text(f"{entry}\n", encoding="utf-8")
    return path


def test_existing_file_baseline_cannot_suppress_a_finding(tmp_path: Path) -> None:
    baseline = _write_legacy_baseline(tmp_path, "always-fails", "src/bad.txt")
    assert (
        gate(
            "always-fails",
            {Path("src/bad.txt")},
            _AlwaysFails.remediation,
            repo_root=tmp_path,
        )
        == 1
    )
    assert baseline.read_text(encoding="utf-8") == "src/bad.txt\n"


def test_existing_key_baseline_cannot_suppress_a_finding(tmp_path: Path) -> None:
    baseline = tmp_path / ".architecture" / "baseline" / "rule-ids.txt"
    baseline.parent.mkdir(parents=True)
    baseline.write_text("known-violation\n", encoding="utf-8")
    assert gate_keys("rule", {"known-violation"}, "fix it", repo_root=tmp_path) == 1


def test_rule_run_fails_without_creating_or_reading_a_baseline(tmp_path: Path) -> None:
    _write_violation(tmp_path)
    baseline = _write_legacy_baseline(tmp_path, "always-fails", "src/bad.txt")
    before = baseline.read_bytes()

    rule = _AlwaysFails(tmp_path, roots=("src",))

    assert rule.run() == 1
    assert baseline.read_bytes() == before
    assert not hasattr(rule, "establish_baseline")
    assert not hasattr(rule, "load_baseline")


def test_core_cli_rejects_establish_baseline_without_writing(tmp_path: Path) -> None:
    _write_violation(tmp_path)
    with pytest.raises(SystemExit) as exc:
        run_core_check(
            _AlwaysFails,
            ["--establish-baseline", "--repo-root", str(tmp_path)],
            config={"roots": ["src"]},
        )
    assert exc.value.code == 2
    assert not (tmp_path / ".architecture" / "baseline").exists()


def test_catalogue_cli_rejects_establish_baseline_without_writing(tmp_path: Path) -> None:
    entry = RuleEntry(id="always", gate="always", check="core:license_present")
    with pytest.raises(SystemExit) as exc:
        main_cli((entry,), ["--establish-baseline"], repo_root=tmp_path)
    assert exc.value.code == 2
    assert not (tmp_path / ".architecture" / "baseline").exists()


def test_runner_api_has_no_establish_baseline_argument(tmp_path: Path) -> None:
    with pytest.raises(TypeError, match="establish_baseline"):
        run((), repo_root=tmp_path, establish_baseline=True)  # type: ignore[call-arg]


@pytest.mark.parametrize("option", ["warn_only", "baseline_ok"])
@pytest.mark.parametrize("value", [False, True])
def test_ci_gate_rejects_advisory_configuration_even_when_false(
    tmp_path: Path, option: str, value: bool
) -> None:
    with pytest.raises(ValueError, match=option):
        build_ci_gate({option: value}, repo_root=tmp_path)
    with pytest.raises(CheckContractError, match=option):
        validate_contract_configuration("core:ci_consumes_shared_gate", {option: value})


def test_gate_config_rejects_removed_baseline_free_option(tmp_path: Path) -> None:
    table = {"steps": [{"id": "checks", "run": ["pytest"], "baseline_free": False}]}
    with pytest.raises(GateConfigError, match="baseline_free"):
        parse_config(table, source=tmp_path / ".tc-fitness.toml")


def test_package_does_not_export_baseline_adoption_api() -> None:
    for name in (
        "BASELINE_DIRNAME",
        "BASELINE_SUFFIX",
        "baseline_dir",
        "baseline_path",
        "establish_baseline",
        "load_baseline",
        "parse_baseline_text",
        "render_baseline",
        "baseline_shrink_only",
        "find_net_new_violations",
        "load_all_baselines",
        "net_new_violations_forbidden",
    ):
        assert not hasattr(tc_fitness, name)


@pytest.mark.parametrize(
    "option",
    [
        "allowed_names",
        "allow_missing_current",
        "baseline_ok",
        "cutover_ref",
        "excluded_parts",
        "excluded_segments",
        "exempt_dirs",
        "exempt_extensions",
        "exempt_files",
        "exempt_keys",
        "exempt_prefixes",
        "exempt_roots",
        "exempt_segments",
        "exempt_specifiers",
        "informational_marker",
        "skip_dir_segments",
        "skip_parts",
        "test_file_regex",
        "warn_only",
    ],
)
@pytest.mark.parametrize("value", [False, [], ["src/known-violation.py"]])
def test_rule_configuration_cannot_suppress_a_finding(tmp_path: Path, option: str, value: object) -> None:
    with pytest.raises(ValueError, match=option):
        _AlwaysFails.from_config({option: value}, repo_root=tmp_path)
