"""Immutable mutation inputs and conservative scope through their public APIs."""

from __future__ import annotations

import hashlib
import io
import json
import signal
import subprocess
import tarfile
from pathlib import Path
from types import FrameType
from typing import Any

import pytest

from tc_fitness.mutation_scope import (
    MutationError,
    archive_files,
    candidate_archives,
    read_policy,
    select_scope,
)

pytestmark = pytest.mark.contract

POLICY = (
    'schema = "tc.fitness/mutation-policy/v1"\n'
    'source_roots = ["src"]\ntests = ["tests"]\n'
    "timeout_seconds = 60\nmax_mutants = 100\n"
)


def _files(policy: str = POLICY) -> dict[str, bytes]:
    return {
        "mutation.toml": policy.encode(),
        "src/subject.py": b"def decision(value):\n    return value > 0\n",
        "tests/test_subject.py": b"from subject import decision\ndef test_decision():\n    assert decision(1) is True\n",
    }


def _traversal_deadline(_signal: int, _frame: FrameType | None) -> None:
    raise TimeoutError("finite production dependency traversal did not terminate")


def _bounded_scope(
    before: dict[str, bytes], after: dict[str, bytes], policy: dict[str, Any], *, broad: bool | None = None
) -> dict[str, Any]:
    """Keep a nonterminating native mutation a test failure, not a hung worker."""
    previous_handler = signal.signal(signal.SIGALRM, _traversal_deadline)
    previous_timer = signal.setitimer(signal.ITIMER_REAL, 1)
    try:
        if broad is None:
            return select_scope(before, after, policy)
        return select_scope(before, after, policy, broad=broad)
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous_handler)
        signal.setitimer(signal.ITIMER_REAL, *previous_timer)


@pytest.mark.parametrize(
    ("old", "new", "message"),
    [
        ('schema = "tc.fitness/mutation-policy/v1"', 'schema = "other"', "^unknown mutation policy schema$"),
        (
            "max_mutants = 100",
            "max_mutants = 100\nexemptions = []",
            "^mutation policy requires exact fields; exemptions are not supported$",
        ),
        ('source_roots = ["src"]', "source_roots = []", "nonempty unique"),
        ('source_roots = ["src"]', 'source_roots = ["src", "src"]', "nonempty unique"),
        ('tests = ["tests"]', 'tests = "tests"', "nonempty unique"),
        ('tests = ["tests"]', "tests = [42]", "literal repository-relative"),
        ('tests = ["tests"]', 'tests = [""]', "literal repository-relative"),
        ('tests = ["tests"]', 'tests = ["-q"]', "literal repository-relative"),
        ('tests = ["tests"]', 'tests = ["/tests"]', "literal repository-relative"),
        ('tests = ["tests"]', 'tests = ["tests/../src"]', "literal repository-relative"),
        ('tests = ["tests"]', 'tests = ["tests\\\\subject"]', "literal repository-relative"),
        ('tests = ["tests"]', 'tests = ["tests/*"]', "literal repository-relative"),
        ('tests = ["tests"]', 'tests = ["tests/?"]', "literal repository-relative"),
        ('tests = ["tests"]', 'tests = ["tests\\nsubject"]', "literal repository-relative"),
        ('tests = ["tests"]', 'tests = ["tests\\rsubject"]', "literal repository-relative"),
        ('tests = ["tests"]', 'tests = ["absent"]', "no tracked inputs"),
        ("timeout_seconds = 60", "timeout_seconds = 0", "bounded between 1 and 900"),
        ("timeout_seconds = 60", "timeout_seconds = 901", "bounded between 1 and 900"),
        ("timeout_seconds = 60", "timeout_seconds = true", "bounded between 1 and 900"),
        ("max_mutants = 100", "max_mutants = 100001", "bounded between 1 and 100000"),
        ("max_mutants = 100", "max_mutants = 0", "bounded between 1 and 100000"),
        ("max_mutants = 100", "max_mutants = 1.0", "bounded between 1 and 100000"),
        ('tests = ["tests"]', 'tests = ["src"]', "must be disjoint"),
        ('tests = ["tests"]', 'tests = ["src/subject.py"]', "must be disjoint"),
        ('source_roots = ["src"]', 'source_roots = ["tests/test_subject.py"]', "must be disjoint"),
    ],
)
def test_policy_rejects_unbounded_ambiguous_or_overlapping_scope(old: str, new: str, message: str) -> None:
    with pytest.raises(MutationError, match=message):
        read_policy(_files(POLICY.replace(old, new)))


@pytest.mark.parametrize("policy", [None, "not = [toml", "schema ="])
def test_policy_must_exist_and_parse(policy: str | None) -> None:
    files = _files()
    if policy is None:
        del files["mutation.toml"]
    else:
        files["mutation.toml"] = policy.encode()
    with pytest.raises(MutationError, match=r"^tracked mutation\.toml policy is required$"):
        read_policy(files)


@pytest.mark.parametrize("timeout,budget", [(1, 1), (900, 100000)])
def test_policy_accepts_exact_bounds_and_literal_test_file(timeout: int, budget: int) -> None:
    text = POLICY.replace("timeout_seconds = 60", f"timeout_seconds = {timeout}").replace(
        "max_mutants = 100", f"max_mutants = {budget}"
    )
    text = text.replace('tests = ["tests"]', 'tests = ["tests/test_subject.py"]')
    policy = read_policy(_files(text))
    assert policy["timeout_seconds"] == timeout
    assert policy["max_mutants"] == budget
    assert policy["tests"] == ["tests/test_subject.py"]


def test_policy_decodes_utf8_non_ascii_paths_without_rewriting_them() -> None:
    files = {
        "mutation.toml": POLICY.replace('source_roots = ["src"]', 'source_roots = ["sourcé"]').encode(),
        "sourcé/café.py": b"def decision(value):\n    return value > 0\n",
        "tests/test_subject.py": _files()["tests/test_subject.py"],
    }
    policy = read_policy(files)
    assert policy["source_roots"] == ["sourcé"]
    assert policy["tests"] == ["tests"]


def test_policy_rejects_non_utf8_bytes() -> None:
    files = {**_files(), "mutation.toml": b"\xff"}
    with pytest.raises(MutationError, match=r"^tracked mutation\.toml policy is required$"):
        read_policy(files)


@pytest.mark.parametrize("name", ["/absolute.py", "../escaped.py", "src/../../escaped.py", "src\\escaped.py"])
def test_archive_paths_cannot_escape_snapshot(name: str) -> None:
    archive = io.BytesIO()
    with tarfile.open(fileobj=archive, mode="w") as stream:
        member = tarfile.TarInfo(name)
        member.size = 4
        stream.addfile(member, io.BytesIO(b"pass"))
    with pytest.raises(MutationError, match="unsafe path"):
        archive_files(archive.getvalue())


@pytest.mark.parametrize("kind", [tarfile.SYMTYPE, tarfile.LNKTYPE, tarfile.FIFOTYPE])
def test_archive_rejects_nonregular_inputs(kind: bytes) -> None:
    archive = io.BytesIO()
    with tarfile.open(fileobj=archive, mode="w") as stream:
        member = tarfile.TarInfo("src/subject.py")
        member.type = kind
        member.linkname = "elsewhere.py"
        stream.addfile(member)
    with pytest.raises(MutationError, match="require regular tracked files"):
        archive_files(archive.getvalue())


def _git(root: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, text=True).stdout.strip()


def _repository(root: Path) -> tuple[str, str]:
    for name, raw in _files().items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    _git(root, "init", "-q")
    _git(root, "config", "user.name", "three-cubes-agent[bot]")
    _git(root, "config", "user.email", "295831460+three-cubes-agent[bot]@users.noreply.github.com")
    _git(root, "add", ".")
    _git(root, "commit", "-qm", "test: initial scope")
    base = _git(root, "rev-parse", "HEAD")
    (root / "src/subject.py").write_text("def decision(value):\n    return value >= 0\n")
    _git(root, "commit", "-qam", "test: changed boundary")
    return base, _git(root, "rev-parse", "HEAD")


@pytest.mark.parametrize("identity", ["short", "unknown", "wrong-head", "tag", "nonancestor"])
def test_candidate_archives_reject_nonexact_or_unrelated_identities(tmp_path: Path, identity: str) -> None:
    base, head = _repository(tmp_path)
    message = "Git identity unavailable"
    if identity == "short":
        base = base[:7]
        message = "full immutable commit SHAs"
    elif identity == "unknown":
        base = "0" * 40
    elif identity == "wrong-head":
        head = base
        message = "current checkout"
    elif identity == "tag":
        _git(tmp_path, "tag", "-am", "test: annotated identity", "test-tag")
        base = _git(tmp_path, "rev-parse", "test-tag")
        message = "commit identity mismatch"
    else:
        _git(tmp_path, "checkout", "--orphan", "unrelated")
        _git(tmp_path, "commit", "-qm", "test: unrelated history")
        head = _git(tmp_path, "rev-parse", "HEAD")
    with pytest.raises(MutationError, match=message):
        candidate_archives(tmp_path, base, head)


@pytest.mark.parametrize("sabotage", ["symlink", "export-subst"])
def test_git_candidate_bytes_cannot_be_replaced_by_export_rules(tmp_path: Path, sabotage: str) -> None:
    base, _ = _repository(tmp_path)
    if sabotage == "symlink":
        (tmp_path / "src/linked.py").symlink_to("subject.py")
        message = "regular tracked files"
    else:
        (tmp_path / "identity.txt").write_text("$Format:%H$\n")
        (tmp_path / ".gitattributes").write_text("identity.txt export-subst\n")
        message = "rewrites tracked inputs"
    _git(tmp_path, "add", ".")
    _git(tmp_path, "commit", "-qm", "test: nonliteral archive")
    with pytest.raises(MutationError, match=message):
        candidate_archives(tmp_path, base, _git(tmp_path, "rev-parse", "HEAD"))


def test_unparseable_production_is_an_error_not_empty_scope() -> None:
    before = _files()
    after = {**before, "src/subject.py": b"def broken(:\n"}
    with pytest.raises(MutationError, match=r"production Python cannot be parsed: src/subject\.py"):
        _bounded_scope(before, after, read_policy(before))


@pytest.mark.parametrize(
    "expression",
    [
        "getattr(object(), 'run')",
        "globals()",
        "locals()",
        "eval('value')",
        "exec('pass')",
        "__import__('os')",
        "loader.import_module('os')",
    ],
)
def test_dynamic_dispatch_requires_whole_production_scope(expression: str) -> None:
    before = _files()
    before["src/other.py"] = b"def unrelated(value):\n    return value + 2\n"
    after = {**before, "src/subject.py": f"def decision(value):\n    return {expression}\n".encode()}
    scope = _bounded_scope(before, after, read_policy(before))
    assert scope["changed_functions"] == ["subject.decision"]
    assert [item["name"] for item in scope["functions"]] == ["other.unrelated", "subject.decision"]


def test_typed_callable_alias_and_relative_import_retain_async_dependency() -> None:
    before = _files()
    before["src/package/helper.py"] = b"async def boundary(value):\n    return value > 0\n"
    before["src/package/caller.py"] = (
        b"from .helper import boundary as compare\nhandler: object = compare\n"
        b"async def decision(value):\n    return await handler(value)\n"
    )
    after = {
        **before,
        "src/package/caller.py": before["src/package/caller.py"].replace(
            b"handler(value)", b"handler(value + 1)"
        ),
    }
    scope = _bounded_scope(before, after, read_policy(before))
    assert [item["name"] for item in scope["functions"]] == [
        "package.caller.decision",
        "package.helper.boundary",
    ]


def test_changed_class_method_preserves_method_selector_and_transitive_call() -> None:
    before = _files()
    before["src/subject.py"] = (
        b"class Policy:\n    threshold = 0\n    def decision(self, value):\n        return helper(value)\n"
        b"def helper(value):\n    return value > 0\n"
    )
    after = {
        **before,
        "src/subject.py": before["src/subject.py"].replace(b"helper(value)\n", b"helper(value + 1)\n", 1),
    }
    scope = _bounded_scope(before, after, read_policy(before))
    assert [item["name"] for item in scope["functions"]] == ["subject.Policy.decision", "subject.helper"]
    assert scope["functions"][0]["selector"] == "subject.xǁPolicyǁdecision__mutmut_*"


def test_imported_changed_module_and_global_attribute_assignment_keep_callers() -> None:
    before = _files()
    before["src/consumer.py"] = (
        b"import subject as policy\npolicy.label = 'decision'\n"
        b"def caller(value):\n    return policy.decision(value)\n"
    )
    after = {**before, "src/subject.py": b"THRESHOLD = 1\n" + before["src/subject.py"]}
    scope = _bounded_scope(before, after, read_policy(before))
    assert scope["changed_functions"] == ["consumer.caller", "subject.decision"]
    assert [item["name"] for item in scope["functions"]] == ["consumer.caller", "subject.decision"]


def test_broad_scope_selects_unchanged_functions_without_claiming_changed_functions() -> None:
    files = _files()
    scope = _bounded_scope(files, files, read_policy(files), broad=True)
    assert scope["required"] is True
    assert scope["mode"] == "broad"
    assert scope["changed_functions"] == []
    assert [item["name"] for item in scope["functions"]] == ["subject.decision"]


@pytest.mark.parametrize(
    "source,test",
    [
        ("src/", "src/tests"),
        ("src//", "src/tests/"),
        ("src/tests", "src/"),
        ("srcX/", "srcX/tests"),
        ("srcX/tests", "srcX/"),
    ],
)
def test_policy_trailing_separators_cannot_hide_production_test_overlap(source: str, test: str) -> None:
    policy = POLICY.replace('source_roots = ["src"]', f'source_roots = ["{source}"]').replace(
        'tests = ["tests"]', f'tests = ["{test}"]'
    )
    files = {
        **_files(policy),
        "src/tests/test_subject.py": b"from subject import decision\n",
        "srcX/subject.py": b"def decision(value):\n    return value > 0\n",
        "srcX/tests/test_subject.py": b"from subject import decision\n",
    }
    with pytest.raises(MutationError, match=r"^production roots and test paths must be disjoint$"):
        read_policy(files)


@pytest.mark.parametrize("source_root", ["src/", "srcX/"])
def test_policy_accepts_disjoint_trailing_separator_paths_without_rewriting_them(source_root: str) -> None:
    text = POLICY.replace('source_roots = ["src"]', f'source_roots = ["{source_root}"]')
    text = text.replace('tests = ["tests"]', 'tests = ["tests/"]')
    files = _files(text)
    files[source_root + "subject.py"] = files.pop("src/subject.py")
    policy = read_policy(files)
    assert policy["source_roots"] == [source_root]
    assert policy["tests"] == ["tests/"]
    scope = _bounded_scope(files, files, policy, broad=True)
    assert [item["path"] for item in scope["functions"]] == [source_root + "subject.py"]


def test_empty_and_populated_dependency_traversals_terminate() -> None:
    before = _files()
    policy = read_policy(before)
    assert _bounded_scope({}, {}, policy)["required"] is False
    after = {**before, "src/subject.py": before["src/subject.py"].replace(b"> 0", b">= 0")}
    scope = _bounded_scope(before, after, policy)
    assert scope["changed_functions"] == ["subject.decision"]
    assert [item["name"] for item in scope["functions"]] == ["subject.decision"]


@pytest.mark.parametrize(
    "path,module",
    [
        ("src/subject.py", "subject"),
        ("src/package/xray.py", "package.xray"),
        ("src/package/xray/extra.py", "package.xray.extra"),
    ],
)
def test_deleted_function_selects_remaining_callers_in_dotted_modules(path: str, module: str) -> None:
    before = _files()
    del before["src/subject.py"]
    before[path] = (
        b"def helper(value):\n    return value > 0\ndef decision(value):\n    return helper(value)\n"
    )
    after = {**before, path: b"def decision(value):\n    return helper(value)\n"}
    scope = _bounded_scope(before, after, read_policy(before))
    assert scope["required"] is True
    assert scope["changed_functions"] == [module + ".decision"]
    assert [item["name"] for item in scope["functions"]] == [module + ".decision"]
    assert scope["functions"][0]["selector"] == module + ".x_decision__mutmut_*"


def test_local_caller_closure_and_plan_metadata_bind_only_required_functions() -> None:
    before = _files()
    before["src/subject.py"] = (
        b"def helper(value):\n    return value > 0\n"
        b"def decision(value):\n    return helper(value)\n"
        b"def unrelated(value):\n    return value * 2\n"
    )
    after = {
        **before,
        "src/subject.py": before["src/subject.py"].replace(
            b"return helper(value)", b"return helper(value + 1)"
        ),
    }
    policy = read_policy(after)
    scope = _bounded_scope(before, after, policy)
    assert scope["mode"] == "changed"
    assert scope["required"] is True
    assert scope["changed_functions"] == ["subject.decision"]
    assert [item["name"] for item in scope["functions"]] == ["subject.decision", "subject.helper"]
    encoded = json.dumps(policy, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    assert scope["policy_digest"] == "sha256:" + hashlib.sha256(encoded).hexdigest()


def test_changed_module_does_not_select_an_unrelated_importer() -> None:
    before = _files()
    before["src/other.py"] = b"def unrelated(value):\n    return value\n"
    before["src/consumer.py"] = b"import other\ndef caller(value):\n    return other.unrelated(value)\n"
    after = {**before, "src/subject.py": b"THRESHOLD = 1\n" + before["src/subject.py"]}
    scope = _bounded_scope(before, after, read_policy(after))
    assert scope["changed_functions"] == ["subject.decision"]
    assert [item["name"] for item in scope["functions"]] == ["subject.decision"]


def test_class_constructor_reference_retains_its_methods_without_free_functions() -> None:
    before = _files()
    before["src/subject.py"] = (
        b"class Policy:\n    def __init__(self, value):\n        self.value = value\n"
        b"    def accepts(self):\n        return self.value > 0\n"
        b"def decision(value):\n    return Policy(value)\n"
        b"def unrelated(value):\n    return value * 2\n"
    )
    after = {
        **before,
        "src/subject.py": before["src/subject.py"].replace(
            b"return Policy(value)", b"return Policy(value + 1)"
        ),
    }
    scope = _bounded_scope(before, after, read_policy(after))
    assert scope["changed_functions"] == ["subject.decision"]
    assert [item["name"] for item in scope["functions"]] == [
        "subject.Policy.__init__",
        "subject.Policy.accepts",
        "subject.decision",
    ]


def test_package_reexport_fallback_preserves_package_scope_but_not_local_unrelated_functions() -> None:
    before = _files()
    before["src/package/__init__.py"] = b"from .helper import boundary\n"
    before["src/package/helper.py"] = b"def boundary(value):\n    return value > 0\n"
    before["src/package/other.py"] = b"def extra(value):\n    return value\n"
    before["src/subject.py"] = (
        b"from package import boundary\ndef decision(value):\n    return boundary(value)\n"
        b"def unrelated(value):\n    return value * 2\n"
    )
    after = {
        **before,
        "src/subject.py": before["src/subject.py"].replace(
            b"return boundary(value)", b"return boundary(value + 1)"
        ),
    }
    scope = _bounded_scope(before, after, read_policy(after))
    assert scope["changed_functions"] == ["subject.decision"]
    assert [item["name"] for item in scope["functions"]] == [
        "package.helper.boundary",
        "package.other.extra",
        "subject.decision",
    ]


def test_self_referencing_registry_terminates_and_preserves_callable_dependency() -> None:
    before = _files()
    before["src/subject.py"] = (
        b"def helper(value):\n    return value > 0\n"
        b"registry = {'handler': helper}\nregistry = {'previous': registry, 'handler': helper}\n"
        b"def decision(value):\n    return registry['handler'](value)\n"
        b"def unrelated(value):\n    return value * 2\n"
    )
    after = {
        **before,
        "src/subject.py": before["src/subject.py"].replace(b"['handler'](value)", b"['handler'](value + 1)"),
    }
    scope = _bounded_scope(before, after, read_policy(after))
    assert scope["changed_functions"] == ["subject.decision"]
    assert [item["name"] for item in scope["functions"]] == ["subject.decision", "subject.helper"]


def test_parameter_method_dispatch_keeps_matching_production_method() -> None:
    before = _files()
    before["src/subject.py"] = (
        b"class Policy:\n    def accepts(self, value):\n        return value > 0\n"
        b"def decision(policy, value):\n    return policy.accepts(value)\n"
        b"def unrelated(value):\n    return value * 2\n"
    )
    after = {
        **before,
        "src/subject.py": before["src/subject.py"].replace(
            b"policy.accepts(value)", b"policy.accepts(value + 1)"
        ),
    }
    scope = _bounded_scope(before, after, read_policy(after))
    assert scope["changed_functions"] == ["subject.decision"]
    assert [item["name"] for item in scope["functions"]] == ["subject.Policy.accepts", "subject.decision"]


@pytest.mark.parametrize(
    "relative,helper", [(".helper", "package.nested.helper"), ("..helper", "package.helper")]
)
def test_relative_import_depth_keeps_only_the_resolved_dependency(relative: str, helper: str) -> None:
    before = _files()
    before["src/" + helper.replace(".", "/") + ".py"] = b"def boundary(value):\n    return value > 0\n"
    before["src/package/unrelated.py"] = b"def unused(value):\n    return value * 2\n"
    caller = "src/package/nested/caller.py"
    before[caller] = (
        f"from {relative} import boundary\ndef decision(value):\n    return boundary(value)\n".encode()
    )
    after = {**before, caller: before[caller].replace(b"boundary(value)", b"boundary(value + 1)")}
    scope = _bounded_scope(before, after, read_policy(after))
    assert scope["changed_functions"] == ["package.nested.caller.decision"]
    assert [item["name"] for item in scope["functions"]] == sorted(
        [helper + ".boundary", "package.nested.caller.decision"]
    )


def test_renamed_module_import_keeps_its_conservative_module_scope() -> None:
    before = _files()
    before["src/helper.py"] = (
        b"def boundary(value):\n    return value > 0\ndef secondary(value):\n    return value + 1\n"
    )
    before["src/subject.py"] = (
        b"import helper as decision_policy\n"
        b"def decision(value):\n    return decision_policy.boundary(value)\n"
        b"def unrelated(value):\n    return value * 2\n"
    )
    after = {
        **before,
        "src/subject.py": before["src/subject.py"].replace(b"boundary(value)", b"boundary(value + 1)"),
    }
    scope = _bounded_scope(before, after, read_policy(after))
    assert scope["changed_functions"] == ["subject.decision"]
    assert [item["name"] for item in scope["functions"]] == [
        "helper.boundary",
        "helper.secondary",
        "subject.decision",
    ]
