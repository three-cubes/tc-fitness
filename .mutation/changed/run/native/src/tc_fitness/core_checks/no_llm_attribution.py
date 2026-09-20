"""CORE check: no_llm_attribution — no AI/LLM self-attribution residue.

Machine-enforced clean authorship (Autonomous Delivery Platform decision D1,
SP-A / SGO-156): agent work is authored by the accountable bot/human identity,
never advertised as model-generated. This rule FAILS when AI-attribution
residue appears in the repo — a ``Co-Authored-By: Claude`` trailer, a
``Generated with <AI tool>`` credit, an AI-vendor ``noreply`` author email, or
the robot emoji (U+1F916) that tools append to commit/PR metadata.

Unlike most CORE checks, the banned set here is **intrinsic, not repo config**:
the attribution *signatures* are provider-neutral and universal, so the engine
ships them as sensible defaults (a consumer only supplies the scan ``roots`` /
``extensions``).

Two surfaces share ONE detector, :func:`scan_text`:

* the :class:`FitnessRule` below scans in-repo files for residue, and
* the standalone :func:`scan_text` is reused by the shipped commit-msg strip
  hook (SGO-159) and the CI trailer-reject leg (SGO-160) to scan commit
  messages and PR title/body — so the pattern set is single-sourced and can
  never drift between the local hook, CI, and the fitness gate.

Every attribution finding is a hard failure.
"""

from __future__ import annotations

import re
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any, NamedTuple

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: The robot emoji (U+1F916) tools append to Claude Code commit/PR metadata.
_ROBOT = "\U0001f916"

#: Provider-neutral AI/agent tool tokens that make a trailer/credit an
#: *attribution* rather than an ordinary mention.
_AI_TOOL = r"(?:claude|anthropic|cursor|copilot|codex|gemini|chatgpt|gpt-?[0-9]|an ai|ai assist(?:ant|ance))"

#: (signature-name, compiled pattern). Intrinsic + provider-neutral — a bare
#: mention of a vendor's *name* is NOT matched; only attribution SIGNATURES are.
SIGNATURES: tuple[tuple[str, re.Pattern[str]], ...] = (
    # A Co-Authored-By / Signed-off-by / Assisted-by trailer that names an AI tool.
    (
        "attribution_trailer",
        re.compile(
            rf"(?im)^[ \t]*(?:co-authored-by|signed-off-by|assisted-by|generated-by)\s*:[^\n]*\b{_AI_TOOL}\b"
        ),
    ),
    # "Generated with [Claude Code]" / "generated with an AI" style credit lines.
    ("generated_with", re.compile(rf"(?i)generated (?:with|by)\s+\[?{_AI_TOOL}\b")),
    # An AI-vendor no-reply author/committer email.
    ("anthropic_noreply", re.compile(r"(?i)\bnoreply@anthropic\.com\b")),
    # The robot emoji tools stamp onto commit/PR metadata.
    ("robot_emoji", re.compile(_ROBOT)),
)

DEFAULT_EXTENSIONS = (
    ".md",
    ".markdown",
    ".txt",
    ".rst",
    ".py",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".sh",
    ".yaml",
    ".yml",
    ".toml",
    ".json",
    ".html",
    ".feature",
)

REMEDIATION = _remediation(
    fix=(
        "remove the AI/LLM self-attribution — strip the `Co-Authored-By: <model>` / "
        "`Generated with <tool>` trailer, the robot emoji, or the `noreply@anthropic.com` "
        "identity. Agent work is authored by the canonical bot/human, never advertised as "
        "model-generated. If an in-source string is genuinely functional (names the tool "
        "without claiming authorship), add its path to this check's `exempt_files`."
    ),
    nxt="re-run this check to confirm it goes green.",
    run="python -m tc_fitness.core_checks.no_llm_attribution",
    passing="Co-Authored-By: Jane Doe <jane@example.com>   # a real accountable human",
    forbidden="Co-Authored-By: Claude <noreply@anthropic.com>   # AI self-attribution",
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


class Hit(NamedTuple):
    """One attribution-signature match: which signature, and the matched text."""

    signature: str
    match: str
mutants_x_scan_text__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_scan_text__mutmut)
def scan_text(text: str) -> list[Hit]:
    """Return every AI-attribution signature match in ``text`` (empty == clean).

    The single detector shared by the file scan, the commit-msg strip hook, and
    the CI trailer-reject leg. Keys on attribution *signatures* (trailers,
    credits, vendor no-reply emails, the robot emoji) — a bare mention of a
    vendor's name in ordinary prose or a genuine human co-author trailer does
    NOT match.
    """
    hits: list[Hit] = []
    for name, pattern in SIGNATURES:
        for m in pattern.finditer(text):
            hits.append(Hit(name, m.group(0)))
    return hits


def x_scan_text__mutmut_orig(text: str) -> list[Hit]:
    """Return every AI-attribution signature match in ``text`` (empty == clean).

    The single detector shared by the file scan, the commit-msg strip hook, and
    the CI trailer-reject leg. Keys on attribution *signatures* (trailers,
    credits, vendor no-reply emails, the robot emoji) — a bare mention of a
    vendor's name in ordinary prose or a genuine human co-author trailer does
    NOT match.
    """
    hits: list[Hit] = []
    for name, pattern in SIGNATURES:
        for m in pattern.finditer(text):
            hits.append(Hit(name, m.group(0)))
    return hits


def x_scan_text__mutmut_1(text: str) -> list[Hit]:
    """Return every AI-attribution signature match in ``text`` (empty == clean).

    The single detector shared by the file scan, the commit-msg strip hook, and
    the CI trailer-reject leg. Keys on attribution *signatures* (trailers,
    credits, vendor no-reply emails, the robot emoji) — a bare mention of a
    vendor's name in ordinary prose or a genuine human co-author trailer does
    NOT match.
    """
    hits: list[Hit] = None
    for name, pattern in SIGNATURES:
        for m in pattern.finditer(text):
            hits.append(Hit(name, m.group(0)))
    return hits


def x_scan_text__mutmut_2(text: str) -> list[Hit]:
    """Return every AI-attribution signature match in ``text`` (empty == clean).

    The single detector shared by the file scan, the commit-msg strip hook, and
    the CI trailer-reject leg. Keys on attribution *signatures* (trailers,
    credits, vendor no-reply emails, the robot emoji) — a bare mention of a
    vendor's name in ordinary prose or a genuine human co-author trailer does
    NOT match.
    """
    hits: list[Hit] = []
    for name, pattern in SIGNATURES:
        for m in pattern.finditer(None):
            hits.append(Hit(name, m.group(0)))
    return hits


def x_scan_text__mutmut_3(text: str) -> list[Hit]:
    """Return every AI-attribution signature match in ``text`` (empty == clean).

    The single detector shared by the file scan, the commit-msg strip hook, and
    the CI trailer-reject leg. Keys on attribution *signatures* (trailers,
    credits, vendor no-reply emails, the robot emoji) — a bare mention of a
    vendor's name in ordinary prose or a genuine human co-author trailer does
    NOT match.
    """
    hits: list[Hit] = []
    for name, pattern in SIGNATURES:
        for m in pattern.finditer(text):
            hits.append(None)
    return hits


def x_scan_text__mutmut_4(text: str) -> list[Hit]:
    """Return every AI-attribution signature match in ``text`` (empty == clean).

    The single detector shared by the file scan, the commit-msg strip hook, and
    the CI trailer-reject leg. Keys on attribution *signatures* (trailers,
    credits, vendor no-reply emails, the robot emoji) — a bare mention of a
    vendor's name in ordinary prose or a genuine human co-author trailer does
    NOT match.
    """
    hits: list[Hit] = []
    for name, pattern in SIGNATURES:
        for m in pattern.finditer(text):
            hits.append(Hit(None, m.group(0)))
    return hits


def x_scan_text__mutmut_5(text: str) -> list[Hit]:
    """Return every AI-attribution signature match in ``text`` (empty == clean).

    The single detector shared by the file scan, the commit-msg strip hook, and
    the CI trailer-reject leg. Keys on attribution *signatures* (trailers,
    credits, vendor no-reply emails, the robot emoji) — a bare mention of a
    vendor's name in ordinary prose or a genuine human co-author trailer does
    NOT match.
    """
    hits: list[Hit] = []
    for name, pattern in SIGNATURES:
        for m in pattern.finditer(text):
            hits.append(Hit(name, None))
    return hits


def x_scan_text__mutmut_6(text: str) -> list[Hit]:
    """Return every AI-attribution signature match in ``text`` (empty == clean).

    The single detector shared by the file scan, the commit-msg strip hook, and
    the CI trailer-reject leg. Keys on attribution *signatures* (trailers,
    credits, vendor no-reply emails, the robot emoji) — a bare mention of a
    vendor's name in ordinary prose or a genuine human co-author trailer does
    NOT match.
    """
    hits: list[Hit] = []
    for name, pattern in SIGNATURES:
        for m in pattern.finditer(text):
            hits.append(Hit(m.group(0)))
    return hits


def x_scan_text__mutmut_7(text: str) -> list[Hit]:
    """Return every AI-attribution signature match in ``text`` (empty == clean).

    The single detector shared by the file scan, the commit-msg strip hook, and
    the CI trailer-reject leg. Keys on attribution *signatures* (trailers,
    credits, vendor no-reply emails, the robot emoji) — a bare mention of a
    vendor's name in ordinary prose or a genuine human co-author trailer does
    NOT match.
    """
    hits: list[Hit] = []
    for name, pattern in SIGNATURES:
        for m in pattern.finditer(text):
            hits.append(Hit(name, ))
    return hits


def x_scan_text__mutmut_8(text: str) -> list[Hit]:
    """Return every AI-attribution signature match in ``text`` (empty == clean).

    The single detector shared by the file scan, the commit-msg strip hook, and
    the CI trailer-reject leg. Keys on attribution *signatures* (trailers,
    credits, vendor no-reply emails, the robot emoji) — a bare mention of a
    vendor's name in ordinary prose or a genuine human co-author trailer does
    NOT match.
    """
    hits: list[Hit] = []
    for name, pattern in SIGNATURES:
        for m in pattern.finditer(text):
            hits.append(Hit(name, m.group(None)))
    return hits


def x_scan_text__mutmut_9(text: str) -> list[Hit]:
    """Return every AI-attribution signature match in ``text`` (empty == clean).

    The single detector shared by the file scan, the commit-msg strip hook, and
    the CI trailer-reject leg. Keys on attribution *signatures* (trailers,
    credits, vendor no-reply emails, the robot emoji) — a bare mention of a
    vendor's name in ordinary prose or a genuine human co-author trailer does
    NOT match.
    """
    hits: list[Hit] = []
    for name, pattern in SIGNATURES:
        for m in pattern.finditer(text):
            hits.append(Hit(name, m.group(1)))
    return hits

mutants_x_scan_text__mutmut['_mutmut_orig'] = x_scan_text__mutmut_orig # type: ignore # mutmut generated
mutants_x_scan_text__mutmut['x_scan_text__mutmut_1'] = x_scan_text__mutmut_1 # type: ignore # mutmut generated
mutants_x_scan_text__mutmut['x_scan_text__mutmut_2'] = x_scan_text__mutmut_2 # type: ignore # mutmut generated
mutants_x_scan_text__mutmut['x_scan_text__mutmut_3'] = x_scan_text__mutmut_3 # type: ignore # mutmut generated
mutants_x_scan_text__mutmut['x_scan_text__mutmut_4'] = x_scan_text__mutmut_4 # type: ignore # mutmut generated
mutants_x_scan_text__mutmut['x_scan_text__mutmut_5'] = x_scan_text__mutmut_5 # type: ignore # mutmut generated
mutants_x_scan_text__mutmut['x_scan_text__mutmut_6'] = x_scan_text__mutmut_6 # type: ignore # mutmut generated
mutants_x_scan_text__mutmut['x_scan_text__mutmut_7'] = x_scan_text__mutmut_7 # type: ignore # mutmut generated
mutants_x_scan_text__mutmut['x_scan_text__mutmut_8'] = x_scan_text__mutmut_8 # type: ignore # mutmut generated
mutants_x_scan_text__mutmut['x_scan_text__mutmut_9'] = x_scan_text__mutmut_9 # type: ignore # mutmut generated
mutants_x__is_strippable_line__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__is_strippable_line__mutmut)
def _is_strippable_line(line: str) -> bool:
    """True when the whole line is an attribution trailer/credit (safe to drop).

    A trailer (``Co-Authored-By: Claude``), a ``Generated with <tool>`` credit
    line, or a line that is nothing but the robot emoji. Inline residue (a robot
    emoji mid-sentence, an anthropic email embedded in prose) is NOT a strippable
    line — it survives :func:`strip_text` and is then reported as non-strippable.
    """
    stripped = line.strip()
    if not stripped:
        return False
    if stripped == _ROBOT:
        return True
    return any(h.signature in ("attribution_trailer", "generated_with") for h in scan_text(line))


def x__is_strippable_line__mutmut_orig(line: str) -> bool:
    """True when the whole line is an attribution trailer/credit (safe to drop).

    A trailer (``Co-Authored-By: Claude``), a ``Generated with <tool>`` credit
    line, or a line that is nothing but the robot emoji. Inline residue (a robot
    emoji mid-sentence, an anthropic email embedded in prose) is NOT a strippable
    line — it survives :func:`strip_text` and is then reported as non-strippable.
    """
    stripped = line.strip()
    if not stripped:
        return False
    if stripped == _ROBOT:
        return True
    return any(h.signature in ("attribution_trailer", "generated_with") for h in scan_text(line))


def x__is_strippable_line__mutmut_1(line: str) -> bool:
    """True when the whole line is an attribution trailer/credit (safe to drop).

    A trailer (``Co-Authored-By: Claude``), a ``Generated with <tool>`` credit
    line, or a line that is nothing but the robot emoji. Inline residue (a robot
    emoji mid-sentence, an anthropic email embedded in prose) is NOT a strippable
    line — it survives :func:`strip_text` and is then reported as non-strippable.
    """
    stripped = None
    if not stripped:
        return False
    if stripped == _ROBOT:
        return True
    return any(h.signature in ("attribution_trailer", "generated_with") for h in scan_text(line))


def x__is_strippable_line__mutmut_2(line: str) -> bool:
    """True when the whole line is an attribution trailer/credit (safe to drop).

    A trailer (``Co-Authored-By: Claude``), a ``Generated with <tool>`` credit
    line, or a line that is nothing but the robot emoji. Inline residue (a robot
    emoji mid-sentence, an anthropic email embedded in prose) is NOT a strippable
    line — it survives :func:`strip_text` and is then reported as non-strippable.
    """
    stripped = line.strip()
    if stripped:
        return False
    if stripped == _ROBOT:
        return True
    return any(h.signature in ("attribution_trailer", "generated_with") for h in scan_text(line))


def x__is_strippable_line__mutmut_3(line: str) -> bool:
    """True when the whole line is an attribution trailer/credit (safe to drop).

    A trailer (``Co-Authored-By: Claude``), a ``Generated with <tool>`` credit
    line, or a line that is nothing but the robot emoji. Inline residue (a robot
    emoji mid-sentence, an anthropic email embedded in prose) is NOT a strippable
    line — it survives :func:`strip_text` and is then reported as non-strippable.
    """
    stripped = line.strip()
    if not stripped:
        return True
    if stripped == _ROBOT:
        return True
    return any(h.signature in ("attribution_trailer", "generated_with") for h in scan_text(line))


def x__is_strippable_line__mutmut_4(line: str) -> bool:
    """True when the whole line is an attribution trailer/credit (safe to drop).

    A trailer (``Co-Authored-By: Claude``), a ``Generated with <tool>`` credit
    line, or a line that is nothing but the robot emoji. Inline residue (a robot
    emoji mid-sentence, an anthropic email embedded in prose) is NOT a strippable
    line — it survives :func:`strip_text` and is then reported as non-strippable.
    """
    stripped = line.strip()
    if not stripped:
        return False
    if stripped != _ROBOT:
        return True
    return any(h.signature in ("attribution_trailer", "generated_with") for h in scan_text(line))


def x__is_strippable_line__mutmut_5(line: str) -> bool:
    """True when the whole line is an attribution trailer/credit (safe to drop).

    A trailer (``Co-Authored-By: Claude``), a ``Generated with <tool>`` credit
    line, or a line that is nothing but the robot emoji. Inline residue (a robot
    emoji mid-sentence, an anthropic email embedded in prose) is NOT a strippable
    line — it survives :func:`strip_text` and is then reported as non-strippable.
    """
    stripped = line.strip()
    if not stripped:
        return False
    if stripped == _ROBOT:
        return False
    return any(h.signature in ("attribution_trailer", "generated_with") for h in scan_text(line))


def x__is_strippable_line__mutmut_6(line: str) -> bool:
    """True when the whole line is an attribution trailer/credit (safe to drop).

    A trailer (``Co-Authored-By: Claude``), a ``Generated with <tool>`` credit
    line, or a line that is nothing but the robot emoji. Inline residue (a robot
    emoji mid-sentence, an anthropic email embedded in prose) is NOT a strippable
    line — it survives :func:`strip_text` and is then reported as non-strippable.
    """
    stripped = line.strip()
    if not stripped:
        return False
    if stripped == _ROBOT:
        return True
    return any(None)


def x__is_strippable_line__mutmut_7(line: str) -> bool:
    """True when the whole line is an attribution trailer/credit (safe to drop).

    A trailer (``Co-Authored-By: Claude``), a ``Generated with <tool>`` credit
    line, or a line that is nothing but the robot emoji. Inline residue (a robot
    emoji mid-sentence, an anthropic email embedded in prose) is NOT a strippable
    line — it survives :func:`strip_text` and is then reported as non-strippable.
    """
    stripped = line.strip()
    if not stripped:
        return False
    if stripped == _ROBOT:
        return True
    return any(h.signature not in ("attribution_trailer", "generated_with") for h in scan_text(line))


def x__is_strippable_line__mutmut_8(line: str) -> bool:
    """True when the whole line is an attribution trailer/credit (safe to drop).

    A trailer (``Co-Authored-By: Claude``), a ``Generated with <tool>`` credit
    line, or a line that is nothing but the robot emoji. Inline residue (a robot
    emoji mid-sentence, an anthropic email embedded in prose) is NOT a strippable
    line — it survives :func:`strip_text` and is then reported as non-strippable.
    """
    stripped = line.strip()
    if not stripped:
        return False
    if stripped == _ROBOT:
        return True
    return any(h.signature in ("XXattribution_trailerXX", "generated_with") for h in scan_text(line))


def x__is_strippable_line__mutmut_9(line: str) -> bool:
    """True when the whole line is an attribution trailer/credit (safe to drop).

    A trailer (``Co-Authored-By: Claude``), a ``Generated with <tool>`` credit
    line, or a line that is nothing but the robot emoji. Inline residue (a robot
    emoji mid-sentence, an anthropic email embedded in prose) is NOT a strippable
    line — it survives :func:`strip_text` and is then reported as non-strippable.
    """
    stripped = line.strip()
    if not stripped:
        return False
    if stripped == _ROBOT:
        return True
    return any(h.signature in ("ATTRIBUTION_TRAILER", "generated_with") for h in scan_text(line))


def x__is_strippable_line__mutmut_10(line: str) -> bool:
    """True when the whole line is an attribution trailer/credit (safe to drop).

    A trailer (``Co-Authored-By: Claude``), a ``Generated with <tool>`` credit
    line, or a line that is nothing but the robot emoji. Inline residue (a robot
    emoji mid-sentence, an anthropic email embedded in prose) is NOT a strippable
    line — it survives :func:`strip_text` and is then reported as non-strippable.
    """
    stripped = line.strip()
    if not stripped:
        return False
    if stripped == _ROBOT:
        return True
    return any(h.signature in ("attribution_trailer", "XXgenerated_withXX") for h in scan_text(line))


def x__is_strippable_line__mutmut_11(line: str) -> bool:
    """True when the whole line is an attribution trailer/credit (safe to drop).

    A trailer (``Co-Authored-By: Claude``), a ``Generated with <tool>`` credit
    line, or a line that is nothing but the robot emoji. Inline residue (a robot
    emoji mid-sentence, an anthropic email embedded in prose) is NOT a strippable
    line — it survives :func:`strip_text` and is then reported as non-strippable.
    """
    stripped = line.strip()
    if not stripped:
        return False
    if stripped == _ROBOT:
        return True
    return any(h.signature in ("attribution_trailer", "GENERATED_WITH") for h in scan_text(line))


def x__is_strippable_line__mutmut_12(line: str) -> bool:
    """True when the whole line is an attribution trailer/credit (safe to drop).

    A trailer (``Co-Authored-By: Claude``), a ``Generated with <tool>`` credit
    line, or a line that is nothing but the robot emoji. Inline residue (a robot
    emoji mid-sentence, an anthropic email embedded in prose) is NOT a strippable
    line — it survives :func:`strip_text` and is then reported as non-strippable.
    """
    stripped = line.strip()
    if not stripped:
        return False
    if stripped == _ROBOT:
        return True
    return any(h.signature in ("attribution_trailer", "generated_with") for h in scan_text(None))

mutants_x__is_strippable_line__mutmut['_mutmut_orig'] = x__is_strippable_line__mutmut_orig # type: ignore # mutmut generated
mutants_x__is_strippable_line__mutmut['x__is_strippable_line__mutmut_1'] = x__is_strippable_line__mutmut_1 # type: ignore # mutmut generated
mutants_x__is_strippable_line__mutmut['x__is_strippable_line__mutmut_2'] = x__is_strippable_line__mutmut_2 # type: ignore # mutmut generated
mutants_x__is_strippable_line__mutmut['x__is_strippable_line__mutmut_3'] = x__is_strippable_line__mutmut_3 # type: ignore # mutmut generated
mutants_x__is_strippable_line__mutmut['x__is_strippable_line__mutmut_4'] = x__is_strippable_line__mutmut_4 # type: ignore # mutmut generated
mutants_x__is_strippable_line__mutmut['x__is_strippable_line__mutmut_5'] = x__is_strippable_line__mutmut_5 # type: ignore # mutmut generated
mutants_x__is_strippable_line__mutmut['x__is_strippable_line__mutmut_6'] = x__is_strippable_line__mutmut_6 # type: ignore # mutmut generated
mutants_x__is_strippable_line__mutmut['x__is_strippable_line__mutmut_7'] = x__is_strippable_line__mutmut_7 # type: ignore # mutmut generated
mutants_x__is_strippable_line__mutmut['x__is_strippable_line__mutmut_8'] = x__is_strippable_line__mutmut_8 # type: ignore # mutmut generated
mutants_x__is_strippable_line__mutmut['x__is_strippable_line__mutmut_9'] = x__is_strippable_line__mutmut_9 # type: ignore # mutmut generated
mutants_x__is_strippable_line__mutmut['x__is_strippable_line__mutmut_10'] = x__is_strippable_line__mutmut_10 # type: ignore # mutmut generated
mutants_x__is_strippable_line__mutmut['x__is_strippable_line__mutmut_11'] = x__is_strippable_line__mutmut_11 # type: ignore # mutmut generated
mutants_x__is_strippable_line__mutmut['x__is_strippable_line__mutmut_12'] = x__is_strippable_line__mutmut_12 # type: ignore # mutmut generated
mutants_x_strip_text__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_strip_text__mutmut)
def strip_text(text: str) -> tuple[str, list[str]]:
    """Remove whole attribution-trailer/credit lines; return ``(cleaned, dropped)``.

    Preserves the original trailing-newline shape. Genuine human co-author
    trailers and ordinary prose are kept. Anything the strip cannot safely remove
    as a whole line remains in ``cleaned`` for the caller to reject.
    """
    kept: list[str] = []
    dropped: list[str] = []
    trailing_newlines = len(text) - len(text.rstrip("\n"))
    for line in text.splitlines():
        (dropped if _is_strippable_line(line) else kept).append(line)
    cleaned = "\n".join(kept).rstrip("\n") + ("\n" * trailing_newlines)
    return cleaned, dropped


def x_strip_text__mutmut_orig(text: str) -> tuple[str, list[str]]:
    """Remove whole attribution-trailer/credit lines; return ``(cleaned, dropped)``.

    Preserves the original trailing-newline shape. Genuine human co-author
    trailers and ordinary prose are kept. Anything the strip cannot safely remove
    as a whole line remains in ``cleaned`` for the caller to reject.
    """
    kept: list[str] = []
    dropped: list[str] = []
    trailing_newlines = len(text) - len(text.rstrip("\n"))
    for line in text.splitlines():
        (dropped if _is_strippable_line(line) else kept).append(line)
    cleaned = "\n".join(kept).rstrip("\n") + ("\n" * trailing_newlines)
    return cleaned, dropped


def x_strip_text__mutmut_1(text: str) -> tuple[str, list[str]]:
    """Remove whole attribution-trailer/credit lines; return ``(cleaned, dropped)``.

    Preserves the original trailing-newline shape. Genuine human co-author
    trailers and ordinary prose are kept. Anything the strip cannot safely remove
    as a whole line remains in ``cleaned`` for the caller to reject.
    """
    kept: list[str] = None
    dropped: list[str] = []
    trailing_newlines = len(text) - len(text.rstrip("\n"))
    for line in text.splitlines():
        (dropped if _is_strippable_line(line) else kept).append(line)
    cleaned = "\n".join(kept).rstrip("\n") + ("\n" * trailing_newlines)
    return cleaned, dropped


def x_strip_text__mutmut_2(text: str) -> tuple[str, list[str]]:
    """Remove whole attribution-trailer/credit lines; return ``(cleaned, dropped)``.

    Preserves the original trailing-newline shape. Genuine human co-author
    trailers and ordinary prose are kept. Anything the strip cannot safely remove
    as a whole line remains in ``cleaned`` for the caller to reject.
    """
    kept: list[str] = []
    dropped: list[str] = None
    trailing_newlines = len(text) - len(text.rstrip("\n"))
    for line in text.splitlines():
        (dropped if _is_strippable_line(line) else kept).append(line)
    cleaned = "\n".join(kept).rstrip("\n") + ("\n" * trailing_newlines)
    return cleaned, dropped


def x_strip_text__mutmut_3(text: str) -> tuple[str, list[str]]:
    """Remove whole attribution-trailer/credit lines; return ``(cleaned, dropped)``.

    Preserves the original trailing-newline shape. Genuine human co-author
    trailers and ordinary prose are kept. Anything the strip cannot safely remove
    as a whole line remains in ``cleaned`` for the caller to reject.
    """
    kept: list[str] = []
    dropped: list[str] = []
    trailing_newlines = None
    for line in text.splitlines():
        (dropped if _is_strippable_line(line) else kept).append(line)
    cleaned = "\n".join(kept).rstrip("\n") + ("\n" * trailing_newlines)
    return cleaned, dropped


def x_strip_text__mutmut_4(text: str) -> tuple[str, list[str]]:
    """Remove whole attribution-trailer/credit lines; return ``(cleaned, dropped)``.

    Preserves the original trailing-newline shape. Genuine human co-author
    trailers and ordinary prose are kept. Anything the strip cannot safely remove
    as a whole line remains in ``cleaned`` for the caller to reject.
    """
    kept: list[str] = []
    dropped: list[str] = []
    trailing_newlines = len(text) + len(text.rstrip("\n"))
    for line in text.splitlines():
        (dropped if _is_strippable_line(line) else kept).append(line)
    cleaned = "\n".join(kept).rstrip("\n") + ("\n" * trailing_newlines)
    return cleaned, dropped


def x_strip_text__mutmut_5(text: str) -> tuple[str, list[str]]:
    """Remove whole attribution-trailer/credit lines; return ``(cleaned, dropped)``.

    Preserves the original trailing-newline shape. Genuine human co-author
    trailers and ordinary prose are kept. Anything the strip cannot safely remove
    as a whole line remains in ``cleaned`` for the caller to reject.
    """
    kept: list[str] = []
    dropped: list[str] = []
    trailing_newlines = len(text) - len(text.rstrip("\n"))
    for line in text.splitlines():
        (dropped if _is_strippable_line(line) else kept).append(None)
    cleaned = "\n".join(kept).rstrip("\n") + ("\n" * trailing_newlines)
    return cleaned, dropped


def x_strip_text__mutmut_6(text: str) -> tuple[str, list[str]]:
    """Remove whole attribution-trailer/credit lines; return ``(cleaned, dropped)``.

    Preserves the original trailing-newline shape. Genuine human co-author
    trailers and ordinary prose are kept. Anything the strip cannot safely remove
    as a whole line remains in ``cleaned`` for the caller to reject.
    """
    kept: list[str] = []
    dropped: list[str] = []
    trailing_newlines = len(text) - len(text.rstrip("\n"))
    for line in text.splitlines():
        (dropped if _is_strippable_line(None) else kept).append(line)
    cleaned = "\n".join(kept).rstrip("\n") + ("\n" * trailing_newlines)
    return cleaned, dropped


def x_strip_text__mutmut_7(text: str) -> tuple[str, list[str]]:
    """Remove whole attribution-trailer/credit lines; return ``(cleaned, dropped)``.

    Preserves the original trailing-newline shape. Genuine human co-author
    trailers and ordinary prose are kept. Anything the strip cannot safely remove
    as a whole line remains in ``cleaned`` for the caller to reject.
    """
    kept: list[str] = []
    dropped: list[str] = []
    trailing_newlines = len(text) - len(text.rstrip("\n"))
    for line in text.splitlines():
        (dropped if _is_strippable_line(line) else kept).append(line)
    cleaned = None
    return cleaned, dropped


def x_strip_text__mutmut_8(text: str) -> tuple[str, list[str]]:
    """Remove whole attribution-trailer/credit lines; return ``(cleaned, dropped)``.

    Preserves the original trailing-newline shape. Genuine human co-author
    trailers and ordinary prose are kept. Anything the strip cannot safely remove
    as a whole line remains in ``cleaned`` for the caller to reject.
    """
    kept: list[str] = []
    dropped: list[str] = []
    trailing_newlines = len(text) - len(text.rstrip("\n"))
    for line in text.splitlines():
        (dropped if _is_strippable_line(line) else kept).append(line)
    cleaned = "\n".join(kept).rstrip("\n") - ("\n" * trailing_newlines)
    return cleaned, dropped


def x_strip_text__mutmut_9(text: str) -> tuple[str, list[str]]:
    """Remove whole attribution-trailer/credit lines; return ``(cleaned, dropped)``.

    Preserves the original trailing-newline shape. Genuine human co-author
    trailers and ordinary prose are kept. Anything the strip cannot safely remove
    as a whole line remains in ``cleaned`` for the caller to reject.
    """
    kept: list[str] = []
    dropped: list[str] = []
    trailing_newlines = len(text) - len(text.rstrip("\n"))
    for line in text.splitlines():
        (dropped if _is_strippable_line(line) else kept).append(line)
    cleaned = "\n".join(kept).rstrip(None) + ("\n" * trailing_newlines)
    return cleaned, dropped


def x_strip_text__mutmut_10(text: str) -> tuple[str, list[str]]:
    """Remove whole attribution-trailer/credit lines; return ``(cleaned, dropped)``.

    Preserves the original trailing-newline shape. Genuine human co-author
    trailers and ordinary prose are kept. Anything the strip cannot safely remove
    as a whole line remains in ``cleaned`` for the caller to reject.
    """
    kept: list[str] = []
    dropped: list[str] = []
    trailing_newlines = len(text) - len(text.rstrip("\n"))
    for line in text.splitlines():
        (dropped if _is_strippable_line(line) else kept).append(line)
    cleaned = "\n".join(kept).lstrip("\n") + ("\n" * trailing_newlines)
    return cleaned, dropped


def x_strip_text__mutmut_11(text: str) -> tuple[str, list[str]]:
    """Remove whole attribution-trailer/credit lines; return ``(cleaned, dropped)``.

    Preserves the original trailing-newline shape. Genuine human co-author
    trailers and ordinary prose are kept. Anything the strip cannot safely remove
    as a whole line remains in ``cleaned`` for the caller to reject.
    """
    kept: list[str] = []
    dropped: list[str] = []
    trailing_newlines = len(text) - len(text.rstrip("\n"))
    for line in text.splitlines():
        (dropped if _is_strippable_line(line) else kept).append(line)
    cleaned = "\n".join(None).rstrip("\n") + ("\n" * trailing_newlines)
    return cleaned, dropped


def x_strip_text__mutmut_12(text: str) -> tuple[str, list[str]]:
    """Remove whole attribution-trailer/credit lines; return ``(cleaned, dropped)``.

    Preserves the original trailing-newline shape. Genuine human co-author
    trailers and ordinary prose are kept. Anything the strip cannot safely remove
    as a whole line remains in ``cleaned`` for the caller to reject.
    """
    kept: list[str] = []
    dropped: list[str] = []
    trailing_newlines = len(text) - len(text.rstrip("\n"))
    for line in text.splitlines():
        (dropped if _is_strippable_line(line) else kept).append(line)
    cleaned = "XX\nXX".join(kept).rstrip("\n") + ("\n" * trailing_newlines)
    return cleaned, dropped


def x_strip_text__mutmut_13(text: str) -> tuple[str, list[str]]:
    """Remove whole attribution-trailer/credit lines; return ``(cleaned, dropped)``.

    Preserves the original trailing-newline shape. Genuine human co-author
    trailers and ordinary prose are kept. Anything the strip cannot safely remove
    as a whole line remains in ``cleaned`` for the caller to reject.
    """
    kept: list[str] = []
    dropped: list[str] = []
    trailing_newlines = len(text) - len(text.rstrip("\n"))
    for line in text.splitlines():
        (dropped if _is_strippable_line(line) else kept).append(line)
    cleaned = "\n".join(kept).rstrip("XX\nXX") + ("\n" * trailing_newlines)
    return cleaned, dropped


def x_strip_text__mutmut_14(text: str) -> tuple[str, list[str]]:
    """Remove whole attribution-trailer/credit lines; return ``(cleaned, dropped)``.

    Preserves the original trailing-newline shape. Genuine human co-author
    trailers and ordinary prose are kept. Anything the strip cannot safely remove
    as a whole line remains in ``cleaned`` for the caller to reject.
    """
    kept: list[str] = []
    dropped: list[str] = []
    trailing_newlines = len(text) - len(text.rstrip("\n"))
    for line in text.splitlines():
        (dropped if _is_strippable_line(line) else kept).append(line)
    cleaned = "\n".join(kept).rstrip("\n") + ("\n" / trailing_newlines)
    return cleaned, dropped


def x_strip_text__mutmut_15(text: str) -> tuple[str, list[str]]:
    """Remove whole attribution-trailer/credit lines; return ``(cleaned, dropped)``.

    Preserves the original trailing-newline shape. Genuine human co-author
    trailers and ordinary prose are kept. Anything the strip cannot safely remove
    as a whole line remains in ``cleaned`` for the caller to reject.
    """
    kept: list[str] = []
    dropped: list[str] = []
    trailing_newlines = len(text) - len(text.rstrip("\n"))
    for line in text.splitlines():
        (dropped if _is_strippable_line(line) else kept).append(line)
    cleaned = "\n".join(kept).rstrip("\n") + ("XX\nXX" * trailing_newlines)
    return cleaned, dropped

mutants_x_strip_text__mutmut['_mutmut_orig'] = x_strip_text__mutmut_orig # type: ignore # mutmut generated
mutants_x_strip_text__mutmut['x_strip_text__mutmut_1'] = x_strip_text__mutmut_1 # type: ignore # mutmut generated
mutants_x_strip_text__mutmut['x_strip_text__mutmut_2'] = x_strip_text__mutmut_2 # type: ignore # mutmut generated
mutants_x_strip_text__mutmut['x_strip_text__mutmut_3'] = x_strip_text__mutmut_3 # type: ignore # mutmut generated
mutants_x_strip_text__mutmut['x_strip_text__mutmut_4'] = x_strip_text__mutmut_4 # type: ignore # mutmut generated
mutants_x_strip_text__mutmut['x_strip_text__mutmut_5'] = x_strip_text__mutmut_5 # type: ignore # mutmut generated
mutants_x_strip_text__mutmut['x_strip_text__mutmut_6'] = x_strip_text__mutmut_6 # type: ignore # mutmut generated
mutants_x_strip_text__mutmut['x_strip_text__mutmut_7'] = x_strip_text__mutmut_7 # type: ignore # mutmut generated
mutants_x_strip_text__mutmut['x_strip_text__mutmut_8'] = x_strip_text__mutmut_8 # type: ignore # mutmut generated
mutants_x_strip_text__mutmut['x_strip_text__mutmut_9'] = x_strip_text__mutmut_9 # type: ignore # mutmut generated
mutants_x_strip_text__mutmut['x_strip_text__mutmut_10'] = x_strip_text__mutmut_10 # type: ignore # mutmut generated
mutants_x_strip_text__mutmut['x_strip_text__mutmut_11'] = x_strip_text__mutmut_11 # type: ignore # mutmut generated
mutants_x_strip_text__mutmut['x_strip_text__mutmut_12'] = x_strip_text__mutmut_12 # type: ignore # mutmut generated
mutants_x_strip_text__mutmut['x_strip_text__mutmut_13'] = x_strip_text__mutmut_13 # type: ignore # mutmut generated
mutants_x_strip_text__mutmut['x_strip_text__mutmut_14'] = x_strip_text__mutmut_14 # type: ignore # mutmut generated
mutants_x_strip_text__mutmut['x_strip_text__mutmut_15'] = x_strip_text__mutmut_15 # type: ignore # mutmut generated
mutants_xǁNoLlmAttributionǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore


class NoLlmAttribution(FitnessRule):
    """Flags files carrying AI/LLM self-attribution residue."""

    name = "no-llm-attribution"
    remediation = REMEDIATION
    extensions = DEFAULT_EXTENSIONS

    @_mutmut_mutated(mutants_xǁNoLlmAttributionǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            return False
        return bool(scan_text(text))

    def xǁNoLlmAttributionǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            return False
        return bool(scan_text(text))

    def xǁNoLlmAttributionǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        try:
            text = None
        except (UnicodeDecodeError, OSError):
            return False
        return bool(scan_text(text))

    def xǁNoLlmAttributionǁfile_has_violation__mutmut_2(self, path: Path) -> bool:
        try:
            text = path.read_text(encoding=None)
        except (UnicodeDecodeError, OSError):
            return False
        return bool(scan_text(text))

    def xǁNoLlmAttributionǁfile_has_violation__mutmut_3(self, path: Path) -> bool:
        try:
            text = path.read_text(encoding="XXutf-8XX")
        except (UnicodeDecodeError, OSError):
            return False
        return bool(scan_text(text))

    def xǁNoLlmAttributionǁfile_has_violation__mutmut_4(self, path: Path) -> bool:
        try:
            text = path.read_text(encoding="UTF-8")
        except (UnicodeDecodeError, OSError):
            return False
        return bool(scan_text(text))

    def xǁNoLlmAttributionǁfile_has_violation__mutmut_5(self, path: Path) -> bool:
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            return True
        return bool(scan_text(text))

    def xǁNoLlmAttributionǁfile_has_violation__mutmut_6(self, path: Path) -> bool:
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            return False
        return bool(None)

    def xǁNoLlmAttributionǁfile_has_violation__mutmut_7(self, path: Path) -> bool:
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            return False
        return bool(scan_text(None))

mutants_xǁNoLlmAttributionǁfile_has_violation__mutmut['_mutmut_orig'] = NoLlmAttribution.xǁNoLlmAttributionǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNoLlmAttributionǁfile_has_violation__mutmut['xǁNoLlmAttributionǁfile_has_violation__mutmut_1'] = NoLlmAttribution.xǁNoLlmAttributionǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNoLlmAttributionǁfile_has_violation__mutmut['xǁNoLlmAttributionǁfile_has_violation__mutmut_2'] = NoLlmAttribution.xǁNoLlmAttributionǁfile_has_violation__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNoLlmAttributionǁfile_has_violation__mutmut['xǁNoLlmAttributionǁfile_has_violation__mutmut_3'] = NoLlmAttribution.xǁNoLlmAttributionǁfile_has_violation__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNoLlmAttributionǁfile_has_violation__mutmut['xǁNoLlmAttributionǁfile_has_violation__mutmut_4'] = NoLlmAttribution.xǁNoLlmAttributionǁfile_has_violation__mutmut_4 # type: ignore # mutmut generated
mutants_xǁNoLlmAttributionǁfile_has_violation__mutmut['xǁNoLlmAttributionǁfile_has_violation__mutmut_5'] = NoLlmAttribution.xǁNoLlmAttributionǁfile_has_violation__mutmut_5 # type: ignore # mutmut generated
mutants_xǁNoLlmAttributionǁfile_has_violation__mutmut['xǁNoLlmAttributionǁfile_has_violation__mutmut_6'] = NoLlmAttribution.xǁNoLlmAttributionǁfile_has_violation__mutmut_6 # type: ignore # mutmut generated
mutants_xǁNoLlmAttributionǁfile_has_violation__mutmut['xǁNoLlmAttributionǁfile_has_violation__mutmut_7'] = NoLlmAttribution.xǁNoLlmAttributionǁfile_has_violation__mutmut_7 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoLlmAttribution:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    rule = NoLlmAttribution.from_config(config, repo_root=repo_root)
    assert isinstance(rule, NoLlmAttribution)  # noqa: S101  # narrowing for mypy
    return rule


def x_build__mutmut_orig(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoLlmAttribution:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    rule = NoLlmAttribution.from_config(config, repo_root=repo_root)
    assert isinstance(rule, NoLlmAttribution)  # noqa: S101  # narrowing for mypy
    return rule


def x_build__mutmut_1(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoLlmAttribution:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    rule = None
    assert isinstance(rule, NoLlmAttribution)  # noqa: S101  # narrowing for mypy
    return rule


def x_build__mutmut_2(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoLlmAttribution:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    rule = NoLlmAttribution.from_config(None, repo_root=repo_root)
    assert isinstance(rule, NoLlmAttribution)  # noqa: S101  # narrowing for mypy
    return rule


def x_build__mutmut_3(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoLlmAttribution:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    rule = NoLlmAttribution.from_config(config, repo_root=None)
    assert isinstance(rule, NoLlmAttribution)  # noqa: S101  # narrowing for mypy
    return rule


def x_build__mutmut_4(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoLlmAttribution:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    rule = NoLlmAttribution.from_config(repo_root=repo_root)
    assert isinstance(rule, NoLlmAttribution)  # noqa: S101  # narrowing for mypy
    return rule


def x_build__mutmut_5(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoLlmAttribution:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    rule = NoLlmAttribution.from_config(config, )
    assert isinstance(rule, NoLlmAttribution)  # noqa: S101  # narrowing for mypy
    return rule

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_5'] = x_build__mutmut_5 # type: ignore # mutmut generated
mutants_x__report__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__report__mutmut)
def _report(path: Path, hits: list[Hit]) -> None:
    print(f"no_llm_attribution: {len(hits)} attribution signature(s) in {path}:")
    for h in hits:
        print(f"  [{h.signature}] {h.match!r}")
    print(REMEDIATION)


def x__report__mutmut_orig(path: Path, hits: list[Hit]) -> None:
    print(f"no_llm_attribution: {len(hits)} attribution signature(s) in {path}:")
    for h in hits:
        print(f"  [{h.signature}] {h.match!r}")
    print(REMEDIATION)


def x__report__mutmut_1(path: Path, hits: list[Hit]) -> None:
    print(None)
    for h in hits:
        print(f"  [{h.signature}] {h.match!r}")
    print(REMEDIATION)


def x__report__mutmut_2(path: Path, hits: list[Hit]) -> None:
    print(f"no_llm_attribution: {len(hits)} attribution signature(s) in {path}:")
    for h in hits:
        print(None)
    print(REMEDIATION)


def x__report__mutmut_3(path: Path, hits: list[Hit]) -> None:
    print(f"no_llm_attribution: {len(hits)} attribution signature(s) in {path}:")
    for h in hits:
        print(f"  [{h.signature}] {h.match!r}")
    print(None)

mutants_x__report__mutmut['_mutmut_orig'] = x__report__mutmut_orig # type: ignore # mutmut generated
mutants_x__report__mutmut['x__report__mutmut_1'] = x__report__mutmut_1 # type: ignore # mutmut generated
mutants_x__report__mutmut['x__report__mutmut_2'] = x__report__mutmut_2 # type: ignore # mutmut generated
mutants_x__report__mutmut['x__report__mutmut_3'] = x__report__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = None
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[2:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is not None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(None)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_5(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args or args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_6(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[1] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_7(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] not in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_8(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("XX--scan-fileXX", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_9(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--SCAN-FILE", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_10(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "XX--strip-fileXX"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_11(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--STRIP-FILE"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_12(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) <= 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_13(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 3:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_14(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(None, file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_15(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=None)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_16(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_17(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", )
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_18(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[1]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_19(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 3
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_20(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = None
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_21(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[1], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_22(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(None)
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_23(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[2])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_24(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = None
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_25(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding=None)
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_26(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="XXutf-8XX")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_27(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="UTF-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_28(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(None, file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_29(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=None)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_30(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_31(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", )
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_32(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 3
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_33(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode != "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_34(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "XX--strip-fileXX":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_35(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--STRIP-FILE":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_36(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = None
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_37(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(None)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_38(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(None, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_39(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding=None)
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_40(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_41(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, )
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_42(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="XXutf-8XX")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_43(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="UTF-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_44(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = None
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_45(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = None
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_46(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(None)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_47(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(None, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_48(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, None)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_49(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_50(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, )
            return 1
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_51(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 2
        return 0
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_52(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 1
    return run_core_check(NoLlmAttribution, args)


def x_main__mutmut_53(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(None, args)


def x_main__mutmut_54(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, None)


def x_main__mutmut_55(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(args)


def x_main__mutmut_56(argv: list[str] | None = None) -> int:
    """CLI entry.

    File/repo mode (the fitness gate): ``--repo-root``.

    Message mode (the single seam the commit-msg hook and CI leg share):

    * ``--scan-file PATH`` — scan a commit message / PR body; exit 1 on residue.
      Read-only (CI must never rewrite history).
    * ``--strip-file PATH`` — strip whole attribution lines IN PLACE, then reject
      (exit 1) only if non-strippable residue remains. The commit-msg hook mode.
    """
    args = sys.argv[1:] if argv is None else list(argv)
    if args and args[0] in ("--scan-file", "--strip-file"):
        if len(args) < 2:
            print(f"usage: {args[0]} PATH", file=sys.stderr)
            return 2
        mode, path = args[0], Path(args[1])
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        if mode == "--strip-file":
            cleaned, dropped = strip_text(text)
            if dropped:
                path.write_text(cleaned, encoding="utf-8")
            text = cleaned
        hits = scan_text(text)
        if hits:
            _report(path, hits)
            return 1
        return 0
    return run_core_check(NoLlmAttribution, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_5'] = x_main__mutmut_5 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_6'] = x_main__mutmut_6 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_7'] = x_main__mutmut_7 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_8'] = x_main__mutmut_8 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_9'] = x_main__mutmut_9 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_10'] = x_main__mutmut_10 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_11'] = x_main__mutmut_11 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_12'] = x_main__mutmut_12 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_13'] = x_main__mutmut_13 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_14'] = x_main__mutmut_14 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_15'] = x_main__mutmut_15 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_16'] = x_main__mutmut_16 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_17'] = x_main__mutmut_17 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_18'] = x_main__mutmut_18 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_19'] = x_main__mutmut_19 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_20'] = x_main__mutmut_20 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_21'] = x_main__mutmut_21 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_22'] = x_main__mutmut_22 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_23'] = x_main__mutmut_23 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_24'] = x_main__mutmut_24 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_25'] = x_main__mutmut_25 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_26'] = x_main__mutmut_26 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_27'] = x_main__mutmut_27 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_28'] = x_main__mutmut_28 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_29'] = x_main__mutmut_29 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_30'] = x_main__mutmut_30 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_31'] = x_main__mutmut_31 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_32'] = x_main__mutmut_32 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_33'] = x_main__mutmut_33 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_34'] = x_main__mutmut_34 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_35'] = x_main__mutmut_35 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_36'] = x_main__mutmut_36 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_37'] = x_main__mutmut_37 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_38'] = x_main__mutmut_38 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_39'] = x_main__mutmut_39 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_40'] = x_main__mutmut_40 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_41'] = x_main__mutmut_41 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_42'] = x_main__mutmut_42 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_43'] = x_main__mutmut_43 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_44'] = x_main__mutmut_44 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_45'] = x_main__mutmut_45 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_46'] = x_main__mutmut_46 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_47'] = x_main__mutmut_47 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_48'] = x_main__mutmut_48 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_49'] = x_main__mutmut_49 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_50'] = x_main__mutmut_50 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_51'] = x_main__mutmut_51 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_52'] = x_main__mutmut_52 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_53'] = x_main__mutmut_53 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_54'] = x_main__mutmut_54 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_55'] = x_main__mutmut_55 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_56'] = x_main__mutmut_56 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
