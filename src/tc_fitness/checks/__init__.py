"""Configurable engine gates shipped by ``tc_fitness`` (v0.4.0).

Reusable, parametrised fitness checks a consumer wires up with its own config —
shared machinery, per-repo domain. Each gate keeps the consumer's exempt sets,
patterns, and any repo-specific knobs as CONSTRUCTOR / CALL arguments; the
engine bakes in no repo identity.

Current gates:

* :mod:`tc_fitness.checks.branch_naming` — the Linear ``gitBranchName``
  branch-name convention, with ``exempt_branches`` / ``exempt_patterns`` as
  config (taz keeps ``develop``; kairix doesn't).
"""

from __future__ import annotations

__all__: list[str] = []
