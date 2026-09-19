"""Execute a contract case through the public gate's existing CORE dispatcher."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import asdict
from datetime import UTC, datetime
from importlib.metadata import version
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any
from uuid import UUID, uuid4

from tc_fitness.baseline import baseline_free_execution
from tc_fitness.catalogue import RuleEntry
from tc_fitness.check_contract_policy import validate_contract_configuration
from tc_fitness.check_contracts import (
    CheckContractError,
    FindingExpectation,
    GitCaseEnvironment,
    load_check_contract,
)
from tc_fitness.check_evidence import capture_check_evidence
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
    manifest_bytes = manifest.read_bytes()
    contract = load_check_contract(manifest, source=manifest_bytes)
    _portable_configuration(contract.config)
    if contract.check not in CORE_CHECKS:
        raise CheckContractError(f"unregistered CORE check: {contract.check}")
    validate_contract_configuration(contract.check, contract.config)
    case = next((case for case in contract.cases if case.id == case_id), None)
    if case is None:
        raise CheckContractError(f"unknown contract case: {case_id}")
    fixture = _fixture_path(manifest, case.fixture)
    if ledger.resolve().is_relative_to(fixture.resolve()):
        raise CheckContractError("ledger must be outside the input fixture")
    if ledger.exists():
        raise CheckContractError("ledger already exists; retain it and select a new output for the retry")
    fixture_digest = tree_digest(fixture)
    candidate = candidate_identity()
    started = datetime.now(UTC).isoformat()
    with TemporaryDirectory(prefix="tc-fitness-contract-") as temporary:
        repo = Path(temporary) / "repo"
        shutil.copytree(fixture, repo)
        if tree_digest(repo) != fixture_digest:
            raise CheckContractError("fixture changed while copying the execution snapshot")
        _materialize_git_fixture(repo, case.environment)
        with (
            _case_environment(case.environment.path, Path(temporary)),
            capture_check_evidence() as evidence,
            baseline_free_execution(),
        ):
            entry = RuleEntry(id=contract.check, gate=contract.check, check=contract.check)
            run(
                (entry,),
                repo_root=repo,
                core_check_configs={contract.check.removeprefix("core:"): contract.config},
            )
        if manifest.read_bytes() != manifest_bytes:
            raise CheckContractError("manifest changed during execution")
        if tree_digest(_fixture_path(manifest, case.fixture)) != fixture_digest:
            raise CheckContractError("original fixture changed during execution")
        if candidate_identity() != candidate:
            raise CheckContractError("candidate source changed during execution")
        if (repo / ".architecture" / "baseline").exists():
            raise CheckContractError("execution created a suppression baseline")
        if len(evidence.results) != 1:
            raise CheckContractError("missing or multiple terminal check results")
        result = evidence.results[0]
        exit_code = 2 if result.status == "error" else result.exit_code
        payload: dict[str, Any] = {
            "schema": LEDGER_SCHEMA,
            "check": contract.check,
            "case_id": case.id,
            "contract_digest": "sha256:" + hashlib.sha256(manifest_bytes).hexdigest(),
            "case_digest": payload_digest(asdict(case)),
            "fixture_digest": fixture_digest,
            "candidate": candidate,
            "execution_id": str(uuid4()),
            "started_at": started,
            "finished_at": datetime.now(UTC).isoformat(),
            "expected": asdict(case.expected),
            "environment": asdict(case.environment),
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


def _portable_configuration(value: object) -> None:
    """Keep configured inputs inside the fixture and forbid baseline overrides."""
    if isinstance(value, dict):
        for key, item in value.items():
            if key == "name" and not re.fullmatch(r"[a-zA-Z0-9_-]+", str(item)):
                raise CheckContractError(
                    "contract configuration cannot select a baseline or external rule name"
                )
            _portable_configuration(item)
    elif isinstance(value, list):
        for item in value:
            _portable_configuration(item)
    elif isinstance(value, str) and (Path(value).is_absolute() or ".." in Path(value).parts):
        raise CheckContractError("contract configuration paths must be portable and fixture-relative")


_GIT_FIXTURE_TIMEOUT_SECONDS = 30
_GIT_FIXTURE_MAX_BYTES = 1024 * 1024


def _run_fixture_git(
    repo: Path,
    arguments: list[str],
    *,
    input_bytes: bytes | None = None,
) -> subprocess.CompletedProcess[bytes]:
    """Run one bounded, non-interactive Git fixture operation."""
    try:
        # argv0 and every subcommand are internal constants; the only manifest
        # value reaching argv is the strictly validated refs/heads checkout.
        result = subprocess.run(  # noqa: S603
            ["git", *arguments],  # noqa: S607
            cwd=repo,
            input=input_bytes,
            capture_output=True,
            check=False,
            timeout=_GIT_FIXTURE_TIMEOUT_SECONDS,
            env={
                **os.environ,
                "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_CONFIG_GLOBAL": os.devnull,
                "GIT_TERMINAL_PROMPT": "0",
                "GCM_INTERACTIVE": "Never",
            },
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        raise CheckContractError(f"cannot materialise Git contract fixture: {type(exc).__name__}") from exc
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", "replace").strip().splitlines()
        reason = detail[-1] if detail else f"git exited {result.returncode}"
        raise CheckContractError(f"cannot materialise Git contract fixture: {reason}")
    return result


def _materialize_git_fixture(
    repo: Path,
    environment: object,
) -> None:
    """Replace a bound ``.contract`` input with its deterministic Git tree."""
    if not isinstance(environment, GitCaseEnvironment):
        return
    history = repo / environment.git.history
    try:
        if not history.is_file() or history.is_symlink():
            raise CheckContractError("Git contract history must be a regular file")
        if history.stat().st_size > _GIT_FIXTURE_MAX_BYTES:
            raise CheckContractError("Git contract history exceeds the 1 MiB limit")
        stream = history.read_bytes()
    except OSError as exc:
        raise CheckContractError(f"cannot read Git contract history: {exc}") from exc
    contract_root = repo / ".contract"
    shutil.rmtree(contract_root)
    if any(repo.iterdir()):
        raise CheckContractError("Git contract fixture may contain only its .contract history input")

    _run_fixture_git(repo, ["init", "--quiet", "--object-format=sha1"])
    _run_fixture_git(repo, ["fast-import", "--quiet"], input_bytes=stream)
    _run_fixture_git(repo, ["rev-parse", "--verify", f"{environment.git.checkout}^{{commit}}"])
    _run_fixture_git(repo, ["checkout", "--quiet", "--force", "--detach", environment.git.checkout])
    modes = _run_fixture_git(repo, ["ls-files", "--stage", "-z"]).stdout.split(b"\x00")
    invalid_modes = sorted(
        entry.split(maxsplit=1)[0].decode("ascii", "replace")
        for entry in modes
        if entry and entry.split(maxsplit=1)[0] not in {b"100644", b"100755"}
    )
    if invalid_modes:
        raise CheckContractError(f"Git contract tree contains unsupported modes: {', '.join(invalid_modes)}")
    status = _run_fixture_git(repo, ["status", "--porcelain=v1", "--untracked-files=all"]).stdout
    if status:
        raise CheckContractError("materialised Git contract fixture is not clean")


@contextmanager
def _case_environment(policy: str, temporary: Path) -> Iterator[None]:
    """Hide PATH-resolved tools for an explicit unavailable case, then restore."""
    if policy == "inherit":
        yield
        return
    empty = temporary / "empty-path"
    empty.mkdir()
    original = os.environ.get("PATH")
    os.environ["PATH"] = str(empty)
    try:
        yield
    finally:
        if original is None:
            os.environ.pop("PATH", None)
        else:
            os.environ["PATH"] = original


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
    try:
        manifest_bytes = manifest.read_bytes()
    except OSError as exc:
        raise CheckContractError(f"cannot read contract snapshot: {exc}") from exc
    contract = load_check_contract(manifest, source=manifest_bytes)
    validate_contract_configuration(contract.check, contract.config)
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
            "contract_digest": "sha256:" + hashlib.sha256(manifest_bytes).hexdigest(),
            "fixture_digest": tree_digest(_fixture_path(manifest, case.fixture)),
            "candidate": candidate_identity(),
            "expected": json.loads(json.dumps(asdict(case.expected))),
            "environment": asdict(case.environment),
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
