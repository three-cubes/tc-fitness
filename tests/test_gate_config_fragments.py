"""Layer-owned gate configuration: ``include`` fragments (v0.21.0).

A repo root config names TOML fragments with ``include``; each fragment holds
``[[steps]]`` and ``[core_checks.<module>]`` tables for the part of the repo it
lives in. These tests drive the real loaders (:func:`load_config`,
:func:`load_core_check_configs`) and the real ``tc-fitness run`` gate over
fragment files on disk, and pin:

- merge order: root steps first, then fragments in sorted path order;
- each step records the file that declared it, and a failing step names it;
- a step id declared twice (root or fragment) is an error naming both files;
- ``core_checks`` lists union in order with duplicates dropped; a scalar that
  disagrees across files is an error, an equal repeat is fine;
- a fragment may not set ``include``, the gate settings, or unknown keys;
- an absolute or escaping pattern is an error, an empty glob is allowed;
- fragment step paths stay repo-root-relative;
- a CORE check scoped only in a fragment bites through the real gate.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

from tc_fitness.gate import run_gate
from tc_fitness.gate_config import (
    GateConfigError,
    load_config,
    load_core_check_configs,
    parse_config,
)

pytestmark = pytest.mark.integration

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def _plain(text: str) -> str:
    return _ANSI_RE.sub("", text)


def _root(repo: Path, include: list[str], body: str = "") -> None:
    """Write a pyproject root config with ``include`` and an optional extra body."""
    patterns = ", ".join(f'"{p}"' for p in include)
    (repo / "pyproject.toml").write_text(
        "[project]\nname = 'consumer'\nversion = '0.0.0'\n\n"
        f'[tool.tc_fitness]\nname = "layered gate"\ninclude = [{patterns}]\n\n'
        '[[tool.tc_fitness.steps]]\nid = "root-step"\nrun = ["true"]\n' + body
    )


def _fragment(repo: Path, rel: str, body: str) -> None:
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body)


def _step(step_id: str, extra: str = "") -> str:
    return f'[[steps]]\nid = "{step_id}"\nrun = ["true"]\n{extra}'


@pytest.fixture(autouse=True)
def _clean_sys_modules() -> object:
    before = set(sys.modules)
    yield
    for name in set(sys.modules) - before:
        if name.startswith(("scripts", "frag_core_cat")):
            del sys.modules[name]


# --------------------------------------------------------------------------- #
# steps: merge order, provenance, duplicates
# --------------------------------------------------------------------------- #


def test_fragment_steps_follow_root_steps_in_sorted_fragment_order(tmp_path: Path) -> None:
    _root(tmp_path, ["*/fitness.toml"])
    _fragment(tmp_path, "zeta/fitness.toml", _step("zeta-step"))
    _fragment(tmp_path, "alpha/fitness.toml", _step("alpha-one") + _step("alpha-two"))

    cfg = load_config(tmp_path)

    assert [s.id for s in cfg.steps] == ["root-step", "alpha-one", "alpha-two", "zeta-step"]
    assert [s.source for s in cfg.steps] == [
        Path("pyproject.toml"),
        Path("alpha/fitness.toml"),
        Path("alpha/fitness.toml"),
        Path("zeta/fitness.toml"),
    ]
    assert cfg.fragments == (Path("alpha/fitness.toml"), Path("zeta/fitness.toml"))
    assert cfg.name == "layered gate"


def test_a_fragment_matched_by_two_patterns_is_merged_once(tmp_path: Path) -> None:
    _root(tmp_path, ["alpha/fitness.toml", "*/fitness.toml", "**/fitness.toml"])
    _fragment(tmp_path, "alpha/fitness.toml", _step("alpha-step"))

    cfg = load_config(tmp_path)

    assert [s.id for s in cfg.steps] == ["root-step", "alpha-step"]


def test_recursive_pattern_finds_nested_fragments(tmp_path: Path) -> None:
    _root(tmp_path, ["**/fitness.toml"])
    _fragment(tmp_path, "layer/deep/er/fitness.toml", _step("deep-step"))

    cfg = load_config(tmp_path)

    assert [s.id for s in cfg.steps] == ["root-step", "deep-step"]


def test_root_without_include_records_the_root_file_on_every_step(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        '[tool.tc_fitness]\n[[tool.tc_fitness.steps]]\nid = "only"\nrun = ["true"]\n'
    )

    cfg = load_config(tmp_path)

    assert [s.source for s in cfg.steps] == [Path("pyproject.toml")]
    assert cfg.fragments == ()


def test_a_step_id_in_root_and_fragment_is_rejected_naming_both(tmp_path: Path) -> None:
    _root(tmp_path, ["capabilities/fitness.toml"])
    _fragment(tmp_path, "capabilities/fitness.toml", _step("root-step"))

    with pytest.raises(GateConfigError) as exc:
        load_config(tmp_path)

    msg = str(exc.value)
    assert "'root-step' in pyproject.toml and capabilities/fitness.toml" in msg
    assert "fix:" in msg and "next:" in msg


def test_a_step_id_in_two_fragments_is_rejected_naming_both(tmp_path: Path) -> None:
    _root(tmp_path, ["*/fitness.toml"])
    _fragment(tmp_path, "agents/fitness.toml", _step("shared"))
    _fragment(tmp_path, "capabilities/fitness.toml", _step("shared"))

    with pytest.raises(GateConfigError) as exc:
        load_config(tmp_path)

    assert "'shared' in agents/fitness.toml and capabilities/fitness.toml" in str(exc.value)


def test_fragment_only_steps_satisfy_the_non_empty_rule(tmp_path: Path) -> None:
    (tmp_path / ".tc-fitness.toml").write_text('include = ["layer/fitness.toml"]\n')
    _fragment(tmp_path, "layer/fitness.toml", _step("layer-step"))

    cfg = load_config(tmp_path)

    assert [(s.id, s.source) for s in cfg.steps] == [("layer-step", Path("layer/fitness.toml"))]


def test_stage_dependencies_resolve_across_files(tmp_path: Path) -> None:
    _root(tmp_path, ["layer/fitness.toml"], 'stage = "static"\n')
    _fragment(
        tmp_path, "layer/fitness.toml", _step("layer-test", 'stage = "test"\ndepends_on = ["static"]\n')
    )

    cfg = load_config(tmp_path)

    assert cfg.steps[1].depends_on == ("static",)


# --------------------------------------------------------------------------- #
# core_checks merge
# --------------------------------------------------------------------------- #


def test_core_check_lists_union_in_order_and_drop_duplicates(tmp_path: Path) -> None:
    _root(
        tmp_path,
        ["*/fitness.toml"],
        '[tool.tc_fitness.core_checks.no_internal_patches]\nroots = ["tests", "shared"]\n',
    )
    _fragment(
        tmp_path,
        "zeta/fitness.toml",
        '[core_checks.no_internal_patches]\nroots = ["zeta/tests", "shared"]\n',
    )
    _fragment(
        tmp_path,
        "alpha/fitness.toml",
        '[core_checks.no_internal_patches]\nroots = ["alpha/tests", "tests"]\ninternal_roots = ["alpha_pkg"]\n'
        '[core_checks.test_skip_rationale]\nroots = ["alpha/tests"]\n',
    )

    configs = load_core_check_configs(tmp_path)

    assert configs["no_internal_patches"] == {
        "roots": ["tests", "shared", "alpha/tests", "zeta/tests"],
        "internal_roots": ["alpha_pkg"],
    }
    assert configs["test_skip_rationale"] == {"roots": ["alpha/tests"]}


def test_an_equal_scalar_repeated_across_files_is_accepted(tmp_path: Path) -> None:
    _root(
        tmp_path,
        ["layer/fitness.toml"],
        "[tool.tc_fitness.core_checks.new_code_coverage]\nfloor_pct = 100.0\n",
    )
    _fragment(
        tmp_path,
        "layer/fitness.toml",
        '[core_checks.new_code_coverage]\nfloor_pct = 100.0\nroots = ["layer"]\n',
    )

    assert load_core_check_configs(tmp_path)["new_code_coverage"] == {"floor_pct": 100.0, "roots": ["layer"]}


def test_a_conflicting_scalar_is_rejected_naming_both_files(tmp_path: Path) -> None:
    _root(
        tmp_path,
        ["layer/fitness.toml"],
        "[tool.tc_fitness.core_checks.new_code_coverage]\nfloor_pct = 100.0\n",
    )
    _fragment(tmp_path, "layer/fitness.toml", "[core_checks.new_code_coverage]\nfloor_pct = 80.0\n")

    for loader in (load_core_check_configs, load_config):
        with pytest.raises(GateConfigError) as exc:
            loader(tmp_path)
        msg = str(exc.value)
        assert "core_checks.new_code_coverage.floor_pct" in msg
        assert "pyproject.toml" in msg and "layer/fitness.toml" in msg
        assert "fix:" in msg and "next:" in msg


def test_a_list_against_a_scalar_is_a_conflict(tmp_path: Path) -> None:
    _root(tmp_path, ["layer/fitness.toml"], '[tool.tc_fitness.core_checks.x]\nroots = "src"\n')
    _fragment(tmp_path, "layer/fitness.toml", '[core_checks.x]\nroots = ["layer"]\n')

    with pytest.raises(GateConfigError, match=r"core_checks\.x\.roots"):
        load_core_check_configs(tmp_path)


def test_a_fragment_core_check_block_must_be_a_table(tmp_path: Path) -> None:
    _root(tmp_path, ["layer/fitness.toml"])
    _fragment(tmp_path, "layer/fitness.toml", 'core_checks = { x = "nope" }\n')

    with pytest.raises(GateConfigError, match="fix:"):
        load_core_check_configs(tmp_path)


# --------------------------------------------------------------------------- #
# what a fragment may hold
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("key", ["include", "name", "fail_fast", "max_workers"])
def test_a_fragment_may_not_set_root_only_keys(tmp_path: Path, key: str) -> None:
    value = {"include": '["x.toml"]', "name": '"x"', "fail_fast": "true", "max_workers": "2"}[key]
    _root(tmp_path, ["layer/fitness.toml"])
    _fragment(tmp_path, "layer/fitness.toml", f"{key} = {value}\n" + _step("layer-step"))

    with pytest.raises(GateConfigError) as exc:
        load_config(tmp_path)

    msg = str(exc.value)
    assert f"layer/fitness.toml declares `{key}`" in msg
    assert "only the root config may set" in msg
    assert "fix:" in msg and "next:" in msg


def test_a_fragment_written_with_the_pyproject_prefix_is_rejected(tmp_path: Path) -> None:
    _root(tmp_path, ["layer/fitness.toml"])
    _fragment(tmp_path, "layer/fitness.toml", '[[tool.tc_fitness.steps]]\nid = "x"\nrun = ["true"]\n')

    with pytest.raises(GateConfigError) as exc:
        load_config(tmp_path)

    assert "unknown key `tool`" in str(exc.value)
    assert "without a [tool.tc_fitness] prefix" in str(exc.value)


def test_fragment_steps_must_be_an_array(tmp_path: Path) -> None:
    _root(tmp_path, ["layer/fitness.toml"])
    _fragment(tmp_path, "layer/fitness.toml", 'steps = "nope"\n')

    with pytest.raises(GateConfigError, match="array of tables"):
        load_config(tmp_path)


def test_root_steps_must_be_an_array_when_fragments_are_included(tmp_path: Path) -> None:
    (tmp_path / ".tc-fitness.toml").write_text('include = ["layer/fitness.toml"]\nsteps = "nope"\n')
    _fragment(tmp_path, "layer/fitness.toml", _step("layer-step"))

    with pytest.raises(GateConfigError, match="array of tables"):
        load_config(tmp_path)


def test_a_malformed_fragment_is_actionable(tmp_path: Path) -> None:
    _root(tmp_path, ["layer/fitness.toml"])
    _fragment(tmp_path, "layer/fitness.toml", "[[steps]\n")

    with pytest.raises(GateConfigError) as exc:
        load_config(tmp_path)

    assert "could not parse gate fragment layer/fitness.toml" in str(exc.value)


def test_a_bad_fragment_step_names_the_fragment(tmp_path: Path) -> None:
    _root(tmp_path, ["layer/fitness.toml"])
    _fragment(tmp_path, "layer/fitness.toml", '[[steps]]\nid = "x"\n')

    with pytest.raises(GateConfigError, match="EXACTLY ONE of run / shell / catalogue"):
        load_config(tmp_path)


def test_parse_config_refuses_an_unresolved_include(tmp_path: Path) -> None:
    with pytest.raises(GateConfigError, match="load_config"):
        parse_config({"include": ["x.toml"], "steps": [{"id": "a", "run": ["true"]}]}, source=tmp_path / "x")


# --------------------------------------------------------------------------- #
# include patterns
# --------------------------------------------------------------------------- #


def test_a_pattern_that_matches_nothing_is_allowed(tmp_path: Path) -> None:
    _root(tmp_path, ["agents/fitness.toml", "nowhere/**/fitness.toml"])

    cfg = load_config(tmp_path)

    assert [s.id for s in cfg.steps] == ["root-step"]
    assert cfg.fragments == ()


def test_a_directory_named_like_a_fragment_is_ignored(tmp_path: Path) -> None:
    _root(tmp_path, ["*/fitness.toml"])
    (tmp_path / "layer" / "fitness.toml").mkdir(parents=True)

    assert load_config(tmp_path).fragments == ()


@pytest.mark.parametrize(
    "pattern",
    ["/etc/fitness.toml", "../sibling/fitness.toml", "layer/../../fitness.toml", "C:/fitness.toml", ""],
)
def test_an_absolute_or_escaping_pattern_is_rejected(tmp_path: Path, pattern: str) -> None:
    _root(tmp_path, [pattern])

    with pytest.raises(GateConfigError) as exc:
        load_config(tmp_path)

    msg = str(exc.value)
    assert "`include` pattern" in msg
    assert "fix:" in msg and "next:" in msg


def test_a_match_that_links_outside_the_repo_is_rejected(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    outside = tmp_path / "outside.toml"
    outside.write_text(_step("outside-step"))
    (repo / "layer").mkdir()
    (repo / "layer" / "fitness.toml").symlink_to(outside)
    _root(repo, ["layer/fitness.toml"])

    with pytest.raises(GateConfigError, match="resolves outside the repository"):
        load_config(repo)


def test_include_must_be_a_list_of_strings(tmp_path: Path) -> None:
    (tmp_path / ".tc-fitness.toml").write_text('include = "layer/fitness.toml"\n' + _step("a"))

    with pytest.raises(GateConfigError, match="list of glob patterns"):
        load_config(tmp_path)


# --------------------------------------------------------------------------- #
# through the real gate
# --------------------------------------------------------------------------- #


def test_fragment_step_paths_are_repo_root_relative(tmp_path: Path) -> None:
    _root(tmp_path, ["layer/fitness.toml"])
    _fragment(
        tmp_path,
        "layer/fitness.toml",
        '[[steps]]\nid = "writes"\ncwd = "out"\n'
        f'run = ["{sys.executable}", "-c", "import pathlib; pathlib.Path(\'marker\').write_text(\'x\')"]\n',
    )
    (tmp_path / "out").mkdir()

    outcome = run_gate(load_config(tmp_path), tmp_path)

    assert outcome.ok
    assert (tmp_path / "out" / "marker").is_file()
    assert not (tmp_path / "layer" / "out").exists()


def test_a_failing_fragment_step_names_its_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    _root(tmp_path, ["layer/fitness.toml"])
    _fragment(
        tmp_path, "layer/fitness.toml", '[[steps]]\nid = "bad"\nrun = ["false"]\nfix = "stop failing"\n'
    )

    outcome = run_gate(load_config(tmp_path), tmp_path)
    out = _plain(capsys.readouterr().out)

    assert outcome.gating_failures == ["bad"]
    assert "(fragments: layer/fitness.toml)" in out
    assert "fix: stop failing" in out
    assert "declared in: layer/fitness.toml" in out


def test_a_malformed_fragment_step_is_attributed_to_its_fragment(tmp_path: Path) -> None:
    _root(tmp_path, ["layer/fitness.toml"])
    _fragment(tmp_path, "layer/fitness.toml", '[[steps]]\nrun = ["true"]\n')

    with pytest.raises(GateConfigError, match=r"in layer/fitness\.toml is missing a string `id`"):
        load_config(tmp_path)


def test_a_fragment_change_runs_the_steps_it_declares(tmp_path: Path) -> None:
    _root(tmp_path, ["layer/fitness.toml"])
    _fragment(
        tmp_path, "layer/fitness.toml", '[[steps]]\nid = "scoped"\npaths = ["src/*"]\nrun = ["false"]\n'
    )

    outcome = run_gate(load_config(tmp_path), tmp_path, affected_files=["layer/fitness.toml"])

    assert outcome.gating_failures == ["scoped"]


def test_a_fragment_that_is_not_utf8_is_a_config_error(tmp_path: Path) -> None:
    _root(tmp_path, ["layer/fitness.toml"])
    (tmp_path / "layer").mkdir()
    (tmp_path / "layer" / "fitness.toml").write_bytes(b"\xff\xfe[[steps]]\n")

    with pytest.raises(GateConfigError, match="could not parse gate fragment"):
        load_config(tmp_path)


def test_command_lists_declared_twice_must_agree(tmp_path: Path) -> None:
    """Unioning two ordered commands would run a third that neither file declared."""
    _root(
        tmp_path,
        ["*/fitness.toml"],
        '[tool.tc_fitness.core_checks.deterministic_tests]\ntest_command = ["uv", "run", "pytest"]\n',
    )
    _fragment(
        tmp_path,
        "alpha/fitness.toml",
        '[core_checks.deterministic_tests]\ntest_command = ["python", "-m", "pytest"]\n',
    )

    with pytest.raises(GateConfigError, match=r"core_checks\.deterministic_tests\.test_command"):
        load_core_check_configs(tmp_path)


_CATALOGUE_SRC = (
    "from tc_fitness.catalogue import RuleEntry\n"
    "ALL_ENTRIES = (\n"
    "    RuleEntry(id='no-duplicate-string', gate='no-duplicate-string',\n"
    "              check='core:no_duplicate_string', category='maintainability',\n"
    "              summary='No string literal duplicated 3+ times in one module.'),\n"
    ")\n"
)

_DUP = 'def a():\n    raise ValueError("the very same long message")\n' * 3


@pytest.mark.parametrize(("fragment_scopes_src", "expected_ok"), [(True, False), (False, True)])
def test_a_core_check_scoped_in_a_fragment_bites_through_the_gate(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], fragment_scopes_src: bool, expected_ok: bool
) -> None:
    checks = tmp_path / "scripts" / "checks"
    checks.mkdir(parents=True)
    (tmp_path / "scripts" / "__init__.py").write_text("")
    (checks / "__init__.py").write_text("")
    (checks / "frag_core_cat.py").write_text(_CATALOGUE_SRC)
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "dup.py").write_text(_DUP)
    (tmp_path / "pyproject.toml").write_text(
        '[tool.tc_fitness]\ninclude = ["src/fitness.toml"]\n'
        '[[tool.tc_fitness.steps]]\nid = "rules"\n'
        'catalogue = "scripts.checks.frag_core_cat:ALL_ENTRIES"\nchecks_dir = "scripts/checks"\n'
    )
    if fragment_scopes_src:
        _fragment(
            tmp_path,
            "src/fitness.toml",
            '[core_checks.no_duplicate_string]\nroots = ["src"]\nextensions = [".py"]\nmin_occurrences = 3\n',
        )
    sys.path.insert(0, str(tmp_path))
    try:
        outcome = run_gate(load_config(tmp_path), tmp_path)
    finally:
        sys.path.remove(str(tmp_path))
    out = _plain(capsys.readouterr().out)

    assert outcome.ok is expected_ok
    assert ("src/dup.py" in out) is not expected_ok
