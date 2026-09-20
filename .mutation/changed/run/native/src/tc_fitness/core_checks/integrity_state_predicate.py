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


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x__is_presence_only_completeness_check__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__is_presence_only_completeness_check__mutmut)
def _is_presence_only_completeness_check(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_orig(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_1(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = None
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_2(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        None,
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_3(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        None,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_4(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        None,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_5(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_6(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_7(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_8(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(None)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_9(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"XX(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\bXX"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_10(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:as\s+)?(?p<alias>[a-za-z_][\w$]*))?\s+on\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_11(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<ALIAS>[A-ZA-Z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_12(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"XX(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)XX",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_13(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?p<on>.*?)(?=\b(?:left|right|inner|full|cross)\s+join\b|\bwhere\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_14(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<ON>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_15(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE & re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_16(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is not None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_17(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return True
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_18(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_19(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(None, sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_20(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", None, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_21(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, None):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_22(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_23(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_24(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, ):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_25(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"XX\bIS\s+NULL\bXX", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_26(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bis\s+null\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_27(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return True
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_28(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = None
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_29(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") and table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_30(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group(None) or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_31(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("XXaliasXX") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_32(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("ALIAS") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_33(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(None, 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_34(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", None)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_35(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_36(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", )[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_37(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.split(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_38(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit("XX.XX", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_39(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 2)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_40(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[+1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_41(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-2]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_42(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = None
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_43(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(None, " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_44(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", None, join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_45(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", None, flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_46(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=None)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_47(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(" ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_48(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_49(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_50(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), )
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_51(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"XX--[^\n]*|/\*.*?\*/XX", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_52(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", "XX XX", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_53(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group(None), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_54(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("XXonXX"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_55(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("ON"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_56(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_57(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        None
    )


def x__is_presence_only_completeness_check__mutmut_58(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(None, on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_59(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", None, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_60(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, None)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_61(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_62(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_63(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(col)}\b", on_clause, )
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_64(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(None)}\s*\.\s*{re.escape(col)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )


def x__is_presence_only_completeness_check__mutmut_65(sql: str, table: str, state_cols: tuple[str, ...]) -> bool:
    """True iff a joined table has a NULL-completeness check but no ON state filter."""
    join = re.search(
        rf"LEFT\s+JOIN\s+{re.escape(table)}\b"
        r"(?:\s+(?:AS\s+)?(?P<alias>[A-Za-z_][\w$]*))?\s+ON\b"
        r"(?P<on>.*?)(?=\b(?:LEFT|RIGHT|INNER|FULL|CROSS)\s+JOIN\b|\bWHERE\b|$)",
        sql,
        re.IGNORECASE | re.DOTALL,
    )
    if join is None:
        return False
    if not re.search(r"\bIS\s+NULL\b", sql, re.IGNORECASE):
        return False
    alias = join.group("alias") or table.rsplit(".", 1)[-1]
    on_clause = re.sub(r"--[^\n]*|/\*.*?\*/", " ", join.group("on"), flags=re.DOTALL)
    return not any(
        re.search(rf"\b{re.escape(alias)}\s*\.\s*{re.escape(None)}\b", on_clause, re.IGNORECASE)
        for col in state_cols
    )

mutants_x__is_presence_only_completeness_check__mutmut['_mutmut_orig'] = x__is_presence_only_completeness_check__mutmut_orig # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_1'] = x__is_presence_only_completeness_check__mutmut_1 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_2'] = x__is_presence_only_completeness_check__mutmut_2 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_3'] = x__is_presence_only_completeness_check__mutmut_3 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_4'] = x__is_presence_only_completeness_check__mutmut_4 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_5'] = x__is_presence_only_completeness_check__mutmut_5 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_6'] = x__is_presence_only_completeness_check__mutmut_6 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_7'] = x__is_presence_only_completeness_check__mutmut_7 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_8'] = x__is_presence_only_completeness_check__mutmut_8 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_9'] = x__is_presence_only_completeness_check__mutmut_9 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_10'] = x__is_presence_only_completeness_check__mutmut_10 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_11'] = x__is_presence_only_completeness_check__mutmut_11 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_12'] = x__is_presence_only_completeness_check__mutmut_12 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_13'] = x__is_presence_only_completeness_check__mutmut_13 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_14'] = x__is_presence_only_completeness_check__mutmut_14 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_15'] = x__is_presence_only_completeness_check__mutmut_15 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_16'] = x__is_presence_only_completeness_check__mutmut_16 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_17'] = x__is_presence_only_completeness_check__mutmut_17 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_18'] = x__is_presence_only_completeness_check__mutmut_18 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_19'] = x__is_presence_only_completeness_check__mutmut_19 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_20'] = x__is_presence_only_completeness_check__mutmut_20 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_21'] = x__is_presence_only_completeness_check__mutmut_21 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_22'] = x__is_presence_only_completeness_check__mutmut_22 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_23'] = x__is_presence_only_completeness_check__mutmut_23 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_24'] = x__is_presence_only_completeness_check__mutmut_24 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_25'] = x__is_presence_only_completeness_check__mutmut_25 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_26'] = x__is_presence_only_completeness_check__mutmut_26 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_27'] = x__is_presence_only_completeness_check__mutmut_27 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_28'] = x__is_presence_only_completeness_check__mutmut_28 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_29'] = x__is_presence_only_completeness_check__mutmut_29 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_30'] = x__is_presence_only_completeness_check__mutmut_30 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_31'] = x__is_presence_only_completeness_check__mutmut_31 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_32'] = x__is_presence_only_completeness_check__mutmut_32 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_33'] = x__is_presence_only_completeness_check__mutmut_33 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_34'] = x__is_presence_only_completeness_check__mutmut_34 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_35'] = x__is_presence_only_completeness_check__mutmut_35 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_36'] = x__is_presence_only_completeness_check__mutmut_36 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_37'] = x__is_presence_only_completeness_check__mutmut_37 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_38'] = x__is_presence_only_completeness_check__mutmut_38 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_39'] = x__is_presence_only_completeness_check__mutmut_39 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_40'] = x__is_presence_only_completeness_check__mutmut_40 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_41'] = x__is_presence_only_completeness_check__mutmut_41 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_42'] = x__is_presence_only_completeness_check__mutmut_42 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_43'] = x__is_presence_only_completeness_check__mutmut_43 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_44'] = x__is_presence_only_completeness_check__mutmut_44 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_45'] = x__is_presence_only_completeness_check__mutmut_45 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_46'] = x__is_presence_only_completeness_check__mutmut_46 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_47'] = x__is_presence_only_completeness_check__mutmut_47 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_48'] = x__is_presence_only_completeness_check__mutmut_48 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_49'] = x__is_presence_only_completeness_check__mutmut_49 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_50'] = x__is_presence_only_completeness_check__mutmut_50 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_51'] = x__is_presence_only_completeness_check__mutmut_51 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_52'] = x__is_presence_only_completeness_check__mutmut_52 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_53'] = x__is_presence_only_completeness_check__mutmut_53 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_54'] = x__is_presence_only_completeness_check__mutmut_54 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_55'] = x__is_presence_only_completeness_check__mutmut_55 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_56'] = x__is_presence_only_completeness_check__mutmut_56 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_57'] = x__is_presence_only_completeness_check__mutmut_57 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_58'] = x__is_presence_only_completeness_check__mutmut_58 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_59'] = x__is_presence_only_completeness_check__mutmut_59 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_60'] = x__is_presence_only_completeness_check__mutmut_60 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_61'] = x__is_presence_only_completeness_check__mutmut_61 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_62'] = x__is_presence_only_completeness_check__mutmut_62 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_63'] = x__is_presence_only_completeness_check__mutmut_63 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_64'] = x__is_presence_only_completeness_check__mutmut_64 # type: ignore # mutmut generated
mutants_x__is_presence_only_completeness_check__mutmut['x__is_presence_only_completeness_check__mutmut_65'] = x__is_presence_only_completeness_check__mutmut_65 # type: ignore # mutmut generated
mutants_x_file_missing_state_predicate__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_file_missing_state_predicate__mutmut)
def file_missing_state_predicate(path: Path, *, state_tables: Mapping[str, tuple[str, ...]]) -> bool:
    """True iff ``path`` has a SQL string with a presence-only completeness check
    on a configured multi-state table.

    Pure helper (the detection core). Walks string literals via the AST —
    adjacent-literal concatenation (the common multi-line SQL shape) is folded
    into one constant by the parser, so the whole query is one string. A
    syntax/decode/read error is a violation because the configured source could
    not be evaluated; an empty ``state_tables`` flags nothing.
    """
    if not state_tables:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            continue
        for table, state_cols in state_tables.items():
            if _is_presence_only_completeness_check(node.value, table, state_cols):
                return True
    return False


def x_file_missing_state_predicate__mutmut_orig(path: Path, *, state_tables: Mapping[str, tuple[str, ...]]) -> bool:
    """True iff ``path`` has a SQL string with a presence-only completeness check
    on a configured multi-state table.

    Pure helper (the detection core). Walks string literals via the AST —
    adjacent-literal concatenation (the common multi-line SQL shape) is folded
    into one constant by the parser, so the whole query is one string. A
    syntax/decode/read error is a violation because the configured source could
    not be evaluated; an empty ``state_tables`` flags nothing.
    """
    if not state_tables:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            continue
        for table, state_cols in state_tables.items():
            if _is_presence_only_completeness_check(node.value, table, state_cols):
                return True
    return False


def x_file_missing_state_predicate__mutmut_1(path: Path, *, state_tables: Mapping[str, tuple[str, ...]]) -> bool:
    """True iff ``path`` has a SQL string with a presence-only completeness check
    on a configured multi-state table.

    Pure helper (the detection core). Walks string literals via the AST —
    adjacent-literal concatenation (the common multi-line SQL shape) is folded
    into one constant by the parser, so the whole query is one string. A
    syntax/decode/read error is a violation because the configured source could
    not be evaluated; an empty ``state_tables`` flags nothing.
    """
    if state_tables:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            continue
        for table, state_cols in state_tables.items():
            if _is_presence_only_completeness_check(node.value, table, state_cols):
                return True
    return False


def x_file_missing_state_predicate__mutmut_2(path: Path, *, state_tables: Mapping[str, tuple[str, ...]]) -> bool:
    """True iff ``path`` has a SQL string with a presence-only completeness check
    on a configured multi-state table.

    Pure helper (the detection core). Walks string literals via the AST —
    adjacent-literal concatenation (the common multi-line SQL shape) is folded
    into one constant by the parser, so the whole query is one string. A
    syntax/decode/read error is a violation because the configured source could
    not be evaluated; an empty ``state_tables`` flags nothing.
    """
    if not state_tables:
        return True
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            continue
        for table, state_cols in state_tables.items():
            if _is_presence_only_completeness_check(node.value, table, state_cols):
                return True
    return False


def x_file_missing_state_predicate__mutmut_3(path: Path, *, state_tables: Mapping[str, tuple[str, ...]]) -> bool:
    """True iff ``path`` has a SQL string with a presence-only completeness check
    on a configured multi-state table.

    Pure helper (the detection core). Walks string literals via the AST —
    adjacent-literal concatenation (the common multi-line SQL shape) is folded
    into one constant by the parser, so the whole query is one string. A
    syntax/decode/read error is a violation because the configured source could
    not be evaluated; an empty ``state_tables`` flags nothing.
    """
    if not state_tables:
        return False
    try:
        tree = None
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            continue
        for table, state_cols in state_tables.items():
            if _is_presence_only_completeness_check(node.value, table, state_cols):
                return True
    return False


def x_file_missing_state_predicate__mutmut_4(path: Path, *, state_tables: Mapping[str, tuple[str, ...]]) -> bool:
    """True iff ``path`` has a SQL string with a presence-only completeness check
    on a configured multi-state table.

    Pure helper (the detection core). Walks string literals via the AST —
    adjacent-literal concatenation (the common multi-line SQL shape) is folded
    into one constant by the parser, so the whole query is one string. A
    syntax/decode/read error is a violation because the configured source could
    not be evaluated; an empty ``state_tables`` flags nothing.
    """
    if not state_tables:
        return False
    try:
        tree = ast.parse(None, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            continue
        for table, state_cols in state_tables.items():
            if _is_presence_only_completeness_check(node.value, table, state_cols):
                return True
    return False


def x_file_missing_state_predicate__mutmut_5(path: Path, *, state_tables: Mapping[str, tuple[str, ...]]) -> bool:
    """True iff ``path`` has a SQL string with a presence-only completeness check
    on a configured multi-state table.

    Pure helper (the detection core). Walks string literals via the AST —
    adjacent-literal concatenation (the common multi-line SQL shape) is folded
    into one constant by the parser, so the whole query is one string. A
    syntax/decode/read error is a violation because the configured source could
    not be evaluated; an empty ``state_tables`` flags nothing.
    """
    if not state_tables:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=None)
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            continue
        for table, state_cols in state_tables.items():
            if _is_presence_only_completeness_check(node.value, table, state_cols):
                return True
    return False


def x_file_missing_state_predicate__mutmut_6(path: Path, *, state_tables: Mapping[str, tuple[str, ...]]) -> bool:
    """True iff ``path`` has a SQL string with a presence-only completeness check
    on a configured multi-state table.

    Pure helper (the detection core). Walks string literals via the AST —
    adjacent-literal concatenation (the common multi-line SQL shape) is folded
    into one constant by the parser, so the whole query is one string. A
    syntax/decode/read error is a violation because the configured source could
    not be evaluated; an empty ``state_tables`` flags nothing.
    """
    if not state_tables:
        return False
    try:
        tree = ast.parse(filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            continue
        for table, state_cols in state_tables.items():
            if _is_presence_only_completeness_check(node.value, table, state_cols):
                return True
    return False


def x_file_missing_state_predicate__mutmut_7(path: Path, *, state_tables: Mapping[str, tuple[str, ...]]) -> bool:
    """True iff ``path`` has a SQL string with a presence-only completeness check
    on a configured multi-state table.

    Pure helper (the detection core). Walks string literals via the AST —
    adjacent-literal concatenation (the common multi-line SQL shape) is folded
    into one constant by the parser, so the whole query is one string. A
    syntax/decode/read error is a violation because the configured source could
    not be evaluated; an empty ``state_tables`` flags nothing.
    """
    if not state_tables:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), )
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            continue
        for table, state_cols in state_tables.items():
            if _is_presence_only_completeness_check(node.value, table, state_cols):
                return True
    return False


def x_file_missing_state_predicate__mutmut_8(path: Path, *, state_tables: Mapping[str, tuple[str, ...]]) -> bool:
    """True iff ``path`` has a SQL string with a presence-only completeness check
    on a configured multi-state table.

    Pure helper (the detection core). Walks string literals via the AST —
    adjacent-literal concatenation (the common multi-line SQL shape) is folded
    into one constant by the parser, so the whole query is one string. A
    syntax/decode/read error is a violation because the configured source could
    not be evaluated; an empty ``state_tables`` flags nothing.
    """
    if not state_tables:
        return False
    try:
        tree = ast.parse(path.read_text(encoding=None), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            continue
        for table, state_cols in state_tables.items():
            if _is_presence_only_completeness_check(node.value, table, state_cols):
                return True
    return False


def x_file_missing_state_predicate__mutmut_9(path: Path, *, state_tables: Mapping[str, tuple[str, ...]]) -> bool:
    """True iff ``path`` has a SQL string with a presence-only completeness check
    on a configured multi-state table.

    Pure helper (the detection core). Walks string literals via the AST —
    adjacent-literal concatenation (the common multi-line SQL shape) is folded
    into one constant by the parser, so the whole query is one string. A
    syntax/decode/read error is a violation because the configured source could
    not be evaluated; an empty ``state_tables`` flags nothing.
    """
    if not state_tables:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="XXutf-8XX"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            continue
        for table, state_cols in state_tables.items():
            if _is_presence_only_completeness_check(node.value, table, state_cols):
                return True
    return False


def x_file_missing_state_predicate__mutmut_10(path: Path, *, state_tables: Mapping[str, tuple[str, ...]]) -> bool:
    """True iff ``path`` has a SQL string with a presence-only completeness check
    on a configured multi-state table.

    Pure helper (the detection core). Walks string literals via the AST —
    adjacent-literal concatenation (the common multi-line SQL shape) is folded
    into one constant by the parser, so the whole query is one string. A
    syntax/decode/read error is a violation because the configured source could
    not be evaluated; an empty ``state_tables`` flags nothing.
    """
    if not state_tables:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="UTF-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            continue
        for table, state_cols in state_tables.items():
            if _is_presence_only_completeness_check(node.value, table, state_cols):
                return True
    return False


def x_file_missing_state_predicate__mutmut_11(path: Path, *, state_tables: Mapping[str, tuple[str, ...]]) -> bool:
    """True iff ``path`` has a SQL string with a presence-only completeness check
    on a configured multi-state table.

    Pure helper (the detection core). Walks string literals via the AST —
    adjacent-literal concatenation (the common multi-line SQL shape) is folded
    into one constant by the parser, so the whole query is one string. A
    syntax/decode/read error is a violation because the configured source could
    not be evaluated; an empty ``state_tables`` flags nothing.
    """
    if not state_tables:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(None))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            continue
        for table, state_cols in state_tables.items():
            if _is_presence_only_completeness_check(node.value, table, state_cols):
                return True
    return False


def x_file_missing_state_predicate__mutmut_12(path: Path, *, state_tables: Mapping[str, tuple[str, ...]]) -> bool:
    """True iff ``path`` has a SQL string with a presence-only completeness check
    on a configured multi-state table.

    Pure helper (the detection core). Walks string literals via the AST —
    adjacent-literal concatenation (the common multi-line SQL shape) is folded
    into one constant by the parser, so the whole query is one string. A
    syntax/decode/read error is a violation because the configured source could
    not be evaluated; an empty ``state_tables`` flags nothing.
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


def x_file_missing_state_predicate__mutmut_13(path: Path, *, state_tables: Mapping[str, tuple[str, ...]]) -> bool:
    """True iff ``path`` has a SQL string with a presence-only completeness check
    on a configured multi-state table.

    Pure helper (the detection core). Walks string literals via the AST —
    adjacent-literal concatenation (the common multi-line SQL shape) is folded
    into one constant by the parser, so the whole query is one string. A
    syntax/decode/read error is a violation because the configured source could
    not be evaluated; an empty ``state_tables`` flags nothing.
    """
    if not state_tables:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(None):
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            continue
        for table, state_cols in state_tables.items():
            if _is_presence_only_completeness_check(node.value, table, state_cols):
                return True
    return False


def x_file_missing_state_predicate__mutmut_14(path: Path, *, state_tables: Mapping[str, tuple[str, ...]]) -> bool:
    """True iff ``path`` has a SQL string with a presence-only completeness check
    on a configured multi-state table.

    Pure helper (the detection core). Walks string literals via the AST —
    adjacent-literal concatenation (the common multi-line SQL shape) is folded
    into one constant by the parser, so the whole query is one string. A
    syntax/decode/read error is a violation because the configured source could
    not be evaluated; an empty ``state_tables`` flags nothing.
    """
    if not state_tables:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            continue
        for table, state_cols in state_tables.items():
            if _is_presence_only_completeness_check(node.value, table, state_cols):
                return True
    return False


def x_file_missing_state_predicate__mutmut_15(path: Path, *, state_tables: Mapping[str, tuple[str, ...]]) -> bool:
    """True iff ``path`` has a SQL string with a presence-only completeness check
    on a configured multi-state table.

    Pure helper (the detection core). Walks string literals via the AST —
    adjacent-literal concatenation (the common multi-line SQL shape) is folded
    into one constant by the parser, so the whole query is one string. A
    syntax/decode/read error is a violation because the configured source could
    not be evaluated; an empty ``state_tables`` flags nothing.
    """
    if not state_tables:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Constant) or isinstance(node.value, str)):
            continue
        for table, state_cols in state_tables.items():
            if _is_presence_only_completeness_check(node.value, table, state_cols):
                return True
    return False


def x_file_missing_state_predicate__mutmut_16(path: Path, *, state_tables: Mapping[str, tuple[str, ...]]) -> bool:
    """True iff ``path`` has a SQL string with a presence-only completeness check
    on a configured multi-state table.

    Pure helper (the detection core). Walks string literals via the AST —
    adjacent-literal concatenation (the common multi-line SQL shape) is folded
    into one constant by the parser, so the whole query is one string. A
    syntax/decode/read error is a violation because the configured source could
    not be evaluated; an empty ``state_tables`` flags nothing.
    """
    if not state_tables:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            break
        for table, state_cols in state_tables.items():
            if _is_presence_only_completeness_check(node.value, table, state_cols):
                return True
    return False


def x_file_missing_state_predicate__mutmut_17(path: Path, *, state_tables: Mapping[str, tuple[str, ...]]) -> bool:
    """True iff ``path`` has a SQL string with a presence-only completeness check
    on a configured multi-state table.

    Pure helper (the detection core). Walks string literals via the AST —
    adjacent-literal concatenation (the common multi-line SQL shape) is folded
    into one constant by the parser, so the whole query is one string. A
    syntax/decode/read error is a violation because the configured source could
    not be evaluated; an empty ``state_tables`` flags nothing.
    """
    if not state_tables:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            continue
        for table, state_cols in state_tables.items():
            if _is_presence_only_completeness_check(None, table, state_cols):
                return True
    return False


def x_file_missing_state_predicate__mutmut_18(path: Path, *, state_tables: Mapping[str, tuple[str, ...]]) -> bool:
    """True iff ``path`` has a SQL string with a presence-only completeness check
    on a configured multi-state table.

    Pure helper (the detection core). Walks string literals via the AST —
    adjacent-literal concatenation (the common multi-line SQL shape) is folded
    into one constant by the parser, so the whole query is one string. A
    syntax/decode/read error is a violation because the configured source could
    not be evaluated; an empty ``state_tables`` flags nothing.
    """
    if not state_tables:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            continue
        for table, state_cols in state_tables.items():
            if _is_presence_only_completeness_check(node.value, None, state_cols):
                return True
    return False


def x_file_missing_state_predicate__mutmut_19(path: Path, *, state_tables: Mapping[str, tuple[str, ...]]) -> bool:
    """True iff ``path`` has a SQL string with a presence-only completeness check
    on a configured multi-state table.

    Pure helper (the detection core). Walks string literals via the AST —
    adjacent-literal concatenation (the common multi-line SQL shape) is folded
    into one constant by the parser, so the whole query is one string. A
    syntax/decode/read error is a violation because the configured source could
    not be evaluated; an empty ``state_tables`` flags nothing.
    """
    if not state_tables:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            continue
        for table, state_cols in state_tables.items():
            if _is_presence_only_completeness_check(node.value, table, None):
                return True
    return False


def x_file_missing_state_predicate__mutmut_20(path: Path, *, state_tables: Mapping[str, tuple[str, ...]]) -> bool:
    """True iff ``path`` has a SQL string with a presence-only completeness check
    on a configured multi-state table.

    Pure helper (the detection core). Walks string literals via the AST —
    adjacent-literal concatenation (the common multi-line SQL shape) is folded
    into one constant by the parser, so the whole query is one string. A
    syntax/decode/read error is a violation because the configured source could
    not be evaluated; an empty ``state_tables`` flags nothing.
    """
    if not state_tables:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            continue
        for table, state_cols in state_tables.items():
            if _is_presence_only_completeness_check(table, state_cols):
                return True
    return False


def x_file_missing_state_predicate__mutmut_21(path: Path, *, state_tables: Mapping[str, tuple[str, ...]]) -> bool:
    """True iff ``path`` has a SQL string with a presence-only completeness check
    on a configured multi-state table.

    Pure helper (the detection core). Walks string literals via the AST —
    adjacent-literal concatenation (the common multi-line SQL shape) is folded
    into one constant by the parser, so the whole query is one string. A
    syntax/decode/read error is a violation because the configured source could
    not be evaluated; an empty ``state_tables`` flags nothing.
    """
    if not state_tables:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            continue
        for table, state_cols in state_tables.items():
            if _is_presence_only_completeness_check(node.value, state_cols):
                return True
    return False


def x_file_missing_state_predicate__mutmut_22(path: Path, *, state_tables: Mapping[str, tuple[str, ...]]) -> bool:
    """True iff ``path`` has a SQL string with a presence-only completeness check
    on a configured multi-state table.

    Pure helper (the detection core). Walks string literals via the AST —
    adjacent-literal concatenation (the common multi-line SQL shape) is folded
    into one constant by the parser, so the whole query is one string. A
    syntax/decode/read error is a violation because the configured source could
    not be evaluated; an empty ``state_tables`` flags nothing.
    """
    if not state_tables:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            continue
        for table, state_cols in state_tables.items():
            if _is_presence_only_completeness_check(node.value, table, ):
                return True
    return False


def x_file_missing_state_predicate__mutmut_23(path: Path, *, state_tables: Mapping[str, tuple[str, ...]]) -> bool:
    """True iff ``path`` has a SQL string with a presence-only completeness check
    on a configured multi-state table.

    Pure helper (the detection core). Walks string literals via the AST —
    adjacent-literal concatenation (the common multi-line SQL shape) is folded
    into one constant by the parser, so the whole query is one string. A
    syntax/decode/read error is a violation because the configured source could
    not be evaluated; an empty ``state_tables`` flags nothing.
    """
    if not state_tables:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            continue
        for table, state_cols in state_tables.items():
            if _is_presence_only_completeness_check(node.value, table, state_cols):
                return False
    return False


def x_file_missing_state_predicate__mutmut_24(path: Path, *, state_tables: Mapping[str, tuple[str, ...]]) -> bool:
    """True iff ``path`` has a SQL string with a presence-only completeness check
    on a configured multi-state table.

    Pure helper (the detection core). Walks string literals via the AST —
    adjacent-literal concatenation (the common multi-line SQL shape) is folded
    into one constant by the parser, so the whole query is one string. A
    syntax/decode/read error is a violation because the configured source could
    not be evaluated; an empty ``state_tables`` flags nothing.
    """
    if not state_tables:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            continue
        for table, state_cols in state_tables.items():
            if _is_presence_only_completeness_check(node.value, table, state_cols):
                return True
    return True

mutants_x_file_missing_state_predicate__mutmut['_mutmut_orig'] = x_file_missing_state_predicate__mutmut_orig # type: ignore # mutmut generated
mutants_x_file_missing_state_predicate__mutmut['x_file_missing_state_predicate__mutmut_1'] = x_file_missing_state_predicate__mutmut_1 # type: ignore # mutmut generated
mutants_x_file_missing_state_predicate__mutmut['x_file_missing_state_predicate__mutmut_2'] = x_file_missing_state_predicate__mutmut_2 # type: ignore # mutmut generated
mutants_x_file_missing_state_predicate__mutmut['x_file_missing_state_predicate__mutmut_3'] = x_file_missing_state_predicate__mutmut_3 # type: ignore # mutmut generated
mutants_x_file_missing_state_predicate__mutmut['x_file_missing_state_predicate__mutmut_4'] = x_file_missing_state_predicate__mutmut_4 # type: ignore # mutmut generated
mutants_x_file_missing_state_predicate__mutmut['x_file_missing_state_predicate__mutmut_5'] = x_file_missing_state_predicate__mutmut_5 # type: ignore # mutmut generated
mutants_x_file_missing_state_predicate__mutmut['x_file_missing_state_predicate__mutmut_6'] = x_file_missing_state_predicate__mutmut_6 # type: ignore # mutmut generated
mutants_x_file_missing_state_predicate__mutmut['x_file_missing_state_predicate__mutmut_7'] = x_file_missing_state_predicate__mutmut_7 # type: ignore # mutmut generated
mutants_x_file_missing_state_predicate__mutmut['x_file_missing_state_predicate__mutmut_8'] = x_file_missing_state_predicate__mutmut_8 # type: ignore # mutmut generated
mutants_x_file_missing_state_predicate__mutmut['x_file_missing_state_predicate__mutmut_9'] = x_file_missing_state_predicate__mutmut_9 # type: ignore # mutmut generated
mutants_x_file_missing_state_predicate__mutmut['x_file_missing_state_predicate__mutmut_10'] = x_file_missing_state_predicate__mutmut_10 # type: ignore # mutmut generated
mutants_x_file_missing_state_predicate__mutmut['x_file_missing_state_predicate__mutmut_11'] = x_file_missing_state_predicate__mutmut_11 # type: ignore # mutmut generated
mutants_x_file_missing_state_predicate__mutmut['x_file_missing_state_predicate__mutmut_12'] = x_file_missing_state_predicate__mutmut_12 # type: ignore # mutmut generated
mutants_x_file_missing_state_predicate__mutmut['x_file_missing_state_predicate__mutmut_13'] = x_file_missing_state_predicate__mutmut_13 # type: ignore # mutmut generated
mutants_x_file_missing_state_predicate__mutmut['x_file_missing_state_predicate__mutmut_14'] = x_file_missing_state_predicate__mutmut_14 # type: ignore # mutmut generated
mutants_x_file_missing_state_predicate__mutmut['x_file_missing_state_predicate__mutmut_15'] = x_file_missing_state_predicate__mutmut_15 # type: ignore # mutmut generated
mutants_x_file_missing_state_predicate__mutmut['x_file_missing_state_predicate__mutmut_16'] = x_file_missing_state_predicate__mutmut_16 # type: ignore # mutmut generated
mutants_x_file_missing_state_predicate__mutmut['x_file_missing_state_predicate__mutmut_17'] = x_file_missing_state_predicate__mutmut_17 # type: ignore # mutmut generated
mutants_x_file_missing_state_predicate__mutmut['x_file_missing_state_predicate__mutmut_18'] = x_file_missing_state_predicate__mutmut_18 # type: ignore # mutmut generated
mutants_x_file_missing_state_predicate__mutmut['x_file_missing_state_predicate__mutmut_19'] = x_file_missing_state_predicate__mutmut_19 # type: ignore # mutmut generated
mutants_x_file_missing_state_predicate__mutmut['x_file_missing_state_predicate__mutmut_20'] = x_file_missing_state_predicate__mutmut_20 # type: ignore # mutmut generated
mutants_x_file_missing_state_predicate__mutmut['x_file_missing_state_predicate__mutmut_21'] = x_file_missing_state_predicate__mutmut_21 # type: ignore # mutmut generated
mutants_x_file_missing_state_predicate__mutmut['x_file_missing_state_predicate__mutmut_22'] = x_file_missing_state_predicate__mutmut_22 # type: ignore # mutmut generated
mutants_x_file_missing_state_predicate__mutmut['x_file_missing_state_predicate__mutmut_23'] = x_file_missing_state_predicate__mutmut_23 # type: ignore # mutmut generated
mutants_x_file_missing_state_predicate__mutmut['x_file_missing_state_predicate__mutmut_24'] = x_file_missing_state_predicate__mutmut_24 # type: ignore # mutmut generated
mutants_xǁIntegrityStatePredicateǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁIntegrityStatePredicateǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore


class IntegrityStatePredicate(FitnessRule):
    """Flags presence-only completeness checks on multi-state child tables."""

    name = "integrity-state-predicate"
    remediation = REMEDIATION
    extensions = (".py",)

    #: ``{table: (state_column, ...)}`` — multi-state child tables whose
    #: completeness checks must filter on a state column. No default identity.
    state_tables: Mapping[str, tuple[str, ...]] = {}

    @classmethod
    @_mutmut_mutated(mutants_xǁIntegrityStatePredicateǁfrom_config__mutmut, is_classmethod = True)
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

    @classmethod
    def xǁIntegrityStatePredicateǁfrom_config__mutmut_orig(
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

    @classmethod
    def xǁIntegrityStatePredicateǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> IntegrityStatePredicate:
        rule = None
        assert isinstance(rule, IntegrityStatePredicate)  # noqa: S101  # narrowing for mypy
        raw = config.get("state_tables")
        if raw is not None:
            rule.state_tables = {str(table): tuple(cols) for table, cols in dict(raw).items()}
        return rule

    @classmethod
    def xǁIntegrityStatePredicateǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> IntegrityStatePredicate:
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, IntegrityStatePredicate)  # noqa: S101  # narrowing for mypy
        raw = config.get("state_tables")
        if raw is not None:
            rule.state_tables = {str(table): tuple(cols) for table, cols in dict(raw).items()}
        return rule

    @classmethod
    def xǁIntegrityStatePredicateǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> IntegrityStatePredicate:
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, IntegrityStatePredicate)  # noqa: S101  # narrowing for mypy
        raw = config.get("state_tables")
        if raw is not None:
            rule.state_tables = {str(table): tuple(cols) for table, cols in dict(raw).items()}
        return rule

    @classmethod
    def xǁIntegrityStatePredicateǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> IntegrityStatePredicate:
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, IntegrityStatePredicate)  # noqa: S101  # narrowing for mypy
        raw = config.get("state_tables")
        if raw is not None:
            rule.state_tables = {str(table): tuple(cols) for table, cols in dict(raw).items()}
        return rule

    @classmethod
    def xǁIntegrityStatePredicateǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> IntegrityStatePredicate:
        rule = super().from_config(config, )
        assert isinstance(rule, IntegrityStatePredicate)  # noqa: S101  # narrowing for mypy
        raw = config.get("state_tables")
        if raw is not None:
            rule.state_tables = {str(table): tuple(cols) for table, cols in dict(raw).items()}
        return rule

    @classmethod
    def xǁIntegrityStatePredicateǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> IntegrityStatePredicate:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, IntegrityStatePredicate)  # noqa: S101  # narrowing for mypy
        raw = None
        if raw is not None:
            rule.state_tables = {str(table): tuple(cols) for table, cols in dict(raw).items()}
        return rule

    @classmethod
    def xǁIntegrityStatePredicateǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> IntegrityStatePredicate:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, IntegrityStatePredicate)  # noqa: S101  # narrowing for mypy
        raw = config.get(None)
        if raw is not None:
            rule.state_tables = {str(table): tuple(cols) for table, cols in dict(raw).items()}
        return rule

    @classmethod
    def xǁIntegrityStatePredicateǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> IntegrityStatePredicate:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, IntegrityStatePredicate)  # noqa: S101  # narrowing for mypy
        raw = config.get("XXstate_tablesXX")
        if raw is not None:
            rule.state_tables = {str(table): tuple(cols) for table, cols in dict(raw).items()}
        return rule

    @classmethod
    def xǁIntegrityStatePredicateǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> IntegrityStatePredicate:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, IntegrityStatePredicate)  # noqa: S101  # narrowing for mypy
        raw = config.get("STATE_TABLES")
        if raw is not None:
            rule.state_tables = {str(table): tuple(cols) for table, cols in dict(raw).items()}
        return rule

    @classmethod
    def xǁIntegrityStatePredicateǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> IntegrityStatePredicate:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, IntegrityStatePredicate)  # noqa: S101  # narrowing for mypy
        raw = config.get("state_tables")
        if raw is None:
            rule.state_tables = {str(table): tuple(cols) for table, cols in dict(raw).items()}
        return rule

    @classmethod
    def xǁIntegrityStatePredicateǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> IntegrityStatePredicate:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, IntegrityStatePredicate)  # noqa: S101  # narrowing for mypy
        raw = config.get("state_tables")
        if raw is not None:
            rule.state_tables = None
        return rule

    @classmethod
    def xǁIntegrityStatePredicateǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> IntegrityStatePredicate:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, IntegrityStatePredicate)  # noqa: S101  # narrowing for mypy
        raw = config.get("state_tables")
        if raw is not None:
            rule.state_tables = {str(None): tuple(cols) for table, cols in dict(raw).items()}
        return rule

    @classmethod
    def xǁIntegrityStatePredicateǁfrom_config__mutmut_13(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> IntegrityStatePredicate:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, IntegrityStatePredicate)  # noqa: S101  # narrowing for mypy
        raw = config.get("state_tables")
        if raw is not None:
            rule.state_tables = {str(table): tuple(None) for table, cols in dict(raw).items()}
        return rule

    @classmethod
    def xǁIntegrityStatePredicateǁfrom_config__mutmut_14(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> IntegrityStatePredicate:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, IntegrityStatePredicate)  # noqa: S101  # narrowing for mypy
        raw = config.get("state_tables")
        if raw is not None:
            rule.state_tables = {str(table): tuple(cols) for table, cols in dict(None).items()}
        return rule

    @_mutmut_mutated(mutants_xǁIntegrityStatePredicateǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        return file_missing_state_predicate(path, state_tables=self.state_tables)

    def xǁIntegrityStatePredicateǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        return file_missing_state_predicate(path, state_tables=self.state_tables)

    def xǁIntegrityStatePredicateǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        return file_missing_state_predicate(None, state_tables=self.state_tables)

    def xǁIntegrityStatePredicateǁfile_has_violation__mutmut_2(self, path: Path) -> bool:
        return file_missing_state_predicate(path, state_tables=None)

    def xǁIntegrityStatePredicateǁfile_has_violation__mutmut_3(self, path: Path) -> bool:
        return file_missing_state_predicate(state_tables=self.state_tables)

    def xǁIntegrityStatePredicateǁfile_has_violation__mutmut_4(self, path: Path) -> bool:
        return file_missing_state_predicate(path, )

mutants_xǁIntegrityStatePredicateǁfrom_config__mutmut['_mutmut_orig'] = IntegrityStatePredicate.xǁIntegrityStatePredicateǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁIntegrityStatePredicateǁfrom_config__mutmut['xǁIntegrityStatePredicateǁfrom_config__mutmut_1'] = IntegrityStatePredicate.xǁIntegrityStatePredicateǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁIntegrityStatePredicateǁfrom_config__mutmut['xǁIntegrityStatePredicateǁfrom_config__mutmut_2'] = IntegrityStatePredicate.xǁIntegrityStatePredicateǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁIntegrityStatePredicateǁfrom_config__mutmut['xǁIntegrityStatePredicateǁfrom_config__mutmut_3'] = IntegrityStatePredicate.xǁIntegrityStatePredicateǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁIntegrityStatePredicateǁfrom_config__mutmut['xǁIntegrityStatePredicateǁfrom_config__mutmut_4'] = IntegrityStatePredicate.xǁIntegrityStatePredicateǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁIntegrityStatePredicateǁfrom_config__mutmut['xǁIntegrityStatePredicateǁfrom_config__mutmut_5'] = IntegrityStatePredicate.xǁIntegrityStatePredicateǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁIntegrityStatePredicateǁfrom_config__mutmut['xǁIntegrityStatePredicateǁfrom_config__mutmut_6'] = IntegrityStatePredicate.xǁIntegrityStatePredicateǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁIntegrityStatePredicateǁfrom_config__mutmut['xǁIntegrityStatePredicateǁfrom_config__mutmut_7'] = IntegrityStatePredicate.xǁIntegrityStatePredicateǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁIntegrityStatePredicateǁfrom_config__mutmut['xǁIntegrityStatePredicateǁfrom_config__mutmut_8'] = IntegrityStatePredicate.xǁIntegrityStatePredicateǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁIntegrityStatePredicateǁfrom_config__mutmut['xǁIntegrityStatePredicateǁfrom_config__mutmut_9'] = IntegrityStatePredicate.xǁIntegrityStatePredicateǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁIntegrityStatePredicateǁfrom_config__mutmut['xǁIntegrityStatePredicateǁfrom_config__mutmut_10'] = IntegrityStatePredicate.xǁIntegrityStatePredicateǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁIntegrityStatePredicateǁfrom_config__mutmut['xǁIntegrityStatePredicateǁfrom_config__mutmut_11'] = IntegrityStatePredicate.xǁIntegrityStatePredicateǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁIntegrityStatePredicateǁfrom_config__mutmut['xǁIntegrityStatePredicateǁfrom_config__mutmut_12'] = IntegrityStatePredicate.xǁIntegrityStatePredicateǁfrom_config__mutmut_12 # type: ignore # mutmut generated
mutants_xǁIntegrityStatePredicateǁfrom_config__mutmut['xǁIntegrityStatePredicateǁfrom_config__mutmut_13'] = IntegrityStatePredicate.xǁIntegrityStatePredicateǁfrom_config__mutmut_13 # type: ignore # mutmut generated
mutants_xǁIntegrityStatePredicateǁfrom_config__mutmut['xǁIntegrityStatePredicateǁfrom_config__mutmut_14'] = IntegrityStatePredicate.xǁIntegrityStatePredicateǁfrom_config__mutmut_14 # type: ignore # mutmut generated

mutants_xǁIntegrityStatePredicateǁfile_has_violation__mutmut['_mutmut_orig'] = IntegrityStatePredicate.xǁIntegrityStatePredicateǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁIntegrityStatePredicateǁfile_has_violation__mutmut['xǁIntegrityStatePredicateǁfile_has_violation__mutmut_1'] = IntegrityStatePredicate.xǁIntegrityStatePredicateǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_xǁIntegrityStatePredicateǁfile_has_violation__mutmut['xǁIntegrityStatePredicateǁfile_has_violation__mutmut_2'] = IntegrityStatePredicate.xǁIntegrityStatePredicateǁfile_has_violation__mutmut_2 # type: ignore # mutmut generated
mutants_xǁIntegrityStatePredicateǁfile_has_violation__mutmut['xǁIntegrityStatePredicateǁfile_has_violation__mutmut_3'] = IntegrityStatePredicate.xǁIntegrityStatePredicateǁfile_has_violation__mutmut_3 # type: ignore # mutmut generated
mutants_xǁIntegrityStatePredicateǁfile_has_violation__mutmut['xǁIntegrityStatePredicateǁfile_has_violation__mutmut_4'] = IntegrityStatePredicate.xǁIntegrityStatePredicateǁfile_has_violation__mutmut_4 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> IntegrityStatePredicate:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return IntegrityStatePredicate.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> IntegrityStatePredicate:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return IntegrityStatePredicate.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> IntegrityStatePredicate:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return IntegrityStatePredicate.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> IntegrityStatePredicate:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return IntegrityStatePredicate.from_config(config, repo_root=None)


def x_build__mutmut_3(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> IntegrityStatePredicate:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return IntegrityStatePredicate.from_config(repo_root=repo_root)


def x_build__mutmut_4(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> IntegrityStatePredicate:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return IntegrityStatePredicate.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(IntegrityStatePredicate, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(IntegrityStatePredicate, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(IntegrityStatePredicate, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(IntegrityStatePredicate, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
