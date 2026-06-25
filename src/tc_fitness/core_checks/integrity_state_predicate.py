"""CORE check: integrity_state_predicate — completeness checks must assert STATE.

A data-completeness integrity check that LEFT-JOINs a child table and filters on
the join key being NULL ("every parent has a child row") proves PRESENCE, not
STATE. When the child table is multi-state — a row can exist as a placeholder
before it reaches its meaningful "done" state — a presence-only check passes
while the parent is functionally incomplete.

This is the chunk-0 incident: ``content_vectors`` rows are written first as
``(hash, seq, pos)`` placeholders (``model`` NULL) and only later carry a real
embedding (``model`` set). The completeness check joined
``LEFT JOIN content_vectors v ON v.hash = d.hash WHERE v.hash IS NULL`` — so a
document whose only vector was a model-NULL placeholder passed the check despite
never being embedded. The fix was to add the state predicate
(``AND v.model IS NOT NULL``).

This rule flags an in-scope SQL string literal that runs a completeness check
(``LEFT JOIN <state_table> ... IS NULL``) on a configured multi-state table
WITHOUT referencing any of that table's STATE columns. Config supplies the
``state_tables`` map ``{table: [state_columns]}`` — NO table is baked in; a
consumer with none configured flags nothing.

Typical config:

    roots = ["kairix/core/db"]
    [tool.tc_fitness.core_checks.integrity_state_predicate.state_tables]
    content_vectors = ["model", "embedded_at"]
"""

from __future__ import annotations

import ast
import re
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

REMEDIATION = _remediation(
    fix=(
        "add the state predicate to the completeness join so it asserts the "
        "child reached its done-state, not merely that a (possibly placeholder) "
        "row exists — e.g. LEFT JOIN content_vectors v ON v.hash = d.hash AND "
        "v.model IS NOT NULL WHERE v.hash IS NULL. If the join genuinely needs "
        "presence-only (the table has no placeholder state in this context), "
        "remove it from the rule's state_tables config with a one-line rationale."
    ),
    nxt="re-run this check to confirm the completeness query asserts state.",
    run="python -m tc_fitness.core_checks.integrity_state_predicate",
    passing="LEFT JOIN content_vectors v ON v.hash = d.hash AND v.model IS NOT NULL WHERE v.hash IS NULL",
    forbidden="LEFT JOIN content_vectors v ON v.hash = d.hash WHERE v.hash IS NULL  # placeholder passes",
)


def _is_presence_only_completeness_check(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff ``sql`` does a LEFT JOIN <table> … IS NULL completeness check
    without referencing any of ``table``'s state columns."""
    if not re.search(rf"LEFT\s+JOIN\s+{re.escape(table)}\b", sql, re.IGNORECASE):
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    return not any(re.search(rf"\b{re.escape(col)}\b", sql, re.IGNORECASE) for col in state_cols)


def file_missing_state_predicate(path: Path, *, state_tables: Mapping[str, tuple[str, ...]]) -> bool:
    """True iff ``path`` has a SQL string with a presence-only completeness check
    on a configured multi-state table.

    Pure helper (the detection core). Walks string literals via the AST —
    adjacent-literal concatenation (the common multi-line SQL shape) is folded
    into one constant by the parser, so the whole query is one string. A
    syntax/decode error is treated as no violation; an empty ``state_tables``
    flags nothing.
    """
    if not state_tables:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            continue
        for table, state_cols in state_tables.items():
            if _is_presence_only_completeness_check(node.value, table, state_cols):
                return True
    return False


class IntegrityStatePredicate(FitnessRule):
    """Flags presence-only completeness checks on multi-state child tables."""

    name = "integrity-state-predicate"
    remediation = REMEDIATION
    extensions = (".py",)

    #: ``{table: (state_column, ...)}`` — multi-state child tables whose
    #: completeness checks must filter on a state column. No default identity.
    state_tables: Mapping[str, tuple[str, ...]] = {}

    @classmethod
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> IntegrityStatePredicate:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, IntegrityStatePredicate)  # noqa: S101  # narrowing for mypy
        raw = config.get("state_tables")
        if raw is not None:
            rule.state_tables = {str(table): tuple(cols) for table, cols in dict(raw).items()}
        return rule

    def file_has_violation(self, path: Path) -> bool:
        return file_missing_state_predicate(path, state_tables=self.state_tables)


def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> IntegrityStatePredicate:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return IntegrityStatePredicate.from_config(config, repo_root=repo_root)


def main(argv: list[str] | None = None) -> int:
    """CLI entry — supports ``--establish-baseline`` and ``--repo-root``."""
    return run_core_check(IntegrityStatePredicate, argv)


if __name__ == "__main__":
    import sys

    sys.exit(main())
