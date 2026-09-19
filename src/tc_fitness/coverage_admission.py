"""Exact-source coverage evidence shared by the existing CORE admission checks.

Strict measurement requires Coverage.py (available in the development extra).
It uses Coverage.py's executable-statement analysis, not an approximate Python
interpreter or report-line intersection that could omit executable source.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import math
import os
import re
import subprocess
import sys
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from tc_fitness.core_checks._coverage_evidence import resolve_coverage_filename
from tc_fitness.core_checks.coverage_floor import parse_coverage_details

SCHEMA = "tc.fitness/coverage-receipt/v1"


def digest(value: object) -> str:
    """Canonical, finite JSON content digest; not a signature or trust anchor."""
    return bytes_digest(json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode())


def bytes_digest(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def configured(value: object) -> str:
    """Read an explicit literal or environment binding; absence is an error."""
    if isinstance(value, str) and value.startswith("env:"):
        value = os.environ.get(value[4:])
    if not isinstance(value, str) or not value:
        raise ValueError("coverage requires a non-empty execution input")
    return value


def trusted_digest(root: Path, value: object) -> str:
    """Resolve an independent digest handoff, never a receipt's own field."""
    token = configured(value)
    if token.startswith("file:"):
        path = Path(configured(token[5:]))
        if not path.is_absolute() or path.is_symlink() or path.resolve().is_relative_to(root.resolve()):
            raise ValueError("coverage digest handoff must be a regular file outside the candidate checkout")
        token = path.read_text().strip()
    if re.fullmatch(r"sha256:[0-9a-f]{64}", token) is None:
        raise ValueError("coverage requires an independently supplied SHA-256 digest")
    return token


def identity(value: object) -> str:
    """Resolve an explicitly named environment input, never a moving Git ref."""
    value = configured(value)
    if re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", value) is None:
        raise ValueError("coverage identity requires an immutable full Git commit")
    return value


def git(root: Path, *args: str) -> str:
    """Use the check's fixed-argv Git boundary and fail on unavailable history."""
    return git_bytes(root, *args).decode("utf-8", "surrogateescape").strip("\n")


def git_bytes(root: Path, *args: str) -> bytes:
    from tc_fitness.core_checks.new_code_coverage import _default_git_runner

    result = _default_git_runner(list(args), root)
    if result.returncode:
        raise ValueError("coverage Git evidence unavailable: " + " ".join(args[:2]))
    return result.stdout


def exact_checkout(root: Path, base: str, candidate: str) -> None:
    """Bind the full tracked checkout to HEAD and the declared exact ancestor."""
    base, candidate = identity(base), identity(candidate)
    if git(root, "rev-parse", "--verify", "HEAD^{commit}") != candidate:
        raise ValueError("coverage candidate does not match HEAD")
    if git(root, "rev-parse", "--verify", base + "^{commit}") != base:
        raise ValueError("coverage exact base is not a commit")
    git(root, "merge-base", "--is-ancestor", base, candidate)
    git(root, "diff", "--quiet", "--no-ext-diff", "HEAD", "--")
    if git(root, "ls-files", "--others", "--exclude-standard", "-z", "--"):
        raise ValueError("coverage candidate contains uncommitted files")


def source_files(root: Path, roots: list[str]) -> dict[str, Path]:
    """Enumerate the complete Python scope, including untracked source."""
    files: dict[str, Path] = {}
    if not roots:
        raise ValueError("coverage requires non-empty source roots")
    for name in roots:
        path = root / name
        if Path(name).is_absolute() or ".." in Path(name).parts or not path.is_dir():
            raise ValueError("coverage requires existing repository-relative roots")
        for source in path.rglob("*.py"):
            if source.is_symlink() or not source.resolve().is_relative_to(root.resolve()):
                raise ValueError("coverage source cannot escape through symlinks")
            if source.is_file():
                files[source.relative_to(root).as_posix()] = source
    if not files:
        raise ValueError("coverage scope contains no Python source")
    tracked = set(git(root, "ls-files", "-z", "--", *roots).split("\0"))
    if set(files) - tracked:
        raise ValueError("coverage source contains uncommitted files")
    # Git's stat cache and assume-unchanged/skip-worktree flags are not proof
    # that the measured bytes are the committed candidate.
    for name, path in files.items():
        if path.read_bytes() != git_bytes(root, "show", "HEAD:" + name):
            raise ValueError("coverage source bytes differ from the candidate")
    return files


def complete_line_hits(root: Path, report: Path, files: dict[str, Path]) -> dict[str, dict[int, int]]:
    """Validate all detail against the actual Coverage.py statement inventory."""
    from tc_fitness.core_checks.new_code_coverage import _resolve_element_tree

    details = parse_coverage_details(report, repo_root=root)
    if set(details) != set(files):
        raise ValueError("coverage report does not measure the complete source set")
    parsed = _resolve_element_tree().parse(report).getroot()
    sources = [element.text for element in parsed.iter("source") if element.text]
    analyzer = importlib.import_module("coverage").Coverage(config_file=False, data_file=None)
    analyzer.set_option("report:exclude_lines", [])
    analyzer.set_option("report:partial_branches", [])
    result: dict[str, dict[int, int]] = {}
    for element in parsed.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        hits = {int(line.get("number")): int(line.get("hits")) for line in element.find("lines")}
        statements = set(analyzer.analysis2(str(files[relative]))[1])
        if set(hits) != statements:
            raise ValueError("coverage report omits or invents executable source lines: " + relative)
        result[relative] = hits
    return result


def changed_line_failures(root: Path, config: dict[str, Any]) -> dict[str, str]:
    """Score every exact-base changed executable line at a hard 100 percent."""
    from tc_fitness.core_checks.new_code_coverage import parse_added_lines

    if (
        config.get("floor_pct") != 100
        or config.get("exempt_files")
        or config.get("extensions", [".py"]) != [".py"]
    ):
        raise ValueError("exact-base coverage requires 100 percent Python coverage without exemptions")
    base, candidate = identity(config.get("exact_base_commit")), identity(config.get("candidate_commit"))
    exact_checkout(root, base, candidate)
    files = source_files(root, config.get("roots", []))
    hits = complete_line_hits(root, root / configured(config.get("coverage_report", "coverage.xml")), files)
    failures: dict[str, str] = receipt_failures(root, config) if "coverage_receipt" in config else {}
    for relative in files:
        diff = git(
            root,
            "diff",
            "--no-ext-diff",
            "--no-textconv",
            "--no-renames",
            "--unified=0",
            base,
            candidate,
            "--",
            relative,
        )
        changed = set().union(*parse_added_lines(diff).values())
        missing = sorted(line for line in changed if line in hits[relative] and hits[relative][line] == 0)
        if missing:
            failures[relative] = "uncovered changed executable lines: " + ", ".join(map(str, missing))
    return failures


def measure(root: Path, report: Path, files: dict[str, Path]) -> dict[str, Any]:
    """Retain exact per-file and package counts after complete-source validation."""
    complete_line_hits(root, report, files)
    counts = parse_coverage_details(report, repo_root=root)
    per_file = {name: asdict(value) for name, value in sorted(counts.items())}
    return {
        "files": per_file,
        "counts": {
            key: sum(value[key] for value in per_file.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        },
    }


def read_receipt(path: Path, expected_digest: str) -> dict[str, Any]:
    """Check integrity against an independently supplied trusted digest."""
    payload = json.loads(path.read_text())
    if not isinstance(payload, dict) or payload.get("schema") != SCHEMA:
        raise ValueError("invalid coverage receipt schema")
    actual = payload.pop("digest", None)
    if actual != expected_digest or actual != digest(payload):
        raise ValueError("coverage receipt digest mismatch")
    for name, expected in payload["reports"].items():
        if (
            name not in {"coverage.xml", "coverage.json"}
            or bytes_digest((path.parent / name).read_bytes()) != expected
        ):
            raise ValueError("coverage report digest mismatch")
    if set(payload["reports"]) != {"coverage.xml", "coverage.json"}:
        raise ValueError("coverage receipt requires both producer reports")
    counts = payload["counts"]
    if set(counts) != {"lines", "covered_lines", "branches", "covered_branches"} or any(
        type(value) is not int or value < 0 for value in counts.values()
    ):
        raise ValueError("coverage receipt requires exact non-negative counts")
    if (
        not counts["lines"]
        or counts["covered_lines"] > counts["lines"]
        or counts["covered_branches"] > counts["branches"]
    ):
        raise ValueError("invalid coverage receipt opportunity counts")
    return payload


def receipt_failures(root: Path, config: dict[str, Any]) -> dict[str, str]:
    """Validate current execution, exact accepted base and monotonic counts.

    Digest anchors MUST come from the trusted producer/admission handoff, not
    be copied from the files being checked. Selecting the latest accepted
    digest is the caller's storage/CI responsibility; no receipt accepts itself.
    """
    base, candidate = identity(config.get("exact_base_commit")), identity(config.get("candidate_commit"))
    exact_checkout(root, base, candidate)
    roots = config.get("roots", [])
    files = source_files(root, roots)
    current_path = root / configured(config.get("coverage_receipt"))
    accepted_path = root / configured(config.get("accepted_coverage_receipt"))
    current = read_receipt(current_path, trusted_digest(root, config.get("coverage_receipt_digest")))
    accepted = read_receipt(accepted_path, trusted_digest(root, config.get("accepted_coverage_digest")))
    if (
        current["base_commit"] != base
        or current["candidate_commit"] != candidate
        or accepted["candidate_commit"] != base
    ):
        raise ValueError("coverage receipt does not bind the exact base and candidate")
    if current["roots"] != sorted(roots) or accepted["roots"] != sorted(roots):
        raise ValueError("coverage receipt changes the measured source scope")
    config_name = configured(config.get("coverage_config"))
    if Path(config_name).is_absolute() or ".." in Path(config_name).parts:
        raise ValueError("coverage configuration must be repository-relative")
    for receipt, commit in ((current, candidate), (accepted, base)):
        if receipt["config_path"] != config_name or receipt["config_digest"] != bytes_digest(
            git_bytes(root, "show", commit + ":" + config_name)
        ):
            raise ValueError("coverage receipt configuration identity mismatch")
        names = [
            name
            for name in git(root, "ls-tree", "-r", "--name-only", "-z", commit, "--", *roots).split("\0")
            if name.endswith(".py")
        ]
        source_hash = digest(
            {name: bytes_digest(git_bytes(root, "show", commit + ":" + name)) for name in sorted(names)}
        )
        if receipt["source_digest"] != source_hash:
            raise ValueError("coverage receipt source identity mismatch")
    execution = current["execution"]
    if any(execution[key] != configured(config.get(key)) for key in ("run_id", "attempt_id")):
        raise ValueError("coverage receipt belongs to a stale run or attempt")
    started, finished = (datetime.fromisoformat(execution[key]) for key in ("started_at", "finished_at"))
    now = datetime.now(UTC)
    age = config.get("max_age_seconds", 3600)
    if isinstance(age, bool) or not isinstance(age, int | float) or not math.isfinite(age) or age <= 0:
        raise ValueError("coverage freshness requires a finite positive age limit")
    if (
        started.tzinfo is None
        or finished.tzinfo is None
        or not started <= finished <= now
        or (now - started).total_seconds() > age
    ):
        raise ValueError("coverage receipt is expired, future-dated or invalid")
    report = root / configured(config.get("coverage_report", "coverage.xml"))
    if report.resolve() != (current_path.parent / "coverage.xml").resolve():
        raise ValueError("coverage admission report is not the bound producer report")
    measured = measure(root, report, files)
    if any(measured[key] != current[key] for key in ("files", "counts")):
        raise ValueError("coverage receipt counts disagree with actual source detail")
    messages = []
    for kind in ("lines", "branches"):
        before, after = accepted["counts"], current["counts"]
        before_total, after_total = before[kind], after[kind]
        # Zero opportunities are fully covered, not an undefined percentage.
        before_hit = before["covered_" + kind] if before_total else 1
        after_hit = after["covered_" + kind] if after_total else 1
        if after_hit * (before_total or 1) < before_hit * (after_total or 1):
            messages.append(
                f"{'line' if kind == 'lines' else 'branch'} coverage decreased from accepted exact base"
            )
    return {".": "; ".join(messages)} if messages else {}


def produce_coverage(
    *,
    root: Path,
    base: str,
    candidate: str,
    roots: list[str],
    config: str,
    run_id: str,
    attempt_id: str,
    output: Path,
    command: list[str],
    digest_output: Path | None = None,
) -> dict[str, Any]:
    """Run Coverage.py from empty data and retain a new digest-bound measurement.

    The caller owns command selection and the independent digest handoff. This
    producer never marks its own receipt accepted and never replaces evidence.
    """
    root, output = root.resolve(), output.resolve()
    base, candidate = identity(base), identity(candidate)
    run_id, attempt_id = configured(run_id), configured(attempt_id)
    exact_checkout(root, base, candidate)
    files = source_files(root, roots)
    config_path = root / config
    if Path(config).is_absolute() or ".." in Path(config).parts:
        raise ValueError("coverage configuration must be a tracked repository file")
    config_hash = bytes_digest(config_path.read_bytes())
    if bytes_digest(git_bytes(root, "show", candidate + ":" + config)) != config_hash:
        raise ValueError("coverage configuration differs from the candidate")
    source_hash = digest({name: bytes_digest(path.read_bytes()) for name, path in sorted(files.items())})
    if not command:
        raise ValueError("coverage producer requires a Python test command")
    if digest_output is not None and (
        not digest_output.is_absolute()
        or digest_output.resolve().is_relative_to(root)
        or digest_output.exists()
    ):
        raise ValueError("coverage digest output must be a new external handoff file")
    output.mkdir(parents=True, exist_ok=False)
    settings = output / "coverage.ini"
    settings.write_text(
        "[run]\nbranch = true\nsource =\n"
        + "".join(f"    {root / name}\n" for name in roots)
        + f"data_file = {output / 'coverage.data'}\n[report]\nexclude_lines =\npartial_branches =\n"
    )
    started = datetime.now(UTC).isoformat()
    for args in (
        ("run", *command),
        ("xml", "-o", str(output / "coverage.xml")),
        ("json", "-o", str(output / "coverage.json")),
    ):
        # The producer deliberately executes caller-selected Python tests with
        # a fixed interpreter and argv, never a shell or executable from PATH.
        result = subprocess.run(  # noqa: S603 - fixed interpreter, explicit producer command, no shell
            [sys.executable, "-m", "coverage", args[0], "--rcfile", str(settings), *args[1:]],
            cwd=root,
            check=False,
            timeout=600,
        )
        if result.returncode:
            raise ValueError("coverage producer command failed; no receipt emitted")
    exact_checkout(root, base, candidate)
    if source_hash != digest(
        {name: bytes_digest(path.read_bytes()) for name, path in sorted(source_files(root, roots).items())}
    ) or config_hash != bytes_digest(config_path.read_bytes()):
        raise ValueError("coverage source or configuration changed during execution")
    payload: dict[str, Any] = {
        "schema": SCHEMA,
        "base_commit": base,
        "candidate_commit": candidate,
        "roots": sorted(roots),
        "source_digest": source_hash,
        "config_path": config,
        "config_digest": config_hash,
        "reports": {
            name: bytes_digest((output / name).read_bytes()) for name in ("coverage.xml", "coverage.json")
        },
        "execution": {
            "run_id": run_id,
            "attempt_id": attempt_id,
            "started_at": started,
            "finished_at": datetime.now(UTC).isoformat(),
            "command": command,
            "coverage_version": importlib.import_module("coverage").__version__,
            "python_version": sys.version,
        },
        **measure(root, output / "coverage.xml", files),
    }
    payload["digest"] = digest(payload)
    (output / "receipt.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    if digest_output is not None:
        with digest_output.open("x") as stream:
            stream.write(payload["digest"] + "\n")
    return payload


def main(argv: list[str] | None = None) -> int:
    """Public evidence producer; admission remains in the existing CORE checks."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["produce"])
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--base-commit", required=True)
    parser.add_argument("--candidate-commit", required=True)
    parser.add_argument("--source", action="append", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--attempt-id", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--digest-output")
    tokens = sys.argv[1:] if argv is None else argv
    split = tokens.index("--") if "--" in tokens else len(tokens)
    args = parser.parse_args(tokens[:split])
    command = tokens[split + 1 :]
    payload = produce_coverage(
        root=args.repo_root,
        base=args.base_commit,
        candidate=args.candidate_commit,
        roots=args.source,
        config=args.config,
        run_id=args.run_id,
        attempt_id=args.attempt_id,
        output=Path(configured(args.output)),
        command=command,
        digest_output=Path(configured(args.digest_output)) if args.digest_output else None,
    )
    print(payload["digest"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
