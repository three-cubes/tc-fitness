"""Tests for the CORE check no_duplicated_dependency_pin."""

from __future__ import annotations

from pathlib import Path

from tc_fitness.core_checks.no_duplicated_dependency_pin import (
    REMEDIATION,
    NoDuplicatedDependencyPin,
    build,
    declared_exact_pins,
    restated_pins,
)

_MANIFEST = """
[project]
name = "demo"
dependencies = ["mutmut==3.6.0", "requests>=2.0"]

[project.optional-dependencies]
dev = ["ruff==0.15.18"]

[dependency-groups]
test = ["pytest==8.4.1"]
"""


def _repo(tmp_path: Path, manifest: str = _MANIFEST) -> Path:
    (tmp_path / "pyproject.toml").write_text(manifest, encoding="utf-8")
    (tmp_path / "src").mkdir(exist_ok=True)
    return tmp_path


def _rule(root: Path, **config: object) -> NoDuplicatedDependencyPin:
    return build({"roots": ["src"], **config}, repo_root=root)


# -- reading the declarations ------------------------------------------------


def test_pins_are_read_from_every_declaration_site(tmp_path: Path) -> None:
    """A pin binds the same whichever table declares it."""
    pins = declared_exact_pins(_repo(tmp_path) / "pyproject.toml")
    assert pins == {"3.6.0": ["mutmut"], "0.15.18": ["ruff"], "8.4.1": ["pytest"]}


def test_a_uv_override_is_a_pin(tmp_path: Path) -> None:
    """An override is often exactly where a transitive version gets fixed.

    Reading only ``[project]`` misses it while the source restating it looks
    clean — the gap that let asteval==1.0.9 through an earlier scan.
    """
    manifest = (
        '[project]\nname = "d"\ndependencies = []\n\n[tool.uv]\noverride-dependencies = ["asteval==1.0.9"]\n'
    )
    root = _repo(tmp_path, manifest)
    assert declared_exact_pins(root / "pyproject.toml") == {"1.0.9": ["asteval"]}


def test_a_uv_constraint_is_a_pin(tmp_path: Path) -> None:
    manifest = (
        '[project]\nname = "d"\ndependencies = []\n\n[tool.uv]\nconstraint-dependencies = ["thing==4.5.6"]\n'
    )
    root = _repo(tmp_path, manifest)
    assert declared_exact_pins(root / "pyproject.toml") == {"4.5.6": ["thing"]}


def test_a_build_requirement_is_a_pin(tmp_path: Path) -> None:
    manifest = '[build-system]\nrequires = ["hatchling==1.27.0"]\n\n[project]\nname = "d"\n'
    root = _repo(tmp_path, manifest)
    assert declared_exact_pins(root / "pyproject.toml") == {"1.27.0": ["hatchling"]}


def test_a_range_specifier_is_not_a_pin(tmp_path: Path) -> None:
    root = _repo(tmp_path, '[project]\nname = "d"\ndependencies = ["requests>=2.31.0"]\n')
    assert declared_exact_pins(root / "pyproject.toml") == {}


def test_two_component_versions_are_ignored_by_default(tmp_path: Path) -> None:
    """ "1.0" collides with ordinary numeric strings too often to be worth flagging."""
    root = _repo(tmp_path, '[project]\nname = "d"\ndependencies = ["thing==1.0"]\n')
    assert declared_exact_pins(root / "pyproject.toml") == {}


def test_an_unreadable_manifest_yields_no_pins(tmp_path: Path) -> None:
    """Vacuous beats noisy: a repo whose manifest cannot be parsed is not an offender."""
    (tmp_path / "pyproject.toml").write_text("this is not = valid toml [[", encoding="utf-8")
    assert declared_exact_pins(tmp_path / "pyproject.toml") == {}


def test_a_missing_manifest_yields_no_pins(tmp_path: Path) -> None:
    assert declared_exact_pins(tmp_path / "absent.toml") == {}


# -- spotting the restatement ------------------------------------------------


def test_a_literal_restating_a_pin_is_found() -> None:
    assert restated_pins('TOOL_VERSION = "3.6.0"\n', {"3.6.0": ["mutmut"]}) == [(1, "3.6.0")]


def test_a_version_the_project_does_not_pin_is_ignored() -> None:
    assert restated_pins('SCHEMA_VERSION = "9.9.9"\n', {"3.6.0": ["mutmut"]}) == []


def test_a_commented_version_is_documentation_not_a_binding() -> None:
    assert restated_pins('# pinned at "3.6.0" upstream\n', {"3.6.0": ["mutmut"]}) == []


# -- the rule end to end -----------------------------------------------------


def test_source_restating_a_pin_violates(tmp_path: Path) -> None:
    root = _repo(tmp_path)
    (root / "src" / "assurance.py").write_text('TOOL_VERSION = "3.6.0"\n', encoding="utf-8")
    assert _rule(root).collect_violations() == {Path("src/assurance.py")}


def test_deriving_the_version_instead_passes(tmp_path: Path) -> None:
    """The remediation the check recommends must actually clear it."""
    root = _repo(tmp_path)
    (root / "src" / "assurance.py").write_text(
        "from importlib.metadata import requires\n\nTOOL_VERSION = _pinned(requires('demo'), 'mutmut')\n",
        encoding="utf-8",
    )
    assert _rule(root).collect_violations() == set()


def test_a_shell_script_restating_a_pin_violates(tmp_path: Path) -> None:
    """Shell is in scope by default.

    A qualification script asserting an installed version is the same second
    source of truth as a Python constant, and scoping the rule to .py alone
    would let the pattern live on in exactly the scripts that enforce it
    hardest.
    """
    root = _repo(tmp_path)
    (root / "src" / "qualify.sh").write_text('assert version("mutmut") == "3.6.0"\n', encoding="utf-8")
    assert _rule(root).collect_violations() == {Path("src/qualify.sh")}


def test_a_repo_declaring_no_exact_pins_is_vacuous(tmp_path: Path) -> None:
    """Adopting the check must not fail a repo that pins nothing exactly."""
    root = _repo(tmp_path, '[project]\nname = "d"\ndependencies = ["requests>=2.0"]\n')
    (root / "src" / "a.py").write_text('X = "3.6.0"\n', encoding="utf-8")
    assert _rule(root).collect_violations() == set()


def test_the_manifest_itself_is_never_its_own_offender(tmp_path: Path) -> None:
    """pyproject.toml declaring the pin is the source of truth, not a restatement."""
    root = _repo(tmp_path)
    rule = _rule(root, roots=["."], extensions=[".toml"])
    assert not rule.file_has_violation(root / "pyproject.toml")


def test_the_remediation_never_directs_an_agent_to_suppress() -> None:
    """The tuning knob is specificity, not an exemption list.

    A gate whose documented remedy is "suppress this file" teaches the habit
    the engine is removing, and would stop working the moment per-file
    exemptions go. min_version_parts raises the bar on what counts as a
    version instead, which is a statement about the rule rather than a hole
    punched in it.
    """
    assert "min_version_parts" in REMEDIATION
    assert "exempt" not in REMEDIATION.lower()


def test_min_version_parts_is_configurable(tmp_path: Path) -> None:
    """A consumer that wants two-component pins caught can ask for them."""
    root = _repo(tmp_path, '[project]\nname = "d"\ndependencies = ["thing==1.0"]\n')
    (root / "src" / "a.py").write_text('X = "1.0"\n', encoding="utf-8")
    assert _rule(root).collect_violations() == set()
    assert _rule(root, min_version_parts=2).collect_violations() == {Path("src/a.py")}


def test_a_pin_carrying_extras_is_still_a_declared_pin(tmp_path: Path) -> None:
    """Extras select optional dependencies; they do not change the pinned version."""
    manifest = tmp_path / "pyproject.toml"
    manifest.write_text(
        '[project]\nname = "x"\ndependencies = ["uvicorn[standard]==0.30.0"]\n', encoding="utf-8"
    )

    assert declared_exact_pins(manifest) == {"0.30.0": ["uvicorn"]}


def test_a_prerelease_or_post_release_literal_is_detected() -> None:
    """PEP 440 admits more than dotted digits, and a restated qualifier binds just as hard."""
    for version in ("1.2.3rc1", "1.2.3.post1", "1.2.3+local.1"):
        assert restated_pins(f'TOOL = "{version}"\n', {version: ["tool"]}) == [(1, version)]


def test_an_unquoted_shell_assignment_is_detected() -> None:
    """A shell binding carries no quotes, and shell is in scope by default."""
    assert restated_pins("TOOL_VERSION=3.6.0\n", {"3.6.0": ["mutmut"]}) == [(1, "3.6.0")]
    assert restated_pins('[[ "$actual" == 3.6.0 ]]\n', {"3.6.0": ["mutmut"]}) == [(1, "3.6.0")]


def test_a_version_named_in_a_trailing_comment_is_documentation() -> None:
    """The rule excludes prose; where the prose starts on the line does not change that."""
    assert restated_pins('timeout = 10  # tool currently emits "3.6.0"\n', {"3.6.0": ["m"]}) == []


def test_a_longer_version_is_not_a_restatement_of_a_shorter_one() -> None:
    """Matching declared strings must still respect token boundaries."""
    assert restated_pins('TOOL = "1.2.30"\n', {"1.2.3": ["tool"]}) == []


def test_a_parenthesised_pin_is_declared(tmp_path: Path) -> None:
    """`foo (==1.2.3)` is valid PEP 508 and pins the same version."""
    manifest = tmp_path / "pyproject.toml"
    manifest.write_text('[project]\nname = "x"\ndependencies = ["foo (==1.2.3)"]\n', encoding="utf-8")

    assert declared_exact_pins(manifest) == {"1.2.3": ["foo"]}


def test_a_v_prefixed_pin_matches_either_spelling(tmp_path: Path) -> None:
    """PEP 440 normalises `v1.2.3` to `1.2.3`; a literal may use either."""
    manifest = tmp_path / "pyproject.toml"
    manifest.write_text('[project]\nname = "x"\ndependencies = ["foo==v1.2.3"]\n', encoding="utf-8")

    assert declared_exact_pins(manifest) == {"1.2.3": ["foo"], "v1.2.3": ["foo"]}


def test_a_wildcard_pin_is_not_a_pin(tmp_path: Path) -> None:
    """`foo==1.2.*` admits every 1.2 release, so no literal restates it."""
    manifest = tmp_path / "pyproject.toml"
    manifest.write_text('[project]\nname = "x"\ndependencies = ["foo==1.2.*"]\n', encoding="utf-8")

    assert declared_exact_pins(manifest) == {}


def test_a_direct_reference_url_declares_no_pin(tmp_path: Path) -> None:
    """An `==` inside a URL query string is not an equality specifier."""
    manifest = tmp_path / "pyproject.toml"
    manifest.write_text(
        '[project]\nname = "x"\ndependencies = ["foo @ https://e.invalid/f.whl?build==1.2.3"]\n',
        encoding="utf-8",
    )

    assert declared_exact_pins(manifest) == {}


def test_uvs_legacy_dev_dependency_table_declares_pins(tmp_path: Path) -> None:
    """uv still accepts dev-dependencies, so a pin there binds like any other."""
    manifest = tmp_path / "pyproject.toml"
    manifest.write_text(
        '[project]\nname = "x"\n[tool.uv]\ndev-dependencies = ["pytest==8.4.1"]\n', encoding="utf-8"
    )

    assert declared_exact_pins(manifest) == {"8.4.1": ["pytest"]}


def test_a_release_qualifier_is_not_a_restatement_of_the_release(tmp_path: Path) -> None:
    """`1.2.3rc1` is a different version, not the declared `1.2.3` restated."""
    for longer in ("1.2.3rc1", "1.2.3.post1", "1.2.3dev1", "x1.2.3y"):
        assert restated_pins(f'TOOL = "{longer}"\n', {"1.2.3": ["tool"]}) == []


def test_a_shell_parameter_expansion_is_not_a_comment() -> None:
    """`${value#prefix}` is expansion; truncating there would hide the pin after it."""
    line = "trimmed=${value#prefix}; EXPECTED=3.6.0\n"

    assert restated_pins(line, {"3.6.0": ["mutmut"]}) == [(1, "3.6.0")]


def test_an_extensionless_shell_entrypoint_is_scanned(tmp_path: Path) -> None:
    """A shell script without a suffix is where a restated pin hides best."""
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "x"\ndependencies = ["mutmut==3.6.0"]\n', encoding="utf-8"
    )
    script = tmp_path / "scripts" / "check-version"
    script.parent.mkdir()
    script.write_text("#!/usr/bin/env bash\nEXPECTED=3.6.0\n", encoding="utf-8")
    rule = build({"roots": ["scripts"]}, repo_root=tmp_path)

    assert script in rule.enumerate_files()
    assert rule.file_has_violation(script)
