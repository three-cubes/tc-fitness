"""Tests for the repo-agnostic, config-driven FitnessRule ABC (v0.6.0)."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from tc_fitness.fitness_rule import FitnessRule

pytestmark = pytest.mark.unit

#: An attribution signature `scan_text` flags — the kind of residue vendored test
#: fixtures and pnpm trash dirs legitimately carry (the issue-25 repro).
_ATTRIBUTION = "Co-Authored-By: Claude <noreply@anthropic.com>\n"


class _BadWord(FitnessRule):
    """A trivial concrete rule: a ``.py`` file containing the token ``BADWORD``."""

    name = "bad-word"
    remediation = "fix: remove BADWORD; next: re-run; run: pytest"
    extensions = (".py",)

    def file_has_violation(self, path: Path) -> bool:
        return "BADWORD" in path.read_text(encoding="utf-8")


def _seed(tmp_path: Path, rel: str, body: str) -> None:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")


def _git_init_and_add(repo: Path, *tracked: str) -> None:
    """Init a git repo at ``repo`` and stage ``tracked`` so ``git ls-files`` sees them.

    Staging (``git add``) is enough — ``git ls-files`` reads the index, so no
    commit (and thus no user identity) is required.
    """
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "add", *tracked], cwd=repo, check=True, capture_output=True)


def test_abstract_cannot_instantiate() -> None:
    with pytest.raises(TypeError):
        FitnessRule()  # type: ignore[abstract]
