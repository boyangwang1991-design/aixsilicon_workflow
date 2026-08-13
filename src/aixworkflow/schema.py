"""JSON Schema validation wrapper for all aix schemas."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema

from aixworkflow.errors import ManifestError

# Map logical schema names to packaged schema filenames.
_SCHEMA_FILES: dict[str, str] = {
    "manifest": "workspace-manifest.schema.json",
    "lock": "workspace-lock.schema.json",
    "change-bundle": "change-bundle.schema.json",
    "flow": "flow.schema.json",
    "tool-profile": "tool-profile.schema.json",
    "evidence-index": "evidence-index.schema.json",
}


def _load_schema(name: str) -> dict[str, Any]:
    try:
        filename = _SCHEMA_FILES[name]
    except KeyError as exc:
        raise ManifestError(f"unknown schema: {name}") from exc

    # Prefer the repository schemas/ directory when present (dev checkout),
    # otherwise fall back to installed package data.
    candidates = [
        Path("schemas") / filename,
        Path(__file__).resolve().parent / "schemas" / filename,
    ]
    for candidate in candidates:
        if candidate.is_file():
            return json.loads(candidate.read_text(encoding="utf-8"))
    raise ManifestError(f"schema file not found for '{name}'")


def validate(data: dict[str, Any], schema_name: str, *, source: str = "document") -> None:
    """Validate `data` against the named schema, raising ManifestError on failure."""
    schema = _load_schema(schema_name)
    try:
        jsonschema.validate(instance=data, schema=schema)
    except jsonschema.ValidationError as exc:
        where = ".".join(str(p) for p in list(exc.absolute_path)[-4:]) or "<root>"
        raise ManifestError(
            f"{source}: schema '{schema_name}' failed at '{where}': {exc.message}"
        ) from exc
    except jsonschema.SchemaError as exc:
        raise ManifestError(f"{source}: invalid schema '{schema_name}': {exc}") from exc
