"""CORE check: pattern_chokepoint — a pattern confined to a single chokepoint.

Some properties belong in exactly ONE place. When a decision (e.g. "is this
write or read?", "which collection does this route to?") is intrinsic to data
and should be derived at a single boundary, letting the deciding token leak to
other call sites recreates the bug it was meant to prevent: a flag you can pass
at N sites is a flag you can forget at one (see the neo4j read/write-session
incident — the write-ness was threaded as a ``write=`` kwarg every caller had to
remember, until it was derived once at ``client.cypher``).

This rule flags any in-scope file — OUTSIDE the configured chokepoint allow-list
(the rule's ``exempt_files``) — that matches a configured regex ``pattern``. The
chokepoint file(s) where the pattern legitimately lives are listed in
``exempt_files``; everywhere else the pattern is forbidden. A consumer with no
``patterns`` configured flags nothing — NO pattern is baked in.

Typical config (a consumer's ``[tool.tc_fitness.core_checks.<name>]`` block):

    name = "cypher-write-mode-chokepoint"
    roots = ["kairix"]
    patterns = ["default_access_mode\\\\s*=", "_is_write_query"]
    exempt_files = ["kairix/knowledge/graph/client.py"]
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
        "the matched token belongs only at its single chokepoint — derive the "
        "property there and call the chokepoint instead of re-introducing the "
        "token here. If a new file is a legitimate part of the chokepoint, add "
        "it to this rule's exempt_files config with a one-line rationale."
    ),
    nxt="re-run this check to confirm the pattern is confined to its chokepoint.",
    run="python -m tc_fitness.core_checks.pattern_chokepoint",
    passing="rows = client.cypher(query, params)  # write-ness derived inside cypher()",
    forbidden='session = driver.session(default_access_mode="WRITE")  # outside the chokepoint',
)


def file_matches_any_pattern(path: Path, *, patterns: tuple[str, ...]) -> bool:
    """True iff ``path``'s text matches any of the regex ``patterns``.

    Pure helper (the detection core) so tests can assert on it directly. A
    non-UTF-8 / unreadable file returns False; an empty ``patterns`` tuple flags
    nothing. Patterns are compiled per call — checks run once, so this is not a
    hot path.
    """
    if not patterns:
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    return any(re.search(p, text) for p in patterns)


class PatternChokepoint(FitnessRule):
    """Flags files outside the chokepoint (``exempt_files``) matching a pattern."""

    name = "pattern-chokepoint"
    remediation = REMEDIATION
    extensions = (".py",)

    #: Regexes whose match outside the chokepoint is a violation. No default:
    #: a consumer with none configured flags nothing.
    patterns: tuple[str, ...] = ()

    @classmethod
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PatternChokepoint:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PatternChokepoint)  # noqa: S101  # narrowing for mypy
        patterns = config.get("patterns")
        if patterns is not None:
            rule.patterns = tuple(patterns)
        return rule

    def file_has_violation(self, path: Path) -> bool:
        # The chokepoint file(s) are skipped by the base via ``exempt_files``;
        # this fires only for in-scope, non-exempt files that match.
        return file_matches_any_pattern(path, patterns=self.patterns)


def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> PatternChokepoint:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return PatternChokepoint.from_config(config, repo_root=repo_root)


def main(argv: list[str] | None = None) -> int:
    """CLI entry — supports ``--establish-baseline`` and ``--repo-root``."""
    return run_core_check(PatternChokepoint, argv)


if __name__ == "__main__":
    import sys

    sys.exit(main())
