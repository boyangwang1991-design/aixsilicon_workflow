"""Lightweight command registry.

A new command is added with one decorator + one handler function; no changes
to the dispatch logic are required.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

CommandHandler = Callable[[Any], None]

_REGISTRY: dict[str, CommandHandler] = {}


def command(domain: str, name: str) -> Callable[[CommandHandler], CommandHandler]:
    """Decorator registering a handler for `domain.name` (e.g. `wf.sync`)."""

    def deco(fn: CommandHandler) -> CommandHandler:
        _REGISTRY[f"{domain}.{name}"] = fn
        return fn

    return deco


def get_handler(domain: str, name: str) -> CommandHandler | None:
    return _REGISTRY.get(f"{domain}.{name}")


def register_all() -> None:
    """Import command modules so their decorators register handlers."""
    from aixworkflow.cli import extras, repo, wf  # noqa: F401
