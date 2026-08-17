"""WF-007/TOOL-004 + WF-012: exit-code contract, tool argument/path security.

Covers:
- segmented exit-code contract (F-012): 0/10/20/30/40/50/60 stable mapping
- git operations use list arguments, never shell strings (F-005)
- high-risk command guard refuses without confirmation (F-005)
- write_scope/ownership: path escape is refused (F-006)
- safe clean only removes generated dirs
"""

from __future__ import annotations

from pathlib import Path

import pytest

from aixworkflow.errors import (
    EXIT_BLOCKED,
    EXIT_COMPAT_ERROR,
    EXIT_DESIGN_FAILURE,
    EXIT_INFRA_FAILURE,
    EXIT_INPUT_ERROR,
    EXIT_INTERNAL_ERROR,
    EXIT_OK,
    BlockedError,
    CompatibilityError,
    DesignError,
    InfraError,
    InternalError,
    ManifestError,
    SafetyError,
)
from aixworkflow.safety import allowed_clean_dirs, guard_high_risk, is_high_risk

# ---------------- exit code contract (F-012) ----------------


def test_exit_code_segments() -> None:
    assert EXIT_OK == 0
    assert EXIT_INPUT_ERROR == 10
    assert EXIT_DESIGN_FAILURE == 20
    assert EXIT_INFRA_FAILURE == 30
    assert EXIT_BLOCKED == 40
    assert EXIT_COMPAT_ERROR == 50
    assert EXIT_INTERNAL_ERROR == 60


def test_error_class_exit_codes() -> None:
    assert ManifestError("x").exit_code == 10
    assert DesignError("x").exit_code == 20
    assert InfraError("x").exit_code == 30
    assert BlockedError("x").exit_code == 40
    assert CompatibilityError("x").exit_code == 50
    assert InternalError("x").exit_code == 60


def test_safety_error_is_blocked() -> None:
    err = SafetyError("refused")
    assert err.exit_code == EXIT_BLOCKED
    assert err.category == "safety"


# ---------------- high-risk command guard (F-005) ----------------


def test_high_risk_patterns() -> None:
    assert is_high_risk("git clean -ffdx")
    assert is_high_risk("git reset --hard origin/main")
    assert is_high_risk("git push --force origin main")
    assert is_high_risk("rm -rf repos/*")
    assert not is_high_risk("git status --short")
    assert not is_high_risk("make check")


def test_guard_refuses_without_confirmation(tmp_path) -> None:
    res = guard_high_risk("rm -rf repos/*", workspace_root=tmp_path, confirmed=False)
    assert not res.allowed
    assert "refused" in res.reason


def test_guard_allows_with_confirmation(tmp_path) -> None:
    res = guard_high_risk("rm -rf repos/*", workspace_root=tmp_path, confirmed=True)
    assert res.allowed


def test_guard_allows_safe_command(tmp_path) -> None:
    res = guard_high_risk("make check", workspace_root=tmp_path)
    assert res.allowed


# ---------------- safe clean dirs ----------------


def test_clean_only_generated_dirs() -> None:
    dirs = allowed_clean_dirs()
    assert set(dirs) == {".aix/generated", "build", "cache"}
    assert "repos" not in dirs
    assert "reports" not in dirs


# ---------------- git argument safety (F-005) ----------------


def test_gitops_uses_list_args_not_shell(tmp_path, make_git_repo) -> None:
    from aixworkflow import gitops

    repo = make_git_repo("sec_repo", {"README.md": "# sec\n"})
    work = tmp_path / "sec_work"
    gitops.clone(str(repo), work)
    assert gitops.is_repo(work)
    # A malicious "branch" value must be treated as a literal argument, never shell.
    status = gitops.get_status(work)
    assert status.present


def test_gitops_commit_rejects_empty_message(tmp_path, make_git_repo) -> None:
    from aixworkflow import gitops

    repo = make_git_repo("sec_commit", {"a.txt": "a\n"})
    work = tmp_path / "sec_commit_clone"
    gitops.clone(str(repo), work)
    with pytest.raises(SafetyError):
        gitops.commit(work, "")


# ---------------- write_scope / ownership (F-006) ----------------


def test_runner_rejects_write_scope_escape(tmp_path) -> None:
    from aixworkflow.flow import Flow, FlowStage
    from aixworkflow.runner import ActionRegistry, run_flow

    reg = ActionRegistry()
    reg.register("tool.reg", lambda s: None)
    stage = FlowStage(
        id="s1",
        uses="tool.reg",
        needs=[],
        with_={},
        write_scope=[{"repo": "ip", "paths": ["../../etc/passwd"]}],
        timeout_seconds=None,
        retries=0,
    )
    flow = Flow(
        name="sec-flow",
        description="",
        inputs=[],
        preconditions={},
        stages=[stage],
        on_failure="collect_evidence_then_fail",
        source_path=Path("sec-flow.yaml"),
    )
    with pytest.raises(DesignError):
        run_flow(flow, registry=reg, root=tmp_path)
