"""Fresh exact-base/candidate self-coverage assurance; no accepted evidence input."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import tempfile
import uuid
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from tc_fitness.check_evidence import capture_check_evidence
from tc_fitness.core_checks._coverage_evidence import CoverageCounts
from tc_fitness.core_checks.coverage_floor import build as coverage_floor
from tc_fitness.coverage_admission import (
    bytes_digest,
    changed_line_failures,
    exact_checkout,
    git,
    produce_coverage,
)
from tc_fitness.runner import run_bounded_process

_ROOTS = ("src/tc_fitness",)
_CRITICAL = tuple(
    "src/tc_fitness/" + name + ".py" for name in ("gate", "runner", "gate_config", "runtime_contract")
)
_PYTEST_CONFIG = """[pytest]
addopts = --strict-markers -p no:cacheprovider
markers =
    unit: in-process behaviour
    contract: public input/output contract
    integration: real local collaborators
    e2e: supported installed entrypoint
"""


@dataclass(frozen=True)
class Toolchain:
    python: str
    python_executable: str
    coverage: str
    pytest: str
    uv: str
    lock_digest: str


@dataclass(frozen=True)
class Measurement:
    """Source identity and fresh counts are immutable within the transaction."""

    commit: str
    source_digest: str
    config_digest: str
    counts: CoverageCounts
    files: tuple[tuple[str, CoverageCounts], ...]
    toolchain: Toolchain


@dataclass(frozen=True)
class CoverageTransaction:
    execution_id: str
    base: Measurement
    candidate: Measurement
    failures: tuple[str, ...]

    def as_payload(self) -> dict[str, Any]:
        """Export is output-only; admission never reads a serialised transaction."""
        return {
            "schema": "tc.fitness/coverage-transaction/v1",
            "status": "fail" if self.failures else "pass",
            **asdict(self),
        }


def _measurement(payload: dict[str, Any], uv_version: str, lock_digest: str) -> Measurement:
    execution = payload["execution"]
    return Measurement(
        commit=payload["candidate_commit"],
        source_digest=payload["source_digest"],
        config_digest=payload["config_digest"],
        counts=CoverageCounts(**payload["counts"]),
        files=tuple((name, CoverageCounts(**counts)) for name, counts in sorted(payload["files"].items())),
        toolchain=Toolchain(
            python=execution["python_version"],
            python_executable=execution["python_executable"],
            coverage=execution["coverage_version"],
            pytest=execution["pytest_version"],
            uv=uv_version,
            lock_digest=lock_digest,
        ),
    )


def _fresh_measurement(snapshot: Path, commit: str, scratch: Path, execution: str) -> Measurement:
    settings = scratch / "pytest.ini"
    settings.write_text(_PYTEST_CONFIG)
    uv = shutil.which("uv")
    if uv is None:
        raise ValueError("locked coverage environments require the trusted uv executable")
    uv = str(Path(uv).resolve())
    identity = run_bounded_process([uv, "--version"], cwd=snapshot, timeout=30)
    if identity.returncode:
        raise ValueError("trusted uv identity is unavailable")
    version = identity.stdout.decode().strip()
    lock = bytes_digest((snapshot / "uv.lock").read_bytes())
    venv = scratch / "venv"
    environment = {
        key: value
        for key, value in os.environ.items()
        if not key.startswith(("PYTEST_", "COVERAGE_", "COV_CORE_"))
        and key not in {"PYTHONPATH", "VIRTUAL_ENV"}
    }
    environment.update(
        PYTHONDONTWRITEBYTECODE="1",
        PYTEST_DISABLE_PLUGIN_AUTOLOAD="1",
        UV_PROJECT_ENVIRONMENT=str(venv),
    )
    provisioned = run_bounded_process(
        [uv, "sync", "--locked", "--all-extras"],
        cwd=snapshot,
        env=environment,
        timeout=600,
        stdout_path=scratch / "uv.stdout.log",
        stderr_path=scratch / "uv.stderr.log",
    )
    if provisioned.returncode:
        raise ValueError("exact-worktree locked environment provisioning failed")
    if bytes_digest((snapshot / "uv.lock").read_bytes()) != lock:
        raise ValueError("locked environment provisioning changed the bound lockfile")
    payload = produce_coverage(
        root=snapshot,
        base=commit,
        candidate=commit,
        roots=list(_ROOTS),
        config="pyproject.toml",
        run_id=execution,
        attempt_id="1",
        output=scratch / "measurement",
        command=["-m", "pytest", "-q", "-c", str(settings), "--rootdir", str(snapshot), "tests"],
        environment=environment,
        python_executable=venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python"),
    )
    return _measurement(payload, version, lock)


def _candidate_failures(snapshot: Path, report: Path, base: str, candidate: str) -> list[str]:
    with capture_check_evidence() as evidence:
        coverage_floor(
            {
                "roots": list(_ROOTS),
                "floor_pct": 95,
                "branch_floor_pct": 95,
                "critical_branch_files": list(_CRITICAL),
                "coverage_report": str(report),
            },
            repo_root=snapshot,
        ).run()
    failures = [finding.path + ": " + finding.message for finding in evidence.findings]
    changed = changed_line_failures(
        snapshot,
        {
            "roots": list(_ROOTS),
            "floor_pct": 100,
            "exact_base_commit": base,
            "candidate_commit": candidate,
            "coverage_report": str(report),
        },
    )
    failures.extend(name + ": " + message for name, message in changed.items())
    return failures


def assure_coverage(root: Path, *, base: str, candidate: str) -> CoverageTransaction:
    """Measure both immutable commits now under the engine-owned self profile.

    Only the trusted invocation supplies identities. This engine never resolves
    moving refs, reads candidate selectors or imports an accepted measurement.
    """
    if any(re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", value) is None for value in (base, candidate)):
        raise ValueError("coverage transaction requires explicit full immutable commit IDs")
    root = root.resolve()
    exact_checkout(root, base, candidate)
    execution = str(uuid.uuid4())
    with tempfile.TemporaryDirectory(prefix="tc-fitness-coverage-transaction-") as directory:
        scratch = Path(directory)
        snapshots: list[Path] = []
        measurements = []
        try:
            for label, commit in (("base", base), ("candidate", candidate)):
                snapshot = scratch / label
                git(root, "worktree", "add", "--detach", str(snapshot), commit)
                snapshots.append(snapshot)
                output = scratch / (label + "-evidence")
                output.mkdir()
                measurements.append(_fresh_measurement(snapshot, commit, output, execution))
            before, after = measurements
            failures = _candidate_failures(
                snapshots[1], scratch / "candidate-evidence/measurement/coverage.xml", base, candidate
            )
            for kind in ("lines", "branches"):
                prior_total, current_total = getattr(before.counts, kind), getattr(after.counts, kind)
                prior_hit = getattr(before.counts, "covered_" + kind) if prior_total else 1
                current_hit = getattr(after.counts, "covered_" + kind) if current_total else 1
                if current_hit * (prior_total or 1) < prior_hit * (current_total or 1):
                    label = "line" if kind == "lines" else "branch"
                    failures.append(label + " coverage decreased from fresh exact base")
            exact_checkout(root, base, candidate)
            return CoverageTransaction(execution, before, after, tuple(sorted(failures)))
        finally:
            for snapshot in reversed(snapshots):
                # These are solely this transaction's detached temporary worktrees.
                git(root, "worktree", "remove", "--force", str(snapshot))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--base-commit", required=True)
    parser.add_argument("--candidate-commit", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    output = args.output
    try:
        if args.output is not None and (
            args.output.exists() or args.output.resolve().is_relative_to(args.repo_root.resolve())
        ):
            output = None
            raise ValueError("transaction output must be a new path outside the checkout")
        result = assure_coverage(args.repo_root, base=args.base_commit, candidate=args.candidate_commit)
        payload = result.as_payload()
        code = int(bool(result.failures))
        if output is not None:
            with output.open("x") as stream:
                stream.write(json.dumps(payload, sort_keys=True) + "\n")
            return code
    except (ValueError, OSError) as exc:
        payload = {"schema": "tc.fitness/coverage-transaction/v1", "status": "error", "error": str(exc)}
        code = 2
        if output is not None and not output.exists():
            try:
                with output.open("x") as stream:
                    stream.write(json.dumps(payload, sort_keys=True) + "\n")
                return code
            except OSError:
                pass
    print(json.dumps(payload, sort_keys=True))
    return code
