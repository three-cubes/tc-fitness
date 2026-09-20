"""CORE check: canonical_commit_identity — commits are authored by allowed identities.

Machine-enforced identity hygiene (Autonomous Delivery Platform SP-A / SGO-158):
every commit in the PR range must carry an author AND committer whose email is
on the consumer's allowlist (the canonical agent GitHub App + named human
maintainers), and — when name patterns are configured — a name matching one of
them (catching emoji/marker-in-name identities like ``Builder 🔨``).

The AUTHOR is held strictly to that allowlist — author identity is what governance
cares about. The COMMITTER is checked against the allowlist UNION an intrinsic set
of platform committers — GitHub's web-flow signer plus Dependabot/Renovate (SGO-198):
GitHub rewrites the committer to ``GitHub <noreply@github.com>`` on every squash/merge
performed through the UI, so gating the committer strictly would fail any scanned
range that includes a merged commit. These platform identities are always allowed as
*committers* so the check can't be broken per-repo by forgetting to allowlist them.

This is a RANGE check, not a file check: the unit of violation is a commit, so
it overrides :meth:`collect_violations` and reads ``git log`` rather than
walking files. It is repo-agnostic — the allowlist, the name patterns, and the
range refs are ALL consumer config; the engine ships no identities.

The configured ``base_ref..head_ref`` range is evaluated in full. With no
allowlist configured the rule is a no-op because no identity policy exists.
"""

from __future__ import annotations

import re
import subprocess
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

DEFAULT_BASE_REF = "origin/main"
DEFAULT_HEAD_REF = "HEAD"

#: Unit-separator delimited git-log record: sha, author name/email, committer name/email.
_SEP = "\x1f"
_FORMAT = _SEP.join(("%H", "%an", "%ae", "%cn", "%ce"))

#: Committers that platform automation stamps onto otherwise-canonical commits and
#: which are therefore ALWAYS allowed as *committers* (never as authors): GitHub's
#: web-flow signer (``GitHub <noreply@github.com>``), set as the committer on every
#: squash/merge performed through the UI, plus the Dependabot and Renovate bot
#: accounts. The committer on a merged or bot-raised commit is the platform, not a
#: rogue identity, so gating it strictly would fail every consumer the moment it
#: accrues merged history (SGO-198). Web-flow is matched by exact email; the bots by
#: the stable ``+<bot>[bot]@users.noreply.github.com`` no-reply suffix GitHub mints.
_WEBFLOW_COMMITTER_EMAIL = "noreply@github.com"
_PLATFORM_COMMITTER_SUFFIXES: tuple[str, ...] = (
    "+dependabot[bot]@users.noreply.github.com",
    "+renovate[bot]@users.noreply.github.com",
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x__is_platform_committer__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__is_platform_committer__mutmut)
def _is_platform_committer(email: str) -> bool:
    """True for the GitHub web-flow / Dependabot / Renovate committer identities."""
    return email == _WEBFLOW_COMMITTER_EMAIL or email.endswith(_PLATFORM_COMMITTER_SUFFIXES)


def x__is_platform_committer__mutmut_orig(email: str) -> bool:
    """True for the GitHub web-flow / Dependabot / Renovate committer identities."""
    return email == _WEBFLOW_COMMITTER_EMAIL or email.endswith(_PLATFORM_COMMITTER_SUFFIXES)


def x__is_platform_committer__mutmut_1(email: str) -> bool:
    """True for the GitHub web-flow / Dependabot / Renovate committer identities."""
    return email == _WEBFLOW_COMMITTER_EMAIL and email.endswith(_PLATFORM_COMMITTER_SUFFIXES)


def x__is_platform_committer__mutmut_2(email: str) -> bool:
    """True for the GitHub web-flow / Dependabot / Renovate committer identities."""
    return email != _WEBFLOW_COMMITTER_EMAIL or email.endswith(_PLATFORM_COMMITTER_SUFFIXES)


def x__is_platform_committer__mutmut_3(email: str) -> bool:
    """True for the GitHub web-flow / Dependabot / Renovate committer identities."""
    return email == _WEBFLOW_COMMITTER_EMAIL or email.endswith(None)

mutants_x__is_platform_committer__mutmut['_mutmut_orig'] = x__is_platform_committer__mutmut_orig # type: ignore # mutmut generated
mutants_x__is_platform_committer__mutmut['x__is_platform_committer__mutmut_1'] = x__is_platform_committer__mutmut_1 # type: ignore # mutmut generated
mutants_x__is_platform_committer__mutmut['x__is_platform_committer__mutmut_2'] = x__is_platform_committer__mutmut_2 # type: ignore # mutmut generated
mutants_x__is_platform_committer__mutmut['x__is_platform_committer__mutmut_3'] = x__is_platform_committer__mutmut_3 # type: ignore # mutmut generated


REMEDIATION = _remediation(
    fix=(
        "set local Git `user.name` and `user.email` to an allowlisted identity, then "
        "amend with `git commit --amend --reset-author` or recreate the affected commits. "
        "Commit metadata does not authenticate GitHub network writes. For push, PR, or "
        "API operations, use the consumer's approved host credential broker; tc-fitness "
        "neither mints nor stores credentials. Add a genuinely new human maintainer to "
        "the check's `allowed_emails` only as a CODEOWNERS-gated control-plane edit."
    ),
    nxt="re-run this check to confirm it goes green.",
    run="python -m tc_fitness.core_checks.canonical_commit_identity",
    passing="Git author + committer metadata = an allowlisted bot or human identity",
    forbidden="author feat-156-deploy <noreply@anthropic.com>  (off-allowlist identity)",
)
mutants_x__log_identities__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__log_identities__mutmut)
def _log_identities(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        ["git", "log", f"--format={_FORMAT}", rev_range],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) == 5:
            rows.append((parts[0], parts[1], parts[2], parts[3], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[0].strip() else "malformed git-log record"
            rows.append((sha, "", "", "", ""))
    return rows


def x__log_identities__mutmut_orig(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        ["git", "log", f"--format={_FORMAT}", rev_range],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) == 5:
            rows.append((parts[0], parts[1], parts[2], parts[3], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[0].strip() else "malformed git-log record"
            rows.append((sha, "", "", "", ""))
    return rows


def x__log_identities__mutmut_1(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = None
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) == 5:
            rows.append((parts[0], parts[1], parts[2], parts[3], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[0].strip() else "malformed git-log record"
            rows.append((sha, "", "", "", ""))
    return rows


def x__log_identities__mutmut_2(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        None,
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) == 5:
            rows.append((parts[0], parts[1], parts[2], parts[3], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[0].strip() else "malformed git-log record"
            rows.append((sha, "", "", "", ""))
    return rows


def x__log_identities__mutmut_3(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        ["git", "log", f"--format={_FORMAT}", rev_range],
        cwd=None,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) == 5:
            rows.append((parts[0], parts[1], parts[2], parts[3], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[0].strip() else "malformed git-log record"
            rows.append((sha, "", "", "", ""))
    return rows


def x__log_identities__mutmut_4(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        ["git", "log", f"--format={_FORMAT}", rev_range],
        cwd=repo_root,
        capture_output=None,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) == 5:
            rows.append((parts[0], parts[1], parts[2], parts[3], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[0].strip() else "malformed git-log record"
            rows.append((sha, "", "", "", ""))
    return rows


def x__log_identities__mutmut_5(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        ["git", "log", f"--format={_FORMAT}", rev_range],
        cwd=repo_root,
        capture_output=True,
        text=None,
        check=False,
    )
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) == 5:
            rows.append((parts[0], parts[1], parts[2], parts[3], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[0].strip() else "malformed git-log record"
            rows.append((sha, "", "", "", ""))
    return rows


def x__log_identities__mutmut_6(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        ["git", "log", f"--format={_FORMAT}", rev_range],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=None,
    )
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) == 5:
            rows.append((parts[0], parts[1], parts[2], parts[3], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[0].strip() else "malformed git-log record"
            rows.append((sha, "", "", "", ""))
    return rows


def x__log_identities__mutmut_7(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) == 5:
            rows.append((parts[0], parts[1], parts[2], parts[3], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[0].strip() else "malformed git-log record"
            rows.append((sha, "", "", "", ""))
    return rows


def x__log_identities__mutmut_8(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        ["git", "log", f"--format={_FORMAT}", rev_range],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) == 5:
            rows.append((parts[0], parts[1], parts[2], parts[3], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[0].strip() else "malformed git-log record"
            rows.append((sha, "", "", "", ""))
    return rows


def x__log_identities__mutmut_9(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        ["git", "log", f"--format={_FORMAT}", rev_range],
        cwd=repo_root,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) == 5:
            rows.append((parts[0], parts[1], parts[2], parts[3], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[0].strip() else "malformed git-log record"
            rows.append((sha, "", "", "", ""))
    return rows


def x__log_identities__mutmut_10(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        ["git", "log", f"--format={_FORMAT}", rev_range],
        cwd=repo_root,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) == 5:
            rows.append((parts[0], parts[1], parts[2], parts[3], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[0].strip() else "malformed git-log record"
            rows.append((sha, "", "", "", ""))
    return rows


def x__log_identities__mutmut_11(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        ["git", "log", f"--format={_FORMAT}", rev_range],
        cwd=repo_root,
        capture_output=True,
        text=True,
        )
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) == 5:
            rows.append((parts[0], parts[1], parts[2], parts[3], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[0].strip() else "malformed git-log record"
            rows.append((sha, "", "", "", ""))
    return rows


def x__log_identities__mutmut_12(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        ["XXgitXX", "log", f"--format={_FORMAT}", rev_range],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) == 5:
            rows.append((parts[0], parts[1], parts[2], parts[3], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[0].strip() else "malformed git-log record"
            rows.append((sha, "", "", "", ""))
    return rows


def x__log_identities__mutmut_13(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        ["GIT", "log", f"--format={_FORMAT}", rev_range],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) == 5:
            rows.append((parts[0], parts[1], parts[2], parts[3], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[0].strip() else "malformed git-log record"
            rows.append((sha, "", "", "", ""))
    return rows


def x__log_identities__mutmut_14(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        ["git", "XXlogXX", f"--format={_FORMAT}", rev_range],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) == 5:
            rows.append((parts[0], parts[1], parts[2], parts[3], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[0].strip() else "malformed git-log record"
            rows.append((sha, "", "", "", ""))
    return rows


def x__log_identities__mutmut_15(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        ["git", "LOG", f"--format={_FORMAT}", rev_range],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) == 5:
            rows.append((parts[0], parts[1], parts[2], parts[3], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[0].strip() else "malformed git-log record"
            rows.append((sha, "", "", "", ""))
    return rows


def x__log_identities__mutmut_16(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        ["git", "log", f"--format={_FORMAT}", rev_range],
        cwd=repo_root,
        capture_output=False,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) == 5:
            rows.append((parts[0], parts[1], parts[2], parts[3], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[0].strip() else "malformed git-log record"
            rows.append((sha, "", "", "", ""))
    return rows


def x__log_identities__mutmut_17(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        ["git", "log", f"--format={_FORMAT}", rev_range],
        cwd=repo_root,
        capture_output=True,
        text=False,
        check=False,
    )
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) == 5:
            rows.append((parts[0], parts[1], parts[2], parts[3], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[0].strip() else "malformed git-log record"
            rows.append((sha, "", "", "", ""))
    return rows


def x__log_identities__mutmut_18(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        ["git", "log", f"--format={_FORMAT}", rev_range],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) == 5:
            rows.append((parts[0], parts[1], parts[2], parts[3], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[0].strip() else "malformed git-log record"
            rows.append((sha, "", "", "", ""))
    return rows


def x__log_identities__mutmut_19(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        ["git", "log", f"--format={_FORMAT}", rev_range],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) == 5:
            rows.append((parts[0], parts[1], parts[2], parts[3], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[0].strip() else "malformed git-log record"
            rows.append((sha, "", "", "", ""))
    return rows


def x__log_identities__mutmut_20(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        ["git", "log", f"--format={_FORMAT}", rev_range],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 1:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) == 5:
            rows.append((parts[0], parts[1], parts[2], parts[3], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[0].strip() else "malformed git-log record"
            rows.append((sha, "", "", "", ""))
    return rows


def x__log_identities__mutmut_21(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        ["git", "log", f"--format={_FORMAT}", rev_range],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = None
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) == 5:
            rows.append((parts[0], parts[1], parts[2], parts[3], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[0].strip() else "malformed git-log record"
            rows.append((sha, "", "", "", ""))
    return rows


def x__log_identities__mutmut_22(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        ["git", "log", f"--format={_FORMAT}", rev_range],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = None
        if len(parts) == 5:
            rows.append((parts[0], parts[1], parts[2], parts[3], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[0].strip() else "malformed git-log record"
            rows.append((sha, "", "", "", ""))
    return rows


def x__log_identities__mutmut_23(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        ["git", "log", f"--format={_FORMAT}", rev_range],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(None)
        if len(parts) == 5:
            rows.append((parts[0], parts[1], parts[2], parts[3], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[0].strip() else "malformed git-log record"
            rows.append((sha, "", "", "", ""))
    return rows


def x__log_identities__mutmut_24(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        ["git", "log", f"--format={_FORMAT}", rev_range],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) != 5:
            rows.append((parts[0], parts[1], parts[2], parts[3], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[0].strip() else "malformed git-log record"
            rows.append((sha, "", "", "", ""))
    return rows


def x__log_identities__mutmut_25(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        ["git", "log", f"--format={_FORMAT}", rev_range],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) == 6:
            rows.append((parts[0], parts[1], parts[2], parts[3], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[0].strip() else "malformed git-log record"
            rows.append((sha, "", "", "", ""))
    return rows


def x__log_identities__mutmut_26(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        ["git", "log", f"--format={_FORMAT}", rev_range],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) == 5:
            rows.append(None)
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[0].strip() else "malformed git-log record"
            rows.append((sha, "", "", "", ""))
    return rows


def x__log_identities__mutmut_27(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        ["git", "log", f"--format={_FORMAT}", rev_range],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) == 5:
            rows.append((parts[1], parts[1], parts[2], parts[3], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[0].strip() else "malformed git-log record"
            rows.append((sha, "", "", "", ""))
    return rows


def x__log_identities__mutmut_28(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        ["git", "log", f"--format={_FORMAT}", rev_range],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) == 5:
            rows.append((parts[0], parts[2], parts[2], parts[3], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[0].strip() else "malformed git-log record"
            rows.append((sha, "", "", "", ""))
    return rows


def x__log_identities__mutmut_29(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        ["git", "log", f"--format={_FORMAT}", rev_range],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) == 5:
            rows.append((parts[0], parts[1], parts[3], parts[3], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[0].strip() else "malformed git-log record"
            rows.append((sha, "", "", "", ""))
    return rows


def x__log_identities__mutmut_30(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        ["git", "log", f"--format={_FORMAT}", rev_range],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) == 5:
            rows.append((parts[0], parts[1], parts[2], parts[4], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[0].strip() else "malformed git-log record"
            rows.append((sha, "", "", "", ""))
    return rows


def x__log_identities__mutmut_31(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        ["git", "log", f"--format={_FORMAT}", rev_range],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) == 5:
            rows.append((parts[0], parts[1], parts[2], parts[3], parts[5]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[0].strip() else "malformed git-log record"
            rows.append((sha, "", "", "", ""))
    return rows


def x__log_identities__mutmut_32(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        ["git", "log", f"--format={_FORMAT}", rev_range],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) == 5:
            rows.append((parts[0], parts[1], parts[2], parts[3], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = None
            rows.append((sha, "", "", "", ""))
    return rows


def x__log_identities__mutmut_33(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        ["git", "log", f"--format={_FORMAT}", rev_range],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) == 5:
            rows.append((parts[0], parts[1], parts[2], parts[3], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[1] if parts[0].strip() else "malformed git-log record"
            rows.append((sha, "", "", "", ""))
    return rows


def x__log_identities__mutmut_34(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        ["git", "log", f"--format={_FORMAT}", rev_range],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) == 5:
            rows.append((parts[0], parts[1], parts[2], parts[3], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[1].strip() else "malformed git-log record"
            rows.append((sha, "", "", "", ""))
    return rows


def x__log_identities__mutmut_35(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        ["git", "log", f"--format={_FORMAT}", rev_range],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) == 5:
            rows.append((parts[0], parts[1], parts[2], parts[3], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[0].strip() else "XXmalformed git-log recordXX"
            rows.append((sha, "", "", "", ""))
    return rows


def x__log_identities__mutmut_36(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        ["git", "log", f"--format={_FORMAT}", rev_range],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) == 5:
            rows.append((parts[0], parts[1], parts[2], parts[3], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[0].strip() else "MALFORMED GIT-LOG RECORD"
            rows.append((sha, "", "", "", ""))
    return rows


def x__log_identities__mutmut_37(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        ["git", "log", f"--format={_FORMAT}", rev_range],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) == 5:
            rows.append((parts[0], parts[1], parts[2], parts[3], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[0].strip() else "malformed git-log record"
            rows.append(None)
    return rows


def x__log_identities__mutmut_38(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        ["git", "log", f"--format={_FORMAT}", rev_range],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) == 5:
            rows.append((parts[0], parts[1], parts[2], parts[3], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[0].strip() else "malformed git-log record"
            rows.append((sha, "XXXX", "", "", ""))
    return rows


def x__log_identities__mutmut_39(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        ["git", "log", f"--format={_FORMAT}", rev_range],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) == 5:
            rows.append((parts[0], parts[1], parts[2], parts[3], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[0].strip() else "malformed git-log record"
            rows.append((sha, "", "XXXX", "", ""))
    return rows


def x__log_identities__mutmut_40(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        ["git", "log", f"--format={_FORMAT}", rev_range],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) == 5:
            rows.append((parts[0], parts[1], parts[2], parts[3], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[0].strip() else "malformed git-log record"
            rows.append((sha, "", "", "XXXX", ""))
    return rows


def x__log_identities__mutmut_41(repo_root: Path, rev_range: str) -> list[tuple[str, str, str, str, str]]:
    """``(sha, author_name, author_email, committer_name, committer_email)`` per commit.

    Returns ``[]`` on any git failure (e.g. an unresolved range in a fresh
    checkout) — an unresolvable range yields no commits to gate, never a crash.
    """
    result = subprocess.run(
        ["git", "log", f"--format={_FORMAT}", rev_range],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str, str, str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(_SEP)
        if len(parts) == 5:
            rows.append((parts[0], parts[1], parts[2], parts[3], parts[4]))
        else:
            # Commit metadata can contain arbitrary control characters. If one
            # collides with the record separator, or Git returns an empty row,
            # do not silently omit the record from the identity gate.
            sha = parts[0] if parts[0].strip() else "malformed git-log record"
            rows.append((sha, "", "", "", "XXXX"))
    return rows

mutants_x__log_identities__mutmut['_mutmut_orig'] = x__log_identities__mutmut_orig # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_1'] = x__log_identities__mutmut_1 # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_2'] = x__log_identities__mutmut_2 # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_3'] = x__log_identities__mutmut_3 # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_4'] = x__log_identities__mutmut_4 # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_5'] = x__log_identities__mutmut_5 # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_6'] = x__log_identities__mutmut_6 # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_7'] = x__log_identities__mutmut_7 # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_8'] = x__log_identities__mutmut_8 # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_9'] = x__log_identities__mutmut_9 # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_10'] = x__log_identities__mutmut_10 # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_11'] = x__log_identities__mutmut_11 # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_12'] = x__log_identities__mutmut_12 # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_13'] = x__log_identities__mutmut_13 # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_14'] = x__log_identities__mutmut_14 # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_15'] = x__log_identities__mutmut_15 # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_16'] = x__log_identities__mutmut_16 # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_17'] = x__log_identities__mutmut_17 # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_18'] = x__log_identities__mutmut_18 # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_19'] = x__log_identities__mutmut_19 # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_20'] = x__log_identities__mutmut_20 # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_21'] = x__log_identities__mutmut_21 # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_22'] = x__log_identities__mutmut_22 # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_23'] = x__log_identities__mutmut_23 # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_24'] = x__log_identities__mutmut_24 # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_25'] = x__log_identities__mutmut_25 # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_26'] = x__log_identities__mutmut_26 # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_27'] = x__log_identities__mutmut_27 # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_28'] = x__log_identities__mutmut_28 # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_29'] = x__log_identities__mutmut_29 # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_30'] = x__log_identities__mutmut_30 # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_31'] = x__log_identities__mutmut_31 # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_32'] = x__log_identities__mutmut_32 # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_33'] = x__log_identities__mutmut_33 # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_34'] = x__log_identities__mutmut_34 # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_35'] = x__log_identities__mutmut_35 # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_36'] = x__log_identities__mutmut_36 # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_37'] = x__log_identities__mutmut_37 # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_38'] = x__log_identities__mutmut_38 # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_39'] = x__log_identities__mutmut_39 # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_40'] = x__log_identities__mutmut_40 # type: ignore # mutmut generated
mutants_x__log_identities__mutmut['x__log_identities__mutmut_41'] = x__log_identities__mutmut_41 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCanonicalCommitIdentityǁ_configured__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCanonicalCommitIdentityǁ_identity_ok__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCanonicalCommitIdentityǁ_committer_ok__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCanonicalCommitIdentityǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCanonicalCommitIdentityǁcollect_violations__mutmut: MutantDict = {}  # type: ignore


class CanonicalCommitIdentity(FitnessRule):
    """Flags commits whose author/committer identity is off the allowlist."""

    name = "canonical-commit-identity"
    remediation = REMEDIATION

    #: Config (repo-neutral defaults; overridden per consumer via from_config).
    allowed_emails: frozenset[str] = frozenset()
    allowed_name_patterns: tuple[re.Pattern[str], ...] = ()
    base_ref: str = DEFAULT_BASE_REF
    head_ref: str = DEFAULT_HEAD_REF

    @classmethod
    @_mutmut_mutated(mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CanonicalCommitIdentity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CanonicalCommitIdentity)  # noqa: S101  # narrowing for mypy
        rule.allowed_emails = frozenset(config.get("allowed_emails", ()))
        rule.allowed_name_patterns = tuple(re.compile(p) for p in config.get("allowed_name_patterns", ()))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.head_ref = str(config.get("head_ref", DEFAULT_HEAD_REF))
        return rule

    @classmethod
    def xǁCanonicalCommitIdentityǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CanonicalCommitIdentity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CanonicalCommitIdentity)  # noqa: S101  # narrowing for mypy
        rule.allowed_emails = frozenset(config.get("allowed_emails", ()))
        rule.allowed_name_patterns = tuple(re.compile(p) for p in config.get("allowed_name_patterns", ()))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.head_ref = str(config.get("head_ref", DEFAULT_HEAD_REF))
        return rule

    @classmethod
    def xǁCanonicalCommitIdentityǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CanonicalCommitIdentity:
        rule = None
        assert isinstance(rule, CanonicalCommitIdentity)  # noqa: S101  # narrowing for mypy
        rule.allowed_emails = frozenset(config.get("allowed_emails", ()))
        rule.allowed_name_patterns = tuple(re.compile(p) for p in config.get("allowed_name_patterns", ()))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.head_ref = str(config.get("head_ref", DEFAULT_HEAD_REF))
        return rule

    @classmethod
    def xǁCanonicalCommitIdentityǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CanonicalCommitIdentity:
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, CanonicalCommitIdentity)  # noqa: S101  # narrowing for mypy
        rule.allowed_emails = frozenset(config.get("allowed_emails", ()))
        rule.allowed_name_patterns = tuple(re.compile(p) for p in config.get("allowed_name_patterns", ()))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.head_ref = str(config.get("head_ref", DEFAULT_HEAD_REF))
        return rule

    @classmethod
    def xǁCanonicalCommitIdentityǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CanonicalCommitIdentity:
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, CanonicalCommitIdentity)  # noqa: S101  # narrowing for mypy
        rule.allowed_emails = frozenset(config.get("allowed_emails", ()))
        rule.allowed_name_patterns = tuple(re.compile(p) for p in config.get("allowed_name_patterns", ()))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.head_ref = str(config.get("head_ref", DEFAULT_HEAD_REF))
        return rule

    @classmethod
    def xǁCanonicalCommitIdentityǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CanonicalCommitIdentity:
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, CanonicalCommitIdentity)  # noqa: S101  # narrowing for mypy
        rule.allowed_emails = frozenset(config.get("allowed_emails", ()))
        rule.allowed_name_patterns = tuple(re.compile(p) for p in config.get("allowed_name_patterns", ()))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.head_ref = str(config.get("head_ref", DEFAULT_HEAD_REF))
        return rule

    @classmethod
    def xǁCanonicalCommitIdentityǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CanonicalCommitIdentity:
        rule = super().from_config(config, )
        assert isinstance(rule, CanonicalCommitIdentity)  # noqa: S101  # narrowing for mypy
        rule.allowed_emails = frozenset(config.get("allowed_emails", ()))
        rule.allowed_name_patterns = tuple(re.compile(p) for p in config.get("allowed_name_patterns", ()))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.head_ref = str(config.get("head_ref", DEFAULT_HEAD_REF))
        return rule

    @classmethod
    def xǁCanonicalCommitIdentityǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CanonicalCommitIdentity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CanonicalCommitIdentity)  # noqa: S101  # narrowing for mypy
        rule.allowed_emails = None
        rule.allowed_name_patterns = tuple(re.compile(p) for p in config.get("allowed_name_patterns", ()))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.head_ref = str(config.get("head_ref", DEFAULT_HEAD_REF))
        return rule

    @classmethod
    def xǁCanonicalCommitIdentityǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CanonicalCommitIdentity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CanonicalCommitIdentity)  # noqa: S101  # narrowing for mypy
        rule.allowed_emails = frozenset(None)
        rule.allowed_name_patterns = tuple(re.compile(p) for p in config.get("allowed_name_patterns", ()))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.head_ref = str(config.get("head_ref", DEFAULT_HEAD_REF))
        return rule

    @classmethod
    def xǁCanonicalCommitIdentityǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CanonicalCommitIdentity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CanonicalCommitIdentity)  # noqa: S101  # narrowing for mypy
        rule.allowed_emails = frozenset(config.get(None, ()))
        rule.allowed_name_patterns = tuple(re.compile(p) for p in config.get("allowed_name_patterns", ()))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.head_ref = str(config.get("head_ref", DEFAULT_HEAD_REF))
        return rule

    @classmethod
    def xǁCanonicalCommitIdentityǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CanonicalCommitIdentity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CanonicalCommitIdentity)  # noqa: S101  # narrowing for mypy
        rule.allowed_emails = frozenset(config.get("allowed_emails", None))
        rule.allowed_name_patterns = tuple(re.compile(p) for p in config.get("allowed_name_patterns", ()))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.head_ref = str(config.get("head_ref", DEFAULT_HEAD_REF))
        return rule

    @classmethod
    def xǁCanonicalCommitIdentityǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CanonicalCommitIdentity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CanonicalCommitIdentity)  # noqa: S101  # narrowing for mypy
        rule.allowed_emails = frozenset(config.get(()))
        rule.allowed_name_patterns = tuple(re.compile(p) for p in config.get("allowed_name_patterns", ()))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.head_ref = str(config.get("head_ref", DEFAULT_HEAD_REF))
        return rule

    @classmethod
    def xǁCanonicalCommitIdentityǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CanonicalCommitIdentity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CanonicalCommitIdentity)  # noqa: S101  # narrowing for mypy
        rule.allowed_emails = frozenset(config.get("allowed_emails", ))
        rule.allowed_name_patterns = tuple(re.compile(p) for p in config.get("allowed_name_patterns", ()))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.head_ref = str(config.get("head_ref", DEFAULT_HEAD_REF))
        return rule

    @classmethod
    def xǁCanonicalCommitIdentityǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CanonicalCommitIdentity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CanonicalCommitIdentity)  # noqa: S101  # narrowing for mypy
        rule.allowed_emails = frozenset(config.get("XXallowed_emailsXX", ()))
        rule.allowed_name_patterns = tuple(re.compile(p) for p in config.get("allowed_name_patterns", ()))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.head_ref = str(config.get("head_ref", DEFAULT_HEAD_REF))
        return rule

    @classmethod
    def xǁCanonicalCommitIdentityǁfrom_config__mutmut_13(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CanonicalCommitIdentity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CanonicalCommitIdentity)  # noqa: S101  # narrowing for mypy
        rule.allowed_emails = frozenset(config.get("ALLOWED_EMAILS", ()))
        rule.allowed_name_patterns = tuple(re.compile(p) for p in config.get("allowed_name_patterns", ()))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.head_ref = str(config.get("head_ref", DEFAULT_HEAD_REF))
        return rule

    @classmethod
    def xǁCanonicalCommitIdentityǁfrom_config__mutmut_14(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CanonicalCommitIdentity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CanonicalCommitIdentity)  # noqa: S101  # narrowing for mypy
        rule.allowed_emails = frozenset(config.get("allowed_emails", ()))
        rule.allowed_name_patterns = None
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.head_ref = str(config.get("head_ref", DEFAULT_HEAD_REF))
        return rule

    @classmethod
    def xǁCanonicalCommitIdentityǁfrom_config__mutmut_15(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CanonicalCommitIdentity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CanonicalCommitIdentity)  # noqa: S101  # narrowing for mypy
        rule.allowed_emails = frozenset(config.get("allowed_emails", ()))
        rule.allowed_name_patterns = tuple(None)
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.head_ref = str(config.get("head_ref", DEFAULT_HEAD_REF))
        return rule

    @classmethod
    def xǁCanonicalCommitIdentityǁfrom_config__mutmut_16(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CanonicalCommitIdentity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CanonicalCommitIdentity)  # noqa: S101  # narrowing for mypy
        rule.allowed_emails = frozenset(config.get("allowed_emails", ()))
        rule.allowed_name_patterns = tuple(re.compile(None) for p in config.get("allowed_name_patterns", ()))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.head_ref = str(config.get("head_ref", DEFAULT_HEAD_REF))
        return rule

    @classmethod
    def xǁCanonicalCommitIdentityǁfrom_config__mutmut_17(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CanonicalCommitIdentity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CanonicalCommitIdentity)  # noqa: S101  # narrowing for mypy
        rule.allowed_emails = frozenset(config.get("allowed_emails", ()))
        rule.allowed_name_patterns = tuple(re.compile(p) for p in config.get(None, ()))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.head_ref = str(config.get("head_ref", DEFAULT_HEAD_REF))
        return rule

    @classmethod
    def xǁCanonicalCommitIdentityǁfrom_config__mutmut_18(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CanonicalCommitIdentity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CanonicalCommitIdentity)  # noqa: S101  # narrowing for mypy
        rule.allowed_emails = frozenset(config.get("allowed_emails", ()))
        rule.allowed_name_patterns = tuple(re.compile(p) for p in config.get("allowed_name_patterns", None))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.head_ref = str(config.get("head_ref", DEFAULT_HEAD_REF))
        return rule

    @classmethod
    def xǁCanonicalCommitIdentityǁfrom_config__mutmut_19(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CanonicalCommitIdentity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CanonicalCommitIdentity)  # noqa: S101  # narrowing for mypy
        rule.allowed_emails = frozenset(config.get("allowed_emails", ()))
        rule.allowed_name_patterns = tuple(re.compile(p) for p in config.get(()))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.head_ref = str(config.get("head_ref", DEFAULT_HEAD_REF))
        return rule

    @classmethod
    def xǁCanonicalCommitIdentityǁfrom_config__mutmut_20(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CanonicalCommitIdentity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CanonicalCommitIdentity)  # noqa: S101  # narrowing for mypy
        rule.allowed_emails = frozenset(config.get("allowed_emails", ()))
        rule.allowed_name_patterns = tuple(re.compile(p) for p in config.get("allowed_name_patterns", ))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.head_ref = str(config.get("head_ref", DEFAULT_HEAD_REF))
        return rule

    @classmethod
    def xǁCanonicalCommitIdentityǁfrom_config__mutmut_21(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CanonicalCommitIdentity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CanonicalCommitIdentity)  # noqa: S101  # narrowing for mypy
        rule.allowed_emails = frozenset(config.get("allowed_emails", ()))
        rule.allowed_name_patterns = tuple(re.compile(p) for p in config.get("XXallowed_name_patternsXX", ()))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.head_ref = str(config.get("head_ref", DEFAULT_HEAD_REF))
        return rule

    @classmethod
    def xǁCanonicalCommitIdentityǁfrom_config__mutmut_22(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CanonicalCommitIdentity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CanonicalCommitIdentity)  # noqa: S101  # narrowing for mypy
        rule.allowed_emails = frozenset(config.get("allowed_emails", ()))
        rule.allowed_name_patterns = tuple(re.compile(p) for p in config.get("ALLOWED_NAME_PATTERNS", ()))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.head_ref = str(config.get("head_ref", DEFAULT_HEAD_REF))
        return rule

    @classmethod
    def xǁCanonicalCommitIdentityǁfrom_config__mutmut_23(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CanonicalCommitIdentity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CanonicalCommitIdentity)  # noqa: S101  # narrowing for mypy
        rule.allowed_emails = frozenset(config.get("allowed_emails", ()))
        rule.allowed_name_patterns = tuple(re.compile(p) for p in config.get("allowed_name_patterns", ()))
        rule.base_ref = None
        rule.head_ref = str(config.get("head_ref", DEFAULT_HEAD_REF))
        return rule

    @classmethod
    def xǁCanonicalCommitIdentityǁfrom_config__mutmut_24(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CanonicalCommitIdentity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CanonicalCommitIdentity)  # noqa: S101  # narrowing for mypy
        rule.allowed_emails = frozenset(config.get("allowed_emails", ()))
        rule.allowed_name_patterns = tuple(re.compile(p) for p in config.get("allowed_name_patterns", ()))
        rule.base_ref = str(None)
        rule.head_ref = str(config.get("head_ref", DEFAULT_HEAD_REF))
        return rule

    @classmethod
    def xǁCanonicalCommitIdentityǁfrom_config__mutmut_25(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CanonicalCommitIdentity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CanonicalCommitIdentity)  # noqa: S101  # narrowing for mypy
        rule.allowed_emails = frozenset(config.get("allowed_emails", ()))
        rule.allowed_name_patterns = tuple(re.compile(p) for p in config.get("allowed_name_patterns", ()))
        rule.base_ref = str(config.get(None, DEFAULT_BASE_REF))
        rule.head_ref = str(config.get("head_ref", DEFAULT_HEAD_REF))
        return rule

    @classmethod
    def xǁCanonicalCommitIdentityǁfrom_config__mutmut_26(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CanonicalCommitIdentity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CanonicalCommitIdentity)  # noqa: S101  # narrowing for mypy
        rule.allowed_emails = frozenset(config.get("allowed_emails", ()))
        rule.allowed_name_patterns = tuple(re.compile(p) for p in config.get("allowed_name_patterns", ()))
        rule.base_ref = str(config.get("base_ref", None))
        rule.head_ref = str(config.get("head_ref", DEFAULT_HEAD_REF))
        return rule

    @classmethod
    def xǁCanonicalCommitIdentityǁfrom_config__mutmut_27(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CanonicalCommitIdentity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CanonicalCommitIdentity)  # noqa: S101  # narrowing for mypy
        rule.allowed_emails = frozenset(config.get("allowed_emails", ()))
        rule.allowed_name_patterns = tuple(re.compile(p) for p in config.get("allowed_name_patterns", ()))
        rule.base_ref = str(config.get(DEFAULT_BASE_REF))
        rule.head_ref = str(config.get("head_ref", DEFAULT_HEAD_REF))
        return rule

    @classmethod
    def xǁCanonicalCommitIdentityǁfrom_config__mutmut_28(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CanonicalCommitIdentity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CanonicalCommitIdentity)  # noqa: S101  # narrowing for mypy
        rule.allowed_emails = frozenset(config.get("allowed_emails", ()))
        rule.allowed_name_patterns = tuple(re.compile(p) for p in config.get("allowed_name_patterns", ()))
        rule.base_ref = str(config.get("base_ref", ))
        rule.head_ref = str(config.get("head_ref", DEFAULT_HEAD_REF))
        return rule

    @classmethod
    def xǁCanonicalCommitIdentityǁfrom_config__mutmut_29(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CanonicalCommitIdentity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CanonicalCommitIdentity)  # noqa: S101  # narrowing for mypy
        rule.allowed_emails = frozenset(config.get("allowed_emails", ()))
        rule.allowed_name_patterns = tuple(re.compile(p) for p in config.get("allowed_name_patterns", ()))
        rule.base_ref = str(config.get("XXbase_refXX", DEFAULT_BASE_REF))
        rule.head_ref = str(config.get("head_ref", DEFAULT_HEAD_REF))
        return rule

    @classmethod
    def xǁCanonicalCommitIdentityǁfrom_config__mutmut_30(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CanonicalCommitIdentity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CanonicalCommitIdentity)  # noqa: S101  # narrowing for mypy
        rule.allowed_emails = frozenset(config.get("allowed_emails", ()))
        rule.allowed_name_patterns = tuple(re.compile(p) for p in config.get("allowed_name_patterns", ()))
        rule.base_ref = str(config.get("BASE_REF", DEFAULT_BASE_REF))
        rule.head_ref = str(config.get("head_ref", DEFAULT_HEAD_REF))
        return rule

    @classmethod
    def xǁCanonicalCommitIdentityǁfrom_config__mutmut_31(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CanonicalCommitIdentity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CanonicalCommitIdentity)  # noqa: S101  # narrowing for mypy
        rule.allowed_emails = frozenset(config.get("allowed_emails", ()))
        rule.allowed_name_patterns = tuple(re.compile(p) for p in config.get("allowed_name_patterns", ()))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.head_ref = None
        return rule

    @classmethod
    def xǁCanonicalCommitIdentityǁfrom_config__mutmut_32(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CanonicalCommitIdentity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CanonicalCommitIdentity)  # noqa: S101  # narrowing for mypy
        rule.allowed_emails = frozenset(config.get("allowed_emails", ()))
        rule.allowed_name_patterns = tuple(re.compile(p) for p in config.get("allowed_name_patterns", ()))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.head_ref = str(None)
        return rule

    @classmethod
    def xǁCanonicalCommitIdentityǁfrom_config__mutmut_33(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CanonicalCommitIdentity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CanonicalCommitIdentity)  # noqa: S101  # narrowing for mypy
        rule.allowed_emails = frozenset(config.get("allowed_emails", ()))
        rule.allowed_name_patterns = tuple(re.compile(p) for p in config.get("allowed_name_patterns", ()))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.head_ref = str(config.get(None, DEFAULT_HEAD_REF))
        return rule

    @classmethod
    def xǁCanonicalCommitIdentityǁfrom_config__mutmut_34(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CanonicalCommitIdentity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CanonicalCommitIdentity)  # noqa: S101  # narrowing for mypy
        rule.allowed_emails = frozenset(config.get("allowed_emails", ()))
        rule.allowed_name_patterns = tuple(re.compile(p) for p in config.get("allowed_name_patterns", ()))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.head_ref = str(config.get("head_ref", None))
        return rule

    @classmethod
    def xǁCanonicalCommitIdentityǁfrom_config__mutmut_35(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CanonicalCommitIdentity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CanonicalCommitIdentity)  # noqa: S101  # narrowing for mypy
        rule.allowed_emails = frozenset(config.get("allowed_emails", ()))
        rule.allowed_name_patterns = tuple(re.compile(p) for p in config.get("allowed_name_patterns", ()))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.head_ref = str(config.get(DEFAULT_HEAD_REF))
        return rule

    @classmethod
    def xǁCanonicalCommitIdentityǁfrom_config__mutmut_36(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CanonicalCommitIdentity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CanonicalCommitIdentity)  # noqa: S101  # narrowing for mypy
        rule.allowed_emails = frozenset(config.get("allowed_emails", ()))
        rule.allowed_name_patterns = tuple(re.compile(p) for p in config.get("allowed_name_patterns", ()))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.head_ref = str(config.get("head_ref", ))
        return rule

    @classmethod
    def xǁCanonicalCommitIdentityǁfrom_config__mutmut_37(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CanonicalCommitIdentity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CanonicalCommitIdentity)  # noqa: S101  # narrowing for mypy
        rule.allowed_emails = frozenset(config.get("allowed_emails", ()))
        rule.allowed_name_patterns = tuple(re.compile(p) for p in config.get("allowed_name_patterns", ()))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.head_ref = str(config.get("XXhead_refXX", DEFAULT_HEAD_REF))
        return rule

    @classmethod
    def xǁCanonicalCommitIdentityǁfrom_config__mutmut_38(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CanonicalCommitIdentity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CanonicalCommitIdentity)  # noqa: S101  # narrowing for mypy
        rule.allowed_emails = frozenset(config.get("allowed_emails", ()))
        rule.allowed_name_patterns = tuple(re.compile(p) for p in config.get("allowed_name_patterns", ()))
        rule.base_ref = str(config.get("base_ref", DEFAULT_BASE_REF))
        rule.head_ref = str(config.get("HEAD_REF", DEFAULT_HEAD_REF))
        return rule

    @_mutmut_mutated(mutants_xǁCanonicalCommitIdentityǁ_configured__mutmut)
    def _configured(self) -> bool:
        """The rule only bites once a consumer supplies an allowlist / patterns."""
        return bool(self.allowed_emails or self.allowed_name_patterns)

    def xǁCanonicalCommitIdentityǁ_configured__mutmut_orig(self) -> bool:
        """The rule only bites once a consumer supplies an allowlist / patterns."""
        return bool(self.allowed_emails or self.allowed_name_patterns)

    def xǁCanonicalCommitIdentityǁ_configured__mutmut_1(self) -> bool:
        """The rule only bites once a consumer supplies an allowlist / patterns."""
        return bool(None)

    def xǁCanonicalCommitIdentityǁ_configured__mutmut_2(self) -> bool:
        """The rule only bites once a consumer supplies an allowlist / patterns."""
        return bool(self.allowed_emails and self.allowed_name_patterns)

    def _rev_range(self) -> str:
        return f"{self.base_ref}..{self.head_ref}"

    @_mutmut_mutated(mutants_xǁCanonicalCommitIdentityǁ_identity_ok__mutmut)
    def _identity_ok(self, name: str, email: str) -> bool:
        if self.allowed_emails and email not in self.allowed_emails:
            return False
        if self.allowed_name_patterns and not any(p.search(name) for p in self.allowed_name_patterns):
            return False
        return True

    def xǁCanonicalCommitIdentityǁ_identity_ok__mutmut_orig(self, name: str, email: str) -> bool:
        if self.allowed_emails and email not in self.allowed_emails:
            return False
        if self.allowed_name_patterns and not any(p.search(name) for p in self.allowed_name_patterns):
            return False
        return True

    def xǁCanonicalCommitIdentityǁ_identity_ok__mutmut_1(self, name: str, email: str) -> bool:
        if self.allowed_emails or email not in self.allowed_emails:
            return False
        if self.allowed_name_patterns and not any(p.search(name) for p in self.allowed_name_patterns):
            return False
        return True

    def xǁCanonicalCommitIdentityǁ_identity_ok__mutmut_2(self, name: str, email: str) -> bool:
        if self.allowed_emails and email in self.allowed_emails:
            return False
        if self.allowed_name_patterns and not any(p.search(name) for p in self.allowed_name_patterns):
            return False
        return True

    def xǁCanonicalCommitIdentityǁ_identity_ok__mutmut_3(self, name: str, email: str) -> bool:
        if self.allowed_emails and email not in self.allowed_emails:
            return True
        if self.allowed_name_patterns and not any(p.search(name) for p in self.allowed_name_patterns):
            return False
        return True

    def xǁCanonicalCommitIdentityǁ_identity_ok__mutmut_4(self, name: str, email: str) -> bool:
        if self.allowed_emails and email not in self.allowed_emails:
            return False
        if self.allowed_name_patterns or not any(p.search(name) for p in self.allowed_name_patterns):
            return False
        return True

    def xǁCanonicalCommitIdentityǁ_identity_ok__mutmut_5(self, name: str, email: str) -> bool:
        if self.allowed_emails and email not in self.allowed_emails:
            return False
        if self.allowed_name_patterns and any(p.search(name) for p in self.allowed_name_patterns):
            return False
        return True

    def xǁCanonicalCommitIdentityǁ_identity_ok__mutmut_6(self, name: str, email: str) -> bool:
        if self.allowed_emails and email not in self.allowed_emails:
            return False
        if self.allowed_name_patterns and not any(None):
            return False
        return True

    def xǁCanonicalCommitIdentityǁ_identity_ok__mutmut_7(self, name: str, email: str) -> bool:
        if self.allowed_emails and email not in self.allowed_emails:
            return False
        if self.allowed_name_patterns and not any(p.search(None) for p in self.allowed_name_patterns):
            return False
        return True

    def xǁCanonicalCommitIdentityǁ_identity_ok__mutmut_8(self, name: str, email: str) -> bool:
        if self.allowed_emails and email not in self.allowed_emails:
            return False
        if self.allowed_name_patterns and not any(p.search(name) for p in self.allowed_name_patterns):
            return True
        return True

    def xǁCanonicalCommitIdentityǁ_identity_ok__mutmut_9(self, name: str, email: str) -> bool:
        if self.allowed_emails and email not in self.allowed_emails:
            return False
        if self.allowed_name_patterns and not any(p.search(name) for p in self.allowed_name_patterns):
            return False
        return False

    @_mutmut_mutated(mutants_xǁCanonicalCommitIdentityǁ_committer_ok__mutmut)
    def _committer_ok(self, name: str, email: str) -> bool:
        """Committer identity check: the configured allowlist plus platform committers.

        Unlike the author, the committer of a merged commit is GitHub's web-flow
        signer and the committer of a bot-raised PR is the bot itself; those
        platform identities (:data:`_is_platform_committer`) are always allowed,
        bypassing both the email allowlist and the name patterns.
        """
        return _is_platform_committer(email) or self._identity_ok(name, email)

    def xǁCanonicalCommitIdentityǁ_committer_ok__mutmut_orig(self, name: str, email: str) -> bool:
        """Committer identity check: the configured allowlist plus platform committers.

        Unlike the author, the committer of a merged commit is GitHub's web-flow
        signer and the committer of a bot-raised PR is the bot itself; those
        platform identities (:data:`_is_platform_committer`) are always allowed,
        bypassing both the email allowlist and the name patterns.
        """
        return _is_platform_committer(email) or self._identity_ok(name, email)

    def xǁCanonicalCommitIdentityǁ_committer_ok__mutmut_1(self, name: str, email: str) -> bool:
        """Committer identity check: the configured allowlist plus platform committers.

        Unlike the author, the committer of a merged commit is GitHub's web-flow
        signer and the committer of a bot-raised PR is the bot itself; those
        platform identities (:data:`_is_platform_committer`) are always allowed,
        bypassing both the email allowlist and the name patterns.
        """
        return _is_platform_committer(email) and self._identity_ok(name, email)

    def xǁCanonicalCommitIdentityǁ_committer_ok__mutmut_2(self, name: str, email: str) -> bool:
        """Committer identity check: the configured allowlist plus platform committers.

        Unlike the author, the committer of a merged commit is GitHub's web-flow
        signer and the committer of a bot-raised PR is the bot itself; those
        platform identities (:data:`_is_platform_committer`) are always allowed,
        bypassing both the email allowlist and the name patterns.
        """
        return _is_platform_committer(None) or self._identity_ok(name, email)

    def xǁCanonicalCommitIdentityǁ_committer_ok__mutmut_3(self, name: str, email: str) -> bool:
        """Committer identity check: the configured allowlist plus platform committers.

        Unlike the author, the committer of a merged commit is GitHub's web-flow
        signer and the committer of a bot-raised PR is the bot itself; those
        platform identities (:data:`_is_platform_committer`) are always allowed,
        bypassing both the email allowlist and the name patterns.
        """
        return _is_platform_committer(email) or self._identity_ok(None, email)

    def xǁCanonicalCommitIdentityǁ_committer_ok__mutmut_4(self, name: str, email: str) -> bool:
        """Committer identity check: the configured allowlist plus platform committers.

        Unlike the author, the committer of a merged commit is GitHub's web-flow
        signer and the committer of a bot-raised PR is the bot itself; those
        platform identities (:data:`_is_platform_committer`) are always allowed,
        bypassing both the email allowlist and the name patterns.
        """
        return _is_platform_committer(email) or self._identity_ok(name, None)

    def xǁCanonicalCommitIdentityǁ_committer_ok__mutmut_5(self, name: str, email: str) -> bool:
        """Committer identity check: the configured allowlist plus platform committers.

        Unlike the author, the committer of a merged commit is GitHub's web-flow
        signer and the committer of a bot-raised PR is the bot itself; those
        platform identities (:data:`_is_platform_committer`) are always allowed,
        bypassing both the email allowlist and the name patterns.
        """
        return _is_platform_committer(email) or self._identity_ok(email)

    def xǁCanonicalCommitIdentityǁ_committer_ok__mutmut_6(self, name: str, email: str) -> bool:
        """Committer identity check: the configured allowlist plus platform committers.

        Unlike the author, the committer of a merged commit is GitHub's web-flow
        signer and the committer of a bot-raised PR is the bot itself; those
        platform identities (:data:`_is_platform_committer`) are always allowed,
        bypassing both the email allowlist and the name patterns.
        """
        return _is_platform_committer(email) or self._identity_ok(name, )

    @_mutmut_mutated(mutants_xǁCanonicalCommitIdentityǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        """Unused — this is a range/commit check (see :meth:`collect_violations`)."""
        return False

    def xǁCanonicalCommitIdentityǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        """Unused — this is a range/commit check (see :meth:`collect_violations`)."""
        return False

    def xǁCanonicalCommitIdentityǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        """Unused — this is a range/commit check (see :meth:`collect_violations`)."""
        return True

    def enumerate_files(self) -> list[Path]:
        """No file surface — identity lives in commit metadata, not the tree."""
        return []

    @_mutmut_mutated(mutants_xǁCanonicalCommitIdentityǁcollect_violations__mutmut)
    def collect_violations(self) -> set[Path]:
        """Every in-range commit with an off-allowlist author/committer identity.

        The AUTHOR is held strictly to the configured allowlist; the COMMITTER is
        allowed if it is a platform committer (web-flow / Dependabot / Renovate) or
        otherwise on the allowlist — see :meth:`_committer_ok`.
        """
        if not self._configured():
            return set()
        out: set[Path] = set()
        for sha, an, ae, cn, ce in _log_identities(self._repo_root, self._rev_range()):
            bad: list[str] = []
            if not self._identity_ok(an, ae):
                bad.append(f"author {an} <{ae}>")
            if not self._committer_ok(cn, ce):
                bad.append(f"committer {cn} <{ce}>")
            if bad:
                out.add(Path(f"{sha[:12]} {'; '.join(bad)}"))
        return out

    def xǁCanonicalCommitIdentityǁcollect_violations__mutmut_orig(self) -> set[Path]:
        """Every in-range commit with an off-allowlist author/committer identity.

        The AUTHOR is held strictly to the configured allowlist; the COMMITTER is
        allowed if it is a platform committer (web-flow / Dependabot / Renovate) or
        otherwise on the allowlist — see :meth:`_committer_ok`.
        """
        if not self._configured():
            return set()
        out: set[Path] = set()
        for sha, an, ae, cn, ce in _log_identities(self._repo_root, self._rev_range()):
            bad: list[str] = []
            if not self._identity_ok(an, ae):
                bad.append(f"author {an} <{ae}>")
            if not self._committer_ok(cn, ce):
                bad.append(f"committer {cn} <{ce}>")
            if bad:
                out.add(Path(f"{sha[:12]} {'; '.join(bad)}"))
        return out

    def xǁCanonicalCommitIdentityǁcollect_violations__mutmut_1(self) -> set[Path]:
        """Every in-range commit with an off-allowlist author/committer identity.

        The AUTHOR is held strictly to the configured allowlist; the COMMITTER is
        allowed if it is a platform committer (web-flow / Dependabot / Renovate) or
        otherwise on the allowlist — see :meth:`_committer_ok`.
        """
        if self._configured():
            return set()
        out: set[Path] = set()
        for sha, an, ae, cn, ce in _log_identities(self._repo_root, self._rev_range()):
            bad: list[str] = []
            if not self._identity_ok(an, ae):
                bad.append(f"author {an} <{ae}>")
            if not self._committer_ok(cn, ce):
                bad.append(f"committer {cn} <{ce}>")
            if bad:
                out.add(Path(f"{sha[:12]} {'; '.join(bad)}"))
        return out

    def xǁCanonicalCommitIdentityǁcollect_violations__mutmut_2(self) -> set[Path]:
        """Every in-range commit with an off-allowlist author/committer identity.

        The AUTHOR is held strictly to the configured allowlist; the COMMITTER is
        allowed if it is a platform committer (web-flow / Dependabot / Renovate) or
        otherwise on the allowlist — see :meth:`_committer_ok`.
        """
        if not self._configured():
            return set()
        out: set[Path] = None
        for sha, an, ae, cn, ce in _log_identities(self._repo_root, self._rev_range()):
            bad: list[str] = []
            if not self._identity_ok(an, ae):
                bad.append(f"author {an} <{ae}>")
            if not self._committer_ok(cn, ce):
                bad.append(f"committer {cn} <{ce}>")
            if bad:
                out.add(Path(f"{sha[:12]} {'; '.join(bad)}"))
        return out

    def xǁCanonicalCommitIdentityǁcollect_violations__mutmut_3(self) -> set[Path]:
        """Every in-range commit with an off-allowlist author/committer identity.

        The AUTHOR is held strictly to the configured allowlist; the COMMITTER is
        allowed if it is a platform committer (web-flow / Dependabot / Renovate) or
        otherwise on the allowlist — see :meth:`_committer_ok`.
        """
        if not self._configured():
            return set()
        out: set[Path] = set()
        for sha, an, ae, cn, ce in _log_identities(None, self._rev_range()):
            bad: list[str] = []
            if not self._identity_ok(an, ae):
                bad.append(f"author {an} <{ae}>")
            if not self._committer_ok(cn, ce):
                bad.append(f"committer {cn} <{ce}>")
            if bad:
                out.add(Path(f"{sha[:12]} {'; '.join(bad)}"))
        return out

    def xǁCanonicalCommitIdentityǁcollect_violations__mutmut_4(self) -> set[Path]:
        """Every in-range commit with an off-allowlist author/committer identity.

        The AUTHOR is held strictly to the configured allowlist; the COMMITTER is
        allowed if it is a platform committer (web-flow / Dependabot / Renovate) or
        otherwise on the allowlist — see :meth:`_committer_ok`.
        """
        if not self._configured():
            return set()
        out: set[Path] = set()
        for sha, an, ae, cn, ce in _log_identities(self._repo_root, None):
            bad: list[str] = []
            if not self._identity_ok(an, ae):
                bad.append(f"author {an} <{ae}>")
            if not self._committer_ok(cn, ce):
                bad.append(f"committer {cn} <{ce}>")
            if bad:
                out.add(Path(f"{sha[:12]} {'; '.join(bad)}"))
        return out

    def xǁCanonicalCommitIdentityǁcollect_violations__mutmut_5(self) -> set[Path]:
        """Every in-range commit with an off-allowlist author/committer identity.

        The AUTHOR is held strictly to the configured allowlist; the COMMITTER is
        allowed if it is a platform committer (web-flow / Dependabot / Renovate) or
        otherwise on the allowlist — see :meth:`_committer_ok`.
        """
        if not self._configured():
            return set()
        out: set[Path] = set()
        for sha, an, ae, cn, ce in _log_identities(self._rev_range()):
            bad: list[str] = []
            if not self._identity_ok(an, ae):
                bad.append(f"author {an} <{ae}>")
            if not self._committer_ok(cn, ce):
                bad.append(f"committer {cn} <{ce}>")
            if bad:
                out.add(Path(f"{sha[:12]} {'; '.join(bad)}"))
        return out

    def xǁCanonicalCommitIdentityǁcollect_violations__mutmut_6(self) -> set[Path]:
        """Every in-range commit with an off-allowlist author/committer identity.

        The AUTHOR is held strictly to the configured allowlist; the COMMITTER is
        allowed if it is a platform committer (web-flow / Dependabot / Renovate) or
        otherwise on the allowlist — see :meth:`_committer_ok`.
        """
        if not self._configured():
            return set()
        out: set[Path] = set()
        for sha, an, ae, cn, ce in _log_identities(self._repo_root, ):
            bad: list[str] = []
            if not self._identity_ok(an, ae):
                bad.append(f"author {an} <{ae}>")
            if not self._committer_ok(cn, ce):
                bad.append(f"committer {cn} <{ce}>")
            if bad:
                out.add(Path(f"{sha[:12]} {'; '.join(bad)}"))
        return out

    def xǁCanonicalCommitIdentityǁcollect_violations__mutmut_7(self) -> set[Path]:
        """Every in-range commit with an off-allowlist author/committer identity.

        The AUTHOR is held strictly to the configured allowlist; the COMMITTER is
        allowed if it is a platform committer (web-flow / Dependabot / Renovate) or
        otherwise on the allowlist — see :meth:`_committer_ok`.
        """
        if not self._configured():
            return set()
        out: set[Path] = set()
        for sha, an, ae, cn, ce in _log_identities(self._repo_root, self._rev_range()):
            bad: list[str] = None
            if not self._identity_ok(an, ae):
                bad.append(f"author {an} <{ae}>")
            if not self._committer_ok(cn, ce):
                bad.append(f"committer {cn} <{ce}>")
            if bad:
                out.add(Path(f"{sha[:12]} {'; '.join(bad)}"))
        return out

    def xǁCanonicalCommitIdentityǁcollect_violations__mutmut_8(self) -> set[Path]:
        """Every in-range commit with an off-allowlist author/committer identity.

        The AUTHOR is held strictly to the configured allowlist; the COMMITTER is
        allowed if it is a platform committer (web-flow / Dependabot / Renovate) or
        otherwise on the allowlist — see :meth:`_committer_ok`.
        """
        if not self._configured():
            return set()
        out: set[Path] = set()
        for sha, an, ae, cn, ce in _log_identities(self._repo_root, self._rev_range()):
            bad: list[str] = []
            if self._identity_ok(an, ae):
                bad.append(f"author {an} <{ae}>")
            if not self._committer_ok(cn, ce):
                bad.append(f"committer {cn} <{ce}>")
            if bad:
                out.add(Path(f"{sha[:12]} {'; '.join(bad)}"))
        return out

    def xǁCanonicalCommitIdentityǁcollect_violations__mutmut_9(self) -> set[Path]:
        """Every in-range commit with an off-allowlist author/committer identity.

        The AUTHOR is held strictly to the configured allowlist; the COMMITTER is
        allowed if it is a platform committer (web-flow / Dependabot / Renovate) or
        otherwise on the allowlist — see :meth:`_committer_ok`.
        """
        if not self._configured():
            return set()
        out: set[Path] = set()
        for sha, an, ae, cn, ce in _log_identities(self._repo_root, self._rev_range()):
            bad: list[str] = []
            if not self._identity_ok(None, ae):
                bad.append(f"author {an} <{ae}>")
            if not self._committer_ok(cn, ce):
                bad.append(f"committer {cn} <{ce}>")
            if bad:
                out.add(Path(f"{sha[:12]} {'; '.join(bad)}"))
        return out

    def xǁCanonicalCommitIdentityǁcollect_violations__mutmut_10(self) -> set[Path]:
        """Every in-range commit with an off-allowlist author/committer identity.

        The AUTHOR is held strictly to the configured allowlist; the COMMITTER is
        allowed if it is a platform committer (web-flow / Dependabot / Renovate) or
        otherwise on the allowlist — see :meth:`_committer_ok`.
        """
        if not self._configured():
            return set()
        out: set[Path] = set()
        for sha, an, ae, cn, ce in _log_identities(self._repo_root, self._rev_range()):
            bad: list[str] = []
            if not self._identity_ok(an, None):
                bad.append(f"author {an} <{ae}>")
            if not self._committer_ok(cn, ce):
                bad.append(f"committer {cn} <{ce}>")
            if bad:
                out.add(Path(f"{sha[:12]} {'; '.join(bad)}"))
        return out

    def xǁCanonicalCommitIdentityǁcollect_violations__mutmut_11(self) -> set[Path]:
        """Every in-range commit with an off-allowlist author/committer identity.

        The AUTHOR is held strictly to the configured allowlist; the COMMITTER is
        allowed if it is a platform committer (web-flow / Dependabot / Renovate) or
        otherwise on the allowlist — see :meth:`_committer_ok`.
        """
        if not self._configured():
            return set()
        out: set[Path] = set()
        for sha, an, ae, cn, ce in _log_identities(self._repo_root, self._rev_range()):
            bad: list[str] = []
            if not self._identity_ok(ae):
                bad.append(f"author {an} <{ae}>")
            if not self._committer_ok(cn, ce):
                bad.append(f"committer {cn} <{ce}>")
            if bad:
                out.add(Path(f"{sha[:12]} {'; '.join(bad)}"))
        return out

    def xǁCanonicalCommitIdentityǁcollect_violations__mutmut_12(self) -> set[Path]:
        """Every in-range commit with an off-allowlist author/committer identity.

        The AUTHOR is held strictly to the configured allowlist; the COMMITTER is
        allowed if it is a platform committer (web-flow / Dependabot / Renovate) or
        otherwise on the allowlist — see :meth:`_committer_ok`.
        """
        if not self._configured():
            return set()
        out: set[Path] = set()
        for sha, an, ae, cn, ce in _log_identities(self._repo_root, self._rev_range()):
            bad: list[str] = []
            if not self._identity_ok(an, ):
                bad.append(f"author {an} <{ae}>")
            if not self._committer_ok(cn, ce):
                bad.append(f"committer {cn} <{ce}>")
            if bad:
                out.add(Path(f"{sha[:12]} {'; '.join(bad)}"))
        return out

    def xǁCanonicalCommitIdentityǁcollect_violations__mutmut_13(self) -> set[Path]:
        """Every in-range commit with an off-allowlist author/committer identity.

        The AUTHOR is held strictly to the configured allowlist; the COMMITTER is
        allowed if it is a platform committer (web-flow / Dependabot / Renovate) or
        otherwise on the allowlist — see :meth:`_committer_ok`.
        """
        if not self._configured():
            return set()
        out: set[Path] = set()
        for sha, an, ae, cn, ce in _log_identities(self._repo_root, self._rev_range()):
            bad: list[str] = []
            if not self._identity_ok(an, ae):
                bad.append(None)
            if not self._committer_ok(cn, ce):
                bad.append(f"committer {cn} <{ce}>")
            if bad:
                out.add(Path(f"{sha[:12]} {'; '.join(bad)}"))
        return out

    def xǁCanonicalCommitIdentityǁcollect_violations__mutmut_14(self) -> set[Path]:
        """Every in-range commit with an off-allowlist author/committer identity.

        The AUTHOR is held strictly to the configured allowlist; the COMMITTER is
        allowed if it is a platform committer (web-flow / Dependabot / Renovate) or
        otherwise on the allowlist — see :meth:`_committer_ok`.
        """
        if not self._configured():
            return set()
        out: set[Path] = set()
        for sha, an, ae, cn, ce in _log_identities(self._repo_root, self._rev_range()):
            bad: list[str] = []
            if not self._identity_ok(an, ae):
                bad.append(f"author {an} <{ae}>")
            if self._committer_ok(cn, ce):
                bad.append(f"committer {cn} <{ce}>")
            if bad:
                out.add(Path(f"{sha[:12]} {'; '.join(bad)}"))
        return out

    def xǁCanonicalCommitIdentityǁcollect_violations__mutmut_15(self) -> set[Path]:
        """Every in-range commit with an off-allowlist author/committer identity.

        The AUTHOR is held strictly to the configured allowlist; the COMMITTER is
        allowed if it is a platform committer (web-flow / Dependabot / Renovate) or
        otherwise on the allowlist — see :meth:`_committer_ok`.
        """
        if not self._configured():
            return set()
        out: set[Path] = set()
        for sha, an, ae, cn, ce in _log_identities(self._repo_root, self._rev_range()):
            bad: list[str] = []
            if not self._identity_ok(an, ae):
                bad.append(f"author {an} <{ae}>")
            if not self._committer_ok(None, ce):
                bad.append(f"committer {cn} <{ce}>")
            if bad:
                out.add(Path(f"{sha[:12]} {'; '.join(bad)}"))
        return out

    def xǁCanonicalCommitIdentityǁcollect_violations__mutmut_16(self) -> set[Path]:
        """Every in-range commit with an off-allowlist author/committer identity.

        The AUTHOR is held strictly to the configured allowlist; the COMMITTER is
        allowed if it is a platform committer (web-flow / Dependabot / Renovate) or
        otherwise on the allowlist — see :meth:`_committer_ok`.
        """
        if not self._configured():
            return set()
        out: set[Path] = set()
        for sha, an, ae, cn, ce in _log_identities(self._repo_root, self._rev_range()):
            bad: list[str] = []
            if not self._identity_ok(an, ae):
                bad.append(f"author {an} <{ae}>")
            if not self._committer_ok(cn, None):
                bad.append(f"committer {cn} <{ce}>")
            if bad:
                out.add(Path(f"{sha[:12]} {'; '.join(bad)}"))
        return out

    def xǁCanonicalCommitIdentityǁcollect_violations__mutmut_17(self) -> set[Path]:
        """Every in-range commit with an off-allowlist author/committer identity.

        The AUTHOR is held strictly to the configured allowlist; the COMMITTER is
        allowed if it is a platform committer (web-flow / Dependabot / Renovate) or
        otherwise on the allowlist — see :meth:`_committer_ok`.
        """
        if not self._configured():
            return set()
        out: set[Path] = set()
        for sha, an, ae, cn, ce in _log_identities(self._repo_root, self._rev_range()):
            bad: list[str] = []
            if not self._identity_ok(an, ae):
                bad.append(f"author {an} <{ae}>")
            if not self._committer_ok(ce):
                bad.append(f"committer {cn} <{ce}>")
            if bad:
                out.add(Path(f"{sha[:12]} {'; '.join(bad)}"))
        return out

    def xǁCanonicalCommitIdentityǁcollect_violations__mutmut_18(self) -> set[Path]:
        """Every in-range commit with an off-allowlist author/committer identity.

        The AUTHOR is held strictly to the configured allowlist; the COMMITTER is
        allowed if it is a platform committer (web-flow / Dependabot / Renovate) or
        otherwise on the allowlist — see :meth:`_committer_ok`.
        """
        if not self._configured():
            return set()
        out: set[Path] = set()
        for sha, an, ae, cn, ce in _log_identities(self._repo_root, self._rev_range()):
            bad: list[str] = []
            if not self._identity_ok(an, ae):
                bad.append(f"author {an} <{ae}>")
            if not self._committer_ok(cn, ):
                bad.append(f"committer {cn} <{ce}>")
            if bad:
                out.add(Path(f"{sha[:12]} {'; '.join(bad)}"))
        return out

    def xǁCanonicalCommitIdentityǁcollect_violations__mutmut_19(self) -> set[Path]:
        """Every in-range commit with an off-allowlist author/committer identity.

        The AUTHOR is held strictly to the configured allowlist; the COMMITTER is
        allowed if it is a platform committer (web-flow / Dependabot / Renovate) or
        otherwise on the allowlist — see :meth:`_committer_ok`.
        """
        if not self._configured():
            return set()
        out: set[Path] = set()
        for sha, an, ae, cn, ce in _log_identities(self._repo_root, self._rev_range()):
            bad: list[str] = []
            if not self._identity_ok(an, ae):
                bad.append(f"author {an} <{ae}>")
            if not self._committer_ok(cn, ce):
                bad.append(None)
            if bad:
                out.add(Path(f"{sha[:12]} {'; '.join(bad)}"))
        return out

    def xǁCanonicalCommitIdentityǁcollect_violations__mutmut_20(self) -> set[Path]:
        """Every in-range commit with an off-allowlist author/committer identity.

        The AUTHOR is held strictly to the configured allowlist; the COMMITTER is
        allowed if it is a platform committer (web-flow / Dependabot / Renovate) or
        otherwise on the allowlist — see :meth:`_committer_ok`.
        """
        if not self._configured():
            return set()
        out: set[Path] = set()
        for sha, an, ae, cn, ce in _log_identities(self._repo_root, self._rev_range()):
            bad: list[str] = []
            if not self._identity_ok(an, ae):
                bad.append(f"author {an} <{ae}>")
            if not self._committer_ok(cn, ce):
                bad.append(f"committer {cn} <{ce}>")
            if bad:
                out.add(None)
        return out

    def xǁCanonicalCommitIdentityǁcollect_violations__mutmut_21(self) -> set[Path]:
        """Every in-range commit with an off-allowlist author/committer identity.

        The AUTHOR is held strictly to the configured allowlist; the COMMITTER is
        allowed if it is a platform committer (web-flow / Dependabot / Renovate) or
        otherwise on the allowlist — see :meth:`_committer_ok`.
        """
        if not self._configured():
            return set()
        out: set[Path] = set()
        for sha, an, ae, cn, ce in _log_identities(self._repo_root, self._rev_range()):
            bad: list[str] = []
            if not self._identity_ok(an, ae):
                bad.append(f"author {an} <{ae}>")
            if not self._committer_ok(cn, ce):
                bad.append(f"committer {cn} <{ce}>")
            if bad:
                out.add(Path(None))
        return out

    def xǁCanonicalCommitIdentityǁcollect_violations__mutmut_22(self) -> set[Path]:
        """Every in-range commit with an off-allowlist author/committer identity.

        The AUTHOR is held strictly to the configured allowlist; the COMMITTER is
        allowed if it is a platform committer (web-flow / Dependabot / Renovate) or
        otherwise on the allowlist — see :meth:`_committer_ok`.
        """
        if not self._configured():
            return set()
        out: set[Path] = set()
        for sha, an, ae, cn, ce in _log_identities(self._repo_root, self._rev_range()):
            bad: list[str] = []
            if not self._identity_ok(an, ae):
                bad.append(f"author {an} <{ae}>")
            if not self._committer_ok(cn, ce):
                bad.append(f"committer {cn} <{ce}>")
            if bad:
                out.add(Path(f"{sha[:13]} {'; '.join(bad)}"))
        return out

    def xǁCanonicalCommitIdentityǁcollect_violations__mutmut_23(self) -> set[Path]:
        """Every in-range commit with an off-allowlist author/committer identity.

        The AUTHOR is held strictly to the configured allowlist; the COMMITTER is
        allowed if it is a platform committer (web-flow / Dependabot / Renovate) or
        otherwise on the allowlist — see :meth:`_committer_ok`.
        """
        if not self._configured():
            return set()
        out: set[Path] = set()
        for sha, an, ae, cn, ce in _log_identities(self._repo_root, self._rev_range()):
            bad: list[str] = []
            if not self._identity_ok(an, ae):
                bad.append(f"author {an} <{ae}>")
            if not self._committer_ok(cn, ce):
                bad.append(f"committer {cn} <{ce}>")
            if bad:
                out.add(Path(f"{sha[:12]} {'; '.join(None)}"))
        return out

    def xǁCanonicalCommitIdentityǁcollect_violations__mutmut_24(self) -> set[Path]:
        """Every in-range commit with an off-allowlist author/committer identity.

        The AUTHOR is held strictly to the configured allowlist; the COMMITTER is
        allowed if it is a platform committer (web-flow / Dependabot / Renovate) or
        otherwise on the allowlist — see :meth:`_committer_ok`.
        """
        if not self._configured():
            return set()
        out: set[Path] = set()
        for sha, an, ae, cn, ce in _log_identities(self._repo_root, self._rev_range()):
            bad: list[str] = []
            if not self._identity_ok(an, ae):
                bad.append(f"author {an} <{ae}>")
            if not self._committer_ok(cn, ce):
                bad.append(f"committer {cn} <{ce}>")
            if bad:
                out.add(Path(f"{sha[:12]} {'XX; XX'.join(bad)}"))
        return out

mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut['_mutmut_orig'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut['xǁCanonicalCommitIdentityǁfrom_config__mutmut_1'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut['xǁCanonicalCommitIdentityǁfrom_config__mutmut_2'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut['xǁCanonicalCommitIdentityǁfrom_config__mutmut_3'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut['xǁCanonicalCommitIdentityǁfrom_config__mutmut_4'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut['xǁCanonicalCommitIdentityǁfrom_config__mutmut_5'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut['xǁCanonicalCommitIdentityǁfrom_config__mutmut_6'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut['xǁCanonicalCommitIdentityǁfrom_config__mutmut_7'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut['xǁCanonicalCommitIdentityǁfrom_config__mutmut_8'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut['xǁCanonicalCommitIdentityǁfrom_config__mutmut_9'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut['xǁCanonicalCommitIdentityǁfrom_config__mutmut_10'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut['xǁCanonicalCommitIdentityǁfrom_config__mutmut_11'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut['xǁCanonicalCommitIdentityǁfrom_config__mutmut_12'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfrom_config__mutmut_12 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut['xǁCanonicalCommitIdentityǁfrom_config__mutmut_13'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfrom_config__mutmut_13 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut['xǁCanonicalCommitIdentityǁfrom_config__mutmut_14'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfrom_config__mutmut_14 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut['xǁCanonicalCommitIdentityǁfrom_config__mutmut_15'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfrom_config__mutmut_15 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut['xǁCanonicalCommitIdentityǁfrom_config__mutmut_16'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfrom_config__mutmut_16 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut['xǁCanonicalCommitIdentityǁfrom_config__mutmut_17'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfrom_config__mutmut_17 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut['xǁCanonicalCommitIdentityǁfrom_config__mutmut_18'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfrom_config__mutmut_18 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut['xǁCanonicalCommitIdentityǁfrom_config__mutmut_19'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfrom_config__mutmut_19 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut['xǁCanonicalCommitIdentityǁfrom_config__mutmut_20'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfrom_config__mutmut_20 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut['xǁCanonicalCommitIdentityǁfrom_config__mutmut_21'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfrom_config__mutmut_21 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut['xǁCanonicalCommitIdentityǁfrom_config__mutmut_22'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfrom_config__mutmut_22 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut['xǁCanonicalCommitIdentityǁfrom_config__mutmut_23'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfrom_config__mutmut_23 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut['xǁCanonicalCommitIdentityǁfrom_config__mutmut_24'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfrom_config__mutmut_24 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut['xǁCanonicalCommitIdentityǁfrom_config__mutmut_25'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfrom_config__mutmut_25 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut['xǁCanonicalCommitIdentityǁfrom_config__mutmut_26'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfrom_config__mutmut_26 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut['xǁCanonicalCommitIdentityǁfrom_config__mutmut_27'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfrom_config__mutmut_27 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut['xǁCanonicalCommitIdentityǁfrom_config__mutmut_28'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfrom_config__mutmut_28 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut['xǁCanonicalCommitIdentityǁfrom_config__mutmut_29'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfrom_config__mutmut_29 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut['xǁCanonicalCommitIdentityǁfrom_config__mutmut_30'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfrom_config__mutmut_30 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut['xǁCanonicalCommitIdentityǁfrom_config__mutmut_31'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfrom_config__mutmut_31 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut['xǁCanonicalCommitIdentityǁfrom_config__mutmut_32'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfrom_config__mutmut_32 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut['xǁCanonicalCommitIdentityǁfrom_config__mutmut_33'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfrom_config__mutmut_33 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut['xǁCanonicalCommitIdentityǁfrom_config__mutmut_34'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfrom_config__mutmut_34 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut['xǁCanonicalCommitIdentityǁfrom_config__mutmut_35'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfrom_config__mutmut_35 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut['xǁCanonicalCommitIdentityǁfrom_config__mutmut_36'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfrom_config__mutmut_36 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut['xǁCanonicalCommitIdentityǁfrom_config__mutmut_37'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfrom_config__mutmut_37 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁfrom_config__mutmut['xǁCanonicalCommitIdentityǁfrom_config__mutmut_38'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfrom_config__mutmut_38 # type: ignore # mutmut generated

mutants_xǁCanonicalCommitIdentityǁ_configured__mutmut['_mutmut_orig'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁ_configured__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁ_configured__mutmut['xǁCanonicalCommitIdentityǁ_configured__mutmut_1'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁ_configured__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁ_configured__mutmut['xǁCanonicalCommitIdentityǁ_configured__mutmut_2'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁ_configured__mutmut_2 # type: ignore # mutmut generated

mutants_xǁCanonicalCommitIdentityǁ_identity_ok__mutmut['_mutmut_orig'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁ_identity_ok__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁ_identity_ok__mutmut['xǁCanonicalCommitIdentityǁ_identity_ok__mutmut_1'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁ_identity_ok__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁ_identity_ok__mutmut['xǁCanonicalCommitIdentityǁ_identity_ok__mutmut_2'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁ_identity_ok__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁ_identity_ok__mutmut['xǁCanonicalCommitIdentityǁ_identity_ok__mutmut_3'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁ_identity_ok__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁ_identity_ok__mutmut['xǁCanonicalCommitIdentityǁ_identity_ok__mutmut_4'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁ_identity_ok__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁ_identity_ok__mutmut['xǁCanonicalCommitIdentityǁ_identity_ok__mutmut_5'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁ_identity_ok__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁ_identity_ok__mutmut['xǁCanonicalCommitIdentityǁ_identity_ok__mutmut_6'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁ_identity_ok__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁ_identity_ok__mutmut['xǁCanonicalCommitIdentityǁ_identity_ok__mutmut_7'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁ_identity_ok__mutmut_7 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁ_identity_ok__mutmut['xǁCanonicalCommitIdentityǁ_identity_ok__mutmut_8'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁ_identity_ok__mutmut_8 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁ_identity_ok__mutmut['xǁCanonicalCommitIdentityǁ_identity_ok__mutmut_9'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁ_identity_ok__mutmut_9 # type: ignore # mutmut generated

mutants_xǁCanonicalCommitIdentityǁ_committer_ok__mutmut['_mutmut_orig'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁ_committer_ok__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁ_committer_ok__mutmut['xǁCanonicalCommitIdentityǁ_committer_ok__mutmut_1'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁ_committer_ok__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁ_committer_ok__mutmut['xǁCanonicalCommitIdentityǁ_committer_ok__mutmut_2'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁ_committer_ok__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁ_committer_ok__mutmut['xǁCanonicalCommitIdentityǁ_committer_ok__mutmut_3'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁ_committer_ok__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁ_committer_ok__mutmut['xǁCanonicalCommitIdentityǁ_committer_ok__mutmut_4'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁ_committer_ok__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁ_committer_ok__mutmut['xǁCanonicalCommitIdentityǁ_committer_ok__mutmut_5'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁ_committer_ok__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁ_committer_ok__mutmut['xǁCanonicalCommitIdentityǁ_committer_ok__mutmut_6'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁ_committer_ok__mutmut_6 # type: ignore # mutmut generated

mutants_xǁCanonicalCommitIdentityǁfile_has_violation__mutmut['_mutmut_orig'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁfile_has_violation__mutmut['xǁCanonicalCommitIdentityǁfile_has_violation__mutmut_1'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated

mutants_xǁCanonicalCommitIdentityǁcollect_violations__mutmut['_mutmut_orig'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁcollect_violations__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁcollect_violations__mutmut['xǁCanonicalCommitIdentityǁcollect_violations__mutmut_1'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁcollect_violations__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁcollect_violations__mutmut['xǁCanonicalCommitIdentityǁcollect_violations__mutmut_2'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁcollect_violations__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁcollect_violations__mutmut['xǁCanonicalCommitIdentityǁcollect_violations__mutmut_3'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁcollect_violations__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁcollect_violations__mutmut['xǁCanonicalCommitIdentityǁcollect_violations__mutmut_4'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁcollect_violations__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁcollect_violations__mutmut['xǁCanonicalCommitIdentityǁcollect_violations__mutmut_5'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁcollect_violations__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁcollect_violations__mutmut['xǁCanonicalCommitIdentityǁcollect_violations__mutmut_6'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁcollect_violations__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁcollect_violations__mutmut['xǁCanonicalCommitIdentityǁcollect_violations__mutmut_7'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁcollect_violations__mutmut_7 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁcollect_violations__mutmut['xǁCanonicalCommitIdentityǁcollect_violations__mutmut_8'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁcollect_violations__mutmut_8 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁcollect_violations__mutmut['xǁCanonicalCommitIdentityǁcollect_violations__mutmut_9'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁcollect_violations__mutmut_9 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁcollect_violations__mutmut['xǁCanonicalCommitIdentityǁcollect_violations__mutmut_10'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁcollect_violations__mutmut_10 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁcollect_violations__mutmut['xǁCanonicalCommitIdentityǁcollect_violations__mutmut_11'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁcollect_violations__mutmut_11 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁcollect_violations__mutmut['xǁCanonicalCommitIdentityǁcollect_violations__mutmut_12'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁcollect_violations__mutmut_12 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁcollect_violations__mutmut['xǁCanonicalCommitIdentityǁcollect_violations__mutmut_13'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁcollect_violations__mutmut_13 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁcollect_violations__mutmut['xǁCanonicalCommitIdentityǁcollect_violations__mutmut_14'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁcollect_violations__mutmut_14 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁcollect_violations__mutmut['xǁCanonicalCommitIdentityǁcollect_violations__mutmut_15'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁcollect_violations__mutmut_15 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁcollect_violations__mutmut['xǁCanonicalCommitIdentityǁcollect_violations__mutmut_16'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁcollect_violations__mutmut_16 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁcollect_violations__mutmut['xǁCanonicalCommitIdentityǁcollect_violations__mutmut_17'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁcollect_violations__mutmut_17 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁcollect_violations__mutmut['xǁCanonicalCommitIdentityǁcollect_violations__mutmut_18'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁcollect_violations__mutmut_18 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁcollect_violations__mutmut['xǁCanonicalCommitIdentityǁcollect_violations__mutmut_19'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁcollect_violations__mutmut_19 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁcollect_violations__mutmut['xǁCanonicalCommitIdentityǁcollect_violations__mutmut_20'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁcollect_violations__mutmut_20 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁcollect_violations__mutmut['xǁCanonicalCommitIdentityǁcollect_violations__mutmut_21'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁcollect_violations__mutmut_21 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁcollect_violations__mutmut['xǁCanonicalCommitIdentityǁcollect_violations__mutmut_22'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁcollect_violations__mutmut_22 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁcollect_violations__mutmut['xǁCanonicalCommitIdentityǁcollect_violations__mutmut_23'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁcollect_violations__mutmut_23 # type: ignore # mutmut generated
mutants_xǁCanonicalCommitIdentityǁcollect_violations__mutmut['xǁCanonicalCommitIdentityǁcollect_violations__mutmut_24'] = CanonicalCommitIdentity.xǁCanonicalCommitIdentityǁcollect_violations__mutmut_24 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> CanonicalCommitIdentity:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CanonicalCommitIdentity.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> CanonicalCommitIdentity:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CanonicalCommitIdentity.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> CanonicalCommitIdentity:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CanonicalCommitIdentity.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> CanonicalCommitIdentity:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CanonicalCommitIdentity.from_config(config, repo_root=None)


def x_build__mutmut_3(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> CanonicalCommitIdentity:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CanonicalCommitIdentity.from_config(repo_root=repo_root)


def x_build__mutmut_4(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> CanonicalCommitIdentity:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CanonicalCommitIdentity.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(CanonicalCommitIdentity, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(CanonicalCommitIdentity, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(CanonicalCommitIdentity, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(CanonicalCommitIdentity, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
