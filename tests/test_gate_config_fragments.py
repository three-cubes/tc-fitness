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


_CATALOGUE_STEP = (
    '[[tool.tc_fitness.steps]]\nid = "catalogue"\ncatalogue = "frag_core_cat_missing:ENTRIES"\n'
    'paths = ["src/*"]\n'
)


def test_a_fragment_change_runs_every_catalogue_step(tmp_path: Path) -> None:
    """A catalogue step reads every fragment's core_checks, so a fragment can change what it checks."""
    _root(tmp_path, ["layer/fitness.toml"], _CATALOGUE_STEP)
    _fragment(tmp_path, "layer/fitness.toml", "[core_checks.no_bare_except]\nroots = ['layer']\n")

    outcome = run_gate(load_config(tmp_path), tmp_path, affected_files=["layer/fitness.toml"])

    assert outcome.gating_failures == ["catalogue"]


def test_a_deleted_fragment_still_runs_every_catalogue_step(tmp_path: Path) -> None:
    """A fragment the change deleted no longer resolves, but its include pattern still names it."""
    _root(tmp_path, ["*/fitness.toml"], _CATALOGUE_STEP)

    outcome = run_gate(load_config(tmp_path), tmp_path, affected_files=["layer/fitness.toml"])

    assert outcome.gating_failures == ["catalogue"]


def test_a_deleted_top_level_fragment_matches_a_double_star_include(tmp_path: Path) -> None:
    """`**/` spans zero directories when include resolves, so a top-level fragment matches it too."""
    _root(tmp_path, ["**/fitness.toml"], _CATALOGUE_STEP)

    outcome = run_gate(load_config(tmp_path), tmp_path, affected_files=["fitness.toml"])

    assert outcome.gating_failures == ["catalogue"]


def test_include_matching_follows_the_hosts_case_rules() -> None:
    """Path.glob resolves `include` case-insensitively on Windows, so a deleted fragment matches the same way."""
    from pathlib import PurePosixPath, PureWindowsPath

    from tc_fitness.gate import _include_matches

    assert _include_matches("layer/fitness.toml", "Layer/fitness.toml", PureWindowsPath)
    assert not _include_matches("layer/fitness.toml", "Layer/fitness.toml", PurePosixPath)
    assert _include_matches("fitness.toml", "**/fitness.toml", PureWindowsPath)


@pytest.mark.parametrize("staged", [False, True], ids=["sequential", "scheduled"])
def test_each_runner_takes_the_fragment_change_from_the_gate(tmp_path: Path, staged: bool) -> None:
    """run_gate decides once whether a fragment changed; a runner never rescans the affected paths."""
    from tc_fitness.gate import _run_scheduled, _run_sequential

    stage = 'stage = "checks"\n' if staged else ""
    _root(tmp_path, ["layer/fitness.toml"], _CATALOGUE_STEP + stage)
    cfg = load_config(tmp_path)
    runner = _run_scheduled if staged else _run_sequential

    outcome = runner(
        cfg,
        tmp_path,
        cfg.steps,
        gate_id=None,
        staged=False,
        changed_files=None,
        shard=None,
        fast_mode=False,
        affected=["docs/readme.md"],
        fragment_changed=True,
    )

    assert [result.id for result in outcome.results if result.status == "fail"] == ["catalogue"]


def test_a_fragment_of_another_checkout_is_not_a_change_here(tmp_path: Path) -> None:
    """A same-named file changed in this checkout is not the external config's fragment."""
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    _root(elsewhere, ["layer/fitness.toml"], _CATALOGUE_STEP)
    _fragment(elsewhere, "layer/fitness.toml", "[core_checks.no_bare_except]\nroots = ['layer']\n")
    checkout = tmp_path / "checkout"
    checkout.mkdir()

    assert run_gate(load_config(elsewhere), checkout, affected_files=["layer/fitness.toml"]).ok


def test_an_in_memory_config_has_no_fragment_to_change(tmp_path: Path) -> None:
    """A config built in code is read from no file, so no affected file can be its fragment."""
    from tc_fitness.gate_config import GateConfig, StepSpec

    step = StepSpec(id="catalogue", catalogue="frag_core_cat_missing:ENTRIES", paths=("src/*",))
    config = GateConfig(name="in-memory", steps=(step,), fragments=(Path("layer/fitness.toml"),))

    assert run_gate(config, tmp_path, affected_files=["layer/fitness.toml"]).ok


def test_a_fragment_change_leaves_other_scoped_steps_skipped(tmp_path: Path) -> None:
    _root(
        tmp_path,
        ["layer/fitness.toml"],
        '[[tool.tc_fitness.steps]]\nid = "src"\npaths = ["src/*"]\nrun = ["false"]\n',
    )
    _fragment(tmp_path, "layer/fitness.toml", "[core_checks.no_bare_except]\nroots = ['layer']\n")

    assert run_gate(load_config(tmp_path), tmp_path, affected_files=["layer/fitness.toml"]).ok


def test_a_catalogue_step_skips_when_no_config_or_scoped_file_changed(tmp_path: Path) -> None:
    _root(tmp_path, ["layer/fitness.toml"], _CATALOGUE_STEP)
    _fragment(tmp_path, "layer/fitness.toml", "[core_checks.no_bare_except]\nroots = ['layer']\n")

    assert run_gate(load_config(tmp_path), tmp_path, affected_files=["docs/readme.md"]).ok


_RATCHET = (
    "path = 'src/app.py'\nrule = 'direct-import'\nmax_count = {count}\ncontents = ['import requests']\n"
)


def test_a_ratchet_declared_twice_with_different_values_is_an_error(tmp_path: Path) -> None:
    """The check enforces the first matching ratchet, so a second, different one would be ignored."""
    _root(
        tmp_path,
        ["layer/fitness.toml"],
        "[[tool.tc_fitness.core_checks.python_dependency_surface.ratchets]]\n" + _RATCHET.format(count=2),
    )
    _fragment(
        tmp_path,
        "layer/fitness.toml",
        "[[core_checks.python_dependency_surface.ratchets]]\n" + _RATCHET.format(count=1),
    )

    with pytest.raises(
        GateConfigError, match=r"python_dependency_surface\.ratchets declares .*src/app\.py.* twice"
    ):
        load_core_check_configs(tmp_path)


def test_ratchets_union_across_files_and_an_equal_repeat_is_kept_once(tmp_path: Path) -> None:
    _root(
        tmp_path,
        ["layer/fitness.toml"],
        "[[tool.tc_fitness.core_checks.python_dependency_surface.ratchets]]\n" + _RATCHET.format(count=1),
    )
    _fragment(
        tmp_path,
        "layer/fitness.toml",
        "[[core_checks.python_dependency_surface.ratchets]]\n"
        + _RATCHET.format(count=1)
        + "[[core_checks.python_dependency_surface.ratchets]]\n"
        + _RATCHET.format(count=1).replace("src/app.py", "src/other.py"),
    )

    ratchets = load_core_check_configs(tmp_path)["python_dependency_surface"]["ratchets"]

    assert [item["path"] for item in ratchets] == ["src/app.py", "src/other.py"]


def test_a_ratchet_that_is_not_a_table_is_an_error(tmp_path: Path) -> None:
    _root(
        tmp_path,
        ["layer/fitness.toml"],
        "[[tool.tc_fitness.core_checks.python_dependency_surface.ratchets]]\n" + _RATCHET.format(count=1),
    )
    _fragment(
        tmp_path, "layer/fitness.toml", "[core_checks.python_dependency_surface]\nratchets = ['src/app.py']\n"
    )

    with pytest.raises(
        GateConfigError, match=r"python_dependency_surface\.ratchets must be an array of tables"
    ):
        load_core_check_configs(tmp_path)


@pytest.mark.parametrize(
    "bad", ["path = ['src/app.py']\nrule = 'direct-import'\n", "path = 'src/app.py'\nrule = { name = 'x' }\n"]
)
def test_a_ratchet_identity_that_is_not_a_string_is_an_error(tmp_path: Path, bad: str) -> None:
    """An array or table cannot identify a ratchet; it is a config error, not a traceback."""
    _root(
        tmp_path,
        ["layer/fitness.toml"],
        "[[tool.tc_fitness.core_checks.python_dependency_surface.ratchets]]\n" + _RATCHET.format(count=1),
    )
    _fragment(tmp_path, "layer/fitness.toml", "[[core_checks.python_dependency_surface.ratchets]]\n" + bad)

    with pytest.raises(GateConfigError, match=r"must name `path` and `rule` as strings; fix: .*next: "):
        load_core_check_configs(tmp_path)


@pytest.mark.parametrize(
    "declaration",
    [
        "[tool.tc_fitness.core_checks.python_dependency_surface]\nratchets = ['src/app.py']\n",
        "[[tool.tc_fitness.core_checks.python_dependency_surface.ratchets]]\npath = ['src/app.py']\nrule = 'r'\n",
    ],
    ids=["not-a-table", "non-string-path"],
)
@pytest.mark.parametrize("include", [True, False], ids=["with-include", "no-include"])
def test_a_single_ratchet_declaration_is_validated_too(
    tmp_path: Path, declaration: str, include: bool
) -> None:
    """A ratchet declared in one file is never merged, but must be as valid as a merged one."""
    if include:
        _root(tmp_path, ["layer/fitness.toml"], declaration)
    else:
        (tmp_path / "pyproject.toml").write_text(
            '[tool.tc_fitness]\nname = "g"\n[[tool.tc_fitness.steps]]\nid = "s"\nrun = ["true"]\n'
            + declaration
        )

    with pytest.raises(GateConfigError, match=r"python_dependency_surface\.ratchets .*fix: .*next: "):
        load_core_check_configs(tmp_path)


@pytest.mark.parametrize("include", [True, False], ids=["with-include", "no-include"])
def test_one_declaration_holding_conflicting_ratchets_is_an_error(tmp_path: Path, include: bool) -> None:
    """Two entries for one path and rule in one file: the check would read only the first."""
    declaration = (
        "[[tool.tc_fitness.core_checks.python_dependency_surface.ratchets]]\n"
        + _RATCHET.format(count=1)
        + "[[tool.tc_fitness.core_checks.python_dependency_surface.ratchets]]\n"
        + _RATCHET.format(count=2)
    )
    if include:
        _root(tmp_path, ["layer/fitness.toml"], declaration)
    else:
        (tmp_path / "pyproject.toml").write_text(
            '[tool.tc_fitness]\nname = "g"\n[[tool.tc_fitness.steps]]\nid = "s"\nrun = ["true"]\n'
            + declaration
        )

    with pytest.raises(GateConfigError, match=r"ratchets declares .*src/app\.py.* twice"):
        load_core_check_configs(tmp_path)


def test_one_declaration_may_repeat_an_identical_ratchet(tmp_path: Path) -> None:
    entry = "[[tool.tc_fitness.core_checks.python_dependency_surface.ratchets]]\n" + _RATCHET.format(count=1)
    _root(tmp_path, ["layer/fitness.toml"], entry + entry)

    ratchets = load_core_check_configs(tmp_path)["python_dependency_surface"]["ratchets"]

    assert len(ratchets) == 2


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
