"""CORE check: engine_version_floor — the pinned engine version clears a floor.

A consumer repo pins the shared fitness engine (``three-cubes-fitness``) to an
exact tag — typically a git ref like
``three-cubes-fitness @ git+https://.../tc-fitness.git@vX.Y.Z``, a git-URL
dependency the uv ecosystem cannot range-track — and over time consumers drift:
one repo sits a minor version behind the gate-critical floor while another rides
the head, so a check that was fixed centrally quietly never runs in the laggard.
This rule reads the consuming repo's OWN pinned engine tag and FAILS when it is
BELOW a centrally-declared floor, surfacing the lag at the gate.

Guard-forward (decision D2): the floor is CONSUMER config
(``[tool.tc_fitness.core_checks.engine_version_floor] floor = "vX.Y.Z"``), not a
constant baked into the engine — a repo with no floor configured is a NO-OP, so
adopting the check never hard-breaks a consumer before its own bump PR lands.
The floor ships set to the current MINIMUM pinned tag across the fleet with a
ratchet note: it may only rise.

Repo-agnostic: the only literal this module carries is the engine's OWN
distribution name (overridable via the ``package`` config key) — it names no
consuming repo. Version resolution prefers the consumer's DECLARED pin (its
``pyproject.toml`` dependency spec or uv source tag) and falls back to the
installed distribution's metadata.
"""

from __future__ import annotations

import re
import tomllib
from collections.abc import Iterator, Mapping
from importlib import metadata as _metadata
from pathlib import Path
from typing import Any

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: The shared engine's own distribution name — the dependency a consumer pins.
#: Overridable via the ``package`` config key; it names the engine, not a repo.
DEFAULT_PACKAGE = "three-cubes-fitness"

#: The consumer manifest read for the declared pin, relative to the repo root.
_PYPROJECT = "pyproject.toml"

#: A dotted numeric release, optionally ``v``-prefixed (``v0.6.1`` → ``0.6.1``).
_RELEASE_RE = re.compile(r"v?(\d+(?:\.\d+)*)")

#: A PEP 508 version specifier carrying an exact-or-lower pin (``name==X.Y.Z``).
_SPECIFIER_RE = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*)(?:\[[^\]]*\])?\s*(?:===|==|~=|>=)\s*([^,;\s]+)")

REMEDIATION = _remediation(
    fix=(
        "bump the pinned engine dependency to at least the configured floor — "
        "update the engine tag in pyproject.toml (its git-URL `@vX.Y.Z` ref or "
        "its uv source `tag`) to a version at or above the floor and re-lock. "
        "The floor is a control-plane ratchet; lowering it is a CODEOWNERS-gated "
        "edit, not a fix."
    ),
    nxt="re-run this check to confirm the pin clears the floor.",
    run="python -m tc_fitness.core_checks.engine_version_floor",
    passing="pinned @v0.7.0 with floor v0.7.0",
    forbidden="pinned @v0.6.1 with floor v0.7.0",
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x_parse_version__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_parse_version__mutmut)
def parse_version(text: str) -> tuple[int, ...] | None:
    """Parse ``vX.Y.Z`` / ``X.Y.Z`` into a comparable release tuple, else ``None``.

    Only the leading dotted-numeric release is read (any pre-release / local
    suffix is ignored), so ``v0.6.1`` → ``(0, 6, 1)``. A string with no leading
    numeric release (a branch name, a bare URL) yields ``None`` — the caller
    treats an unparseable version as "cannot determine", never as a violation.
    """
    match = _RELEASE_RE.match(text.strip())
    if match is None:
        return None
    return tuple(int(part) for part in match.group(1).split("."))


def x_parse_version__mutmut_orig(text: str) -> tuple[int, ...] | None:
    """Parse ``vX.Y.Z`` / ``X.Y.Z`` into a comparable release tuple, else ``None``.

    Only the leading dotted-numeric release is read (any pre-release / local
    suffix is ignored), so ``v0.6.1`` → ``(0, 6, 1)``. A string with no leading
    numeric release (a branch name, a bare URL) yields ``None`` — the caller
    treats an unparseable version as "cannot determine", never as a violation.
    """
    match = _RELEASE_RE.match(text.strip())
    if match is None:
        return None
    return tuple(int(part) for part in match.group(1).split("."))


def x_parse_version__mutmut_1(text: str) -> tuple[int, ...] | None:
    """Parse ``vX.Y.Z`` / ``X.Y.Z`` into a comparable release tuple, else ``None``.

    Only the leading dotted-numeric release is read (any pre-release / local
    suffix is ignored), so ``v0.6.1`` → ``(0, 6, 1)``. A string with no leading
    numeric release (a branch name, a bare URL) yields ``None`` — the caller
    treats an unparseable version as "cannot determine", never as a violation.
    """
    match = None
    if match is None:
        return None
    return tuple(int(part) for part in match.group(1).split("."))


def x_parse_version__mutmut_2(text: str) -> tuple[int, ...] | None:
    """Parse ``vX.Y.Z`` / ``X.Y.Z`` into a comparable release tuple, else ``None``.

    Only the leading dotted-numeric release is read (any pre-release / local
    suffix is ignored), so ``v0.6.1`` → ``(0, 6, 1)``. A string with no leading
    numeric release (a branch name, a bare URL) yields ``None`` — the caller
    treats an unparseable version as "cannot determine", never as a violation.
    """
    match = _RELEASE_RE.match(None)
    if match is None:
        return None
    return tuple(int(part) for part in match.group(1).split("."))


def x_parse_version__mutmut_3(text: str) -> tuple[int, ...] | None:
    """Parse ``vX.Y.Z`` / ``X.Y.Z`` into a comparable release tuple, else ``None``.

    Only the leading dotted-numeric release is read (any pre-release / local
    suffix is ignored), so ``v0.6.1`` → ``(0, 6, 1)``. A string with no leading
    numeric release (a branch name, a bare URL) yields ``None`` — the caller
    treats an unparseable version as "cannot determine", never as a violation.
    """
    match = _RELEASE_RE.match(text.strip())
    if match is not None:
        return None
    return tuple(int(part) for part in match.group(1).split("."))


def x_parse_version__mutmut_4(text: str) -> tuple[int, ...] | None:
    """Parse ``vX.Y.Z`` / ``X.Y.Z`` into a comparable release tuple, else ``None``.

    Only the leading dotted-numeric release is read (any pre-release / local
    suffix is ignored), so ``v0.6.1`` → ``(0, 6, 1)``. A string with no leading
    numeric release (a branch name, a bare URL) yields ``None`` — the caller
    treats an unparseable version as "cannot determine", never as a violation.
    """
    match = _RELEASE_RE.match(text.strip())
    if match is None:
        return None
    return tuple(None)


def x_parse_version__mutmut_5(text: str) -> tuple[int, ...] | None:
    """Parse ``vX.Y.Z`` / ``X.Y.Z`` into a comparable release tuple, else ``None``.

    Only the leading dotted-numeric release is read (any pre-release / local
    suffix is ignored), so ``v0.6.1`` → ``(0, 6, 1)``. A string with no leading
    numeric release (a branch name, a bare URL) yields ``None`` — the caller
    treats an unparseable version as "cannot determine", never as a violation.
    """
    match = _RELEASE_RE.match(text.strip())
    if match is None:
        return None
    return tuple(int(None) for part in match.group(1).split("."))


def x_parse_version__mutmut_6(text: str) -> tuple[int, ...] | None:
    """Parse ``vX.Y.Z`` / ``X.Y.Z`` into a comparable release tuple, else ``None``.

    Only the leading dotted-numeric release is read (any pre-release / local
    suffix is ignored), so ``v0.6.1`` → ``(0, 6, 1)``. A string with no leading
    numeric release (a branch name, a bare URL) yields ``None`` — the caller
    treats an unparseable version as "cannot determine", never as a violation.
    """
    match = _RELEASE_RE.match(text.strip())
    if match is None:
        return None
    return tuple(int(part) for part in match.group(1).split(None))


def x_parse_version__mutmut_7(text: str) -> tuple[int, ...] | None:
    """Parse ``vX.Y.Z`` / ``X.Y.Z`` into a comparable release tuple, else ``None``.

    Only the leading dotted-numeric release is read (any pre-release / local
    suffix is ignored), so ``v0.6.1`` → ``(0, 6, 1)``. A string with no leading
    numeric release (a branch name, a bare URL) yields ``None`` — the caller
    treats an unparseable version as "cannot determine", never as a violation.
    """
    match = _RELEASE_RE.match(text.strip())
    if match is None:
        return None
    return tuple(int(part) for part in match.group(None).split("."))


def x_parse_version__mutmut_8(text: str) -> tuple[int, ...] | None:
    """Parse ``vX.Y.Z`` / ``X.Y.Z`` into a comparable release tuple, else ``None``.

    Only the leading dotted-numeric release is read (any pre-release / local
    suffix is ignored), so ``v0.6.1`` → ``(0, 6, 1)``. A string with no leading
    numeric release (a branch name, a bare URL) yields ``None`` — the caller
    treats an unparseable version as "cannot determine", never as a violation.
    """
    match = _RELEASE_RE.match(text.strip())
    if match is None:
        return None
    return tuple(int(part) for part in match.group(2).split("."))


def x_parse_version__mutmut_9(text: str) -> tuple[int, ...] | None:
    """Parse ``vX.Y.Z`` / ``X.Y.Z`` into a comparable release tuple, else ``None``.

    Only the leading dotted-numeric release is read (any pre-release / local
    suffix is ignored), so ``v0.6.1`` → ``(0, 6, 1)``. A string with no leading
    numeric release (a branch name, a bare URL) yields ``None`` — the caller
    treats an unparseable version as "cannot determine", never as a violation.
    """
    match = _RELEASE_RE.match(text.strip())
    if match is None:
        return None
    return tuple(int(part) for part in match.group(1).split("XX.XX"))

mutants_x_parse_version__mutmut['_mutmut_orig'] = x_parse_version__mutmut_orig # type: ignore # mutmut generated
mutants_x_parse_version__mutmut['x_parse_version__mutmut_1'] = x_parse_version__mutmut_1 # type: ignore # mutmut generated
mutants_x_parse_version__mutmut['x_parse_version__mutmut_2'] = x_parse_version__mutmut_2 # type: ignore # mutmut generated
mutants_x_parse_version__mutmut['x_parse_version__mutmut_3'] = x_parse_version__mutmut_3 # type: ignore # mutmut generated
mutants_x_parse_version__mutmut['x_parse_version__mutmut_4'] = x_parse_version__mutmut_4 # type: ignore # mutmut generated
mutants_x_parse_version__mutmut['x_parse_version__mutmut_5'] = x_parse_version__mutmut_5 # type: ignore # mutmut generated
mutants_x_parse_version__mutmut['x_parse_version__mutmut_6'] = x_parse_version__mutmut_6 # type: ignore # mutmut generated
mutants_x_parse_version__mutmut['x_parse_version__mutmut_7'] = x_parse_version__mutmut_7 # type: ignore # mutmut generated
mutants_x_parse_version__mutmut['x_parse_version__mutmut_8'] = x_parse_version__mutmut_8 # type: ignore # mutmut generated
mutants_x_parse_version__mutmut['x_parse_version__mutmut_9'] = x_parse_version__mutmut_9 # type: ignore # mutmut generated
mutants_x__normalize__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__normalize__mutmut)
def _normalize(name: str) -> str:
    """PEP 503 name normalisation so ``Three_Cubes.Fitness`` matches its package."""
    return re.sub(r"[-_.]+", "-", name).strip().lower()


def x__normalize__mutmut_orig(name: str) -> str:
    """PEP 503 name normalisation so ``Three_Cubes.Fitness`` matches its package."""
    return re.sub(r"[-_.]+", "-", name).strip().lower()


def x__normalize__mutmut_1(name: str) -> str:
    """PEP 503 name normalisation so ``Three_Cubes.Fitness`` matches its package."""
    return re.sub(r"[-_.]+", "-", name).strip().upper()


def x__normalize__mutmut_2(name: str) -> str:
    """PEP 503 name normalisation so ``Three_Cubes.Fitness`` matches its package."""
    return re.sub(None, "-", name).strip().lower()


def x__normalize__mutmut_3(name: str) -> str:
    """PEP 503 name normalisation so ``Three_Cubes.Fitness`` matches its package."""
    return re.sub(r"[-_.]+", None, name).strip().lower()


def x__normalize__mutmut_4(name: str) -> str:
    """PEP 503 name normalisation so ``Three_Cubes.Fitness`` matches its package."""
    return re.sub(r"[-_.]+", "-", None).strip().lower()


def x__normalize__mutmut_5(name: str) -> str:
    """PEP 503 name normalisation so ``Three_Cubes.Fitness`` matches its package."""
    return re.sub("-", name).strip().lower()


def x__normalize__mutmut_6(name: str) -> str:
    """PEP 503 name normalisation so ``Three_Cubes.Fitness`` matches its package."""
    return re.sub(r"[-_.]+", name).strip().lower()


def x__normalize__mutmut_7(name: str) -> str:
    """PEP 503 name normalisation so ``Three_Cubes.Fitness`` matches its package."""
    return re.sub(r"[-_.]+", "-", ).strip().lower()


def x__normalize__mutmut_8(name: str) -> str:
    """PEP 503 name normalisation so ``Three_Cubes.Fitness`` matches its package."""
    return re.sub(r"XX[-_.]+XX", "-", name).strip().lower()


def x__normalize__mutmut_9(name: str) -> str:
    """PEP 503 name normalisation so ``Three_Cubes.Fitness`` matches its package."""
    return re.sub(r"[-_.]+", "XX-XX", name).strip().lower()

mutants_x__normalize__mutmut['_mutmut_orig'] = x__normalize__mutmut_orig # type: ignore # mutmut generated
mutants_x__normalize__mutmut['x__normalize__mutmut_1'] = x__normalize__mutmut_1 # type: ignore # mutmut generated
mutants_x__normalize__mutmut['x__normalize__mutmut_2'] = x__normalize__mutmut_2 # type: ignore # mutmut generated
mutants_x__normalize__mutmut['x__normalize__mutmut_3'] = x__normalize__mutmut_3 # type: ignore # mutmut generated
mutants_x__normalize__mutmut['x__normalize__mutmut_4'] = x__normalize__mutmut_4 # type: ignore # mutmut generated
mutants_x__normalize__mutmut['x__normalize__mutmut_5'] = x__normalize__mutmut_5 # type: ignore # mutmut generated
mutants_x__normalize__mutmut['x__normalize__mutmut_6'] = x__normalize__mutmut_6 # type: ignore # mutmut generated
mutants_x__normalize__mutmut['x__normalize__mutmut_7'] = x__normalize__mutmut_7 # type: ignore # mutmut generated
mutants_x__normalize__mutmut['x__normalize__mutmut_8'] = x__normalize__mutmut_8 # type: ignore # mutmut generated
mutants_x__normalize__mutmut['x__normalize__mutmut_9'] = x__normalize__mutmut_9 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__pin_from_spec__mutmut)
def _pin_from_spec(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(name_part.split("[", 1)[0]) != _normalize(package):
            return None
        url = ref.split("#", 1)[0].strip()
        _, at, tag = url.rpartition("@")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(match.group(1)) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_orig(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(name_part.split("[", 1)[0]) != _normalize(package):
            return None
        url = ref.split("#", 1)[0].strip()
        _, at, tag = url.rpartition("@")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(match.group(1)) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_1(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = None
    if "://" in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(name_part.split("[", 1)[0]) != _normalize(package):
            return None
        url = ref.split("#", 1)[0].strip()
        _, at, tag = url.rpartition("@")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(match.group(1)) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_2(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "XX://XX" in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(name_part.split("[", 1)[0]) != _normalize(package):
            return None
        url = ref.split("#", 1)[0].strip()
        _, at, tag = url.rpartition("@")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(match.group(1)) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_3(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" not in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(name_part.split("[", 1)[0]) != _normalize(package):
            return None
        url = ref.split("#", 1)[0].strip()
        _, at, tag = url.rpartition("@")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(match.group(1)) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_4(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = None
        if _normalize(name_part.split("[", 1)[0]) != _normalize(package):
            return None
        url = ref.split("#", 1)[0].strip()
        _, at, tag = url.rpartition("@")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(match.group(1)) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_5(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.partition(None)
        if _normalize(name_part.split("[", 1)[0]) != _normalize(package):
            return None
        url = ref.split("#", 1)[0].strip()
        _, at, tag = url.rpartition("@")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(match.group(1)) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_6(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.rpartition("@")
        if _normalize(name_part.split("[", 1)[0]) != _normalize(package):
            return None
        url = ref.split("#", 1)[0].strip()
        _, at, tag = url.rpartition("@")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(match.group(1)) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_7(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.partition("XX@XX")
        if _normalize(name_part.split("[", 1)[0]) != _normalize(package):
            return None
        url = ref.split("#", 1)[0].strip()
        _, at, tag = url.rpartition("@")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(match.group(1)) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_8(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(None) != _normalize(package):
            return None
        url = ref.split("#", 1)[0].strip()
        _, at, tag = url.rpartition("@")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(match.group(1)) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_9(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(name_part.split(None, 1)[0]) != _normalize(package):
            return None
        url = ref.split("#", 1)[0].strip()
        _, at, tag = url.rpartition("@")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(match.group(1)) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_10(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(name_part.split("[", None)[0]) != _normalize(package):
            return None
        url = ref.split("#", 1)[0].strip()
        _, at, tag = url.rpartition("@")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(match.group(1)) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_11(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(name_part.split(1)[0]) != _normalize(package):
            return None
        url = ref.split("#", 1)[0].strip()
        _, at, tag = url.rpartition("@")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(match.group(1)) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_12(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(name_part.split("[", )[0]) != _normalize(package):
            return None
        url = ref.split("#", 1)[0].strip()
        _, at, tag = url.rpartition("@")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(match.group(1)) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_13(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(name_part.rsplit("[", 1)[0]) != _normalize(package):
            return None
        url = ref.split("#", 1)[0].strip()
        _, at, tag = url.rpartition("@")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(match.group(1)) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_14(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(name_part.split("XX[XX", 1)[0]) != _normalize(package):
            return None
        url = ref.split("#", 1)[0].strip()
        _, at, tag = url.rpartition("@")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(match.group(1)) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_15(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(name_part.split("[", 2)[0]) != _normalize(package):
            return None
        url = ref.split("#", 1)[0].strip()
        _, at, tag = url.rpartition("@")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(match.group(1)) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_16(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(name_part.split("[", 1)[1]) != _normalize(package):
            return None
        url = ref.split("#", 1)[0].strip()
        _, at, tag = url.rpartition("@")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(match.group(1)) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_17(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(name_part.split("[", 1)[0]) == _normalize(package):
            return None
        url = ref.split("#", 1)[0].strip()
        _, at, tag = url.rpartition("@")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(match.group(1)) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_18(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(name_part.split("[", 1)[0]) != _normalize(None):
            return None
        url = ref.split("#", 1)[0].strip()
        _, at, tag = url.rpartition("@")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(match.group(1)) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_19(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(name_part.split("[", 1)[0]) != _normalize(package):
            return None
        url = None
        _, at, tag = url.rpartition("@")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(match.group(1)) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_20(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(name_part.split("[", 1)[0]) != _normalize(package):
            return None
        url = ref.split(None, 1)[0].strip()
        _, at, tag = url.rpartition("@")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(match.group(1)) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_21(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(name_part.split("[", 1)[0]) != _normalize(package):
            return None
        url = ref.split("#", None)[0].strip()
        _, at, tag = url.rpartition("@")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(match.group(1)) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_22(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(name_part.split("[", 1)[0]) != _normalize(package):
            return None
        url = ref.split(1)[0].strip()
        _, at, tag = url.rpartition("@")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(match.group(1)) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_23(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(name_part.split("[", 1)[0]) != _normalize(package):
            return None
        url = ref.split("#", )[0].strip()
        _, at, tag = url.rpartition("@")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(match.group(1)) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_24(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(name_part.split("[", 1)[0]) != _normalize(package):
            return None
        url = ref.rsplit("#", 1)[0].strip()
        _, at, tag = url.rpartition("@")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(match.group(1)) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_25(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(name_part.split("[", 1)[0]) != _normalize(package):
            return None
        url = ref.split("XX#XX", 1)[0].strip()
        _, at, tag = url.rpartition("@")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(match.group(1)) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_26(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(name_part.split("[", 1)[0]) != _normalize(package):
            return None
        url = ref.split("#", 2)[0].strip()
        _, at, tag = url.rpartition("@")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(match.group(1)) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_27(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(name_part.split("[", 1)[0]) != _normalize(package):
            return None
        url = ref.split("#", 1)[1].strip()
        _, at, tag = url.rpartition("@")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(match.group(1)) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_28(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(name_part.split("[", 1)[0]) != _normalize(package):
            return None
        url = ref.split("#", 1)[0].strip()
        _, at, tag = None
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(match.group(1)) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_29(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(name_part.split("[", 1)[0]) != _normalize(package):
            return None
        url = ref.split("#", 1)[0].strip()
        _, at, tag = url.rpartition(None)
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(match.group(1)) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_30(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(name_part.split("[", 1)[0]) != _normalize(package):
            return None
        url = ref.split("#", 1)[0].strip()
        _, at, tag = url.partition("@")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(match.group(1)) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_31(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(name_part.split("[", 1)[0]) != _normalize(package):
            return None
        url = ref.split("#", 1)[0].strip()
        _, at, tag = url.rpartition("XX@XX")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(match.group(1)) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_32(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(name_part.split("[", 1)[0]) != _normalize(package):
            return None
        url = ref.split("#", 1)[0].strip()
        _, at, tag = url.rpartition("@")
        return tag if at or tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(match.group(1)) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_33(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(name_part.split("[", 1)[0]) != _normalize(package):
            return None
        url = ref.split("#", 1)[0].strip()
        _, at, tag = url.rpartition("@")
        return tag if at and tag else None
    match = None
    if match is None or _normalize(match.group(1)) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_34(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(name_part.split("[", 1)[0]) != _normalize(package):
            return None
        url = ref.split("#", 1)[0].strip()
        _, at, tag = url.rpartition("@")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(None)
    if match is None or _normalize(match.group(1)) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_35(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(name_part.split("[", 1)[0]) != _normalize(package):
            return None
        url = ref.split("#", 1)[0].strip()
        _, at, tag = url.rpartition("@")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None and _normalize(match.group(1)) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_36(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(name_part.split("[", 1)[0]) != _normalize(package):
            return None
        url = ref.split("#", 1)[0].strip()
        _, at, tag = url.rpartition("@")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is not None or _normalize(match.group(1)) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_37(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(name_part.split("[", 1)[0]) != _normalize(package):
            return None
        url = ref.split("#", 1)[0].strip()
        _, at, tag = url.rpartition("@")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(None) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_38(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(name_part.split("[", 1)[0]) != _normalize(package):
            return None
        url = ref.split("#", 1)[0].strip()
        _, at, tag = url.rpartition("@")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(match.group(None)) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_39(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(name_part.split("[", 1)[0]) != _normalize(package):
            return None
        url = ref.split("#", 1)[0].strip()
        _, at, tag = url.rpartition("@")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(match.group(2)) != _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_40(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(name_part.split("[", 1)[0]) != _normalize(package):
            return None
        url = ref.split("#", 1)[0].strip()
        _, at, tag = url.rpartition("@")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(match.group(1)) == _normalize(package):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_41(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(name_part.split("[", 1)[0]) != _normalize(package):
            return None
        url = ref.split("#", 1)[0].strip()
        _, at, tag = url.rpartition("@")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(match.group(1)) != _normalize(None):
        return None
    return match.group(2)


def x__pin_from_spec__mutmut_42(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(name_part.split("[", 1)[0]) != _normalize(package):
            return None
        url = ref.split("#", 1)[0].strip()
        _, at, tag = url.rpartition("@")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(match.group(1)) != _normalize(package):
        return None
    return match.group(None)


def x__pin_from_spec__mutmut_43(spec: str, package: str) -> str | None:
    """Extract the pinned version token from one dependency spec, or ``None``.

    Handles a PEP 508 direct-URL reference (``name @ git+...@<tag>`` — the tag is
    the segment after the URL's final ``@``, minus any ``#`` fragment) and an
    exact/compatible version specifier (``name==X.Y.Z``). A spec for a different
    package yields ``None``.
    """
    spec = spec.strip()
    if "://" in spec:
        name_part, _, ref = spec.partition("@")
        if _normalize(name_part.split("[", 1)[0]) != _normalize(package):
            return None
        url = ref.split("#", 1)[0].strip()
        _, at, tag = url.rpartition("@")
        return tag if at and tag else None
    match = _SPECIFIER_RE.match(spec)
    if match is None or _normalize(match.group(1)) != _normalize(package):
        return None
    return match.group(3)

mutants_x__pin_from_spec__mutmut['_mutmut_orig'] = x__pin_from_spec__mutmut_orig # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_1'] = x__pin_from_spec__mutmut_1 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_2'] = x__pin_from_spec__mutmut_2 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_3'] = x__pin_from_spec__mutmut_3 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_4'] = x__pin_from_spec__mutmut_4 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_5'] = x__pin_from_spec__mutmut_5 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_6'] = x__pin_from_spec__mutmut_6 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_7'] = x__pin_from_spec__mutmut_7 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_8'] = x__pin_from_spec__mutmut_8 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_9'] = x__pin_from_spec__mutmut_9 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_10'] = x__pin_from_spec__mutmut_10 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_11'] = x__pin_from_spec__mutmut_11 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_12'] = x__pin_from_spec__mutmut_12 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_13'] = x__pin_from_spec__mutmut_13 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_14'] = x__pin_from_spec__mutmut_14 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_15'] = x__pin_from_spec__mutmut_15 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_16'] = x__pin_from_spec__mutmut_16 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_17'] = x__pin_from_spec__mutmut_17 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_18'] = x__pin_from_spec__mutmut_18 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_19'] = x__pin_from_spec__mutmut_19 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_20'] = x__pin_from_spec__mutmut_20 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_21'] = x__pin_from_spec__mutmut_21 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_22'] = x__pin_from_spec__mutmut_22 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_23'] = x__pin_from_spec__mutmut_23 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_24'] = x__pin_from_spec__mutmut_24 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_25'] = x__pin_from_spec__mutmut_25 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_26'] = x__pin_from_spec__mutmut_26 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_27'] = x__pin_from_spec__mutmut_27 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_28'] = x__pin_from_spec__mutmut_28 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_29'] = x__pin_from_spec__mutmut_29 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_30'] = x__pin_from_spec__mutmut_30 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_31'] = x__pin_from_spec__mutmut_31 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_32'] = x__pin_from_spec__mutmut_32 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_33'] = x__pin_from_spec__mutmut_33 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_34'] = x__pin_from_spec__mutmut_34 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_35'] = x__pin_from_spec__mutmut_35 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_36'] = x__pin_from_spec__mutmut_36 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_37'] = x__pin_from_spec__mutmut_37 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_38'] = x__pin_from_spec__mutmut_38 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_39'] = x__pin_from_spec__mutmut_39 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_40'] = x__pin_from_spec__mutmut_40 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_41'] = x__pin_from_spec__mutmut_41 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_42'] = x__pin_from_spec__mutmut_42 # type: ignore # mutmut generated
mutants_x__pin_from_spec__mutmut['x__pin_from_spec__mutmut_43'] = x__pin_from_spec__mutmut_43 # type: ignore # mutmut generated
mutants_x__iter_dependency_specs__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__iter_dependency_specs__mutmut)
def _iter_dependency_specs(data: Mapping[str, Any]) -> Iterator[str]:
    """Yield every string dependency spec across the manifest's dependency tables.

    Covers ``[project.dependencies]``, each ``[project.optional-dependencies]``
    group, and each PEP 735 ``[dependency-groups]`` group. Non-string entries (a
    dependency-group ``include-group`` table) are skipped.
    """
    project = data.get("project", {})
    if isinstance(project, Mapping):
        for dep in project.get("dependencies", []) or []:
            if isinstance(dep, str):
                yield dep
        optional = project.get("optional-dependencies", {})
        if isinstance(optional, Mapping):
            for group in optional.values():
                for dep in group or []:
                    if isinstance(dep, str):
                        yield dep
    groups = data.get("dependency-groups", {})
    if isinstance(groups, Mapping):
        for group in groups.values():
            if isinstance(group, list):
                for dep in group:
                    if isinstance(dep, str):
                        yield dep


def x__iter_dependency_specs__mutmut_orig(data: Mapping[str, Any]) -> Iterator[str]:
    """Yield every string dependency spec across the manifest's dependency tables.

    Covers ``[project.dependencies]``, each ``[project.optional-dependencies]``
    group, and each PEP 735 ``[dependency-groups]`` group. Non-string entries (a
    dependency-group ``include-group`` table) are skipped.
    """
    project = data.get("project", {})
    if isinstance(project, Mapping):
        for dep in project.get("dependencies", []) or []:
            if isinstance(dep, str):
                yield dep
        optional = project.get("optional-dependencies", {})
        if isinstance(optional, Mapping):
            for group in optional.values():
                for dep in group or []:
                    if isinstance(dep, str):
                        yield dep
    groups = data.get("dependency-groups", {})
    if isinstance(groups, Mapping):
        for group in groups.values():
            if isinstance(group, list):
                for dep in group:
                    if isinstance(dep, str):
                        yield dep


def x__iter_dependency_specs__mutmut_1(data: Mapping[str, Any]) -> Iterator[str]:
    """Yield every string dependency spec across the manifest's dependency tables.

    Covers ``[project.dependencies]``, each ``[project.optional-dependencies]``
    group, and each PEP 735 ``[dependency-groups]`` group. Non-string entries (a
    dependency-group ``include-group`` table) are skipped.
    """
    project = None
    if isinstance(project, Mapping):
        for dep in project.get("dependencies", []) or []:
            if isinstance(dep, str):
                yield dep
        optional = project.get("optional-dependencies", {})
        if isinstance(optional, Mapping):
            for group in optional.values():
                for dep in group or []:
                    if isinstance(dep, str):
                        yield dep
    groups = data.get("dependency-groups", {})
    if isinstance(groups, Mapping):
        for group in groups.values():
            if isinstance(group, list):
                for dep in group:
                    if isinstance(dep, str):
                        yield dep


def x__iter_dependency_specs__mutmut_2(data: Mapping[str, Any]) -> Iterator[str]:
    """Yield every string dependency spec across the manifest's dependency tables.

    Covers ``[project.dependencies]``, each ``[project.optional-dependencies]``
    group, and each PEP 735 ``[dependency-groups]`` group. Non-string entries (a
    dependency-group ``include-group`` table) are skipped.
    """
    project = data.get(None, {})
    if isinstance(project, Mapping):
        for dep in project.get("dependencies", []) or []:
            if isinstance(dep, str):
                yield dep
        optional = project.get("optional-dependencies", {})
        if isinstance(optional, Mapping):
            for group in optional.values():
                for dep in group or []:
                    if isinstance(dep, str):
                        yield dep
    groups = data.get("dependency-groups", {})
    if isinstance(groups, Mapping):
        for group in groups.values():
            if isinstance(group, list):
                for dep in group:
                    if isinstance(dep, str):
                        yield dep


def x__iter_dependency_specs__mutmut_3(data: Mapping[str, Any]) -> Iterator[str]:
    """Yield every string dependency spec across the manifest's dependency tables.

    Covers ``[project.dependencies]``, each ``[project.optional-dependencies]``
    group, and each PEP 735 ``[dependency-groups]`` group. Non-string entries (a
    dependency-group ``include-group`` table) are skipped.
    """
    project = data.get("project", None)
    if isinstance(project, Mapping):
        for dep in project.get("dependencies", []) or []:
            if isinstance(dep, str):
                yield dep
        optional = project.get("optional-dependencies", {})
        if isinstance(optional, Mapping):
            for group in optional.values():
                for dep in group or []:
                    if isinstance(dep, str):
                        yield dep
    groups = data.get("dependency-groups", {})
    if isinstance(groups, Mapping):
        for group in groups.values():
            if isinstance(group, list):
                for dep in group:
                    if isinstance(dep, str):
                        yield dep


def x__iter_dependency_specs__mutmut_4(data: Mapping[str, Any]) -> Iterator[str]:
    """Yield every string dependency spec across the manifest's dependency tables.

    Covers ``[project.dependencies]``, each ``[project.optional-dependencies]``
    group, and each PEP 735 ``[dependency-groups]`` group. Non-string entries (a
    dependency-group ``include-group`` table) are skipped.
    """
    project = data.get({})
    if isinstance(project, Mapping):
        for dep in project.get("dependencies", []) or []:
            if isinstance(dep, str):
                yield dep
        optional = project.get("optional-dependencies", {})
        if isinstance(optional, Mapping):
            for group in optional.values():
                for dep in group or []:
                    if isinstance(dep, str):
                        yield dep
    groups = data.get("dependency-groups", {})
    if isinstance(groups, Mapping):
        for group in groups.values():
            if isinstance(group, list):
                for dep in group:
                    if isinstance(dep, str):
                        yield dep


def x__iter_dependency_specs__mutmut_5(data: Mapping[str, Any]) -> Iterator[str]:
    """Yield every string dependency spec across the manifest's dependency tables.

    Covers ``[project.dependencies]``, each ``[project.optional-dependencies]``
    group, and each PEP 735 ``[dependency-groups]`` group. Non-string entries (a
    dependency-group ``include-group`` table) are skipped.
    """
    project = data.get("project", )
    if isinstance(project, Mapping):
        for dep in project.get("dependencies", []) or []:
            if isinstance(dep, str):
                yield dep
        optional = project.get("optional-dependencies", {})
        if isinstance(optional, Mapping):
            for group in optional.values():
                for dep in group or []:
                    if isinstance(dep, str):
                        yield dep
    groups = data.get("dependency-groups", {})
    if isinstance(groups, Mapping):
        for group in groups.values():
            if isinstance(group, list):
                for dep in group:
                    if isinstance(dep, str):
                        yield dep


def x__iter_dependency_specs__mutmut_6(data: Mapping[str, Any]) -> Iterator[str]:
    """Yield every string dependency spec across the manifest's dependency tables.

    Covers ``[project.dependencies]``, each ``[project.optional-dependencies]``
    group, and each PEP 735 ``[dependency-groups]`` group. Non-string entries (a
    dependency-group ``include-group`` table) are skipped.
    """
    project = data.get("XXprojectXX", {})
    if isinstance(project, Mapping):
        for dep in project.get("dependencies", []) or []:
            if isinstance(dep, str):
                yield dep
        optional = project.get("optional-dependencies", {})
        if isinstance(optional, Mapping):
            for group in optional.values():
                for dep in group or []:
                    if isinstance(dep, str):
                        yield dep
    groups = data.get("dependency-groups", {})
    if isinstance(groups, Mapping):
        for group in groups.values():
            if isinstance(group, list):
                for dep in group:
                    if isinstance(dep, str):
                        yield dep


def x__iter_dependency_specs__mutmut_7(data: Mapping[str, Any]) -> Iterator[str]:
    """Yield every string dependency spec across the manifest's dependency tables.

    Covers ``[project.dependencies]``, each ``[project.optional-dependencies]``
    group, and each PEP 735 ``[dependency-groups]`` group. Non-string entries (a
    dependency-group ``include-group`` table) are skipped.
    """
    project = data.get("PROJECT", {})
    if isinstance(project, Mapping):
        for dep in project.get("dependencies", []) or []:
            if isinstance(dep, str):
                yield dep
        optional = project.get("optional-dependencies", {})
        if isinstance(optional, Mapping):
            for group in optional.values():
                for dep in group or []:
                    if isinstance(dep, str):
                        yield dep
    groups = data.get("dependency-groups", {})
    if isinstance(groups, Mapping):
        for group in groups.values():
            if isinstance(group, list):
                for dep in group:
                    if isinstance(dep, str):
                        yield dep


def x__iter_dependency_specs__mutmut_8(data: Mapping[str, Any]) -> Iterator[str]:
    """Yield every string dependency spec across the manifest's dependency tables.

    Covers ``[project.dependencies]``, each ``[project.optional-dependencies]``
    group, and each PEP 735 ``[dependency-groups]`` group. Non-string entries (a
    dependency-group ``include-group`` table) are skipped.
    """
    project = data.get("project", {})
    if isinstance(project, Mapping):
        for dep in project.get("dependencies", []) and []:
            if isinstance(dep, str):
                yield dep
        optional = project.get("optional-dependencies", {})
        if isinstance(optional, Mapping):
            for group in optional.values():
                for dep in group or []:
                    if isinstance(dep, str):
                        yield dep
    groups = data.get("dependency-groups", {})
    if isinstance(groups, Mapping):
        for group in groups.values():
            if isinstance(group, list):
                for dep in group:
                    if isinstance(dep, str):
                        yield dep


def x__iter_dependency_specs__mutmut_9(data: Mapping[str, Any]) -> Iterator[str]:
    """Yield every string dependency spec across the manifest's dependency tables.

    Covers ``[project.dependencies]``, each ``[project.optional-dependencies]``
    group, and each PEP 735 ``[dependency-groups]`` group. Non-string entries (a
    dependency-group ``include-group`` table) are skipped.
    """
    project = data.get("project", {})
    if isinstance(project, Mapping):
        for dep in project.get(None, []) or []:
            if isinstance(dep, str):
                yield dep
        optional = project.get("optional-dependencies", {})
        if isinstance(optional, Mapping):
            for group in optional.values():
                for dep in group or []:
                    if isinstance(dep, str):
                        yield dep
    groups = data.get("dependency-groups", {})
    if isinstance(groups, Mapping):
        for group in groups.values():
            if isinstance(group, list):
                for dep in group:
                    if isinstance(dep, str):
                        yield dep


def x__iter_dependency_specs__mutmut_10(data: Mapping[str, Any]) -> Iterator[str]:
    """Yield every string dependency spec across the manifest's dependency tables.

    Covers ``[project.dependencies]``, each ``[project.optional-dependencies]``
    group, and each PEP 735 ``[dependency-groups]`` group. Non-string entries (a
    dependency-group ``include-group`` table) are skipped.
    """
    project = data.get("project", {})
    if isinstance(project, Mapping):
        for dep in project.get("dependencies", None) or []:
            if isinstance(dep, str):
                yield dep
        optional = project.get("optional-dependencies", {})
        if isinstance(optional, Mapping):
            for group in optional.values():
                for dep in group or []:
                    if isinstance(dep, str):
                        yield dep
    groups = data.get("dependency-groups", {})
    if isinstance(groups, Mapping):
        for group in groups.values():
            if isinstance(group, list):
                for dep in group:
                    if isinstance(dep, str):
                        yield dep


def x__iter_dependency_specs__mutmut_11(data: Mapping[str, Any]) -> Iterator[str]:
    """Yield every string dependency spec across the manifest's dependency tables.

    Covers ``[project.dependencies]``, each ``[project.optional-dependencies]``
    group, and each PEP 735 ``[dependency-groups]`` group. Non-string entries (a
    dependency-group ``include-group`` table) are skipped.
    """
    project = data.get("project", {})
    if isinstance(project, Mapping):
        for dep in project.get([]) or []:
            if isinstance(dep, str):
                yield dep
        optional = project.get("optional-dependencies", {})
        if isinstance(optional, Mapping):
            for group in optional.values():
                for dep in group or []:
                    if isinstance(dep, str):
                        yield dep
    groups = data.get("dependency-groups", {})
    if isinstance(groups, Mapping):
        for group in groups.values():
            if isinstance(group, list):
                for dep in group:
                    if isinstance(dep, str):
                        yield dep


def x__iter_dependency_specs__mutmut_12(data: Mapping[str, Any]) -> Iterator[str]:
    """Yield every string dependency spec across the manifest's dependency tables.

    Covers ``[project.dependencies]``, each ``[project.optional-dependencies]``
    group, and each PEP 735 ``[dependency-groups]`` group. Non-string entries (a
    dependency-group ``include-group`` table) are skipped.
    """
    project = data.get("project", {})
    if isinstance(project, Mapping):
        for dep in project.get("dependencies", ) or []:
            if isinstance(dep, str):
                yield dep
        optional = project.get("optional-dependencies", {})
        if isinstance(optional, Mapping):
            for group in optional.values():
                for dep in group or []:
                    if isinstance(dep, str):
                        yield dep
    groups = data.get("dependency-groups", {})
    if isinstance(groups, Mapping):
        for group in groups.values():
            if isinstance(group, list):
                for dep in group:
                    if isinstance(dep, str):
                        yield dep


def x__iter_dependency_specs__mutmut_13(data: Mapping[str, Any]) -> Iterator[str]:
    """Yield every string dependency spec across the manifest's dependency tables.

    Covers ``[project.dependencies]``, each ``[project.optional-dependencies]``
    group, and each PEP 735 ``[dependency-groups]`` group. Non-string entries (a
    dependency-group ``include-group`` table) are skipped.
    """
    project = data.get("project", {})
    if isinstance(project, Mapping):
        for dep in project.get("XXdependenciesXX", []) or []:
            if isinstance(dep, str):
                yield dep
        optional = project.get("optional-dependencies", {})
        if isinstance(optional, Mapping):
            for group in optional.values():
                for dep in group or []:
                    if isinstance(dep, str):
                        yield dep
    groups = data.get("dependency-groups", {})
    if isinstance(groups, Mapping):
        for group in groups.values():
            if isinstance(group, list):
                for dep in group:
                    if isinstance(dep, str):
                        yield dep


def x__iter_dependency_specs__mutmut_14(data: Mapping[str, Any]) -> Iterator[str]:
    """Yield every string dependency spec across the manifest's dependency tables.

    Covers ``[project.dependencies]``, each ``[project.optional-dependencies]``
    group, and each PEP 735 ``[dependency-groups]`` group. Non-string entries (a
    dependency-group ``include-group`` table) are skipped.
    """
    project = data.get("project", {})
    if isinstance(project, Mapping):
        for dep in project.get("DEPENDENCIES", []) or []:
            if isinstance(dep, str):
                yield dep
        optional = project.get("optional-dependencies", {})
        if isinstance(optional, Mapping):
            for group in optional.values():
                for dep in group or []:
                    if isinstance(dep, str):
                        yield dep
    groups = data.get("dependency-groups", {})
    if isinstance(groups, Mapping):
        for group in groups.values():
            if isinstance(group, list):
                for dep in group:
                    if isinstance(dep, str):
                        yield dep


def x__iter_dependency_specs__mutmut_15(data: Mapping[str, Any]) -> Iterator[str]:
    """Yield every string dependency spec across the manifest's dependency tables.

    Covers ``[project.dependencies]``, each ``[project.optional-dependencies]``
    group, and each PEP 735 ``[dependency-groups]`` group. Non-string entries (a
    dependency-group ``include-group`` table) are skipped.
    """
    project = data.get("project", {})
    if isinstance(project, Mapping):
        for dep in project.get("dependencies", []) or []:
            if isinstance(dep, str):
                yield dep
        optional = None
        if isinstance(optional, Mapping):
            for group in optional.values():
                for dep in group or []:
                    if isinstance(dep, str):
                        yield dep
    groups = data.get("dependency-groups", {})
    if isinstance(groups, Mapping):
        for group in groups.values():
            if isinstance(group, list):
                for dep in group:
                    if isinstance(dep, str):
                        yield dep


def x__iter_dependency_specs__mutmut_16(data: Mapping[str, Any]) -> Iterator[str]:
    """Yield every string dependency spec across the manifest's dependency tables.

    Covers ``[project.dependencies]``, each ``[project.optional-dependencies]``
    group, and each PEP 735 ``[dependency-groups]`` group. Non-string entries (a
    dependency-group ``include-group`` table) are skipped.
    """
    project = data.get("project", {})
    if isinstance(project, Mapping):
        for dep in project.get("dependencies", []) or []:
            if isinstance(dep, str):
                yield dep
        optional = project.get(None, {})
        if isinstance(optional, Mapping):
            for group in optional.values():
                for dep in group or []:
                    if isinstance(dep, str):
                        yield dep
    groups = data.get("dependency-groups", {})
    if isinstance(groups, Mapping):
        for group in groups.values():
            if isinstance(group, list):
                for dep in group:
                    if isinstance(dep, str):
                        yield dep


def x__iter_dependency_specs__mutmut_17(data: Mapping[str, Any]) -> Iterator[str]:
    """Yield every string dependency spec across the manifest's dependency tables.

    Covers ``[project.dependencies]``, each ``[project.optional-dependencies]``
    group, and each PEP 735 ``[dependency-groups]`` group. Non-string entries (a
    dependency-group ``include-group`` table) are skipped.
    """
    project = data.get("project", {})
    if isinstance(project, Mapping):
        for dep in project.get("dependencies", []) or []:
            if isinstance(dep, str):
                yield dep
        optional = project.get("optional-dependencies", None)
        if isinstance(optional, Mapping):
            for group in optional.values():
                for dep in group or []:
                    if isinstance(dep, str):
                        yield dep
    groups = data.get("dependency-groups", {})
    if isinstance(groups, Mapping):
        for group in groups.values():
            if isinstance(group, list):
                for dep in group:
                    if isinstance(dep, str):
                        yield dep


def x__iter_dependency_specs__mutmut_18(data: Mapping[str, Any]) -> Iterator[str]:
    """Yield every string dependency spec across the manifest's dependency tables.

    Covers ``[project.dependencies]``, each ``[project.optional-dependencies]``
    group, and each PEP 735 ``[dependency-groups]`` group. Non-string entries (a
    dependency-group ``include-group`` table) are skipped.
    """
    project = data.get("project", {})
    if isinstance(project, Mapping):
        for dep in project.get("dependencies", []) or []:
            if isinstance(dep, str):
                yield dep
        optional = project.get({})
        if isinstance(optional, Mapping):
            for group in optional.values():
                for dep in group or []:
                    if isinstance(dep, str):
                        yield dep
    groups = data.get("dependency-groups", {})
    if isinstance(groups, Mapping):
        for group in groups.values():
            if isinstance(group, list):
                for dep in group:
                    if isinstance(dep, str):
                        yield dep


def x__iter_dependency_specs__mutmut_19(data: Mapping[str, Any]) -> Iterator[str]:
    """Yield every string dependency spec across the manifest's dependency tables.

    Covers ``[project.dependencies]``, each ``[project.optional-dependencies]``
    group, and each PEP 735 ``[dependency-groups]`` group. Non-string entries (a
    dependency-group ``include-group`` table) are skipped.
    """
    project = data.get("project", {})
    if isinstance(project, Mapping):
        for dep in project.get("dependencies", []) or []:
            if isinstance(dep, str):
                yield dep
        optional = project.get("optional-dependencies", )
        if isinstance(optional, Mapping):
            for group in optional.values():
                for dep in group or []:
                    if isinstance(dep, str):
                        yield dep
    groups = data.get("dependency-groups", {})
    if isinstance(groups, Mapping):
        for group in groups.values():
            if isinstance(group, list):
                for dep in group:
                    if isinstance(dep, str):
                        yield dep


def x__iter_dependency_specs__mutmut_20(data: Mapping[str, Any]) -> Iterator[str]:
    """Yield every string dependency spec across the manifest's dependency tables.

    Covers ``[project.dependencies]``, each ``[project.optional-dependencies]``
    group, and each PEP 735 ``[dependency-groups]`` group. Non-string entries (a
    dependency-group ``include-group`` table) are skipped.
    """
    project = data.get("project", {})
    if isinstance(project, Mapping):
        for dep in project.get("dependencies", []) or []:
            if isinstance(dep, str):
                yield dep
        optional = project.get("XXoptional-dependenciesXX", {})
        if isinstance(optional, Mapping):
            for group in optional.values():
                for dep in group or []:
                    if isinstance(dep, str):
                        yield dep
    groups = data.get("dependency-groups", {})
    if isinstance(groups, Mapping):
        for group in groups.values():
            if isinstance(group, list):
                for dep in group:
                    if isinstance(dep, str):
                        yield dep


def x__iter_dependency_specs__mutmut_21(data: Mapping[str, Any]) -> Iterator[str]:
    """Yield every string dependency spec across the manifest's dependency tables.

    Covers ``[project.dependencies]``, each ``[project.optional-dependencies]``
    group, and each PEP 735 ``[dependency-groups]`` group. Non-string entries (a
    dependency-group ``include-group`` table) are skipped.
    """
    project = data.get("project", {})
    if isinstance(project, Mapping):
        for dep in project.get("dependencies", []) or []:
            if isinstance(dep, str):
                yield dep
        optional = project.get("OPTIONAL-DEPENDENCIES", {})
        if isinstance(optional, Mapping):
            for group in optional.values():
                for dep in group or []:
                    if isinstance(dep, str):
                        yield dep
    groups = data.get("dependency-groups", {})
    if isinstance(groups, Mapping):
        for group in groups.values():
            if isinstance(group, list):
                for dep in group:
                    if isinstance(dep, str):
                        yield dep


def x__iter_dependency_specs__mutmut_22(data: Mapping[str, Any]) -> Iterator[str]:
    """Yield every string dependency spec across the manifest's dependency tables.

    Covers ``[project.dependencies]``, each ``[project.optional-dependencies]``
    group, and each PEP 735 ``[dependency-groups]`` group. Non-string entries (a
    dependency-group ``include-group`` table) are skipped.
    """
    project = data.get("project", {})
    if isinstance(project, Mapping):
        for dep in project.get("dependencies", []) or []:
            if isinstance(dep, str):
                yield dep
        optional = project.get("optional-dependencies", {})
        if isinstance(optional, Mapping):
            for group in optional.values():
                for dep in group and []:
                    if isinstance(dep, str):
                        yield dep
    groups = data.get("dependency-groups", {})
    if isinstance(groups, Mapping):
        for group in groups.values():
            if isinstance(group, list):
                for dep in group:
                    if isinstance(dep, str):
                        yield dep


def x__iter_dependency_specs__mutmut_23(data: Mapping[str, Any]) -> Iterator[str]:
    """Yield every string dependency spec across the manifest's dependency tables.

    Covers ``[project.dependencies]``, each ``[project.optional-dependencies]``
    group, and each PEP 735 ``[dependency-groups]`` group. Non-string entries (a
    dependency-group ``include-group`` table) are skipped.
    """
    project = data.get("project", {})
    if isinstance(project, Mapping):
        for dep in project.get("dependencies", []) or []:
            if isinstance(dep, str):
                yield dep
        optional = project.get("optional-dependencies", {})
        if isinstance(optional, Mapping):
            for group in optional.values():
                for dep in group or []:
                    if isinstance(dep, str):
                        yield dep
    groups = None
    if isinstance(groups, Mapping):
        for group in groups.values():
            if isinstance(group, list):
                for dep in group:
                    if isinstance(dep, str):
                        yield dep


def x__iter_dependency_specs__mutmut_24(data: Mapping[str, Any]) -> Iterator[str]:
    """Yield every string dependency spec across the manifest's dependency tables.

    Covers ``[project.dependencies]``, each ``[project.optional-dependencies]``
    group, and each PEP 735 ``[dependency-groups]`` group. Non-string entries (a
    dependency-group ``include-group`` table) are skipped.
    """
    project = data.get("project", {})
    if isinstance(project, Mapping):
        for dep in project.get("dependencies", []) or []:
            if isinstance(dep, str):
                yield dep
        optional = project.get("optional-dependencies", {})
        if isinstance(optional, Mapping):
            for group in optional.values():
                for dep in group or []:
                    if isinstance(dep, str):
                        yield dep
    groups = data.get(None, {})
    if isinstance(groups, Mapping):
        for group in groups.values():
            if isinstance(group, list):
                for dep in group:
                    if isinstance(dep, str):
                        yield dep


def x__iter_dependency_specs__mutmut_25(data: Mapping[str, Any]) -> Iterator[str]:
    """Yield every string dependency spec across the manifest's dependency tables.

    Covers ``[project.dependencies]``, each ``[project.optional-dependencies]``
    group, and each PEP 735 ``[dependency-groups]`` group. Non-string entries (a
    dependency-group ``include-group`` table) are skipped.
    """
    project = data.get("project", {})
    if isinstance(project, Mapping):
        for dep in project.get("dependencies", []) or []:
            if isinstance(dep, str):
                yield dep
        optional = project.get("optional-dependencies", {})
        if isinstance(optional, Mapping):
            for group in optional.values():
                for dep in group or []:
                    if isinstance(dep, str):
                        yield dep
    groups = data.get("dependency-groups", None)
    if isinstance(groups, Mapping):
        for group in groups.values():
            if isinstance(group, list):
                for dep in group:
                    if isinstance(dep, str):
                        yield dep


def x__iter_dependency_specs__mutmut_26(data: Mapping[str, Any]) -> Iterator[str]:
    """Yield every string dependency spec across the manifest's dependency tables.

    Covers ``[project.dependencies]``, each ``[project.optional-dependencies]``
    group, and each PEP 735 ``[dependency-groups]`` group. Non-string entries (a
    dependency-group ``include-group`` table) are skipped.
    """
    project = data.get("project", {})
    if isinstance(project, Mapping):
        for dep in project.get("dependencies", []) or []:
            if isinstance(dep, str):
                yield dep
        optional = project.get("optional-dependencies", {})
        if isinstance(optional, Mapping):
            for group in optional.values():
                for dep in group or []:
                    if isinstance(dep, str):
                        yield dep
    groups = data.get({})
    if isinstance(groups, Mapping):
        for group in groups.values():
            if isinstance(group, list):
                for dep in group:
                    if isinstance(dep, str):
                        yield dep


def x__iter_dependency_specs__mutmut_27(data: Mapping[str, Any]) -> Iterator[str]:
    """Yield every string dependency spec across the manifest's dependency tables.

    Covers ``[project.dependencies]``, each ``[project.optional-dependencies]``
    group, and each PEP 735 ``[dependency-groups]`` group. Non-string entries (a
    dependency-group ``include-group`` table) are skipped.
    """
    project = data.get("project", {})
    if isinstance(project, Mapping):
        for dep in project.get("dependencies", []) or []:
            if isinstance(dep, str):
                yield dep
        optional = project.get("optional-dependencies", {})
        if isinstance(optional, Mapping):
            for group in optional.values():
                for dep in group or []:
                    if isinstance(dep, str):
                        yield dep
    groups = data.get("dependency-groups", )
    if isinstance(groups, Mapping):
        for group in groups.values():
            if isinstance(group, list):
                for dep in group:
                    if isinstance(dep, str):
                        yield dep


def x__iter_dependency_specs__mutmut_28(data: Mapping[str, Any]) -> Iterator[str]:
    """Yield every string dependency spec across the manifest's dependency tables.

    Covers ``[project.dependencies]``, each ``[project.optional-dependencies]``
    group, and each PEP 735 ``[dependency-groups]`` group. Non-string entries (a
    dependency-group ``include-group`` table) are skipped.
    """
    project = data.get("project", {})
    if isinstance(project, Mapping):
        for dep in project.get("dependencies", []) or []:
            if isinstance(dep, str):
                yield dep
        optional = project.get("optional-dependencies", {})
        if isinstance(optional, Mapping):
            for group in optional.values():
                for dep in group or []:
                    if isinstance(dep, str):
                        yield dep
    groups = data.get("XXdependency-groupsXX", {})
    if isinstance(groups, Mapping):
        for group in groups.values():
            if isinstance(group, list):
                for dep in group:
                    if isinstance(dep, str):
                        yield dep


def x__iter_dependency_specs__mutmut_29(data: Mapping[str, Any]) -> Iterator[str]:
    """Yield every string dependency spec across the manifest's dependency tables.

    Covers ``[project.dependencies]``, each ``[project.optional-dependencies]``
    group, and each PEP 735 ``[dependency-groups]`` group. Non-string entries (a
    dependency-group ``include-group`` table) are skipped.
    """
    project = data.get("project", {})
    if isinstance(project, Mapping):
        for dep in project.get("dependencies", []) or []:
            if isinstance(dep, str):
                yield dep
        optional = project.get("optional-dependencies", {})
        if isinstance(optional, Mapping):
            for group in optional.values():
                for dep in group or []:
                    if isinstance(dep, str):
                        yield dep
    groups = data.get("DEPENDENCY-GROUPS", {})
    if isinstance(groups, Mapping):
        for group in groups.values():
            if isinstance(group, list):
                for dep in group:
                    if isinstance(dep, str):
                        yield dep

mutants_x__iter_dependency_specs__mutmut['_mutmut_orig'] = x__iter_dependency_specs__mutmut_orig # type: ignore # mutmut generated
mutants_x__iter_dependency_specs__mutmut['x__iter_dependency_specs__mutmut_1'] = x__iter_dependency_specs__mutmut_1 # type: ignore # mutmut generated
mutants_x__iter_dependency_specs__mutmut['x__iter_dependency_specs__mutmut_2'] = x__iter_dependency_specs__mutmut_2 # type: ignore # mutmut generated
mutants_x__iter_dependency_specs__mutmut['x__iter_dependency_specs__mutmut_3'] = x__iter_dependency_specs__mutmut_3 # type: ignore # mutmut generated
mutants_x__iter_dependency_specs__mutmut['x__iter_dependency_specs__mutmut_4'] = x__iter_dependency_specs__mutmut_4 # type: ignore # mutmut generated
mutants_x__iter_dependency_specs__mutmut['x__iter_dependency_specs__mutmut_5'] = x__iter_dependency_specs__mutmut_5 # type: ignore # mutmut generated
mutants_x__iter_dependency_specs__mutmut['x__iter_dependency_specs__mutmut_6'] = x__iter_dependency_specs__mutmut_6 # type: ignore # mutmut generated
mutants_x__iter_dependency_specs__mutmut['x__iter_dependency_specs__mutmut_7'] = x__iter_dependency_specs__mutmut_7 # type: ignore # mutmut generated
mutants_x__iter_dependency_specs__mutmut['x__iter_dependency_specs__mutmut_8'] = x__iter_dependency_specs__mutmut_8 # type: ignore # mutmut generated
mutants_x__iter_dependency_specs__mutmut['x__iter_dependency_specs__mutmut_9'] = x__iter_dependency_specs__mutmut_9 # type: ignore # mutmut generated
mutants_x__iter_dependency_specs__mutmut['x__iter_dependency_specs__mutmut_10'] = x__iter_dependency_specs__mutmut_10 # type: ignore # mutmut generated
mutants_x__iter_dependency_specs__mutmut['x__iter_dependency_specs__mutmut_11'] = x__iter_dependency_specs__mutmut_11 # type: ignore # mutmut generated
mutants_x__iter_dependency_specs__mutmut['x__iter_dependency_specs__mutmut_12'] = x__iter_dependency_specs__mutmut_12 # type: ignore # mutmut generated
mutants_x__iter_dependency_specs__mutmut['x__iter_dependency_specs__mutmut_13'] = x__iter_dependency_specs__mutmut_13 # type: ignore # mutmut generated
mutants_x__iter_dependency_specs__mutmut['x__iter_dependency_specs__mutmut_14'] = x__iter_dependency_specs__mutmut_14 # type: ignore # mutmut generated
mutants_x__iter_dependency_specs__mutmut['x__iter_dependency_specs__mutmut_15'] = x__iter_dependency_specs__mutmut_15 # type: ignore # mutmut generated
mutants_x__iter_dependency_specs__mutmut['x__iter_dependency_specs__mutmut_16'] = x__iter_dependency_specs__mutmut_16 # type: ignore # mutmut generated
mutants_x__iter_dependency_specs__mutmut['x__iter_dependency_specs__mutmut_17'] = x__iter_dependency_specs__mutmut_17 # type: ignore # mutmut generated
mutants_x__iter_dependency_specs__mutmut['x__iter_dependency_specs__mutmut_18'] = x__iter_dependency_specs__mutmut_18 # type: ignore # mutmut generated
mutants_x__iter_dependency_specs__mutmut['x__iter_dependency_specs__mutmut_19'] = x__iter_dependency_specs__mutmut_19 # type: ignore # mutmut generated
mutants_x__iter_dependency_specs__mutmut['x__iter_dependency_specs__mutmut_20'] = x__iter_dependency_specs__mutmut_20 # type: ignore # mutmut generated
mutants_x__iter_dependency_specs__mutmut['x__iter_dependency_specs__mutmut_21'] = x__iter_dependency_specs__mutmut_21 # type: ignore # mutmut generated
mutants_x__iter_dependency_specs__mutmut['x__iter_dependency_specs__mutmut_22'] = x__iter_dependency_specs__mutmut_22 # type: ignore # mutmut generated
mutants_x__iter_dependency_specs__mutmut['x__iter_dependency_specs__mutmut_23'] = x__iter_dependency_specs__mutmut_23 # type: ignore # mutmut generated
mutants_x__iter_dependency_specs__mutmut['x__iter_dependency_specs__mutmut_24'] = x__iter_dependency_specs__mutmut_24 # type: ignore # mutmut generated
mutants_x__iter_dependency_specs__mutmut['x__iter_dependency_specs__mutmut_25'] = x__iter_dependency_specs__mutmut_25 # type: ignore # mutmut generated
mutants_x__iter_dependency_specs__mutmut['x__iter_dependency_specs__mutmut_26'] = x__iter_dependency_specs__mutmut_26 # type: ignore # mutmut generated
mutants_x__iter_dependency_specs__mutmut['x__iter_dependency_specs__mutmut_27'] = x__iter_dependency_specs__mutmut_27 # type: ignore # mutmut generated
mutants_x__iter_dependency_specs__mutmut['x__iter_dependency_specs__mutmut_28'] = x__iter_dependency_specs__mutmut_28 # type: ignore # mutmut generated
mutants_x__iter_dependency_specs__mutmut['x__iter_dependency_specs__mutmut_29'] = x__iter_dependency_specs__mutmut_29 # type: ignore # mutmut generated
mutants_x__uv_source_tag__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__uv_source_tag__mutmut)
def _uv_source_tag(data: Mapping[str, Any], package: str) -> str | None:
    """The ``tag`` a ``[tool.uv.sources]`` entry pins ``package`` to, or ``None``.

    When a consumer uses uv sources, the ``[project.dependencies]`` spec is a
    bare name and the pinned tag lives here instead.
    """
    tool = data.get("tool", {})
    if not isinstance(tool, Mapping):
        return None
    uv = tool.get("uv", {})
    if not isinstance(uv, Mapping):
        return None
    sources = uv.get("sources", {})
    if not isinstance(sources, Mapping):
        return None
    for name, source in sources.items():
        if _normalize(str(name)) == _normalize(package) and isinstance(source, Mapping):
            tag = source.get("tag")
            if isinstance(tag, str):
                return tag
    return None


def x__uv_source_tag__mutmut_orig(data: Mapping[str, Any], package: str) -> str | None:
    """The ``tag`` a ``[tool.uv.sources]`` entry pins ``package`` to, or ``None``.

    When a consumer uses uv sources, the ``[project.dependencies]`` spec is a
    bare name and the pinned tag lives here instead.
    """
    tool = data.get("tool", {})
    if not isinstance(tool, Mapping):
        return None
    uv = tool.get("uv", {})
    if not isinstance(uv, Mapping):
        return None
    sources = uv.get("sources", {})
    if not isinstance(sources, Mapping):
        return None
    for name, source in sources.items():
        if _normalize(str(name)) == _normalize(package) and isinstance(source, Mapping):
            tag = source.get("tag")
            if isinstance(tag, str):
                return tag
    return None


def x__uv_source_tag__mutmut_1(data: Mapping[str, Any], package: str) -> str | None:
    """The ``tag`` a ``[tool.uv.sources]`` entry pins ``package`` to, or ``None``.

    When a consumer uses uv sources, the ``[project.dependencies]`` spec is a
    bare name and the pinned tag lives here instead.
    """
    tool = None
    if not isinstance(tool, Mapping):
        return None
    uv = tool.get("uv", {})
    if not isinstance(uv, Mapping):
        return None
    sources = uv.get("sources", {})
    if not isinstance(sources, Mapping):
        return None
    for name, source in sources.items():
        if _normalize(str(name)) == _normalize(package) and isinstance(source, Mapping):
            tag = source.get("tag")
            if isinstance(tag, str):
                return tag
    return None


def x__uv_source_tag__mutmut_2(data: Mapping[str, Any], package: str) -> str | None:
    """The ``tag`` a ``[tool.uv.sources]`` entry pins ``package`` to, or ``None``.

    When a consumer uses uv sources, the ``[project.dependencies]`` spec is a
    bare name and the pinned tag lives here instead.
    """
    tool = data.get(None, {})
    if not isinstance(tool, Mapping):
        return None
    uv = tool.get("uv", {})
    if not isinstance(uv, Mapping):
        return None
    sources = uv.get("sources", {})
    if not isinstance(sources, Mapping):
        return None
    for name, source in sources.items():
        if _normalize(str(name)) == _normalize(package) and isinstance(source, Mapping):
            tag = source.get("tag")
            if isinstance(tag, str):
                return tag
    return None


def x__uv_source_tag__mutmut_3(data: Mapping[str, Any], package: str) -> str | None:
    """The ``tag`` a ``[tool.uv.sources]`` entry pins ``package`` to, or ``None``.

    When a consumer uses uv sources, the ``[project.dependencies]`` spec is a
    bare name and the pinned tag lives here instead.
    """
    tool = data.get("tool", None)
    if not isinstance(tool, Mapping):
        return None
    uv = tool.get("uv", {})
    if not isinstance(uv, Mapping):
        return None
    sources = uv.get("sources", {})
    if not isinstance(sources, Mapping):
        return None
    for name, source in sources.items():
        if _normalize(str(name)) == _normalize(package) and isinstance(source, Mapping):
            tag = source.get("tag")
            if isinstance(tag, str):
                return tag
    return None


def x__uv_source_tag__mutmut_4(data: Mapping[str, Any], package: str) -> str | None:
    """The ``tag`` a ``[tool.uv.sources]`` entry pins ``package`` to, or ``None``.

    When a consumer uses uv sources, the ``[project.dependencies]`` spec is a
    bare name and the pinned tag lives here instead.
    """
    tool = data.get({})
    if not isinstance(tool, Mapping):
        return None
    uv = tool.get("uv", {})
    if not isinstance(uv, Mapping):
        return None
    sources = uv.get("sources", {})
    if not isinstance(sources, Mapping):
        return None
    for name, source in sources.items():
        if _normalize(str(name)) == _normalize(package) and isinstance(source, Mapping):
            tag = source.get("tag")
            if isinstance(tag, str):
                return tag
    return None


def x__uv_source_tag__mutmut_5(data: Mapping[str, Any], package: str) -> str | None:
    """The ``tag`` a ``[tool.uv.sources]`` entry pins ``package`` to, or ``None``.

    When a consumer uses uv sources, the ``[project.dependencies]`` spec is a
    bare name and the pinned tag lives here instead.
    """
    tool = data.get("tool", )
    if not isinstance(tool, Mapping):
        return None
    uv = tool.get("uv", {})
    if not isinstance(uv, Mapping):
        return None
    sources = uv.get("sources", {})
    if not isinstance(sources, Mapping):
        return None
    for name, source in sources.items():
        if _normalize(str(name)) == _normalize(package) and isinstance(source, Mapping):
            tag = source.get("tag")
            if isinstance(tag, str):
                return tag
    return None


def x__uv_source_tag__mutmut_6(data: Mapping[str, Any], package: str) -> str | None:
    """The ``tag`` a ``[tool.uv.sources]`` entry pins ``package`` to, or ``None``.

    When a consumer uses uv sources, the ``[project.dependencies]`` spec is a
    bare name and the pinned tag lives here instead.
    """
    tool = data.get("XXtoolXX", {})
    if not isinstance(tool, Mapping):
        return None
    uv = tool.get("uv", {})
    if not isinstance(uv, Mapping):
        return None
    sources = uv.get("sources", {})
    if not isinstance(sources, Mapping):
        return None
    for name, source in sources.items():
        if _normalize(str(name)) == _normalize(package) and isinstance(source, Mapping):
            tag = source.get("tag")
            if isinstance(tag, str):
                return tag
    return None


def x__uv_source_tag__mutmut_7(data: Mapping[str, Any], package: str) -> str | None:
    """The ``tag`` a ``[tool.uv.sources]`` entry pins ``package`` to, or ``None``.

    When a consumer uses uv sources, the ``[project.dependencies]`` spec is a
    bare name and the pinned tag lives here instead.
    """
    tool = data.get("TOOL", {})
    if not isinstance(tool, Mapping):
        return None
    uv = tool.get("uv", {})
    if not isinstance(uv, Mapping):
        return None
    sources = uv.get("sources", {})
    if not isinstance(sources, Mapping):
        return None
    for name, source in sources.items():
        if _normalize(str(name)) == _normalize(package) and isinstance(source, Mapping):
            tag = source.get("tag")
            if isinstance(tag, str):
                return tag
    return None


def x__uv_source_tag__mutmut_8(data: Mapping[str, Any], package: str) -> str | None:
    """The ``tag`` a ``[tool.uv.sources]`` entry pins ``package`` to, or ``None``.

    When a consumer uses uv sources, the ``[project.dependencies]`` spec is a
    bare name and the pinned tag lives here instead.
    """
    tool = data.get("tool", {})
    if isinstance(tool, Mapping):
        return None
    uv = tool.get("uv", {})
    if not isinstance(uv, Mapping):
        return None
    sources = uv.get("sources", {})
    if not isinstance(sources, Mapping):
        return None
    for name, source in sources.items():
        if _normalize(str(name)) == _normalize(package) and isinstance(source, Mapping):
            tag = source.get("tag")
            if isinstance(tag, str):
                return tag
    return None


def x__uv_source_tag__mutmut_9(data: Mapping[str, Any], package: str) -> str | None:
    """The ``tag`` a ``[tool.uv.sources]`` entry pins ``package`` to, or ``None``.

    When a consumer uses uv sources, the ``[project.dependencies]`` spec is a
    bare name and the pinned tag lives here instead.
    """
    tool = data.get("tool", {})
    if not isinstance(tool, Mapping):
        return None
    uv = None
    if not isinstance(uv, Mapping):
        return None
    sources = uv.get("sources", {})
    if not isinstance(sources, Mapping):
        return None
    for name, source in sources.items():
        if _normalize(str(name)) == _normalize(package) and isinstance(source, Mapping):
            tag = source.get("tag")
            if isinstance(tag, str):
                return tag
    return None


def x__uv_source_tag__mutmut_10(data: Mapping[str, Any], package: str) -> str | None:
    """The ``tag`` a ``[tool.uv.sources]`` entry pins ``package`` to, or ``None``.

    When a consumer uses uv sources, the ``[project.dependencies]`` spec is a
    bare name and the pinned tag lives here instead.
    """
    tool = data.get("tool", {})
    if not isinstance(tool, Mapping):
        return None
    uv = tool.get(None, {})
    if not isinstance(uv, Mapping):
        return None
    sources = uv.get("sources", {})
    if not isinstance(sources, Mapping):
        return None
    for name, source in sources.items():
        if _normalize(str(name)) == _normalize(package) and isinstance(source, Mapping):
            tag = source.get("tag")
            if isinstance(tag, str):
                return tag
    return None


def x__uv_source_tag__mutmut_11(data: Mapping[str, Any], package: str) -> str | None:
    """The ``tag`` a ``[tool.uv.sources]`` entry pins ``package`` to, or ``None``.

    When a consumer uses uv sources, the ``[project.dependencies]`` spec is a
    bare name and the pinned tag lives here instead.
    """
    tool = data.get("tool", {})
    if not isinstance(tool, Mapping):
        return None
    uv = tool.get("uv", None)
    if not isinstance(uv, Mapping):
        return None
    sources = uv.get("sources", {})
    if not isinstance(sources, Mapping):
        return None
    for name, source in sources.items():
        if _normalize(str(name)) == _normalize(package) and isinstance(source, Mapping):
            tag = source.get("tag")
            if isinstance(tag, str):
                return tag
    return None


def x__uv_source_tag__mutmut_12(data: Mapping[str, Any], package: str) -> str | None:
    """The ``tag`` a ``[tool.uv.sources]`` entry pins ``package`` to, or ``None``.

    When a consumer uses uv sources, the ``[project.dependencies]`` spec is a
    bare name and the pinned tag lives here instead.
    """
    tool = data.get("tool", {})
    if not isinstance(tool, Mapping):
        return None
    uv = tool.get({})
    if not isinstance(uv, Mapping):
        return None
    sources = uv.get("sources", {})
    if not isinstance(sources, Mapping):
        return None
    for name, source in sources.items():
        if _normalize(str(name)) == _normalize(package) and isinstance(source, Mapping):
            tag = source.get("tag")
            if isinstance(tag, str):
                return tag
    return None


def x__uv_source_tag__mutmut_13(data: Mapping[str, Any], package: str) -> str | None:
    """The ``tag`` a ``[tool.uv.sources]`` entry pins ``package`` to, or ``None``.

    When a consumer uses uv sources, the ``[project.dependencies]`` spec is a
    bare name and the pinned tag lives here instead.
    """
    tool = data.get("tool", {})
    if not isinstance(tool, Mapping):
        return None
    uv = tool.get("uv", )
    if not isinstance(uv, Mapping):
        return None
    sources = uv.get("sources", {})
    if not isinstance(sources, Mapping):
        return None
    for name, source in sources.items():
        if _normalize(str(name)) == _normalize(package) and isinstance(source, Mapping):
            tag = source.get("tag")
            if isinstance(tag, str):
                return tag
    return None


def x__uv_source_tag__mutmut_14(data: Mapping[str, Any], package: str) -> str | None:
    """The ``tag`` a ``[tool.uv.sources]`` entry pins ``package`` to, or ``None``.

    When a consumer uses uv sources, the ``[project.dependencies]`` spec is a
    bare name and the pinned tag lives here instead.
    """
    tool = data.get("tool", {})
    if not isinstance(tool, Mapping):
        return None
    uv = tool.get("XXuvXX", {})
    if not isinstance(uv, Mapping):
        return None
    sources = uv.get("sources", {})
    if not isinstance(sources, Mapping):
        return None
    for name, source in sources.items():
        if _normalize(str(name)) == _normalize(package) and isinstance(source, Mapping):
            tag = source.get("tag")
            if isinstance(tag, str):
                return tag
    return None


def x__uv_source_tag__mutmut_15(data: Mapping[str, Any], package: str) -> str | None:
    """The ``tag`` a ``[tool.uv.sources]`` entry pins ``package`` to, or ``None``.

    When a consumer uses uv sources, the ``[project.dependencies]`` spec is a
    bare name and the pinned tag lives here instead.
    """
    tool = data.get("tool", {})
    if not isinstance(tool, Mapping):
        return None
    uv = tool.get("UV", {})
    if not isinstance(uv, Mapping):
        return None
    sources = uv.get("sources", {})
    if not isinstance(sources, Mapping):
        return None
    for name, source in sources.items():
        if _normalize(str(name)) == _normalize(package) and isinstance(source, Mapping):
            tag = source.get("tag")
            if isinstance(tag, str):
                return tag
    return None


def x__uv_source_tag__mutmut_16(data: Mapping[str, Any], package: str) -> str | None:
    """The ``tag`` a ``[tool.uv.sources]`` entry pins ``package`` to, or ``None``.

    When a consumer uses uv sources, the ``[project.dependencies]`` spec is a
    bare name and the pinned tag lives here instead.
    """
    tool = data.get("tool", {})
    if not isinstance(tool, Mapping):
        return None
    uv = tool.get("uv", {})
    if isinstance(uv, Mapping):
        return None
    sources = uv.get("sources", {})
    if not isinstance(sources, Mapping):
        return None
    for name, source in sources.items():
        if _normalize(str(name)) == _normalize(package) and isinstance(source, Mapping):
            tag = source.get("tag")
            if isinstance(tag, str):
                return tag
    return None


def x__uv_source_tag__mutmut_17(data: Mapping[str, Any], package: str) -> str | None:
    """The ``tag`` a ``[tool.uv.sources]`` entry pins ``package`` to, or ``None``.

    When a consumer uses uv sources, the ``[project.dependencies]`` spec is a
    bare name and the pinned tag lives here instead.
    """
    tool = data.get("tool", {})
    if not isinstance(tool, Mapping):
        return None
    uv = tool.get("uv", {})
    if not isinstance(uv, Mapping):
        return None
    sources = None
    if not isinstance(sources, Mapping):
        return None
    for name, source in sources.items():
        if _normalize(str(name)) == _normalize(package) and isinstance(source, Mapping):
            tag = source.get("tag")
            if isinstance(tag, str):
                return tag
    return None


def x__uv_source_tag__mutmut_18(data: Mapping[str, Any], package: str) -> str | None:
    """The ``tag`` a ``[tool.uv.sources]`` entry pins ``package`` to, or ``None``.

    When a consumer uses uv sources, the ``[project.dependencies]`` spec is a
    bare name and the pinned tag lives here instead.
    """
    tool = data.get("tool", {})
    if not isinstance(tool, Mapping):
        return None
    uv = tool.get("uv", {})
    if not isinstance(uv, Mapping):
        return None
    sources = uv.get(None, {})
    if not isinstance(sources, Mapping):
        return None
    for name, source in sources.items():
        if _normalize(str(name)) == _normalize(package) and isinstance(source, Mapping):
            tag = source.get("tag")
            if isinstance(tag, str):
                return tag
    return None


def x__uv_source_tag__mutmut_19(data: Mapping[str, Any], package: str) -> str | None:
    """The ``tag`` a ``[tool.uv.sources]`` entry pins ``package`` to, or ``None``.

    When a consumer uses uv sources, the ``[project.dependencies]`` spec is a
    bare name and the pinned tag lives here instead.
    """
    tool = data.get("tool", {})
    if not isinstance(tool, Mapping):
        return None
    uv = tool.get("uv", {})
    if not isinstance(uv, Mapping):
        return None
    sources = uv.get("sources", None)
    if not isinstance(sources, Mapping):
        return None
    for name, source in sources.items():
        if _normalize(str(name)) == _normalize(package) and isinstance(source, Mapping):
            tag = source.get("tag")
            if isinstance(tag, str):
                return tag
    return None


def x__uv_source_tag__mutmut_20(data: Mapping[str, Any], package: str) -> str | None:
    """The ``tag`` a ``[tool.uv.sources]`` entry pins ``package`` to, or ``None``.

    When a consumer uses uv sources, the ``[project.dependencies]`` spec is a
    bare name and the pinned tag lives here instead.
    """
    tool = data.get("tool", {})
    if not isinstance(tool, Mapping):
        return None
    uv = tool.get("uv", {})
    if not isinstance(uv, Mapping):
        return None
    sources = uv.get({})
    if not isinstance(sources, Mapping):
        return None
    for name, source in sources.items():
        if _normalize(str(name)) == _normalize(package) and isinstance(source, Mapping):
            tag = source.get("tag")
            if isinstance(tag, str):
                return tag
    return None


def x__uv_source_tag__mutmut_21(data: Mapping[str, Any], package: str) -> str | None:
    """The ``tag`` a ``[tool.uv.sources]`` entry pins ``package`` to, or ``None``.

    When a consumer uses uv sources, the ``[project.dependencies]`` spec is a
    bare name and the pinned tag lives here instead.
    """
    tool = data.get("tool", {})
    if not isinstance(tool, Mapping):
        return None
    uv = tool.get("uv", {})
    if not isinstance(uv, Mapping):
        return None
    sources = uv.get("sources", )
    if not isinstance(sources, Mapping):
        return None
    for name, source in sources.items():
        if _normalize(str(name)) == _normalize(package) and isinstance(source, Mapping):
            tag = source.get("tag")
            if isinstance(tag, str):
                return tag
    return None


def x__uv_source_tag__mutmut_22(data: Mapping[str, Any], package: str) -> str | None:
    """The ``tag`` a ``[tool.uv.sources]`` entry pins ``package`` to, or ``None``.

    When a consumer uses uv sources, the ``[project.dependencies]`` spec is a
    bare name and the pinned tag lives here instead.
    """
    tool = data.get("tool", {})
    if not isinstance(tool, Mapping):
        return None
    uv = tool.get("uv", {})
    if not isinstance(uv, Mapping):
        return None
    sources = uv.get("XXsourcesXX", {})
    if not isinstance(sources, Mapping):
        return None
    for name, source in sources.items():
        if _normalize(str(name)) == _normalize(package) and isinstance(source, Mapping):
            tag = source.get("tag")
            if isinstance(tag, str):
                return tag
    return None


def x__uv_source_tag__mutmut_23(data: Mapping[str, Any], package: str) -> str | None:
    """The ``tag`` a ``[tool.uv.sources]`` entry pins ``package`` to, or ``None``.

    When a consumer uses uv sources, the ``[project.dependencies]`` spec is a
    bare name and the pinned tag lives here instead.
    """
    tool = data.get("tool", {})
    if not isinstance(tool, Mapping):
        return None
    uv = tool.get("uv", {})
    if not isinstance(uv, Mapping):
        return None
    sources = uv.get("SOURCES", {})
    if not isinstance(sources, Mapping):
        return None
    for name, source in sources.items():
        if _normalize(str(name)) == _normalize(package) and isinstance(source, Mapping):
            tag = source.get("tag")
            if isinstance(tag, str):
                return tag
    return None


def x__uv_source_tag__mutmut_24(data: Mapping[str, Any], package: str) -> str | None:
    """The ``tag`` a ``[tool.uv.sources]`` entry pins ``package`` to, or ``None``.

    When a consumer uses uv sources, the ``[project.dependencies]`` spec is a
    bare name and the pinned tag lives here instead.
    """
    tool = data.get("tool", {})
    if not isinstance(tool, Mapping):
        return None
    uv = tool.get("uv", {})
    if not isinstance(uv, Mapping):
        return None
    sources = uv.get("sources", {})
    if isinstance(sources, Mapping):
        return None
    for name, source in sources.items():
        if _normalize(str(name)) == _normalize(package) and isinstance(source, Mapping):
            tag = source.get("tag")
            if isinstance(tag, str):
                return tag
    return None


def x__uv_source_tag__mutmut_25(data: Mapping[str, Any], package: str) -> str | None:
    """The ``tag`` a ``[tool.uv.sources]`` entry pins ``package`` to, or ``None``.

    When a consumer uses uv sources, the ``[project.dependencies]`` spec is a
    bare name and the pinned tag lives here instead.
    """
    tool = data.get("tool", {})
    if not isinstance(tool, Mapping):
        return None
    uv = tool.get("uv", {})
    if not isinstance(uv, Mapping):
        return None
    sources = uv.get("sources", {})
    if not isinstance(sources, Mapping):
        return None
    for name, source in sources.items():
        if _normalize(str(name)) == _normalize(package) or isinstance(source, Mapping):
            tag = source.get("tag")
            if isinstance(tag, str):
                return tag
    return None


def x__uv_source_tag__mutmut_26(data: Mapping[str, Any], package: str) -> str | None:
    """The ``tag`` a ``[tool.uv.sources]`` entry pins ``package`` to, or ``None``.

    When a consumer uses uv sources, the ``[project.dependencies]`` spec is a
    bare name and the pinned tag lives here instead.
    """
    tool = data.get("tool", {})
    if not isinstance(tool, Mapping):
        return None
    uv = tool.get("uv", {})
    if not isinstance(uv, Mapping):
        return None
    sources = uv.get("sources", {})
    if not isinstance(sources, Mapping):
        return None
    for name, source in sources.items():
        if _normalize(None) == _normalize(package) and isinstance(source, Mapping):
            tag = source.get("tag")
            if isinstance(tag, str):
                return tag
    return None


def x__uv_source_tag__mutmut_27(data: Mapping[str, Any], package: str) -> str | None:
    """The ``tag`` a ``[tool.uv.sources]`` entry pins ``package`` to, or ``None``.

    When a consumer uses uv sources, the ``[project.dependencies]`` spec is a
    bare name and the pinned tag lives here instead.
    """
    tool = data.get("tool", {})
    if not isinstance(tool, Mapping):
        return None
    uv = tool.get("uv", {})
    if not isinstance(uv, Mapping):
        return None
    sources = uv.get("sources", {})
    if not isinstance(sources, Mapping):
        return None
    for name, source in sources.items():
        if _normalize(str(None)) == _normalize(package) and isinstance(source, Mapping):
            tag = source.get("tag")
            if isinstance(tag, str):
                return tag
    return None


def x__uv_source_tag__mutmut_28(data: Mapping[str, Any], package: str) -> str | None:
    """The ``tag`` a ``[tool.uv.sources]`` entry pins ``package`` to, or ``None``.

    When a consumer uses uv sources, the ``[project.dependencies]`` spec is a
    bare name and the pinned tag lives here instead.
    """
    tool = data.get("tool", {})
    if not isinstance(tool, Mapping):
        return None
    uv = tool.get("uv", {})
    if not isinstance(uv, Mapping):
        return None
    sources = uv.get("sources", {})
    if not isinstance(sources, Mapping):
        return None
    for name, source in sources.items():
        if _normalize(str(name)) != _normalize(package) and isinstance(source, Mapping):
            tag = source.get("tag")
            if isinstance(tag, str):
                return tag
    return None


def x__uv_source_tag__mutmut_29(data: Mapping[str, Any], package: str) -> str | None:
    """The ``tag`` a ``[tool.uv.sources]`` entry pins ``package`` to, or ``None``.

    When a consumer uses uv sources, the ``[project.dependencies]`` spec is a
    bare name and the pinned tag lives here instead.
    """
    tool = data.get("tool", {})
    if not isinstance(tool, Mapping):
        return None
    uv = tool.get("uv", {})
    if not isinstance(uv, Mapping):
        return None
    sources = uv.get("sources", {})
    if not isinstance(sources, Mapping):
        return None
    for name, source in sources.items():
        if _normalize(str(name)) == _normalize(None) and isinstance(source, Mapping):
            tag = source.get("tag")
            if isinstance(tag, str):
                return tag
    return None


def x__uv_source_tag__mutmut_30(data: Mapping[str, Any], package: str) -> str | None:
    """The ``tag`` a ``[tool.uv.sources]`` entry pins ``package`` to, or ``None``.

    When a consumer uses uv sources, the ``[project.dependencies]`` spec is a
    bare name and the pinned tag lives here instead.
    """
    tool = data.get("tool", {})
    if not isinstance(tool, Mapping):
        return None
    uv = tool.get("uv", {})
    if not isinstance(uv, Mapping):
        return None
    sources = uv.get("sources", {})
    if not isinstance(sources, Mapping):
        return None
    for name, source in sources.items():
        if _normalize(str(name)) == _normalize(package) and isinstance(source, Mapping):
            tag = None
            if isinstance(tag, str):
                return tag
    return None


def x__uv_source_tag__mutmut_31(data: Mapping[str, Any], package: str) -> str | None:
    """The ``tag`` a ``[tool.uv.sources]`` entry pins ``package`` to, or ``None``.

    When a consumer uses uv sources, the ``[project.dependencies]`` spec is a
    bare name and the pinned tag lives here instead.
    """
    tool = data.get("tool", {})
    if not isinstance(tool, Mapping):
        return None
    uv = tool.get("uv", {})
    if not isinstance(uv, Mapping):
        return None
    sources = uv.get("sources", {})
    if not isinstance(sources, Mapping):
        return None
    for name, source in sources.items():
        if _normalize(str(name)) == _normalize(package) and isinstance(source, Mapping):
            tag = source.get(None)
            if isinstance(tag, str):
                return tag
    return None


def x__uv_source_tag__mutmut_32(data: Mapping[str, Any], package: str) -> str | None:
    """The ``tag`` a ``[tool.uv.sources]`` entry pins ``package`` to, or ``None``.

    When a consumer uses uv sources, the ``[project.dependencies]`` spec is a
    bare name and the pinned tag lives here instead.
    """
    tool = data.get("tool", {})
    if not isinstance(tool, Mapping):
        return None
    uv = tool.get("uv", {})
    if not isinstance(uv, Mapping):
        return None
    sources = uv.get("sources", {})
    if not isinstance(sources, Mapping):
        return None
    for name, source in sources.items():
        if _normalize(str(name)) == _normalize(package) and isinstance(source, Mapping):
            tag = source.get("XXtagXX")
            if isinstance(tag, str):
                return tag
    return None


def x__uv_source_tag__mutmut_33(data: Mapping[str, Any], package: str) -> str | None:
    """The ``tag`` a ``[tool.uv.sources]`` entry pins ``package`` to, or ``None``.

    When a consumer uses uv sources, the ``[project.dependencies]`` spec is a
    bare name and the pinned tag lives here instead.
    """
    tool = data.get("tool", {})
    if not isinstance(tool, Mapping):
        return None
    uv = tool.get("uv", {})
    if not isinstance(uv, Mapping):
        return None
    sources = uv.get("sources", {})
    if not isinstance(sources, Mapping):
        return None
    for name, source in sources.items():
        if _normalize(str(name)) == _normalize(package) and isinstance(source, Mapping):
            tag = source.get("TAG")
            if isinstance(tag, str):
                return tag
    return None

mutants_x__uv_source_tag__mutmut['_mutmut_orig'] = x__uv_source_tag__mutmut_orig # type: ignore # mutmut generated
mutants_x__uv_source_tag__mutmut['x__uv_source_tag__mutmut_1'] = x__uv_source_tag__mutmut_1 # type: ignore # mutmut generated
mutants_x__uv_source_tag__mutmut['x__uv_source_tag__mutmut_2'] = x__uv_source_tag__mutmut_2 # type: ignore # mutmut generated
mutants_x__uv_source_tag__mutmut['x__uv_source_tag__mutmut_3'] = x__uv_source_tag__mutmut_3 # type: ignore # mutmut generated
mutants_x__uv_source_tag__mutmut['x__uv_source_tag__mutmut_4'] = x__uv_source_tag__mutmut_4 # type: ignore # mutmut generated
mutants_x__uv_source_tag__mutmut['x__uv_source_tag__mutmut_5'] = x__uv_source_tag__mutmut_5 # type: ignore # mutmut generated
mutants_x__uv_source_tag__mutmut['x__uv_source_tag__mutmut_6'] = x__uv_source_tag__mutmut_6 # type: ignore # mutmut generated
mutants_x__uv_source_tag__mutmut['x__uv_source_tag__mutmut_7'] = x__uv_source_tag__mutmut_7 # type: ignore # mutmut generated
mutants_x__uv_source_tag__mutmut['x__uv_source_tag__mutmut_8'] = x__uv_source_tag__mutmut_8 # type: ignore # mutmut generated
mutants_x__uv_source_tag__mutmut['x__uv_source_tag__mutmut_9'] = x__uv_source_tag__mutmut_9 # type: ignore # mutmut generated
mutants_x__uv_source_tag__mutmut['x__uv_source_tag__mutmut_10'] = x__uv_source_tag__mutmut_10 # type: ignore # mutmut generated
mutants_x__uv_source_tag__mutmut['x__uv_source_tag__mutmut_11'] = x__uv_source_tag__mutmut_11 # type: ignore # mutmut generated
mutants_x__uv_source_tag__mutmut['x__uv_source_tag__mutmut_12'] = x__uv_source_tag__mutmut_12 # type: ignore # mutmut generated
mutants_x__uv_source_tag__mutmut['x__uv_source_tag__mutmut_13'] = x__uv_source_tag__mutmut_13 # type: ignore # mutmut generated
mutants_x__uv_source_tag__mutmut['x__uv_source_tag__mutmut_14'] = x__uv_source_tag__mutmut_14 # type: ignore # mutmut generated
mutants_x__uv_source_tag__mutmut['x__uv_source_tag__mutmut_15'] = x__uv_source_tag__mutmut_15 # type: ignore # mutmut generated
mutants_x__uv_source_tag__mutmut['x__uv_source_tag__mutmut_16'] = x__uv_source_tag__mutmut_16 # type: ignore # mutmut generated
mutants_x__uv_source_tag__mutmut['x__uv_source_tag__mutmut_17'] = x__uv_source_tag__mutmut_17 # type: ignore # mutmut generated
mutants_x__uv_source_tag__mutmut['x__uv_source_tag__mutmut_18'] = x__uv_source_tag__mutmut_18 # type: ignore # mutmut generated
mutants_x__uv_source_tag__mutmut['x__uv_source_tag__mutmut_19'] = x__uv_source_tag__mutmut_19 # type: ignore # mutmut generated
mutants_x__uv_source_tag__mutmut['x__uv_source_tag__mutmut_20'] = x__uv_source_tag__mutmut_20 # type: ignore # mutmut generated
mutants_x__uv_source_tag__mutmut['x__uv_source_tag__mutmut_21'] = x__uv_source_tag__mutmut_21 # type: ignore # mutmut generated
mutants_x__uv_source_tag__mutmut['x__uv_source_tag__mutmut_22'] = x__uv_source_tag__mutmut_22 # type: ignore # mutmut generated
mutants_x__uv_source_tag__mutmut['x__uv_source_tag__mutmut_23'] = x__uv_source_tag__mutmut_23 # type: ignore # mutmut generated
mutants_x__uv_source_tag__mutmut['x__uv_source_tag__mutmut_24'] = x__uv_source_tag__mutmut_24 # type: ignore # mutmut generated
mutants_x__uv_source_tag__mutmut['x__uv_source_tag__mutmut_25'] = x__uv_source_tag__mutmut_25 # type: ignore # mutmut generated
mutants_x__uv_source_tag__mutmut['x__uv_source_tag__mutmut_26'] = x__uv_source_tag__mutmut_26 # type: ignore # mutmut generated
mutants_x__uv_source_tag__mutmut['x__uv_source_tag__mutmut_27'] = x__uv_source_tag__mutmut_27 # type: ignore # mutmut generated
mutants_x__uv_source_tag__mutmut['x__uv_source_tag__mutmut_28'] = x__uv_source_tag__mutmut_28 # type: ignore # mutmut generated
mutants_x__uv_source_tag__mutmut['x__uv_source_tag__mutmut_29'] = x__uv_source_tag__mutmut_29 # type: ignore # mutmut generated
mutants_x__uv_source_tag__mutmut['x__uv_source_tag__mutmut_30'] = x__uv_source_tag__mutmut_30 # type: ignore # mutmut generated
mutants_x__uv_source_tag__mutmut['x__uv_source_tag__mutmut_31'] = x__uv_source_tag__mutmut_31 # type: ignore # mutmut generated
mutants_x__uv_source_tag__mutmut['x__uv_source_tag__mutmut_32'] = x__uv_source_tag__mutmut_32 # type: ignore # mutmut generated
mutants_x__uv_source_tag__mutmut['x__uv_source_tag__mutmut_33'] = x__uv_source_tag__mutmut_33 # type: ignore # mutmut generated
mutants_x_resolve_declared_version__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_resolve_declared_version__mutmut)
def resolve_declared_version(pyproject_path: Path, package: str) -> str | None:
    """The version the consumer DECLARES for ``package`` in its manifest, or ``None``.

    Reads the dependency specs first (a direct-URL ``@tag`` or a ``==`` pin), then
    a ``[tool.uv.sources]`` tag. A missing / unreadable / malformed manifest, or
    a manifest that does not mention ``package``, yields ``None``.
    """
    try:
        text = pyproject_path.read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError:
        return None
    for spec in _iter_dependency_specs(data):
        pin = _pin_from_spec(spec, package)
        if pin is not None:
            return pin
    return _uv_source_tag(data, package)


def x_resolve_declared_version__mutmut_orig(pyproject_path: Path, package: str) -> str | None:
    """The version the consumer DECLARES for ``package`` in its manifest, or ``None``.

    Reads the dependency specs first (a direct-URL ``@tag`` or a ``==`` pin), then
    a ``[tool.uv.sources]`` tag. A missing / unreadable / malformed manifest, or
    a manifest that does not mention ``package``, yields ``None``.
    """
    try:
        text = pyproject_path.read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError:
        return None
    for spec in _iter_dependency_specs(data):
        pin = _pin_from_spec(spec, package)
        if pin is not None:
            return pin
    return _uv_source_tag(data, package)


def x_resolve_declared_version__mutmut_1(pyproject_path: Path, package: str) -> str | None:
    """The version the consumer DECLARES for ``package`` in its manifest, or ``None``.

    Reads the dependency specs first (a direct-URL ``@tag`` or a ``==`` pin), then
    a ``[tool.uv.sources]`` tag. A missing / unreadable / malformed manifest, or
    a manifest that does not mention ``package``, yields ``None``.
    """
    try:
        text = None
    except OSError:
        return None
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError:
        return None
    for spec in _iter_dependency_specs(data):
        pin = _pin_from_spec(spec, package)
        if pin is not None:
            return pin
    return _uv_source_tag(data, package)


def x_resolve_declared_version__mutmut_2(pyproject_path: Path, package: str) -> str | None:
    """The version the consumer DECLARES for ``package`` in its manifest, or ``None``.

    Reads the dependency specs first (a direct-URL ``@tag`` or a ``==`` pin), then
    a ``[tool.uv.sources]`` tag. A missing / unreadable / malformed manifest, or
    a manifest that does not mention ``package``, yields ``None``.
    """
    try:
        text = pyproject_path.read_text(encoding=None)
    except OSError:
        return None
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError:
        return None
    for spec in _iter_dependency_specs(data):
        pin = _pin_from_spec(spec, package)
        if pin is not None:
            return pin
    return _uv_source_tag(data, package)


def x_resolve_declared_version__mutmut_3(pyproject_path: Path, package: str) -> str | None:
    """The version the consumer DECLARES for ``package`` in its manifest, or ``None``.

    Reads the dependency specs first (a direct-URL ``@tag`` or a ``==`` pin), then
    a ``[tool.uv.sources]`` tag. A missing / unreadable / malformed manifest, or
    a manifest that does not mention ``package``, yields ``None``.
    """
    try:
        text = pyproject_path.read_text(encoding="XXutf-8XX")
    except OSError:
        return None
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError:
        return None
    for spec in _iter_dependency_specs(data):
        pin = _pin_from_spec(spec, package)
        if pin is not None:
            return pin
    return _uv_source_tag(data, package)


def x_resolve_declared_version__mutmut_4(pyproject_path: Path, package: str) -> str | None:
    """The version the consumer DECLARES for ``package`` in its manifest, or ``None``.

    Reads the dependency specs first (a direct-URL ``@tag`` or a ``==`` pin), then
    a ``[tool.uv.sources]`` tag. A missing / unreadable / malformed manifest, or
    a manifest that does not mention ``package``, yields ``None``.
    """
    try:
        text = pyproject_path.read_text(encoding="UTF-8")
    except OSError:
        return None
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError:
        return None
    for spec in _iter_dependency_specs(data):
        pin = _pin_from_spec(spec, package)
        if pin is not None:
            return pin
    return _uv_source_tag(data, package)


def x_resolve_declared_version__mutmut_5(pyproject_path: Path, package: str) -> str | None:
    """The version the consumer DECLARES for ``package`` in its manifest, or ``None``.

    Reads the dependency specs first (a direct-URL ``@tag`` or a ``==`` pin), then
    a ``[tool.uv.sources]`` tag. A missing / unreadable / malformed manifest, or
    a manifest that does not mention ``package``, yields ``None``.
    """
    try:
        text = pyproject_path.read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        data = None
    except tomllib.TOMLDecodeError:
        return None
    for spec in _iter_dependency_specs(data):
        pin = _pin_from_spec(spec, package)
        if pin is not None:
            return pin
    return _uv_source_tag(data, package)


def x_resolve_declared_version__mutmut_6(pyproject_path: Path, package: str) -> str | None:
    """The version the consumer DECLARES for ``package`` in its manifest, or ``None``.

    Reads the dependency specs first (a direct-URL ``@tag`` or a ``==`` pin), then
    a ``[tool.uv.sources]`` tag. A missing / unreadable / malformed manifest, or
    a manifest that does not mention ``package``, yields ``None``.
    """
    try:
        text = pyproject_path.read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        data = tomllib.loads(None)
    except tomllib.TOMLDecodeError:
        return None
    for spec in _iter_dependency_specs(data):
        pin = _pin_from_spec(spec, package)
        if pin is not None:
            return pin
    return _uv_source_tag(data, package)


def x_resolve_declared_version__mutmut_7(pyproject_path: Path, package: str) -> str | None:
    """The version the consumer DECLARES for ``package`` in its manifest, or ``None``.

    Reads the dependency specs first (a direct-URL ``@tag`` or a ``==`` pin), then
    a ``[tool.uv.sources]`` tag. A missing / unreadable / malformed manifest, or
    a manifest that does not mention ``package``, yields ``None``.
    """
    try:
        text = pyproject_path.read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError:
        return None
    for spec in _iter_dependency_specs(None):
        pin = _pin_from_spec(spec, package)
        if pin is not None:
            return pin
    return _uv_source_tag(data, package)


def x_resolve_declared_version__mutmut_8(pyproject_path: Path, package: str) -> str | None:
    """The version the consumer DECLARES for ``package`` in its manifest, or ``None``.

    Reads the dependency specs first (a direct-URL ``@tag`` or a ``==`` pin), then
    a ``[tool.uv.sources]`` tag. A missing / unreadable / malformed manifest, or
    a manifest that does not mention ``package``, yields ``None``.
    """
    try:
        text = pyproject_path.read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError:
        return None
    for spec in _iter_dependency_specs(data):
        pin = None
        if pin is not None:
            return pin
    return _uv_source_tag(data, package)


def x_resolve_declared_version__mutmut_9(pyproject_path: Path, package: str) -> str | None:
    """The version the consumer DECLARES for ``package`` in its manifest, or ``None``.

    Reads the dependency specs first (a direct-URL ``@tag`` or a ``==`` pin), then
    a ``[tool.uv.sources]`` tag. A missing / unreadable / malformed manifest, or
    a manifest that does not mention ``package``, yields ``None``.
    """
    try:
        text = pyproject_path.read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError:
        return None
    for spec in _iter_dependency_specs(data):
        pin = _pin_from_spec(None, package)
        if pin is not None:
            return pin
    return _uv_source_tag(data, package)


def x_resolve_declared_version__mutmut_10(pyproject_path: Path, package: str) -> str | None:
    """The version the consumer DECLARES for ``package`` in its manifest, or ``None``.

    Reads the dependency specs first (a direct-URL ``@tag`` or a ``==`` pin), then
    a ``[tool.uv.sources]`` tag. A missing / unreadable / malformed manifest, or
    a manifest that does not mention ``package``, yields ``None``.
    """
    try:
        text = pyproject_path.read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError:
        return None
    for spec in _iter_dependency_specs(data):
        pin = _pin_from_spec(spec, None)
        if pin is not None:
            return pin
    return _uv_source_tag(data, package)


def x_resolve_declared_version__mutmut_11(pyproject_path: Path, package: str) -> str | None:
    """The version the consumer DECLARES for ``package`` in its manifest, or ``None``.

    Reads the dependency specs first (a direct-URL ``@tag`` or a ``==`` pin), then
    a ``[tool.uv.sources]`` tag. A missing / unreadable / malformed manifest, or
    a manifest that does not mention ``package``, yields ``None``.
    """
    try:
        text = pyproject_path.read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError:
        return None
    for spec in _iter_dependency_specs(data):
        pin = _pin_from_spec(package)
        if pin is not None:
            return pin
    return _uv_source_tag(data, package)


def x_resolve_declared_version__mutmut_12(pyproject_path: Path, package: str) -> str | None:
    """The version the consumer DECLARES for ``package`` in its manifest, or ``None``.

    Reads the dependency specs first (a direct-URL ``@tag`` or a ``==`` pin), then
    a ``[tool.uv.sources]`` tag. A missing / unreadable / malformed manifest, or
    a manifest that does not mention ``package``, yields ``None``.
    """
    try:
        text = pyproject_path.read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError:
        return None
    for spec in _iter_dependency_specs(data):
        pin = _pin_from_spec(spec, )
        if pin is not None:
            return pin
    return _uv_source_tag(data, package)


def x_resolve_declared_version__mutmut_13(pyproject_path: Path, package: str) -> str | None:
    """The version the consumer DECLARES for ``package`` in its manifest, or ``None``.

    Reads the dependency specs first (a direct-URL ``@tag`` or a ``==`` pin), then
    a ``[tool.uv.sources]`` tag. A missing / unreadable / malformed manifest, or
    a manifest that does not mention ``package``, yields ``None``.
    """
    try:
        text = pyproject_path.read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError:
        return None
    for spec in _iter_dependency_specs(data):
        pin = _pin_from_spec(spec, package)
        if pin is None:
            return pin
    return _uv_source_tag(data, package)


def x_resolve_declared_version__mutmut_14(pyproject_path: Path, package: str) -> str | None:
    """The version the consumer DECLARES for ``package`` in its manifest, or ``None``.

    Reads the dependency specs first (a direct-URL ``@tag`` or a ``==`` pin), then
    a ``[tool.uv.sources]`` tag. A missing / unreadable / malformed manifest, or
    a manifest that does not mention ``package``, yields ``None``.
    """
    try:
        text = pyproject_path.read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError:
        return None
    for spec in _iter_dependency_specs(data):
        pin = _pin_from_spec(spec, package)
        if pin is not None:
            return pin
    return _uv_source_tag(None, package)


def x_resolve_declared_version__mutmut_15(pyproject_path: Path, package: str) -> str | None:
    """The version the consumer DECLARES for ``package`` in its manifest, or ``None``.

    Reads the dependency specs first (a direct-URL ``@tag`` or a ``==`` pin), then
    a ``[tool.uv.sources]`` tag. A missing / unreadable / malformed manifest, or
    a manifest that does not mention ``package``, yields ``None``.
    """
    try:
        text = pyproject_path.read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError:
        return None
    for spec in _iter_dependency_specs(data):
        pin = _pin_from_spec(spec, package)
        if pin is not None:
            return pin
    return _uv_source_tag(data, None)


def x_resolve_declared_version__mutmut_16(pyproject_path: Path, package: str) -> str | None:
    """The version the consumer DECLARES for ``package`` in its manifest, or ``None``.

    Reads the dependency specs first (a direct-URL ``@tag`` or a ``==`` pin), then
    a ``[tool.uv.sources]`` tag. A missing / unreadable / malformed manifest, or
    a manifest that does not mention ``package``, yields ``None``.
    """
    try:
        text = pyproject_path.read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError:
        return None
    for spec in _iter_dependency_specs(data):
        pin = _pin_from_spec(spec, package)
        if pin is not None:
            return pin
    return _uv_source_tag(package)


def x_resolve_declared_version__mutmut_17(pyproject_path: Path, package: str) -> str | None:
    """The version the consumer DECLARES for ``package`` in its manifest, or ``None``.

    Reads the dependency specs first (a direct-URL ``@tag`` or a ``==`` pin), then
    a ``[tool.uv.sources]`` tag. A missing / unreadable / malformed manifest, or
    a manifest that does not mention ``package``, yields ``None``.
    """
    try:
        text = pyproject_path.read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError:
        return None
    for spec in _iter_dependency_specs(data):
        pin = _pin_from_spec(spec, package)
        if pin is not None:
            return pin
    return _uv_source_tag(data, )

mutants_x_resolve_declared_version__mutmut['_mutmut_orig'] = x_resolve_declared_version__mutmut_orig # type: ignore # mutmut generated
mutants_x_resolve_declared_version__mutmut['x_resolve_declared_version__mutmut_1'] = x_resolve_declared_version__mutmut_1 # type: ignore # mutmut generated
mutants_x_resolve_declared_version__mutmut['x_resolve_declared_version__mutmut_2'] = x_resolve_declared_version__mutmut_2 # type: ignore # mutmut generated
mutants_x_resolve_declared_version__mutmut['x_resolve_declared_version__mutmut_3'] = x_resolve_declared_version__mutmut_3 # type: ignore # mutmut generated
mutants_x_resolve_declared_version__mutmut['x_resolve_declared_version__mutmut_4'] = x_resolve_declared_version__mutmut_4 # type: ignore # mutmut generated
mutants_x_resolve_declared_version__mutmut['x_resolve_declared_version__mutmut_5'] = x_resolve_declared_version__mutmut_5 # type: ignore # mutmut generated
mutants_x_resolve_declared_version__mutmut['x_resolve_declared_version__mutmut_6'] = x_resolve_declared_version__mutmut_6 # type: ignore # mutmut generated
mutants_x_resolve_declared_version__mutmut['x_resolve_declared_version__mutmut_7'] = x_resolve_declared_version__mutmut_7 # type: ignore # mutmut generated
mutants_x_resolve_declared_version__mutmut['x_resolve_declared_version__mutmut_8'] = x_resolve_declared_version__mutmut_8 # type: ignore # mutmut generated
mutants_x_resolve_declared_version__mutmut['x_resolve_declared_version__mutmut_9'] = x_resolve_declared_version__mutmut_9 # type: ignore # mutmut generated
mutants_x_resolve_declared_version__mutmut['x_resolve_declared_version__mutmut_10'] = x_resolve_declared_version__mutmut_10 # type: ignore # mutmut generated
mutants_x_resolve_declared_version__mutmut['x_resolve_declared_version__mutmut_11'] = x_resolve_declared_version__mutmut_11 # type: ignore # mutmut generated
mutants_x_resolve_declared_version__mutmut['x_resolve_declared_version__mutmut_12'] = x_resolve_declared_version__mutmut_12 # type: ignore # mutmut generated
mutants_x_resolve_declared_version__mutmut['x_resolve_declared_version__mutmut_13'] = x_resolve_declared_version__mutmut_13 # type: ignore # mutmut generated
mutants_x_resolve_declared_version__mutmut['x_resolve_declared_version__mutmut_14'] = x_resolve_declared_version__mutmut_14 # type: ignore # mutmut generated
mutants_x_resolve_declared_version__mutmut['x_resolve_declared_version__mutmut_15'] = x_resolve_declared_version__mutmut_15 # type: ignore # mutmut generated
mutants_x_resolve_declared_version__mutmut['x_resolve_declared_version__mutmut_16'] = x_resolve_declared_version__mutmut_16 # type: ignore # mutmut generated
mutants_x_resolve_declared_version__mutmut['x_resolve_declared_version__mutmut_17'] = x_resolve_declared_version__mutmut_17 # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁEngineVersionFloorǁ_installed_version__mutmut: MutantDict = {}  # type: ignore
mutants_xǁEngineVersionFloorǁresolve_version__mutmut: MutantDict = {}  # type: ignore
mutants_xǁEngineVersionFloorǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore
mutants_xǁEngineVersionFloorǁcollect_violations__mutmut: MutantDict = {}  # type: ignore


class EngineVersionFloor(FitnessRule):
    """Flags a consumer whose pinned engine version is below the floor."""

    name = "engine-version-floor"
    remediation = REMEDIATION

    #: Config (repo-neutral defaults; overridden per consumer via from_config).
    floor: str = ""
    package: str = DEFAULT_PACKAGE

    @classmethod
    @_mutmut_mutated(mutants_xǁEngineVersionFloorǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EngineVersionFloor:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EngineVersionFloor)  # noqa: S101  # narrowing for mypy
        floor = config.get("floor")
        rule.floor = str(floor) if floor else ""
        rule.package = str(config.get("package", DEFAULT_PACKAGE))
        return rule

    @classmethod
    def xǁEngineVersionFloorǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EngineVersionFloor:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EngineVersionFloor)  # noqa: S101  # narrowing for mypy
        floor = config.get("floor")
        rule.floor = str(floor) if floor else ""
        rule.package = str(config.get("package", DEFAULT_PACKAGE))
        return rule

    @classmethod
    def xǁEngineVersionFloorǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EngineVersionFloor:
        rule = None
        assert isinstance(rule, EngineVersionFloor)  # noqa: S101  # narrowing for mypy
        floor = config.get("floor")
        rule.floor = str(floor) if floor else ""
        rule.package = str(config.get("package", DEFAULT_PACKAGE))
        return rule

    @classmethod
    def xǁEngineVersionFloorǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EngineVersionFloor:
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, EngineVersionFloor)  # noqa: S101  # narrowing for mypy
        floor = config.get("floor")
        rule.floor = str(floor) if floor else ""
        rule.package = str(config.get("package", DEFAULT_PACKAGE))
        return rule

    @classmethod
    def xǁEngineVersionFloorǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EngineVersionFloor:
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, EngineVersionFloor)  # noqa: S101  # narrowing for mypy
        floor = config.get("floor")
        rule.floor = str(floor) if floor else ""
        rule.package = str(config.get("package", DEFAULT_PACKAGE))
        return rule

    @classmethod
    def xǁEngineVersionFloorǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EngineVersionFloor:
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, EngineVersionFloor)  # noqa: S101  # narrowing for mypy
        floor = config.get("floor")
        rule.floor = str(floor) if floor else ""
        rule.package = str(config.get("package", DEFAULT_PACKAGE))
        return rule

    @classmethod
    def xǁEngineVersionFloorǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EngineVersionFloor:
        rule = super().from_config(config, )
        assert isinstance(rule, EngineVersionFloor)  # noqa: S101  # narrowing for mypy
        floor = config.get("floor")
        rule.floor = str(floor) if floor else ""
        rule.package = str(config.get("package", DEFAULT_PACKAGE))
        return rule

    @classmethod
    def xǁEngineVersionFloorǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EngineVersionFloor:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EngineVersionFloor)  # noqa: S101  # narrowing for mypy
        floor = None
        rule.floor = str(floor) if floor else ""
        rule.package = str(config.get("package", DEFAULT_PACKAGE))
        return rule

    @classmethod
    def xǁEngineVersionFloorǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EngineVersionFloor:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EngineVersionFloor)  # noqa: S101  # narrowing for mypy
        floor = config.get(None)
        rule.floor = str(floor) if floor else ""
        rule.package = str(config.get("package", DEFAULT_PACKAGE))
        return rule

    @classmethod
    def xǁEngineVersionFloorǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EngineVersionFloor:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EngineVersionFloor)  # noqa: S101  # narrowing for mypy
        floor = config.get("XXfloorXX")
        rule.floor = str(floor) if floor else ""
        rule.package = str(config.get("package", DEFAULT_PACKAGE))
        return rule

    @classmethod
    def xǁEngineVersionFloorǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EngineVersionFloor:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EngineVersionFloor)  # noqa: S101  # narrowing for mypy
        floor = config.get("FLOOR")
        rule.floor = str(floor) if floor else ""
        rule.package = str(config.get("package", DEFAULT_PACKAGE))
        return rule

    @classmethod
    def xǁEngineVersionFloorǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EngineVersionFloor:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EngineVersionFloor)  # noqa: S101  # narrowing for mypy
        floor = config.get("floor")
        rule.floor = None
        rule.package = str(config.get("package", DEFAULT_PACKAGE))
        return rule

    @classmethod
    def xǁEngineVersionFloorǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EngineVersionFloor:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EngineVersionFloor)  # noqa: S101  # narrowing for mypy
        floor = config.get("floor")
        rule.floor = str(None) if floor else ""
        rule.package = str(config.get("package", DEFAULT_PACKAGE))
        return rule

    @classmethod
    def xǁEngineVersionFloorǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EngineVersionFloor:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EngineVersionFloor)  # noqa: S101  # narrowing for mypy
        floor = config.get("floor")
        rule.floor = str(floor) if floor else "XXXX"
        rule.package = str(config.get("package", DEFAULT_PACKAGE))
        return rule

    @classmethod
    def xǁEngineVersionFloorǁfrom_config__mutmut_13(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EngineVersionFloor:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EngineVersionFloor)  # noqa: S101  # narrowing for mypy
        floor = config.get("floor")
        rule.floor = str(floor) if floor else ""
        rule.package = None
        return rule

    @classmethod
    def xǁEngineVersionFloorǁfrom_config__mutmut_14(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EngineVersionFloor:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EngineVersionFloor)  # noqa: S101  # narrowing for mypy
        floor = config.get("floor")
        rule.floor = str(floor) if floor else ""
        rule.package = str(None)
        return rule

    @classmethod
    def xǁEngineVersionFloorǁfrom_config__mutmut_15(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EngineVersionFloor:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EngineVersionFloor)  # noqa: S101  # narrowing for mypy
        floor = config.get("floor")
        rule.floor = str(floor) if floor else ""
        rule.package = str(config.get(None, DEFAULT_PACKAGE))
        return rule

    @classmethod
    def xǁEngineVersionFloorǁfrom_config__mutmut_16(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EngineVersionFloor:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EngineVersionFloor)  # noqa: S101  # narrowing for mypy
        floor = config.get("floor")
        rule.floor = str(floor) if floor else ""
        rule.package = str(config.get("package", None))
        return rule

    @classmethod
    def xǁEngineVersionFloorǁfrom_config__mutmut_17(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EngineVersionFloor:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EngineVersionFloor)  # noqa: S101  # narrowing for mypy
        floor = config.get("floor")
        rule.floor = str(floor) if floor else ""
        rule.package = str(config.get(DEFAULT_PACKAGE))
        return rule

    @classmethod
    def xǁEngineVersionFloorǁfrom_config__mutmut_18(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EngineVersionFloor:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EngineVersionFloor)  # noqa: S101  # narrowing for mypy
        floor = config.get("floor")
        rule.floor = str(floor) if floor else ""
        rule.package = str(config.get("package", ))
        return rule

    @classmethod
    def xǁEngineVersionFloorǁfrom_config__mutmut_19(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EngineVersionFloor:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EngineVersionFloor)  # noqa: S101  # narrowing for mypy
        floor = config.get("floor")
        rule.floor = str(floor) if floor else ""
        rule.package = str(config.get("XXpackageXX", DEFAULT_PACKAGE))
        return rule

    @classmethod
    def xǁEngineVersionFloorǁfrom_config__mutmut_20(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EngineVersionFloor:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EngineVersionFloor)  # noqa: S101  # narrowing for mypy
        floor = config.get("floor")
        rule.floor = str(floor) if floor else ""
        rule.package = str(config.get("PACKAGE", DEFAULT_PACKAGE))
        return rule

    @_mutmut_mutated(mutants_xǁEngineVersionFloorǁ_installed_version__mutmut)
    def _installed_version(self) -> str | None:
        """The installed distribution's own version, or ``None`` when absent."""
        try:
            return _metadata.version(self.package)
        except _metadata.PackageNotFoundError:
            return None

    def xǁEngineVersionFloorǁ_installed_version__mutmut_orig(self) -> str | None:
        """The installed distribution's own version, or ``None`` when absent."""
        try:
            return _metadata.version(self.package)
        except _metadata.PackageNotFoundError:
            return None

    def xǁEngineVersionFloorǁ_installed_version__mutmut_1(self) -> str | None:
        """The installed distribution's own version, or ``None`` when absent."""
        try:
            return _metadata.version(None)
        except _metadata.PackageNotFoundError:
            return None

    @_mutmut_mutated(mutants_xǁEngineVersionFloorǁresolve_version__mutmut)
    def resolve_version(self) -> str | None:
        """The consumer's DECLARED pin, else the installed distribution version."""
        declared = resolve_declared_version(self._repo_root / _PYPROJECT, self.package)
        return declared if declared is not None else self._installed_version()

    def xǁEngineVersionFloorǁresolve_version__mutmut_orig(self) -> str | None:
        """The consumer's DECLARED pin, else the installed distribution version."""
        declared = resolve_declared_version(self._repo_root / _PYPROJECT, self.package)
        return declared if declared is not None else self._installed_version()

    def xǁEngineVersionFloorǁresolve_version__mutmut_1(self) -> str | None:
        """The consumer's DECLARED pin, else the installed distribution version."""
        declared = None
        return declared if declared is not None else self._installed_version()

    def xǁEngineVersionFloorǁresolve_version__mutmut_2(self) -> str | None:
        """The consumer's DECLARED pin, else the installed distribution version."""
        declared = resolve_declared_version(None, self.package)
        return declared if declared is not None else self._installed_version()

    def xǁEngineVersionFloorǁresolve_version__mutmut_3(self) -> str | None:
        """The consumer's DECLARED pin, else the installed distribution version."""
        declared = resolve_declared_version(self._repo_root / _PYPROJECT, None)
        return declared if declared is not None else self._installed_version()

    def xǁEngineVersionFloorǁresolve_version__mutmut_4(self) -> str | None:
        """The consumer's DECLARED pin, else the installed distribution version."""
        declared = resolve_declared_version(self.package)
        return declared if declared is not None else self._installed_version()

    def xǁEngineVersionFloorǁresolve_version__mutmut_5(self) -> str | None:
        """The consumer's DECLARED pin, else the installed distribution version."""
        declared = resolve_declared_version(self._repo_root / _PYPROJECT, )
        return declared if declared is not None else self._installed_version()

    def xǁEngineVersionFloorǁresolve_version__mutmut_6(self) -> str | None:
        """The consumer's DECLARED pin, else the installed distribution version."""
        declared = resolve_declared_version(self._repo_root * _PYPROJECT, self.package)
        return declared if declared is not None else self._installed_version()

    def xǁEngineVersionFloorǁresolve_version__mutmut_7(self) -> str | None:
        """The consumer's DECLARED pin, else the installed distribution version."""
        declared = resolve_declared_version(self._repo_root / _PYPROJECT, self.package)
        return declared if declared is None else self._installed_version()

    @_mutmut_mutated(mutants_xǁEngineVersionFloorǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        """Unused — the unit of violation is the version pin, not a file."""
        return False

    def xǁEngineVersionFloorǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        """Unused — the unit of violation is the version pin, not a file."""
        return False

    def xǁEngineVersionFloorǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        """Unused — the unit of violation is the version pin, not a file."""
        return True

    def enumerate_files(self) -> list[Path]:
        """No file surface — the pin lives in the manifest, not the tree."""
        return []

    @_mutmut_mutated(mutants_xǁEngineVersionFloorǁcollect_violations__mutmut)
    def collect_violations(self) -> set[Path]:
        """A single violation entry iff the resolved pin is below the floor.

        No floor configured, an unparseable floor, or an unresolvable pin are all
        guard-forward no-ops (empty set): a consumer is never hard-broken before
        it can determine and bump its own version.
        """
        if not self.floor:
            return set()
        floor = parse_version(self.floor)
        if floor is None:
            return set()
        resolved = self.resolve_version()
        if resolved is None:
            return set()
        pinned = parse_version(resolved)
        if pinned is None or pinned >= floor:
            return set()
        return {Path(f"{self.package} pinned {resolved} is below floor {self.floor}")}

    def xǁEngineVersionFloorǁcollect_violations__mutmut_orig(self) -> set[Path]:
        """A single violation entry iff the resolved pin is below the floor.

        No floor configured, an unparseable floor, or an unresolvable pin are all
        guard-forward no-ops (empty set): a consumer is never hard-broken before
        it can determine and bump its own version.
        """
        if not self.floor:
            return set()
        floor = parse_version(self.floor)
        if floor is None:
            return set()
        resolved = self.resolve_version()
        if resolved is None:
            return set()
        pinned = parse_version(resolved)
        if pinned is None or pinned >= floor:
            return set()
        return {Path(f"{self.package} pinned {resolved} is below floor {self.floor}")}

    def xǁEngineVersionFloorǁcollect_violations__mutmut_1(self) -> set[Path]:
        """A single violation entry iff the resolved pin is below the floor.

        No floor configured, an unparseable floor, or an unresolvable pin are all
        guard-forward no-ops (empty set): a consumer is never hard-broken before
        it can determine and bump its own version.
        """
        if self.floor:
            return set()
        floor = parse_version(self.floor)
        if floor is None:
            return set()
        resolved = self.resolve_version()
        if resolved is None:
            return set()
        pinned = parse_version(resolved)
        if pinned is None or pinned >= floor:
            return set()
        return {Path(f"{self.package} pinned {resolved} is below floor {self.floor}")}

    def xǁEngineVersionFloorǁcollect_violations__mutmut_2(self) -> set[Path]:
        """A single violation entry iff the resolved pin is below the floor.

        No floor configured, an unparseable floor, or an unresolvable pin are all
        guard-forward no-ops (empty set): a consumer is never hard-broken before
        it can determine and bump its own version.
        """
        if not self.floor:
            return set()
        floor = None
        if floor is None:
            return set()
        resolved = self.resolve_version()
        if resolved is None:
            return set()
        pinned = parse_version(resolved)
        if pinned is None or pinned >= floor:
            return set()
        return {Path(f"{self.package} pinned {resolved} is below floor {self.floor}")}

    def xǁEngineVersionFloorǁcollect_violations__mutmut_3(self) -> set[Path]:
        """A single violation entry iff the resolved pin is below the floor.

        No floor configured, an unparseable floor, or an unresolvable pin are all
        guard-forward no-ops (empty set): a consumer is never hard-broken before
        it can determine and bump its own version.
        """
        if not self.floor:
            return set()
        floor = parse_version(None)
        if floor is None:
            return set()
        resolved = self.resolve_version()
        if resolved is None:
            return set()
        pinned = parse_version(resolved)
        if pinned is None or pinned >= floor:
            return set()
        return {Path(f"{self.package} pinned {resolved} is below floor {self.floor}")}

    def xǁEngineVersionFloorǁcollect_violations__mutmut_4(self) -> set[Path]:
        """A single violation entry iff the resolved pin is below the floor.

        No floor configured, an unparseable floor, or an unresolvable pin are all
        guard-forward no-ops (empty set): a consumer is never hard-broken before
        it can determine and bump its own version.
        """
        if not self.floor:
            return set()
        floor = parse_version(self.floor)
        if floor is not None:
            return set()
        resolved = self.resolve_version()
        if resolved is None:
            return set()
        pinned = parse_version(resolved)
        if pinned is None or pinned >= floor:
            return set()
        return {Path(f"{self.package} pinned {resolved} is below floor {self.floor}")}

    def xǁEngineVersionFloorǁcollect_violations__mutmut_5(self) -> set[Path]:
        """A single violation entry iff the resolved pin is below the floor.

        No floor configured, an unparseable floor, or an unresolvable pin are all
        guard-forward no-ops (empty set): a consumer is never hard-broken before
        it can determine and bump its own version.
        """
        if not self.floor:
            return set()
        floor = parse_version(self.floor)
        if floor is None:
            return set()
        resolved = None
        if resolved is None:
            return set()
        pinned = parse_version(resolved)
        if pinned is None or pinned >= floor:
            return set()
        return {Path(f"{self.package} pinned {resolved} is below floor {self.floor}")}

    def xǁEngineVersionFloorǁcollect_violations__mutmut_6(self) -> set[Path]:
        """A single violation entry iff the resolved pin is below the floor.

        No floor configured, an unparseable floor, or an unresolvable pin are all
        guard-forward no-ops (empty set): a consumer is never hard-broken before
        it can determine and bump its own version.
        """
        if not self.floor:
            return set()
        floor = parse_version(self.floor)
        if floor is None:
            return set()
        resolved = self.resolve_version()
        if resolved is not None:
            return set()
        pinned = parse_version(resolved)
        if pinned is None or pinned >= floor:
            return set()
        return {Path(f"{self.package} pinned {resolved} is below floor {self.floor}")}

    def xǁEngineVersionFloorǁcollect_violations__mutmut_7(self) -> set[Path]:
        """A single violation entry iff the resolved pin is below the floor.

        No floor configured, an unparseable floor, or an unresolvable pin are all
        guard-forward no-ops (empty set): a consumer is never hard-broken before
        it can determine and bump its own version.
        """
        if not self.floor:
            return set()
        floor = parse_version(self.floor)
        if floor is None:
            return set()
        resolved = self.resolve_version()
        if resolved is None:
            return set()
        pinned = None
        if pinned is None or pinned >= floor:
            return set()
        return {Path(f"{self.package} pinned {resolved} is below floor {self.floor}")}

    def xǁEngineVersionFloorǁcollect_violations__mutmut_8(self) -> set[Path]:
        """A single violation entry iff the resolved pin is below the floor.

        No floor configured, an unparseable floor, or an unresolvable pin are all
        guard-forward no-ops (empty set): a consumer is never hard-broken before
        it can determine and bump its own version.
        """
        if not self.floor:
            return set()
        floor = parse_version(self.floor)
        if floor is None:
            return set()
        resolved = self.resolve_version()
        if resolved is None:
            return set()
        pinned = parse_version(None)
        if pinned is None or pinned >= floor:
            return set()
        return {Path(f"{self.package} pinned {resolved} is below floor {self.floor}")}

    def xǁEngineVersionFloorǁcollect_violations__mutmut_9(self) -> set[Path]:
        """A single violation entry iff the resolved pin is below the floor.

        No floor configured, an unparseable floor, or an unresolvable pin are all
        guard-forward no-ops (empty set): a consumer is never hard-broken before
        it can determine and bump its own version.
        """
        if not self.floor:
            return set()
        floor = parse_version(self.floor)
        if floor is None:
            return set()
        resolved = self.resolve_version()
        if resolved is None:
            return set()
        pinned = parse_version(resolved)
        if pinned is None and pinned >= floor:
            return set()
        return {Path(f"{self.package} pinned {resolved} is below floor {self.floor}")}

    def xǁEngineVersionFloorǁcollect_violations__mutmut_10(self) -> set[Path]:
        """A single violation entry iff the resolved pin is below the floor.

        No floor configured, an unparseable floor, or an unresolvable pin are all
        guard-forward no-ops (empty set): a consumer is never hard-broken before
        it can determine and bump its own version.
        """
        if not self.floor:
            return set()
        floor = parse_version(self.floor)
        if floor is None:
            return set()
        resolved = self.resolve_version()
        if resolved is None:
            return set()
        pinned = parse_version(resolved)
        if pinned is not None or pinned >= floor:
            return set()
        return {Path(f"{self.package} pinned {resolved} is below floor {self.floor}")}

    def xǁEngineVersionFloorǁcollect_violations__mutmut_11(self) -> set[Path]:
        """A single violation entry iff the resolved pin is below the floor.

        No floor configured, an unparseable floor, or an unresolvable pin are all
        guard-forward no-ops (empty set): a consumer is never hard-broken before
        it can determine and bump its own version.
        """
        if not self.floor:
            return set()
        floor = parse_version(self.floor)
        if floor is None:
            return set()
        resolved = self.resolve_version()
        if resolved is None:
            return set()
        pinned = parse_version(resolved)
        if pinned is None or pinned > floor:
            return set()
        return {Path(f"{self.package} pinned {resolved} is below floor {self.floor}")}

    def xǁEngineVersionFloorǁcollect_violations__mutmut_12(self) -> set[Path]:
        """A single violation entry iff the resolved pin is below the floor.

        No floor configured, an unparseable floor, or an unresolvable pin are all
        guard-forward no-ops (empty set): a consumer is never hard-broken before
        it can determine and bump its own version.
        """
        if not self.floor:
            return set()
        floor = parse_version(self.floor)
        if floor is None:
            return set()
        resolved = self.resolve_version()
        if resolved is None:
            return set()
        pinned = parse_version(resolved)
        if pinned is None or pinned >= floor:
            return set()
        return {Path(None)}

mutants_xǁEngineVersionFloorǁfrom_config__mutmut['_mutmut_orig'] = EngineVersionFloor.xǁEngineVersionFloorǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁfrom_config__mutmut['xǁEngineVersionFloorǁfrom_config__mutmut_1'] = EngineVersionFloor.xǁEngineVersionFloorǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁfrom_config__mutmut['xǁEngineVersionFloorǁfrom_config__mutmut_2'] = EngineVersionFloor.xǁEngineVersionFloorǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁfrom_config__mutmut['xǁEngineVersionFloorǁfrom_config__mutmut_3'] = EngineVersionFloor.xǁEngineVersionFloorǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁfrom_config__mutmut['xǁEngineVersionFloorǁfrom_config__mutmut_4'] = EngineVersionFloor.xǁEngineVersionFloorǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁfrom_config__mutmut['xǁEngineVersionFloorǁfrom_config__mutmut_5'] = EngineVersionFloor.xǁEngineVersionFloorǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁfrom_config__mutmut['xǁEngineVersionFloorǁfrom_config__mutmut_6'] = EngineVersionFloor.xǁEngineVersionFloorǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁfrom_config__mutmut['xǁEngineVersionFloorǁfrom_config__mutmut_7'] = EngineVersionFloor.xǁEngineVersionFloorǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁfrom_config__mutmut['xǁEngineVersionFloorǁfrom_config__mutmut_8'] = EngineVersionFloor.xǁEngineVersionFloorǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁfrom_config__mutmut['xǁEngineVersionFloorǁfrom_config__mutmut_9'] = EngineVersionFloor.xǁEngineVersionFloorǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁfrom_config__mutmut['xǁEngineVersionFloorǁfrom_config__mutmut_10'] = EngineVersionFloor.xǁEngineVersionFloorǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁfrom_config__mutmut['xǁEngineVersionFloorǁfrom_config__mutmut_11'] = EngineVersionFloor.xǁEngineVersionFloorǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁfrom_config__mutmut['xǁEngineVersionFloorǁfrom_config__mutmut_12'] = EngineVersionFloor.xǁEngineVersionFloorǁfrom_config__mutmut_12 # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁfrom_config__mutmut['xǁEngineVersionFloorǁfrom_config__mutmut_13'] = EngineVersionFloor.xǁEngineVersionFloorǁfrom_config__mutmut_13 # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁfrom_config__mutmut['xǁEngineVersionFloorǁfrom_config__mutmut_14'] = EngineVersionFloor.xǁEngineVersionFloorǁfrom_config__mutmut_14 # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁfrom_config__mutmut['xǁEngineVersionFloorǁfrom_config__mutmut_15'] = EngineVersionFloor.xǁEngineVersionFloorǁfrom_config__mutmut_15 # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁfrom_config__mutmut['xǁEngineVersionFloorǁfrom_config__mutmut_16'] = EngineVersionFloor.xǁEngineVersionFloorǁfrom_config__mutmut_16 # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁfrom_config__mutmut['xǁEngineVersionFloorǁfrom_config__mutmut_17'] = EngineVersionFloor.xǁEngineVersionFloorǁfrom_config__mutmut_17 # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁfrom_config__mutmut['xǁEngineVersionFloorǁfrom_config__mutmut_18'] = EngineVersionFloor.xǁEngineVersionFloorǁfrom_config__mutmut_18 # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁfrom_config__mutmut['xǁEngineVersionFloorǁfrom_config__mutmut_19'] = EngineVersionFloor.xǁEngineVersionFloorǁfrom_config__mutmut_19 # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁfrom_config__mutmut['xǁEngineVersionFloorǁfrom_config__mutmut_20'] = EngineVersionFloor.xǁEngineVersionFloorǁfrom_config__mutmut_20 # type: ignore # mutmut generated

mutants_xǁEngineVersionFloorǁ_installed_version__mutmut['_mutmut_orig'] = EngineVersionFloor.xǁEngineVersionFloorǁ_installed_version__mutmut_orig # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁ_installed_version__mutmut['xǁEngineVersionFloorǁ_installed_version__mutmut_1'] = EngineVersionFloor.xǁEngineVersionFloorǁ_installed_version__mutmut_1 # type: ignore # mutmut generated

mutants_xǁEngineVersionFloorǁresolve_version__mutmut['_mutmut_orig'] = EngineVersionFloor.xǁEngineVersionFloorǁresolve_version__mutmut_orig # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁresolve_version__mutmut['xǁEngineVersionFloorǁresolve_version__mutmut_1'] = EngineVersionFloor.xǁEngineVersionFloorǁresolve_version__mutmut_1 # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁresolve_version__mutmut['xǁEngineVersionFloorǁresolve_version__mutmut_2'] = EngineVersionFloor.xǁEngineVersionFloorǁresolve_version__mutmut_2 # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁresolve_version__mutmut['xǁEngineVersionFloorǁresolve_version__mutmut_3'] = EngineVersionFloor.xǁEngineVersionFloorǁresolve_version__mutmut_3 # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁresolve_version__mutmut['xǁEngineVersionFloorǁresolve_version__mutmut_4'] = EngineVersionFloor.xǁEngineVersionFloorǁresolve_version__mutmut_4 # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁresolve_version__mutmut['xǁEngineVersionFloorǁresolve_version__mutmut_5'] = EngineVersionFloor.xǁEngineVersionFloorǁresolve_version__mutmut_5 # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁresolve_version__mutmut['xǁEngineVersionFloorǁresolve_version__mutmut_6'] = EngineVersionFloor.xǁEngineVersionFloorǁresolve_version__mutmut_6 # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁresolve_version__mutmut['xǁEngineVersionFloorǁresolve_version__mutmut_7'] = EngineVersionFloor.xǁEngineVersionFloorǁresolve_version__mutmut_7 # type: ignore # mutmut generated

mutants_xǁEngineVersionFloorǁfile_has_violation__mutmut['_mutmut_orig'] = EngineVersionFloor.xǁEngineVersionFloorǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁfile_has_violation__mutmut['xǁEngineVersionFloorǁfile_has_violation__mutmut_1'] = EngineVersionFloor.xǁEngineVersionFloorǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated

mutants_xǁEngineVersionFloorǁcollect_violations__mutmut['_mutmut_orig'] = EngineVersionFloor.xǁEngineVersionFloorǁcollect_violations__mutmut_orig # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁcollect_violations__mutmut['xǁEngineVersionFloorǁcollect_violations__mutmut_1'] = EngineVersionFloor.xǁEngineVersionFloorǁcollect_violations__mutmut_1 # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁcollect_violations__mutmut['xǁEngineVersionFloorǁcollect_violations__mutmut_2'] = EngineVersionFloor.xǁEngineVersionFloorǁcollect_violations__mutmut_2 # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁcollect_violations__mutmut['xǁEngineVersionFloorǁcollect_violations__mutmut_3'] = EngineVersionFloor.xǁEngineVersionFloorǁcollect_violations__mutmut_3 # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁcollect_violations__mutmut['xǁEngineVersionFloorǁcollect_violations__mutmut_4'] = EngineVersionFloor.xǁEngineVersionFloorǁcollect_violations__mutmut_4 # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁcollect_violations__mutmut['xǁEngineVersionFloorǁcollect_violations__mutmut_5'] = EngineVersionFloor.xǁEngineVersionFloorǁcollect_violations__mutmut_5 # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁcollect_violations__mutmut['xǁEngineVersionFloorǁcollect_violations__mutmut_6'] = EngineVersionFloor.xǁEngineVersionFloorǁcollect_violations__mutmut_6 # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁcollect_violations__mutmut['xǁEngineVersionFloorǁcollect_violations__mutmut_7'] = EngineVersionFloor.xǁEngineVersionFloorǁcollect_violations__mutmut_7 # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁcollect_violations__mutmut['xǁEngineVersionFloorǁcollect_violations__mutmut_8'] = EngineVersionFloor.xǁEngineVersionFloorǁcollect_violations__mutmut_8 # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁcollect_violations__mutmut['xǁEngineVersionFloorǁcollect_violations__mutmut_9'] = EngineVersionFloor.xǁEngineVersionFloorǁcollect_violations__mutmut_9 # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁcollect_violations__mutmut['xǁEngineVersionFloorǁcollect_violations__mutmut_10'] = EngineVersionFloor.xǁEngineVersionFloorǁcollect_violations__mutmut_10 # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁcollect_violations__mutmut['xǁEngineVersionFloorǁcollect_violations__mutmut_11'] = EngineVersionFloor.xǁEngineVersionFloorǁcollect_violations__mutmut_11 # type: ignore # mutmut generated
mutants_xǁEngineVersionFloorǁcollect_violations__mutmut['xǁEngineVersionFloorǁcollect_violations__mutmut_12'] = EngineVersionFloor.xǁEngineVersionFloorǁcollect_violations__mutmut_12 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> EngineVersionFloor:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return EngineVersionFloor.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> EngineVersionFloor:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return EngineVersionFloor.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> EngineVersionFloor:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return EngineVersionFloor.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> EngineVersionFloor:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return EngineVersionFloor.from_config(config, repo_root=None)


def x_build__mutmut_3(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> EngineVersionFloor:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return EngineVersionFloor.from_config(repo_root=repo_root)


def x_build__mutmut_4(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> EngineVersionFloor:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return EngineVersionFloor.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(EngineVersionFloor, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(EngineVersionFloor, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(EngineVersionFloor, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(EngineVersionFloor, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
