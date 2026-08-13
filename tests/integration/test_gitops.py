"""Integration tests: git operations against local temporary repositories."""

from __future__ import annotations

from aixworkflow import gitops


def test_clone_and_status(make_git_repo, tmp_path):
    remote = make_git_repo("hwif_repo", files={"README.md": "# hwif\n"})
    dest = tmp_path / "clone"
    gitops.clone(str(remote), dest, branch="main")
    assert gitops.is_repo(dest)
    status = gitops.get_status(dest, str(remote))
    assert status.present
    assert status.dirty is False
    assert status.remote_url is not None
    assert gitops.verify_remote(dest, str(remote))


def test_remote_mismatch_detected(make_git_repo, tmp_path):
    remote = make_git_repo("hwif_repo", files={"a": "1"})
    dest = tmp_path / "clone"
    gitops.clone(str(remote), dest, branch="main")
    assert not gitops.verify_remote(dest, "git@github.com:aixsilicon/other.git")


def test_dirty_detection(make_git_repo, tmp_path):
    remote = make_git_repo("hwif_repo", files={"a.txt": "v1"})
    dest = tmp_path / "clone"
    gitops.clone(str(remote), dest, branch="main")
    (dest / "untracked.txt").write_text("x", encoding="utf-8")
    dirty, staged, unstaged, untracked = gitops.dirty_status(dest)
    assert dirty and untracked == 1


def test_branch_and_commit(make_git_repo, tmp_path):
    remote = make_git_repo("vip_repo", files={"t.sv": "module t;\nendmodule\n"})
    dest = tmp_path / "clone"
    gitops.clone(str(remote), dest, branch="main")
    gitops.create_branch(dest, "feature/x")
    (dest / "new.sv").write_text("// new\n", encoding="utf-8")
    gitops._run(["add", "."], cwd=dest)
    gitops.commit(dest, "feat: add new")
    branch, detached = gitops.current_branch(dest)
    assert branch == "feature/x"
    assert not detached


def test_unreachable_commit(make_git_repo, tmp_path):
    remote = make_git_repo("hwif_repo", files={"a": "1"})
    dest = tmp_path / "clone"
    gitops.clone(str(remote), dest, branch="main")
    assert gitops.rev_parse(dest, "deadbeef" * 5) is None


def test_ls_remote_resolves_branch(make_git_repo):
    remote = make_git_repo("hwif_repo", files={"a": "1"})
    sha = gitops.ls_remote(str(remote), "refs/heads/main")
    assert sha and len(sha) == 40


def test_remote_has_branches(make_git_repo):
    remote = make_git_repo("hwif_repo", files={"a": "1"})
    assert gitops.remote_has_branches(str(remote))


def test_remote_empty_detected(tmp_path):
    import subprocess

    empty = tmp_path / "empty.git"
    subprocess.run(["git", "init", "--bare", str(empty)], check=True, capture_output=True)
    assert not gitops.remote_has_branches(str(empty))


def test_rev_parse_any_tree(make_git_repo, tmp_path):
    """`rev_parse_any` must peel `sha^{tree}` (regression: lockfile tree was empty)."""
    remote = make_git_repo("hwif_repo", files={"a.txt": "1"})
    dest = tmp_path / "clone"
    gitops.clone(str(remote), dest, branch="main")
    sha = gitops.head_sha(dest)
    tree = gitops.rev_parse_any(dest, f"{sha}^{{tree}}")
    assert tree and len(tree) == 40
    # the old path (rev_parse appending ^{commit}) must still be a commit sha
    assert gitops.rev_parse(dest, sha) == sha
