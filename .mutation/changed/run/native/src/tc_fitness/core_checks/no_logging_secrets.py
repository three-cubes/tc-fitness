"""CORE check: no_logging_secrets — never log a secret-named value in plaintext.

A variable whose name strongly implies it holds a secret (``api_key``,
``token``, ``password``, ``client_secret``, ``bearer``, ``jwt``,
``private_key``) passed to a logging / print / exception sink without
redaction is a recurring incident class: boot-time credential reveals,
exception messages echoing the value to operators, debug prints left over
from an investigation. The cure is cheap (log ``token is not None`` or
``len(token)``); the cost of the leak is a credential rotation.

Ported from tc-agent-zone ``scripts/checks/no_logging_secrets.py`` (itself
kairix F15) and re-expressed as a configurable, repo-agnostic rule. The AST
detection is already domain-intrinsic; what was repo-specific (the scanned
source roots, the boundary modules that own redaction and are exempt) is now
consumer config. The secret-name patterns and sink surface ship as
domain-intrinsic defaults (the shape of "a secret reaching a log sink"), every
one overridable via ``[tool.tc_fitness]``.
"""

from __future__ import annotations

import ast
import re
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: Identifier patterns implying a secret value — matched against the trailing
#: segment of a Name/Attribute (``self.api_key`` -> ``api_key``). Domain-
#: intrinsic (the shape of a secret name), overridable via config.
DEFAULT_SECRET_PATTERNS: tuple[str, ...] = (
    r"^api_key$",
    r".*_api_key$",
    r"^token$",
    r".*_token$",
    r"^secret$",
    r".*_secret$",
    r"^password$",
    r".*_password$",
    r"^credential$|^credentials$",
    r".*_credentials?$",
    r"^bearer$",
    r"^jwt$",
    r".*_jwt$",
    r"^private_key$",
    r".*_private_key$",
)

#: Logger / sink method names (``logger.info`` / ``log.debug``). The receiver
#: is ignored, so renamed loggers are still caught.
DEFAULT_LOG_METHODS: frozenset[str] = frozenset(
    {"debug", "info", "warning", "warn", "error", "critical", "exception", "log"}
)

#: Direct function-call sinks.
DEFAULT_DIRECT_SINKS: frozenset[str] = frozenset({"print"})

# These builtins reduce a secret value to a non-reversible summary. Other
# one-argument calls remain conservatively treated as preserving the value.
_SAFE_SECRET_SUMMARIES = frozenset({"bool", "len"})

REMEDIATION = _remediation(
    fix=(
        "rewrite each flagged log/print/raise call so the secret-named value is "
        "summarised before it reaches the sink — pass `api_key is not None` (a "
        "bool), `len(token)` (an int), or a non-secret correlation key. If the "
        "call legitimately handles a secret, move it inside one of the configured "
        "redaction-boundary modules (the exempt_files)."
    ),
    nxt="re-run this check to confirm the gate goes green.",
    run="python -m tc_fitness.core_checks.no_logging_secrets",
    passing='logger.info("api_key present: %s", api_key is not None)',
    forbidden='logger.info("api key is %s", api_key)  # passes the raw secret',
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


def _trailing_name(node: ast.expr) -> str | None:
    """The trailing identifier of a Name/Attribute (``a.b.c`` -> ``c``)."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None
mutants_x__looks_like_secret__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__looks_like_secret__mutmut)
def _looks_like_secret(name: str, patterns: Sequence[re.Pattern[str]]) -> bool:
    return any(p.match(name) for p in patterns)


def x__looks_like_secret__mutmut_orig(name: str, patterns: Sequence[re.Pattern[str]]) -> bool:
    return any(p.match(name) for p in patterns)


def x__looks_like_secret__mutmut_1(name: str, patterns: Sequence[re.Pattern[str]]) -> bool:
    return any(None)


def x__looks_like_secret__mutmut_2(name: str, patterns: Sequence[re.Pattern[str]]) -> bool:
    return any(p.match(None) for p in patterns)

mutants_x__looks_like_secret__mutmut['_mutmut_orig'] = x__looks_like_secret__mutmut_orig # type: ignore # mutmut generated
mutants_x__looks_like_secret__mutmut['x__looks_like_secret__mutmut_1'] = x__looks_like_secret__mutmut_1 # type: ignore # mutmut generated
mutants_x__looks_like_secret__mutmut['x__looks_like_secret__mutmut_2'] = x__looks_like_secret__mutmut_2 # type: ignore # mutmut generated
mutants_x__arg_references_secret__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__arg_references_secret__mutmut)
def _arg_references_secret(arg: ast.expr, patterns: Sequence[re.Pattern[str]]) -> bool:
    """True iff ``arg`` exposes a secret-named identifier to a surrounding sink.

    Handles bare Names, Attributes, f-string interpolations
    (``JoinedStr -> FormattedValue``), and single-arg wrappers (``str(token)``).
    """
    leaf = _trailing_name(arg)
    if leaf is not None:
        return _looks_like_secret(leaf, patterns)
    if isinstance(arg, ast.JoinedStr):
        return any(
            isinstance(part, ast.FormattedValue) and _arg_references_secret(part.value, patterns)
            for part in arg.values
        )
    if isinstance(arg, ast.Call) and len(arg.args) == 1 and not arg.keywords:
        if isinstance(arg.func, ast.Name) and arg.func.id in _SAFE_SECRET_SUMMARIES:
            return False
        return _arg_references_secret(arg.args[0], patterns)
    return False


def x__arg_references_secret__mutmut_orig(arg: ast.expr, patterns: Sequence[re.Pattern[str]]) -> bool:
    """True iff ``arg`` exposes a secret-named identifier to a surrounding sink.

    Handles bare Names, Attributes, f-string interpolations
    (``JoinedStr -> FormattedValue``), and single-arg wrappers (``str(token)``).
    """
    leaf = _trailing_name(arg)
    if leaf is not None:
        return _looks_like_secret(leaf, patterns)
    if isinstance(arg, ast.JoinedStr):
        return any(
            isinstance(part, ast.FormattedValue) and _arg_references_secret(part.value, patterns)
            for part in arg.values
        )
    if isinstance(arg, ast.Call) and len(arg.args) == 1 and not arg.keywords:
        if isinstance(arg.func, ast.Name) and arg.func.id in _SAFE_SECRET_SUMMARIES:
            return False
        return _arg_references_secret(arg.args[0], patterns)
    return False


def x__arg_references_secret__mutmut_1(arg: ast.expr, patterns: Sequence[re.Pattern[str]]) -> bool:
    """True iff ``arg`` exposes a secret-named identifier to a surrounding sink.

    Handles bare Names, Attributes, f-string interpolations
    (``JoinedStr -> FormattedValue``), and single-arg wrappers (``str(token)``).
    """
    leaf = None
    if leaf is not None:
        return _looks_like_secret(leaf, patterns)
    if isinstance(arg, ast.JoinedStr):
        return any(
            isinstance(part, ast.FormattedValue) and _arg_references_secret(part.value, patterns)
            for part in arg.values
        )
    if isinstance(arg, ast.Call) and len(arg.args) == 1 and not arg.keywords:
        if isinstance(arg.func, ast.Name) and arg.func.id in _SAFE_SECRET_SUMMARIES:
            return False
        return _arg_references_secret(arg.args[0], patterns)
    return False


def x__arg_references_secret__mutmut_2(arg: ast.expr, patterns: Sequence[re.Pattern[str]]) -> bool:
    """True iff ``arg`` exposes a secret-named identifier to a surrounding sink.

    Handles bare Names, Attributes, f-string interpolations
    (``JoinedStr -> FormattedValue``), and single-arg wrappers (``str(token)``).
    """
    leaf = _trailing_name(None)
    if leaf is not None:
        return _looks_like_secret(leaf, patterns)
    if isinstance(arg, ast.JoinedStr):
        return any(
            isinstance(part, ast.FormattedValue) and _arg_references_secret(part.value, patterns)
            for part in arg.values
        )
    if isinstance(arg, ast.Call) and len(arg.args) == 1 and not arg.keywords:
        if isinstance(arg.func, ast.Name) and arg.func.id in _SAFE_SECRET_SUMMARIES:
            return False
        return _arg_references_secret(arg.args[0], patterns)
    return False


def x__arg_references_secret__mutmut_3(arg: ast.expr, patterns: Sequence[re.Pattern[str]]) -> bool:
    """True iff ``arg`` exposes a secret-named identifier to a surrounding sink.

    Handles bare Names, Attributes, f-string interpolations
    (``JoinedStr -> FormattedValue``), and single-arg wrappers (``str(token)``).
    """
    leaf = _trailing_name(arg)
    if leaf is None:
        return _looks_like_secret(leaf, patterns)
    if isinstance(arg, ast.JoinedStr):
        return any(
            isinstance(part, ast.FormattedValue) and _arg_references_secret(part.value, patterns)
            for part in arg.values
        )
    if isinstance(arg, ast.Call) and len(arg.args) == 1 and not arg.keywords:
        if isinstance(arg.func, ast.Name) and arg.func.id in _SAFE_SECRET_SUMMARIES:
            return False
        return _arg_references_secret(arg.args[0], patterns)
    return False


def x__arg_references_secret__mutmut_4(arg: ast.expr, patterns: Sequence[re.Pattern[str]]) -> bool:
    """True iff ``arg`` exposes a secret-named identifier to a surrounding sink.

    Handles bare Names, Attributes, f-string interpolations
    (``JoinedStr -> FormattedValue``), and single-arg wrappers (``str(token)``).
    """
    leaf = _trailing_name(arg)
    if leaf is not None:
        return _looks_like_secret(None, patterns)
    if isinstance(arg, ast.JoinedStr):
        return any(
            isinstance(part, ast.FormattedValue) and _arg_references_secret(part.value, patterns)
            for part in arg.values
        )
    if isinstance(arg, ast.Call) and len(arg.args) == 1 and not arg.keywords:
        if isinstance(arg.func, ast.Name) and arg.func.id in _SAFE_SECRET_SUMMARIES:
            return False
        return _arg_references_secret(arg.args[0], patterns)
    return False


def x__arg_references_secret__mutmut_5(arg: ast.expr, patterns: Sequence[re.Pattern[str]]) -> bool:
    """True iff ``arg`` exposes a secret-named identifier to a surrounding sink.

    Handles bare Names, Attributes, f-string interpolations
    (``JoinedStr -> FormattedValue``), and single-arg wrappers (``str(token)``).
    """
    leaf = _trailing_name(arg)
    if leaf is not None:
        return _looks_like_secret(leaf, None)
    if isinstance(arg, ast.JoinedStr):
        return any(
            isinstance(part, ast.FormattedValue) and _arg_references_secret(part.value, patterns)
            for part in arg.values
        )
    if isinstance(arg, ast.Call) and len(arg.args) == 1 and not arg.keywords:
        if isinstance(arg.func, ast.Name) and arg.func.id in _SAFE_SECRET_SUMMARIES:
            return False
        return _arg_references_secret(arg.args[0], patterns)
    return False


def x__arg_references_secret__mutmut_6(arg: ast.expr, patterns: Sequence[re.Pattern[str]]) -> bool:
    """True iff ``arg`` exposes a secret-named identifier to a surrounding sink.

    Handles bare Names, Attributes, f-string interpolations
    (``JoinedStr -> FormattedValue``), and single-arg wrappers (``str(token)``).
    """
    leaf = _trailing_name(arg)
    if leaf is not None:
        return _looks_like_secret(patterns)
    if isinstance(arg, ast.JoinedStr):
        return any(
            isinstance(part, ast.FormattedValue) and _arg_references_secret(part.value, patterns)
            for part in arg.values
        )
    if isinstance(arg, ast.Call) and len(arg.args) == 1 and not arg.keywords:
        if isinstance(arg.func, ast.Name) and arg.func.id in _SAFE_SECRET_SUMMARIES:
            return False
        return _arg_references_secret(arg.args[0], patterns)
    return False


def x__arg_references_secret__mutmut_7(arg: ast.expr, patterns: Sequence[re.Pattern[str]]) -> bool:
    """True iff ``arg`` exposes a secret-named identifier to a surrounding sink.

    Handles bare Names, Attributes, f-string interpolations
    (``JoinedStr -> FormattedValue``), and single-arg wrappers (``str(token)``).
    """
    leaf = _trailing_name(arg)
    if leaf is not None:
        return _looks_like_secret(leaf, )
    if isinstance(arg, ast.JoinedStr):
        return any(
            isinstance(part, ast.FormattedValue) and _arg_references_secret(part.value, patterns)
            for part in arg.values
        )
    if isinstance(arg, ast.Call) and len(arg.args) == 1 and not arg.keywords:
        if isinstance(arg.func, ast.Name) and arg.func.id in _SAFE_SECRET_SUMMARIES:
            return False
        return _arg_references_secret(arg.args[0], patterns)
    return False


def x__arg_references_secret__mutmut_8(arg: ast.expr, patterns: Sequence[re.Pattern[str]]) -> bool:
    """True iff ``arg`` exposes a secret-named identifier to a surrounding sink.

    Handles bare Names, Attributes, f-string interpolations
    (``JoinedStr -> FormattedValue``), and single-arg wrappers (``str(token)``).
    """
    leaf = _trailing_name(arg)
    if leaf is not None:
        return _looks_like_secret(leaf, patterns)
    if isinstance(arg, ast.JoinedStr):
        return any(
            None
        )
    if isinstance(arg, ast.Call) and len(arg.args) == 1 and not arg.keywords:
        if isinstance(arg.func, ast.Name) and arg.func.id in _SAFE_SECRET_SUMMARIES:
            return False
        return _arg_references_secret(arg.args[0], patterns)
    return False


def x__arg_references_secret__mutmut_9(arg: ast.expr, patterns: Sequence[re.Pattern[str]]) -> bool:
    """True iff ``arg`` exposes a secret-named identifier to a surrounding sink.

    Handles bare Names, Attributes, f-string interpolations
    (``JoinedStr -> FormattedValue``), and single-arg wrappers (``str(token)``).
    """
    leaf = _trailing_name(arg)
    if leaf is not None:
        return _looks_like_secret(leaf, patterns)
    if isinstance(arg, ast.JoinedStr):
        return any(
            isinstance(part, ast.FormattedValue) or _arg_references_secret(part.value, patterns)
            for part in arg.values
        )
    if isinstance(arg, ast.Call) and len(arg.args) == 1 and not arg.keywords:
        if isinstance(arg.func, ast.Name) and arg.func.id in _SAFE_SECRET_SUMMARIES:
            return False
        return _arg_references_secret(arg.args[0], patterns)
    return False


def x__arg_references_secret__mutmut_10(arg: ast.expr, patterns: Sequence[re.Pattern[str]]) -> bool:
    """True iff ``arg`` exposes a secret-named identifier to a surrounding sink.

    Handles bare Names, Attributes, f-string interpolations
    (``JoinedStr -> FormattedValue``), and single-arg wrappers (``str(token)``).
    """
    leaf = _trailing_name(arg)
    if leaf is not None:
        return _looks_like_secret(leaf, patterns)
    if isinstance(arg, ast.JoinedStr):
        return any(
            isinstance(part, ast.FormattedValue) and _arg_references_secret(None, patterns)
            for part in arg.values
        )
    if isinstance(arg, ast.Call) and len(arg.args) == 1 and not arg.keywords:
        if isinstance(arg.func, ast.Name) and arg.func.id in _SAFE_SECRET_SUMMARIES:
            return False
        return _arg_references_secret(arg.args[0], patterns)
    return False


def x__arg_references_secret__mutmut_11(arg: ast.expr, patterns: Sequence[re.Pattern[str]]) -> bool:
    """True iff ``arg`` exposes a secret-named identifier to a surrounding sink.

    Handles bare Names, Attributes, f-string interpolations
    (``JoinedStr -> FormattedValue``), and single-arg wrappers (``str(token)``).
    """
    leaf = _trailing_name(arg)
    if leaf is not None:
        return _looks_like_secret(leaf, patterns)
    if isinstance(arg, ast.JoinedStr):
        return any(
            isinstance(part, ast.FormattedValue) and _arg_references_secret(part.value, None)
            for part in arg.values
        )
    if isinstance(arg, ast.Call) and len(arg.args) == 1 and not arg.keywords:
        if isinstance(arg.func, ast.Name) and arg.func.id in _SAFE_SECRET_SUMMARIES:
            return False
        return _arg_references_secret(arg.args[0], patterns)
    return False


def x__arg_references_secret__mutmut_12(arg: ast.expr, patterns: Sequence[re.Pattern[str]]) -> bool:
    """True iff ``arg`` exposes a secret-named identifier to a surrounding sink.

    Handles bare Names, Attributes, f-string interpolations
    (``JoinedStr -> FormattedValue``), and single-arg wrappers (``str(token)``).
    """
    leaf = _trailing_name(arg)
    if leaf is not None:
        return _looks_like_secret(leaf, patterns)
    if isinstance(arg, ast.JoinedStr):
        return any(
            isinstance(part, ast.FormattedValue) and _arg_references_secret(patterns)
            for part in arg.values
        )
    if isinstance(arg, ast.Call) and len(arg.args) == 1 and not arg.keywords:
        if isinstance(arg.func, ast.Name) and arg.func.id in _SAFE_SECRET_SUMMARIES:
            return False
        return _arg_references_secret(arg.args[0], patterns)
    return False


def x__arg_references_secret__mutmut_13(arg: ast.expr, patterns: Sequence[re.Pattern[str]]) -> bool:
    """True iff ``arg`` exposes a secret-named identifier to a surrounding sink.

    Handles bare Names, Attributes, f-string interpolations
    (``JoinedStr -> FormattedValue``), and single-arg wrappers (``str(token)``).
    """
    leaf = _trailing_name(arg)
    if leaf is not None:
        return _looks_like_secret(leaf, patterns)
    if isinstance(arg, ast.JoinedStr):
        return any(
            isinstance(part, ast.FormattedValue) and _arg_references_secret(part.value, )
            for part in arg.values
        )
    if isinstance(arg, ast.Call) and len(arg.args) == 1 and not arg.keywords:
        if isinstance(arg.func, ast.Name) and arg.func.id in _SAFE_SECRET_SUMMARIES:
            return False
        return _arg_references_secret(arg.args[0], patterns)
    return False


def x__arg_references_secret__mutmut_14(arg: ast.expr, patterns: Sequence[re.Pattern[str]]) -> bool:
    """True iff ``arg`` exposes a secret-named identifier to a surrounding sink.

    Handles bare Names, Attributes, f-string interpolations
    (``JoinedStr -> FormattedValue``), and single-arg wrappers (``str(token)``).
    """
    leaf = _trailing_name(arg)
    if leaf is not None:
        return _looks_like_secret(leaf, patterns)
    if isinstance(arg, ast.JoinedStr):
        return any(
            isinstance(part, ast.FormattedValue) and _arg_references_secret(part.value, patterns)
            for part in arg.values
        )
    if isinstance(arg, ast.Call) and len(arg.args) == 1 or not arg.keywords:
        if isinstance(arg.func, ast.Name) and arg.func.id in _SAFE_SECRET_SUMMARIES:
            return False
        return _arg_references_secret(arg.args[0], patterns)
    return False


def x__arg_references_secret__mutmut_15(arg: ast.expr, patterns: Sequence[re.Pattern[str]]) -> bool:
    """True iff ``arg`` exposes a secret-named identifier to a surrounding sink.

    Handles bare Names, Attributes, f-string interpolations
    (``JoinedStr -> FormattedValue``), and single-arg wrappers (``str(token)``).
    """
    leaf = _trailing_name(arg)
    if leaf is not None:
        return _looks_like_secret(leaf, patterns)
    if isinstance(arg, ast.JoinedStr):
        return any(
            isinstance(part, ast.FormattedValue) and _arg_references_secret(part.value, patterns)
            for part in arg.values
        )
    if isinstance(arg, ast.Call) or len(arg.args) == 1 and not arg.keywords:
        if isinstance(arg.func, ast.Name) and arg.func.id in _SAFE_SECRET_SUMMARIES:
            return False
        return _arg_references_secret(arg.args[0], patterns)
    return False


def x__arg_references_secret__mutmut_16(arg: ast.expr, patterns: Sequence[re.Pattern[str]]) -> bool:
    """True iff ``arg`` exposes a secret-named identifier to a surrounding sink.

    Handles bare Names, Attributes, f-string interpolations
    (``JoinedStr -> FormattedValue``), and single-arg wrappers (``str(token)``).
    """
    leaf = _trailing_name(arg)
    if leaf is not None:
        return _looks_like_secret(leaf, patterns)
    if isinstance(arg, ast.JoinedStr):
        return any(
            isinstance(part, ast.FormattedValue) and _arg_references_secret(part.value, patterns)
            for part in arg.values
        )
    if isinstance(arg, ast.Call) and len(arg.args) != 1 and not arg.keywords:
        if isinstance(arg.func, ast.Name) and arg.func.id in _SAFE_SECRET_SUMMARIES:
            return False
        return _arg_references_secret(arg.args[0], patterns)
    return False


def x__arg_references_secret__mutmut_17(arg: ast.expr, patterns: Sequence[re.Pattern[str]]) -> bool:
    """True iff ``arg`` exposes a secret-named identifier to a surrounding sink.

    Handles bare Names, Attributes, f-string interpolations
    (``JoinedStr -> FormattedValue``), and single-arg wrappers (``str(token)``).
    """
    leaf = _trailing_name(arg)
    if leaf is not None:
        return _looks_like_secret(leaf, patterns)
    if isinstance(arg, ast.JoinedStr):
        return any(
            isinstance(part, ast.FormattedValue) and _arg_references_secret(part.value, patterns)
            for part in arg.values
        )
    if isinstance(arg, ast.Call) and len(arg.args) == 2 and not arg.keywords:
        if isinstance(arg.func, ast.Name) and arg.func.id in _SAFE_SECRET_SUMMARIES:
            return False
        return _arg_references_secret(arg.args[0], patterns)
    return False


def x__arg_references_secret__mutmut_18(arg: ast.expr, patterns: Sequence[re.Pattern[str]]) -> bool:
    """True iff ``arg`` exposes a secret-named identifier to a surrounding sink.

    Handles bare Names, Attributes, f-string interpolations
    (``JoinedStr -> FormattedValue``), and single-arg wrappers (``str(token)``).
    """
    leaf = _trailing_name(arg)
    if leaf is not None:
        return _looks_like_secret(leaf, patterns)
    if isinstance(arg, ast.JoinedStr):
        return any(
            isinstance(part, ast.FormattedValue) and _arg_references_secret(part.value, patterns)
            for part in arg.values
        )
    if isinstance(arg, ast.Call) and len(arg.args) == 1 and arg.keywords:
        if isinstance(arg.func, ast.Name) and arg.func.id in _SAFE_SECRET_SUMMARIES:
            return False
        return _arg_references_secret(arg.args[0], patterns)
    return False


def x__arg_references_secret__mutmut_19(arg: ast.expr, patterns: Sequence[re.Pattern[str]]) -> bool:
    """True iff ``arg`` exposes a secret-named identifier to a surrounding sink.

    Handles bare Names, Attributes, f-string interpolations
    (``JoinedStr -> FormattedValue``), and single-arg wrappers (``str(token)``).
    """
    leaf = _trailing_name(arg)
    if leaf is not None:
        return _looks_like_secret(leaf, patterns)
    if isinstance(arg, ast.JoinedStr):
        return any(
            isinstance(part, ast.FormattedValue) and _arg_references_secret(part.value, patterns)
            for part in arg.values
        )
    if isinstance(arg, ast.Call) and len(arg.args) == 1 and not arg.keywords:
        if isinstance(arg.func, ast.Name) or arg.func.id in _SAFE_SECRET_SUMMARIES:
            return False
        return _arg_references_secret(arg.args[0], patterns)
    return False


def x__arg_references_secret__mutmut_20(arg: ast.expr, patterns: Sequence[re.Pattern[str]]) -> bool:
    """True iff ``arg`` exposes a secret-named identifier to a surrounding sink.

    Handles bare Names, Attributes, f-string interpolations
    (``JoinedStr -> FormattedValue``), and single-arg wrappers (``str(token)``).
    """
    leaf = _trailing_name(arg)
    if leaf is not None:
        return _looks_like_secret(leaf, patterns)
    if isinstance(arg, ast.JoinedStr):
        return any(
            isinstance(part, ast.FormattedValue) and _arg_references_secret(part.value, patterns)
            for part in arg.values
        )
    if isinstance(arg, ast.Call) and len(arg.args) == 1 and not arg.keywords:
        if isinstance(arg.func, ast.Name) and arg.func.id not in _SAFE_SECRET_SUMMARIES:
            return False
        return _arg_references_secret(arg.args[0], patterns)
    return False


def x__arg_references_secret__mutmut_21(arg: ast.expr, patterns: Sequence[re.Pattern[str]]) -> bool:
    """True iff ``arg`` exposes a secret-named identifier to a surrounding sink.

    Handles bare Names, Attributes, f-string interpolations
    (``JoinedStr -> FormattedValue``), and single-arg wrappers (``str(token)``).
    """
    leaf = _trailing_name(arg)
    if leaf is not None:
        return _looks_like_secret(leaf, patterns)
    if isinstance(arg, ast.JoinedStr):
        return any(
            isinstance(part, ast.FormattedValue) and _arg_references_secret(part.value, patterns)
            for part in arg.values
        )
    if isinstance(arg, ast.Call) and len(arg.args) == 1 and not arg.keywords:
        if isinstance(arg.func, ast.Name) and arg.func.id in _SAFE_SECRET_SUMMARIES:
            return True
        return _arg_references_secret(arg.args[0], patterns)
    return False


def x__arg_references_secret__mutmut_22(arg: ast.expr, patterns: Sequence[re.Pattern[str]]) -> bool:
    """True iff ``arg`` exposes a secret-named identifier to a surrounding sink.

    Handles bare Names, Attributes, f-string interpolations
    (``JoinedStr -> FormattedValue``), and single-arg wrappers (``str(token)``).
    """
    leaf = _trailing_name(arg)
    if leaf is not None:
        return _looks_like_secret(leaf, patterns)
    if isinstance(arg, ast.JoinedStr):
        return any(
            isinstance(part, ast.FormattedValue) and _arg_references_secret(part.value, patterns)
            for part in arg.values
        )
    if isinstance(arg, ast.Call) and len(arg.args) == 1 and not arg.keywords:
        if isinstance(arg.func, ast.Name) and arg.func.id in _SAFE_SECRET_SUMMARIES:
            return False
        return _arg_references_secret(None, patterns)
    return False


def x__arg_references_secret__mutmut_23(arg: ast.expr, patterns: Sequence[re.Pattern[str]]) -> bool:
    """True iff ``arg`` exposes a secret-named identifier to a surrounding sink.

    Handles bare Names, Attributes, f-string interpolations
    (``JoinedStr -> FormattedValue``), and single-arg wrappers (``str(token)``).
    """
    leaf = _trailing_name(arg)
    if leaf is not None:
        return _looks_like_secret(leaf, patterns)
    if isinstance(arg, ast.JoinedStr):
        return any(
            isinstance(part, ast.FormattedValue) and _arg_references_secret(part.value, patterns)
            for part in arg.values
        )
    if isinstance(arg, ast.Call) and len(arg.args) == 1 and not arg.keywords:
        if isinstance(arg.func, ast.Name) and arg.func.id in _SAFE_SECRET_SUMMARIES:
            return False
        return _arg_references_secret(arg.args[0], None)
    return False


def x__arg_references_secret__mutmut_24(arg: ast.expr, patterns: Sequence[re.Pattern[str]]) -> bool:
    """True iff ``arg`` exposes a secret-named identifier to a surrounding sink.

    Handles bare Names, Attributes, f-string interpolations
    (``JoinedStr -> FormattedValue``), and single-arg wrappers (``str(token)``).
    """
    leaf = _trailing_name(arg)
    if leaf is not None:
        return _looks_like_secret(leaf, patterns)
    if isinstance(arg, ast.JoinedStr):
        return any(
            isinstance(part, ast.FormattedValue) and _arg_references_secret(part.value, patterns)
            for part in arg.values
        )
    if isinstance(arg, ast.Call) and len(arg.args) == 1 and not arg.keywords:
        if isinstance(arg.func, ast.Name) and arg.func.id in _SAFE_SECRET_SUMMARIES:
            return False
        return _arg_references_secret(patterns)
    return False


def x__arg_references_secret__mutmut_25(arg: ast.expr, patterns: Sequence[re.Pattern[str]]) -> bool:
    """True iff ``arg`` exposes a secret-named identifier to a surrounding sink.

    Handles bare Names, Attributes, f-string interpolations
    (``JoinedStr -> FormattedValue``), and single-arg wrappers (``str(token)``).
    """
    leaf = _trailing_name(arg)
    if leaf is not None:
        return _looks_like_secret(leaf, patterns)
    if isinstance(arg, ast.JoinedStr):
        return any(
            isinstance(part, ast.FormattedValue) and _arg_references_secret(part.value, patterns)
            for part in arg.values
        )
    if isinstance(arg, ast.Call) and len(arg.args) == 1 and not arg.keywords:
        if isinstance(arg.func, ast.Name) and arg.func.id in _SAFE_SECRET_SUMMARIES:
            return False
        return _arg_references_secret(arg.args[0], )
    return False


def x__arg_references_secret__mutmut_26(arg: ast.expr, patterns: Sequence[re.Pattern[str]]) -> bool:
    """True iff ``arg`` exposes a secret-named identifier to a surrounding sink.

    Handles bare Names, Attributes, f-string interpolations
    (``JoinedStr -> FormattedValue``), and single-arg wrappers (``str(token)``).
    """
    leaf = _trailing_name(arg)
    if leaf is not None:
        return _looks_like_secret(leaf, patterns)
    if isinstance(arg, ast.JoinedStr):
        return any(
            isinstance(part, ast.FormattedValue) and _arg_references_secret(part.value, patterns)
            for part in arg.values
        )
    if isinstance(arg, ast.Call) and len(arg.args) == 1 and not arg.keywords:
        if isinstance(arg.func, ast.Name) and arg.func.id in _SAFE_SECRET_SUMMARIES:
            return False
        return _arg_references_secret(arg.args[1], patterns)
    return False


def x__arg_references_secret__mutmut_27(arg: ast.expr, patterns: Sequence[re.Pattern[str]]) -> bool:
    """True iff ``arg`` exposes a secret-named identifier to a surrounding sink.

    Handles bare Names, Attributes, f-string interpolations
    (``JoinedStr -> FormattedValue``), and single-arg wrappers (``str(token)``).
    """
    leaf = _trailing_name(arg)
    if leaf is not None:
        return _looks_like_secret(leaf, patterns)
    if isinstance(arg, ast.JoinedStr):
        return any(
            isinstance(part, ast.FormattedValue) and _arg_references_secret(part.value, patterns)
            for part in arg.values
        )
    if isinstance(arg, ast.Call) and len(arg.args) == 1 and not arg.keywords:
        if isinstance(arg.func, ast.Name) and arg.func.id in _SAFE_SECRET_SUMMARIES:
            return False
        return _arg_references_secret(arg.args[0], patterns)
    return True

mutants_x__arg_references_secret__mutmut['_mutmut_orig'] = x__arg_references_secret__mutmut_orig # type: ignore # mutmut generated
mutants_x__arg_references_secret__mutmut['x__arg_references_secret__mutmut_1'] = x__arg_references_secret__mutmut_1 # type: ignore # mutmut generated
mutants_x__arg_references_secret__mutmut['x__arg_references_secret__mutmut_2'] = x__arg_references_secret__mutmut_2 # type: ignore # mutmut generated
mutants_x__arg_references_secret__mutmut['x__arg_references_secret__mutmut_3'] = x__arg_references_secret__mutmut_3 # type: ignore # mutmut generated
mutants_x__arg_references_secret__mutmut['x__arg_references_secret__mutmut_4'] = x__arg_references_secret__mutmut_4 # type: ignore # mutmut generated
mutants_x__arg_references_secret__mutmut['x__arg_references_secret__mutmut_5'] = x__arg_references_secret__mutmut_5 # type: ignore # mutmut generated
mutants_x__arg_references_secret__mutmut['x__arg_references_secret__mutmut_6'] = x__arg_references_secret__mutmut_6 # type: ignore # mutmut generated
mutants_x__arg_references_secret__mutmut['x__arg_references_secret__mutmut_7'] = x__arg_references_secret__mutmut_7 # type: ignore # mutmut generated
mutants_x__arg_references_secret__mutmut['x__arg_references_secret__mutmut_8'] = x__arg_references_secret__mutmut_8 # type: ignore # mutmut generated
mutants_x__arg_references_secret__mutmut['x__arg_references_secret__mutmut_9'] = x__arg_references_secret__mutmut_9 # type: ignore # mutmut generated
mutants_x__arg_references_secret__mutmut['x__arg_references_secret__mutmut_10'] = x__arg_references_secret__mutmut_10 # type: ignore # mutmut generated
mutants_x__arg_references_secret__mutmut['x__arg_references_secret__mutmut_11'] = x__arg_references_secret__mutmut_11 # type: ignore # mutmut generated
mutants_x__arg_references_secret__mutmut['x__arg_references_secret__mutmut_12'] = x__arg_references_secret__mutmut_12 # type: ignore # mutmut generated
mutants_x__arg_references_secret__mutmut['x__arg_references_secret__mutmut_13'] = x__arg_references_secret__mutmut_13 # type: ignore # mutmut generated
mutants_x__arg_references_secret__mutmut['x__arg_references_secret__mutmut_14'] = x__arg_references_secret__mutmut_14 # type: ignore # mutmut generated
mutants_x__arg_references_secret__mutmut['x__arg_references_secret__mutmut_15'] = x__arg_references_secret__mutmut_15 # type: ignore # mutmut generated
mutants_x__arg_references_secret__mutmut['x__arg_references_secret__mutmut_16'] = x__arg_references_secret__mutmut_16 # type: ignore # mutmut generated
mutants_x__arg_references_secret__mutmut['x__arg_references_secret__mutmut_17'] = x__arg_references_secret__mutmut_17 # type: ignore # mutmut generated
mutants_x__arg_references_secret__mutmut['x__arg_references_secret__mutmut_18'] = x__arg_references_secret__mutmut_18 # type: ignore # mutmut generated
mutants_x__arg_references_secret__mutmut['x__arg_references_secret__mutmut_19'] = x__arg_references_secret__mutmut_19 # type: ignore # mutmut generated
mutants_x__arg_references_secret__mutmut['x__arg_references_secret__mutmut_20'] = x__arg_references_secret__mutmut_20 # type: ignore # mutmut generated
mutants_x__arg_references_secret__mutmut['x__arg_references_secret__mutmut_21'] = x__arg_references_secret__mutmut_21 # type: ignore # mutmut generated
mutants_x__arg_references_secret__mutmut['x__arg_references_secret__mutmut_22'] = x__arg_references_secret__mutmut_22 # type: ignore # mutmut generated
mutants_x__arg_references_secret__mutmut['x__arg_references_secret__mutmut_23'] = x__arg_references_secret__mutmut_23 # type: ignore # mutmut generated
mutants_x__arg_references_secret__mutmut['x__arg_references_secret__mutmut_24'] = x__arg_references_secret__mutmut_24 # type: ignore # mutmut generated
mutants_x__arg_references_secret__mutmut['x__arg_references_secret__mutmut_25'] = x__arg_references_secret__mutmut_25 # type: ignore # mutmut generated
mutants_x__arg_references_secret__mutmut['x__arg_references_secret__mutmut_26'] = x__arg_references_secret__mutmut_26 # type: ignore # mutmut generated
mutants_x__arg_references_secret__mutmut['x__arg_references_secret__mutmut_27'] = x__arg_references_secret__mutmut_27 # type: ignore # mutmut generated
mutants_x__is_log_call__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__is_log_call__mutmut)
def _is_log_call(call: ast.Call, log_methods: frozenset[str]) -> bool:
    return isinstance(call.func, ast.Attribute) and call.func.attr in log_methods


def x__is_log_call__mutmut_orig(call: ast.Call, log_methods: frozenset[str]) -> bool:
    return isinstance(call.func, ast.Attribute) and call.func.attr in log_methods


def x__is_log_call__mutmut_1(call: ast.Call, log_methods: frozenset[str]) -> bool:
    return isinstance(call.func, ast.Attribute) or call.func.attr in log_methods


def x__is_log_call__mutmut_2(call: ast.Call, log_methods: frozenset[str]) -> bool:
    return isinstance(call.func, ast.Attribute) and call.func.attr not in log_methods

mutants_x__is_log_call__mutmut['_mutmut_orig'] = x__is_log_call__mutmut_orig # type: ignore # mutmut generated
mutants_x__is_log_call__mutmut['x__is_log_call__mutmut_1'] = x__is_log_call__mutmut_1 # type: ignore # mutmut generated
mutants_x__is_log_call__mutmut['x__is_log_call__mutmut_2'] = x__is_log_call__mutmut_2 # type: ignore # mutmut generated
mutants_x__is_direct_sink_call__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__is_direct_sink_call__mutmut)
def _is_direct_sink_call(call: ast.Call, direct_sinks: frozenset[str]) -> bool:
    if isinstance(call.func, ast.Name) and call.func.id in direct_sinks:
        return True
    if isinstance(call.func, ast.Attribute) and call.func.attr == "write":
        value = call.func.value
        if isinstance(value, ast.Attribute) and value.attr in {"stdout", "stderr"}:
            return True
    return False


def x__is_direct_sink_call__mutmut_orig(call: ast.Call, direct_sinks: frozenset[str]) -> bool:
    if isinstance(call.func, ast.Name) and call.func.id in direct_sinks:
        return True
    if isinstance(call.func, ast.Attribute) and call.func.attr == "write":
        value = call.func.value
        if isinstance(value, ast.Attribute) and value.attr in {"stdout", "stderr"}:
            return True
    return False


def x__is_direct_sink_call__mutmut_1(call: ast.Call, direct_sinks: frozenset[str]) -> bool:
    if isinstance(call.func, ast.Name) or call.func.id in direct_sinks:
        return True
    if isinstance(call.func, ast.Attribute) and call.func.attr == "write":
        value = call.func.value
        if isinstance(value, ast.Attribute) and value.attr in {"stdout", "stderr"}:
            return True
    return False


def x__is_direct_sink_call__mutmut_2(call: ast.Call, direct_sinks: frozenset[str]) -> bool:
    if isinstance(call.func, ast.Name) and call.func.id not in direct_sinks:
        return True
    if isinstance(call.func, ast.Attribute) and call.func.attr == "write":
        value = call.func.value
        if isinstance(value, ast.Attribute) and value.attr in {"stdout", "stderr"}:
            return True
    return False


def x__is_direct_sink_call__mutmut_3(call: ast.Call, direct_sinks: frozenset[str]) -> bool:
    if isinstance(call.func, ast.Name) and call.func.id in direct_sinks:
        return False
    if isinstance(call.func, ast.Attribute) and call.func.attr == "write":
        value = call.func.value
        if isinstance(value, ast.Attribute) and value.attr in {"stdout", "stderr"}:
            return True
    return False


def x__is_direct_sink_call__mutmut_4(call: ast.Call, direct_sinks: frozenset[str]) -> bool:
    if isinstance(call.func, ast.Name) and call.func.id in direct_sinks:
        return True
    if isinstance(call.func, ast.Attribute) or call.func.attr == "write":
        value = call.func.value
        if isinstance(value, ast.Attribute) and value.attr in {"stdout", "stderr"}:
            return True
    return False


def x__is_direct_sink_call__mutmut_5(call: ast.Call, direct_sinks: frozenset[str]) -> bool:
    if isinstance(call.func, ast.Name) and call.func.id in direct_sinks:
        return True
    if isinstance(call.func, ast.Attribute) and call.func.attr != "write":
        value = call.func.value
        if isinstance(value, ast.Attribute) and value.attr in {"stdout", "stderr"}:
            return True
    return False


def x__is_direct_sink_call__mutmut_6(call: ast.Call, direct_sinks: frozenset[str]) -> bool:
    if isinstance(call.func, ast.Name) and call.func.id in direct_sinks:
        return True
    if isinstance(call.func, ast.Attribute) and call.func.attr == "XXwriteXX":
        value = call.func.value
        if isinstance(value, ast.Attribute) and value.attr in {"stdout", "stderr"}:
            return True
    return False


def x__is_direct_sink_call__mutmut_7(call: ast.Call, direct_sinks: frozenset[str]) -> bool:
    if isinstance(call.func, ast.Name) and call.func.id in direct_sinks:
        return True
    if isinstance(call.func, ast.Attribute) and call.func.attr == "WRITE":
        value = call.func.value
        if isinstance(value, ast.Attribute) and value.attr in {"stdout", "stderr"}:
            return True
    return False


def x__is_direct_sink_call__mutmut_8(call: ast.Call, direct_sinks: frozenset[str]) -> bool:
    if isinstance(call.func, ast.Name) and call.func.id in direct_sinks:
        return True
    if isinstance(call.func, ast.Attribute) and call.func.attr == "write":
        value = None
        if isinstance(value, ast.Attribute) and value.attr in {"stdout", "stderr"}:
            return True
    return False


def x__is_direct_sink_call__mutmut_9(call: ast.Call, direct_sinks: frozenset[str]) -> bool:
    if isinstance(call.func, ast.Name) and call.func.id in direct_sinks:
        return True
    if isinstance(call.func, ast.Attribute) and call.func.attr == "write":
        value = call.func.value
        if isinstance(value, ast.Attribute) or value.attr in {"stdout", "stderr"}:
            return True
    return False


def x__is_direct_sink_call__mutmut_10(call: ast.Call, direct_sinks: frozenset[str]) -> bool:
    if isinstance(call.func, ast.Name) and call.func.id in direct_sinks:
        return True
    if isinstance(call.func, ast.Attribute) and call.func.attr == "write":
        value = call.func.value
        if isinstance(value, ast.Attribute) and value.attr not in {"stdout", "stderr"}:
            return True
    return False


def x__is_direct_sink_call__mutmut_11(call: ast.Call, direct_sinks: frozenset[str]) -> bool:
    if isinstance(call.func, ast.Name) and call.func.id in direct_sinks:
        return True
    if isinstance(call.func, ast.Attribute) and call.func.attr == "write":
        value = call.func.value
        if isinstance(value, ast.Attribute) and value.attr in {"XXstdoutXX", "stderr"}:
            return True
    return False


def x__is_direct_sink_call__mutmut_12(call: ast.Call, direct_sinks: frozenset[str]) -> bool:
    if isinstance(call.func, ast.Name) and call.func.id in direct_sinks:
        return True
    if isinstance(call.func, ast.Attribute) and call.func.attr == "write":
        value = call.func.value
        if isinstance(value, ast.Attribute) and value.attr in {"STDOUT", "stderr"}:
            return True
    return False


def x__is_direct_sink_call__mutmut_13(call: ast.Call, direct_sinks: frozenset[str]) -> bool:
    if isinstance(call.func, ast.Name) and call.func.id in direct_sinks:
        return True
    if isinstance(call.func, ast.Attribute) and call.func.attr == "write":
        value = call.func.value
        if isinstance(value, ast.Attribute) and value.attr in {"stdout", "XXstderrXX"}:
            return True
    return False


def x__is_direct_sink_call__mutmut_14(call: ast.Call, direct_sinks: frozenset[str]) -> bool:
    if isinstance(call.func, ast.Name) and call.func.id in direct_sinks:
        return True
    if isinstance(call.func, ast.Attribute) and call.func.attr == "write":
        value = call.func.value
        if isinstance(value, ast.Attribute) and value.attr in {"stdout", "STDERR"}:
            return True
    return False


def x__is_direct_sink_call__mutmut_15(call: ast.Call, direct_sinks: frozenset[str]) -> bool:
    if isinstance(call.func, ast.Name) and call.func.id in direct_sinks:
        return True
    if isinstance(call.func, ast.Attribute) and call.func.attr == "write":
        value = call.func.value
        if isinstance(value, ast.Attribute) and value.attr in {"stdout", "stderr"}:
            return False
    return False


def x__is_direct_sink_call__mutmut_16(call: ast.Call, direct_sinks: frozenset[str]) -> bool:
    if isinstance(call.func, ast.Name) and call.func.id in direct_sinks:
        return True
    if isinstance(call.func, ast.Attribute) and call.func.attr == "write":
        value = call.func.value
        if isinstance(value, ast.Attribute) and value.attr in {"stdout", "stderr"}:
            return True
    return True

mutants_x__is_direct_sink_call__mutmut['_mutmut_orig'] = x__is_direct_sink_call__mutmut_orig # type: ignore # mutmut generated
mutants_x__is_direct_sink_call__mutmut['x__is_direct_sink_call__mutmut_1'] = x__is_direct_sink_call__mutmut_1 # type: ignore # mutmut generated
mutants_x__is_direct_sink_call__mutmut['x__is_direct_sink_call__mutmut_2'] = x__is_direct_sink_call__mutmut_2 # type: ignore # mutmut generated
mutants_x__is_direct_sink_call__mutmut['x__is_direct_sink_call__mutmut_3'] = x__is_direct_sink_call__mutmut_3 # type: ignore # mutmut generated
mutants_x__is_direct_sink_call__mutmut['x__is_direct_sink_call__mutmut_4'] = x__is_direct_sink_call__mutmut_4 # type: ignore # mutmut generated
mutants_x__is_direct_sink_call__mutmut['x__is_direct_sink_call__mutmut_5'] = x__is_direct_sink_call__mutmut_5 # type: ignore # mutmut generated
mutants_x__is_direct_sink_call__mutmut['x__is_direct_sink_call__mutmut_6'] = x__is_direct_sink_call__mutmut_6 # type: ignore # mutmut generated
mutants_x__is_direct_sink_call__mutmut['x__is_direct_sink_call__mutmut_7'] = x__is_direct_sink_call__mutmut_7 # type: ignore # mutmut generated
mutants_x__is_direct_sink_call__mutmut['x__is_direct_sink_call__mutmut_8'] = x__is_direct_sink_call__mutmut_8 # type: ignore # mutmut generated
mutants_x__is_direct_sink_call__mutmut['x__is_direct_sink_call__mutmut_9'] = x__is_direct_sink_call__mutmut_9 # type: ignore # mutmut generated
mutants_x__is_direct_sink_call__mutmut['x__is_direct_sink_call__mutmut_10'] = x__is_direct_sink_call__mutmut_10 # type: ignore # mutmut generated
mutants_x__is_direct_sink_call__mutmut['x__is_direct_sink_call__mutmut_11'] = x__is_direct_sink_call__mutmut_11 # type: ignore # mutmut generated
mutants_x__is_direct_sink_call__mutmut['x__is_direct_sink_call__mutmut_12'] = x__is_direct_sink_call__mutmut_12 # type: ignore # mutmut generated
mutants_x__is_direct_sink_call__mutmut['x__is_direct_sink_call__mutmut_13'] = x__is_direct_sink_call__mutmut_13 # type: ignore # mutmut generated
mutants_x__is_direct_sink_call__mutmut['x__is_direct_sink_call__mutmut_14'] = x__is_direct_sink_call__mutmut_14 # type: ignore # mutmut generated
mutants_x__is_direct_sink_call__mutmut['x__is_direct_sink_call__mutmut_15'] = x__is_direct_sink_call__mutmut_15 # type: ignore # mutmut generated
mutants_x__is_direct_sink_call__mutmut['x__is_direct_sink_call__mutmut_16'] = x__is_direct_sink_call__mutmut_16 # type: ignore # mutmut generated
mutants_x__sink_call_leaks_secret__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__sink_call_leaks_secret__mutmut)
def _sink_call_leaks_secret(
    call: ast.Call,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    if not (_is_log_call(call, log_methods) or _is_direct_sink_call(call, direct_sinks)):
        return False
    if any(_arg_references_secret(a, patterns) for a in call.args):
        return True
    return any(kw.value is not None and _arg_references_secret(kw.value, patterns) for kw in call.keywords)


def x__sink_call_leaks_secret__mutmut_orig(
    call: ast.Call,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    if not (_is_log_call(call, log_methods) or _is_direct_sink_call(call, direct_sinks)):
        return False
    if any(_arg_references_secret(a, patterns) for a in call.args):
        return True
    return any(kw.value is not None and _arg_references_secret(kw.value, patterns) for kw in call.keywords)


def x__sink_call_leaks_secret__mutmut_1(
    call: ast.Call,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    if (_is_log_call(call, log_methods) or _is_direct_sink_call(call, direct_sinks)):
        return False
    if any(_arg_references_secret(a, patterns) for a in call.args):
        return True
    return any(kw.value is not None and _arg_references_secret(kw.value, patterns) for kw in call.keywords)


def x__sink_call_leaks_secret__mutmut_2(
    call: ast.Call,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    if not (_is_log_call(call, log_methods) and _is_direct_sink_call(call, direct_sinks)):
        return False
    if any(_arg_references_secret(a, patterns) for a in call.args):
        return True
    return any(kw.value is not None and _arg_references_secret(kw.value, patterns) for kw in call.keywords)


def x__sink_call_leaks_secret__mutmut_3(
    call: ast.Call,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    if not (_is_log_call(None, log_methods) or _is_direct_sink_call(call, direct_sinks)):
        return False
    if any(_arg_references_secret(a, patterns) for a in call.args):
        return True
    return any(kw.value is not None and _arg_references_secret(kw.value, patterns) for kw in call.keywords)


def x__sink_call_leaks_secret__mutmut_4(
    call: ast.Call,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    if not (_is_log_call(call, None) or _is_direct_sink_call(call, direct_sinks)):
        return False
    if any(_arg_references_secret(a, patterns) for a in call.args):
        return True
    return any(kw.value is not None and _arg_references_secret(kw.value, patterns) for kw in call.keywords)


def x__sink_call_leaks_secret__mutmut_5(
    call: ast.Call,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    if not (_is_log_call(log_methods) or _is_direct_sink_call(call, direct_sinks)):
        return False
    if any(_arg_references_secret(a, patterns) for a in call.args):
        return True
    return any(kw.value is not None and _arg_references_secret(kw.value, patterns) for kw in call.keywords)


def x__sink_call_leaks_secret__mutmut_6(
    call: ast.Call,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    if not (_is_log_call(call, ) or _is_direct_sink_call(call, direct_sinks)):
        return False
    if any(_arg_references_secret(a, patterns) for a in call.args):
        return True
    return any(kw.value is not None and _arg_references_secret(kw.value, patterns) for kw in call.keywords)


def x__sink_call_leaks_secret__mutmut_7(
    call: ast.Call,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    if not (_is_log_call(call, log_methods) or _is_direct_sink_call(None, direct_sinks)):
        return False
    if any(_arg_references_secret(a, patterns) for a in call.args):
        return True
    return any(kw.value is not None and _arg_references_secret(kw.value, patterns) for kw in call.keywords)


def x__sink_call_leaks_secret__mutmut_8(
    call: ast.Call,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    if not (_is_log_call(call, log_methods) or _is_direct_sink_call(call, None)):
        return False
    if any(_arg_references_secret(a, patterns) for a in call.args):
        return True
    return any(kw.value is not None and _arg_references_secret(kw.value, patterns) for kw in call.keywords)


def x__sink_call_leaks_secret__mutmut_9(
    call: ast.Call,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    if not (_is_log_call(call, log_methods) or _is_direct_sink_call(direct_sinks)):
        return False
    if any(_arg_references_secret(a, patterns) for a in call.args):
        return True
    return any(kw.value is not None and _arg_references_secret(kw.value, patterns) for kw in call.keywords)


def x__sink_call_leaks_secret__mutmut_10(
    call: ast.Call,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    if not (_is_log_call(call, log_methods) or _is_direct_sink_call(call, )):
        return False
    if any(_arg_references_secret(a, patterns) for a in call.args):
        return True
    return any(kw.value is not None and _arg_references_secret(kw.value, patterns) for kw in call.keywords)


def x__sink_call_leaks_secret__mutmut_11(
    call: ast.Call,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    if not (_is_log_call(call, log_methods) or _is_direct_sink_call(call, direct_sinks)):
        return True
    if any(_arg_references_secret(a, patterns) for a in call.args):
        return True
    return any(kw.value is not None and _arg_references_secret(kw.value, patterns) for kw in call.keywords)


def x__sink_call_leaks_secret__mutmut_12(
    call: ast.Call,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    if not (_is_log_call(call, log_methods) or _is_direct_sink_call(call, direct_sinks)):
        return False
    if any(None):
        return True
    return any(kw.value is not None and _arg_references_secret(kw.value, patterns) for kw in call.keywords)


def x__sink_call_leaks_secret__mutmut_13(
    call: ast.Call,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    if not (_is_log_call(call, log_methods) or _is_direct_sink_call(call, direct_sinks)):
        return False
    if any(_arg_references_secret(None, patterns) for a in call.args):
        return True
    return any(kw.value is not None and _arg_references_secret(kw.value, patterns) for kw in call.keywords)


def x__sink_call_leaks_secret__mutmut_14(
    call: ast.Call,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    if not (_is_log_call(call, log_methods) or _is_direct_sink_call(call, direct_sinks)):
        return False
    if any(_arg_references_secret(a, None) for a in call.args):
        return True
    return any(kw.value is not None and _arg_references_secret(kw.value, patterns) for kw in call.keywords)


def x__sink_call_leaks_secret__mutmut_15(
    call: ast.Call,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    if not (_is_log_call(call, log_methods) or _is_direct_sink_call(call, direct_sinks)):
        return False
    if any(_arg_references_secret(patterns) for a in call.args):
        return True
    return any(kw.value is not None and _arg_references_secret(kw.value, patterns) for kw in call.keywords)


def x__sink_call_leaks_secret__mutmut_16(
    call: ast.Call,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    if not (_is_log_call(call, log_methods) or _is_direct_sink_call(call, direct_sinks)):
        return False
    if any(_arg_references_secret(a, ) for a in call.args):
        return True
    return any(kw.value is not None and _arg_references_secret(kw.value, patterns) for kw in call.keywords)


def x__sink_call_leaks_secret__mutmut_17(
    call: ast.Call,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    if not (_is_log_call(call, log_methods) or _is_direct_sink_call(call, direct_sinks)):
        return False
    if any(_arg_references_secret(a, patterns) for a in call.args):
        return False
    return any(kw.value is not None and _arg_references_secret(kw.value, patterns) for kw in call.keywords)


def x__sink_call_leaks_secret__mutmut_18(
    call: ast.Call,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    if not (_is_log_call(call, log_methods) or _is_direct_sink_call(call, direct_sinks)):
        return False
    if any(_arg_references_secret(a, patterns) for a in call.args):
        return True
    return any(None)


def x__sink_call_leaks_secret__mutmut_19(
    call: ast.Call,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    if not (_is_log_call(call, log_methods) or _is_direct_sink_call(call, direct_sinks)):
        return False
    if any(_arg_references_secret(a, patterns) for a in call.args):
        return True
    return any(kw.value is not None or _arg_references_secret(kw.value, patterns) for kw in call.keywords)


def x__sink_call_leaks_secret__mutmut_20(
    call: ast.Call,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    if not (_is_log_call(call, log_methods) or _is_direct_sink_call(call, direct_sinks)):
        return False
    if any(_arg_references_secret(a, patterns) for a in call.args):
        return True
    return any(kw.value is None and _arg_references_secret(kw.value, patterns) for kw in call.keywords)


def x__sink_call_leaks_secret__mutmut_21(
    call: ast.Call,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    if not (_is_log_call(call, log_methods) or _is_direct_sink_call(call, direct_sinks)):
        return False
    if any(_arg_references_secret(a, patterns) for a in call.args):
        return True
    return any(kw.value is not None and _arg_references_secret(None, patterns) for kw in call.keywords)


def x__sink_call_leaks_secret__mutmut_22(
    call: ast.Call,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    if not (_is_log_call(call, log_methods) or _is_direct_sink_call(call, direct_sinks)):
        return False
    if any(_arg_references_secret(a, patterns) for a in call.args):
        return True
    return any(kw.value is not None and _arg_references_secret(kw.value, None) for kw in call.keywords)


def x__sink_call_leaks_secret__mutmut_23(
    call: ast.Call,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    if not (_is_log_call(call, log_methods) or _is_direct_sink_call(call, direct_sinks)):
        return False
    if any(_arg_references_secret(a, patterns) for a in call.args):
        return True
    return any(kw.value is not None and _arg_references_secret(patterns) for kw in call.keywords)


def x__sink_call_leaks_secret__mutmut_24(
    call: ast.Call,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    if not (_is_log_call(call, log_methods) or _is_direct_sink_call(call, direct_sinks)):
        return False
    if any(_arg_references_secret(a, patterns) for a in call.args):
        return True
    return any(kw.value is not None and _arg_references_secret(kw.value, ) for kw in call.keywords)

mutants_x__sink_call_leaks_secret__mutmut['_mutmut_orig'] = x__sink_call_leaks_secret__mutmut_orig # type: ignore # mutmut generated
mutants_x__sink_call_leaks_secret__mutmut['x__sink_call_leaks_secret__mutmut_1'] = x__sink_call_leaks_secret__mutmut_1 # type: ignore # mutmut generated
mutants_x__sink_call_leaks_secret__mutmut['x__sink_call_leaks_secret__mutmut_2'] = x__sink_call_leaks_secret__mutmut_2 # type: ignore # mutmut generated
mutants_x__sink_call_leaks_secret__mutmut['x__sink_call_leaks_secret__mutmut_3'] = x__sink_call_leaks_secret__mutmut_3 # type: ignore # mutmut generated
mutants_x__sink_call_leaks_secret__mutmut['x__sink_call_leaks_secret__mutmut_4'] = x__sink_call_leaks_secret__mutmut_4 # type: ignore # mutmut generated
mutants_x__sink_call_leaks_secret__mutmut['x__sink_call_leaks_secret__mutmut_5'] = x__sink_call_leaks_secret__mutmut_5 # type: ignore # mutmut generated
mutants_x__sink_call_leaks_secret__mutmut['x__sink_call_leaks_secret__mutmut_6'] = x__sink_call_leaks_secret__mutmut_6 # type: ignore # mutmut generated
mutants_x__sink_call_leaks_secret__mutmut['x__sink_call_leaks_secret__mutmut_7'] = x__sink_call_leaks_secret__mutmut_7 # type: ignore # mutmut generated
mutants_x__sink_call_leaks_secret__mutmut['x__sink_call_leaks_secret__mutmut_8'] = x__sink_call_leaks_secret__mutmut_8 # type: ignore # mutmut generated
mutants_x__sink_call_leaks_secret__mutmut['x__sink_call_leaks_secret__mutmut_9'] = x__sink_call_leaks_secret__mutmut_9 # type: ignore # mutmut generated
mutants_x__sink_call_leaks_secret__mutmut['x__sink_call_leaks_secret__mutmut_10'] = x__sink_call_leaks_secret__mutmut_10 # type: ignore # mutmut generated
mutants_x__sink_call_leaks_secret__mutmut['x__sink_call_leaks_secret__mutmut_11'] = x__sink_call_leaks_secret__mutmut_11 # type: ignore # mutmut generated
mutants_x__sink_call_leaks_secret__mutmut['x__sink_call_leaks_secret__mutmut_12'] = x__sink_call_leaks_secret__mutmut_12 # type: ignore # mutmut generated
mutants_x__sink_call_leaks_secret__mutmut['x__sink_call_leaks_secret__mutmut_13'] = x__sink_call_leaks_secret__mutmut_13 # type: ignore # mutmut generated
mutants_x__sink_call_leaks_secret__mutmut['x__sink_call_leaks_secret__mutmut_14'] = x__sink_call_leaks_secret__mutmut_14 # type: ignore # mutmut generated
mutants_x__sink_call_leaks_secret__mutmut['x__sink_call_leaks_secret__mutmut_15'] = x__sink_call_leaks_secret__mutmut_15 # type: ignore # mutmut generated
mutants_x__sink_call_leaks_secret__mutmut['x__sink_call_leaks_secret__mutmut_16'] = x__sink_call_leaks_secret__mutmut_16 # type: ignore # mutmut generated
mutants_x__sink_call_leaks_secret__mutmut['x__sink_call_leaks_secret__mutmut_17'] = x__sink_call_leaks_secret__mutmut_17 # type: ignore # mutmut generated
mutants_x__sink_call_leaks_secret__mutmut['x__sink_call_leaks_secret__mutmut_18'] = x__sink_call_leaks_secret__mutmut_18 # type: ignore # mutmut generated
mutants_x__sink_call_leaks_secret__mutmut['x__sink_call_leaks_secret__mutmut_19'] = x__sink_call_leaks_secret__mutmut_19 # type: ignore # mutmut generated
mutants_x__sink_call_leaks_secret__mutmut['x__sink_call_leaks_secret__mutmut_20'] = x__sink_call_leaks_secret__mutmut_20 # type: ignore # mutmut generated
mutants_x__sink_call_leaks_secret__mutmut['x__sink_call_leaks_secret__mutmut_21'] = x__sink_call_leaks_secret__mutmut_21 # type: ignore # mutmut generated
mutants_x__sink_call_leaks_secret__mutmut['x__sink_call_leaks_secret__mutmut_22'] = x__sink_call_leaks_secret__mutmut_22 # type: ignore # mutmut generated
mutants_x__sink_call_leaks_secret__mutmut['x__sink_call_leaks_secret__mutmut_23'] = x__sink_call_leaks_secret__mutmut_23 # type: ignore # mutmut generated
mutants_x__sink_call_leaks_secret__mutmut['x__sink_call_leaks_secret__mutmut_24'] = x__sink_call_leaks_secret__mutmut_24 # type: ignore # mutmut generated
mutants_x__raise_leaks_secret__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__raise_leaks_secret__mutmut)
def _raise_leaks_secret(node: ast.Raise, patterns: Sequence[re.Pattern[str]]) -> bool:
    if not isinstance(node.exc, ast.Call):
        return False
    return any(_arg_references_secret(a, patterns) for a in node.exc.args)


def x__raise_leaks_secret__mutmut_orig(node: ast.Raise, patterns: Sequence[re.Pattern[str]]) -> bool:
    if not isinstance(node.exc, ast.Call):
        return False
    return any(_arg_references_secret(a, patterns) for a in node.exc.args)


def x__raise_leaks_secret__mutmut_1(node: ast.Raise, patterns: Sequence[re.Pattern[str]]) -> bool:
    if isinstance(node.exc, ast.Call):
        return False
    return any(_arg_references_secret(a, patterns) for a in node.exc.args)


def x__raise_leaks_secret__mutmut_2(node: ast.Raise, patterns: Sequence[re.Pattern[str]]) -> bool:
    if not isinstance(node.exc, ast.Call):
        return True
    return any(_arg_references_secret(a, patterns) for a in node.exc.args)


def x__raise_leaks_secret__mutmut_3(node: ast.Raise, patterns: Sequence[re.Pattern[str]]) -> bool:
    if not isinstance(node.exc, ast.Call):
        return False
    return any(None)


def x__raise_leaks_secret__mutmut_4(node: ast.Raise, patterns: Sequence[re.Pattern[str]]) -> bool:
    if not isinstance(node.exc, ast.Call):
        return False
    return any(_arg_references_secret(None, patterns) for a in node.exc.args)


def x__raise_leaks_secret__mutmut_5(node: ast.Raise, patterns: Sequence[re.Pattern[str]]) -> bool:
    if not isinstance(node.exc, ast.Call):
        return False
    return any(_arg_references_secret(a, None) for a in node.exc.args)


def x__raise_leaks_secret__mutmut_6(node: ast.Raise, patterns: Sequence[re.Pattern[str]]) -> bool:
    if not isinstance(node.exc, ast.Call):
        return False
    return any(_arg_references_secret(patterns) for a in node.exc.args)


def x__raise_leaks_secret__mutmut_7(node: ast.Raise, patterns: Sequence[re.Pattern[str]]) -> bool:
    if not isinstance(node.exc, ast.Call):
        return False
    return any(_arg_references_secret(a, ) for a in node.exc.args)

mutants_x__raise_leaks_secret__mutmut['_mutmut_orig'] = x__raise_leaks_secret__mutmut_orig # type: ignore # mutmut generated
mutants_x__raise_leaks_secret__mutmut['x__raise_leaks_secret__mutmut_1'] = x__raise_leaks_secret__mutmut_1 # type: ignore # mutmut generated
mutants_x__raise_leaks_secret__mutmut['x__raise_leaks_secret__mutmut_2'] = x__raise_leaks_secret__mutmut_2 # type: ignore # mutmut generated
mutants_x__raise_leaks_secret__mutmut['x__raise_leaks_secret__mutmut_3'] = x__raise_leaks_secret__mutmut_3 # type: ignore # mutmut generated
mutants_x__raise_leaks_secret__mutmut['x__raise_leaks_secret__mutmut_4'] = x__raise_leaks_secret__mutmut_4 # type: ignore # mutmut generated
mutants_x__raise_leaks_secret__mutmut['x__raise_leaks_secret__mutmut_5'] = x__raise_leaks_secret__mutmut_5 # type: ignore # mutmut generated
mutants_x__raise_leaks_secret__mutmut['x__raise_leaks_secret__mutmut_6'] = x__raise_leaks_secret__mutmut_6 # type: ignore # mutmut generated
mutants_x__raise_leaks_secret__mutmut['x__raise_leaks_secret__mutmut_7'] = x__raise_leaks_secret__mutmut_7 # type: ignore # mutmut generated
mutants_x_module_logs_secret__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_module_logs_secret__mutmut)
def module_logs_secret(
    path: Path,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    """Pure detection helper: True iff any sink in ``path`` leaks a secret-named arg.

    A syntax / decode / read error is treated as "no violation" (another check
    owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _sink_call_leaks_secret(
            node, patterns=patterns, log_methods=log_methods, direct_sinks=direct_sinks
        ):
            return True
        if isinstance(node, ast.Raise) and _raise_leaks_secret(node, patterns):
            return True
    return False


def x_module_logs_secret__mutmut_orig(
    path: Path,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    """Pure detection helper: True iff any sink in ``path`` leaks a secret-named arg.

    A syntax / decode / read error is treated as "no violation" (another check
    owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _sink_call_leaks_secret(
            node, patterns=patterns, log_methods=log_methods, direct_sinks=direct_sinks
        ):
            return True
        if isinstance(node, ast.Raise) and _raise_leaks_secret(node, patterns):
            return True
    return False


def x_module_logs_secret__mutmut_1(
    path: Path,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    """Pure detection helper: True iff any sink in ``path`` leaks a secret-named arg.

    A syntax / decode / read error is treated as "no violation" (another check
    owns unparseable files).
    """
    try:
        tree = None
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _sink_call_leaks_secret(
            node, patterns=patterns, log_methods=log_methods, direct_sinks=direct_sinks
        ):
            return True
        if isinstance(node, ast.Raise) and _raise_leaks_secret(node, patterns):
            return True
    return False


def x_module_logs_secret__mutmut_2(
    path: Path,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    """Pure detection helper: True iff any sink in ``path`` leaks a secret-named arg.

    A syntax / decode / read error is treated as "no violation" (another check
    owns unparseable files).
    """
    try:
        tree = ast.parse(None, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _sink_call_leaks_secret(
            node, patterns=patterns, log_methods=log_methods, direct_sinks=direct_sinks
        ):
            return True
        if isinstance(node, ast.Raise) and _raise_leaks_secret(node, patterns):
            return True
    return False


def x_module_logs_secret__mutmut_3(
    path: Path,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    """Pure detection helper: True iff any sink in ``path`` leaks a secret-named arg.

    A syntax / decode / read error is treated as "no violation" (another check
    owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=None)
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _sink_call_leaks_secret(
            node, patterns=patterns, log_methods=log_methods, direct_sinks=direct_sinks
        ):
            return True
        if isinstance(node, ast.Raise) and _raise_leaks_secret(node, patterns):
            return True
    return False


def x_module_logs_secret__mutmut_4(
    path: Path,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    """Pure detection helper: True iff any sink in ``path`` leaks a secret-named arg.

    A syntax / decode / read error is treated as "no violation" (another check
    owns unparseable files).
    """
    try:
        tree = ast.parse(filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _sink_call_leaks_secret(
            node, patterns=patterns, log_methods=log_methods, direct_sinks=direct_sinks
        ):
            return True
        if isinstance(node, ast.Raise) and _raise_leaks_secret(node, patterns):
            return True
    return False


def x_module_logs_secret__mutmut_5(
    path: Path,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    """Pure detection helper: True iff any sink in ``path`` leaks a secret-named arg.

    A syntax / decode / read error is treated as "no violation" (another check
    owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), )
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _sink_call_leaks_secret(
            node, patterns=patterns, log_methods=log_methods, direct_sinks=direct_sinks
        ):
            return True
        if isinstance(node, ast.Raise) and _raise_leaks_secret(node, patterns):
            return True
    return False


def x_module_logs_secret__mutmut_6(
    path: Path,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    """Pure detection helper: True iff any sink in ``path`` leaks a secret-named arg.

    A syntax / decode / read error is treated as "no violation" (another check
    owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding=None), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _sink_call_leaks_secret(
            node, patterns=patterns, log_methods=log_methods, direct_sinks=direct_sinks
        ):
            return True
        if isinstance(node, ast.Raise) and _raise_leaks_secret(node, patterns):
            return True
    return False


def x_module_logs_secret__mutmut_7(
    path: Path,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    """Pure detection helper: True iff any sink in ``path`` leaks a secret-named arg.

    A syntax / decode / read error is treated as "no violation" (another check
    owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="XXutf-8XX"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _sink_call_leaks_secret(
            node, patterns=patterns, log_methods=log_methods, direct_sinks=direct_sinks
        ):
            return True
        if isinstance(node, ast.Raise) and _raise_leaks_secret(node, patterns):
            return True
    return False


def x_module_logs_secret__mutmut_8(
    path: Path,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    """Pure detection helper: True iff any sink in ``path`` leaks a secret-named arg.

    A syntax / decode / read error is treated as "no violation" (another check
    owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="UTF-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _sink_call_leaks_secret(
            node, patterns=patterns, log_methods=log_methods, direct_sinks=direct_sinks
        ):
            return True
        if isinstance(node, ast.Raise) and _raise_leaks_secret(node, patterns):
            return True
    return False


def x_module_logs_secret__mutmut_9(
    path: Path,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    """Pure detection helper: True iff any sink in ``path`` leaks a secret-named arg.

    A syntax / decode / read error is treated as "no violation" (another check
    owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(None))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _sink_call_leaks_secret(
            node, patterns=patterns, log_methods=log_methods, direct_sinks=direct_sinks
        ):
            return True
        if isinstance(node, ast.Raise) and _raise_leaks_secret(node, patterns):
            return True
    return False


def x_module_logs_secret__mutmut_10(
    path: Path,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    """Pure detection helper: True iff any sink in ``path`` leaks a secret-named arg.

    A syntax / decode / read error is treated as "no violation" (another check
    owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _sink_call_leaks_secret(
            node, patterns=patterns, log_methods=log_methods, direct_sinks=direct_sinks
        ):
            return True
        if isinstance(node, ast.Raise) and _raise_leaks_secret(node, patterns):
            return True
    return False


def x_module_logs_secret__mutmut_11(
    path: Path,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    """Pure detection helper: True iff any sink in ``path`` leaks a secret-named arg.

    A syntax / decode / read error is treated as "no violation" (another check
    owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(None):
        if isinstance(node, ast.Call) and _sink_call_leaks_secret(
            node, patterns=patterns, log_methods=log_methods, direct_sinks=direct_sinks
        ):
            return True
        if isinstance(node, ast.Raise) and _raise_leaks_secret(node, patterns):
            return True
    return False


def x_module_logs_secret__mutmut_12(
    path: Path,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    """Pure detection helper: True iff any sink in ``path`` leaks a secret-named arg.

    A syntax / decode / read error is treated as "no violation" (another check
    owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) or _sink_call_leaks_secret(
            node, patterns=patterns, log_methods=log_methods, direct_sinks=direct_sinks
        ):
            return True
        if isinstance(node, ast.Raise) and _raise_leaks_secret(node, patterns):
            return True
    return False


def x_module_logs_secret__mutmut_13(
    path: Path,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    """Pure detection helper: True iff any sink in ``path`` leaks a secret-named arg.

    A syntax / decode / read error is treated as "no violation" (another check
    owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _sink_call_leaks_secret(
            None, patterns=patterns, log_methods=log_methods, direct_sinks=direct_sinks
        ):
            return True
        if isinstance(node, ast.Raise) and _raise_leaks_secret(node, patterns):
            return True
    return False


def x_module_logs_secret__mutmut_14(
    path: Path,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    """Pure detection helper: True iff any sink in ``path`` leaks a secret-named arg.

    A syntax / decode / read error is treated as "no violation" (another check
    owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _sink_call_leaks_secret(
            node, patterns=None, log_methods=log_methods, direct_sinks=direct_sinks
        ):
            return True
        if isinstance(node, ast.Raise) and _raise_leaks_secret(node, patterns):
            return True
    return False


def x_module_logs_secret__mutmut_15(
    path: Path,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    """Pure detection helper: True iff any sink in ``path`` leaks a secret-named arg.

    A syntax / decode / read error is treated as "no violation" (another check
    owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _sink_call_leaks_secret(
            node, patterns=patterns, log_methods=None, direct_sinks=direct_sinks
        ):
            return True
        if isinstance(node, ast.Raise) and _raise_leaks_secret(node, patterns):
            return True
    return False


def x_module_logs_secret__mutmut_16(
    path: Path,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    """Pure detection helper: True iff any sink in ``path`` leaks a secret-named arg.

    A syntax / decode / read error is treated as "no violation" (another check
    owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _sink_call_leaks_secret(
            node, patterns=patterns, log_methods=log_methods, direct_sinks=None
        ):
            return True
        if isinstance(node, ast.Raise) and _raise_leaks_secret(node, patterns):
            return True
    return False


def x_module_logs_secret__mutmut_17(
    path: Path,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    """Pure detection helper: True iff any sink in ``path`` leaks a secret-named arg.

    A syntax / decode / read error is treated as "no violation" (another check
    owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _sink_call_leaks_secret(
            patterns=patterns, log_methods=log_methods, direct_sinks=direct_sinks
        ):
            return True
        if isinstance(node, ast.Raise) and _raise_leaks_secret(node, patterns):
            return True
    return False


def x_module_logs_secret__mutmut_18(
    path: Path,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    """Pure detection helper: True iff any sink in ``path`` leaks a secret-named arg.

    A syntax / decode / read error is treated as "no violation" (another check
    owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _sink_call_leaks_secret(
            node, log_methods=log_methods, direct_sinks=direct_sinks
        ):
            return True
        if isinstance(node, ast.Raise) and _raise_leaks_secret(node, patterns):
            return True
    return False


def x_module_logs_secret__mutmut_19(
    path: Path,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    """Pure detection helper: True iff any sink in ``path`` leaks a secret-named arg.

    A syntax / decode / read error is treated as "no violation" (another check
    owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _sink_call_leaks_secret(
            node, patterns=patterns, direct_sinks=direct_sinks
        ):
            return True
        if isinstance(node, ast.Raise) and _raise_leaks_secret(node, patterns):
            return True
    return False


def x_module_logs_secret__mutmut_20(
    path: Path,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    """Pure detection helper: True iff any sink in ``path`` leaks a secret-named arg.

    A syntax / decode / read error is treated as "no violation" (another check
    owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _sink_call_leaks_secret(
            node, patterns=patterns, log_methods=log_methods, ):
            return True
        if isinstance(node, ast.Raise) and _raise_leaks_secret(node, patterns):
            return True
    return False


def x_module_logs_secret__mutmut_21(
    path: Path,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    """Pure detection helper: True iff any sink in ``path`` leaks a secret-named arg.

    A syntax / decode / read error is treated as "no violation" (another check
    owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _sink_call_leaks_secret(
            node, patterns=patterns, log_methods=log_methods, direct_sinks=direct_sinks
        ):
            return False
        if isinstance(node, ast.Raise) and _raise_leaks_secret(node, patterns):
            return True
    return False


def x_module_logs_secret__mutmut_22(
    path: Path,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    """Pure detection helper: True iff any sink in ``path`` leaks a secret-named arg.

    A syntax / decode / read error is treated as "no violation" (another check
    owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _sink_call_leaks_secret(
            node, patterns=patterns, log_methods=log_methods, direct_sinks=direct_sinks
        ):
            return True
        if isinstance(node, ast.Raise) or _raise_leaks_secret(node, patterns):
            return True
    return False


def x_module_logs_secret__mutmut_23(
    path: Path,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    """Pure detection helper: True iff any sink in ``path`` leaks a secret-named arg.

    A syntax / decode / read error is treated as "no violation" (another check
    owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _sink_call_leaks_secret(
            node, patterns=patterns, log_methods=log_methods, direct_sinks=direct_sinks
        ):
            return True
        if isinstance(node, ast.Raise) and _raise_leaks_secret(None, patterns):
            return True
    return False


def x_module_logs_secret__mutmut_24(
    path: Path,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    """Pure detection helper: True iff any sink in ``path`` leaks a secret-named arg.

    A syntax / decode / read error is treated as "no violation" (another check
    owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _sink_call_leaks_secret(
            node, patterns=patterns, log_methods=log_methods, direct_sinks=direct_sinks
        ):
            return True
        if isinstance(node, ast.Raise) and _raise_leaks_secret(node, None):
            return True
    return False


def x_module_logs_secret__mutmut_25(
    path: Path,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    """Pure detection helper: True iff any sink in ``path`` leaks a secret-named arg.

    A syntax / decode / read error is treated as "no violation" (another check
    owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _sink_call_leaks_secret(
            node, patterns=patterns, log_methods=log_methods, direct_sinks=direct_sinks
        ):
            return True
        if isinstance(node, ast.Raise) and _raise_leaks_secret(patterns):
            return True
    return False


def x_module_logs_secret__mutmut_26(
    path: Path,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    """Pure detection helper: True iff any sink in ``path`` leaks a secret-named arg.

    A syntax / decode / read error is treated as "no violation" (another check
    owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _sink_call_leaks_secret(
            node, patterns=patterns, log_methods=log_methods, direct_sinks=direct_sinks
        ):
            return True
        if isinstance(node, ast.Raise) and _raise_leaks_secret(node, ):
            return True
    return False


def x_module_logs_secret__mutmut_27(
    path: Path,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    """Pure detection helper: True iff any sink in ``path`` leaks a secret-named arg.

    A syntax / decode / read error is treated as "no violation" (another check
    owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _sink_call_leaks_secret(
            node, patterns=patterns, log_methods=log_methods, direct_sinks=direct_sinks
        ):
            return True
        if isinstance(node, ast.Raise) and _raise_leaks_secret(node, patterns):
            return False
    return False


def x_module_logs_secret__mutmut_28(
    path: Path,
    *,
    patterns: Sequence[re.Pattern[str]],
    log_methods: frozenset[str],
    direct_sinks: frozenset[str],
) -> bool:
    """Pure detection helper: True iff any sink in ``path`` leaks a secret-named arg.

    A syntax / decode / read error is treated as "no violation" (another check
    owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _sink_call_leaks_secret(
            node, patterns=patterns, log_methods=log_methods, direct_sinks=direct_sinks
        ):
            return True
        if isinstance(node, ast.Raise) and _raise_leaks_secret(node, patterns):
            return True
    return True

mutants_x_module_logs_secret__mutmut['_mutmut_orig'] = x_module_logs_secret__mutmut_orig # type: ignore # mutmut generated
mutants_x_module_logs_secret__mutmut['x_module_logs_secret__mutmut_1'] = x_module_logs_secret__mutmut_1 # type: ignore # mutmut generated
mutants_x_module_logs_secret__mutmut['x_module_logs_secret__mutmut_2'] = x_module_logs_secret__mutmut_2 # type: ignore # mutmut generated
mutants_x_module_logs_secret__mutmut['x_module_logs_secret__mutmut_3'] = x_module_logs_secret__mutmut_3 # type: ignore # mutmut generated
mutants_x_module_logs_secret__mutmut['x_module_logs_secret__mutmut_4'] = x_module_logs_secret__mutmut_4 # type: ignore # mutmut generated
mutants_x_module_logs_secret__mutmut['x_module_logs_secret__mutmut_5'] = x_module_logs_secret__mutmut_5 # type: ignore # mutmut generated
mutants_x_module_logs_secret__mutmut['x_module_logs_secret__mutmut_6'] = x_module_logs_secret__mutmut_6 # type: ignore # mutmut generated
mutants_x_module_logs_secret__mutmut['x_module_logs_secret__mutmut_7'] = x_module_logs_secret__mutmut_7 # type: ignore # mutmut generated
mutants_x_module_logs_secret__mutmut['x_module_logs_secret__mutmut_8'] = x_module_logs_secret__mutmut_8 # type: ignore # mutmut generated
mutants_x_module_logs_secret__mutmut['x_module_logs_secret__mutmut_9'] = x_module_logs_secret__mutmut_9 # type: ignore # mutmut generated
mutants_x_module_logs_secret__mutmut['x_module_logs_secret__mutmut_10'] = x_module_logs_secret__mutmut_10 # type: ignore # mutmut generated
mutants_x_module_logs_secret__mutmut['x_module_logs_secret__mutmut_11'] = x_module_logs_secret__mutmut_11 # type: ignore # mutmut generated
mutants_x_module_logs_secret__mutmut['x_module_logs_secret__mutmut_12'] = x_module_logs_secret__mutmut_12 # type: ignore # mutmut generated
mutants_x_module_logs_secret__mutmut['x_module_logs_secret__mutmut_13'] = x_module_logs_secret__mutmut_13 # type: ignore # mutmut generated
mutants_x_module_logs_secret__mutmut['x_module_logs_secret__mutmut_14'] = x_module_logs_secret__mutmut_14 # type: ignore # mutmut generated
mutants_x_module_logs_secret__mutmut['x_module_logs_secret__mutmut_15'] = x_module_logs_secret__mutmut_15 # type: ignore # mutmut generated
mutants_x_module_logs_secret__mutmut['x_module_logs_secret__mutmut_16'] = x_module_logs_secret__mutmut_16 # type: ignore # mutmut generated
mutants_x_module_logs_secret__mutmut['x_module_logs_secret__mutmut_17'] = x_module_logs_secret__mutmut_17 # type: ignore # mutmut generated
mutants_x_module_logs_secret__mutmut['x_module_logs_secret__mutmut_18'] = x_module_logs_secret__mutmut_18 # type: ignore # mutmut generated
mutants_x_module_logs_secret__mutmut['x_module_logs_secret__mutmut_19'] = x_module_logs_secret__mutmut_19 # type: ignore # mutmut generated
mutants_x_module_logs_secret__mutmut['x_module_logs_secret__mutmut_20'] = x_module_logs_secret__mutmut_20 # type: ignore # mutmut generated
mutants_x_module_logs_secret__mutmut['x_module_logs_secret__mutmut_21'] = x_module_logs_secret__mutmut_21 # type: ignore # mutmut generated
mutants_x_module_logs_secret__mutmut['x_module_logs_secret__mutmut_22'] = x_module_logs_secret__mutmut_22 # type: ignore # mutmut generated
mutants_x_module_logs_secret__mutmut['x_module_logs_secret__mutmut_23'] = x_module_logs_secret__mutmut_23 # type: ignore # mutmut generated
mutants_x_module_logs_secret__mutmut['x_module_logs_secret__mutmut_24'] = x_module_logs_secret__mutmut_24 # type: ignore # mutmut generated
mutants_x_module_logs_secret__mutmut['x_module_logs_secret__mutmut_25'] = x_module_logs_secret__mutmut_25 # type: ignore # mutmut generated
mutants_x_module_logs_secret__mutmut['x_module_logs_secret__mutmut_26'] = x_module_logs_secret__mutmut_26 # type: ignore # mutmut generated
mutants_x_module_logs_secret__mutmut['x_module_logs_secret__mutmut_27'] = x_module_logs_secret__mutmut_27 # type: ignore # mutmut generated
mutants_x_module_logs_secret__mutmut['x_module_logs_secret__mutmut_28'] = x_module_logs_secret__mutmut_28 # type: ignore # mutmut generated
mutants_xǁNoLoggingSecretsǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁNoLoggingSecretsǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore


class NoLoggingSecrets(FitnessRule):
    """Flags modules that pass a secret-named value to a log / print / raise sink."""

    name = "no-logging-secrets"
    remediation = REMEDIATION
    extensions = (".py",)

    #: Rule-specific config (instance attrs; from_config overrides per consumer).
    secret_patterns: tuple[re.Pattern[str], ...] = tuple(
        re.compile(pattern) for pattern in DEFAULT_SECRET_PATTERNS
    )
    log_methods: frozenset[str] = DEFAULT_LOG_METHODS
    direct_sinks: frozenset[str] = DEFAULT_DIRECT_SINKS

    @classmethod
    @_mutmut_mutated(mutants_xǁNoLoggingSecretsǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLoggingSecrets:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLoggingSecrets)  # noqa: S101  # narrowing for mypy
        raw_patterns = config.get("secret_patterns", DEFAULT_SECRET_PATTERNS)
        rule.secret_patterns = tuple(re.compile(p) for p in raw_patterns)
        log_methods = config.get("log_methods")
        if log_methods is not None:
            rule.log_methods = frozenset(log_methods)
        direct_sinks = config.get("direct_sinks")
        if direct_sinks is not None:
            rule.direct_sinks = frozenset(direct_sinks)
        return rule

    @classmethod
    def xǁNoLoggingSecretsǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLoggingSecrets:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLoggingSecrets)  # noqa: S101  # narrowing for mypy
        raw_patterns = config.get("secret_patterns", DEFAULT_SECRET_PATTERNS)
        rule.secret_patterns = tuple(re.compile(p) for p in raw_patterns)
        log_methods = config.get("log_methods")
        if log_methods is not None:
            rule.log_methods = frozenset(log_methods)
        direct_sinks = config.get("direct_sinks")
        if direct_sinks is not None:
            rule.direct_sinks = frozenset(direct_sinks)
        return rule

    @classmethod
    def xǁNoLoggingSecretsǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLoggingSecrets:
        rule = None
        assert isinstance(rule, NoLoggingSecrets)  # noqa: S101  # narrowing for mypy
        raw_patterns = config.get("secret_patterns", DEFAULT_SECRET_PATTERNS)
        rule.secret_patterns = tuple(re.compile(p) for p in raw_patterns)
        log_methods = config.get("log_methods")
        if log_methods is not None:
            rule.log_methods = frozenset(log_methods)
        direct_sinks = config.get("direct_sinks")
        if direct_sinks is not None:
            rule.direct_sinks = frozenset(direct_sinks)
        return rule

    @classmethod
    def xǁNoLoggingSecretsǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLoggingSecrets:
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, NoLoggingSecrets)  # noqa: S101  # narrowing for mypy
        raw_patterns = config.get("secret_patterns", DEFAULT_SECRET_PATTERNS)
        rule.secret_patterns = tuple(re.compile(p) for p in raw_patterns)
        log_methods = config.get("log_methods")
        if log_methods is not None:
            rule.log_methods = frozenset(log_methods)
        direct_sinks = config.get("direct_sinks")
        if direct_sinks is not None:
            rule.direct_sinks = frozenset(direct_sinks)
        return rule

    @classmethod
    def xǁNoLoggingSecretsǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLoggingSecrets:
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, NoLoggingSecrets)  # noqa: S101  # narrowing for mypy
        raw_patterns = config.get("secret_patterns", DEFAULT_SECRET_PATTERNS)
        rule.secret_patterns = tuple(re.compile(p) for p in raw_patterns)
        log_methods = config.get("log_methods")
        if log_methods is not None:
            rule.log_methods = frozenset(log_methods)
        direct_sinks = config.get("direct_sinks")
        if direct_sinks is not None:
            rule.direct_sinks = frozenset(direct_sinks)
        return rule

    @classmethod
    def xǁNoLoggingSecretsǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLoggingSecrets:
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, NoLoggingSecrets)  # noqa: S101  # narrowing for mypy
        raw_patterns = config.get("secret_patterns", DEFAULT_SECRET_PATTERNS)
        rule.secret_patterns = tuple(re.compile(p) for p in raw_patterns)
        log_methods = config.get("log_methods")
        if log_methods is not None:
            rule.log_methods = frozenset(log_methods)
        direct_sinks = config.get("direct_sinks")
        if direct_sinks is not None:
            rule.direct_sinks = frozenset(direct_sinks)
        return rule

    @classmethod
    def xǁNoLoggingSecretsǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLoggingSecrets:
        rule = super().from_config(config, )
        assert isinstance(rule, NoLoggingSecrets)  # noqa: S101  # narrowing for mypy
        raw_patterns = config.get("secret_patterns", DEFAULT_SECRET_PATTERNS)
        rule.secret_patterns = tuple(re.compile(p) for p in raw_patterns)
        log_methods = config.get("log_methods")
        if log_methods is not None:
            rule.log_methods = frozenset(log_methods)
        direct_sinks = config.get("direct_sinks")
        if direct_sinks is not None:
            rule.direct_sinks = frozenset(direct_sinks)
        return rule

    @classmethod
    def xǁNoLoggingSecretsǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLoggingSecrets:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLoggingSecrets)  # noqa: S101  # narrowing for mypy
        raw_patterns = None
        rule.secret_patterns = tuple(re.compile(p) for p in raw_patterns)
        log_methods = config.get("log_methods")
        if log_methods is not None:
            rule.log_methods = frozenset(log_methods)
        direct_sinks = config.get("direct_sinks")
        if direct_sinks is not None:
            rule.direct_sinks = frozenset(direct_sinks)
        return rule

    @classmethod
    def xǁNoLoggingSecretsǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLoggingSecrets:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLoggingSecrets)  # noqa: S101  # narrowing for mypy
        raw_patterns = config.get(None, DEFAULT_SECRET_PATTERNS)
        rule.secret_patterns = tuple(re.compile(p) for p in raw_patterns)
        log_methods = config.get("log_methods")
        if log_methods is not None:
            rule.log_methods = frozenset(log_methods)
        direct_sinks = config.get("direct_sinks")
        if direct_sinks is not None:
            rule.direct_sinks = frozenset(direct_sinks)
        return rule

    @classmethod
    def xǁNoLoggingSecretsǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLoggingSecrets:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLoggingSecrets)  # noqa: S101  # narrowing for mypy
        raw_patterns = config.get("secret_patterns", None)
        rule.secret_patterns = tuple(re.compile(p) for p in raw_patterns)
        log_methods = config.get("log_methods")
        if log_methods is not None:
            rule.log_methods = frozenset(log_methods)
        direct_sinks = config.get("direct_sinks")
        if direct_sinks is not None:
            rule.direct_sinks = frozenset(direct_sinks)
        return rule

    @classmethod
    def xǁNoLoggingSecretsǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLoggingSecrets:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLoggingSecrets)  # noqa: S101  # narrowing for mypy
        raw_patterns = config.get(DEFAULT_SECRET_PATTERNS)
        rule.secret_patterns = tuple(re.compile(p) for p in raw_patterns)
        log_methods = config.get("log_methods")
        if log_methods is not None:
            rule.log_methods = frozenset(log_methods)
        direct_sinks = config.get("direct_sinks")
        if direct_sinks is not None:
            rule.direct_sinks = frozenset(direct_sinks)
        return rule

    @classmethod
    def xǁNoLoggingSecretsǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLoggingSecrets:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLoggingSecrets)  # noqa: S101  # narrowing for mypy
        raw_patterns = config.get("secret_patterns", )
        rule.secret_patterns = tuple(re.compile(p) for p in raw_patterns)
        log_methods = config.get("log_methods")
        if log_methods is not None:
            rule.log_methods = frozenset(log_methods)
        direct_sinks = config.get("direct_sinks")
        if direct_sinks is not None:
            rule.direct_sinks = frozenset(direct_sinks)
        return rule

    @classmethod
    def xǁNoLoggingSecretsǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLoggingSecrets:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLoggingSecrets)  # noqa: S101  # narrowing for mypy
        raw_patterns = config.get("XXsecret_patternsXX", DEFAULT_SECRET_PATTERNS)
        rule.secret_patterns = tuple(re.compile(p) for p in raw_patterns)
        log_methods = config.get("log_methods")
        if log_methods is not None:
            rule.log_methods = frozenset(log_methods)
        direct_sinks = config.get("direct_sinks")
        if direct_sinks is not None:
            rule.direct_sinks = frozenset(direct_sinks)
        return rule

    @classmethod
    def xǁNoLoggingSecretsǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLoggingSecrets:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLoggingSecrets)  # noqa: S101  # narrowing for mypy
        raw_patterns = config.get("SECRET_PATTERNS", DEFAULT_SECRET_PATTERNS)
        rule.secret_patterns = tuple(re.compile(p) for p in raw_patterns)
        log_methods = config.get("log_methods")
        if log_methods is not None:
            rule.log_methods = frozenset(log_methods)
        direct_sinks = config.get("direct_sinks")
        if direct_sinks is not None:
            rule.direct_sinks = frozenset(direct_sinks)
        return rule

    @classmethod
    def xǁNoLoggingSecretsǁfrom_config__mutmut_13(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLoggingSecrets:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLoggingSecrets)  # noqa: S101  # narrowing for mypy
        raw_patterns = config.get("secret_patterns", DEFAULT_SECRET_PATTERNS)
        rule.secret_patterns = None
        log_methods = config.get("log_methods")
        if log_methods is not None:
            rule.log_methods = frozenset(log_methods)
        direct_sinks = config.get("direct_sinks")
        if direct_sinks is not None:
            rule.direct_sinks = frozenset(direct_sinks)
        return rule

    @classmethod
    def xǁNoLoggingSecretsǁfrom_config__mutmut_14(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLoggingSecrets:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLoggingSecrets)  # noqa: S101  # narrowing for mypy
        raw_patterns = config.get("secret_patterns", DEFAULT_SECRET_PATTERNS)
        rule.secret_patterns = tuple(None)
        log_methods = config.get("log_methods")
        if log_methods is not None:
            rule.log_methods = frozenset(log_methods)
        direct_sinks = config.get("direct_sinks")
        if direct_sinks is not None:
            rule.direct_sinks = frozenset(direct_sinks)
        return rule

    @classmethod
    def xǁNoLoggingSecretsǁfrom_config__mutmut_15(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLoggingSecrets:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLoggingSecrets)  # noqa: S101  # narrowing for mypy
        raw_patterns = config.get("secret_patterns", DEFAULT_SECRET_PATTERNS)
        rule.secret_patterns = tuple(re.compile(None) for p in raw_patterns)
        log_methods = config.get("log_methods")
        if log_methods is not None:
            rule.log_methods = frozenset(log_methods)
        direct_sinks = config.get("direct_sinks")
        if direct_sinks is not None:
            rule.direct_sinks = frozenset(direct_sinks)
        return rule

    @classmethod
    def xǁNoLoggingSecretsǁfrom_config__mutmut_16(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLoggingSecrets:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLoggingSecrets)  # noqa: S101  # narrowing for mypy
        raw_patterns = config.get("secret_patterns", DEFAULT_SECRET_PATTERNS)
        rule.secret_patterns = tuple(re.compile(p) for p in raw_patterns)
        log_methods = None
        if log_methods is not None:
            rule.log_methods = frozenset(log_methods)
        direct_sinks = config.get("direct_sinks")
        if direct_sinks is not None:
            rule.direct_sinks = frozenset(direct_sinks)
        return rule

    @classmethod
    def xǁNoLoggingSecretsǁfrom_config__mutmut_17(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLoggingSecrets:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLoggingSecrets)  # noqa: S101  # narrowing for mypy
        raw_patterns = config.get("secret_patterns", DEFAULT_SECRET_PATTERNS)
        rule.secret_patterns = tuple(re.compile(p) for p in raw_patterns)
        log_methods = config.get(None)
        if log_methods is not None:
            rule.log_methods = frozenset(log_methods)
        direct_sinks = config.get("direct_sinks")
        if direct_sinks is not None:
            rule.direct_sinks = frozenset(direct_sinks)
        return rule

    @classmethod
    def xǁNoLoggingSecretsǁfrom_config__mutmut_18(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLoggingSecrets:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLoggingSecrets)  # noqa: S101  # narrowing for mypy
        raw_patterns = config.get("secret_patterns", DEFAULT_SECRET_PATTERNS)
        rule.secret_patterns = tuple(re.compile(p) for p in raw_patterns)
        log_methods = config.get("XXlog_methodsXX")
        if log_methods is not None:
            rule.log_methods = frozenset(log_methods)
        direct_sinks = config.get("direct_sinks")
        if direct_sinks is not None:
            rule.direct_sinks = frozenset(direct_sinks)
        return rule

    @classmethod
    def xǁNoLoggingSecretsǁfrom_config__mutmut_19(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLoggingSecrets:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLoggingSecrets)  # noqa: S101  # narrowing for mypy
        raw_patterns = config.get("secret_patterns", DEFAULT_SECRET_PATTERNS)
        rule.secret_patterns = tuple(re.compile(p) for p in raw_patterns)
        log_methods = config.get("LOG_METHODS")
        if log_methods is not None:
            rule.log_methods = frozenset(log_methods)
        direct_sinks = config.get("direct_sinks")
        if direct_sinks is not None:
            rule.direct_sinks = frozenset(direct_sinks)
        return rule

    @classmethod
    def xǁNoLoggingSecretsǁfrom_config__mutmut_20(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLoggingSecrets:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLoggingSecrets)  # noqa: S101  # narrowing for mypy
        raw_patterns = config.get("secret_patterns", DEFAULT_SECRET_PATTERNS)
        rule.secret_patterns = tuple(re.compile(p) for p in raw_patterns)
        log_methods = config.get("log_methods")
        if log_methods is None:
            rule.log_methods = frozenset(log_methods)
        direct_sinks = config.get("direct_sinks")
        if direct_sinks is not None:
            rule.direct_sinks = frozenset(direct_sinks)
        return rule

    @classmethod
    def xǁNoLoggingSecretsǁfrom_config__mutmut_21(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLoggingSecrets:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLoggingSecrets)  # noqa: S101  # narrowing for mypy
        raw_patterns = config.get("secret_patterns", DEFAULT_SECRET_PATTERNS)
        rule.secret_patterns = tuple(re.compile(p) for p in raw_patterns)
        log_methods = config.get("log_methods")
        if log_methods is not None:
            rule.log_methods = None
        direct_sinks = config.get("direct_sinks")
        if direct_sinks is not None:
            rule.direct_sinks = frozenset(direct_sinks)
        return rule

    @classmethod
    def xǁNoLoggingSecretsǁfrom_config__mutmut_22(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLoggingSecrets:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLoggingSecrets)  # noqa: S101  # narrowing for mypy
        raw_patterns = config.get("secret_patterns", DEFAULT_SECRET_PATTERNS)
        rule.secret_patterns = tuple(re.compile(p) for p in raw_patterns)
        log_methods = config.get("log_methods")
        if log_methods is not None:
            rule.log_methods = frozenset(None)
        direct_sinks = config.get("direct_sinks")
        if direct_sinks is not None:
            rule.direct_sinks = frozenset(direct_sinks)
        return rule

    @classmethod
    def xǁNoLoggingSecretsǁfrom_config__mutmut_23(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLoggingSecrets:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLoggingSecrets)  # noqa: S101  # narrowing for mypy
        raw_patterns = config.get("secret_patterns", DEFAULT_SECRET_PATTERNS)
        rule.secret_patterns = tuple(re.compile(p) for p in raw_patterns)
        log_methods = config.get("log_methods")
        if log_methods is not None:
            rule.log_methods = frozenset(log_methods)
        direct_sinks = None
        if direct_sinks is not None:
            rule.direct_sinks = frozenset(direct_sinks)
        return rule

    @classmethod
    def xǁNoLoggingSecretsǁfrom_config__mutmut_24(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLoggingSecrets:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLoggingSecrets)  # noqa: S101  # narrowing for mypy
        raw_patterns = config.get("secret_patterns", DEFAULT_SECRET_PATTERNS)
        rule.secret_patterns = tuple(re.compile(p) for p in raw_patterns)
        log_methods = config.get("log_methods")
        if log_methods is not None:
            rule.log_methods = frozenset(log_methods)
        direct_sinks = config.get(None)
        if direct_sinks is not None:
            rule.direct_sinks = frozenset(direct_sinks)
        return rule

    @classmethod
    def xǁNoLoggingSecretsǁfrom_config__mutmut_25(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLoggingSecrets:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLoggingSecrets)  # noqa: S101  # narrowing for mypy
        raw_patterns = config.get("secret_patterns", DEFAULT_SECRET_PATTERNS)
        rule.secret_patterns = tuple(re.compile(p) for p in raw_patterns)
        log_methods = config.get("log_methods")
        if log_methods is not None:
            rule.log_methods = frozenset(log_methods)
        direct_sinks = config.get("XXdirect_sinksXX")
        if direct_sinks is not None:
            rule.direct_sinks = frozenset(direct_sinks)
        return rule

    @classmethod
    def xǁNoLoggingSecretsǁfrom_config__mutmut_26(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLoggingSecrets:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLoggingSecrets)  # noqa: S101  # narrowing for mypy
        raw_patterns = config.get("secret_patterns", DEFAULT_SECRET_PATTERNS)
        rule.secret_patterns = tuple(re.compile(p) for p in raw_patterns)
        log_methods = config.get("log_methods")
        if log_methods is not None:
            rule.log_methods = frozenset(log_methods)
        direct_sinks = config.get("DIRECT_SINKS")
        if direct_sinks is not None:
            rule.direct_sinks = frozenset(direct_sinks)
        return rule

    @classmethod
    def xǁNoLoggingSecretsǁfrom_config__mutmut_27(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLoggingSecrets:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLoggingSecrets)  # noqa: S101  # narrowing for mypy
        raw_patterns = config.get("secret_patterns", DEFAULT_SECRET_PATTERNS)
        rule.secret_patterns = tuple(re.compile(p) for p in raw_patterns)
        log_methods = config.get("log_methods")
        if log_methods is not None:
            rule.log_methods = frozenset(log_methods)
        direct_sinks = config.get("direct_sinks")
        if direct_sinks is None:
            rule.direct_sinks = frozenset(direct_sinks)
        return rule

    @classmethod
    def xǁNoLoggingSecretsǁfrom_config__mutmut_28(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLoggingSecrets:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLoggingSecrets)  # noqa: S101  # narrowing for mypy
        raw_patterns = config.get("secret_patterns", DEFAULT_SECRET_PATTERNS)
        rule.secret_patterns = tuple(re.compile(p) for p in raw_patterns)
        log_methods = config.get("log_methods")
        if log_methods is not None:
            rule.log_methods = frozenset(log_methods)
        direct_sinks = config.get("direct_sinks")
        if direct_sinks is not None:
            rule.direct_sinks = None
        return rule

    @classmethod
    def xǁNoLoggingSecretsǁfrom_config__mutmut_29(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLoggingSecrets:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLoggingSecrets)  # noqa: S101  # narrowing for mypy
        raw_patterns = config.get("secret_patterns", DEFAULT_SECRET_PATTERNS)
        rule.secret_patterns = tuple(re.compile(p) for p in raw_patterns)
        log_methods = config.get("log_methods")
        if log_methods is not None:
            rule.log_methods = frozenset(log_methods)
        direct_sinks = config.get("direct_sinks")
        if direct_sinks is not None:
            rule.direct_sinks = frozenset(None)
        return rule

    @_mutmut_mutated(mutants_xǁNoLoggingSecretsǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        return module_logs_secret(
            path,
            patterns=self.secret_patterns,
            log_methods=self.log_methods,
            direct_sinks=self.direct_sinks,
        )

    def xǁNoLoggingSecretsǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        return module_logs_secret(
            path,
            patterns=self.secret_patterns,
            log_methods=self.log_methods,
            direct_sinks=self.direct_sinks,
        )

    def xǁNoLoggingSecretsǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        return module_logs_secret(
            None,
            patterns=self.secret_patterns,
            log_methods=self.log_methods,
            direct_sinks=self.direct_sinks,
        )

    def xǁNoLoggingSecretsǁfile_has_violation__mutmut_2(self, path: Path) -> bool:
        return module_logs_secret(
            path,
            patterns=None,
            log_methods=self.log_methods,
            direct_sinks=self.direct_sinks,
        )

    def xǁNoLoggingSecretsǁfile_has_violation__mutmut_3(self, path: Path) -> bool:
        return module_logs_secret(
            path,
            patterns=self.secret_patterns,
            log_methods=None,
            direct_sinks=self.direct_sinks,
        )

    def xǁNoLoggingSecretsǁfile_has_violation__mutmut_4(self, path: Path) -> bool:
        return module_logs_secret(
            path,
            patterns=self.secret_patterns,
            log_methods=self.log_methods,
            direct_sinks=None,
        )

    def xǁNoLoggingSecretsǁfile_has_violation__mutmut_5(self, path: Path) -> bool:
        return module_logs_secret(
            patterns=self.secret_patterns,
            log_methods=self.log_methods,
            direct_sinks=self.direct_sinks,
        )

    def xǁNoLoggingSecretsǁfile_has_violation__mutmut_6(self, path: Path) -> bool:
        return module_logs_secret(
            path,
            log_methods=self.log_methods,
            direct_sinks=self.direct_sinks,
        )

    def xǁNoLoggingSecretsǁfile_has_violation__mutmut_7(self, path: Path) -> bool:
        return module_logs_secret(
            path,
            patterns=self.secret_patterns,
            direct_sinks=self.direct_sinks,
        )

    def xǁNoLoggingSecretsǁfile_has_violation__mutmut_8(self, path: Path) -> bool:
        return module_logs_secret(
            path,
            patterns=self.secret_patterns,
            log_methods=self.log_methods,
            )

mutants_xǁNoLoggingSecretsǁfrom_config__mutmut['_mutmut_orig'] = NoLoggingSecrets.xǁNoLoggingSecretsǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNoLoggingSecretsǁfrom_config__mutmut['xǁNoLoggingSecretsǁfrom_config__mutmut_1'] = NoLoggingSecrets.xǁNoLoggingSecretsǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNoLoggingSecretsǁfrom_config__mutmut['xǁNoLoggingSecretsǁfrom_config__mutmut_2'] = NoLoggingSecrets.xǁNoLoggingSecretsǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNoLoggingSecretsǁfrom_config__mutmut['xǁNoLoggingSecretsǁfrom_config__mutmut_3'] = NoLoggingSecrets.xǁNoLoggingSecretsǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNoLoggingSecretsǁfrom_config__mutmut['xǁNoLoggingSecretsǁfrom_config__mutmut_4'] = NoLoggingSecrets.xǁNoLoggingSecretsǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁNoLoggingSecretsǁfrom_config__mutmut['xǁNoLoggingSecretsǁfrom_config__mutmut_5'] = NoLoggingSecrets.xǁNoLoggingSecretsǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁNoLoggingSecretsǁfrom_config__mutmut['xǁNoLoggingSecretsǁfrom_config__mutmut_6'] = NoLoggingSecrets.xǁNoLoggingSecretsǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁNoLoggingSecretsǁfrom_config__mutmut['xǁNoLoggingSecretsǁfrom_config__mutmut_7'] = NoLoggingSecrets.xǁNoLoggingSecretsǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁNoLoggingSecretsǁfrom_config__mutmut['xǁNoLoggingSecretsǁfrom_config__mutmut_8'] = NoLoggingSecrets.xǁNoLoggingSecretsǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁNoLoggingSecretsǁfrom_config__mutmut['xǁNoLoggingSecretsǁfrom_config__mutmut_9'] = NoLoggingSecrets.xǁNoLoggingSecretsǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁNoLoggingSecretsǁfrom_config__mutmut['xǁNoLoggingSecretsǁfrom_config__mutmut_10'] = NoLoggingSecrets.xǁNoLoggingSecretsǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁNoLoggingSecretsǁfrom_config__mutmut['xǁNoLoggingSecretsǁfrom_config__mutmut_11'] = NoLoggingSecrets.xǁNoLoggingSecretsǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁNoLoggingSecretsǁfrom_config__mutmut['xǁNoLoggingSecretsǁfrom_config__mutmut_12'] = NoLoggingSecrets.xǁNoLoggingSecretsǁfrom_config__mutmut_12 # type: ignore # mutmut generated
mutants_xǁNoLoggingSecretsǁfrom_config__mutmut['xǁNoLoggingSecretsǁfrom_config__mutmut_13'] = NoLoggingSecrets.xǁNoLoggingSecretsǁfrom_config__mutmut_13 # type: ignore # mutmut generated
mutants_xǁNoLoggingSecretsǁfrom_config__mutmut['xǁNoLoggingSecretsǁfrom_config__mutmut_14'] = NoLoggingSecrets.xǁNoLoggingSecretsǁfrom_config__mutmut_14 # type: ignore # mutmut generated
mutants_xǁNoLoggingSecretsǁfrom_config__mutmut['xǁNoLoggingSecretsǁfrom_config__mutmut_15'] = NoLoggingSecrets.xǁNoLoggingSecretsǁfrom_config__mutmut_15 # type: ignore # mutmut generated
mutants_xǁNoLoggingSecretsǁfrom_config__mutmut['xǁNoLoggingSecretsǁfrom_config__mutmut_16'] = NoLoggingSecrets.xǁNoLoggingSecretsǁfrom_config__mutmut_16 # type: ignore # mutmut generated
mutants_xǁNoLoggingSecretsǁfrom_config__mutmut['xǁNoLoggingSecretsǁfrom_config__mutmut_17'] = NoLoggingSecrets.xǁNoLoggingSecretsǁfrom_config__mutmut_17 # type: ignore # mutmut generated
mutants_xǁNoLoggingSecretsǁfrom_config__mutmut['xǁNoLoggingSecretsǁfrom_config__mutmut_18'] = NoLoggingSecrets.xǁNoLoggingSecretsǁfrom_config__mutmut_18 # type: ignore # mutmut generated
mutants_xǁNoLoggingSecretsǁfrom_config__mutmut['xǁNoLoggingSecretsǁfrom_config__mutmut_19'] = NoLoggingSecrets.xǁNoLoggingSecretsǁfrom_config__mutmut_19 # type: ignore # mutmut generated
mutants_xǁNoLoggingSecretsǁfrom_config__mutmut['xǁNoLoggingSecretsǁfrom_config__mutmut_20'] = NoLoggingSecrets.xǁNoLoggingSecretsǁfrom_config__mutmut_20 # type: ignore # mutmut generated
mutants_xǁNoLoggingSecretsǁfrom_config__mutmut['xǁNoLoggingSecretsǁfrom_config__mutmut_21'] = NoLoggingSecrets.xǁNoLoggingSecretsǁfrom_config__mutmut_21 # type: ignore # mutmut generated
mutants_xǁNoLoggingSecretsǁfrom_config__mutmut['xǁNoLoggingSecretsǁfrom_config__mutmut_22'] = NoLoggingSecrets.xǁNoLoggingSecretsǁfrom_config__mutmut_22 # type: ignore # mutmut generated
mutants_xǁNoLoggingSecretsǁfrom_config__mutmut['xǁNoLoggingSecretsǁfrom_config__mutmut_23'] = NoLoggingSecrets.xǁNoLoggingSecretsǁfrom_config__mutmut_23 # type: ignore # mutmut generated
mutants_xǁNoLoggingSecretsǁfrom_config__mutmut['xǁNoLoggingSecretsǁfrom_config__mutmut_24'] = NoLoggingSecrets.xǁNoLoggingSecretsǁfrom_config__mutmut_24 # type: ignore # mutmut generated
mutants_xǁNoLoggingSecretsǁfrom_config__mutmut['xǁNoLoggingSecretsǁfrom_config__mutmut_25'] = NoLoggingSecrets.xǁNoLoggingSecretsǁfrom_config__mutmut_25 # type: ignore # mutmut generated
mutants_xǁNoLoggingSecretsǁfrom_config__mutmut['xǁNoLoggingSecretsǁfrom_config__mutmut_26'] = NoLoggingSecrets.xǁNoLoggingSecretsǁfrom_config__mutmut_26 # type: ignore # mutmut generated
mutants_xǁNoLoggingSecretsǁfrom_config__mutmut['xǁNoLoggingSecretsǁfrom_config__mutmut_27'] = NoLoggingSecrets.xǁNoLoggingSecretsǁfrom_config__mutmut_27 # type: ignore # mutmut generated
mutants_xǁNoLoggingSecretsǁfrom_config__mutmut['xǁNoLoggingSecretsǁfrom_config__mutmut_28'] = NoLoggingSecrets.xǁNoLoggingSecretsǁfrom_config__mutmut_28 # type: ignore # mutmut generated
mutants_xǁNoLoggingSecretsǁfrom_config__mutmut['xǁNoLoggingSecretsǁfrom_config__mutmut_29'] = NoLoggingSecrets.xǁNoLoggingSecretsǁfrom_config__mutmut_29 # type: ignore # mutmut generated

mutants_xǁNoLoggingSecretsǁfile_has_violation__mutmut['_mutmut_orig'] = NoLoggingSecrets.xǁNoLoggingSecretsǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNoLoggingSecretsǁfile_has_violation__mutmut['xǁNoLoggingSecretsǁfile_has_violation__mutmut_1'] = NoLoggingSecrets.xǁNoLoggingSecretsǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNoLoggingSecretsǁfile_has_violation__mutmut['xǁNoLoggingSecretsǁfile_has_violation__mutmut_2'] = NoLoggingSecrets.xǁNoLoggingSecretsǁfile_has_violation__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNoLoggingSecretsǁfile_has_violation__mutmut['xǁNoLoggingSecretsǁfile_has_violation__mutmut_3'] = NoLoggingSecrets.xǁNoLoggingSecretsǁfile_has_violation__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNoLoggingSecretsǁfile_has_violation__mutmut['xǁNoLoggingSecretsǁfile_has_violation__mutmut_4'] = NoLoggingSecrets.xǁNoLoggingSecretsǁfile_has_violation__mutmut_4 # type: ignore # mutmut generated
mutants_xǁNoLoggingSecretsǁfile_has_violation__mutmut['xǁNoLoggingSecretsǁfile_has_violation__mutmut_5'] = NoLoggingSecrets.xǁNoLoggingSecretsǁfile_has_violation__mutmut_5 # type: ignore # mutmut generated
mutants_xǁNoLoggingSecretsǁfile_has_violation__mutmut['xǁNoLoggingSecretsǁfile_has_violation__mutmut_6'] = NoLoggingSecrets.xǁNoLoggingSecretsǁfile_has_violation__mutmut_6 # type: ignore # mutmut generated
mutants_xǁNoLoggingSecretsǁfile_has_violation__mutmut['xǁNoLoggingSecretsǁfile_has_violation__mutmut_7'] = NoLoggingSecrets.xǁNoLoggingSecretsǁfile_has_violation__mutmut_7 # type: ignore # mutmut generated
mutants_xǁNoLoggingSecretsǁfile_has_violation__mutmut['xǁNoLoggingSecretsǁfile_has_violation__mutmut_8'] = NoLoggingSecrets.xǁNoLoggingSecretsǁfile_has_violation__mutmut_8 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoLoggingSecrets:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoLoggingSecrets.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoLoggingSecrets:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoLoggingSecrets.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoLoggingSecrets:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoLoggingSecrets.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoLoggingSecrets:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoLoggingSecrets.from_config(config, repo_root=None)


def x_build__mutmut_3(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoLoggingSecrets:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoLoggingSecrets.from_config(repo_root=repo_root)


def x_build__mutmut_4(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoLoggingSecrets:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoLoggingSecrets.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoLoggingSecrets, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoLoggingSecrets, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoLoggingSecrets, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoLoggingSecrets, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
