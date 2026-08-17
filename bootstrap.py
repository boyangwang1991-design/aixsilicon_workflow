#!/usr/bin/env python3
"""AIXSILICON workflow bootstrap launcher (pure stdlib, no third-party deps).

Skill 集中管理架构：`aixworkflow` 的 canonical 源码/测试/脚本由私有 skill repo
`repos/aixsilicon_skill_repo/skills/aixsilicon-workspace-management/` 统一管理；
workflow 根目录不再保存源码副本。

本引导器（workflow 根唯一保留的启动代码）：
1. 定位/克隆 skill repo（`repos/aixsilicon_skill_repo`）；
2. 把 skill repo 的 `skills/*` 物化（复制）到 git-忽略的 `/.roo/skills/`；
3. 把物化后的 `aixsilicon-workspace-management/src` 加入 `sys.path`，
   委托给 `aixworkflow.cli:main`（`aix`）。

用法（均从 workflow 根执行）：
    uv run python bootstrap.py --ensure      # 仅下载/更新 skill repo + 物化 skills
    uv run python bootstrap.py aix wf init --profile <name>
    uv run python bootstrap.py wf status      # 等效（自动去掉前导 aix）
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

WORKFLOW_ROOT = Path(__file__).resolve().parent
SKILL_REPO_REL = Path("repos") / "aixsilicon_skill_repo"
SKILL_REPO_URL = "git@github.com:boyangwang1991-design/aixsilicon_skill_repo.git"
SKILLS_TARGET_REL = Path(".roo") / "skills"
# canonical skill 目录（物化后从 .roo/skills 运行）
SKILL_NAME = "aixsilicon-workspace-management"


def _copytree_clean(src: Path, dst: Path) -> int:
    """Copy `src` tree into `dst`, replacing stale copies; returns file count."""
    if dst.exists():
        shutil.rmtree(dst)
    if not src.is_dir():
        return 0
    shutil.copytree(
        src,
        dst,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".venv", ".git", ".pytest_cache"),
    )
    return sum(1 for _ in dst.rglob("*") if _.is_file())


def _ensure_skill_repo() -> Path | None:
    """Return skill repo path, cloning it if missing (private repo)."""
    path = WORKFLOW_ROOT / SKILL_REPO_REL
    if (path / "skills").is_dir():
        return path
    print(f"bootstrap: cloning skill repo -> {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        ["git", "clone", SKILL_REPO_URL, str(path)],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0 or not (path / "skills").is_dir():
        print(
            f"ERROR: failed to clone skill repo: {proc.stderr.strip() or proc.stdout.strip()}\n"
            "  (private repo; platform access required)",
            file=sys.stderr,
        )
        return None
    return path


def _materialize_skills(skill_repo: Path) -> None:
    """Copy skill repo `skills/*` into git-ignored `/.roo/skills/`."""
    src_dir = skill_repo / "skills"
    target = WORKFLOW_ROOT / SKILLS_TARGET_REL
    target.mkdir(parents=True, exist_ok=True)
    total = 0
    for entry in sorted(src_dir.iterdir()):
        if not entry.is_dir():
            continue
        total += _copytree_clean(entry, target / entry.name)
    print(f"bootstrap: materialized skills -> {target} ({total} files)")


def _ensure(force: bool = False) -> bool:
    """Download/update skill repo + materialize skills. Returns True on success."""
    skill_repo = _ensure_skill_repo()
    if skill_repo is None:
        return False
    if not force:
        # lightweight: keep existing repo (fetch later if needed); materialize anyway
        pass
    _materialize_skills(skill_repo)
    return True


def _run_aix(argv: list[str]) -> int:
    # Accept both `bootstrap.py aix wf ...` and `bootstrap.py wf ...`.
    if argv and argv[0] == "aix":
        argv = argv[1:]
    skills_src = WORKFLOW_ROOT / SKILLS_TARGET_REL / SKILL_NAME / "src"
    sys.path.insert(0, str(skills_src))
    try:
        from aixworkflow.cli import main
    except ImportError as exc:  # pragma: no cover - materialization failed
        print(
            f"ERROR: aixworkflow not available ({exc}); run `bootstrap.py --ensure`",
            file=sys.stderr,
        )
        return 1
    main(argv)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="bootstrap.py",
        description="download skill repo, materialize skills to .roo/skills, run `aix`.",
    )
    parser.add_argument("--ensure", action="store_true", help="only materialize skills")
    parser.add_argument("--force", action="store_true", help="re-materialize even if present")
    parser.add_argument("rest", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)

    if not _ensure(force=args.force):
        return 1
    if args.ensure or args.force:
        return 0
    return _run_aix(list(args.rest))


if __name__ == "__main__":
    sys.exit(main())
