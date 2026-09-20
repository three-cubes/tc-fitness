"""Reviewed configuration boundary for unsuppressed CORE contract assurance.

This inventory belongs to assurance, not consumer configuration. Every new CORE
option needs classification here before a contract can use it. Unknown aliases
fail closed; ordinary consumers continue to use each check's own from_config.
Scope, detector predicates and expected identities are policy inputs. Adoption
switches, missing-input passes and post-selection exceptions are not evidence.
"""

from __future__ import annotations

from collections.abc import Mapping

from tc_fitness.check_contracts import CheckContractError

_FILE_OPTIONS = frozenset({"roots", "extensions", "name"})
_COVERAGE_EVIDENCE_OPTIONS = frozenset(
    {
        "exact_base_commit",
        "candidate_commit",
        "coverage_receipt",
        "coverage_receipt_digest",
        "accepted_coverage_receipt",
        "accepted_coverage_digest",
        "coverage_config",
        "run_id",
        "attempt_id",
        "max_age_seconds",
    }
)
_RUNTIME_OPTIONS = frozenset(
    {
        "contract_file",
        "evidence_file",
        "environment",
        "target",
        "expected_identity",
        "expected_source_sha",
        "expected_image_digest",
        "expected_host_id",
        "expected_runtime_user",
        "expected_deployment_id",
        "expected_configuration_identity",
        "expected_run_id",
        "expected_attempt_id",
        "required_checks",
        "max_age_seconds",
    }
)

# Exact options read by current CORE configuration paths. Suppressive options
# are absent so their presence is rejected as an unreviewed option.
_CORE_OPTIONS: dict[str, frozenset[str]] = {
    "actionable_feedback": frozenset({"markers"}),
    "adr_number_unique": frozenset({"record_dir", "record_pattern"}),
    "behavioural_evidence": frozenset({"behaviour_markers", "surface_globs", "claims"}),
    "bicep_arm_lint": frozenset(),
    "canonical_commit_identity": frozenset(
        {"allowed_emails", "allowed_name_patterns", "base_ref", "head_ref"}
    ),
    "checkov_iac_security": frozenset({"scan_dir", "framework", "timeout"}),
    "ci_consumes_shared_gate": frozenset({"workflows_dir", "reusable_pattern", "engine_pattern"}),
    "ci_fanin_parity": frozenset({"workflow", "aggregator_name"}),
    "ci_silencers_have_rationale": frozenset(
        {"rationale_tokens", "silencer_patterns", "window", "workflows_dir", "scan_files"}
    ),
    "cognitive_complexity": frozenset({"threshold"}),
    "contract_change_has_test": frozenset({"contract_surface", "test_globs", "base_ref"}),
    "coverage_floor": frozenset({"floor_pct", "coverage_report", "branch_floor_pct", "critical_branch_files"})
    | _COVERAGE_EVIDENCE_OPTIONS,
    "coverage_includes_branches": frozenset({"coverage_report"}),
    "deterministic_tests": frozenset(
        {"seed", "repeats", "order_seeds", "test_command", "use_randomly", "timeout_seconds"}
    ),
    "empty_body_intent": frozenset({"marker"}),
    "engine_version_floor": frozenset({"floor", "package"}),
    "every_test_has_tier_marker": frozenset({"tier_markers", "require_module_marker"}),
    "harness_canon_reference": frozenset(
        {"repo_type", "required_files", "banner_marker", "standards_ref_pattern", "banner_path"}
    ),
    "integrity_state_predicate": frozenset({"state_tables"}),
    "license_present": frozenset({"markers", "header_lines"}),
    "mutation_survival_ratchet": frozenset({"baseline_report", "current_report"}),
    "new_code_coverage": frozenset({"floor_pct", "coverage_report", "base_ref"}) | _COVERAGE_EVIDENCE_OPTIONS,
    "no_commented_out_code": frozenset({"min_run"}),
    "no_duplicate_string": frozenset({"min_length", "min_occurrences"}),
    "no_env_monkeypatch": frozenset({"env_prefixes"}),
    "no_hardcoded_repo_paths": frozenset({"needles"}),
    "no_internal_monkeypatch": frozenset({"internal_packages"}),
    "no_internal_patches": frozenset({"internal_roots"}),
    "no_internal_patches_ts": frozenset({"internal_packages"}),
    "no_language_suffix_in_package_names": frozenset(
        {"boundary_roots", "marker_roots", "marker_file", "forbidden_suffixes"}
    ),
    "no_llm_attribution": frozenset(),
    "no_logging_secrets": frozenset({"secret_patterns", "log_methods", "direct_sinks"}),
    "no_noop_test_scripts": frozenset(
        {"prod_package_prefixes", "placeholder_pattern", "real_runner_pattern"}
    ),
    "no_production_suppressions": frozenset({"suppression_patterns"}),
    "no_real_names": frozenset({"tokens", "substitutions", "scope_segments"}),
    "no_test_doubles_in_runtime_tiers": frozenset({"runtime_markers", "forbidden_keyword_arguments"}),
    "no_test_imports_in_prod": frozenset({"forbidden_import_roots"}),
    "no_test_only_kwargs": frozenset({"seam_suffixes"}),
    "osv_scanner_sca": frozenset({"scanner_version", "lockfiles", "required", "timeout"}),
    "path_naming": frozenset({"kebab_roots", "snake_roots"}),
    "pattern_chokepoint": frozenset({"patterns", "chokepoint_files"}),
    "posix_path_serialisation": frozenset(),
    "readme_resolver_coverage": frozenset({"resolver_file"}),
    "runtime_evidence_contract": _RUNTIME_OPTIONS,
    "runtime_filesystem_contract": _RUNTIME_OPTIONS,
    "schema_conformance": frozenset({"required_keys"}),
    "script_help_smoke": frozenset({"help_timeout_seconds", "python_executable"}),
    "shellcheck_disable_with_reason": frozenset({"rationale_markers", "min_rationale_len"}),
    "sonar_ignore_rationale": frozenset({"sonar_file", "rule_key_pattern"}),
    "suppressions_have_rationale": frozenset({"bare_patterns"}),
    "test_skip_rationale": frozenset({"importorskip_lookback"}),
    "untrusted_automation_boundary": frozenset(
        {
            "workflows",
            "untrusted_action_prefixes",
            "privileged_action_prefixes",
            "privileged_permissions",
            "credential_env_names",
            "credential_command_markers",
            "runtime_contract_roots",
            "contract_keys",
        }
    ),
    "unused_params_named": frozenset(),
}
_CUSTOM_CONFIGURATION = frozenset(
    {
        "behavioural_evidence",
        "checkov_iac_security",
        "osv_scanner_sca",
        "runtime_evidence_contract",
        "runtime_filesystem_contract",
    }
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x_validate_contract_configuration__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_validate_contract_configuration__mutmut)
def validate_contract_configuration(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("core:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name == "osv_scanner_sca" and config.get("required") is not True:
        raise CheckContractError("OSV contract requires required=true")
    if name == "every_test_has_tier_marker" and config.get("require_module_marker") is not True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_orig(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("core:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name == "osv_scanner_sca" and config.get("required") is not True:
        raise CheckContractError("OSV contract requires required=true")
    if name == "every_test_has_tier_marker" and config.get("require_module_marker") is not True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_1(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = None
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name == "osv_scanner_sca" and config.get("required") is not True:
        raise CheckContractError("OSV contract requires required=true")
    if name == "every_test_has_tier_marker" and config.get("require_module_marker") is not True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_2(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix(None)
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name == "osv_scanner_sca" and config.get("required") is not True:
        raise CheckContractError("OSV contract requires required=true")
    if name == "every_test_has_tier_marker" and config.get("require_module_marker") is not True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_3(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removesuffix("core:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name == "osv_scanner_sca" and config.get("required") is not True:
        raise CheckContractError("OSV contract requires required=true")
    if name == "every_test_has_tier_marker" and config.get("require_module_marker") is not True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_4(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("XXcore:XX")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name == "osv_scanner_sca" and config.get("required") is not True:
        raise CheckContractError("OSV contract requires required=true")
    if name == "every_test_has_tier_marker" and config.get("require_module_marker") is not True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_5(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("CORE:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name == "osv_scanner_sca" and config.get("required") is not True:
        raise CheckContractError("OSV contract requires required=true")
    if name == "every_test_has_tier_marker" and config.get("require_module_marker") is not True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_6(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("core:")
    if name in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name == "osv_scanner_sca" and config.get("required") is not True:
        raise CheckContractError("OSV contract requires required=true")
    if name == "every_test_has_tier_marker" and config.get("require_module_marker") is not True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_7(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("core:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(None)
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name == "osv_scanner_sca" and config.get("required") is not True:
        raise CheckContractError("OSV contract requires required=true")
    if name == "every_test_has_tier_marker" and config.get("require_module_marker") is not True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_8(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("core:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = None
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name == "osv_scanner_sca" and config.get("required") is not True:
        raise CheckContractError("OSV contract requires required=true")
    if name == "every_test_has_tier_marker" and config.get("require_module_marker") is not True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_9(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("core:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name == "osv_scanner_sca" and config.get("required") is not True:
        raise CheckContractError("OSV contract requires required=true")
    if name == "every_test_has_tier_marker" and config.get("require_module_marker") is not True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_10(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("core:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed = _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name == "osv_scanner_sca" and config.get("required") is not True:
        raise CheckContractError("OSV contract requires required=true")
    if name == "every_test_has_tier_marker" and config.get("require_module_marker") is not True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_11(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("core:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed &= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name == "osv_scanner_sca" and config.get("required") is not True:
        raise CheckContractError("OSV contract requires required=true")
    if name == "every_test_has_tier_marker" and config.get("require_module_marker") is not True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_12(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("core:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = None
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name == "osv_scanner_sca" and config.get("required") is not True:
        raise CheckContractError("OSV contract requires required=true")
    if name == "every_test_has_tier_marker" and config.get("require_module_marker") is not True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_13(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("core:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) + allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name == "osv_scanner_sca" and config.get("required") is not True:
        raise CheckContractError("OSV contract requires required=true")
    if name == "every_test_has_tier_marker" and config.get("require_module_marker") is not True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_14(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("core:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(None) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name == "osv_scanner_sca" and config.get("required") is not True:
        raise CheckContractError("OSV contract requires required=true")
    if name == "every_test_has_tier_marker" and config.get("require_module_marker") is not True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_15(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("core:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(None)
    if name == "osv_scanner_sca" and config.get("required") is not True:
        raise CheckContractError("OSV contract requires required=true")
    if name == "every_test_has_tier_marker" and config.get("require_module_marker") is not True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_16(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("core:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(None)}")
    if name == "osv_scanner_sca" and config.get("required") is not True:
        raise CheckContractError("OSV contract requires required=true")
    if name == "every_test_has_tier_marker" and config.get("require_module_marker") is not True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_17(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("core:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {'XX, XX'.join(sorted(unknown))}")
    if name == "osv_scanner_sca" and config.get("required") is not True:
        raise CheckContractError("OSV contract requires required=true")
    if name == "every_test_has_tier_marker" and config.get("require_module_marker") is not True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_18(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("core:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(None))}")
    if name == "osv_scanner_sca" and config.get("required") is not True:
        raise CheckContractError("OSV contract requires required=true")
    if name == "every_test_has_tier_marker" and config.get("require_module_marker") is not True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_19(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("core:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name == "osv_scanner_sca" or config.get("required") is not True:
        raise CheckContractError("OSV contract requires required=true")
    if name == "every_test_has_tier_marker" and config.get("require_module_marker") is not True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_20(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("core:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name != "osv_scanner_sca" and config.get("required") is not True:
        raise CheckContractError("OSV contract requires required=true")
    if name == "every_test_has_tier_marker" and config.get("require_module_marker") is not True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_21(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("core:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name == "XXosv_scanner_scaXX" and config.get("required") is not True:
        raise CheckContractError("OSV contract requires required=true")
    if name == "every_test_has_tier_marker" and config.get("require_module_marker") is not True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_22(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("core:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name == "OSV_SCANNER_SCA" and config.get("required") is not True:
        raise CheckContractError("OSV contract requires required=true")
    if name == "every_test_has_tier_marker" and config.get("require_module_marker") is not True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_23(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("core:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name == "osv_scanner_sca" and config.get(None) is not True:
        raise CheckContractError("OSV contract requires required=true")
    if name == "every_test_has_tier_marker" and config.get("require_module_marker") is not True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_24(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("core:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name == "osv_scanner_sca" and config.get("XXrequiredXX") is not True:
        raise CheckContractError("OSV contract requires required=true")
    if name == "every_test_has_tier_marker" and config.get("require_module_marker") is not True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_25(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("core:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name == "osv_scanner_sca" and config.get("REQUIRED") is not True:
        raise CheckContractError("OSV contract requires required=true")
    if name == "every_test_has_tier_marker" and config.get("require_module_marker") is not True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_26(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("core:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name == "osv_scanner_sca" and config.get("required") is True:
        raise CheckContractError("OSV contract requires required=true")
    if name == "every_test_has_tier_marker" and config.get("require_module_marker") is not True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_27(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("core:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name == "osv_scanner_sca" and config.get("required") is not False:
        raise CheckContractError("OSV contract requires required=true")
    if name == "every_test_has_tier_marker" and config.get("require_module_marker") is not True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_28(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("core:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name == "osv_scanner_sca" and config.get("required") is not True:
        raise CheckContractError(None)
    if name == "every_test_has_tier_marker" and config.get("require_module_marker") is not True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_29(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("core:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name == "osv_scanner_sca" and config.get("required") is not True:
        raise CheckContractError("XXOSV contract requires required=trueXX")
    if name == "every_test_has_tier_marker" and config.get("require_module_marker") is not True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_30(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("core:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name == "osv_scanner_sca" and config.get("required") is not True:
        raise CheckContractError("osv contract requires required=true")
    if name == "every_test_has_tier_marker" and config.get("require_module_marker") is not True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_31(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("core:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name == "osv_scanner_sca" and config.get("required") is not True:
        raise CheckContractError("OSV CONTRACT REQUIRES REQUIRED=TRUE")
    if name == "every_test_has_tier_marker" and config.get("require_module_marker") is not True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_32(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("core:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name == "osv_scanner_sca" and config.get("required") is not True:
        raise CheckContractError("OSV contract requires required=true")
    if name == "every_test_has_tier_marker" or config.get("require_module_marker") is not True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_33(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("core:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name == "osv_scanner_sca" and config.get("required") is not True:
        raise CheckContractError("OSV contract requires required=true")
    if name != "every_test_has_tier_marker" and config.get("require_module_marker") is not True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_34(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("core:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name == "osv_scanner_sca" and config.get("required") is not True:
        raise CheckContractError("OSV contract requires required=true")
    if name == "XXevery_test_has_tier_markerXX" and config.get("require_module_marker") is not True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_35(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("core:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name == "osv_scanner_sca" and config.get("required") is not True:
        raise CheckContractError("OSV contract requires required=true")
    if name == "EVERY_TEST_HAS_TIER_MARKER" and config.get("require_module_marker") is not True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_36(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("core:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name == "osv_scanner_sca" and config.get("required") is not True:
        raise CheckContractError("OSV contract requires required=true")
    if name == "every_test_has_tier_marker" and config.get(None) is not True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_37(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("core:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name == "osv_scanner_sca" and config.get("required") is not True:
        raise CheckContractError("OSV contract requires required=true")
    if name == "every_test_has_tier_marker" and config.get("XXrequire_module_markerXX") is not True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_38(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("core:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name == "osv_scanner_sca" and config.get("required") is not True:
        raise CheckContractError("OSV contract requires required=true")
    if name == "every_test_has_tier_marker" and config.get("REQUIRE_MODULE_MARKER") is not True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_39(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("core:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name == "osv_scanner_sca" and config.get("required") is not True:
        raise CheckContractError("OSV contract requires required=true")
    if name == "every_test_has_tier_marker" and config.get("require_module_marker") is True:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_40(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("core:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name == "osv_scanner_sca" and config.get("required") is not True:
        raise CheckContractError("OSV contract requires required=true")
    if name == "every_test_has_tier_marker" and config.get("require_module_marker") is not False:
        raise CheckContractError("tier contract requires require_module_marker=true")


def x_validate_contract_configuration__mutmut_41(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("core:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name == "osv_scanner_sca" and config.get("required") is not True:
        raise CheckContractError("OSV contract requires required=true")
    if name == "every_test_has_tier_marker" and config.get("require_module_marker") is not True:
        raise CheckContractError(None)


def x_validate_contract_configuration__mutmut_42(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("core:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name == "osv_scanner_sca" and config.get("required") is not True:
        raise CheckContractError("OSV contract requires required=true")
    if name == "every_test_has_tier_marker" and config.get("require_module_marker") is not True:
        raise CheckContractError("XXtier contract requires require_module_marker=trueXX")


def x_validate_contract_configuration__mutmut_43(check: str, config: Mapping[str, object]) -> None:
    """Admit only reviewed options with adoption and exclusion overrides off."""
    name = check.removeprefix("core:")
    if name not in _CORE_OPTIONS:
        raise CheckContractError(f"no reviewed contract configuration policy for {check}")
    allowed = _CORE_OPTIONS[name]
    if name not in _CUSTOM_CONFIGURATION:
        allowed |= _FILE_OPTIONS
    unknown = set(config) - allowed
    if unknown:
        raise CheckContractError(f"unreviewed contract configuration option(s): {', '.join(sorted(unknown))}")
    if name == "osv_scanner_sca" and config.get("required") is not True:
        raise CheckContractError("OSV contract requires required=true")
    if name == "every_test_has_tier_marker" and config.get("require_module_marker") is not True:
        raise CheckContractError("TIER CONTRACT REQUIRES REQUIRE_MODULE_MARKER=TRUE")

mutants_x_validate_contract_configuration__mutmut['_mutmut_orig'] = x_validate_contract_configuration__mutmut_orig # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_1'] = x_validate_contract_configuration__mutmut_1 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_2'] = x_validate_contract_configuration__mutmut_2 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_3'] = x_validate_contract_configuration__mutmut_3 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_4'] = x_validate_contract_configuration__mutmut_4 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_5'] = x_validate_contract_configuration__mutmut_5 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_6'] = x_validate_contract_configuration__mutmut_6 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_7'] = x_validate_contract_configuration__mutmut_7 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_8'] = x_validate_contract_configuration__mutmut_8 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_9'] = x_validate_contract_configuration__mutmut_9 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_10'] = x_validate_contract_configuration__mutmut_10 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_11'] = x_validate_contract_configuration__mutmut_11 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_12'] = x_validate_contract_configuration__mutmut_12 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_13'] = x_validate_contract_configuration__mutmut_13 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_14'] = x_validate_contract_configuration__mutmut_14 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_15'] = x_validate_contract_configuration__mutmut_15 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_16'] = x_validate_contract_configuration__mutmut_16 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_17'] = x_validate_contract_configuration__mutmut_17 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_18'] = x_validate_contract_configuration__mutmut_18 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_19'] = x_validate_contract_configuration__mutmut_19 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_20'] = x_validate_contract_configuration__mutmut_20 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_21'] = x_validate_contract_configuration__mutmut_21 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_22'] = x_validate_contract_configuration__mutmut_22 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_23'] = x_validate_contract_configuration__mutmut_23 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_24'] = x_validate_contract_configuration__mutmut_24 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_25'] = x_validate_contract_configuration__mutmut_25 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_26'] = x_validate_contract_configuration__mutmut_26 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_27'] = x_validate_contract_configuration__mutmut_27 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_28'] = x_validate_contract_configuration__mutmut_28 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_29'] = x_validate_contract_configuration__mutmut_29 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_30'] = x_validate_contract_configuration__mutmut_30 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_31'] = x_validate_contract_configuration__mutmut_31 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_32'] = x_validate_contract_configuration__mutmut_32 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_33'] = x_validate_contract_configuration__mutmut_33 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_34'] = x_validate_contract_configuration__mutmut_34 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_35'] = x_validate_contract_configuration__mutmut_35 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_36'] = x_validate_contract_configuration__mutmut_36 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_37'] = x_validate_contract_configuration__mutmut_37 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_38'] = x_validate_contract_configuration__mutmut_38 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_39'] = x_validate_contract_configuration__mutmut_39 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_40'] = x_validate_contract_configuration__mutmut_40 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_41'] = x_validate_contract_configuration__mutmut_41 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_42'] = x_validate_contract_configuration__mutmut_42 # type: ignore # mutmut generated
mutants_x_validate_contract_configuration__mutmut['x_validate_contract_configuration__mutmut_43'] = x_validate_contract_configuration__mutmut_43 # type: ignore # mutmut generated
