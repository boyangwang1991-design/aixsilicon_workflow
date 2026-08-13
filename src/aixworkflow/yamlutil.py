"""Safe YAML load/dump helpers.

We never load arbitrary objects from YAML (no unsafe `!!python` tags).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from aixworkflow.errors import InfraError


class _SafeLoader(yaml.SafeLoader):
    """SafeLoader that also accepts merge keys (already default in PyYAML)."""


def load_yaml(path: Path) -> dict[str, Any]:
    """Load a YAML file as plain data (dict)."""
    try:
        with path.open("r", encoding="utf-8") as fh:
            data = yaml.load(fh, Loader=_SafeLoader)
    except yaml.YAMLError as exc:  # pragma: no cover - trivial passthrough
        raise InfraError(f"invalid YAML in {path}: {exc}") from exc
    except OSError as exc:
        raise InfraError(f"cannot read {path}: {exc}") from exc
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise InfraError(f"{path}: top-level YAML must be a mapping")
    return data


def load_yaml_str(text: str) -> dict[str, Any]:
    """Load YAML from a string (used for fixtures and tests)."""
    data = yaml.safe_load(text)
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise InfraError("top-level YAML must be a mapping")
    return data


def dump_yaml(data: Any) -> str:
    """Serialize data to canonical YAML."""
    return yaml.safe_dump(
        data,
        sort_keys=False,
        default_flow_style=False,
        allow_unicode=True,
        width=100,
    )


def write_yaml(path: Path, data: Any) -> None:
    """Write data as YAML to a file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump_yaml(data), encoding="utf-8")


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge `override` into `base` (override wins on conflicts).

    Dictionaries are merged recursively; lists and scalars are replaced.
    """
    result = dict(base)
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result
