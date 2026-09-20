"""CORE check: no_duplicated_dependency_pin — source must not restate a declared pin.

A project that pins a dependency exactly (``tool==1.2.3``) already has one
source of truth for that version: its manifest, and the lockfile resolved from
it. Restating the same version as a literal in source creates a second one that
no dependency tooling updates. The bump then lands in the manifest and the lock
while the literal stays behind, and the mismatch surfaces at runtime — usually
in CI, on an unrelated change, with an error that names the tool rather than the
stale constant.

The pattern is most damaging where the literal is *enforced*, because the code
fails closed against a version the project no longer installs, and an automated
dependency PR cannot go green without a human editing source in lockstep.

The rule is narrow on purpose: it flags a literal only when it equals the
version of an exact pin the project itself declares. A version string that
matches nothing the project pins is not this rule's business.

Read the pin back instead of restating it. Inside the distribution::

    from tc_fitness.lib import pinned_version

    TOOL_VERSION = pinned_version("three-cubes-fitness", "mutmut")

Outside it — a qualification script running against an environment synced
``--no-install-project`` cannot import the distribution — read the manifest
under test::

    import tomllib
    manifest = tomllib.loads((repo_root / "pyproject.toml").read_text())

Either way the enforcement is unchanged and the manifest stays the only place a
bump is edited.
"""

from __future__ import annotations

import re
import tomllib
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: The manifest declaring the project's dependencies, repo-relative.
DEFAULT_MANIFEST = "pyproject.toml"
#: Minimum dot-separated components a pin must have before a matching literal
#: counts. Two-component versions ("1.0", "2.0") collide with ordinary numeric
#: strings often enough that flagging them costs more than it catches.
DEFAULT_MIN_VERSION_PARTS = 3
#: File kinds a restated pin binds behaviour in. Shell belongs here as much as
#: Python: a qualification script asserting an installed version is the same
#: second source of truth, and scoping the rule to .py alone would let the
#: pattern live on in exactly the scripts that enforce it hardest.
DEFAULT_EXTENSIONS = (".py", ".sh", ".bash")

_EXACT_PIN_RE = re.compile(r"^\s*([A-Za-z0-9._-]+)\s*==\s*([0-9][^;\s,\]]*)")
_STRING_LITERAL_RE = re.compile(r"[\"']([0-9]+(?:\.[0-9]+)+)[\"']")

REMEDIATION = _remediation(
    fix=(
        "replace the literal with the pin read back from the manifest. Inside the "
        "distribution, call tc_fitness.lib.pinned_version(<distribution>, <package>) "
        "— it returns the declared `package==<version>` and raises a named error "
        "when the package is absent or not exactly pinned, so enforcement is kept "
        "and the manifest stays the only place a bump is edited. Outside it (a "
        "qualification script against an environment synced --no-install-project "
        "cannot import the distribution) read the manifest under test instead: "
        "tomllib.load(<repo>/pyproject.toml) and take the `==` version. Where the "
        "literal is genuinely unrelated to the pin it happens to match, add the "
        "file to exempt_files."
    ),
    nxt="re-run this check to confirm it goes green.",
    run="python -m tc_fitness.core_checks.no_duplicated_dependency_pin",
    passing='TOOL_VERSION = pinned_version("three-cubes-fitness", "mutmut")',
    forbidden='TOOL_VERSION = "3.6.0"   (manifest already declares mutmut==3.6.0)',
)


def declared_exact_pins(
    manifest: Path, *, min_parts: int = DEFAULT_MIN_VERSION_PARTS
) -> dict[str, list[str]]:
    """Map each exactly-pinned version to the packages pinned at it.

    Reads every table that can carry an exact version: ``[project]
    dependencies``, each ``optional-dependencies`` group, each PEP 735
    ``dependency-groups`` entry, ``[build-system] requires``, and uv's
    ``override-dependencies`` / ``constraint-dependencies``. A pin is a pin
    wherever it is declared — an override in particular is often where a
    transitive version gets fixed, and reading only ``[project]`` would miss it
    while the source restating it looked clean.

    A missing or unparseable manifest yields no pins, which makes the rule
    vacuous rather than noisy — the check cannot tell a consumer that declares
    nothing from one it cannot read, and failing on the latter would punish the
    wrong repositories.
    """
    try:
        data = tomllib.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError):
        return {}

    project = data.get("project", {}) or {}
    requirements: list[str] = [r for r in (project.get("dependencies", []) or []) if isinstance(r, str)]
    for group in (project.get("optional-dependencies", {}) or {}).values():
        requirements.extend(r for r in group if isinstance(r, str))
    for group in (data.get("dependency-groups", {}) or {}).values():
        requirements.extend(r for r in group if isinstance(r, str))
    requirements.extend(
        r for r in (data.get("build-system", {}) or {}).get("requires", []) or [] if isinstance(r, str)
    )
    uv = (data.get("tool", {}) or {}).get("uv", {}) or {}
    for key in ("override-dependencies", "constraint-dependencies"):
        requirements.extend(r for r in (uv.get(key, []) or []) if isinstance(r, str))

    pins: dict[str, list[str]] = {}
    for requirement in requirements:
        match = _EXACT_PIN_RE.match(requirement)
        if not match:
            continue
        package, version = match.group(1), match.group(2)
        if version.count(".") + 1 < min_parts:
            continue
        pins.setdefault(version, []).append(package)
    return {version: sorted(set(names)) for version, names in pins.items()}


def restated_pins(text: str, pins: Mapping[str, list[str]]) -> list[tuple[int, str]]:
    """Return ``(line number, version)`` for each literal restating a pin.

    Whole-line comments are skipped: prose naming a version documents it rather
    than binding behaviour to it.
    """
    found: list[tuple[int, str]] = []
    for number, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("#"):
            continue
        for literal in _STRING_LITERAL_RE.findall(line):
            if literal in pins:
                found.append((number, literal))
    return found


class NoDuplicatedDependencyPin(FitnessRule):
    """Flags a source literal that restates a version the manifest already pins."""

    name = "no-duplicated-dependency-pin"
    remediation = REMEDIATION
    extensions = DEFAULT_EXTENSIONS

    #: Rule-specific config (instance attrs; from_config overrides per consumer).
    manifest: str = DEFAULT_MANIFEST
    min_version_parts: int = DEFAULT_MIN_VERSION_PARTS

    @classmethod
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoDuplicatedDependencyPin:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoDuplicatedDependencyPin)  # noqa: S101  # narrowing for mypy
        rule.manifest = str(config.get("manifest", DEFAULT_MANIFEST))
        rule.min_version_parts = int(config.get("min_version_parts", DEFAULT_MIN_VERSION_PARTS))
        return rule

    def _pins(self) -> dict[str, list[str]]:
        return declared_exact_pins(
            self._repo_root / self.manifest,
            min_parts=self.min_version_parts,
        )

    def file_has_violation(self, path: Path) -> bool:
        """True when ``path`` restates a version the manifest pins exactly."""
        pins = self._pins()
        if not pins:
            return False
        if path.resolve() == (self._repo_root / self.manifest).resolve():
            return False
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return False
        return bool(restated_pins(text, pins))


def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoDuplicatedDependencyPin:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoDuplicatedDependencyPin.from_config(config, repo_root=repo_root)


def main(argv: list[str] | None = None) -> int:
    """CLI entry for the standalone invocation."""
    return run_core_check(NoDuplicatedDependencyPin, argv)


if __name__ == "__main__":
    import sys

    sys.exit(main())
