"""CORE check: no-noop-test-scripts — no placeholder ``test`` script reports green.

A package with production code must not report green by running a placeholder
``test`` script (``echo "no tests yet" && exit 0`` or equivalent). A fake
passing test script makes CI green without running any assertions -- the worst
kind of coverage theatre. This rule scans each in-scope ``package.json`` and
flags one whose ``scripts.test`` matches a placeholder pattern AND does not
invoke a real test runner.

Ported from tc-agent-zone ``scripts/checks/no_noop_test_scripts.py`` and
re-expressed as a configurable, repo-agnostic rule: the production-package
path prefixes and skipped directory segments arrive from config -- NO repo
path is baked in. The placeholder pattern and the real-runner pattern are the
rule's own shape (JS test-runner vocabulary), overridable per consumer.
"""

from __future__ import annotations

import json
import re
import shlex
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: A ``test`` script matching this AND no real runner is a no-op placeholder.
DEFAULT_PLACEHOLDER_PATTERN = r"(?:no tests? yet|todo|placeholder|not implemented|skip tests?|exit\s+0)"
#: When the script invokes one of these, it is a real test command -- not a no-op.
DEFAULT_REAL_RUNNER_PATTERN = r"\b(vitest|jest|node\s+--test|tsx|mocha|tap|ava|playwright)\b"
#: Directory segments never descended into when discovering ``package.json``.
DEFAULT_SKIP_PARTS: tuple[str, ...] = ("node_modules", ".pnpm", "dist", ".venv", ".git")
#: The manifest filename this rule inspects.
_MANIFEST_NAME = "package.json"

REMEDIATION = _remediation(
    fix=(
        "change the package's test script so it executes unit / contract / "
        "smoke coverage for the package, or remove/rename the production "
        "package until tests exist. Do not use a placeholder command that "
        "makes CI green without running assertions."
    ),
    nxt="re-run this check to confirm it goes green.",
    run="python -m tc_fitness.core_checks.no_noop_test_scripts",
    passing='"test": "vitest run src --coverage"',
    forbidden='"test": "echo \'no tests yet\' && exit 0"',
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x_script_is_noop__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_script_is_noop__mutmut)
def script_is_noop(script: str, *, placeholder: re.Pattern[str], real_runner: re.Pattern[str]) -> bool:
    """True iff ``script`` looks like a placeholder and runs no real test runner.

    Pure helper (the detection core) so tests assert on it directly.
    """
    text = " ".join(script.split())
    if not placeholder.search(text):
        return False
    try:
        lexer = shlex.shlex(script, posix=True, punctuation_chars=";&|")
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return True

    command: list[str] = []
    for token in [*tokens, ";"]:
        if token in {";", "&&", "||", "|"}:
            if _command_invokes_runner(command, real_runner):
                return False
            command = []
        else:
            command.append(token)
    return True


def x_script_is_noop__mutmut_orig(script: str, *, placeholder: re.Pattern[str], real_runner: re.Pattern[str]) -> bool:
    """True iff ``script`` looks like a placeholder and runs no real test runner.

    Pure helper (the detection core) so tests assert on it directly.
    """
    text = " ".join(script.split())
    if not placeholder.search(text):
        return False
    try:
        lexer = shlex.shlex(script, posix=True, punctuation_chars=";&|")
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return True

    command: list[str] = []
    for token in [*tokens, ";"]:
        if token in {";", "&&", "||", "|"}:
            if _command_invokes_runner(command, real_runner):
                return False
            command = []
        else:
            command.append(token)
    return True


def x_script_is_noop__mutmut_1(script: str, *, placeholder: re.Pattern[str], real_runner: re.Pattern[str]) -> bool:
    """True iff ``script`` looks like a placeholder and runs no real test runner.

    Pure helper (the detection core) so tests assert on it directly.
    """
    text = None
    if not placeholder.search(text):
        return False
    try:
        lexer = shlex.shlex(script, posix=True, punctuation_chars=";&|")
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return True

    command: list[str] = []
    for token in [*tokens, ";"]:
        if token in {";", "&&", "||", "|"}:
            if _command_invokes_runner(command, real_runner):
                return False
            command = []
        else:
            command.append(token)
    return True


def x_script_is_noop__mutmut_2(script: str, *, placeholder: re.Pattern[str], real_runner: re.Pattern[str]) -> bool:
    """True iff ``script`` looks like a placeholder and runs no real test runner.

    Pure helper (the detection core) so tests assert on it directly.
    """
    text = " ".join(None)
    if not placeholder.search(text):
        return False
    try:
        lexer = shlex.shlex(script, posix=True, punctuation_chars=";&|")
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return True

    command: list[str] = []
    for token in [*tokens, ";"]:
        if token in {";", "&&", "||", "|"}:
            if _command_invokes_runner(command, real_runner):
                return False
            command = []
        else:
            command.append(token)
    return True


def x_script_is_noop__mutmut_3(script: str, *, placeholder: re.Pattern[str], real_runner: re.Pattern[str]) -> bool:
    """True iff ``script`` looks like a placeholder and runs no real test runner.

    Pure helper (the detection core) so tests assert on it directly.
    """
    text = "XX XX".join(script.split())
    if not placeholder.search(text):
        return False
    try:
        lexer = shlex.shlex(script, posix=True, punctuation_chars=";&|")
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return True

    command: list[str] = []
    for token in [*tokens, ";"]:
        if token in {";", "&&", "||", "|"}:
            if _command_invokes_runner(command, real_runner):
                return False
            command = []
        else:
            command.append(token)
    return True


def x_script_is_noop__mutmut_4(script: str, *, placeholder: re.Pattern[str], real_runner: re.Pattern[str]) -> bool:
    """True iff ``script`` looks like a placeholder and runs no real test runner.

    Pure helper (the detection core) so tests assert on it directly.
    """
    text = " ".join(script.split())
    if placeholder.search(text):
        return False
    try:
        lexer = shlex.shlex(script, posix=True, punctuation_chars=";&|")
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return True

    command: list[str] = []
    for token in [*tokens, ";"]:
        if token in {";", "&&", "||", "|"}:
            if _command_invokes_runner(command, real_runner):
                return False
            command = []
        else:
            command.append(token)
    return True


def x_script_is_noop__mutmut_5(script: str, *, placeholder: re.Pattern[str], real_runner: re.Pattern[str]) -> bool:
    """True iff ``script`` looks like a placeholder and runs no real test runner.

    Pure helper (the detection core) so tests assert on it directly.
    """
    text = " ".join(script.split())
    if not placeholder.search(None):
        return False
    try:
        lexer = shlex.shlex(script, posix=True, punctuation_chars=";&|")
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return True

    command: list[str] = []
    for token in [*tokens, ";"]:
        if token in {";", "&&", "||", "|"}:
            if _command_invokes_runner(command, real_runner):
                return False
            command = []
        else:
            command.append(token)
    return True


def x_script_is_noop__mutmut_6(script: str, *, placeholder: re.Pattern[str], real_runner: re.Pattern[str]) -> bool:
    """True iff ``script`` looks like a placeholder and runs no real test runner.

    Pure helper (the detection core) so tests assert on it directly.
    """
    text = " ".join(script.split())
    if not placeholder.search(text):
        return True
    try:
        lexer = shlex.shlex(script, posix=True, punctuation_chars=";&|")
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return True

    command: list[str] = []
    for token in [*tokens, ";"]:
        if token in {";", "&&", "||", "|"}:
            if _command_invokes_runner(command, real_runner):
                return False
            command = []
        else:
            command.append(token)
    return True


def x_script_is_noop__mutmut_7(script: str, *, placeholder: re.Pattern[str], real_runner: re.Pattern[str]) -> bool:
    """True iff ``script`` looks like a placeholder and runs no real test runner.

    Pure helper (the detection core) so tests assert on it directly.
    """
    text = " ".join(script.split())
    if not placeholder.search(text):
        return False
    try:
        lexer = None
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return True

    command: list[str] = []
    for token in [*tokens, ";"]:
        if token in {";", "&&", "||", "|"}:
            if _command_invokes_runner(command, real_runner):
                return False
            command = []
        else:
            command.append(token)
    return True


def x_script_is_noop__mutmut_8(script: str, *, placeholder: re.Pattern[str], real_runner: re.Pattern[str]) -> bool:
    """True iff ``script`` looks like a placeholder and runs no real test runner.

    Pure helper (the detection core) so tests assert on it directly.
    """
    text = " ".join(script.split())
    if not placeholder.search(text):
        return False
    try:
        lexer = shlex.shlex(None, posix=True, punctuation_chars=";&|")
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return True

    command: list[str] = []
    for token in [*tokens, ";"]:
        if token in {";", "&&", "||", "|"}:
            if _command_invokes_runner(command, real_runner):
                return False
            command = []
        else:
            command.append(token)
    return True


def x_script_is_noop__mutmut_9(script: str, *, placeholder: re.Pattern[str], real_runner: re.Pattern[str]) -> bool:
    """True iff ``script`` looks like a placeholder and runs no real test runner.

    Pure helper (the detection core) so tests assert on it directly.
    """
    text = " ".join(script.split())
    if not placeholder.search(text):
        return False
    try:
        lexer = shlex.shlex(script, posix=None, punctuation_chars=";&|")
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return True

    command: list[str] = []
    for token in [*tokens, ";"]:
        if token in {";", "&&", "||", "|"}:
            if _command_invokes_runner(command, real_runner):
                return False
            command = []
        else:
            command.append(token)
    return True


def x_script_is_noop__mutmut_10(script: str, *, placeholder: re.Pattern[str], real_runner: re.Pattern[str]) -> bool:
    """True iff ``script`` looks like a placeholder and runs no real test runner.

    Pure helper (the detection core) so tests assert on it directly.
    """
    text = " ".join(script.split())
    if not placeholder.search(text):
        return False
    try:
        lexer = shlex.shlex(script, posix=True, punctuation_chars=None)
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return True

    command: list[str] = []
    for token in [*tokens, ";"]:
        if token in {";", "&&", "||", "|"}:
            if _command_invokes_runner(command, real_runner):
                return False
            command = []
        else:
            command.append(token)
    return True


def x_script_is_noop__mutmut_11(script: str, *, placeholder: re.Pattern[str], real_runner: re.Pattern[str]) -> bool:
    """True iff ``script`` looks like a placeholder and runs no real test runner.

    Pure helper (the detection core) so tests assert on it directly.
    """
    text = " ".join(script.split())
    if not placeholder.search(text):
        return False
    try:
        lexer = shlex.shlex(posix=True, punctuation_chars=";&|")
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return True

    command: list[str] = []
    for token in [*tokens, ";"]:
        if token in {";", "&&", "||", "|"}:
            if _command_invokes_runner(command, real_runner):
                return False
            command = []
        else:
            command.append(token)
    return True


def x_script_is_noop__mutmut_12(script: str, *, placeholder: re.Pattern[str], real_runner: re.Pattern[str]) -> bool:
    """True iff ``script`` looks like a placeholder and runs no real test runner.

    Pure helper (the detection core) so tests assert on it directly.
    """
    text = " ".join(script.split())
    if not placeholder.search(text):
        return False
    try:
        lexer = shlex.shlex(script, punctuation_chars=";&|")
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return True

    command: list[str] = []
    for token in [*tokens, ";"]:
        if token in {";", "&&", "||", "|"}:
            if _command_invokes_runner(command, real_runner):
                return False
            command = []
        else:
            command.append(token)
    return True


def x_script_is_noop__mutmut_13(script: str, *, placeholder: re.Pattern[str], real_runner: re.Pattern[str]) -> bool:
    """True iff ``script`` looks like a placeholder and runs no real test runner.

    Pure helper (the detection core) so tests assert on it directly.
    """
    text = " ".join(script.split())
    if not placeholder.search(text):
        return False
    try:
        lexer = shlex.shlex(script, posix=True, )
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return True

    command: list[str] = []
    for token in [*tokens, ";"]:
        if token in {";", "&&", "||", "|"}:
            if _command_invokes_runner(command, real_runner):
                return False
            command = []
        else:
            command.append(token)
    return True


def x_script_is_noop__mutmut_14(script: str, *, placeholder: re.Pattern[str], real_runner: re.Pattern[str]) -> bool:
    """True iff ``script`` looks like a placeholder and runs no real test runner.

    Pure helper (the detection core) so tests assert on it directly.
    """
    text = " ".join(script.split())
    if not placeholder.search(text):
        return False
    try:
        lexer = shlex.shlex(script, posix=False, punctuation_chars=";&|")
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return True

    command: list[str] = []
    for token in [*tokens, ";"]:
        if token in {";", "&&", "||", "|"}:
            if _command_invokes_runner(command, real_runner):
                return False
            command = []
        else:
            command.append(token)
    return True


def x_script_is_noop__mutmut_15(script: str, *, placeholder: re.Pattern[str], real_runner: re.Pattern[str]) -> bool:
    """True iff ``script`` looks like a placeholder and runs no real test runner.

    Pure helper (the detection core) so tests assert on it directly.
    """
    text = " ".join(script.split())
    if not placeholder.search(text):
        return False
    try:
        lexer = shlex.shlex(script, posix=True, punctuation_chars="XX;&|XX")
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return True

    command: list[str] = []
    for token in [*tokens, ";"]:
        if token in {";", "&&", "||", "|"}:
            if _command_invokes_runner(command, real_runner):
                return False
            command = []
        else:
            command.append(token)
    return True


def x_script_is_noop__mutmut_16(script: str, *, placeholder: re.Pattern[str], real_runner: re.Pattern[str]) -> bool:
    """True iff ``script`` looks like a placeholder and runs no real test runner.

    Pure helper (the detection core) so tests assert on it directly.
    """
    text = " ".join(script.split())
    if not placeholder.search(text):
        return False
    try:
        lexer = shlex.shlex(script, posix=True, punctuation_chars=";&|")
        lexer.whitespace_split = None
        tokens = list(lexer)
    except ValueError:
        return True

    command: list[str] = []
    for token in [*tokens, ";"]:
        if token in {";", "&&", "||", "|"}:
            if _command_invokes_runner(command, real_runner):
                return False
            command = []
        else:
            command.append(token)
    return True


def x_script_is_noop__mutmut_17(script: str, *, placeholder: re.Pattern[str], real_runner: re.Pattern[str]) -> bool:
    """True iff ``script`` looks like a placeholder and runs no real test runner.

    Pure helper (the detection core) so tests assert on it directly.
    """
    text = " ".join(script.split())
    if not placeholder.search(text):
        return False
    try:
        lexer = shlex.shlex(script, posix=True, punctuation_chars=";&|")
        lexer.whitespace_split = False
        tokens = list(lexer)
    except ValueError:
        return True

    command: list[str] = []
    for token in [*tokens, ";"]:
        if token in {";", "&&", "||", "|"}:
            if _command_invokes_runner(command, real_runner):
                return False
            command = []
        else:
            command.append(token)
    return True


def x_script_is_noop__mutmut_18(script: str, *, placeholder: re.Pattern[str], real_runner: re.Pattern[str]) -> bool:
    """True iff ``script`` looks like a placeholder and runs no real test runner.

    Pure helper (the detection core) so tests assert on it directly.
    """
    text = " ".join(script.split())
    if not placeholder.search(text):
        return False
    try:
        lexer = shlex.shlex(script, posix=True, punctuation_chars=";&|")
        lexer.whitespace_split = True
        tokens = None
    except ValueError:
        return True

    command: list[str] = []
    for token in [*tokens, ";"]:
        if token in {";", "&&", "||", "|"}:
            if _command_invokes_runner(command, real_runner):
                return False
            command = []
        else:
            command.append(token)
    return True


def x_script_is_noop__mutmut_19(script: str, *, placeholder: re.Pattern[str], real_runner: re.Pattern[str]) -> bool:
    """True iff ``script`` looks like a placeholder and runs no real test runner.

    Pure helper (the detection core) so tests assert on it directly.
    """
    text = " ".join(script.split())
    if not placeholder.search(text):
        return False
    try:
        lexer = shlex.shlex(script, posix=True, punctuation_chars=";&|")
        lexer.whitespace_split = True
        tokens = list(None)
    except ValueError:
        return True

    command: list[str] = []
    for token in [*tokens, ";"]:
        if token in {";", "&&", "||", "|"}:
            if _command_invokes_runner(command, real_runner):
                return False
            command = []
        else:
            command.append(token)
    return True


def x_script_is_noop__mutmut_20(script: str, *, placeholder: re.Pattern[str], real_runner: re.Pattern[str]) -> bool:
    """True iff ``script`` looks like a placeholder and runs no real test runner.

    Pure helper (the detection core) so tests assert on it directly.
    """
    text = " ".join(script.split())
    if not placeholder.search(text):
        return False
    try:
        lexer = shlex.shlex(script, posix=True, punctuation_chars=";&|")
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return False

    command: list[str] = []
    for token in [*tokens, ";"]:
        if token in {";", "&&", "||", "|"}:
            if _command_invokes_runner(command, real_runner):
                return False
            command = []
        else:
            command.append(token)
    return True


def x_script_is_noop__mutmut_21(script: str, *, placeholder: re.Pattern[str], real_runner: re.Pattern[str]) -> bool:
    """True iff ``script`` looks like a placeholder and runs no real test runner.

    Pure helper (the detection core) so tests assert on it directly.
    """
    text = " ".join(script.split())
    if not placeholder.search(text):
        return False
    try:
        lexer = shlex.shlex(script, posix=True, punctuation_chars=";&|")
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return True

    command: list[str] = None
    for token in [*tokens, ";"]:
        if token in {";", "&&", "||", "|"}:
            if _command_invokes_runner(command, real_runner):
                return False
            command = []
        else:
            command.append(token)
    return True


def x_script_is_noop__mutmut_22(script: str, *, placeholder: re.Pattern[str], real_runner: re.Pattern[str]) -> bool:
    """True iff ``script`` looks like a placeholder and runs no real test runner.

    Pure helper (the detection core) so tests assert on it directly.
    """
    text = " ".join(script.split())
    if not placeholder.search(text):
        return False
    try:
        lexer = shlex.shlex(script, posix=True, punctuation_chars=";&|")
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return True

    command: list[str] = []
    for token in [*tokens, "XX;XX"]:
        if token in {";", "&&", "||", "|"}:
            if _command_invokes_runner(command, real_runner):
                return False
            command = []
        else:
            command.append(token)
    return True


def x_script_is_noop__mutmut_23(script: str, *, placeholder: re.Pattern[str], real_runner: re.Pattern[str]) -> bool:
    """True iff ``script`` looks like a placeholder and runs no real test runner.

    Pure helper (the detection core) so tests assert on it directly.
    """
    text = " ".join(script.split())
    if not placeholder.search(text):
        return False
    try:
        lexer = shlex.shlex(script, posix=True, punctuation_chars=";&|")
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return True

    command: list[str] = []
    for token in [*tokens, ";"]:
        if token not in {";", "&&", "||", "|"}:
            if _command_invokes_runner(command, real_runner):
                return False
            command = []
        else:
            command.append(token)
    return True


def x_script_is_noop__mutmut_24(script: str, *, placeholder: re.Pattern[str], real_runner: re.Pattern[str]) -> bool:
    """True iff ``script`` looks like a placeholder and runs no real test runner.

    Pure helper (the detection core) so tests assert on it directly.
    """
    text = " ".join(script.split())
    if not placeholder.search(text):
        return False
    try:
        lexer = shlex.shlex(script, posix=True, punctuation_chars=";&|")
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return True

    command: list[str] = []
    for token in [*tokens, ";"]:
        if token in {"XX;XX", "&&", "||", "|"}:
            if _command_invokes_runner(command, real_runner):
                return False
            command = []
        else:
            command.append(token)
    return True


def x_script_is_noop__mutmut_25(script: str, *, placeholder: re.Pattern[str], real_runner: re.Pattern[str]) -> bool:
    """True iff ``script`` looks like a placeholder and runs no real test runner.

    Pure helper (the detection core) so tests assert on it directly.
    """
    text = " ".join(script.split())
    if not placeholder.search(text):
        return False
    try:
        lexer = shlex.shlex(script, posix=True, punctuation_chars=";&|")
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return True

    command: list[str] = []
    for token in [*tokens, ";"]:
        if token in {";", "XX&&XX", "||", "|"}:
            if _command_invokes_runner(command, real_runner):
                return False
            command = []
        else:
            command.append(token)
    return True


def x_script_is_noop__mutmut_26(script: str, *, placeholder: re.Pattern[str], real_runner: re.Pattern[str]) -> bool:
    """True iff ``script`` looks like a placeholder and runs no real test runner.

    Pure helper (the detection core) so tests assert on it directly.
    """
    text = " ".join(script.split())
    if not placeholder.search(text):
        return False
    try:
        lexer = shlex.shlex(script, posix=True, punctuation_chars=";&|")
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return True

    command: list[str] = []
    for token in [*tokens, ";"]:
        if token in {";", "&&", "XX||XX", "|"}:
            if _command_invokes_runner(command, real_runner):
                return False
            command = []
        else:
            command.append(token)
    return True


def x_script_is_noop__mutmut_27(script: str, *, placeholder: re.Pattern[str], real_runner: re.Pattern[str]) -> bool:
    """True iff ``script`` looks like a placeholder and runs no real test runner.

    Pure helper (the detection core) so tests assert on it directly.
    """
    text = " ".join(script.split())
    if not placeholder.search(text):
        return False
    try:
        lexer = shlex.shlex(script, posix=True, punctuation_chars=";&|")
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return True

    command: list[str] = []
    for token in [*tokens, ";"]:
        if token in {";", "&&", "||", "XX|XX"}:
            if _command_invokes_runner(command, real_runner):
                return False
            command = []
        else:
            command.append(token)
    return True


def x_script_is_noop__mutmut_28(script: str, *, placeholder: re.Pattern[str], real_runner: re.Pattern[str]) -> bool:
    """True iff ``script`` looks like a placeholder and runs no real test runner.

    Pure helper (the detection core) so tests assert on it directly.
    """
    text = " ".join(script.split())
    if not placeholder.search(text):
        return False
    try:
        lexer = shlex.shlex(script, posix=True, punctuation_chars=";&|")
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return True

    command: list[str] = []
    for token in [*tokens, ";"]:
        if token in {";", "&&", "||", "|"}:
            if _command_invokes_runner(None, real_runner):
                return False
            command = []
        else:
            command.append(token)
    return True


def x_script_is_noop__mutmut_29(script: str, *, placeholder: re.Pattern[str], real_runner: re.Pattern[str]) -> bool:
    """True iff ``script`` looks like a placeholder and runs no real test runner.

    Pure helper (the detection core) so tests assert on it directly.
    """
    text = " ".join(script.split())
    if not placeholder.search(text):
        return False
    try:
        lexer = shlex.shlex(script, posix=True, punctuation_chars=";&|")
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return True

    command: list[str] = []
    for token in [*tokens, ";"]:
        if token in {";", "&&", "||", "|"}:
            if _command_invokes_runner(command, None):
                return False
            command = []
        else:
            command.append(token)
    return True


def x_script_is_noop__mutmut_30(script: str, *, placeholder: re.Pattern[str], real_runner: re.Pattern[str]) -> bool:
    """True iff ``script`` looks like a placeholder and runs no real test runner.

    Pure helper (the detection core) so tests assert on it directly.
    """
    text = " ".join(script.split())
    if not placeholder.search(text):
        return False
    try:
        lexer = shlex.shlex(script, posix=True, punctuation_chars=";&|")
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return True

    command: list[str] = []
    for token in [*tokens, ";"]:
        if token in {";", "&&", "||", "|"}:
            if _command_invokes_runner(real_runner):
                return False
            command = []
        else:
            command.append(token)
    return True


def x_script_is_noop__mutmut_31(script: str, *, placeholder: re.Pattern[str], real_runner: re.Pattern[str]) -> bool:
    """True iff ``script`` looks like a placeholder and runs no real test runner.

    Pure helper (the detection core) so tests assert on it directly.
    """
    text = " ".join(script.split())
    if not placeholder.search(text):
        return False
    try:
        lexer = shlex.shlex(script, posix=True, punctuation_chars=";&|")
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return True

    command: list[str] = []
    for token in [*tokens, ";"]:
        if token in {";", "&&", "||", "|"}:
            if _command_invokes_runner(command, ):
                return False
            command = []
        else:
            command.append(token)
    return True


def x_script_is_noop__mutmut_32(script: str, *, placeholder: re.Pattern[str], real_runner: re.Pattern[str]) -> bool:
    """True iff ``script`` looks like a placeholder and runs no real test runner.

    Pure helper (the detection core) so tests assert on it directly.
    """
    text = " ".join(script.split())
    if not placeholder.search(text):
        return False
    try:
        lexer = shlex.shlex(script, posix=True, punctuation_chars=";&|")
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return True

    command: list[str] = []
    for token in [*tokens, ";"]:
        if token in {";", "&&", "||", "|"}:
            if _command_invokes_runner(command, real_runner):
                return True
            command = []
        else:
            command.append(token)
    return True


def x_script_is_noop__mutmut_33(script: str, *, placeholder: re.Pattern[str], real_runner: re.Pattern[str]) -> bool:
    """True iff ``script`` looks like a placeholder and runs no real test runner.

    Pure helper (the detection core) so tests assert on it directly.
    """
    text = " ".join(script.split())
    if not placeholder.search(text):
        return False
    try:
        lexer = shlex.shlex(script, posix=True, punctuation_chars=";&|")
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return True

    command: list[str] = []
    for token in [*tokens, ";"]:
        if token in {";", "&&", "||", "|"}:
            if _command_invokes_runner(command, real_runner):
                return False
            command = None
        else:
            command.append(token)
    return True


def x_script_is_noop__mutmut_34(script: str, *, placeholder: re.Pattern[str], real_runner: re.Pattern[str]) -> bool:
    """True iff ``script`` looks like a placeholder and runs no real test runner.

    Pure helper (the detection core) so tests assert on it directly.
    """
    text = " ".join(script.split())
    if not placeholder.search(text):
        return False
    try:
        lexer = shlex.shlex(script, posix=True, punctuation_chars=";&|")
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return True

    command: list[str] = []
    for token in [*tokens, ";"]:
        if token in {";", "&&", "||", "|"}:
            if _command_invokes_runner(command, real_runner):
                return False
            command = []
        else:
            command.append(None)
    return True


def x_script_is_noop__mutmut_35(script: str, *, placeholder: re.Pattern[str], real_runner: re.Pattern[str]) -> bool:
    """True iff ``script`` looks like a placeholder and runs no real test runner.

    Pure helper (the detection core) so tests assert on it directly.
    """
    text = " ".join(script.split())
    if not placeholder.search(text):
        return False
    try:
        lexer = shlex.shlex(script, posix=True, punctuation_chars=";&|")
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return True

    command: list[str] = []
    for token in [*tokens, ";"]:
        if token in {";", "&&", "||", "|"}:
            if _command_invokes_runner(command, real_runner):
                return False
            command = []
        else:
            command.append(token)
    return False

mutants_x_script_is_noop__mutmut['_mutmut_orig'] = x_script_is_noop__mutmut_orig # type: ignore # mutmut generated
mutants_x_script_is_noop__mutmut['x_script_is_noop__mutmut_1'] = x_script_is_noop__mutmut_1 # type: ignore # mutmut generated
mutants_x_script_is_noop__mutmut['x_script_is_noop__mutmut_2'] = x_script_is_noop__mutmut_2 # type: ignore # mutmut generated
mutants_x_script_is_noop__mutmut['x_script_is_noop__mutmut_3'] = x_script_is_noop__mutmut_3 # type: ignore # mutmut generated
mutants_x_script_is_noop__mutmut['x_script_is_noop__mutmut_4'] = x_script_is_noop__mutmut_4 # type: ignore # mutmut generated
mutants_x_script_is_noop__mutmut['x_script_is_noop__mutmut_5'] = x_script_is_noop__mutmut_5 # type: ignore # mutmut generated
mutants_x_script_is_noop__mutmut['x_script_is_noop__mutmut_6'] = x_script_is_noop__mutmut_6 # type: ignore # mutmut generated
mutants_x_script_is_noop__mutmut['x_script_is_noop__mutmut_7'] = x_script_is_noop__mutmut_7 # type: ignore # mutmut generated
mutants_x_script_is_noop__mutmut['x_script_is_noop__mutmut_8'] = x_script_is_noop__mutmut_8 # type: ignore # mutmut generated
mutants_x_script_is_noop__mutmut['x_script_is_noop__mutmut_9'] = x_script_is_noop__mutmut_9 # type: ignore # mutmut generated
mutants_x_script_is_noop__mutmut['x_script_is_noop__mutmut_10'] = x_script_is_noop__mutmut_10 # type: ignore # mutmut generated
mutants_x_script_is_noop__mutmut['x_script_is_noop__mutmut_11'] = x_script_is_noop__mutmut_11 # type: ignore # mutmut generated
mutants_x_script_is_noop__mutmut['x_script_is_noop__mutmut_12'] = x_script_is_noop__mutmut_12 # type: ignore # mutmut generated
mutants_x_script_is_noop__mutmut['x_script_is_noop__mutmut_13'] = x_script_is_noop__mutmut_13 # type: ignore # mutmut generated
mutants_x_script_is_noop__mutmut['x_script_is_noop__mutmut_14'] = x_script_is_noop__mutmut_14 # type: ignore # mutmut generated
mutants_x_script_is_noop__mutmut['x_script_is_noop__mutmut_15'] = x_script_is_noop__mutmut_15 # type: ignore # mutmut generated
mutants_x_script_is_noop__mutmut['x_script_is_noop__mutmut_16'] = x_script_is_noop__mutmut_16 # type: ignore # mutmut generated
mutants_x_script_is_noop__mutmut['x_script_is_noop__mutmut_17'] = x_script_is_noop__mutmut_17 # type: ignore # mutmut generated
mutants_x_script_is_noop__mutmut['x_script_is_noop__mutmut_18'] = x_script_is_noop__mutmut_18 # type: ignore # mutmut generated
mutants_x_script_is_noop__mutmut['x_script_is_noop__mutmut_19'] = x_script_is_noop__mutmut_19 # type: ignore # mutmut generated
mutants_x_script_is_noop__mutmut['x_script_is_noop__mutmut_20'] = x_script_is_noop__mutmut_20 # type: ignore # mutmut generated
mutants_x_script_is_noop__mutmut['x_script_is_noop__mutmut_21'] = x_script_is_noop__mutmut_21 # type: ignore # mutmut generated
mutants_x_script_is_noop__mutmut['x_script_is_noop__mutmut_22'] = x_script_is_noop__mutmut_22 # type: ignore # mutmut generated
mutants_x_script_is_noop__mutmut['x_script_is_noop__mutmut_23'] = x_script_is_noop__mutmut_23 # type: ignore # mutmut generated
mutants_x_script_is_noop__mutmut['x_script_is_noop__mutmut_24'] = x_script_is_noop__mutmut_24 # type: ignore # mutmut generated
mutants_x_script_is_noop__mutmut['x_script_is_noop__mutmut_25'] = x_script_is_noop__mutmut_25 # type: ignore # mutmut generated
mutants_x_script_is_noop__mutmut['x_script_is_noop__mutmut_26'] = x_script_is_noop__mutmut_26 # type: ignore # mutmut generated
mutants_x_script_is_noop__mutmut['x_script_is_noop__mutmut_27'] = x_script_is_noop__mutmut_27 # type: ignore # mutmut generated
mutants_x_script_is_noop__mutmut['x_script_is_noop__mutmut_28'] = x_script_is_noop__mutmut_28 # type: ignore # mutmut generated
mutants_x_script_is_noop__mutmut['x_script_is_noop__mutmut_29'] = x_script_is_noop__mutmut_29 # type: ignore # mutmut generated
mutants_x_script_is_noop__mutmut['x_script_is_noop__mutmut_30'] = x_script_is_noop__mutmut_30 # type: ignore # mutmut generated
mutants_x_script_is_noop__mutmut['x_script_is_noop__mutmut_31'] = x_script_is_noop__mutmut_31 # type: ignore # mutmut generated
mutants_x_script_is_noop__mutmut['x_script_is_noop__mutmut_32'] = x_script_is_noop__mutmut_32 # type: ignore # mutmut generated
mutants_x_script_is_noop__mutmut['x_script_is_noop__mutmut_33'] = x_script_is_noop__mutmut_33 # type: ignore # mutmut generated
mutants_x_script_is_noop__mutmut['x_script_is_noop__mutmut_34'] = x_script_is_noop__mutmut_34 # type: ignore # mutmut generated
mutants_x_script_is_noop__mutmut['x_script_is_noop__mutmut_35'] = x_script_is_noop__mutmut_35 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__command_invokes_runner__mutmut)
def _command_invokes_runner(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_orig(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_1(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_2(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return True
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_3(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = None
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_4(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 1
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_5(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position <= len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_6(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = None
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_7(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token or token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_8(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "XX=XX" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_9(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" not in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_10(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace(None, "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_11(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", None).isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_12(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_13(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", ).isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_14(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split(None, 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_15(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", None)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_16(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split(1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_17(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", )[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_18(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.rsplit("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_19(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("XX=XX", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_20(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 2)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_21(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[1].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_22(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("XX_XX", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_23(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "XXaXX").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_24(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "A").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_25(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position = 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_26(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position -= 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_27(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 2
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_28(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            break
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_29(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token not in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_30(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"XXenvXX", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_31(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"ENV", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_32(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "XXcross-envXX"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_33(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "CROSS-ENV"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_34(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position = 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_35(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position -= 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_36(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 2
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_37(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = None
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_38(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(None, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_39(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, None)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_40(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_41(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, )
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_42(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            break
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_43(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token not in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_44(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"XXnpxXX", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_45(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"NPX", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_46(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "XXyarnXX", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_47(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "YARN", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_48(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "XXbunxXX"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_49(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "BUNX"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_50(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = None
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_51(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(None, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_52(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, None)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_53(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_54(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, )
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_55(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position - 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_56(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 2)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_57(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            break
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_58(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token not in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_59(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"XXpnpmXX", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_60(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"PNPM", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_61(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "XXnpmXX", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_62(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "NPM", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_63(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "XXbunXX"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_64(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "BUN"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_65(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = None
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_66(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(None, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_67(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, None)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_68(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_69(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, )
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_70(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position - 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_71(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 2)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_72(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) or command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_73(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position <= len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_74(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] not in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_75(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"XXexecXX", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_76(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"EXEC", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_77(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "XXrunXX", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_78(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "RUN", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_79(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "XXxXX"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_80(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "X"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_81(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = None
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_82(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(None, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_83(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, None)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_84(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_85(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, )
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_86(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position - 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_87(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 2)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_88(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                break
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_89(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        return
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_90(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position != len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_91(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return True
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_92(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = None
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_93(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(None) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_94(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_95(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return False
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_96(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command) or real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_97(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node" or position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_98(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable != "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_99(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "XXnodeXX"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_100(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "NODE"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_101(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position - 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_102(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 2 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_103(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 <= len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is not None
    )


def x__command_invokes_runner__mutmut_104(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(None) is not None
    )


def x__command_invokes_runner__mutmut_105(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position - 1]}") is not None
    )


def x__command_invokes_runner__mutmut_106(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 2]}") is not None
    )


def x__command_invokes_runner__mutmut_107(command: list[str], real_runner: re.Pattern[str]) -> bool:
    """Match a runner only where it is an executable, not an argument to echo."""
    if not command:
        return False
    position = 0
    while position < len(command):
        token = command[position]
        if "=" in token and token.split("=", 1)[0].replace("_", "a").isalnum():
            position += 1
            continue
        if token in {"env", "cross-env"}:
            position += 1
            position = _skip_options(command, position)
            continue
        if token in {"npx", "yarn", "bunx"}:
            position = _skip_options(command, position + 1)
            continue
        if token in {"pnpm", "npm", "bun"}:
            action_position = _skip_options(command, position + 1)
            if action_position < len(command) and command[action_position] in {"exec", "run", "x"}:
                position = _skip_options(command, action_position + 1)
                continue
        break
    if position == len(command):
        return False
    executable = command[position]
    if real_runner.search(executable) is not None:
        return True
    return (
        executable == "node"
        and position + 1 < len(command)
        and real_runner.search(f"{executable} {command[position + 1]}") is None
    )

mutants_x__command_invokes_runner__mutmut['_mutmut_orig'] = x__command_invokes_runner__mutmut_orig # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_1'] = x__command_invokes_runner__mutmut_1 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_2'] = x__command_invokes_runner__mutmut_2 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_3'] = x__command_invokes_runner__mutmut_3 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_4'] = x__command_invokes_runner__mutmut_4 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_5'] = x__command_invokes_runner__mutmut_5 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_6'] = x__command_invokes_runner__mutmut_6 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_7'] = x__command_invokes_runner__mutmut_7 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_8'] = x__command_invokes_runner__mutmut_8 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_9'] = x__command_invokes_runner__mutmut_9 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_10'] = x__command_invokes_runner__mutmut_10 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_11'] = x__command_invokes_runner__mutmut_11 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_12'] = x__command_invokes_runner__mutmut_12 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_13'] = x__command_invokes_runner__mutmut_13 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_14'] = x__command_invokes_runner__mutmut_14 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_15'] = x__command_invokes_runner__mutmut_15 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_16'] = x__command_invokes_runner__mutmut_16 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_17'] = x__command_invokes_runner__mutmut_17 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_18'] = x__command_invokes_runner__mutmut_18 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_19'] = x__command_invokes_runner__mutmut_19 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_20'] = x__command_invokes_runner__mutmut_20 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_21'] = x__command_invokes_runner__mutmut_21 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_22'] = x__command_invokes_runner__mutmut_22 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_23'] = x__command_invokes_runner__mutmut_23 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_24'] = x__command_invokes_runner__mutmut_24 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_25'] = x__command_invokes_runner__mutmut_25 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_26'] = x__command_invokes_runner__mutmut_26 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_27'] = x__command_invokes_runner__mutmut_27 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_28'] = x__command_invokes_runner__mutmut_28 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_29'] = x__command_invokes_runner__mutmut_29 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_30'] = x__command_invokes_runner__mutmut_30 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_31'] = x__command_invokes_runner__mutmut_31 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_32'] = x__command_invokes_runner__mutmut_32 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_33'] = x__command_invokes_runner__mutmut_33 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_34'] = x__command_invokes_runner__mutmut_34 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_35'] = x__command_invokes_runner__mutmut_35 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_36'] = x__command_invokes_runner__mutmut_36 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_37'] = x__command_invokes_runner__mutmut_37 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_38'] = x__command_invokes_runner__mutmut_38 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_39'] = x__command_invokes_runner__mutmut_39 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_40'] = x__command_invokes_runner__mutmut_40 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_41'] = x__command_invokes_runner__mutmut_41 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_42'] = x__command_invokes_runner__mutmut_42 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_43'] = x__command_invokes_runner__mutmut_43 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_44'] = x__command_invokes_runner__mutmut_44 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_45'] = x__command_invokes_runner__mutmut_45 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_46'] = x__command_invokes_runner__mutmut_46 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_47'] = x__command_invokes_runner__mutmut_47 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_48'] = x__command_invokes_runner__mutmut_48 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_49'] = x__command_invokes_runner__mutmut_49 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_50'] = x__command_invokes_runner__mutmut_50 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_51'] = x__command_invokes_runner__mutmut_51 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_52'] = x__command_invokes_runner__mutmut_52 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_53'] = x__command_invokes_runner__mutmut_53 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_54'] = x__command_invokes_runner__mutmut_54 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_55'] = x__command_invokes_runner__mutmut_55 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_56'] = x__command_invokes_runner__mutmut_56 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_57'] = x__command_invokes_runner__mutmut_57 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_58'] = x__command_invokes_runner__mutmut_58 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_59'] = x__command_invokes_runner__mutmut_59 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_60'] = x__command_invokes_runner__mutmut_60 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_61'] = x__command_invokes_runner__mutmut_61 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_62'] = x__command_invokes_runner__mutmut_62 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_63'] = x__command_invokes_runner__mutmut_63 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_64'] = x__command_invokes_runner__mutmut_64 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_65'] = x__command_invokes_runner__mutmut_65 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_66'] = x__command_invokes_runner__mutmut_66 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_67'] = x__command_invokes_runner__mutmut_67 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_68'] = x__command_invokes_runner__mutmut_68 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_69'] = x__command_invokes_runner__mutmut_69 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_70'] = x__command_invokes_runner__mutmut_70 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_71'] = x__command_invokes_runner__mutmut_71 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_72'] = x__command_invokes_runner__mutmut_72 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_73'] = x__command_invokes_runner__mutmut_73 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_74'] = x__command_invokes_runner__mutmut_74 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_75'] = x__command_invokes_runner__mutmut_75 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_76'] = x__command_invokes_runner__mutmut_76 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_77'] = x__command_invokes_runner__mutmut_77 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_78'] = x__command_invokes_runner__mutmut_78 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_79'] = x__command_invokes_runner__mutmut_79 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_80'] = x__command_invokes_runner__mutmut_80 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_81'] = x__command_invokes_runner__mutmut_81 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_82'] = x__command_invokes_runner__mutmut_82 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_83'] = x__command_invokes_runner__mutmut_83 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_84'] = x__command_invokes_runner__mutmut_84 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_85'] = x__command_invokes_runner__mutmut_85 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_86'] = x__command_invokes_runner__mutmut_86 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_87'] = x__command_invokes_runner__mutmut_87 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_88'] = x__command_invokes_runner__mutmut_88 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_89'] = x__command_invokes_runner__mutmut_89 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_90'] = x__command_invokes_runner__mutmut_90 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_91'] = x__command_invokes_runner__mutmut_91 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_92'] = x__command_invokes_runner__mutmut_92 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_93'] = x__command_invokes_runner__mutmut_93 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_94'] = x__command_invokes_runner__mutmut_94 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_95'] = x__command_invokes_runner__mutmut_95 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_96'] = x__command_invokes_runner__mutmut_96 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_97'] = x__command_invokes_runner__mutmut_97 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_98'] = x__command_invokes_runner__mutmut_98 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_99'] = x__command_invokes_runner__mutmut_99 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_100'] = x__command_invokes_runner__mutmut_100 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_101'] = x__command_invokes_runner__mutmut_101 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_102'] = x__command_invokes_runner__mutmut_102 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_103'] = x__command_invokes_runner__mutmut_103 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_104'] = x__command_invokes_runner__mutmut_104 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_105'] = x__command_invokes_runner__mutmut_105 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_106'] = x__command_invokes_runner__mutmut_106 # type: ignore # mutmut generated
mutants_x__command_invokes_runner__mutmut['x__command_invokes_runner__mutmut_107'] = x__command_invokes_runner__mutmut_107 # type: ignore # mutmut generated
mutants_x__skip_options__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__skip_options__mutmut)
def _skip_options(command: list[str], position: int) -> int:
    """Skip wrapper flags before its executable, including value-taking flags."""
    takes_value = {"--package", "-p", "--filter", "--dir", "--workspace-root", "--config", "--registry"}
    while position < len(command) and command[position].startswith("-"):
        if command[position] == "--":
            return position + 1
        position += 2 if command[position] in takes_value else 1
    return position


def x__skip_options__mutmut_orig(command: list[str], position: int) -> int:
    """Skip wrapper flags before its executable, including value-taking flags."""
    takes_value = {"--package", "-p", "--filter", "--dir", "--workspace-root", "--config", "--registry"}
    while position < len(command) and command[position].startswith("-"):
        if command[position] == "--":
            return position + 1
        position += 2 if command[position] in takes_value else 1
    return position


def x__skip_options__mutmut_1(command: list[str], position: int) -> int:
    """Skip wrapper flags before its executable, including value-taking flags."""
    takes_value = None
    while position < len(command) and command[position].startswith("-"):
        if command[position] == "--":
            return position + 1
        position += 2 if command[position] in takes_value else 1
    return position


def x__skip_options__mutmut_2(command: list[str], position: int) -> int:
    """Skip wrapper flags before its executable, including value-taking flags."""
    takes_value = {"XX--packageXX", "-p", "--filter", "--dir", "--workspace-root", "--config", "--registry"}
    while position < len(command) and command[position].startswith("-"):
        if command[position] == "--":
            return position + 1
        position += 2 if command[position] in takes_value else 1
    return position


def x__skip_options__mutmut_3(command: list[str], position: int) -> int:
    """Skip wrapper flags before its executable, including value-taking flags."""
    takes_value = {"--PACKAGE", "-p", "--filter", "--dir", "--workspace-root", "--config", "--registry"}
    while position < len(command) and command[position].startswith("-"):
        if command[position] == "--":
            return position + 1
        position += 2 if command[position] in takes_value else 1
    return position


def x__skip_options__mutmut_4(command: list[str], position: int) -> int:
    """Skip wrapper flags before its executable, including value-taking flags."""
    takes_value = {"--package", "XX-pXX", "--filter", "--dir", "--workspace-root", "--config", "--registry"}
    while position < len(command) and command[position].startswith("-"):
        if command[position] == "--":
            return position + 1
        position += 2 if command[position] in takes_value else 1
    return position


def x__skip_options__mutmut_5(command: list[str], position: int) -> int:
    """Skip wrapper flags before its executable, including value-taking flags."""
    takes_value = {"--package", "-P", "--filter", "--dir", "--workspace-root", "--config", "--registry"}
    while position < len(command) and command[position].startswith("-"):
        if command[position] == "--":
            return position + 1
        position += 2 if command[position] in takes_value else 1
    return position


def x__skip_options__mutmut_6(command: list[str], position: int) -> int:
    """Skip wrapper flags before its executable, including value-taking flags."""
    takes_value = {"--package", "-p", "XX--filterXX", "--dir", "--workspace-root", "--config", "--registry"}
    while position < len(command) and command[position].startswith("-"):
        if command[position] == "--":
            return position + 1
        position += 2 if command[position] in takes_value else 1
    return position


def x__skip_options__mutmut_7(command: list[str], position: int) -> int:
    """Skip wrapper flags before its executable, including value-taking flags."""
    takes_value = {"--package", "-p", "--FILTER", "--dir", "--workspace-root", "--config", "--registry"}
    while position < len(command) and command[position].startswith("-"):
        if command[position] == "--":
            return position + 1
        position += 2 if command[position] in takes_value else 1
    return position


def x__skip_options__mutmut_8(command: list[str], position: int) -> int:
    """Skip wrapper flags before its executable, including value-taking flags."""
    takes_value = {"--package", "-p", "--filter", "XX--dirXX", "--workspace-root", "--config", "--registry"}
    while position < len(command) and command[position].startswith("-"):
        if command[position] == "--":
            return position + 1
        position += 2 if command[position] in takes_value else 1
    return position


def x__skip_options__mutmut_9(command: list[str], position: int) -> int:
    """Skip wrapper flags before its executable, including value-taking flags."""
    takes_value = {"--package", "-p", "--filter", "--DIR", "--workspace-root", "--config", "--registry"}
    while position < len(command) and command[position].startswith("-"):
        if command[position] == "--":
            return position + 1
        position += 2 if command[position] in takes_value else 1
    return position


def x__skip_options__mutmut_10(command: list[str], position: int) -> int:
    """Skip wrapper flags before its executable, including value-taking flags."""
    takes_value = {"--package", "-p", "--filter", "--dir", "XX--workspace-rootXX", "--config", "--registry"}
    while position < len(command) and command[position].startswith("-"):
        if command[position] == "--":
            return position + 1
        position += 2 if command[position] in takes_value else 1
    return position


def x__skip_options__mutmut_11(command: list[str], position: int) -> int:
    """Skip wrapper flags before its executable, including value-taking flags."""
    takes_value = {"--package", "-p", "--filter", "--dir", "--WORKSPACE-ROOT", "--config", "--registry"}
    while position < len(command) and command[position].startswith("-"):
        if command[position] == "--":
            return position + 1
        position += 2 if command[position] in takes_value else 1
    return position


def x__skip_options__mutmut_12(command: list[str], position: int) -> int:
    """Skip wrapper flags before its executable, including value-taking flags."""
    takes_value = {"--package", "-p", "--filter", "--dir", "--workspace-root", "XX--configXX", "--registry"}
    while position < len(command) and command[position].startswith("-"):
        if command[position] == "--":
            return position + 1
        position += 2 if command[position] in takes_value else 1
    return position


def x__skip_options__mutmut_13(command: list[str], position: int) -> int:
    """Skip wrapper flags before its executable, including value-taking flags."""
    takes_value = {"--package", "-p", "--filter", "--dir", "--workspace-root", "--CONFIG", "--registry"}
    while position < len(command) and command[position].startswith("-"):
        if command[position] == "--":
            return position + 1
        position += 2 if command[position] in takes_value else 1
    return position


def x__skip_options__mutmut_14(command: list[str], position: int) -> int:
    """Skip wrapper flags before its executable, including value-taking flags."""
    takes_value = {"--package", "-p", "--filter", "--dir", "--workspace-root", "--config", "XX--registryXX"}
    while position < len(command) and command[position].startswith("-"):
        if command[position] == "--":
            return position + 1
        position += 2 if command[position] in takes_value else 1
    return position


def x__skip_options__mutmut_15(command: list[str], position: int) -> int:
    """Skip wrapper flags before its executable, including value-taking flags."""
    takes_value = {"--package", "-p", "--filter", "--dir", "--workspace-root", "--config", "--REGISTRY"}
    while position < len(command) and command[position].startswith("-"):
        if command[position] == "--":
            return position + 1
        position += 2 if command[position] in takes_value else 1
    return position


def x__skip_options__mutmut_16(command: list[str], position: int) -> int:
    """Skip wrapper flags before its executable, including value-taking flags."""
    takes_value = {"--package", "-p", "--filter", "--dir", "--workspace-root", "--config", "--registry"}
    while position < len(command) or command[position].startswith("-"):
        if command[position] == "--":
            return position + 1
        position += 2 if command[position] in takes_value else 1
    return position


def x__skip_options__mutmut_17(command: list[str], position: int) -> int:
    """Skip wrapper flags before its executable, including value-taking flags."""
    takes_value = {"--package", "-p", "--filter", "--dir", "--workspace-root", "--config", "--registry"}
    while position <= len(command) and command[position].startswith("-"):
        if command[position] == "--":
            return position + 1
        position += 2 if command[position] in takes_value else 1
    return position


def x__skip_options__mutmut_18(command: list[str], position: int) -> int:
    """Skip wrapper flags before its executable, including value-taking flags."""
    takes_value = {"--package", "-p", "--filter", "--dir", "--workspace-root", "--config", "--registry"}
    while position < len(command) and command[position].startswith(None):
        if command[position] == "--":
            return position + 1
        position += 2 if command[position] in takes_value else 1
    return position


def x__skip_options__mutmut_19(command: list[str], position: int) -> int:
    """Skip wrapper flags before its executable, including value-taking flags."""
    takes_value = {"--package", "-p", "--filter", "--dir", "--workspace-root", "--config", "--registry"}
    while position < len(command) and command[position].startswith("XX-XX"):
        if command[position] == "--":
            return position + 1
        position += 2 if command[position] in takes_value else 1
    return position


def x__skip_options__mutmut_20(command: list[str], position: int) -> int:
    """Skip wrapper flags before its executable, including value-taking flags."""
    takes_value = {"--package", "-p", "--filter", "--dir", "--workspace-root", "--config", "--registry"}
    while position < len(command) and command[position].startswith("-"):
        if command[position] != "--":
            return position + 1
        position += 2 if command[position] in takes_value else 1
    return position


def x__skip_options__mutmut_21(command: list[str], position: int) -> int:
    """Skip wrapper flags before its executable, including value-taking flags."""
    takes_value = {"--package", "-p", "--filter", "--dir", "--workspace-root", "--config", "--registry"}
    while position < len(command) and command[position].startswith("-"):
        if command[position] == "XX--XX":
            return position + 1
        position += 2 if command[position] in takes_value else 1
    return position


def x__skip_options__mutmut_22(command: list[str], position: int) -> int:
    """Skip wrapper flags before its executable, including value-taking flags."""
    takes_value = {"--package", "-p", "--filter", "--dir", "--workspace-root", "--config", "--registry"}
    while position < len(command) and command[position].startswith("-"):
        if command[position] == "--":
            return position - 1
        position += 2 if command[position] in takes_value else 1
    return position


def x__skip_options__mutmut_23(command: list[str], position: int) -> int:
    """Skip wrapper flags before its executable, including value-taking flags."""
    takes_value = {"--package", "-p", "--filter", "--dir", "--workspace-root", "--config", "--registry"}
    while position < len(command) and command[position].startswith("-"):
        if command[position] == "--":
            return position + 2
        position += 2 if command[position] in takes_value else 1
    return position


def x__skip_options__mutmut_24(command: list[str], position: int) -> int:
    """Skip wrapper flags before its executable, including value-taking flags."""
    takes_value = {"--package", "-p", "--filter", "--dir", "--workspace-root", "--config", "--registry"}
    while position < len(command) and command[position].startswith("-"):
        if command[position] == "--":
            return position + 1
        position = 2 if command[position] in takes_value else 1
    return position


def x__skip_options__mutmut_25(command: list[str], position: int) -> int:
    """Skip wrapper flags before its executable, including value-taking flags."""
    takes_value = {"--package", "-p", "--filter", "--dir", "--workspace-root", "--config", "--registry"}
    while position < len(command) and command[position].startswith("-"):
        if command[position] == "--":
            return position + 1
        position -= 2 if command[position] in takes_value else 1
    return position


def x__skip_options__mutmut_26(command: list[str], position: int) -> int:
    """Skip wrapper flags before its executable, including value-taking flags."""
    takes_value = {"--package", "-p", "--filter", "--dir", "--workspace-root", "--config", "--registry"}
    while position < len(command) and command[position].startswith("-"):
        if command[position] == "--":
            return position + 1
        position += 3 if command[position] in takes_value else 1
    return position


def x__skip_options__mutmut_27(command: list[str], position: int) -> int:
    """Skip wrapper flags before its executable, including value-taking flags."""
    takes_value = {"--package", "-p", "--filter", "--dir", "--workspace-root", "--config", "--registry"}
    while position < len(command) and command[position].startswith("-"):
        if command[position] == "--":
            return position + 1
        position += 2 if command[position] not in takes_value else 1
    return position


def x__skip_options__mutmut_28(command: list[str], position: int) -> int:
    """Skip wrapper flags before its executable, including value-taking flags."""
    takes_value = {"--package", "-p", "--filter", "--dir", "--workspace-root", "--config", "--registry"}
    while position < len(command) and command[position].startswith("-"):
        if command[position] == "--":
            return position + 1
        position += 2 if command[position] in takes_value else 2
    return position

mutants_x__skip_options__mutmut['_mutmut_orig'] = x__skip_options__mutmut_orig # type: ignore # mutmut generated
mutants_x__skip_options__mutmut['x__skip_options__mutmut_1'] = x__skip_options__mutmut_1 # type: ignore # mutmut generated
mutants_x__skip_options__mutmut['x__skip_options__mutmut_2'] = x__skip_options__mutmut_2 # type: ignore # mutmut generated
mutants_x__skip_options__mutmut['x__skip_options__mutmut_3'] = x__skip_options__mutmut_3 # type: ignore # mutmut generated
mutants_x__skip_options__mutmut['x__skip_options__mutmut_4'] = x__skip_options__mutmut_4 # type: ignore # mutmut generated
mutants_x__skip_options__mutmut['x__skip_options__mutmut_5'] = x__skip_options__mutmut_5 # type: ignore # mutmut generated
mutants_x__skip_options__mutmut['x__skip_options__mutmut_6'] = x__skip_options__mutmut_6 # type: ignore # mutmut generated
mutants_x__skip_options__mutmut['x__skip_options__mutmut_7'] = x__skip_options__mutmut_7 # type: ignore # mutmut generated
mutants_x__skip_options__mutmut['x__skip_options__mutmut_8'] = x__skip_options__mutmut_8 # type: ignore # mutmut generated
mutants_x__skip_options__mutmut['x__skip_options__mutmut_9'] = x__skip_options__mutmut_9 # type: ignore # mutmut generated
mutants_x__skip_options__mutmut['x__skip_options__mutmut_10'] = x__skip_options__mutmut_10 # type: ignore # mutmut generated
mutants_x__skip_options__mutmut['x__skip_options__mutmut_11'] = x__skip_options__mutmut_11 # type: ignore # mutmut generated
mutants_x__skip_options__mutmut['x__skip_options__mutmut_12'] = x__skip_options__mutmut_12 # type: ignore # mutmut generated
mutants_x__skip_options__mutmut['x__skip_options__mutmut_13'] = x__skip_options__mutmut_13 # type: ignore # mutmut generated
mutants_x__skip_options__mutmut['x__skip_options__mutmut_14'] = x__skip_options__mutmut_14 # type: ignore # mutmut generated
mutants_x__skip_options__mutmut['x__skip_options__mutmut_15'] = x__skip_options__mutmut_15 # type: ignore # mutmut generated
mutants_x__skip_options__mutmut['x__skip_options__mutmut_16'] = x__skip_options__mutmut_16 # type: ignore # mutmut generated
mutants_x__skip_options__mutmut['x__skip_options__mutmut_17'] = x__skip_options__mutmut_17 # type: ignore # mutmut generated
mutants_x__skip_options__mutmut['x__skip_options__mutmut_18'] = x__skip_options__mutmut_18 # type: ignore # mutmut generated
mutants_x__skip_options__mutmut['x__skip_options__mutmut_19'] = x__skip_options__mutmut_19 # type: ignore # mutmut generated
mutants_x__skip_options__mutmut['x__skip_options__mutmut_20'] = x__skip_options__mutmut_20 # type: ignore # mutmut generated
mutants_x__skip_options__mutmut['x__skip_options__mutmut_21'] = x__skip_options__mutmut_21 # type: ignore # mutmut generated
mutants_x__skip_options__mutmut['x__skip_options__mutmut_22'] = x__skip_options__mutmut_22 # type: ignore # mutmut generated
mutants_x__skip_options__mutmut['x__skip_options__mutmut_23'] = x__skip_options__mutmut_23 # type: ignore # mutmut generated
mutants_x__skip_options__mutmut['x__skip_options__mutmut_24'] = x__skip_options__mutmut_24 # type: ignore # mutmut generated
mutants_x__skip_options__mutmut['x__skip_options__mutmut_25'] = x__skip_options__mutmut_25 # type: ignore # mutmut generated
mutants_x__skip_options__mutmut['x__skip_options__mutmut_26'] = x__skip_options__mutmut_26 # type: ignore # mutmut generated
mutants_x__skip_options__mutmut['x__skip_options__mutmut_27'] = x__skip_options__mutmut_27 # type: ignore # mutmut generated
mutants_x__skip_options__mutmut['x__skip_options__mutmut_28'] = x__skip_options__mutmut_28 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁNoNoopTestScriptsǁ_is_prod_manifest__mutmut: MutantDict = {}  # type: ignore
mutants_xǁNoNoopTestScriptsǁenumerate_files__mutmut: MutantDict = {}  # type: ignore
mutants_xǁNoNoopTestScriptsǁis_in_scope__mutmut: MutantDict = {}  # type: ignore
mutants_xǁNoNoopTestScriptsǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore


class NoNoopTestScripts(FitnessRule):
    """Flags production packages whose ``test`` script is a no-op placeholder."""

    name = "no-noop-test-scripts"
    remediation = REMEDIATION
    # extensions is unused (enumeration + scope are overridden) but kept at the
    # repo-neutral default for the ABC contract.
    extensions = (".json",)

    #: Repo-relative path prefixes under which a package is production code.
    prod_package_prefixes: tuple[str, ...] = ()
    #: Placeholder + real-runner patterns (compiled lazily, see ``from_config``).
    placeholder_pattern: str = DEFAULT_PLACEHOLDER_PATTERN
    real_runner_pattern: str = DEFAULT_REAL_RUNNER_PATTERN

    @classmethod
    @_mutmut_mutated(mutants_xǁNoNoopTestScriptsǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoNoopTestScripts:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoNoopTestScripts)  # noqa: S101  # narrowing for mypy
        prefixes = config.get("prod_package_prefixes")
        rule.prod_package_prefixes = tuple(prefixes) if prefixes is not None else ()
        rule.placeholder_pattern = config.get("placeholder_pattern", DEFAULT_PLACEHOLDER_PATTERN)
        rule.real_runner_pattern = config.get("real_runner_pattern", DEFAULT_REAL_RUNNER_PATTERN)
        return rule

    @classmethod
    def xǁNoNoopTestScriptsǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoNoopTestScripts:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoNoopTestScripts)  # noqa: S101  # narrowing for mypy
        prefixes = config.get("prod_package_prefixes")
        rule.prod_package_prefixes = tuple(prefixes) if prefixes is not None else ()
        rule.placeholder_pattern = config.get("placeholder_pattern", DEFAULT_PLACEHOLDER_PATTERN)
        rule.real_runner_pattern = config.get("real_runner_pattern", DEFAULT_REAL_RUNNER_PATTERN)
        return rule

    @classmethod
    def xǁNoNoopTestScriptsǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoNoopTestScripts:
        rule = None
        assert isinstance(rule, NoNoopTestScripts)  # noqa: S101  # narrowing for mypy
        prefixes = config.get("prod_package_prefixes")
        rule.prod_package_prefixes = tuple(prefixes) if prefixes is not None else ()
        rule.placeholder_pattern = config.get("placeholder_pattern", DEFAULT_PLACEHOLDER_PATTERN)
        rule.real_runner_pattern = config.get("real_runner_pattern", DEFAULT_REAL_RUNNER_PATTERN)
        return rule

    @classmethod
    def xǁNoNoopTestScriptsǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoNoopTestScripts:
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, NoNoopTestScripts)  # noqa: S101  # narrowing for mypy
        prefixes = config.get("prod_package_prefixes")
        rule.prod_package_prefixes = tuple(prefixes) if prefixes is not None else ()
        rule.placeholder_pattern = config.get("placeholder_pattern", DEFAULT_PLACEHOLDER_PATTERN)
        rule.real_runner_pattern = config.get("real_runner_pattern", DEFAULT_REAL_RUNNER_PATTERN)
        return rule

    @classmethod
    def xǁNoNoopTestScriptsǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoNoopTestScripts:
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, NoNoopTestScripts)  # noqa: S101  # narrowing for mypy
        prefixes = config.get("prod_package_prefixes")
        rule.prod_package_prefixes = tuple(prefixes) if prefixes is not None else ()
        rule.placeholder_pattern = config.get("placeholder_pattern", DEFAULT_PLACEHOLDER_PATTERN)
        rule.real_runner_pattern = config.get("real_runner_pattern", DEFAULT_REAL_RUNNER_PATTERN)
        return rule

    @classmethod
    def xǁNoNoopTestScriptsǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoNoopTestScripts:
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, NoNoopTestScripts)  # noqa: S101  # narrowing for mypy
        prefixes = config.get("prod_package_prefixes")
        rule.prod_package_prefixes = tuple(prefixes) if prefixes is not None else ()
        rule.placeholder_pattern = config.get("placeholder_pattern", DEFAULT_PLACEHOLDER_PATTERN)
        rule.real_runner_pattern = config.get("real_runner_pattern", DEFAULT_REAL_RUNNER_PATTERN)
        return rule

    @classmethod
    def xǁNoNoopTestScriptsǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoNoopTestScripts:
        rule = super().from_config(config, )
        assert isinstance(rule, NoNoopTestScripts)  # noqa: S101  # narrowing for mypy
        prefixes = config.get("prod_package_prefixes")
        rule.prod_package_prefixes = tuple(prefixes) if prefixes is not None else ()
        rule.placeholder_pattern = config.get("placeholder_pattern", DEFAULT_PLACEHOLDER_PATTERN)
        rule.real_runner_pattern = config.get("real_runner_pattern", DEFAULT_REAL_RUNNER_PATTERN)
        return rule

    @classmethod
    def xǁNoNoopTestScriptsǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoNoopTestScripts:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoNoopTestScripts)  # noqa: S101  # narrowing for mypy
        prefixes = None
        rule.prod_package_prefixes = tuple(prefixes) if prefixes is not None else ()
        rule.placeholder_pattern = config.get("placeholder_pattern", DEFAULT_PLACEHOLDER_PATTERN)
        rule.real_runner_pattern = config.get("real_runner_pattern", DEFAULT_REAL_RUNNER_PATTERN)
        return rule

    @classmethod
    def xǁNoNoopTestScriptsǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoNoopTestScripts:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoNoopTestScripts)  # noqa: S101  # narrowing for mypy
        prefixes = config.get(None)
        rule.prod_package_prefixes = tuple(prefixes) if prefixes is not None else ()
        rule.placeholder_pattern = config.get("placeholder_pattern", DEFAULT_PLACEHOLDER_PATTERN)
        rule.real_runner_pattern = config.get("real_runner_pattern", DEFAULT_REAL_RUNNER_PATTERN)
        return rule

    @classmethod
    def xǁNoNoopTestScriptsǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoNoopTestScripts:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoNoopTestScripts)  # noqa: S101  # narrowing for mypy
        prefixes = config.get("XXprod_package_prefixesXX")
        rule.prod_package_prefixes = tuple(prefixes) if prefixes is not None else ()
        rule.placeholder_pattern = config.get("placeholder_pattern", DEFAULT_PLACEHOLDER_PATTERN)
        rule.real_runner_pattern = config.get("real_runner_pattern", DEFAULT_REAL_RUNNER_PATTERN)
        return rule

    @classmethod
    def xǁNoNoopTestScriptsǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoNoopTestScripts:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoNoopTestScripts)  # noqa: S101  # narrowing for mypy
        prefixes = config.get("PROD_PACKAGE_PREFIXES")
        rule.prod_package_prefixes = tuple(prefixes) if prefixes is not None else ()
        rule.placeholder_pattern = config.get("placeholder_pattern", DEFAULT_PLACEHOLDER_PATTERN)
        rule.real_runner_pattern = config.get("real_runner_pattern", DEFAULT_REAL_RUNNER_PATTERN)
        return rule

    @classmethod
    def xǁNoNoopTestScriptsǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoNoopTestScripts:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoNoopTestScripts)  # noqa: S101  # narrowing for mypy
        prefixes = config.get("prod_package_prefixes")
        rule.prod_package_prefixes = None
        rule.placeholder_pattern = config.get("placeholder_pattern", DEFAULT_PLACEHOLDER_PATTERN)
        rule.real_runner_pattern = config.get("real_runner_pattern", DEFAULT_REAL_RUNNER_PATTERN)
        return rule

    @classmethod
    def xǁNoNoopTestScriptsǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoNoopTestScripts:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoNoopTestScripts)  # noqa: S101  # narrowing for mypy
        prefixes = config.get("prod_package_prefixes")
        rule.prod_package_prefixes = tuple(None) if prefixes is not None else ()
        rule.placeholder_pattern = config.get("placeholder_pattern", DEFAULT_PLACEHOLDER_PATTERN)
        rule.real_runner_pattern = config.get("real_runner_pattern", DEFAULT_REAL_RUNNER_PATTERN)
        return rule

    @classmethod
    def xǁNoNoopTestScriptsǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoNoopTestScripts:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoNoopTestScripts)  # noqa: S101  # narrowing for mypy
        prefixes = config.get("prod_package_prefixes")
        rule.prod_package_prefixes = tuple(prefixes) if prefixes is None else ()
        rule.placeholder_pattern = config.get("placeholder_pattern", DEFAULT_PLACEHOLDER_PATTERN)
        rule.real_runner_pattern = config.get("real_runner_pattern", DEFAULT_REAL_RUNNER_PATTERN)
        return rule

    @classmethod
    def xǁNoNoopTestScriptsǁfrom_config__mutmut_13(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoNoopTestScripts:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoNoopTestScripts)  # noqa: S101  # narrowing for mypy
        prefixes = config.get("prod_package_prefixes")
        rule.prod_package_prefixes = tuple(prefixes) if prefixes is not None else ()
        rule.placeholder_pattern = None
        rule.real_runner_pattern = config.get("real_runner_pattern", DEFAULT_REAL_RUNNER_PATTERN)
        return rule

    @classmethod
    def xǁNoNoopTestScriptsǁfrom_config__mutmut_14(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoNoopTestScripts:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoNoopTestScripts)  # noqa: S101  # narrowing for mypy
        prefixes = config.get("prod_package_prefixes")
        rule.prod_package_prefixes = tuple(prefixes) if prefixes is not None else ()
        rule.placeholder_pattern = config.get(None, DEFAULT_PLACEHOLDER_PATTERN)
        rule.real_runner_pattern = config.get("real_runner_pattern", DEFAULT_REAL_RUNNER_PATTERN)
        return rule

    @classmethod
    def xǁNoNoopTestScriptsǁfrom_config__mutmut_15(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoNoopTestScripts:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoNoopTestScripts)  # noqa: S101  # narrowing for mypy
        prefixes = config.get("prod_package_prefixes")
        rule.prod_package_prefixes = tuple(prefixes) if prefixes is not None else ()
        rule.placeholder_pattern = config.get("placeholder_pattern", None)
        rule.real_runner_pattern = config.get("real_runner_pattern", DEFAULT_REAL_RUNNER_PATTERN)
        return rule

    @classmethod
    def xǁNoNoopTestScriptsǁfrom_config__mutmut_16(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoNoopTestScripts:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoNoopTestScripts)  # noqa: S101  # narrowing for mypy
        prefixes = config.get("prod_package_prefixes")
        rule.prod_package_prefixes = tuple(prefixes) if prefixes is not None else ()
        rule.placeholder_pattern = config.get(DEFAULT_PLACEHOLDER_PATTERN)
        rule.real_runner_pattern = config.get("real_runner_pattern", DEFAULT_REAL_RUNNER_PATTERN)
        return rule

    @classmethod
    def xǁNoNoopTestScriptsǁfrom_config__mutmut_17(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoNoopTestScripts:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoNoopTestScripts)  # noqa: S101  # narrowing for mypy
        prefixes = config.get("prod_package_prefixes")
        rule.prod_package_prefixes = tuple(prefixes) if prefixes is not None else ()
        rule.placeholder_pattern = config.get("placeholder_pattern", )
        rule.real_runner_pattern = config.get("real_runner_pattern", DEFAULT_REAL_RUNNER_PATTERN)
        return rule

    @classmethod
    def xǁNoNoopTestScriptsǁfrom_config__mutmut_18(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoNoopTestScripts:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoNoopTestScripts)  # noqa: S101  # narrowing for mypy
        prefixes = config.get("prod_package_prefixes")
        rule.prod_package_prefixes = tuple(prefixes) if prefixes is not None else ()
        rule.placeholder_pattern = config.get("XXplaceholder_patternXX", DEFAULT_PLACEHOLDER_PATTERN)
        rule.real_runner_pattern = config.get("real_runner_pattern", DEFAULT_REAL_RUNNER_PATTERN)
        return rule

    @classmethod
    def xǁNoNoopTestScriptsǁfrom_config__mutmut_19(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoNoopTestScripts:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoNoopTestScripts)  # noqa: S101  # narrowing for mypy
        prefixes = config.get("prod_package_prefixes")
        rule.prod_package_prefixes = tuple(prefixes) if prefixes is not None else ()
        rule.placeholder_pattern = config.get("PLACEHOLDER_PATTERN", DEFAULT_PLACEHOLDER_PATTERN)
        rule.real_runner_pattern = config.get("real_runner_pattern", DEFAULT_REAL_RUNNER_PATTERN)
        return rule

    @classmethod
    def xǁNoNoopTestScriptsǁfrom_config__mutmut_20(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoNoopTestScripts:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoNoopTestScripts)  # noqa: S101  # narrowing for mypy
        prefixes = config.get("prod_package_prefixes")
        rule.prod_package_prefixes = tuple(prefixes) if prefixes is not None else ()
        rule.placeholder_pattern = config.get("placeholder_pattern", DEFAULT_PLACEHOLDER_PATTERN)
        rule.real_runner_pattern = None
        return rule

    @classmethod
    def xǁNoNoopTestScriptsǁfrom_config__mutmut_21(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoNoopTestScripts:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoNoopTestScripts)  # noqa: S101  # narrowing for mypy
        prefixes = config.get("prod_package_prefixes")
        rule.prod_package_prefixes = tuple(prefixes) if prefixes is not None else ()
        rule.placeholder_pattern = config.get("placeholder_pattern", DEFAULT_PLACEHOLDER_PATTERN)
        rule.real_runner_pattern = config.get(None, DEFAULT_REAL_RUNNER_PATTERN)
        return rule

    @classmethod
    def xǁNoNoopTestScriptsǁfrom_config__mutmut_22(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoNoopTestScripts:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoNoopTestScripts)  # noqa: S101  # narrowing for mypy
        prefixes = config.get("prod_package_prefixes")
        rule.prod_package_prefixes = tuple(prefixes) if prefixes is not None else ()
        rule.placeholder_pattern = config.get("placeholder_pattern", DEFAULT_PLACEHOLDER_PATTERN)
        rule.real_runner_pattern = config.get("real_runner_pattern", None)
        return rule

    @classmethod
    def xǁNoNoopTestScriptsǁfrom_config__mutmut_23(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoNoopTestScripts:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoNoopTestScripts)  # noqa: S101  # narrowing for mypy
        prefixes = config.get("prod_package_prefixes")
        rule.prod_package_prefixes = tuple(prefixes) if prefixes is not None else ()
        rule.placeholder_pattern = config.get("placeholder_pattern", DEFAULT_PLACEHOLDER_PATTERN)
        rule.real_runner_pattern = config.get(DEFAULT_REAL_RUNNER_PATTERN)
        return rule

    @classmethod
    def xǁNoNoopTestScriptsǁfrom_config__mutmut_24(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoNoopTestScripts:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoNoopTestScripts)  # noqa: S101  # narrowing for mypy
        prefixes = config.get("prod_package_prefixes")
        rule.prod_package_prefixes = tuple(prefixes) if prefixes is not None else ()
        rule.placeholder_pattern = config.get("placeholder_pattern", DEFAULT_PLACEHOLDER_PATTERN)
        rule.real_runner_pattern = config.get("real_runner_pattern", )
        return rule

    @classmethod
    def xǁNoNoopTestScriptsǁfrom_config__mutmut_25(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoNoopTestScripts:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoNoopTestScripts)  # noqa: S101  # narrowing for mypy
        prefixes = config.get("prod_package_prefixes")
        rule.prod_package_prefixes = tuple(prefixes) if prefixes is not None else ()
        rule.placeholder_pattern = config.get("placeholder_pattern", DEFAULT_PLACEHOLDER_PATTERN)
        rule.real_runner_pattern = config.get("XXreal_runner_patternXX", DEFAULT_REAL_RUNNER_PATTERN)
        return rule

    @classmethod
    def xǁNoNoopTestScriptsǁfrom_config__mutmut_26(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoNoopTestScripts:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoNoopTestScripts)  # noqa: S101  # narrowing for mypy
        prefixes = config.get("prod_package_prefixes")
        rule.prod_package_prefixes = tuple(prefixes) if prefixes is not None else ()
        rule.placeholder_pattern = config.get("placeholder_pattern", DEFAULT_PLACEHOLDER_PATTERN)
        rule.real_runner_pattern = config.get("REAL_RUNNER_PATTERN", DEFAULT_REAL_RUNNER_PATTERN)
        return rule

    @_mutmut_mutated(mutants_xǁNoNoopTestScriptsǁ_is_prod_manifest__mutmut)
    def _is_prod_manifest(self, rel: str) -> bool:
        """The root manifest, or any manifest under a production prefix, is in scope."""
        if rel == _MANIFEST_NAME:
            return True
        return any(rel.startswith(prefix) for prefix in self.prod_package_prefixes)

    def xǁNoNoopTestScriptsǁ_is_prod_manifest__mutmut_orig(self, rel: str) -> bool:
        """The root manifest, or any manifest under a production prefix, is in scope."""
        if rel == _MANIFEST_NAME:
            return True
        return any(rel.startswith(prefix) for prefix in self.prod_package_prefixes)

    def xǁNoNoopTestScriptsǁ_is_prod_manifest__mutmut_1(self, rel: str) -> bool:
        """The root manifest, or any manifest under a production prefix, is in scope."""
        if rel != _MANIFEST_NAME:
            return True
        return any(rel.startswith(prefix) for prefix in self.prod_package_prefixes)

    def xǁNoNoopTestScriptsǁ_is_prod_manifest__mutmut_2(self, rel: str) -> bool:
        """The root manifest, or any manifest under a production prefix, is in scope."""
        if rel == _MANIFEST_NAME:
            return False
        return any(rel.startswith(prefix) for prefix in self.prod_package_prefixes)

    def xǁNoNoopTestScriptsǁ_is_prod_manifest__mutmut_3(self, rel: str) -> bool:
        """The root manifest, or any manifest under a production prefix, is in scope."""
        if rel == _MANIFEST_NAME:
            return True
        return any(None)

    def xǁNoNoopTestScriptsǁ_is_prod_manifest__mutmut_4(self, rel: str) -> bool:
        """The root manifest, or any manifest under a production prefix, is in scope."""
        if rel == _MANIFEST_NAME:
            return True
        return any(rel.startswith(None) for prefix in self.prod_package_prefixes)

    @_mutmut_mutated(mutants_xǁNoNoopTestScriptsǁenumerate_files__mutmut)
    def enumerate_files(self) -> list[Path]:
        """Discover every in-scope ``package.json`` under the repo root."""
        out: list[Path] = []
        for path in self._repo_root.rglob(_MANIFEST_NAME):
            if any(part in DEFAULT_SKIP_PARTS for part in path.parts):
                continue
            rel = self._repo_relative(path).as_posix()
            if self._is_prod_manifest(rel):
                out.append(path)
        return out

    def xǁNoNoopTestScriptsǁenumerate_files__mutmut_orig(self) -> list[Path]:
        """Discover every in-scope ``package.json`` under the repo root."""
        out: list[Path] = []
        for path in self._repo_root.rglob(_MANIFEST_NAME):
            if any(part in DEFAULT_SKIP_PARTS for part in path.parts):
                continue
            rel = self._repo_relative(path).as_posix()
            if self._is_prod_manifest(rel):
                out.append(path)
        return out

    def xǁNoNoopTestScriptsǁenumerate_files__mutmut_1(self) -> list[Path]:
        """Discover every in-scope ``package.json`` under the repo root."""
        out: list[Path] = None
        for path in self._repo_root.rglob(_MANIFEST_NAME):
            if any(part in DEFAULT_SKIP_PARTS for part in path.parts):
                continue
            rel = self._repo_relative(path).as_posix()
            if self._is_prod_manifest(rel):
                out.append(path)
        return out

    def xǁNoNoopTestScriptsǁenumerate_files__mutmut_2(self) -> list[Path]:
        """Discover every in-scope ``package.json`` under the repo root."""
        out: list[Path] = []
        for path in self._repo_root.rglob(None):
            if any(part in DEFAULT_SKIP_PARTS for part in path.parts):
                continue
            rel = self._repo_relative(path).as_posix()
            if self._is_prod_manifest(rel):
                out.append(path)
        return out

    def xǁNoNoopTestScriptsǁenumerate_files__mutmut_3(self) -> list[Path]:
        """Discover every in-scope ``package.json`` under the repo root."""
        out: list[Path] = []
        for path in self._repo_root.rglob(_MANIFEST_NAME):
            if any(None):
                continue
            rel = self._repo_relative(path).as_posix()
            if self._is_prod_manifest(rel):
                out.append(path)
        return out

    def xǁNoNoopTestScriptsǁenumerate_files__mutmut_4(self) -> list[Path]:
        """Discover every in-scope ``package.json`` under the repo root."""
        out: list[Path] = []
        for path in self._repo_root.rglob(_MANIFEST_NAME):
            if any(part not in DEFAULT_SKIP_PARTS for part in path.parts):
                continue
            rel = self._repo_relative(path).as_posix()
            if self._is_prod_manifest(rel):
                out.append(path)
        return out

    def xǁNoNoopTestScriptsǁenumerate_files__mutmut_5(self) -> list[Path]:
        """Discover every in-scope ``package.json`` under the repo root."""
        out: list[Path] = []
        for path in self._repo_root.rglob(_MANIFEST_NAME):
            if any(part in DEFAULT_SKIP_PARTS for part in path.parts):
                break
            rel = self._repo_relative(path).as_posix()
            if self._is_prod_manifest(rel):
                out.append(path)
        return out

    def xǁNoNoopTestScriptsǁenumerate_files__mutmut_6(self) -> list[Path]:
        """Discover every in-scope ``package.json`` under the repo root."""
        out: list[Path] = []
        for path in self._repo_root.rglob(_MANIFEST_NAME):
            if any(part in DEFAULT_SKIP_PARTS for part in path.parts):
                continue
            rel = None
            if self._is_prod_manifest(rel):
                out.append(path)
        return out

    def xǁNoNoopTestScriptsǁenumerate_files__mutmut_7(self) -> list[Path]:
        """Discover every in-scope ``package.json`` under the repo root."""
        out: list[Path] = []
        for path in self._repo_root.rglob(_MANIFEST_NAME):
            if any(part in DEFAULT_SKIP_PARTS for part in path.parts):
                continue
            rel = self._repo_relative(None).as_posix()
            if self._is_prod_manifest(rel):
                out.append(path)
        return out

    def xǁNoNoopTestScriptsǁenumerate_files__mutmut_8(self) -> list[Path]:
        """Discover every in-scope ``package.json`` under the repo root."""
        out: list[Path] = []
        for path in self._repo_root.rglob(_MANIFEST_NAME):
            if any(part in DEFAULT_SKIP_PARTS for part in path.parts):
                continue
            rel = self._repo_relative(path).as_posix()
            if self._is_prod_manifest(None):
                out.append(path)
        return out

    def xǁNoNoopTestScriptsǁenumerate_files__mutmut_9(self) -> list[Path]:
        """Discover every in-scope ``package.json`` under the repo root."""
        out: list[Path] = []
        for path in self._repo_root.rglob(_MANIFEST_NAME):
            if any(part in DEFAULT_SKIP_PARTS for part in path.parts):
                continue
            rel = self._repo_relative(path).as_posix()
            if self._is_prod_manifest(rel):
                out.append(None)
        return out

    @_mutmut_mutated(mutants_xǁNoNoopTestScriptsǁis_in_scope__mutmut)
    def is_in_scope(self, rel: str) -> bool:
        # Enumeration already restricts to in-scope manifests; the gate's scope
        # predicate just needs to accept what enumeration yields.
        return rel.endswith(_MANIFEST_NAME) and self._is_prod_manifest(rel)

    def xǁNoNoopTestScriptsǁis_in_scope__mutmut_orig(self, rel: str) -> bool:
        # Enumeration already restricts to in-scope manifests; the gate's scope
        # predicate just needs to accept what enumeration yields.
        return rel.endswith(_MANIFEST_NAME) and self._is_prod_manifest(rel)

    def xǁNoNoopTestScriptsǁis_in_scope__mutmut_1(self, rel: str) -> bool:
        # Enumeration already restricts to in-scope manifests; the gate's scope
        # predicate just needs to accept what enumeration yields.
        return rel.endswith(_MANIFEST_NAME) or self._is_prod_manifest(rel)

    def xǁNoNoopTestScriptsǁis_in_scope__mutmut_2(self, rel: str) -> bool:
        # Enumeration already restricts to in-scope manifests; the gate's scope
        # predicate just needs to accept what enumeration yields.
        return rel.endswith(None) and self._is_prod_manifest(rel)

    def xǁNoNoopTestScriptsǁis_in_scope__mutmut_3(self, rel: str) -> bool:
        # Enumeration already restricts to in-scope manifests; the gate's scope
        # predicate just needs to accept what enumeration yields.
        return rel.endswith(_MANIFEST_NAME) and self._is_prod_manifest(None)

    @_mutmut_mutated(mutants_xǁNoNoopTestScriptsǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return True
        if not isinstance(data, Mapping):
            return True
        scripts = data.get("scripts")
        if scripts is not None and not isinstance(scripts, Mapping):
            return True
        test_script = (scripts or {}).get("test")
        if not isinstance(test_script, str):
            return False
        return script_is_noop(
            test_script,
            placeholder=re.compile(self.placeholder_pattern, re.IGNORECASE),
            real_runner=re.compile(self.real_runner_pattern),
        )

    def xǁNoNoopTestScriptsǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return True
        if not isinstance(data, Mapping):
            return True
        scripts = data.get("scripts")
        if scripts is not None and not isinstance(scripts, Mapping):
            return True
        test_script = (scripts or {}).get("test")
        if not isinstance(test_script, str):
            return False
        return script_is_noop(
            test_script,
            placeholder=re.compile(self.placeholder_pattern, re.IGNORECASE),
            real_runner=re.compile(self.real_runner_pattern),
        )

    def xǁNoNoopTestScriptsǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        try:
            data = None
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return True
        if not isinstance(data, Mapping):
            return True
        scripts = data.get("scripts")
        if scripts is not None and not isinstance(scripts, Mapping):
            return True
        test_script = (scripts or {}).get("test")
        if not isinstance(test_script, str):
            return False
        return script_is_noop(
            test_script,
            placeholder=re.compile(self.placeholder_pattern, re.IGNORECASE),
            real_runner=re.compile(self.real_runner_pattern),
        )

    def xǁNoNoopTestScriptsǁfile_has_violation__mutmut_2(self, path: Path) -> bool:
        try:
            data = json.loads(None)
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return True
        if not isinstance(data, Mapping):
            return True
        scripts = data.get("scripts")
        if scripts is not None and not isinstance(scripts, Mapping):
            return True
        test_script = (scripts or {}).get("test")
        if not isinstance(test_script, str):
            return False
        return script_is_noop(
            test_script,
            placeholder=re.compile(self.placeholder_pattern, re.IGNORECASE),
            real_runner=re.compile(self.real_runner_pattern),
        )

    def xǁNoNoopTestScriptsǁfile_has_violation__mutmut_3(self, path: Path) -> bool:
        try:
            data = json.loads(path.read_text(encoding=None))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return True
        if not isinstance(data, Mapping):
            return True
        scripts = data.get("scripts")
        if scripts is not None and not isinstance(scripts, Mapping):
            return True
        test_script = (scripts or {}).get("test")
        if not isinstance(test_script, str):
            return False
        return script_is_noop(
            test_script,
            placeholder=re.compile(self.placeholder_pattern, re.IGNORECASE),
            real_runner=re.compile(self.real_runner_pattern),
        )

    def xǁNoNoopTestScriptsǁfile_has_violation__mutmut_4(self, path: Path) -> bool:
        try:
            data = json.loads(path.read_text(encoding="XXutf-8XX"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return True
        if not isinstance(data, Mapping):
            return True
        scripts = data.get("scripts")
        if scripts is not None and not isinstance(scripts, Mapping):
            return True
        test_script = (scripts or {}).get("test")
        if not isinstance(test_script, str):
            return False
        return script_is_noop(
            test_script,
            placeholder=re.compile(self.placeholder_pattern, re.IGNORECASE),
            real_runner=re.compile(self.real_runner_pattern),
        )

    def xǁNoNoopTestScriptsǁfile_has_violation__mutmut_5(self, path: Path) -> bool:
        try:
            data = json.loads(path.read_text(encoding="UTF-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return True
        if not isinstance(data, Mapping):
            return True
        scripts = data.get("scripts")
        if scripts is not None and not isinstance(scripts, Mapping):
            return True
        test_script = (scripts or {}).get("test")
        if not isinstance(test_script, str):
            return False
        return script_is_noop(
            test_script,
            placeholder=re.compile(self.placeholder_pattern, re.IGNORECASE),
            real_runner=re.compile(self.real_runner_pattern),
        )

    def xǁNoNoopTestScriptsǁfile_has_violation__mutmut_6(self, path: Path) -> bool:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return False
        if not isinstance(data, Mapping):
            return True
        scripts = data.get("scripts")
        if scripts is not None and not isinstance(scripts, Mapping):
            return True
        test_script = (scripts or {}).get("test")
        if not isinstance(test_script, str):
            return False
        return script_is_noop(
            test_script,
            placeholder=re.compile(self.placeholder_pattern, re.IGNORECASE),
            real_runner=re.compile(self.real_runner_pattern),
        )

    def xǁNoNoopTestScriptsǁfile_has_violation__mutmut_7(self, path: Path) -> bool:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return True
        if isinstance(data, Mapping):
            return True
        scripts = data.get("scripts")
        if scripts is not None and not isinstance(scripts, Mapping):
            return True
        test_script = (scripts or {}).get("test")
        if not isinstance(test_script, str):
            return False
        return script_is_noop(
            test_script,
            placeholder=re.compile(self.placeholder_pattern, re.IGNORECASE),
            real_runner=re.compile(self.real_runner_pattern),
        )

    def xǁNoNoopTestScriptsǁfile_has_violation__mutmut_8(self, path: Path) -> bool:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return True
        if not isinstance(data, Mapping):
            return False
        scripts = data.get("scripts")
        if scripts is not None and not isinstance(scripts, Mapping):
            return True
        test_script = (scripts or {}).get("test")
        if not isinstance(test_script, str):
            return False
        return script_is_noop(
            test_script,
            placeholder=re.compile(self.placeholder_pattern, re.IGNORECASE),
            real_runner=re.compile(self.real_runner_pattern),
        )

    def xǁNoNoopTestScriptsǁfile_has_violation__mutmut_9(self, path: Path) -> bool:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return True
        if not isinstance(data, Mapping):
            return True
        scripts = None
        if scripts is not None and not isinstance(scripts, Mapping):
            return True
        test_script = (scripts or {}).get("test")
        if not isinstance(test_script, str):
            return False
        return script_is_noop(
            test_script,
            placeholder=re.compile(self.placeholder_pattern, re.IGNORECASE),
            real_runner=re.compile(self.real_runner_pattern),
        )

    def xǁNoNoopTestScriptsǁfile_has_violation__mutmut_10(self, path: Path) -> bool:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return True
        if not isinstance(data, Mapping):
            return True
        scripts = data.get(None)
        if scripts is not None and not isinstance(scripts, Mapping):
            return True
        test_script = (scripts or {}).get("test")
        if not isinstance(test_script, str):
            return False
        return script_is_noop(
            test_script,
            placeholder=re.compile(self.placeholder_pattern, re.IGNORECASE),
            real_runner=re.compile(self.real_runner_pattern),
        )

    def xǁNoNoopTestScriptsǁfile_has_violation__mutmut_11(self, path: Path) -> bool:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return True
        if not isinstance(data, Mapping):
            return True
        scripts = data.get("XXscriptsXX")
        if scripts is not None and not isinstance(scripts, Mapping):
            return True
        test_script = (scripts or {}).get("test")
        if not isinstance(test_script, str):
            return False
        return script_is_noop(
            test_script,
            placeholder=re.compile(self.placeholder_pattern, re.IGNORECASE),
            real_runner=re.compile(self.real_runner_pattern),
        )

    def xǁNoNoopTestScriptsǁfile_has_violation__mutmut_12(self, path: Path) -> bool:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return True
        if not isinstance(data, Mapping):
            return True
        scripts = data.get("SCRIPTS")
        if scripts is not None and not isinstance(scripts, Mapping):
            return True
        test_script = (scripts or {}).get("test")
        if not isinstance(test_script, str):
            return False
        return script_is_noop(
            test_script,
            placeholder=re.compile(self.placeholder_pattern, re.IGNORECASE),
            real_runner=re.compile(self.real_runner_pattern),
        )

    def xǁNoNoopTestScriptsǁfile_has_violation__mutmut_13(self, path: Path) -> bool:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return True
        if not isinstance(data, Mapping):
            return True
        scripts = data.get("scripts")
        if scripts is not None or not isinstance(scripts, Mapping):
            return True
        test_script = (scripts or {}).get("test")
        if not isinstance(test_script, str):
            return False
        return script_is_noop(
            test_script,
            placeholder=re.compile(self.placeholder_pattern, re.IGNORECASE),
            real_runner=re.compile(self.real_runner_pattern),
        )

    def xǁNoNoopTestScriptsǁfile_has_violation__mutmut_14(self, path: Path) -> bool:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return True
        if not isinstance(data, Mapping):
            return True
        scripts = data.get("scripts")
        if scripts is None and not isinstance(scripts, Mapping):
            return True
        test_script = (scripts or {}).get("test")
        if not isinstance(test_script, str):
            return False
        return script_is_noop(
            test_script,
            placeholder=re.compile(self.placeholder_pattern, re.IGNORECASE),
            real_runner=re.compile(self.real_runner_pattern),
        )

    def xǁNoNoopTestScriptsǁfile_has_violation__mutmut_15(self, path: Path) -> bool:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return True
        if not isinstance(data, Mapping):
            return True
        scripts = data.get("scripts")
        if scripts is not None and isinstance(scripts, Mapping):
            return True
        test_script = (scripts or {}).get("test")
        if not isinstance(test_script, str):
            return False
        return script_is_noop(
            test_script,
            placeholder=re.compile(self.placeholder_pattern, re.IGNORECASE),
            real_runner=re.compile(self.real_runner_pattern),
        )

    def xǁNoNoopTestScriptsǁfile_has_violation__mutmut_16(self, path: Path) -> bool:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return True
        if not isinstance(data, Mapping):
            return True
        scripts = data.get("scripts")
        if scripts is not None and not isinstance(scripts, Mapping):
            return False
        test_script = (scripts or {}).get("test")
        if not isinstance(test_script, str):
            return False
        return script_is_noop(
            test_script,
            placeholder=re.compile(self.placeholder_pattern, re.IGNORECASE),
            real_runner=re.compile(self.real_runner_pattern),
        )

    def xǁNoNoopTestScriptsǁfile_has_violation__mutmut_17(self, path: Path) -> bool:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return True
        if not isinstance(data, Mapping):
            return True
        scripts = data.get("scripts")
        if scripts is not None and not isinstance(scripts, Mapping):
            return True
        test_script = None
        if not isinstance(test_script, str):
            return False
        return script_is_noop(
            test_script,
            placeholder=re.compile(self.placeholder_pattern, re.IGNORECASE),
            real_runner=re.compile(self.real_runner_pattern),
        )

    def xǁNoNoopTestScriptsǁfile_has_violation__mutmut_18(self, path: Path) -> bool:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return True
        if not isinstance(data, Mapping):
            return True
        scripts = data.get("scripts")
        if scripts is not None and not isinstance(scripts, Mapping):
            return True
        test_script = (scripts or {}).get(None)
        if not isinstance(test_script, str):
            return False
        return script_is_noop(
            test_script,
            placeholder=re.compile(self.placeholder_pattern, re.IGNORECASE),
            real_runner=re.compile(self.real_runner_pattern),
        )

    def xǁNoNoopTestScriptsǁfile_has_violation__mutmut_19(self, path: Path) -> bool:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return True
        if not isinstance(data, Mapping):
            return True
        scripts = data.get("scripts")
        if scripts is not None and not isinstance(scripts, Mapping):
            return True
        test_script = (scripts and {}).get("test")
        if not isinstance(test_script, str):
            return False
        return script_is_noop(
            test_script,
            placeholder=re.compile(self.placeholder_pattern, re.IGNORECASE),
            real_runner=re.compile(self.real_runner_pattern),
        )

    def xǁNoNoopTestScriptsǁfile_has_violation__mutmut_20(self, path: Path) -> bool:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return True
        if not isinstance(data, Mapping):
            return True
        scripts = data.get("scripts")
        if scripts is not None and not isinstance(scripts, Mapping):
            return True
        test_script = (scripts or {}).get("XXtestXX")
        if not isinstance(test_script, str):
            return False
        return script_is_noop(
            test_script,
            placeholder=re.compile(self.placeholder_pattern, re.IGNORECASE),
            real_runner=re.compile(self.real_runner_pattern),
        )

    def xǁNoNoopTestScriptsǁfile_has_violation__mutmut_21(self, path: Path) -> bool:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return True
        if not isinstance(data, Mapping):
            return True
        scripts = data.get("scripts")
        if scripts is not None and not isinstance(scripts, Mapping):
            return True
        test_script = (scripts or {}).get("TEST")
        if not isinstance(test_script, str):
            return False
        return script_is_noop(
            test_script,
            placeholder=re.compile(self.placeholder_pattern, re.IGNORECASE),
            real_runner=re.compile(self.real_runner_pattern),
        )

    def xǁNoNoopTestScriptsǁfile_has_violation__mutmut_22(self, path: Path) -> bool:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return True
        if not isinstance(data, Mapping):
            return True
        scripts = data.get("scripts")
        if scripts is not None and not isinstance(scripts, Mapping):
            return True
        test_script = (scripts or {}).get("test")
        if isinstance(test_script, str):
            return False
        return script_is_noop(
            test_script,
            placeholder=re.compile(self.placeholder_pattern, re.IGNORECASE),
            real_runner=re.compile(self.real_runner_pattern),
        )

    def xǁNoNoopTestScriptsǁfile_has_violation__mutmut_23(self, path: Path) -> bool:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return True
        if not isinstance(data, Mapping):
            return True
        scripts = data.get("scripts")
        if scripts is not None and not isinstance(scripts, Mapping):
            return True
        test_script = (scripts or {}).get("test")
        if not isinstance(test_script, str):
            return True
        return script_is_noop(
            test_script,
            placeholder=re.compile(self.placeholder_pattern, re.IGNORECASE),
            real_runner=re.compile(self.real_runner_pattern),
        )

    def xǁNoNoopTestScriptsǁfile_has_violation__mutmut_24(self, path: Path) -> bool:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return True
        if not isinstance(data, Mapping):
            return True
        scripts = data.get("scripts")
        if scripts is not None and not isinstance(scripts, Mapping):
            return True
        test_script = (scripts or {}).get("test")
        if not isinstance(test_script, str):
            return False
        return script_is_noop(
            None,
            placeholder=re.compile(self.placeholder_pattern, re.IGNORECASE),
            real_runner=re.compile(self.real_runner_pattern),
        )

    def xǁNoNoopTestScriptsǁfile_has_violation__mutmut_25(self, path: Path) -> bool:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return True
        if not isinstance(data, Mapping):
            return True
        scripts = data.get("scripts")
        if scripts is not None and not isinstance(scripts, Mapping):
            return True
        test_script = (scripts or {}).get("test")
        if not isinstance(test_script, str):
            return False
        return script_is_noop(
            test_script,
            placeholder=None,
            real_runner=re.compile(self.real_runner_pattern),
        )

    def xǁNoNoopTestScriptsǁfile_has_violation__mutmut_26(self, path: Path) -> bool:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return True
        if not isinstance(data, Mapping):
            return True
        scripts = data.get("scripts")
        if scripts is not None and not isinstance(scripts, Mapping):
            return True
        test_script = (scripts or {}).get("test")
        if not isinstance(test_script, str):
            return False
        return script_is_noop(
            test_script,
            placeholder=re.compile(self.placeholder_pattern, re.IGNORECASE),
            real_runner=None,
        )

    def xǁNoNoopTestScriptsǁfile_has_violation__mutmut_27(self, path: Path) -> bool:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return True
        if not isinstance(data, Mapping):
            return True
        scripts = data.get("scripts")
        if scripts is not None and not isinstance(scripts, Mapping):
            return True
        test_script = (scripts or {}).get("test")
        if not isinstance(test_script, str):
            return False
        return script_is_noop(
            placeholder=re.compile(self.placeholder_pattern, re.IGNORECASE),
            real_runner=re.compile(self.real_runner_pattern),
        )

    def xǁNoNoopTestScriptsǁfile_has_violation__mutmut_28(self, path: Path) -> bool:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return True
        if not isinstance(data, Mapping):
            return True
        scripts = data.get("scripts")
        if scripts is not None and not isinstance(scripts, Mapping):
            return True
        test_script = (scripts or {}).get("test")
        if not isinstance(test_script, str):
            return False
        return script_is_noop(
            test_script,
            real_runner=re.compile(self.real_runner_pattern),
        )

    def xǁNoNoopTestScriptsǁfile_has_violation__mutmut_29(self, path: Path) -> bool:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return True
        if not isinstance(data, Mapping):
            return True
        scripts = data.get("scripts")
        if scripts is not None and not isinstance(scripts, Mapping):
            return True
        test_script = (scripts or {}).get("test")
        if not isinstance(test_script, str):
            return False
        return script_is_noop(
            test_script,
            placeholder=re.compile(self.placeholder_pattern, re.IGNORECASE),
            )

    def xǁNoNoopTestScriptsǁfile_has_violation__mutmut_30(self, path: Path) -> bool:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return True
        if not isinstance(data, Mapping):
            return True
        scripts = data.get("scripts")
        if scripts is not None and not isinstance(scripts, Mapping):
            return True
        test_script = (scripts or {}).get("test")
        if not isinstance(test_script, str):
            return False
        return script_is_noop(
            test_script,
            placeholder=re.compile(None, re.IGNORECASE),
            real_runner=re.compile(self.real_runner_pattern),
        )

    def xǁNoNoopTestScriptsǁfile_has_violation__mutmut_31(self, path: Path) -> bool:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return True
        if not isinstance(data, Mapping):
            return True
        scripts = data.get("scripts")
        if scripts is not None and not isinstance(scripts, Mapping):
            return True
        test_script = (scripts or {}).get("test")
        if not isinstance(test_script, str):
            return False
        return script_is_noop(
            test_script,
            placeholder=re.compile(self.placeholder_pattern, None),
            real_runner=re.compile(self.real_runner_pattern),
        )

    def xǁNoNoopTestScriptsǁfile_has_violation__mutmut_32(self, path: Path) -> bool:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return True
        if not isinstance(data, Mapping):
            return True
        scripts = data.get("scripts")
        if scripts is not None and not isinstance(scripts, Mapping):
            return True
        test_script = (scripts or {}).get("test")
        if not isinstance(test_script, str):
            return False
        return script_is_noop(
            test_script,
            placeholder=re.compile(re.IGNORECASE),
            real_runner=re.compile(self.real_runner_pattern),
        )

    def xǁNoNoopTestScriptsǁfile_has_violation__mutmut_33(self, path: Path) -> bool:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return True
        if not isinstance(data, Mapping):
            return True
        scripts = data.get("scripts")
        if scripts is not None and not isinstance(scripts, Mapping):
            return True
        test_script = (scripts or {}).get("test")
        if not isinstance(test_script, str):
            return False
        return script_is_noop(
            test_script,
            placeholder=re.compile(self.placeholder_pattern, ),
            real_runner=re.compile(self.real_runner_pattern),
        )

    def xǁNoNoopTestScriptsǁfile_has_violation__mutmut_34(self, path: Path) -> bool:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return True
        if not isinstance(data, Mapping):
            return True
        scripts = data.get("scripts")
        if scripts is not None and not isinstance(scripts, Mapping):
            return True
        test_script = (scripts or {}).get("test")
        if not isinstance(test_script, str):
            return False
        return script_is_noop(
            test_script,
            placeholder=re.compile(self.placeholder_pattern, re.IGNORECASE),
            real_runner=re.compile(None),
        )

mutants_xǁNoNoopTestScriptsǁfrom_config__mutmut['_mutmut_orig'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfrom_config__mutmut['xǁNoNoopTestScriptsǁfrom_config__mutmut_1'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfrom_config__mutmut['xǁNoNoopTestScriptsǁfrom_config__mutmut_2'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfrom_config__mutmut['xǁNoNoopTestScriptsǁfrom_config__mutmut_3'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfrom_config__mutmut['xǁNoNoopTestScriptsǁfrom_config__mutmut_4'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfrom_config__mutmut['xǁNoNoopTestScriptsǁfrom_config__mutmut_5'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfrom_config__mutmut['xǁNoNoopTestScriptsǁfrom_config__mutmut_6'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfrom_config__mutmut['xǁNoNoopTestScriptsǁfrom_config__mutmut_7'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfrom_config__mutmut['xǁNoNoopTestScriptsǁfrom_config__mutmut_8'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfrom_config__mutmut['xǁNoNoopTestScriptsǁfrom_config__mutmut_9'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfrom_config__mutmut['xǁNoNoopTestScriptsǁfrom_config__mutmut_10'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfrom_config__mutmut['xǁNoNoopTestScriptsǁfrom_config__mutmut_11'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfrom_config__mutmut['xǁNoNoopTestScriptsǁfrom_config__mutmut_12'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfrom_config__mutmut_12 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfrom_config__mutmut['xǁNoNoopTestScriptsǁfrom_config__mutmut_13'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfrom_config__mutmut_13 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfrom_config__mutmut['xǁNoNoopTestScriptsǁfrom_config__mutmut_14'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfrom_config__mutmut_14 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfrom_config__mutmut['xǁNoNoopTestScriptsǁfrom_config__mutmut_15'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfrom_config__mutmut_15 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfrom_config__mutmut['xǁNoNoopTestScriptsǁfrom_config__mutmut_16'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfrom_config__mutmut_16 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfrom_config__mutmut['xǁNoNoopTestScriptsǁfrom_config__mutmut_17'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfrom_config__mutmut_17 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfrom_config__mutmut['xǁNoNoopTestScriptsǁfrom_config__mutmut_18'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfrom_config__mutmut_18 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfrom_config__mutmut['xǁNoNoopTestScriptsǁfrom_config__mutmut_19'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfrom_config__mutmut_19 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfrom_config__mutmut['xǁNoNoopTestScriptsǁfrom_config__mutmut_20'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfrom_config__mutmut_20 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfrom_config__mutmut['xǁNoNoopTestScriptsǁfrom_config__mutmut_21'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfrom_config__mutmut_21 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfrom_config__mutmut['xǁNoNoopTestScriptsǁfrom_config__mutmut_22'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfrom_config__mutmut_22 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfrom_config__mutmut['xǁNoNoopTestScriptsǁfrom_config__mutmut_23'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfrom_config__mutmut_23 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfrom_config__mutmut['xǁNoNoopTestScriptsǁfrom_config__mutmut_24'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfrom_config__mutmut_24 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfrom_config__mutmut['xǁNoNoopTestScriptsǁfrom_config__mutmut_25'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfrom_config__mutmut_25 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfrom_config__mutmut['xǁNoNoopTestScriptsǁfrom_config__mutmut_26'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfrom_config__mutmut_26 # type: ignore # mutmut generated

mutants_xǁNoNoopTestScriptsǁ_is_prod_manifest__mutmut['_mutmut_orig'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁ_is_prod_manifest__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁ_is_prod_manifest__mutmut['xǁNoNoopTestScriptsǁ_is_prod_manifest__mutmut_1'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁ_is_prod_manifest__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁ_is_prod_manifest__mutmut['xǁNoNoopTestScriptsǁ_is_prod_manifest__mutmut_2'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁ_is_prod_manifest__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁ_is_prod_manifest__mutmut['xǁNoNoopTestScriptsǁ_is_prod_manifest__mutmut_3'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁ_is_prod_manifest__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁ_is_prod_manifest__mutmut['xǁNoNoopTestScriptsǁ_is_prod_manifest__mutmut_4'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁ_is_prod_manifest__mutmut_4 # type: ignore # mutmut generated

mutants_xǁNoNoopTestScriptsǁenumerate_files__mutmut['_mutmut_orig'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁenumerate_files__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁenumerate_files__mutmut['xǁNoNoopTestScriptsǁenumerate_files__mutmut_1'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁenumerate_files__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁenumerate_files__mutmut['xǁNoNoopTestScriptsǁenumerate_files__mutmut_2'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁenumerate_files__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁenumerate_files__mutmut['xǁNoNoopTestScriptsǁenumerate_files__mutmut_3'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁenumerate_files__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁenumerate_files__mutmut['xǁNoNoopTestScriptsǁenumerate_files__mutmut_4'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁenumerate_files__mutmut_4 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁenumerate_files__mutmut['xǁNoNoopTestScriptsǁenumerate_files__mutmut_5'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁenumerate_files__mutmut_5 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁenumerate_files__mutmut['xǁNoNoopTestScriptsǁenumerate_files__mutmut_6'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁenumerate_files__mutmut_6 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁenumerate_files__mutmut['xǁNoNoopTestScriptsǁenumerate_files__mutmut_7'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁenumerate_files__mutmut_7 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁenumerate_files__mutmut['xǁNoNoopTestScriptsǁenumerate_files__mutmut_8'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁenumerate_files__mutmut_8 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁenumerate_files__mutmut['xǁNoNoopTestScriptsǁenumerate_files__mutmut_9'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁenumerate_files__mutmut_9 # type: ignore # mutmut generated

mutants_xǁNoNoopTestScriptsǁis_in_scope__mutmut['_mutmut_orig'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁis_in_scope__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁis_in_scope__mutmut['xǁNoNoopTestScriptsǁis_in_scope__mutmut_1'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁis_in_scope__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁis_in_scope__mutmut['xǁNoNoopTestScriptsǁis_in_scope__mutmut_2'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁis_in_scope__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁis_in_scope__mutmut['xǁNoNoopTestScriptsǁis_in_scope__mutmut_3'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁis_in_scope__mutmut_3 # type: ignore # mutmut generated

mutants_xǁNoNoopTestScriptsǁfile_has_violation__mutmut['_mutmut_orig'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfile_has_violation__mutmut['xǁNoNoopTestScriptsǁfile_has_violation__mutmut_1'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfile_has_violation__mutmut['xǁNoNoopTestScriptsǁfile_has_violation__mutmut_2'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfile_has_violation__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfile_has_violation__mutmut['xǁNoNoopTestScriptsǁfile_has_violation__mutmut_3'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfile_has_violation__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfile_has_violation__mutmut['xǁNoNoopTestScriptsǁfile_has_violation__mutmut_4'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfile_has_violation__mutmut_4 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfile_has_violation__mutmut['xǁNoNoopTestScriptsǁfile_has_violation__mutmut_5'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfile_has_violation__mutmut_5 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfile_has_violation__mutmut['xǁNoNoopTestScriptsǁfile_has_violation__mutmut_6'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfile_has_violation__mutmut_6 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfile_has_violation__mutmut['xǁNoNoopTestScriptsǁfile_has_violation__mutmut_7'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfile_has_violation__mutmut_7 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfile_has_violation__mutmut['xǁNoNoopTestScriptsǁfile_has_violation__mutmut_8'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfile_has_violation__mutmut_8 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfile_has_violation__mutmut['xǁNoNoopTestScriptsǁfile_has_violation__mutmut_9'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfile_has_violation__mutmut_9 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfile_has_violation__mutmut['xǁNoNoopTestScriptsǁfile_has_violation__mutmut_10'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfile_has_violation__mutmut_10 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfile_has_violation__mutmut['xǁNoNoopTestScriptsǁfile_has_violation__mutmut_11'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfile_has_violation__mutmut_11 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfile_has_violation__mutmut['xǁNoNoopTestScriptsǁfile_has_violation__mutmut_12'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfile_has_violation__mutmut_12 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfile_has_violation__mutmut['xǁNoNoopTestScriptsǁfile_has_violation__mutmut_13'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfile_has_violation__mutmut_13 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfile_has_violation__mutmut['xǁNoNoopTestScriptsǁfile_has_violation__mutmut_14'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfile_has_violation__mutmut_14 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfile_has_violation__mutmut['xǁNoNoopTestScriptsǁfile_has_violation__mutmut_15'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfile_has_violation__mutmut_15 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfile_has_violation__mutmut['xǁNoNoopTestScriptsǁfile_has_violation__mutmut_16'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfile_has_violation__mutmut_16 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfile_has_violation__mutmut['xǁNoNoopTestScriptsǁfile_has_violation__mutmut_17'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfile_has_violation__mutmut_17 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfile_has_violation__mutmut['xǁNoNoopTestScriptsǁfile_has_violation__mutmut_18'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfile_has_violation__mutmut_18 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfile_has_violation__mutmut['xǁNoNoopTestScriptsǁfile_has_violation__mutmut_19'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfile_has_violation__mutmut_19 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfile_has_violation__mutmut['xǁNoNoopTestScriptsǁfile_has_violation__mutmut_20'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfile_has_violation__mutmut_20 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfile_has_violation__mutmut['xǁNoNoopTestScriptsǁfile_has_violation__mutmut_21'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfile_has_violation__mutmut_21 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfile_has_violation__mutmut['xǁNoNoopTestScriptsǁfile_has_violation__mutmut_22'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfile_has_violation__mutmut_22 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfile_has_violation__mutmut['xǁNoNoopTestScriptsǁfile_has_violation__mutmut_23'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfile_has_violation__mutmut_23 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfile_has_violation__mutmut['xǁNoNoopTestScriptsǁfile_has_violation__mutmut_24'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfile_has_violation__mutmut_24 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfile_has_violation__mutmut['xǁNoNoopTestScriptsǁfile_has_violation__mutmut_25'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfile_has_violation__mutmut_25 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfile_has_violation__mutmut['xǁNoNoopTestScriptsǁfile_has_violation__mutmut_26'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfile_has_violation__mutmut_26 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfile_has_violation__mutmut['xǁNoNoopTestScriptsǁfile_has_violation__mutmut_27'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfile_has_violation__mutmut_27 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfile_has_violation__mutmut['xǁNoNoopTestScriptsǁfile_has_violation__mutmut_28'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfile_has_violation__mutmut_28 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfile_has_violation__mutmut['xǁNoNoopTestScriptsǁfile_has_violation__mutmut_29'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfile_has_violation__mutmut_29 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfile_has_violation__mutmut['xǁNoNoopTestScriptsǁfile_has_violation__mutmut_30'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfile_has_violation__mutmut_30 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfile_has_violation__mutmut['xǁNoNoopTestScriptsǁfile_has_violation__mutmut_31'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfile_has_violation__mutmut_31 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfile_has_violation__mutmut['xǁNoNoopTestScriptsǁfile_has_violation__mutmut_32'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfile_has_violation__mutmut_32 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfile_has_violation__mutmut['xǁNoNoopTestScriptsǁfile_has_violation__mutmut_33'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfile_has_violation__mutmut_33 # type: ignore # mutmut generated
mutants_xǁNoNoopTestScriptsǁfile_has_violation__mutmut['xǁNoNoopTestScriptsǁfile_has_violation__mutmut_34'] = NoNoopTestScripts.xǁNoNoopTestScriptsǁfile_has_violation__mutmut_34 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoNoopTestScripts:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoNoopTestScripts.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoNoopTestScripts:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoNoopTestScripts.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoNoopTestScripts:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoNoopTestScripts.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoNoopTestScripts:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoNoopTestScripts.from_config(config, repo_root=None)


def x_build__mutmut_3(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoNoopTestScripts:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoNoopTestScripts.from_config(repo_root=repo_root)


def x_build__mutmut_4(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoNoopTestScripts:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoNoopTestScripts.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoNoopTestScripts, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoNoopTestScripts, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoNoopTestScripts, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoNoopTestScripts, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
