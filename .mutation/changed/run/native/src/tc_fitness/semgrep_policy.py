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


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x__replace_exactly_once__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__replace_exactly_once__mutmut)
def _replace_exactly_once(text: str, old: str, new: str) -> str:
    """Replace one known upstream predicate or fail closed on snapshot drift."""
    count = text.count(old)
    if count != 1:
        raise ValueError(
            f"OWASP snapshot has {count} occurrences of expected permission predicate {old!r}; "
            "refresh the canonical policy before scanning."
        )
    return text.replace(old, new)


def x__replace_exactly_once__mutmut_orig(text: str, old: str, new: str) -> str:
    """Replace one known upstream predicate or fail closed on snapshot drift."""
    count = text.count(old)
    if count != 1:
        raise ValueError(
            f"OWASP snapshot has {count} occurrences of expected permission predicate {old!r}; "
            "refresh the canonical policy before scanning."
        )
    return text.replace(old, new)


def x__replace_exactly_once__mutmut_1(text: str, old: str, new: str) -> str:
    """Replace one known upstream predicate or fail closed on snapshot drift."""
    count = None
    if count != 1:
        raise ValueError(
            f"OWASP snapshot has {count} occurrences of expected permission predicate {old!r}; "
            "refresh the canonical policy before scanning."
        )
    return text.replace(old, new)


def x__replace_exactly_once__mutmut_2(text: str, old: str, new: str) -> str:
    """Replace one known upstream predicate or fail closed on snapshot drift."""
    count = text.count(None)
    if count != 1:
        raise ValueError(
            f"OWASP snapshot has {count} occurrences of expected permission predicate {old!r}; "
            "refresh the canonical policy before scanning."
        )
    return text.replace(old, new)


def x__replace_exactly_once__mutmut_3(text: str, old: str, new: str) -> str:
    """Replace one known upstream predicate or fail closed on snapshot drift."""
    count = text.count(old)
    if count == 1:
        raise ValueError(
            f"OWASP snapshot has {count} occurrences of expected permission predicate {old!r}; "
            "refresh the canonical policy before scanning."
        )
    return text.replace(old, new)


def x__replace_exactly_once__mutmut_4(text: str, old: str, new: str) -> str:
    """Replace one known upstream predicate or fail closed on snapshot drift."""
    count = text.count(old)
    if count != 2:
        raise ValueError(
            f"OWASP snapshot has {count} occurrences of expected permission predicate {old!r}; "
            "refresh the canonical policy before scanning."
        )
    return text.replace(old, new)


def x__replace_exactly_once__mutmut_5(text: str, old: str, new: str) -> str:
    """Replace one known upstream predicate or fail closed on snapshot drift."""
    count = text.count(old)
    if count != 1:
        raise ValueError(
            None
        )
    return text.replace(old, new)


def x__replace_exactly_once__mutmut_6(text: str, old: str, new: str) -> str:
    """Replace one known upstream predicate or fail closed on snapshot drift."""
    count = text.count(old)
    if count != 1:
        raise ValueError(
            f"OWASP snapshot has {count} occurrences of expected permission predicate {old!r}; "
            "XXrefresh the canonical policy before scanning.XX"
        )
    return text.replace(old, new)


def x__replace_exactly_once__mutmut_7(text: str, old: str, new: str) -> str:
    """Replace one known upstream predicate or fail closed on snapshot drift."""
    count = text.count(old)
    if count != 1:
        raise ValueError(
            f"OWASP snapshot has {count} occurrences of expected permission predicate {old!r}; "
            "REFRESH THE CANONICAL POLICY BEFORE SCANNING."
        )
    return text.replace(old, new)


def x__replace_exactly_once__mutmut_8(text: str, old: str, new: str) -> str:
    """Replace one known upstream predicate or fail closed on snapshot drift."""
    count = text.count(old)
    if count != 1:
        raise ValueError(
            f"OWASP snapshot has {count} occurrences of expected permission predicate {old!r}; "
            "refresh the canonical policy before scanning."
        )
    return text.replace(None, new)


def x__replace_exactly_once__mutmut_9(text: str, old: str, new: str) -> str:
    """Replace one known upstream predicate or fail closed on snapshot drift."""
    count = text.count(old)
    if count != 1:
        raise ValueError(
            f"OWASP snapshot has {count} occurrences of expected permission predicate {old!r}; "
            "refresh the canonical policy before scanning."
        )
    return text.replace(old, None)


def x__replace_exactly_once__mutmut_10(text: str, old: str, new: str) -> str:
    """Replace one known upstream predicate or fail closed on snapshot drift."""
    count = text.count(old)
    if count != 1:
        raise ValueError(
            f"OWASP snapshot has {count} occurrences of expected permission predicate {old!r}; "
            "refresh the canonical policy before scanning."
        )
    return text.replace(new)


def x__replace_exactly_once__mutmut_11(text: str, old: str, new: str) -> str:
    """Replace one known upstream predicate or fail closed on snapshot drift."""
    count = text.count(old)
    if count != 1:
        raise ValueError(
            f"OWASP snapshot has {count} occurrences of expected permission predicate {old!r}; "
            "refresh the canonical policy before scanning."
        )
    return text.replace(old, )

mutants_x__replace_exactly_once__mutmut['_mutmut_orig'] = x__replace_exactly_once__mutmut_orig # type: ignore # mutmut generated
mutants_x__replace_exactly_once__mutmut['x__replace_exactly_once__mutmut_1'] = x__replace_exactly_once__mutmut_1 # type: ignore # mutmut generated
mutants_x__replace_exactly_once__mutmut['x__replace_exactly_once__mutmut_2'] = x__replace_exactly_once__mutmut_2 # type: ignore # mutmut generated
mutants_x__replace_exactly_once__mutmut['x__replace_exactly_once__mutmut_3'] = x__replace_exactly_once__mutmut_3 # type: ignore # mutmut generated
mutants_x__replace_exactly_once__mutmut['x__replace_exactly_once__mutmut_4'] = x__replace_exactly_once__mutmut_4 # type: ignore # mutmut generated
mutants_x__replace_exactly_once__mutmut['x__replace_exactly_once__mutmut_5'] = x__replace_exactly_once__mutmut_5 # type: ignore # mutmut generated
mutants_x__replace_exactly_once__mutmut['x__replace_exactly_once__mutmut_6'] = x__replace_exactly_once__mutmut_6 # type: ignore # mutmut generated
mutants_x__replace_exactly_once__mutmut['x__replace_exactly_once__mutmut_7'] = x__replace_exactly_once__mutmut_7 # type: ignore # mutmut generated
mutants_x__replace_exactly_once__mutmut['x__replace_exactly_once__mutmut_8'] = x__replace_exactly_once__mutmut_8 # type: ignore # mutmut generated
mutants_x__replace_exactly_once__mutmut['x__replace_exactly_once__mutmut_9'] = x__replace_exactly_once__mutmut_9 # type: ignore # mutmut generated
mutants_x__replace_exactly_once__mutmut['x__replace_exactly_once__mutmut_10'] = x__replace_exactly_once__mutmut_10 # type: ignore # mutmut generated
mutants_x__replace_exactly_once__mutmut['x__replace_exactly_once__mutmut_11'] = x__replace_exactly_once__mutmut_11 # type: ignore # mutmut generated
mutants_x_materialize_owasp_permissions_policy__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_materialize_owasp_permissions_policy__mutmut)
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


def x_materialize_owasp_permissions_policy__mutmut_orig(source: Path, target: Path) -> None:
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


def x_materialize_owasp_permissions_policy__mutmut_1(source: Path, target: Path) -> None:
    """Write a policy-corrected OWASP snapshot to ``target``.

    The upstream rule compares octal modes numerically and therefore classifies
    owner-only ``0o700`` as widely permissive. The canonical policy evaluates
    group and other bits directly, retaining findings for modes that grant any
    non-owner access. Snapshot shape is validated before replacing predicates,
    so a registry refresh cannot silently weaken or remove this correction.
    """
    if source.resolve() != target.resolve():
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


def x_materialize_owasp_permissions_policy__mutmut_2(source: Path, target: Path) -> None:
    """Write a policy-corrected OWASP snapshot to ``target``.

    The upstream rule compares octal modes numerically and therefore classifies
    owner-only ``0o700`` as widely permissive. The canonical policy evaluates
    group and other bits directly, retaining findings for modes that grant any
    non-owner access. Snapshot shape is validated before replacing predicates,
    so a registry refresh cannot silently weaken or remove this correction.
    """
    if source.resolve() == target.resolve():
        raise ValueError(None)
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


def x_materialize_owasp_permissions_policy__mutmut_3(source: Path, target: Path) -> None:
    """Write a policy-corrected OWASP snapshot to ``target``.

    The upstream rule compares octal modes numerically and therefore classifies
    owner-only ``0o700`` as widely permissive. The canonical policy evaluates
    group and other bits directly, retaining findings for modes that grant any
    non-owner access. Snapshot shape is validated before replacing predicates,
    so a registry refresh cannot silently weaken or remove this correction.
    """
    if source.resolve() == target.resolve():
        raise ValueError("XXsource and target must differ; the upstream snapshot is immutable inputXX")
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


def x_materialize_owasp_permissions_policy__mutmut_4(source: Path, target: Path) -> None:
    """Write a policy-corrected OWASP snapshot to ``target``.

    The upstream rule compares octal modes numerically and therefore classifies
    owner-only ``0o700`` as widely permissive. The canonical policy evaluates
    group and other bits directly, retaining findings for modes that grant any
    non-owner access. Snapshot shape is validated before replacing predicates,
    so a registry refresh cannot silently weaken or remove this correction.
    """
    if source.resolve() == target.resolve():
        raise ValueError("SOURCE AND TARGET MUST DIFFER; THE UPSTREAM SNAPSHOT IS IMMUTABLE INPUT")
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


def x_materialize_owasp_permissions_policy__mutmut_5(source: Path, target: Path) -> None:
    """Write a policy-corrected OWASP snapshot to ``target``.

    The upstream rule compares octal modes numerically and therefore classifies
    owner-only ``0o700`` as widely permissive. The canonical policy evaluates
    group and other bits directly, retaining findings for modes that grant any
    non-owner access. Snapshot shape is validated before replacing predicates,
    so a registry refresh cannot silently weaken or remove this correction.
    """
    if source.resolve() == target.resolve():
        raise ValueError("source and target must differ; the upstream snapshot is immutable input")
    source_text = None
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


def x_materialize_owasp_permissions_policy__mutmut_6(source: Path, target: Path) -> None:
    """Write a policy-corrected OWASP snapshot to ``target``.

    The upstream rule compares octal modes numerically and therefore classifies
    owner-only ``0o700`` as widely permissive. The canonical policy evaluates
    group and other bits directly, retaining findings for modes that grant any
    non-owner access. Snapshot shape is validated before replacing predicates,
    so a registry refresh cannot silently weaken or remove this correction.
    """
    if source.resolve() == target.resolve():
        raise ValueError("source and target must differ; the upstream snapshot is immutable input")
    source_text = source.read_text(encoding=None)
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


def x_materialize_owasp_permissions_policy__mutmut_7(source: Path, target: Path) -> None:
    """Write a policy-corrected OWASP snapshot to ``target``.

    The upstream rule compares octal modes numerically and therefore classifies
    owner-only ``0o700`` as widely permissive. The canonical policy evaluates
    group and other bits directly, retaining findings for modes that grant any
    non-owner access. Snapshot shape is validated before replacing predicates,
    so a registry refresh cannot silently weaken or remove this correction.
    """
    if source.resolve() == target.resolve():
        raise ValueError("source and target must differ; the upstream snapshot is immutable input")
    source_text = source.read_text(encoding="XXutf-8XX")
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


def x_materialize_owasp_permissions_policy__mutmut_8(source: Path, target: Path) -> None:
    """Write a policy-corrected OWASP snapshot to ``target``.

    The upstream rule compares octal modes numerically and therefore classifies
    owner-only ``0o700`` as widely permissive. The canonical policy evaluates
    group and other bits directly, retaining findings for modes that grant any
    non-owner access. Snapshot shape is validated before replacing predicates,
    so a registry refresh cannot silently weaken or remove this correction.
    """
    if source.resolve() == target.resolve():
        raise ValueError("source and target must differ; the upstream snapshot is immutable input")
    source_text = source.read_text(encoding="UTF-8")
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


def x_materialize_owasp_permissions_policy__mutmut_9(source: Path, target: Path) -> None:
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
    if OWASP_INSECURE_FILE_PERMISSIONS_RULE_ID in source_text:
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


def x_materialize_owasp_permissions_policy__mutmut_10(source: Path, target: Path) -> None:
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
        raise ValueError(None)
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


def x_materialize_owasp_permissions_policy__mutmut_11(source: Path, target: Path) -> None:
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
        raise ValueError("XXOWASP snapshot does not contain the expected insecure-file-permissions ruleXX")
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


def x_materialize_owasp_permissions_policy__mutmut_12(source: Path, target: Path) -> None:
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
        raise ValueError("owasp snapshot does not contain the expected insecure-file-permissions rule")
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


def x_materialize_owasp_permissions_policy__mutmut_13(source: Path, target: Path) -> None:
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
        raise ValueError("OWASP SNAPSHOT DOES NOT CONTAIN THE EXPECTED INSECURE-FILE-PERMISSIONS RULE")
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


def x_materialize_owasp_permissions_policy__mutmut_14(source: Path, target: Path) -> None:
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
    rendered = None
    rendered = _replace_exactly_once(
        rendered,
        _SECOND_NUMERIC_MODE_COMPARISON,
        _SECOND_NON_OWNER_MODE_COMPARISON,
    )
    target.write_text(rendered, encoding="utf-8")


def x_materialize_owasp_permissions_policy__mutmut_15(source: Path, target: Path) -> None:
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
        None,
        _FIRST_NUMERIC_MODE_COMPARISON,
        _FIRST_NON_OWNER_MODE_COMPARISON,
    )
    rendered = _replace_exactly_once(
        rendered,
        _SECOND_NUMERIC_MODE_COMPARISON,
        _SECOND_NON_OWNER_MODE_COMPARISON,
    )
    target.write_text(rendered, encoding="utf-8")


def x_materialize_owasp_permissions_policy__mutmut_16(source: Path, target: Path) -> None:
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
        None,
        _FIRST_NON_OWNER_MODE_COMPARISON,
    )
    rendered = _replace_exactly_once(
        rendered,
        _SECOND_NUMERIC_MODE_COMPARISON,
        _SECOND_NON_OWNER_MODE_COMPARISON,
    )
    target.write_text(rendered, encoding="utf-8")


def x_materialize_owasp_permissions_policy__mutmut_17(source: Path, target: Path) -> None:
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
        None,
    )
    rendered = _replace_exactly_once(
        rendered,
        _SECOND_NUMERIC_MODE_COMPARISON,
        _SECOND_NON_OWNER_MODE_COMPARISON,
    )
    target.write_text(rendered, encoding="utf-8")


def x_materialize_owasp_permissions_policy__mutmut_18(source: Path, target: Path) -> None:
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
        _FIRST_NUMERIC_MODE_COMPARISON,
        _FIRST_NON_OWNER_MODE_COMPARISON,
    )
    rendered = _replace_exactly_once(
        rendered,
        _SECOND_NUMERIC_MODE_COMPARISON,
        _SECOND_NON_OWNER_MODE_COMPARISON,
    )
    target.write_text(rendered, encoding="utf-8")


def x_materialize_owasp_permissions_policy__mutmut_19(source: Path, target: Path) -> None:
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
        _FIRST_NON_OWNER_MODE_COMPARISON,
    )
    rendered = _replace_exactly_once(
        rendered,
        _SECOND_NUMERIC_MODE_COMPARISON,
        _SECOND_NON_OWNER_MODE_COMPARISON,
    )
    target.write_text(rendered, encoding="utf-8")


def x_materialize_owasp_permissions_policy__mutmut_20(source: Path, target: Path) -> None:
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
        )
    rendered = _replace_exactly_once(
        rendered,
        _SECOND_NUMERIC_MODE_COMPARISON,
        _SECOND_NON_OWNER_MODE_COMPARISON,
    )
    target.write_text(rendered, encoding="utf-8")


def x_materialize_owasp_permissions_policy__mutmut_21(source: Path, target: Path) -> None:
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
    rendered = None
    target.write_text(rendered, encoding="utf-8")


def x_materialize_owasp_permissions_policy__mutmut_22(source: Path, target: Path) -> None:
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
        None,
        _SECOND_NUMERIC_MODE_COMPARISON,
        _SECOND_NON_OWNER_MODE_COMPARISON,
    )
    target.write_text(rendered, encoding="utf-8")


def x_materialize_owasp_permissions_policy__mutmut_23(source: Path, target: Path) -> None:
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
        None,
        _SECOND_NON_OWNER_MODE_COMPARISON,
    )
    target.write_text(rendered, encoding="utf-8")


def x_materialize_owasp_permissions_policy__mutmut_24(source: Path, target: Path) -> None:
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
        None,
    )
    target.write_text(rendered, encoding="utf-8")


def x_materialize_owasp_permissions_policy__mutmut_25(source: Path, target: Path) -> None:
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
        _SECOND_NUMERIC_MODE_COMPARISON,
        _SECOND_NON_OWNER_MODE_COMPARISON,
    )
    target.write_text(rendered, encoding="utf-8")


def x_materialize_owasp_permissions_policy__mutmut_26(source: Path, target: Path) -> None:
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
        _SECOND_NON_OWNER_MODE_COMPARISON,
    )
    target.write_text(rendered, encoding="utf-8")


def x_materialize_owasp_permissions_policy__mutmut_27(source: Path, target: Path) -> None:
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
        )
    target.write_text(rendered, encoding="utf-8")


def x_materialize_owasp_permissions_policy__mutmut_28(source: Path, target: Path) -> None:
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
    target.write_text(None, encoding="utf-8")


def x_materialize_owasp_permissions_policy__mutmut_29(source: Path, target: Path) -> None:
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
    target.write_text(rendered, encoding=None)


def x_materialize_owasp_permissions_policy__mutmut_30(source: Path, target: Path) -> None:
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
    target.write_text(encoding="utf-8")


def x_materialize_owasp_permissions_policy__mutmut_31(source: Path, target: Path) -> None:
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
    target.write_text(rendered, )


def x_materialize_owasp_permissions_policy__mutmut_32(source: Path, target: Path) -> None:
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
    target.write_text(rendered, encoding="XXutf-8XX")


def x_materialize_owasp_permissions_policy__mutmut_33(source: Path, target: Path) -> None:
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
    target.write_text(rendered, encoding="UTF-8")

mutants_x_materialize_owasp_permissions_policy__mutmut['_mutmut_orig'] = x_materialize_owasp_permissions_policy__mutmut_orig # type: ignore # mutmut generated
mutants_x_materialize_owasp_permissions_policy__mutmut['x_materialize_owasp_permissions_policy__mutmut_1'] = x_materialize_owasp_permissions_policy__mutmut_1 # type: ignore # mutmut generated
mutants_x_materialize_owasp_permissions_policy__mutmut['x_materialize_owasp_permissions_policy__mutmut_2'] = x_materialize_owasp_permissions_policy__mutmut_2 # type: ignore # mutmut generated
mutants_x_materialize_owasp_permissions_policy__mutmut['x_materialize_owasp_permissions_policy__mutmut_3'] = x_materialize_owasp_permissions_policy__mutmut_3 # type: ignore # mutmut generated
mutants_x_materialize_owasp_permissions_policy__mutmut['x_materialize_owasp_permissions_policy__mutmut_4'] = x_materialize_owasp_permissions_policy__mutmut_4 # type: ignore # mutmut generated
mutants_x_materialize_owasp_permissions_policy__mutmut['x_materialize_owasp_permissions_policy__mutmut_5'] = x_materialize_owasp_permissions_policy__mutmut_5 # type: ignore # mutmut generated
mutants_x_materialize_owasp_permissions_policy__mutmut['x_materialize_owasp_permissions_policy__mutmut_6'] = x_materialize_owasp_permissions_policy__mutmut_6 # type: ignore # mutmut generated
mutants_x_materialize_owasp_permissions_policy__mutmut['x_materialize_owasp_permissions_policy__mutmut_7'] = x_materialize_owasp_permissions_policy__mutmut_7 # type: ignore # mutmut generated
mutants_x_materialize_owasp_permissions_policy__mutmut['x_materialize_owasp_permissions_policy__mutmut_8'] = x_materialize_owasp_permissions_policy__mutmut_8 # type: ignore # mutmut generated
mutants_x_materialize_owasp_permissions_policy__mutmut['x_materialize_owasp_permissions_policy__mutmut_9'] = x_materialize_owasp_permissions_policy__mutmut_9 # type: ignore # mutmut generated
mutants_x_materialize_owasp_permissions_policy__mutmut['x_materialize_owasp_permissions_policy__mutmut_10'] = x_materialize_owasp_permissions_policy__mutmut_10 # type: ignore # mutmut generated
mutants_x_materialize_owasp_permissions_policy__mutmut['x_materialize_owasp_permissions_policy__mutmut_11'] = x_materialize_owasp_permissions_policy__mutmut_11 # type: ignore # mutmut generated
mutants_x_materialize_owasp_permissions_policy__mutmut['x_materialize_owasp_permissions_policy__mutmut_12'] = x_materialize_owasp_permissions_policy__mutmut_12 # type: ignore # mutmut generated
mutants_x_materialize_owasp_permissions_policy__mutmut['x_materialize_owasp_permissions_policy__mutmut_13'] = x_materialize_owasp_permissions_policy__mutmut_13 # type: ignore # mutmut generated
mutants_x_materialize_owasp_permissions_policy__mutmut['x_materialize_owasp_permissions_policy__mutmut_14'] = x_materialize_owasp_permissions_policy__mutmut_14 # type: ignore # mutmut generated
mutants_x_materialize_owasp_permissions_policy__mutmut['x_materialize_owasp_permissions_policy__mutmut_15'] = x_materialize_owasp_permissions_policy__mutmut_15 # type: ignore # mutmut generated
mutants_x_materialize_owasp_permissions_policy__mutmut['x_materialize_owasp_permissions_policy__mutmut_16'] = x_materialize_owasp_permissions_policy__mutmut_16 # type: ignore # mutmut generated
mutants_x_materialize_owasp_permissions_policy__mutmut['x_materialize_owasp_permissions_policy__mutmut_17'] = x_materialize_owasp_permissions_policy__mutmut_17 # type: ignore # mutmut generated
mutants_x_materialize_owasp_permissions_policy__mutmut['x_materialize_owasp_permissions_policy__mutmut_18'] = x_materialize_owasp_permissions_policy__mutmut_18 # type: ignore # mutmut generated
mutants_x_materialize_owasp_permissions_policy__mutmut['x_materialize_owasp_permissions_policy__mutmut_19'] = x_materialize_owasp_permissions_policy__mutmut_19 # type: ignore # mutmut generated
mutants_x_materialize_owasp_permissions_policy__mutmut['x_materialize_owasp_permissions_policy__mutmut_20'] = x_materialize_owasp_permissions_policy__mutmut_20 # type: ignore # mutmut generated
mutants_x_materialize_owasp_permissions_policy__mutmut['x_materialize_owasp_permissions_policy__mutmut_21'] = x_materialize_owasp_permissions_policy__mutmut_21 # type: ignore # mutmut generated
mutants_x_materialize_owasp_permissions_policy__mutmut['x_materialize_owasp_permissions_policy__mutmut_22'] = x_materialize_owasp_permissions_policy__mutmut_22 # type: ignore # mutmut generated
mutants_x_materialize_owasp_permissions_policy__mutmut['x_materialize_owasp_permissions_policy__mutmut_23'] = x_materialize_owasp_permissions_policy__mutmut_23 # type: ignore # mutmut generated
mutants_x_materialize_owasp_permissions_policy__mutmut['x_materialize_owasp_permissions_policy__mutmut_24'] = x_materialize_owasp_permissions_policy__mutmut_24 # type: ignore # mutmut generated
mutants_x_materialize_owasp_permissions_policy__mutmut['x_materialize_owasp_permissions_policy__mutmut_25'] = x_materialize_owasp_permissions_policy__mutmut_25 # type: ignore # mutmut generated
mutants_x_materialize_owasp_permissions_policy__mutmut['x_materialize_owasp_permissions_policy__mutmut_26'] = x_materialize_owasp_permissions_policy__mutmut_26 # type: ignore # mutmut generated
mutants_x_materialize_owasp_permissions_policy__mutmut['x_materialize_owasp_permissions_policy__mutmut_27'] = x_materialize_owasp_permissions_policy__mutmut_27 # type: ignore # mutmut generated
mutants_x_materialize_owasp_permissions_policy__mutmut['x_materialize_owasp_permissions_policy__mutmut_28'] = x_materialize_owasp_permissions_policy__mutmut_28 # type: ignore # mutmut generated
mutants_x_materialize_owasp_permissions_policy__mutmut['x_materialize_owasp_permissions_policy__mutmut_29'] = x_materialize_owasp_permissions_policy__mutmut_29 # type: ignore # mutmut generated
mutants_x_materialize_owasp_permissions_policy__mutmut['x_materialize_owasp_permissions_policy__mutmut_30'] = x_materialize_owasp_permissions_policy__mutmut_30 # type: ignore # mutmut generated
mutants_x_materialize_owasp_permissions_policy__mutmut['x_materialize_owasp_permissions_policy__mutmut_31'] = x_materialize_owasp_permissions_policy__mutmut_31 # type: ignore # mutmut generated
mutants_x_materialize_owasp_permissions_policy__mutmut['x_materialize_owasp_permissions_policy__mutmut_32'] = x_materialize_owasp_permissions_policy__mutmut_32 # type: ignore # mutmut generated
mutants_x_materialize_owasp_permissions_policy__mutmut['x_materialize_owasp_permissions_policy__mutmut_33'] = x_materialize_owasp_permissions_policy__mutmut_33 # type: ignore # mutmut generated
