"""Tests for canonical Semgrep policy materialisation."""

from __future__ import annotations

from pathlib import Path

import pytest

from tc_fitness import materialize_owasp_permissions_policy

_RULE_FRAGMENT = """\
rules:
- id: python.lang.security.audit.insecure-file-permissions.insecure-file-permissions
  patterns:
  - pattern-either:
    - patterns:
      - pattern: os.$METHOD($FILE, $BITS, ...)
      - metavariable-comparison:
          metavariable: $BITS
          comparison: $BITS >= 0o650 and $BITS < 0o100000
    - patterns:
      - pattern: os.$METHOD($FILE, $BITS)
      - metavariable-comparison:
          metavariable: $BITS
          comparison: $BITS >= 0o100650
"""


def test_materialize_owasp_permissions_policy_replaces_numeric_mode_heuristic(tmp_path: Path) -> None:
    source = tmp_path / "owasp-source.yaml"
    target = tmp_path / "owasp-policy.yaml"
    source.write_text(_RULE_FRAGMENT, encoding="utf-8")

    materialize_owasp_permissions_policy(source, target)

    assert source.read_text(encoding="utf-8") == _RULE_FRAGMENT
    rendered = target.read_text(encoding="utf-8")
    assert "comparison: $BITS >= 0o650 and $BITS < 0o100000 and ($BITS & 0o077) != 0" in rendered
    assert "comparison: $BITS >= 0o100650 and ($BITS & 0o077) != 0" in rendered


def test_materialize_owasp_permissions_policy_rejects_unknown_snapshot(tmp_path: Path) -> None:
    source = tmp_path / "unknown.yaml"
    target = tmp_path / "owasp-policy.yaml"
    source.write_text("rules: []\n", encoding="utf-8")

    with pytest.raises(ValueError, match="does not contain the expected insecure-file-permissions rule"):
        materialize_owasp_permissions_policy(source, target)


def test_materialize_owasp_permissions_policy_preserves_upstream_input(tmp_path: Path) -> None:
    source = tmp_path / "owasp-source.yaml"
    source.write_text(_RULE_FRAGMENT, encoding="utf-8")

    with pytest.raises(ValueError, match="source and target must differ"):
        materialize_owasp_permissions_policy(source, source)


def test_materialize_owasp_permissions_policy_rejects_ambiguous_predicates(tmp_path: Path) -> None:
    source = tmp_path / "ambiguous.yaml"
    target = tmp_path / "owasp-policy.yaml"
    source.write_text(
        _RULE_FRAGMENT + "          comparison: $BITS >= 0o650 and $BITS < 0o100000\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="2 occurrences"):
        materialize_owasp_permissions_policy(source, target)
