"""Tests for the CORE check no_logging_secrets (v0.6.0 security-freshness batch)."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from tc_fitness.core_checks.no_logging_secrets import (
    DEFAULT_DIRECT_SINKS,
    DEFAULT_LOG_METHODS,
    DEFAULT_SECRET_PATTERNS,
    NoLoggingSecrets,
    build,
    module_logs_secret,
)

pytestmark = pytest.mark.integration

_PATTERNS = tuple(re.compile(p) for p in DEFAULT_SECRET_PATTERNS)


def _seed(tmp_path: Path, rel: str, body: str) -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


def test_detection_flags_logged_secret(tmp_path: Path) -> None:
    p = _seed(tmp_path, "m.py", "import logging\nlogging.info(api_key)\n")
    assert (
        module_logs_secret(
            p, patterns=_PATTERNS, log_methods=DEFAULT_LOG_METHODS, direct_sinks=DEFAULT_DIRECT_SINKS
        )
        is True
    )


def test_detection_flags_fstring_interpolation(tmp_path: Path) -> None:
    p = _seed(tmp_path, "m.py", 'logger.info(f"auth = {access_token}")\n')
    assert (
        module_logs_secret(
            p, patterns=_PATTERNS, log_methods=DEFAULT_LOG_METHODS, direct_sinks=DEFAULT_DIRECT_SINKS
        )
        is True
    )


def test_detection_flags_raise_with_secret(tmp_path: Path) -> None:
    p = _seed(tmp_path, "m.py", 'raise RuntimeError(f"bad token: {token}")\n')
    assert (
        module_logs_secret(
            p, patterns=_PATTERNS, log_methods=DEFAULT_LOG_METHODS, direct_sinks=DEFAULT_DIRECT_SINKS
        )
        is True
    )


def test_redacted_summary_is_clean(tmp_path: Path) -> None:
    p = _seed(tmp_path, "m.py", 'logger.info("api_key present: %s", api_key is not None)\n')
    assert (
        module_logs_secret(
            p, patterns=_PATTERNS, log_methods=DEFAULT_LOG_METHODS, direct_sinks=DEFAULT_DIRECT_SINKS
        )
        is False
    )


def test_length_of_secret_is_a_redacted_summary(tmp_path: Path) -> None:
    p = _seed(tmp_path, "m.py", 'logger.info("token length: %d", len(token))\n')

    assert (
        module_logs_secret(
            p, patterns=_PATTERNS, log_methods=DEFAULT_LOG_METHODS, direct_sinks=DEFAULT_DIRECT_SINKS
        )
        is False
    )


@pytest.mark.parametrize(
    "source",
    [
        'logger.info("credentials %s", user.credentials)\n',
        'logger.info("token=%s", token=token)\n',
        "print(password)\n",
        "sys.stderr.write(str(private_key))\n",
        'logger.info("token=%s", redact(token))\n',
        "raise RuntimeError(token)\n",
    ],
)
def test_secret_preserving_sinks_are_flagged(tmp_path: Path, source: str) -> None:
    p = _seed(tmp_path, "m.py", source)

    assert (
        module_logs_secret(
            p, patterns=_PATTERNS, log_methods=DEFAULT_LOG_METHODS, direct_sinks=DEFAULT_DIRECT_SINKS
        )
        is True
    )


def test_non_sink_calls_non_call_raises_and_non_secret_wrappers_are_clean(tmp_path: Path) -> None:
    p = _seed(
        tmp_path,
        "m.py",
        'send(token)\nlogger.info("token state: %s", bool(token))\nraise error\n',
    )

    assert (
        module_logs_secret(
            p, patterns=_PATTERNS, log_methods=DEFAULT_LOG_METHODS, direct_sinks=DEFAULT_DIRECT_SINKS
        )
        is False
    )


def test_unknown_stream_write_is_not_treated_as_process_output(tmp_path: Path) -> None:
    p = _seed(tmp_path, "m.py", "stream.write(token)\n")

    assert (
        module_logs_secret(
            p, patterns=_PATTERNS, log_methods=DEFAULT_LOG_METHODS, direct_sinks=DEFAULT_DIRECT_SINKS
        )
        is False
    )


def test_bad_and_unreadable_source_is_ignored(tmp_path: Path) -> None:
    missing = tmp_path / "missing.py"
    bad_syntax = _seed(tmp_path, "syntax.py", "logger.info(\n")
    invalid_encoding = tmp_path / "encoding.py"
    invalid_encoding.write_bytes(b"print(token)\n\xff")

    for path in (missing, bad_syntax, invalid_encoding):
        assert (
            module_logs_secret(
                path, patterns=_PATTERNS, log_methods=DEFAULT_LOG_METHODS, direct_sinks=DEFAULT_DIRECT_SINKS
            )
            is False
        )


def test_sink_names_and_secret_patterns_are_configurable(tmp_path: Path) -> None:
    path = _seed(tmp_path, "src/message.py", "audit.emit(secret_value)\n")
    rule = build(
        {
            "roots": ["src"],
            "secret_patterns": [r"^secret_value$"],
            "log_methods": ["emit"],
            "direct_sinks": [],
        },
        repo_root=tmp_path,
    )

    assert rule.file_has_violation(path) is True


def test_direct_constructor_uses_default_secret_patterns(tmp_path: Path) -> None:
    path = _seed(tmp_path, "module.py", "logger.info(private_key)\n")

    assert NoLoggingSecrets(repo_root=tmp_path).file_has_violation(path) is True


def test_non_secret_name_is_clean(tmp_path: Path) -> None:
    p = _seed(tmp_path, "m.py", "logger.info(client_id)\n")
    assert (
        module_logs_secret(
            p, patterns=_PATTERNS, log_methods=DEFAULT_LOG_METHODS, direct_sinks=DEFAULT_DIRECT_SINKS
        )
        is False
    )
