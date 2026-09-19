"""CORE check for digest-bound, independently identified runtime evidence."""

from __future__ import annotations

import hashlib
import re
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from typing import Any, cast

from tc_fitness.check_evidence import report_finding
from tc_fitness.core_checks import run_core_check
from tc_fitness.core_checks._runtime_contracts import (
    ContractDocuments,
    ContractFinding,
    RuntimeContractRule,
    canonical_json_bytes,
    is_integer_identity,
    is_sha256_digest,
    sort_findings,
)
from tc_fitness.lib import remediation as _remediation

_SHA256_RE = re.compile(r"sha256:[0-9a-f]{64}\Z")
_SOURCE_SHA_RE = re.compile(r"[0-9a-f]{40}(?:[0-9a-f]{24})?\Z")
_BASE_IDENTITY_FIELDS = ("source_sha", "image_digest", "host_id", "runtime_user")
_STRING_RECEIPT_IDENTITIES = ("deployment_id", "configuration_identity")
_INTEGER_RECEIPT_IDENTITIES = ("run_id", "attempt_id")
_IDENTITY_FIELDS = (*_BASE_IDENTITY_FIELDS, *_STRING_RECEIPT_IDENTITIES, *_INTEGER_RECEIPT_IDENTITIES)
_CHECK_STATUSES = frozenset({"passed", "failed", "skipped", "expected-denial"})
_FAILURE_OBSERVATIONS = frozenset({"denied", "error", "failed", "failure", "false", "rejected", "unhealthy"})

REMEDIATION = _remediation(
    fix=(
        "collect a complete runtime receipt for the exact selected contract, source commit, immutable "
        "artifact, host and runtime user; retain and hash every referenced diagnostic artifact"
    ),
    nxt="re-run evidence verification with independently supplied expected identity values",
    run="tc-fitness-runtime-contract verify-evidence --help",
    passing="fresh evidence with matching identities, observed required checks and verified artifact bytes",
    forbidden="a stale, skipped, exit-code-only or identity-mismatched receipt",
)


def _finding(source: Path, pointer: str, code: str, message: str, fix: str) -> ContractFinding:
    return ContractFinding(source=source, pointer=pointer, code=code, message=message, fix=fix)


def _expected_identity_findings(
    expected_identity: Mapping[str, object],
    *,
    source: Path,
) -> list[ContractFinding]:
    findings: list[ContractFinding] = []
    for field in (*_BASE_IDENTITY_FIELDS, *_STRING_RECEIPT_IDENTITIES):
        value = expected_identity.get(field)
        if not isinstance(value, str) or not value.strip():
            findings.append(
                _finding(
                    source,
                    f"/expected_identity/{field}",
                    "missing-expected-identity",
                    f"independent expected {field} is required",
                    f"supply expected {field} outside the evidence document",
                )
            )
    for field in _INTEGER_RECEIPT_IDENTITIES:
        value = expected_identity.get(field)
        if not is_integer_identity(value):
            findings.append(
                _finding(
                    source,
                    f"/expected_identity/{field}",
                    "invalid-expected-identity",
                    f"independent expected {field} must be a non-negative integer, not a boolean",
                    f"supply expected {field} outside the evidence document as an integer",
                )
            )
    source_sha = expected_identity.get("source_sha")
    if isinstance(source_sha, str) and source_sha and _SOURCE_SHA_RE.fullmatch(source_sha) is None:
        findings.append(
            _finding(
                source,
                "/expected_identity/source_sha",
                "invalid-source-sha",
                "expected source SHA must be 40 or 64 lowercase hexadecimal characters",
                "supply the full lowercase source commit SHA",
            )
        )
    image_digest = expected_identity.get("image_digest")
    if isinstance(image_digest, str) and image_digest and _SHA256_RE.fullmatch(image_digest) is None:
        findings.append(
            _finding(
                source,
                "/expected_identity/image_digest",
                "invalid-image-digest",
                "expected image digest must use sha256 followed by 64 lowercase hexadecimal characters",
                "supply the immutable sha256 image or artifact digest",
            )
        )
    return findings


def _identity_findings(
    evidence: Mapping[str, object],
    *,
    expected_identity: Mapping[str, object],
    source: Path,
) -> list[ContractFinding]:
    findings: list[ContractFinding] = []
    for field in _IDENTITY_FIELDS:
        expected = expected_identity.get(field)
        actual = evidence.get(field)
        expected_is_valid = (
            isinstance(expected, str) and bool(expected.strip())
            if field not in _INTEGER_RECEIPT_IDENTITIES
            else is_integer_identity(expected)
        )
        if expected_is_valid and actual != expected:
            findings.append(
                _finding(
                    source,
                    f"/{field}",
                    f"{field.replace('_', '-')}-mismatch",
                    f"evidence {field} does not match the independently expected value",
                    f"collect evidence from the expected {field}",
                )
            )
    return findings


def _normalise_required_checks(
    value: object,
    *,
    source: Path,
) -> tuple[tuple[str, ...], tuple[ContractFinding, ...]]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return (), (
            _finding(
                source,
                "/required_checks",
                "invalid-required-checks",
                "required_checks must be a list of unique non-empty strings",
                "configure required_checks as an array of check ids",
            ),
        )
    valid: list[str] = []
    findings: list[ContractFinding] = []
    seen: set[str] = set()
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            findings.append(
                _finding(
                    source,
                    f"/required_checks/{index}",
                    "invalid-required-checks",
                    "each required check id must be a non-empty string",
                    "replace the member with one declared non-empty check id",
                )
            )
            continue
        if item in seen:
            findings.append(
                _finding(
                    source,
                    f"/required_checks/{index}",
                    "invalid-required-checks",
                    f"required check {item!r} is listed more than once",
                    "keep each required check id exactly once",
                )
            )
            continue
        seen.add(item)
        valid.append(item)
    return tuple(valid), sort_findings(findings)


def _receipt_identity_findings(
    evidence: Mapping[str, object],
    *,
    source: Path,
) -> list[ContractFinding]:
    findings: list[ContractFinding] = []
    for field in _IDENTITY_FIELDS:
        if field not in evidence:
            findings.append(
                _finding(
                    source,
                    f"/{field}",
                    "missing-receipt-identity",
                    f"receipt identity {field} is required",
                    f"record the observed {field} for this deployment attempt",
                )
            )
    for field in (*_BASE_IDENTITY_FIELDS, *_STRING_RECEIPT_IDENTITIES):
        value = evidence.get(field)
        if field in evidence and (not isinstance(value, str) or not value.strip()):
            findings.append(
                _finding(
                    source,
                    f"/{field}",
                    "invalid-receipt-identity",
                    f"receipt identity {field} must be a non-empty string",
                    f"record a non-empty observed {field}",
                )
            )
    for field in _INTEGER_RECEIPT_IDENTITIES:
        value = evidence.get(field)
        if field in evidence and not is_integer_identity(value):
            findings.append(
                _finding(
                    source,
                    f"/{field}",
                    "invalid-receipt-identity",
                    f"receipt identity {field} must be a non-negative integer, not a boolean",
                    f"record {field} as a JSON integer",
                )
            )
    source_sha = evidence.get("source_sha")
    if isinstance(source_sha, str) and source_sha and _SOURCE_SHA_RE.fullmatch(source_sha) is None:
        findings.append(
            _finding(
                source,
                "/source_sha",
                "invalid-receipt-identity",
                "receipt source_sha must be 40 or 64 lowercase hexadecimal characters",
                "record the full lowercase source commit SHA",
            )
        )
    image_digest = evidence.get("image_digest")
    if isinstance(image_digest, str) and image_digest and not is_sha256_digest(image_digest):
        findings.append(
            _finding(
                source,
                "/image_digest",
                "invalid-receipt-identity",
                "receipt image_digest must use canonical sha256 notation",
                "record sha256 followed by 64 lowercase hexadecimal characters",
            )
        )
    return findings


def _freshness_findings(
    evidence: Mapping[str, object],
    *,
    source: Path,
    now: datetime,
    max_age_seconds: int,
) -> list[ContractFinding]:
    captured = evidence.get("captured_at")
    if not isinstance(captured, str):
        return [
            _finding(
                source,
                "/captured_at",
                "missing-capture-time",
                "evidence requires a timezone-aware capture timestamp",
                "record captured_at as an ISO 8601 timestamp with a timezone",
            )
        ]
    try:
        captured_at = datetime.fromisoformat(captured.replace("Z", "+00:00"))
    except ValueError:
        captured_at = None
    if captured_at is None or captured_at.tzinfo is None or captured_at.utcoffset() is None:
        return [
            _finding(
                source,
                "/captured_at",
                "invalid-capture-time",
                "captured_at must be a valid timezone-aware ISO 8601 timestamp",
                "record captured_at with an explicit UTC offset",
            )
        ]
    if now.tzinfo is None or now.utcoffset() is None:
        return [
            _finding(
                source,
                "/captured_at",
                "invalid-verification-time",
                "verification time must be timezone-aware",
                "verify using a timezone-aware current time",
            )
        ]
    age_seconds = (now.astimezone(UTC) - captured_at.astimezone(UTC)).total_seconds()
    if age_seconds < 0:
        return [
            _finding(
                source,
                "/captured_at",
                "future-evidence",
                "evidence capture time is later than the verifier clock",
                "synchronise clocks and collect a new receipt",
            )
        ]
    if age_seconds > max_age_seconds:
        return [
            _finding(
                source,
                "/captured_at",
                "stale-evidence",
                f"evidence age exceeds the {max_age_seconds}-second freshness window",
                "collect a fresh receipt for this deployment attempt",
            )
        ]
    return []


def _check_findings(
    evidence: Mapping[str, object],
    *,
    required_checks: tuple[str, ...],
    source: Path,
) -> list[ContractFinding]:
    checks = evidence.get("checks")
    if not isinstance(checks, list):
        return [
            _finding(
                source,
                "/checks",
                "missing-checks",
                "evidence checks must be a list",
                "record every required check observation",
            )
        ]
    findings: list[ContractFinding] = []
    by_id: dict[str, tuple[int, Mapping[str, object]]] = {}
    for index, value in enumerate(checks):
        if not isinstance(value, Mapping):
            findings.append(
                _finding(
                    source,
                    f"/checks/{index}",
                    "invalid-check",
                    "check evidence must be an object",
                    "record a structured check result",
                )
            )
            continue
        check = cast(Mapping[str, object], value)
        check_id = check.get("id")
        if not isinstance(check_id, str) or not check_id:
            findings.append(
                _finding(
                    source,
                    f"/checks/{index}/id",
                    "missing-check-id",
                    "check evidence requires a non-empty id",
                    "set the declared check id",
                )
            )
            continue
        if check_id in by_id:
            findings.append(
                _finding(
                    source,
                    f"/checks/{index}/id",
                    "duplicate-check",
                    f"check {check_id!r} appears more than once",
                    "record exactly one result per check id",
                )
            )
        else:
            by_id[check_id] = (index, check)
        status = check.get("status")
        if not isinstance(status, str) or status not in _CHECK_STATUSES:
            findings.append(
                _finding(
                    source,
                    f"/checks/{index}/status",
                    "invalid-check-verdict",
                    f"check {check_id!r} has an unsupported status",
                    "record passed, failed, skipped or expected-denial",
                )
            )
        elif status == "failed":
            findings.append(
                _finding(
                    source,
                    f"/checks/{index}/status",
                    "failed-check-verdict",
                    f"emitted check {check_id!r} records a failure",
                    "correct the runtime defect and collect new passing evidence",
                )
            )
        elif status == "skipped":
            findings.append(
                _finding(
                    source,
                    f"/checks/{index}/status",
                    "check-skipped",
                    f"check {check_id!r} was skipped",
                    "execute the check and record an observed result",
                )
            )
        observation = check.get("observation")
        if not isinstance(observation, Mapping) or not observation or set(observation) <= {"exit_code"}:
            findings.append(
                _finding(
                    source,
                    f"/checks/{index}/observation",
                    "incomplete-observation",
                    f"check {check_id!r} has no substantive observation beyond an exit code",
                    "record the observed runtime state that proves the check outcome",
                )
            )
            continue
        observation = cast(Mapping[str, object], observation)
        top_exit_code = check.get("exit_code")
        observed_exit_code = observation.get("exit_code")
        if top_exit_code is not None and not is_integer_identity(top_exit_code):
            findings.append(
                _finding(
                    source,
                    f"/checks/{index}/exit_code",
                    "contradictory-check-verdict",
                    f"check {check_id!r} exit_code must be a non-negative integer, not a boolean",
                    "record the actual integer process exit code",
                )
            )
        if observed_exit_code is not None and not is_integer_identity(observed_exit_code):
            findings.append(
                _finding(
                    source,
                    f"/checks/{index}/observation/exit_code",
                    "contradictory-check-verdict",
                    f"check {check_id!r} observation exit_code is not a valid integer",
                    "record the actual integer process exit code",
                )
            )
        if (
            top_exit_code is not None
            and observed_exit_code is not None
            and top_exit_code != observed_exit_code
        ):
            findings.append(
                _finding(
                    source,
                    f"/checks/{index}/observation/exit_code",
                    "contradictory-check-verdict",
                    f"check {check_id!r} records conflicting exit codes",
                    "record one consistent process exit code",
                )
            )
        effective_exit_code = top_exit_code if top_exit_code is not None else observed_exit_code
        if status == "passed":
            if is_integer_identity(effective_exit_code) and effective_exit_code != 0:
                findings.append(
                    _finding(
                        source,
                        f"/checks/{index}/exit_code",
                        "contradictory-check-verdict",
                        f"check {check_id!r} is marked passed but has a non-zero exit code",
                        "mark the check failed or collect a zero-exit passing observation",
                    )
                )
            for field in ("state", "status", "result", "outcome", "verdict"):
                value = observation.get(field)
                if isinstance(value, str) and value.casefold() in _FAILURE_OBSERVATIONS:
                    findings.append(
                        _finding(
                            source,
                            f"/checks/{index}/observation/{field}",
                            "contradictory-check-verdict",
                            f"check {check_id!r} is marked passed but its {field} records {value!r}",
                            "mark the check failed or record the actual successful observation",
                        )
                    )
            for field in ("success", "passed", "healthy", "allowed"):
                if observation.get(field) is False:
                    findings.append(
                        _finding(
                            source,
                            f"/checks/{index}/observation/{field}",
                            "contradictory-check-verdict",
                            f"check {check_id!r} is marked passed but {field} is false",
                            "mark the check failed or record the actual successful observation",
                        )
                    )
        elif status == "expected-denial":
            if observation.get("outcome") != "denied":
                findings.append(
                    _finding(
                        source,
                        f"/checks/{index}/observation/outcome",
                        "contradictory-check-verdict",
                        f"check {check_id!r} uses expected-denial without observing a denied outcome",
                        "record outcome as denied or use the status matching the observed result",
                    )
                )
            if is_integer_identity(effective_exit_code) and effective_exit_code == 0:
                findings.append(
                    _finding(
                        source,
                        f"/checks/{index}/exit_code",
                        "contradictory-check-verdict",
                        f"check {check_id!r} expected denial but its process exited successfully",
                        "record the non-zero denial exit code or correct the observation status",
                    )
                )

    for check_id in required_checks:
        located = by_id.get(check_id)
        if located is None:
            findings.append(
                _finding(
                    source,
                    "/checks",
                    "missing-required-check",
                    f"required check {check_id!r} is absent",
                    "collect and record the required check",
                )
            )
            continue
        index, check = located
        status = check.get("status")
        if not isinstance(status, str) or status not in {"passed", "expected-denial", "skipped"}:
            findings.append(
                _finding(
                    source,
                    f"/checks/{index}/status",
                    "required-check-failed",
                    f"required check {check_id!r} did not pass",
                    "correct the runtime defect and collect new passing evidence",
                )
            )
    return findings


def _safe_artifact_path(base: Path, value: object) -> Path | None:
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        return None
    relative = PurePosixPath(value)
    if relative.is_absolute() or ".." in relative.parts:
        return None
    root = base.resolve()
    try:
        path = (root / Path(*relative.parts)).resolve()
    except (OSError, RuntimeError, ValueError):
        return None
    try:
        path.relative_to(root)
    except ValueError:
        return None
    return path


def _artifact_findings(evidence: Mapping[str, object], *, source: Path) -> list[ContractFinding]:
    artifacts = evidence.get("artifacts")
    if not isinstance(artifacts, list):
        return [
            _finding(
                source,
                "/artifacts",
                "missing-artifacts",
                "evidence artifacts must be a list",
                "record an empty list or each referenced artifact and digest",
            )
        ]
    findings: list[ContractFinding] = []
    seen: set[str] = set()
    for index, value in enumerate(artifacts):
        if not isinstance(value, Mapping):
            findings.append(
                _finding(
                    source,
                    f"/artifacts/{index}",
                    "invalid-artifact",
                    "artifact reference must be an object",
                    "record path and sha256 fields",
                )
            )
            continue
        artifact = cast(Mapping[str, object], value)
        reference = artifact.get("path")
        path = _safe_artifact_path(source.parent, reference)
        if path is None:
            findings.append(
                _finding(
                    source,
                    f"/artifacts/{index}/path",
                    "unsafe-artifact-path",
                    "artifact path must remain beneath the evidence directory",
                    "use a relative POSIX path without '..', backslashes or symlink escape",
                )
            )
            continue
        reference_text = cast(str, reference)
        if reference_text in seen:
            findings.append(
                _finding(
                    source,
                    f"/artifacts/{index}/path",
                    "duplicate-artifact",
                    f"artifact {reference_text!r} is referenced more than once",
                    "record one authoritative digest per artifact",
                )
            )
            continue
        seen.add(reference_text)
        digest = artifact.get("sha256")
        if not isinstance(digest, str) or _SHA256_RE.fullmatch(digest) is None:
            findings.append(
                _finding(
                    source,
                    f"/artifacts/{index}/sha256",
                    "invalid-artifact-digest",
                    "artifact digest must be sha256 followed by 64 lowercase hexadecimal characters",
                    "record the exact sha256 digest of the artifact bytes",
                )
            )
            continue
        try:
            hasher = hashlib.sha256()
            with path.open("rb") as artifact_file:
                for chunk in iter(lambda: artifact_file.read(1024 * 1024), b""):
                    hasher.update(chunk)
            actual = "sha256:" + hasher.hexdigest()
        except OSError:
            findings.append(
                _finding(
                    source,
                    f"/artifacts/{index}/path",
                    "missing-artifact",
                    f"referenced artifact {reference_text!r} cannot be read",
                    "retain the referenced artifact beside the evidence receipt",
                )
            )
            continue
        if actual != digest:
            findings.append(
                _finding(
                    source,
                    f"/artifacts/{index}/sha256",
                    "artifact-digest-mismatch",
                    f"referenced artifact {reference_text!r} does not match its digest",
                    "restore the exact retained artifact bytes or collect a new receipt",
                )
            )
    return findings


def validate_runtime_evidence(
    documents: ContractDocuments,
    *,
    expected_identity: Mapping[str, object],
    required_checks: tuple[str, ...],
    now: datetime,
    max_age_seconds: int,
) -> tuple[ContractFinding, ...]:
    """Validate a receipt against canonical contract bytes and independent identity."""
    source = documents.evidence_path or documents.contract_path
    evidence = documents.evidence
    if evidence is None or documents.evidence_path is None:
        return (
            _finding(
                source,
                "/",
                "missing-evidence",
                "runtime evidence document is required",
                "configure and retain a runtime evidence receipt",
            ),
        )
    validated_required_checks, required_check_findings = _normalise_required_checks(
        required_checks,
        source=source,
    )
    findings = list(required_check_findings)
    findings.extend(_expected_identity_findings(expected_identity, source=source))
    findings.extend(_receipt_identity_findings(evidence, source=source))
    if isinstance(max_age_seconds, bool) or not isinstance(max_age_seconds, int) or max_age_seconds < 0:
        findings.append(
            _finding(
                source,
                "/max_age_seconds",
                "invalid-max-age",
                "max_age_seconds must be a non-negative integer",
                "configure a bounded non-negative freshness window",
            )
        )
    else:
        findings.extend(
            _freshness_findings(evidence, source=source, now=now, max_age_seconds=max_age_seconds)
        )

    expected_contract_digest = (
        "sha256:" + hashlib.sha256(canonical_json_bytes(documents.contract)).hexdigest()
    )
    actual_contract_digest = evidence.get("contract_digest")
    if not isinstance(actual_contract_digest, str) or _SHA256_RE.fullmatch(actual_contract_digest) is None:
        findings.append(
            _finding(
                source,
                "/contract_digest",
                "invalid-contract-digest",
                "contract digest must be sha256 followed by 64 lowercase hexadecimal characters",
                "hash the selected canonical contract bytes with SHA-256",
            )
        )
    elif actual_contract_digest != expected_contract_digest:
        findings.append(
            _finding(
                source,
                "/contract_digest",
                "contract-digest-mismatch",
                "evidence is bound to different contract bytes",
                "collect evidence using the exact selected canonical contract",
            )
        )

    findings.extend(_identity_findings(evidence, expected_identity=expected_identity, source=source))
    findings.extend(_check_findings(evidence, required_checks=validated_required_checks, source=source))
    findings.extend(_artifact_findings(evidence, source=source))
    return sort_findings(findings)


class RuntimeEvidenceContract(RuntimeContractRule):
    """Hard-adoption CORE rule for fresh, digest-bound runtime receipts."""

    name = "runtime-evidence-contract"
    remediation = REMEDIATION
    requires_evidence = True

    def __init__(self, config: Mapping[str, object], *, repo_root: Path | None = None) -> None:
        super().__init__(config, repo_root=repo_root)
        nested_identity = config.get("expected_identity")
        if isinstance(nested_identity, Mapping):
            self.expected_identity = dict(cast(Mapping[str, object], nested_identity))
        else:
            self.expected_identity = {field: config.get(f"expected_{field}") for field in _IDENTITY_FIELDS}
        self.required_checks, self._required_check_findings = _normalise_required_checks(
            config.get("required_checks", ()),
            source=self._repo_root / "pyproject.toml",
        )
        raw_max_age = config.get("max_age_seconds", 300)
        self.max_age_seconds = cast(int, raw_max_age)

    def validate_configuration(self) -> tuple[ContractFinding, ...]:
        return self._required_check_findings

    def validate_documents(self, documents: ContractDocuments) -> tuple[ContractFinding, ...]:
        return validate_runtime_evidence(
            documents,
            expected_identity=self.expected_identity,
            required_checks=self.required_checks,
            now=datetime.now(UTC),
            max_age_seconds=self.max_age_seconds,
        )

    def run(self) -> int:
        """Emit each validated receipt defect into the structured check ledger."""
        for finding in self.collect_findings():
            report_finding(
                finding.code,
                str(finding.source.relative_to(self._repo_root)),
                finding.message,
            )
        return super().run()


def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> RuntimeEvidenceContract:
    """Bind this CORE check to one consumer configuration block."""
    return RuntimeEvidenceContract(cast(Mapping[str, object], config), repo_root=repo_root)


def main(argv: list[str] | None = None) -> int:
    """CLI entry compatible with the shared CORE-check runner."""
    return run_core_check(RuntimeEvidenceContract, argv)


if __name__ == "__main__":
    import sys

    sys.exit(main())


__all__ = ["RuntimeEvidenceContract", "build", "main", "validate_runtime_evidence"]
