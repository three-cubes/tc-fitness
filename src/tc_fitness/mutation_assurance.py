"""Real mutmut execution and fail-closed exact-candidate mutation admission."""

from __future__ import annotations

import argparse
import ast
import fnmatch
import json
import os
import shutil
import sys
from datetime import UTC, datetime
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any
from uuid import UUID, uuid4

from tc_fitness.check_contract_execution import candidate_identity, payload_digest
from tc_fitness.mutation_scope import (
    MutationError,
    archive_executables,
    archive_files,
    candidate_archives,
    definition_digest,
    digest_bytes,
    read_policy,
    select_scope,
)
from tc_fitness.runner import run_bounded_process

TOOL_VERSION = "3.6.0"
SCHEMA = "tc.fitness/mutation-receipt/v1"
MAX_LOG_BYTES = 2 * 1024 * 1024


def _json(path: Path) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise MutationError("duplicate JSON field in mutation evidence")
            result[key] = value
        return result

    try:
        value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique)
    except (OSError, ValueError) as exc:
        raise MutationError(f"missing or malformed mutation output: {path.name}") from exc
    if not isinstance(value, dict):
        raise MutationError("mutation output must be an object")
    return value


def _write_json(path: Path, value: object) -> None:
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, sort_keys=True, indent=2, allow_nan=False)
        stream.write("\n")


def _inputs(
    root: Path, base: str, head: str, broad: bool
) -> tuple[dict[str, Any], dict[str, bytes], dict[str, Any]]:
    before, after = candidate_archives(root, base, head)
    head_files = archive_files(after)
    policy = read_policy(head_files)
    scope = select_scope(archive_files(before), head_files, policy, broad=broad)
    binding = {
        "base": base,
        "head": head,
        "base_source_digest": digest_bytes(before),
        "source_digest": digest_bytes(after),
        "executable_paths": archive_executables(after),
        "scope": scope,
        "engine": candidate_identity(),
        "tool": {"name": "mutmut", "version": TOOL_VERSION},
    }
    return binding, head_files, policy


def _native_config(snapshot: Path, files: dict[str, bytes], policy: dict[str, Any]) -> None:
    """Create authoritative tool controls in the disposable snapshot only."""
    project = snapshot / "pyproject.toml"
    original = project.read_text() if project.exists() else ""
    if "[tool.mutmut]" in original:
        raise MutationError("mutation policy must own mutmut controls; a second configuration is forbidden")
    copy_roots = sorted(
        {path.split("/")[0] for path in files}
        - set(policy["source_roots"])
        - {"tests", "test", "pyproject.toml", "setup.cfg"}
    )
    controls = {
        "source_paths": policy["source_roots"],
        "pytest_add_cli_args_test_selection": policy["tests"],
        "also_copy": copy_roots,
        "max_stack_depth": -1,
        "mutate_only_covered_lines": False,
        "timeout_multiplier": 5,
        "timeout_constant": 1,
    }
    project.write_text(
        original
        + "\n[tool.mutmut]\n"
        + "".join(f"{key} = {json.dumps(value)}\n" for key, value in controls.items())
    )


def _native_mutants(native: Path, scope: dict[str, Any]) -> list[dict[str, Any]]:
    mutants: list[dict[str, Any]] = []
    seen: set[str] = set()
    stats = _json(native / "mutmut-stats.json")
    associations = stats.get("tests_by_mangled_function_name")
    durations = stats.get("duration_by_test")
    if (
        not isinstance(associations, dict)
        or not associations
        or not isinstance(durations, dict)
        or not durations
    ):
        raise MutationError("empty native test scope or missing test execution map")
    for function in scope["functions"]:
        metadata = _json(native / (function["path"] + ".meta"))
        statuses = metadata.get("exit_code_by_key")
        if not isinstance(statuses, dict):
            raise MutationError("native mutation result has no terminal status map")
        module = function["selector"].rsplit(".", 1)[0]
        try:
            source = ast.parse((native / function["path"]).read_bytes())
        except (OSError, SyntaxError) as exc:
            raise MutationError("missing or invalid generated mutant source") from exc
        definitions = {
            module + "." + node.name: node
            for node in ast.walk(source)
            if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
        }
        prefix = function["selector"].removesuffix("*")
        inventory = {
            name for name in definitions if name.startswith(prefix) and name[len(prefix) :].isdigit()
        }
        reported = {name for name in statuses if fnmatch.fnmatchcase(name, function["selector"])}
        if inventory != reported:
            raise MutationError("native mutant inventory is missing or has unexpected result entries")
        original = definitions.get(prefix + "orig")
        if inventory and (original is None or definition_digest(original) != function["definition_digest"]):
            raise MutationError("native mutant source does not match the exact candidate definition")
        tests = associations.get(prefix.removesuffix("__mutmut_"))
        if inventory and (
            not isinstance(tests, list)
            or not tests
            or not all(
                isinstance(test, str)
                and test in durations
                and isinstance(durations[test], int | float)
                and not isinstance(durations[test], bool)
                and durations[test] >= 0
                for test in tests
            )
        ):
            raise MutationError("selected mutant has no real native test association")
        for name, code in sorted(statuses.items()):
            if not fnmatch.fnmatchcase(name, function["selector"]):
                continue
            if name in seen:
                raise MutationError("duplicate native mutant identity")
            if definition_digest(definitions[name]) == function["definition_digest"]:
                raise MutationError("native result names an unchanged, no-op mutant")
            seen.add(name)
            if type(code) is not int:
                status = "error"
            elif code == 1:
                status = "killed"
            elif code == 0:
                status = "survived"
            else:
                status = "error"
            mutants.append(
                {
                    "id": name,
                    "function": function["name"],
                    "path": function["path"],
                    "exit_code": code,
                    "status": status,
                }
            )
    if not mutants:
        raise MutationError("empty or zero-scope native mutation evidence")
    return sorted(mutants, key=lambda item: item["id"])


def _artifacts(output: Path) -> list[dict[str, str]]:
    artifacts = []
    for path in sorted(output.rglob("*")):
        if path == output / "receipt.json" or not path.is_file():
            continue
        if path.is_symlink():
            raise MutationError("mutation artifacts must not be symlinks")
        artifacts.append(
            {"path": path.relative_to(output).as_posix(), "digest": digest_bytes(path.read_bytes())}
        )
    return artifacts


def execute_mutation(
    root: Path, base: str, head: str, output: Path, *, run_id: str, attempt: int, broad: bool = False
) -> dict[str, Any]:
    binding, files, policy = _inputs(root, base, head, broad)
    if not binding["scope"]["functions"]:
        raise MutationError(
            "no changed production function scope; no mutation receipt can be admitted", "zero-scope"
        )
    try:
        installed_version = version("mutmut")
    except PackageNotFoundError as exc:
        raise MutationError("required mutmut executable is unavailable", "dependency-unavailable") from exc
    executable = Path(sys.executable).with_name("mutmut")
    if installed_version != TOOL_VERSION or not executable.is_file():
        raise MutationError("mutation execution requires the exact pinned mutmut tool")
    if output.exists():
        raise MutationError("output already exists; retain the prior attempt and use a new directory")
    output.mkdir(parents=True)
    receipt: dict[str, Any] = {
        "schema": SCHEMA,
        **binding,
        "run_id": run_id,
        "attempt": attempt,
        "execution_id": str(uuid4()),
        "started_at": datetime.now(UTC).isoformat(),
        "status": "error",
        "mutants": [],
    }
    with TemporaryDirectory(prefix="tc-mutation-") as temporary:
        snapshot = Path(temporary)
        for path, raw in files.items():
            destination = snapshot / path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(raw)
            destination.chmod(0o755 if path in binding["executable_paths"] else 0o644)
        _native_config(snapshot, files, policy)
        (output / "native-config.toml").write_bytes((snapshot / "pyproject.toml").read_bytes())
        command = [
            str(executable),
            "run",
            "--max-children",
            "2",
            *[item["selector"] for item in binding["scope"]["functions"]],
        ]
        receipt["command"] = command
        env = dict(os.environ)
        env.pop("PYTEST_ADDOPTS", None)
        env.pop("PYTEST_PLUGINS", None)
        env.pop("MUTANT_UNDER_TEST", None)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        result = run_bounded_process(
            command,
            cwd=snapshot,
            env=env,
            timeout=policy["timeout_seconds"],
            stdout_path=output / "stdout.log",
            stderr_path=output / "stderr.log",
        )
        receipt["tool_exit_code"] = result.returncode
        native = snapshot / "mutants"
        if native.is_dir():
            shutil.copytree(native, output / "native")
        try:
            if result.returncode != 0:
                raise MutationError(f"native mutation execution did not complete: exit {result.returncode}")
            if any((output / name).stat().st_size > MAX_LOG_BYTES for name in ("stdout.log", "stderr.log")):
                raise MutationError("native mutation diagnostics exceeded the bounded output budget")
            receipt["mutants"] = _native_mutants(output / "native", binding["scope"])
            if len(receipt["mutants"]) > policy["max_mutants"]:
                raise MutationError("mutation scope exceeds the reviewed mutant budget")
            if any(item["status"] == "error" for item in receipt["mutants"]):
                raise MutationError(
                    "native mutation results include missing, untested, interrupted or errored mutants"
                )
            receipt["status"] = (
                "fail" if any(item["status"] == "survived" for item in receipt["mutants"]) else "pass"
            )
            current, _, _ = _inputs(root, base, head, broad)
            if current != binding:
                raise MutationError("candidate inputs changed during mutation execution")
        except MutationError as exc:
            receipt["status"] = "error"
            receipt["error"] = str(exc)
    receipt["finished_at"] = datetime.now(UTC).isoformat()
    receipt["artifacts"] = _artifacts(output)
    receipt["payload_digest"] = payload_digest(receipt)
    _write_json(output / "receipt.json", receipt)
    return receipt


def validate_mutation_receipt(
    root: Path, base: str, head: str, output: Path, *, run_id: str, attempt: int, broad: bool = False
) -> dict[str, Any]:
    """Admit only complete current native results; outer claims are insufficient."""
    if not (output / "receipt.json").is_file():
        raise MutationError("missing mutation receipt", "missing-receipt")
    receipt = _json(output / "receipt.json")
    recorded_digest = receipt.pop("payload_digest", None)
    if recorded_digest != payload_digest(receipt):
        raise MutationError("mutation receipt digest mismatch")
    binding, _, policy = _inputs(root, base, head, broad)
    for key, expected in {"schema": SCHEMA, **binding, "run_id": run_id, "attempt": attempt}.items():
        if receipt.get(key) != expected or type(receipt.get(key)) is not type(expected):
            raise MutationError(f"mutation receipt {key} mismatch")
    try:
        UUID(receipt["execution_id"])
        started = datetime.fromisoformat(receipt["started_at"])
        finished = datetime.fromisoformat(receipt["finished_at"])
        now = datetime.now(UTC)
        if not started <= finished <= now or (now - finished).total_seconds() > 86400:
            raise MutationError("stale or reversed mutation execution timestamps")
    except (KeyError, TypeError, ValueError) as exc:
        raise MutationError("invalid mutation execution identity or timestamps") from exc
    artifacts = _artifacts(output)
    if not artifacts or receipt.get("artifacts") != artifacts:
        raise MutationError("missing, extra or altered native mutation artifacts")
    required = {"native-config.toml", "stdout.log", "stderr.log", "native/mutmut-stats.json"}
    if not required <= {artifact["path"] for artifact in artifacts}:
        raise MutationError("missing required native mutation outputs")
    actual = _native_mutants(output / "native", binding["scope"])
    if receipt.get("mutants") != actual or len(actual) > policy["max_mutants"]:
        raise MutationError("native mutant set does not match the claimed evidence")
    if (
        receipt.get("status") != "pass"
        or receipt.get("tool_exit_code") != 0
        or any(item["status"] != "killed" for item in actual)
    ):
        raise MutationError("mutation admission requires terminal killed results for every selected mutant")
    receipt["payload_digest"] = recorded_digest
    return receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="tc-fitness mutation")
    parser.add_argument("action", choices=("plan", "check", "run", "verify"))
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--attempt", type=int, required=True)
    parser.add_argument("--broad", action="store_true")
    args = parser.parse_args(argv)
    try:
        if not args.run_id.strip() or args.attempt < 1:
            raise MutationError("run-id and positive attempt are required")
        root, output = args.repo_root.resolve(), args.output.resolve()
        if args.action in {"plan", "check"}:
            binding, _, _ = _inputs(root, args.base, args.head, args.broad)
            value = {
                "schema": "tc.fitness/mutation-plan/v1",
                **binding,
                "required": binding["scope"]["required"],
            }
            if args.action == "plan":
                _write_json(output, value)
                print(json.dumps(value))
                return 0
            output.mkdir(parents=True, exist_ok=False)
            _write_json(output / "selection.json", value)
            if not value["required"]:
                print(json.dumps({"status": "not-required", "selection": str(output / "selection.json")}))
                return 0
            output = output / "run"
        function = execute_mutation if args.action in {"run", "check"} else validate_mutation_receipt
        receipt = function(
            root, args.base, args.head, output, run_id=args.run_id, attempt=args.attempt, broad=args.broad
        )
        if args.action in {"run", "check"} and receipt["status"] == "pass":
            receipt = validate_mutation_receipt(
                root, args.base, args.head, output, run_id=args.run_id, attempt=args.attempt, broad=args.broad
            )
        print(json.dumps({"status": receipt["status"], "receipt": str(output / "receipt.json")}))
        return {"pass": 0, "fail": 1, "error": 2}[receipt["status"]]
    except (MutationError, OSError, KeyError, TypeError, ValueError) as exc:
        print(
            json.dumps(
                {"status": "error", "code": getattr(exc, "code", "invalid-evidence"), "message": str(exc)}
            )
        )
        return 2
