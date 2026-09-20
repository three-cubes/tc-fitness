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

#: Everything after an unquoted `#` that starts a comment. A `#` only opens a
#: comment at the start of a word: `${value#prefix}` and `x#y` are shell
#: parameter expansion and an ordinary word, not documentation.
_TRAILING_COMMENT_RE = re.compile(r"""(?:[^"'#]|"[^"]*"|'[^']*'|(?<=[^\s])#)*""")
#: A shell interpreter named on a shebang line, for files carrying no suffix.
_SHELL_SHEBANG_RE = re.compile(r"^#!.*\b(?:ba|da|k|z)?sh\b")


def declared_pin(requirement: str) -> tuple[str, str] | None:
    """Return ``(canonical name, pinned version)`` for an exact pin, else None.

    Parsed rather than pattern-matched. The grammars involved are PEP 508 for
    the requirement, PEP 440 for the version and PEP 503 for the name, and a
    regex over them is wrong in both directions: it misses the parenthesised
    ``foo (==1.2.3)`` and the ``v``-prefixed ``foo==v1.2.3``, while reading the
    prefix match ``foo==1.2.*`` as exact and finding a pin in a direct
    reference such as ``foo @ https://host/foo.whl?build==1.2.3``.

    Only ``==`` without a wildcard is a pin. ``===`` is arbitrary-equality on an
    unparseable version and is left alone, and a requirement carrying an
    environment marker is still a pin -- which one applies is the caller's
    problem, not this parser's.
    """
    from packaging.requirements import InvalidRequirement, Requirement
    from packaging.utils import canonicalize_name

    try:
        parsed = Requirement(requirement)
    except InvalidRequirement:
        return None
    exact = [
        specifier.version
        for specifier in parsed.specifier
        if specifier.operator == "==" and not specifier.version.endswith(".*")
    ]
    if len(exact) != 1:
        return None
    return canonicalize_name(parsed.name), exact[0]


def version_spellings(version: str) -> set[str]:
    """Return every spelling a source literal could use for one declared version.

    PEP 440 admits spellings that normalise to the same release -- ``v1.2.3``
    and ``1.2.3`` among them -- so a literal restating the pin need not match
    the manifest's own characters. Both forms are matched; an unparseable
    version is matched literally rather than dropped.
    """
    from packaging.version import InvalidVersion, Version

    spellings = {version}
    try:
        spellings.add(str(Version(version)))
    except InvalidVersion:
        pass
    return spellings


REMEDIATION = _remediation(
    fix=(
        "replace the literal with the pin read back from the manifest, so a bump "
        "is edited in one place and enforcement is kept. Which reader applies "
        "depends on where the pin is declared, not on taste. A pin in [project] "
        "dependencies or optional-dependencies becomes the installed "
        "distribution's Requires-Dist metadata, so call "
        "tc_fitness.lib.pinned_version(<distribution>, <package>): it returns the "
        "declared version and raises a named error when the package is absent or "
        "not pinned exactly. A pin in [dependency-groups], [build-system] "
        "requires, or [tool.uv] override-dependencies/constraint-dependencies is "
        "NOT published as that metadata, so pinned_version cannot serve it and "
        "will report that the distribution does not require the package; read the "
        "manifest instead — tomllib.load(<repo>/pyproject.toml) and take the `==` "
        "version from the table that declares it. The same manifest read applies "
        "anywhere the distribution cannot be imported, such as a qualification "
        "script running against an environment synced --no-install-project. A "
        "literal that merely coincides with a pin is raised past by "
        "min_version_parts, which sets how specific a version must be before it "
        "counts; a finding is never suppressed per file."
    ),
    nxt="re-run this check to confirm it goes green.",
    # The module entry point builds an unconfigured rule, whose empty scan
    # roots enumerate nothing and report clean while the offender stands.
    # Re-running through the catalogue is the only command that repeats the
    # check the consumer actually configured.
    run="uv run tc-fitness run",
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
    # `dev-dependencies` is uv's older spelling of a development group. uv still
    # accepts and resolves it, so a pin declared there binds exactly as hard as
    # one in `[dependency-groups]`.
    for key in ("override-dependencies", "constraint-dependencies", "dev-dependencies"):
        requirements.extend(r for r in (uv.get(key, []) or []) if isinstance(r, str))

    pins: dict[str, list[str]] = {}
    for requirement in requirements:
        parsed = declared_pin(requirement)
        if parsed is None:
            continue
        package, version = parsed
        if version.count(".") + 1 < min_parts:
            continue
        for spelling in version_spellings(version):
            pins.setdefault(spelling, []).append(package)
    return {version: sorted(set(names)) for version, names in pins.items()}


def _continues_a_version(character: str) -> bool:
    """True when a neighbouring character makes the match part of a longer version.

    PEP 440 versions carry more than digits and dots: ``1.2.3rc1``,
    ``1.2.3.post1``, ``1.2.3+local.1`` and the epoch form ``1!2.3`` all extend a
    shorter version that would otherwise appear to be restated inside them. Any
    character a version can contain therefore continues one; the start and end
    of a line are boundaries, so an absent neighbour must not be tested for
    membership -- "" is a substring of every string.
    """
    return character != "" and (character.isalnum() or character in ".+!_-")


def _code_before_comment(line: str) -> str:
    """Return the executable part of a line, dropping any trailing comment."""
    match = _TRAILING_COMMENT_RE.match(line)
    return match.group(0) if match else line


def restated_pins(text: str, pins: Mapping[str, list[str]]) -> list[tuple[int, str]]:
    """Return ``(line number, version)`` for each literal restating a pin.

    Matching is against the declared versions themselves rather than against a
    version-shaped pattern. A pattern has to guess what a version looks like,
    and PEP 440 admits more than dotted digits — `1.2.3rc1`, `1.2.3.post1` and
    local versions would all be missed. It also has to guess how the literal is
    written, and a shell binding is `TOOL_VERSION=3.6.0` with no quotes at all.
    Comparing against the manifest's own strings needs neither guess.

    Comments are skipped, wherever on the line they start: prose naming a
    version documents it rather than binding behaviour to it.
    """
    candidates = sorted(pins, key=len, reverse=True)
    found: list[tuple[int, str]] = []
    for number, line in enumerate(text.splitlines(), 1):
        code = _code_before_comment(line)
        if not code.strip():
            continue
        for version in candidates:
            for match in re.finditer(re.escape(version), code):
                # A version is restated only as a whole token. Without this,
                # "1.2.3" also matches inside "1.2.30" and inside a path. The
                # start and end of the line are boundaries, so an absent
                # neighbour must not be tested for membership — "" is a
                # substring of every string.
                before = code[match.start() - 1 : match.start()]
                after = code[match.end() : match.end() + 1]
                if _continues_a_version(before) or _continues_a_version(after):
                    continue
                found.append((number, version))
                break
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

    def is_in_scope(self, rel: str) -> bool:
        """Admit suffixed sources, and extensionless files a shell will run.

        A shell entrypoint is commonly written without a suffix -- `scripts/`
        and `bin/` are full of them -- and the inherited predicate filters on
        suffix before anything reads the file. Scoping the rule to shell while
        skipping every extensionless shell script would leave the pattern alive
        in the scripts that enforce versions hardest.
        """
        if super().is_in_scope(rel):
            return True
        if Path(rel).suffix:
            return False
        if self._roots and not any(rel.startswith(prefix) for prefix in self._roots):
            return False
        return self._runs_under_a_shell(self._repo_root / rel)

    @staticmethod
    def _runs_under_a_shell(path: Path) -> bool:
        """True when the file's shebang names a shell interpreter."""
        try:
            with path.open("r", encoding="utf-8", errors="replace") as handle:
                first = handle.readline()
        except OSError:
            return False
        return bool(_SHELL_SHEBANG_RE.match(first))

    def enumerate_files(self) -> list[Path]:
        """Enumerate suffixed sources plus the extensionless shell entrypoints."""
        found = {path.resolve(): path for path in super().enumerate_files()}
        for root in self._roots or ("",):
            base = self._repo_root / root
            if not base.is_dir():
                continue
            for path in base.rglob("*"):
                if path.suffix or not path.is_file() or path.is_symlink():
                    continue
                if any(part.startswith(".") for part in path.relative_to(self._repo_root).parts):
                    continue
                if path.resolve() not in found and self._runs_under_a_shell(path):
                    found[path.resolve()] = path
        return sorted(found.values())

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
