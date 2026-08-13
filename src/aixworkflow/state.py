"""Local workspace state persisted under `.aix/` (git-ignored)."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

STATE_FILENAME = "state.json"


@dataclass
class WorkspaceState:
    workspace_root: Path
    manifest_path: str = ""
    profile: str = ""
    initialized: bool = False
    extra: dict[str, Any] = field(default_factory=dict)

    @property
    def state_file(self) -> Path:
        return self.workspace_root / ".aix" / STATE_FILENAME

    def load(self) -> WorkspaceState:
        if not self.state_file.is_file():
            return self
        try:
            data = json.loads(self.state_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return self
        self.manifest_path = str(data.get("manifest_path", ""))
        self.profile = str(data.get("profile", ""))
        self.initialized = bool(data.get("initialized", False))
        self.extra = dict(data.get("extra", {}))
        return self

    def save(self) -> None:
        data = {
            "manifest_path": self.manifest_path,
            "profile": self.profile,
            "initialized": self.initialized,
            "extra": self.extra,
        }
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state_file.write_text(
            json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )


def local_state_path(workspace_root: Path) -> Path:
    return workspace_root / ".aix" / STATE_FILENAME


def python_version() -> str:
    return f"{sys.version_info.major}.{sys.version_info.minor}"
