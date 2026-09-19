"""Tests for the CORE check engine_version_floor (SGO-190).

Reads the consuming repo's pinned three-cubes-fitness tag and FAILS when it is
below a centrally-declared floor; a repo with no floor configured — or whose
version cannot be resolved — is a guard-forward no-op.
"""

from __future__ import annotations

from importlib import metadata
from pathlib import Path

import pytest
from _core_check_assertions import assert_no_repo_identity

from tc_fitness.core_checks.engine_version_floor import (
    DEFAULT_PACKAGE,
    EngineVersionFloor,
    build,
    main,
    resolve_declared_version,
)

pytestmark = pytest.mark.integration

PKG = DEFAULT_PACKAGE


def _git_dep(tag: str) -> str:
    return f"{PKG} @ git+https://github.com/three-cubes/tc-fitness.git@{tag}"


def _manifest(tmp_path: Path, body: str) -> Path:
    path = tmp_path / "pyproject.toml"
    path.write_text(body, encoding="utf-8")
    return path


def _project_with_dep(tmp_path: Path, dep: str) -> Path:
    return _manifest(tmp_path, f'[project]\nname = "consumer"\ndependencies = ["{dep}"]\n')


def test_resolve_declared_version_from_git_url(tmp_path: Path) -> None:
    manifest = _project_with_dep(tmp_path, _git_dep("v0.6.1"))
    assert resolve_declared_version(manifest, PKG) == "v0.6.1"


def test_resolve_declared_version_from_pep440_pin(tmp_path: Path) -> None:
    manifest = _project_with_dep(tmp_path, f"{PKG}==0.7.0")
    assert resolve_declared_version(manifest, PKG) == "0.7.0"


def test_resolve_declared_version_from_optional_group(tmp_path: Path) -> None:
    body = (
        '[project]\nname = "consumer"\ndependencies = []\n'
        f'[project.optional-dependencies]\ndev = ["{_git_dep("v0.7.0")}"]\n'
    )
    manifest = _manifest(tmp_path, body)
    assert resolve_declared_version(manifest, PKG) == "v0.7.0"


def test_resolve_declared_version_from_uv_source_tag(tmp_path: Path) -> None:
    body = (
        '[project]\nname = "consumer"\ndependencies = ["three-cubes-fitness"]\n'
        f"[tool.uv.sources]\n{PKG} = {{ git = "
        '"https://github.com/three-cubes/tc-fitness.git", tag = "v0.6.1" }\n'
    )
    manifest = _manifest(tmp_path, body)
    assert resolve_declared_version(manifest, PKG) == "v0.6.1"


def test_resolve_declared_version_absent_is_none(tmp_path: Path) -> None:
    manifest = _manifest(tmp_path, '[project]\nname = "consumer"\ndependencies = []\n')
    assert resolve_declared_version(manifest, PKG) is None


@pytest.mark.parametrize(
    "body",
    [
        "project = 1\n",
        '[project]\nname = "consumer"\ndependencies = [1]\n',
        '[project]\nname = "consumer"\noptional-dependencies = ["invalid-shape"]\n',
        '[project]\nname = "consumer"\n'
        'dependencies = ["other-package @ https://example.invalid/repo@v9.0"]\n',
        '[project]\nname = "consumer"\n'
        'dependencies = ["three-cubes-fitness @ https://example.invalid/repo"]\n',
        '[project]\nname = "consumer"\ndependencies = ["other-package==9.0"]\n',
        '[project]\nname = "consumer"\n'
        'dependencies = ["three-cubes-fitness"]\n'
        '[tool.uv]\nsources = ["invalid-shape"]\n',
        '[project]\nname = "consumer"\n'
        'dependencies = ["three-cubes-fitness"]\n'
        '[tool.uv.sources]\n"other-package" = { tag = "v9.0" }\n',
        '[project]\nname = "consumer"\n'
        'dependencies = ["three-cubes-fitness"]\n'
        '[tool.uv.sources]\n"three-cubes-fitness" = { tag = 9 }\n',
        '[dependency-groups]\ntest = [{ include-group = "dev" }, 7]\n'
        'other = ["other==2"]\ninvalid = { include-group = "dev" }\n',
        "dependency-groups = 1\n",
    ],
)
def test_malformed_or_unrelated_dependency_shapes_do_not_resolve_a_pin(tmp_path: Path, body: str) -> None:
    manifest = _manifest(tmp_path, body)

    assert resolve_declared_version(manifest, PKG) is None


def test_dependency_groups_can_declare_the_pin(tmp_path: Path) -> None:
    manifest = _manifest(tmp_path, '[dependency-groups]\ntest = ["three-cubes-fitness==0.8.0"]\n')

    assert resolve_declared_version(manifest, PKG) == "0.8.0"


def test_multiple_optional_groups_and_dependencies_are_scanned(tmp_path: Path) -> None:
    body = (
        '[project]\nname = "consumer"\n'
        'dependencies = ["unrelated==1"]\n'
        "[project.optional-dependencies]\n"
        'docs = [1, "unrelated==2"]\n'
        'dev = ["unrelated==3", "three-cubes-fitness==0.9.0"]\n'
    )

    assert resolve_declared_version(_manifest(tmp_path, body), PKG) == "0.9.0"


def test_compatible_specifier_reports_its_lower_bound(tmp_path: Path) -> None:
    manifest = _project_with_dep(tmp_path, f"{PKG}~=0.7")

    assert resolve_declared_version(manifest, PKG) == "0.7"


@pytest.mark.parametrize("body", ["tool = 1\n", "tool = { uv = 1 }\n"])
def test_non_mapping_uv_source_shapes_have_no_pin(tmp_path: Path, body: str) -> None:
    manifest = _manifest(tmp_path, body)

    assert resolve_declared_version(manifest, PKG) is None


def test_uv_source_searches_past_other_sources(tmp_path: Path) -> None:
    body = (
        '[project]\nname = "consumer"\ndependencies = ["three-cubes-fitness"]\n'
        "[tool.uv.sources]\n"
        'unrelated = { tag = "v1.0.0" }\n'
        '"three-cubes-fitness" = { tag = "v0.8.0" }\n'
    )

    assert resolve_declared_version(_manifest(tmp_path, body), PKG) == "v0.8.0"


@pytest.mark.parametrize("manifest_text", [None, "[project\n", "\xff"])
def test_missing_malformed_or_non_utf8_manifest_is_unresolved(
    tmp_path: Path, manifest_text: str | None
) -> None:
    path = tmp_path / "pyproject.toml"
    if manifest_text is not None:
        path.write_bytes(manifest_text.encode("utf-8", errors="surrogateescape"))

    assert resolve_declared_version(path, PKG) is None


def test_version_floor_no_file_surface(tmp_path: Path) -> None:
    rule = build({"floor": "v0.1.0"}, repo_root=tmp_path)

    assert rule.enumerate_files() == []
    assert rule.file_has_violation(tmp_path / "pyproject.toml") is False


@pytest.mark.parametrize("floor, pin", [("release", "v0.1.0"), ("v0.8.0", "preview")])
def test_unparseable_floor_or_pin_is_a_noop(tmp_path: Path, floor: str, pin: str) -> None:
    _project_with_dep(tmp_path, _git_dep(pin))
    rule = build({"floor": floor}, repo_root=tmp_path)

    assert rule.collect_violations() == set()


def test_below_floor_fails(tmp_path: Path) -> None:
    _project_with_dep(tmp_path, _git_dep("v0.6.1"))
    rule = build({"floor": "v0.7.0"}, repo_root=tmp_path)
    violations = rule.collect_violations()
    assert len(violations) == 1
    assert rule.run() == 1


def test_at_floor_passes(tmp_path: Path) -> None:
    _project_with_dep(tmp_path, _git_dep("v0.7.0"))
    rule = build({"floor": "v0.7.0"}, repo_root=tmp_path)
    assert rule.collect_violations() == set()
    assert rule.run() == 0


def test_above_floor_passes(tmp_path: Path) -> None:
    _project_with_dep(tmp_path, _git_dep("v0.8.0"))
    rule = build({"floor": "v0.7.0"}, repo_root=tmp_path)
    assert rule.run() == 0


def test_no_floor_configured_is_noop(tmp_path: Path) -> None:
    _project_with_dep(tmp_path, _git_dep("v0.1.0"))
    rule = build({}, repo_root=tmp_path)
    assert rule.collect_violations() == set()
    assert rule.run() == 0


def test_unresolvable_version_is_noop(tmp_path: Path) -> None:
    # Manifest exists but declares no such dependency, and the package is not
    # installed → the version cannot be resolved → guard-forward no-op.
    _manifest(tmp_path, '[project]\nname = "consumer"\ndependencies = []\n')
    rule = build({"floor": "v9.9.9", "package": "tc-fitness-not-installed"}, repo_root=tmp_path)
    assert rule.collect_violations() == set()
    assert rule.run() == 0


def test_falls_back_to_installed_metadata(tmp_path: Path) -> None:
    # No declared pin in the manifest → resolve_version() uses the installed
    # distribution's own metadata version.
    _manifest(tmp_path, '[project]\nname = "consumer"\ndependencies = []\n')
    rule = build({"floor": "v0.1.0"}, repo_root=tmp_path)
    assert rule.resolve_version() == metadata.version(PKG)


def test_declared_pin_takes_priority_over_installed(tmp_path: Path) -> None:
    _project_with_dep(tmp_path, _git_dep("v0.6.1"))
    rule = build({"floor": "v0.7.0"}, repo_root=tmp_path)
    assert rule.resolve_version() == "v0.6.1"


def test_main_no_config_is_noop(tmp_path: Path) -> None:
    _project_with_dep(tmp_path, _git_dep("v0.1.0"))
    # main() injects no config block, so with no floor it is a no-op pass.
    assert main(["--repo-root", str(tmp_path)]) == 0


def test_build_and_main_are_exposed(tmp_path: Path) -> None:
    assert callable(build)
    assert callable(main)
    assert isinstance(build({}, repo_root=tmp_path), EngineVersionFloor)
    assert EngineVersionFloor.name == "engine-version-floor"


def test_no_repo_strings_in_executable_code() -> None:
    import tc_fitness.core_checks.engine_version_floor as mod

    assert_no_repo_identity(mod.__file__)
