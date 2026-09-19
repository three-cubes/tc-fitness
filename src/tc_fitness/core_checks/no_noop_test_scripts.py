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


def _skip_options(command: list[str], position: int) -> int:
    """Skip wrapper flags before its executable, including value-taking flags."""
    takes_value = {"--package", "-p", "--filter", "--dir", "--workspace-root", "--config", "--registry"}
    while position < len(command) and command[position].startswith("-"):
        if command[position] == "--":
            return position + 1
        position += 2 if command[position] in takes_value else 1
    return position


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

    def _is_prod_manifest(self, rel: str) -> bool:
        """The root manifest, or any manifest under a production prefix, is in scope."""
        if rel == _MANIFEST_NAME:
            return True
        return any(rel.startswith(prefix) for prefix in self.prod_package_prefixes)

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

    def is_in_scope(self, rel: str) -> bool:
        # Enumeration already restricts to in-scope manifests; the gate's scope
        # predicate just needs to accept what enumeration yields.
        return rel.endswith(_MANIFEST_NAME) and self._is_prod_manifest(rel)

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


def build(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoNoopTestScripts:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoNoopTestScripts.from_config(config, repo_root=repo_root)


def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoNoopTestScripts, argv)


if __name__ == "__main__":
    import sys

    sys.exit(main())
