"""CORE check: no_real_names — keep real identities out of fixtures and examples.

Test fixtures, BDD scenarios, and documentation examples must use synthetic
identities, never real client / person / company names. A leaked real name in
a committed example is a confidentiality and reputational hazard that survives
every fork of the fixture. This rule walks the configured fixture / example
surface and FAILS when a banned name token appears outside an allow-list.

Ported from tc-agent-zone ``scripts/checks/no_real_names_in_fixtures.py``
(issue #184) and re-expressed as a configurable, repo-agnostic rule. The
banned-token-to-substitute mapping, the directory surface that is scanned, the
in-scope text extensions, and the allow-list are ALL consumer config — the
engine ships no real names, no synthetic placeholders, and no repo paths. A
consumer supplies its own mapping via ``[tool.tc_fitness]`` (taz uses
Bupa->AcmeHealth, Avanade->NexusDigital, etc.; another repo's mapping differs).
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: Domain-intrinsic defaults for the *shape* of the scan (not repo identity).
#: A consumer always supplies its own ``substitutions``; with an empty map the
#: rule is a no-op, so the default never silently passes a real name.
DEFAULT_EXTENSIONS = (
    ".md",
    ".markdown",
    ".txt",
    ".rst",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".py",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".sh",
    ".html",
    ".xml",
    ".csv",
    ".feature",
    ".jinja",
    ".j2",
    ".tmpl",
)

REMEDIATION = _remediation(
    fix=(
        "substitute the real name with the synthetic placeholder your standard "
        "maps it to (the consumer's substitution map names the replacement); OR, "
        "if the file is legitimately authoritative, add its repo-relative path to "
        "the configured allow-list with a justifying comment."
    ),
    nxt="re-run this check to confirm it goes green.",
    run="python -m tc_fitness.core_checks.no_real_names",
    passing='client = "AcmeHealth"  # synthetic substitute, never the real client',
    forbidden='client = "<real-company-name>"  # leaks a real identity into a fixture',
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x__compile_token__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__compile_token__mutmut)
def _compile_token(token: str) -> re.Pattern[str]:
    """Word-boundary matcher tolerating digit-bearing tokens (e.g. ``3CV``).

    A plain ``\\b`` boundary fails next to a digit at a word edge, so this uses
    explicit alphanumeric look-arounds: the token matches only when not flanked
    by another alphanumeric char.
    """
    return re.compile(rf"(?<![A-Za-z0-9]){re.escape(token)}(?![A-Za-z0-9])")


def x__compile_token__mutmut_orig(token: str) -> re.Pattern[str]:
    """Word-boundary matcher tolerating digit-bearing tokens (e.g. ``3CV``).

    A plain ``\\b`` boundary fails next to a digit at a word edge, so this uses
    explicit alphanumeric look-arounds: the token matches only when not flanked
    by another alphanumeric char.
    """
    return re.compile(rf"(?<![A-Za-z0-9]){re.escape(token)}(?![A-Za-z0-9])")


def x__compile_token__mutmut_1(token: str) -> re.Pattern[str]:
    """Word-boundary matcher tolerating digit-bearing tokens (e.g. ``3CV``).

    A plain ``\\b`` boundary fails next to a digit at a word edge, so this uses
    explicit alphanumeric look-arounds: the token matches only when not flanked
    by another alphanumeric char.
    """
    return re.compile(None)


def x__compile_token__mutmut_2(token: str) -> re.Pattern[str]:
    """Word-boundary matcher tolerating digit-bearing tokens (e.g. ``3CV``).

    A plain ``\\b`` boundary fails next to a digit at a word edge, so this uses
    explicit alphanumeric look-arounds: the token matches only when not flanked
    by another alphanumeric char.
    """
    return re.compile(rf"(?<![A-Za-z0-9]){re.escape(None)}(?![A-Za-z0-9])")

mutants_x__compile_token__mutmut['_mutmut_orig'] = x__compile_token__mutmut_orig # type: ignore # mutmut generated
mutants_x__compile_token__mutmut['x__compile_token__mutmut_1'] = x__compile_token__mutmut_1 # type: ignore # mutmut generated
mutants_x__compile_token__mutmut['x__compile_token__mutmut_2'] = x__compile_token__mutmut_2 # type: ignore # mutmut generated
mutants_x_file_has_real_name__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_file_has_real_name__mutmut)
def file_has_real_name(
    path: Path,
    *,
    tokens: Sequence[str],
    scope_segments: Sequence[str],
    repo_root: Path,
) -> bool:
    """True iff ``path`` is in the scan surface AND contains a banned token.

    ``scope_segments`` are path segments any one of which must appear in the
    file's repo-relative path for it to be in scope (e.g. an examples directory
    anywhere in the ancestry). An empty ``scope_segments`` means every in-scope
    extension is scanned. A decode error returns False (binary / unreadable
    files carry no readable identity to leak).
    """
    try:
        rel = path.resolve().relative_to(repo_root).as_posix()
    except ValueError:
        rel = path.as_posix()
    if scope_segments and not any(seg in rel.split("/") for seg in scope_segments):
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return False
    return any(_compile_token(tok).search(text) for tok in tokens)


def x_file_has_real_name__mutmut_orig(
    path: Path,
    *,
    tokens: Sequence[str],
    scope_segments: Sequence[str],
    repo_root: Path,
) -> bool:
    """True iff ``path`` is in the scan surface AND contains a banned token.

    ``scope_segments`` are path segments any one of which must appear in the
    file's repo-relative path for it to be in scope (e.g. an examples directory
    anywhere in the ancestry). An empty ``scope_segments`` means every in-scope
    extension is scanned. A decode error returns False (binary / unreadable
    files carry no readable identity to leak).
    """
    try:
        rel = path.resolve().relative_to(repo_root).as_posix()
    except ValueError:
        rel = path.as_posix()
    if scope_segments and not any(seg in rel.split("/") for seg in scope_segments):
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return False
    return any(_compile_token(tok).search(text) for tok in tokens)


def x_file_has_real_name__mutmut_1(
    path: Path,
    *,
    tokens: Sequence[str],
    scope_segments: Sequence[str],
    repo_root: Path,
) -> bool:
    """True iff ``path`` is in the scan surface AND contains a banned token.

    ``scope_segments`` are path segments any one of which must appear in the
    file's repo-relative path for it to be in scope (e.g. an examples directory
    anywhere in the ancestry). An empty ``scope_segments`` means every in-scope
    extension is scanned. A decode error returns False (binary / unreadable
    files carry no readable identity to leak).
    """
    try:
        rel = None
    except ValueError:
        rel = path.as_posix()
    if scope_segments and not any(seg in rel.split("/") for seg in scope_segments):
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return False
    return any(_compile_token(tok).search(text) for tok in tokens)


def x_file_has_real_name__mutmut_2(
    path: Path,
    *,
    tokens: Sequence[str],
    scope_segments: Sequence[str],
    repo_root: Path,
) -> bool:
    """True iff ``path`` is in the scan surface AND contains a banned token.

    ``scope_segments`` are path segments any one of which must appear in the
    file's repo-relative path for it to be in scope (e.g. an examples directory
    anywhere in the ancestry). An empty ``scope_segments`` means every in-scope
    extension is scanned. A decode error returns False (binary / unreadable
    files carry no readable identity to leak).
    """
    try:
        rel = path.resolve().relative_to(None).as_posix()
    except ValueError:
        rel = path.as_posix()
    if scope_segments and not any(seg in rel.split("/") for seg in scope_segments):
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return False
    return any(_compile_token(tok).search(text) for tok in tokens)


def x_file_has_real_name__mutmut_3(
    path: Path,
    *,
    tokens: Sequence[str],
    scope_segments: Sequence[str],
    repo_root: Path,
) -> bool:
    """True iff ``path`` is in the scan surface AND contains a banned token.

    ``scope_segments`` are path segments any one of which must appear in the
    file's repo-relative path for it to be in scope (e.g. an examples directory
    anywhere in the ancestry). An empty ``scope_segments`` means every in-scope
    extension is scanned. A decode error returns False (binary / unreadable
    files carry no readable identity to leak).
    """
    try:
        rel = path.resolve().relative_to(repo_root).as_posix()
    except ValueError:
        rel = None
    if scope_segments and not any(seg in rel.split("/") for seg in scope_segments):
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return False
    return any(_compile_token(tok).search(text) for tok in tokens)


def x_file_has_real_name__mutmut_4(
    path: Path,
    *,
    tokens: Sequence[str],
    scope_segments: Sequence[str],
    repo_root: Path,
) -> bool:
    """True iff ``path`` is in the scan surface AND contains a banned token.

    ``scope_segments`` are path segments any one of which must appear in the
    file's repo-relative path for it to be in scope (e.g. an examples directory
    anywhere in the ancestry). An empty ``scope_segments`` means every in-scope
    extension is scanned. A decode error returns False (binary / unreadable
    files carry no readable identity to leak).
    """
    try:
        rel = path.resolve().relative_to(repo_root).as_posix()
    except ValueError:
        rel = path.as_posix()
    if scope_segments or not any(seg in rel.split("/") for seg in scope_segments):
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return False
    return any(_compile_token(tok).search(text) for tok in tokens)


def x_file_has_real_name__mutmut_5(
    path: Path,
    *,
    tokens: Sequence[str],
    scope_segments: Sequence[str],
    repo_root: Path,
) -> bool:
    """True iff ``path`` is in the scan surface AND contains a banned token.

    ``scope_segments`` are path segments any one of which must appear in the
    file's repo-relative path for it to be in scope (e.g. an examples directory
    anywhere in the ancestry). An empty ``scope_segments`` means every in-scope
    extension is scanned. A decode error returns False (binary / unreadable
    files carry no readable identity to leak).
    """
    try:
        rel = path.resolve().relative_to(repo_root).as_posix()
    except ValueError:
        rel = path.as_posix()
    if scope_segments and any(seg in rel.split("/") for seg in scope_segments):
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return False
    return any(_compile_token(tok).search(text) for tok in tokens)


def x_file_has_real_name__mutmut_6(
    path: Path,
    *,
    tokens: Sequence[str],
    scope_segments: Sequence[str],
    repo_root: Path,
) -> bool:
    """True iff ``path`` is in the scan surface AND contains a banned token.

    ``scope_segments`` are path segments any one of which must appear in the
    file's repo-relative path for it to be in scope (e.g. an examples directory
    anywhere in the ancestry). An empty ``scope_segments`` means every in-scope
    extension is scanned. A decode error returns False (binary / unreadable
    files carry no readable identity to leak).
    """
    try:
        rel = path.resolve().relative_to(repo_root).as_posix()
    except ValueError:
        rel = path.as_posix()
    if scope_segments and not any(None):
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return False
    return any(_compile_token(tok).search(text) for tok in tokens)


def x_file_has_real_name__mutmut_7(
    path: Path,
    *,
    tokens: Sequence[str],
    scope_segments: Sequence[str],
    repo_root: Path,
) -> bool:
    """True iff ``path`` is in the scan surface AND contains a banned token.

    ``scope_segments`` are path segments any one of which must appear in the
    file's repo-relative path for it to be in scope (e.g. an examples directory
    anywhere in the ancestry). An empty ``scope_segments`` means every in-scope
    extension is scanned. A decode error returns False (binary / unreadable
    files carry no readable identity to leak).
    """
    try:
        rel = path.resolve().relative_to(repo_root).as_posix()
    except ValueError:
        rel = path.as_posix()
    if scope_segments and not any(seg not in rel.split("/") for seg in scope_segments):
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return False
    return any(_compile_token(tok).search(text) for tok in tokens)


def x_file_has_real_name__mutmut_8(
    path: Path,
    *,
    tokens: Sequence[str],
    scope_segments: Sequence[str],
    repo_root: Path,
) -> bool:
    """True iff ``path`` is in the scan surface AND contains a banned token.

    ``scope_segments`` are path segments any one of which must appear in the
    file's repo-relative path for it to be in scope (e.g. an examples directory
    anywhere in the ancestry). An empty ``scope_segments`` means every in-scope
    extension is scanned. A decode error returns False (binary / unreadable
    files carry no readable identity to leak).
    """
    try:
        rel = path.resolve().relative_to(repo_root).as_posix()
    except ValueError:
        rel = path.as_posix()
    if scope_segments and not any(seg in rel.split(None) for seg in scope_segments):
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return False
    return any(_compile_token(tok).search(text) for tok in tokens)


def x_file_has_real_name__mutmut_9(
    path: Path,
    *,
    tokens: Sequence[str],
    scope_segments: Sequence[str],
    repo_root: Path,
) -> bool:
    """True iff ``path`` is in the scan surface AND contains a banned token.

    ``scope_segments`` are path segments any one of which must appear in the
    file's repo-relative path for it to be in scope (e.g. an examples directory
    anywhere in the ancestry). An empty ``scope_segments`` means every in-scope
    extension is scanned. A decode error returns False (binary / unreadable
    files carry no readable identity to leak).
    """
    try:
        rel = path.resolve().relative_to(repo_root).as_posix()
    except ValueError:
        rel = path.as_posix()
    if scope_segments and not any(seg in rel.split("XX/XX") for seg in scope_segments):
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return False
    return any(_compile_token(tok).search(text) for tok in tokens)


def x_file_has_real_name__mutmut_10(
    path: Path,
    *,
    tokens: Sequence[str],
    scope_segments: Sequence[str],
    repo_root: Path,
) -> bool:
    """True iff ``path`` is in the scan surface AND contains a banned token.

    ``scope_segments`` are path segments any one of which must appear in the
    file's repo-relative path for it to be in scope (e.g. an examples directory
    anywhere in the ancestry). An empty ``scope_segments`` means every in-scope
    extension is scanned. A decode error returns False (binary / unreadable
    files carry no readable identity to leak).
    """
    try:
        rel = path.resolve().relative_to(repo_root).as_posix()
    except ValueError:
        rel = path.as_posix()
    if scope_segments and not any(seg in rel.split("/") for seg in scope_segments):
        return True
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return False
    return any(_compile_token(tok).search(text) for tok in tokens)


def x_file_has_real_name__mutmut_11(
    path: Path,
    *,
    tokens: Sequence[str],
    scope_segments: Sequence[str],
    repo_root: Path,
) -> bool:
    """True iff ``path`` is in the scan surface AND contains a banned token.

    ``scope_segments`` are path segments any one of which must appear in the
    file's repo-relative path for it to be in scope (e.g. an examples directory
    anywhere in the ancestry). An empty ``scope_segments`` means every in-scope
    extension is scanned. A decode error returns False (binary / unreadable
    files carry no readable identity to leak).
    """
    try:
        rel = path.resolve().relative_to(repo_root).as_posix()
    except ValueError:
        rel = path.as_posix()
    if scope_segments and not any(seg in rel.split("/") for seg in scope_segments):
        return False
    try:
        text = None
    except (UnicodeDecodeError, OSError):
        return False
    return any(_compile_token(tok).search(text) for tok in tokens)


def x_file_has_real_name__mutmut_12(
    path: Path,
    *,
    tokens: Sequence[str],
    scope_segments: Sequence[str],
    repo_root: Path,
) -> bool:
    """True iff ``path`` is in the scan surface AND contains a banned token.

    ``scope_segments`` are path segments any one of which must appear in the
    file's repo-relative path for it to be in scope (e.g. an examples directory
    anywhere in the ancestry). An empty ``scope_segments`` means every in-scope
    extension is scanned. A decode error returns False (binary / unreadable
    files carry no readable identity to leak).
    """
    try:
        rel = path.resolve().relative_to(repo_root).as_posix()
    except ValueError:
        rel = path.as_posix()
    if scope_segments and not any(seg in rel.split("/") for seg in scope_segments):
        return False
    try:
        text = path.read_text(encoding=None)
    except (UnicodeDecodeError, OSError):
        return False
    return any(_compile_token(tok).search(text) for tok in tokens)


def x_file_has_real_name__mutmut_13(
    path: Path,
    *,
    tokens: Sequence[str],
    scope_segments: Sequence[str],
    repo_root: Path,
) -> bool:
    """True iff ``path`` is in the scan surface AND contains a banned token.

    ``scope_segments`` are path segments any one of which must appear in the
    file's repo-relative path for it to be in scope (e.g. an examples directory
    anywhere in the ancestry). An empty ``scope_segments`` means every in-scope
    extension is scanned. A decode error returns False (binary / unreadable
    files carry no readable identity to leak).
    """
    try:
        rel = path.resolve().relative_to(repo_root).as_posix()
    except ValueError:
        rel = path.as_posix()
    if scope_segments and not any(seg in rel.split("/") for seg in scope_segments):
        return False
    try:
        text = path.read_text(encoding="XXutf-8XX")
    except (UnicodeDecodeError, OSError):
        return False
    return any(_compile_token(tok).search(text) for tok in tokens)


def x_file_has_real_name__mutmut_14(
    path: Path,
    *,
    tokens: Sequence[str],
    scope_segments: Sequence[str],
    repo_root: Path,
) -> bool:
    """True iff ``path`` is in the scan surface AND contains a banned token.

    ``scope_segments`` are path segments any one of which must appear in the
    file's repo-relative path for it to be in scope (e.g. an examples directory
    anywhere in the ancestry). An empty ``scope_segments`` means every in-scope
    extension is scanned. A decode error returns False (binary / unreadable
    files carry no readable identity to leak).
    """
    try:
        rel = path.resolve().relative_to(repo_root).as_posix()
    except ValueError:
        rel = path.as_posix()
    if scope_segments and not any(seg in rel.split("/") for seg in scope_segments):
        return False
    try:
        text = path.read_text(encoding="UTF-8")
    except (UnicodeDecodeError, OSError):
        return False
    return any(_compile_token(tok).search(text) for tok in tokens)


def x_file_has_real_name__mutmut_15(
    path: Path,
    *,
    tokens: Sequence[str],
    scope_segments: Sequence[str],
    repo_root: Path,
) -> bool:
    """True iff ``path`` is in the scan surface AND contains a banned token.

    ``scope_segments`` are path segments any one of which must appear in the
    file's repo-relative path for it to be in scope (e.g. an examples directory
    anywhere in the ancestry). An empty ``scope_segments`` means every in-scope
    extension is scanned. A decode error returns False (binary / unreadable
    files carry no readable identity to leak).
    """
    try:
        rel = path.resolve().relative_to(repo_root).as_posix()
    except ValueError:
        rel = path.as_posix()
    if scope_segments and not any(seg in rel.split("/") for seg in scope_segments):
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return True
    return any(_compile_token(tok).search(text) for tok in tokens)


def x_file_has_real_name__mutmut_16(
    path: Path,
    *,
    tokens: Sequence[str],
    scope_segments: Sequence[str],
    repo_root: Path,
) -> bool:
    """True iff ``path`` is in the scan surface AND contains a banned token.

    ``scope_segments`` are path segments any one of which must appear in the
    file's repo-relative path for it to be in scope (e.g. an examples directory
    anywhere in the ancestry). An empty ``scope_segments`` means every in-scope
    extension is scanned. A decode error returns False (binary / unreadable
    files carry no readable identity to leak).
    """
    try:
        rel = path.resolve().relative_to(repo_root).as_posix()
    except ValueError:
        rel = path.as_posix()
    if scope_segments and not any(seg in rel.split("/") for seg in scope_segments):
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return False
    return any(None)


def x_file_has_real_name__mutmut_17(
    path: Path,
    *,
    tokens: Sequence[str],
    scope_segments: Sequence[str],
    repo_root: Path,
) -> bool:
    """True iff ``path`` is in the scan surface AND contains a banned token.

    ``scope_segments`` are path segments any one of which must appear in the
    file's repo-relative path for it to be in scope (e.g. an examples directory
    anywhere in the ancestry). An empty ``scope_segments`` means every in-scope
    extension is scanned. A decode error returns False (binary / unreadable
    files carry no readable identity to leak).
    """
    try:
        rel = path.resolve().relative_to(repo_root).as_posix()
    except ValueError:
        rel = path.as_posix()
    if scope_segments and not any(seg in rel.split("/") for seg in scope_segments):
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return False
    return any(_compile_token(tok).search(None) for tok in tokens)


def x_file_has_real_name__mutmut_18(
    path: Path,
    *,
    tokens: Sequence[str],
    scope_segments: Sequence[str],
    repo_root: Path,
) -> bool:
    """True iff ``path`` is in the scan surface AND contains a banned token.

    ``scope_segments`` are path segments any one of which must appear in the
    file's repo-relative path for it to be in scope (e.g. an examples directory
    anywhere in the ancestry). An empty ``scope_segments`` means every in-scope
    extension is scanned. A decode error returns False (binary / unreadable
    files carry no readable identity to leak).
    """
    try:
        rel = path.resolve().relative_to(repo_root).as_posix()
    except ValueError:
        rel = path.as_posix()
    if scope_segments and not any(seg in rel.split("/") for seg in scope_segments):
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return False
    return any(_compile_token(None).search(text) for tok in tokens)

mutants_x_file_has_real_name__mutmut['_mutmut_orig'] = x_file_has_real_name__mutmut_orig # type: ignore # mutmut generated
mutants_x_file_has_real_name__mutmut['x_file_has_real_name__mutmut_1'] = x_file_has_real_name__mutmut_1 # type: ignore # mutmut generated
mutants_x_file_has_real_name__mutmut['x_file_has_real_name__mutmut_2'] = x_file_has_real_name__mutmut_2 # type: ignore # mutmut generated
mutants_x_file_has_real_name__mutmut['x_file_has_real_name__mutmut_3'] = x_file_has_real_name__mutmut_3 # type: ignore # mutmut generated
mutants_x_file_has_real_name__mutmut['x_file_has_real_name__mutmut_4'] = x_file_has_real_name__mutmut_4 # type: ignore # mutmut generated
mutants_x_file_has_real_name__mutmut['x_file_has_real_name__mutmut_5'] = x_file_has_real_name__mutmut_5 # type: ignore # mutmut generated
mutants_x_file_has_real_name__mutmut['x_file_has_real_name__mutmut_6'] = x_file_has_real_name__mutmut_6 # type: ignore # mutmut generated
mutants_x_file_has_real_name__mutmut['x_file_has_real_name__mutmut_7'] = x_file_has_real_name__mutmut_7 # type: ignore # mutmut generated
mutants_x_file_has_real_name__mutmut['x_file_has_real_name__mutmut_8'] = x_file_has_real_name__mutmut_8 # type: ignore # mutmut generated
mutants_x_file_has_real_name__mutmut['x_file_has_real_name__mutmut_9'] = x_file_has_real_name__mutmut_9 # type: ignore # mutmut generated
mutants_x_file_has_real_name__mutmut['x_file_has_real_name__mutmut_10'] = x_file_has_real_name__mutmut_10 # type: ignore # mutmut generated
mutants_x_file_has_real_name__mutmut['x_file_has_real_name__mutmut_11'] = x_file_has_real_name__mutmut_11 # type: ignore # mutmut generated
mutants_x_file_has_real_name__mutmut['x_file_has_real_name__mutmut_12'] = x_file_has_real_name__mutmut_12 # type: ignore # mutmut generated
mutants_x_file_has_real_name__mutmut['x_file_has_real_name__mutmut_13'] = x_file_has_real_name__mutmut_13 # type: ignore # mutmut generated
mutants_x_file_has_real_name__mutmut['x_file_has_real_name__mutmut_14'] = x_file_has_real_name__mutmut_14 # type: ignore # mutmut generated
mutants_x_file_has_real_name__mutmut['x_file_has_real_name__mutmut_15'] = x_file_has_real_name__mutmut_15 # type: ignore # mutmut generated
mutants_x_file_has_real_name__mutmut['x_file_has_real_name__mutmut_16'] = x_file_has_real_name__mutmut_16 # type: ignore # mutmut generated
mutants_x_file_has_real_name__mutmut['x_file_has_real_name__mutmut_17'] = x_file_has_real_name__mutmut_17 # type: ignore # mutmut generated
mutants_x_file_has_real_name__mutmut['x_file_has_real_name__mutmut_18'] = x_file_has_real_name__mutmut_18 # type: ignore # mutmut generated
mutants_xǁNoRealNamesǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁNoRealNamesǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore


class NoRealNames(FitnessRule):
    """Flags fixtures / examples that carry a banned real-name token."""

    name = "no-real-names"
    remediation = REMEDIATION
    extensions = DEFAULT_EXTENSIONS

    #: Rule-specific config (instance attrs so from_config can override them).
    #: ``tokens`` is the set of banned name literals the consumer supplies;
    #: ``scope_segments`` narrows the scan to directories whose name appears as
    #: a path segment (e.g. an ``examples`` dir anywhere in the tree).
    tokens: tuple[str, ...] = ()
    scope_segments: tuple[str, ...] = ()

    @classmethod
    @_mutmut_mutated(mutants_xǁNoRealNamesǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoRealNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoRealNames)  # noqa: S101  # narrowing for mypy
        # Accept either a flat list of banned tokens, or a {token: substitute}
        # map (the substitute is surfaced only in remediation prose, so the
        # detector keys on the token set either way).
        raw_tokens = config.get("tokens")
        if raw_tokens is None:
            mapping = config.get("substitutions")
            raw_tokens = list(mapping) if isinstance(mapping, Mapping) else []
        rule.tokens = tuple(raw_tokens)
        rule.scope_segments = tuple(config.get("scope_segments", ()))
        return rule

    @classmethod
    def xǁNoRealNamesǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoRealNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoRealNames)  # noqa: S101  # narrowing for mypy
        # Accept either a flat list of banned tokens, or a {token: substitute}
        # map (the substitute is surfaced only in remediation prose, so the
        # detector keys on the token set either way).
        raw_tokens = config.get("tokens")
        if raw_tokens is None:
            mapping = config.get("substitutions")
            raw_tokens = list(mapping) if isinstance(mapping, Mapping) else []
        rule.tokens = tuple(raw_tokens)
        rule.scope_segments = tuple(config.get("scope_segments", ()))
        return rule

    @classmethod
    def xǁNoRealNamesǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoRealNames:
        rule = None
        assert isinstance(rule, NoRealNames)  # noqa: S101  # narrowing for mypy
        # Accept either a flat list of banned tokens, or a {token: substitute}
        # map (the substitute is surfaced only in remediation prose, so the
        # detector keys on the token set either way).
        raw_tokens = config.get("tokens")
        if raw_tokens is None:
            mapping = config.get("substitutions")
            raw_tokens = list(mapping) if isinstance(mapping, Mapping) else []
        rule.tokens = tuple(raw_tokens)
        rule.scope_segments = tuple(config.get("scope_segments", ()))
        return rule

    @classmethod
    def xǁNoRealNamesǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoRealNames:
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, NoRealNames)  # noqa: S101  # narrowing for mypy
        # Accept either a flat list of banned tokens, or a {token: substitute}
        # map (the substitute is surfaced only in remediation prose, so the
        # detector keys on the token set either way).
        raw_tokens = config.get("tokens")
        if raw_tokens is None:
            mapping = config.get("substitutions")
            raw_tokens = list(mapping) if isinstance(mapping, Mapping) else []
        rule.tokens = tuple(raw_tokens)
        rule.scope_segments = tuple(config.get("scope_segments", ()))
        return rule

    @classmethod
    def xǁNoRealNamesǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoRealNames:
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, NoRealNames)  # noqa: S101  # narrowing for mypy
        # Accept either a flat list of banned tokens, or a {token: substitute}
        # map (the substitute is surfaced only in remediation prose, so the
        # detector keys on the token set either way).
        raw_tokens = config.get("tokens")
        if raw_tokens is None:
            mapping = config.get("substitutions")
            raw_tokens = list(mapping) if isinstance(mapping, Mapping) else []
        rule.tokens = tuple(raw_tokens)
        rule.scope_segments = tuple(config.get("scope_segments", ()))
        return rule

    @classmethod
    def xǁNoRealNamesǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoRealNames:
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, NoRealNames)  # noqa: S101  # narrowing for mypy
        # Accept either a flat list of banned tokens, or a {token: substitute}
        # map (the substitute is surfaced only in remediation prose, so the
        # detector keys on the token set either way).
        raw_tokens = config.get("tokens")
        if raw_tokens is None:
            mapping = config.get("substitutions")
            raw_tokens = list(mapping) if isinstance(mapping, Mapping) else []
        rule.tokens = tuple(raw_tokens)
        rule.scope_segments = tuple(config.get("scope_segments", ()))
        return rule

    @classmethod
    def xǁNoRealNamesǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoRealNames:
        rule = super().from_config(config, )
        assert isinstance(rule, NoRealNames)  # noqa: S101  # narrowing for mypy
        # Accept either a flat list of banned tokens, or a {token: substitute}
        # map (the substitute is surfaced only in remediation prose, so the
        # detector keys on the token set either way).
        raw_tokens = config.get("tokens")
        if raw_tokens is None:
            mapping = config.get("substitutions")
            raw_tokens = list(mapping) if isinstance(mapping, Mapping) else []
        rule.tokens = tuple(raw_tokens)
        rule.scope_segments = tuple(config.get("scope_segments", ()))
        return rule

    @classmethod
    def xǁNoRealNamesǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoRealNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoRealNames)  # noqa: S101  # narrowing for mypy
        # Accept either a flat list of banned tokens, or a {token: substitute}
        # map (the substitute is surfaced only in remediation prose, so the
        # detector keys on the token set either way).
        raw_tokens = None
        if raw_tokens is None:
            mapping = config.get("substitutions")
            raw_tokens = list(mapping) if isinstance(mapping, Mapping) else []
        rule.tokens = tuple(raw_tokens)
        rule.scope_segments = tuple(config.get("scope_segments", ()))
        return rule

    @classmethod
    def xǁNoRealNamesǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoRealNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoRealNames)  # noqa: S101  # narrowing for mypy
        # Accept either a flat list of banned tokens, or a {token: substitute}
        # map (the substitute is surfaced only in remediation prose, so the
        # detector keys on the token set either way).
        raw_tokens = config.get(None)
        if raw_tokens is None:
            mapping = config.get("substitutions")
            raw_tokens = list(mapping) if isinstance(mapping, Mapping) else []
        rule.tokens = tuple(raw_tokens)
        rule.scope_segments = tuple(config.get("scope_segments", ()))
        return rule

    @classmethod
    def xǁNoRealNamesǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoRealNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoRealNames)  # noqa: S101  # narrowing for mypy
        # Accept either a flat list of banned tokens, or a {token: substitute}
        # map (the substitute is surfaced only in remediation prose, so the
        # detector keys on the token set either way).
        raw_tokens = config.get("XXtokensXX")
        if raw_tokens is None:
            mapping = config.get("substitutions")
            raw_tokens = list(mapping) if isinstance(mapping, Mapping) else []
        rule.tokens = tuple(raw_tokens)
        rule.scope_segments = tuple(config.get("scope_segments", ()))
        return rule

    @classmethod
    def xǁNoRealNamesǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoRealNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoRealNames)  # noqa: S101  # narrowing for mypy
        # Accept either a flat list of banned tokens, or a {token: substitute}
        # map (the substitute is surfaced only in remediation prose, so the
        # detector keys on the token set either way).
        raw_tokens = config.get("TOKENS")
        if raw_tokens is None:
            mapping = config.get("substitutions")
            raw_tokens = list(mapping) if isinstance(mapping, Mapping) else []
        rule.tokens = tuple(raw_tokens)
        rule.scope_segments = tuple(config.get("scope_segments", ()))
        return rule

    @classmethod
    def xǁNoRealNamesǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoRealNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoRealNames)  # noqa: S101  # narrowing for mypy
        # Accept either a flat list of banned tokens, or a {token: substitute}
        # map (the substitute is surfaced only in remediation prose, so the
        # detector keys on the token set either way).
        raw_tokens = config.get("tokens")
        if raw_tokens is not None:
            mapping = config.get("substitutions")
            raw_tokens = list(mapping) if isinstance(mapping, Mapping) else []
        rule.tokens = tuple(raw_tokens)
        rule.scope_segments = tuple(config.get("scope_segments", ()))
        return rule

    @classmethod
    def xǁNoRealNamesǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoRealNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoRealNames)  # noqa: S101  # narrowing for mypy
        # Accept either a flat list of banned tokens, or a {token: substitute}
        # map (the substitute is surfaced only in remediation prose, so the
        # detector keys on the token set either way).
        raw_tokens = config.get("tokens")
        if raw_tokens is None:
            mapping = None
            raw_tokens = list(mapping) if isinstance(mapping, Mapping) else []
        rule.tokens = tuple(raw_tokens)
        rule.scope_segments = tuple(config.get("scope_segments", ()))
        return rule

    @classmethod
    def xǁNoRealNamesǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoRealNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoRealNames)  # noqa: S101  # narrowing for mypy
        # Accept either a flat list of banned tokens, or a {token: substitute}
        # map (the substitute is surfaced only in remediation prose, so the
        # detector keys on the token set either way).
        raw_tokens = config.get("tokens")
        if raw_tokens is None:
            mapping = config.get(None)
            raw_tokens = list(mapping) if isinstance(mapping, Mapping) else []
        rule.tokens = tuple(raw_tokens)
        rule.scope_segments = tuple(config.get("scope_segments", ()))
        return rule

    @classmethod
    def xǁNoRealNamesǁfrom_config__mutmut_13(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoRealNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoRealNames)  # noqa: S101  # narrowing for mypy
        # Accept either a flat list of banned tokens, or a {token: substitute}
        # map (the substitute is surfaced only in remediation prose, so the
        # detector keys on the token set either way).
        raw_tokens = config.get("tokens")
        if raw_tokens is None:
            mapping = config.get("XXsubstitutionsXX")
            raw_tokens = list(mapping) if isinstance(mapping, Mapping) else []
        rule.tokens = tuple(raw_tokens)
        rule.scope_segments = tuple(config.get("scope_segments", ()))
        return rule

    @classmethod
    def xǁNoRealNamesǁfrom_config__mutmut_14(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoRealNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoRealNames)  # noqa: S101  # narrowing for mypy
        # Accept either a flat list of banned tokens, or a {token: substitute}
        # map (the substitute is surfaced only in remediation prose, so the
        # detector keys on the token set either way).
        raw_tokens = config.get("tokens")
        if raw_tokens is None:
            mapping = config.get("SUBSTITUTIONS")
            raw_tokens = list(mapping) if isinstance(mapping, Mapping) else []
        rule.tokens = tuple(raw_tokens)
        rule.scope_segments = tuple(config.get("scope_segments", ()))
        return rule

    @classmethod
    def xǁNoRealNamesǁfrom_config__mutmut_15(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoRealNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoRealNames)  # noqa: S101  # narrowing for mypy
        # Accept either a flat list of banned tokens, or a {token: substitute}
        # map (the substitute is surfaced only in remediation prose, so the
        # detector keys on the token set either way).
        raw_tokens = config.get("tokens")
        if raw_tokens is None:
            mapping = config.get("substitutions")
            raw_tokens = None
        rule.tokens = tuple(raw_tokens)
        rule.scope_segments = tuple(config.get("scope_segments", ()))
        return rule

    @classmethod
    def xǁNoRealNamesǁfrom_config__mutmut_16(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoRealNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoRealNames)  # noqa: S101  # narrowing for mypy
        # Accept either a flat list of banned tokens, or a {token: substitute}
        # map (the substitute is surfaced only in remediation prose, so the
        # detector keys on the token set either way).
        raw_tokens = config.get("tokens")
        if raw_tokens is None:
            mapping = config.get("substitutions")
            raw_tokens = list(None) if isinstance(mapping, Mapping) else []
        rule.tokens = tuple(raw_tokens)
        rule.scope_segments = tuple(config.get("scope_segments", ()))
        return rule

    @classmethod
    def xǁNoRealNamesǁfrom_config__mutmut_17(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoRealNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoRealNames)  # noqa: S101  # narrowing for mypy
        # Accept either a flat list of banned tokens, or a {token: substitute}
        # map (the substitute is surfaced only in remediation prose, so the
        # detector keys on the token set either way).
        raw_tokens = config.get("tokens")
        if raw_tokens is None:
            mapping = config.get("substitutions")
            raw_tokens = list(mapping) if isinstance(mapping, Mapping) else []
        rule.tokens = None
        rule.scope_segments = tuple(config.get("scope_segments", ()))
        return rule

    @classmethod
    def xǁNoRealNamesǁfrom_config__mutmut_18(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoRealNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoRealNames)  # noqa: S101  # narrowing for mypy
        # Accept either a flat list of banned tokens, or a {token: substitute}
        # map (the substitute is surfaced only in remediation prose, so the
        # detector keys on the token set either way).
        raw_tokens = config.get("tokens")
        if raw_tokens is None:
            mapping = config.get("substitutions")
            raw_tokens = list(mapping) if isinstance(mapping, Mapping) else []
        rule.tokens = tuple(None)
        rule.scope_segments = tuple(config.get("scope_segments", ()))
        return rule

    @classmethod
    def xǁNoRealNamesǁfrom_config__mutmut_19(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoRealNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoRealNames)  # noqa: S101  # narrowing for mypy
        # Accept either a flat list of banned tokens, or a {token: substitute}
        # map (the substitute is surfaced only in remediation prose, so the
        # detector keys on the token set either way).
        raw_tokens = config.get("tokens")
        if raw_tokens is None:
            mapping = config.get("substitutions")
            raw_tokens = list(mapping) if isinstance(mapping, Mapping) else []
        rule.tokens = tuple(raw_tokens)
        rule.scope_segments = None
        return rule

    @classmethod
    def xǁNoRealNamesǁfrom_config__mutmut_20(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoRealNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoRealNames)  # noqa: S101  # narrowing for mypy
        # Accept either a flat list of banned tokens, or a {token: substitute}
        # map (the substitute is surfaced only in remediation prose, so the
        # detector keys on the token set either way).
        raw_tokens = config.get("tokens")
        if raw_tokens is None:
            mapping = config.get("substitutions")
            raw_tokens = list(mapping) if isinstance(mapping, Mapping) else []
        rule.tokens = tuple(raw_tokens)
        rule.scope_segments = tuple(None)
        return rule

    @classmethod
    def xǁNoRealNamesǁfrom_config__mutmut_21(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoRealNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoRealNames)  # noqa: S101  # narrowing for mypy
        # Accept either a flat list of banned tokens, or a {token: substitute}
        # map (the substitute is surfaced only in remediation prose, so the
        # detector keys on the token set either way).
        raw_tokens = config.get("tokens")
        if raw_tokens is None:
            mapping = config.get("substitutions")
            raw_tokens = list(mapping) if isinstance(mapping, Mapping) else []
        rule.tokens = tuple(raw_tokens)
        rule.scope_segments = tuple(config.get(None, ()))
        return rule

    @classmethod
    def xǁNoRealNamesǁfrom_config__mutmut_22(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoRealNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoRealNames)  # noqa: S101  # narrowing for mypy
        # Accept either a flat list of banned tokens, or a {token: substitute}
        # map (the substitute is surfaced only in remediation prose, so the
        # detector keys on the token set either way).
        raw_tokens = config.get("tokens")
        if raw_tokens is None:
            mapping = config.get("substitutions")
            raw_tokens = list(mapping) if isinstance(mapping, Mapping) else []
        rule.tokens = tuple(raw_tokens)
        rule.scope_segments = tuple(config.get("scope_segments", None))
        return rule

    @classmethod
    def xǁNoRealNamesǁfrom_config__mutmut_23(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoRealNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoRealNames)  # noqa: S101  # narrowing for mypy
        # Accept either a flat list of banned tokens, or a {token: substitute}
        # map (the substitute is surfaced only in remediation prose, so the
        # detector keys on the token set either way).
        raw_tokens = config.get("tokens")
        if raw_tokens is None:
            mapping = config.get("substitutions")
            raw_tokens = list(mapping) if isinstance(mapping, Mapping) else []
        rule.tokens = tuple(raw_tokens)
        rule.scope_segments = tuple(config.get(()))
        return rule

    @classmethod
    def xǁNoRealNamesǁfrom_config__mutmut_24(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoRealNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoRealNames)  # noqa: S101  # narrowing for mypy
        # Accept either a flat list of banned tokens, or a {token: substitute}
        # map (the substitute is surfaced only in remediation prose, so the
        # detector keys on the token set either way).
        raw_tokens = config.get("tokens")
        if raw_tokens is None:
            mapping = config.get("substitutions")
            raw_tokens = list(mapping) if isinstance(mapping, Mapping) else []
        rule.tokens = tuple(raw_tokens)
        rule.scope_segments = tuple(config.get("scope_segments", ))
        return rule

    @classmethod
    def xǁNoRealNamesǁfrom_config__mutmut_25(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoRealNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoRealNames)  # noqa: S101  # narrowing for mypy
        # Accept either a flat list of banned tokens, or a {token: substitute}
        # map (the substitute is surfaced only in remediation prose, so the
        # detector keys on the token set either way).
        raw_tokens = config.get("tokens")
        if raw_tokens is None:
            mapping = config.get("substitutions")
            raw_tokens = list(mapping) if isinstance(mapping, Mapping) else []
        rule.tokens = tuple(raw_tokens)
        rule.scope_segments = tuple(config.get("XXscope_segmentsXX", ()))
        return rule

    @classmethod
    def xǁNoRealNamesǁfrom_config__mutmut_26(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoRealNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoRealNames)  # noqa: S101  # narrowing for mypy
        # Accept either a flat list of banned tokens, or a {token: substitute}
        # map (the substitute is surfaced only in remediation prose, so the
        # detector keys on the token set either way).
        raw_tokens = config.get("tokens")
        if raw_tokens is None:
            mapping = config.get("substitutions")
            raw_tokens = list(mapping) if isinstance(mapping, Mapping) else []
        rule.tokens = tuple(raw_tokens)
        rule.scope_segments = tuple(config.get("SCOPE_SEGMENTS", ()))
        return rule

    @_mutmut_mutated(mutants_xǁNoRealNamesǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        if not self.tokens:
            return False
        return file_has_real_name(
            path,
            tokens=self.tokens,
            scope_segments=self.scope_segments,
            repo_root=self._repo_root,
        )

    def xǁNoRealNamesǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        if not self.tokens:
            return False
        return file_has_real_name(
            path,
            tokens=self.tokens,
            scope_segments=self.scope_segments,
            repo_root=self._repo_root,
        )

    def xǁNoRealNamesǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        if self.tokens:
            return False
        return file_has_real_name(
            path,
            tokens=self.tokens,
            scope_segments=self.scope_segments,
            repo_root=self._repo_root,
        )

    def xǁNoRealNamesǁfile_has_violation__mutmut_2(self, path: Path) -> bool:
        if not self.tokens:
            return True
        return file_has_real_name(
            path,
            tokens=self.tokens,
            scope_segments=self.scope_segments,
            repo_root=self._repo_root,
        )

    def xǁNoRealNamesǁfile_has_violation__mutmut_3(self, path: Path) -> bool:
        if not self.tokens:
            return False
        return file_has_real_name(
            None,
            tokens=self.tokens,
            scope_segments=self.scope_segments,
            repo_root=self._repo_root,
        )

    def xǁNoRealNamesǁfile_has_violation__mutmut_4(self, path: Path) -> bool:
        if not self.tokens:
            return False
        return file_has_real_name(
            path,
            tokens=None,
            scope_segments=self.scope_segments,
            repo_root=self._repo_root,
        )

    def xǁNoRealNamesǁfile_has_violation__mutmut_5(self, path: Path) -> bool:
        if not self.tokens:
            return False
        return file_has_real_name(
            path,
            tokens=self.tokens,
            scope_segments=None,
            repo_root=self._repo_root,
        )

    def xǁNoRealNamesǁfile_has_violation__mutmut_6(self, path: Path) -> bool:
        if not self.tokens:
            return False
        return file_has_real_name(
            path,
            tokens=self.tokens,
            scope_segments=self.scope_segments,
            repo_root=None,
        )

    def xǁNoRealNamesǁfile_has_violation__mutmut_7(self, path: Path) -> bool:
        if not self.tokens:
            return False
        return file_has_real_name(
            tokens=self.tokens,
            scope_segments=self.scope_segments,
            repo_root=self._repo_root,
        )

    def xǁNoRealNamesǁfile_has_violation__mutmut_8(self, path: Path) -> bool:
        if not self.tokens:
            return False
        return file_has_real_name(
            path,
            scope_segments=self.scope_segments,
            repo_root=self._repo_root,
        )

    def xǁNoRealNamesǁfile_has_violation__mutmut_9(self, path: Path) -> bool:
        if not self.tokens:
            return False
        return file_has_real_name(
            path,
            tokens=self.tokens,
            repo_root=self._repo_root,
        )

    def xǁNoRealNamesǁfile_has_violation__mutmut_10(self, path: Path) -> bool:
        if not self.tokens:
            return False
        return file_has_real_name(
            path,
            tokens=self.tokens,
            scope_segments=self.scope_segments,
            )

mutants_xǁNoRealNamesǁfrom_config__mutmut['_mutmut_orig'] = NoRealNames.xǁNoRealNamesǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNoRealNamesǁfrom_config__mutmut['xǁNoRealNamesǁfrom_config__mutmut_1'] = NoRealNames.xǁNoRealNamesǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNoRealNamesǁfrom_config__mutmut['xǁNoRealNamesǁfrom_config__mutmut_2'] = NoRealNames.xǁNoRealNamesǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNoRealNamesǁfrom_config__mutmut['xǁNoRealNamesǁfrom_config__mutmut_3'] = NoRealNames.xǁNoRealNamesǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNoRealNamesǁfrom_config__mutmut['xǁNoRealNamesǁfrom_config__mutmut_4'] = NoRealNames.xǁNoRealNamesǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁNoRealNamesǁfrom_config__mutmut['xǁNoRealNamesǁfrom_config__mutmut_5'] = NoRealNames.xǁNoRealNamesǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁNoRealNamesǁfrom_config__mutmut['xǁNoRealNamesǁfrom_config__mutmut_6'] = NoRealNames.xǁNoRealNamesǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁNoRealNamesǁfrom_config__mutmut['xǁNoRealNamesǁfrom_config__mutmut_7'] = NoRealNames.xǁNoRealNamesǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁNoRealNamesǁfrom_config__mutmut['xǁNoRealNamesǁfrom_config__mutmut_8'] = NoRealNames.xǁNoRealNamesǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁNoRealNamesǁfrom_config__mutmut['xǁNoRealNamesǁfrom_config__mutmut_9'] = NoRealNames.xǁNoRealNamesǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁNoRealNamesǁfrom_config__mutmut['xǁNoRealNamesǁfrom_config__mutmut_10'] = NoRealNames.xǁNoRealNamesǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁNoRealNamesǁfrom_config__mutmut['xǁNoRealNamesǁfrom_config__mutmut_11'] = NoRealNames.xǁNoRealNamesǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁNoRealNamesǁfrom_config__mutmut['xǁNoRealNamesǁfrom_config__mutmut_12'] = NoRealNames.xǁNoRealNamesǁfrom_config__mutmut_12 # type: ignore # mutmut generated
mutants_xǁNoRealNamesǁfrom_config__mutmut['xǁNoRealNamesǁfrom_config__mutmut_13'] = NoRealNames.xǁNoRealNamesǁfrom_config__mutmut_13 # type: ignore # mutmut generated
mutants_xǁNoRealNamesǁfrom_config__mutmut['xǁNoRealNamesǁfrom_config__mutmut_14'] = NoRealNames.xǁNoRealNamesǁfrom_config__mutmut_14 # type: ignore # mutmut generated
mutants_xǁNoRealNamesǁfrom_config__mutmut['xǁNoRealNamesǁfrom_config__mutmut_15'] = NoRealNames.xǁNoRealNamesǁfrom_config__mutmut_15 # type: ignore # mutmut generated
mutants_xǁNoRealNamesǁfrom_config__mutmut['xǁNoRealNamesǁfrom_config__mutmut_16'] = NoRealNames.xǁNoRealNamesǁfrom_config__mutmut_16 # type: ignore # mutmut generated
mutants_xǁNoRealNamesǁfrom_config__mutmut['xǁNoRealNamesǁfrom_config__mutmut_17'] = NoRealNames.xǁNoRealNamesǁfrom_config__mutmut_17 # type: ignore # mutmut generated
mutants_xǁNoRealNamesǁfrom_config__mutmut['xǁNoRealNamesǁfrom_config__mutmut_18'] = NoRealNames.xǁNoRealNamesǁfrom_config__mutmut_18 # type: ignore # mutmut generated
mutants_xǁNoRealNamesǁfrom_config__mutmut['xǁNoRealNamesǁfrom_config__mutmut_19'] = NoRealNames.xǁNoRealNamesǁfrom_config__mutmut_19 # type: ignore # mutmut generated
mutants_xǁNoRealNamesǁfrom_config__mutmut['xǁNoRealNamesǁfrom_config__mutmut_20'] = NoRealNames.xǁNoRealNamesǁfrom_config__mutmut_20 # type: ignore # mutmut generated
mutants_xǁNoRealNamesǁfrom_config__mutmut['xǁNoRealNamesǁfrom_config__mutmut_21'] = NoRealNames.xǁNoRealNamesǁfrom_config__mutmut_21 # type: ignore # mutmut generated
mutants_xǁNoRealNamesǁfrom_config__mutmut['xǁNoRealNamesǁfrom_config__mutmut_22'] = NoRealNames.xǁNoRealNamesǁfrom_config__mutmut_22 # type: ignore # mutmut generated
mutants_xǁNoRealNamesǁfrom_config__mutmut['xǁNoRealNamesǁfrom_config__mutmut_23'] = NoRealNames.xǁNoRealNamesǁfrom_config__mutmut_23 # type: ignore # mutmut generated
mutants_xǁNoRealNamesǁfrom_config__mutmut['xǁNoRealNamesǁfrom_config__mutmut_24'] = NoRealNames.xǁNoRealNamesǁfrom_config__mutmut_24 # type: ignore # mutmut generated
mutants_xǁNoRealNamesǁfrom_config__mutmut['xǁNoRealNamesǁfrom_config__mutmut_25'] = NoRealNames.xǁNoRealNamesǁfrom_config__mutmut_25 # type: ignore # mutmut generated
mutants_xǁNoRealNamesǁfrom_config__mutmut['xǁNoRealNamesǁfrom_config__mutmut_26'] = NoRealNames.xǁNoRealNamesǁfrom_config__mutmut_26 # type: ignore # mutmut generated

mutants_xǁNoRealNamesǁfile_has_violation__mutmut['_mutmut_orig'] = NoRealNames.xǁNoRealNamesǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNoRealNamesǁfile_has_violation__mutmut['xǁNoRealNamesǁfile_has_violation__mutmut_1'] = NoRealNames.xǁNoRealNamesǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNoRealNamesǁfile_has_violation__mutmut['xǁNoRealNamesǁfile_has_violation__mutmut_2'] = NoRealNames.xǁNoRealNamesǁfile_has_violation__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNoRealNamesǁfile_has_violation__mutmut['xǁNoRealNamesǁfile_has_violation__mutmut_3'] = NoRealNames.xǁNoRealNamesǁfile_has_violation__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNoRealNamesǁfile_has_violation__mutmut['xǁNoRealNamesǁfile_has_violation__mutmut_4'] = NoRealNames.xǁNoRealNamesǁfile_has_violation__mutmut_4 # type: ignore # mutmut generated
mutants_xǁNoRealNamesǁfile_has_violation__mutmut['xǁNoRealNamesǁfile_has_violation__mutmut_5'] = NoRealNames.xǁNoRealNamesǁfile_has_violation__mutmut_5 # type: ignore # mutmut generated
mutants_xǁNoRealNamesǁfile_has_violation__mutmut['xǁNoRealNamesǁfile_has_violation__mutmut_6'] = NoRealNames.xǁNoRealNamesǁfile_has_violation__mutmut_6 # type: ignore # mutmut generated
mutants_xǁNoRealNamesǁfile_has_violation__mutmut['xǁNoRealNamesǁfile_has_violation__mutmut_7'] = NoRealNames.xǁNoRealNamesǁfile_has_violation__mutmut_7 # type: ignore # mutmut generated
mutants_xǁNoRealNamesǁfile_has_violation__mutmut['xǁNoRealNamesǁfile_has_violation__mutmut_8'] = NoRealNames.xǁNoRealNamesǁfile_has_violation__mutmut_8 # type: ignore # mutmut generated
mutants_xǁNoRealNamesǁfile_has_violation__mutmut['xǁNoRealNamesǁfile_has_violation__mutmut_9'] = NoRealNames.xǁNoRealNamesǁfile_has_violation__mutmut_9 # type: ignore # mutmut generated
mutants_xǁNoRealNamesǁfile_has_violation__mutmut['xǁNoRealNamesǁfile_has_violation__mutmut_10'] = NoRealNames.xǁNoRealNamesǁfile_has_violation__mutmut_10 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoRealNames:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoRealNames.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoRealNames:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoRealNames.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoRealNames:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoRealNames.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoRealNames:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoRealNames.from_config(config, repo_root=None)


def x_build__mutmut_3(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoRealNames:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoRealNames.from_config(repo_root=repo_root)


def x_build__mutmut_4(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoRealNames:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoRealNames.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoRealNames, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoRealNames, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoRealNames, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoRealNames, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
