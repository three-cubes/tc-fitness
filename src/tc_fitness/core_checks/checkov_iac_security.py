"""CORE check: checkov_iac_security — IaC-security scan that gates NET-NEW
Checkov misconfigurations in an Infrastructure-as-Code tree.

A consumer that ships cloud IaC (Bicep, Terraform, CloudFormation, …) wraps
Checkov (Apache-2.0, ``pip``-installable) over its IaC directory, parses the
failed checks, and FAILs the build ONLY on findings not already recorded in a
shrink-only baseline. Pre-existing findings are grandfathered there so the gate
never breaks the build on debt it did not introduce — it blocks a NEW
misconfiguration reaching the trunk.

Key-based, not per-file
-----------------------
A Checkov finding's identity is ``<check_id>|<file_path>|<resource>`` — a
line-independent KEY, and one file can carry several findings. That does not fit
the per-file :class:`tc_fitness.fitness_rule.FitnessRule` baseline (whose unit is
an offending file), so this CORE check is a bespoke key-baselined gate — the
same shape the engine's own ``branch_naming`` takes when the per-file model
does not apply. It reads/writes ``.architecture/baseline/<name>-findings.txt``
via the canonical baseline parse contract (:func:`tc_fitness.parse_baseline_text`).

Optional tool, soft-skip
------------------------
Checkov is the only heavy dependency, and it is CONSUMER-provided: when the
``checkov`` binary is absent the gate soft-skips (exit 0) rather than hard-fail,
mirroring how a shell detector degrades when ``shellcheck`` is not installed.
The engine adds NO runtime dependency — a consumer pins Checkov into its own
tool environment so ``tc-fitness run`` has the binary. The scan itself runs as a
subprocess of the trusted binary over the consumer-configured scan directory.

Injectable runner
-----------------
The Checkov invocation is a dependency-injected ``runner`` seam, so a test drives
the diff logic with canned Checkov JSON (no binary, no network) instead of
patching module internals.

Config (``[tool.tc_fitness.core_checks.checkov_iac_security]``):

* ``scan_dir`` — repo-relative IaC directory to scan (default ``"."``).
* ``framework`` — Checkov framework flag (default ``"bicep"``).
* ``name`` — baseline-name root → ``.architecture/baseline/<name>-findings.txt``.
* ``timeout`` — subprocess wall-clock ceiling in seconds (default ``180``).

Ported from tc-agent-zone ``scripts/checks/checkov_iac_security.py`` (SGO-297)
and re-expressed repo-agnostic: no scan path, framework, or baseline name is
baked in — every one arrives from the consumer's config.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any

from tc_fitness.baseline import baseline_dir, parse_baseline_text, render_baseline
from tc_fitness.lib import REPO_ROOT
from tc_fitness.lib import remediation as _remediation

#: Repo-NEUTRAL defaults — a consumer narrows these via config.
DEFAULT_SCAN_DIR = "."
DEFAULT_FRAMEWORK = "bicep"
DEFAULT_NAME = "checkov-iac-security"
DEFAULT_TIMEOUT = 180

#: Baseline suffix for the key-based grandfather list (distinct from the
#: per-file ``-files.txt`` a :class:`FitnessRule` uses).
BASELINE_SUFFIX = "-findings.txt"

#: Checkov summary key for the count of files its parser skipped. Hoisted to a
#: single site so the coupling between the report shape and the readers is
#: explicit.
_PARSING_ERRORS_KEY = "parsing_errors"

# A runner takes the (resolved) scan dir and returns Checkov's parsed JSON, or
# None when Checkov is unavailable. Injected in tests to avoid patching internals.
Runner = Callable[[Path], "dict[str, Any] | list[Any] | None"]

REMEDIATION = _remediation(
    fix=(
        "remediate each net-new misconfiguration above (the per-line trailer names "
        "the policy + fix), OR — if the risk is accepted — append the finding key to "
        "the checkov findings baseline with a justification."
    ),
    nxt="re-run this check to confirm no net-new findings remain.",
    run="python -m tc_fitness.core_checks.checkov_iac_security",
    passing="every IaC resource passes its Checkov policy, or an accepted risk is baselined with a reason",
    forbidden="a new resource ships a Checkov policy violation with no remediation and no baseline entry",
)


def checkov_binary() -> str | None:
    """Absolute path to the ``checkov`` executable, or ``None`` when not installed."""
    return shutil.which("checkov")


def run_checkov(
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    checkov_bin: str | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> dict[str, Any] | list[Any] | None:
    """Run Checkov over ``scan_dir`` and return its parsed JSON.

    Returns ``None`` when the Checkov binary is not installed (soft-skip). The
    binary is a fixed, trusted argv0 and the scan dir is a config-declared path
    resolved under the repo root — no shell, no attacker-controlled input.
    """
    binary = checkov_bin or checkov_binary()
    if binary is None:
        return None
    proc = subprocess.run(
        [binary, "-d", str(scan_dir), "--framework", framework, "--output", "json", "--quiet", "--compact"],
        capture_output=True,
        text=True,
        check=False,
        timeout=timeout,
    )
    payload = proc.stdout.strip()
    if not payload:
        # No parsable output (e.g. nothing to scan) — treat as an empty report.
        return {"results": {"failed_checks": []}, "summary": {_PARSING_ERRORS_KEY: 0}}
    parsed: dict[str, Any] | list[Any] = json.loads(payload)
    return parsed


def _reports(data: dict[str, Any] | list[Any]) -> list[dict[str, Any]]:
    """Checkov emits a single report dict, or a list of them (multi-framework)."""
    return data if isinstance(data, list) else [data]


def parse_failed(data: dict[str, Any] | list[Any]) -> list[dict[str, Any]]:
    """Flatten every ``failed_checks`` entry across one-or-many Checkov reports."""
    out: list[dict[str, Any]] = []
    for report in _reports(data):
        results = report.get("results") or {}
        out.extend(results.get("failed_checks") or [])
    return out


def parsing_error_count(data: dict[str, Any] | list[Any]) -> int:
    """Total Checkov parse failures — surfaced (not gated) so silent skips show."""
    total = 0
    for report in _reports(data):
        errors = (report.get("summary") or {}).get(_PARSING_ERRORS_KEY, 0)
        total += errors if isinstance(errors, int) else len(errors)
    return total


def finding_key(failed_check: dict[str, Any]) -> str:
    """Line-independent identity for a failed check: ``check_id|file_path|resource``."""
    return f"{failed_check.get('check_id')}|{failed_check.get('file_path')}|{failed_check.get('resource')}"


def net_new_findings(failed: list[dict[str, Any]], baseline: set[str]) -> list[dict[str, Any]]:
    """Failed checks whose key is not already grandfathered in the baseline."""
    return [fc for fc in failed if finding_key(fc) not in baseline]


def _format_finding(failed_check: dict[str, Any], *, scan_dir: str) -> str:
    """One agent-actionable line per net-new finding (fix:/next:/run:)."""
    key = finding_key(failed_check)
    line_range = failed_check.get("file_line_range") or []
    location = failed_check.get("file_path", "<unknown>")
    if len(line_range) >= 2:
        location = f"{location}:{line_range[0]}-{line_range[1]}"
    guide = failed_check.get("guideline") or f"Checkov policy {failed_check.get('check_id')}"
    return (
        f"  - [{failed_check.get('check_id')}] {failed_check.get('check_name', '')} — "
        f"resource {failed_check.get('resource')} at {location}. "
        f"fix: remediate the resource per {guide}, OR — if the risk is accepted — append "
        f"'{key}' to the checkov findings baseline with a justification; "
        f"next: re-run this check to confirm clean; "
        f"run: checkov -d {scan_dir} --framework {failed_check.get('framework', DEFAULT_FRAMEWORK)} "
        f"--check {failed_check.get('check_id')}"
    )


class CheckovIacSecurity:
    """Key-baselined IaC-security gate over a Checkov scan (not a per-file rule)."""

    #: Canonical check name — mirrors the ``FitnessRule.name`` role so the
    #: registry/discovery can reason about this module uniformly.
    name = DEFAULT_NAME

    def __init__(
        self,
        repo_root: Path | None = None,
        *,
        scan_dir: str = DEFAULT_SCAN_DIR,
        framework: str = DEFAULT_FRAMEWORK,
        name: str = DEFAULT_NAME,
        timeout: int = DEFAULT_TIMEOUT,
        runner: Runner | None = None,
    ) -> None:
        raw_root = repo_root if repo_root is not None else REPO_ROOT
        self._repo_root: Path = raw_root.resolve()
        self._scan_dir = scan_dir
        self._framework = framework
        self._name = name
        self._timeout = timeout
        # DI seam: a test injects canned Checkov JSON; None => the real binary.
        self._runner = runner

    @classmethod
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CheckovIacSecurity:
        """Build an instance from a consumer's ``[tool.tc_fitness]`` config dict."""
        return cls(
            repo_root=repo_root,
            scan_dir=str(config.get("scan_dir", DEFAULT_SCAN_DIR)),
            framework=str(config.get("framework", DEFAULT_FRAMEWORK)),
            name=str(config.get("name", DEFAULT_NAME)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @property
    def scan_path(self) -> Path:
        """The resolved absolute scan directory under the repo root."""
        return (self._repo_root / self._scan_dir).resolve()

    @property
    def baseline_path(self) -> Path:
        """The key-based baseline file for this check."""
        return baseline_dir(self._repo_root) / f"{self._name}{BASELINE_SUFFIX}"

    def _active_runner(self) -> Runner:
        if self._runner is not None:
            return self._runner
        return lambda sd: run_checkov(sd, framework=self._framework, timeout=self._timeout)

    def _load_baseline(self) -> set[str]:
        path = self.baseline_path
        if not path.exists():
            return set()
        return parse_baseline_text(path.read_text(encoding="utf-8"))

    def evaluate(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run the scan and diff against the baseline.

        Pure orchestration around the injected runner: canned JSON in tests,
        the real binary in production. When the runner returns ``None`` (Checkov
        absent) the gate soft-skips.
        """
        data = self._active_runner()(self.scan_path)
        if data is None:
            return (
                True,
                [],
                {"skipped": True, "failed": 0, "baselined": 0, "net_new": 0, _PARSING_ERRORS_KEY: 0},
            )
        failed = parse_failed(data)
        baseline = self._load_baseline()
        net_new = net_new_findings(failed, baseline)
        errors = [_format_finding(fc, scan_dir=self._scan_dir) for fc in net_new]
        meta = {
            "skipped": False,
            "failed": len(failed),
            "baselined": len(baseline),
            "net_new": len(net_new),
            _PARSING_ERRORS_KEY: parsing_error_count(data),
        }
        return (not net_new), errors, meta

    def run(self) -> int:
        """Print a PASS/FAIL verdict and return the process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["skipped"]:
            print(
                "PASS checkov_iac_security (checkov not installed — soft-skip). "
                "fix: install checkov into the tool environment to enable the scan; "
                "next: re-run this check; "
                "run: checkov --version"
            )
            return 0
        if meta[_PARSING_ERRORS_KEY]:
            print(
                f"NOTE checkov_iac_security: {meta[_PARSING_ERRORS_KEY]} "
                "IaC file(s) Checkov could not parse (not gated)."
            )
        if passed:
            print(
                f"PASS checkov_iac_security ({meta['failed']} finding(s), "
                f"all {meta['baselined']} baselined; 0 net-new)"
            )
            return 0
        print(f"FAIL checkov_iac_security ({meta['net_new']} net-new finding(s)):")
        for line in errors:
            print(line)
        print()
        print(REMEDIATION)
        return 1

    def establish_baseline(self) -> Path:
        """Freeze today's findings as the frozen key baseline; return the path."""
        data = self._active_runner()(self.scan_path)
        keys = sorted({finding_key(fc) for fc in parse_failed(data)}) if data is not None else []
        path = self.baseline_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_baseline(self._name, keys), encoding="utf-8")
        return path


def build(config: Mapping[str, Any], *, repo_root: Path | None = None) -> CheckovIacSecurity:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CheckovIacSecurity.from_config(config, repo_root=repo_root)


def main(argv: list[str] | None = None) -> int:
    """CLI entry — supports ``--establish-baseline`` and ``--repo-root``.

    A bespoke entrypoint (this check is not a :class:`FitnessRule`, so it does
    not reuse ``run_core_check``); the two universal flags behave identically.
    """
    parser = argparse.ArgumentParser(prog=CheckovIacSecurity.name)
    parser.add_argument(
        "--establish-baseline",
        action="store_true",
        help="freeze today's findings as the baseline (rule adoption mode).",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="repo root to scan (default: current working directory).",
    )
    args = parser.parse_args(argv)

    rule = CheckovIacSecurity.from_config({}, repo_root=args.repo_root)
    if args.establish_baseline:
        path = rule.establish_baseline()
        print(f"established baseline: {path}")
        return 0
    return rule.run()


if __name__ == "__main__":
    import sys

    sys.exit(main())
