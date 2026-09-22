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
    "no_duplicated_dependency_pin": frozenset({"manifest", "min_version_parts"}),
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
    "python_dependency_surface": frozenset({"manifest_patterns", "canonical_manifests", "ratchets"}),
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
