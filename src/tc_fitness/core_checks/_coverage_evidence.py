"""Shared Cobertura path resolution for coverage assurance.

Coverage producers may emit repository-relative source roots, absolute source
roots, or several roots. Assurance resolves every class filename back to one
repository-relative file and rejects ambiguous or out-of-repository evidence.
"""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path


def _relative_to_repository(candidate: Path, repo_root: Path) -> str:
    try:
        return candidate.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError as exc:
        raise ValueError(f"coverage path is outside the repository: {candidate}") from exc


def resolve_coverage_filename(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


__all__ = ["resolve_coverage_filename"]


def reject_external_report(report: str, repo_root: Path) -> None:
    """Refuse a coverage report configured outside the repository.

    A missing report is reported as a violation keyed on the report path, and
    the gate relativises every violation to the repository root. An absolute
    path outside it cannot be relativised, so the check would crash with a
    ValueError instead of emitting the fail-closed missing-evidence verdict it
    exists to give. Refusing the configuration keeps the failure at the point
    someone can act on it.
    """
    path = Path(report)
    if not path.is_absolute():
        return
    if not path.resolve().is_relative_to(repo_root.resolve()):
        raise ValueError(
            f"coverage_report must name a path inside the repository; {report} is outside {repo_root}"
        )
