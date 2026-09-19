"""Behaviour tests for executable evidence claims."""

from __future__ import annotations

from pathlib import Path

import pytest
from _core_check_assertions import assert_no_repo_identity

from tc_fitness.catalogue import RuleEntry
from tc_fitness.check_evidence import CheckResult, capture_check_evidence
from tc_fitness.core_checks.behavioural_evidence import BehaviouralEvidence, build
from tc_fitness.runner import run

pytestmark = pytest.mark.integration


def _seed(repo: Path, rel: str, body: str = "") -> Path:
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    return path


def _config(*, test: str = "tests/integration/test_image_build.py") -> dict[str, object]:
    return {
        "surface_globs": ["infra/docker/Dockerfile.*", "infra/docker/build-*-runtime.sh"],
        "behaviour_markers": ["integration", "e2e"],
        "claims": [
            {
                "id": "release-image-build",
                "surfaces": [
                    "infra/docker/Dockerfile.release",
                    "infra/docker/build-tool-runtime.sh",
                ],
                "tests": [test],
                "executables": ["infra/docker/build-tool-runtime.sh"],
            }
        ],
    }


def _valid_test() -> str:
    return """
import subprocess
from pathlib import Path
import pytest

pytestmark = pytest.mark.integration
ROOT = Path(__file__).parents[2]
BUILD = ROOT / "infra" / "docker" / "build-tool-runtime.sh"

def test_clean_release_build(tmp_path):
    output = tmp_path / "runtime" / "dist" / "index.js"
    result = subprocess.run([str(BUILD), str(tmp_path), str(output.parent)], capture_output=True)
    assert result.returncode == 0
    assert output.exists()
"""


def _seed_surfaces(repo: Path) -> None:
    _seed(repo, "infra/docker/Dockerfile.release", "FROM scratch\n")
    _seed(repo, "infra/docker/build-tool-runtime.sh", "#!/usr/bin/env bash\n")


def test_real_executable_and_observed_artifact_satisfy_claim(tmp_path: Path) -> None:
    _seed_surfaces(tmp_path)
    _seed(tmp_path, "tests/integration/test_image_build.py", _valid_test())

    assert build(_config(), repo_root=tmp_path).collect_findings() == ()


def test_source_text_assertions_cannot_satisfy_behavioural_claim(tmp_path: Path) -> None:
    _seed_surfaces(tmp_path)
    _seed(
        tmp_path,
        "tests/integration/test_image_build.py",
        """
from pathlib import Path
import pytest
pytestmark = pytest.mark.integration

def test_image_shape():
    text = Path("infra/docker/Dockerfile.release").read_text()
    assert "RUN build-tool-runtime.sh" in text
""",
    )

    findings = build(_config(), repo_root=tmp_path).collect_findings()

    assert {finding.code for finding in findings} == {"missing-executable-evidence"}


def test_unrelated_subprocess_cannot_satisfy_named_executable(tmp_path: Path) -> None:
    _seed_surfaces(tmp_path)
    _seed(
        tmp_path,
        "tests/integration/test_image_build.py",
        """
import subprocess
import pytest
pytestmark = pytest.mark.integration

def test_image_shape():
    result = subprocess.run(["git", "status"], capture_output=True)
    assert result.returncode == 0
""",
    )

    findings = build(_config(), repo_root=tmp_path).collect_findings()

    assert {finding.code for finding in findings} == {"missing-executable-evidence"}


def test_execution_without_observed_process_result_is_not_evidence(tmp_path: Path) -> None:
    _seed_surfaces(tmp_path)
    _seed(
        tmp_path,
        "tests/integration/test_image_build.py",
        """
import subprocess
from pathlib import Path
import pytest
pytestmark = pytest.mark.integration
ROOT = Path(__file__).parents[2]
BUILD = ROOT / "infra" / "docker" / "build-tool-runtime.sh"

def test_image_shape(tmp_path):
    subprocess.run([str(BUILD), str(tmp_path)])
    assert True
""",
    )

    findings = build(_config(), repo_root=tmp_path).collect_findings()

    assert {finding.code for finding in findings} == {
        "missing-output-observation",
        "missing-process-observation",
    }


def test_process_success_without_observed_output_is_not_evidence(tmp_path: Path) -> None:
    _seed_surfaces(tmp_path)
    _seed(
        tmp_path,
        "tests/integration/test_image_build.py",
        _valid_test().replace("    assert output.exists()\n", ""),
    )

    findings = build(_config(), repo_root=tmp_path).collect_findings()

    assert {finding.code for finding in findings} == {"missing-output-observation"}


def test_public_runner_emits_structured_behavioural_findings(tmp_path: Path) -> None:
    _seed_surfaces(tmp_path)
    _seed(
        tmp_path,
        "tests/integration/test_image_build.py",
        _valid_test().replace("    assert output.exists()\n", ""),
    )
    entry = RuleEntry(
        id="core:behavioural_evidence",
        gate="core:behavioural_evidence",
        check="core:behavioural_evidence",
    )

    with capture_check_evidence() as evidence:
        verdicts = run(
            (entry,),
            repo_root=tmp_path,
            core_check_configs={"behavioural_evidence": _config()},
        )

    assert verdicts.exit_code == 1
    assert evidence.results == [CheckResult("core:behavioural_evidence", "fail", 1)]
    assert [
        (finding.rule, finding.path, finding.message, finding.status) for finding in evidence.findings
    ] == [
        (
            "behavioural-evidence",
            "infra/docker/build-tool-runtime.sh",
            "/claims/0/executables/0: missing-output-observation: "
            "claim 'release-image-build' executes infra/docker/build-tool-runtime.sh without asserting a passed output; "
            "fix: assert a produced file, response or retained receipt passed to the executable",
            "fail",
        )
    ]


def test_unrelated_file_assertion_is_not_an_output_observation(tmp_path: Path) -> None:
    _seed_surfaces(tmp_path)
    _seed(
        tmp_path,
        "tests/integration/test_image_build.py",
        _valid_test().replace("assert output.exists()", "assert Path('/unrelated').exists()"),
    )

    findings = build(_config(), repo_root=tmp_path).collect_findings()

    assert {finding.code for finding in findings} == {"missing-output-observation"}


def test_every_matched_critical_surface_requires_a_claim(tmp_path: Path) -> None:
    _seed_surfaces(tmp_path)
    _seed(tmp_path, "infra/docker/Dockerfile.other", "FROM scratch\n")
    _seed(tmp_path, "tests/integration/test_image_build.py", _valid_test())

    findings = build(_config(), repo_root=tmp_path).collect_findings()

    assert [(finding.code, finding.source.as_posix()) for finding in findings] == [
        ("unclaimed-critical-surface", "infra/docker/Dockerfile.other")
    ]


def test_missing_test_and_surface_fail_instead_of_vacuously_passing(tmp_path: Path) -> None:
    findings = build(_config(test="tests/integration/missing.py"), repo_root=tmp_path).collect_findings()

    assert {finding.code for finding in findings} == {
        "missing-claimed-surface",
        "missing-evidence-test",
        "unmatched-surface-glob",
    }


def test_behaviour_marker_is_required_on_evidence_test(tmp_path: Path) -> None:
    _seed_surfaces(tmp_path)
    _seed(
        tmp_path,
        "tests/integration/test_image_build.py",
        _valid_test().replace("pytestmark = pytest.mark.integration\n", ""),
    )

    findings = build(_config(), repo_root=tmp_path).collect_findings()

    assert {finding.code for finding in findings} == {"missing-behaviour-marker"}


def test_claim_cannot_omit_surfaces_tests_or_executables(tmp_path: Path) -> None:
    config = {
        "surface_globs": ["infra/docker/Dockerfile.*"],
        "behaviour_markers": ["integration"],
        "claims": [{"id": "empty", "surfaces": [], "tests": [], "executables": []}],
    }

    findings = build(config, repo_root=tmp_path).collect_findings()

    assert {finding.code for finding in findings} == {
        "missing-claim-executables",
        "missing-claim-surfaces",
        "missing-claim-tests",
        "unmatched-surface-glob",
    }


def test_invalid_public_config_values_produce_actionable_findings(tmp_path: Path) -> None:
    config: dict[str, object] = {
        "surface_globs": ["/absolute/path", "../outside", "bad\\path", "", 3, "missing/*"],
        "behaviour_markers": "integration",
        "claims": [
            "not a mapping",
            {
                "id": "",
                "surfaces": ["/absolute", "../escape", "missing.py"],
                "tests": ["../outside.py", "tests/missing.py"],
                "executables": ["../run.sh"],
            },
            {"id": "", "surfaces": [], "tests": [], "executables": []},
        ],
    }

    findings = build(config, repo_root=tmp_path).collect_findings()
    codes = {finding.code for finding in findings}

    assert {
        "invalid-behaviour-markers",
        "invalid-surface-glob",
        "unmatched-surface-glob",
        "invalid-evidence-claim",
        "invalid-evidence-claim-id",
        "invalid-claimed-surface",
        "missing-claimed-surface",
        "invalid-evidence-test",
        "missing-evidence-test",
        "invalid-evidence-executable",
        "missing-claim-surfaces",
        "missing-claim-tests",
        "missing-claim-executables",
    } <= codes


def test_missing_or_non_sequence_claims_are_reported(tmp_path: Path) -> None:
    no_claims = build(
        {"surface_globs": [], "behaviour_markers": ["e2e"]}, repo_root=tmp_path
    ).collect_findings()
    wrong_shape = build(
        {"surface_globs": [], "behaviour_markers": ["e2e"], "claims": "one claim"}, repo_root=tmp_path
    ).collect_findings()

    assert {finding.code for finding in no_claims} == {
        "missing-evidence-claims",
    }
    assert {finding.code for finding in wrong_shape} == {
        "missing-evidence-claims",
    }


@pytest.mark.parametrize("binary", [False, True])
def test_unreadable_evidence_test_cannot_supply_a_marker(tmp_path: Path, binary: bool) -> None:
    _seed_surfaces(tmp_path)
    path = tmp_path / "tests/integration/test_image_build.py"
    path.parent.mkdir(parents=True, exist_ok=True)
    if binary:
        path.write_bytes(b"def test_broken(): pass\n\xff")
    else:
        path.write_text("def test_broken(:\n", encoding="utf-8")

    findings = build(_config(), repo_root=tmp_path).collect_findings()

    assert {finding.code for finding in findings} == {"missing-behaviour-marker"}


def test_aliased_runner_check_true_and_observed_file_satisfy_claim(tmp_path: Path) -> None:
    _seed_surfaces(tmp_path)
    test_source = """
import pytest
from pathlib import Path as FilePath
from subprocess import run as execute

pytestmark = [pytest.mark.integration]
BUILD = "infra/docker/build-tool-runtime.sh"

def test_image_build():
    result: object = execute([str(BUILD)], check=True)
    assert FilePath(BUILD).is_file()
"""
    _seed(tmp_path, "tests/integration/test_image_build.py", test_source)

    assert build(_config(), repo_root=tmp_path).collect_findings() == ()


def test_unknown_path_suffix_cannot_prove_the_declared_executable(tmp_path: Path) -> None:
    _seed_surfaces(tmp_path)
    test_source = """
import subprocess
from pathlib import Path
import pytest

pytestmark = pytest.mark.integration
BUILD = Path("infra/docker/build-tool-runtime.sh") / runtime_suffix

def test_image_build(tmp_path):
    output = tmp_path / "image.tar"
    result = subprocess.run([str(BUILD), str(output)], capture_output=True)
    assert result.returncode == 0
    assert output.exists()
"""
    _seed(tmp_path, "tests/integration/test_image_build.py", test_source)

    findings = build(_config(), repo_root=tmp_path).collect_findings()

    assert {finding.code for finding in findings} == {"missing-executable-evidence"}


def test_empty_and_unrelated_process_calls_do_not_prove_the_executable(tmp_path: Path) -> None:
    _seed_surfaces(tmp_path)
    test_source = """
import os
import subprocess
import pytest

pytestmark = pytest.mark.integration

def test_image_build():
    subprocess.run()
    subprocess.run([])
    os.system("infra/docker/build-tool-runtime.sh")
"""
    _seed(tmp_path, "tests/integration/test_image_build.py", test_source)

    findings = build(_config(), repo_root=tmp_path).collect_findings()

    assert {finding.code for finding in findings} == {"missing-executable-evidence"}


def test_import_aliases_callable_markers_and_reassigned_paths_are_resolved(tmp_path: Path) -> None:
    _seed_surfaces(tmp_path)
    test_source = """
import subprocess as child
from pathlib import Path
from . import helpers
import pytest

ROOT = Path()
BUILD = "not-the-build-command"
BUILD = "infra/docker/build-tool-runtime.sh"

@pytest.mark.integration()
def test_image_build(tmp_path):
    output = tmp_path / "image.tar"
    result = child.run([str(BUILD), str(output)], capture_output=True)
    assert result.returncode == 0
    assert output.exists()
"""
    _seed(tmp_path, "tests/integration/test_image_build.py", test_source)

    assert build(_config(), repo_root=tmp_path).collect_findings() == ()


def test_empty_configuration_is_vacuous_for_additive_adoption(tmp_path: Path) -> None:
    assert build({}, repo_root=tmp_path).run() == 0


def test_build_returns_rule() -> None:
    assert isinstance(build({}), BehaviouralEvidence)


def test_no_repo_strings_in_executable_code() -> None:
    import tc_fitness.core_checks.behavioural_evidence as mod

    assert_no_repo_identity(mod.__file__)
