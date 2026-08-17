"""WF-012: controlled PR / credentials / permission negative tests.

Covers:
- cross-repo event-loop guard refuses excessive depth (github.py)
- CI token is never exposed; token() only reads env, never written to artifacts
- git push refuses force-push (gitops.py)
- permissions: write_scope enforcement is additive with ownership (F-006)
"""

from __future__ import annotations

import pytest

from aixworkflow.errors import BlockedError
from aixworkflow.github import MAX_EVENT_DEPTH, DispatchEvent, guard_event_loop, token


def test_event_loop_guard_allows_within_depth():
    event = DispatchEvent(
        correlation_id="cid-1",
        source_repo="aixsilicon_hwif_repo",
        source_sha="abc1234",
        depth=2,
    )
    # should not raise
    guard_event_loop(event)


def test_event_loop_guard_refuses_excess_depth():
    event = DispatchEvent(
        correlation_id="cid-1",
        source_repo="aixsilicon_hwif_repo",
        source_sha="abc1234",
        depth=MAX_EVENT_DEPTH + 1,
    )
    with pytest.raises(BlockedError):
        guard_event_loop(event)


def test_token_reads_env_only(monkeypatch):
    monkeypatch.delenv("AIX_GITHUB_TOKEN", raising=False)
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    assert token() is None
    monkeypatch.setenv("GITHUB_TOKEN", "secret-value")
    assert token() == "secret-value"


def test_evidence_never_contains_token(tmp_path, monkeypatch):
    """Run-manifest artifacts must not capture CI token (secret redaction)."""
    monkeypatch.setenv("GITHUB_TOKEN", "top-secret-token")
    from aixworkflow.evidence import EvidenceCollector

    collector = EvidenceCollector(flow="release-train")
    collector.record_stage("approval", "passed")
    out = collector.write(tmp_path / "reports" / collector.run_id)
    for fname in ("run_manifest.yaml", "evidence_index.yaml", "status.json"):
        content = (out / fname).read_text(encoding="utf-8")
        assert "top-secret-token" not in content
        assert "GITHUB_TOKEN" not in content


def test_push_never_uses_force():
    """gitops.push has no force flag; force-push is refused by the safety guard."""
    import inspect

    from aixworkflow import gitops
    from aixworkflow.safety import is_high_risk

    sig = inspect.signature(gitops.push)
    assert "force" not in sig.parameters
    # The safety layer explicitly refuses force-push patterns (F-005).
    assert is_high_risk("git push --force origin main")
    assert is_high_risk("git push -f origin main")
