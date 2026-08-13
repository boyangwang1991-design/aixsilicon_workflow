"""Lightweight command registry + plugin discovery.

A new builtin command is added with one decorator + one handler function; no
changes to the dispatch logic are required.

Deterministic tools (e.g. `aix tool ...` from `aixsilicon_tool_repo`) register
themselves through the `aixsilicon.commands` entry point group (ADR-0004).
Plugins are loaded lazily by `register_all()`; missing plugins surface as
`OPTIONAL_UNAVAILABLE` at call time, never as silent degradation.
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from typing import Any

CommandHandler = Callable[[Any], None]

_REGISTRY: dict[str, CommandHandler] = {}
_PLUGINS: dict[str, Any] = {}


def command(domain: str, name: str) -> Callable[[CommandHandler], CommandHandler]:
    """Decorator registering a handler for `domain.name` (e.g. `wf.sync`)."""

    def deco(fn: CommandHandler) -> CommandHandler:
        _REGISTRY[f"{domain}.{name}"] = fn
        return fn

    return deco


def get_handler(domain: str, name: str) -> CommandHandler | None:
    return _REGISTRY.get(f"{domain}.{name}")


def get_plugin(name: str) -> Any | None:
    """Return a loaded `aix.commands` plugin callable (or None)."""
    return _PLUGINS.get(name)


def plugins_loaded() -> dict[str, Any]:
    """Snapshot of currently loaded `aix.commands` plugins."""
    return dict(_PLUGINS)


def discover_plugins() -> list[str]:
    """Load all registered `aixsilicon.commands` entry points (ADR-0004).

    Each entry point name is the plugin id (e.g. `tool`); its callable receives
    the raw remaining argv when invoked via `aix <domain> ...`.
    """
    try:
        from importlib.metadata import entry_points
    except ImportError:  # pragma: no cover - py<3.10
        return []
    try:
        eps = entry_points(group="aixsilicon.commands")
    except Exception as exc:  # pragma: no cover - metadata issue
        print(f"warning: cannot enumerate aixsilicon.commands entry points: {exc}", file=sys.stderr)
        return []
    loaded: list[str] = []
    for ep in eps:
        try:
            _PLUGINS[ep.name] = ep.load()
            loaded.append(ep.name)
        except Exception as exc:  # pragma: no cover - plugin failure
            print(
                f"warning: failed to load aix.commands plugin '{ep.name}': {exc}", file=sys.stderr
            )
    return loaded


def register_all() -> None:
    """Import builtin command modules and discover plugin entry points."""
    from aixworkflow.cli import extras, repo, wf  # noqa: F401

    discover_plugins()
