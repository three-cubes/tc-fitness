"""Fail the protected CI result unless every required worker succeeded."""

from __future__ import annotations

import json
import os
import sys
from typing import Any


def _worker_results(value: object) -> dict[str, str] | None:
    if not isinstance(value, dict) or not value:
        return None
    results: dict[str, str] = {}
    for worker, details in value.items():
        if not isinstance(worker, str):
            return None
        if not isinstance(details, dict):
            return None
        result = details.get("result")
        if not isinstance(result, str):
            return None
        results[worker] = result
    return results


def main() -> int:
    raw = os.environ.get("NEEDS_JSON")
    if raw is None:
        print("Quality gate cannot evaluate workers: NEEDS_JSON is missing", file=sys.stderr)
        return 1
    try:
        needs: Any = json.loads(raw)
    except json.JSONDecodeError:
        print("Quality gate cannot evaluate workers: NEEDS_JSON is invalid JSON", file=sys.stderr)
        return 1

    results = _worker_results(needs)
    if results is None:
        print(
            "Quality gate cannot evaluate workers: no worker results were supplied or a result is invalid",
            file=sys.stderr,
        )
        return 1
    failed = [f"{worker}={result}" for worker, result in results.items() if result != "success"]
    if failed:
        print(f"Quality gate blocked by worker results: {', '.join(failed)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
