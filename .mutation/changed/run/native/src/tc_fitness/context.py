"""Shared per-run state for the in-process fitness runner.

Motivation
----------
A catalogue-driven runner that spawns one cold subprocess per rule re-parses
the same source trees dozens of times — every AST-based check re-``ast.parse``s
the files it walks, and every process re-imports the check library. The
dominant cost of a full run is cold-start + redundant parsing.

:class:`CheckContext` is built ONCE per process and shared across every
in-process check:

* a ``python_files(*roots)`` index — each relevant tree is ``rglob``-d once;
* an ``ast.parse`` cache keyed by ``(filename, source-text)`` so every file is
  parsed AT MOST ONCE per run, no matter how many rules inspect it;
* an ``ast.walk`` cache keyed by tree identity so a parsed tree is traversed
  once and the node list shared;
* a source-text cache for the regex / text checks.

Parse-once mechanism
--------------------
Rather than thread a context object through every AST call site (high blast
radius, high risk of a verdict-changing edit), :meth:`install` swaps
``ast.parse`` / ``ast.walk`` for memoising wrappers for the lifetime of an
in-process run. The cache key for parsing is ``(filename, source-text)``:
identical source for the same file yields the identical tree, and the checks
only ever read / walk trees (never mutate them), so sharing one parsed tree
across rules is observably identical to re-parsing. The real functions are
restored on context exit, so the patch never leaks past a run.

The cache key folds in the source TEXT (not just a stat) so a file edited
mid-run — or two distinct files that happen to share a stat — can never serve
a stale tree.
"""

from __future__ import annotations

import ast
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

# The pristine stdlib parser + walker, captured at import time. Every cached
# parse / walk delegates to THESE, never to the (possibly-already-patched)
# ``ast.parse`` / ``ast.walk`` names, so nesting installs can't recurse.
_REAL_AST_PARSE = ast.parse
_REAL_AST_WALK = ast.walk


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_xǁCheckContextǁ__init____mutmut: MutantDict = {}  # type: ignore
mutants_xǁCheckContextǁpython_files__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCheckContextǁsource_for__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCheckContextǁtree_for__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCheckContextǁparse__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCheckContextǁwalk__mutmut: MutantDict = {}  # type: ignore


class CheckContext:
    """One-per-run shared index + parse/source caches.

    The runner constructs a single ``CheckContext`` and installs its parse
    cache for the duration of an ``--all`` / ``--staged`` / ``--gate`` run.
    Accessors are intentionally small and read-only; the heavy lifting is the
    ``ast.parse`` / ``ast.walk`` memoisation installed via :meth:`install`.
    """

    @_mutmut_mutated(mutants_xǁCheckContextǁ__init____mutmut)
    def __init__(self, repo_root: Path | None = None) -> None:
        self._repo_root = (repo_root if repo_root is not None else Path.cwd()).resolve()
        # filename(str) -> (source-text -> parsed tree). Two-level so a file
        # rewritten between parses keys on its new text, never a stale tree.
        self._tree_cache: dict[str, dict[str, ast.AST]] = {}
        self._source_cache: dict[Path, str | None] = {}
        self._files_cache: dict[tuple[str, ...], tuple[Path, ...]] = {}
        # id(tree) -> fully-materialised node list (the ``ast.walk`` order).
        # Keyed by object identity: the parse cache returns the SAME tree
        # object for the same file, so every rule's walk of that tree reuses
        # one traversal. Cleared with the context (no cross-run leak).
        self._walk_cache: dict[int, list[ast.AST]] = {}
        # Instrumentation: real parses (cache misses) vs cache hits. The
        # parse-once test asserts misses <= distinct-files and hits > 0.
        self.parse_misses = 0
        self.parse_hits = 0
        self.walk_misses = 0
        self.walk_hits = 0

    def xǁCheckContextǁ__init____mutmut_orig(self, repo_root: Path | None = None) -> None:
        self._repo_root = (repo_root if repo_root is not None else Path.cwd()).resolve()
        # filename(str) -> (source-text -> parsed tree). Two-level so a file
        # rewritten between parses keys on its new text, never a stale tree.
        self._tree_cache: dict[str, dict[str, ast.AST]] = {}
        self._source_cache: dict[Path, str | None] = {}
        self._files_cache: dict[tuple[str, ...], tuple[Path, ...]] = {}
        # id(tree) -> fully-materialised node list (the ``ast.walk`` order).
        # Keyed by object identity: the parse cache returns the SAME tree
        # object for the same file, so every rule's walk of that tree reuses
        # one traversal. Cleared with the context (no cross-run leak).
        self._walk_cache: dict[int, list[ast.AST]] = {}
        # Instrumentation: real parses (cache misses) vs cache hits. The
        # parse-once test asserts misses <= distinct-files and hits > 0.
        self.parse_misses = 0
        self.parse_hits = 0
        self.walk_misses = 0
        self.walk_hits = 0

    def xǁCheckContextǁ__init____mutmut_1(self, repo_root: Path | None = None) -> None:
        self._repo_root = None
        # filename(str) -> (source-text -> parsed tree). Two-level so a file
        # rewritten between parses keys on its new text, never a stale tree.
        self._tree_cache: dict[str, dict[str, ast.AST]] = {}
        self._source_cache: dict[Path, str | None] = {}
        self._files_cache: dict[tuple[str, ...], tuple[Path, ...]] = {}
        # id(tree) -> fully-materialised node list (the ``ast.walk`` order).
        # Keyed by object identity: the parse cache returns the SAME tree
        # object for the same file, so every rule's walk of that tree reuses
        # one traversal. Cleared with the context (no cross-run leak).
        self._walk_cache: dict[int, list[ast.AST]] = {}
        # Instrumentation: real parses (cache misses) vs cache hits. The
        # parse-once test asserts misses <= distinct-files and hits > 0.
        self.parse_misses = 0
        self.parse_hits = 0
        self.walk_misses = 0
        self.walk_hits = 0

    def xǁCheckContextǁ__init____mutmut_2(self, repo_root: Path | None = None) -> None:
        self._repo_root = (repo_root if repo_root is None else Path.cwd()).resolve()
        # filename(str) -> (source-text -> parsed tree). Two-level so a file
        # rewritten between parses keys on its new text, never a stale tree.
        self._tree_cache: dict[str, dict[str, ast.AST]] = {}
        self._source_cache: dict[Path, str | None] = {}
        self._files_cache: dict[tuple[str, ...], tuple[Path, ...]] = {}
        # id(tree) -> fully-materialised node list (the ``ast.walk`` order).
        # Keyed by object identity: the parse cache returns the SAME tree
        # object for the same file, so every rule's walk of that tree reuses
        # one traversal. Cleared with the context (no cross-run leak).
        self._walk_cache: dict[int, list[ast.AST]] = {}
        # Instrumentation: real parses (cache misses) vs cache hits. The
        # parse-once test asserts misses <= distinct-files and hits > 0.
        self.parse_misses = 0
        self.parse_hits = 0
        self.walk_misses = 0
        self.walk_hits = 0

    def xǁCheckContextǁ__init____mutmut_3(self, repo_root: Path | None = None) -> None:
        self._repo_root = (repo_root if repo_root is not None else Path.cwd()).resolve()
        # filename(str) -> (source-text -> parsed tree). Two-level so a file
        # rewritten between parses keys on its new text, never a stale tree.
        self._tree_cache: dict[str, dict[str, ast.AST]] = None
        self._source_cache: dict[Path, str | None] = {}
        self._files_cache: dict[tuple[str, ...], tuple[Path, ...]] = {}
        # id(tree) -> fully-materialised node list (the ``ast.walk`` order).
        # Keyed by object identity: the parse cache returns the SAME tree
        # object for the same file, so every rule's walk of that tree reuses
        # one traversal. Cleared with the context (no cross-run leak).
        self._walk_cache: dict[int, list[ast.AST]] = {}
        # Instrumentation: real parses (cache misses) vs cache hits. The
        # parse-once test asserts misses <= distinct-files and hits > 0.
        self.parse_misses = 0
        self.parse_hits = 0
        self.walk_misses = 0
        self.walk_hits = 0

    def xǁCheckContextǁ__init____mutmut_4(self, repo_root: Path | None = None) -> None:
        self._repo_root = (repo_root if repo_root is not None else Path.cwd()).resolve()
        # filename(str) -> (source-text -> parsed tree). Two-level so a file
        # rewritten between parses keys on its new text, never a stale tree.
        self._tree_cache: dict[str, dict[str, ast.AST]] = {}
        self._source_cache: dict[Path, str | None] = None
        self._files_cache: dict[tuple[str, ...], tuple[Path, ...]] = {}
        # id(tree) -> fully-materialised node list (the ``ast.walk`` order).
        # Keyed by object identity: the parse cache returns the SAME tree
        # object for the same file, so every rule's walk of that tree reuses
        # one traversal. Cleared with the context (no cross-run leak).
        self._walk_cache: dict[int, list[ast.AST]] = {}
        # Instrumentation: real parses (cache misses) vs cache hits. The
        # parse-once test asserts misses <= distinct-files and hits > 0.
        self.parse_misses = 0
        self.parse_hits = 0
        self.walk_misses = 0
        self.walk_hits = 0

    def xǁCheckContextǁ__init____mutmut_5(self, repo_root: Path | None = None) -> None:
        self._repo_root = (repo_root if repo_root is not None else Path.cwd()).resolve()
        # filename(str) -> (source-text -> parsed tree). Two-level so a file
        # rewritten between parses keys on its new text, never a stale tree.
        self._tree_cache: dict[str, dict[str, ast.AST]] = {}
        self._source_cache: dict[Path, str | None] = {}
        self._files_cache: dict[tuple[str, ...], tuple[Path, ...]] = None
        # id(tree) -> fully-materialised node list (the ``ast.walk`` order).
        # Keyed by object identity: the parse cache returns the SAME tree
        # object for the same file, so every rule's walk of that tree reuses
        # one traversal. Cleared with the context (no cross-run leak).
        self._walk_cache: dict[int, list[ast.AST]] = {}
        # Instrumentation: real parses (cache misses) vs cache hits. The
        # parse-once test asserts misses <= distinct-files and hits > 0.
        self.parse_misses = 0
        self.parse_hits = 0
        self.walk_misses = 0
        self.walk_hits = 0

    def xǁCheckContextǁ__init____mutmut_6(self, repo_root: Path | None = None) -> None:
        self._repo_root = (repo_root if repo_root is not None else Path.cwd()).resolve()
        # filename(str) -> (source-text -> parsed tree). Two-level so a file
        # rewritten between parses keys on its new text, never a stale tree.
        self._tree_cache: dict[str, dict[str, ast.AST]] = {}
        self._source_cache: dict[Path, str | None] = {}
        self._files_cache: dict[tuple[str, ...], tuple[Path, ...]] = {}
        # id(tree) -> fully-materialised node list (the ``ast.walk`` order).
        # Keyed by object identity: the parse cache returns the SAME tree
        # object for the same file, so every rule's walk of that tree reuses
        # one traversal. Cleared with the context (no cross-run leak).
        self._walk_cache: dict[int, list[ast.AST]] = None
        # Instrumentation: real parses (cache misses) vs cache hits. The
        # parse-once test asserts misses <= distinct-files and hits > 0.
        self.parse_misses = 0
        self.parse_hits = 0
        self.walk_misses = 0
        self.walk_hits = 0

    def xǁCheckContextǁ__init____mutmut_7(self, repo_root: Path | None = None) -> None:
        self._repo_root = (repo_root if repo_root is not None else Path.cwd()).resolve()
        # filename(str) -> (source-text -> parsed tree). Two-level so a file
        # rewritten between parses keys on its new text, never a stale tree.
        self._tree_cache: dict[str, dict[str, ast.AST]] = {}
        self._source_cache: dict[Path, str | None] = {}
        self._files_cache: dict[tuple[str, ...], tuple[Path, ...]] = {}
        # id(tree) -> fully-materialised node list (the ``ast.walk`` order).
        # Keyed by object identity: the parse cache returns the SAME tree
        # object for the same file, so every rule's walk of that tree reuses
        # one traversal. Cleared with the context (no cross-run leak).
        self._walk_cache: dict[int, list[ast.AST]] = {}
        # Instrumentation: real parses (cache misses) vs cache hits. The
        # parse-once test asserts misses <= distinct-files and hits > 0.
        self.parse_misses = None
        self.parse_hits = 0
        self.walk_misses = 0
        self.walk_hits = 0

    def xǁCheckContextǁ__init____mutmut_8(self, repo_root: Path | None = None) -> None:
        self._repo_root = (repo_root if repo_root is not None else Path.cwd()).resolve()
        # filename(str) -> (source-text -> parsed tree). Two-level so a file
        # rewritten between parses keys on its new text, never a stale tree.
        self._tree_cache: dict[str, dict[str, ast.AST]] = {}
        self._source_cache: dict[Path, str | None] = {}
        self._files_cache: dict[tuple[str, ...], tuple[Path, ...]] = {}
        # id(tree) -> fully-materialised node list (the ``ast.walk`` order).
        # Keyed by object identity: the parse cache returns the SAME tree
        # object for the same file, so every rule's walk of that tree reuses
        # one traversal. Cleared with the context (no cross-run leak).
        self._walk_cache: dict[int, list[ast.AST]] = {}
        # Instrumentation: real parses (cache misses) vs cache hits. The
        # parse-once test asserts misses <= distinct-files and hits > 0.
        self.parse_misses = 1
        self.parse_hits = 0
        self.walk_misses = 0
        self.walk_hits = 0

    def xǁCheckContextǁ__init____mutmut_9(self, repo_root: Path | None = None) -> None:
        self._repo_root = (repo_root if repo_root is not None else Path.cwd()).resolve()
        # filename(str) -> (source-text -> parsed tree). Two-level so a file
        # rewritten between parses keys on its new text, never a stale tree.
        self._tree_cache: dict[str, dict[str, ast.AST]] = {}
        self._source_cache: dict[Path, str | None] = {}
        self._files_cache: dict[tuple[str, ...], tuple[Path, ...]] = {}
        # id(tree) -> fully-materialised node list (the ``ast.walk`` order).
        # Keyed by object identity: the parse cache returns the SAME tree
        # object for the same file, so every rule's walk of that tree reuses
        # one traversal. Cleared with the context (no cross-run leak).
        self._walk_cache: dict[int, list[ast.AST]] = {}
        # Instrumentation: real parses (cache misses) vs cache hits. The
        # parse-once test asserts misses <= distinct-files and hits > 0.
        self.parse_misses = 0
        self.parse_hits = None
        self.walk_misses = 0
        self.walk_hits = 0

    def xǁCheckContextǁ__init____mutmut_10(self, repo_root: Path | None = None) -> None:
        self._repo_root = (repo_root if repo_root is not None else Path.cwd()).resolve()
        # filename(str) -> (source-text -> parsed tree). Two-level so a file
        # rewritten between parses keys on its new text, never a stale tree.
        self._tree_cache: dict[str, dict[str, ast.AST]] = {}
        self._source_cache: dict[Path, str | None] = {}
        self._files_cache: dict[tuple[str, ...], tuple[Path, ...]] = {}
        # id(tree) -> fully-materialised node list (the ``ast.walk`` order).
        # Keyed by object identity: the parse cache returns the SAME tree
        # object for the same file, so every rule's walk of that tree reuses
        # one traversal. Cleared with the context (no cross-run leak).
        self._walk_cache: dict[int, list[ast.AST]] = {}
        # Instrumentation: real parses (cache misses) vs cache hits. The
        # parse-once test asserts misses <= distinct-files and hits > 0.
        self.parse_misses = 0
        self.parse_hits = 1
        self.walk_misses = 0
        self.walk_hits = 0

    def xǁCheckContextǁ__init____mutmut_11(self, repo_root: Path | None = None) -> None:
        self._repo_root = (repo_root if repo_root is not None else Path.cwd()).resolve()
        # filename(str) -> (source-text -> parsed tree). Two-level so a file
        # rewritten between parses keys on its new text, never a stale tree.
        self._tree_cache: dict[str, dict[str, ast.AST]] = {}
        self._source_cache: dict[Path, str | None] = {}
        self._files_cache: dict[tuple[str, ...], tuple[Path, ...]] = {}
        # id(tree) -> fully-materialised node list (the ``ast.walk`` order).
        # Keyed by object identity: the parse cache returns the SAME tree
        # object for the same file, so every rule's walk of that tree reuses
        # one traversal. Cleared with the context (no cross-run leak).
        self._walk_cache: dict[int, list[ast.AST]] = {}
        # Instrumentation: real parses (cache misses) vs cache hits. The
        # parse-once test asserts misses <= distinct-files and hits > 0.
        self.parse_misses = 0
        self.parse_hits = 0
        self.walk_misses = None
        self.walk_hits = 0

    def xǁCheckContextǁ__init____mutmut_12(self, repo_root: Path | None = None) -> None:
        self._repo_root = (repo_root if repo_root is not None else Path.cwd()).resolve()
        # filename(str) -> (source-text -> parsed tree). Two-level so a file
        # rewritten between parses keys on its new text, never a stale tree.
        self._tree_cache: dict[str, dict[str, ast.AST]] = {}
        self._source_cache: dict[Path, str | None] = {}
        self._files_cache: dict[tuple[str, ...], tuple[Path, ...]] = {}
        # id(tree) -> fully-materialised node list (the ``ast.walk`` order).
        # Keyed by object identity: the parse cache returns the SAME tree
        # object for the same file, so every rule's walk of that tree reuses
        # one traversal. Cleared with the context (no cross-run leak).
        self._walk_cache: dict[int, list[ast.AST]] = {}
        # Instrumentation: real parses (cache misses) vs cache hits. The
        # parse-once test asserts misses <= distinct-files and hits > 0.
        self.parse_misses = 0
        self.parse_hits = 0
        self.walk_misses = 1
        self.walk_hits = 0

    def xǁCheckContextǁ__init____mutmut_13(self, repo_root: Path | None = None) -> None:
        self._repo_root = (repo_root if repo_root is not None else Path.cwd()).resolve()
        # filename(str) -> (source-text -> parsed tree). Two-level so a file
        # rewritten between parses keys on its new text, never a stale tree.
        self._tree_cache: dict[str, dict[str, ast.AST]] = {}
        self._source_cache: dict[Path, str | None] = {}
        self._files_cache: dict[tuple[str, ...], tuple[Path, ...]] = {}
        # id(tree) -> fully-materialised node list (the ``ast.walk`` order).
        # Keyed by object identity: the parse cache returns the SAME tree
        # object for the same file, so every rule's walk of that tree reuses
        # one traversal. Cleared with the context (no cross-run leak).
        self._walk_cache: dict[int, list[ast.AST]] = {}
        # Instrumentation: real parses (cache misses) vs cache hits. The
        # parse-once test asserts misses <= distinct-files and hits > 0.
        self.parse_misses = 0
        self.parse_hits = 0
        self.walk_misses = 0
        self.walk_hits = None

    def xǁCheckContextǁ__init____mutmut_14(self, repo_root: Path | None = None) -> None:
        self._repo_root = (repo_root if repo_root is not None else Path.cwd()).resolve()
        # filename(str) -> (source-text -> parsed tree). Two-level so a file
        # rewritten between parses keys on its new text, never a stale tree.
        self._tree_cache: dict[str, dict[str, ast.AST]] = {}
        self._source_cache: dict[Path, str | None] = {}
        self._files_cache: dict[tuple[str, ...], tuple[Path, ...]] = {}
        # id(tree) -> fully-materialised node list (the ``ast.walk`` order).
        # Keyed by object identity: the parse cache returns the SAME tree
        # object for the same file, so every rule's walk of that tree reuses
        # one traversal. Cleared with the context (no cross-run leak).
        self._walk_cache: dict[int, list[ast.AST]] = {}
        # Instrumentation: real parses (cache misses) vs cache hits. The
        # parse-once test asserts misses <= distinct-files and hits > 0.
        self.parse_misses = 0
        self.parse_hits = 0
        self.walk_misses = 0
        self.walk_hits = 1

    # ── repo anchor ──────────────────────────────────────────────────────

    @property
    def repo_root(self) -> Path:
        """The repository root every scope/relativisation resolves against."""
        return self._repo_root

    # ── file index ───────────────────────────────────────────────────────

    @_mutmut_mutated(mutants_xǁCheckContextǁpython_files__mutmut)
    def python_files(self, *roots: str) -> tuple[Path, ...]:
        """Every ``.py`` file under each of ``roots`` (repo-relative dirs),
        skipping ``__pycache__``. Built once per distinct ``roots`` tuple and
        memoised — the same index the per-rule walks would each rebuild."""
        key = tuple(roots)
        cached = self._files_cache.get(key)
        if cached is not None:
            return cached
        out: list[Path] = []
        for rel in roots:
            base = self._repo_root / rel
            if not base.exists():
                continue
            for path in base.rglob("*.py"):
                if "__pycache__" in path.parts:
                    continue
                out.append(path)
        result = tuple(out)
        self._files_cache[key] = result
        return result

    # ── file index ───────────────────────────────────────────────────────

    def xǁCheckContextǁpython_files__mutmut_orig(self, *roots: str) -> tuple[Path, ...]:
        """Every ``.py`` file under each of ``roots`` (repo-relative dirs),
        skipping ``__pycache__``. Built once per distinct ``roots`` tuple and
        memoised — the same index the per-rule walks would each rebuild."""
        key = tuple(roots)
        cached = self._files_cache.get(key)
        if cached is not None:
            return cached
        out: list[Path] = []
        for rel in roots:
            base = self._repo_root / rel
            if not base.exists():
                continue
            for path in base.rglob("*.py"):
                if "__pycache__" in path.parts:
                    continue
                out.append(path)
        result = tuple(out)
        self._files_cache[key] = result
        return result

    # ── file index ───────────────────────────────────────────────────────

    def xǁCheckContextǁpython_files__mutmut_1(self, *roots: str) -> tuple[Path, ...]:
        """Every ``.py`` file under each of ``roots`` (repo-relative dirs),
        skipping ``__pycache__``. Built once per distinct ``roots`` tuple and
        memoised — the same index the per-rule walks would each rebuild."""
        key = None
        cached = self._files_cache.get(key)
        if cached is not None:
            return cached
        out: list[Path] = []
        for rel in roots:
            base = self._repo_root / rel
            if not base.exists():
                continue
            for path in base.rglob("*.py"):
                if "__pycache__" in path.parts:
                    continue
                out.append(path)
        result = tuple(out)
        self._files_cache[key] = result
        return result

    # ── file index ───────────────────────────────────────────────────────

    def xǁCheckContextǁpython_files__mutmut_2(self, *roots: str) -> tuple[Path, ...]:
        """Every ``.py`` file under each of ``roots`` (repo-relative dirs),
        skipping ``__pycache__``. Built once per distinct ``roots`` tuple and
        memoised — the same index the per-rule walks would each rebuild."""
        key = tuple(None)
        cached = self._files_cache.get(key)
        if cached is not None:
            return cached
        out: list[Path] = []
        for rel in roots:
            base = self._repo_root / rel
            if not base.exists():
                continue
            for path in base.rglob("*.py"):
                if "__pycache__" in path.parts:
                    continue
                out.append(path)
        result = tuple(out)
        self._files_cache[key] = result
        return result

    # ── file index ───────────────────────────────────────────────────────

    def xǁCheckContextǁpython_files__mutmut_3(self, *roots: str) -> tuple[Path, ...]:
        """Every ``.py`` file under each of ``roots`` (repo-relative dirs),
        skipping ``__pycache__``. Built once per distinct ``roots`` tuple and
        memoised — the same index the per-rule walks would each rebuild."""
        key = tuple(roots)
        cached = None
        if cached is not None:
            return cached
        out: list[Path] = []
        for rel in roots:
            base = self._repo_root / rel
            if not base.exists():
                continue
            for path in base.rglob("*.py"):
                if "__pycache__" in path.parts:
                    continue
                out.append(path)
        result = tuple(out)
        self._files_cache[key] = result
        return result

    # ── file index ───────────────────────────────────────────────────────

    def xǁCheckContextǁpython_files__mutmut_4(self, *roots: str) -> tuple[Path, ...]:
        """Every ``.py`` file under each of ``roots`` (repo-relative dirs),
        skipping ``__pycache__``. Built once per distinct ``roots`` tuple and
        memoised — the same index the per-rule walks would each rebuild."""
        key = tuple(roots)
        cached = self._files_cache.get(None)
        if cached is not None:
            return cached
        out: list[Path] = []
        for rel in roots:
            base = self._repo_root / rel
            if not base.exists():
                continue
            for path in base.rglob("*.py"):
                if "__pycache__" in path.parts:
                    continue
                out.append(path)
        result = tuple(out)
        self._files_cache[key] = result
        return result

    # ── file index ───────────────────────────────────────────────────────

    def xǁCheckContextǁpython_files__mutmut_5(self, *roots: str) -> tuple[Path, ...]:
        """Every ``.py`` file under each of ``roots`` (repo-relative dirs),
        skipping ``__pycache__``. Built once per distinct ``roots`` tuple and
        memoised — the same index the per-rule walks would each rebuild."""
        key = tuple(roots)
        cached = self._files_cache.get(key)
        if cached is None:
            return cached
        out: list[Path] = []
        for rel in roots:
            base = self._repo_root / rel
            if not base.exists():
                continue
            for path in base.rglob("*.py"):
                if "__pycache__" in path.parts:
                    continue
                out.append(path)
        result = tuple(out)
        self._files_cache[key] = result
        return result

    # ── file index ───────────────────────────────────────────────────────

    def xǁCheckContextǁpython_files__mutmut_6(self, *roots: str) -> tuple[Path, ...]:
        """Every ``.py`` file under each of ``roots`` (repo-relative dirs),
        skipping ``__pycache__``. Built once per distinct ``roots`` tuple and
        memoised — the same index the per-rule walks would each rebuild."""
        key = tuple(roots)
        cached = self._files_cache.get(key)
        if cached is not None:
            return cached
        out: list[Path] = None
        for rel in roots:
            base = self._repo_root / rel
            if not base.exists():
                continue
            for path in base.rglob("*.py"):
                if "__pycache__" in path.parts:
                    continue
                out.append(path)
        result = tuple(out)
        self._files_cache[key] = result
        return result

    # ── file index ───────────────────────────────────────────────────────

    def xǁCheckContextǁpython_files__mutmut_7(self, *roots: str) -> tuple[Path, ...]:
        """Every ``.py`` file under each of ``roots`` (repo-relative dirs),
        skipping ``__pycache__``. Built once per distinct ``roots`` tuple and
        memoised — the same index the per-rule walks would each rebuild."""
        key = tuple(roots)
        cached = self._files_cache.get(key)
        if cached is not None:
            return cached
        out: list[Path] = []
        for rel in roots:
            base = None
            if not base.exists():
                continue
            for path in base.rglob("*.py"):
                if "__pycache__" in path.parts:
                    continue
                out.append(path)
        result = tuple(out)
        self._files_cache[key] = result
        return result

    # ── file index ───────────────────────────────────────────────────────

    def xǁCheckContextǁpython_files__mutmut_8(self, *roots: str) -> tuple[Path, ...]:
        """Every ``.py`` file under each of ``roots`` (repo-relative dirs),
        skipping ``__pycache__``. Built once per distinct ``roots`` tuple and
        memoised — the same index the per-rule walks would each rebuild."""
        key = tuple(roots)
        cached = self._files_cache.get(key)
        if cached is not None:
            return cached
        out: list[Path] = []
        for rel in roots:
            base = self._repo_root * rel
            if not base.exists():
                continue
            for path in base.rglob("*.py"):
                if "__pycache__" in path.parts:
                    continue
                out.append(path)
        result = tuple(out)
        self._files_cache[key] = result
        return result

    # ── file index ───────────────────────────────────────────────────────

    def xǁCheckContextǁpython_files__mutmut_9(self, *roots: str) -> tuple[Path, ...]:
        """Every ``.py`` file under each of ``roots`` (repo-relative dirs),
        skipping ``__pycache__``. Built once per distinct ``roots`` tuple and
        memoised — the same index the per-rule walks would each rebuild."""
        key = tuple(roots)
        cached = self._files_cache.get(key)
        if cached is not None:
            return cached
        out: list[Path] = []
        for rel in roots:
            base = self._repo_root / rel
            if base.exists():
                continue
            for path in base.rglob("*.py"):
                if "__pycache__" in path.parts:
                    continue
                out.append(path)
        result = tuple(out)
        self._files_cache[key] = result
        return result

    # ── file index ───────────────────────────────────────────────────────

    def xǁCheckContextǁpython_files__mutmut_10(self, *roots: str) -> tuple[Path, ...]:
        """Every ``.py`` file under each of ``roots`` (repo-relative dirs),
        skipping ``__pycache__``. Built once per distinct ``roots`` tuple and
        memoised — the same index the per-rule walks would each rebuild."""
        key = tuple(roots)
        cached = self._files_cache.get(key)
        if cached is not None:
            return cached
        out: list[Path] = []
        for rel in roots:
            base = self._repo_root / rel
            if not base.exists():
                break
            for path in base.rglob("*.py"):
                if "__pycache__" in path.parts:
                    continue
                out.append(path)
        result = tuple(out)
        self._files_cache[key] = result
        return result

    # ── file index ───────────────────────────────────────────────────────

    def xǁCheckContextǁpython_files__mutmut_11(self, *roots: str) -> tuple[Path, ...]:
        """Every ``.py`` file under each of ``roots`` (repo-relative dirs),
        skipping ``__pycache__``. Built once per distinct ``roots`` tuple and
        memoised — the same index the per-rule walks would each rebuild."""
        key = tuple(roots)
        cached = self._files_cache.get(key)
        if cached is not None:
            return cached
        out: list[Path] = []
        for rel in roots:
            base = self._repo_root / rel
            if not base.exists():
                continue
            for path in base.rglob(None):
                if "__pycache__" in path.parts:
                    continue
                out.append(path)
        result = tuple(out)
        self._files_cache[key] = result
        return result

    # ── file index ───────────────────────────────────────────────────────

    def xǁCheckContextǁpython_files__mutmut_12(self, *roots: str) -> tuple[Path, ...]:
        """Every ``.py`` file under each of ``roots`` (repo-relative dirs),
        skipping ``__pycache__``. Built once per distinct ``roots`` tuple and
        memoised — the same index the per-rule walks would each rebuild."""
        key = tuple(roots)
        cached = self._files_cache.get(key)
        if cached is not None:
            return cached
        out: list[Path] = []
        for rel in roots:
            base = self._repo_root / rel
            if not base.exists():
                continue
            for path in base.rglob("XX*.pyXX"):
                if "__pycache__" in path.parts:
                    continue
                out.append(path)
        result = tuple(out)
        self._files_cache[key] = result
        return result

    # ── file index ───────────────────────────────────────────────────────

    def xǁCheckContextǁpython_files__mutmut_13(self, *roots: str) -> tuple[Path, ...]:
        """Every ``.py`` file under each of ``roots`` (repo-relative dirs),
        skipping ``__pycache__``. Built once per distinct ``roots`` tuple and
        memoised — the same index the per-rule walks would each rebuild."""
        key = tuple(roots)
        cached = self._files_cache.get(key)
        if cached is not None:
            return cached
        out: list[Path] = []
        for rel in roots:
            base = self._repo_root / rel
            if not base.exists():
                continue
            for path in base.rglob("*.PY"):
                if "__pycache__" in path.parts:
                    continue
                out.append(path)
        result = tuple(out)
        self._files_cache[key] = result
        return result

    # ── file index ───────────────────────────────────────────────────────

    def xǁCheckContextǁpython_files__mutmut_14(self, *roots: str) -> tuple[Path, ...]:
        """Every ``.py`` file under each of ``roots`` (repo-relative dirs),
        skipping ``__pycache__``. Built once per distinct ``roots`` tuple and
        memoised — the same index the per-rule walks would each rebuild."""
        key = tuple(roots)
        cached = self._files_cache.get(key)
        if cached is not None:
            return cached
        out: list[Path] = []
        for rel in roots:
            base = self._repo_root / rel
            if not base.exists():
                continue
            for path in base.rglob("*.py"):
                if "XX__pycache__XX" in path.parts:
                    continue
                out.append(path)
        result = tuple(out)
        self._files_cache[key] = result
        return result

    # ── file index ───────────────────────────────────────────────────────

    def xǁCheckContextǁpython_files__mutmut_15(self, *roots: str) -> tuple[Path, ...]:
        """Every ``.py`` file under each of ``roots`` (repo-relative dirs),
        skipping ``__pycache__``. Built once per distinct ``roots`` tuple and
        memoised — the same index the per-rule walks would each rebuild."""
        key = tuple(roots)
        cached = self._files_cache.get(key)
        if cached is not None:
            return cached
        out: list[Path] = []
        for rel in roots:
            base = self._repo_root / rel
            if not base.exists():
                continue
            for path in base.rglob("*.py"):
                if "__PYCACHE__" in path.parts:
                    continue
                out.append(path)
        result = tuple(out)
        self._files_cache[key] = result
        return result

    # ── file index ───────────────────────────────────────────────────────

    def xǁCheckContextǁpython_files__mutmut_16(self, *roots: str) -> tuple[Path, ...]:
        """Every ``.py`` file under each of ``roots`` (repo-relative dirs),
        skipping ``__pycache__``. Built once per distinct ``roots`` tuple and
        memoised — the same index the per-rule walks would each rebuild."""
        key = tuple(roots)
        cached = self._files_cache.get(key)
        if cached is not None:
            return cached
        out: list[Path] = []
        for rel in roots:
            base = self._repo_root / rel
            if not base.exists():
                continue
            for path in base.rglob("*.py"):
                if "__pycache__" not in path.parts:
                    continue
                out.append(path)
        result = tuple(out)
        self._files_cache[key] = result
        return result

    # ── file index ───────────────────────────────────────────────────────

    def xǁCheckContextǁpython_files__mutmut_17(self, *roots: str) -> tuple[Path, ...]:
        """Every ``.py`` file under each of ``roots`` (repo-relative dirs),
        skipping ``__pycache__``. Built once per distinct ``roots`` tuple and
        memoised — the same index the per-rule walks would each rebuild."""
        key = tuple(roots)
        cached = self._files_cache.get(key)
        if cached is not None:
            return cached
        out: list[Path] = []
        for rel in roots:
            base = self._repo_root / rel
            if not base.exists():
                continue
            for path in base.rglob("*.py"):
                if "__pycache__" in path.parts:
                    break
                out.append(path)
        result = tuple(out)
        self._files_cache[key] = result
        return result

    # ── file index ───────────────────────────────────────────────────────

    def xǁCheckContextǁpython_files__mutmut_18(self, *roots: str) -> tuple[Path, ...]:
        """Every ``.py`` file under each of ``roots`` (repo-relative dirs),
        skipping ``__pycache__``. Built once per distinct ``roots`` tuple and
        memoised — the same index the per-rule walks would each rebuild."""
        key = tuple(roots)
        cached = self._files_cache.get(key)
        if cached is not None:
            return cached
        out: list[Path] = []
        for rel in roots:
            base = self._repo_root / rel
            if not base.exists():
                continue
            for path in base.rglob("*.py"):
                if "__pycache__" in path.parts:
                    continue
                out.append(None)
        result = tuple(out)
        self._files_cache[key] = result
        return result

    # ── file index ───────────────────────────────────────────────────────

    def xǁCheckContextǁpython_files__mutmut_19(self, *roots: str) -> tuple[Path, ...]:
        """Every ``.py`` file under each of ``roots`` (repo-relative dirs),
        skipping ``__pycache__``. Built once per distinct ``roots`` tuple and
        memoised — the same index the per-rule walks would each rebuild."""
        key = tuple(roots)
        cached = self._files_cache.get(key)
        if cached is not None:
            return cached
        out: list[Path] = []
        for rel in roots:
            base = self._repo_root / rel
            if not base.exists():
                continue
            for path in base.rglob("*.py"):
                if "__pycache__" in path.parts:
                    continue
                out.append(path)
        result = None
        self._files_cache[key] = result
        return result

    # ── file index ───────────────────────────────────────────────────────

    def xǁCheckContextǁpython_files__mutmut_20(self, *roots: str) -> tuple[Path, ...]:
        """Every ``.py`` file under each of ``roots`` (repo-relative dirs),
        skipping ``__pycache__``. Built once per distinct ``roots`` tuple and
        memoised — the same index the per-rule walks would each rebuild."""
        key = tuple(roots)
        cached = self._files_cache.get(key)
        if cached is not None:
            return cached
        out: list[Path] = []
        for rel in roots:
            base = self._repo_root / rel
            if not base.exists():
                continue
            for path in base.rglob("*.py"):
                if "__pycache__" in path.parts:
                    continue
                out.append(path)
        result = tuple(None)
        self._files_cache[key] = result
        return result

    # ── file index ───────────────────────────────────────────────────────

    def xǁCheckContextǁpython_files__mutmut_21(self, *roots: str) -> tuple[Path, ...]:
        """Every ``.py`` file under each of ``roots`` (repo-relative dirs),
        skipping ``__pycache__``. Built once per distinct ``roots`` tuple and
        memoised — the same index the per-rule walks would each rebuild."""
        key = tuple(roots)
        cached = self._files_cache.get(key)
        if cached is not None:
            return cached
        out: list[Path] = []
        for rel in roots:
            base = self._repo_root / rel
            if not base.exists():
                continue
            for path in base.rglob("*.py"):
                if "__pycache__" in path.parts:
                    continue
                out.append(path)
        result = tuple(out)
        self._files_cache[key] = None
        return result

    # ── source text ──────────────────────────────────────────────────────

    @_mutmut_mutated(mutants_xǁCheckContextǁsource_for__mutmut)
    def source_for(self, path: Path) -> str | None:
        """UTF-8 source text of ``path``, cached. ``None`` on a read error
        (mirrors the tolerant behaviour every detector already has)."""
        if path in self._source_cache:
            return self._source_cache[path]
        try:
            text: str | None = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            text = None
        self._source_cache[path] = text
        return text

    # ── source text ──────────────────────────────────────────────────────

    def xǁCheckContextǁsource_for__mutmut_orig(self, path: Path) -> str | None:
        """UTF-8 source text of ``path``, cached. ``None`` on a read error
        (mirrors the tolerant behaviour every detector already has)."""
        if path in self._source_cache:
            return self._source_cache[path]
        try:
            text: str | None = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            text = None
        self._source_cache[path] = text
        return text

    # ── source text ──────────────────────────────────────────────────────

    def xǁCheckContextǁsource_for__mutmut_1(self, path: Path) -> str | None:
        """UTF-8 source text of ``path``, cached. ``None`` on a read error
        (mirrors the tolerant behaviour every detector already has)."""
        if path not in self._source_cache:
            return self._source_cache[path]
        try:
            text: str | None = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            text = None
        self._source_cache[path] = text
        return text

    # ── source text ──────────────────────────────────────────────────────

    def xǁCheckContextǁsource_for__mutmut_2(self, path: Path) -> str | None:
        """UTF-8 source text of ``path``, cached. ``None`` on a read error
        (mirrors the tolerant behaviour every detector already has)."""
        if path in self._source_cache:
            return self._source_cache[path]
        try:
            text: str | None = None
        except (OSError, UnicodeDecodeError):
            text = None
        self._source_cache[path] = text
        return text

    # ── source text ──────────────────────────────────────────────────────

    def xǁCheckContextǁsource_for__mutmut_3(self, path: Path) -> str | None:
        """UTF-8 source text of ``path``, cached. ``None`` on a read error
        (mirrors the tolerant behaviour every detector already has)."""
        if path in self._source_cache:
            return self._source_cache[path]
        try:
            text: str | None = path.read_text(encoding=None)
        except (OSError, UnicodeDecodeError):
            text = None
        self._source_cache[path] = text
        return text

    # ── source text ──────────────────────────────────────────────────────

    def xǁCheckContextǁsource_for__mutmut_4(self, path: Path) -> str | None:
        """UTF-8 source text of ``path``, cached. ``None`` on a read error
        (mirrors the tolerant behaviour every detector already has)."""
        if path in self._source_cache:
            return self._source_cache[path]
        try:
            text: str | None = path.read_text(encoding="XXutf-8XX")
        except (OSError, UnicodeDecodeError):
            text = None
        self._source_cache[path] = text
        return text

    # ── source text ──────────────────────────────────────────────────────

    def xǁCheckContextǁsource_for__mutmut_5(self, path: Path) -> str | None:
        """UTF-8 source text of ``path``, cached. ``None`` on a read error
        (mirrors the tolerant behaviour every detector already has)."""
        if path in self._source_cache:
            return self._source_cache[path]
        try:
            text: str | None = path.read_text(encoding="UTF-8")
        except (OSError, UnicodeDecodeError):
            text = None
        self._source_cache[path] = text
        return text

    # ── source text ──────────────────────────────────────────────────────

    def xǁCheckContextǁsource_for__mutmut_6(self, path: Path) -> str | None:
        """UTF-8 source text of ``path``, cached. ``None`` on a read error
        (mirrors the tolerant behaviour every detector already has)."""
        if path in self._source_cache:
            return self._source_cache[path]
        try:
            text: str | None = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            text = ""
        self._source_cache[path] = text
        return text

    # ── source text ──────────────────────────────────────────────────────

    def xǁCheckContextǁsource_for__mutmut_7(self, path: Path) -> str | None:
        """UTF-8 source text of ``path``, cached. ``None`` on a read error
        (mirrors the tolerant behaviour every detector already has)."""
        if path in self._source_cache:
            return self._source_cache[path]
        try:
            text: str | None = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            text = None
        self._source_cache[path] = None
        return text

    # ── AST ──────────────────────────────────────────────────────────────

    @_mutmut_mutated(mutants_xǁCheckContextǁtree_for__mutmut)
    def tree_for(self, path: Path) -> ast.AST | None:
        """Parsed AST of ``path``, cached, or ``None`` on read / syntax error.

        Convenience accessor for checks that want to ask the context directly.
        The runner-wide win comes from :meth:`install` patching ``ast.parse``
        so even checks that never reference the context are de-duplicated.
        """
        source = self.source_for(path)
        if source is None:
            return None
        try:
            return self.parse(source, filename=str(path))
        except SyntaxError:
            return None

    # ── AST ──────────────────────────────────────────────────────────────

    def xǁCheckContextǁtree_for__mutmut_orig(self, path: Path) -> ast.AST | None:
        """Parsed AST of ``path``, cached, or ``None`` on read / syntax error.

        Convenience accessor for checks that want to ask the context directly.
        The runner-wide win comes from :meth:`install` patching ``ast.parse``
        so even checks that never reference the context are de-duplicated.
        """
        source = self.source_for(path)
        if source is None:
            return None
        try:
            return self.parse(source, filename=str(path))
        except SyntaxError:
            return None

    # ── AST ──────────────────────────────────────────────────────────────

    def xǁCheckContextǁtree_for__mutmut_1(self, path: Path) -> ast.AST | None:
        """Parsed AST of ``path``, cached, or ``None`` on read / syntax error.

        Convenience accessor for checks that want to ask the context directly.
        The runner-wide win comes from :meth:`install` patching ``ast.parse``
        so even checks that never reference the context are de-duplicated.
        """
        source = None
        if source is None:
            return None
        try:
            return self.parse(source, filename=str(path))
        except SyntaxError:
            return None

    # ── AST ──────────────────────────────────────────────────────────────

    def xǁCheckContextǁtree_for__mutmut_2(self, path: Path) -> ast.AST | None:
        """Parsed AST of ``path``, cached, or ``None`` on read / syntax error.

        Convenience accessor for checks that want to ask the context directly.
        The runner-wide win comes from :meth:`install` patching ``ast.parse``
        so even checks that never reference the context are de-duplicated.
        """
        source = self.source_for(None)
        if source is None:
            return None
        try:
            return self.parse(source, filename=str(path))
        except SyntaxError:
            return None

    # ── AST ──────────────────────────────────────────────────────────────

    def xǁCheckContextǁtree_for__mutmut_3(self, path: Path) -> ast.AST | None:
        """Parsed AST of ``path``, cached, or ``None`` on read / syntax error.

        Convenience accessor for checks that want to ask the context directly.
        The runner-wide win comes from :meth:`install` patching ``ast.parse``
        so even checks that never reference the context are de-duplicated.
        """
        source = self.source_for(path)
        if source is not None:
            return None
        try:
            return self.parse(source, filename=str(path))
        except SyntaxError:
            return None

    # ── AST ──────────────────────────────────────────────────────────────

    def xǁCheckContextǁtree_for__mutmut_4(self, path: Path) -> ast.AST | None:
        """Parsed AST of ``path``, cached, or ``None`` on read / syntax error.

        Convenience accessor for checks that want to ask the context directly.
        The runner-wide win comes from :meth:`install` patching ``ast.parse``
        so even checks that never reference the context are de-duplicated.
        """
        source = self.source_for(path)
        if source is None:
            return None
        try:
            return self.parse(None, filename=str(path))
        except SyntaxError:
            return None

    # ── AST ──────────────────────────────────────────────────────────────

    def xǁCheckContextǁtree_for__mutmut_5(self, path: Path) -> ast.AST | None:
        """Parsed AST of ``path``, cached, or ``None`` on read / syntax error.

        Convenience accessor for checks that want to ask the context directly.
        The runner-wide win comes from :meth:`install` patching ``ast.parse``
        so even checks that never reference the context are de-duplicated.
        """
        source = self.source_for(path)
        if source is None:
            return None
        try:
            return self.parse(source, filename=None)
        except SyntaxError:
            return None

    # ── AST ──────────────────────────────────────────────────────────────

    def xǁCheckContextǁtree_for__mutmut_6(self, path: Path) -> ast.AST | None:
        """Parsed AST of ``path``, cached, or ``None`` on read / syntax error.

        Convenience accessor for checks that want to ask the context directly.
        The runner-wide win comes from :meth:`install` patching ``ast.parse``
        so even checks that never reference the context are de-duplicated.
        """
        source = self.source_for(path)
        if source is None:
            return None
        try:
            return self.parse(filename=str(path))
        except SyntaxError:
            return None

    # ── AST ──────────────────────────────────────────────────────────────

    def xǁCheckContextǁtree_for__mutmut_7(self, path: Path) -> ast.AST | None:
        """Parsed AST of ``path``, cached, or ``None`` on read / syntax error.

        Convenience accessor for checks that want to ask the context directly.
        The runner-wide win comes from :meth:`install` patching ``ast.parse``
        so even checks that never reference the context are de-duplicated.
        """
        source = self.source_for(path)
        if source is None:
            return None
        try:
            return self.parse(source, )
        except SyntaxError:
            return None

    # ── AST ──────────────────────────────────────────────────────────────

    def xǁCheckContextǁtree_for__mutmut_8(self, path: Path) -> ast.AST | None:
        """Parsed AST of ``path``, cached, or ``None`` on read / syntax error.

        Convenience accessor for checks that want to ask the context directly.
        The runner-wide win comes from :meth:`install` patching ``ast.parse``
        so even checks that never reference the context are de-duplicated.
        """
        source = self.source_for(path)
        if source is None:
            return None
        try:
            return self.parse(source, filename=str(None))
        except SyntaxError:
            return None

    @_mutmut_mutated(mutants_xǁCheckContextǁparse__mutmut)
    def parse(self, source: str, *, filename: str = "<unknown>") -> ast.AST:
        """Memoised ``ast.parse`` — the cache the installed wrapper delegates
        to. Keyed by ``(filename, source-text)``; a miss parses with the real
        stdlib parser and records the tree."""
        by_text = self._tree_cache.get(filename)
        if by_text is not None:
            hit = by_text.get(source)
            if hit is not None:
                self.parse_hits += 1
                return hit
        else:
            by_text = {}
            self._tree_cache[filename] = by_text
        tree = _REAL_AST_PARSE(source, filename=filename)
        by_text[source] = tree
        self.parse_misses += 1
        return tree

    def xǁCheckContextǁparse__mutmut_orig(self, source: str, *, filename: str = "<unknown>") -> ast.AST:
        """Memoised ``ast.parse`` — the cache the installed wrapper delegates
        to. Keyed by ``(filename, source-text)``; a miss parses with the real
        stdlib parser and records the tree."""
        by_text = self._tree_cache.get(filename)
        if by_text is not None:
            hit = by_text.get(source)
            if hit is not None:
                self.parse_hits += 1
                return hit
        else:
            by_text = {}
            self._tree_cache[filename] = by_text
        tree = _REAL_AST_PARSE(source, filename=filename)
        by_text[source] = tree
        self.parse_misses += 1
        return tree

    def xǁCheckContextǁparse__mutmut_1(self, source: str, *, filename: str = "XX<unknown>XX") -> ast.AST:
        """Memoised ``ast.parse`` — the cache the installed wrapper delegates
        to. Keyed by ``(filename, source-text)``; a miss parses with the real
        stdlib parser and records the tree."""
        by_text = self._tree_cache.get(filename)
        if by_text is not None:
            hit = by_text.get(source)
            if hit is not None:
                self.parse_hits += 1
                return hit
        else:
            by_text = {}
            self._tree_cache[filename] = by_text
        tree = _REAL_AST_PARSE(source, filename=filename)
        by_text[source] = tree
        self.parse_misses += 1
        return tree

    def xǁCheckContextǁparse__mutmut_2(self, source: str, *, filename: str = "<UNKNOWN>") -> ast.AST:
        """Memoised ``ast.parse`` — the cache the installed wrapper delegates
        to. Keyed by ``(filename, source-text)``; a miss parses with the real
        stdlib parser and records the tree."""
        by_text = self._tree_cache.get(filename)
        if by_text is not None:
            hit = by_text.get(source)
            if hit is not None:
                self.parse_hits += 1
                return hit
        else:
            by_text = {}
            self._tree_cache[filename] = by_text
        tree = _REAL_AST_PARSE(source, filename=filename)
        by_text[source] = tree
        self.parse_misses += 1
        return tree

    def xǁCheckContextǁparse__mutmut_3(self, source: str, *, filename: str = "<unknown>") -> ast.AST:
        """Memoised ``ast.parse`` — the cache the installed wrapper delegates
        to. Keyed by ``(filename, source-text)``; a miss parses with the real
        stdlib parser and records the tree."""
        by_text = None
        if by_text is not None:
            hit = by_text.get(source)
            if hit is not None:
                self.parse_hits += 1
                return hit
        else:
            by_text = {}
            self._tree_cache[filename] = by_text
        tree = _REAL_AST_PARSE(source, filename=filename)
        by_text[source] = tree
        self.parse_misses += 1
        return tree

    def xǁCheckContextǁparse__mutmut_4(self, source: str, *, filename: str = "<unknown>") -> ast.AST:
        """Memoised ``ast.parse`` — the cache the installed wrapper delegates
        to. Keyed by ``(filename, source-text)``; a miss parses with the real
        stdlib parser and records the tree."""
        by_text = self._tree_cache.get(None)
        if by_text is not None:
            hit = by_text.get(source)
            if hit is not None:
                self.parse_hits += 1
                return hit
        else:
            by_text = {}
            self._tree_cache[filename] = by_text
        tree = _REAL_AST_PARSE(source, filename=filename)
        by_text[source] = tree
        self.parse_misses += 1
        return tree

    def xǁCheckContextǁparse__mutmut_5(self, source: str, *, filename: str = "<unknown>") -> ast.AST:
        """Memoised ``ast.parse`` — the cache the installed wrapper delegates
        to. Keyed by ``(filename, source-text)``; a miss parses with the real
        stdlib parser and records the tree."""
        by_text = self._tree_cache.get(filename)
        if by_text is None:
            hit = by_text.get(source)
            if hit is not None:
                self.parse_hits += 1
                return hit
        else:
            by_text = {}
            self._tree_cache[filename] = by_text
        tree = _REAL_AST_PARSE(source, filename=filename)
        by_text[source] = tree
        self.parse_misses += 1
        return tree

    def xǁCheckContextǁparse__mutmut_6(self, source: str, *, filename: str = "<unknown>") -> ast.AST:
        """Memoised ``ast.parse`` — the cache the installed wrapper delegates
        to. Keyed by ``(filename, source-text)``; a miss parses with the real
        stdlib parser and records the tree."""
        by_text = self._tree_cache.get(filename)
        if by_text is not None:
            hit = None
            if hit is not None:
                self.parse_hits += 1
                return hit
        else:
            by_text = {}
            self._tree_cache[filename] = by_text
        tree = _REAL_AST_PARSE(source, filename=filename)
        by_text[source] = tree
        self.parse_misses += 1
        return tree

    def xǁCheckContextǁparse__mutmut_7(self, source: str, *, filename: str = "<unknown>") -> ast.AST:
        """Memoised ``ast.parse`` — the cache the installed wrapper delegates
        to. Keyed by ``(filename, source-text)``; a miss parses with the real
        stdlib parser and records the tree."""
        by_text = self._tree_cache.get(filename)
        if by_text is not None:
            hit = by_text.get(None)
            if hit is not None:
                self.parse_hits += 1
                return hit
        else:
            by_text = {}
            self._tree_cache[filename] = by_text
        tree = _REAL_AST_PARSE(source, filename=filename)
        by_text[source] = tree
        self.parse_misses += 1
        return tree

    def xǁCheckContextǁparse__mutmut_8(self, source: str, *, filename: str = "<unknown>") -> ast.AST:
        """Memoised ``ast.parse`` — the cache the installed wrapper delegates
        to. Keyed by ``(filename, source-text)``; a miss parses with the real
        stdlib parser and records the tree."""
        by_text = self._tree_cache.get(filename)
        if by_text is not None:
            hit = by_text.get(source)
            if hit is None:
                self.parse_hits += 1
                return hit
        else:
            by_text = {}
            self._tree_cache[filename] = by_text
        tree = _REAL_AST_PARSE(source, filename=filename)
        by_text[source] = tree
        self.parse_misses += 1
        return tree

    def xǁCheckContextǁparse__mutmut_9(self, source: str, *, filename: str = "<unknown>") -> ast.AST:
        """Memoised ``ast.parse`` — the cache the installed wrapper delegates
        to. Keyed by ``(filename, source-text)``; a miss parses with the real
        stdlib parser and records the tree."""
        by_text = self._tree_cache.get(filename)
        if by_text is not None:
            hit = by_text.get(source)
            if hit is not None:
                self.parse_hits = 1
                return hit
        else:
            by_text = {}
            self._tree_cache[filename] = by_text
        tree = _REAL_AST_PARSE(source, filename=filename)
        by_text[source] = tree
        self.parse_misses += 1
        return tree

    def xǁCheckContextǁparse__mutmut_10(self, source: str, *, filename: str = "<unknown>") -> ast.AST:
        """Memoised ``ast.parse`` — the cache the installed wrapper delegates
        to. Keyed by ``(filename, source-text)``; a miss parses with the real
        stdlib parser and records the tree."""
        by_text = self._tree_cache.get(filename)
        if by_text is not None:
            hit = by_text.get(source)
            if hit is not None:
                self.parse_hits -= 1
                return hit
        else:
            by_text = {}
            self._tree_cache[filename] = by_text
        tree = _REAL_AST_PARSE(source, filename=filename)
        by_text[source] = tree
        self.parse_misses += 1
        return tree

    def xǁCheckContextǁparse__mutmut_11(self, source: str, *, filename: str = "<unknown>") -> ast.AST:
        """Memoised ``ast.parse`` — the cache the installed wrapper delegates
        to. Keyed by ``(filename, source-text)``; a miss parses with the real
        stdlib parser and records the tree."""
        by_text = self._tree_cache.get(filename)
        if by_text is not None:
            hit = by_text.get(source)
            if hit is not None:
                self.parse_hits += 2
                return hit
        else:
            by_text = {}
            self._tree_cache[filename] = by_text
        tree = _REAL_AST_PARSE(source, filename=filename)
        by_text[source] = tree
        self.parse_misses += 1
        return tree

    def xǁCheckContextǁparse__mutmut_12(self, source: str, *, filename: str = "<unknown>") -> ast.AST:
        """Memoised ``ast.parse`` — the cache the installed wrapper delegates
        to. Keyed by ``(filename, source-text)``; a miss parses with the real
        stdlib parser and records the tree."""
        by_text = self._tree_cache.get(filename)
        if by_text is not None:
            hit = by_text.get(source)
            if hit is not None:
                self.parse_hits += 1
                return hit
        else:
            by_text = None
            self._tree_cache[filename] = by_text
        tree = _REAL_AST_PARSE(source, filename=filename)
        by_text[source] = tree
        self.parse_misses += 1
        return tree

    def xǁCheckContextǁparse__mutmut_13(self, source: str, *, filename: str = "<unknown>") -> ast.AST:
        """Memoised ``ast.parse`` — the cache the installed wrapper delegates
        to. Keyed by ``(filename, source-text)``; a miss parses with the real
        stdlib parser and records the tree."""
        by_text = self._tree_cache.get(filename)
        if by_text is not None:
            hit = by_text.get(source)
            if hit is not None:
                self.parse_hits += 1
                return hit
        else:
            by_text = {}
            self._tree_cache[filename] = None
        tree = _REAL_AST_PARSE(source, filename=filename)
        by_text[source] = tree
        self.parse_misses += 1
        return tree

    def xǁCheckContextǁparse__mutmut_14(self, source: str, *, filename: str = "<unknown>") -> ast.AST:
        """Memoised ``ast.parse`` — the cache the installed wrapper delegates
        to. Keyed by ``(filename, source-text)``; a miss parses with the real
        stdlib parser and records the tree."""
        by_text = self._tree_cache.get(filename)
        if by_text is not None:
            hit = by_text.get(source)
            if hit is not None:
                self.parse_hits += 1
                return hit
        else:
            by_text = {}
            self._tree_cache[filename] = by_text
        tree = None
        by_text[source] = tree
        self.parse_misses += 1
        return tree

    def xǁCheckContextǁparse__mutmut_15(self, source: str, *, filename: str = "<unknown>") -> ast.AST:
        """Memoised ``ast.parse`` — the cache the installed wrapper delegates
        to. Keyed by ``(filename, source-text)``; a miss parses with the real
        stdlib parser and records the tree."""
        by_text = self._tree_cache.get(filename)
        if by_text is not None:
            hit = by_text.get(source)
            if hit is not None:
                self.parse_hits += 1
                return hit
        else:
            by_text = {}
            self._tree_cache[filename] = by_text
        tree = _REAL_AST_PARSE(None, filename=filename)
        by_text[source] = tree
        self.parse_misses += 1
        return tree

    def xǁCheckContextǁparse__mutmut_16(self, source: str, *, filename: str = "<unknown>") -> ast.AST:
        """Memoised ``ast.parse`` — the cache the installed wrapper delegates
        to. Keyed by ``(filename, source-text)``; a miss parses with the real
        stdlib parser and records the tree."""
        by_text = self._tree_cache.get(filename)
        if by_text is not None:
            hit = by_text.get(source)
            if hit is not None:
                self.parse_hits += 1
                return hit
        else:
            by_text = {}
            self._tree_cache[filename] = by_text
        tree = _REAL_AST_PARSE(source, filename=None)
        by_text[source] = tree
        self.parse_misses += 1
        return tree

    def xǁCheckContextǁparse__mutmut_17(self, source: str, *, filename: str = "<unknown>") -> ast.AST:
        """Memoised ``ast.parse`` — the cache the installed wrapper delegates
        to. Keyed by ``(filename, source-text)``; a miss parses with the real
        stdlib parser and records the tree."""
        by_text = self._tree_cache.get(filename)
        if by_text is not None:
            hit = by_text.get(source)
            if hit is not None:
                self.parse_hits += 1
                return hit
        else:
            by_text = {}
            self._tree_cache[filename] = by_text
        tree = _REAL_AST_PARSE(filename=filename)
        by_text[source] = tree
        self.parse_misses += 1
        return tree

    def xǁCheckContextǁparse__mutmut_18(self, source: str, *, filename: str = "<unknown>") -> ast.AST:
        """Memoised ``ast.parse`` — the cache the installed wrapper delegates
        to. Keyed by ``(filename, source-text)``; a miss parses with the real
        stdlib parser and records the tree."""
        by_text = self._tree_cache.get(filename)
        if by_text is not None:
            hit = by_text.get(source)
            if hit is not None:
                self.parse_hits += 1
                return hit
        else:
            by_text = {}
            self._tree_cache[filename] = by_text
        tree = _REAL_AST_PARSE(source, )
        by_text[source] = tree
        self.parse_misses += 1
        return tree

    def xǁCheckContextǁparse__mutmut_19(self, source: str, *, filename: str = "<unknown>") -> ast.AST:
        """Memoised ``ast.parse`` — the cache the installed wrapper delegates
        to. Keyed by ``(filename, source-text)``; a miss parses with the real
        stdlib parser and records the tree."""
        by_text = self._tree_cache.get(filename)
        if by_text is not None:
            hit = by_text.get(source)
            if hit is not None:
                self.parse_hits += 1
                return hit
        else:
            by_text = {}
            self._tree_cache[filename] = by_text
        tree = _REAL_AST_PARSE(source, filename=filename)
        by_text[source] = None
        self.parse_misses += 1
        return tree

    def xǁCheckContextǁparse__mutmut_20(self, source: str, *, filename: str = "<unknown>") -> ast.AST:
        """Memoised ``ast.parse`` — the cache the installed wrapper delegates
        to. Keyed by ``(filename, source-text)``; a miss parses with the real
        stdlib parser and records the tree."""
        by_text = self._tree_cache.get(filename)
        if by_text is not None:
            hit = by_text.get(source)
            if hit is not None:
                self.parse_hits += 1
                return hit
        else:
            by_text = {}
            self._tree_cache[filename] = by_text
        tree = _REAL_AST_PARSE(source, filename=filename)
        by_text[source] = tree
        self.parse_misses = 1
        return tree

    def xǁCheckContextǁparse__mutmut_21(self, source: str, *, filename: str = "<unknown>") -> ast.AST:
        """Memoised ``ast.parse`` — the cache the installed wrapper delegates
        to. Keyed by ``(filename, source-text)``; a miss parses with the real
        stdlib parser and records the tree."""
        by_text = self._tree_cache.get(filename)
        if by_text is not None:
            hit = by_text.get(source)
            if hit is not None:
                self.parse_hits += 1
                return hit
        else:
            by_text = {}
            self._tree_cache[filename] = by_text
        tree = _REAL_AST_PARSE(source, filename=filename)
        by_text[source] = tree
        self.parse_misses -= 1
        return tree

    def xǁCheckContextǁparse__mutmut_22(self, source: str, *, filename: str = "<unknown>") -> ast.AST:
        """Memoised ``ast.parse`` — the cache the installed wrapper delegates
        to. Keyed by ``(filename, source-text)``; a miss parses with the real
        stdlib parser and records the tree."""
        by_text = self._tree_cache.get(filename)
        if by_text is not None:
            hit = by_text.get(source)
            if hit is not None:
                self.parse_hits += 1
                return hit
        else:
            by_text = {}
            self._tree_cache[filename] = by_text
        tree = _REAL_AST_PARSE(source, filename=filename)
        by_text[source] = tree
        self.parse_misses += 2
        return tree

    @_mutmut_mutated(mutants_xǁCheckContextǁwalk__mutmut)
    def walk(self, node: ast.AST) -> list[ast.AST]:
        """Memoised ``ast.walk`` — return the full BFS node list for ``node``.

        Because the parse cache returns the SAME tree object for a given file,
        the walk can be done ONCE and the materialised node list shared by
        object identity. Order is byte-for-byte the stdlib ``ast.walk`` BFS
        order, so every caller — including the ones that build parent maps from
        walk order — sees an identical sequence. Returns a list (not a
        generator); the installed wrapper yields from it.
        """
        key = id(node)
        cached = self._walk_cache.get(key)
        if cached is not None:
            self.walk_hits += 1
            return cached
        nodes = list(_REAL_AST_WALK(node))
        self._walk_cache[key] = nodes
        self.walk_misses += 1
        return nodes

    def xǁCheckContextǁwalk__mutmut_orig(self, node: ast.AST) -> list[ast.AST]:
        """Memoised ``ast.walk`` — return the full BFS node list for ``node``.

        Because the parse cache returns the SAME tree object for a given file,
        the walk can be done ONCE and the materialised node list shared by
        object identity. Order is byte-for-byte the stdlib ``ast.walk`` BFS
        order, so every caller — including the ones that build parent maps from
        walk order — sees an identical sequence. Returns a list (not a
        generator); the installed wrapper yields from it.
        """
        key = id(node)
        cached = self._walk_cache.get(key)
        if cached is not None:
            self.walk_hits += 1
            return cached
        nodes = list(_REAL_AST_WALK(node))
        self._walk_cache[key] = nodes
        self.walk_misses += 1
        return nodes

    def xǁCheckContextǁwalk__mutmut_1(self, node: ast.AST) -> list[ast.AST]:
        """Memoised ``ast.walk`` — return the full BFS node list for ``node``.

        Because the parse cache returns the SAME tree object for a given file,
        the walk can be done ONCE and the materialised node list shared by
        object identity. Order is byte-for-byte the stdlib ``ast.walk`` BFS
        order, so every caller — including the ones that build parent maps from
        walk order — sees an identical sequence. Returns a list (not a
        generator); the installed wrapper yields from it.
        """
        key = None
        cached = self._walk_cache.get(key)
        if cached is not None:
            self.walk_hits += 1
            return cached
        nodes = list(_REAL_AST_WALK(node))
        self._walk_cache[key] = nodes
        self.walk_misses += 1
        return nodes

    def xǁCheckContextǁwalk__mutmut_2(self, node: ast.AST) -> list[ast.AST]:
        """Memoised ``ast.walk`` — return the full BFS node list for ``node``.

        Because the parse cache returns the SAME tree object for a given file,
        the walk can be done ONCE and the materialised node list shared by
        object identity. Order is byte-for-byte the stdlib ``ast.walk`` BFS
        order, so every caller — including the ones that build parent maps from
        walk order — sees an identical sequence. Returns a list (not a
        generator); the installed wrapper yields from it.
        """
        key = id(None)
        cached = self._walk_cache.get(key)
        if cached is not None:
            self.walk_hits += 1
            return cached
        nodes = list(_REAL_AST_WALK(node))
        self._walk_cache[key] = nodes
        self.walk_misses += 1
        return nodes

    def xǁCheckContextǁwalk__mutmut_3(self, node: ast.AST) -> list[ast.AST]:
        """Memoised ``ast.walk`` — return the full BFS node list for ``node``.

        Because the parse cache returns the SAME tree object for a given file,
        the walk can be done ONCE and the materialised node list shared by
        object identity. Order is byte-for-byte the stdlib ``ast.walk`` BFS
        order, so every caller — including the ones that build parent maps from
        walk order — sees an identical sequence. Returns a list (not a
        generator); the installed wrapper yields from it.
        """
        key = id(node)
        cached = None
        if cached is not None:
            self.walk_hits += 1
            return cached
        nodes = list(_REAL_AST_WALK(node))
        self._walk_cache[key] = nodes
        self.walk_misses += 1
        return nodes

    def xǁCheckContextǁwalk__mutmut_4(self, node: ast.AST) -> list[ast.AST]:
        """Memoised ``ast.walk`` — return the full BFS node list for ``node``.

        Because the parse cache returns the SAME tree object for a given file,
        the walk can be done ONCE and the materialised node list shared by
        object identity. Order is byte-for-byte the stdlib ``ast.walk`` BFS
        order, so every caller — including the ones that build parent maps from
        walk order — sees an identical sequence. Returns a list (not a
        generator); the installed wrapper yields from it.
        """
        key = id(node)
        cached = self._walk_cache.get(None)
        if cached is not None:
            self.walk_hits += 1
            return cached
        nodes = list(_REAL_AST_WALK(node))
        self._walk_cache[key] = nodes
        self.walk_misses += 1
        return nodes

    def xǁCheckContextǁwalk__mutmut_5(self, node: ast.AST) -> list[ast.AST]:
        """Memoised ``ast.walk`` — return the full BFS node list for ``node``.

        Because the parse cache returns the SAME tree object for a given file,
        the walk can be done ONCE and the materialised node list shared by
        object identity. Order is byte-for-byte the stdlib ``ast.walk`` BFS
        order, so every caller — including the ones that build parent maps from
        walk order — sees an identical sequence. Returns a list (not a
        generator); the installed wrapper yields from it.
        """
        key = id(node)
        cached = self._walk_cache.get(key)
        if cached is None:
            self.walk_hits += 1
            return cached
        nodes = list(_REAL_AST_WALK(node))
        self._walk_cache[key] = nodes
        self.walk_misses += 1
        return nodes

    def xǁCheckContextǁwalk__mutmut_6(self, node: ast.AST) -> list[ast.AST]:
        """Memoised ``ast.walk`` — return the full BFS node list for ``node``.

        Because the parse cache returns the SAME tree object for a given file,
        the walk can be done ONCE and the materialised node list shared by
        object identity. Order is byte-for-byte the stdlib ``ast.walk`` BFS
        order, so every caller — including the ones that build parent maps from
        walk order — sees an identical sequence. Returns a list (not a
        generator); the installed wrapper yields from it.
        """
        key = id(node)
        cached = self._walk_cache.get(key)
        if cached is not None:
            self.walk_hits = 1
            return cached
        nodes = list(_REAL_AST_WALK(node))
        self._walk_cache[key] = nodes
        self.walk_misses += 1
        return nodes

    def xǁCheckContextǁwalk__mutmut_7(self, node: ast.AST) -> list[ast.AST]:
        """Memoised ``ast.walk`` — return the full BFS node list for ``node``.

        Because the parse cache returns the SAME tree object for a given file,
        the walk can be done ONCE and the materialised node list shared by
        object identity. Order is byte-for-byte the stdlib ``ast.walk`` BFS
        order, so every caller — including the ones that build parent maps from
        walk order — sees an identical sequence. Returns a list (not a
        generator); the installed wrapper yields from it.
        """
        key = id(node)
        cached = self._walk_cache.get(key)
        if cached is not None:
            self.walk_hits -= 1
            return cached
        nodes = list(_REAL_AST_WALK(node))
        self._walk_cache[key] = nodes
        self.walk_misses += 1
        return nodes

    def xǁCheckContextǁwalk__mutmut_8(self, node: ast.AST) -> list[ast.AST]:
        """Memoised ``ast.walk`` — return the full BFS node list for ``node``.

        Because the parse cache returns the SAME tree object for a given file,
        the walk can be done ONCE and the materialised node list shared by
        object identity. Order is byte-for-byte the stdlib ``ast.walk`` BFS
        order, so every caller — including the ones that build parent maps from
        walk order — sees an identical sequence. Returns a list (not a
        generator); the installed wrapper yields from it.
        """
        key = id(node)
        cached = self._walk_cache.get(key)
        if cached is not None:
            self.walk_hits += 2
            return cached
        nodes = list(_REAL_AST_WALK(node))
        self._walk_cache[key] = nodes
        self.walk_misses += 1
        return nodes

    def xǁCheckContextǁwalk__mutmut_9(self, node: ast.AST) -> list[ast.AST]:
        """Memoised ``ast.walk`` — return the full BFS node list for ``node``.

        Because the parse cache returns the SAME tree object for a given file,
        the walk can be done ONCE and the materialised node list shared by
        object identity. Order is byte-for-byte the stdlib ``ast.walk`` BFS
        order, so every caller — including the ones that build parent maps from
        walk order — sees an identical sequence. Returns a list (not a
        generator); the installed wrapper yields from it.
        """
        key = id(node)
        cached = self._walk_cache.get(key)
        if cached is not None:
            self.walk_hits += 1
            return cached
        nodes = None
        self._walk_cache[key] = nodes
        self.walk_misses += 1
        return nodes

    def xǁCheckContextǁwalk__mutmut_10(self, node: ast.AST) -> list[ast.AST]:
        """Memoised ``ast.walk`` — return the full BFS node list for ``node``.

        Because the parse cache returns the SAME tree object for a given file,
        the walk can be done ONCE and the materialised node list shared by
        object identity. Order is byte-for-byte the stdlib ``ast.walk`` BFS
        order, so every caller — including the ones that build parent maps from
        walk order — sees an identical sequence. Returns a list (not a
        generator); the installed wrapper yields from it.
        """
        key = id(node)
        cached = self._walk_cache.get(key)
        if cached is not None:
            self.walk_hits += 1
            return cached
        nodes = list(None)
        self._walk_cache[key] = nodes
        self.walk_misses += 1
        return nodes

    def xǁCheckContextǁwalk__mutmut_11(self, node: ast.AST) -> list[ast.AST]:
        """Memoised ``ast.walk`` — return the full BFS node list for ``node``.

        Because the parse cache returns the SAME tree object for a given file,
        the walk can be done ONCE and the materialised node list shared by
        object identity. Order is byte-for-byte the stdlib ``ast.walk`` BFS
        order, so every caller — including the ones that build parent maps from
        walk order — sees an identical sequence. Returns a list (not a
        generator); the installed wrapper yields from it.
        """
        key = id(node)
        cached = self._walk_cache.get(key)
        if cached is not None:
            self.walk_hits += 1
            return cached
        nodes = list(_REAL_AST_WALK(None))
        self._walk_cache[key] = nodes
        self.walk_misses += 1
        return nodes

    def xǁCheckContextǁwalk__mutmut_12(self, node: ast.AST) -> list[ast.AST]:
        """Memoised ``ast.walk`` — return the full BFS node list for ``node``.

        Because the parse cache returns the SAME tree object for a given file,
        the walk can be done ONCE and the materialised node list shared by
        object identity. Order is byte-for-byte the stdlib ``ast.walk`` BFS
        order, so every caller — including the ones that build parent maps from
        walk order — sees an identical sequence. Returns a list (not a
        generator); the installed wrapper yields from it.
        """
        key = id(node)
        cached = self._walk_cache.get(key)
        if cached is not None:
            self.walk_hits += 1
            return cached
        nodes = list(_REAL_AST_WALK(node))
        self._walk_cache[key] = None
        self.walk_misses += 1
        return nodes

    def xǁCheckContextǁwalk__mutmut_13(self, node: ast.AST) -> list[ast.AST]:
        """Memoised ``ast.walk`` — return the full BFS node list for ``node``.

        Because the parse cache returns the SAME tree object for a given file,
        the walk can be done ONCE and the materialised node list shared by
        object identity. Order is byte-for-byte the stdlib ``ast.walk`` BFS
        order, so every caller — including the ones that build parent maps from
        walk order — sees an identical sequence. Returns a list (not a
        generator); the installed wrapper yields from it.
        """
        key = id(node)
        cached = self._walk_cache.get(key)
        if cached is not None:
            self.walk_hits += 1
            return cached
        nodes = list(_REAL_AST_WALK(node))
        self._walk_cache[key] = nodes
        self.walk_misses = 1
        return nodes

    def xǁCheckContextǁwalk__mutmut_14(self, node: ast.AST) -> list[ast.AST]:
        """Memoised ``ast.walk`` — return the full BFS node list for ``node``.

        Because the parse cache returns the SAME tree object for a given file,
        the walk can be done ONCE and the materialised node list shared by
        object identity. Order is byte-for-byte the stdlib ``ast.walk`` BFS
        order, so every caller — including the ones that build parent maps from
        walk order — sees an identical sequence. Returns a list (not a
        generator); the installed wrapper yields from it.
        """
        key = id(node)
        cached = self._walk_cache.get(key)
        if cached is not None:
            self.walk_hits += 1
            return cached
        nodes = list(_REAL_AST_WALK(node))
        self._walk_cache[key] = nodes
        self.walk_misses -= 1
        return nodes

    def xǁCheckContextǁwalk__mutmut_15(self, node: ast.AST) -> list[ast.AST]:
        """Memoised ``ast.walk`` — return the full BFS node list for ``node``.

        Because the parse cache returns the SAME tree object for a given file,
        the walk can be done ONCE and the materialised node list shared by
        object identity. Order is byte-for-byte the stdlib ``ast.walk`` BFS
        order, so every caller — including the ones that build parent maps from
        walk order — sees an identical sequence. Returns a list (not a
        generator); the installed wrapper yields from it.
        """
        key = id(node)
        cached = self._walk_cache.get(key)
        if cached is not None:
            self.walk_hits += 1
            return cached
        nodes = list(_REAL_AST_WALK(node))
        self._walk_cache[key] = nodes
        self.walk_misses += 2
        return nodes

    @property
    def distinct_files_parsed(self) -> int:
        """How many distinct ``(filename, source)`` pairs were parsed — the
        ceiling the parse-once invariant holds against."""
        return self.parse_misses

    # ── installation ─────────────────────────────────────────────────────

    @contextmanager
    def install(self) -> Iterator[CheckContext]:
        """Patch ``ast.parse`` and ``ast.walk`` to route through this context's
        caches for the duration of the ``with`` block, restoring the real
        functions on exit.

        ``ast.parse``: only the plain shapes the fitness checks use are
        memoised — ``ast.parse(source)`` and ``ast.parse(source, filename=...)``.
        Any call passing a non-default ``mode`` / ``type_comments`` /
        ``feature_version`` falls straight through to the real parser uncached,
        so the wrapper can never change semantics for an exotic caller.

        ``ast.walk``: yields from the memoised BFS node list (keyed by tree
        identity), so re-walking a cached tree is a list iteration instead of a
        fresh traversal. The yield order is the stdlib BFS order.
        """

        # Signatures kept loose (``Any``) so the wrappers are drop-in
        # replacements for ``ast.parse`` / ``ast.walk``'s own overloaded shapes.
        def _cached_parse(
            source: Any,
            filename: Any = "<unknown>",
            mode: Any = "exec",
            *args: Any,
            **kwargs: Any,
        ) -> ast.AST:
            # Only the plain ``source`` / ``filename`` shape is memoisable;
            # anything exotic delegates straight to the real parser.
            if mode != "exec" or args or kwargs or not isinstance(source, str):
                exotic: ast.AST = _REAL_AST_PARSE(source, filename, mode, *args, **kwargs)
                return exotic
            return self.parse(source, filename=filename)

        def _cached_walk(node: ast.AST) -> Iterator[ast.AST]:
            yield from self.walk(node)

        prev_parse = ast.parse
        prev_walk = ast.walk
        # ``ast.parse`` is an overloaded stub; assigning a plain callable to it
        # is a deliberate run-scoped memoisation seam (restored in ``finally``),
        # which mypy can't express against the overload set.
        ast.parse = _cached_parse  # type: ignore[assignment]  # run-scoped parse-cache seam; restored in finally
        ast.walk = _cached_walk
        try:
            yield self
        finally:
            # Restore the pristine overloaded stdlib functions captured above.
            ast.parse = prev_parse
            ast.walk = prev_walk

mutants_xǁCheckContextǁ__init____mutmut['_mutmut_orig'] = CheckContext.xǁCheckContextǁ__init____mutmut_orig # type: ignore # mutmut generated
mutants_xǁCheckContextǁ__init____mutmut['xǁCheckContextǁ__init____mutmut_1'] = CheckContext.xǁCheckContextǁ__init____mutmut_1 # type: ignore # mutmut generated
mutants_xǁCheckContextǁ__init____mutmut['xǁCheckContextǁ__init____mutmut_2'] = CheckContext.xǁCheckContextǁ__init____mutmut_2 # type: ignore # mutmut generated
mutants_xǁCheckContextǁ__init____mutmut['xǁCheckContextǁ__init____mutmut_3'] = CheckContext.xǁCheckContextǁ__init____mutmut_3 # type: ignore # mutmut generated
mutants_xǁCheckContextǁ__init____mutmut['xǁCheckContextǁ__init____mutmut_4'] = CheckContext.xǁCheckContextǁ__init____mutmut_4 # type: ignore # mutmut generated
mutants_xǁCheckContextǁ__init____mutmut['xǁCheckContextǁ__init____mutmut_5'] = CheckContext.xǁCheckContextǁ__init____mutmut_5 # type: ignore # mutmut generated
mutants_xǁCheckContextǁ__init____mutmut['xǁCheckContextǁ__init____mutmut_6'] = CheckContext.xǁCheckContextǁ__init____mutmut_6 # type: ignore # mutmut generated
mutants_xǁCheckContextǁ__init____mutmut['xǁCheckContextǁ__init____mutmut_7'] = CheckContext.xǁCheckContextǁ__init____mutmut_7 # type: ignore # mutmut generated
mutants_xǁCheckContextǁ__init____mutmut['xǁCheckContextǁ__init____mutmut_8'] = CheckContext.xǁCheckContextǁ__init____mutmut_8 # type: ignore # mutmut generated
mutants_xǁCheckContextǁ__init____mutmut['xǁCheckContextǁ__init____mutmut_9'] = CheckContext.xǁCheckContextǁ__init____mutmut_9 # type: ignore # mutmut generated
mutants_xǁCheckContextǁ__init____mutmut['xǁCheckContextǁ__init____mutmut_10'] = CheckContext.xǁCheckContextǁ__init____mutmut_10 # type: ignore # mutmut generated
mutants_xǁCheckContextǁ__init____mutmut['xǁCheckContextǁ__init____mutmut_11'] = CheckContext.xǁCheckContextǁ__init____mutmut_11 # type: ignore # mutmut generated
mutants_xǁCheckContextǁ__init____mutmut['xǁCheckContextǁ__init____mutmut_12'] = CheckContext.xǁCheckContextǁ__init____mutmut_12 # type: ignore # mutmut generated
mutants_xǁCheckContextǁ__init____mutmut['xǁCheckContextǁ__init____mutmut_13'] = CheckContext.xǁCheckContextǁ__init____mutmut_13 # type: ignore # mutmut generated
mutants_xǁCheckContextǁ__init____mutmut['xǁCheckContextǁ__init____mutmut_14'] = CheckContext.xǁCheckContextǁ__init____mutmut_14 # type: ignore # mutmut generated

mutants_xǁCheckContextǁpython_files__mutmut['_mutmut_orig'] = CheckContext.xǁCheckContextǁpython_files__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCheckContextǁpython_files__mutmut['xǁCheckContextǁpython_files__mutmut_1'] = CheckContext.xǁCheckContextǁpython_files__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCheckContextǁpython_files__mutmut['xǁCheckContextǁpython_files__mutmut_2'] = CheckContext.xǁCheckContextǁpython_files__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCheckContextǁpython_files__mutmut['xǁCheckContextǁpython_files__mutmut_3'] = CheckContext.xǁCheckContextǁpython_files__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCheckContextǁpython_files__mutmut['xǁCheckContextǁpython_files__mutmut_4'] = CheckContext.xǁCheckContextǁpython_files__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCheckContextǁpython_files__mutmut['xǁCheckContextǁpython_files__mutmut_5'] = CheckContext.xǁCheckContextǁpython_files__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCheckContextǁpython_files__mutmut['xǁCheckContextǁpython_files__mutmut_6'] = CheckContext.xǁCheckContextǁpython_files__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCheckContextǁpython_files__mutmut['xǁCheckContextǁpython_files__mutmut_7'] = CheckContext.xǁCheckContextǁpython_files__mutmut_7 # type: ignore # mutmut generated
mutants_xǁCheckContextǁpython_files__mutmut['xǁCheckContextǁpython_files__mutmut_8'] = CheckContext.xǁCheckContextǁpython_files__mutmut_8 # type: ignore # mutmut generated
mutants_xǁCheckContextǁpython_files__mutmut['xǁCheckContextǁpython_files__mutmut_9'] = CheckContext.xǁCheckContextǁpython_files__mutmut_9 # type: ignore # mutmut generated
mutants_xǁCheckContextǁpython_files__mutmut['xǁCheckContextǁpython_files__mutmut_10'] = CheckContext.xǁCheckContextǁpython_files__mutmut_10 # type: ignore # mutmut generated
mutants_xǁCheckContextǁpython_files__mutmut['xǁCheckContextǁpython_files__mutmut_11'] = CheckContext.xǁCheckContextǁpython_files__mutmut_11 # type: ignore # mutmut generated
mutants_xǁCheckContextǁpython_files__mutmut['xǁCheckContextǁpython_files__mutmut_12'] = CheckContext.xǁCheckContextǁpython_files__mutmut_12 # type: ignore # mutmut generated
mutants_xǁCheckContextǁpython_files__mutmut['xǁCheckContextǁpython_files__mutmut_13'] = CheckContext.xǁCheckContextǁpython_files__mutmut_13 # type: ignore # mutmut generated
mutants_xǁCheckContextǁpython_files__mutmut['xǁCheckContextǁpython_files__mutmut_14'] = CheckContext.xǁCheckContextǁpython_files__mutmut_14 # type: ignore # mutmut generated
mutants_xǁCheckContextǁpython_files__mutmut['xǁCheckContextǁpython_files__mutmut_15'] = CheckContext.xǁCheckContextǁpython_files__mutmut_15 # type: ignore # mutmut generated
mutants_xǁCheckContextǁpython_files__mutmut['xǁCheckContextǁpython_files__mutmut_16'] = CheckContext.xǁCheckContextǁpython_files__mutmut_16 # type: ignore # mutmut generated
mutants_xǁCheckContextǁpython_files__mutmut['xǁCheckContextǁpython_files__mutmut_17'] = CheckContext.xǁCheckContextǁpython_files__mutmut_17 # type: ignore # mutmut generated
mutants_xǁCheckContextǁpython_files__mutmut['xǁCheckContextǁpython_files__mutmut_18'] = CheckContext.xǁCheckContextǁpython_files__mutmut_18 # type: ignore # mutmut generated
mutants_xǁCheckContextǁpython_files__mutmut['xǁCheckContextǁpython_files__mutmut_19'] = CheckContext.xǁCheckContextǁpython_files__mutmut_19 # type: ignore # mutmut generated
mutants_xǁCheckContextǁpython_files__mutmut['xǁCheckContextǁpython_files__mutmut_20'] = CheckContext.xǁCheckContextǁpython_files__mutmut_20 # type: ignore # mutmut generated
mutants_xǁCheckContextǁpython_files__mutmut['xǁCheckContextǁpython_files__mutmut_21'] = CheckContext.xǁCheckContextǁpython_files__mutmut_21 # type: ignore # mutmut generated

mutants_xǁCheckContextǁsource_for__mutmut['_mutmut_orig'] = CheckContext.xǁCheckContextǁsource_for__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCheckContextǁsource_for__mutmut['xǁCheckContextǁsource_for__mutmut_1'] = CheckContext.xǁCheckContextǁsource_for__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCheckContextǁsource_for__mutmut['xǁCheckContextǁsource_for__mutmut_2'] = CheckContext.xǁCheckContextǁsource_for__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCheckContextǁsource_for__mutmut['xǁCheckContextǁsource_for__mutmut_3'] = CheckContext.xǁCheckContextǁsource_for__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCheckContextǁsource_for__mutmut['xǁCheckContextǁsource_for__mutmut_4'] = CheckContext.xǁCheckContextǁsource_for__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCheckContextǁsource_for__mutmut['xǁCheckContextǁsource_for__mutmut_5'] = CheckContext.xǁCheckContextǁsource_for__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCheckContextǁsource_for__mutmut['xǁCheckContextǁsource_for__mutmut_6'] = CheckContext.xǁCheckContextǁsource_for__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCheckContextǁsource_for__mutmut['xǁCheckContextǁsource_for__mutmut_7'] = CheckContext.xǁCheckContextǁsource_for__mutmut_7 # type: ignore # mutmut generated

mutants_xǁCheckContextǁtree_for__mutmut['_mutmut_orig'] = CheckContext.xǁCheckContextǁtree_for__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCheckContextǁtree_for__mutmut['xǁCheckContextǁtree_for__mutmut_1'] = CheckContext.xǁCheckContextǁtree_for__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCheckContextǁtree_for__mutmut['xǁCheckContextǁtree_for__mutmut_2'] = CheckContext.xǁCheckContextǁtree_for__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCheckContextǁtree_for__mutmut['xǁCheckContextǁtree_for__mutmut_3'] = CheckContext.xǁCheckContextǁtree_for__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCheckContextǁtree_for__mutmut['xǁCheckContextǁtree_for__mutmut_4'] = CheckContext.xǁCheckContextǁtree_for__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCheckContextǁtree_for__mutmut['xǁCheckContextǁtree_for__mutmut_5'] = CheckContext.xǁCheckContextǁtree_for__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCheckContextǁtree_for__mutmut['xǁCheckContextǁtree_for__mutmut_6'] = CheckContext.xǁCheckContextǁtree_for__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCheckContextǁtree_for__mutmut['xǁCheckContextǁtree_for__mutmut_7'] = CheckContext.xǁCheckContextǁtree_for__mutmut_7 # type: ignore # mutmut generated
mutants_xǁCheckContextǁtree_for__mutmut['xǁCheckContextǁtree_for__mutmut_8'] = CheckContext.xǁCheckContextǁtree_for__mutmut_8 # type: ignore # mutmut generated

mutants_xǁCheckContextǁparse__mutmut['_mutmut_orig'] = CheckContext.xǁCheckContextǁparse__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCheckContextǁparse__mutmut['xǁCheckContextǁparse__mutmut_1'] = CheckContext.xǁCheckContextǁparse__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCheckContextǁparse__mutmut['xǁCheckContextǁparse__mutmut_2'] = CheckContext.xǁCheckContextǁparse__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCheckContextǁparse__mutmut['xǁCheckContextǁparse__mutmut_3'] = CheckContext.xǁCheckContextǁparse__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCheckContextǁparse__mutmut['xǁCheckContextǁparse__mutmut_4'] = CheckContext.xǁCheckContextǁparse__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCheckContextǁparse__mutmut['xǁCheckContextǁparse__mutmut_5'] = CheckContext.xǁCheckContextǁparse__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCheckContextǁparse__mutmut['xǁCheckContextǁparse__mutmut_6'] = CheckContext.xǁCheckContextǁparse__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCheckContextǁparse__mutmut['xǁCheckContextǁparse__mutmut_7'] = CheckContext.xǁCheckContextǁparse__mutmut_7 # type: ignore # mutmut generated
mutants_xǁCheckContextǁparse__mutmut['xǁCheckContextǁparse__mutmut_8'] = CheckContext.xǁCheckContextǁparse__mutmut_8 # type: ignore # mutmut generated
mutants_xǁCheckContextǁparse__mutmut['xǁCheckContextǁparse__mutmut_9'] = CheckContext.xǁCheckContextǁparse__mutmut_9 # type: ignore # mutmut generated
mutants_xǁCheckContextǁparse__mutmut['xǁCheckContextǁparse__mutmut_10'] = CheckContext.xǁCheckContextǁparse__mutmut_10 # type: ignore # mutmut generated
mutants_xǁCheckContextǁparse__mutmut['xǁCheckContextǁparse__mutmut_11'] = CheckContext.xǁCheckContextǁparse__mutmut_11 # type: ignore # mutmut generated
mutants_xǁCheckContextǁparse__mutmut['xǁCheckContextǁparse__mutmut_12'] = CheckContext.xǁCheckContextǁparse__mutmut_12 # type: ignore # mutmut generated
mutants_xǁCheckContextǁparse__mutmut['xǁCheckContextǁparse__mutmut_13'] = CheckContext.xǁCheckContextǁparse__mutmut_13 # type: ignore # mutmut generated
mutants_xǁCheckContextǁparse__mutmut['xǁCheckContextǁparse__mutmut_14'] = CheckContext.xǁCheckContextǁparse__mutmut_14 # type: ignore # mutmut generated
mutants_xǁCheckContextǁparse__mutmut['xǁCheckContextǁparse__mutmut_15'] = CheckContext.xǁCheckContextǁparse__mutmut_15 # type: ignore # mutmut generated
mutants_xǁCheckContextǁparse__mutmut['xǁCheckContextǁparse__mutmut_16'] = CheckContext.xǁCheckContextǁparse__mutmut_16 # type: ignore # mutmut generated
mutants_xǁCheckContextǁparse__mutmut['xǁCheckContextǁparse__mutmut_17'] = CheckContext.xǁCheckContextǁparse__mutmut_17 # type: ignore # mutmut generated
mutants_xǁCheckContextǁparse__mutmut['xǁCheckContextǁparse__mutmut_18'] = CheckContext.xǁCheckContextǁparse__mutmut_18 # type: ignore # mutmut generated
mutants_xǁCheckContextǁparse__mutmut['xǁCheckContextǁparse__mutmut_19'] = CheckContext.xǁCheckContextǁparse__mutmut_19 # type: ignore # mutmut generated
mutants_xǁCheckContextǁparse__mutmut['xǁCheckContextǁparse__mutmut_20'] = CheckContext.xǁCheckContextǁparse__mutmut_20 # type: ignore # mutmut generated
mutants_xǁCheckContextǁparse__mutmut['xǁCheckContextǁparse__mutmut_21'] = CheckContext.xǁCheckContextǁparse__mutmut_21 # type: ignore # mutmut generated
mutants_xǁCheckContextǁparse__mutmut['xǁCheckContextǁparse__mutmut_22'] = CheckContext.xǁCheckContextǁparse__mutmut_22 # type: ignore # mutmut generated

mutants_xǁCheckContextǁwalk__mutmut['_mutmut_orig'] = CheckContext.xǁCheckContextǁwalk__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCheckContextǁwalk__mutmut['xǁCheckContextǁwalk__mutmut_1'] = CheckContext.xǁCheckContextǁwalk__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCheckContextǁwalk__mutmut['xǁCheckContextǁwalk__mutmut_2'] = CheckContext.xǁCheckContextǁwalk__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCheckContextǁwalk__mutmut['xǁCheckContextǁwalk__mutmut_3'] = CheckContext.xǁCheckContextǁwalk__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCheckContextǁwalk__mutmut['xǁCheckContextǁwalk__mutmut_4'] = CheckContext.xǁCheckContextǁwalk__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCheckContextǁwalk__mutmut['xǁCheckContextǁwalk__mutmut_5'] = CheckContext.xǁCheckContextǁwalk__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCheckContextǁwalk__mutmut['xǁCheckContextǁwalk__mutmut_6'] = CheckContext.xǁCheckContextǁwalk__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCheckContextǁwalk__mutmut['xǁCheckContextǁwalk__mutmut_7'] = CheckContext.xǁCheckContextǁwalk__mutmut_7 # type: ignore # mutmut generated
mutants_xǁCheckContextǁwalk__mutmut['xǁCheckContextǁwalk__mutmut_8'] = CheckContext.xǁCheckContextǁwalk__mutmut_8 # type: ignore # mutmut generated
mutants_xǁCheckContextǁwalk__mutmut['xǁCheckContextǁwalk__mutmut_9'] = CheckContext.xǁCheckContextǁwalk__mutmut_9 # type: ignore # mutmut generated
mutants_xǁCheckContextǁwalk__mutmut['xǁCheckContextǁwalk__mutmut_10'] = CheckContext.xǁCheckContextǁwalk__mutmut_10 # type: ignore # mutmut generated
mutants_xǁCheckContextǁwalk__mutmut['xǁCheckContextǁwalk__mutmut_11'] = CheckContext.xǁCheckContextǁwalk__mutmut_11 # type: ignore # mutmut generated
mutants_xǁCheckContextǁwalk__mutmut['xǁCheckContextǁwalk__mutmut_12'] = CheckContext.xǁCheckContextǁwalk__mutmut_12 # type: ignore # mutmut generated
mutants_xǁCheckContextǁwalk__mutmut['xǁCheckContextǁwalk__mutmut_13'] = CheckContext.xǁCheckContextǁwalk__mutmut_13 # type: ignore # mutmut generated
mutants_xǁCheckContextǁwalk__mutmut['xǁCheckContextǁwalk__mutmut_14'] = CheckContext.xǁCheckContextǁwalk__mutmut_14 # type: ignore # mutmut generated
mutants_xǁCheckContextǁwalk__mutmut['xǁCheckContextǁwalk__mutmut_15'] = CheckContext.xǁCheckContextǁwalk__mutmut_15 # type: ignore # mutmut generated


__all__ = ["CheckContext"]
