"""Error types and exit code contract for the aix CLI.

Exit code contract (see policies/security-policy.yaml):

- 0  success
- 1  design failure (lint/compile/sim/gate failures)
- 2  infra failure (network/git/EDA infrastructure problems)
- 3  blocked (missing permission, dirty/override guard, approval required)
"""

from __future__ import annotations

EXIT_OK = 0
EXIT_DESIGN_FAILURE = 1
EXIT_INFRA_FAILURE = 2
EXIT_BLOCKED = 3


class AixError(Exception):
    """Base class for all aix workflow errors."""

    exit_code = EXIT_DESIGN_FAILURE
    category = "error"

    def __init__(self, message: str, *, repo: str | None = None, stage: str | None = None) -> None:
        self.message = message
        self.repo = repo
        self.stage = stage
        super().__init__(message)


class InfraError(AixError):
    """Infrastructure failure: network, git, toolchain availability."""

    exit_code = EXIT_INFRA_FAILURE
    category = "infra"


class BlockedError(AixError):
    """Blocked by a policy/guard: needs approval, dirty tree, override, etc."""

    exit_code = EXIT_BLOCKED
    category = "blocked"


class DesignError(AixError):
    """Design/verification failure (gate failure)."""

    exit_code = EXIT_DESIGN_FAILURE
    category = "design"


class ManifestError(AixError):
    """Manifest/schema problem."""

    exit_code = EXIT_DESIGN_FAILURE
    category = "manifest"


class SafetyError(BlockedError):
    """A high-risk operation was refused by the safety layer."""

    category = "safety"
