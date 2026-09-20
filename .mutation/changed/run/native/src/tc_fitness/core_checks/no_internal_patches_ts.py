"""CORE check: no_internal_patches_ts — TS tests must not mock internal modules.

The TypeScript companion to :mod:`tc_fitness.core_checks.no_internal_patches`.
``vi.mock('../src/foo.js')`` / ``vi.spyOn(internalNs, 'fn')`` (and the ``jest``
equivalents) are the same inappropriate-intimacy anti-pattern wearing a
different language hat: simulating composition instead of exercising it. The
right unit of work is to construct the unit under test with explicit fakes
passed through its constructor / call signature.

Ported from tc-agent-zone ``scripts/checks/no_internal_patches_ts.py`` and
re-expressed as a configurable, repo-agnostic rule. The regex shapes (the mock
/ spy / import grammar) are domain-intrinsic; what was repo-specific is now
consumer config: ``internal_packages`` (workspace package names whose mocking
is the smell). Relative-path
specifiers (``./`` / ``../``) are always internal. The engine ships NO repo
package names.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

REMEDIATION = _remediation(
    fix=(
        "rewrite the test to inject a fake (HTTP client, filesystem adapter, "
        "etc.) through the function/class signature; if the production code "
        "lacks a DI seam, add one. Mocking internal modules hides composition "
        "failures."
    ),
    nxt="re-run this check to confirm the file falls off the violator list.",
    run="python -m tc_fitness.core_checks.no_internal_patches_ts",
    passing="const server = buildServer({ graphClient: fakeGraph, fs: new MemFs() })",
    forbidden="vi.mock('../../src/client.js', () => ({ graphGet: vi.fn() }))",
)

# Domain-intrinsic grammar (the mock / spy / import shapes). Repo-neutral.
_RX_MOCK_STRING = re.compile(
    r"""\b(?:vi|jest)\.(?:do)?[Mm]ock\s*\(\s*(['"`])([^'"`]+)\1""",
    re.MULTILINE,
)
_RX_SPY_ON = re.compile(
    r"""\b(?:vi|jest)\.spyOn\s*\(\s*([A-Za-z_$][\w$]*)\s*,""",
    re.MULTILINE,
)
_RX_IMPORT_NS = re.compile(
    r"""^\s*import\s+\*\s+as\s+([A-Za-z_$][\w$]*)\s+from\s+(['"`])([^'"`]+)\2""",
    re.MULTILINE,
)
_RX_IMPORT_DEFAULT = re.compile(
    r"""^\s*import\s+([A-Za-z_$][\w$]*)(?:\s*,\s*\{[^}]*\})?\s+from\s+(['"`])([^'"`]+)\2""",
    re.MULTILINE,
)
_RX_IMPORT_NAMED = re.compile(
    r"""^\s*import\s+\{([^}]+)\}\s+from\s+(['"`])([^'"`]+)\2""",
    re.MULTILINE,
)
_RX_LINE_COMMENT = re.compile(r"//[^\n]*")
_RX_BLOCK_COMMENT = re.compile(r"/\*[\s\S]*?\*/", re.MULTILINE)
_RX_IDENT = re.compile(r"[A-Za-z_$][\w$]*")


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x__strip_comments__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__strip_comments__mutmut)
def _strip_comments(text: str) -> str:
    """Strip JS/TS comments so example snippets in comments don't fire the gate."""
    text = _RX_BLOCK_COMMENT.sub("", text)
    return _RX_LINE_COMMENT.sub("", text)


def x__strip_comments__mutmut_orig(text: str) -> str:
    """Strip JS/TS comments so example snippets in comments don't fire the gate."""
    text = _RX_BLOCK_COMMENT.sub("", text)
    return _RX_LINE_COMMENT.sub("", text)


def x__strip_comments__mutmut_1(text: str) -> str:
    """Strip JS/TS comments so example snippets in comments don't fire the gate."""
    text = None
    return _RX_LINE_COMMENT.sub("", text)


def x__strip_comments__mutmut_2(text: str) -> str:
    """Strip JS/TS comments so example snippets in comments don't fire the gate."""
    text = _RX_BLOCK_COMMENT.sub(None, text)
    return _RX_LINE_COMMENT.sub("", text)


def x__strip_comments__mutmut_3(text: str) -> str:
    """Strip JS/TS comments so example snippets in comments don't fire the gate."""
    text = _RX_BLOCK_COMMENT.sub("", None)
    return _RX_LINE_COMMENT.sub("", text)


def x__strip_comments__mutmut_4(text: str) -> str:
    """Strip JS/TS comments so example snippets in comments don't fire the gate."""
    text = _RX_BLOCK_COMMENT.sub(text)
    return _RX_LINE_COMMENT.sub("", text)


def x__strip_comments__mutmut_5(text: str) -> str:
    """Strip JS/TS comments so example snippets in comments don't fire the gate."""
    text = _RX_BLOCK_COMMENT.sub("", )
    return _RX_LINE_COMMENT.sub("", text)


def x__strip_comments__mutmut_6(text: str) -> str:
    """Strip JS/TS comments so example snippets in comments don't fire the gate."""
    text = _RX_BLOCK_COMMENT.sub("XXXX", text)
    return _RX_LINE_COMMENT.sub("", text)


def x__strip_comments__mutmut_7(text: str) -> str:
    """Strip JS/TS comments so example snippets in comments don't fire the gate."""
    text = _RX_BLOCK_COMMENT.sub("", text)
    return _RX_LINE_COMMENT.sub(None, text)


def x__strip_comments__mutmut_8(text: str) -> str:
    """Strip JS/TS comments so example snippets in comments don't fire the gate."""
    text = _RX_BLOCK_COMMENT.sub("", text)
    return _RX_LINE_COMMENT.sub("", None)


def x__strip_comments__mutmut_9(text: str) -> str:
    """Strip JS/TS comments so example snippets in comments don't fire the gate."""
    text = _RX_BLOCK_COMMENT.sub("", text)
    return _RX_LINE_COMMENT.sub(text)


def x__strip_comments__mutmut_10(text: str) -> str:
    """Strip JS/TS comments so example snippets in comments don't fire the gate."""
    text = _RX_BLOCK_COMMENT.sub("", text)
    return _RX_LINE_COMMENT.sub("", )


def x__strip_comments__mutmut_11(text: str) -> str:
    """Strip JS/TS comments so example snippets in comments don't fire the gate."""
    text = _RX_BLOCK_COMMENT.sub("", text)
    return _RX_LINE_COMMENT.sub("XXXX", text)

mutants_x__strip_comments__mutmut['_mutmut_orig'] = x__strip_comments__mutmut_orig # type: ignore # mutmut generated
mutants_x__strip_comments__mutmut['x__strip_comments__mutmut_1'] = x__strip_comments__mutmut_1 # type: ignore # mutmut generated
mutants_x__strip_comments__mutmut['x__strip_comments__mutmut_2'] = x__strip_comments__mutmut_2 # type: ignore # mutmut generated
mutants_x__strip_comments__mutmut['x__strip_comments__mutmut_3'] = x__strip_comments__mutmut_3 # type: ignore # mutmut generated
mutants_x__strip_comments__mutmut['x__strip_comments__mutmut_4'] = x__strip_comments__mutmut_4 # type: ignore # mutmut generated
mutants_x__strip_comments__mutmut['x__strip_comments__mutmut_5'] = x__strip_comments__mutmut_5 # type: ignore # mutmut generated
mutants_x__strip_comments__mutmut['x__strip_comments__mutmut_6'] = x__strip_comments__mutmut_6 # type: ignore # mutmut generated
mutants_x__strip_comments__mutmut['x__strip_comments__mutmut_7'] = x__strip_comments__mutmut_7 # type: ignore # mutmut generated
mutants_x__strip_comments__mutmut['x__strip_comments__mutmut_8'] = x__strip_comments__mutmut_8 # type: ignore # mutmut generated
mutants_x__strip_comments__mutmut['x__strip_comments__mutmut_9'] = x__strip_comments__mutmut_9 # type: ignore # mutmut generated
mutants_x__strip_comments__mutmut['x__strip_comments__mutmut_10'] = x__strip_comments__mutmut_10 # type: ignore # mutmut generated
mutants_x__strip_comments__mutmut['x__strip_comments__mutmut_11'] = x__strip_comments__mutmut_11 # type: ignore # mutmut generated
mutants_x__is_internal_specifier__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__is_internal_specifier__mutmut)
def _is_internal_specifier(spec: str, internal_packages: frozenset[str]) -> bool:
    """True iff ``spec`` resolves to an internal module.

    A relative path (``./`` / ``../``) is always internal; otherwise the first
    path segment must be a configured internal workspace package.
    """
    if spec.startswith("./") or spec.startswith("../"):
        return True
    return spec.split("/", 1)[0] in internal_packages


def x__is_internal_specifier__mutmut_orig(spec: str, internal_packages: frozenset[str]) -> bool:
    """True iff ``spec`` resolves to an internal module.

    A relative path (``./`` / ``../``) is always internal; otherwise the first
    path segment must be a configured internal workspace package.
    """
    if spec.startswith("./") or spec.startswith("../"):
        return True
    return spec.split("/", 1)[0] in internal_packages


def x__is_internal_specifier__mutmut_1(spec: str, internal_packages: frozenset[str]) -> bool:
    """True iff ``spec`` resolves to an internal module.

    A relative path (``./`` / ``../``) is always internal; otherwise the first
    path segment must be a configured internal workspace package.
    """
    if spec.startswith("./") and spec.startswith("../"):
        return True
    return spec.split("/", 1)[0] in internal_packages


def x__is_internal_specifier__mutmut_2(spec: str, internal_packages: frozenset[str]) -> bool:
    """True iff ``spec`` resolves to an internal module.

    A relative path (``./`` / ``../``) is always internal; otherwise the first
    path segment must be a configured internal workspace package.
    """
    if spec.startswith(None) or spec.startswith("../"):
        return True
    return spec.split("/", 1)[0] in internal_packages


def x__is_internal_specifier__mutmut_3(spec: str, internal_packages: frozenset[str]) -> bool:
    """True iff ``spec`` resolves to an internal module.

    A relative path (``./`` / ``../``) is always internal; otherwise the first
    path segment must be a configured internal workspace package.
    """
    if spec.startswith("XX./XX") or spec.startswith("../"):
        return True
    return spec.split("/", 1)[0] in internal_packages


def x__is_internal_specifier__mutmut_4(spec: str, internal_packages: frozenset[str]) -> bool:
    """True iff ``spec`` resolves to an internal module.

    A relative path (``./`` / ``../``) is always internal; otherwise the first
    path segment must be a configured internal workspace package.
    """
    if spec.startswith("./") or spec.startswith(None):
        return True
    return spec.split("/", 1)[0] in internal_packages


def x__is_internal_specifier__mutmut_5(spec: str, internal_packages: frozenset[str]) -> bool:
    """True iff ``spec`` resolves to an internal module.

    A relative path (``./`` / ``../``) is always internal; otherwise the first
    path segment must be a configured internal workspace package.
    """
    if spec.startswith("./") or spec.startswith("XX../XX"):
        return True
    return spec.split("/", 1)[0] in internal_packages


def x__is_internal_specifier__mutmut_6(spec: str, internal_packages: frozenset[str]) -> bool:
    """True iff ``spec`` resolves to an internal module.

    A relative path (``./`` / ``../``) is always internal; otherwise the first
    path segment must be a configured internal workspace package.
    """
    if spec.startswith("./") or spec.startswith("../"):
        return False
    return spec.split("/", 1)[0] in internal_packages


def x__is_internal_specifier__mutmut_7(spec: str, internal_packages: frozenset[str]) -> bool:
    """True iff ``spec`` resolves to an internal module.

    A relative path (``./`` / ``../``) is always internal; otherwise the first
    path segment must be a configured internal workspace package.
    """
    if spec.startswith("./") or spec.startswith("../"):
        return True
    return spec.split(None, 1)[0] in internal_packages


def x__is_internal_specifier__mutmut_8(spec: str, internal_packages: frozenset[str]) -> bool:
    """True iff ``spec`` resolves to an internal module.

    A relative path (``./`` / ``../``) is always internal; otherwise the first
    path segment must be a configured internal workspace package.
    """
    if spec.startswith("./") or spec.startswith("../"):
        return True
    return spec.split("/", None)[0] in internal_packages


def x__is_internal_specifier__mutmut_9(spec: str, internal_packages: frozenset[str]) -> bool:
    """True iff ``spec`` resolves to an internal module.

    A relative path (``./`` / ``../``) is always internal; otherwise the first
    path segment must be a configured internal workspace package.
    """
    if spec.startswith("./") or spec.startswith("../"):
        return True
    return spec.split(1)[0] in internal_packages


def x__is_internal_specifier__mutmut_10(spec: str, internal_packages: frozenset[str]) -> bool:
    """True iff ``spec`` resolves to an internal module.

    A relative path (``./`` / ``../``) is always internal; otherwise the first
    path segment must be a configured internal workspace package.
    """
    if spec.startswith("./") or spec.startswith("../"):
        return True
    return spec.split("/", )[0] in internal_packages


def x__is_internal_specifier__mutmut_11(spec: str, internal_packages: frozenset[str]) -> bool:
    """True iff ``spec`` resolves to an internal module.

    A relative path (``./`` / ``../``) is always internal; otherwise the first
    path segment must be a configured internal workspace package.
    """
    if spec.startswith("./") or spec.startswith("../"):
        return True
    return spec.rsplit("/", 1)[0] in internal_packages


def x__is_internal_specifier__mutmut_12(spec: str, internal_packages: frozenset[str]) -> bool:
    """True iff ``spec`` resolves to an internal module.

    A relative path (``./`` / ``../``) is always internal; otherwise the first
    path segment must be a configured internal workspace package.
    """
    if spec.startswith("./") or spec.startswith("../"):
        return True
    return spec.split("XX/XX", 1)[0] in internal_packages


def x__is_internal_specifier__mutmut_13(spec: str, internal_packages: frozenset[str]) -> bool:
    """True iff ``spec`` resolves to an internal module.

    A relative path (``./`` / ``../``) is always internal; otherwise the first
    path segment must be a configured internal workspace package.
    """
    if spec.startswith("./") or spec.startswith("../"):
        return True
    return spec.split("/", 2)[0] in internal_packages


def x__is_internal_specifier__mutmut_14(spec: str, internal_packages: frozenset[str]) -> bool:
    """True iff ``spec`` resolves to an internal module.

    A relative path (``./`` / ``../``) is always internal; otherwise the first
    path segment must be a configured internal workspace package.
    """
    if spec.startswith("./") or spec.startswith("../"):
        return True
    return spec.split("/", 1)[1] in internal_packages


def x__is_internal_specifier__mutmut_15(spec: str, internal_packages: frozenset[str]) -> bool:
    """True iff ``spec`` resolves to an internal module.

    A relative path (``./`` / ``../``) is always internal; otherwise the first
    path segment must be a configured internal workspace package.
    """
    if spec.startswith("./") or spec.startswith("../"):
        return True
    return spec.split("/", 1)[0] not in internal_packages

mutants_x__is_internal_specifier__mutmut['_mutmut_orig'] = x__is_internal_specifier__mutmut_orig # type: ignore # mutmut generated
mutants_x__is_internal_specifier__mutmut['x__is_internal_specifier__mutmut_1'] = x__is_internal_specifier__mutmut_1 # type: ignore # mutmut generated
mutants_x__is_internal_specifier__mutmut['x__is_internal_specifier__mutmut_2'] = x__is_internal_specifier__mutmut_2 # type: ignore # mutmut generated
mutants_x__is_internal_specifier__mutmut['x__is_internal_specifier__mutmut_3'] = x__is_internal_specifier__mutmut_3 # type: ignore # mutmut generated
mutants_x__is_internal_specifier__mutmut['x__is_internal_specifier__mutmut_4'] = x__is_internal_specifier__mutmut_4 # type: ignore # mutmut generated
mutants_x__is_internal_specifier__mutmut['x__is_internal_specifier__mutmut_5'] = x__is_internal_specifier__mutmut_5 # type: ignore # mutmut generated
mutants_x__is_internal_specifier__mutmut['x__is_internal_specifier__mutmut_6'] = x__is_internal_specifier__mutmut_6 # type: ignore # mutmut generated
mutants_x__is_internal_specifier__mutmut['x__is_internal_specifier__mutmut_7'] = x__is_internal_specifier__mutmut_7 # type: ignore # mutmut generated
mutants_x__is_internal_specifier__mutmut['x__is_internal_specifier__mutmut_8'] = x__is_internal_specifier__mutmut_8 # type: ignore # mutmut generated
mutants_x__is_internal_specifier__mutmut['x__is_internal_specifier__mutmut_9'] = x__is_internal_specifier__mutmut_9 # type: ignore # mutmut generated
mutants_x__is_internal_specifier__mutmut['x__is_internal_specifier__mutmut_10'] = x__is_internal_specifier__mutmut_10 # type: ignore # mutmut generated
mutants_x__is_internal_specifier__mutmut['x__is_internal_specifier__mutmut_11'] = x__is_internal_specifier__mutmut_11 # type: ignore # mutmut generated
mutants_x__is_internal_specifier__mutmut['x__is_internal_specifier__mutmut_12'] = x__is_internal_specifier__mutmut_12 # type: ignore # mutmut generated
mutants_x__is_internal_specifier__mutmut['x__is_internal_specifier__mutmut_13'] = x__is_internal_specifier__mutmut_13 # type: ignore # mutmut generated
mutants_x__is_internal_specifier__mutmut['x__is_internal_specifier__mutmut_14'] = x__is_internal_specifier__mutmut_14 # type: ignore # mutmut generated
mutants_x__is_internal_specifier__mutmut['x__is_internal_specifier__mutmut_15'] = x__is_internal_specifier__mutmut_15 # type: ignore # mutmut generated
mutants_x__resolve_imports__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__resolve_imports__mutmut)
def _resolve_imports(text: str) -> dict[str, str]:
    """Map each imported name -> its source specifier (for spyOn resolution)."""
    out: dict[str, str] = {}
    for m in _RX_IMPORT_NS.finditer(text):
        out[m.group(1)] = m.group(3)
    for m in _RX_IMPORT_DEFAULT.finditer(text):
        out.setdefault(m.group(1), m.group(3))
    for m in _RX_IMPORT_NAMED.finditer(text):
        spec = m.group(3)
        for raw in m.group(1).split(","):
            name = raw.strip().split(" as ")[-1].strip()
            if name and _RX_IDENT.fullmatch(name):
                out.setdefault(name, spec)
    return out


def x__resolve_imports__mutmut_orig(text: str) -> dict[str, str]:
    """Map each imported name -> its source specifier (for spyOn resolution)."""
    out: dict[str, str] = {}
    for m in _RX_IMPORT_NS.finditer(text):
        out[m.group(1)] = m.group(3)
    for m in _RX_IMPORT_DEFAULT.finditer(text):
        out.setdefault(m.group(1), m.group(3))
    for m in _RX_IMPORT_NAMED.finditer(text):
        spec = m.group(3)
        for raw in m.group(1).split(","):
            name = raw.strip().split(" as ")[-1].strip()
            if name and _RX_IDENT.fullmatch(name):
                out.setdefault(name, spec)
    return out


def x__resolve_imports__mutmut_1(text: str) -> dict[str, str]:
    """Map each imported name -> its source specifier (for spyOn resolution)."""
    out: dict[str, str] = None
    for m in _RX_IMPORT_NS.finditer(text):
        out[m.group(1)] = m.group(3)
    for m in _RX_IMPORT_DEFAULT.finditer(text):
        out.setdefault(m.group(1), m.group(3))
    for m in _RX_IMPORT_NAMED.finditer(text):
        spec = m.group(3)
        for raw in m.group(1).split(","):
            name = raw.strip().split(" as ")[-1].strip()
            if name and _RX_IDENT.fullmatch(name):
                out.setdefault(name, spec)
    return out


def x__resolve_imports__mutmut_2(text: str) -> dict[str, str]:
    """Map each imported name -> its source specifier (for spyOn resolution)."""
    out: dict[str, str] = {}
    for m in _RX_IMPORT_NS.finditer(None):
        out[m.group(1)] = m.group(3)
    for m in _RX_IMPORT_DEFAULT.finditer(text):
        out.setdefault(m.group(1), m.group(3))
    for m in _RX_IMPORT_NAMED.finditer(text):
        spec = m.group(3)
        for raw in m.group(1).split(","):
            name = raw.strip().split(" as ")[-1].strip()
            if name and _RX_IDENT.fullmatch(name):
                out.setdefault(name, spec)
    return out


def x__resolve_imports__mutmut_3(text: str) -> dict[str, str]:
    """Map each imported name -> its source specifier (for spyOn resolution)."""
    out: dict[str, str] = {}
    for m in _RX_IMPORT_NS.finditer(text):
        out[m.group(1)] = None
    for m in _RX_IMPORT_DEFAULT.finditer(text):
        out.setdefault(m.group(1), m.group(3))
    for m in _RX_IMPORT_NAMED.finditer(text):
        spec = m.group(3)
        for raw in m.group(1).split(","):
            name = raw.strip().split(" as ")[-1].strip()
            if name and _RX_IDENT.fullmatch(name):
                out.setdefault(name, spec)
    return out


def x__resolve_imports__mutmut_4(text: str) -> dict[str, str]:
    """Map each imported name -> its source specifier (for spyOn resolution)."""
    out: dict[str, str] = {}
    for m in _RX_IMPORT_NS.finditer(text):
        out[m.group(None)] = m.group(3)
    for m in _RX_IMPORT_DEFAULT.finditer(text):
        out.setdefault(m.group(1), m.group(3))
    for m in _RX_IMPORT_NAMED.finditer(text):
        spec = m.group(3)
        for raw in m.group(1).split(","):
            name = raw.strip().split(" as ")[-1].strip()
            if name and _RX_IDENT.fullmatch(name):
                out.setdefault(name, spec)
    return out


def x__resolve_imports__mutmut_5(text: str) -> dict[str, str]:
    """Map each imported name -> its source specifier (for spyOn resolution)."""
    out: dict[str, str] = {}
    for m in _RX_IMPORT_NS.finditer(text):
        out[m.group(2)] = m.group(3)
    for m in _RX_IMPORT_DEFAULT.finditer(text):
        out.setdefault(m.group(1), m.group(3))
    for m in _RX_IMPORT_NAMED.finditer(text):
        spec = m.group(3)
        for raw in m.group(1).split(","):
            name = raw.strip().split(" as ")[-1].strip()
            if name and _RX_IDENT.fullmatch(name):
                out.setdefault(name, spec)
    return out


def x__resolve_imports__mutmut_6(text: str) -> dict[str, str]:
    """Map each imported name -> its source specifier (for spyOn resolution)."""
    out: dict[str, str] = {}
    for m in _RX_IMPORT_NS.finditer(text):
        out[m.group(1)] = m.group(None)
    for m in _RX_IMPORT_DEFAULT.finditer(text):
        out.setdefault(m.group(1), m.group(3))
    for m in _RX_IMPORT_NAMED.finditer(text):
        spec = m.group(3)
        for raw in m.group(1).split(","):
            name = raw.strip().split(" as ")[-1].strip()
            if name and _RX_IDENT.fullmatch(name):
                out.setdefault(name, spec)
    return out


def x__resolve_imports__mutmut_7(text: str) -> dict[str, str]:
    """Map each imported name -> its source specifier (for spyOn resolution)."""
    out: dict[str, str] = {}
    for m in _RX_IMPORT_NS.finditer(text):
        out[m.group(1)] = m.group(4)
    for m in _RX_IMPORT_DEFAULT.finditer(text):
        out.setdefault(m.group(1), m.group(3))
    for m in _RX_IMPORT_NAMED.finditer(text):
        spec = m.group(3)
        for raw in m.group(1).split(","):
            name = raw.strip().split(" as ")[-1].strip()
            if name and _RX_IDENT.fullmatch(name):
                out.setdefault(name, spec)
    return out


def x__resolve_imports__mutmut_8(text: str) -> dict[str, str]:
    """Map each imported name -> its source specifier (for spyOn resolution)."""
    out: dict[str, str] = {}
    for m in _RX_IMPORT_NS.finditer(text):
        out[m.group(1)] = m.group(3)
    for m in _RX_IMPORT_DEFAULT.finditer(None):
        out.setdefault(m.group(1), m.group(3))
    for m in _RX_IMPORT_NAMED.finditer(text):
        spec = m.group(3)
        for raw in m.group(1).split(","):
            name = raw.strip().split(" as ")[-1].strip()
            if name and _RX_IDENT.fullmatch(name):
                out.setdefault(name, spec)
    return out


def x__resolve_imports__mutmut_9(text: str) -> dict[str, str]:
    """Map each imported name -> its source specifier (for spyOn resolution)."""
    out: dict[str, str] = {}
    for m in _RX_IMPORT_NS.finditer(text):
        out[m.group(1)] = m.group(3)
    for m in _RX_IMPORT_DEFAULT.finditer(text):
        out.setdefault(None, m.group(3))
    for m in _RX_IMPORT_NAMED.finditer(text):
        spec = m.group(3)
        for raw in m.group(1).split(","):
            name = raw.strip().split(" as ")[-1].strip()
            if name and _RX_IDENT.fullmatch(name):
                out.setdefault(name, spec)
    return out


def x__resolve_imports__mutmut_10(text: str) -> dict[str, str]:
    """Map each imported name -> its source specifier (for spyOn resolution)."""
    out: dict[str, str] = {}
    for m in _RX_IMPORT_NS.finditer(text):
        out[m.group(1)] = m.group(3)
    for m in _RX_IMPORT_DEFAULT.finditer(text):
        out.setdefault(m.group(1), None)
    for m in _RX_IMPORT_NAMED.finditer(text):
        spec = m.group(3)
        for raw in m.group(1).split(","):
            name = raw.strip().split(" as ")[-1].strip()
            if name and _RX_IDENT.fullmatch(name):
                out.setdefault(name, spec)
    return out


def x__resolve_imports__mutmut_11(text: str) -> dict[str, str]:
    """Map each imported name -> its source specifier (for spyOn resolution)."""
    out: dict[str, str] = {}
    for m in _RX_IMPORT_NS.finditer(text):
        out[m.group(1)] = m.group(3)
    for m in _RX_IMPORT_DEFAULT.finditer(text):
        out.setdefault(m.group(3))
    for m in _RX_IMPORT_NAMED.finditer(text):
        spec = m.group(3)
        for raw in m.group(1).split(","):
            name = raw.strip().split(" as ")[-1].strip()
            if name and _RX_IDENT.fullmatch(name):
                out.setdefault(name, spec)
    return out


def x__resolve_imports__mutmut_12(text: str) -> dict[str, str]:
    """Map each imported name -> its source specifier (for spyOn resolution)."""
    out: dict[str, str] = {}
    for m in _RX_IMPORT_NS.finditer(text):
        out[m.group(1)] = m.group(3)
    for m in _RX_IMPORT_DEFAULT.finditer(text):
        out.setdefault(m.group(1), )
    for m in _RX_IMPORT_NAMED.finditer(text):
        spec = m.group(3)
        for raw in m.group(1).split(","):
            name = raw.strip().split(" as ")[-1].strip()
            if name and _RX_IDENT.fullmatch(name):
                out.setdefault(name, spec)
    return out


def x__resolve_imports__mutmut_13(text: str) -> dict[str, str]:
    """Map each imported name -> its source specifier (for spyOn resolution)."""
    out: dict[str, str] = {}
    for m in _RX_IMPORT_NS.finditer(text):
        out[m.group(1)] = m.group(3)
    for m in _RX_IMPORT_DEFAULT.finditer(text):
        out.setdefault(m.group(None), m.group(3))
    for m in _RX_IMPORT_NAMED.finditer(text):
        spec = m.group(3)
        for raw in m.group(1).split(","):
            name = raw.strip().split(" as ")[-1].strip()
            if name and _RX_IDENT.fullmatch(name):
                out.setdefault(name, spec)
    return out


def x__resolve_imports__mutmut_14(text: str) -> dict[str, str]:
    """Map each imported name -> its source specifier (for spyOn resolution)."""
    out: dict[str, str] = {}
    for m in _RX_IMPORT_NS.finditer(text):
        out[m.group(1)] = m.group(3)
    for m in _RX_IMPORT_DEFAULT.finditer(text):
        out.setdefault(m.group(2), m.group(3))
    for m in _RX_IMPORT_NAMED.finditer(text):
        spec = m.group(3)
        for raw in m.group(1).split(","):
            name = raw.strip().split(" as ")[-1].strip()
            if name and _RX_IDENT.fullmatch(name):
                out.setdefault(name, spec)
    return out


def x__resolve_imports__mutmut_15(text: str) -> dict[str, str]:
    """Map each imported name -> its source specifier (for spyOn resolution)."""
    out: dict[str, str] = {}
    for m in _RX_IMPORT_NS.finditer(text):
        out[m.group(1)] = m.group(3)
    for m in _RX_IMPORT_DEFAULT.finditer(text):
        out.setdefault(m.group(1), m.group(None))
    for m in _RX_IMPORT_NAMED.finditer(text):
        spec = m.group(3)
        for raw in m.group(1).split(","):
            name = raw.strip().split(" as ")[-1].strip()
            if name and _RX_IDENT.fullmatch(name):
                out.setdefault(name, spec)
    return out


def x__resolve_imports__mutmut_16(text: str) -> dict[str, str]:
    """Map each imported name -> its source specifier (for spyOn resolution)."""
    out: dict[str, str] = {}
    for m in _RX_IMPORT_NS.finditer(text):
        out[m.group(1)] = m.group(3)
    for m in _RX_IMPORT_DEFAULT.finditer(text):
        out.setdefault(m.group(1), m.group(4))
    for m in _RX_IMPORT_NAMED.finditer(text):
        spec = m.group(3)
        for raw in m.group(1).split(","):
            name = raw.strip().split(" as ")[-1].strip()
            if name and _RX_IDENT.fullmatch(name):
                out.setdefault(name, spec)
    return out


def x__resolve_imports__mutmut_17(text: str) -> dict[str, str]:
    """Map each imported name -> its source specifier (for spyOn resolution)."""
    out: dict[str, str] = {}
    for m in _RX_IMPORT_NS.finditer(text):
        out[m.group(1)] = m.group(3)
    for m in _RX_IMPORT_DEFAULT.finditer(text):
        out.setdefault(m.group(1), m.group(3))
    for m in _RX_IMPORT_NAMED.finditer(None):
        spec = m.group(3)
        for raw in m.group(1).split(","):
            name = raw.strip().split(" as ")[-1].strip()
            if name and _RX_IDENT.fullmatch(name):
                out.setdefault(name, spec)
    return out


def x__resolve_imports__mutmut_18(text: str) -> dict[str, str]:
    """Map each imported name -> its source specifier (for spyOn resolution)."""
    out: dict[str, str] = {}
    for m in _RX_IMPORT_NS.finditer(text):
        out[m.group(1)] = m.group(3)
    for m in _RX_IMPORT_DEFAULT.finditer(text):
        out.setdefault(m.group(1), m.group(3))
    for m in _RX_IMPORT_NAMED.finditer(text):
        spec = None
        for raw in m.group(1).split(","):
            name = raw.strip().split(" as ")[-1].strip()
            if name and _RX_IDENT.fullmatch(name):
                out.setdefault(name, spec)
    return out


def x__resolve_imports__mutmut_19(text: str) -> dict[str, str]:
    """Map each imported name -> its source specifier (for spyOn resolution)."""
    out: dict[str, str] = {}
    for m in _RX_IMPORT_NS.finditer(text):
        out[m.group(1)] = m.group(3)
    for m in _RX_IMPORT_DEFAULT.finditer(text):
        out.setdefault(m.group(1), m.group(3))
    for m in _RX_IMPORT_NAMED.finditer(text):
        spec = m.group(None)
        for raw in m.group(1).split(","):
            name = raw.strip().split(" as ")[-1].strip()
            if name and _RX_IDENT.fullmatch(name):
                out.setdefault(name, spec)
    return out


def x__resolve_imports__mutmut_20(text: str) -> dict[str, str]:
    """Map each imported name -> its source specifier (for spyOn resolution)."""
    out: dict[str, str] = {}
    for m in _RX_IMPORT_NS.finditer(text):
        out[m.group(1)] = m.group(3)
    for m in _RX_IMPORT_DEFAULT.finditer(text):
        out.setdefault(m.group(1), m.group(3))
    for m in _RX_IMPORT_NAMED.finditer(text):
        spec = m.group(4)
        for raw in m.group(1).split(","):
            name = raw.strip().split(" as ")[-1].strip()
            if name and _RX_IDENT.fullmatch(name):
                out.setdefault(name, spec)
    return out


def x__resolve_imports__mutmut_21(text: str) -> dict[str, str]:
    """Map each imported name -> its source specifier (for spyOn resolution)."""
    out: dict[str, str] = {}
    for m in _RX_IMPORT_NS.finditer(text):
        out[m.group(1)] = m.group(3)
    for m in _RX_IMPORT_DEFAULT.finditer(text):
        out.setdefault(m.group(1), m.group(3))
    for m in _RX_IMPORT_NAMED.finditer(text):
        spec = m.group(3)
        for raw in m.group(1).split(None):
            name = raw.strip().split(" as ")[-1].strip()
            if name and _RX_IDENT.fullmatch(name):
                out.setdefault(name, spec)
    return out


def x__resolve_imports__mutmut_22(text: str) -> dict[str, str]:
    """Map each imported name -> its source specifier (for spyOn resolution)."""
    out: dict[str, str] = {}
    for m in _RX_IMPORT_NS.finditer(text):
        out[m.group(1)] = m.group(3)
    for m in _RX_IMPORT_DEFAULT.finditer(text):
        out.setdefault(m.group(1), m.group(3))
    for m in _RX_IMPORT_NAMED.finditer(text):
        spec = m.group(3)
        for raw in m.group(None).split(","):
            name = raw.strip().split(" as ")[-1].strip()
            if name and _RX_IDENT.fullmatch(name):
                out.setdefault(name, spec)
    return out


def x__resolve_imports__mutmut_23(text: str) -> dict[str, str]:
    """Map each imported name -> its source specifier (for spyOn resolution)."""
    out: dict[str, str] = {}
    for m in _RX_IMPORT_NS.finditer(text):
        out[m.group(1)] = m.group(3)
    for m in _RX_IMPORT_DEFAULT.finditer(text):
        out.setdefault(m.group(1), m.group(3))
    for m in _RX_IMPORT_NAMED.finditer(text):
        spec = m.group(3)
        for raw in m.group(2).split(","):
            name = raw.strip().split(" as ")[-1].strip()
            if name and _RX_IDENT.fullmatch(name):
                out.setdefault(name, spec)
    return out


def x__resolve_imports__mutmut_24(text: str) -> dict[str, str]:
    """Map each imported name -> its source specifier (for spyOn resolution)."""
    out: dict[str, str] = {}
    for m in _RX_IMPORT_NS.finditer(text):
        out[m.group(1)] = m.group(3)
    for m in _RX_IMPORT_DEFAULT.finditer(text):
        out.setdefault(m.group(1), m.group(3))
    for m in _RX_IMPORT_NAMED.finditer(text):
        spec = m.group(3)
        for raw in m.group(1).split("XX,XX"):
            name = raw.strip().split(" as ")[-1].strip()
            if name and _RX_IDENT.fullmatch(name):
                out.setdefault(name, spec)
    return out


def x__resolve_imports__mutmut_25(text: str) -> dict[str, str]:
    """Map each imported name -> its source specifier (for spyOn resolution)."""
    out: dict[str, str] = {}
    for m in _RX_IMPORT_NS.finditer(text):
        out[m.group(1)] = m.group(3)
    for m in _RX_IMPORT_DEFAULT.finditer(text):
        out.setdefault(m.group(1), m.group(3))
    for m in _RX_IMPORT_NAMED.finditer(text):
        spec = m.group(3)
        for raw in m.group(1).split(","):
            name = None
            if name and _RX_IDENT.fullmatch(name):
                out.setdefault(name, spec)
    return out


def x__resolve_imports__mutmut_26(text: str) -> dict[str, str]:
    """Map each imported name -> its source specifier (for spyOn resolution)."""
    out: dict[str, str] = {}
    for m in _RX_IMPORT_NS.finditer(text):
        out[m.group(1)] = m.group(3)
    for m in _RX_IMPORT_DEFAULT.finditer(text):
        out.setdefault(m.group(1), m.group(3))
    for m in _RX_IMPORT_NAMED.finditer(text):
        spec = m.group(3)
        for raw in m.group(1).split(","):
            name = raw.strip().split(None)[-1].strip()
            if name and _RX_IDENT.fullmatch(name):
                out.setdefault(name, spec)
    return out


def x__resolve_imports__mutmut_27(text: str) -> dict[str, str]:
    """Map each imported name -> its source specifier (for spyOn resolution)."""
    out: dict[str, str] = {}
    for m in _RX_IMPORT_NS.finditer(text):
        out[m.group(1)] = m.group(3)
    for m in _RX_IMPORT_DEFAULT.finditer(text):
        out.setdefault(m.group(1), m.group(3))
    for m in _RX_IMPORT_NAMED.finditer(text):
        spec = m.group(3)
        for raw in m.group(1).split(","):
            name = raw.strip().split("XX as XX")[-1].strip()
            if name and _RX_IDENT.fullmatch(name):
                out.setdefault(name, spec)
    return out


def x__resolve_imports__mutmut_28(text: str) -> dict[str, str]:
    """Map each imported name -> its source specifier (for spyOn resolution)."""
    out: dict[str, str] = {}
    for m in _RX_IMPORT_NS.finditer(text):
        out[m.group(1)] = m.group(3)
    for m in _RX_IMPORT_DEFAULT.finditer(text):
        out.setdefault(m.group(1), m.group(3))
    for m in _RX_IMPORT_NAMED.finditer(text):
        spec = m.group(3)
        for raw in m.group(1).split(","):
            name = raw.strip().split(" AS ")[-1].strip()
            if name and _RX_IDENT.fullmatch(name):
                out.setdefault(name, spec)
    return out


def x__resolve_imports__mutmut_29(text: str) -> dict[str, str]:
    """Map each imported name -> its source specifier (for spyOn resolution)."""
    out: dict[str, str] = {}
    for m in _RX_IMPORT_NS.finditer(text):
        out[m.group(1)] = m.group(3)
    for m in _RX_IMPORT_DEFAULT.finditer(text):
        out.setdefault(m.group(1), m.group(3))
    for m in _RX_IMPORT_NAMED.finditer(text):
        spec = m.group(3)
        for raw in m.group(1).split(","):
            name = raw.strip().split(" as ")[+1].strip()
            if name and _RX_IDENT.fullmatch(name):
                out.setdefault(name, spec)
    return out


def x__resolve_imports__mutmut_30(text: str) -> dict[str, str]:
    """Map each imported name -> its source specifier (for spyOn resolution)."""
    out: dict[str, str] = {}
    for m in _RX_IMPORT_NS.finditer(text):
        out[m.group(1)] = m.group(3)
    for m in _RX_IMPORT_DEFAULT.finditer(text):
        out.setdefault(m.group(1), m.group(3))
    for m in _RX_IMPORT_NAMED.finditer(text):
        spec = m.group(3)
        for raw in m.group(1).split(","):
            name = raw.strip().split(" as ")[-2].strip()
            if name and _RX_IDENT.fullmatch(name):
                out.setdefault(name, spec)
    return out


def x__resolve_imports__mutmut_31(text: str) -> dict[str, str]:
    """Map each imported name -> its source specifier (for spyOn resolution)."""
    out: dict[str, str] = {}
    for m in _RX_IMPORT_NS.finditer(text):
        out[m.group(1)] = m.group(3)
    for m in _RX_IMPORT_DEFAULT.finditer(text):
        out.setdefault(m.group(1), m.group(3))
    for m in _RX_IMPORT_NAMED.finditer(text):
        spec = m.group(3)
        for raw in m.group(1).split(","):
            name = raw.strip().split(" as ")[-1].strip()
            if name or _RX_IDENT.fullmatch(name):
                out.setdefault(name, spec)
    return out


def x__resolve_imports__mutmut_32(text: str) -> dict[str, str]:
    """Map each imported name -> its source specifier (for spyOn resolution)."""
    out: dict[str, str] = {}
    for m in _RX_IMPORT_NS.finditer(text):
        out[m.group(1)] = m.group(3)
    for m in _RX_IMPORT_DEFAULT.finditer(text):
        out.setdefault(m.group(1), m.group(3))
    for m in _RX_IMPORT_NAMED.finditer(text):
        spec = m.group(3)
        for raw in m.group(1).split(","):
            name = raw.strip().split(" as ")[-1].strip()
            if name and _RX_IDENT.fullmatch(None):
                out.setdefault(name, spec)
    return out


def x__resolve_imports__mutmut_33(text: str) -> dict[str, str]:
    """Map each imported name -> its source specifier (for spyOn resolution)."""
    out: dict[str, str] = {}
    for m in _RX_IMPORT_NS.finditer(text):
        out[m.group(1)] = m.group(3)
    for m in _RX_IMPORT_DEFAULT.finditer(text):
        out.setdefault(m.group(1), m.group(3))
    for m in _RX_IMPORT_NAMED.finditer(text):
        spec = m.group(3)
        for raw in m.group(1).split(","):
            name = raw.strip().split(" as ")[-1].strip()
            if name and _RX_IDENT.fullmatch(name):
                out.setdefault(None, spec)
    return out


def x__resolve_imports__mutmut_34(text: str) -> dict[str, str]:
    """Map each imported name -> its source specifier (for spyOn resolution)."""
    out: dict[str, str] = {}
    for m in _RX_IMPORT_NS.finditer(text):
        out[m.group(1)] = m.group(3)
    for m in _RX_IMPORT_DEFAULT.finditer(text):
        out.setdefault(m.group(1), m.group(3))
    for m in _RX_IMPORT_NAMED.finditer(text):
        spec = m.group(3)
        for raw in m.group(1).split(","):
            name = raw.strip().split(" as ")[-1].strip()
            if name and _RX_IDENT.fullmatch(name):
                out.setdefault(name, None)
    return out


def x__resolve_imports__mutmut_35(text: str) -> dict[str, str]:
    """Map each imported name -> its source specifier (for spyOn resolution)."""
    out: dict[str, str] = {}
    for m in _RX_IMPORT_NS.finditer(text):
        out[m.group(1)] = m.group(3)
    for m in _RX_IMPORT_DEFAULT.finditer(text):
        out.setdefault(m.group(1), m.group(3))
    for m in _RX_IMPORT_NAMED.finditer(text):
        spec = m.group(3)
        for raw in m.group(1).split(","):
            name = raw.strip().split(" as ")[-1].strip()
            if name and _RX_IDENT.fullmatch(name):
                out.setdefault(spec)
    return out


def x__resolve_imports__mutmut_36(text: str) -> dict[str, str]:
    """Map each imported name -> its source specifier (for spyOn resolution)."""
    out: dict[str, str] = {}
    for m in _RX_IMPORT_NS.finditer(text):
        out[m.group(1)] = m.group(3)
    for m in _RX_IMPORT_DEFAULT.finditer(text):
        out.setdefault(m.group(1), m.group(3))
    for m in _RX_IMPORT_NAMED.finditer(text):
        spec = m.group(3)
        for raw in m.group(1).split(","):
            name = raw.strip().split(" as ")[-1].strip()
            if name and _RX_IDENT.fullmatch(name):
                out.setdefault(name, )
    return out

mutants_x__resolve_imports__mutmut['_mutmut_orig'] = x__resolve_imports__mutmut_orig # type: ignore # mutmut generated
mutants_x__resolve_imports__mutmut['x__resolve_imports__mutmut_1'] = x__resolve_imports__mutmut_1 # type: ignore # mutmut generated
mutants_x__resolve_imports__mutmut['x__resolve_imports__mutmut_2'] = x__resolve_imports__mutmut_2 # type: ignore # mutmut generated
mutants_x__resolve_imports__mutmut['x__resolve_imports__mutmut_3'] = x__resolve_imports__mutmut_3 # type: ignore # mutmut generated
mutants_x__resolve_imports__mutmut['x__resolve_imports__mutmut_4'] = x__resolve_imports__mutmut_4 # type: ignore # mutmut generated
mutants_x__resolve_imports__mutmut['x__resolve_imports__mutmut_5'] = x__resolve_imports__mutmut_5 # type: ignore # mutmut generated
mutants_x__resolve_imports__mutmut['x__resolve_imports__mutmut_6'] = x__resolve_imports__mutmut_6 # type: ignore # mutmut generated
mutants_x__resolve_imports__mutmut['x__resolve_imports__mutmut_7'] = x__resolve_imports__mutmut_7 # type: ignore # mutmut generated
mutants_x__resolve_imports__mutmut['x__resolve_imports__mutmut_8'] = x__resolve_imports__mutmut_8 # type: ignore # mutmut generated
mutants_x__resolve_imports__mutmut['x__resolve_imports__mutmut_9'] = x__resolve_imports__mutmut_9 # type: ignore # mutmut generated
mutants_x__resolve_imports__mutmut['x__resolve_imports__mutmut_10'] = x__resolve_imports__mutmut_10 # type: ignore # mutmut generated
mutants_x__resolve_imports__mutmut['x__resolve_imports__mutmut_11'] = x__resolve_imports__mutmut_11 # type: ignore # mutmut generated
mutants_x__resolve_imports__mutmut['x__resolve_imports__mutmut_12'] = x__resolve_imports__mutmut_12 # type: ignore # mutmut generated
mutants_x__resolve_imports__mutmut['x__resolve_imports__mutmut_13'] = x__resolve_imports__mutmut_13 # type: ignore # mutmut generated
mutants_x__resolve_imports__mutmut['x__resolve_imports__mutmut_14'] = x__resolve_imports__mutmut_14 # type: ignore # mutmut generated
mutants_x__resolve_imports__mutmut['x__resolve_imports__mutmut_15'] = x__resolve_imports__mutmut_15 # type: ignore # mutmut generated
mutants_x__resolve_imports__mutmut['x__resolve_imports__mutmut_16'] = x__resolve_imports__mutmut_16 # type: ignore # mutmut generated
mutants_x__resolve_imports__mutmut['x__resolve_imports__mutmut_17'] = x__resolve_imports__mutmut_17 # type: ignore # mutmut generated
mutants_x__resolve_imports__mutmut['x__resolve_imports__mutmut_18'] = x__resolve_imports__mutmut_18 # type: ignore # mutmut generated
mutants_x__resolve_imports__mutmut['x__resolve_imports__mutmut_19'] = x__resolve_imports__mutmut_19 # type: ignore # mutmut generated
mutants_x__resolve_imports__mutmut['x__resolve_imports__mutmut_20'] = x__resolve_imports__mutmut_20 # type: ignore # mutmut generated
mutants_x__resolve_imports__mutmut['x__resolve_imports__mutmut_21'] = x__resolve_imports__mutmut_21 # type: ignore # mutmut generated
mutants_x__resolve_imports__mutmut['x__resolve_imports__mutmut_22'] = x__resolve_imports__mutmut_22 # type: ignore # mutmut generated
mutants_x__resolve_imports__mutmut['x__resolve_imports__mutmut_23'] = x__resolve_imports__mutmut_23 # type: ignore # mutmut generated
mutants_x__resolve_imports__mutmut['x__resolve_imports__mutmut_24'] = x__resolve_imports__mutmut_24 # type: ignore # mutmut generated
mutants_x__resolve_imports__mutmut['x__resolve_imports__mutmut_25'] = x__resolve_imports__mutmut_25 # type: ignore # mutmut generated
mutants_x__resolve_imports__mutmut['x__resolve_imports__mutmut_26'] = x__resolve_imports__mutmut_26 # type: ignore # mutmut generated
mutants_x__resolve_imports__mutmut['x__resolve_imports__mutmut_27'] = x__resolve_imports__mutmut_27 # type: ignore # mutmut generated
mutants_x__resolve_imports__mutmut['x__resolve_imports__mutmut_28'] = x__resolve_imports__mutmut_28 # type: ignore # mutmut generated
mutants_x__resolve_imports__mutmut['x__resolve_imports__mutmut_29'] = x__resolve_imports__mutmut_29 # type: ignore # mutmut generated
mutants_x__resolve_imports__mutmut['x__resolve_imports__mutmut_30'] = x__resolve_imports__mutmut_30 # type: ignore # mutmut generated
mutants_x__resolve_imports__mutmut['x__resolve_imports__mutmut_31'] = x__resolve_imports__mutmut_31 # type: ignore # mutmut generated
mutants_x__resolve_imports__mutmut['x__resolve_imports__mutmut_32'] = x__resolve_imports__mutmut_32 # type: ignore # mutmut generated
mutants_x__resolve_imports__mutmut['x__resolve_imports__mutmut_33'] = x__resolve_imports__mutmut_33 # type: ignore # mutmut generated
mutants_x__resolve_imports__mutmut['x__resolve_imports__mutmut_34'] = x__resolve_imports__mutmut_34 # type: ignore # mutmut generated
mutants_x__resolve_imports__mutmut['x__resolve_imports__mutmut_35'] = x__resolve_imports__mutmut_35 # type: ignore # mutmut generated
mutants_x__resolve_imports__mutmut['x__resolve_imports__mutmut_36'] = x__resolve_imports__mutmut_36 # type: ignore # mutmut generated
mutants_x_file_mocks_internal_ts__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_file_mocks_internal_ts__mutmut)
def file_mocks_internal_ts(
    path: Path,
    *,
    internal_packages: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` mocks/spies an internal module.

    A read error is treated as "no violation" (another check owns unreadable
    files).
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    stripped = _strip_comments(text)
    for m in _RX_MOCK_STRING.finditer(stripped):
        spec = m.group(2)
        if _is_internal_specifier(spec, internal_packages):
            return True
    imports = _resolve_imports(stripped)
    for m in _RX_SPY_ON.finditer(stripped):
        spec = imports.get(m.group(1))
        if spec is None:
            continue
        if _is_internal_specifier(spec, internal_packages):
            return True
    return False


def x_file_mocks_internal_ts__mutmut_orig(
    path: Path,
    *,
    internal_packages: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` mocks/spies an internal module.

    A read error is treated as "no violation" (another check owns unreadable
    files).
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    stripped = _strip_comments(text)
    for m in _RX_MOCK_STRING.finditer(stripped):
        spec = m.group(2)
        if _is_internal_specifier(spec, internal_packages):
            return True
    imports = _resolve_imports(stripped)
    for m in _RX_SPY_ON.finditer(stripped):
        spec = imports.get(m.group(1))
        if spec is None:
            continue
        if _is_internal_specifier(spec, internal_packages):
            return True
    return False


def x_file_mocks_internal_ts__mutmut_1(
    path: Path,
    *,
    internal_packages: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` mocks/spies an internal module.

    A read error is treated as "no violation" (another check owns unreadable
    files).
    """
    try:
        text = None
    except OSError:
        return False
    stripped = _strip_comments(text)
    for m in _RX_MOCK_STRING.finditer(stripped):
        spec = m.group(2)
        if _is_internal_specifier(spec, internal_packages):
            return True
    imports = _resolve_imports(stripped)
    for m in _RX_SPY_ON.finditer(stripped):
        spec = imports.get(m.group(1))
        if spec is None:
            continue
        if _is_internal_specifier(spec, internal_packages):
            return True
    return False


def x_file_mocks_internal_ts__mutmut_2(
    path: Path,
    *,
    internal_packages: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` mocks/spies an internal module.

    A read error is treated as "no violation" (another check owns unreadable
    files).
    """
    try:
        text = path.read_text(encoding=None)
    except OSError:
        return False
    stripped = _strip_comments(text)
    for m in _RX_MOCK_STRING.finditer(stripped):
        spec = m.group(2)
        if _is_internal_specifier(spec, internal_packages):
            return True
    imports = _resolve_imports(stripped)
    for m in _RX_SPY_ON.finditer(stripped):
        spec = imports.get(m.group(1))
        if spec is None:
            continue
        if _is_internal_specifier(spec, internal_packages):
            return True
    return False


def x_file_mocks_internal_ts__mutmut_3(
    path: Path,
    *,
    internal_packages: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` mocks/spies an internal module.

    A read error is treated as "no violation" (another check owns unreadable
    files).
    """
    try:
        text = path.read_text(encoding="XXutf-8XX")
    except OSError:
        return False
    stripped = _strip_comments(text)
    for m in _RX_MOCK_STRING.finditer(stripped):
        spec = m.group(2)
        if _is_internal_specifier(spec, internal_packages):
            return True
    imports = _resolve_imports(stripped)
    for m in _RX_SPY_ON.finditer(stripped):
        spec = imports.get(m.group(1))
        if spec is None:
            continue
        if _is_internal_specifier(spec, internal_packages):
            return True
    return False


def x_file_mocks_internal_ts__mutmut_4(
    path: Path,
    *,
    internal_packages: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` mocks/spies an internal module.

    A read error is treated as "no violation" (another check owns unreadable
    files).
    """
    try:
        text = path.read_text(encoding="UTF-8")
    except OSError:
        return False
    stripped = _strip_comments(text)
    for m in _RX_MOCK_STRING.finditer(stripped):
        spec = m.group(2)
        if _is_internal_specifier(spec, internal_packages):
            return True
    imports = _resolve_imports(stripped)
    for m in _RX_SPY_ON.finditer(stripped):
        spec = imports.get(m.group(1))
        if spec is None:
            continue
        if _is_internal_specifier(spec, internal_packages):
            return True
    return False


def x_file_mocks_internal_ts__mutmut_5(
    path: Path,
    *,
    internal_packages: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` mocks/spies an internal module.

    A read error is treated as "no violation" (another check owns unreadable
    files).
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return True
    stripped = _strip_comments(text)
    for m in _RX_MOCK_STRING.finditer(stripped):
        spec = m.group(2)
        if _is_internal_specifier(spec, internal_packages):
            return True
    imports = _resolve_imports(stripped)
    for m in _RX_SPY_ON.finditer(stripped):
        spec = imports.get(m.group(1))
        if spec is None:
            continue
        if _is_internal_specifier(spec, internal_packages):
            return True
    return False


def x_file_mocks_internal_ts__mutmut_6(
    path: Path,
    *,
    internal_packages: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` mocks/spies an internal module.

    A read error is treated as "no violation" (another check owns unreadable
    files).
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    stripped = None
    for m in _RX_MOCK_STRING.finditer(stripped):
        spec = m.group(2)
        if _is_internal_specifier(spec, internal_packages):
            return True
    imports = _resolve_imports(stripped)
    for m in _RX_SPY_ON.finditer(stripped):
        spec = imports.get(m.group(1))
        if spec is None:
            continue
        if _is_internal_specifier(spec, internal_packages):
            return True
    return False


def x_file_mocks_internal_ts__mutmut_7(
    path: Path,
    *,
    internal_packages: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` mocks/spies an internal module.

    A read error is treated as "no violation" (another check owns unreadable
    files).
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    stripped = _strip_comments(None)
    for m in _RX_MOCK_STRING.finditer(stripped):
        spec = m.group(2)
        if _is_internal_specifier(spec, internal_packages):
            return True
    imports = _resolve_imports(stripped)
    for m in _RX_SPY_ON.finditer(stripped):
        spec = imports.get(m.group(1))
        if spec is None:
            continue
        if _is_internal_specifier(spec, internal_packages):
            return True
    return False


def x_file_mocks_internal_ts__mutmut_8(
    path: Path,
    *,
    internal_packages: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` mocks/spies an internal module.

    A read error is treated as "no violation" (another check owns unreadable
    files).
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    stripped = _strip_comments(text)
    for m in _RX_MOCK_STRING.finditer(None):
        spec = m.group(2)
        if _is_internal_specifier(spec, internal_packages):
            return True
    imports = _resolve_imports(stripped)
    for m in _RX_SPY_ON.finditer(stripped):
        spec = imports.get(m.group(1))
        if spec is None:
            continue
        if _is_internal_specifier(spec, internal_packages):
            return True
    return False


def x_file_mocks_internal_ts__mutmut_9(
    path: Path,
    *,
    internal_packages: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` mocks/spies an internal module.

    A read error is treated as "no violation" (another check owns unreadable
    files).
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    stripped = _strip_comments(text)
    for m in _RX_MOCK_STRING.finditer(stripped):
        spec = None
        if _is_internal_specifier(spec, internal_packages):
            return True
    imports = _resolve_imports(stripped)
    for m in _RX_SPY_ON.finditer(stripped):
        spec = imports.get(m.group(1))
        if spec is None:
            continue
        if _is_internal_specifier(spec, internal_packages):
            return True
    return False


def x_file_mocks_internal_ts__mutmut_10(
    path: Path,
    *,
    internal_packages: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` mocks/spies an internal module.

    A read error is treated as "no violation" (another check owns unreadable
    files).
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    stripped = _strip_comments(text)
    for m in _RX_MOCK_STRING.finditer(stripped):
        spec = m.group(None)
        if _is_internal_specifier(spec, internal_packages):
            return True
    imports = _resolve_imports(stripped)
    for m in _RX_SPY_ON.finditer(stripped):
        spec = imports.get(m.group(1))
        if spec is None:
            continue
        if _is_internal_specifier(spec, internal_packages):
            return True
    return False


def x_file_mocks_internal_ts__mutmut_11(
    path: Path,
    *,
    internal_packages: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` mocks/spies an internal module.

    A read error is treated as "no violation" (another check owns unreadable
    files).
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    stripped = _strip_comments(text)
    for m in _RX_MOCK_STRING.finditer(stripped):
        spec = m.group(3)
        if _is_internal_specifier(spec, internal_packages):
            return True
    imports = _resolve_imports(stripped)
    for m in _RX_SPY_ON.finditer(stripped):
        spec = imports.get(m.group(1))
        if spec is None:
            continue
        if _is_internal_specifier(spec, internal_packages):
            return True
    return False


def x_file_mocks_internal_ts__mutmut_12(
    path: Path,
    *,
    internal_packages: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` mocks/spies an internal module.

    A read error is treated as "no violation" (another check owns unreadable
    files).
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    stripped = _strip_comments(text)
    for m in _RX_MOCK_STRING.finditer(stripped):
        spec = m.group(2)
        if _is_internal_specifier(None, internal_packages):
            return True
    imports = _resolve_imports(stripped)
    for m in _RX_SPY_ON.finditer(stripped):
        spec = imports.get(m.group(1))
        if spec is None:
            continue
        if _is_internal_specifier(spec, internal_packages):
            return True
    return False


def x_file_mocks_internal_ts__mutmut_13(
    path: Path,
    *,
    internal_packages: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` mocks/spies an internal module.

    A read error is treated as "no violation" (another check owns unreadable
    files).
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    stripped = _strip_comments(text)
    for m in _RX_MOCK_STRING.finditer(stripped):
        spec = m.group(2)
        if _is_internal_specifier(spec, None):
            return True
    imports = _resolve_imports(stripped)
    for m in _RX_SPY_ON.finditer(stripped):
        spec = imports.get(m.group(1))
        if spec is None:
            continue
        if _is_internal_specifier(spec, internal_packages):
            return True
    return False


def x_file_mocks_internal_ts__mutmut_14(
    path: Path,
    *,
    internal_packages: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` mocks/spies an internal module.

    A read error is treated as "no violation" (another check owns unreadable
    files).
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    stripped = _strip_comments(text)
    for m in _RX_MOCK_STRING.finditer(stripped):
        spec = m.group(2)
        if _is_internal_specifier(internal_packages):
            return True
    imports = _resolve_imports(stripped)
    for m in _RX_SPY_ON.finditer(stripped):
        spec = imports.get(m.group(1))
        if spec is None:
            continue
        if _is_internal_specifier(spec, internal_packages):
            return True
    return False


def x_file_mocks_internal_ts__mutmut_15(
    path: Path,
    *,
    internal_packages: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` mocks/spies an internal module.

    A read error is treated as "no violation" (another check owns unreadable
    files).
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    stripped = _strip_comments(text)
    for m in _RX_MOCK_STRING.finditer(stripped):
        spec = m.group(2)
        if _is_internal_specifier(spec, ):
            return True
    imports = _resolve_imports(stripped)
    for m in _RX_SPY_ON.finditer(stripped):
        spec = imports.get(m.group(1))
        if spec is None:
            continue
        if _is_internal_specifier(spec, internal_packages):
            return True
    return False


def x_file_mocks_internal_ts__mutmut_16(
    path: Path,
    *,
    internal_packages: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` mocks/spies an internal module.

    A read error is treated as "no violation" (another check owns unreadable
    files).
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    stripped = _strip_comments(text)
    for m in _RX_MOCK_STRING.finditer(stripped):
        spec = m.group(2)
        if _is_internal_specifier(spec, internal_packages):
            return False
    imports = _resolve_imports(stripped)
    for m in _RX_SPY_ON.finditer(stripped):
        spec = imports.get(m.group(1))
        if spec is None:
            continue
        if _is_internal_specifier(spec, internal_packages):
            return True
    return False


def x_file_mocks_internal_ts__mutmut_17(
    path: Path,
    *,
    internal_packages: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` mocks/spies an internal module.

    A read error is treated as "no violation" (another check owns unreadable
    files).
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    stripped = _strip_comments(text)
    for m in _RX_MOCK_STRING.finditer(stripped):
        spec = m.group(2)
        if _is_internal_specifier(spec, internal_packages):
            return True
    imports = None
    for m in _RX_SPY_ON.finditer(stripped):
        spec = imports.get(m.group(1))
        if spec is None:
            continue
        if _is_internal_specifier(spec, internal_packages):
            return True
    return False


def x_file_mocks_internal_ts__mutmut_18(
    path: Path,
    *,
    internal_packages: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` mocks/spies an internal module.

    A read error is treated as "no violation" (another check owns unreadable
    files).
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    stripped = _strip_comments(text)
    for m in _RX_MOCK_STRING.finditer(stripped):
        spec = m.group(2)
        if _is_internal_specifier(spec, internal_packages):
            return True
    imports = _resolve_imports(None)
    for m in _RX_SPY_ON.finditer(stripped):
        spec = imports.get(m.group(1))
        if spec is None:
            continue
        if _is_internal_specifier(spec, internal_packages):
            return True
    return False


def x_file_mocks_internal_ts__mutmut_19(
    path: Path,
    *,
    internal_packages: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` mocks/spies an internal module.

    A read error is treated as "no violation" (another check owns unreadable
    files).
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    stripped = _strip_comments(text)
    for m in _RX_MOCK_STRING.finditer(stripped):
        spec = m.group(2)
        if _is_internal_specifier(spec, internal_packages):
            return True
    imports = _resolve_imports(stripped)
    for m in _RX_SPY_ON.finditer(None):
        spec = imports.get(m.group(1))
        if spec is None:
            continue
        if _is_internal_specifier(spec, internal_packages):
            return True
    return False


def x_file_mocks_internal_ts__mutmut_20(
    path: Path,
    *,
    internal_packages: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` mocks/spies an internal module.

    A read error is treated as "no violation" (another check owns unreadable
    files).
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    stripped = _strip_comments(text)
    for m in _RX_MOCK_STRING.finditer(stripped):
        spec = m.group(2)
        if _is_internal_specifier(spec, internal_packages):
            return True
    imports = _resolve_imports(stripped)
    for m in _RX_SPY_ON.finditer(stripped):
        spec = None
        if spec is None:
            continue
        if _is_internal_specifier(spec, internal_packages):
            return True
    return False


def x_file_mocks_internal_ts__mutmut_21(
    path: Path,
    *,
    internal_packages: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` mocks/spies an internal module.

    A read error is treated as "no violation" (another check owns unreadable
    files).
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    stripped = _strip_comments(text)
    for m in _RX_MOCK_STRING.finditer(stripped):
        spec = m.group(2)
        if _is_internal_specifier(spec, internal_packages):
            return True
    imports = _resolve_imports(stripped)
    for m in _RX_SPY_ON.finditer(stripped):
        spec = imports.get(None)
        if spec is None:
            continue
        if _is_internal_specifier(spec, internal_packages):
            return True
    return False


def x_file_mocks_internal_ts__mutmut_22(
    path: Path,
    *,
    internal_packages: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` mocks/spies an internal module.

    A read error is treated as "no violation" (another check owns unreadable
    files).
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    stripped = _strip_comments(text)
    for m in _RX_MOCK_STRING.finditer(stripped):
        spec = m.group(2)
        if _is_internal_specifier(spec, internal_packages):
            return True
    imports = _resolve_imports(stripped)
    for m in _RX_SPY_ON.finditer(stripped):
        spec = imports.get(m.group(None))
        if spec is None:
            continue
        if _is_internal_specifier(spec, internal_packages):
            return True
    return False


def x_file_mocks_internal_ts__mutmut_23(
    path: Path,
    *,
    internal_packages: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` mocks/spies an internal module.

    A read error is treated as "no violation" (another check owns unreadable
    files).
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    stripped = _strip_comments(text)
    for m in _RX_MOCK_STRING.finditer(stripped):
        spec = m.group(2)
        if _is_internal_specifier(spec, internal_packages):
            return True
    imports = _resolve_imports(stripped)
    for m in _RX_SPY_ON.finditer(stripped):
        spec = imports.get(m.group(2))
        if spec is None:
            continue
        if _is_internal_specifier(spec, internal_packages):
            return True
    return False


def x_file_mocks_internal_ts__mutmut_24(
    path: Path,
    *,
    internal_packages: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` mocks/spies an internal module.

    A read error is treated as "no violation" (another check owns unreadable
    files).
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    stripped = _strip_comments(text)
    for m in _RX_MOCK_STRING.finditer(stripped):
        spec = m.group(2)
        if _is_internal_specifier(spec, internal_packages):
            return True
    imports = _resolve_imports(stripped)
    for m in _RX_SPY_ON.finditer(stripped):
        spec = imports.get(m.group(1))
        if spec is not None:
            continue
        if _is_internal_specifier(spec, internal_packages):
            return True
    return False


def x_file_mocks_internal_ts__mutmut_25(
    path: Path,
    *,
    internal_packages: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` mocks/spies an internal module.

    A read error is treated as "no violation" (another check owns unreadable
    files).
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    stripped = _strip_comments(text)
    for m in _RX_MOCK_STRING.finditer(stripped):
        spec = m.group(2)
        if _is_internal_specifier(spec, internal_packages):
            return True
    imports = _resolve_imports(stripped)
    for m in _RX_SPY_ON.finditer(stripped):
        spec = imports.get(m.group(1))
        if spec is None:
            break
        if _is_internal_specifier(spec, internal_packages):
            return True
    return False


def x_file_mocks_internal_ts__mutmut_26(
    path: Path,
    *,
    internal_packages: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` mocks/spies an internal module.

    A read error is treated as "no violation" (another check owns unreadable
    files).
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    stripped = _strip_comments(text)
    for m in _RX_MOCK_STRING.finditer(stripped):
        spec = m.group(2)
        if _is_internal_specifier(spec, internal_packages):
            return True
    imports = _resolve_imports(stripped)
    for m in _RX_SPY_ON.finditer(stripped):
        spec = imports.get(m.group(1))
        if spec is None:
            continue
        if _is_internal_specifier(None, internal_packages):
            return True
    return False


def x_file_mocks_internal_ts__mutmut_27(
    path: Path,
    *,
    internal_packages: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` mocks/spies an internal module.

    A read error is treated as "no violation" (another check owns unreadable
    files).
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    stripped = _strip_comments(text)
    for m in _RX_MOCK_STRING.finditer(stripped):
        spec = m.group(2)
        if _is_internal_specifier(spec, internal_packages):
            return True
    imports = _resolve_imports(stripped)
    for m in _RX_SPY_ON.finditer(stripped):
        spec = imports.get(m.group(1))
        if spec is None:
            continue
        if _is_internal_specifier(spec, None):
            return True
    return False


def x_file_mocks_internal_ts__mutmut_28(
    path: Path,
    *,
    internal_packages: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` mocks/spies an internal module.

    A read error is treated as "no violation" (another check owns unreadable
    files).
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    stripped = _strip_comments(text)
    for m in _RX_MOCK_STRING.finditer(stripped):
        spec = m.group(2)
        if _is_internal_specifier(spec, internal_packages):
            return True
    imports = _resolve_imports(stripped)
    for m in _RX_SPY_ON.finditer(stripped):
        spec = imports.get(m.group(1))
        if spec is None:
            continue
        if _is_internal_specifier(internal_packages):
            return True
    return False


def x_file_mocks_internal_ts__mutmut_29(
    path: Path,
    *,
    internal_packages: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` mocks/spies an internal module.

    A read error is treated as "no violation" (another check owns unreadable
    files).
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    stripped = _strip_comments(text)
    for m in _RX_MOCK_STRING.finditer(stripped):
        spec = m.group(2)
        if _is_internal_specifier(spec, internal_packages):
            return True
    imports = _resolve_imports(stripped)
    for m in _RX_SPY_ON.finditer(stripped):
        spec = imports.get(m.group(1))
        if spec is None:
            continue
        if _is_internal_specifier(spec, ):
            return True
    return False


def x_file_mocks_internal_ts__mutmut_30(
    path: Path,
    *,
    internal_packages: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` mocks/spies an internal module.

    A read error is treated as "no violation" (another check owns unreadable
    files).
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    stripped = _strip_comments(text)
    for m in _RX_MOCK_STRING.finditer(stripped):
        spec = m.group(2)
        if _is_internal_specifier(spec, internal_packages):
            return True
    imports = _resolve_imports(stripped)
    for m in _RX_SPY_ON.finditer(stripped):
        spec = imports.get(m.group(1))
        if spec is None:
            continue
        if _is_internal_specifier(spec, internal_packages):
            return False
    return False


def x_file_mocks_internal_ts__mutmut_31(
    path: Path,
    *,
    internal_packages: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` mocks/spies an internal module.

    A read error is treated as "no violation" (another check owns unreadable
    files).
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    stripped = _strip_comments(text)
    for m in _RX_MOCK_STRING.finditer(stripped):
        spec = m.group(2)
        if _is_internal_specifier(spec, internal_packages):
            return True
    imports = _resolve_imports(stripped)
    for m in _RX_SPY_ON.finditer(stripped):
        spec = imports.get(m.group(1))
        if spec is None:
            continue
        if _is_internal_specifier(spec, internal_packages):
            return True
    return True

mutants_x_file_mocks_internal_ts__mutmut['_mutmut_orig'] = x_file_mocks_internal_ts__mutmut_orig # type: ignore # mutmut generated
mutants_x_file_mocks_internal_ts__mutmut['x_file_mocks_internal_ts__mutmut_1'] = x_file_mocks_internal_ts__mutmut_1 # type: ignore # mutmut generated
mutants_x_file_mocks_internal_ts__mutmut['x_file_mocks_internal_ts__mutmut_2'] = x_file_mocks_internal_ts__mutmut_2 # type: ignore # mutmut generated
mutants_x_file_mocks_internal_ts__mutmut['x_file_mocks_internal_ts__mutmut_3'] = x_file_mocks_internal_ts__mutmut_3 # type: ignore # mutmut generated
mutants_x_file_mocks_internal_ts__mutmut['x_file_mocks_internal_ts__mutmut_4'] = x_file_mocks_internal_ts__mutmut_4 # type: ignore # mutmut generated
mutants_x_file_mocks_internal_ts__mutmut['x_file_mocks_internal_ts__mutmut_5'] = x_file_mocks_internal_ts__mutmut_5 # type: ignore # mutmut generated
mutants_x_file_mocks_internal_ts__mutmut['x_file_mocks_internal_ts__mutmut_6'] = x_file_mocks_internal_ts__mutmut_6 # type: ignore # mutmut generated
mutants_x_file_mocks_internal_ts__mutmut['x_file_mocks_internal_ts__mutmut_7'] = x_file_mocks_internal_ts__mutmut_7 # type: ignore # mutmut generated
mutants_x_file_mocks_internal_ts__mutmut['x_file_mocks_internal_ts__mutmut_8'] = x_file_mocks_internal_ts__mutmut_8 # type: ignore # mutmut generated
mutants_x_file_mocks_internal_ts__mutmut['x_file_mocks_internal_ts__mutmut_9'] = x_file_mocks_internal_ts__mutmut_9 # type: ignore # mutmut generated
mutants_x_file_mocks_internal_ts__mutmut['x_file_mocks_internal_ts__mutmut_10'] = x_file_mocks_internal_ts__mutmut_10 # type: ignore # mutmut generated
mutants_x_file_mocks_internal_ts__mutmut['x_file_mocks_internal_ts__mutmut_11'] = x_file_mocks_internal_ts__mutmut_11 # type: ignore # mutmut generated
mutants_x_file_mocks_internal_ts__mutmut['x_file_mocks_internal_ts__mutmut_12'] = x_file_mocks_internal_ts__mutmut_12 # type: ignore # mutmut generated
mutants_x_file_mocks_internal_ts__mutmut['x_file_mocks_internal_ts__mutmut_13'] = x_file_mocks_internal_ts__mutmut_13 # type: ignore # mutmut generated
mutants_x_file_mocks_internal_ts__mutmut['x_file_mocks_internal_ts__mutmut_14'] = x_file_mocks_internal_ts__mutmut_14 # type: ignore # mutmut generated
mutants_x_file_mocks_internal_ts__mutmut['x_file_mocks_internal_ts__mutmut_15'] = x_file_mocks_internal_ts__mutmut_15 # type: ignore # mutmut generated
mutants_x_file_mocks_internal_ts__mutmut['x_file_mocks_internal_ts__mutmut_16'] = x_file_mocks_internal_ts__mutmut_16 # type: ignore # mutmut generated
mutants_x_file_mocks_internal_ts__mutmut['x_file_mocks_internal_ts__mutmut_17'] = x_file_mocks_internal_ts__mutmut_17 # type: ignore # mutmut generated
mutants_x_file_mocks_internal_ts__mutmut['x_file_mocks_internal_ts__mutmut_18'] = x_file_mocks_internal_ts__mutmut_18 # type: ignore # mutmut generated
mutants_x_file_mocks_internal_ts__mutmut['x_file_mocks_internal_ts__mutmut_19'] = x_file_mocks_internal_ts__mutmut_19 # type: ignore # mutmut generated
mutants_x_file_mocks_internal_ts__mutmut['x_file_mocks_internal_ts__mutmut_20'] = x_file_mocks_internal_ts__mutmut_20 # type: ignore # mutmut generated
mutants_x_file_mocks_internal_ts__mutmut['x_file_mocks_internal_ts__mutmut_21'] = x_file_mocks_internal_ts__mutmut_21 # type: ignore # mutmut generated
mutants_x_file_mocks_internal_ts__mutmut['x_file_mocks_internal_ts__mutmut_22'] = x_file_mocks_internal_ts__mutmut_22 # type: ignore # mutmut generated
mutants_x_file_mocks_internal_ts__mutmut['x_file_mocks_internal_ts__mutmut_23'] = x_file_mocks_internal_ts__mutmut_23 # type: ignore # mutmut generated
mutants_x_file_mocks_internal_ts__mutmut['x_file_mocks_internal_ts__mutmut_24'] = x_file_mocks_internal_ts__mutmut_24 # type: ignore # mutmut generated
mutants_x_file_mocks_internal_ts__mutmut['x_file_mocks_internal_ts__mutmut_25'] = x_file_mocks_internal_ts__mutmut_25 # type: ignore # mutmut generated
mutants_x_file_mocks_internal_ts__mutmut['x_file_mocks_internal_ts__mutmut_26'] = x_file_mocks_internal_ts__mutmut_26 # type: ignore # mutmut generated
mutants_x_file_mocks_internal_ts__mutmut['x_file_mocks_internal_ts__mutmut_27'] = x_file_mocks_internal_ts__mutmut_27 # type: ignore # mutmut generated
mutants_x_file_mocks_internal_ts__mutmut['x_file_mocks_internal_ts__mutmut_28'] = x_file_mocks_internal_ts__mutmut_28 # type: ignore # mutmut generated
mutants_x_file_mocks_internal_ts__mutmut['x_file_mocks_internal_ts__mutmut_29'] = x_file_mocks_internal_ts__mutmut_29 # type: ignore # mutmut generated
mutants_x_file_mocks_internal_ts__mutmut['x_file_mocks_internal_ts__mutmut_30'] = x_file_mocks_internal_ts__mutmut_30 # type: ignore # mutmut generated
mutants_x_file_mocks_internal_ts__mutmut['x_file_mocks_internal_ts__mutmut_31'] = x_file_mocks_internal_ts__mutmut_31 # type: ignore # mutmut generated
mutants_xǁNoInternalPatchesTsǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁNoInternalPatchesTsǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore


class NoInternalPatchesTs(FitnessRule):
    """Flags TS/TSX test files that mock/spy an INTERNAL module (F1-TS)."""

    name = "no-internal-patches-ts"
    remediation = REMEDIATION
    extensions = (".test.ts", ".test.tsx")

    #: Rule-specific config (instance attrs; from_config overrides per consumer).
    internal_packages: frozenset[str] = frozenset()

    @classmethod
    @_mutmut_mutated(mutants_xǁNoInternalPatchesTsǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalPatchesTs:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoInternalPatchesTs)  # noqa: S101  # narrowing for mypy
        rule.internal_packages = frozenset(config.get("internal_packages", ()))
        return rule

    @classmethod
    def xǁNoInternalPatchesTsǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalPatchesTs:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoInternalPatchesTs)  # noqa: S101  # narrowing for mypy
        rule.internal_packages = frozenset(config.get("internal_packages", ()))
        return rule

    @classmethod
    def xǁNoInternalPatchesTsǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalPatchesTs:
        rule = None
        assert isinstance(rule, NoInternalPatchesTs)  # noqa: S101  # narrowing for mypy
        rule.internal_packages = frozenset(config.get("internal_packages", ()))
        return rule

    @classmethod
    def xǁNoInternalPatchesTsǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalPatchesTs:
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, NoInternalPatchesTs)  # noqa: S101  # narrowing for mypy
        rule.internal_packages = frozenset(config.get("internal_packages", ()))
        return rule

    @classmethod
    def xǁNoInternalPatchesTsǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalPatchesTs:
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, NoInternalPatchesTs)  # noqa: S101  # narrowing for mypy
        rule.internal_packages = frozenset(config.get("internal_packages", ()))
        return rule

    @classmethod
    def xǁNoInternalPatchesTsǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalPatchesTs:
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, NoInternalPatchesTs)  # noqa: S101  # narrowing for mypy
        rule.internal_packages = frozenset(config.get("internal_packages", ()))
        return rule

    @classmethod
    def xǁNoInternalPatchesTsǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalPatchesTs:
        rule = super().from_config(config, )
        assert isinstance(rule, NoInternalPatchesTs)  # noqa: S101  # narrowing for mypy
        rule.internal_packages = frozenset(config.get("internal_packages", ()))
        return rule

    @classmethod
    def xǁNoInternalPatchesTsǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalPatchesTs:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoInternalPatchesTs)  # noqa: S101  # narrowing for mypy
        rule.internal_packages = None
        return rule

    @classmethod
    def xǁNoInternalPatchesTsǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalPatchesTs:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoInternalPatchesTs)  # noqa: S101  # narrowing for mypy
        rule.internal_packages = frozenset(None)
        return rule

    @classmethod
    def xǁNoInternalPatchesTsǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalPatchesTs:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoInternalPatchesTs)  # noqa: S101  # narrowing for mypy
        rule.internal_packages = frozenset(config.get(None, ()))
        return rule

    @classmethod
    def xǁNoInternalPatchesTsǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalPatchesTs:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoInternalPatchesTs)  # noqa: S101  # narrowing for mypy
        rule.internal_packages = frozenset(config.get("internal_packages", None))
        return rule

    @classmethod
    def xǁNoInternalPatchesTsǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalPatchesTs:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoInternalPatchesTs)  # noqa: S101  # narrowing for mypy
        rule.internal_packages = frozenset(config.get(()))
        return rule

    @classmethod
    def xǁNoInternalPatchesTsǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalPatchesTs:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoInternalPatchesTs)  # noqa: S101  # narrowing for mypy
        rule.internal_packages = frozenset(config.get("internal_packages", ))
        return rule

    @classmethod
    def xǁNoInternalPatchesTsǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalPatchesTs:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoInternalPatchesTs)  # noqa: S101  # narrowing for mypy
        rule.internal_packages = frozenset(config.get("XXinternal_packagesXX", ()))
        return rule

    @classmethod
    def xǁNoInternalPatchesTsǁfrom_config__mutmut_13(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalPatchesTs:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoInternalPatchesTs)  # noqa: S101  # narrowing for mypy
        rule.internal_packages = frozenset(config.get("INTERNAL_PACKAGES", ()))
        return rule

    @_mutmut_mutated(mutants_xǁNoInternalPatchesTsǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        return file_mocks_internal_ts(
            path,
            internal_packages=self.internal_packages,
        )

    def xǁNoInternalPatchesTsǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        return file_mocks_internal_ts(
            path,
            internal_packages=self.internal_packages,
        )

    def xǁNoInternalPatchesTsǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        return file_mocks_internal_ts(
            None,
            internal_packages=self.internal_packages,
        )

    def xǁNoInternalPatchesTsǁfile_has_violation__mutmut_2(self, path: Path) -> bool:
        return file_mocks_internal_ts(
            path,
            internal_packages=None,
        )

    def xǁNoInternalPatchesTsǁfile_has_violation__mutmut_3(self, path: Path) -> bool:
        return file_mocks_internal_ts(
            internal_packages=self.internal_packages,
        )

    def xǁNoInternalPatchesTsǁfile_has_violation__mutmut_4(self, path: Path) -> bool:
        return file_mocks_internal_ts(
            path,
            )

mutants_xǁNoInternalPatchesTsǁfrom_config__mutmut['_mutmut_orig'] = NoInternalPatchesTs.xǁNoInternalPatchesTsǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNoInternalPatchesTsǁfrom_config__mutmut['xǁNoInternalPatchesTsǁfrom_config__mutmut_1'] = NoInternalPatchesTs.xǁNoInternalPatchesTsǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNoInternalPatchesTsǁfrom_config__mutmut['xǁNoInternalPatchesTsǁfrom_config__mutmut_2'] = NoInternalPatchesTs.xǁNoInternalPatchesTsǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNoInternalPatchesTsǁfrom_config__mutmut['xǁNoInternalPatchesTsǁfrom_config__mutmut_3'] = NoInternalPatchesTs.xǁNoInternalPatchesTsǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNoInternalPatchesTsǁfrom_config__mutmut['xǁNoInternalPatchesTsǁfrom_config__mutmut_4'] = NoInternalPatchesTs.xǁNoInternalPatchesTsǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁNoInternalPatchesTsǁfrom_config__mutmut['xǁNoInternalPatchesTsǁfrom_config__mutmut_5'] = NoInternalPatchesTs.xǁNoInternalPatchesTsǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁNoInternalPatchesTsǁfrom_config__mutmut['xǁNoInternalPatchesTsǁfrom_config__mutmut_6'] = NoInternalPatchesTs.xǁNoInternalPatchesTsǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁNoInternalPatchesTsǁfrom_config__mutmut['xǁNoInternalPatchesTsǁfrom_config__mutmut_7'] = NoInternalPatchesTs.xǁNoInternalPatchesTsǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁNoInternalPatchesTsǁfrom_config__mutmut['xǁNoInternalPatchesTsǁfrom_config__mutmut_8'] = NoInternalPatchesTs.xǁNoInternalPatchesTsǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁNoInternalPatchesTsǁfrom_config__mutmut['xǁNoInternalPatchesTsǁfrom_config__mutmut_9'] = NoInternalPatchesTs.xǁNoInternalPatchesTsǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁNoInternalPatchesTsǁfrom_config__mutmut['xǁNoInternalPatchesTsǁfrom_config__mutmut_10'] = NoInternalPatchesTs.xǁNoInternalPatchesTsǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁNoInternalPatchesTsǁfrom_config__mutmut['xǁNoInternalPatchesTsǁfrom_config__mutmut_11'] = NoInternalPatchesTs.xǁNoInternalPatchesTsǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁNoInternalPatchesTsǁfrom_config__mutmut['xǁNoInternalPatchesTsǁfrom_config__mutmut_12'] = NoInternalPatchesTs.xǁNoInternalPatchesTsǁfrom_config__mutmut_12 # type: ignore # mutmut generated
mutants_xǁNoInternalPatchesTsǁfrom_config__mutmut['xǁNoInternalPatchesTsǁfrom_config__mutmut_13'] = NoInternalPatchesTs.xǁNoInternalPatchesTsǁfrom_config__mutmut_13 # type: ignore # mutmut generated

mutants_xǁNoInternalPatchesTsǁfile_has_violation__mutmut['_mutmut_orig'] = NoInternalPatchesTs.xǁNoInternalPatchesTsǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNoInternalPatchesTsǁfile_has_violation__mutmut['xǁNoInternalPatchesTsǁfile_has_violation__mutmut_1'] = NoInternalPatchesTs.xǁNoInternalPatchesTsǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNoInternalPatchesTsǁfile_has_violation__mutmut['xǁNoInternalPatchesTsǁfile_has_violation__mutmut_2'] = NoInternalPatchesTs.xǁNoInternalPatchesTsǁfile_has_violation__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNoInternalPatchesTsǁfile_has_violation__mutmut['xǁNoInternalPatchesTsǁfile_has_violation__mutmut_3'] = NoInternalPatchesTs.xǁNoInternalPatchesTsǁfile_has_violation__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNoInternalPatchesTsǁfile_has_violation__mutmut['xǁNoInternalPatchesTsǁfile_has_violation__mutmut_4'] = NoInternalPatchesTs.xǁNoInternalPatchesTsǁfile_has_violation__mutmut_4 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoInternalPatchesTs:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoInternalPatchesTs.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoInternalPatchesTs:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoInternalPatchesTs.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoInternalPatchesTs:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoInternalPatchesTs.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoInternalPatchesTs:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoInternalPatchesTs.from_config(config, repo_root=None)


def x_build__mutmut_3(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoInternalPatchesTs:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoInternalPatchesTs.from_config(repo_root=repo_root)


def x_build__mutmut_4(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoInternalPatchesTs:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoInternalPatchesTs.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoInternalPatchesTs, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoInternalPatchesTs, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoInternalPatchesTs, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoInternalPatchesTs, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
