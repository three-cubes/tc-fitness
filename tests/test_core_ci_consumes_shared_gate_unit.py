"""Tests for the CORE check ci_consumes_shared_gate (CI runs the shared gate)."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from tc_fitness.core_checks.ci_consumes_shared_gate import (
    satisfying_mechanism,
)

pytestmark = pytest.mark.unit

# A workflow that satisfies the reusable arm: a `uses:` reference to the pinned
# canonical python-quality-gate reusable.
_VIA_REUSABLE = (
    "name: Quality gate\n"
    "on: [pull_request]\n"
    "jobs:\n"
    "  quality:\n"
    "    uses: three-cubes/tc-pipelines/.github/workflows/python-quality-gate.yml@v1.13.0\n"
)

# A workflow that satisfies the engine arm: a step that runs `tc-fitness run`.
_VIA_ENGINE = (
    "name: Quality gate\n"
    "on: [pull_request]\n"
    "jobs:\n"
    "  quality:\n"
    "    runs-on: ubuntu-latest\n"
    "    steps:\n"
    "      - run: uv run tc-fitness run\n"
)

# A workflow that consumes NEITHER — a hand-rolled gate forked off the standard.
_FORKED_GATE = (
    "name: Quality gate\n"
    "on: [pull_request]\n"
    "jobs:\n"
    "  quality:\n"
    "    runs-on: ubuntu-latest\n"
    "    steps:\n"
    "      - run: ruff check . && pytest\n"
)


def _write_workflow(tmp_path: Path, name: str, body: str) -> Path:
    p = tmp_path / ".github" / "workflows" / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


# --------------------------------------------------------------------------- #
# Pure-helper unit tests (the detection + enumeration cores).
# --------------------------------------------------------------------------- #


def test_satisfying_mechanism_prefers_reusable() -> None:
    reusable = re.compile(r"three-cubes/tc-pipelines/\.github/workflows/python-quality-gate\.yml@")
    engine = re.compile(r"\btc-fitness run\b")
    # Carries BOTH: a comment mentioning `tc-fitness run` above the `uses:` line.
    both = "# runs tc-fitness run under the hood\n" + _VIA_REUSABLE
    hit = satisfying_mechanism(both, reusable_pattern=reusable, engine_pattern=engine)
    assert hit is not None
    mechanism, _line_no, _line = hit
    assert "reusable-workflow" in mechanism


def test_satisfying_mechanism_none_on_fork() -> None:
    reusable = re.compile(r"three-cubes/tc-pipelines/\.github/workflows/python-quality-gate\.yml@")
    engine = re.compile(r"\btc-fitness run\b")
    assert satisfying_mechanism(_FORKED_GATE, reusable_pattern=reusable, engine_pattern=engine) is None


# --------------------------------------------------------------------------- #
# PASS arms.
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
# FAIL arm — CI present, but the gate is forked off the shared standard.
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
# SKIP arm — no CI workflows to enforce.
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
# WARN mode — a fork is reported but does NOT fail the build (adoption).
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
# Config knobs.
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
# CLI + engine-conformance parity with the sibling CORE checks.
# --------------------------------------------------------------------------- #
