"""Real changed-code mutation and exact-candidate admission controls."""

from __future__ import annotations

import ast
import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
import threading
import time
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from tc_fitness.mutation_assurance import (
    _native_mutants,
    execute_mutation,
    main,
    validate_mutation_receipt,
)
from tc_fitness.mutation_scope import MutationError

pytestmark = pytest.mark.integration

CLI = str(Path(sys.executable).with_name("tc-fitness"))


def _git(root: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def _consumer(root: Path, *, weak: bool = False) -> tuple[str, str]:
    root.mkdir()
    (root / "src").mkdir()
    (root / "tests").mkdir()
    (root / "src/admission.py").write_text("def accepts(age):\n    return age > 18\n")
    tests = (
        "import pytest\nfrom admission import accepts\n\npytestmark = pytest.mark.unit\n\ndef test_admission():\n"
        + (
            "    assert isinstance(accepts(20), bool)\n"
            if weak
            else "    assert accepts(17) is False\n    assert accepts(18) is True\n    assert accepts(19) is True\n"
        )
    )
    (root / "tests/test_admission.py").write_text(tests)
    (root / "mutation.toml").write_text(
        'schema = "tc.fitness/mutation-policy/v1"\n'
        'source_roots = ["src"]\ntests = ["tests"]\n'
        "timeout_seconds = 60\nmax_mutants = 100\n"
    )
    _git(root, "init", "-q")
    _git(root, "config", "user.name", "three-cubes-agent[bot]")
    _git(root, "config", "user.email", "295831460+three-cubes-agent[bot]@users.noreply.github.com")
    _git(root, "add", ".")
    _git(root, "commit", "-qm", "test: initial consumer")
    base = _git(root, "rev-parse", "HEAD")
    (root / "src/admission.py").write_text("def accepts(age):\n    return age >= 18\n")
    _git(root, "add", ".")
    _git(root, "commit", "-qm", "fix: accept boundary age")
    return base, _git(root, "rev-parse", "HEAD")


def _command(
    root: Path, base: str, head: str, output: Path, action: str = "run"
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            CLI,
            "mutation",
            action,
            "--repo-root",
            str(root),
            "--base",
            base,
            "--head",
            head,
            "--output",
            str(output),
            "--run-id",
            "local-test",
            "--attempt",
            "1",
        ],
        capture_output=True,
        text=True,
        check=False,
        timeout=90,
    )


def test_real_changed_comparison_mutants_are_killed_and_admitted(tmp_path: Path) -> None:
    root = tmp_path / "consumer"
    base, head = _consumer(root)
    output = tmp_path / "evidence"
    result = _command(root, base, head, output)
    assert result.returncode == 0, result.stdout + result.stderr
    receipt = json.loads((output / "receipt.json").read_text())
    assert receipt["schema"] == "tc.fitness/mutation-receipt/v1"
    assert receipt["base"] == base
    assert receipt["head"] == head
    assert receipt["status"] == "pass"
    assert receipt["mutants"]
    assert all(item["status"] == "killed" for item in receipt["mutants"])
    assert any(item["function"] == "admission.accepts" for item in receipt["mutants"])
    admitted = _command(root, base, head, output, "verify")
    assert admitted.returncode == 0, admitted.stdout + admitted.stderr


def test_surviving_real_mutant_blocks_admission(tmp_path: Path) -> None:
    root = tmp_path / "consumer"
    base, head = _consumer(root, weak=True)
    output = tmp_path / "evidence"
    result = _command(root, base, head, output)
    assert result.returncode == 1, result.stdout + result.stderr
    receipt = json.loads((output / "receipt.json").read_text())
    assert receipt["status"] == "fail"
    assert any(item["status"] == "survived" for item in receipt["mutants"])
    assert _command(root, base, head, output, "verify").returncode != 0


def test_missing_receipt_cannot_satisfy_admission(tmp_path: Path) -> None:
    root = tmp_path / "consumer"
    base, head = _consumer(root)
    result = _command(root, base, head, tmp_path / "missing", "verify")
    assert result.returncode == 2
    assert json.loads(result.stdout)["code"] == "missing-receipt"


def test_missing_mutation_distribution_is_a_dependency_error(tmp_path: Path) -> None:
    from importlib.metadata import distribution

    root = tmp_path / "consumer"
    base, head = _consumer(root)
    metadata = Path(str(distribution("mutmut")._path))
    hidden = metadata.with_name(metadata.name + ".hidden-for-test")
    metadata.rename(hidden)
    try:
        with pytest.raises(MutationError, match="required mutmut executable is unavailable"):
            execute_mutation(root, base, head, tmp_path / "evidence", run_id="test", attempt=1)
    finally:
        hidden.rename(metadata)


def test_wrong_installed_mutation_version_is_rejected(tmp_path: Path) -> None:
    root = tmp_path / "consumer"
    base, head = _consumer(root)
    fake_distribution = tmp_path / "fake-distribution"
    metadata = fake_distribution / "mutmut-0.0.0.dist-info"
    metadata.mkdir(parents=True)
    (metadata / "METADATA").write_text("Metadata-Version: 2.1\nName: mutmut\nVersion: 0.0.0\n")
    sys.path.insert(0, str(fake_distribution))
    try:
        with pytest.raises(MutationError, match="exact pinned mutmut tool"):
            execute_mutation(root, base, head, tmp_path / "evidence", run_id="test", attempt=1)
    finally:
        sys.path.remove(str(fake_distribution))


def test_candidate_change_during_real_mutation_is_rejected(tmp_path: Path) -> None:
    root = tmp_path / "consumer"
    base, head = _consumer(root)
    barrier = tmp_path / "mutation-started.fifo"
    signalled = tmp_path / "mutation-signalled"
    os.mkfifo(barrier)
    test_file = root / "tests/test_admission.py"
    test_file.write_text(
        test_file.read_text()
        + "\ndef test_signal_mutation_started():\n"
        + f"    marker = __import__('pathlib').Path({str(signalled)!r})\n"
        + "    if not marker.exists():\n"
        + "        marker.write_text('sent')\n"
        + f"        open({str(barrier)!r}, 'w').close()\n"
    )
    _git(root, "add", ".")
    _git(root, "commit", "-qm", "test: deterministic mutation barrier")
    head = _git(root, "rev-parse", "HEAD")

    changed = threading.Event()

    def alter_candidate() -> None:
        with barrier.open("rb"):
            pass
        source = root / "src/admission.py"
        source.write_text(source.read_text() + "\n# changed during execution\n")
        changed.set()

    thread = threading.Thread(target=alter_candidate, daemon=True)
    thread.start()
    receipt = execute_mutation(root, base, head, tmp_path / "evidence", run_id="test", attempt=1)
    thread.join(timeout=2)

    assert changed.is_set()
    assert receipt["status"] == "error"
    assert receipt["error"] == "candidate checkout has tracked modifications"


def test_duplicate_native_mutant_identity_is_rejected(
    killed_evidence: tuple[Path, str, str, Path],
) -> None:
    _root, _base, _head, output = killed_evidence
    receipt = json.loads((output / "receipt.json").read_text())
    scope = copy.deepcopy(receipt["scope"])
    scope["functions"].append(copy.deepcopy(scope["functions"][0]))
    with pytest.raises(MutationError, match="duplicate native mutant identity"):
        _native_mutants(output / "native", scope)


def _seal(output: Path, receipt: dict[str, object]) -> None:
    """An attacker can recompute an outer digest; admission must still disagree."""
    receipt.pop("payload_digest", None)
    encoded = json.dumps(receipt, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    receipt["payload_digest"] = "sha256:" + hashlib.sha256(encoded).hexdigest()
    (output / "receipt.json").write_text(json.dumps(receipt))


@pytest.fixture(scope="module")
def killed_evidence(tmp_path_factory: pytest.TempPathFactory) -> tuple[Path, str, str, Path]:
    temporary = tmp_path_factory.mktemp("killed-mutation")
    root = temporary / "consumer"
    base, head = _consumer(root)
    output = temporary / "evidence"
    receipt = execute_mutation(root, base, head, output, run_id="local-test", attempt=1)
    assert receipt["status"] == "pass", receipt
    return root, base, head, output


@pytest.mark.parametrize(
    "sabotage",
    [
        "empty-mutants",
        "wrong-base",
        "wrong-head",
        "wrong-source",
        "wrong-run",
        "wrong-attempt",
        "stale",
        "missing-native",
        "remove-one-native-mutant",
        "empty-test-map",
        "no-op-mutant",
        "unbound-nested-receipt",
    ],
)
def test_resealed_incomplete_or_mismatched_evidence_is_rejected(
    tmp_path: Path,
    killed_evidence: tuple[Path, str, str, Path],
    sabotage: str,
) -> None:
    root, base, head, original = killed_evidence
    output = tmp_path / "sabotaged"
    shutil.copytree(original, output)
    receipt = json.loads((output / "receipt.json").read_text())
    if sabotage == "empty-mutants":
        receipt["mutants"] = []
    elif sabotage == "wrong-base":
        receipt["base"] = "f" * 40
    elif sabotage == "wrong-head":
        receipt["head"] = "f" * 40
    elif sabotage == "wrong-source":
        receipt["source_digest"] = "sha256:" + "f" * 64
    elif sabotage == "wrong-run":
        receipt["run_id"] = "different-run"
    elif sabotage == "wrong-attempt":
        receipt["attempt"] = 2
    elif sabotage == "stale":
        receipt["started_at"] = receipt["finished_at"] = (datetime.now(UTC) - timedelta(days=2)).isoformat()
    elif sabotage == "missing-native":
        (output / "native/src/admission.py.meta").unlink()
    elif sabotage == "remove-one-native-mutant":
        meta_path = output / "native/src/admission.py.meta"
        meta = json.loads(meta_path.read_text())
        removed = next(iter(meta["exit_code_by_key"]))
        del meta["exit_code_by_key"][removed]
        meta_path.write_text(json.dumps(meta))
        receipt["mutants"] = [item for item in receipt["mutants"] if item["id"] != removed]
    elif sabotage == "empty-test-map":
        stats_path = output / "native/mutmut-stats.json"
        stats = json.loads(stats_path.read_text())
        stats["tests_by_mangled_function_name"] = {}
        stats_path.write_text(json.dumps(stats))
    elif sabotage == "no-op-mutant":
        source = output / "native/src/admission.py"
        source.write_text(source.read_text().replace("return age > 18", "return age >= 18"))
    elif sabotage == "unbound-nested-receipt":
        (output / "native/receipt.json").write_text('{"status":"pass"}')
    if sabotage in {"remove-one-native-mutant", "empty-test-map", "no-op-mutant"}:
        for artifact in receipt["artifacts"]:
            artifact["digest"] = (
                "sha256:" + hashlib.sha256((output / artifact["path"]).read_bytes()).hexdigest()
            )
    _seal(output, receipt)
    result = _command(root, base, head, output, "verify")
    assert result.returncode == 2, result.stdout + result.stderr
    assert json.loads(result.stdout)["status"] == "error"


def test_zero_changed_scope_does_not_emit_admissible_receipt(tmp_path: Path) -> None:
    root = tmp_path / "consumer"
    _, head = _consumer(root)
    result = _command(root, head, head, tmp_path / "evidence")
    assert result.returncode == 2
    assert json.loads(result.stdout)["code"] == "zero-scope"
    assert not (tmp_path / "evidence/receipt.json").exists()


def test_source_edit_after_receipt_prevents_admission(tmp_path: Path) -> None:
    root = tmp_path / "consumer"
    base, head = _consumer(root)
    output = tmp_path / "evidence"
    assert _command(root, base, head, output).returncode == 0
    (root / "src/admission.py").write_text("def accepts(age):\n    return True\n")
    assert _command(root, base, head, output, "verify").returncode == 2


def test_mutation_suppression_cannot_remove_a_decision_from_scope(tmp_path: Path) -> None:
    root = tmp_path / "consumer"
    base, _ = _consumer(root)
    (root / "src/admission.py").write_text(
        "def accepts(age):\n    return age >= 18  # pragma: no mutate\n\ndef other(value):\n    return value + 1\n"
    )
    _git(root, "add", ".")
    _git(root, "commit", "-qm", "test: forbidden mutation suppression")
    head = _git(root, "rev-parse", "HEAD")
    result = _command(root, base, head, tmp_path / "plan.json", "plan")
    assert result.returncode == 2
    assert "suppression" in json.loads(result.stdout)["message"]


def test_deleted_production_function_still_selects_its_remaining_callers(tmp_path: Path) -> None:
    root = tmp_path / "consumer"
    _consumer(root)
    (root / "src/admission.py").write_text(
        "def helper(age):\n    return age >= 18\n\ndef accepts(age):\n    return helper(age)\n"
    )
    _git(root, "add", ".")
    _git(root, "commit", "-qm", "refactor: extract decision")
    base = _git(root, "rev-parse", "HEAD")
    (root / "src/admission.py").write_text("def accepts(age):\n    return helper(age)\n")
    _git(root, "add", ".")
    _git(root, "commit", "-qm", "test: deleted dependency")
    head = _git(root, "rev-parse", "HEAD")
    result = _command(root, base, head, tmp_path / "plan.json", "plan")
    assert result.returncode == 0, result.stdout
    plan = json.loads(result.stdout)
    assert plan["required"] is True
    assert {item["name"] for item in plan["scope"]["functions"]} == {"admission.accepts"}


def test_dependency_closure_includes_relative_imports_but_not_unrelated_functions(tmp_path: Path) -> None:
    root = tmp_path / "consumer"
    _consumer(root)
    (root / "src/package").mkdir()
    (root / "src/package/__init__.py").write_text("")
    (root / "src/package/helper.py").write_text("def boundary(age):\n    return age >= 18\n")
    (root / "src/package/check.py").write_text(
        "from . import helper\n\ndef decision(age):\n    return helper.boundary(age)\n\ndef unrelated(value):\n    return value + 1\n"
    )
    _git(root, "add", ".")
    _git(root, "commit", "-qm", "test: relative dependency")
    base = _git(root, "rev-parse", "HEAD")
    (root / "src/package/check.py").write_text(
        "from . import helper\n\ndef decision(age):\n    return helper.boundary(age + 1)\n\ndef unrelated(value):\n    return value + 1\n"
    )
    _git(root, "add", ".")
    _git(root, "commit", "-qm", "fix: changed caller")
    head = _git(root, "rev-parse", "HEAD")
    result = _command(root, base, head, tmp_path / "plan.json", "plan")
    assert result.returncode == 0, result.stdout
    scope = json.loads(result.stdout)["scope"]
    assert scope["changed_functions"] == ["package.check.decision"]
    assert {item["name"] for item in scope["functions"]} == {
        "package.check.decision",
        "package.helper.boundary",
    }


def test_documentation_only_check_records_selection_not_a_mutation_pass(tmp_path: Path) -> None:
    root = tmp_path / "consumer"
    _, base = _consumer(root)
    (root / "README.md").write_text("Public admission example.\n")
    _git(root, "add", ".")
    _git(root, "commit", "-qm", "docs: explain admission")
    head = _git(root, "rev-parse", "HEAD")
    output = tmp_path / "evidence"
    result = _command(root, base, head, output, "check")
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout)["status"] == "not-required"
    plan = json.loads((output / "selection.json").read_text())
    assert plan["required"] is False
    assert not list(output.rglob("receipt.json"))
    assert _command(root, base, head, output, "verify").returncode == 2


def test_changed_check_produces_and_validates_a_real_mutation_receipt(tmp_path: Path) -> None:
    root = tmp_path / "consumer"
    base, head = _consumer(root)
    output = tmp_path / "evidence"
    result = _command(root, base, head, output, "check")
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads((output / "selection.json").read_text())["required"] is True
    assert _command(root, base, head, output / "run", "verify").returncode == 0


def test_native_deadline_retains_error_instead_of_a_killed_mutant(tmp_path: Path) -> None:
    root = tmp_path / "consumer"
    base, _ = _consumer(root)
    (root / "tests/test_admission.py").write_text(
        "import time\nimport pytest\nfrom admission import accepts\n\npytestmark = pytest.mark.unit\n\ndef test_admission():\n    time.sleep(10)\n    assert accepts(18)\n"
    )
    policy = root / "mutation.toml"
    policy.write_text(policy.read_text().replace("timeout_seconds = 60", "timeout_seconds = 1"))
    _git(root, "add", ".")
    _git(root, "commit", "-qm", "test: native deadline")
    head = _git(root, "rev-parse", "HEAD")
    output = tmp_path / "evidence"
    result = _command(root, base, head, output)
    assert result.returncode == 2, result.stdout + result.stderr
    receipt = json.loads((output / "receipt.json").read_text())
    assert receipt["status"] == "error"
    assert receipt["tool_exit_code"] == 124
    assert _command(root, base, head, output, "verify").returncode == 2


def test_global_callable_alias_does_not_disappear_from_dependency_closure(tmp_path: Path) -> None:
    root = tmp_path / "consumer"
    _consumer(root)
    source = root / "src/admission.py"
    source.write_text(
        "def boundary(age):\n    return age >= 18\n\nhandler = boundary\n\ndef accepts(age):\n    return handler(age)\n"
    )
    _git(root, "add", ".")
    _git(root, "commit", "-qm", "test: callable alias")
    base = _git(root, "rev-parse", "HEAD")
    source.write_text(source.read_text().replace("return handler(age)", "return handler(age + 1)"))
    _git(root, "add", ".")
    _git(root, "commit", "-qm", "test: changed alias caller")
    head = _git(root, "rev-parse", "HEAD")
    result = _command(root, base, head, tmp_path / "plan.json", "plan")
    assert result.returncode == 0, result.stdout
    assert {item["name"] for item in json.loads(result.stdout)["scope"]["functions"]} >= {
        "admission.accepts",
        "admission.boundary",
    }


def test_package_reexport_does_not_hide_an_imported_dependency(tmp_path: Path) -> None:
    root = tmp_path / "consumer"
    _consumer(root)
    (root / "src/package").mkdir()
    (root / "src/package/__init__.py").write_text("from .helper import boundary\n")
    (root / "src/package/helper.py").write_text("def boundary(age):\n    return age >= 18\n")
    source = root / "src/admission.py"
    source.write_text("from package import boundary\n\ndef accepts(age):\n    return boundary(age)\n")
    _git(root, "add", ".")
    _git(root, "commit", "-qm", "test: package reexport")
    base = _git(root, "rev-parse", "HEAD")
    source.write_text(source.read_text().replace("return boundary(age)", "return boundary(age + 1)"))
    _git(root, "add", ".")
    _git(root, "commit", "-qm", "test: changed reexport caller")
    head = _git(root, "rev-parse", "HEAD")
    result = _command(root, base, head, tmp_path / "plan.json", "plan")
    assert result.returncode == 0, result.stdout
    assert {item["name"] for item in json.loads(result.stdout)["scope"]["functions"]} >= {
        "admission.accepts",
        "package.helper.boundary",
    }


def test_native_snapshot_preserves_tracked_executable_dependencies(tmp_path: Path) -> None:
    root = tmp_path / "consumer"
    base, _ = _consumer(root)
    (root / "scripts").mkdir()
    executable = root / "scripts/ready"
    executable.write_text("#!/bin/sh\nexit 0\n")
    executable.chmod(0o755)
    test = root / "tests/test_admission.py"
    test.write_text(
        "import subprocess\n"
        + test.read_text().replace("pytest.mark.unit", "pytest.mark.contract")
        + "\ndef test_native_dependency():\n    subprocess.run(['./scripts/ready'], check=True)\n"
    )
    _git(root, "add", ".")
    _git(root, "commit", "-qm", "test: executable native dependency")
    head = _git(root, "rev-parse", "HEAD")
    result = _command(root, base, head, tmp_path / "evidence")
    assert result.returncode == 0, result.stdout + result.stderr


def test_public_help_advertises_mutation_assurance() -> None:
    result = subprocess.run([CLI, "--help"], capture_output=True, text=True, check=True)
    assert "mutation" in result.stdout


def test_git_export_attributes_cannot_hide_changed_production(tmp_path: Path) -> None:
    root = tmp_path / "consumer"
    base, _ = _consumer(root)
    (root / ".gitattributes").write_text("src/admission.py export-ignore\n")
    (root / "src/other.py").write_text("def other(value):\n    return value\n")
    _git(root, "add", ".")
    _git(root, "commit", "-qm", "test: hidden production export")
    head = _git(root, "rev-parse", "HEAD")
    result = _command(root, base, head, tmp_path / "plan.json", "plan")
    assert result.returncode == 2, result.stdout
    assert "archive" in json.loads(result.stdout)["message"]


def test_mutation_uses_contract_unit_tests_not_distribution_e2e(tmp_path: Path) -> None:
    root = tmp_path / "consumer"
    base, _ = _consumer(root)
    (root / "tests/test_distribution.py").write_text(
        "import pytest\npytestmark = pytest.mark.e2e\n\ndef test_distribution():\n    raise RuntimeError('not a mutation test tier')\n"
    )
    _git(root, "add", ".")
    _git(root, "commit", "-qm", "test: separate distribution qualification")
    head = _git(root, "rev-parse", "HEAD")
    result = _command(root, base, head, tmp_path / "evidence")
    assert result.returncode == 0, result.stdout + result.stderr
    receipt = json.loads((tmp_path / "evidence/receipt.json").read_text())
    assert receipt["status"] == "pass"
    assert receipt["mutants"]


def test_e2e_only_tests_cannot_claim_unit_contract_mutation_proof(tmp_path: Path) -> None:
    root = tmp_path / "consumer"
    base, _ = _consumer(root)
    source = root / "tests/test_admission.py"
    source.write_text(source.read_text().replace("pytest.mark.unit", "pytest.mark.e2e"))
    _git(root, "add", ".")
    _git(root, "commit", "-qm", "test: absent mutation test tier")
    head = _git(root, "rev-parse", "HEAD")
    result = _command(root, base, head, tmp_path / "evidence")
    assert result.returncode == 2, result.stdout + result.stderr
    assert _command(root, base, head, tmp_path / "evidence", "verify").returncode == 2


def _reseal_artifacts(output: Path, receipt: dict[str, object]) -> None:
    receipt["artifacts"] = [
        {
            "path": path.relative_to(output).as_posix(),
            "digest": "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest(),
        }
        for path in sorted(output.rglob("*"))
        if path.is_file() and path != output / "receipt.json"
    ]
    _seal(output, receipt)


def test_native_admission_returns_the_complete_bound_receipt(
    killed_evidence: tuple[Path, str, str, Path],
) -> None:
    root, base, head, output = killed_evidence
    original = (output / "receipt.json").read_bytes()
    result = validate_mutation_receipt(root, base, head, output, run_id="local-test", attempt=1)
    assert result == json.loads(original)
    assert (output / "receipt.json").read_bytes() == original


@pytest.mark.parametrize(
    ("sabotage", "message"),
    [
        ("duplicate-json", "missing or malformed mutation output"),
        ("malformed-json", "missing or malformed mutation output"),
        ("array-json", "must be an object"),
        ("digest", "^mutation receipt digest mismatch$"),
        ("missing-digest", "^mutation receipt digest mismatch$"),
        ("uuid", "invalid mutation execution identity"),
        ("naive-time", "invalid mutation execution identity"),
        ("missing-time", "invalid mutation execution identity"),
        ("reversed-time", "invalid mutation execution identity"),
        ("future-time", "invalid mutation execution identity"),
        ("boolean-attempt", "attempt mismatch"),
        ("missing-required-log", "^missing required native mutation outputs$"),
        ("symlink-log", "must not be symlinks"),
        ("missing-status-map", "no terminal status map"),
        ("missing-source", "missing or invalid generated mutant source"),
        ("invalid-source", "missing or invalid generated mutant source"),
        ("missing-original", "exact candidate definition"),
        ("changed-original", "exact candidate definition"),
        ("unchanged-mutant", "unchanged, no-op mutant"),
        ("missing-association", "no real native test association"),
        ("nonlist-association", "no real native test association"),
        ("unknown-test", "no real native test association"),
        ("nonstring-test", "no real native test association"),
        ("boolean-duration", "no real native test association"),
        ("negative-duration", "no real native test association"),
        ("nonnumeric-duration", "no real native test association"),
        ("nonterminal-code", "terminal killed results"),
        ("error-code", "terminal killed results"),
        ("empty-inventory", "empty or zero-scope native mutation evidence"),
        (
            "tool-exit",
            "^mutation admission requires terminal killed results for every selected mutant$",
        ),
    ],
)
def test_native_admission_rejects_resealed_protocol_corruption(
    tmp_path: Path, killed_evidence: tuple[Path, str, str, Path], sabotage: str, message: str
) -> None:
    root, base, head, original = killed_evidence
    output = tmp_path / "evidence"
    shutil.copytree(original, output)
    receipt_path = output / "receipt.json"
    receipt = json.loads(receipt_path.read_text())
    meta_path = output / "native/src/admission.py.meta"
    stats_path = output / "native/mutmut-stats.json"
    source_path = output / "native/src/admission.py"
    meta = json.loads(meta_path.read_text())
    stats = json.loads(stats_path.read_text())
    function = "admission.x_accepts"
    test = stats["tests_by_mangled_function_name"][function][0]
    if sabotage == "uuid":
        receipt["execution_id"] = "not-a-uuid"
    elif sabotage == "naive-time":
        receipt["started_at"] = "2026-01-01T00:00:00"
    elif sabotage == "missing-time":
        del receipt["started_at"]
    elif sabotage == "reversed-time":
        receipt["started_at"], receipt["finished_at"] = receipt["finished_at"], receipt["started_at"]
    elif sabotage == "future-time":
        receipt["finished_at"] = (datetime.now(UTC) + timedelta(days=1)).isoformat()
    elif sabotage == "boolean-attempt":
        receipt["attempt"] = True
    elif sabotage == "missing-required-log":
        (output / "stdout.log").unlink()
    elif sabotage == "symlink-log":
        (output / "stdout.log").unlink()
        (output / "stdout.log").symlink_to(original / "stdout.log")
    elif sabotage == "missing-status-map":
        meta["exit_code_by_key"] = []
    elif sabotage == "missing-source":
        source_path.unlink()
    elif sabotage == "invalid-source":
        source_path.write_text("def invalid(:\n")
    elif sabotage == "missing-original":
        source_path.write_text(
            source_path.read_text().replace("def x_accepts__mutmut_orig(", "def removed_original(")
        )
    elif sabotage == "changed-original":
        source_path.write_text(source_path.read_text().replace("return age >= 18", "return age >= 21"))
    elif sabotage == "unchanged-mutant":
        source = ast.parse(source_path.read_text())
        definitions = {node.name: node for node in ast.walk(source) if isinstance(node, ast.FunctionDef)}
        name = next(iter(meta["exit_code_by_key"])).rsplit(".", 1)[1]
        definitions[name].body = copy.deepcopy(definitions["x_accepts__mutmut_orig"].body)
        source_path.write_text(ast.unparse(source))
    elif sabotage == "missing-association":
        stats["tests_by_mangled_function_name"][function] = []
    elif sabotage == "nonlist-association":
        stats["tests_by_mangled_function_name"][function] = test
    elif sabotage == "unknown-test":
        stats["tests_by_mangled_function_name"][function] = ["test_unknown.py::test_unrun"]
    elif sabotage == "nonstring-test":
        stats["tests_by_mangled_function_name"][function] = [42]
    elif sabotage == "boolean-duration":
        stats["duration_by_test"][test] = True
    elif sabotage == "negative-duration":
        stats["duration_by_test"][test] = -1
    elif sabotage == "nonnumeric-duration":
        stats["duration_by_test"][test] = "fast"
    elif sabotage in {"nonterminal-code", "error-code"}:
        code = None if sabotage == "nonterminal-code" else 2
        for name in meta["exit_code_by_key"]:
            meta["exit_code_by_key"][name] = code
        for mutant in receipt["mutants"]:
            mutant.update(exit_code=code, status="error")
    elif sabotage == "empty-inventory":
        source_path.write_text("def x_accepts__mutmut_orig(age):\n    return age >= 18\n")
        meta["exit_code_by_key"] = {}
        receipt["mutants"] = []
    elif sabotage == "tool-exit":
        receipt["tool_exit_code"] = 1
    meta_path.write_text(json.dumps(meta))
    stats_path.write_text(json.dumps(stats))
    _reseal_artifacts(output, receipt)
    if sabotage == "duplicate-json":
        receipt_path.write_text('{"status":"pass","status":"fail"}')
    elif sabotage == "malformed-json":
        receipt_path.write_text("{")
    elif sabotage == "array-json":
        receipt_path.write_text("[]")
    elif sabotage == "digest":
        receipt["payload_digest"] = "sha256:" + "0" * 64
        receipt_path.write_text(json.dumps(receipt))
    elif sabotage == "missing-digest":
        del receipt["payload_digest"]
        receipt_path.write_text(json.dumps(receipt))
    with pytest.raises(MutationError, match=message):
        validate_mutation_receipt(root, base, head, output, run_id="local-test", attempt=1)


@pytest.mark.parametrize("run_id,attempt", [("", 1), ("  ", 1), ("local-test", 0), ("local-test", -1)])
def test_public_main_requires_attempt_identity(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], run_id: str, attempt: int
) -> None:
    output = tmp_path / "must-not-exist"
    result = main(
        [
            "plan",
            "--base",
            "0" * 40,
            "--head",
            "1" * 40,
            "--output",
            str(output),
            "--run-id",
            run_id,
            "--attempt",
            str(attempt),
        ]
    )
    assert result == 2
    assert json.loads(capsys.readouterr().out) == {
        "status": "error",
        "code": "invalid-evidence",
        "message": "run-id and positive attempt are required",
    }
    assert not output.exists()


def test_existing_output_preserves_prior_attempt(killed_evidence: tuple[Path, str, str, Path]) -> None:
    root, base, head, output = killed_evidence
    before = (output / "receipt.json").read_bytes()
    result = _command(root, base, head, output)
    assert result.returncode == 2
    assert "output already exists" in json.loads(result.stdout)["message"]
    assert (output / "receipt.json").read_bytes() == before


def test_native_configuration_cannot_override_reviewed_mutation_controls(tmp_path: Path) -> None:
    root = tmp_path / "consumer"
    base, _ = _consumer(root)
    (root / "pyproject.toml").write_text('[tool.mutmut]\nsource_paths = ["irrelevant"]\n')
    _git(root, "add", ".")
    _git(root, "commit", "-qm", "test: conflicting native controls")
    result = _command(root, base, _git(root, "rev-parse", "HEAD"), tmp_path / "evidence")
    assert result.returncode == 2
    assert "second configuration is forbidden" in json.loads(result.stdout)["message"]
    assert not (tmp_path / "evidence/receipt.json").exists()


def test_real_mutant_inventory_cannot_exceed_declared_budget(tmp_path: Path) -> None:
    root = tmp_path / "consumer"
    base, _ = _consumer(root)
    policy = root / "mutation.toml"
    policy.write_text(policy.read_text().replace("max_mutants = 100", "max_mutants = 1"))
    _git(root, "add", ".")
    _git(root, "commit", "-qm", "test: bounded native inventory")
    head = _git(root, "rev-parse", "HEAD")
    output = tmp_path / "evidence"
    result = _command(root, base, head, output)
    assert result.returncode == 2, result.stdout + result.stderr
    receipt = json.loads((output / "receipt.json").read_text())
    assert receipt["status"] == "error"
    assert receipt["error"] == "mutation scope exceeds the reviewed mutant budget"
    assert len(receipt["mutants"]) > 1
    assert _command(root, base, head, output, "verify").returncode == 2


def test_native_test_process_error_is_not_a_killed_mutant(tmp_path: Path) -> None:
    root = tmp_path / "consumer"
    base, _ = _consumer(root)
    (root / "tests/test_admission.py").write_text(
        "import os\nimport pytest\nfrom admission import accepts\n"
        "pytestmark = pytest.mark.unit\n"
        "def test_admission():\n"
        "    if not accepts(18):\n        os._exit(2)\n"
        "    assert accepts(17) is False\n    assert accepts(19) is True\n"
    )
    _git(root, "add", ".")
    _git(root, "commit", "-qm", "test: native process failure")
    output = tmp_path / "evidence"
    result = _command(root, base, _git(root, "rev-parse", "HEAD"), output)
    assert result.returncode == 2, result.stdout + result.stderr
    receipt = json.loads((output / "receipt.json").read_text())
    assert receipt["tool_exit_code"] == 0
    assert receipt["status"] == "error"
    assert (
        receipt["error"]
        == "native mutation results include missing, untested, interrupted or errored mutants"
    )
    assert any(item["exit_code"] == 2 and item["status"] == "error" for item in receipt["mutants"])


def test_native_diagnostics_budget_retains_failure_evidence(tmp_path: Path) -> None:
    root = tmp_path / "consumer"
    base, _ = _consumer(root)
    (root / "pyproject.toml").write_text('[tool.pytest.ini_options]\naddopts = "-s"\n')
    test = root / "tests/test_admission.py"
    test.write_text(
        "import os\n"
        + test.read_text().replace(
            "def test_admission():\n", "def test_admission():\n    os.write(1, b'diagnostic ' * 220000)\n"
        )
    )
    _git(root, "add", ".")
    _git(root, "commit", "-qm", "test: bounded native diagnostics")
    output = tmp_path / "evidence"
    result = _command(root, base, _git(root, "rev-parse", "HEAD"), output)
    assert result.returncode == 2, result.stdout + result.stderr
    receipt = json.loads((output / "receipt.json").read_text())
    assert receipt["status"] == "error"
    assert receipt["error"] == "native mutation diagnostics exceeded the bounded output budget"
    assert (output / "stdout.log").stat().st_size > 2 * 1024 * 1024
    assert receipt["mutants"] == []


def test_native_results_keep_distinct_functions_in_one_module(tmp_path: Path) -> None:
    root = tmp_path / "consumer"
    base, _ = _consumer(root)
    source = root / "src/admission.py"
    source.write_text(source.read_text() + "\ndef next_age(age):\n    return age + 1\n")
    test = root / "tests/test_admission.py"
    test.write_text(
        test.read_text()
        + "\ndef test_next_age():\n    from admission import next_age\n"
        + "    assert next_age(0) == 1\n    assert next_age(1) == 2\n    assert next_age(-1) == 0\n"
    )
    _git(root, "add", ".")
    _git(root, "commit", "-qm", "test: multiple native function results")
    head = _git(root, "rev-parse", "HEAD")
    output = tmp_path / "evidence"
    result = _command(root, base, head, output)
    assert result.returncode == 0, result.stdout + result.stderr
    receipt = json.loads((output / "receipt.json").read_text())
    assert {item["function"] for item in receipt["mutants"]} == {"admission.accepts", "admission.next_age"}
    assert all(item["status"] == "killed" for item in receipt["mutants"])
    assert _command(root, base, head, output, "verify").returncode == 0


def test_public_admission_reports_exact_missing_receipt_error(
    tmp_path: Path, killed_evidence: tuple[Path, str, str, Path]
) -> None:
    root, base, head, _ = killed_evidence
    with pytest.raises(MutationError) as failure:
        validate_mutation_receipt(root, base, head, tmp_path / "missing", run_id="local-test", attempt=1)
    assert failure.value.code == "missing-receipt"
    assert str(failure.value) == "missing mutation receipt"


@pytest.mark.parametrize(
    "sabotage,message",
    [
        ("artifact", "missing, extra or altered native mutation artifacts"),
        ("mutants", "native mutant set does not match the claimed evidence"),
    ],
)
def test_public_admission_distinguishes_artifact_corruption_from_claimed_inventory(
    tmp_path: Path, killed_evidence: tuple[Path, str, str, Path], sabotage: str, message: str
) -> None:
    root, base, head, original = killed_evidence
    output = tmp_path / "evidence"
    shutil.copytree(original, output)
    receipt = json.loads((output / "receipt.json").read_text())
    if sabotage == "artifact":
        (output / "stdout.log").write_text("replacement diagnostics")
    else:
        receipt["mutants"] = []
    _seal(output, receipt)
    with pytest.raises(MutationError) as failure:
        validate_mutation_receipt(root, base, head, output, run_id="local-test", attempt=1)
    assert failure.value.code == "invalid-evidence"
    assert str(failure.value) == message


def test_public_admission_accepts_equal_fresh_start_finish_timestamps(
    tmp_path: Path, killed_evidence: tuple[Path, str, str, Path]
) -> None:
    root, base, head, original = killed_evidence
    output = tmp_path / "evidence"
    shutil.copytree(original, output)
    receipt = json.loads((output / "receipt.json").read_text())
    stamp = (datetime.now(UTC) - timedelta(seconds=1)).isoformat()
    receipt["started_at"] = receipt["finished_at"] = stamp
    _seal(output, receipt)
    admitted = validate_mutation_receipt(root, base, head, output, run_id="local-test", attempt=1)
    assert admitted == json.loads((output / "receipt.json").read_text())
    assert admitted["started_at"] == admitted["finished_at"] == stamp


def test_public_admission_rejects_just_over_twenty_four_hours_using_the_real_clock(
    tmp_path: Path, killed_evidence: tuple[Path, str, str, Path]
) -> None:
    root, base, head, original = killed_evidence
    output = tmp_path / "evidence"
    shutil.copytree(original, output)
    receipt = json.loads((output / "receipt.json").read_text())
    for _ in range(5):
        stamp = (datetime.now(UTC) - timedelta(seconds=86400.1)).isoformat()
        receipt["started_at"] = receipt["finished_at"] = stamp
        _seal(output, receipt)
        started = time.monotonic()
        failure = None
        try:
            validate_mutation_receipt(root, base, head, output, run_id="local-test", attempt=1)
        except MutationError as error:
            failure = error
        if time.monotonic() - started < 0.8:
            assert failure is not None, "evidence older than 24 hours was admitted"
            assert str(failure) == "invalid mutation execution identity or timestamps"
            assert isinstance(failure.__cause__, MutationError)
            assert str(failure.__cause__) == "stale or reversed mutation execution timestamps"
            return
    pytest.fail("could not exercise the real one-second age boundary within its measurement window")


def test_public_admission_accepts_broad_execution_at_the_exact_native_budget(
    tmp_path: Path, killed_evidence: tuple[Path, str, str, Path]
) -> None:
    _, _, _, original = killed_evidence
    budget = len(json.loads((original / "receipt.json").read_text())["mutants"])
    root = tmp_path / "consumer"
    base, _ = _consumer(root)
    policy = root / "mutation.toml"
    policy.write_text(policy.read_text().replace("max_mutants = 100", f"max_mutants = {budget}"))
    _git(root, "add", ".")
    _git(root, "commit", "-qm", "test: exact native result budget")
    head = _git(root, "rev-parse", "HEAD")
    output = tmp_path / "evidence"
    receipt = execute_mutation(root, base, head, output, run_id="broad-boundary", attempt=1, broad=True)
    assert receipt["status"] == "pass", receipt
    assert len(receipt["mutants"]) == budget
    assert receipt["scope"]["mode"] == "broad"
    admitted = validate_mutation_receipt(
        root, base, head, output, run_id="broad-boundary", attempt=1, broad=True
    )
    assert admitted == receipt


def test_public_admission_distinguishes_complete_logs_from_missing_native_inventory(
    tmp_path: Path, killed_evidence: tuple[Path, str, str, Path]
) -> None:
    root, base, head, original = killed_evidence
    output = tmp_path / "evidence"
    output.mkdir()
    for name in ("native-config.toml", "stdout.log", "stderr.log", "native/mutmut-stats.json"):
        target = output / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(original / name, target)
    receipt = json.loads((original / "receipt.json").read_text())
    _reseal_artifacts(output, receipt)
    with pytest.raises(MutationError, match=r"^missing or malformed mutation output: admission\.py\.meta$"):
        validate_mutation_receipt(root, base, head, output, run_id="local-test", attempt=1)
