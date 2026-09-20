"""Unified ratchet primitives — the three reconciled drift zones.

Two repos grew parallel ratchet gates (coverage, mutation-survival, sonar-quality)
that drifted apart on three details. This module is the single source for all
three, so a consumer's coverage ratchet and mutation ratchet agree by
construction.

Drift zone 1 — override min-length
----------------------------------
tc-agent-zone's coverage ratchet treated a rationale "vague" below **20** chars
(``<=``); its mutation ratchet used **40** chars (``<``). The remediation text in
*both* gates already advertised "≥40 chars" to the operator — so the coverage
gate's 20 was a latent bug (code disagreed with the message it printed).

Decision: **40 chars, strictly-less-than** (``len(reason) < 40`` is vague).
40 is the stricter superset and matches the contract both repos already
documented to operators. Exposed as :data:`OVERRIDE_MIN_REASON_LEN`.

Drift zone 2 — suppression-pattern list
---------------------------------------
tc-agent-zone added ``NOSONAR`` (and the ``//`` C-style variants) to the
suppression set kairix originally tracked. There were also possessive-quantifier
variations across the regex copies.

Decision: **the superset** of every marker any repo tracked, as one grammar.
Exposed as :data:`SUPPRESSION_PATTERNS` (substring markers, e.g. the
no-production-suppressions sweep) and :data:`BARE_SUPPRESSION_PATTERNS` (compiled
end-of-line regexes, e.g. the rationale gate). ``NOSONAR`` is in both.

Drift zone 3 — override-marker syntax
-------------------------------------
tc-agent-zone's override line regex accepted an em-dash OR a hyphen as the
separator (``[—-]++``); some kairix copies were stricter (em-dash only).

Decision: **accept both** em-dash and hyphen (the superset). A consumer that
wrote ``coverage-ratchet-acknowledged: path - reason`` with a plain hyphen must
keep passing, and so must the em-dash form. Use :func:`make_override_re` to build
a marker parser for any acknowledgement keyword.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# ---------------------------------------------------------------------------
# Drift zone 1 — ONE override-rationale min-length
# ---------------------------------------------------------------------------

#: A ratchet-override rationale shorter than this many characters is "vague".
#: Reconciled to 40 (the stricter of {20, 40}); matches the "≥40 chars" text
#: both repos' remediation messages already printed.
OVERRIDE_MIN_REASON_LEN = 40

#: Lead-in tokens that mark a rationale as vague regardless of length.
#: Union of every variant either repo's VAGUE_OVERRIDE_RE matched.
VAGUE_OVERRIDE_RE = re.compile(
    r"^(wip|minor|todo|skip|later|n/a|out of scope|will[- ]?fix[- ]?later)\b",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Drift zone 3 — ONE override-marker parser (em-dash OR hyphen)
# ---------------------------------------------------------------------------

# Separator class: em-dash (—) OR ASCII hyphen (-), one-or-more, possessive so
# there's no catastrophic backtracking against the trailing reason. This is the
# superset that accepts both repos' historical forms.
_SEP = r"[—-]++"


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x_make_override_re__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_make_override_re__mutmut)
def make_override_re(keyword: str) -> re.Pattern[str]:
    r"""Build the regex that parses an override acknowledgement line.

    ``keyword`` is the acknowledgement token, e.g. ``"coverage-ratchet-acknowledged"``
    or ``"mutation-ratchet-acknowledged"``. The line shape is::

        <keyword>: <target> <sep> <reason>

    where ``<sep>`` is an em-dash or a hyphen (one or more), matching both repos.
    Two named groups are returned: ``target`` (the path/package) and ``reason``.
    """
    return re.compile(
        rf"^\s*+{re.escape(keyword)}:\s*+(?P<target>\S++)\s*+{_SEP}\s*+(?P<reason>.*)$",
    )


def x_make_override_re__mutmut_orig(keyword: str) -> re.Pattern[str]:
    r"""Build the regex that parses an override acknowledgement line.

    ``keyword`` is the acknowledgement token, e.g. ``"coverage-ratchet-acknowledged"``
    or ``"mutation-ratchet-acknowledged"``. The line shape is::

        <keyword>: <target> <sep> <reason>

    where ``<sep>`` is an em-dash or a hyphen (one or more), matching both repos.
    Two named groups are returned: ``target`` (the path/package) and ``reason``.
    """
    return re.compile(
        rf"^\s*+{re.escape(keyword)}:\s*+(?P<target>\S++)\s*+{_SEP}\s*+(?P<reason>.*)$",
    )


def x_make_override_re__mutmut_1(keyword: str) -> re.Pattern[str]:
    r"""Build the regex that parses an override acknowledgement line.

    ``keyword`` is the acknowledgement token, e.g. ``"coverage-ratchet-acknowledged"``
    or ``"mutation-ratchet-acknowledged"``. The line shape is::

        <keyword>: <target> <sep> <reason>

    where ``<sep>`` is an em-dash or a hyphen (one or more), matching both repos.
    Two named groups are returned: ``target`` (the path/package) and ``reason``.
    """
    return re.compile(
        None,
    )


def x_make_override_re__mutmut_2(keyword: str) -> re.Pattern[str]:
    r"""Build the regex that parses an override acknowledgement line.

    ``keyword`` is the acknowledgement token, e.g. ``"coverage-ratchet-acknowledged"``
    or ``"mutation-ratchet-acknowledged"``. The line shape is::

        <keyword>: <target> <sep> <reason>

    where ``<sep>`` is an em-dash or a hyphen (one or more), matching both repos.
    Two named groups are returned: ``target`` (the path/package) and ``reason``.
    """
    return re.compile(
        rf"^\s*+{re.escape(None)}:\s*+(?P<target>\S++)\s*+{_SEP}\s*+(?P<reason>.*)$",
    )

mutants_x_make_override_re__mutmut['_mutmut_orig'] = x_make_override_re__mutmut_orig # type: ignore # mutmut generated
mutants_x_make_override_re__mutmut['x_make_override_re__mutmut_1'] = x_make_override_re__mutmut_1 # type: ignore # mutmut generated
mutants_x_make_override_re__mutmut['x_make_override_re__mutmut_2'] = x_make_override_re__mutmut_2 # type: ignore # mutmut generated


#: Pre-built parsers for the two canonical ratchet keywords.
COVERAGE_OVERRIDE_RE = make_override_re("coverage-ratchet-acknowledged")
MUTATION_OVERRIDE_RE = make_override_re("mutation-ratchet-acknowledged")


@dataclass(frozen=True)
class Override:
    """One parsed acknowledgement line.

    ``target`` is the path (coverage) or package (mutation). ``vague`` is True
    when the reason is too short or matches :data:`VAGUE_OVERRIDE_RE`; vague
    overrides do NOT clear a ratchet failure.
    """

    target: str
    reason: str
    vague: bool
mutants_x_is_vague_reason__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_is_vague_reason__mutmut)
def is_vague_reason(reason: str, *, min_len: int = OVERRIDE_MIN_REASON_LEN) -> bool:
    """Return True when ``reason`` is too short or matches the vague lead-in set.

    Trailing dots and surrounding whitespace are stripped before measuring, so
    ``"WIP."`` and ``"   short  "`` are judged on their substance. The length
    floor defaults to the reconciled ``OVERRIDE_MIN_REASON_LEN`` (=40,
    strictly-less-than). Pass ``min_len`` to override the floor — tc-agent-zone's
    shell directives use a 10-char floor, so its checks call with
    ``min_len=10``. The default keeps the v0.1.0 behaviour byte-identical.
    """
    compact = reason.strip().rstrip(".").strip()
    return len(compact) < min_len or bool(VAGUE_OVERRIDE_RE.match(compact))


def x_is_vague_reason__mutmut_orig(reason: str, *, min_len: int = OVERRIDE_MIN_REASON_LEN) -> bool:
    """Return True when ``reason`` is too short or matches the vague lead-in set.

    Trailing dots and surrounding whitespace are stripped before measuring, so
    ``"WIP."`` and ``"   short  "`` are judged on their substance. The length
    floor defaults to the reconciled ``OVERRIDE_MIN_REASON_LEN`` (=40,
    strictly-less-than). Pass ``min_len`` to override the floor — tc-agent-zone's
    shell directives use a 10-char floor, so its checks call with
    ``min_len=10``. The default keeps the v0.1.0 behaviour byte-identical.
    """
    compact = reason.strip().rstrip(".").strip()
    return len(compact) < min_len or bool(VAGUE_OVERRIDE_RE.match(compact))


def x_is_vague_reason__mutmut_1(reason: str, *, min_len: int = OVERRIDE_MIN_REASON_LEN) -> bool:
    """Return True when ``reason`` is too short or matches the vague lead-in set.

    Trailing dots and surrounding whitespace are stripped before measuring, so
    ``"WIP."`` and ``"   short  "`` are judged on their substance. The length
    floor defaults to the reconciled ``OVERRIDE_MIN_REASON_LEN`` (=40,
    strictly-less-than). Pass ``min_len`` to override the floor — tc-agent-zone's
    shell directives use a 10-char floor, so its checks call with
    ``min_len=10``. The default keeps the v0.1.0 behaviour byte-identical.
    """
    compact = None
    return len(compact) < min_len or bool(VAGUE_OVERRIDE_RE.match(compact))


def x_is_vague_reason__mutmut_2(reason: str, *, min_len: int = OVERRIDE_MIN_REASON_LEN) -> bool:
    """Return True when ``reason`` is too short or matches the vague lead-in set.

    Trailing dots and surrounding whitespace are stripped before measuring, so
    ``"WIP."`` and ``"   short  "`` are judged on their substance. The length
    floor defaults to the reconciled ``OVERRIDE_MIN_REASON_LEN`` (=40,
    strictly-less-than). Pass ``min_len`` to override the floor — tc-agent-zone's
    shell directives use a 10-char floor, so its checks call with
    ``min_len=10``. The default keeps the v0.1.0 behaviour byte-identical.
    """
    compact = reason.strip().rstrip(None).strip()
    return len(compact) < min_len or bool(VAGUE_OVERRIDE_RE.match(compact))


def x_is_vague_reason__mutmut_3(reason: str, *, min_len: int = OVERRIDE_MIN_REASON_LEN) -> bool:
    """Return True when ``reason`` is too short or matches the vague lead-in set.

    Trailing dots and surrounding whitespace are stripped before measuring, so
    ``"WIP."`` and ``"   short  "`` are judged on their substance. The length
    floor defaults to the reconciled ``OVERRIDE_MIN_REASON_LEN`` (=40,
    strictly-less-than). Pass ``min_len`` to override the floor — tc-agent-zone's
    shell directives use a 10-char floor, so its checks call with
    ``min_len=10``. The default keeps the v0.1.0 behaviour byte-identical.
    """
    compact = reason.strip().lstrip(".").strip()
    return len(compact) < min_len or bool(VAGUE_OVERRIDE_RE.match(compact))


def x_is_vague_reason__mutmut_4(reason: str, *, min_len: int = OVERRIDE_MIN_REASON_LEN) -> bool:
    """Return True when ``reason`` is too short or matches the vague lead-in set.

    Trailing dots and surrounding whitespace are stripped before measuring, so
    ``"WIP."`` and ``"   short  "`` are judged on their substance. The length
    floor defaults to the reconciled ``OVERRIDE_MIN_REASON_LEN`` (=40,
    strictly-less-than). Pass ``min_len`` to override the floor — tc-agent-zone's
    shell directives use a 10-char floor, so its checks call with
    ``min_len=10``. The default keeps the v0.1.0 behaviour byte-identical.
    """
    compact = reason.strip().rstrip("XX.XX").strip()
    return len(compact) < min_len or bool(VAGUE_OVERRIDE_RE.match(compact))


def x_is_vague_reason__mutmut_5(reason: str, *, min_len: int = OVERRIDE_MIN_REASON_LEN) -> bool:
    """Return True when ``reason`` is too short or matches the vague lead-in set.

    Trailing dots and surrounding whitespace are stripped before measuring, so
    ``"WIP."`` and ``"   short  "`` are judged on their substance. The length
    floor defaults to the reconciled ``OVERRIDE_MIN_REASON_LEN`` (=40,
    strictly-less-than). Pass ``min_len`` to override the floor — tc-agent-zone's
    shell directives use a 10-char floor, so its checks call with
    ``min_len=10``. The default keeps the v0.1.0 behaviour byte-identical.
    """
    compact = reason.strip().rstrip(".").strip()
    return len(compact) < min_len and bool(VAGUE_OVERRIDE_RE.match(compact))


def x_is_vague_reason__mutmut_6(reason: str, *, min_len: int = OVERRIDE_MIN_REASON_LEN) -> bool:
    """Return True when ``reason`` is too short or matches the vague lead-in set.

    Trailing dots and surrounding whitespace are stripped before measuring, so
    ``"WIP."`` and ``"   short  "`` are judged on their substance. The length
    floor defaults to the reconciled ``OVERRIDE_MIN_REASON_LEN`` (=40,
    strictly-less-than). Pass ``min_len`` to override the floor — tc-agent-zone's
    shell directives use a 10-char floor, so its checks call with
    ``min_len=10``. The default keeps the v0.1.0 behaviour byte-identical.
    """
    compact = reason.strip().rstrip(".").strip()
    return len(compact) <= min_len or bool(VAGUE_OVERRIDE_RE.match(compact))


def x_is_vague_reason__mutmut_7(reason: str, *, min_len: int = OVERRIDE_MIN_REASON_LEN) -> bool:
    """Return True when ``reason`` is too short or matches the vague lead-in set.

    Trailing dots and surrounding whitespace are stripped before measuring, so
    ``"WIP."`` and ``"   short  "`` are judged on their substance. The length
    floor defaults to the reconciled ``OVERRIDE_MIN_REASON_LEN`` (=40,
    strictly-less-than). Pass ``min_len`` to override the floor — tc-agent-zone's
    shell directives use a 10-char floor, so its checks call with
    ``min_len=10``. The default keeps the v0.1.0 behaviour byte-identical.
    """
    compact = reason.strip().rstrip(".").strip()
    return len(compact) < min_len or bool(None)


def x_is_vague_reason__mutmut_8(reason: str, *, min_len: int = OVERRIDE_MIN_REASON_LEN) -> bool:
    """Return True when ``reason`` is too short or matches the vague lead-in set.

    Trailing dots and surrounding whitespace are stripped before measuring, so
    ``"WIP."`` and ``"   short  "`` are judged on their substance. The length
    floor defaults to the reconciled ``OVERRIDE_MIN_REASON_LEN`` (=40,
    strictly-less-than). Pass ``min_len`` to override the floor — tc-agent-zone's
    shell directives use a 10-char floor, so its checks call with
    ``min_len=10``. The default keeps the v0.1.0 behaviour byte-identical.
    """
    compact = reason.strip().rstrip(".").strip()
    return len(compact) < min_len or bool(VAGUE_OVERRIDE_RE.match(None))

mutants_x_is_vague_reason__mutmut['_mutmut_orig'] = x_is_vague_reason__mutmut_orig # type: ignore # mutmut generated
mutants_x_is_vague_reason__mutmut['x_is_vague_reason__mutmut_1'] = x_is_vague_reason__mutmut_1 # type: ignore # mutmut generated
mutants_x_is_vague_reason__mutmut['x_is_vague_reason__mutmut_2'] = x_is_vague_reason__mutmut_2 # type: ignore # mutmut generated
mutants_x_is_vague_reason__mutmut['x_is_vague_reason__mutmut_3'] = x_is_vague_reason__mutmut_3 # type: ignore # mutmut generated
mutants_x_is_vague_reason__mutmut['x_is_vague_reason__mutmut_4'] = x_is_vague_reason__mutmut_4 # type: ignore # mutmut generated
mutants_x_is_vague_reason__mutmut['x_is_vague_reason__mutmut_5'] = x_is_vague_reason__mutmut_5 # type: ignore # mutmut generated
mutants_x_is_vague_reason__mutmut['x_is_vague_reason__mutmut_6'] = x_is_vague_reason__mutmut_6 # type: ignore # mutmut generated
mutants_x_is_vague_reason__mutmut['x_is_vague_reason__mutmut_7'] = x_is_vague_reason__mutmut_7 # type: ignore # mutmut generated
mutants_x_is_vague_reason__mutmut['x_is_vague_reason__mutmut_8'] = x_is_vague_reason__mutmut_8 # type: ignore # mutmut generated
mutants_x_parse_overrides__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_parse_overrides__mutmut)
def parse_overrides(
    text: str,
    override_re: re.Pattern[str],
    *,
    min_len: int = OVERRIDE_MIN_REASON_LEN,
) -> list[Override]:
    """Parse every acknowledgement line in ``text`` using ``override_re``.

    ``text`` is typically a commit message or PR body. Lines that don't match
    are ignored. Each match becomes an :class:`Override` with ``vague`` computed
    via :func:`is_vague_reason`. ``min_len`` is forwarded to
    :func:`is_vague_reason` and defaults to :data:`OVERRIDE_MIN_REASON_LEN`
    (=40), so the v0.1.0 call shape is unchanged; pass ``min_len=10`` for
    tc-agent-zone's shell-directive floor.
    """
    out: list[Override] = []
    for line in (text or "").splitlines():
        match = override_re.match(line)
        if not match:
            continue
        reason = match.group("reason").strip()
        out.append(
            Override(
                target=match.group("target"),
                reason=reason,
                vague=is_vague_reason(reason, min_len=min_len),
            )
        )
    return out


def x_parse_overrides__mutmut_orig(
    text: str,
    override_re: re.Pattern[str],
    *,
    min_len: int = OVERRIDE_MIN_REASON_LEN,
) -> list[Override]:
    """Parse every acknowledgement line in ``text`` using ``override_re``.

    ``text`` is typically a commit message or PR body. Lines that don't match
    are ignored. Each match becomes an :class:`Override` with ``vague`` computed
    via :func:`is_vague_reason`. ``min_len`` is forwarded to
    :func:`is_vague_reason` and defaults to :data:`OVERRIDE_MIN_REASON_LEN`
    (=40), so the v0.1.0 call shape is unchanged; pass ``min_len=10`` for
    tc-agent-zone's shell-directive floor.
    """
    out: list[Override] = []
    for line in (text or "").splitlines():
        match = override_re.match(line)
        if not match:
            continue
        reason = match.group("reason").strip()
        out.append(
            Override(
                target=match.group("target"),
                reason=reason,
                vague=is_vague_reason(reason, min_len=min_len),
            )
        )
    return out


def x_parse_overrides__mutmut_1(
    text: str,
    override_re: re.Pattern[str],
    *,
    min_len: int = OVERRIDE_MIN_REASON_LEN,
) -> list[Override]:
    """Parse every acknowledgement line in ``text`` using ``override_re``.

    ``text`` is typically a commit message or PR body. Lines that don't match
    are ignored. Each match becomes an :class:`Override` with ``vague`` computed
    via :func:`is_vague_reason`. ``min_len`` is forwarded to
    :func:`is_vague_reason` and defaults to :data:`OVERRIDE_MIN_REASON_LEN`
    (=40), so the v0.1.0 call shape is unchanged; pass ``min_len=10`` for
    tc-agent-zone's shell-directive floor.
    """
    out: list[Override] = None
    for line in (text or "").splitlines():
        match = override_re.match(line)
        if not match:
            continue
        reason = match.group("reason").strip()
        out.append(
            Override(
                target=match.group("target"),
                reason=reason,
                vague=is_vague_reason(reason, min_len=min_len),
            )
        )
    return out


def x_parse_overrides__mutmut_2(
    text: str,
    override_re: re.Pattern[str],
    *,
    min_len: int = OVERRIDE_MIN_REASON_LEN,
) -> list[Override]:
    """Parse every acknowledgement line in ``text`` using ``override_re``.

    ``text`` is typically a commit message or PR body. Lines that don't match
    are ignored. Each match becomes an :class:`Override` with ``vague`` computed
    via :func:`is_vague_reason`. ``min_len`` is forwarded to
    :func:`is_vague_reason` and defaults to :data:`OVERRIDE_MIN_REASON_LEN`
    (=40), so the v0.1.0 call shape is unchanged; pass ``min_len=10`` for
    tc-agent-zone's shell-directive floor.
    """
    out: list[Override] = []
    for line in (text and "").splitlines():
        match = override_re.match(line)
        if not match:
            continue
        reason = match.group("reason").strip()
        out.append(
            Override(
                target=match.group("target"),
                reason=reason,
                vague=is_vague_reason(reason, min_len=min_len),
            )
        )
    return out


def x_parse_overrides__mutmut_3(
    text: str,
    override_re: re.Pattern[str],
    *,
    min_len: int = OVERRIDE_MIN_REASON_LEN,
) -> list[Override]:
    """Parse every acknowledgement line in ``text`` using ``override_re``.

    ``text`` is typically a commit message or PR body. Lines that don't match
    are ignored. Each match becomes an :class:`Override` with ``vague`` computed
    via :func:`is_vague_reason`. ``min_len`` is forwarded to
    :func:`is_vague_reason` and defaults to :data:`OVERRIDE_MIN_REASON_LEN`
    (=40), so the v0.1.0 call shape is unchanged; pass ``min_len=10`` for
    tc-agent-zone's shell-directive floor.
    """
    out: list[Override] = []
    for line in (text or "XXXX").splitlines():
        match = override_re.match(line)
        if not match:
            continue
        reason = match.group("reason").strip()
        out.append(
            Override(
                target=match.group("target"),
                reason=reason,
                vague=is_vague_reason(reason, min_len=min_len),
            )
        )
    return out


def x_parse_overrides__mutmut_4(
    text: str,
    override_re: re.Pattern[str],
    *,
    min_len: int = OVERRIDE_MIN_REASON_LEN,
) -> list[Override]:
    """Parse every acknowledgement line in ``text`` using ``override_re``.

    ``text`` is typically a commit message or PR body. Lines that don't match
    are ignored. Each match becomes an :class:`Override` with ``vague`` computed
    via :func:`is_vague_reason`. ``min_len`` is forwarded to
    :func:`is_vague_reason` and defaults to :data:`OVERRIDE_MIN_REASON_LEN`
    (=40), so the v0.1.0 call shape is unchanged; pass ``min_len=10`` for
    tc-agent-zone's shell-directive floor.
    """
    out: list[Override] = []
    for line in (text or "").splitlines():
        match = None
        if not match:
            continue
        reason = match.group("reason").strip()
        out.append(
            Override(
                target=match.group("target"),
                reason=reason,
                vague=is_vague_reason(reason, min_len=min_len),
            )
        )
    return out


def x_parse_overrides__mutmut_5(
    text: str,
    override_re: re.Pattern[str],
    *,
    min_len: int = OVERRIDE_MIN_REASON_LEN,
) -> list[Override]:
    """Parse every acknowledgement line in ``text`` using ``override_re``.

    ``text`` is typically a commit message or PR body. Lines that don't match
    are ignored. Each match becomes an :class:`Override` with ``vague`` computed
    via :func:`is_vague_reason`. ``min_len`` is forwarded to
    :func:`is_vague_reason` and defaults to :data:`OVERRIDE_MIN_REASON_LEN`
    (=40), so the v0.1.0 call shape is unchanged; pass ``min_len=10`` for
    tc-agent-zone's shell-directive floor.
    """
    out: list[Override] = []
    for line in (text or "").splitlines():
        match = override_re.match(None)
        if not match:
            continue
        reason = match.group("reason").strip()
        out.append(
            Override(
                target=match.group("target"),
                reason=reason,
                vague=is_vague_reason(reason, min_len=min_len),
            )
        )
    return out


def x_parse_overrides__mutmut_6(
    text: str,
    override_re: re.Pattern[str],
    *,
    min_len: int = OVERRIDE_MIN_REASON_LEN,
) -> list[Override]:
    """Parse every acknowledgement line in ``text`` using ``override_re``.

    ``text`` is typically a commit message or PR body. Lines that don't match
    are ignored. Each match becomes an :class:`Override` with ``vague`` computed
    via :func:`is_vague_reason`. ``min_len`` is forwarded to
    :func:`is_vague_reason` and defaults to :data:`OVERRIDE_MIN_REASON_LEN`
    (=40), so the v0.1.0 call shape is unchanged; pass ``min_len=10`` for
    tc-agent-zone's shell-directive floor.
    """
    out: list[Override] = []
    for line in (text or "").splitlines():
        match = override_re.match(line)
        if match:
            continue
        reason = match.group("reason").strip()
        out.append(
            Override(
                target=match.group("target"),
                reason=reason,
                vague=is_vague_reason(reason, min_len=min_len),
            )
        )
    return out


def x_parse_overrides__mutmut_7(
    text: str,
    override_re: re.Pattern[str],
    *,
    min_len: int = OVERRIDE_MIN_REASON_LEN,
) -> list[Override]:
    """Parse every acknowledgement line in ``text`` using ``override_re``.

    ``text`` is typically a commit message or PR body. Lines that don't match
    are ignored. Each match becomes an :class:`Override` with ``vague`` computed
    via :func:`is_vague_reason`. ``min_len`` is forwarded to
    :func:`is_vague_reason` and defaults to :data:`OVERRIDE_MIN_REASON_LEN`
    (=40), so the v0.1.0 call shape is unchanged; pass ``min_len=10`` for
    tc-agent-zone's shell-directive floor.
    """
    out: list[Override] = []
    for line in (text or "").splitlines():
        match = override_re.match(line)
        if not match:
            break
        reason = match.group("reason").strip()
        out.append(
            Override(
                target=match.group("target"),
                reason=reason,
                vague=is_vague_reason(reason, min_len=min_len),
            )
        )
    return out


def x_parse_overrides__mutmut_8(
    text: str,
    override_re: re.Pattern[str],
    *,
    min_len: int = OVERRIDE_MIN_REASON_LEN,
) -> list[Override]:
    """Parse every acknowledgement line in ``text`` using ``override_re``.

    ``text`` is typically a commit message or PR body. Lines that don't match
    are ignored. Each match becomes an :class:`Override` with ``vague`` computed
    via :func:`is_vague_reason`. ``min_len`` is forwarded to
    :func:`is_vague_reason` and defaults to :data:`OVERRIDE_MIN_REASON_LEN`
    (=40), so the v0.1.0 call shape is unchanged; pass ``min_len=10`` for
    tc-agent-zone's shell-directive floor.
    """
    out: list[Override] = []
    for line in (text or "").splitlines():
        match = override_re.match(line)
        if not match:
            continue
        reason = None
        out.append(
            Override(
                target=match.group("target"),
                reason=reason,
                vague=is_vague_reason(reason, min_len=min_len),
            )
        )
    return out


def x_parse_overrides__mutmut_9(
    text: str,
    override_re: re.Pattern[str],
    *,
    min_len: int = OVERRIDE_MIN_REASON_LEN,
) -> list[Override]:
    """Parse every acknowledgement line in ``text`` using ``override_re``.

    ``text`` is typically a commit message or PR body. Lines that don't match
    are ignored. Each match becomes an :class:`Override` with ``vague`` computed
    via :func:`is_vague_reason`. ``min_len`` is forwarded to
    :func:`is_vague_reason` and defaults to :data:`OVERRIDE_MIN_REASON_LEN`
    (=40), so the v0.1.0 call shape is unchanged; pass ``min_len=10`` for
    tc-agent-zone's shell-directive floor.
    """
    out: list[Override] = []
    for line in (text or "").splitlines():
        match = override_re.match(line)
        if not match:
            continue
        reason = match.group(None).strip()
        out.append(
            Override(
                target=match.group("target"),
                reason=reason,
                vague=is_vague_reason(reason, min_len=min_len),
            )
        )
    return out


def x_parse_overrides__mutmut_10(
    text: str,
    override_re: re.Pattern[str],
    *,
    min_len: int = OVERRIDE_MIN_REASON_LEN,
) -> list[Override]:
    """Parse every acknowledgement line in ``text`` using ``override_re``.

    ``text`` is typically a commit message or PR body. Lines that don't match
    are ignored. Each match becomes an :class:`Override` with ``vague`` computed
    via :func:`is_vague_reason`. ``min_len`` is forwarded to
    :func:`is_vague_reason` and defaults to :data:`OVERRIDE_MIN_REASON_LEN`
    (=40), so the v0.1.0 call shape is unchanged; pass ``min_len=10`` for
    tc-agent-zone's shell-directive floor.
    """
    out: list[Override] = []
    for line in (text or "").splitlines():
        match = override_re.match(line)
        if not match:
            continue
        reason = match.group("XXreasonXX").strip()
        out.append(
            Override(
                target=match.group("target"),
                reason=reason,
                vague=is_vague_reason(reason, min_len=min_len),
            )
        )
    return out


def x_parse_overrides__mutmut_11(
    text: str,
    override_re: re.Pattern[str],
    *,
    min_len: int = OVERRIDE_MIN_REASON_LEN,
) -> list[Override]:
    """Parse every acknowledgement line in ``text`` using ``override_re``.

    ``text`` is typically a commit message or PR body. Lines that don't match
    are ignored. Each match becomes an :class:`Override` with ``vague`` computed
    via :func:`is_vague_reason`. ``min_len`` is forwarded to
    :func:`is_vague_reason` and defaults to :data:`OVERRIDE_MIN_REASON_LEN`
    (=40), so the v0.1.0 call shape is unchanged; pass ``min_len=10`` for
    tc-agent-zone's shell-directive floor.
    """
    out: list[Override] = []
    for line in (text or "").splitlines():
        match = override_re.match(line)
        if not match:
            continue
        reason = match.group("REASON").strip()
        out.append(
            Override(
                target=match.group("target"),
                reason=reason,
                vague=is_vague_reason(reason, min_len=min_len),
            )
        )
    return out


def x_parse_overrides__mutmut_12(
    text: str,
    override_re: re.Pattern[str],
    *,
    min_len: int = OVERRIDE_MIN_REASON_LEN,
) -> list[Override]:
    """Parse every acknowledgement line in ``text`` using ``override_re``.

    ``text`` is typically a commit message or PR body. Lines that don't match
    are ignored. Each match becomes an :class:`Override` with ``vague`` computed
    via :func:`is_vague_reason`. ``min_len`` is forwarded to
    :func:`is_vague_reason` and defaults to :data:`OVERRIDE_MIN_REASON_LEN`
    (=40), so the v0.1.0 call shape is unchanged; pass ``min_len=10`` for
    tc-agent-zone's shell-directive floor.
    """
    out: list[Override] = []
    for line in (text or "").splitlines():
        match = override_re.match(line)
        if not match:
            continue
        reason = match.group("reason").strip()
        out.append(
            None
        )
    return out


def x_parse_overrides__mutmut_13(
    text: str,
    override_re: re.Pattern[str],
    *,
    min_len: int = OVERRIDE_MIN_REASON_LEN,
) -> list[Override]:
    """Parse every acknowledgement line in ``text`` using ``override_re``.

    ``text`` is typically a commit message or PR body. Lines that don't match
    are ignored. Each match becomes an :class:`Override` with ``vague`` computed
    via :func:`is_vague_reason`. ``min_len`` is forwarded to
    :func:`is_vague_reason` and defaults to :data:`OVERRIDE_MIN_REASON_LEN`
    (=40), so the v0.1.0 call shape is unchanged; pass ``min_len=10`` for
    tc-agent-zone's shell-directive floor.
    """
    out: list[Override] = []
    for line in (text or "").splitlines():
        match = override_re.match(line)
        if not match:
            continue
        reason = match.group("reason").strip()
        out.append(
            Override(
                target=None,
                reason=reason,
                vague=is_vague_reason(reason, min_len=min_len),
            )
        )
    return out


def x_parse_overrides__mutmut_14(
    text: str,
    override_re: re.Pattern[str],
    *,
    min_len: int = OVERRIDE_MIN_REASON_LEN,
) -> list[Override]:
    """Parse every acknowledgement line in ``text`` using ``override_re``.

    ``text`` is typically a commit message or PR body. Lines that don't match
    are ignored. Each match becomes an :class:`Override` with ``vague`` computed
    via :func:`is_vague_reason`. ``min_len`` is forwarded to
    :func:`is_vague_reason` and defaults to :data:`OVERRIDE_MIN_REASON_LEN`
    (=40), so the v0.1.0 call shape is unchanged; pass ``min_len=10`` for
    tc-agent-zone's shell-directive floor.
    """
    out: list[Override] = []
    for line in (text or "").splitlines():
        match = override_re.match(line)
        if not match:
            continue
        reason = match.group("reason").strip()
        out.append(
            Override(
                target=match.group("target"),
                reason=None,
                vague=is_vague_reason(reason, min_len=min_len),
            )
        )
    return out


def x_parse_overrides__mutmut_15(
    text: str,
    override_re: re.Pattern[str],
    *,
    min_len: int = OVERRIDE_MIN_REASON_LEN,
) -> list[Override]:
    """Parse every acknowledgement line in ``text`` using ``override_re``.

    ``text`` is typically a commit message or PR body. Lines that don't match
    are ignored. Each match becomes an :class:`Override` with ``vague`` computed
    via :func:`is_vague_reason`. ``min_len`` is forwarded to
    :func:`is_vague_reason` and defaults to :data:`OVERRIDE_MIN_REASON_LEN`
    (=40), so the v0.1.0 call shape is unchanged; pass ``min_len=10`` for
    tc-agent-zone's shell-directive floor.
    """
    out: list[Override] = []
    for line in (text or "").splitlines():
        match = override_re.match(line)
        if not match:
            continue
        reason = match.group("reason").strip()
        out.append(
            Override(
                target=match.group("target"),
                reason=reason,
                vague=None,
            )
        )
    return out


def x_parse_overrides__mutmut_16(
    text: str,
    override_re: re.Pattern[str],
    *,
    min_len: int = OVERRIDE_MIN_REASON_LEN,
) -> list[Override]:
    """Parse every acknowledgement line in ``text`` using ``override_re``.

    ``text`` is typically a commit message or PR body. Lines that don't match
    are ignored. Each match becomes an :class:`Override` with ``vague`` computed
    via :func:`is_vague_reason`. ``min_len`` is forwarded to
    :func:`is_vague_reason` and defaults to :data:`OVERRIDE_MIN_REASON_LEN`
    (=40), so the v0.1.0 call shape is unchanged; pass ``min_len=10`` for
    tc-agent-zone's shell-directive floor.
    """
    out: list[Override] = []
    for line in (text or "").splitlines():
        match = override_re.match(line)
        if not match:
            continue
        reason = match.group("reason").strip()
        out.append(
            Override(
                reason=reason,
                vague=is_vague_reason(reason, min_len=min_len),
            )
        )
    return out


def x_parse_overrides__mutmut_17(
    text: str,
    override_re: re.Pattern[str],
    *,
    min_len: int = OVERRIDE_MIN_REASON_LEN,
) -> list[Override]:
    """Parse every acknowledgement line in ``text`` using ``override_re``.

    ``text`` is typically a commit message or PR body. Lines that don't match
    are ignored. Each match becomes an :class:`Override` with ``vague`` computed
    via :func:`is_vague_reason`. ``min_len`` is forwarded to
    :func:`is_vague_reason` and defaults to :data:`OVERRIDE_MIN_REASON_LEN`
    (=40), so the v0.1.0 call shape is unchanged; pass ``min_len=10`` for
    tc-agent-zone's shell-directive floor.
    """
    out: list[Override] = []
    for line in (text or "").splitlines():
        match = override_re.match(line)
        if not match:
            continue
        reason = match.group("reason").strip()
        out.append(
            Override(
                target=match.group("target"),
                vague=is_vague_reason(reason, min_len=min_len),
            )
        )
    return out


def x_parse_overrides__mutmut_18(
    text: str,
    override_re: re.Pattern[str],
    *,
    min_len: int = OVERRIDE_MIN_REASON_LEN,
) -> list[Override]:
    """Parse every acknowledgement line in ``text`` using ``override_re``.

    ``text`` is typically a commit message or PR body. Lines that don't match
    are ignored. Each match becomes an :class:`Override` with ``vague`` computed
    via :func:`is_vague_reason`. ``min_len`` is forwarded to
    :func:`is_vague_reason` and defaults to :data:`OVERRIDE_MIN_REASON_LEN`
    (=40), so the v0.1.0 call shape is unchanged; pass ``min_len=10`` for
    tc-agent-zone's shell-directive floor.
    """
    out: list[Override] = []
    for line in (text or "").splitlines():
        match = override_re.match(line)
        if not match:
            continue
        reason = match.group("reason").strip()
        out.append(
            Override(
                target=match.group("target"),
                reason=reason,
                )
        )
    return out


def x_parse_overrides__mutmut_19(
    text: str,
    override_re: re.Pattern[str],
    *,
    min_len: int = OVERRIDE_MIN_REASON_LEN,
) -> list[Override]:
    """Parse every acknowledgement line in ``text`` using ``override_re``.

    ``text`` is typically a commit message or PR body. Lines that don't match
    are ignored. Each match becomes an :class:`Override` with ``vague`` computed
    via :func:`is_vague_reason`. ``min_len`` is forwarded to
    :func:`is_vague_reason` and defaults to :data:`OVERRIDE_MIN_REASON_LEN`
    (=40), so the v0.1.0 call shape is unchanged; pass ``min_len=10`` for
    tc-agent-zone's shell-directive floor.
    """
    out: list[Override] = []
    for line in (text or "").splitlines():
        match = override_re.match(line)
        if not match:
            continue
        reason = match.group("reason").strip()
        out.append(
            Override(
                target=match.group(None),
                reason=reason,
                vague=is_vague_reason(reason, min_len=min_len),
            )
        )
    return out


def x_parse_overrides__mutmut_20(
    text: str,
    override_re: re.Pattern[str],
    *,
    min_len: int = OVERRIDE_MIN_REASON_LEN,
) -> list[Override]:
    """Parse every acknowledgement line in ``text`` using ``override_re``.

    ``text`` is typically a commit message or PR body. Lines that don't match
    are ignored. Each match becomes an :class:`Override` with ``vague`` computed
    via :func:`is_vague_reason`. ``min_len`` is forwarded to
    :func:`is_vague_reason` and defaults to :data:`OVERRIDE_MIN_REASON_LEN`
    (=40), so the v0.1.0 call shape is unchanged; pass ``min_len=10`` for
    tc-agent-zone's shell-directive floor.
    """
    out: list[Override] = []
    for line in (text or "").splitlines():
        match = override_re.match(line)
        if not match:
            continue
        reason = match.group("reason").strip()
        out.append(
            Override(
                target=match.group("XXtargetXX"),
                reason=reason,
                vague=is_vague_reason(reason, min_len=min_len),
            )
        )
    return out


def x_parse_overrides__mutmut_21(
    text: str,
    override_re: re.Pattern[str],
    *,
    min_len: int = OVERRIDE_MIN_REASON_LEN,
) -> list[Override]:
    """Parse every acknowledgement line in ``text`` using ``override_re``.

    ``text`` is typically a commit message or PR body. Lines that don't match
    are ignored. Each match becomes an :class:`Override` with ``vague`` computed
    via :func:`is_vague_reason`. ``min_len`` is forwarded to
    :func:`is_vague_reason` and defaults to :data:`OVERRIDE_MIN_REASON_LEN`
    (=40), so the v0.1.0 call shape is unchanged; pass ``min_len=10`` for
    tc-agent-zone's shell-directive floor.
    """
    out: list[Override] = []
    for line in (text or "").splitlines():
        match = override_re.match(line)
        if not match:
            continue
        reason = match.group("reason").strip()
        out.append(
            Override(
                target=match.group("TARGET"),
                reason=reason,
                vague=is_vague_reason(reason, min_len=min_len),
            )
        )
    return out


def x_parse_overrides__mutmut_22(
    text: str,
    override_re: re.Pattern[str],
    *,
    min_len: int = OVERRIDE_MIN_REASON_LEN,
) -> list[Override]:
    """Parse every acknowledgement line in ``text`` using ``override_re``.

    ``text`` is typically a commit message or PR body. Lines that don't match
    are ignored. Each match becomes an :class:`Override` with ``vague`` computed
    via :func:`is_vague_reason`. ``min_len`` is forwarded to
    :func:`is_vague_reason` and defaults to :data:`OVERRIDE_MIN_REASON_LEN`
    (=40), so the v0.1.0 call shape is unchanged; pass ``min_len=10`` for
    tc-agent-zone's shell-directive floor.
    """
    out: list[Override] = []
    for line in (text or "").splitlines():
        match = override_re.match(line)
        if not match:
            continue
        reason = match.group("reason").strip()
        out.append(
            Override(
                target=match.group("target"),
                reason=reason,
                vague=is_vague_reason(None, min_len=min_len),
            )
        )
    return out


def x_parse_overrides__mutmut_23(
    text: str,
    override_re: re.Pattern[str],
    *,
    min_len: int = OVERRIDE_MIN_REASON_LEN,
) -> list[Override]:
    """Parse every acknowledgement line in ``text`` using ``override_re``.

    ``text`` is typically a commit message or PR body. Lines that don't match
    are ignored. Each match becomes an :class:`Override` with ``vague`` computed
    via :func:`is_vague_reason`. ``min_len`` is forwarded to
    :func:`is_vague_reason` and defaults to :data:`OVERRIDE_MIN_REASON_LEN`
    (=40), so the v0.1.0 call shape is unchanged; pass ``min_len=10`` for
    tc-agent-zone's shell-directive floor.
    """
    out: list[Override] = []
    for line in (text or "").splitlines():
        match = override_re.match(line)
        if not match:
            continue
        reason = match.group("reason").strip()
        out.append(
            Override(
                target=match.group("target"),
                reason=reason,
                vague=is_vague_reason(reason, min_len=None),
            )
        )
    return out


def x_parse_overrides__mutmut_24(
    text: str,
    override_re: re.Pattern[str],
    *,
    min_len: int = OVERRIDE_MIN_REASON_LEN,
) -> list[Override]:
    """Parse every acknowledgement line in ``text`` using ``override_re``.

    ``text`` is typically a commit message or PR body. Lines that don't match
    are ignored. Each match becomes an :class:`Override` with ``vague`` computed
    via :func:`is_vague_reason`. ``min_len`` is forwarded to
    :func:`is_vague_reason` and defaults to :data:`OVERRIDE_MIN_REASON_LEN`
    (=40), so the v0.1.0 call shape is unchanged; pass ``min_len=10`` for
    tc-agent-zone's shell-directive floor.
    """
    out: list[Override] = []
    for line in (text or "").splitlines():
        match = override_re.match(line)
        if not match:
            continue
        reason = match.group("reason").strip()
        out.append(
            Override(
                target=match.group("target"),
                reason=reason,
                vague=is_vague_reason(min_len=min_len),
            )
        )
    return out


def x_parse_overrides__mutmut_25(
    text: str,
    override_re: re.Pattern[str],
    *,
    min_len: int = OVERRIDE_MIN_REASON_LEN,
) -> list[Override]:
    """Parse every acknowledgement line in ``text`` using ``override_re``.

    ``text`` is typically a commit message or PR body. Lines that don't match
    are ignored. Each match becomes an :class:`Override` with ``vague`` computed
    via :func:`is_vague_reason`. ``min_len`` is forwarded to
    :func:`is_vague_reason` and defaults to :data:`OVERRIDE_MIN_REASON_LEN`
    (=40), so the v0.1.0 call shape is unchanged; pass ``min_len=10`` for
    tc-agent-zone's shell-directive floor.
    """
    out: list[Override] = []
    for line in (text or "").splitlines():
        match = override_re.match(line)
        if not match:
            continue
        reason = match.group("reason").strip()
        out.append(
            Override(
                target=match.group("target"),
                reason=reason,
                vague=is_vague_reason(reason, ),
            )
        )
    return out

mutants_x_parse_overrides__mutmut['_mutmut_orig'] = x_parse_overrides__mutmut_orig # type: ignore # mutmut generated
mutants_x_parse_overrides__mutmut['x_parse_overrides__mutmut_1'] = x_parse_overrides__mutmut_1 # type: ignore # mutmut generated
mutants_x_parse_overrides__mutmut['x_parse_overrides__mutmut_2'] = x_parse_overrides__mutmut_2 # type: ignore # mutmut generated
mutants_x_parse_overrides__mutmut['x_parse_overrides__mutmut_3'] = x_parse_overrides__mutmut_3 # type: ignore # mutmut generated
mutants_x_parse_overrides__mutmut['x_parse_overrides__mutmut_4'] = x_parse_overrides__mutmut_4 # type: ignore # mutmut generated
mutants_x_parse_overrides__mutmut['x_parse_overrides__mutmut_5'] = x_parse_overrides__mutmut_5 # type: ignore # mutmut generated
mutants_x_parse_overrides__mutmut['x_parse_overrides__mutmut_6'] = x_parse_overrides__mutmut_6 # type: ignore # mutmut generated
mutants_x_parse_overrides__mutmut['x_parse_overrides__mutmut_7'] = x_parse_overrides__mutmut_7 # type: ignore # mutmut generated
mutants_x_parse_overrides__mutmut['x_parse_overrides__mutmut_8'] = x_parse_overrides__mutmut_8 # type: ignore # mutmut generated
mutants_x_parse_overrides__mutmut['x_parse_overrides__mutmut_9'] = x_parse_overrides__mutmut_9 # type: ignore # mutmut generated
mutants_x_parse_overrides__mutmut['x_parse_overrides__mutmut_10'] = x_parse_overrides__mutmut_10 # type: ignore # mutmut generated
mutants_x_parse_overrides__mutmut['x_parse_overrides__mutmut_11'] = x_parse_overrides__mutmut_11 # type: ignore # mutmut generated
mutants_x_parse_overrides__mutmut['x_parse_overrides__mutmut_12'] = x_parse_overrides__mutmut_12 # type: ignore # mutmut generated
mutants_x_parse_overrides__mutmut['x_parse_overrides__mutmut_13'] = x_parse_overrides__mutmut_13 # type: ignore # mutmut generated
mutants_x_parse_overrides__mutmut['x_parse_overrides__mutmut_14'] = x_parse_overrides__mutmut_14 # type: ignore # mutmut generated
mutants_x_parse_overrides__mutmut['x_parse_overrides__mutmut_15'] = x_parse_overrides__mutmut_15 # type: ignore # mutmut generated
mutants_x_parse_overrides__mutmut['x_parse_overrides__mutmut_16'] = x_parse_overrides__mutmut_16 # type: ignore # mutmut generated
mutants_x_parse_overrides__mutmut['x_parse_overrides__mutmut_17'] = x_parse_overrides__mutmut_17 # type: ignore # mutmut generated
mutants_x_parse_overrides__mutmut['x_parse_overrides__mutmut_18'] = x_parse_overrides__mutmut_18 # type: ignore # mutmut generated
mutants_x_parse_overrides__mutmut['x_parse_overrides__mutmut_19'] = x_parse_overrides__mutmut_19 # type: ignore # mutmut generated
mutants_x_parse_overrides__mutmut['x_parse_overrides__mutmut_20'] = x_parse_overrides__mutmut_20 # type: ignore # mutmut generated
mutants_x_parse_overrides__mutmut['x_parse_overrides__mutmut_21'] = x_parse_overrides__mutmut_21 # type: ignore # mutmut generated
mutants_x_parse_overrides__mutmut['x_parse_overrides__mutmut_22'] = x_parse_overrides__mutmut_22 # type: ignore # mutmut generated
mutants_x_parse_overrides__mutmut['x_parse_overrides__mutmut_23'] = x_parse_overrides__mutmut_23 # type: ignore # mutmut generated
mutants_x_parse_overrides__mutmut['x_parse_overrides__mutmut_24'] = x_parse_overrides__mutmut_24 # type: ignore # mutmut generated
mutants_x_parse_overrides__mutmut['x_parse_overrides__mutmut_25'] = x_parse_overrides__mutmut_25 # type: ignore # mutmut generated


# ---------------------------------------------------------------------------
# Drift zone 2 — ONE suppression grammar (superset)
# ---------------------------------------------------------------------------

#: Substring suppression markers — the superset of every marker either repo
#: tracked. Used by no-production-suppressions style sweeps that flag any line
#: CONTAINING one of these (rationale or not).
SUPPRESSION_PATTERNS: tuple[str, ...] = (
    "# pragma: no cover",
    "# NOSONAR",
    "// NOSONAR",
    "# noqa:",
    "// noqa:",
    "# type: ignore",
    "# nosec",
)

#: End-of-line "bare suppression" regexes — a suppression token followed only by
#: optional whitespace, i.e. NO trailing rationale. Used by the
#: suppressions-have-rationale gate: a match is a BARE (failing) suppression; a
#: line carrying a same-line rationale after the token does NOT match. Possessive
#: quantifiers keep the code/space classes from backtracking against trailing
#: whitespace. ``NOSONAR`` is included (the tc-agent-zone addition).
BARE_SUPPRESSION_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"#\s*+NOSONAR\s*+$"),
    re.compile(r"#\s*+noqa(?::\s*+[A-Z0-9, ]++)?\s*+$"),
    re.compile(r"#\s*+pragma:\s*+no cover\s*+$"),
    re.compile(r"#\s*+type:\s*+ignore(\[[A-Za-z0-9,_-]+\])?\s*+$"),
    re.compile(r"#\s*+nosec(\s++B\d++|:\s*+B?\d++)?\s*+$"),
)
mutants_x_contains_suppression__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_contains_suppression__mutmut)
def contains_suppression(line: str) -> bool:
    """Return True when ``line`` contains any suppression marker (rationale or not)."""
    return any(pattern in line for pattern in SUPPRESSION_PATTERNS)


def x_contains_suppression__mutmut_orig(line: str) -> bool:
    """Return True when ``line`` contains any suppression marker (rationale or not)."""
    return any(pattern in line for pattern in SUPPRESSION_PATTERNS)


def x_contains_suppression__mutmut_1(line: str) -> bool:
    """Return True when ``line`` contains any suppression marker (rationale or not)."""
    return any(None)


def x_contains_suppression__mutmut_2(line: str) -> bool:
    """Return True when ``line`` contains any suppression marker (rationale or not)."""
    return any(pattern not in line for pattern in SUPPRESSION_PATTERNS)

mutants_x_contains_suppression__mutmut['_mutmut_orig'] = x_contains_suppression__mutmut_orig # type: ignore # mutmut generated
mutants_x_contains_suppression__mutmut['x_contains_suppression__mutmut_1'] = x_contains_suppression__mutmut_1 # type: ignore # mutmut generated
mutants_x_contains_suppression__mutmut['x_contains_suppression__mutmut_2'] = x_contains_suppression__mutmut_2 # type: ignore # mutmut generated
mutants_x_is_bare_suppression__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_is_bare_suppression__mutmut)
def is_bare_suppression(line: str) -> bool:
    """Return True when ``line`` ends in a suppression token with NO rationale after it."""
    return any(pattern.search(line) for pattern in BARE_SUPPRESSION_PATTERNS)


def x_is_bare_suppression__mutmut_orig(line: str) -> bool:
    """Return True when ``line`` ends in a suppression token with NO rationale after it."""
    return any(pattern.search(line) for pattern in BARE_SUPPRESSION_PATTERNS)


def x_is_bare_suppression__mutmut_1(line: str) -> bool:
    """Return True when ``line`` ends in a suppression token with NO rationale after it."""
    return any(None)


def x_is_bare_suppression__mutmut_2(line: str) -> bool:
    """Return True when ``line`` ends in a suppression token with NO rationale after it."""
    return any(pattern.search(None) for pattern in BARE_SUPPRESSION_PATTERNS)

mutants_x_is_bare_suppression__mutmut['_mutmut_orig'] = x_is_bare_suppression__mutmut_orig # type: ignore # mutmut generated
mutants_x_is_bare_suppression__mutmut['x_is_bare_suppression__mutmut_1'] = x_is_bare_suppression__mutmut_1 # type: ignore # mutmut generated
mutants_x_is_bare_suppression__mutmut['x_is_bare_suppression__mutmut_2'] = x_is_bare_suppression__mutmut_2 # type: ignore # mutmut generated


__all__ = [
    "OVERRIDE_MIN_REASON_LEN",
    "VAGUE_OVERRIDE_RE",
    "Override",
    "make_override_re",
    "COVERAGE_OVERRIDE_RE",
    "MUTATION_OVERRIDE_RE",
    "is_vague_reason",
    "parse_overrides",
    "SUPPRESSION_PATTERNS",
    "BARE_SUPPRESSION_PATTERNS",
    "contains_suppression",
    "is_bare_suppression",
]
