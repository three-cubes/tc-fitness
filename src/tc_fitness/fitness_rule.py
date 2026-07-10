"""FitnessRule ABC — the repo-agnostic, config-driven base for a CORE check.

Promoted from kairix's ``scripts/checks/_fitness_rule.py`` (ADR-026 Track B)
into the shared engine and made REPO-AGNOSTIC: every repo-specific knob
(scan roots, file extensions, exempt paths, baseline name) is a class
attribute or constructor argument the CONSUMER supplies — the engine bakes in
no ``kairix`` / ``taz`` identity. A concrete CORE check is a small subclass:

.. code-block:: python

    class NoDuplicateString(FitnessRule):
        name = "no-duplicate-string"          # → baseline filename root
        remediation = REMEDIATION
        # roots / extensions / exempt_files come from CONFIG (see below)

        def file_has_violation(self, path: Path) -> bool:
            ...

The base class inherits everything that does NOT vary per rule: loading the
per-file baseline (:mod:`tc_fitness.baseline`), enumerating in-scope files,
applying the scope predicate, gating on NET-NEW violations vs the baseline
(:func:`tc_fitness.gate`), and the ``--establish-baseline`` adoption mode.

Config injection
----------------
A CORE check module ships a subclass whose *behavioural* attributes default to
empty / repo-neutral values, then a consumer binds it from its
``[tool.tc_fitness]`` catalogue entry by passing config to
:meth:`from_config`. The two surfaces:

* **Class attributes** — a CORE check sets ``name`` + ``remediation`` (the
  parts intrinsic to the rule) and leaves ``roots`` / ``extensions`` /
  ``exempt_files`` at their repo-neutral defaults.
* **``from_config(config, repo_root=...)``** — overrides ``roots`` /
  ``extensions`` / ``exempt_files`` / ``name`` from the consumer's config dict
  (sourced from its catalogue entry), returning a ready-to-run instance.

The low-level functional helpers (:func:`tc_fitness.gate`,
:func:`tc_fitness.python_files`) remain canonical; this ABC collapses the
boilerplate around them. Checks needing custom enumeration override
:meth:`enumerate_files`; checks with a non-path scope override
:meth:`is_in_scope`.
"""

from __future__ import annotations

import subprocess
from abc import ABC, abstractmethod
from collections.abc import Mapping
from pathlib import Path
from typing import Any, ClassVar

from tc_fitness.baseline import establish_baseline, load_baseline
from tc_fitness.lib import REPO_ROOT, gate

#: Wall-clock ceiling for the ``git ls-files`` enumeration subprocess. A tracked
#: listing on any real tree returns in well under a second; the bound only guards
#: against a wedged git process, after which enumeration falls back to a walk.
_GIT_LS_FILES_TIMEOUT_S = 30


class FitnessRule(ABC):
    """A repo-agnostic, config-driven fitness rule.

    Class attributes (required on a concrete subclass):
        name: canonical check name → baseline filename
            (``.architecture/baseline/<name>-files.txt``). May be overridden
            per-consumer via :meth:`from_config`.
        remediation: the ``fix:`` / ``next:`` / ``run:`` remediation block
            (build it with :func:`tc_fitness.remediation`).

    Class attributes (config — repo-neutral defaults, overridden per consumer):
        roots: repo-relative directories to scan. Default ``()`` — a CORE
            check ships NO repo paths; the consumer supplies them via config.
        extensions: filename extensions in scope. Default ``(".py",)``.
        exempt_files: repo-relative paths to skip. Default empty.

    Concrete method (required):
        :meth:`file_has_violation`: truthy when the file violates the rule.

    Optional overrides:
        :meth:`is_in_scope` — customise the scope predicate.
        :meth:`enumerate_files` — customise file enumeration.
    """

    name: ClassVar[str]
    remediation: ClassVar[str]
    # Repo-NEUTRAL defaults: a CORE check ships no repo paths. The consumer's
    # catalogue entry supplies roots/exempt_files via from_config().
    roots: ClassVar[tuple[str, ...]] = ()
    extensions: ClassVar[tuple[str, ...]] = (".py",)
    exempt_files: ClassVar[frozenset[str]] = frozenset()

    def __init__(
        self,
        repo_root: Path | None = None,
        *,
        roots: tuple[str, ...] | None = None,
        extensions: tuple[str, ...] | None = None,
        exempt_files: frozenset[str] | None = None,
        name: str | None = None,
    ) -> None:
        """Construct a rule instance, overriding class-level config per call.

        ``repo_root`` overrides the default :data:`tc_fitness.REPO_ROOT` (tests
        pass a ``tmp_path`` for isolation). The keyword config overrides
        (``roots`` / ``extensions`` / ``exempt_files`` / ``name``) let a
        consumer bind the shared CORE check to its own paths without
        subclassing; ``None`` keeps the class attribute.
        """
        # Resolve the root so symlinked roots (e.g. macOS /tmp → /private/tmp)
        # match the resolved enumerated paths in _repo_relative; an unresolved
        # root would make relative_to() raise and silently fall back to the
        # absolute path, which then fails every is_in_scope() prefix test.
        raw_root = repo_root if repo_root is not None else REPO_ROOT
        self._repo_root: Path = raw_root.resolve()
        self._roots: tuple[str, ...] = roots if roots is not None else self.roots
        self._extensions: tuple[str, ...] = extensions if extensions is not None else self.extensions
        self._exempt_files: frozenset[str] = exempt_files if exempt_files is not None else self.exempt_files
        self._name: str = name if name is not None else self.name

    @classmethod
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> FitnessRule:
        """Build an instance from a consumer's ``[tool.tc_fitness]`` config dict.

        Recognised keys (all optional — each falls back to the class attribute):

        * ``roots`` — list of repo-relative scan-root prefixes.
        * ``extensions`` — list of in-scope filename extensions.
        * ``exempt_files`` — list of repo-relative paths to skip.
        * ``name`` — override the canonical check / baseline name.

        Unknown keys are ignored (a consumer may carry rule-specific knobs the
        subclass reads itself). Repo-agnostic: the engine never inspects the
        VALUES for repo identity.
        """
        roots = config.get("roots")
        extensions = config.get("extensions")
        exempt = config.get("exempt_files")
        return cls(
            repo_root=repo_root,
            roots=tuple(roots) if roots is not None else None,
            extensions=tuple(extensions) if extensions is not None else None,
            exempt_files=frozenset(exempt) if exempt is not None else None,
            name=config.get("name"),
        )

    @abstractmethod
    def file_has_violation(self, path: Path) -> bool:
        """Return True when the file at ``path`` violates this rule."""

    def is_in_scope(self, rel: str) -> bool:
        """Default scope predicate: under a configured root AND a matching ext.

        When ``roots`` is empty the predicate matches on extension alone, so a
        consumer that drives enumeration entirely from config still scopes
        correctly. Override for non-path scopes (single-file scans, ``.feature``
        files).
        """
        ext_ok = rel.endswith(self._extensions)
        if not self._roots:
            return ext_ok
        return ext_ok and any(rel.startswith(prefix) for prefix in self._roots)

    def enumerate_files(self) -> list[Path]:
        """Default enumeration: the git-tracked, in-scope files under the repo root.

        Empty ``roots`` enumerate NOTHING by default: with no configured scan
        root the default enumeration yields ``[]``, so a check run against the
        class-default config (``_roots == ()``) scans no files. A check that
        means to scan by extension alone must configure a root (e.g. ``roots``
        with an empty-prefix entry, which :meth:`is_in_scope` matches on every
        path) or override :meth:`enumerate_files`. The ``is_in_scope``
        "empty roots match on extension alone" rule is the scope PREDICATE, not
        the default enumeration.

        With a configured root, enumerates from ``git ls-files`` — exactly the
        set a fresh checkout materialises — so untracked and ``.gitignore``-d
        build/vendor residue (pnpm ``node_modules/.ignored`` trash, vendored test
        fixtures) is never scanned. This keeps a local run's verdict identical to
        CI's, which only ever sees tracked files. Returns absolute paths, filtered
        by :meth:`is_in_scope`.

        Fallback: when the repo root is not a git working tree (e.g. an unpacked
        source tarball) or ``git`` is unavailable, :meth:`_walk_working_tree`
        rglob-walks the configured roots, skipping ``__pycache__`` and any
        ``node_modules`` segment so vendor residue cannot trip a non-git scan
        either.

        Override for custom enumeration (Gherkin parsing, single-file scans).
        """
        if not self._roots:
            return []
        tracked = self._git_tracked_files()
        if tracked is not None:
            return [self._repo_root / rel for rel in tracked if self.is_in_scope(rel)]
        return self._walk_working_tree()

    def _git_tracked_files(self) -> list[str] | None:
        """Repo-relative paths of every git-tracked file, or ``None`` off-git.

        Runs ``git -C <repo_root> ls-files -z`` and returns the NUL-split,
        repo-relative tracked paths. Returns ``None`` — the signal to fall back
        to a working-tree walk — when the repo root is not a git working tree
        (``git`` exits non-zero) or ``git`` is unavailable / wedged. argv0 is the
        fixed literal ``git`` and ``shell`` is never used; the only variable is
        the repo-root path.
        """
        try:
            result = subprocess.run(
                ["git", "-C", str(self._repo_root), "ls-files", "-z"],
                check=True,
                capture_output=True,
                timeout=_GIT_LS_FILES_TIMEOUT_S,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return None
        return [rel.decode("utf-8", "surrogateescape") for rel in result.stdout.split(b"\x00") if rel]

    def _walk_working_tree(self) -> list[Path]:
        """Off-git fallback: rglob each configured root, skipping vendor residue.

        Skips ``__pycache__`` and any ``node_modules`` segment so untracked
        vendor residue cannot trip a scan that has no git tree to filter by.
        Returns absolute paths.
        """
        out: list[Path] = []
        for root in self._roots:
            root_path = self._repo_root / root
            if not root_path.exists():
                continue
            for path in root_path.rglob("*"):
                if not path.is_file():
                    continue
                if "__pycache__" in path.parts or "node_modules" in path.parts:
                    continue
                if path.name.endswith(self._extensions):
                    out.append(path)
        return out

    def _repo_relative(self, path: Path) -> Path:
        """Repo-relative path; tolerates absolute or already-relative inputs."""
        if path.is_absolute():
            try:
                return path.resolve().relative_to(self._repo_root)
            except ValueError:
                pass
        return path

    def collect_violations(self) -> set[Path]:
        """Walk in-scope files; return the repo-relative paths that violate.

        Exempt files (and out-of-scope files) are skipped. The set this returns
        is what both :meth:`run` (gate vs baseline) and
        :meth:`establish_baseline` (freeze as the new baseline) consume.
        """
        out: set[Path] = set()
        for path in self.enumerate_files():
            rel_path = self._repo_relative(path)
            rel = str(rel_path)
            if rel in self._exempt_files:
                continue
            if not self.is_in_scope(rel):
                continue
            if self.file_has_violation(path):
                out.add(rel_path)
        return out

    def run(self) -> int:
        """Gate the current violation set against the baseline; return exit code.

        ``0`` when no net-new violations (baseline offenders are grandfathered);
        ``1`` when a net-new violation is introduced. Delegates to
        :func:`tc_fitness.gate`, which reads
        ``.architecture/baseline/<name>-files.txt``.
        """
        return gate(
            self._name,
            self.collect_violations(),
            self.remediation,
            repo_root=self._repo_root,
        )

    def establish_baseline(self) -> Path:
        """``--establish-baseline`` mode: freeze today's offenders as baseline.

        Writes the current violation set to
        ``.architecture/baseline/<name>-files.txt`` (with the mandatory leading
        comment block), so a consumer adopting this rule never breaks the build
        on pre-existing offenders. Returns the path written.
        """
        violations = {str(p) for p in self.collect_violations()}
        return establish_baseline(self._name, violations, self._repo_root)

    def load_baseline(self) -> set[str]:
        """The grandfathered entry set for this rule (empty if none yet)."""
        return load_baseline(self._name, self._repo_root)


__all__ = ["FitnessRule"]
