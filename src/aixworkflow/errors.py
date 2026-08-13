"""Error types and exit code contract for the aix CLI.

Exit code contract follows the organization-wide segmented scheme
(see `docs/adr/0004-cli-entry-and-plugin-registry.md` and the tool repo
Result/exit-code convention):

- 0     success
- 10    input / schema errors (manifest, args, schema validation)
- 20    design / rule check failures (lint, compile, sim, gate)
- 30    external tool / environment failures (network, git, EDA, toolchain)
- 40    file / permission / security errors (blocked guards, missing file)
- 50    compatibility / version errors
- 60    internal errors

This keeps "design failure" (20) distinct from "environment failure" (30)
so release automation can retry infra errors without masking design issues.
"""

from __future__ import annotations

EXIT_OK = 0
EXIT_INPUT_ERROR = 10
EXIT_DESIGN_FAILURE = 20
EXIT_INFRA_FAILURE = 30
EXIT_BLOCKED = 40
EXIT_COMPAT_ERROR = 50
EXIT_INTERNAL_ERROR = 60

# Backward-compatible aliases (old single-digit codes are still exported for
# callers that referenced them before the segmented contract).
EXIT_LEGACY_DESIGN_FAILURE = EXIT_DESIGN_FAILURE
EXIT_LEGACY_INFRA_FAILURE = EXIT_INFRA_FAILURE
EXIT_LEGACY_BLOCKED = EXIT_BLOCKED


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
    """Manifest/schema problem (input layer)."""

    exit_code = EXIT_INPUT_ERROR
    category = "manifest"


class CompatibilityError(AixError):
    """Compatibility or version mismatch (VLNV, contract, tool profile)."""

    exit_code = EXIT_COMPAT_ERROR
    category = "compatibility"


class InternalError(AixError):
    """Unexpected internal error; should not normally surface to users."""

    exit_code = EXIT_INTERNAL_ERROR
    category = "internal"


class SafetyError(BlockedError):
    """A high-risk operation was refused by the safety layer."""

    category = "safety"
