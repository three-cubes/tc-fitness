"""Immutable Git inputs and conservative changed-function dependency closure."""

from __future__ import annotations

import ast
import copy
import hashlib
import io
import re
import tarfile
import tomllib
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from tc_fitness.check_contract_execution import payload_digest
from tc_fitness.runner import run_bounded_process


class MutationError(ValueError):
    """Mutation evidence cannot establish the required candidate claim."""

    def __init__(self, message: str, code: str = "invalid-evidence") -> None:
        super().__init__(message)
        self.code = code


def digest_bytes(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def git_bytes(root: Path, *args: str) -> bytes:
    result = run_bounded_process(["git", *args], cwd=root)
    if result.returncode:
        raise MutationError(f"Git identity unavailable: {' '.join(args[:2])}")
    return result.stdout


def candidate_archives(root: Path, base: str, head: str) -> tuple[bytes, bytes]:
    """Resolve immutable identities and reject any different or dirty checkout."""
    for commit in (base, head):
        if re.fullmatch(r"[0-9a-f]{40}(?:[0-9a-f]{24})?", commit) is None:
            raise MutationError("base and head must be full immutable commit SHAs")
        if git_bytes(root, "rev-parse", f"{commit}^{{commit}}").decode().strip() != commit:
            raise MutationError("commit identity mismatch")
    if git_bytes(root, "rev-parse", "HEAD").decode().strip() != head:
        raise MutationError("head does not identify the current checkout")
    git_bytes(root, "merge-base", "--is-ancestor", base, head)
    if git_bytes(root, "status", "--porcelain", "--untracked-files=no"):
        raise MutationError("candidate checkout has tracked modifications")
    archives = (git_bytes(root, "archive", base), git_bytes(root, "archive", head))
    for commit, archive in zip((base, head), archives, strict=True):
        _validate_archive(root, commit, archive)
    return archives


def _validate_archive(root: Path, commit: str, archive: bytes) -> None:
    """Git export attributes must not omit or rewrite tracked candidate bytes."""
    files = archive_files(archive)
    objects = {}
    for record in git_bytes(root, "ls-tree", "-r", "-z", commit).split(b"\0"):
        if not record:
            continue
        metadata, raw_path = record.split(b"\t", 1)
        mode, kind, object_id = metadata.split()
        if mode not in {b"100644", b"100755"} or kind != b"blob":
            raise MutationError("candidate archive requires regular tracked files")
        objects[raw_path.decode("utf-8")] = object_id.decode("ascii")
    if files.keys() != objects.keys():
        raise MutationError("candidate archive omits tracked inputs; export-ignore is forbidden")
    for path, raw in files.items():
        blob = b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw
        algorithm = "sha1" if len(objects[path]) == 40 else "sha256"
        actual = hashlib.new(algorithm, blob, usedforsecurity=False).hexdigest()
        if actual != objects[path]:
            raise MutationError("candidate archive rewrites tracked inputs; export-subst is forbidden")


def archive_files(archive: bytes) -> dict[str, bytes]:
    files: dict[str, bytes] = {}
    with tarfile.open(fileobj=io.BytesIO(archive)) as stream:
        for member in stream.getmembers():
            path = PurePosixPath(member.name)
            if path.is_absolute() or ".." in path.parts or "\\" in member.name:
                raise MutationError("unsafe path in candidate archive")
            if member.isdir():
                continue
            if not member.isfile():
                raise MutationError("candidate mutation snapshots require regular tracked files")
            source = stream.extractfile(member)
            if source is None:
                raise MutationError("missing archived source")
            files[path.as_posix()] = source.read()
    return files


def archive_executables(archive: bytes) -> list[str]:
    """Retain Git's executable bit alongside the already validated archive paths."""
    with tarfile.open(fileobj=io.BytesIO(archive)) as stream:
        return sorted(
            member.name for member in stream.getmembers() if member.isfile() and member.mode & 0o111
        )


#: Bounds on the derived campaign budget. The floor keeps a fast machine with a
#: small change from being handed an unusable budget; the ceiling is what still
#: catches a genuine hang, which is the one thing an absolute bound was good at.
BUDGET_FIELDS = ("baseline_multiplier", "per_function_multiplier", "floor_seconds", "ceiling_seconds")
BUDGET_CEILING = 3600


def _validate_budget(value: Any) -> None:
    """Reject a budget that is not a complete, ordered, positive specification."""
    if not isinstance(value, dict) or set(value) != set(BUDGET_FIELDS):
        raise MutationError(
            "budget requires exactly " + ", ".join(BUDGET_FIELDS) + "; "
            "fix: declare each field in mutation.toml; next: re-run the mutation check"
        )
    for field in BUDGET_FIELDS:
        entry = value[field]
        if type(entry) not in (int, float) or entry <= 0:
            raise MutationError(f"budget.{field} must be a positive number")
    if value["floor_seconds"] > value["ceiling_seconds"]:
        raise MutationError("budget.floor_seconds cannot exceed budget.ceiling_seconds")
    if value["ceiling_seconds"] > BUDGET_CEILING:
        raise MutationError(f"budget.ceiling_seconds must not exceed {BUDGET_CEILING}")


def derive_budget(budget: dict[str, Any], *, baseline_seconds: float, changed_functions: int) -> int:
    """Return the campaign budget for this machine and this change.

    An absolute bound conflates two independent things: how much work a campaign
    is, and how fast the machine running it is. A single number can only ever be
    right on the machine it was tuned on, and it goes wrong silently — a campaign
    cut off before it evaluates a mutant reports the same way whether the budget
    was too small or the code untested.

    The campaign costs roughly one unmutated run per mutant, and the mutants come
    from the changed functions, so both terms are measured rather than guessed:
    ``baseline_seconds`` is this machine's cost for one scoped run, and
    ``changed_functions`` is how much this particular change demands. The result
    is clamped, and the caller records all of it in the receipt — a derived bound
    that is not recorded is less accountable than the constant it replaced.
    """
    per_function = float(budget["per_function_multiplier"])
    raw = baseline_seconds * (float(budget["baseline_multiplier"]) + per_function * changed_functions)
    clamped = min(max(raw, float(budget["floor_seconds"])), float(budget["ceiling_seconds"]))
    return round(clamped)


def read_policy(files: dict[str, bytes]) -> dict[str, Any]:
    try:
        value = tomllib.loads(files["mutation.toml"].decode("utf-8"))
    except (KeyError, ValueError) as exc:
        raise MutationError("tracked mutation.toml policy is required") from exc
    if set(value) != {"schema", "source_roots", "tests", "budget", "max_mutants"}:
        raise MutationError("mutation policy requires exact fields; exemptions are not supported")
    if value["schema"] != "tc.fitness/mutation-policy/v1":
        raise MutationError("unknown mutation policy schema")
    for key in ("source_roots", "tests"):
        paths = value[key]
        if not isinstance(paths, list) or not paths or len(paths) != len(set(paths)):
            raise MutationError(f"{key} must be a nonempty unique path list")
        for path in paths:
            if (
                not isinstance(path, str)
                or not path
                or path.startswith("-")
                or PurePosixPath(path).is_absolute()
                or ".." in PurePosixPath(path).parts
                or "\\" in path
                or any(char in path for char in "*?\n\r")
            ):
                raise MutationError(f"{key} must contain literal repository-relative paths")
            if not any(name == path or name.startswith(path.rstrip("/") + "/") for name in files):
                raise MutationError(f"policy path has no tracked inputs: {path}")
    if type(value["max_mutants"]) is not int or not 1 <= value["max_mutants"] <= 100000:
        raise MutationError("max_mutants must be bounded between 1 and 100000")
    _validate_budget(value["budget"])
    if any(
        root == test or root.startswith(test + "/") or test.startswith(root + "/")
        for root in value["source_roots"]
        for test in value["tests"]
    ):
        raise MutationError("production roots and test paths must be disjoint")
    return value


@dataclass(frozen=True)
class Function:
    name: str
    path: str
    node: ast.FunctionDef | ast.AsyncFunctionDef
    selector: str


def definition_digest(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    """Bind the executable definition, independently of generated trampoline names."""
    normalised = copy.deepcopy(node)
    normalised.name = "subject"
    normalised.decorator_list = []
    return payload_digest(ast.dump(normalised))


def _functions(
    files: dict[str, bytes], roots: list[str]
) -> tuple[dict[str, Function], dict[str, ast.Module]]:
    functions: dict[str, Function] = {}
    modules: dict[str, ast.Module] = {}
    for path, raw in sorted(files.items()):
        if not path.endswith(".py") or not any(path.startswith(root.rstrip("/") + "/") for root in roots):
            continue
        if re.search(rb"pragma\s*:\s*no\s+mutate", raw, re.IGNORECASE):
            raise MutationError(f"mutation suppression is forbidden: {path}")
        try:
            tree = ast.parse(raw, filename=path)
        except (SyntaxError, ValueError) as exc:
            raise MutationError(f"production Python cannot be parsed: {path}") from exc
        module = path.removesuffix(".py").replace("/", ".").removeprefix("src.")
        module = module.removesuffix(".__init__")
        modules[module] = tree
        for node in tree.body:
            candidates: list[tuple[ast.stmt, str | None]] = [(node, None)]
            if isinstance(node, ast.ClassDef):
                candidates = [(child, node.name) for child in node.body]
            for child, owner in candidates:
                if isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef):
                    suffix = f"{owner}.{child.name}" if owner else child.name
                    name = f"{module}.{suffix}"
                    mangled = f"xǁ{owner}ǁ{child.name}" if owner else f"x_{child.name}"
                    functions[name] = Function(name, path, child, f"{module}.{mangled}__mutmut_*")
    return functions, modules


def select_scope(
    base_files: dict[str, bytes], head_files: dict[str, bytes], policy: dict[str, Any], *, broad: bool = False
) -> dict[str, Any]:
    """Select changed functions and transitive statically referenced production functions.

    Module-level changes include every function in the affected module.
    Attribute dispatch is conservatively matched by method name; dynamic import
    causes whole-package closure rather than silently omitting dependencies.
    """
    functions, modules = _functions(head_files, policy["source_roots"])
    old, old_modules = _functions(base_files, policy["source_roots"])
    changed = {
        name
        for name, item in functions.items()
        if name not in old or ast.dump(item.node) != ast.dump(old[name].node)
    }
    changed_modules = set(old_modules) ^ set(modules)
    changed_modules.update(old[name].selector.rsplit(".x", 1)[0] for name in old.keys() - functions.keys())
    for name, tree in modules.items():
        outside = ast.Module(
            body=[node for node in tree.body if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)],
            type_ignores=[],
        )
        previous = old_modules.get(name)
        before = (
            ast.Module(
                body=[
                    node
                    for node in previous.body
                    if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
                ],
                type_ignores=[],
            )
            if previous
            else None
        )
        if before is None or ast.dump(outside) != ast.dump(before):
            changed_modules.add(name)
    for name, item in functions.items():
        module = item.selector.rsplit(".x", 1)[0]
        if module in changed_modules:
            changed.add(name)
        tree = modules[module]
        imports = {alias.name for node in tree.body if isinstance(node, ast.Import) for alias in node.names}
        imports.update(node.module for node in tree.body if isinstance(node, ast.ImportFrom) and node.module)
        if imports & changed_modules:
            changed.add(name)
    selected = set(functions) if broad else set(changed)
    queue = list(selected)
    while queue:
        name = queue.pop()
        item = functions[name]
        module = item.selector.rsplit(".x", 1)[0]
        tree = modules[module]
        aliases: dict[str, str] = {}
        for node in tree.body:
            if isinstance(node, ast.ImportFrom) and node.module:
                prefix = node.module
                if node.level:
                    prefix = ".".join(module.split(".")[: -node.level]) + "." + prefix
                aliases.update(
                    {alias.asname or alias.name: prefix + "." + alias.name for alias in node.names}
                )
            elif isinstance(node, ast.Import):
                aliases.update({alias.asname or alias.name: alias.name for alias in node.names})
        dependencies: set[str] = set()
        global_values: dict[str, ast.expr] = {}
        for statement in tree.body:
            if isinstance(statement, ast.Assign):
                for target in statement.targets:
                    if isinstance(target, ast.Name):
                        global_values[target.id] = statement.value
            elif (
                isinstance(statement, ast.AnnAssign)
                and isinstance(statement.target, ast.Name)
                and statement.value
            ):
                global_values[statement.target.id] = statement.value
        pending = list(ast.walk(item.node))
        visited_globals: set[str] = set()
        while pending:
            expression = pending.pop()
            if isinstance(expression, ast.Name):
                resolved = aliases.get(expression.id, module + "." + expression.id)
                direct = {
                    candidate
                    for candidate in functions
                    if candidate == resolved or candidate.startswith(resolved + ".")
                }
                dependencies.update(direct)
                if expression.id in global_values and expression.id not in visited_globals:
                    visited_globals.add(expression.id)
                    pending.extend(ast.walk(global_values[expression.id]))
                if expression.id in aliases and not direct:
                    package = resolved.split(".")[0]
                    dependencies.update(
                        candidate for candidate in functions if candidate.startswith(package + ".")
                    )
                if expression.id in {"__import__", "getattr", "globals", "locals", "eval", "exec"}:
                    dependencies.update(functions)
            if isinstance(expression, ast.Attribute):
                dependencies.update(
                    candidate for candidate in functions if candidate.endswith("." + expression.attr)
                )
                if expression.attr == "import_module":
                    dependencies.update(functions)
        for dependency in dependencies - selected:
            selected.add(dependency)
            queue.append(dependency)
    return {
        "mode": "broad" if broad else "changed",
        "required": bool(functions) if broad else bool(changed or changed_modules),
        "changed_functions": sorted(changed),
        "functions": [
            {
                "name": name,
                "path": functions[name].path,
                "selector": functions[name].selector,
                "definition_digest": definition_digest(functions[name].node),
            }
            for name in sorted(selected)
        ],
        "policy_digest": payload_digest(policy),
    }
