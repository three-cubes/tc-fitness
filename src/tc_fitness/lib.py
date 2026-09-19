"""Shared helpers for architecture-fitness checks across Three Cubes repos.

This module unions two independently-grown libraries into one source:

- **kairix** ``scripts/checks/_arch_lib.py`` — hard-gating helpers:
  :func:`gate`, :func:`python_files`, :func:`main_entry`, :func:`repo_relative`,
  and the :data:`REPO_ROOT` anchor. Each check reports a set of offending
  paths and fails whenever violations exist.

- **tc-agent-zone** ``scripts/checks/_lib/__init__.py`` — agent-actionable
  emit/YAML helpers: :func:`actionable`, :func:`emit_failures`, :func:`emit_pass`,
  :func:`load_yaml`, :func:`missing_keys`. These shape FAIL/PASS output per the
  canonical ``<what>; fix: <fix>; next: <nxt>`` form and load YAML with a
  ``(data, error)`` contract.

Both call patterns are preserved exactly so the ~80 kairix checks and ~95
tc-agent-zone checks can adopt this package without rewriting their call sites.

REPO_ROOT note
--------------
The original kairix module derived ``REPO_ROOT`` from its own file location
(``parent.parent.parent``). Inside an installed package that anchor is wrong,
so :data:`REPO_ROOT` here resolves from the current working directory, which is
the repo root when checks run from ``scripts/safe-commit.sh`` / pre-commit / CI.
Every gating helper also accepts an explicit ``repo_root`` argument; callers that
need isolation (tests, monorepo sub-trees) pass it directly rather than relying
on the default.
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# kairix _arch_lib surface — hard gating
# ---------------------------------------------------------------------------

# Anchored to CWD so an installed package gates the *consumer* repo, not the
# site-packages tree. Checks run from the repo root, so this is correct in the
# pre-commit / safe-commit / CI invocation paths. Pass repo_root= explicitly
# anywhere that assumption does not hold.
REPO_ROOT = Path.cwd()

_RED = "\033[0;31m"
_GREEN = "\033[0;32m"
_RESET = "\033[0m"


def gate(
    name: str,
    current: set[Path],
    remediation: str,
    *,
    repo_root: Path | None = None,
) -> int:
    """Fail when any current path violates the rule; print + return exit code.

    Args:
        name: short rule name used in messages.
        current: set of repo-relative (or absolute under ``repo_root``) Paths
            with the violation.
        remediation: operator-actionable remediation hint.
        repo_root: repo root used to relativise
            absolute paths. Defaults to :data:`REPO_ROOT` (the CWD).

    Returns:
        ``0`` if there are no violations; ``1`` otherwise.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    current_rel = {p.relative_to(root) if p.is_absolute() else p for p in current}
    violations = sorted(current_rel)

    if violations:
        from tc_fitness.check_evidence import report_finding

        for path in violations:
            report_finding(name, path.as_posix(), remediation)
        print(f"{_RED}FAIL [arch:{name}]{_RESET} — violation(s) found:")
        for p in violations:
            print(f"  {p}")
        print()
        print(remediation)
        return 1
    print(f"{_GREEN}ok [arch:{name}]{_RESET} — clean.")
    return 0


def gate_keys(
    name: str,
    current: set[str],
    remediation: str,
    *,
    repo_root: Path | None = None,
) -> int:
    """Fail when any current opaque key violates the rule."""
    del repo_root
    violations = sorted(current)
    if violations:
        print(f"{_RED}FAIL [arch:{name}]{_RESET} — violation(s) found:")
        for key in violations:
            print(f"  {key}")
        print()
        print(remediation)
        return 1
    print(f"{_GREEN}ok [arch:{name}]{_RESET} — clean.")
    return 0


def repo_relative(path: Path, *, repo_root: Path | None = None) -> Path:
    """Convert an absolute path under the repo root to a repo-relative Path."""
    root = repo_root if repo_root is not None else REPO_ROOT
    return path.resolve().relative_to(root)


def python_files(*roots: str, repo_root: Path | None = None) -> list[Path]:
    """Return all ``.py`` files under the given relative roots, skipping ``__pycache__``."""
    root = repo_root if repo_root is not None else REPO_ROOT
    out: list[Path] = []
    for rel in roots:
        root_path = root / rel
        if not root_path.exists():
            continue
        for p in root_path.rglob("*.py"):
            if "__pycache__" in p.parts:
                continue
            out.append(p)
    return out


def main_entry(
    check_fn: Callable[[Path], object] | object,
    name: str,
    remediation: str,
    *roots: str,
    repo_root: Path | None = None,
) -> int:
    """Scan ``roots``, call ``check_fn(path)`` on each ``.py`` file, gate on the union.

    ``check_fn`` returns either ``True`` (file has a violation) or a falsy value.
    """
    root = repo_root if repo_root is not None else REPO_ROOT
    violations: set[Path] = set()
    for path in python_files(*roots, repo_root=root):
        if callable(check_fn) and check_fn(path):
            violations.add(repo_relative(path, repo_root=root))
    return gate(name, violations, remediation, repo_root=root)


# ---------------------------------------------------------------------------
# tc-agent-zone _lib surface — agent-actionable emit / YAML
# ---------------------------------------------------------------------------


def actionable(what: str, fix: str, nxt: str, run: str | None = None) -> str:
    """Format an agent-actionable single-line failure.

    Shape (default): ``<what>; fix: <fix>; next: <nxt>``. Standardising the shape
    lets the actionable-feedback parser keep up without chasing each call site's
    bespoke formatting.

    When ``run`` is supplied, a third ``; run: <run>`` marker is appended,
    yielding the 3-marker ``<what>; fix: <fix>; next: <nxt>; run: <run>`` form
    that tc-agent-zone's 59 fix/next/run checks emit. ``run`` defaults to
    ``None``, so the 2-marker v0.1.0 output is byte-identical for every existing
    call site.
    """
    base = f"{what}; fix: {fix}; next: {nxt}"
    if run is None:
        return base
    return f"{base}; run: {run}"


def remediation(
    fix: str,
    nxt: str,
    run: str,
    *,
    passing: str | None = None,
    forbidden: str | None = None,
) -> str:
    """Format the multiline ``fix:`` / ``next:`` / ``run:`` remediation block.

    The F21-shape block tc-agent-zone's 30 checks emit alongside a failure: the
    three action markers on their own lines, optionally followed by a ``Pass``
    example and a ``Forbidden`` example. Returns the joined block as one string
    (no trailing newline), ready to ``print()``.

    Example output::

        fix: redact the secret before logging
        next: re-run the check
        run: python scripts/checks/check_f15.py
        Pass: logger.info("token redacted")
        Forbidden: logger.info(f"token={token}")

    Args:
        fix: the corrective action.
        nxt: the follow-up step after fixing.
        run: the exact command to re-verify.
        passing: optional Pass-example line (omitted when ``None``).
        forbidden: optional Forbidden-example line (omitted when ``None``).
    """
    lines = [f"fix: {fix}", f"next: {nxt}", f"run: {run}"]
    if passing is not None:
        lines.append(f"Pass: {passing}")
    if forbidden is not None:
        lines.append(f"Forbidden: {forbidden}")
    return "\n".join(lines)


def emit_failures(check_name: str, fails: list[str], stream: Any = None) -> None:
    """Emit the canonical FAIL banner + bulleted failure list.

    Defaults to ``sys.stderr`` (resolved at call time so tests can capture it).
    """
    out = stream if stream is not None else sys.stderr
    print(f"FAIL {check_name} ({len(fails)} violations)", file=out)
    for f in fails:
        print(f"  - {f}", file=out)


def emit_pass(message: str, stream: Any = None) -> None:
    """Emit the canonical PASS line for a check (defaults to ``sys.stdout``)."""
    out = stream if stream is not None else sys.stdout
    print(message, file=out)


def load_yaml(
    path: Path, *, reject_duplicate_keys: bool = False, source: bytes | None = None
) -> tuple[Any, str | None]:
    """Load YAML returning ``(data, error)``.

    Returns ``({} or scalar, None)`` on success or ``(None, error-str)`` when
    the required dependency is unavailable or parsing fails.
    ``reject_duplicate_keys`` selects the strict mapping loader used by
    schema-bound manifest consumers, where last-write-wins would hide a
    conflicting declaration.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML missing"

    try:
        text = path.read_text() if source is None else source.decode("utf-8")
        if not reject_duplicate_keys:
            return yaml.safe_load(text) or {}, None

        def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
            loader.flatten_mapping(node)
            mapping: dict[Any, Any] = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in mapping
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"unhashable YAML mapping key: {key!r}",
                        key_node.start_mark,
                    ) from exc
                if duplicate:
                    raise yaml.constructor.ConstructorError(
                        "while constructing a mapping",
                        node.start_mark,
                        f"duplicate YAML mapping key: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = loader.construct_object(value_node, deep=deep)
            return mapping

        strict_loader = type(
            "StrictLoader",
            (yaml.SafeLoader,),
            {"construct_mapping": construct_mapping},
        )
        loader = strict_loader(text)
        try:
            return loader.get_single_data() or {}, None
        finally:
            loader.dispose()
    except (yaml.YAMLError, UnicodeError) as e:
        return None, f"invalid YAML — {e}"


def missing_keys(parsed: dict[str, Any], required: tuple[str, ...]) -> list[str]:
    """Return the subset of ``required`` keys that are absent in ``parsed``."""
    return [k for k in required if k not in parsed]


__all__ = [
    "REPO_ROOT",
    "actionable",
    "emit_failures",
    "emit_pass",
    "gate",
    "gate_keys",
    "load_yaml",
    "main_entry",
    "missing_keys",
    "python_files",
    "remediation",
    "repo_relative",
]
