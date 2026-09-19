"""Runtime resolution contracts use real documents and independently expected values."""

from __future__ import annotations

import copy
import sys
from pathlib import Path

import pytest

from tc_fitness.core_checks._runtime_contracts import (
    ContractFinding,
    absolute_posix_components,
    component_paths_overlap,
    is_component_prefix,
    is_integer_identity,
    is_sha256_digest,
    resolve_contract,
    sort_findings,
)

pytestmark = pytest.mark.contract


def _selected(**values: object) -> dict[str, object]:
    return {
        "schema": "tc-fitness/runtime-contract/v1",
        "environment": "prod",
        "target": "service",
        **values,
    }


def _assert_actionable(findings: tuple[ContractFinding, ...], source: Path) -> None:
    """A denial must locate the document and give a nonempty cause and repair."""
    assert findings
    for finding in findings:
        assert finding.source == source
        assert isinstance(finding.message, str) and finding.message.strip()
        assert isinstance(finding.fix, str) and finding.fix.strip()


@pytest.mark.parametrize(
    ("value", "valid"),
    [
        (0, True),
        (1, True),
        (1000, True),
        (-1, False),
        (True, False),
        (False, False),
        (1.0, False),
        ("1", False),
        (None, False),
    ],
)
def test_integer_identity_includes_zero_but_rejects_coercible_nonintegers(value: object, valid: bool) -> None:
    assert is_integer_identity(value) is valid


@pytest.mark.parametrize(
    "value",
    [
        None,
        123,
        True,
        [],
        {},
        b"/path",
        "",
        "relative/path",
        "/safe/../escape",
        "/safe\\escape",
        "/safe\x00escape",
    ],
)
def test_absolute_path_contract_rejects_each_unsafe_component_independently(value: object) -> None:
    assert absolute_posix_components(value) is None


@pytest.mark.parametrize(
    ("path", "components"),
    [("/", ()), ("/safe", ("safe",)), ("/safe//child/", ("safe", "child"))],
)
def test_absolute_path_contract_preserves_components_without_root_or_empty_segments(
    path: str, components: tuple[str, ...]
) -> None:
    assert absolute_posix_components(path) == components


@pytest.mark.parametrize(
    ("parent", "child", "prefix", "overlap"),
    [
        ((), ("a",), True, True),
        (("a",), ("a",), True, True),
        (("a", "b"), ("a",), False, True),
        (("a",), ("ab",), False, False),
    ],
)
def test_component_prefix_and_overlap_preserve_boundary_and_direction(
    parent: tuple[str, ...], child: tuple[str, ...], prefix: bool, overlap: bool
) -> None:
    assert is_component_prefix(parent, child) is prefix
    assert component_paths_overlap(parent, child) is overlap


@pytest.mark.parametrize(
    "value",
    [
        None,
        42,
        "sha256:" + "A" * 64,
        "sha256:" + "a" * 63,
        "sha256:" + "a" * 65,
        "sha256:" + "a" * 64 + "\n",
        "SHA256:" + "a" * 64,
    ],
)
def test_digest_contract_rejects_noncanonical_wire_identity(value: object) -> None:
    assert is_sha256_digest(value) is False


def test_findings_are_ordered_by_source_pointer_code_and_message_without_mutating_input() -> None:
    ordered = [
        ContractFinding(Path("a.json"), "/a", "a-code", "a-message", "repair"),
        ContractFinding(Path("a.json"), "/a", "a-code", "z-message", "repair"),
        ContractFinding(Path("a.json"), "/a", "z-code", "message", "repair"),
        ContractFinding(Path("a.json"), "/z", "a-code", "message", "repair"),
        ContractFinding(Path("z.json"), "/a", "a-code", "message", "repair"),
    ]
    unsorted = list(reversed(ordered))
    assert sort_findings(unsorted) == tuple(ordered)
    assert unsorted == list(reversed(ordered))


def test_populated_external_references_resolve_nested_values_and_escaped_pointers(tmp_path: Path) -> None:
    external = tmp_path / "external.json"
    external.write_text(
        '{"groups":{"a/b":{"~key":[{"id":"first"},{"id":"second"}]}},"empty":[],"zero":0}',
        encoding="utf-8",
    )
    contract = _selected(
        external_references={
            "chosen": {"file": "external.json", "pointer": "/groups/a~1b/~0key/1"},
            "empty": {"file": "external.json", "pointer": "/empty"},
            "zero": {"file": "external.json", "pointer": "/zero"},
        },
        deployment={"nodes": [{"$external_ref": "chosen"}, {"nested": {"$external_ref": "empty"}}]},
        value={"$external_ref": "zero"},
        literal="preserved",
    )
    before = copy.deepcopy(contract)
    raw = external.read_bytes()
    resolved, findings = resolve_contract(
        contract, environment="prod", target="service", source=tmp_path / "registry.json"
    )
    assert findings == ()
    assert resolved == _selected(
        deployment={"nodes": [{"id": "second"}, {"nested": []}]}, value=0, literal="preserved"
    )
    assert contract == before
    assert external.read_bytes() == raw


def test_selection_does_not_load_another_targets_missing_external_dependency(tmp_path: Path) -> None:
    (tmp_path / "selected.json").write_text('{"value":{"name":"selected"}}', encoding="utf-8")
    registry = {
        "schema": "tc-fitness/runtime-contract/v1",
        "external_references": {
            "selected": {"file": "selected.json", "pointer": "/value"},
            "other": {"file": "missing.json", "pointer": "/value"},
        },
        "environments": {
            "prod": {"targets": {"service": {"value": {"$external_ref": "selected"}}}},
            "staging": {"targets": {"service": {"value": {"$external_ref": "other"}}}},
        },
    }
    before = copy.deepcopy(registry)
    resolved, findings = resolve_contract(
        registry, environment="prod", target="service", source=tmp_path / "registry.json"
    )
    assert findings == ()
    assert resolved == _selected(value={"name": "selected"})
    assert registry == before


@pytest.mark.parametrize(
    ("declaration", "code", "location"),
    [
        ("external.json", "invalid-external-reference", "/external_references/chosen"),
        ({"file": "external.json"}, "invalid-external-reference", "/external_references/chosen"),
        ({"pointer": "/value"}, "invalid-external-reference", "/external_references/chosen"),
        (
            {"file": "external.json", "pointer": "/value", "extra": True},
            "invalid-external-reference",
            "/external_references/chosen",
        ),
        ({"file": 42, "pointer": "/value"}, "invalid-external-reference", "/external_references/chosen/file"),
        ({"file": "", "pointer": "/value"}, "invalid-external-reference", "/external_references/chosen/file"),
        (
            {"file": "../outside.json", "pointer": "/value"},
            "unsafe-external-reference",
            "/external_references/chosen/file",
        ),
        (
            {"file": "/outside.json", "pointer": "/value"},
            "unsafe-external-reference",
            "/external_references/chosen/file",
        ),
        (
            {"file": "nested\\outside.json", "pointer": "/value"},
            "unsafe-external-reference",
            "/external_references/chosen/file",
        ),
        (
            {"file": "bad\x00.json", "pointer": "/value"},
            "unsafe-external-reference",
            "/external_references/chosen/file",
        ),
        (
            {"file": "external.json", "pointer": "value"},
            "invalid-external-pointer",
            "/external_references/chosen/pointer",
        ),
        (
            {"file": "external.json", "pointer": 42},
            "invalid-external-pointer",
            "/external_references/chosen/pointer",
        ),
        (
            {"file": "external.json", "pointer": "/bad~"},
            "invalid-external-pointer",
            "/external_references/chosen/pointer",
        ),
        (
            {"file": "external.json", "pointer": "/bad~2escape"},
            "invalid-external-pointer",
            "/external_references/chosen/pointer",
        ),
    ],
)
def test_malformed_external_declaration_denies_resolution_at_the_exact_location(
    tmp_path: Path, declaration: object, code: str, location: str
) -> None:
    (tmp_path / "external.json").write_text('{"value":[]}', encoding="utf-8")
    source = tmp_path / "registry.json"
    resolved, findings = resolve_contract(
        _selected(external_references={"chosen": declaration}, value={"$external_ref": "chosen"}),
        environment="prod",
        target="service",
        source=source,
    )
    assert resolved is None
    assert [(finding.source, finding.pointer, finding.code) for finding in findings] == [
        (source, location, code),
        (source, "/value/$external_ref", "undefined-external-reference"),
    ]
    assert all(finding.message and finding.fix for finding in findings)


@pytest.mark.parametrize(
    ("pointer", "code"),
    [
        ("/missing", "external-pointer-missing"),
        ("/items/2", "external-pointer-missing"),
        ("/items/-1", "external-pointer-missing"),
        ("/items/01", "invalid-external-pointer"),
        ("/items/\u0661", "external-pointer-missing"),
        ("/items/" + "9" * 5000, "invalid-external-pointer"),
    ],
)
def test_external_pointer_cannot_fall_back_to_a_different_value(
    tmp_path: Path, pointer: str, code: str
) -> None:
    external = tmp_path / "external.json"
    external.write_text('{"items":["first","second"]}', encoding="utf-8")
    resolved, findings = resolve_contract(
        _selected(
            external_references={"chosen": {"file": "external.json", "pointer": pointer}},
            value={"$external_ref": "chosen"},
        ),
        environment="prod",
        target="service",
        source=tmp_path / "registry.json",
    )
    assert resolved is None
    assert any(
        finding.source == external and finding.pointer == pointer and finding.code == code
        for finding in findings
    )
    assert {finding.code for finding in findings} == {code, "undefined-external-reference"}


def test_missing_external_file_is_not_replaced_with_an_empty_success(tmp_path: Path) -> None:
    resolved, findings = resolve_contract(
        _selected(
            external_references={"chosen": {"file": "missing.json", "pointer": "/value"}},
            value={"$external_ref": "chosen"},
        ),
        environment="prod",
        target="service",
        source=tmp_path / "registry.json",
    )
    assert resolved is None
    assert {finding.code for finding in findings} == {"missing-file", "undefined-external-reference"}
    assert (
        next(finding for finding in findings if finding.code == "missing-file").source
        == tmp_path / "missing.json"
    )


@pytest.mark.parametrize(
    "placeholder",
    [
        {"$external_ref": "missing"},
        {"$external_ref": ""},
        {"$external_ref": 42},
        {"$external_ref": "chosen", "fallback": []},
    ],
)
def test_invalid_nested_reference_use_retains_its_pointer(tmp_path: Path, placeholder: object) -> None:
    resolved, findings = resolve_contract(
        _selected(deployment={"a/b~c": [placeholder]}),
        environment="prod",
        target="service",
        source=tmp_path / "registry.json",
    )
    assert resolved is None
    assert len(findings) == 1
    _assert_actionable(findings, tmp_path / "registry.json")
    finding = findings[0]
    if isinstance(placeholder, dict) and "fallback" in placeholder:
        assert (finding.pointer, finding.code) == ("/deployment/a~1b~0c/0", "invalid-external-reference-use")
    else:
        assert (finding.pointer, finding.code) == (
            "/deployment/a~1b~0c/0/$external_ref",
            "undefined-external-reference",
        )


@pytest.mark.parametrize("environment", [None, "prod"])
@pytest.mark.parametrize("target", [None, "service"])
def test_already_selected_identity_is_preserved_with_optional_selectors(
    tmp_path: Path, environment: str | None, target: str | None
) -> None:
    contract = _selected(filesystem={"roots": []})
    resolved, findings = resolve_contract(
        contract, environment=environment, target=target, source=tmp_path / "registry.json"
    )
    assert findings == ()
    assert resolved == _selected(filesystem={"roots": []})
    assert contract == _selected(filesystem={"roots": []})


def test_missing_selected_identity_is_filled_from_independent_selectors(tmp_path: Path) -> None:
    original = {"schema": "tc-fitness/runtime-contract/v1", "value": "kept"}
    resolved, findings = resolve_contract(
        original, environment="prod", target="service", source=tmp_path / "registry.json"
    )
    assert findings == ()
    assert resolved == _selected(value="kept")
    assert original == {"schema": "tc-fitness/runtime-contract/v1", "value": "kept"}


@pytest.mark.parametrize(("key", "wrong"), [("environment", "staging"), ("target", "other")])
def test_already_selected_contract_cannot_override_requested_identity(
    tmp_path: Path, key: str, wrong: str
) -> None:
    source = tmp_path / "registry.json"
    contract = _selected(**{key: wrong})
    resolved, findings = resolve_contract(contract, environment="prod", target="service", source=source)
    assert resolved is None
    assert [(f.source, f.pointer, f.code) for f in findings] == [(source, f"/{key}", "selection-mismatch")]
    assert wrong in findings[0].fix
    _assert_actionable(findings, source)


@pytest.mark.parametrize("environments", [None, [], "prod", 42])
def test_present_but_malformed_environment_registry_is_not_a_selected_contract(
    tmp_path: Path, environments: object
) -> None:
    resolved, findings = resolve_contract(
        {"schema": "tc-fitness/runtime-contract/v1", "environments": environments},
        environment="prod",
        target="service",
        source=tmp_path / "registry.json",
    )
    assert resolved is None
    assert [(f.pointer, f.code) for f in findings] == [("/environments", "invalid-environments")]
    _assert_actionable(findings, tmp_path / "registry.json")


@pytest.mark.parametrize(
    ("environment", "target"), [(None, "service"), ("", "service"), ("prod", None), ("prod", "")]
)
def test_registry_requires_both_nonempty_selectors(
    tmp_path: Path, environment: str | None, target: str | None
) -> None:
    registry = {
        "schema": "tc-fitness/runtime-contract/v1",
        "environments": {"prod": {"targets": {"service": {}}}},
    }
    resolved, findings = resolve_contract(
        registry, environment=environment, target=target, source=tmp_path / "registry.json"
    )
    assert resolved is None
    assert [(f.pointer, f.code) for f in findings] == [("/environments", "missing-selection")]
    _assert_actionable(findings, tmp_path / "registry.json")


@pytest.mark.parametrize("environment_value", [None, [], "prod"])
def test_unknown_environment_reports_escaped_selector_location(
    tmp_path: Path, environment_value: object
) -> None:
    resolved, findings = resolve_contract(
        {"environments": {"a/b~c": environment_value}},
        environment="a/b~c",
        target="service",
        source=tmp_path / "registry.json",
    )
    assert resolved is None
    assert [(f.pointer, f.code) for f in findings] == [("/environments/a~1b~0c", "unknown-environment")]
    _assert_actionable(findings, tmp_path / "registry.json")


@pytest.mark.parametrize("targets", [None, [], {}, {"a/b~c": None}, {"a/b~c": []}])
def test_unknown_target_does_not_select_another_target(tmp_path: Path, targets: object) -> None:
    resolved, findings = resolve_contract(
        {"environments": {"prod": {"targets": targets}}},
        environment="prod",
        target="a/b~c",
        source=tmp_path / "registry.json",
    )
    assert resolved is None
    assert [(f.pointer, f.code) for f in findings] == [
        ("/environments/prod/targets/a~1b~0c", "unknown-target")
    ]
    _assert_actionable(findings, tmp_path / "registry.json")


@pytest.mark.parametrize("key", ["schema", "environment", "target"])
def test_target_local_reserved_identity_cannot_conflict_with_registry(tmp_path: Path, key: str) -> None:
    resolved, findings = resolve_contract(
        {"environments": {"prod": {"targets": {"service": {key: "conflicting-value"}}}}},
        environment="prod",
        target="service",
        source=tmp_path / "registry.json",
    )
    assert resolved is None
    assert [(f.pointer, f.code) for f in findings] == [
        (f"/environments/prod/targets/service/{key}", "selection-conflict")
    ]
    _assert_actionable(findings, tmp_path / "registry.json")


def test_target_local_matching_reserved_identity_is_accepted(tmp_path: Path) -> None:
    resolved, findings = resolve_contract(
        {"environments": {"prod": {"targets": {"service": _selected(value=True)}}}},
        environment="prod",
        target="service",
        source=tmp_path / "registry.json",
    )
    assert findings == ()
    assert resolved == _selected(value=True)


@pytest.mark.parametrize("declarations", [[], 42, "external.json"])
def test_external_reference_table_must_be_a_mapping(tmp_path: Path, declarations: object) -> None:
    resolved, findings = resolve_contract(
        _selected(external_references=declarations, value={"$external_ref": "chosen"}),
        environment="prod",
        target="service",
        source=tmp_path / "registry.json",
    )
    assert resolved is None
    assert [(f.pointer, f.code) for f in findings] == [
        ("/external_references", "invalid-external-references"),
        ("/value/$external_ref", "undefined-external-reference"),
    ]
    _assert_actionable(findings, tmp_path / "registry.json")


@pytest.mark.parametrize(
    ("raw", "code"),
    [
        ('{"value":1,"value":2}', "duplicate-key"),
        ('{"value":NaN}', "invalid-json-constant"),
        ('{"value":', "invalid-json"),
    ],
)
def test_external_document_parse_failure_cannot_supply_a_reference(
    tmp_path: Path, raw: str, code: str
) -> None:
    external = tmp_path / "external.json"
    external.write_text(raw, encoding="utf-8")
    resolved, findings = resolve_contract(
        _selected(
            external_references={"chosen": {"file": "external.json", "pointer": "/value"}},
            value={"$external_ref": "chosen"},
        ),
        environment="prod",
        target="service",
        source=tmp_path / "registry.json",
    )
    assert resolved is None
    assert {f.code for f in findings} == {code, "undefined-external-reference"}
    assert next(f for f in findings if f.code == code).source == external


def test_external_symlink_cannot_escape_the_contract_directory(tmp_path: Path) -> None:
    directory = tmp_path / "contract"
    directory.mkdir()
    outside = tmp_path / "outside.json"
    outside.write_text('{"value":"outside"}', encoding="utf-8")
    (directory / "external.json").symlink_to(outside)
    resolved, findings = resolve_contract(
        _selected(
            external_references={"chosen": {"file": "external.json", "pointer": "/value"}},
            value={"$external_ref": "chosen"},
        ),
        environment="prod",
        target="service",
        source=directory / "registry.json",
    )
    assert resolved is None
    assert {f.code for f in findings} == {"unsafe-external-reference", "undefined-external-reference"}
    _assert_actionable(findings, directory / "registry.json")


@pytest.mark.parametrize("declared_path", ["nested/../external.json", "nested/../../contract/external.json"])
def test_external_parent_segments_are_forbidden_even_when_resolution_returns_inside_root(
    tmp_path: Path, declared_path: str
) -> None:
    directory = tmp_path / "contract"
    directory.mkdir()
    (directory / "nested").mkdir()
    (directory / "external.json").write_text('{"value":"reachable"}', encoding="utf-8")
    source = directory / "registry.json"
    resolved, findings = resolve_contract(
        _selected(
            external_references={"chosen": {"file": declared_path, "pointer": "/value"}},
            value={"$external_ref": "chosen"},
        ),
        environment="prod",
        target="service",
        source=source,
    )
    assert resolved is None
    assert [(f.pointer, f.code) for f in findings] == [
        ("/external_references/chosen/file", "unsafe-external-reference"),
        ("/value/$external_ref", "undefined-external-reference"),
    ]
    _assert_actionable(findings, source)


@pytest.mark.parametrize(("pointer", "expected"), [("/~0", "tilde"), ("/~1", "slash"), ("/a~1", "suffix")])
def test_terminal_json_pointer_escape_selects_the_literal_document_key(
    tmp_path: Path, pointer: str, expected: str
) -> None:
    (tmp_path / "external.json").write_text('{"~":"tilde","/":"slash","a/":"suffix"}', encoding="utf-8")
    resolved, findings = resolve_contract(
        _selected(
            external_references={"chosen": {"file": "external.json", "pointer": pointer}},
            value={"$external_ref": "chosen"},
        ),
        environment="prod",
        target="service",
        source=tmp_path / "registry.json",
    )
    assert findings == ()
    assert resolved == _selected(value=expected)


@pytest.mark.parametrize(("index", "expected"), [(0, "value-0"), (10, "value-10")])
def test_canonical_array_indices_include_zero_and_multiple_digits(
    tmp_path: Path, index: int, expected: str
) -> None:
    (tmp_path / "external.json").write_text(
        '{"values":["value-0",1,2,3,4,5,6,7,8,9,"value-10"]}', encoding="utf-8"
    )
    resolved, findings = resolve_contract(
        _selected(
            external_references={"chosen": {"file": "external.json", "pointer": f"/values/{index}"}},
            value={"$external_ref": "chosen"},
        ),
        environment="prod",
        target="service",
        source=tmp_path / "registry.json",
    )
    assert findings == ()
    assert resolved == _selected(value=expected)


@pytest.mark.parametrize(
    ("index", "code"),
    [
        (sys.maxsize - 1, "external-pointer-missing"),
        (sys.maxsize, "external-pointer-missing"),
        (sys.maxsize + 1, "invalid-external-pointer"),
    ],
)
def test_array_index_size_boundary_distinguishes_missing_from_unrepresentable(
    tmp_path: Path, index: int, code: str
) -> None:
    external = tmp_path / "external.json"
    external.write_text('{"values":[]}', encoding="utf-8")
    pointer = f"/values/{index}"
    resolved, findings = resolve_contract(
        _selected(
            external_references={"chosen": {"file": "external.json", "pointer": pointer}},
            value={"$external_ref": "chosen"},
        ),
        environment="prod",
        target="service",
        source=tmp_path / "registry.json",
    )
    assert resolved is None
    assert {f.code for f in findings} == {code, "undefined-external-reference"}
    selected = tuple(f for f in findings if f.code == code)
    assert len(selected) == 1 and selected[0].pointer == pointer
    _assert_actionable(selected, external)


@pytest.mark.parametrize(
    "first",
    [
        None,
        {"file": "external.json"},
        {"file": "../outside.json", "pointer": "/value"},
        {"file": "broken.json", "pointer": "/value"},
    ],
)
def test_bad_external_reference_does_not_prevent_loading_a_later_valid_reference(
    tmp_path: Path, first: object
) -> None:
    (tmp_path / "external.json").write_text('{"value":"available"}', encoding="utf-8")
    (tmp_path / "broken.json").write_text('{"value":', encoding="utf-8")
    contract = _selected(
        external_references={"bad": first, "good": {"file": "external.json", "pointer": "/value"}},
        values=[{"$external_ref": "bad"}, {"$external_ref": "good"}],
    )
    resolved, findings = resolve_contract(
        contract, environment="prod", target="service", source=tmp_path / "registry.json"
    )
    assert resolved is None
    assert [f.pointer for f in findings if f.code == "undefined-external-reference"] == [
        "/values/0/$external_ref"
    ]
    assert all(f.message and f.fix for f in findings)


def test_pointer_continues_through_object_fields_after_selecting_an_array_element(tmp_path: Path) -> None:
    (tmp_path / "external.json").write_text('{"values":[{"id":"selected"}]}', encoding="utf-8")
    resolved, findings = resolve_contract(
        _selected(
            external_references={"chosen": {"file": "external.json", "pointer": "/values/0/id"}},
            value={"$external_ref": "chosen"},
        ),
        environment="prod",
        target="service",
        source=tmp_path / "registry.json",
    )
    assert findings == ()
    assert resolved == _selected(value="selected")


def test_unused_declaration_before_selected_reference_does_not_stop_loading(tmp_path: Path) -> None:
    (tmp_path / "external.json").write_text('{"value":"selected"}', encoding="utf-8")
    resolved, findings = resolve_contract(
        _selected(
            external_references={
                "unused": {"file": "missing.json", "pointer": "/value"},
                "chosen": {"file": "external.json", "pointer": "/value"},
            },
            value={"$external_ref": "chosen"},
        ),
        environment="prod",
        target="service",
        source=tmp_path / "registry.json",
    )
    assert findings == ()
    assert resolved == _selected(value="selected")


def test_root_reference_placeholder_with_siblings_is_located_at_the_document_root(tmp_path: Path) -> None:
    source = tmp_path / "registry.json"
    resolved, findings = resolve_contract(
        _selected(**{"$external_ref": "chosen"}), environment="prod", target="service", source=source
    )
    assert resolved is None
    assert [(f.pointer, f.code) for f in findings] == [("/", "invalid-external-reference-use")]
    _assert_actionable(findings, source)
