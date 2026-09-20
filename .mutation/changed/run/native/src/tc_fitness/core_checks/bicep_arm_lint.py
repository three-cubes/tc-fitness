"""CORE check: bicep_arm_lint — Bicep static analysis for SonarSource
``azureresourcemanager:*`` rules the Bicep CLI's built-in linter doesn't cover.

Mirrors three SonarSource rules with localised detection + agent-actionable
feedback:

  - **S6954** — empty object/array literals (``property: {}`` / ``property: []``)
    as property values. Either fill with meaningful config OR remove the
    property entirely.

  - **S6975 / S6956** — property order within a resource block. Canonical
    SonarSource order for Bicep resources::

        scope → parent → name/location → zones → sku → kind → scale → plan
        → identity → copy → dependsOn → tags → properties

    Violations: ``tags`` appearing BEFORE ``zones`` / ``sku`` / ``identity`` is
    the common pattern.

These are stylistic rules in Sonar's taxonomy but real code-quality signals:
empty objects encode "TODO" without commitment, and out-of-order properties
make resource intent harder to scan across the codebase.

The detector is line-based — it does not parse Bicep into an AST. The Bicep CLI
doesn't expose a Python-callable AST, and a regex line walker is sufficient for
these specific rules.

Enforcement model
-----------------------
A ``.bicep`` file that carries any finding is an offender. The consumer supplies
the scan ``roots`` (where its ``.bicep`` tree lives) via
``[tool.tc_fitness.core_checks.bicep_arm_lint]``; the ``.bicep`` extension is the
rule's domain-intrinsic default.

Ported from tc-agent-zone ``scripts/checks/bicep_arm_lint.py`` (SGO-297) and
re-expressed as a repo-agnostic, config-driven ``FitnessRule``: the detectors
are pure line walkers with zero repo identity, and every scan path arrives from
the consumer's config.
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
        "address each finding in the flagged .bicep file: for S6954 delete the "
        "empty-literal line OR populate it with the config the resource needs; "
        "for S6975/S6956 move the property to its canonical position "
        "(scope, parent, name, location, zones, sku, kind, scale, plan, identity, "
        "copy, dependsOn, tags, properties)."
    ),
    nxt="re-run this check to confirm the file is clean.",
    run="python -m tc_fitness.core_checks.bicep_arm_lint",
    passing="tags declared AFTER identity/sku; no `property: {}` empty literals",
    forbidden="tags declared BEFORE sku/identity, or a `property: {}` empty literal",
)

# Canonical SonarSource Bicep property order.
PROPERTY_ORDER = [
    "scope",
    "parent",
    "name",
    "location",
    "zones",
    "sku",
    "kind",
    "scale",
    "plan",
    "identity",
    "copy",
    "dependsOn",
    "tags",
    "properties",
]
PROPERTY_RANK = {name: i for i, name in enumerate(PROPERTY_ORDER)}

# Match `<prop>:` at the start of a (whitespace-indented) line.
PROP_LINE_RE = re.compile(r"^(\s+)([a-zA-Z_]\w*):")

# Match empty object/array literal at end of property line: `prop: {}` or `prop: []`
EMPTY_LITERAL_RE = re.compile(r"^\s+([a-zA-Z_]\w*):\s*[{\[]\s*[}\]]\s*$")

# Match a resource declaration opening: `resource <id> '<type>@<ver>' = {`
# We track these to scope our analysis to within a single resource block.
RESOURCE_OPEN_RE = re.compile(r"^\s*resource\s+\w+\s+'[^']+'\s*=\s*\{")


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x__empty_literal_findings__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__empty_literal_findings__mutmut)
def _empty_literal_findings(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 1: emit S6954 for every `prop: {}` / `prop: []` literal."""
    out: list[tuple[int, str, str]] = []
    for i, line in enumerate(lines, 1):
        m = EMPTY_LITERAL_RE.match(line)
        if not m:
            continue
        prop = m.group(1)
        out.append(
            (
                i,
                "S6954",
                f"empty literal on '{prop}': remove the property OR fill with meaningful content",
            )
        )
    return out


def x__empty_literal_findings__mutmut_orig(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 1: emit S6954 for every `prop: {}` / `prop: []` literal."""
    out: list[tuple[int, str, str]] = []
    for i, line in enumerate(lines, 1):
        m = EMPTY_LITERAL_RE.match(line)
        if not m:
            continue
        prop = m.group(1)
        out.append(
            (
                i,
                "S6954",
                f"empty literal on '{prop}': remove the property OR fill with meaningful content",
            )
        )
    return out


def x__empty_literal_findings__mutmut_1(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 1: emit S6954 for every `prop: {}` / `prop: []` literal."""
    out: list[tuple[int, str, str]] = None
    for i, line in enumerate(lines, 1):
        m = EMPTY_LITERAL_RE.match(line)
        if not m:
            continue
        prop = m.group(1)
        out.append(
            (
                i,
                "S6954",
                f"empty literal on '{prop}': remove the property OR fill with meaningful content",
            )
        )
    return out


def x__empty_literal_findings__mutmut_2(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 1: emit S6954 for every `prop: {}` / `prop: []` literal."""
    out: list[tuple[int, str, str]] = []
    for i, line in enumerate(None, 1):
        m = EMPTY_LITERAL_RE.match(line)
        if not m:
            continue
        prop = m.group(1)
        out.append(
            (
                i,
                "S6954",
                f"empty literal on '{prop}': remove the property OR fill with meaningful content",
            )
        )
    return out


def x__empty_literal_findings__mutmut_3(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 1: emit S6954 for every `prop: {}` / `prop: []` literal."""
    out: list[tuple[int, str, str]] = []
    for i, line in enumerate(lines, None):
        m = EMPTY_LITERAL_RE.match(line)
        if not m:
            continue
        prop = m.group(1)
        out.append(
            (
                i,
                "S6954",
                f"empty literal on '{prop}': remove the property OR fill with meaningful content",
            )
        )
    return out


def x__empty_literal_findings__mutmut_4(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 1: emit S6954 for every `prop: {}` / `prop: []` literal."""
    out: list[tuple[int, str, str]] = []
    for i, line in enumerate(1):
        m = EMPTY_LITERAL_RE.match(line)
        if not m:
            continue
        prop = m.group(1)
        out.append(
            (
                i,
                "S6954",
                f"empty literal on '{prop}': remove the property OR fill with meaningful content",
            )
        )
    return out


def x__empty_literal_findings__mutmut_5(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 1: emit S6954 for every `prop: {}` / `prop: []` literal."""
    out: list[tuple[int, str, str]] = []
    for i, line in enumerate(lines, ):
        m = EMPTY_LITERAL_RE.match(line)
        if not m:
            continue
        prop = m.group(1)
        out.append(
            (
                i,
                "S6954",
                f"empty literal on '{prop}': remove the property OR fill with meaningful content",
            )
        )
    return out


def x__empty_literal_findings__mutmut_6(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 1: emit S6954 for every `prop: {}` / `prop: []` literal."""
    out: list[tuple[int, str, str]] = []
    for i, line in enumerate(lines, 2):
        m = EMPTY_LITERAL_RE.match(line)
        if not m:
            continue
        prop = m.group(1)
        out.append(
            (
                i,
                "S6954",
                f"empty literal on '{prop}': remove the property OR fill with meaningful content",
            )
        )
    return out


def x__empty_literal_findings__mutmut_7(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 1: emit S6954 for every `prop: {}` / `prop: []` literal."""
    out: list[tuple[int, str, str]] = []
    for i, line in enumerate(lines, 1):
        m = None
        if not m:
            continue
        prop = m.group(1)
        out.append(
            (
                i,
                "S6954",
                f"empty literal on '{prop}': remove the property OR fill with meaningful content",
            )
        )
    return out


def x__empty_literal_findings__mutmut_8(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 1: emit S6954 for every `prop: {}` / `prop: []` literal."""
    out: list[tuple[int, str, str]] = []
    for i, line in enumerate(lines, 1):
        m = EMPTY_LITERAL_RE.match(None)
        if not m:
            continue
        prop = m.group(1)
        out.append(
            (
                i,
                "S6954",
                f"empty literal on '{prop}': remove the property OR fill with meaningful content",
            )
        )
    return out


def x__empty_literal_findings__mutmut_9(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 1: emit S6954 for every `prop: {}` / `prop: []` literal."""
    out: list[tuple[int, str, str]] = []
    for i, line in enumerate(lines, 1):
        m = EMPTY_LITERAL_RE.match(line)
        if m:
            continue
        prop = m.group(1)
        out.append(
            (
                i,
                "S6954",
                f"empty literal on '{prop}': remove the property OR fill with meaningful content",
            )
        )
    return out


def x__empty_literal_findings__mutmut_10(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 1: emit S6954 for every `prop: {}` / `prop: []` literal."""
    out: list[tuple[int, str, str]] = []
    for i, line in enumerate(lines, 1):
        m = EMPTY_LITERAL_RE.match(line)
        if not m:
            break
        prop = m.group(1)
        out.append(
            (
                i,
                "S6954",
                f"empty literal on '{prop}': remove the property OR fill with meaningful content",
            )
        )
    return out


def x__empty_literal_findings__mutmut_11(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 1: emit S6954 for every `prop: {}` / `prop: []` literal."""
    out: list[tuple[int, str, str]] = []
    for i, line in enumerate(lines, 1):
        m = EMPTY_LITERAL_RE.match(line)
        if not m:
            continue
        prop = None
        out.append(
            (
                i,
                "S6954",
                f"empty literal on '{prop}': remove the property OR fill with meaningful content",
            )
        )
    return out


def x__empty_literal_findings__mutmut_12(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 1: emit S6954 for every `prop: {}` / `prop: []` literal."""
    out: list[tuple[int, str, str]] = []
    for i, line in enumerate(lines, 1):
        m = EMPTY_LITERAL_RE.match(line)
        if not m:
            continue
        prop = m.group(None)
        out.append(
            (
                i,
                "S6954",
                f"empty literal on '{prop}': remove the property OR fill with meaningful content",
            )
        )
    return out


def x__empty_literal_findings__mutmut_13(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 1: emit S6954 for every `prop: {}` / `prop: []` literal."""
    out: list[tuple[int, str, str]] = []
    for i, line in enumerate(lines, 1):
        m = EMPTY_LITERAL_RE.match(line)
        if not m:
            continue
        prop = m.group(2)
        out.append(
            (
                i,
                "S6954",
                f"empty literal on '{prop}': remove the property OR fill with meaningful content",
            )
        )
    return out


def x__empty_literal_findings__mutmut_14(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 1: emit S6954 for every `prop: {}` / `prop: []` literal."""
    out: list[tuple[int, str, str]] = []
    for i, line in enumerate(lines, 1):
        m = EMPTY_LITERAL_RE.match(line)
        if not m:
            continue
        prop = m.group(1)
        out.append(
            None
        )
    return out


def x__empty_literal_findings__mutmut_15(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 1: emit S6954 for every `prop: {}` / `prop: []` literal."""
    out: list[tuple[int, str, str]] = []
    for i, line in enumerate(lines, 1):
        m = EMPTY_LITERAL_RE.match(line)
        if not m:
            continue
        prop = m.group(1)
        out.append(
            (
                i,
                "XXS6954XX",
                f"empty literal on '{prop}': remove the property OR fill with meaningful content",
            )
        )
    return out


def x__empty_literal_findings__mutmut_16(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 1: emit S6954 for every `prop: {}` / `prop: []` literal."""
    out: list[tuple[int, str, str]] = []
    for i, line in enumerate(lines, 1):
        m = EMPTY_LITERAL_RE.match(line)
        if not m:
            continue
        prop = m.group(1)
        out.append(
            (
                i,
                "s6954",
                f"empty literal on '{prop}': remove the property OR fill with meaningful content",
            )
        )
    return out

mutants_x__empty_literal_findings__mutmut['_mutmut_orig'] = x__empty_literal_findings__mutmut_orig # type: ignore # mutmut generated
mutants_x__empty_literal_findings__mutmut['x__empty_literal_findings__mutmut_1'] = x__empty_literal_findings__mutmut_1 # type: ignore # mutmut generated
mutants_x__empty_literal_findings__mutmut['x__empty_literal_findings__mutmut_2'] = x__empty_literal_findings__mutmut_2 # type: ignore # mutmut generated
mutants_x__empty_literal_findings__mutmut['x__empty_literal_findings__mutmut_3'] = x__empty_literal_findings__mutmut_3 # type: ignore # mutmut generated
mutants_x__empty_literal_findings__mutmut['x__empty_literal_findings__mutmut_4'] = x__empty_literal_findings__mutmut_4 # type: ignore # mutmut generated
mutants_x__empty_literal_findings__mutmut['x__empty_literal_findings__mutmut_5'] = x__empty_literal_findings__mutmut_5 # type: ignore # mutmut generated
mutants_x__empty_literal_findings__mutmut['x__empty_literal_findings__mutmut_6'] = x__empty_literal_findings__mutmut_6 # type: ignore # mutmut generated
mutants_x__empty_literal_findings__mutmut['x__empty_literal_findings__mutmut_7'] = x__empty_literal_findings__mutmut_7 # type: ignore # mutmut generated
mutants_x__empty_literal_findings__mutmut['x__empty_literal_findings__mutmut_8'] = x__empty_literal_findings__mutmut_8 # type: ignore # mutmut generated
mutants_x__empty_literal_findings__mutmut['x__empty_literal_findings__mutmut_9'] = x__empty_literal_findings__mutmut_9 # type: ignore # mutmut generated
mutants_x__empty_literal_findings__mutmut['x__empty_literal_findings__mutmut_10'] = x__empty_literal_findings__mutmut_10 # type: ignore # mutmut generated
mutants_x__empty_literal_findings__mutmut['x__empty_literal_findings__mutmut_11'] = x__empty_literal_findings__mutmut_11 # type: ignore # mutmut generated
mutants_x__empty_literal_findings__mutmut['x__empty_literal_findings__mutmut_12'] = x__empty_literal_findings__mutmut_12 # type: ignore # mutmut generated
mutants_x__empty_literal_findings__mutmut['x__empty_literal_findings__mutmut_13'] = x__empty_literal_findings__mutmut_13 # type: ignore # mutmut generated
mutants_x__empty_literal_findings__mutmut['x__empty_literal_findings__mutmut_14'] = x__empty_literal_findings__mutmut_14 # type: ignore # mutmut generated
mutants_x__empty_literal_findings__mutmut['x__empty_literal_findings__mutmut_15'] = x__empty_literal_findings__mutmut_15 # type: ignore # mutmut generated
mutants_x__empty_literal_findings__mutmut['x__empty_literal_findings__mutmut_16'] = x__empty_literal_findings__mutmut_16 # type: ignore # mutmut generated
mutants_x__canonical_predecessor__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__canonical_predecessor__mutmut)
def _canonical_predecessor(prop: str) -> str:
    """Name of the property that should immediately precede ``prop`` in canon."""
    rank = PROPERTY_RANK[prop]
    return PROPERTY_ORDER[rank - 1] if rank > 0 else "(start)"


def x__canonical_predecessor__mutmut_orig(prop: str) -> str:
    """Name of the property that should immediately precede ``prop`` in canon."""
    rank = PROPERTY_RANK[prop]
    return PROPERTY_ORDER[rank - 1] if rank > 0 else "(start)"


def x__canonical_predecessor__mutmut_1(prop: str) -> str:
    """Name of the property that should immediately precede ``prop`` in canon."""
    rank = None
    return PROPERTY_ORDER[rank - 1] if rank > 0 else "(start)"


def x__canonical_predecessor__mutmut_2(prop: str) -> str:
    """Name of the property that should immediately precede ``prop`` in canon."""
    rank = PROPERTY_RANK[prop]
    return PROPERTY_ORDER[rank + 1] if rank > 0 else "(start)"


def x__canonical_predecessor__mutmut_3(prop: str) -> str:
    """Name of the property that should immediately precede ``prop`` in canon."""
    rank = PROPERTY_RANK[prop]
    return PROPERTY_ORDER[rank - 2] if rank > 0 else "(start)"


def x__canonical_predecessor__mutmut_4(prop: str) -> str:
    """Name of the property that should immediately precede ``prop`` in canon."""
    rank = PROPERTY_RANK[prop]
    return PROPERTY_ORDER[rank - 1] if rank >= 0 else "(start)"


def x__canonical_predecessor__mutmut_5(prop: str) -> str:
    """Name of the property that should immediately precede ``prop`` in canon."""
    rank = PROPERTY_RANK[prop]
    return PROPERTY_ORDER[rank - 1] if rank > 1 else "(start)"


def x__canonical_predecessor__mutmut_6(prop: str) -> str:
    """Name of the property that should immediately precede ``prop`` in canon."""
    rank = PROPERTY_RANK[prop]
    return PROPERTY_ORDER[rank - 1] if rank > 0 else "XX(start)XX"


def x__canonical_predecessor__mutmut_7(prop: str) -> str:
    """Name of the property that should immediately precede ``prop`` in canon."""
    rank = PROPERTY_RANK[prop]
    return PROPERTY_ORDER[rank - 1] if rank > 0 else "(START)"

mutants_x__canonical_predecessor__mutmut['_mutmut_orig'] = x__canonical_predecessor__mutmut_orig # type: ignore # mutmut generated
mutants_x__canonical_predecessor__mutmut['x__canonical_predecessor__mutmut_1'] = x__canonical_predecessor__mutmut_1 # type: ignore # mutmut generated
mutants_x__canonical_predecessor__mutmut['x__canonical_predecessor__mutmut_2'] = x__canonical_predecessor__mutmut_2 # type: ignore # mutmut generated
mutants_x__canonical_predecessor__mutmut['x__canonical_predecessor__mutmut_3'] = x__canonical_predecessor__mutmut_3 # type: ignore # mutmut generated
mutants_x__canonical_predecessor__mutmut['x__canonical_predecessor__mutmut_4'] = x__canonical_predecessor__mutmut_4 # type: ignore # mutmut generated
mutants_x__canonical_predecessor__mutmut['x__canonical_predecessor__mutmut_5'] = x__canonical_predecessor__mutmut_5 # type: ignore # mutmut generated
mutants_x__canonical_predecessor__mutmut['x__canonical_predecessor__mutmut_6'] = x__canonical_predecessor__mutmut_6 # type: ignore # mutmut generated
mutants_x__canonical_predecessor__mutmut['x__canonical_predecessor__mutmut_7'] = x__canonical_predecessor__mutmut_7 # type: ignore # mutmut generated
mutants_x__order_violations_for_resource__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__order_violations_for_resource__mutmut)
def _order_violations_for_resource(
    seen: list[tuple[int, str]],
) -> list[tuple[int, str, str]]:
    """Emit S6975 findings for any pair of seen properties out of canonical order."""
    out: list[tuple[int, str, str]] = []
    for j in range(1, len(seen)):
        line_no, prop = seen[j]
        _prev_line, prev_prop = seen[j - 1]
        if PROPERTY_RANK[prop] >= PROPERTY_RANK[prev_prop]:
            continue
        out.append(
            (
                line_no,
                "S6975",
                f"property '{prop}' out of order — should come BEFORE '{prev_prop}' "
                f"per the canonical Bicep order (after '{_canonical_predecessor(prop)}')",
            )
        )
    return out


def x__order_violations_for_resource__mutmut_orig(
    seen: list[tuple[int, str]],
) -> list[tuple[int, str, str]]:
    """Emit S6975 findings for any pair of seen properties out of canonical order."""
    out: list[tuple[int, str, str]] = []
    for j in range(1, len(seen)):
        line_no, prop = seen[j]
        _prev_line, prev_prop = seen[j - 1]
        if PROPERTY_RANK[prop] >= PROPERTY_RANK[prev_prop]:
            continue
        out.append(
            (
                line_no,
                "S6975",
                f"property '{prop}' out of order — should come BEFORE '{prev_prop}' "
                f"per the canonical Bicep order (after '{_canonical_predecessor(prop)}')",
            )
        )
    return out


def x__order_violations_for_resource__mutmut_1(
    seen: list[tuple[int, str]],
) -> list[tuple[int, str, str]]:
    """Emit S6975 findings for any pair of seen properties out of canonical order."""
    out: list[tuple[int, str, str]] = None
    for j in range(1, len(seen)):
        line_no, prop = seen[j]
        _prev_line, prev_prop = seen[j - 1]
        if PROPERTY_RANK[prop] >= PROPERTY_RANK[prev_prop]:
            continue
        out.append(
            (
                line_no,
                "S6975",
                f"property '{prop}' out of order — should come BEFORE '{prev_prop}' "
                f"per the canonical Bicep order (after '{_canonical_predecessor(prop)}')",
            )
        )
    return out


def x__order_violations_for_resource__mutmut_2(
    seen: list[tuple[int, str]],
) -> list[tuple[int, str, str]]:
    """Emit S6975 findings for any pair of seen properties out of canonical order."""
    out: list[tuple[int, str, str]] = []
    for j in range(None, len(seen)):
        line_no, prop = seen[j]
        _prev_line, prev_prop = seen[j - 1]
        if PROPERTY_RANK[prop] >= PROPERTY_RANK[prev_prop]:
            continue
        out.append(
            (
                line_no,
                "S6975",
                f"property '{prop}' out of order — should come BEFORE '{prev_prop}' "
                f"per the canonical Bicep order (after '{_canonical_predecessor(prop)}')",
            )
        )
    return out


def x__order_violations_for_resource__mutmut_3(
    seen: list[tuple[int, str]],
) -> list[tuple[int, str, str]]:
    """Emit S6975 findings for any pair of seen properties out of canonical order."""
    out: list[tuple[int, str, str]] = []
    for j in range(1, None):
        line_no, prop = seen[j]
        _prev_line, prev_prop = seen[j - 1]
        if PROPERTY_RANK[prop] >= PROPERTY_RANK[prev_prop]:
            continue
        out.append(
            (
                line_no,
                "S6975",
                f"property '{prop}' out of order — should come BEFORE '{prev_prop}' "
                f"per the canonical Bicep order (after '{_canonical_predecessor(prop)}')",
            )
        )
    return out


def x__order_violations_for_resource__mutmut_4(
    seen: list[tuple[int, str]],
) -> list[tuple[int, str, str]]:
    """Emit S6975 findings for any pair of seen properties out of canonical order."""
    out: list[tuple[int, str, str]] = []
    for j in range(len(seen)):
        line_no, prop = seen[j]
        _prev_line, prev_prop = seen[j - 1]
        if PROPERTY_RANK[prop] >= PROPERTY_RANK[prev_prop]:
            continue
        out.append(
            (
                line_no,
                "S6975",
                f"property '{prop}' out of order — should come BEFORE '{prev_prop}' "
                f"per the canonical Bicep order (after '{_canonical_predecessor(prop)}')",
            )
        )
    return out


def x__order_violations_for_resource__mutmut_5(
    seen: list[tuple[int, str]],
) -> list[tuple[int, str, str]]:
    """Emit S6975 findings for any pair of seen properties out of canonical order."""
    out: list[tuple[int, str, str]] = []
    for j in range(1, ):
        line_no, prop = seen[j]
        _prev_line, prev_prop = seen[j - 1]
        if PROPERTY_RANK[prop] >= PROPERTY_RANK[prev_prop]:
            continue
        out.append(
            (
                line_no,
                "S6975",
                f"property '{prop}' out of order — should come BEFORE '{prev_prop}' "
                f"per the canonical Bicep order (after '{_canonical_predecessor(prop)}')",
            )
        )
    return out


def x__order_violations_for_resource__mutmut_6(
    seen: list[tuple[int, str]],
) -> list[tuple[int, str, str]]:
    """Emit S6975 findings for any pair of seen properties out of canonical order."""
    out: list[tuple[int, str, str]] = []
    for j in range(2, len(seen)):
        line_no, prop = seen[j]
        _prev_line, prev_prop = seen[j - 1]
        if PROPERTY_RANK[prop] >= PROPERTY_RANK[prev_prop]:
            continue
        out.append(
            (
                line_no,
                "S6975",
                f"property '{prop}' out of order — should come BEFORE '{prev_prop}' "
                f"per the canonical Bicep order (after '{_canonical_predecessor(prop)}')",
            )
        )
    return out


def x__order_violations_for_resource__mutmut_7(
    seen: list[tuple[int, str]],
) -> list[tuple[int, str, str]]:
    """Emit S6975 findings for any pair of seen properties out of canonical order."""
    out: list[tuple[int, str, str]] = []
    for j in range(1, len(seen)):
        line_no, prop = None
        _prev_line, prev_prop = seen[j - 1]
        if PROPERTY_RANK[prop] >= PROPERTY_RANK[prev_prop]:
            continue
        out.append(
            (
                line_no,
                "S6975",
                f"property '{prop}' out of order — should come BEFORE '{prev_prop}' "
                f"per the canonical Bicep order (after '{_canonical_predecessor(prop)}')",
            )
        )
    return out


def x__order_violations_for_resource__mutmut_8(
    seen: list[tuple[int, str]],
) -> list[tuple[int, str, str]]:
    """Emit S6975 findings for any pair of seen properties out of canonical order."""
    out: list[tuple[int, str, str]] = []
    for j in range(1, len(seen)):
        line_no, prop = seen[j]
        _prev_line, prev_prop = None
        if PROPERTY_RANK[prop] >= PROPERTY_RANK[prev_prop]:
            continue
        out.append(
            (
                line_no,
                "S6975",
                f"property '{prop}' out of order — should come BEFORE '{prev_prop}' "
                f"per the canonical Bicep order (after '{_canonical_predecessor(prop)}')",
            )
        )
    return out


def x__order_violations_for_resource__mutmut_9(
    seen: list[tuple[int, str]],
) -> list[tuple[int, str, str]]:
    """Emit S6975 findings for any pair of seen properties out of canonical order."""
    out: list[tuple[int, str, str]] = []
    for j in range(1, len(seen)):
        line_no, prop = seen[j]
        _prev_line, prev_prop = seen[j + 1]
        if PROPERTY_RANK[prop] >= PROPERTY_RANK[prev_prop]:
            continue
        out.append(
            (
                line_no,
                "S6975",
                f"property '{prop}' out of order — should come BEFORE '{prev_prop}' "
                f"per the canonical Bicep order (after '{_canonical_predecessor(prop)}')",
            )
        )
    return out


def x__order_violations_for_resource__mutmut_10(
    seen: list[tuple[int, str]],
) -> list[tuple[int, str, str]]:
    """Emit S6975 findings for any pair of seen properties out of canonical order."""
    out: list[tuple[int, str, str]] = []
    for j in range(1, len(seen)):
        line_no, prop = seen[j]
        _prev_line, prev_prop = seen[j - 2]
        if PROPERTY_RANK[prop] >= PROPERTY_RANK[prev_prop]:
            continue
        out.append(
            (
                line_no,
                "S6975",
                f"property '{prop}' out of order — should come BEFORE '{prev_prop}' "
                f"per the canonical Bicep order (after '{_canonical_predecessor(prop)}')",
            )
        )
    return out


def x__order_violations_for_resource__mutmut_11(
    seen: list[tuple[int, str]],
) -> list[tuple[int, str, str]]:
    """Emit S6975 findings for any pair of seen properties out of canonical order."""
    out: list[tuple[int, str, str]] = []
    for j in range(1, len(seen)):
        line_no, prop = seen[j]
        _prev_line, prev_prop = seen[j - 1]
        if PROPERTY_RANK[prop] > PROPERTY_RANK[prev_prop]:
            continue
        out.append(
            (
                line_no,
                "S6975",
                f"property '{prop}' out of order — should come BEFORE '{prev_prop}' "
                f"per the canonical Bicep order (after '{_canonical_predecessor(prop)}')",
            )
        )
    return out


def x__order_violations_for_resource__mutmut_12(
    seen: list[tuple[int, str]],
) -> list[tuple[int, str, str]]:
    """Emit S6975 findings for any pair of seen properties out of canonical order."""
    out: list[tuple[int, str, str]] = []
    for j in range(1, len(seen)):
        line_no, prop = seen[j]
        _prev_line, prev_prop = seen[j - 1]
        if PROPERTY_RANK[prop] >= PROPERTY_RANK[prev_prop]:
            break
        out.append(
            (
                line_no,
                "S6975",
                f"property '{prop}' out of order — should come BEFORE '{prev_prop}' "
                f"per the canonical Bicep order (after '{_canonical_predecessor(prop)}')",
            )
        )
    return out


def x__order_violations_for_resource__mutmut_13(
    seen: list[tuple[int, str]],
) -> list[tuple[int, str, str]]:
    """Emit S6975 findings for any pair of seen properties out of canonical order."""
    out: list[tuple[int, str, str]] = []
    for j in range(1, len(seen)):
        line_no, prop = seen[j]
        _prev_line, prev_prop = seen[j - 1]
        if PROPERTY_RANK[prop] >= PROPERTY_RANK[prev_prop]:
            continue
        out.append(
            None
        )
    return out


def x__order_violations_for_resource__mutmut_14(
    seen: list[tuple[int, str]],
) -> list[tuple[int, str, str]]:
    """Emit S6975 findings for any pair of seen properties out of canonical order."""
    out: list[tuple[int, str, str]] = []
    for j in range(1, len(seen)):
        line_no, prop = seen[j]
        _prev_line, prev_prop = seen[j - 1]
        if PROPERTY_RANK[prop] >= PROPERTY_RANK[prev_prop]:
            continue
        out.append(
            (
                line_no,
                "XXS6975XX",
                f"property '{prop}' out of order — should come BEFORE '{prev_prop}' "
                f"per the canonical Bicep order (after '{_canonical_predecessor(prop)}')",
            )
        )
    return out


def x__order_violations_for_resource__mutmut_15(
    seen: list[tuple[int, str]],
) -> list[tuple[int, str, str]]:
    """Emit S6975 findings for any pair of seen properties out of canonical order."""
    out: list[tuple[int, str, str]] = []
    for j in range(1, len(seen)):
        line_no, prop = seen[j]
        _prev_line, prev_prop = seen[j - 1]
        if PROPERTY_RANK[prop] >= PROPERTY_RANK[prev_prop]:
            continue
        out.append(
            (
                line_no,
                "s6975",
                f"property '{prop}' out of order — should come BEFORE '{prev_prop}' "
                f"per the canonical Bicep order (after '{_canonical_predecessor(prop)}')",
            )
        )
    return out


def x__order_violations_for_resource__mutmut_16(
    seen: list[tuple[int, str]],
) -> list[tuple[int, str, str]]:
    """Emit S6975 findings for any pair of seen properties out of canonical order."""
    out: list[tuple[int, str, str]] = []
    for j in range(1, len(seen)):
        line_no, prop = seen[j]
        _prev_line, prev_prop = seen[j - 1]
        if PROPERTY_RANK[prop] >= PROPERTY_RANK[prev_prop]:
            continue
        out.append(
            (
                line_no,
                "S6975",
                f"property '{prop}' out of order — should come BEFORE '{prev_prop}' "
                f"per the canonical Bicep order (after '{_canonical_predecessor(None)}')",
            )
        )
    return out

mutants_x__order_violations_for_resource__mutmut['_mutmut_orig'] = x__order_violations_for_resource__mutmut_orig # type: ignore # mutmut generated
mutants_x__order_violations_for_resource__mutmut['x__order_violations_for_resource__mutmut_1'] = x__order_violations_for_resource__mutmut_1 # type: ignore # mutmut generated
mutants_x__order_violations_for_resource__mutmut['x__order_violations_for_resource__mutmut_2'] = x__order_violations_for_resource__mutmut_2 # type: ignore # mutmut generated
mutants_x__order_violations_for_resource__mutmut['x__order_violations_for_resource__mutmut_3'] = x__order_violations_for_resource__mutmut_3 # type: ignore # mutmut generated
mutants_x__order_violations_for_resource__mutmut['x__order_violations_for_resource__mutmut_4'] = x__order_violations_for_resource__mutmut_4 # type: ignore # mutmut generated
mutants_x__order_violations_for_resource__mutmut['x__order_violations_for_resource__mutmut_5'] = x__order_violations_for_resource__mutmut_5 # type: ignore # mutmut generated
mutants_x__order_violations_for_resource__mutmut['x__order_violations_for_resource__mutmut_6'] = x__order_violations_for_resource__mutmut_6 # type: ignore # mutmut generated
mutants_x__order_violations_for_resource__mutmut['x__order_violations_for_resource__mutmut_7'] = x__order_violations_for_resource__mutmut_7 # type: ignore # mutmut generated
mutants_x__order_violations_for_resource__mutmut['x__order_violations_for_resource__mutmut_8'] = x__order_violations_for_resource__mutmut_8 # type: ignore # mutmut generated
mutants_x__order_violations_for_resource__mutmut['x__order_violations_for_resource__mutmut_9'] = x__order_violations_for_resource__mutmut_9 # type: ignore # mutmut generated
mutants_x__order_violations_for_resource__mutmut['x__order_violations_for_resource__mutmut_10'] = x__order_violations_for_resource__mutmut_10 # type: ignore # mutmut generated
mutants_x__order_violations_for_resource__mutmut['x__order_violations_for_resource__mutmut_11'] = x__order_violations_for_resource__mutmut_11 # type: ignore # mutmut generated
mutants_x__order_violations_for_resource__mutmut['x__order_violations_for_resource__mutmut_12'] = x__order_violations_for_resource__mutmut_12 # type: ignore # mutmut generated
mutants_x__order_violations_for_resource__mutmut['x__order_violations_for_resource__mutmut_13'] = x__order_violations_for_resource__mutmut_13 # type: ignore # mutmut generated
mutants_x__order_violations_for_resource__mutmut['x__order_violations_for_resource__mutmut_14'] = x__order_violations_for_resource__mutmut_14 # type: ignore # mutmut generated
mutants_x__order_violations_for_resource__mutmut['x__order_violations_for_resource__mutmut_15'] = x__order_violations_for_resource__mutmut_15 # type: ignore # mutmut generated
mutants_x__order_violations_for_resource__mutmut['x__order_violations_for_resource__mutmut_16'] = x__order_violations_for_resource__mutmut_16 # type: ignore # mutmut generated
mutants_x__top_level_prop__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__top_level_prop__mutmut)
def _top_level_prop(line: str, resource_indent: int | None) -> tuple[str | None, int | None]:
    """Return ``(prop_name, snapped_indent)`` if ``line`` is a top-level resource prop.

    ``prop_name`` is ``None`` when the line isn't a prop OR is nested deeper
    than the resource's top level. ``snapped_indent`` is the value the caller
    should adopt as ``resource_indent`` if it was previously ``None``.
    """
    m = PROP_LINE_RE.match(line)
    if not m:
        return None, resource_indent
    indent, prop = m.group(1), m.group(2)
    indent_len = len(indent.expandtabs(2))
    snapped = indent_len if resource_indent is None else resource_indent
    if indent_len != snapped:
        return None, snapped
    if prop not in PROPERTY_RANK:
        return None, snapped
    return prop, snapped


def x__top_level_prop__mutmut_orig(line: str, resource_indent: int | None) -> tuple[str | None, int | None]:
    """Return ``(prop_name, snapped_indent)`` if ``line`` is a top-level resource prop.

    ``prop_name`` is ``None`` when the line isn't a prop OR is nested deeper
    than the resource's top level. ``snapped_indent`` is the value the caller
    should adopt as ``resource_indent`` if it was previously ``None``.
    """
    m = PROP_LINE_RE.match(line)
    if not m:
        return None, resource_indent
    indent, prop = m.group(1), m.group(2)
    indent_len = len(indent.expandtabs(2))
    snapped = indent_len if resource_indent is None else resource_indent
    if indent_len != snapped:
        return None, snapped
    if prop not in PROPERTY_RANK:
        return None, snapped
    return prop, snapped


def x__top_level_prop__mutmut_1(line: str, resource_indent: int | None) -> tuple[str | None, int | None]:
    """Return ``(prop_name, snapped_indent)`` if ``line`` is a top-level resource prop.

    ``prop_name`` is ``None`` when the line isn't a prop OR is nested deeper
    than the resource's top level. ``snapped_indent`` is the value the caller
    should adopt as ``resource_indent`` if it was previously ``None``.
    """
    m = None
    if not m:
        return None, resource_indent
    indent, prop = m.group(1), m.group(2)
    indent_len = len(indent.expandtabs(2))
    snapped = indent_len if resource_indent is None else resource_indent
    if indent_len != snapped:
        return None, snapped
    if prop not in PROPERTY_RANK:
        return None, snapped
    return prop, snapped


def x__top_level_prop__mutmut_2(line: str, resource_indent: int | None) -> tuple[str | None, int | None]:
    """Return ``(prop_name, snapped_indent)`` if ``line`` is a top-level resource prop.

    ``prop_name`` is ``None`` when the line isn't a prop OR is nested deeper
    than the resource's top level. ``snapped_indent`` is the value the caller
    should adopt as ``resource_indent`` if it was previously ``None``.
    """
    m = PROP_LINE_RE.match(None)
    if not m:
        return None, resource_indent
    indent, prop = m.group(1), m.group(2)
    indent_len = len(indent.expandtabs(2))
    snapped = indent_len if resource_indent is None else resource_indent
    if indent_len != snapped:
        return None, snapped
    if prop not in PROPERTY_RANK:
        return None, snapped
    return prop, snapped


def x__top_level_prop__mutmut_3(line: str, resource_indent: int | None) -> tuple[str | None, int | None]:
    """Return ``(prop_name, snapped_indent)`` if ``line`` is a top-level resource prop.

    ``prop_name`` is ``None`` when the line isn't a prop OR is nested deeper
    than the resource's top level. ``snapped_indent`` is the value the caller
    should adopt as ``resource_indent`` if it was previously ``None``.
    """
    m = PROP_LINE_RE.match(line)
    if m:
        return None, resource_indent
    indent, prop = m.group(1), m.group(2)
    indent_len = len(indent.expandtabs(2))
    snapped = indent_len if resource_indent is None else resource_indent
    if indent_len != snapped:
        return None, snapped
    if prop not in PROPERTY_RANK:
        return None, snapped
    return prop, snapped


def x__top_level_prop__mutmut_4(line: str, resource_indent: int | None) -> tuple[str | None, int | None]:
    """Return ``(prop_name, snapped_indent)`` if ``line`` is a top-level resource prop.

    ``prop_name`` is ``None`` when the line isn't a prop OR is nested deeper
    than the resource's top level. ``snapped_indent`` is the value the caller
    should adopt as ``resource_indent`` if it was previously ``None``.
    """
    m = PROP_LINE_RE.match(line)
    if not m:
        return None, resource_indent
    indent, prop = None
    indent_len = len(indent.expandtabs(2))
    snapped = indent_len if resource_indent is None else resource_indent
    if indent_len != snapped:
        return None, snapped
    if prop not in PROPERTY_RANK:
        return None, snapped
    return prop, snapped


def x__top_level_prop__mutmut_5(line: str, resource_indent: int | None) -> tuple[str | None, int | None]:
    """Return ``(prop_name, snapped_indent)`` if ``line`` is a top-level resource prop.

    ``prop_name`` is ``None`` when the line isn't a prop OR is nested deeper
    than the resource's top level. ``snapped_indent`` is the value the caller
    should adopt as ``resource_indent`` if it was previously ``None``.
    """
    m = PROP_LINE_RE.match(line)
    if not m:
        return None, resource_indent
    indent, prop = m.group(None), m.group(2)
    indent_len = len(indent.expandtabs(2))
    snapped = indent_len if resource_indent is None else resource_indent
    if indent_len != snapped:
        return None, snapped
    if prop not in PROPERTY_RANK:
        return None, snapped
    return prop, snapped


def x__top_level_prop__mutmut_6(line: str, resource_indent: int | None) -> tuple[str | None, int | None]:
    """Return ``(prop_name, snapped_indent)`` if ``line`` is a top-level resource prop.

    ``prop_name`` is ``None`` when the line isn't a prop OR is nested deeper
    than the resource's top level. ``snapped_indent`` is the value the caller
    should adopt as ``resource_indent`` if it was previously ``None``.
    """
    m = PROP_LINE_RE.match(line)
    if not m:
        return None, resource_indent
    indent, prop = m.group(2), m.group(2)
    indent_len = len(indent.expandtabs(2))
    snapped = indent_len if resource_indent is None else resource_indent
    if indent_len != snapped:
        return None, snapped
    if prop not in PROPERTY_RANK:
        return None, snapped
    return prop, snapped


def x__top_level_prop__mutmut_7(line: str, resource_indent: int | None) -> tuple[str | None, int | None]:
    """Return ``(prop_name, snapped_indent)`` if ``line`` is a top-level resource prop.

    ``prop_name`` is ``None`` when the line isn't a prop OR is nested deeper
    than the resource's top level. ``snapped_indent`` is the value the caller
    should adopt as ``resource_indent`` if it was previously ``None``.
    """
    m = PROP_LINE_RE.match(line)
    if not m:
        return None, resource_indent
    indent, prop = m.group(1), m.group(None)
    indent_len = len(indent.expandtabs(2))
    snapped = indent_len if resource_indent is None else resource_indent
    if indent_len != snapped:
        return None, snapped
    if prop not in PROPERTY_RANK:
        return None, snapped
    return prop, snapped


def x__top_level_prop__mutmut_8(line: str, resource_indent: int | None) -> tuple[str | None, int | None]:
    """Return ``(prop_name, snapped_indent)`` if ``line`` is a top-level resource prop.

    ``prop_name`` is ``None`` when the line isn't a prop OR is nested deeper
    than the resource's top level. ``snapped_indent`` is the value the caller
    should adopt as ``resource_indent`` if it was previously ``None``.
    """
    m = PROP_LINE_RE.match(line)
    if not m:
        return None, resource_indent
    indent, prop = m.group(1), m.group(3)
    indent_len = len(indent.expandtabs(2))
    snapped = indent_len if resource_indent is None else resource_indent
    if indent_len != snapped:
        return None, snapped
    if prop not in PROPERTY_RANK:
        return None, snapped
    return prop, snapped


def x__top_level_prop__mutmut_9(line: str, resource_indent: int | None) -> tuple[str | None, int | None]:
    """Return ``(prop_name, snapped_indent)`` if ``line`` is a top-level resource prop.

    ``prop_name`` is ``None`` when the line isn't a prop OR is nested deeper
    than the resource's top level. ``snapped_indent`` is the value the caller
    should adopt as ``resource_indent`` if it was previously ``None``.
    """
    m = PROP_LINE_RE.match(line)
    if not m:
        return None, resource_indent
    indent, prop = m.group(1), m.group(2)
    indent_len = None
    snapped = indent_len if resource_indent is None else resource_indent
    if indent_len != snapped:
        return None, snapped
    if prop not in PROPERTY_RANK:
        return None, snapped
    return prop, snapped


def x__top_level_prop__mutmut_10(line: str, resource_indent: int | None) -> tuple[str | None, int | None]:
    """Return ``(prop_name, snapped_indent)`` if ``line`` is a top-level resource prop.

    ``prop_name`` is ``None`` when the line isn't a prop OR is nested deeper
    than the resource's top level. ``snapped_indent`` is the value the caller
    should adopt as ``resource_indent`` if it was previously ``None``.
    """
    m = PROP_LINE_RE.match(line)
    if not m:
        return None, resource_indent
    indent, prop = m.group(1), m.group(2)
    indent_len = len(indent.expandtabs(2))
    snapped = None
    if indent_len != snapped:
        return None, snapped
    if prop not in PROPERTY_RANK:
        return None, snapped
    return prop, snapped


def x__top_level_prop__mutmut_11(line: str, resource_indent: int | None) -> tuple[str | None, int | None]:
    """Return ``(prop_name, snapped_indent)`` if ``line`` is a top-level resource prop.

    ``prop_name`` is ``None`` when the line isn't a prop OR is nested deeper
    than the resource's top level. ``snapped_indent`` is the value the caller
    should adopt as ``resource_indent`` if it was previously ``None``.
    """
    m = PROP_LINE_RE.match(line)
    if not m:
        return None, resource_indent
    indent, prop = m.group(1), m.group(2)
    indent_len = len(indent.expandtabs(2))
    snapped = indent_len if resource_indent is not None else resource_indent
    if indent_len != snapped:
        return None, snapped
    if prop not in PROPERTY_RANK:
        return None, snapped
    return prop, snapped


def x__top_level_prop__mutmut_12(line: str, resource_indent: int | None) -> tuple[str | None, int | None]:
    """Return ``(prop_name, snapped_indent)`` if ``line`` is a top-level resource prop.

    ``prop_name`` is ``None`` when the line isn't a prop OR is nested deeper
    than the resource's top level. ``snapped_indent`` is the value the caller
    should adopt as ``resource_indent`` if it was previously ``None``.
    """
    m = PROP_LINE_RE.match(line)
    if not m:
        return None, resource_indent
    indent, prop = m.group(1), m.group(2)
    indent_len = len(indent.expandtabs(2))
    snapped = indent_len if resource_indent is None else resource_indent
    if indent_len == snapped:
        return None, snapped
    if prop not in PROPERTY_RANK:
        return None, snapped
    return prop, snapped


def x__top_level_prop__mutmut_13(line: str, resource_indent: int | None) -> tuple[str | None, int | None]:
    """Return ``(prop_name, snapped_indent)`` if ``line`` is a top-level resource prop.

    ``prop_name`` is ``None`` when the line isn't a prop OR is nested deeper
    than the resource's top level. ``snapped_indent`` is the value the caller
    should adopt as ``resource_indent`` if it was previously ``None``.
    """
    m = PROP_LINE_RE.match(line)
    if not m:
        return None, resource_indent
    indent, prop = m.group(1), m.group(2)
    indent_len = len(indent.expandtabs(2))
    snapped = indent_len if resource_indent is None else resource_indent
    if indent_len != snapped:
        return None, snapped
    if prop in PROPERTY_RANK:
        return None, snapped
    return prop, snapped

mutants_x__top_level_prop__mutmut['_mutmut_orig'] = x__top_level_prop__mutmut_orig # type: ignore # mutmut generated
mutants_x__top_level_prop__mutmut['x__top_level_prop__mutmut_1'] = x__top_level_prop__mutmut_1 # type: ignore # mutmut generated
mutants_x__top_level_prop__mutmut['x__top_level_prop__mutmut_2'] = x__top_level_prop__mutmut_2 # type: ignore # mutmut generated
mutants_x__top_level_prop__mutmut['x__top_level_prop__mutmut_3'] = x__top_level_prop__mutmut_3 # type: ignore # mutmut generated
mutants_x__top_level_prop__mutmut['x__top_level_prop__mutmut_4'] = x__top_level_prop__mutmut_4 # type: ignore # mutmut generated
mutants_x__top_level_prop__mutmut['x__top_level_prop__mutmut_5'] = x__top_level_prop__mutmut_5 # type: ignore # mutmut generated
mutants_x__top_level_prop__mutmut['x__top_level_prop__mutmut_6'] = x__top_level_prop__mutmut_6 # type: ignore # mutmut generated
mutants_x__top_level_prop__mutmut['x__top_level_prop__mutmut_7'] = x__top_level_prop__mutmut_7 # type: ignore # mutmut generated
mutants_x__top_level_prop__mutmut['x__top_level_prop__mutmut_8'] = x__top_level_prop__mutmut_8 # type: ignore # mutmut generated
mutants_x__top_level_prop__mutmut['x__top_level_prop__mutmut_9'] = x__top_level_prop__mutmut_9 # type: ignore # mutmut generated
mutants_x__top_level_prop__mutmut['x__top_level_prop__mutmut_10'] = x__top_level_prop__mutmut_10 # type: ignore # mutmut generated
mutants_x__top_level_prop__mutmut['x__top_level_prop__mutmut_11'] = x__top_level_prop__mutmut_11 # type: ignore # mutmut generated
mutants_x__top_level_prop__mutmut['x__top_level_prop__mutmut_12'] = x__top_level_prop__mutmut_12 # type: ignore # mutmut generated
mutants_x__top_level_prop__mutmut['x__top_level_prop__mutmut_13'] = x__top_level_prop__mutmut_13 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__property_order_findings__mutmut)
def _property_order_findings(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_orig(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_1(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = None
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_2(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = None
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_3(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 1
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_4(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = None
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_5(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = True
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_6(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = ""
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_7(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = None

    for i, line in enumerate(lines, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_8(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(None, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_9(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, None):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_10(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_11(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, ):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_12(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 2):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_13(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_14(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(None):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_15(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = None
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_16(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = False
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_17(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = None
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_18(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 2
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_19(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = ""
                seen = []
            continue
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_20(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = None
            continue
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_21(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = []
            break
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_22(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth = line.count("{") - line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_23(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth -= line.count("{") - line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_24(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count("{") + line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_25(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count(None) - line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_26(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count("XX{XX") - line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_27(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count("{") - line.count(None)
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_28(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count("{") - line.count("XX}XX")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_29(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count("{") - line.count("}")
        if brace_depth < 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_30(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 1:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_31(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0:
            out.extend(None)
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_32(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(None))
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_33(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = None
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_34(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = True
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_35(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = None
            continue
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_36(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 1
            continue
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_37(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 0
            break
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_38(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = None
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_39(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(None, resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_40(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(line, None)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_41(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(resource_indent)
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_42(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(line, )
        if prop is not None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_43(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is None:
            seen.append((i, prop))
    return out


def x__property_order_findings__mutmut_44(lines: list[str]) -> list[tuple[int, str, str]]:
    """Pass 2: walk each resource block, collecting prop order violations."""
    out: list[tuple[int, str, str]] = []
    brace_depth = 0
    in_resource = False
    resource_indent: int | None = None
    seen: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        if not in_resource:
            if RESOURCE_OPEN_RE.match(line):
                in_resource = True
                brace_depth = 1
                resource_indent = None
                seen = []
            continue
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0:
            out.extend(_order_violations_for_resource(seen))
            in_resource = False
            brace_depth = 0
            continue
        prop, resource_indent = _top_level_prop(line, resource_indent)
        if prop is not None:
            seen.append(None)
    return out

mutants_x__property_order_findings__mutmut['_mutmut_orig'] = x__property_order_findings__mutmut_orig # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_1'] = x__property_order_findings__mutmut_1 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_2'] = x__property_order_findings__mutmut_2 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_3'] = x__property_order_findings__mutmut_3 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_4'] = x__property_order_findings__mutmut_4 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_5'] = x__property_order_findings__mutmut_5 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_6'] = x__property_order_findings__mutmut_6 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_7'] = x__property_order_findings__mutmut_7 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_8'] = x__property_order_findings__mutmut_8 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_9'] = x__property_order_findings__mutmut_9 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_10'] = x__property_order_findings__mutmut_10 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_11'] = x__property_order_findings__mutmut_11 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_12'] = x__property_order_findings__mutmut_12 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_13'] = x__property_order_findings__mutmut_13 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_14'] = x__property_order_findings__mutmut_14 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_15'] = x__property_order_findings__mutmut_15 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_16'] = x__property_order_findings__mutmut_16 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_17'] = x__property_order_findings__mutmut_17 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_18'] = x__property_order_findings__mutmut_18 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_19'] = x__property_order_findings__mutmut_19 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_20'] = x__property_order_findings__mutmut_20 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_21'] = x__property_order_findings__mutmut_21 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_22'] = x__property_order_findings__mutmut_22 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_23'] = x__property_order_findings__mutmut_23 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_24'] = x__property_order_findings__mutmut_24 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_25'] = x__property_order_findings__mutmut_25 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_26'] = x__property_order_findings__mutmut_26 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_27'] = x__property_order_findings__mutmut_27 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_28'] = x__property_order_findings__mutmut_28 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_29'] = x__property_order_findings__mutmut_29 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_30'] = x__property_order_findings__mutmut_30 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_31'] = x__property_order_findings__mutmut_31 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_32'] = x__property_order_findings__mutmut_32 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_33'] = x__property_order_findings__mutmut_33 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_34'] = x__property_order_findings__mutmut_34 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_35'] = x__property_order_findings__mutmut_35 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_36'] = x__property_order_findings__mutmut_36 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_37'] = x__property_order_findings__mutmut_37 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_38'] = x__property_order_findings__mutmut_38 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_39'] = x__property_order_findings__mutmut_39 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_40'] = x__property_order_findings__mutmut_40 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_41'] = x__property_order_findings__mutmut_41 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_42'] = x__property_order_findings__mutmut_42 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_43'] = x__property_order_findings__mutmut_43 # type: ignore # mutmut generated
mutants_x__property_order_findings__mutmut['x__property_order_findings__mutmut_44'] = x__property_order_findings__mutmut_44 # type: ignore # mutmut generated
mutants_x_bicep_findings__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_bicep_findings__mutmut)
def bicep_findings(path: Path) -> list[tuple[int, str, str]]:
    """Return the ``(line_no, rule, message)`` findings for one ``.bicep`` file.

    The pure detection core (the analogue of ``module_has_duplicate`` in the
    exemplar): tests assert on it directly. Two passes — empty literals (S6954)
    then property order (S6975) — over the file's lines. A file that cannot be
    read as UTF-8 yields no findings (another concern owns unreadable files).
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return []
    return _empty_literal_findings(lines) + _property_order_findings(lines)


def x_bicep_findings__mutmut_orig(path: Path) -> list[tuple[int, str, str]]:
    """Return the ``(line_no, rule, message)`` findings for one ``.bicep`` file.

    The pure detection core (the analogue of ``module_has_duplicate`` in the
    exemplar): tests assert on it directly. Two passes — empty literals (S6954)
    then property order (S6975) — over the file's lines. A file that cannot be
    read as UTF-8 yields no findings (another concern owns unreadable files).
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return []
    return _empty_literal_findings(lines) + _property_order_findings(lines)


def x_bicep_findings__mutmut_1(path: Path) -> list[tuple[int, str, str]]:
    """Return the ``(line_no, rule, message)`` findings for one ``.bicep`` file.

    The pure detection core (the analogue of ``module_has_duplicate`` in the
    exemplar): tests assert on it directly. Two passes — empty literals (S6954)
    then property order (S6975) — over the file's lines. A file that cannot be
    read as UTF-8 yields no findings (another concern owns unreadable files).
    """
    try:
        lines = None
    except (OSError, UnicodeDecodeError):
        return []
    return _empty_literal_findings(lines) + _property_order_findings(lines)


def x_bicep_findings__mutmut_2(path: Path) -> list[tuple[int, str, str]]:
    """Return the ``(line_no, rule, message)`` findings for one ``.bicep`` file.

    The pure detection core (the analogue of ``module_has_duplicate`` in the
    exemplar): tests assert on it directly. Two passes — empty literals (S6954)
    then property order (S6975) — over the file's lines. A file that cannot be
    read as UTF-8 yields no findings (another concern owns unreadable files).
    """
    try:
        lines = path.read_text(encoding=None).splitlines()
    except (OSError, UnicodeDecodeError):
        return []
    return _empty_literal_findings(lines) + _property_order_findings(lines)


def x_bicep_findings__mutmut_3(path: Path) -> list[tuple[int, str, str]]:
    """Return the ``(line_no, rule, message)`` findings for one ``.bicep`` file.

    The pure detection core (the analogue of ``module_has_duplicate`` in the
    exemplar): tests assert on it directly. Two passes — empty literals (S6954)
    then property order (S6975) — over the file's lines. A file that cannot be
    read as UTF-8 yields no findings (another concern owns unreadable files).
    """
    try:
        lines = path.read_text(encoding="XXutf-8XX").splitlines()
    except (OSError, UnicodeDecodeError):
        return []
    return _empty_literal_findings(lines) + _property_order_findings(lines)


def x_bicep_findings__mutmut_4(path: Path) -> list[tuple[int, str, str]]:
    """Return the ``(line_no, rule, message)`` findings for one ``.bicep`` file.

    The pure detection core (the analogue of ``module_has_duplicate`` in the
    exemplar): tests assert on it directly. Two passes — empty literals (S6954)
    then property order (S6975) — over the file's lines. A file that cannot be
    read as UTF-8 yields no findings (another concern owns unreadable files).
    """
    try:
        lines = path.read_text(encoding="UTF-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return []
    return _empty_literal_findings(lines) + _property_order_findings(lines)


def x_bicep_findings__mutmut_5(path: Path) -> list[tuple[int, str, str]]:
    """Return the ``(line_no, rule, message)`` findings for one ``.bicep`` file.

    The pure detection core (the analogue of ``module_has_duplicate`` in the
    exemplar): tests assert on it directly. Two passes — empty literals (S6954)
    then property order (S6975) — over the file's lines. A file that cannot be
    read as UTF-8 yields no findings (another concern owns unreadable files).
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return []
    return _empty_literal_findings(lines) - _property_order_findings(lines)


def x_bicep_findings__mutmut_6(path: Path) -> list[tuple[int, str, str]]:
    """Return the ``(line_no, rule, message)`` findings for one ``.bicep`` file.

    The pure detection core (the analogue of ``module_has_duplicate`` in the
    exemplar): tests assert on it directly. Two passes — empty literals (S6954)
    then property order (S6975) — over the file's lines. A file that cannot be
    read as UTF-8 yields no findings (another concern owns unreadable files).
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return []
    return _empty_literal_findings(None) + _property_order_findings(lines)


def x_bicep_findings__mutmut_7(path: Path) -> list[tuple[int, str, str]]:
    """Return the ``(line_no, rule, message)`` findings for one ``.bicep`` file.

    The pure detection core (the analogue of ``module_has_duplicate`` in the
    exemplar): tests assert on it directly. Two passes — empty literals (S6954)
    then property order (S6975) — over the file's lines. A file that cannot be
    read as UTF-8 yields no findings (another concern owns unreadable files).
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return []
    return _empty_literal_findings(lines) + _property_order_findings(None)

mutants_x_bicep_findings__mutmut['_mutmut_orig'] = x_bicep_findings__mutmut_orig # type: ignore # mutmut generated
mutants_x_bicep_findings__mutmut['x_bicep_findings__mutmut_1'] = x_bicep_findings__mutmut_1 # type: ignore # mutmut generated
mutants_x_bicep_findings__mutmut['x_bicep_findings__mutmut_2'] = x_bicep_findings__mutmut_2 # type: ignore # mutmut generated
mutants_x_bicep_findings__mutmut['x_bicep_findings__mutmut_3'] = x_bicep_findings__mutmut_3 # type: ignore # mutmut generated
mutants_x_bicep_findings__mutmut['x_bicep_findings__mutmut_4'] = x_bicep_findings__mutmut_4 # type: ignore # mutmut generated
mutants_x_bicep_findings__mutmut['x_bicep_findings__mutmut_5'] = x_bicep_findings__mutmut_5 # type: ignore # mutmut generated
mutants_x_bicep_findings__mutmut['x_bicep_findings__mutmut_6'] = x_bicep_findings__mutmut_6 # type: ignore # mutmut generated
mutants_x_bicep_findings__mutmut['x_bicep_findings__mutmut_7'] = x_bicep_findings__mutmut_7 # type: ignore # mutmut generated
mutants_xǁBicepArmLintǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁBicepArmLintǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore


class BicepArmLint(FitnessRule):
    """Flags ``.bicep`` files with ARM-lint findings (Sonar S6954/S6975/S6956)."""

    name = "bicep-arm-lint"
    remediation = REMEDIATION
    extensions = (".bicep",)

    @classmethod
    @_mutmut_mutated(mutants_xǁBicepArmLintǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> BicepArmLint:
        """Build from config (narrowed return for mypy — no extra knobs)."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, BicepArmLint)  # noqa: S101  # narrowing for mypy
        return rule

    @classmethod
    def xǁBicepArmLintǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> BicepArmLint:
        """Build from config (narrowed return for mypy — no extra knobs)."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, BicepArmLint)  # noqa: S101  # narrowing for mypy
        return rule

    @classmethod
    def xǁBicepArmLintǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> BicepArmLint:
        """Build from config (narrowed return for mypy — no extra knobs)."""
        rule = None
        assert isinstance(rule, BicepArmLint)  # noqa: S101  # narrowing for mypy
        return rule

    @classmethod
    def xǁBicepArmLintǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> BicepArmLint:
        """Build from config (narrowed return for mypy — no extra knobs)."""
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, BicepArmLint)  # noqa: S101  # narrowing for mypy
        return rule

    @classmethod
    def xǁBicepArmLintǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> BicepArmLint:
        """Build from config (narrowed return for mypy — no extra knobs)."""
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, BicepArmLint)  # noqa: S101  # narrowing for mypy
        return rule

    @classmethod
    def xǁBicepArmLintǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> BicepArmLint:
        """Build from config (narrowed return for mypy — no extra knobs)."""
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, BicepArmLint)  # noqa: S101  # narrowing for mypy
        return rule

    @classmethod
    def xǁBicepArmLintǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> BicepArmLint:
        """Build from config (narrowed return for mypy — no extra knobs)."""
        rule = super().from_config(config, )
        assert isinstance(rule, BicepArmLint)  # noqa: S101  # narrowing for mypy
        return rule

    @_mutmut_mutated(mutants_xǁBicepArmLintǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        return bool(bicep_findings(path))

    def xǁBicepArmLintǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        return bool(bicep_findings(path))

    def xǁBicepArmLintǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        return bool(None)

    def xǁBicepArmLintǁfile_has_violation__mutmut_2(self, path: Path) -> bool:
        return bool(bicep_findings(None))

mutants_xǁBicepArmLintǁfrom_config__mutmut['_mutmut_orig'] = BicepArmLint.xǁBicepArmLintǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁBicepArmLintǁfrom_config__mutmut['xǁBicepArmLintǁfrom_config__mutmut_1'] = BicepArmLint.xǁBicepArmLintǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁBicepArmLintǁfrom_config__mutmut['xǁBicepArmLintǁfrom_config__mutmut_2'] = BicepArmLint.xǁBicepArmLintǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁBicepArmLintǁfrom_config__mutmut['xǁBicepArmLintǁfrom_config__mutmut_3'] = BicepArmLint.xǁBicepArmLintǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁBicepArmLintǁfrom_config__mutmut['xǁBicepArmLintǁfrom_config__mutmut_4'] = BicepArmLint.xǁBicepArmLintǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁBicepArmLintǁfrom_config__mutmut['xǁBicepArmLintǁfrom_config__mutmut_5'] = BicepArmLint.xǁBicepArmLintǁfrom_config__mutmut_5 # type: ignore # mutmut generated

mutants_xǁBicepArmLintǁfile_has_violation__mutmut['_mutmut_orig'] = BicepArmLint.xǁBicepArmLintǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁBicepArmLintǁfile_has_violation__mutmut['xǁBicepArmLintǁfile_has_violation__mutmut_1'] = BicepArmLint.xǁBicepArmLintǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_xǁBicepArmLintǁfile_has_violation__mutmut['xǁBicepArmLintǁfile_has_violation__mutmut_2'] = BicepArmLint.xǁBicepArmLintǁfile_has_violation__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(config: Mapping[str, Any], *, repo_root: Path | None = None) -> BicepArmLint:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return BicepArmLint.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(config: Mapping[str, Any], *, repo_root: Path | None = None) -> BicepArmLint:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return BicepArmLint.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(config: Mapping[str, Any], *, repo_root: Path | None = None) -> BicepArmLint:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return BicepArmLint.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(config: Mapping[str, Any], *, repo_root: Path | None = None) -> BicepArmLint:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return BicepArmLint.from_config(config, repo_root=None)


def x_build__mutmut_3(config: Mapping[str, Any], *, repo_root: Path | None = None) -> BicepArmLint:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return BicepArmLint.from_config(repo_root=repo_root)


def x_build__mutmut_4(config: Mapping[str, Any], *, repo_root: Path | None = None) -> BicepArmLint:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return BicepArmLint.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(BicepArmLint, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(BicepArmLint, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(BicepArmLint, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(BicepArmLint, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
