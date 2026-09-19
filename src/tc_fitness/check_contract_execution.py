"""Execute a contract case through the public gate's existing CORE dispatcher."""

from __future__ import annotations

import hashlib
import json
import shutil
from dataclasses import asdict
from datetime import UTC, datetime
from importlib.metadata import version
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any
from uuid import UUID, uuid4

from tc_fitness.catalogue import RuleEntry
from tc_fitness.check_contracts import CheckContractError, FindingExpectation, load_check_contract
from tc_fitness.check_evidence import capture_check_evidence, report_finding, report_result
from tc_fitness.core_checks import CORE_CHECKS
from tc_fitness.runner import run
from tc_fitness.runner import run_contract_case as run_contract_case

LEDGER_SCHEMA = "tc.fitness/check-ledger/v1"


def payload_digest(value: object) -> str:
    """SHA-256 of canonical UTF-8 JSON; the digest field is excluded by callers."""
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    return "sha256:" + hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def tree_digest(root: Path, *, ignore_caches: bool = False) -> str:
    """Bind names, bytes, file permissions and empty directory presence."""
    files = {
        path.relative_to(root).as_posix(): {
            "content": hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None,
            "mode": path.stat().st_mode & 0o777,
        }
        for path in sorted(root.rglob("*"))
        if not (ignore_caches and "__pycache__" in path.relative_to(root).parts)
    }
    return payload_digest(files)


def candidate_identity() -> dict[str, str]:
    """Identity of the executing package, including uncommitted source changes."""
    return {
        "package_version": version("three-cubes-fitness"),
        "source_digest": tree_digest(Path(__file__).parent, ignore_caches=True),
    }


def execute_contract_case(manifest: Path, case_id: str, ledger: Path) -> int:
    """Run one case and retain its terminal evidence; return its actual exit."""
    contract = load_check_contract(manifest)
    if contract.check not in CORE_CHECKS:
        raise CheckContractError(f"unregistered CORE check: {contract.check}")
    case = next((case for case in contract.cases if case.id == case_id), None)
    if case is None:
        raise CheckContractError(f"unknown contract case: {case_id}")
    fixture = _fixture_path(manifest, case.fixture)
    if ledger.resolve().is_relative_to(fixture.resolve()):
        raise CheckContractError("ledger must be outside the input fixture")
    if ledger.exists():
        raise CheckContractError("ledger already exists; retain it and select a new output for the retry")
    fixture_digest = tree_digest(fixture)
    started = datetime.now(UTC).isoformat()
    with TemporaryDirectory(prefix="tc-fitness-contract-") as temporary:
        repo = Path(temporary) / "repo"
        shutil.copytree(fixture, repo)
        with capture_check_evidence() as evidence:
            missing = [dependency for dependency in contract.dependencies if shutil.which(dependency) is None]
            if missing:
                for dependency in missing:
                    report_finding(
                        "dependency-unavailable",
                        ".",
                        f"required executable unavailable: {dependency}",
                        status="error",
                    )
                report_result(contract.check, 2)
            else:
                entry = RuleEntry(id=contract.check, gate=contract.check, check=contract.check)
                run(
                    (entry,),
                    repo_root=repo,
                    core_check_configs={contract.check.removeprefix("core:"): contract.config},
                )
        if len(evidence.results) != 1:
            raise CheckContractError("missing or multiple terminal check results")
        result = evidence.results[0]
        exit_code = 2 if result.status == "error" else result.exit_code
        payload: dict[str, Any] = {
            "schema": LEDGER_SCHEMA,
            "check": contract.check,
            "case_id": case.id,
            "contract_digest": "sha256:" + hashlib.sha256(manifest.read_bytes()).hexdigest(),
            "case_digest": payload_digest(asdict(case)),
            "fixture_digest": fixture_digest,
            "candidate": candidate_identity(),
            "execution_id": str(uuid4()),
            "started_at": started,
            "finished_at": datetime.now(UTC).isoformat(),
            "expected": asdict(case.expected),
            "actual": {
                "status": result.status,
                "exit_code": exit_code,
                "exit": "zero" if exit_code == 0 else "nonzero",
                "findings": [asdict(finding) for finding in evidence.findings],
            },
        }
        payload["payload_digest"] = payload_digest(payload)
        with ledger.open("x", encoding="utf-8") as output:
            output.write(json.dumps(payload, sort_keys=True, indent=2) + "\n")
        return exit_code


def _fixture_path(manifest: Path, name: str) -> Path:
    relative = Path(name)
    fixture = manifest.parent / relative
    if relative.is_absolute() or ".." in relative.parts or not fixture.is_dir():
        raise CheckContractError("fixture must be an existing directory beneath the manifest")
    ancestors = [
        manifest.parent.joinpath(*relative.parts[:index]) for index in range(1, len(relative.parts) + 1)
    ]
    if any(path.is_symlink() for path in ancestors) or any(path.is_symlink() for path in fixture.rglob("*")):
        raise CheckContractError("contract fixtures cannot contain symlinks")
    if (fixture / ".architecture" / "baseline").exists():
        raise CheckContractError("contract fixtures cannot contain a suppression baseline")
    return fixture


def _match_findings(expected: tuple[FindingExpectation, ...], actual: list[dict[str, Any]]) -> bool:
    """Require a one-to-one match, including every unexpected finding."""
    if len(expected) != len(actual):
        return False
    if not expected:
        return True
    finding = expected[0]
    for index, observed in enumerate(actual):
        if (
            observed["rule"] == finding.rule
            and observed["path"] == finding.path
            and finding.message_contains in observed["message"]
            and _match_findings(expected[1:], actual[:index] + actual[index + 1 :])
        ):
            return True
    return False


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise CheckContractError(f"duplicate ledger key: {key}")
        value[key] = item
    return value


def validate_contract_ledger(
    manifest: Path,
    case_id: str,
    ledger: Path,
    *,
    process_exit: int,
    started_after: datetime,
) -> dict[str, Any]:
    """Admit only fresh, complete evidence bound to this candidate and input.

    ``process_exit`` and ``started_after`` come from the caller's invocation,
    never from the ledger being validated. A digest protects integrity, not
    authenticity; release signing remains the admission layer's responsibility.
    """
    contract = load_check_contract(manifest)
    case = next((case for case in contract.cases if case.id == case_id), None)
    if case is None:
        raise CheckContractError(f"unknown contract case: {case_id}")
    try:
        value: dict[str, Any] = json.loads(
            ledger.read_text(encoding="utf-8"), object_pairs_hook=_unique_object
        )
        digest = value.pop("payload_digest")
        if digest != payload_digest(value):
            raise CheckContractError("ledger payload digest mismatch")
        bindings = {
            "schema": LEDGER_SCHEMA,
            "check": contract.check,
            "case_id": case.id,
            "case_digest": payload_digest(asdict(case)),
            "contract_digest": "sha256:" + hashlib.sha256(manifest.read_bytes()).hexdigest(),
            "fixture_digest": tree_digest(_fixture_path(manifest, case.fixture)),
            "candidate": candidate_identity(),
            "expected": json.loads(json.dumps(asdict(case.expected))),
        }
        for name, expected in bindings.items():
            if value[name] != expected:
                raise CheckContractError(f"ledger {name} mismatch")
        UUID(value["execution_id"])
        started = datetime.fromisoformat(value["started_at"])
        finished = datetime.fromisoformat(value["finished_at"])
        if not started_after <= started <= finished <= datetime.now(UTC):
            raise CheckContractError("ledger timestamps are stale, reversed or in the future")
        actual = value["actual"]
        exit_class = "zero" if process_exit == 0 else "nonzero"
        if (
            type(actual["exit_code"]) is not int
            or actual["exit_code"] != process_exit
            or actual["exit"] != exit_class
            or exit_class != case.expected.exit
            or actual["status"] != case.expected.status
        ):
            raise CheckContractError("ledger status or process exit does not match the case")
        findings = actual["findings"]
        if not isinstance(findings, list) or any(
            not isinstance(finding, dict)
            or not all(isinstance(finding.get(key), str) for key in ("rule", "path", "message"))
            or finding.get("status") != actual["status"]
            for finding in findings
        ):
            raise CheckContractError("invalid structured findings")
        if not _match_findings(case.expected.findings, findings):
            raise CheckContractError("ledger findings do not match the case")
        value["payload_digest"] = digest
        return value
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        if isinstance(exc, CheckContractError):
            raise
        raise CheckContractError(f"invalid or missing ledger: {exc}") from exc
