"""CORE check: untrusted_automation_boundary — isolate autonomous analysis.

An autonomous workflow may read untrusted incident material, repository content,
or issue comments. It must not run in the same GitHub Actions job as cloud
login, token minting, or publishing credentials: prompt injection in the
analysis surface would otherwise have a direct route to those credentials.

Consumers opt in by naming the workflow paths and the action and credential
surfaces relevant to their platform. The check is repository-agnostic: no
workflow, action, secret, or runtime path is built in. For each configured
workflow it rejects a job that invokes a configured untrusted automation action
and also has any configured privileged capability. It also requires that the
automation action's configured contract input points at a configured runtime
contract root, keeping behaviour portable and runtime-verifiable.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path, PurePosixPath
from typing import Any

from tc_fitness.check_evidence import report_finding
from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

REMEDIATION = _remediation(
    fix=(
        "split autonomous analysis from privileged publishing into separate jobs. "
        "The analysis job may use only read-only permissions and no cloud login, "
        "token, or publishing command. Move its contract to the configured runtime "
        "contract root; make a separately validated publisher own privileged access."
    ),
    nxt="re-run this check and the workflow contract tests before opening the PR.",
    run="tc-fitness run",
    passing=(
        "investigate job: autonomous action + runtime contract + read-only permissions; "
        "publish job: validated output + cloud login or token minting"
    ),
    forbidden=(
        "one job combines an autonomous action with id-token write, cloud login, "
        "a credential environment variable, or a token/publish command"
    ),
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x__as_strings__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__as_strings__mutmut)
def _as_strings(value: object) -> tuple[str, ...]:
    """Return string members of a scalar-or-sequence config value."""
    if value is None:
        return ()
    if isinstance(value, str):
        if not value:
            raise ValueError("configured values must be a string or a sequence of non-empty strings")
        return (value,)
    if isinstance(value, Sequence) and not isinstance(value, bytes):
        if all(isinstance(item, str) and item for item in value):
            return tuple(value)
    raise ValueError("configured values must be a string or a sequence of non-empty strings")


def x__as_strings__mutmut_orig(value: object) -> tuple[str, ...]:
    """Return string members of a scalar-or-sequence config value."""
    if value is None:
        return ()
    if isinstance(value, str):
        if not value:
            raise ValueError("configured values must be a string or a sequence of non-empty strings")
        return (value,)
    if isinstance(value, Sequence) and not isinstance(value, bytes):
        if all(isinstance(item, str) and item for item in value):
            return tuple(value)
    raise ValueError("configured values must be a string or a sequence of non-empty strings")


def x__as_strings__mutmut_1(value: object) -> tuple[str, ...]:
    """Return string members of a scalar-or-sequence config value."""
    if value is not None:
        return ()
    if isinstance(value, str):
        if not value:
            raise ValueError("configured values must be a string or a sequence of non-empty strings")
        return (value,)
    if isinstance(value, Sequence) and not isinstance(value, bytes):
        if all(isinstance(item, str) and item for item in value):
            return tuple(value)
    raise ValueError("configured values must be a string or a sequence of non-empty strings")


def x__as_strings__mutmut_2(value: object) -> tuple[str, ...]:
    """Return string members of a scalar-or-sequence config value."""
    if value is None:
        return ()
    if isinstance(value, str):
        if value:
            raise ValueError("configured values must be a string or a sequence of non-empty strings")
        return (value,)
    if isinstance(value, Sequence) and not isinstance(value, bytes):
        if all(isinstance(item, str) and item for item in value):
            return tuple(value)
    raise ValueError("configured values must be a string or a sequence of non-empty strings")


def x__as_strings__mutmut_3(value: object) -> tuple[str, ...]:
    """Return string members of a scalar-or-sequence config value."""
    if value is None:
        return ()
    if isinstance(value, str):
        if not value:
            raise ValueError(None)
        return (value,)
    if isinstance(value, Sequence) and not isinstance(value, bytes):
        if all(isinstance(item, str) and item for item in value):
            return tuple(value)
    raise ValueError("configured values must be a string or a sequence of non-empty strings")


def x__as_strings__mutmut_4(value: object) -> tuple[str, ...]:
    """Return string members of a scalar-or-sequence config value."""
    if value is None:
        return ()
    if isinstance(value, str):
        if not value:
            raise ValueError("XXconfigured values must be a string or a sequence of non-empty stringsXX")
        return (value,)
    if isinstance(value, Sequence) and not isinstance(value, bytes):
        if all(isinstance(item, str) and item for item in value):
            return tuple(value)
    raise ValueError("configured values must be a string or a sequence of non-empty strings")


def x__as_strings__mutmut_5(value: object) -> tuple[str, ...]:
    """Return string members of a scalar-or-sequence config value."""
    if value is None:
        return ()
    if isinstance(value, str):
        if not value:
            raise ValueError("CONFIGURED VALUES MUST BE A STRING OR A SEQUENCE OF NON-EMPTY STRINGS")
        return (value,)
    if isinstance(value, Sequence) and not isinstance(value, bytes):
        if all(isinstance(item, str) and item for item in value):
            return tuple(value)
    raise ValueError("configured values must be a string or a sequence of non-empty strings")


def x__as_strings__mutmut_6(value: object) -> tuple[str, ...]:
    """Return string members of a scalar-or-sequence config value."""
    if value is None:
        return ()
    if isinstance(value, str):
        if not value:
            raise ValueError("configured values must be a string or a sequence of non-empty strings")
        return (value,)
    if isinstance(value, Sequence) or not isinstance(value, bytes):
        if all(isinstance(item, str) and item for item in value):
            return tuple(value)
    raise ValueError("configured values must be a string or a sequence of non-empty strings")


def x__as_strings__mutmut_7(value: object) -> tuple[str, ...]:
    """Return string members of a scalar-or-sequence config value."""
    if value is None:
        return ()
    if isinstance(value, str):
        if not value:
            raise ValueError("configured values must be a string or a sequence of non-empty strings")
        return (value,)
    if isinstance(value, Sequence) and isinstance(value, bytes):
        if all(isinstance(item, str) and item for item in value):
            return tuple(value)
    raise ValueError("configured values must be a string or a sequence of non-empty strings")


def x__as_strings__mutmut_8(value: object) -> tuple[str, ...]:
    """Return string members of a scalar-or-sequence config value."""
    if value is None:
        return ()
    if isinstance(value, str):
        if not value:
            raise ValueError("configured values must be a string or a sequence of non-empty strings")
        return (value,)
    if isinstance(value, Sequence) and not isinstance(value, bytes):
        if all(None):
            return tuple(value)
    raise ValueError("configured values must be a string or a sequence of non-empty strings")


def x__as_strings__mutmut_9(value: object) -> tuple[str, ...]:
    """Return string members of a scalar-or-sequence config value."""
    if value is None:
        return ()
    if isinstance(value, str):
        if not value:
            raise ValueError("configured values must be a string or a sequence of non-empty strings")
        return (value,)
    if isinstance(value, Sequence) and not isinstance(value, bytes):
        if all(isinstance(item, str) or item for item in value):
            return tuple(value)
    raise ValueError("configured values must be a string or a sequence of non-empty strings")


def x__as_strings__mutmut_10(value: object) -> tuple[str, ...]:
    """Return string members of a scalar-or-sequence config value."""
    if value is None:
        return ()
    if isinstance(value, str):
        if not value:
            raise ValueError("configured values must be a string or a sequence of non-empty strings")
        return (value,)
    if isinstance(value, Sequence) and not isinstance(value, bytes):
        if all(isinstance(item, str) and item for item in value):
            return tuple(None)
    raise ValueError("configured values must be a string or a sequence of non-empty strings")


def x__as_strings__mutmut_11(value: object) -> tuple[str, ...]:
    """Return string members of a scalar-or-sequence config value."""
    if value is None:
        return ()
    if isinstance(value, str):
        if not value:
            raise ValueError("configured values must be a string or a sequence of non-empty strings")
        return (value,)
    if isinstance(value, Sequence) and not isinstance(value, bytes):
        if all(isinstance(item, str) and item for item in value):
            return tuple(value)
    raise ValueError(None)


def x__as_strings__mutmut_12(value: object) -> tuple[str, ...]:
    """Return string members of a scalar-or-sequence config value."""
    if value is None:
        return ()
    if isinstance(value, str):
        if not value:
            raise ValueError("configured values must be a string or a sequence of non-empty strings")
        return (value,)
    if isinstance(value, Sequence) and not isinstance(value, bytes):
        if all(isinstance(item, str) and item for item in value):
            return tuple(value)
    raise ValueError("XXconfigured values must be a string or a sequence of non-empty stringsXX")


def x__as_strings__mutmut_13(value: object) -> tuple[str, ...]:
    """Return string members of a scalar-or-sequence config value."""
    if value is None:
        return ()
    if isinstance(value, str):
        if not value:
            raise ValueError("configured values must be a string or a sequence of non-empty strings")
        return (value,)
    if isinstance(value, Sequence) and not isinstance(value, bytes):
        if all(isinstance(item, str) and item for item in value):
            return tuple(value)
    raise ValueError("CONFIGURED VALUES MUST BE A STRING OR A SEQUENCE OF NON-EMPTY STRINGS")

mutants_x__as_strings__mutmut['_mutmut_orig'] = x__as_strings__mutmut_orig # type: ignore # mutmut generated
mutants_x__as_strings__mutmut['x__as_strings__mutmut_1'] = x__as_strings__mutmut_1 # type: ignore # mutmut generated
mutants_x__as_strings__mutmut['x__as_strings__mutmut_2'] = x__as_strings__mutmut_2 # type: ignore # mutmut generated
mutants_x__as_strings__mutmut['x__as_strings__mutmut_3'] = x__as_strings__mutmut_3 # type: ignore # mutmut generated
mutants_x__as_strings__mutmut['x__as_strings__mutmut_4'] = x__as_strings__mutmut_4 # type: ignore # mutmut generated
mutants_x__as_strings__mutmut['x__as_strings__mutmut_5'] = x__as_strings__mutmut_5 # type: ignore # mutmut generated
mutants_x__as_strings__mutmut['x__as_strings__mutmut_6'] = x__as_strings__mutmut_6 # type: ignore # mutmut generated
mutants_x__as_strings__mutmut['x__as_strings__mutmut_7'] = x__as_strings__mutmut_7 # type: ignore # mutmut generated
mutants_x__as_strings__mutmut['x__as_strings__mutmut_8'] = x__as_strings__mutmut_8 # type: ignore # mutmut generated
mutants_x__as_strings__mutmut['x__as_strings__mutmut_9'] = x__as_strings__mutmut_9 # type: ignore # mutmut generated
mutants_x__as_strings__mutmut['x__as_strings__mutmut_10'] = x__as_strings__mutmut_10 # type: ignore # mutmut generated
mutants_x__as_strings__mutmut['x__as_strings__mutmut_11'] = x__as_strings__mutmut_11 # type: ignore # mutmut generated
mutants_x__as_strings__mutmut['x__as_strings__mutmut_12'] = x__as_strings__mutmut_12 # type: ignore # mutmut generated
mutants_x__as_strings__mutmut['x__as_strings__mutmut_13'] = x__as_strings__mutmut_13 # type: ignore # mutmut generated
mutants_x__load_workflow__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__load_workflow__mutmut)
def _load_workflow(path: Path) -> Mapping[str, Any] | None:
    """Parse one workflow, returning ``None`` for unreadable or invalid YAML."""
    try:
        import yaml
    except ImportError:
        return None
    try:
        loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        return None
    return loaded if isinstance(loaded, Mapping) else None


def x__load_workflow__mutmut_orig(path: Path) -> Mapping[str, Any] | None:
    """Parse one workflow, returning ``None`` for unreadable or invalid YAML."""
    try:
        import yaml
    except ImportError:
        return None
    try:
        loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        return None
    return loaded if isinstance(loaded, Mapping) else None


def x__load_workflow__mutmut_1(path: Path) -> Mapping[str, Any] | None:
    """Parse one workflow, returning ``None`` for unreadable or invalid YAML."""
    try:
        import yaml
    except ImportError:
        return None
    try:
        loaded = None
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        return None
    return loaded if isinstance(loaded, Mapping) else None


def x__load_workflow__mutmut_2(path: Path) -> Mapping[str, Any] | None:
    """Parse one workflow, returning ``None`` for unreadable or invalid YAML."""
    try:
        import yaml
    except ImportError:
        return None
    try:
        loaded = yaml.safe_load(None)
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        return None
    return loaded if isinstance(loaded, Mapping) else None


def x__load_workflow__mutmut_3(path: Path) -> Mapping[str, Any] | None:
    """Parse one workflow, returning ``None`` for unreadable or invalid YAML."""
    try:
        import yaml
    except ImportError:
        return None
    try:
        loaded = yaml.safe_load(path.read_text(encoding=None))
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        return None
    return loaded if isinstance(loaded, Mapping) else None


def x__load_workflow__mutmut_4(path: Path) -> Mapping[str, Any] | None:
    """Parse one workflow, returning ``None`` for unreadable or invalid YAML."""
    try:
        import yaml
    except ImportError:
        return None
    try:
        loaded = yaml.safe_load(path.read_text(encoding="XXutf-8XX"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        return None
    return loaded if isinstance(loaded, Mapping) else None


def x__load_workflow__mutmut_5(path: Path) -> Mapping[str, Any] | None:
    """Parse one workflow, returning ``None`` for unreadable or invalid YAML."""
    try:
        import yaml
    except ImportError:
        return None
    try:
        loaded = yaml.safe_load(path.read_text(encoding="UTF-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        return None
    return loaded if isinstance(loaded, Mapping) else None

mutants_x__load_workflow__mutmut['_mutmut_orig'] = x__load_workflow__mutmut_orig # type: ignore # mutmut generated
mutants_x__load_workflow__mutmut['x__load_workflow__mutmut_1'] = x__load_workflow__mutmut_1 # type: ignore # mutmut generated
mutants_x__load_workflow__mutmut['x__load_workflow__mutmut_2'] = x__load_workflow__mutmut_2 # type: ignore # mutmut generated
mutants_x__load_workflow__mutmut['x__load_workflow__mutmut_3'] = x__load_workflow__mutmut_3 # type: ignore # mutmut generated
mutants_x__load_workflow__mutmut['x__load_workflow__mutmut_4'] = x__load_workflow__mutmut_4 # type: ignore # mutmut generated
mutants_x__load_workflow__mutmut['x__load_workflow__mutmut_5'] = x__load_workflow__mutmut_5 # type: ignore # mutmut generated
mutants_x__step_uses__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__step_uses__mutmut)
def _step_uses(step: Mapping[str, Any], prefixes: tuple[str, ...]) -> bool:
    """Whether ``step`` invokes an action with a configured prefix."""
    uses = step.get("uses")
    return isinstance(uses, str) and any(uses.casefold().startswith(prefix.casefold()) for prefix in prefixes)


def x__step_uses__mutmut_orig(step: Mapping[str, Any], prefixes: tuple[str, ...]) -> bool:
    """Whether ``step`` invokes an action with a configured prefix."""
    uses = step.get("uses")
    return isinstance(uses, str) and any(uses.casefold().startswith(prefix.casefold()) for prefix in prefixes)


def x__step_uses__mutmut_1(step: Mapping[str, Any], prefixes: tuple[str, ...]) -> bool:
    """Whether ``step`` invokes an action with a configured prefix."""
    uses = None
    return isinstance(uses, str) and any(uses.casefold().startswith(prefix.casefold()) for prefix in prefixes)


def x__step_uses__mutmut_2(step: Mapping[str, Any], prefixes: tuple[str, ...]) -> bool:
    """Whether ``step`` invokes an action with a configured prefix."""
    uses = step.get(None)
    return isinstance(uses, str) and any(uses.casefold().startswith(prefix.casefold()) for prefix in prefixes)


def x__step_uses__mutmut_3(step: Mapping[str, Any], prefixes: tuple[str, ...]) -> bool:
    """Whether ``step`` invokes an action with a configured prefix."""
    uses = step.get("XXusesXX")
    return isinstance(uses, str) and any(uses.casefold().startswith(prefix.casefold()) for prefix in prefixes)


def x__step_uses__mutmut_4(step: Mapping[str, Any], prefixes: tuple[str, ...]) -> bool:
    """Whether ``step`` invokes an action with a configured prefix."""
    uses = step.get("USES")
    return isinstance(uses, str) and any(uses.casefold().startswith(prefix.casefold()) for prefix in prefixes)


def x__step_uses__mutmut_5(step: Mapping[str, Any], prefixes: tuple[str, ...]) -> bool:
    """Whether ``step`` invokes an action with a configured prefix."""
    uses = step.get("uses")
    return isinstance(uses, str) or any(uses.casefold().startswith(prefix.casefold()) for prefix in prefixes)


def x__step_uses__mutmut_6(step: Mapping[str, Any], prefixes: tuple[str, ...]) -> bool:
    """Whether ``step`` invokes an action with a configured prefix."""
    uses = step.get("uses")
    return isinstance(uses, str) and any(None)


def x__step_uses__mutmut_7(step: Mapping[str, Any], prefixes: tuple[str, ...]) -> bool:
    """Whether ``step`` invokes an action with a configured prefix."""
    uses = step.get("uses")
    return isinstance(uses, str) and any(uses.casefold().startswith(None) for prefix in prefixes)

mutants_x__step_uses__mutmut['_mutmut_orig'] = x__step_uses__mutmut_orig # type: ignore # mutmut generated
mutants_x__step_uses__mutmut['x__step_uses__mutmut_1'] = x__step_uses__mutmut_1 # type: ignore # mutmut generated
mutants_x__step_uses__mutmut['x__step_uses__mutmut_2'] = x__step_uses__mutmut_2 # type: ignore # mutmut generated
mutants_x__step_uses__mutmut['x__step_uses__mutmut_3'] = x__step_uses__mutmut_3 # type: ignore # mutmut generated
mutants_x__step_uses__mutmut['x__step_uses__mutmut_4'] = x__step_uses__mutmut_4 # type: ignore # mutmut generated
mutants_x__step_uses__mutmut['x__step_uses__mutmut_5'] = x__step_uses__mutmut_5 # type: ignore # mutmut generated
mutants_x__step_uses__mutmut['x__step_uses__mutmut_6'] = x__step_uses__mutmut_6 # type: ignore # mutmut generated
mutants_x__step_uses__mutmut['x__step_uses__mutmut_7'] = x__step_uses__mutmut_7 # type: ignore # mutmut generated
mutants_x__mapping_has_credential_env__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__mapping_has_credential_env__mutmut)
def _mapping_has_credential_env(value: object, names: tuple[str, ...]) -> bool:
    """Whether an ``env`` mapping names a configured credential variable."""
    return isinstance(value, Mapping) and any(name in value for name in names)


def x__mapping_has_credential_env__mutmut_orig(value: object, names: tuple[str, ...]) -> bool:
    """Whether an ``env`` mapping names a configured credential variable."""
    return isinstance(value, Mapping) and any(name in value for name in names)


def x__mapping_has_credential_env__mutmut_1(value: object, names: tuple[str, ...]) -> bool:
    """Whether an ``env`` mapping names a configured credential variable."""
    return isinstance(value, Mapping) or any(name in value for name in names)


def x__mapping_has_credential_env__mutmut_2(value: object, names: tuple[str, ...]) -> bool:
    """Whether an ``env`` mapping names a configured credential variable."""
    return isinstance(value, Mapping) and any(None)


def x__mapping_has_credential_env__mutmut_3(value: object, names: tuple[str, ...]) -> bool:
    """Whether an ``env`` mapping names a configured credential variable."""
    return isinstance(value, Mapping) and any(name not in value for name in names)

mutants_x__mapping_has_credential_env__mutmut['_mutmut_orig'] = x__mapping_has_credential_env__mutmut_orig # type: ignore # mutmut generated
mutants_x__mapping_has_credential_env__mutmut['x__mapping_has_credential_env__mutmut_1'] = x__mapping_has_credential_env__mutmut_1 # type: ignore # mutmut generated
mutants_x__mapping_has_credential_env__mutmut['x__mapping_has_credential_env__mutmut_2'] = x__mapping_has_credential_env__mutmut_2 # type: ignore # mutmut generated
mutants_x__mapping_has_credential_env__mutmut['x__mapping_has_credential_env__mutmut_3'] = x__mapping_has_credential_env__mutmut_3 # type: ignore # mutmut generated
mutants_x__has_privileged_permission__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__has_privileged_permission__mutmut)
def _has_privileged_permission(value: object, names: tuple[str, ...]) -> bool:
    """Whether a GitHub permissions mapping grants a configured write capability."""
    if isinstance(value, str):
        return value.casefold() == "write-all" and bool(names)
    if not isinstance(value, Mapping):
        return False
    return any(str(value.get(name, "")).lower() == "write" for name in names)


def x__has_privileged_permission__mutmut_orig(value: object, names: tuple[str, ...]) -> bool:
    """Whether a GitHub permissions mapping grants a configured write capability."""
    if isinstance(value, str):
        return value.casefold() == "write-all" and bool(names)
    if not isinstance(value, Mapping):
        return False
    return any(str(value.get(name, "")).lower() == "write" for name in names)


def x__has_privileged_permission__mutmut_1(value: object, names: tuple[str, ...]) -> bool:
    """Whether a GitHub permissions mapping grants a configured write capability."""
    if isinstance(value, str):
        return value.casefold() == "write-all" or bool(names)
    if not isinstance(value, Mapping):
        return False
    return any(str(value.get(name, "")).lower() == "write" for name in names)


def x__has_privileged_permission__mutmut_2(value: object, names: tuple[str, ...]) -> bool:
    """Whether a GitHub permissions mapping grants a configured write capability."""
    if isinstance(value, str):
        return value.casefold() != "write-all" and bool(names)
    if not isinstance(value, Mapping):
        return False
    return any(str(value.get(name, "")).lower() == "write" for name in names)


def x__has_privileged_permission__mutmut_3(value: object, names: tuple[str, ...]) -> bool:
    """Whether a GitHub permissions mapping grants a configured write capability."""
    if isinstance(value, str):
        return value.casefold() == "XXwrite-allXX" and bool(names)
    if not isinstance(value, Mapping):
        return False
    return any(str(value.get(name, "")).lower() == "write" for name in names)


def x__has_privileged_permission__mutmut_4(value: object, names: tuple[str, ...]) -> bool:
    """Whether a GitHub permissions mapping grants a configured write capability."""
    if isinstance(value, str):
        return value.casefold() == "WRITE-ALL" and bool(names)
    if not isinstance(value, Mapping):
        return False
    return any(str(value.get(name, "")).lower() == "write" for name in names)


def x__has_privileged_permission__mutmut_5(value: object, names: tuple[str, ...]) -> bool:
    """Whether a GitHub permissions mapping grants a configured write capability."""
    if isinstance(value, str):
        return value.casefold() == "write-all" and bool(None)
    if not isinstance(value, Mapping):
        return False
    return any(str(value.get(name, "")).lower() == "write" for name in names)


def x__has_privileged_permission__mutmut_6(value: object, names: tuple[str, ...]) -> bool:
    """Whether a GitHub permissions mapping grants a configured write capability."""
    if isinstance(value, str):
        return value.casefold() == "write-all" and bool(names)
    if isinstance(value, Mapping):
        return False
    return any(str(value.get(name, "")).lower() == "write" for name in names)


def x__has_privileged_permission__mutmut_7(value: object, names: tuple[str, ...]) -> bool:
    """Whether a GitHub permissions mapping grants a configured write capability."""
    if isinstance(value, str):
        return value.casefold() == "write-all" and bool(names)
    if not isinstance(value, Mapping):
        return True
    return any(str(value.get(name, "")).lower() == "write" for name in names)


def x__has_privileged_permission__mutmut_8(value: object, names: tuple[str, ...]) -> bool:
    """Whether a GitHub permissions mapping grants a configured write capability."""
    if isinstance(value, str):
        return value.casefold() == "write-all" and bool(names)
    if not isinstance(value, Mapping):
        return False
    return any(None)


def x__has_privileged_permission__mutmut_9(value: object, names: tuple[str, ...]) -> bool:
    """Whether a GitHub permissions mapping grants a configured write capability."""
    if isinstance(value, str):
        return value.casefold() == "write-all" and bool(names)
    if not isinstance(value, Mapping):
        return False
    return any(str(value.get(name, "")).upper() == "write" for name in names)


def x__has_privileged_permission__mutmut_10(value: object, names: tuple[str, ...]) -> bool:
    """Whether a GitHub permissions mapping grants a configured write capability."""
    if isinstance(value, str):
        return value.casefold() == "write-all" and bool(names)
    if not isinstance(value, Mapping):
        return False
    return any(str(None).lower() == "write" for name in names)


def x__has_privileged_permission__mutmut_11(value: object, names: tuple[str, ...]) -> bool:
    """Whether a GitHub permissions mapping grants a configured write capability."""
    if isinstance(value, str):
        return value.casefold() == "write-all" and bool(names)
    if not isinstance(value, Mapping):
        return False
    return any(str(value.get(None, "")).lower() == "write" for name in names)


def x__has_privileged_permission__mutmut_12(value: object, names: tuple[str, ...]) -> bool:
    """Whether a GitHub permissions mapping grants a configured write capability."""
    if isinstance(value, str):
        return value.casefold() == "write-all" and bool(names)
    if not isinstance(value, Mapping):
        return False
    return any(str(value.get(name, None)).lower() == "write" for name in names)


def x__has_privileged_permission__mutmut_13(value: object, names: tuple[str, ...]) -> bool:
    """Whether a GitHub permissions mapping grants a configured write capability."""
    if isinstance(value, str):
        return value.casefold() == "write-all" and bool(names)
    if not isinstance(value, Mapping):
        return False
    return any(str(value.get("")).lower() == "write" for name in names)


def x__has_privileged_permission__mutmut_14(value: object, names: tuple[str, ...]) -> bool:
    """Whether a GitHub permissions mapping grants a configured write capability."""
    if isinstance(value, str):
        return value.casefold() == "write-all" and bool(names)
    if not isinstance(value, Mapping):
        return False
    return any(str(value.get(name, )).lower() == "write" for name in names)


def x__has_privileged_permission__mutmut_15(value: object, names: tuple[str, ...]) -> bool:
    """Whether a GitHub permissions mapping grants a configured write capability."""
    if isinstance(value, str):
        return value.casefold() == "write-all" and bool(names)
    if not isinstance(value, Mapping):
        return False
    return any(str(value.get(name, "XXXX")).lower() == "write" for name in names)


def x__has_privileged_permission__mutmut_16(value: object, names: tuple[str, ...]) -> bool:
    """Whether a GitHub permissions mapping grants a configured write capability."""
    if isinstance(value, str):
        return value.casefold() == "write-all" and bool(names)
    if not isinstance(value, Mapping):
        return False
    return any(str(value.get(name, "")).lower() != "write" for name in names)


def x__has_privileged_permission__mutmut_17(value: object, names: tuple[str, ...]) -> bool:
    """Whether a GitHub permissions mapping grants a configured write capability."""
    if isinstance(value, str):
        return value.casefold() == "write-all" and bool(names)
    if not isinstance(value, Mapping):
        return False
    return any(str(value.get(name, "")).lower() == "XXwriteXX" for name in names)


def x__has_privileged_permission__mutmut_18(value: object, names: tuple[str, ...]) -> bool:
    """Whether a GitHub permissions mapping grants a configured write capability."""
    if isinstance(value, str):
        return value.casefold() == "write-all" and bool(names)
    if not isinstance(value, Mapping):
        return False
    return any(str(value.get(name, "")).lower() == "WRITE" for name in names)

mutants_x__has_privileged_permission__mutmut['_mutmut_orig'] = x__has_privileged_permission__mutmut_orig # type: ignore # mutmut generated
mutants_x__has_privileged_permission__mutmut['x__has_privileged_permission__mutmut_1'] = x__has_privileged_permission__mutmut_1 # type: ignore # mutmut generated
mutants_x__has_privileged_permission__mutmut['x__has_privileged_permission__mutmut_2'] = x__has_privileged_permission__mutmut_2 # type: ignore # mutmut generated
mutants_x__has_privileged_permission__mutmut['x__has_privileged_permission__mutmut_3'] = x__has_privileged_permission__mutmut_3 # type: ignore # mutmut generated
mutants_x__has_privileged_permission__mutmut['x__has_privileged_permission__mutmut_4'] = x__has_privileged_permission__mutmut_4 # type: ignore # mutmut generated
mutants_x__has_privileged_permission__mutmut['x__has_privileged_permission__mutmut_5'] = x__has_privileged_permission__mutmut_5 # type: ignore # mutmut generated
mutants_x__has_privileged_permission__mutmut['x__has_privileged_permission__mutmut_6'] = x__has_privileged_permission__mutmut_6 # type: ignore # mutmut generated
mutants_x__has_privileged_permission__mutmut['x__has_privileged_permission__mutmut_7'] = x__has_privileged_permission__mutmut_7 # type: ignore # mutmut generated
mutants_x__has_privileged_permission__mutmut['x__has_privileged_permission__mutmut_8'] = x__has_privileged_permission__mutmut_8 # type: ignore # mutmut generated
mutants_x__has_privileged_permission__mutmut['x__has_privileged_permission__mutmut_9'] = x__has_privileged_permission__mutmut_9 # type: ignore # mutmut generated
mutants_x__has_privileged_permission__mutmut['x__has_privileged_permission__mutmut_10'] = x__has_privileged_permission__mutmut_10 # type: ignore # mutmut generated
mutants_x__has_privileged_permission__mutmut['x__has_privileged_permission__mutmut_11'] = x__has_privileged_permission__mutmut_11 # type: ignore # mutmut generated
mutants_x__has_privileged_permission__mutmut['x__has_privileged_permission__mutmut_12'] = x__has_privileged_permission__mutmut_12 # type: ignore # mutmut generated
mutants_x__has_privileged_permission__mutmut['x__has_privileged_permission__mutmut_13'] = x__has_privileged_permission__mutmut_13 # type: ignore # mutmut generated
mutants_x__has_privileged_permission__mutmut['x__has_privileged_permission__mutmut_14'] = x__has_privileged_permission__mutmut_14 # type: ignore # mutmut generated
mutants_x__has_privileged_permission__mutmut['x__has_privileged_permission__mutmut_15'] = x__has_privileged_permission__mutmut_15 # type: ignore # mutmut generated
mutants_x__has_privileged_permission__mutmut['x__has_privileged_permission__mutmut_16'] = x__has_privileged_permission__mutmut_16 # type: ignore # mutmut generated
mutants_x__has_privileged_permission__mutmut['x__has_privileged_permission__mutmut_17'] = x__has_privileged_permission__mutmut_17 # type: ignore # mutmut generated
mutants_x__has_privileged_permission__mutmut['x__has_privileged_permission__mutmut_18'] = x__has_privileged_permission__mutmut_18 # type: ignore # mutmut generated
mutants_x__normalise_relative_path__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__normalise_relative_path__mutmut)
def _normalise_relative_path(value: str) -> tuple[str, ...] | None:
    """Return normalised relative POSIX components, rejecting root escape."""
    path = PurePosixPath(value)
    if path.is_absolute():
        return None
    parts: list[str] = []
    for part in path.parts:
        if part == "..":
            if not parts:
                return None
            parts.pop()
            continue
        parts.append(part)
    return tuple(parts)


def x__normalise_relative_path__mutmut_orig(value: str) -> tuple[str, ...] | None:
    """Return normalised relative POSIX components, rejecting root escape."""
    path = PurePosixPath(value)
    if path.is_absolute():
        return None
    parts: list[str] = []
    for part in path.parts:
        if part == "..":
            if not parts:
                return None
            parts.pop()
            continue
        parts.append(part)
    return tuple(parts)


def x__normalise_relative_path__mutmut_1(value: str) -> tuple[str, ...] | None:
    """Return normalised relative POSIX components, rejecting root escape."""
    path = None
    if path.is_absolute():
        return None
    parts: list[str] = []
    for part in path.parts:
        if part == "..":
            if not parts:
                return None
            parts.pop()
            continue
        parts.append(part)
    return tuple(parts)


def x__normalise_relative_path__mutmut_2(value: str) -> tuple[str, ...] | None:
    """Return normalised relative POSIX components, rejecting root escape."""
    path = PurePosixPath(None)
    if path.is_absolute():
        return None
    parts: list[str] = []
    for part in path.parts:
        if part == "..":
            if not parts:
                return None
            parts.pop()
            continue
        parts.append(part)
    return tuple(parts)


def x__normalise_relative_path__mutmut_3(value: str) -> tuple[str, ...] | None:
    """Return normalised relative POSIX components, rejecting root escape."""
    path = PurePosixPath(value)
    if path.is_absolute():
        return None
    parts: list[str] = None
    for part in path.parts:
        if part == "..":
            if not parts:
                return None
            parts.pop()
            continue
        parts.append(part)
    return tuple(parts)


def x__normalise_relative_path__mutmut_4(value: str) -> tuple[str, ...] | None:
    """Return normalised relative POSIX components, rejecting root escape."""
    path = PurePosixPath(value)
    if path.is_absolute():
        return None
    parts: list[str] = []
    for part in path.parts:
        if part != "..":
            if not parts:
                return None
            parts.pop()
            continue
        parts.append(part)
    return tuple(parts)


def x__normalise_relative_path__mutmut_5(value: str) -> tuple[str, ...] | None:
    """Return normalised relative POSIX components, rejecting root escape."""
    path = PurePosixPath(value)
    if path.is_absolute():
        return None
    parts: list[str] = []
    for part in path.parts:
        if part == "XX..XX":
            if not parts:
                return None
            parts.pop()
            continue
        parts.append(part)
    return tuple(parts)


def x__normalise_relative_path__mutmut_6(value: str) -> tuple[str, ...] | None:
    """Return normalised relative POSIX components, rejecting root escape."""
    path = PurePosixPath(value)
    if path.is_absolute():
        return None
    parts: list[str] = []
    for part in path.parts:
        if part == "..":
            if parts:
                return None
            parts.pop()
            continue
        parts.append(part)
    return tuple(parts)


def x__normalise_relative_path__mutmut_7(value: str) -> tuple[str, ...] | None:
    """Return normalised relative POSIX components, rejecting root escape."""
    path = PurePosixPath(value)
    if path.is_absolute():
        return None
    parts: list[str] = []
    for part in path.parts:
        if part == "..":
            if not parts:
                return None
            parts.pop()
            break
        parts.append(part)
    return tuple(parts)


def x__normalise_relative_path__mutmut_8(value: str) -> tuple[str, ...] | None:
    """Return normalised relative POSIX components, rejecting root escape."""
    path = PurePosixPath(value)
    if path.is_absolute():
        return None
    parts: list[str] = []
    for part in path.parts:
        if part == "..":
            if not parts:
                return None
            parts.pop()
            continue
        parts.append(None)
    return tuple(parts)


def x__normalise_relative_path__mutmut_9(value: str) -> tuple[str, ...] | None:
    """Return normalised relative POSIX components, rejecting root escape."""
    path = PurePosixPath(value)
    if path.is_absolute():
        return None
    parts: list[str] = []
    for part in path.parts:
        if part == "..":
            if not parts:
                return None
            parts.pop()
            continue
        parts.append(part)
    return tuple(None)

mutants_x__normalise_relative_path__mutmut['_mutmut_orig'] = x__normalise_relative_path__mutmut_orig # type: ignore # mutmut generated
mutants_x__normalise_relative_path__mutmut['x__normalise_relative_path__mutmut_1'] = x__normalise_relative_path__mutmut_1 # type: ignore # mutmut generated
mutants_x__normalise_relative_path__mutmut['x__normalise_relative_path__mutmut_2'] = x__normalise_relative_path__mutmut_2 # type: ignore # mutmut generated
mutants_x__normalise_relative_path__mutmut['x__normalise_relative_path__mutmut_3'] = x__normalise_relative_path__mutmut_3 # type: ignore # mutmut generated
mutants_x__normalise_relative_path__mutmut['x__normalise_relative_path__mutmut_4'] = x__normalise_relative_path__mutmut_4 # type: ignore # mutmut generated
mutants_x__normalise_relative_path__mutmut['x__normalise_relative_path__mutmut_5'] = x__normalise_relative_path__mutmut_5 # type: ignore # mutmut generated
mutants_x__normalise_relative_path__mutmut['x__normalise_relative_path__mutmut_6'] = x__normalise_relative_path__mutmut_6 # type: ignore # mutmut generated
mutants_x__normalise_relative_path__mutmut['x__normalise_relative_path__mutmut_7'] = x__normalise_relative_path__mutmut_7 # type: ignore # mutmut generated
mutants_x__normalise_relative_path__mutmut['x__normalise_relative_path__mutmut_8'] = x__normalise_relative_path__mutmut_8 # type: ignore # mutmut generated
mutants_x__normalise_relative_path__mutmut['x__normalise_relative_path__mutmut_9'] = x__normalise_relative_path__mutmut_9 # type: ignore # mutmut generated
mutants_x__is_at_runtime_root__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__is_at_runtime_root__mutmut)
def _is_at_runtime_root(contract_path: str, runtime_contract_roots: tuple[str, ...]) -> bool:
    """Whether a normalised contract path is within one configured root."""
    contract_parts = _normalise_relative_path(contract_path)
    if contract_parts is None:
        return False
    for root in runtime_contract_roots:
        root_parts = _normalise_relative_path(root)
        if root_parts and contract_parts[: len(root_parts)] == root_parts:
            return True
    return False


def x__is_at_runtime_root__mutmut_orig(contract_path: str, runtime_contract_roots: tuple[str, ...]) -> bool:
    """Whether a normalised contract path is within one configured root."""
    contract_parts = _normalise_relative_path(contract_path)
    if contract_parts is None:
        return False
    for root in runtime_contract_roots:
        root_parts = _normalise_relative_path(root)
        if root_parts and contract_parts[: len(root_parts)] == root_parts:
            return True
    return False


def x__is_at_runtime_root__mutmut_1(contract_path: str, runtime_contract_roots: tuple[str, ...]) -> bool:
    """Whether a normalised contract path is within one configured root."""
    contract_parts = None
    if contract_parts is None:
        return False
    for root in runtime_contract_roots:
        root_parts = _normalise_relative_path(root)
        if root_parts and contract_parts[: len(root_parts)] == root_parts:
            return True
    return False


def x__is_at_runtime_root__mutmut_2(contract_path: str, runtime_contract_roots: tuple[str, ...]) -> bool:
    """Whether a normalised contract path is within one configured root."""
    contract_parts = _normalise_relative_path(None)
    if contract_parts is None:
        return False
    for root in runtime_contract_roots:
        root_parts = _normalise_relative_path(root)
        if root_parts and contract_parts[: len(root_parts)] == root_parts:
            return True
    return False


def x__is_at_runtime_root__mutmut_3(contract_path: str, runtime_contract_roots: tuple[str, ...]) -> bool:
    """Whether a normalised contract path is within one configured root."""
    contract_parts = _normalise_relative_path(contract_path)
    if contract_parts is not None:
        return False
    for root in runtime_contract_roots:
        root_parts = _normalise_relative_path(root)
        if root_parts and contract_parts[: len(root_parts)] == root_parts:
            return True
    return False


def x__is_at_runtime_root__mutmut_4(contract_path: str, runtime_contract_roots: tuple[str, ...]) -> bool:
    """Whether a normalised contract path is within one configured root."""
    contract_parts = _normalise_relative_path(contract_path)
    if contract_parts is None:
        return True
    for root in runtime_contract_roots:
        root_parts = _normalise_relative_path(root)
        if root_parts and contract_parts[: len(root_parts)] == root_parts:
            return True
    return False


def x__is_at_runtime_root__mutmut_5(contract_path: str, runtime_contract_roots: tuple[str, ...]) -> bool:
    """Whether a normalised contract path is within one configured root."""
    contract_parts = _normalise_relative_path(contract_path)
    if contract_parts is None:
        return False
    for root in runtime_contract_roots:
        root_parts = None
        if root_parts and contract_parts[: len(root_parts)] == root_parts:
            return True
    return False


def x__is_at_runtime_root__mutmut_6(contract_path: str, runtime_contract_roots: tuple[str, ...]) -> bool:
    """Whether a normalised contract path is within one configured root."""
    contract_parts = _normalise_relative_path(contract_path)
    if contract_parts is None:
        return False
    for root in runtime_contract_roots:
        root_parts = _normalise_relative_path(None)
        if root_parts and contract_parts[: len(root_parts)] == root_parts:
            return True
    return False


def x__is_at_runtime_root__mutmut_7(contract_path: str, runtime_contract_roots: tuple[str, ...]) -> bool:
    """Whether a normalised contract path is within one configured root."""
    contract_parts = _normalise_relative_path(contract_path)
    if contract_parts is None:
        return False
    for root in runtime_contract_roots:
        root_parts = _normalise_relative_path(root)
        if root_parts or contract_parts[: len(root_parts)] == root_parts:
            return True
    return False


def x__is_at_runtime_root__mutmut_8(contract_path: str, runtime_contract_roots: tuple[str, ...]) -> bool:
    """Whether a normalised contract path is within one configured root."""
    contract_parts = _normalise_relative_path(contract_path)
    if contract_parts is None:
        return False
    for root in runtime_contract_roots:
        root_parts = _normalise_relative_path(root)
        if root_parts and contract_parts[: len(root_parts)] != root_parts:
            return True
    return False


def x__is_at_runtime_root__mutmut_9(contract_path: str, runtime_contract_roots: tuple[str, ...]) -> bool:
    """Whether a normalised contract path is within one configured root."""
    contract_parts = _normalise_relative_path(contract_path)
    if contract_parts is None:
        return False
    for root in runtime_contract_roots:
        root_parts = _normalise_relative_path(root)
        if root_parts and contract_parts[: len(root_parts)] == root_parts:
            return False
    return False


def x__is_at_runtime_root__mutmut_10(contract_path: str, runtime_contract_roots: tuple[str, ...]) -> bool:
    """Whether a normalised contract path is within one configured root."""
    contract_parts = _normalise_relative_path(contract_path)
    if contract_parts is None:
        return False
    for root in runtime_contract_roots:
        root_parts = _normalise_relative_path(root)
        if root_parts and contract_parts[: len(root_parts)] == root_parts:
            return True
    return True

mutants_x__is_at_runtime_root__mutmut['_mutmut_orig'] = x__is_at_runtime_root__mutmut_orig # type: ignore # mutmut generated
mutants_x__is_at_runtime_root__mutmut['x__is_at_runtime_root__mutmut_1'] = x__is_at_runtime_root__mutmut_1 # type: ignore # mutmut generated
mutants_x__is_at_runtime_root__mutmut['x__is_at_runtime_root__mutmut_2'] = x__is_at_runtime_root__mutmut_2 # type: ignore # mutmut generated
mutants_x__is_at_runtime_root__mutmut['x__is_at_runtime_root__mutmut_3'] = x__is_at_runtime_root__mutmut_3 # type: ignore # mutmut generated
mutants_x__is_at_runtime_root__mutmut['x__is_at_runtime_root__mutmut_4'] = x__is_at_runtime_root__mutmut_4 # type: ignore # mutmut generated
mutants_x__is_at_runtime_root__mutmut['x__is_at_runtime_root__mutmut_5'] = x__is_at_runtime_root__mutmut_5 # type: ignore # mutmut generated
mutants_x__is_at_runtime_root__mutmut['x__is_at_runtime_root__mutmut_6'] = x__is_at_runtime_root__mutmut_6 # type: ignore # mutmut generated
mutants_x__is_at_runtime_root__mutmut['x__is_at_runtime_root__mutmut_7'] = x__is_at_runtime_root__mutmut_7 # type: ignore # mutmut generated
mutants_x__is_at_runtime_root__mutmut['x__is_at_runtime_root__mutmut_8'] = x__is_at_runtime_root__mutmut_8 # type: ignore # mutmut generated
mutants_x__is_at_runtime_root__mutmut['x__is_at_runtime_root__mutmut_9'] = x__is_at_runtime_root__mutmut_9 # type: ignore # mutmut generated
mutants_x__is_at_runtime_root__mutmut['x__is_at_runtime_root__mutmut_10'] = x__is_at_runtime_root__mutmut_10 # type: ignore # mutmut generated
mutants_x__has_contract_at_runtime_root__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__has_contract_at_runtime_root__mutmut)
def _has_contract_at_runtime_root(
    step: Mapping[str, Any],
    *,
    contract_keys: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
) -> bool:
    """Whether the autonomous action reads a configured contract from runtime scope."""
    if not contract_keys or not runtime_contract_roots:
        return True
    with_value = step.get("with")
    if not isinstance(with_value, Mapping):
        return False
    for key in contract_keys:
        contract_path = with_value.get(key)
        if isinstance(contract_path, str) and _is_at_runtime_root(contract_path, runtime_contract_roots):
            return True
    return False


def x__has_contract_at_runtime_root__mutmut_orig(
    step: Mapping[str, Any],
    *,
    contract_keys: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
) -> bool:
    """Whether the autonomous action reads a configured contract from runtime scope."""
    if not contract_keys or not runtime_contract_roots:
        return True
    with_value = step.get("with")
    if not isinstance(with_value, Mapping):
        return False
    for key in contract_keys:
        contract_path = with_value.get(key)
        if isinstance(contract_path, str) and _is_at_runtime_root(contract_path, runtime_contract_roots):
            return True
    return False


def x__has_contract_at_runtime_root__mutmut_1(
    step: Mapping[str, Any],
    *,
    contract_keys: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
) -> bool:
    """Whether the autonomous action reads a configured contract from runtime scope."""
    if not contract_keys and not runtime_contract_roots:
        return True
    with_value = step.get("with")
    if not isinstance(with_value, Mapping):
        return False
    for key in contract_keys:
        contract_path = with_value.get(key)
        if isinstance(contract_path, str) and _is_at_runtime_root(contract_path, runtime_contract_roots):
            return True
    return False


def x__has_contract_at_runtime_root__mutmut_2(
    step: Mapping[str, Any],
    *,
    contract_keys: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
) -> bool:
    """Whether the autonomous action reads a configured contract from runtime scope."""
    if contract_keys or not runtime_contract_roots:
        return True
    with_value = step.get("with")
    if not isinstance(with_value, Mapping):
        return False
    for key in contract_keys:
        contract_path = with_value.get(key)
        if isinstance(contract_path, str) and _is_at_runtime_root(contract_path, runtime_contract_roots):
            return True
    return False


def x__has_contract_at_runtime_root__mutmut_3(
    step: Mapping[str, Any],
    *,
    contract_keys: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
) -> bool:
    """Whether the autonomous action reads a configured contract from runtime scope."""
    if not contract_keys or runtime_contract_roots:
        return True
    with_value = step.get("with")
    if not isinstance(with_value, Mapping):
        return False
    for key in contract_keys:
        contract_path = with_value.get(key)
        if isinstance(contract_path, str) and _is_at_runtime_root(contract_path, runtime_contract_roots):
            return True
    return False


def x__has_contract_at_runtime_root__mutmut_4(
    step: Mapping[str, Any],
    *,
    contract_keys: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
) -> bool:
    """Whether the autonomous action reads a configured contract from runtime scope."""
    if not contract_keys or not runtime_contract_roots:
        return False
    with_value = step.get("with")
    if not isinstance(with_value, Mapping):
        return False
    for key in contract_keys:
        contract_path = with_value.get(key)
        if isinstance(contract_path, str) and _is_at_runtime_root(contract_path, runtime_contract_roots):
            return True
    return False


def x__has_contract_at_runtime_root__mutmut_5(
    step: Mapping[str, Any],
    *,
    contract_keys: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
) -> bool:
    """Whether the autonomous action reads a configured contract from runtime scope."""
    if not contract_keys or not runtime_contract_roots:
        return True
    with_value = None
    if not isinstance(with_value, Mapping):
        return False
    for key in contract_keys:
        contract_path = with_value.get(key)
        if isinstance(contract_path, str) and _is_at_runtime_root(contract_path, runtime_contract_roots):
            return True
    return False


def x__has_contract_at_runtime_root__mutmut_6(
    step: Mapping[str, Any],
    *,
    contract_keys: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
) -> bool:
    """Whether the autonomous action reads a configured contract from runtime scope."""
    if not contract_keys or not runtime_contract_roots:
        return True
    with_value = step.get(None)
    if not isinstance(with_value, Mapping):
        return False
    for key in contract_keys:
        contract_path = with_value.get(key)
        if isinstance(contract_path, str) and _is_at_runtime_root(contract_path, runtime_contract_roots):
            return True
    return False


def x__has_contract_at_runtime_root__mutmut_7(
    step: Mapping[str, Any],
    *,
    contract_keys: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
) -> bool:
    """Whether the autonomous action reads a configured contract from runtime scope."""
    if not contract_keys or not runtime_contract_roots:
        return True
    with_value = step.get("XXwithXX")
    if not isinstance(with_value, Mapping):
        return False
    for key in contract_keys:
        contract_path = with_value.get(key)
        if isinstance(contract_path, str) and _is_at_runtime_root(contract_path, runtime_contract_roots):
            return True
    return False


def x__has_contract_at_runtime_root__mutmut_8(
    step: Mapping[str, Any],
    *,
    contract_keys: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
) -> bool:
    """Whether the autonomous action reads a configured contract from runtime scope."""
    if not contract_keys or not runtime_contract_roots:
        return True
    with_value = step.get("WITH")
    if not isinstance(with_value, Mapping):
        return False
    for key in contract_keys:
        contract_path = with_value.get(key)
        if isinstance(contract_path, str) and _is_at_runtime_root(contract_path, runtime_contract_roots):
            return True
    return False


def x__has_contract_at_runtime_root__mutmut_9(
    step: Mapping[str, Any],
    *,
    contract_keys: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
) -> bool:
    """Whether the autonomous action reads a configured contract from runtime scope."""
    if not contract_keys or not runtime_contract_roots:
        return True
    with_value = step.get("with")
    if isinstance(with_value, Mapping):
        return False
    for key in contract_keys:
        contract_path = with_value.get(key)
        if isinstance(contract_path, str) and _is_at_runtime_root(contract_path, runtime_contract_roots):
            return True
    return False


def x__has_contract_at_runtime_root__mutmut_10(
    step: Mapping[str, Any],
    *,
    contract_keys: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
) -> bool:
    """Whether the autonomous action reads a configured contract from runtime scope."""
    if not contract_keys or not runtime_contract_roots:
        return True
    with_value = step.get("with")
    if not isinstance(with_value, Mapping):
        return True
    for key in contract_keys:
        contract_path = with_value.get(key)
        if isinstance(contract_path, str) and _is_at_runtime_root(contract_path, runtime_contract_roots):
            return True
    return False


def x__has_contract_at_runtime_root__mutmut_11(
    step: Mapping[str, Any],
    *,
    contract_keys: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
) -> bool:
    """Whether the autonomous action reads a configured contract from runtime scope."""
    if not contract_keys or not runtime_contract_roots:
        return True
    with_value = step.get("with")
    if not isinstance(with_value, Mapping):
        return False
    for key in contract_keys:
        contract_path = None
        if isinstance(contract_path, str) and _is_at_runtime_root(contract_path, runtime_contract_roots):
            return True
    return False


def x__has_contract_at_runtime_root__mutmut_12(
    step: Mapping[str, Any],
    *,
    contract_keys: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
) -> bool:
    """Whether the autonomous action reads a configured contract from runtime scope."""
    if not contract_keys or not runtime_contract_roots:
        return True
    with_value = step.get("with")
    if not isinstance(with_value, Mapping):
        return False
    for key in contract_keys:
        contract_path = with_value.get(None)
        if isinstance(contract_path, str) and _is_at_runtime_root(contract_path, runtime_contract_roots):
            return True
    return False


def x__has_contract_at_runtime_root__mutmut_13(
    step: Mapping[str, Any],
    *,
    contract_keys: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
) -> bool:
    """Whether the autonomous action reads a configured contract from runtime scope."""
    if not contract_keys or not runtime_contract_roots:
        return True
    with_value = step.get("with")
    if not isinstance(with_value, Mapping):
        return False
    for key in contract_keys:
        contract_path = with_value.get(key)
        if isinstance(contract_path, str) or _is_at_runtime_root(contract_path, runtime_contract_roots):
            return True
    return False


def x__has_contract_at_runtime_root__mutmut_14(
    step: Mapping[str, Any],
    *,
    contract_keys: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
) -> bool:
    """Whether the autonomous action reads a configured contract from runtime scope."""
    if not contract_keys or not runtime_contract_roots:
        return True
    with_value = step.get("with")
    if not isinstance(with_value, Mapping):
        return False
    for key in contract_keys:
        contract_path = with_value.get(key)
        if isinstance(contract_path, str) and _is_at_runtime_root(None, runtime_contract_roots):
            return True
    return False


def x__has_contract_at_runtime_root__mutmut_15(
    step: Mapping[str, Any],
    *,
    contract_keys: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
) -> bool:
    """Whether the autonomous action reads a configured contract from runtime scope."""
    if not contract_keys or not runtime_contract_roots:
        return True
    with_value = step.get("with")
    if not isinstance(with_value, Mapping):
        return False
    for key in contract_keys:
        contract_path = with_value.get(key)
        if isinstance(contract_path, str) and _is_at_runtime_root(contract_path, None):
            return True
    return False


def x__has_contract_at_runtime_root__mutmut_16(
    step: Mapping[str, Any],
    *,
    contract_keys: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
) -> bool:
    """Whether the autonomous action reads a configured contract from runtime scope."""
    if not contract_keys or not runtime_contract_roots:
        return True
    with_value = step.get("with")
    if not isinstance(with_value, Mapping):
        return False
    for key in contract_keys:
        contract_path = with_value.get(key)
        if isinstance(contract_path, str) and _is_at_runtime_root(runtime_contract_roots):
            return True
    return False


def x__has_contract_at_runtime_root__mutmut_17(
    step: Mapping[str, Any],
    *,
    contract_keys: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
) -> bool:
    """Whether the autonomous action reads a configured contract from runtime scope."""
    if not contract_keys or not runtime_contract_roots:
        return True
    with_value = step.get("with")
    if not isinstance(with_value, Mapping):
        return False
    for key in contract_keys:
        contract_path = with_value.get(key)
        if isinstance(contract_path, str) and _is_at_runtime_root(contract_path, ):
            return True
    return False


def x__has_contract_at_runtime_root__mutmut_18(
    step: Mapping[str, Any],
    *,
    contract_keys: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
) -> bool:
    """Whether the autonomous action reads a configured contract from runtime scope."""
    if not contract_keys or not runtime_contract_roots:
        return True
    with_value = step.get("with")
    if not isinstance(with_value, Mapping):
        return False
    for key in contract_keys:
        contract_path = with_value.get(key)
        if isinstance(contract_path, str) and _is_at_runtime_root(contract_path, runtime_contract_roots):
            return False
    return False


def x__has_contract_at_runtime_root__mutmut_19(
    step: Mapping[str, Any],
    *,
    contract_keys: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
) -> bool:
    """Whether the autonomous action reads a configured contract from runtime scope."""
    if not contract_keys or not runtime_contract_roots:
        return True
    with_value = step.get("with")
    if not isinstance(with_value, Mapping):
        return False
    for key in contract_keys:
        contract_path = with_value.get(key)
        if isinstance(contract_path, str) and _is_at_runtime_root(contract_path, runtime_contract_roots):
            return True
    return True

mutants_x__has_contract_at_runtime_root__mutmut['_mutmut_orig'] = x__has_contract_at_runtime_root__mutmut_orig # type: ignore # mutmut generated
mutants_x__has_contract_at_runtime_root__mutmut['x__has_contract_at_runtime_root__mutmut_1'] = x__has_contract_at_runtime_root__mutmut_1 # type: ignore # mutmut generated
mutants_x__has_contract_at_runtime_root__mutmut['x__has_contract_at_runtime_root__mutmut_2'] = x__has_contract_at_runtime_root__mutmut_2 # type: ignore # mutmut generated
mutants_x__has_contract_at_runtime_root__mutmut['x__has_contract_at_runtime_root__mutmut_3'] = x__has_contract_at_runtime_root__mutmut_3 # type: ignore # mutmut generated
mutants_x__has_contract_at_runtime_root__mutmut['x__has_contract_at_runtime_root__mutmut_4'] = x__has_contract_at_runtime_root__mutmut_4 # type: ignore # mutmut generated
mutants_x__has_contract_at_runtime_root__mutmut['x__has_contract_at_runtime_root__mutmut_5'] = x__has_contract_at_runtime_root__mutmut_5 # type: ignore # mutmut generated
mutants_x__has_contract_at_runtime_root__mutmut['x__has_contract_at_runtime_root__mutmut_6'] = x__has_contract_at_runtime_root__mutmut_6 # type: ignore # mutmut generated
mutants_x__has_contract_at_runtime_root__mutmut['x__has_contract_at_runtime_root__mutmut_7'] = x__has_contract_at_runtime_root__mutmut_7 # type: ignore # mutmut generated
mutants_x__has_contract_at_runtime_root__mutmut['x__has_contract_at_runtime_root__mutmut_8'] = x__has_contract_at_runtime_root__mutmut_8 # type: ignore # mutmut generated
mutants_x__has_contract_at_runtime_root__mutmut['x__has_contract_at_runtime_root__mutmut_9'] = x__has_contract_at_runtime_root__mutmut_9 # type: ignore # mutmut generated
mutants_x__has_contract_at_runtime_root__mutmut['x__has_contract_at_runtime_root__mutmut_10'] = x__has_contract_at_runtime_root__mutmut_10 # type: ignore # mutmut generated
mutants_x__has_contract_at_runtime_root__mutmut['x__has_contract_at_runtime_root__mutmut_11'] = x__has_contract_at_runtime_root__mutmut_11 # type: ignore # mutmut generated
mutants_x__has_contract_at_runtime_root__mutmut['x__has_contract_at_runtime_root__mutmut_12'] = x__has_contract_at_runtime_root__mutmut_12 # type: ignore # mutmut generated
mutants_x__has_contract_at_runtime_root__mutmut['x__has_contract_at_runtime_root__mutmut_13'] = x__has_contract_at_runtime_root__mutmut_13 # type: ignore # mutmut generated
mutants_x__has_contract_at_runtime_root__mutmut['x__has_contract_at_runtime_root__mutmut_14'] = x__has_contract_at_runtime_root__mutmut_14 # type: ignore # mutmut generated
mutants_x__has_contract_at_runtime_root__mutmut['x__has_contract_at_runtime_root__mutmut_15'] = x__has_contract_at_runtime_root__mutmut_15 # type: ignore # mutmut generated
mutants_x__has_contract_at_runtime_root__mutmut['x__has_contract_at_runtime_root__mutmut_16'] = x__has_contract_at_runtime_root__mutmut_16 # type: ignore # mutmut generated
mutants_x__has_contract_at_runtime_root__mutmut['x__has_contract_at_runtime_root__mutmut_17'] = x__has_contract_at_runtime_root__mutmut_17 # type: ignore # mutmut generated
mutants_x__has_contract_at_runtime_root__mutmut['x__has_contract_at_runtime_root__mutmut_18'] = x__has_contract_at_runtime_root__mutmut_18 # type: ignore # mutmut generated
mutants_x__has_contract_at_runtime_root__mutmut['x__has_contract_at_runtime_root__mutmut_19'] = x__has_contract_at_runtime_root__mutmut_19 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut)
def workflow_has_untrusted_automation_boundary_violation(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_orig(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_1(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = None
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_2(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(None)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_3(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is not None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_4(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return False
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_5(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = None
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_6(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get(None)
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_7(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("XXjobsXX")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_8(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("JOBS")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_9(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_10(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return False
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_11(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = None
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_12(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get(None)
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_13(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("XXpermissionsXX")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_14(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("PERMISSIONS")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_15(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = None
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_16(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get(None)
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_17(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("XXenvXX")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_18(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("ENV")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_19(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_20(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return False
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_21(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = None
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_22(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get(None)
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_23(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("XXstepsXX")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_24(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("STEPS")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_25(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) and isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_26(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_27(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return False
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_28(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(None):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_29(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_30(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return False
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_31(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = None
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_32(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(None, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_33(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, None)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_34(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_35(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, )]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_36(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_37(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            break
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_38(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(None, privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_39(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), None):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_40(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_41(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), ):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_42(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get(None, workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_43(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", None), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_44(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get(workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_45(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", ), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_46(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("XXpermissionsXX", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_47(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("PERMISSIONS", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_48(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return False
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_49(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) and _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_50(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(None, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_51(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, None) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_52(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_53(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, ) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_54(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            None, credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_55(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), None
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_56(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_57(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_58(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get(None), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_59(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("XXenvXX"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_60(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("ENV"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_61(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return False
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_62(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(None, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_63(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, None):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_64(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_65(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, ):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_66(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return False
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_67(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(None, credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_68(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), None):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_69(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_70(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), ):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_71(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get(None), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_72(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("XXenvXX"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_73(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("ENV"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_74(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return False
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_75(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = None
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_76(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get(None)
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_77(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("XXrunXX")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_78(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("RUN")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_79(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) or any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_80(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                None
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_81(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(None) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_82(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                "XX XX".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_83(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) not in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_84(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(None) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_85(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in "XX XX".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_86(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return False
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_87(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            None
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_88(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_89(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                None,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_90(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=None,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_91(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=None,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_92(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_93(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_94(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_95(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return False
    return False


def x_workflow_has_untrusted_automation_boundary_violation__mutmut_96(
    path: Path,
    *,
    untrusted_action_prefixes: tuple[str, ...],
    privileged_action_prefixes: tuple[str, ...],
    privileged_permissions: tuple[str, ...],
    credential_env_names: tuple[str, ...],
    credential_command_markers: tuple[str, ...],
    runtime_contract_roots: tuple[str, ...],
    contract_keys: tuple[str, ...],
) -> bool:
    """True when configured autonomous work crosses a credential boundary.

    Invalid YAML is a violation for an explicitly configured workflow: silently
    skipping it would create a false-green local gate.
    """
    workflow = _load_workflow(path)
    if workflow is None:
        return True
    jobs = workflow.get("jobs")
    if not isinstance(jobs, Mapping):
        return True
    workflow_permissions = workflow.get("permissions")
    workflow_env = workflow.get("env")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            return True
        steps = job.get("steps")
        if not isinstance(steps, Sequence) or isinstance(steps, str | bytes):
            return True
        if any(not isinstance(step, Mapping) for step in steps):
            return True
        untrusted_steps = [step for step in steps if _step_uses(step, untrusted_action_prefixes)]
        if not untrusted_steps:
            continue
        if _has_privileged_permission(job.get("permissions", workflow_permissions), privileged_permissions):
            return True
        if _mapping_has_credential_env(workflow_env, credential_env_names) or _mapping_has_credential_env(
            job.get("env"), credential_env_names
        ):
            return True
        for step in steps:
            if _step_uses(step, privileged_action_prefixes):
                return True
            if _mapping_has_credential_env(step.get("env"), credential_env_names):
                return True
            run = step.get("run")
            if isinstance(run, str) and any(
                " ".join(marker.split()) in " ".join(run.split()) for marker in credential_command_markers
            ):
                return True
        if any(
            not _has_contract_at_runtime_root(
                step,
                contract_keys=contract_keys,
                runtime_contract_roots=runtime_contract_roots,
            )
            for step in untrusted_steps
            if isinstance(step, Mapping)
        ):
            return True
    return True

mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['_mutmut_orig'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_orig # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_1'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_1 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_2'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_2 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_3'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_3 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_4'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_4 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_5'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_5 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_6'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_6 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_7'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_7 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_8'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_8 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_9'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_9 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_10'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_10 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_11'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_11 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_12'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_12 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_13'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_13 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_14'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_14 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_15'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_15 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_16'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_16 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_17'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_17 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_18'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_18 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_19'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_19 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_20'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_20 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_21'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_21 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_22'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_22 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_23'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_23 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_24'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_24 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_25'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_25 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_26'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_26 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_27'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_27 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_28'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_28 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_29'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_29 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_30'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_30 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_31'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_31 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_32'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_32 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_33'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_33 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_34'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_34 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_35'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_35 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_36'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_36 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_37'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_37 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_38'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_38 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_39'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_39 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_40'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_40 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_41'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_41 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_42'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_42 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_43'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_43 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_44'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_44 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_45'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_45 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_46'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_46 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_47'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_47 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_48'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_48 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_49'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_49 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_50'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_50 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_51'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_51 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_52'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_52 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_53'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_53 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_54'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_54 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_55'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_55 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_56'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_56 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_57'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_57 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_58'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_58 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_59'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_59 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_60'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_60 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_61'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_61 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_62'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_62 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_63'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_63 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_64'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_64 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_65'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_65 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_66'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_66 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_67'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_67 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_68'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_68 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_69'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_69 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_70'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_70 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_71'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_71 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_72'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_72 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_73'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_73 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_74'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_74 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_75'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_75 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_76'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_76 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_77'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_77 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_78'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_78 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_79'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_79 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_80'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_80 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_81'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_81 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_82'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_82 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_83'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_83 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_84'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_84 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_85'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_85 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_86'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_86 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_87'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_87 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_88'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_88 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_89'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_89 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_90'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_90 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_91'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_91 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_92'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_92 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_93'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_93 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_94'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_94 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_95'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_95 # type: ignore # mutmut generated
mutants_x_workflow_has_untrusted_automation_boundary_violation__mutmut['x_workflow_has_untrusted_automation_boundary_violation__mutmut_96'] = x_workflow_has_untrusted_automation_boundary_violation__mutmut_96 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁUntrustedAutomationBoundaryǁenumerate_files__mutmut: MutantDict = {}  # type: ignore
mutants_xǁUntrustedAutomationBoundaryǁis_in_scope__mutmut: MutantDict = {}  # type: ignore
mutants_xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore
mutants_xǁUntrustedAutomationBoundaryǁrun__mutmut: MutantDict = {}  # type: ignore


class UntrustedAutomationBoundary(FitnessRule):
    """Flags an autonomous workflow job that can reach privileged credentials."""

    name = "untrusted-automation-boundary"
    remediation = REMEDIATION
    extensions = (".yml", ".yaml")

    workflows: tuple[str, ...] = ()
    untrusted_action_prefixes: tuple[str, ...] = ()
    privileged_action_prefixes: tuple[str, ...] = ()
    privileged_permissions: tuple[str, ...] = ()
    credential_env_names: tuple[str, ...] = ()
    credential_command_markers: tuple[str, ...] = ()
    runtime_contract_roots: tuple[str, ...] = ()
    contract_keys: tuple[str, ...] = ()

    @classmethod
    @_mutmut_mutated(mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = None
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, )
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = None
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(None)
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get(None))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("XXworkflowsXX"))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("WORKFLOWS"))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = None
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(None)
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_13(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get(None))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_14(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get("XXuntrusted_action_prefixesXX"))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_15(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get("UNTRUSTED_ACTION_PREFIXES"))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_16(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = None
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_17(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(None)
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_18(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get(None))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_19(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get("XXprivileged_action_prefixesXX"))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_20(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get("PRIVILEGED_ACTION_PREFIXES"))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_21(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = None
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_22(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(None)
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_23(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get(None))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_24(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get("XXprivileged_permissionsXX"))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_25(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get("PRIVILEGED_PERMISSIONS"))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_26(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = None
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_27(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(None)
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_28(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get(None))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_29(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get("XXcredential_env_namesXX"))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_30(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get("CREDENTIAL_ENV_NAMES"))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_31(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = None
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_32(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(None)
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_33(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get(None))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_34(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get("XXcredential_command_markersXX"))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_35(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get("CREDENTIAL_COMMAND_MARKERS"))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_36(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = None
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_37(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(None)
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_38(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get(None))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_39(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get("XXruntime_contract_rootsXX"))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_40(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get("RUNTIME_CONTRACT_ROOTS"))
        rule.contract_keys = _as_strings(config.get("contract_keys"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_41(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = None
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_42(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(None)
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_43(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get(None))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_44(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get("XXcontract_keysXX"))
        return rule

    @classmethod
    def xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_45(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> UntrustedAutomationBoundary:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, UntrustedAutomationBoundary)  # noqa: S101  # narrowing for mypy
        rule.workflows = _as_strings(config.get("workflows"))
        rule.untrusted_action_prefixes = _as_strings(config.get("untrusted_action_prefixes"))
        rule.privileged_action_prefixes = _as_strings(config.get("privileged_action_prefixes"))
        rule.privileged_permissions = _as_strings(config.get("privileged_permissions"))
        rule.credential_env_names = _as_strings(config.get("credential_env_names"))
        rule.credential_command_markers = _as_strings(config.get("credential_command_markers"))
        rule.runtime_contract_roots = _as_strings(config.get("runtime_contract_roots"))
        rule.contract_keys = _as_strings(config.get("CONTRACT_KEYS"))
        return rule

    @_mutmut_mutated(mutants_xǁUntrustedAutomationBoundaryǁenumerate_files__mutmut)
    def enumerate_files(self) -> list[Path]:
        """Enumerate every configured workflow so missing files are reported."""
        return [self._repo_root / workflow for workflow in self.workflows]

    def xǁUntrustedAutomationBoundaryǁenumerate_files__mutmut_orig(self) -> list[Path]:
        """Enumerate every configured workflow so missing files are reported."""
        return [self._repo_root / workflow for workflow in self.workflows]

    def xǁUntrustedAutomationBoundaryǁenumerate_files__mutmut_1(self) -> list[Path]:
        """Enumerate every configured workflow so missing files are reported."""
        return [self._repo_root * workflow for workflow in self.workflows]

    @_mutmut_mutated(mutants_xǁUntrustedAutomationBoundaryǁis_in_scope__mutmut)
    def is_in_scope(self, rel: str) -> bool:
        return rel in self.workflows

    def xǁUntrustedAutomationBoundaryǁis_in_scope__mutmut_orig(self, rel: str) -> bool:
        return rel in self.workflows

    def xǁUntrustedAutomationBoundaryǁis_in_scope__mutmut_1(self, rel: str) -> bool:
        return rel not in self.workflows

    @_mutmut_mutated(mutants_xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        return workflow_has_untrusted_automation_boundary_violation(
            path,
            untrusted_action_prefixes=self.untrusted_action_prefixes,
            privileged_action_prefixes=self.privileged_action_prefixes,
            privileged_permissions=self.privileged_permissions,
            credential_env_names=self.credential_env_names,
            credential_command_markers=self.credential_command_markers,
            runtime_contract_roots=self.runtime_contract_roots,
            contract_keys=self.contract_keys,
        )

    def xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        return workflow_has_untrusted_automation_boundary_violation(
            path,
            untrusted_action_prefixes=self.untrusted_action_prefixes,
            privileged_action_prefixes=self.privileged_action_prefixes,
            privileged_permissions=self.privileged_permissions,
            credential_env_names=self.credential_env_names,
            credential_command_markers=self.credential_command_markers,
            runtime_contract_roots=self.runtime_contract_roots,
            contract_keys=self.contract_keys,
        )

    def xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        return workflow_has_untrusted_automation_boundary_violation(
            None,
            untrusted_action_prefixes=self.untrusted_action_prefixes,
            privileged_action_prefixes=self.privileged_action_prefixes,
            privileged_permissions=self.privileged_permissions,
            credential_env_names=self.credential_env_names,
            credential_command_markers=self.credential_command_markers,
            runtime_contract_roots=self.runtime_contract_roots,
            contract_keys=self.contract_keys,
        )

    def xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_2(self, path: Path) -> bool:
        return workflow_has_untrusted_automation_boundary_violation(
            path,
            untrusted_action_prefixes=None,
            privileged_action_prefixes=self.privileged_action_prefixes,
            privileged_permissions=self.privileged_permissions,
            credential_env_names=self.credential_env_names,
            credential_command_markers=self.credential_command_markers,
            runtime_contract_roots=self.runtime_contract_roots,
            contract_keys=self.contract_keys,
        )

    def xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_3(self, path: Path) -> bool:
        return workflow_has_untrusted_automation_boundary_violation(
            path,
            untrusted_action_prefixes=self.untrusted_action_prefixes,
            privileged_action_prefixes=None,
            privileged_permissions=self.privileged_permissions,
            credential_env_names=self.credential_env_names,
            credential_command_markers=self.credential_command_markers,
            runtime_contract_roots=self.runtime_contract_roots,
            contract_keys=self.contract_keys,
        )

    def xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_4(self, path: Path) -> bool:
        return workflow_has_untrusted_automation_boundary_violation(
            path,
            untrusted_action_prefixes=self.untrusted_action_prefixes,
            privileged_action_prefixes=self.privileged_action_prefixes,
            privileged_permissions=None,
            credential_env_names=self.credential_env_names,
            credential_command_markers=self.credential_command_markers,
            runtime_contract_roots=self.runtime_contract_roots,
            contract_keys=self.contract_keys,
        )

    def xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_5(self, path: Path) -> bool:
        return workflow_has_untrusted_automation_boundary_violation(
            path,
            untrusted_action_prefixes=self.untrusted_action_prefixes,
            privileged_action_prefixes=self.privileged_action_prefixes,
            privileged_permissions=self.privileged_permissions,
            credential_env_names=None,
            credential_command_markers=self.credential_command_markers,
            runtime_contract_roots=self.runtime_contract_roots,
            contract_keys=self.contract_keys,
        )

    def xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_6(self, path: Path) -> bool:
        return workflow_has_untrusted_automation_boundary_violation(
            path,
            untrusted_action_prefixes=self.untrusted_action_prefixes,
            privileged_action_prefixes=self.privileged_action_prefixes,
            privileged_permissions=self.privileged_permissions,
            credential_env_names=self.credential_env_names,
            credential_command_markers=None,
            runtime_contract_roots=self.runtime_contract_roots,
            contract_keys=self.contract_keys,
        )

    def xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_7(self, path: Path) -> bool:
        return workflow_has_untrusted_automation_boundary_violation(
            path,
            untrusted_action_prefixes=self.untrusted_action_prefixes,
            privileged_action_prefixes=self.privileged_action_prefixes,
            privileged_permissions=self.privileged_permissions,
            credential_env_names=self.credential_env_names,
            credential_command_markers=self.credential_command_markers,
            runtime_contract_roots=None,
            contract_keys=self.contract_keys,
        )

    def xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_8(self, path: Path) -> bool:
        return workflow_has_untrusted_automation_boundary_violation(
            path,
            untrusted_action_prefixes=self.untrusted_action_prefixes,
            privileged_action_prefixes=self.privileged_action_prefixes,
            privileged_permissions=self.privileged_permissions,
            credential_env_names=self.credential_env_names,
            credential_command_markers=self.credential_command_markers,
            runtime_contract_roots=self.runtime_contract_roots,
            contract_keys=None,
        )

    def xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_9(self, path: Path) -> bool:
        return workflow_has_untrusted_automation_boundary_violation(
            untrusted_action_prefixes=self.untrusted_action_prefixes,
            privileged_action_prefixes=self.privileged_action_prefixes,
            privileged_permissions=self.privileged_permissions,
            credential_env_names=self.credential_env_names,
            credential_command_markers=self.credential_command_markers,
            runtime_contract_roots=self.runtime_contract_roots,
            contract_keys=self.contract_keys,
        )

    def xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_10(self, path: Path) -> bool:
        return workflow_has_untrusted_automation_boundary_violation(
            path,
            privileged_action_prefixes=self.privileged_action_prefixes,
            privileged_permissions=self.privileged_permissions,
            credential_env_names=self.credential_env_names,
            credential_command_markers=self.credential_command_markers,
            runtime_contract_roots=self.runtime_contract_roots,
            contract_keys=self.contract_keys,
        )

    def xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_11(self, path: Path) -> bool:
        return workflow_has_untrusted_automation_boundary_violation(
            path,
            untrusted_action_prefixes=self.untrusted_action_prefixes,
            privileged_permissions=self.privileged_permissions,
            credential_env_names=self.credential_env_names,
            credential_command_markers=self.credential_command_markers,
            runtime_contract_roots=self.runtime_contract_roots,
            contract_keys=self.contract_keys,
        )

    def xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_12(self, path: Path) -> bool:
        return workflow_has_untrusted_automation_boundary_violation(
            path,
            untrusted_action_prefixes=self.untrusted_action_prefixes,
            privileged_action_prefixes=self.privileged_action_prefixes,
            credential_env_names=self.credential_env_names,
            credential_command_markers=self.credential_command_markers,
            runtime_contract_roots=self.runtime_contract_roots,
            contract_keys=self.contract_keys,
        )

    def xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_13(self, path: Path) -> bool:
        return workflow_has_untrusted_automation_boundary_violation(
            path,
            untrusted_action_prefixes=self.untrusted_action_prefixes,
            privileged_action_prefixes=self.privileged_action_prefixes,
            privileged_permissions=self.privileged_permissions,
            credential_command_markers=self.credential_command_markers,
            runtime_contract_roots=self.runtime_contract_roots,
            contract_keys=self.contract_keys,
        )

    def xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_14(self, path: Path) -> bool:
        return workflow_has_untrusted_automation_boundary_violation(
            path,
            untrusted_action_prefixes=self.untrusted_action_prefixes,
            privileged_action_prefixes=self.privileged_action_prefixes,
            privileged_permissions=self.privileged_permissions,
            credential_env_names=self.credential_env_names,
            runtime_contract_roots=self.runtime_contract_roots,
            contract_keys=self.contract_keys,
        )

    def xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_15(self, path: Path) -> bool:
        return workflow_has_untrusted_automation_boundary_violation(
            path,
            untrusted_action_prefixes=self.untrusted_action_prefixes,
            privileged_action_prefixes=self.privileged_action_prefixes,
            privileged_permissions=self.privileged_permissions,
            credential_env_names=self.credential_env_names,
            credential_command_markers=self.credential_command_markers,
            contract_keys=self.contract_keys,
        )

    def xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_16(self, path: Path) -> bool:
        return workflow_has_untrusted_automation_boundary_violation(
            path,
            untrusted_action_prefixes=self.untrusted_action_prefixes,
            privileged_action_prefixes=self.privileged_action_prefixes,
            privileged_permissions=self.privileged_permissions,
            credential_env_names=self.credential_env_names,
            credential_command_markers=self.credential_command_markers,
            runtime_contract_roots=self.runtime_contract_roots,
            )

    @_mutmut_mutated(mutants_xǁUntrustedAutomationBoundaryǁrun__mutmut)
    def run(self) -> int:
        """Evaluate every configured workflow's current credential boundary."""
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — autonomous workflows are isolated from credentials.")
            return 0
        print(f"FAIL [arch:{self._name}] — autonomous workflow crosses a credential boundary:")
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(path).as_posix(),
                "autonomous workflow crosses a credential boundary",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁUntrustedAutomationBoundaryǁrun__mutmut_orig(self) -> int:
        """Evaluate every configured workflow's current credential boundary."""
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — autonomous workflows are isolated from credentials.")
            return 0
        print(f"FAIL [arch:{self._name}] — autonomous workflow crosses a credential boundary:")
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(path).as_posix(),
                "autonomous workflow crosses a credential boundary",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁUntrustedAutomationBoundaryǁrun__mutmut_1(self) -> int:
        """Evaluate every configured workflow's current credential boundary."""
        violations = None
        if not violations:
            print(f"ok [arch:{self._name}] — autonomous workflows are isolated from credentials.")
            return 0
        print(f"FAIL [arch:{self._name}] — autonomous workflow crosses a credential boundary:")
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(path).as_posix(),
                "autonomous workflow crosses a credential boundary",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁUntrustedAutomationBoundaryǁrun__mutmut_2(self) -> int:
        """Evaluate every configured workflow's current credential boundary."""
        violations = sorted(None, key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — autonomous workflows are isolated from credentials.")
            return 0
        print(f"FAIL [arch:{self._name}] — autonomous workflow crosses a credential boundary:")
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(path).as_posix(),
                "autonomous workflow crosses a credential boundary",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁUntrustedAutomationBoundaryǁrun__mutmut_3(self) -> int:
        """Evaluate every configured workflow's current credential boundary."""
        violations = sorted(self.collect_violations(), key=None)
        if not violations:
            print(f"ok [arch:{self._name}] — autonomous workflows are isolated from credentials.")
            return 0
        print(f"FAIL [arch:{self._name}] — autonomous workflow crosses a credential boundary:")
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(path).as_posix(),
                "autonomous workflow crosses a credential boundary",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁUntrustedAutomationBoundaryǁrun__mutmut_4(self) -> int:
        """Evaluate every configured workflow's current credential boundary."""
        violations = sorted(key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — autonomous workflows are isolated from credentials.")
            return 0
        print(f"FAIL [arch:{self._name}] — autonomous workflow crosses a credential boundary:")
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(path).as_posix(),
                "autonomous workflow crosses a credential boundary",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁUntrustedAutomationBoundaryǁrun__mutmut_5(self) -> int:
        """Evaluate every configured workflow's current credential boundary."""
        violations = sorted(self.collect_violations(), )
        if not violations:
            print(f"ok [arch:{self._name}] — autonomous workflows are isolated from credentials.")
            return 0
        print(f"FAIL [arch:{self._name}] — autonomous workflow crosses a credential boundary:")
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(path).as_posix(),
                "autonomous workflow crosses a credential boundary",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁUntrustedAutomationBoundaryǁrun__mutmut_6(self) -> int:
        """Evaluate every configured workflow's current credential boundary."""
        violations = sorted(self.collect_violations(), key=lambda path: None)
        if not violations:
            print(f"ok [arch:{self._name}] — autonomous workflows are isolated from credentials.")
            return 0
        print(f"FAIL [arch:{self._name}] — autonomous workflow crosses a credential boundary:")
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(path).as_posix(),
                "autonomous workflow crosses a credential boundary",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁUntrustedAutomationBoundaryǁrun__mutmut_7(self) -> int:
        """Evaluate every configured workflow's current credential boundary."""
        violations = sorted(self.collect_violations(), key=lambda path: str(None))
        if not violations:
            print(f"ok [arch:{self._name}] — autonomous workflows are isolated from credentials.")
            return 0
        print(f"FAIL [arch:{self._name}] — autonomous workflow crosses a credential boundary:")
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(path).as_posix(),
                "autonomous workflow crosses a credential boundary",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁUntrustedAutomationBoundaryǁrun__mutmut_8(self) -> int:
        """Evaluate every configured workflow's current credential boundary."""
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if violations:
            print(f"ok [arch:{self._name}] — autonomous workflows are isolated from credentials.")
            return 0
        print(f"FAIL [arch:{self._name}] — autonomous workflow crosses a credential boundary:")
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(path).as_posix(),
                "autonomous workflow crosses a credential boundary",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁUntrustedAutomationBoundaryǁrun__mutmut_9(self) -> int:
        """Evaluate every configured workflow's current credential boundary."""
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(None)
            return 0
        print(f"FAIL [arch:{self._name}] — autonomous workflow crosses a credential boundary:")
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(path).as_posix(),
                "autonomous workflow crosses a credential boundary",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁUntrustedAutomationBoundaryǁrun__mutmut_10(self) -> int:
        """Evaluate every configured workflow's current credential boundary."""
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — autonomous workflows are isolated from credentials.")
            return 1
        print(f"FAIL [arch:{self._name}] — autonomous workflow crosses a credential boundary:")
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(path).as_posix(),
                "autonomous workflow crosses a credential boundary",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁUntrustedAutomationBoundaryǁrun__mutmut_11(self) -> int:
        """Evaluate every configured workflow's current credential boundary."""
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — autonomous workflows are isolated from credentials.")
            return 0
        print(None)
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(path).as_posix(),
                "autonomous workflow crosses a credential boundary",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁUntrustedAutomationBoundaryǁrun__mutmut_12(self) -> int:
        """Evaluate every configured workflow's current credential boundary."""
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — autonomous workflows are isolated from credentials.")
            return 0
        print(f"FAIL [arch:{self._name}] — autonomous workflow crosses a credential boundary:")
        for path in violations:
            report_finding(
                None,
                self._repo_relative(path).as_posix(),
                "autonomous workflow crosses a credential boundary",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁUntrustedAutomationBoundaryǁrun__mutmut_13(self) -> int:
        """Evaluate every configured workflow's current credential boundary."""
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — autonomous workflows are isolated from credentials.")
            return 0
        print(f"FAIL [arch:{self._name}] — autonomous workflow crosses a credential boundary:")
        for path in violations:
            report_finding(
                self.name,
                None,
                "autonomous workflow crosses a credential boundary",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁUntrustedAutomationBoundaryǁrun__mutmut_14(self) -> int:
        """Evaluate every configured workflow's current credential boundary."""
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — autonomous workflows are isolated from credentials.")
            return 0
        print(f"FAIL [arch:{self._name}] — autonomous workflow crosses a credential boundary:")
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(path).as_posix(),
                None,
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁUntrustedAutomationBoundaryǁrun__mutmut_15(self) -> int:
        """Evaluate every configured workflow's current credential boundary."""
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — autonomous workflows are isolated from credentials.")
            return 0
        print(f"FAIL [arch:{self._name}] — autonomous workflow crosses a credential boundary:")
        for path in violations:
            report_finding(
                self._repo_relative(path).as_posix(),
                "autonomous workflow crosses a credential boundary",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁUntrustedAutomationBoundaryǁrun__mutmut_16(self) -> int:
        """Evaluate every configured workflow's current credential boundary."""
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — autonomous workflows are isolated from credentials.")
            return 0
        print(f"FAIL [arch:{self._name}] — autonomous workflow crosses a credential boundary:")
        for path in violations:
            report_finding(
                self.name,
                "autonomous workflow crosses a credential boundary",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁUntrustedAutomationBoundaryǁrun__mutmut_17(self) -> int:
        """Evaluate every configured workflow's current credential boundary."""
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — autonomous workflows are isolated from credentials.")
            return 0
        print(f"FAIL [arch:{self._name}] — autonomous workflow crosses a credential boundary:")
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(path).as_posix(),
                )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁUntrustedAutomationBoundaryǁrun__mutmut_18(self) -> int:
        """Evaluate every configured workflow's current credential boundary."""
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — autonomous workflows are isolated from credentials.")
            return 0
        print(f"FAIL [arch:{self._name}] — autonomous workflow crosses a credential boundary:")
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(None).as_posix(),
                "autonomous workflow crosses a credential boundary",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁUntrustedAutomationBoundaryǁrun__mutmut_19(self) -> int:
        """Evaluate every configured workflow's current credential boundary."""
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — autonomous workflows are isolated from credentials.")
            return 0
        print(f"FAIL [arch:{self._name}] — autonomous workflow crosses a credential boundary:")
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(path).as_posix(),
                "XXautonomous workflow crosses a credential boundaryXX",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁUntrustedAutomationBoundaryǁrun__mutmut_20(self) -> int:
        """Evaluate every configured workflow's current credential boundary."""
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — autonomous workflows are isolated from credentials.")
            return 0
        print(f"FAIL [arch:{self._name}] — autonomous workflow crosses a credential boundary:")
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(path).as_posix(),
                "AUTONOMOUS WORKFLOW CROSSES A CREDENTIAL BOUNDARY",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 1

    def xǁUntrustedAutomationBoundaryǁrun__mutmut_21(self) -> int:
        """Evaluate every configured workflow's current credential boundary."""
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — autonomous workflows are isolated from credentials.")
            return 0
        print(f"FAIL [arch:{self._name}] — autonomous workflow crosses a credential boundary:")
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(path).as_posix(),
                "autonomous workflow crosses a credential boundary",
            )
            print(None)
        print()
        print(self.remediation)
        return 1

    def xǁUntrustedAutomationBoundaryǁrun__mutmut_22(self) -> int:
        """Evaluate every configured workflow's current credential boundary."""
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — autonomous workflows are isolated from credentials.")
            return 0
        print(f"FAIL [arch:{self._name}] — autonomous workflow crosses a credential boundary:")
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(path).as_posix(),
                "autonomous workflow crosses a credential boundary",
            )
            print(f"  {path}")
        print()
        print(None)
        return 1

    def xǁUntrustedAutomationBoundaryǁrun__mutmut_23(self) -> int:
        """Evaluate every configured workflow's current credential boundary."""
        violations = sorted(self.collect_violations(), key=lambda path: str(path))
        if not violations:
            print(f"ok [arch:{self._name}] — autonomous workflows are isolated from credentials.")
            return 0
        print(f"FAIL [arch:{self._name}] — autonomous workflow crosses a credential boundary:")
        for path in violations:
            report_finding(
                self.name,
                self._repo_relative(path).as_posix(),
                "autonomous workflow crosses a credential boundary",
            )
            print(f"  {path}")
        print()
        print(self.remediation)
        return 2

mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['_mutmut_orig'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_1'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_2'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_3'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_4'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_5'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_6'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_7'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_8'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_9'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_10'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_11'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_12'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_12 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_13'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_13 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_14'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_14 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_15'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_15 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_16'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_16 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_17'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_17 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_18'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_18 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_19'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_19 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_20'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_20 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_21'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_21 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_22'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_22 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_23'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_23 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_24'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_24 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_25'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_25 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_26'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_26 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_27'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_27 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_28'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_28 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_29'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_29 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_30'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_30 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_31'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_31 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_32'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_32 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_33'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_33 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_34'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_34 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_35'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_35 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_36'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_36 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_37'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_37 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_38'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_38 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_39'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_39 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_40'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_40 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_41'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_41 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_42'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_42 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_43'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_43 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_44'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_44 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfrom_config__mutmut['xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_45'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfrom_config__mutmut_45 # type: ignore # mutmut generated

mutants_xǁUntrustedAutomationBoundaryǁenumerate_files__mutmut['_mutmut_orig'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁenumerate_files__mutmut_orig # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁenumerate_files__mutmut['xǁUntrustedAutomationBoundaryǁenumerate_files__mutmut_1'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁenumerate_files__mutmut_1 # type: ignore # mutmut generated

mutants_xǁUntrustedAutomationBoundaryǁis_in_scope__mutmut['_mutmut_orig'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁis_in_scope__mutmut_orig # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁis_in_scope__mutmut['xǁUntrustedAutomationBoundaryǁis_in_scope__mutmut_1'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁis_in_scope__mutmut_1 # type: ignore # mutmut generated

mutants_xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut['_mutmut_orig'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut['xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_1'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut['xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_2'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_2 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut['xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_3'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_3 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut['xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_4'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_4 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut['xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_5'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_5 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut['xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_6'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_6 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut['xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_7'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_7 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut['xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_8'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_8 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut['xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_9'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_9 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut['xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_10'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_10 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut['xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_11'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_11 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut['xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_12'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_12 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut['xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_13'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_13 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut['xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_14'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_14 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut['xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_15'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_15 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut['xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_16'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁfile_has_violation__mutmut_16 # type: ignore # mutmut generated

mutants_xǁUntrustedAutomationBoundaryǁrun__mutmut['_mutmut_orig'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁrun__mutmut_orig # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁrun__mutmut['xǁUntrustedAutomationBoundaryǁrun__mutmut_1'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁrun__mutmut_1 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁrun__mutmut['xǁUntrustedAutomationBoundaryǁrun__mutmut_2'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁrun__mutmut_2 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁrun__mutmut['xǁUntrustedAutomationBoundaryǁrun__mutmut_3'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁrun__mutmut_3 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁrun__mutmut['xǁUntrustedAutomationBoundaryǁrun__mutmut_4'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁrun__mutmut_4 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁrun__mutmut['xǁUntrustedAutomationBoundaryǁrun__mutmut_5'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁrun__mutmut_5 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁrun__mutmut['xǁUntrustedAutomationBoundaryǁrun__mutmut_6'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁrun__mutmut_6 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁrun__mutmut['xǁUntrustedAutomationBoundaryǁrun__mutmut_7'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁrun__mutmut_7 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁrun__mutmut['xǁUntrustedAutomationBoundaryǁrun__mutmut_8'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁrun__mutmut_8 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁrun__mutmut['xǁUntrustedAutomationBoundaryǁrun__mutmut_9'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁrun__mutmut_9 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁrun__mutmut['xǁUntrustedAutomationBoundaryǁrun__mutmut_10'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁrun__mutmut_10 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁrun__mutmut['xǁUntrustedAutomationBoundaryǁrun__mutmut_11'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁrun__mutmut_11 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁrun__mutmut['xǁUntrustedAutomationBoundaryǁrun__mutmut_12'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁrun__mutmut_12 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁrun__mutmut['xǁUntrustedAutomationBoundaryǁrun__mutmut_13'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁrun__mutmut_13 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁrun__mutmut['xǁUntrustedAutomationBoundaryǁrun__mutmut_14'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁrun__mutmut_14 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁrun__mutmut['xǁUntrustedAutomationBoundaryǁrun__mutmut_15'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁrun__mutmut_15 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁrun__mutmut['xǁUntrustedAutomationBoundaryǁrun__mutmut_16'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁrun__mutmut_16 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁrun__mutmut['xǁUntrustedAutomationBoundaryǁrun__mutmut_17'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁrun__mutmut_17 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁrun__mutmut['xǁUntrustedAutomationBoundaryǁrun__mutmut_18'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁrun__mutmut_18 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁrun__mutmut['xǁUntrustedAutomationBoundaryǁrun__mutmut_19'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁrun__mutmut_19 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁrun__mutmut['xǁUntrustedAutomationBoundaryǁrun__mutmut_20'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁrun__mutmut_20 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁrun__mutmut['xǁUntrustedAutomationBoundaryǁrun__mutmut_21'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁrun__mutmut_21 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁrun__mutmut['xǁUntrustedAutomationBoundaryǁrun__mutmut_22'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁrun__mutmut_22 # type: ignore # mutmut generated
mutants_xǁUntrustedAutomationBoundaryǁrun__mutmut['xǁUntrustedAutomationBoundaryǁrun__mutmut_23'] = UntrustedAutomationBoundary.xǁUntrustedAutomationBoundaryǁrun__mutmut_23 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> UntrustedAutomationBoundary:
    """Factory the engine calls to bind this CORE check to consumer config."""
    return UntrustedAutomationBoundary.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> UntrustedAutomationBoundary:
    """Factory the engine calls to bind this CORE check to consumer config."""
    return UntrustedAutomationBoundary.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> UntrustedAutomationBoundary:
    """Factory the engine calls to bind this CORE check to consumer config."""
    return UntrustedAutomationBoundary.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> UntrustedAutomationBoundary:
    """Factory the engine calls to bind this CORE check to consumer config."""
    return UntrustedAutomationBoundary.from_config(config, repo_root=None)


def x_build__mutmut_3(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> UntrustedAutomationBoundary:
    """Factory the engine calls to bind this CORE check to consumer config."""
    return UntrustedAutomationBoundary.from_config(repo_root=repo_root)


def x_build__mutmut_4(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> UntrustedAutomationBoundary:
    """Factory the engine calls to bind this CORE check to consumer config."""
    return UntrustedAutomationBoundary.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(UntrustedAutomationBoundary, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(UntrustedAutomationBoundary, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(UntrustedAutomationBoundary, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(UntrustedAutomationBoundary, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
