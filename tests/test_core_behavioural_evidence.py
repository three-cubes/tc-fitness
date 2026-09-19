"""Behaviour tests for executable evidence claims."""

from __future__ import annotations

from pathlib import Path

import pytest
from _core_check_assertions import assert_no_repo_identity

from tc_fitness.core_checks.behavioural_evidence import BehaviouralEvidence, build


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


@pytest.mark.integration
def test_real_executable_and_observed_artifact_satisfy_claim(tmp_path: Path) -> None:
    _seed_surfaces(tmp_path)
    _seed(tmp_path, "tests/integration/test_image_build.py", _valid_test())

    assert build(_config(), repo_root=tmp_path).collect_findings() == ()


@pytest.mark.integration
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


@pytest.mark.integration
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


@pytest.mark.integration
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


@pytest.mark.integration
def test_process_success_without_observed_output_is_not_evidence(tmp_path: Path) -> None:
    _seed_surfaces(tmp_path)
    _seed(
        tmp_path,
        "tests/integration/test_image_build.py",
        _valid_test().replace("    assert output.exists()\n", ""),
    )

    findings = build(_config(), repo_root=tmp_path).collect_findings()

    assert {finding.code for finding in findings} == {"missing-output-observation"}


@pytest.mark.integration
def test_unrelated_file_assertion_is_not_an_output_observation(tmp_path: Path) -> None:
    _seed_surfaces(tmp_path)
    _seed(
        tmp_path,
        "tests/integration/test_image_build.py",
        _valid_test().replace("assert output.exists()", "assert Path('/unrelated').exists()"),
    )

    findings = build(_config(), repo_root=tmp_path).collect_findings()

    assert {finding.code for finding in findings} == {"missing-output-observation"}


@pytest.mark.integration
def test_every_matched_critical_surface_requires_a_claim(tmp_path: Path) -> None:
    _seed_surfaces(tmp_path)
    _seed(tmp_path, "infra/docker/Dockerfile.other", "FROM scratch\n")
    _seed(tmp_path, "tests/integration/test_image_build.py", _valid_test())

    findings = build(_config(), repo_root=tmp_path).collect_findings()

    assert [(finding.code, finding.source.as_posix()) for finding in findings] == [
        ("unclaimed-critical-surface", "infra/docker/Dockerfile.other")
    ]


@pytest.mark.integration
def test_missing_test_and_surface_fail_instead_of_vacuously_passing(tmp_path: Path) -> None:
    findings = build(_config(test="tests/integration/missing.py"), repo_root=tmp_path).collect_findings()

    assert {finding.code for finding in findings} == {
        "missing-claimed-surface",
        "missing-evidence-test",
        "unmatched-surface-glob",
    }


@pytest.mark.integration
def test_behaviour_marker_is_required_on_evidence_test(tmp_path: Path) -> None:
    _seed_surfaces(tmp_path)
    _seed(
        tmp_path,
        "tests/integration/test_image_build.py",
        _valid_test().replace("pytestmark = pytest.mark.integration\n", ""),
    )

    findings = build(_config(), repo_root=tmp_path).collect_findings()

    assert {finding.code for finding in findings} == {"missing-behaviour-marker"}


@pytest.mark.integration
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


@pytest.mark.integration
def test_empty_configuration_is_vacuous_for_additive_adoption(tmp_path: Path) -> None:
    assert build({}, repo_root=tmp_path).run() == 0


@pytest.mark.integration
def test_findings_are_hard_and_cannot_be_grandfathered(tmp_path: Path) -> None:
    rule = build(_config(), repo_root=tmp_path)

    with pytest.raises(RuntimeError, match="cannot establish a baseline"):
        rule.establish_baseline()


@pytest.mark.integration
def test_build_returns_rule() -> None:
    assert isinstance(build({}), BehaviouralEvidence)


@pytest.mark.integration
def test_no_repo_strings_in_executable_code() -> None:
    import tc_fitness.core_checks.behavioural_evidence as mod

    assert_no_repo_identity(mod.__file__)
