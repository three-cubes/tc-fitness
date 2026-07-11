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

Per-file baseline model
-----------------------
A ``.bicep`` file that carries any finding is an offender; the rule gates on
NET-NEW offending files vs ``.architecture/baseline/<name>-files.txt`` through
the :class:`tc_fitness.fitness_rule.FitnessRule` machinery. The consumer supplies
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


def _canonical_predecessor(prop: str) -> str:
    """Name of the property that should immediately precede ``prop`` in canon."""
    rank = PROPERTY_RANK[prop]
    return PROPERTY_ORDER[rank - 1] if rank > 0 else "(start)"


def _order_violations_for_resource(
    seen: list[tuple[int, str]],
) -> list[tuple[int, str, str]]:
    """Emit S6975 findings for any pair of seen properties out of canonical order."""
    out: list[tuple[int, str, str]] = []
    for j in range(1, len(seen)):
        line_no, prop = seen[j]
        _prev_line, prev_prop = seen[j - 1]
        if prop not in PROPERTY_RANK or prev_prop not in PROPERTY_RANK:
            continue
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


class BicepArmLint(FitnessRule):
    """Flags ``.bicep`` files with ARM-lint findings (Sonar S6954/S6975/S6956)."""

    name = "bicep-arm-lint"
    remediation = REMEDIATION
    extensions = (".bicep",)

    @classmethod
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

    def file_has_violation(self, path: Path) -> bool:
        return bool(bicep_findings(path))


def build(config: Mapping[str, Any], *, repo_root: Path | None = None) -> BicepArmLint:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return BicepArmLint.from_config(config, repo_root=repo_root)


def main(argv: list[str] | None = None) -> int:
    """CLI entry — supports ``--establish-baseline`` and ``--repo-root``."""
    return run_core_check(BicepArmLint, argv)


if __name__ == "__main__":
    import sys

    sys.exit(main())
