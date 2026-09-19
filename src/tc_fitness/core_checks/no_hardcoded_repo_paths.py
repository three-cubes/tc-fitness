"""CORE check: no_hardcoded_repo_paths — no absolute checkout path baked in code.

A literal absolute checkout path (the directory a repo is cloned to on a build
host or VM) hardcoded in source or config breaks the moment the code runs
anywhere else: a different developer's machine, a container, a renamed host. The
sanctioned forms are a path resolved relative to the script
(``Path(__file__).resolve().parents[N]``) or an environment variable.

This rule flags any in-scope text file containing a configured NEEDLE substring
(the absolute path prefix the consumer wants banned). Markdown and other doc
extensions are exempt by default — they describe paths, they don't execute them.

Ported from tc-agent-zone ``scripts/checks/no_hardcoded_repo_paths.py`` and
re-expressed as a configurable, repo-agnostic rule: the banned NEEDLE, the scan
roots, the exempt extensions and the exempt prefixes ALL arrive from the
consumer's ``[tool.tc_fitness]`` config. The donor hardcoded its own
``/data/development/<repo>/`` literal; this module bakes in NONE — a consumer
with no ``needles`` configured flags nothing.
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: Doc extensions that describe paths rather than execute them. Domain-intrinsic
#: default and part of the rule definition, not consumer config.
DEFAULT_EXEMPT_EXTENSIONS: tuple[str, ...] = (".md",)

#: Any text extension is a candidate — a consumer scopes via ``extensions``.
#: The rule itself has no language; it is a substring search.
DEFAULT_EXTENSIONS: tuple[str, ...] = (".py", ".sh", ".yaml", ".yml", ".json", ".toml")

REMEDIATION = _remediation(
    fix=(
        "replace the hardcoded absolute checkout path with a path resolved "
        "relative to the script (Path(__file__).resolve().parents[N]) or an "
        "environment variable or explicit runtime input."
    ),
    nxt="re-run this check to confirm the hardcode is gone.",
    run="python -m tc_fitness.core_checks.no_hardcoded_repo_paths",
    passing="ROOT = Path(__file__).resolve().parents[2]",
    forbidden='ROOT = "/data/development/<repo>/"',
)


def file_contains_needle(
    path: Path,
    *,
    needles: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the banned ``needles`` substrings.

    Pure helper (the detection core) so tests can assert on it directly. A
    non-UTF-8 file (binary) decodes to nothing of interest and returns False;
    an empty ``needles`` tuple flags nothing.
    """
    if not needles:
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    return any(needle in text for needle in needles)


class NoHardcodedRepoPaths(FitnessRule):
    """Flags files holding a banned absolute-checkout-path needle."""

    name = "no-hardcoded-repo-paths"
    remediation = REMEDIATION
    extensions = DEFAULT_EXTENSIONS

    #: The banned absolute-path substrings — the consumer's OWN checkout
    #: literals. No default: a consumer with none configured flags nothing.
    needles: tuple[str, ...] = ()

    @classmethod
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoHardcodedRepoPaths:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoHardcodedRepoPaths)  # noqa: S101  # narrowing for mypy
        needles = config.get("needles")
        if needles is not None:
            rule.needles = tuple(needles)
        return rule

    def is_in_scope(self, rel: str) -> bool:
        if rel.endswith(DEFAULT_EXEMPT_EXTENSIONS):
            return False
        return super().is_in_scope(rel)

    def file_has_violation(self, path: Path) -> bool:
        return file_contains_needle(path, needles=self.needles)


def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoHardcodedRepoPaths:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoHardcodedRepoPaths.from_config(config, repo_root=repo_root)


def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoHardcodedRepoPaths, argv)


if __name__ == "__main__":
    import sys

    sys.exit(main())
