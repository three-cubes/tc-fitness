"""Tests for the integrity_state_predicate CORE check."""

from __future__ import annotations

from pathlib import Path

from tc_fitness.core_checks.integrity_state_predicate import build, file_missing_state_predicate

_STATE = {"content_vectors": ("model", "embedded_at")}

# Presence-only completeness check — the chunk-0 bug shape (no model predicate).
_BAD = (
    "def check(db):\n"
    "    return db.execute(\n"
    '        "SELECT d.path FROM documents d "\n'
    '        "LEFT JOIN content_vectors v ON v.hash = d.hash "\n'
    '        "WHERE d.active = 1 AND v.hash IS NULL"\n'
    "    ).fetchall()\n"
)

# Strengthened — joins on the state predicate (the fix).
_OK = (
    "def check(db):\n"
    "    return db.execute(\n"
    '        "SELECT d.path FROM documents d "\n'
    '        "LEFT JOIN content_vectors v ON v.hash = d.hash AND v.model IS NOT NULL "\n'
    '        "WHERE d.active = 1 AND v.hash IS NULL"\n'
    "    ).fetchall()\n"
)

# Orphan check on a NON-state table (documents) — must NOT be flagged.
_ORPHAN = (
    "def check(db):\n"
    "    return db.execute(\n"
    '        "SELECT v.hash FROM content_vectors v "\n'
    '        "LEFT JOIN documents d ON d.hash = v.hash WHERE d.hash IS NULL"\n'
    "    ).fetchall()\n"
)


def _seed(tmp_path: Path, rel: str, body: str) -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


def test_detection_flags_presence_only_check(tmp_path: Path) -> None:
    p = _seed(tmp_path, "integrity.py", _BAD)
    assert file_missing_state_predicate(p, state_tables=_STATE) is True


def test_detection_passes_with_state_predicate(tmp_path: Path) -> None:
    p = _seed(tmp_path, "integrity.py", _OK)
    assert file_missing_state_predicate(p, state_tables=_STATE) is False


def test_orphan_check_on_non_state_table_is_clean(tmp_path: Path) -> None:
    """LEFT JOIN documents (not a configured state table) must not fire."""
    p = _seed(tmp_path, "integrity.py", _ORPHAN)
    assert file_missing_state_predicate(p, state_tables=_STATE) is False


def test_empty_state_tables_flags_nothing(tmp_path: Path) -> None:
    p = _seed(tmp_path, "integrity.py", _BAD)
    assert file_missing_state_predicate(p, state_tables={}) is False


def test_no_state_tables_configured_is_clean(tmp_path: Path) -> None:
    _seed(tmp_path, "src/integrity.py", _BAD)
    rule = build({"roots": ["src"]}, repo_root=tmp_path)
    assert rule.collect_violations() == set()


def test_build_flags_in_scope_presence_only_check(tmp_path: Path) -> None:
    _seed(tmp_path, "src/integrity.py", _BAD)
    rule = build(
        {"roots": ["src"], "state_tables": {"content_vectors": ["model", "embedded_at"]}}, repo_root=tmp_path
    )
    assert Path("src/integrity.py") in rule.collect_violations()


def test_build_clean_when_state_predicate_present(tmp_path: Path) -> None:
    _seed(tmp_path, "src/integrity.py", _OK)
    rule = build(
        {"roots": ["src"], "state_tables": {"content_vectors": ["model", "embedded_at"]}}, repo_root=tmp_path
    )
    assert rule.collect_violations() == set()
