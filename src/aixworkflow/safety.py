"""Safety layer: high-risk command guards.

These implement policies/security-policy.yaml high-risk guards:

- refuse recursive `git clean -ffdx` / `rm -rf repos/*` in the workspace root
- refuse auto `reset --hard`, auto force-push, auto branch delete
- refuse dropping dirty trees without confirmation
- `aix wf clean` only removes generated dirs registered in local state
"""

from __future__ import annotations

import shlex
from dataclasses import dataclass
from pathlib import Path

from aixworkflow.errors import SafetyError

# Substrings that mark a command line as high-risk when operating on the
# workspace root (or anywhere in `repos/`).
_HIGH_RISK_PATTERNS: tuple[str, ...] = (
    "git clean",
    "git reset --hard",
    "git push --force",
    "git push -f",
    "git branch -D",
    "git branch --delete",
    "rm -rf",
    "rm -fr",
)


@dataclass(frozen=True)
class GuardResult:
    allowed: bool
    reason: str = ""


def is_high_risk(command: str) -> bool:
    """Return True when a raw shell command looks high-risk (conservative)."""
    lowered = command.lower()
    return any(pattern.lower() in lowered for pattern in _HIGH_RISK_PATTERNS)


def guard_high_risk(
    command: str,
    *,
    workspace_root: Path,
    confirmed: bool = False,
) -> GuardResult:
    """Guard high-risk commands; requires explicit confirmation."""
    if not is_high_risk(command):
        return GuardResult(allowed=True)
    if not confirmed:
        return GuardResult(
            allowed=False,
            reason=(
                "high-risk command refused without explicit confirmation: "
                f"{shlex.split(command)}"
            ),
        )
    return GuardResult(allowed=True)


def guard_recursive_clean(workspace_root: Path) -> None:
    """Refuse `git clean -ffdx` / `rm -rf repos/*` in the workspace root."""
    # Placeholder hook: called before wf clean; only generated dirs may be removed.
    raise SafetyError(
        "refusing recursive clean of the workspace root; use `aix wf clean` which "
        "only removes generated dirs registered in local state"
    )


def allowed_clean_dirs() -> list[str]:
    """Directories that `aix wf clean` may remove (generated only)."""
    return [".aix/generated", "build", "cache"]
