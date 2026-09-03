"""Canonical, versioned policy materialisation for pinned Semgrep snapshots.

Consumers retain their own immutable upstream snapshot so they control the
registry revision they scan. This module owns policy corrections that must have
one meaning across consumers. It writes a derived file and never mutates the
upstream snapshot in place.
"""

from __future__ import annotations

from pathlib import Path

OWASP_INSECURE_FILE_PERMISSIONS_RULE_ID = (
    "python.lang.security.audit.insecure-file-permissions.insecure-file-permissions"
)

_FIRST_NUMERIC_MODE_COMPARISON = "comparison: $BITS >= 0o650 and $BITS < 0o100000"
_FIRST_NON_OWNER_MODE_COMPARISON = "comparison: $BITS >= 0o650 and $BITS < 0o100000 and ($BITS & 0o077) != 0"
_SECOND_NUMERIC_MODE_COMPARISON = "comparison: $BITS >= 0o100650"
_SECOND_NON_OWNER_MODE_COMPARISON = "comparison: $BITS >= 0o100650 and ($BITS & 0o077) != 0"


def _replace_exactly_once(text: str, old: str, new: str) -> str:
    """Replace one known upstream predicate or fail closed on snapshot drift."""
    count = text.count(old)
    if count != 1:
        raise ValueError(
            f"OWASP snapshot has {count} occurrences of expected permission predicate {old!r}; "
            "refresh the canonical policy before scanning."
        )
    return text.replace(old, new)


def materialize_owasp_permissions_policy(source: Path, target: Path) -> None:
    """Write a policy-corrected OWASP snapshot to ``target``.

    The upstream rule compares octal modes numerically and therefore classifies
    owner-only ``0o700`` as widely permissive. The canonical policy evaluates
    group and other bits directly, retaining findings for modes that grant any
    non-owner access. Snapshot shape is validated before replacing predicates,
    so a registry refresh cannot silently weaken or remove this correction.
    """
    if source.resolve() == target.resolve():
        raise ValueError("source and target must differ; the upstream snapshot is immutable input")
    source_text = source.read_text(encoding="utf-8")
    if OWASP_INSECURE_FILE_PERMISSIONS_RULE_ID not in source_text:
        raise ValueError("OWASP snapshot does not contain the expected insecure-file-permissions rule")
    rendered = _replace_exactly_once(
        source_text,
        _FIRST_NUMERIC_MODE_COMPARISON,
        _FIRST_NON_OWNER_MODE_COMPARISON,
    )
    rendered = _replace_exactly_once(
        rendered,
        _SECOND_NUMERIC_MODE_COMPARISON,
        _SECOND_NON_OWNER_MODE_COMPARISON,
    )
    target.write_text(rendered, encoding="utf-8")
