"""Real changed-code mutation and exact-candidate admission controls."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

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
    tests = "from admission import accepts\n\ndef test_admission():\n" + (
        "    assert isinstance(accepts(20), bool)\n"
        if weak
        else "    assert accepts(17) is False\n    assert accepts(18) is True\n    assert accepts(19) is True\n"
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
    result = _command(root, base, head, output)
    assert result.returncode == 0, result.stdout + result.stderr
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
        "import time\nfrom admission import accepts\n\ndef test_admission():\n    time.sleep(10)\n    assert accepts(18)\n"
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
        + test.read_text()
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
