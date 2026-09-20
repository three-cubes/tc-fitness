"""CORE check: cognitive_complexity — Sonar S3776 (Campbell).

Cognitive complexity measures how hard a function is to *read*, not how hard
it is to test. The score climbs with each branch (``if`` / ``elif`` / ``else``
/ ``for`` / ``while`` / ``try`` / ``except`` / ternary / boolean operator) and
is amplified by nesting depth — a triple-nested ``if`` is harder to follow
than three sequential ones. A function scoring above the threshold is flagged;
the file is the unit reported.

Ported from kairix ``scripts/checks/check_cognitive_complexity.py`` (F16) and
re-expressed as a configurable, repo-agnostic rule: the only domain-intrinsic
number is S3776's own default ceiling (15), exposed as a ``threshold`` knob the
consumer overrides via ``[tool.tc_fitness]``. No repo paths or globs are baked
in — the consumer supplies ``roots`` / ``exempt_files``.
"""

from __future__ import annotations

import ast
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: S3776's own default ceiling — domain-intrinsic, not repo identity. Overridable.
DEFAULT_THRESHOLD = 15

REMEDIATION = _remediation(
    fix=(
        "pick the most-nested branch in the flagged function and extract it "
        "into a named helper; or replace an if/elif chain with a dispatch "
        "dict; or invert a guard so the happy path returns early."
    ),
    nxt="re-run this check to confirm the gate goes green.",
    run="python -m tc_fitness.core_checks.cognitive_complexity",
    passing="handler = _HANDLERS.get(cmd, _default); return handler(args)",
    forbidden="nested if/elif chains scoring above the cognitive-complexity ceiling",
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_xǁ_Scorerǁ__init____mutmut: MutantDict = {}  # type: ignore
mutants_xǁ_Scorerǁ_bump__mutmut: MutantDict = {}  # type: ignore
mutants_xǁ_Scorerǁ_walk_nested__mutmut: MutantDict = {}  # type: ignore
mutants_xǁ_Scorerǁvisit_If__mutmut: MutantDict = {}  # type: ignore
mutants_xǁ_Scorerǁvisit_For__mutmut: MutantDict = {}  # type: ignore
mutants_xǁ_Scorerǁvisit_AsyncFor__mutmut: MutantDict = {}  # type: ignore
mutants_xǁ_Scorerǁvisit_While__mutmut: MutantDict = {}  # type: ignore
mutants_xǁ_Scorerǁvisit_Try__mutmut: MutantDict = {}  # type: ignore
mutants_xǁ_Scorerǁvisit_With__mutmut: MutantDict = {}  # type: ignore
mutants_xǁ_Scorerǁvisit_AsyncWith__mutmut: MutantDict = {}  # type: ignore
mutants_xǁ_Scorerǁvisit_BoolOp__mutmut: MutantDict = {}  # type: ignore
mutants_xǁ_Scorerǁvisit_IfExp__mutmut: MutantDict = {}  # type: ignore
mutants_xǁ_Scorerǁvisit_FunctionDef__mutmut: MutantDict = {}  # type: ignore
mutants_xǁ_Scorerǁvisit_AsyncFunctionDef__mutmut: MutantDict = {}  # type: ignore


class _Scorer(ast.NodeVisitor):
    """Accumulate a cognitive-complexity score for one function body.

    The ``nesting`` counter rises on every branch construct and is added to
    each subsequent branch encountered inside it (the nesting amplifier).
    """

    @_mutmut_mutated(mutants_xǁ_Scorerǁ__init____mutmut)
    def __init__(self) -> None:
        self.score = 0
        self.nesting = 0

    def xǁ_Scorerǁ__init____mutmut_orig(self) -> None:
        self.score = 0
        self.nesting = 0

    def xǁ_Scorerǁ__init____mutmut_1(self) -> None:
        self.score = None
        self.nesting = 0

    def xǁ_Scorerǁ__init____mutmut_2(self) -> None:
        self.score = 1
        self.nesting = 0

    def xǁ_Scorerǁ__init____mutmut_3(self) -> None:
        self.score = 0
        self.nesting = None

    def xǁ_Scorerǁ__init____mutmut_4(self) -> None:
        self.score = 0
        self.nesting = 1

    @_mutmut_mutated(mutants_xǁ_Scorerǁ_bump__mutmut)
    def _bump(self) -> None:
        self.score += 1 + self.nesting

    def xǁ_Scorerǁ_bump__mutmut_orig(self) -> None:
        self.score += 1 + self.nesting

    def xǁ_Scorerǁ_bump__mutmut_1(self) -> None:
        self.score = 1 + self.nesting

    def xǁ_Scorerǁ_bump__mutmut_2(self) -> None:
        self.score -= 1 + self.nesting

    def xǁ_Scorerǁ_bump__mutmut_3(self) -> None:
        self.score += 1 - self.nesting

    def xǁ_Scorerǁ_bump__mutmut_4(self) -> None:
        self.score += 2 + self.nesting

    @_mutmut_mutated(mutants_xǁ_Scorerǁ_walk_nested__mutmut)
    def _walk_nested(self, body: list[ast.stmt]) -> None:
        self.nesting += 1
        for child in body:
            self.visit(child)
        self.nesting -= 1

    def xǁ_Scorerǁ_walk_nested__mutmut_orig(self, body: list[ast.stmt]) -> None:
        self.nesting += 1
        for child in body:
            self.visit(child)
        self.nesting -= 1

    def xǁ_Scorerǁ_walk_nested__mutmut_1(self, body: list[ast.stmt]) -> None:
        self.nesting = 1
        for child in body:
            self.visit(child)
        self.nesting -= 1

    def xǁ_Scorerǁ_walk_nested__mutmut_2(self, body: list[ast.stmt]) -> None:
        self.nesting -= 1
        for child in body:
            self.visit(child)
        self.nesting -= 1

    def xǁ_Scorerǁ_walk_nested__mutmut_3(self, body: list[ast.stmt]) -> None:
        self.nesting += 2
        for child in body:
            self.visit(child)
        self.nesting -= 1

    def xǁ_Scorerǁ_walk_nested__mutmut_4(self, body: list[ast.stmt]) -> None:
        self.nesting += 1
        for child in body:
            self.visit(None)
        self.nesting -= 1

    def xǁ_Scorerǁ_walk_nested__mutmut_5(self, body: list[ast.stmt]) -> None:
        self.nesting += 1
        for child in body:
            self.visit(child)
        self.nesting = 1

    def xǁ_Scorerǁ_walk_nested__mutmut_6(self, body: list[ast.stmt]) -> None:
        self.nesting += 1
        for child in body:
            self.visit(child)
        self.nesting += 1

    def xǁ_Scorerǁ_walk_nested__mutmut_7(self, body: list[ast.stmt]) -> None:
        self.nesting += 1
        for child in body:
            self.visit(child)
        self.nesting -= 2

    @_mutmut_mutated(mutants_xǁ_Scorerǁvisit_If__mutmut)
    def visit_If(self, node: ast.If) -> None:
        self._bump()
        self.visit(node.test)
        self._walk_nested(node.body)
        if node.orelse:
            # An ``elif`` is a single nested If in orelse — recurse so it is
            # counted once; a plain ``else`` body bumps and nests.
            if len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If):
                self.visit(node.orelse[0])
            else:
                self._bump()
                self._walk_nested(node.orelse)

    def xǁ_Scorerǁvisit_If__mutmut_orig(self, node: ast.If) -> None:
        self._bump()
        self.visit(node.test)
        self._walk_nested(node.body)
        if node.orelse:
            # An ``elif`` is a single nested If in orelse — recurse so it is
            # counted once; a plain ``else`` body bumps and nests.
            if len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If):
                self.visit(node.orelse[0])
            else:
                self._bump()
                self._walk_nested(node.orelse)

    def xǁ_Scorerǁvisit_If__mutmut_1(self, node: ast.If) -> None:
        self._bump()
        self.visit(None)
        self._walk_nested(node.body)
        if node.orelse:
            # An ``elif`` is a single nested If in orelse — recurse so it is
            # counted once; a plain ``else`` body bumps and nests.
            if len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If):
                self.visit(node.orelse[0])
            else:
                self._bump()
                self._walk_nested(node.orelse)

    def xǁ_Scorerǁvisit_If__mutmut_2(self, node: ast.If) -> None:
        self._bump()
        self.visit(node.test)
        self._walk_nested(None)
        if node.orelse:
            # An ``elif`` is a single nested If in orelse — recurse so it is
            # counted once; a plain ``else`` body bumps and nests.
            if len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If):
                self.visit(node.orelse[0])
            else:
                self._bump()
                self._walk_nested(node.orelse)

    def xǁ_Scorerǁvisit_If__mutmut_3(self, node: ast.If) -> None:
        self._bump()
        self.visit(node.test)
        self._walk_nested(node.body)
        if node.orelse:
            # An ``elif`` is a single nested If in orelse — recurse so it is
            # counted once; a plain ``else`` body bumps and nests.
            if len(node.orelse) == 1 or isinstance(node.orelse[0], ast.If):
                self.visit(node.orelse[0])
            else:
                self._bump()
                self._walk_nested(node.orelse)

    def xǁ_Scorerǁvisit_If__mutmut_4(self, node: ast.If) -> None:
        self._bump()
        self.visit(node.test)
        self._walk_nested(node.body)
        if node.orelse:
            # An ``elif`` is a single nested If in orelse — recurse so it is
            # counted once; a plain ``else`` body bumps and nests.
            if len(node.orelse) != 1 and isinstance(node.orelse[0], ast.If):
                self.visit(node.orelse[0])
            else:
                self._bump()
                self._walk_nested(node.orelse)

    def xǁ_Scorerǁvisit_If__mutmut_5(self, node: ast.If) -> None:
        self._bump()
        self.visit(node.test)
        self._walk_nested(node.body)
        if node.orelse:
            # An ``elif`` is a single nested If in orelse — recurse so it is
            # counted once; a plain ``else`` body bumps and nests.
            if len(node.orelse) == 2 and isinstance(node.orelse[0], ast.If):
                self.visit(node.orelse[0])
            else:
                self._bump()
                self._walk_nested(node.orelse)

    def xǁ_Scorerǁvisit_If__mutmut_6(self, node: ast.If) -> None:
        self._bump()
        self.visit(node.test)
        self._walk_nested(node.body)
        if node.orelse:
            # An ``elif`` is a single nested If in orelse — recurse so it is
            # counted once; a plain ``else`` body bumps and nests.
            if len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If):
                self.visit(None)
            else:
                self._bump()
                self._walk_nested(node.orelse)

    def xǁ_Scorerǁvisit_If__mutmut_7(self, node: ast.If) -> None:
        self._bump()
        self.visit(node.test)
        self._walk_nested(node.body)
        if node.orelse:
            # An ``elif`` is a single nested If in orelse — recurse so it is
            # counted once; a plain ``else`` body bumps and nests.
            if len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If):
                self.visit(node.orelse[1])
            else:
                self._bump()
                self._walk_nested(node.orelse)

    def xǁ_Scorerǁvisit_If__mutmut_8(self, node: ast.If) -> None:
        self._bump()
        self.visit(node.test)
        self._walk_nested(node.body)
        if node.orelse:
            # An ``elif`` is a single nested If in orelse — recurse so it is
            # counted once; a plain ``else`` body bumps and nests.
            if len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If):
                self.visit(node.orelse[0])
            else:
                self._bump()
                self._walk_nested(None)

    @_mutmut_mutated(mutants_xǁ_Scorerǁvisit_For__mutmut)
    def visit_For(self, node: ast.For) -> None:
        self._bump()
        self._walk_nested(node.body)
        if node.orelse:
            self._walk_nested(node.orelse)

    def xǁ_Scorerǁvisit_For__mutmut_orig(self, node: ast.For) -> None:
        self._bump()
        self._walk_nested(node.body)
        if node.orelse:
            self._walk_nested(node.orelse)

    def xǁ_Scorerǁvisit_For__mutmut_1(self, node: ast.For) -> None:
        self._bump()
        self._walk_nested(None)
        if node.orelse:
            self._walk_nested(node.orelse)

    def xǁ_Scorerǁvisit_For__mutmut_2(self, node: ast.For) -> None:
        self._bump()
        self._walk_nested(node.body)
        if node.orelse:
            self._walk_nested(None)

    @_mutmut_mutated(mutants_xǁ_Scorerǁvisit_AsyncFor__mutmut)
    def visit_AsyncFor(self, node: ast.AsyncFor) -> None:
        self._bump()
        self._walk_nested(node.body)
        if node.orelse:
            self._walk_nested(node.orelse)

    def xǁ_Scorerǁvisit_AsyncFor__mutmut_orig(self, node: ast.AsyncFor) -> None:
        self._bump()
        self._walk_nested(node.body)
        if node.orelse:
            self._walk_nested(node.orelse)

    def xǁ_Scorerǁvisit_AsyncFor__mutmut_1(self, node: ast.AsyncFor) -> None:
        self._bump()
        self._walk_nested(None)
        if node.orelse:
            self._walk_nested(node.orelse)

    def xǁ_Scorerǁvisit_AsyncFor__mutmut_2(self, node: ast.AsyncFor) -> None:
        self._bump()
        self._walk_nested(node.body)
        if node.orelse:
            self._walk_nested(None)

    @_mutmut_mutated(mutants_xǁ_Scorerǁvisit_While__mutmut)
    def visit_While(self, node: ast.While) -> None:
        self._bump()
        self.visit(node.test)
        self._walk_nested(node.body)
        if node.orelse:
            self._walk_nested(node.orelse)

    def xǁ_Scorerǁvisit_While__mutmut_orig(self, node: ast.While) -> None:
        self._bump()
        self.visit(node.test)
        self._walk_nested(node.body)
        if node.orelse:
            self._walk_nested(node.orelse)

    def xǁ_Scorerǁvisit_While__mutmut_1(self, node: ast.While) -> None:
        self._bump()
        self.visit(None)
        self._walk_nested(node.body)
        if node.orelse:
            self._walk_nested(node.orelse)

    def xǁ_Scorerǁvisit_While__mutmut_2(self, node: ast.While) -> None:
        self._bump()
        self.visit(node.test)
        self._walk_nested(None)
        if node.orelse:
            self._walk_nested(node.orelse)

    def xǁ_Scorerǁvisit_While__mutmut_3(self, node: ast.While) -> None:
        self._bump()
        self.visit(node.test)
        self._walk_nested(node.body)
        if node.orelse:
            self._walk_nested(None)

    @_mutmut_mutated(mutants_xǁ_Scorerǁvisit_Try__mutmut)
    def visit_Try(self, node: ast.Try) -> None:
        self._bump()
        self._walk_nested(node.body)
        for handler in node.handlers:
            self._bump()
            self._walk_nested(handler.body)
        if node.orelse:
            self._walk_nested(node.orelse)
        if node.finalbody:
            self._walk_nested(node.finalbody)

    def xǁ_Scorerǁvisit_Try__mutmut_orig(self, node: ast.Try) -> None:
        self._bump()
        self._walk_nested(node.body)
        for handler in node.handlers:
            self._bump()
            self._walk_nested(handler.body)
        if node.orelse:
            self._walk_nested(node.orelse)
        if node.finalbody:
            self._walk_nested(node.finalbody)

    def xǁ_Scorerǁvisit_Try__mutmut_1(self, node: ast.Try) -> None:
        self._bump()
        self._walk_nested(None)
        for handler in node.handlers:
            self._bump()
            self._walk_nested(handler.body)
        if node.orelse:
            self._walk_nested(node.orelse)
        if node.finalbody:
            self._walk_nested(node.finalbody)

    def xǁ_Scorerǁvisit_Try__mutmut_2(self, node: ast.Try) -> None:
        self._bump()
        self._walk_nested(node.body)
        for handler in node.handlers:
            self._bump()
            self._walk_nested(None)
        if node.orelse:
            self._walk_nested(node.orelse)
        if node.finalbody:
            self._walk_nested(node.finalbody)

    def xǁ_Scorerǁvisit_Try__mutmut_3(self, node: ast.Try) -> None:
        self._bump()
        self._walk_nested(node.body)
        for handler in node.handlers:
            self._bump()
            self._walk_nested(handler.body)
        if node.orelse:
            self._walk_nested(None)
        if node.finalbody:
            self._walk_nested(node.finalbody)

    def xǁ_Scorerǁvisit_Try__mutmut_4(self, node: ast.Try) -> None:
        self._bump()
        self._walk_nested(node.body)
        for handler in node.handlers:
            self._bump()
            self._walk_nested(handler.body)
        if node.orelse:
            self._walk_nested(node.orelse)
        if node.finalbody:
            self._walk_nested(None)

    @_mutmut_mutated(mutants_xǁ_Scorerǁvisit_With__mutmut)
    def visit_With(self, node: ast.With) -> None:
        # ``with`` does not branch, so it adds nothing to the score.
        self.generic_visit(node)

    def xǁ_Scorerǁvisit_With__mutmut_orig(self, node: ast.With) -> None:
        # ``with`` does not branch, so it adds nothing to the score.
        self.generic_visit(node)

    def xǁ_Scorerǁvisit_With__mutmut_1(self, node: ast.With) -> None:
        # ``with`` does not branch, so it adds nothing to the score.
        self.generic_visit(None)

    @_mutmut_mutated(mutants_xǁ_Scorerǁvisit_AsyncWith__mutmut)
    def visit_AsyncWith(self, node: ast.AsyncWith) -> None:
        self.generic_visit(node)

    def xǁ_Scorerǁvisit_AsyncWith__mutmut_orig(self, node: ast.AsyncWith) -> None:
        self.generic_visit(node)

    def xǁ_Scorerǁvisit_AsyncWith__mutmut_1(self, node: ast.AsyncWith) -> None:
        self.generic_visit(None)

    @_mutmut_mutated(mutants_xǁ_Scorerǁvisit_BoolOp__mutmut)
    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        # A chain ``a and b and c`` has two operators → +2 (flat, no amplifier).
        self.score += max(len(node.values) - 1, 0)
        self.generic_visit(node)

    def xǁ_Scorerǁvisit_BoolOp__mutmut_orig(self, node: ast.BoolOp) -> None:
        # A chain ``a and b and c`` has two operators → +2 (flat, no amplifier).
        self.score += max(len(node.values) - 1, 0)
        self.generic_visit(node)

    def xǁ_Scorerǁvisit_BoolOp__mutmut_1(self, node: ast.BoolOp) -> None:
        # A chain ``a and b and c`` has two operators → +2 (flat, no amplifier).
        self.score = max(len(node.values) - 1, 0)
        self.generic_visit(node)

    def xǁ_Scorerǁvisit_BoolOp__mutmut_2(self, node: ast.BoolOp) -> None:
        # A chain ``a and b and c`` has two operators → +2 (flat, no amplifier).
        self.score -= max(len(node.values) - 1, 0)
        self.generic_visit(node)

    def xǁ_Scorerǁvisit_BoolOp__mutmut_3(self, node: ast.BoolOp) -> None:
        # A chain ``a and b and c`` has two operators → +2 (flat, no amplifier).
        self.score += max(None, 0)
        self.generic_visit(node)

    def xǁ_Scorerǁvisit_BoolOp__mutmut_4(self, node: ast.BoolOp) -> None:
        # A chain ``a and b and c`` has two operators → +2 (flat, no amplifier).
        self.score += max(len(node.values) - 1, None)
        self.generic_visit(node)

    def xǁ_Scorerǁvisit_BoolOp__mutmut_5(self, node: ast.BoolOp) -> None:
        # A chain ``a and b and c`` has two operators → +2 (flat, no amplifier).
        self.score += max(0)
        self.generic_visit(node)

    def xǁ_Scorerǁvisit_BoolOp__mutmut_6(self, node: ast.BoolOp) -> None:
        # A chain ``a and b and c`` has two operators → +2 (flat, no amplifier).
        self.score += max(len(node.values) - 1, )
        self.generic_visit(node)

    def xǁ_Scorerǁvisit_BoolOp__mutmut_7(self, node: ast.BoolOp) -> None:
        # A chain ``a and b and c`` has two operators → +2 (flat, no amplifier).
        self.score += max(len(node.values) + 1, 0)
        self.generic_visit(node)

    def xǁ_Scorerǁvisit_BoolOp__mutmut_8(self, node: ast.BoolOp) -> None:
        # A chain ``a and b and c`` has two operators → +2 (flat, no amplifier).
        self.score += max(len(node.values) - 2, 0)
        self.generic_visit(node)

    def xǁ_Scorerǁvisit_BoolOp__mutmut_9(self, node: ast.BoolOp) -> None:
        # A chain ``a and b and c`` has two operators → +2 (flat, no amplifier).
        self.score += max(len(node.values) - 1, 1)
        self.generic_visit(node)

    def xǁ_Scorerǁvisit_BoolOp__mutmut_10(self, node: ast.BoolOp) -> None:
        # A chain ``a and b and c`` has two operators → +2 (flat, no amplifier).
        self.score += max(len(node.values) - 1, 0)
        self.generic_visit(None)

    @_mutmut_mutated(mutants_xǁ_Scorerǁvisit_IfExp__mutmut)
    def visit_IfExp(self, node: ast.IfExp) -> None:
        self._bump()
        self.generic_visit(node)

    def xǁ_Scorerǁvisit_IfExp__mutmut_orig(self, node: ast.IfExp) -> None:
        self._bump()
        self.generic_visit(node)

    def xǁ_Scorerǁvisit_IfExp__mutmut_1(self, node: ast.IfExp) -> None:
        self._bump()
        self.generic_visit(None)

    @_mutmut_mutated(mutants_xǁ_Scorerǁvisit_FunctionDef__mutmut)
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.generic_visit(node)

    def xǁ_Scorerǁvisit_FunctionDef__mutmut_orig(self, node: ast.FunctionDef) -> None:
        self.generic_visit(node)

    def xǁ_Scorerǁvisit_FunctionDef__mutmut_1(self, node: ast.FunctionDef) -> None:
        self.generic_visit(None)

    @_mutmut_mutated(mutants_xǁ_Scorerǁvisit_AsyncFunctionDef__mutmut)
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self.generic_visit(node)

    def xǁ_Scorerǁvisit_AsyncFunctionDef__mutmut_orig(self, node: ast.AsyncFunctionDef) -> None:
        self.generic_visit(node)

    def xǁ_Scorerǁvisit_AsyncFunctionDef__mutmut_1(self, node: ast.AsyncFunctionDef) -> None:
        self.generic_visit(None)

mutants_xǁ_Scorerǁ__init____mutmut['_mutmut_orig'] = _Scorer.xǁ_Scorerǁ__init____mutmut_orig # type: ignore # mutmut generated
mutants_xǁ_Scorerǁ__init____mutmut['xǁ_Scorerǁ__init____mutmut_1'] = _Scorer.xǁ_Scorerǁ__init____mutmut_1 # type: ignore # mutmut generated
mutants_xǁ_Scorerǁ__init____mutmut['xǁ_Scorerǁ__init____mutmut_2'] = _Scorer.xǁ_Scorerǁ__init____mutmut_2 # type: ignore # mutmut generated
mutants_xǁ_Scorerǁ__init____mutmut['xǁ_Scorerǁ__init____mutmut_3'] = _Scorer.xǁ_Scorerǁ__init____mutmut_3 # type: ignore # mutmut generated
mutants_xǁ_Scorerǁ__init____mutmut['xǁ_Scorerǁ__init____mutmut_4'] = _Scorer.xǁ_Scorerǁ__init____mutmut_4 # type: ignore # mutmut generated

mutants_xǁ_Scorerǁ_bump__mutmut['_mutmut_orig'] = _Scorer.xǁ_Scorerǁ_bump__mutmut_orig # type: ignore # mutmut generated
mutants_xǁ_Scorerǁ_bump__mutmut['xǁ_Scorerǁ_bump__mutmut_1'] = _Scorer.xǁ_Scorerǁ_bump__mutmut_1 # type: ignore # mutmut generated
mutants_xǁ_Scorerǁ_bump__mutmut['xǁ_Scorerǁ_bump__mutmut_2'] = _Scorer.xǁ_Scorerǁ_bump__mutmut_2 # type: ignore # mutmut generated
mutants_xǁ_Scorerǁ_bump__mutmut['xǁ_Scorerǁ_bump__mutmut_3'] = _Scorer.xǁ_Scorerǁ_bump__mutmut_3 # type: ignore # mutmut generated
mutants_xǁ_Scorerǁ_bump__mutmut['xǁ_Scorerǁ_bump__mutmut_4'] = _Scorer.xǁ_Scorerǁ_bump__mutmut_4 # type: ignore # mutmut generated

mutants_xǁ_Scorerǁ_walk_nested__mutmut['_mutmut_orig'] = _Scorer.xǁ_Scorerǁ_walk_nested__mutmut_orig # type: ignore # mutmut generated
mutants_xǁ_Scorerǁ_walk_nested__mutmut['xǁ_Scorerǁ_walk_nested__mutmut_1'] = _Scorer.xǁ_Scorerǁ_walk_nested__mutmut_1 # type: ignore # mutmut generated
mutants_xǁ_Scorerǁ_walk_nested__mutmut['xǁ_Scorerǁ_walk_nested__mutmut_2'] = _Scorer.xǁ_Scorerǁ_walk_nested__mutmut_2 # type: ignore # mutmut generated
mutants_xǁ_Scorerǁ_walk_nested__mutmut['xǁ_Scorerǁ_walk_nested__mutmut_3'] = _Scorer.xǁ_Scorerǁ_walk_nested__mutmut_3 # type: ignore # mutmut generated
mutants_xǁ_Scorerǁ_walk_nested__mutmut['xǁ_Scorerǁ_walk_nested__mutmut_4'] = _Scorer.xǁ_Scorerǁ_walk_nested__mutmut_4 # type: ignore # mutmut generated
mutants_xǁ_Scorerǁ_walk_nested__mutmut['xǁ_Scorerǁ_walk_nested__mutmut_5'] = _Scorer.xǁ_Scorerǁ_walk_nested__mutmut_5 # type: ignore # mutmut generated
mutants_xǁ_Scorerǁ_walk_nested__mutmut['xǁ_Scorerǁ_walk_nested__mutmut_6'] = _Scorer.xǁ_Scorerǁ_walk_nested__mutmut_6 # type: ignore # mutmut generated
mutants_xǁ_Scorerǁ_walk_nested__mutmut['xǁ_Scorerǁ_walk_nested__mutmut_7'] = _Scorer.xǁ_Scorerǁ_walk_nested__mutmut_7 # type: ignore # mutmut generated

mutants_xǁ_Scorerǁvisit_If__mutmut['_mutmut_orig'] = _Scorer.xǁ_Scorerǁvisit_If__mutmut_orig # type: ignore # mutmut generated
mutants_xǁ_Scorerǁvisit_If__mutmut['xǁ_Scorerǁvisit_If__mutmut_1'] = _Scorer.xǁ_Scorerǁvisit_If__mutmut_1 # type: ignore # mutmut generated
mutants_xǁ_Scorerǁvisit_If__mutmut['xǁ_Scorerǁvisit_If__mutmut_2'] = _Scorer.xǁ_Scorerǁvisit_If__mutmut_2 # type: ignore # mutmut generated
mutants_xǁ_Scorerǁvisit_If__mutmut['xǁ_Scorerǁvisit_If__mutmut_3'] = _Scorer.xǁ_Scorerǁvisit_If__mutmut_3 # type: ignore # mutmut generated
mutants_xǁ_Scorerǁvisit_If__mutmut['xǁ_Scorerǁvisit_If__mutmut_4'] = _Scorer.xǁ_Scorerǁvisit_If__mutmut_4 # type: ignore # mutmut generated
mutants_xǁ_Scorerǁvisit_If__mutmut['xǁ_Scorerǁvisit_If__mutmut_5'] = _Scorer.xǁ_Scorerǁvisit_If__mutmut_5 # type: ignore # mutmut generated
mutants_xǁ_Scorerǁvisit_If__mutmut['xǁ_Scorerǁvisit_If__mutmut_6'] = _Scorer.xǁ_Scorerǁvisit_If__mutmut_6 # type: ignore # mutmut generated
mutants_xǁ_Scorerǁvisit_If__mutmut['xǁ_Scorerǁvisit_If__mutmut_7'] = _Scorer.xǁ_Scorerǁvisit_If__mutmut_7 # type: ignore # mutmut generated
mutants_xǁ_Scorerǁvisit_If__mutmut['xǁ_Scorerǁvisit_If__mutmut_8'] = _Scorer.xǁ_Scorerǁvisit_If__mutmut_8 # type: ignore # mutmut generated

mutants_xǁ_Scorerǁvisit_For__mutmut['_mutmut_orig'] = _Scorer.xǁ_Scorerǁvisit_For__mutmut_orig # type: ignore # mutmut generated
mutants_xǁ_Scorerǁvisit_For__mutmut['xǁ_Scorerǁvisit_For__mutmut_1'] = _Scorer.xǁ_Scorerǁvisit_For__mutmut_1 # type: ignore # mutmut generated
mutants_xǁ_Scorerǁvisit_For__mutmut['xǁ_Scorerǁvisit_For__mutmut_2'] = _Scorer.xǁ_Scorerǁvisit_For__mutmut_2 # type: ignore # mutmut generated

mutants_xǁ_Scorerǁvisit_AsyncFor__mutmut['_mutmut_orig'] = _Scorer.xǁ_Scorerǁvisit_AsyncFor__mutmut_orig # type: ignore # mutmut generated
mutants_xǁ_Scorerǁvisit_AsyncFor__mutmut['xǁ_Scorerǁvisit_AsyncFor__mutmut_1'] = _Scorer.xǁ_Scorerǁvisit_AsyncFor__mutmut_1 # type: ignore # mutmut generated
mutants_xǁ_Scorerǁvisit_AsyncFor__mutmut['xǁ_Scorerǁvisit_AsyncFor__mutmut_2'] = _Scorer.xǁ_Scorerǁvisit_AsyncFor__mutmut_2 # type: ignore # mutmut generated

mutants_xǁ_Scorerǁvisit_While__mutmut['_mutmut_orig'] = _Scorer.xǁ_Scorerǁvisit_While__mutmut_orig # type: ignore # mutmut generated
mutants_xǁ_Scorerǁvisit_While__mutmut['xǁ_Scorerǁvisit_While__mutmut_1'] = _Scorer.xǁ_Scorerǁvisit_While__mutmut_1 # type: ignore # mutmut generated
mutants_xǁ_Scorerǁvisit_While__mutmut['xǁ_Scorerǁvisit_While__mutmut_2'] = _Scorer.xǁ_Scorerǁvisit_While__mutmut_2 # type: ignore # mutmut generated
mutants_xǁ_Scorerǁvisit_While__mutmut['xǁ_Scorerǁvisit_While__mutmut_3'] = _Scorer.xǁ_Scorerǁvisit_While__mutmut_3 # type: ignore # mutmut generated

mutants_xǁ_Scorerǁvisit_Try__mutmut['_mutmut_orig'] = _Scorer.xǁ_Scorerǁvisit_Try__mutmut_orig # type: ignore # mutmut generated
mutants_xǁ_Scorerǁvisit_Try__mutmut['xǁ_Scorerǁvisit_Try__mutmut_1'] = _Scorer.xǁ_Scorerǁvisit_Try__mutmut_1 # type: ignore # mutmut generated
mutants_xǁ_Scorerǁvisit_Try__mutmut['xǁ_Scorerǁvisit_Try__mutmut_2'] = _Scorer.xǁ_Scorerǁvisit_Try__mutmut_2 # type: ignore # mutmut generated
mutants_xǁ_Scorerǁvisit_Try__mutmut['xǁ_Scorerǁvisit_Try__mutmut_3'] = _Scorer.xǁ_Scorerǁvisit_Try__mutmut_3 # type: ignore # mutmut generated
mutants_xǁ_Scorerǁvisit_Try__mutmut['xǁ_Scorerǁvisit_Try__mutmut_4'] = _Scorer.xǁ_Scorerǁvisit_Try__mutmut_4 # type: ignore # mutmut generated

mutants_xǁ_Scorerǁvisit_With__mutmut['_mutmut_orig'] = _Scorer.xǁ_Scorerǁvisit_With__mutmut_orig # type: ignore # mutmut generated
mutants_xǁ_Scorerǁvisit_With__mutmut['xǁ_Scorerǁvisit_With__mutmut_1'] = _Scorer.xǁ_Scorerǁvisit_With__mutmut_1 # type: ignore # mutmut generated

mutants_xǁ_Scorerǁvisit_AsyncWith__mutmut['_mutmut_orig'] = _Scorer.xǁ_Scorerǁvisit_AsyncWith__mutmut_orig # type: ignore # mutmut generated
mutants_xǁ_Scorerǁvisit_AsyncWith__mutmut['xǁ_Scorerǁvisit_AsyncWith__mutmut_1'] = _Scorer.xǁ_Scorerǁvisit_AsyncWith__mutmut_1 # type: ignore # mutmut generated

mutants_xǁ_Scorerǁvisit_BoolOp__mutmut['_mutmut_orig'] = _Scorer.xǁ_Scorerǁvisit_BoolOp__mutmut_orig # type: ignore # mutmut generated
mutants_xǁ_Scorerǁvisit_BoolOp__mutmut['xǁ_Scorerǁvisit_BoolOp__mutmut_1'] = _Scorer.xǁ_Scorerǁvisit_BoolOp__mutmut_1 # type: ignore # mutmut generated
mutants_xǁ_Scorerǁvisit_BoolOp__mutmut['xǁ_Scorerǁvisit_BoolOp__mutmut_2'] = _Scorer.xǁ_Scorerǁvisit_BoolOp__mutmut_2 # type: ignore # mutmut generated
mutants_xǁ_Scorerǁvisit_BoolOp__mutmut['xǁ_Scorerǁvisit_BoolOp__mutmut_3'] = _Scorer.xǁ_Scorerǁvisit_BoolOp__mutmut_3 # type: ignore # mutmut generated
mutants_xǁ_Scorerǁvisit_BoolOp__mutmut['xǁ_Scorerǁvisit_BoolOp__mutmut_4'] = _Scorer.xǁ_Scorerǁvisit_BoolOp__mutmut_4 # type: ignore # mutmut generated
mutants_xǁ_Scorerǁvisit_BoolOp__mutmut['xǁ_Scorerǁvisit_BoolOp__mutmut_5'] = _Scorer.xǁ_Scorerǁvisit_BoolOp__mutmut_5 # type: ignore # mutmut generated
mutants_xǁ_Scorerǁvisit_BoolOp__mutmut['xǁ_Scorerǁvisit_BoolOp__mutmut_6'] = _Scorer.xǁ_Scorerǁvisit_BoolOp__mutmut_6 # type: ignore # mutmut generated
mutants_xǁ_Scorerǁvisit_BoolOp__mutmut['xǁ_Scorerǁvisit_BoolOp__mutmut_7'] = _Scorer.xǁ_Scorerǁvisit_BoolOp__mutmut_7 # type: ignore # mutmut generated
mutants_xǁ_Scorerǁvisit_BoolOp__mutmut['xǁ_Scorerǁvisit_BoolOp__mutmut_8'] = _Scorer.xǁ_Scorerǁvisit_BoolOp__mutmut_8 # type: ignore # mutmut generated
mutants_xǁ_Scorerǁvisit_BoolOp__mutmut['xǁ_Scorerǁvisit_BoolOp__mutmut_9'] = _Scorer.xǁ_Scorerǁvisit_BoolOp__mutmut_9 # type: ignore # mutmut generated
mutants_xǁ_Scorerǁvisit_BoolOp__mutmut['xǁ_Scorerǁvisit_BoolOp__mutmut_10'] = _Scorer.xǁ_Scorerǁvisit_BoolOp__mutmut_10 # type: ignore # mutmut generated

mutants_xǁ_Scorerǁvisit_IfExp__mutmut['_mutmut_orig'] = _Scorer.xǁ_Scorerǁvisit_IfExp__mutmut_orig # type: ignore # mutmut generated
mutants_xǁ_Scorerǁvisit_IfExp__mutmut['xǁ_Scorerǁvisit_IfExp__mutmut_1'] = _Scorer.xǁ_Scorerǁvisit_IfExp__mutmut_1 # type: ignore # mutmut generated

mutants_xǁ_Scorerǁvisit_FunctionDef__mutmut['_mutmut_orig'] = _Scorer.xǁ_Scorerǁvisit_FunctionDef__mutmut_orig # type: ignore # mutmut generated
mutants_xǁ_Scorerǁvisit_FunctionDef__mutmut['xǁ_Scorerǁvisit_FunctionDef__mutmut_1'] = _Scorer.xǁ_Scorerǁvisit_FunctionDef__mutmut_1 # type: ignore # mutmut generated

mutants_xǁ_Scorerǁvisit_AsyncFunctionDef__mutmut['_mutmut_orig'] = _Scorer.xǁ_Scorerǁvisit_AsyncFunctionDef__mutmut_orig # type: ignore # mutmut generated
mutants_xǁ_Scorerǁvisit_AsyncFunctionDef__mutmut['xǁ_Scorerǁvisit_AsyncFunctionDef__mutmut_1'] = _Scorer.xǁ_Scorerǁvisit_AsyncFunctionDef__mutmut_1 # type: ignore # mutmut generated
mutants_x__score_function__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__score_function__mutmut)
def _score_function(func: ast.FunctionDef | ast.AsyncFunctionDef) -> int:
    scorer = _Scorer()
    for stmt in func.body:
        scorer.visit(stmt)
    return scorer.score


def x__score_function__mutmut_orig(func: ast.FunctionDef | ast.AsyncFunctionDef) -> int:
    scorer = _Scorer()
    for stmt in func.body:
        scorer.visit(stmt)
    return scorer.score


def x__score_function__mutmut_1(func: ast.FunctionDef | ast.AsyncFunctionDef) -> int:
    scorer = None
    for stmt in func.body:
        scorer.visit(stmt)
    return scorer.score


def x__score_function__mutmut_2(func: ast.FunctionDef | ast.AsyncFunctionDef) -> int:
    scorer = _Scorer()
    for stmt in func.body:
        scorer.visit(None)
    return scorer.score

mutants_x__score_function__mutmut['_mutmut_orig'] = x__score_function__mutmut_orig # type: ignore # mutmut generated
mutants_x__score_function__mutmut['x__score_function__mutmut_1'] = x__score_function__mutmut_1 # type: ignore # mutmut generated
mutants_x__score_function__mutmut['x__score_function__mutmut_2'] = x__score_function__mutmut_2 # type: ignore # mutmut generated
mutants_x_module_over_threshold__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_module_over_threshold__mutmut)
def module_over_threshold(path: Path, *, threshold: int) -> bool:
    """True iff any function in ``path`` scores above ``threshold``.

    Pure helper (the detection core) so tests assert on it directly. A syntax /
    decode error is treated as "no violation" — another check owns unparseable
    files.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _score_function(node) > threshold:
            return True
    return False


def x_module_over_threshold__mutmut_orig(path: Path, *, threshold: int) -> bool:
    """True iff any function in ``path`` scores above ``threshold``.

    Pure helper (the detection core) so tests assert on it directly. A syntax /
    decode error is treated as "no violation" — another check owns unparseable
    files.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _score_function(node) > threshold:
            return True
    return False


def x_module_over_threshold__mutmut_1(path: Path, *, threshold: int) -> bool:
    """True iff any function in ``path`` scores above ``threshold``.

    Pure helper (the detection core) so tests assert on it directly. A syntax /
    decode error is treated as "no violation" — another check owns unparseable
    files.
    """
    try:
        tree = None
    except (SyntaxError, UnicodeDecodeError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _score_function(node) > threshold:
            return True
    return False


def x_module_over_threshold__mutmut_2(path: Path, *, threshold: int) -> bool:
    """True iff any function in ``path`` scores above ``threshold``.

    Pure helper (the detection core) so tests assert on it directly. A syntax /
    decode error is treated as "no violation" — another check owns unparseable
    files.
    """
    try:
        tree = ast.parse(None, filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _score_function(node) > threshold:
            return True
    return False


def x_module_over_threshold__mutmut_3(path: Path, *, threshold: int) -> bool:
    """True iff any function in ``path`` scores above ``threshold``.

    Pure helper (the detection core) so tests assert on it directly. A syntax /
    decode error is treated as "no violation" — another check owns unparseable
    files.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=None)
    except (SyntaxError, UnicodeDecodeError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _score_function(node) > threshold:
            return True
    return False


def x_module_over_threshold__mutmut_4(path: Path, *, threshold: int) -> bool:
    """True iff any function in ``path`` scores above ``threshold``.

    Pure helper (the detection core) so tests assert on it directly. A syntax /
    decode error is treated as "no violation" — another check owns unparseable
    files.
    """
    try:
        tree = ast.parse(filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _score_function(node) > threshold:
            return True
    return False


def x_module_over_threshold__mutmut_5(path: Path, *, threshold: int) -> bool:
    """True iff any function in ``path`` scores above ``threshold``.

    Pure helper (the detection core) so tests assert on it directly. A syntax /
    decode error is treated as "no violation" — another check owns unparseable
    files.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), )
    except (SyntaxError, UnicodeDecodeError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _score_function(node) > threshold:
            return True
    return False


def x_module_over_threshold__mutmut_6(path: Path, *, threshold: int) -> bool:
    """True iff any function in ``path`` scores above ``threshold``.

    Pure helper (the detection core) so tests assert on it directly. A syntax /
    decode error is treated as "no violation" — another check owns unparseable
    files.
    """
    try:
        tree = ast.parse(path.read_text(encoding=None), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _score_function(node) > threshold:
            return True
    return False


def x_module_over_threshold__mutmut_7(path: Path, *, threshold: int) -> bool:
    """True iff any function in ``path`` scores above ``threshold``.

    Pure helper (the detection core) so tests assert on it directly. A syntax /
    decode error is treated as "no violation" — another check owns unparseable
    files.
    """
    try:
        tree = ast.parse(path.read_text(encoding="XXutf-8XX"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _score_function(node) > threshold:
            return True
    return False


def x_module_over_threshold__mutmut_8(path: Path, *, threshold: int) -> bool:
    """True iff any function in ``path`` scores above ``threshold``.

    Pure helper (the detection core) so tests assert on it directly. A syntax /
    decode error is treated as "no violation" — another check owns unparseable
    files.
    """
    try:
        tree = ast.parse(path.read_text(encoding="UTF-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _score_function(node) > threshold:
            return True
    return False


def x_module_over_threshold__mutmut_9(path: Path, *, threshold: int) -> bool:
    """True iff any function in ``path`` scores above ``threshold``.

    Pure helper (the detection core) so tests assert on it directly. A syntax /
    decode error is treated as "no violation" — another check owns unparseable
    files.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(None))
    except (SyntaxError, UnicodeDecodeError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _score_function(node) > threshold:
            return True
    return False


def x_module_over_threshold__mutmut_10(path: Path, *, threshold: int) -> bool:
    """True iff any function in ``path`` scores above ``threshold``.

    Pure helper (the detection core) so tests assert on it directly. A syntax /
    decode error is treated as "no violation" — another check owns unparseable
    files.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return True
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _score_function(node) > threshold:
            return True
    return False


def x_module_over_threshold__mutmut_11(path: Path, *, threshold: int) -> bool:
    """True iff any function in ``path`` scores above ``threshold``.

    Pure helper (the detection core) so tests assert on it directly. A syntax /
    decode error is treated as "no violation" — another check owns unparseable
    files.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    for node in ast.walk(None):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _score_function(node) > threshold:
            return True
    return False


def x_module_over_threshold__mutmut_12(path: Path, *, threshold: int) -> bool:
    """True iff any function in ``path`` scores above ``threshold``.

    Pure helper (the detection core) so tests assert on it directly. A syntax /
    decode error is treated as "no violation" — another check owns unparseable
    files.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or _score_function(node) > threshold:
            return True
    return False


def x_module_over_threshold__mutmut_13(path: Path, *, threshold: int) -> bool:
    """True iff any function in ``path`` scores above ``threshold``.

    Pure helper (the detection core) so tests assert on it directly. A syntax /
    decode error is treated as "no violation" — another check owns unparseable
    files.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _score_function(None) > threshold:
            return True
    return False


def x_module_over_threshold__mutmut_14(path: Path, *, threshold: int) -> bool:
    """True iff any function in ``path`` scores above ``threshold``.

    Pure helper (the detection core) so tests assert on it directly. A syntax /
    decode error is treated as "no violation" — another check owns unparseable
    files.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _score_function(node) >= threshold:
            return True
    return False


def x_module_over_threshold__mutmut_15(path: Path, *, threshold: int) -> bool:
    """True iff any function in ``path`` scores above ``threshold``.

    Pure helper (the detection core) so tests assert on it directly. A syntax /
    decode error is treated as "no violation" — another check owns unparseable
    files.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _score_function(node) > threshold:
            return False
    return False


def x_module_over_threshold__mutmut_16(path: Path, *, threshold: int) -> bool:
    """True iff any function in ``path`` scores above ``threshold``.

    Pure helper (the detection core) so tests assert on it directly. A syntax /
    decode error is treated as "no violation" — another check owns unparseable
    files.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _score_function(node) > threshold:
            return True
    return True

mutants_x_module_over_threshold__mutmut['_mutmut_orig'] = x_module_over_threshold__mutmut_orig # type: ignore # mutmut generated
mutants_x_module_over_threshold__mutmut['x_module_over_threshold__mutmut_1'] = x_module_over_threshold__mutmut_1 # type: ignore # mutmut generated
mutants_x_module_over_threshold__mutmut['x_module_over_threshold__mutmut_2'] = x_module_over_threshold__mutmut_2 # type: ignore # mutmut generated
mutants_x_module_over_threshold__mutmut['x_module_over_threshold__mutmut_3'] = x_module_over_threshold__mutmut_3 # type: ignore # mutmut generated
mutants_x_module_over_threshold__mutmut['x_module_over_threshold__mutmut_4'] = x_module_over_threshold__mutmut_4 # type: ignore # mutmut generated
mutants_x_module_over_threshold__mutmut['x_module_over_threshold__mutmut_5'] = x_module_over_threshold__mutmut_5 # type: ignore # mutmut generated
mutants_x_module_over_threshold__mutmut['x_module_over_threshold__mutmut_6'] = x_module_over_threshold__mutmut_6 # type: ignore # mutmut generated
mutants_x_module_over_threshold__mutmut['x_module_over_threshold__mutmut_7'] = x_module_over_threshold__mutmut_7 # type: ignore # mutmut generated
mutants_x_module_over_threshold__mutmut['x_module_over_threshold__mutmut_8'] = x_module_over_threshold__mutmut_8 # type: ignore # mutmut generated
mutants_x_module_over_threshold__mutmut['x_module_over_threshold__mutmut_9'] = x_module_over_threshold__mutmut_9 # type: ignore # mutmut generated
mutants_x_module_over_threshold__mutmut['x_module_over_threshold__mutmut_10'] = x_module_over_threshold__mutmut_10 # type: ignore # mutmut generated
mutants_x_module_over_threshold__mutmut['x_module_over_threshold__mutmut_11'] = x_module_over_threshold__mutmut_11 # type: ignore # mutmut generated
mutants_x_module_over_threshold__mutmut['x_module_over_threshold__mutmut_12'] = x_module_over_threshold__mutmut_12 # type: ignore # mutmut generated
mutants_x_module_over_threshold__mutmut['x_module_over_threshold__mutmut_13'] = x_module_over_threshold__mutmut_13 # type: ignore # mutmut generated
mutants_x_module_over_threshold__mutmut['x_module_over_threshold__mutmut_14'] = x_module_over_threshold__mutmut_14 # type: ignore # mutmut generated
mutants_x_module_over_threshold__mutmut['x_module_over_threshold__mutmut_15'] = x_module_over_threshold__mutmut_15 # type: ignore # mutmut generated
mutants_x_module_over_threshold__mutmut['x_module_over_threshold__mutmut_16'] = x_module_over_threshold__mutmut_16 # type: ignore # mutmut generated
mutants_xǁCognitiveComplexityǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCognitiveComplexityǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore


class CognitiveComplexity(FitnessRule):
    """Flags files holding a function above the cognitive-complexity ceiling (S3776)."""

    name = "cognitive-complexity"
    remediation = REMEDIATION
    extensions = (".py",)

    #: Rule-specific knob — S3776's own ceiling; overridable per consumer.
    threshold: int = DEFAULT_THRESHOLD

    @classmethod
    @_mutmut_mutated(mutants_xǁCognitiveComplexityǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CognitiveComplexity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CognitiveComplexity)  # noqa: S101  # narrowing for mypy
        rule.threshold = int(config.get("threshold", DEFAULT_THRESHOLD))
        return rule

    @classmethod
    def xǁCognitiveComplexityǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CognitiveComplexity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CognitiveComplexity)  # noqa: S101  # narrowing for mypy
        rule.threshold = int(config.get("threshold", DEFAULT_THRESHOLD))
        return rule

    @classmethod
    def xǁCognitiveComplexityǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CognitiveComplexity:
        rule = None
        assert isinstance(rule, CognitiveComplexity)  # noqa: S101  # narrowing for mypy
        rule.threshold = int(config.get("threshold", DEFAULT_THRESHOLD))
        return rule

    @classmethod
    def xǁCognitiveComplexityǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CognitiveComplexity:
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, CognitiveComplexity)  # noqa: S101  # narrowing for mypy
        rule.threshold = int(config.get("threshold", DEFAULT_THRESHOLD))
        return rule

    @classmethod
    def xǁCognitiveComplexityǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CognitiveComplexity:
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, CognitiveComplexity)  # noqa: S101  # narrowing for mypy
        rule.threshold = int(config.get("threshold", DEFAULT_THRESHOLD))
        return rule

    @classmethod
    def xǁCognitiveComplexityǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CognitiveComplexity:
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, CognitiveComplexity)  # noqa: S101  # narrowing for mypy
        rule.threshold = int(config.get("threshold", DEFAULT_THRESHOLD))
        return rule

    @classmethod
    def xǁCognitiveComplexityǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CognitiveComplexity:
        rule = super().from_config(config, )
        assert isinstance(rule, CognitiveComplexity)  # noqa: S101  # narrowing for mypy
        rule.threshold = int(config.get("threshold", DEFAULT_THRESHOLD))
        return rule

    @classmethod
    def xǁCognitiveComplexityǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CognitiveComplexity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CognitiveComplexity)  # noqa: S101  # narrowing for mypy
        rule.threshold = None
        return rule

    @classmethod
    def xǁCognitiveComplexityǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CognitiveComplexity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CognitiveComplexity)  # noqa: S101  # narrowing for mypy
        rule.threshold = int(None)
        return rule

    @classmethod
    def xǁCognitiveComplexityǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CognitiveComplexity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CognitiveComplexity)  # noqa: S101  # narrowing for mypy
        rule.threshold = int(config.get(None, DEFAULT_THRESHOLD))
        return rule

    @classmethod
    def xǁCognitiveComplexityǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CognitiveComplexity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CognitiveComplexity)  # noqa: S101  # narrowing for mypy
        rule.threshold = int(config.get("threshold", None))
        return rule

    @classmethod
    def xǁCognitiveComplexityǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CognitiveComplexity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CognitiveComplexity)  # noqa: S101  # narrowing for mypy
        rule.threshold = int(config.get(DEFAULT_THRESHOLD))
        return rule

    @classmethod
    def xǁCognitiveComplexityǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CognitiveComplexity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CognitiveComplexity)  # noqa: S101  # narrowing for mypy
        rule.threshold = int(config.get("threshold", ))
        return rule

    @classmethod
    def xǁCognitiveComplexityǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CognitiveComplexity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CognitiveComplexity)  # noqa: S101  # narrowing for mypy
        rule.threshold = int(config.get("XXthresholdXX", DEFAULT_THRESHOLD))
        return rule

    @classmethod
    def xǁCognitiveComplexityǁfrom_config__mutmut_13(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CognitiveComplexity:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CognitiveComplexity)  # noqa: S101  # narrowing for mypy
        rule.threshold = int(config.get("THRESHOLD", DEFAULT_THRESHOLD))
        return rule

    @_mutmut_mutated(mutants_xǁCognitiveComplexityǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        return module_over_threshold(path, threshold=self.threshold)

    def xǁCognitiveComplexityǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        return module_over_threshold(path, threshold=self.threshold)

    def xǁCognitiveComplexityǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        return module_over_threshold(None, threshold=self.threshold)

    def xǁCognitiveComplexityǁfile_has_violation__mutmut_2(self, path: Path) -> bool:
        return module_over_threshold(path, threshold=None)

    def xǁCognitiveComplexityǁfile_has_violation__mutmut_3(self, path: Path) -> bool:
        return module_over_threshold(threshold=self.threshold)

    def xǁCognitiveComplexityǁfile_has_violation__mutmut_4(self, path: Path) -> bool:
        return module_over_threshold(path, )

mutants_xǁCognitiveComplexityǁfrom_config__mutmut['_mutmut_orig'] = CognitiveComplexity.xǁCognitiveComplexityǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCognitiveComplexityǁfrom_config__mutmut['xǁCognitiveComplexityǁfrom_config__mutmut_1'] = CognitiveComplexity.xǁCognitiveComplexityǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCognitiveComplexityǁfrom_config__mutmut['xǁCognitiveComplexityǁfrom_config__mutmut_2'] = CognitiveComplexity.xǁCognitiveComplexityǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCognitiveComplexityǁfrom_config__mutmut['xǁCognitiveComplexityǁfrom_config__mutmut_3'] = CognitiveComplexity.xǁCognitiveComplexityǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCognitiveComplexityǁfrom_config__mutmut['xǁCognitiveComplexityǁfrom_config__mutmut_4'] = CognitiveComplexity.xǁCognitiveComplexityǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCognitiveComplexityǁfrom_config__mutmut['xǁCognitiveComplexityǁfrom_config__mutmut_5'] = CognitiveComplexity.xǁCognitiveComplexityǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCognitiveComplexityǁfrom_config__mutmut['xǁCognitiveComplexityǁfrom_config__mutmut_6'] = CognitiveComplexity.xǁCognitiveComplexityǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCognitiveComplexityǁfrom_config__mutmut['xǁCognitiveComplexityǁfrom_config__mutmut_7'] = CognitiveComplexity.xǁCognitiveComplexityǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁCognitiveComplexityǁfrom_config__mutmut['xǁCognitiveComplexityǁfrom_config__mutmut_8'] = CognitiveComplexity.xǁCognitiveComplexityǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁCognitiveComplexityǁfrom_config__mutmut['xǁCognitiveComplexityǁfrom_config__mutmut_9'] = CognitiveComplexity.xǁCognitiveComplexityǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁCognitiveComplexityǁfrom_config__mutmut['xǁCognitiveComplexityǁfrom_config__mutmut_10'] = CognitiveComplexity.xǁCognitiveComplexityǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁCognitiveComplexityǁfrom_config__mutmut['xǁCognitiveComplexityǁfrom_config__mutmut_11'] = CognitiveComplexity.xǁCognitiveComplexityǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁCognitiveComplexityǁfrom_config__mutmut['xǁCognitiveComplexityǁfrom_config__mutmut_12'] = CognitiveComplexity.xǁCognitiveComplexityǁfrom_config__mutmut_12 # type: ignore # mutmut generated
mutants_xǁCognitiveComplexityǁfrom_config__mutmut['xǁCognitiveComplexityǁfrom_config__mutmut_13'] = CognitiveComplexity.xǁCognitiveComplexityǁfrom_config__mutmut_13 # type: ignore # mutmut generated

mutants_xǁCognitiveComplexityǁfile_has_violation__mutmut['_mutmut_orig'] = CognitiveComplexity.xǁCognitiveComplexityǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCognitiveComplexityǁfile_has_violation__mutmut['xǁCognitiveComplexityǁfile_has_violation__mutmut_1'] = CognitiveComplexity.xǁCognitiveComplexityǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCognitiveComplexityǁfile_has_violation__mutmut['xǁCognitiveComplexityǁfile_has_violation__mutmut_2'] = CognitiveComplexity.xǁCognitiveComplexityǁfile_has_violation__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCognitiveComplexityǁfile_has_violation__mutmut['xǁCognitiveComplexityǁfile_has_violation__mutmut_3'] = CognitiveComplexity.xǁCognitiveComplexityǁfile_has_violation__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCognitiveComplexityǁfile_has_violation__mutmut['xǁCognitiveComplexityǁfile_has_violation__mutmut_4'] = CognitiveComplexity.xǁCognitiveComplexityǁfile_has_violation__mutmut_4 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(config: Mapping[str, Any], *, repo_root: Path | None = None) -> CognitiveComplexity:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CognitiveComplexity.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(config: Mapping[str, Any], *, repo_root: Path | None = None) -> CognitiveComplexity:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CognitiveComplexity.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(config: Mapping[str, Any], *, repo_root: Path | None = None) -> CognitiveComplexity:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CognitiveComplexity.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(config: Mapping[str, Any], *, repo_root: Path | None = None) -> CognitiveComplexity:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CognitiveComplexity.from_config(config, repo_root=None)


def x_build__mutmut_3(config: Mapping[str, Any], *, repo_root: Path | None = None) -> CognitiveComplexity:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CognitiveComplexity.from_config(repo_root=repo_root)


def x_build__mutmut_4(config: Mapping[str, Any], *, repo_root: Path | None = None) -> CognitiveComplexity:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CognitiveComplexity.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(CognitiveComplexity, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(CognitiveComplexity, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(CognitiveComplexity, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(CognitiveComplexity, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
