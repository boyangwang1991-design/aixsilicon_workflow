#!/usr/bin/env python3
"""AIXSILICON workflow bootstrap launcher (pure stdlib, no third-party deps).

Skill 集中管理架构：`aixworkflow` 的源码/测试/脚本由私有 `aixsilicon_skill_repo`
（`repos/aixsilicon_skill_repo/skills/aixsilicon-workspace-management/`）统一管理；
workflow 根目录不再保存源码副本。

本引导器（workflow 根唯一保留的启动代码）：
1. 定位/克隆 skill repo（`repos/aixsilicon_skill_repo`）；
2. 委托 `aixsilicon_skill_repo` 中的 `bootstrap_env.py materialize-skills`
   把 skill repo 的 `skills/*` 物化（复制）到 git-忽略的 agent 目录
   （`/<agent-dir>/skills/`，默认 `.roo`）-- 物化逻辑只维护在
   `bootstrap_env.py` 一份（单一事实源），本文件禁止再实现一套复制逻辑；
3. 把物化后的 `aixsilicon-workspace-management/src` 加入 `sys.path`，
   委托给 `aixworkflow.cli:main`（`aix`）。

agent 目录解析优先级：`--agent-dir <dir>` 参数 > `AIX_AGENT_DIR` 环境变量 >
默认 `.roo`。业界常用值：`.roo`、`.claude`、`.opencode`、`.cursor`、`.codex`、
`.windsurf`。技能、agent 配置、rules 等均存放于该目录下。

用法（均从 workflow 根执行）：
    uv run python bootstrap.py --ensure              # 仅下载/更新 skill repo + 物化 skills
    uv run python bootstrap.py --force               # 同 --ensure，并强制快进更新 skill repo
    uv run python bootstrap.py --agent-dir .claude --ensure
    uv run python bootstrap.py --run-hook guard_runtime_paths.py   # 运行 guard hook（pre-commit 用）
    uv run python bootstrap.py aix wf init --profile <name>
    uv run python bootstrap.py wf status              # 等效（自动去掉前导 aix）
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

WORKFLOW_ROOT = Path(__file__).resolve().parent
SKILL_REPO_REL = Path("repos") / "aixsilicon_skill_repo"
SKILL_REPO_URL = "git@github.com:boyangwang1991-design/aixsilicon_skill_repo.git"
# skill 目录（物化后从 <agent-dir>/skills 运行）与其引导脚本
SKILL_NAME = "aixsilicon-workspace-management"
ENV_SCRIPT_REL = SKILL_REPO_REL / "skills" / SKILL_NAME / "scripts" / "bootstrap_env.py"
HOOKS_REL = Path(SKILL_NAME) / "scripts" / "hooks"

DEFAULT_AGENT_DIR = ".roo"
AGENT_DIR_ENV = "AIX_AGENT_DIR"
# 业界常用 agent 目录（skill/agent/rules 等的候选存放位置）
KNOWN_AGENT_DIRS = (".roo", ".claude", ".opencode", ".cursor", ".codex", ".windsurf")


def _run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, capture_output=True, text=True, check=False)


def resolve_agent_dir(agent_dir: str | None) -> str:
    """Resolve agent dir: CLI arg > AIX_AGENT_DIR env > default `.roo`."""
    candidate = agent_dir or os.environ.get(AGENT_DIR_ENV, DEFAULT_AGENT_DIR)
    return candidate.strip("/\\") or DEFAULT_AGENT_DIR


def _skills_target(agent_dir: str) -> Path:
    return WORKFLOW_ROOT / agent_dir / "skills"


def _ensure_skill_repo(force: bool = False) -> Path | None:
    """Return skill repo path, cloning it if missing (private repo).

    `force=True` additionally fast-forwards the repo from origin; a failed pull
    is only a warning (the local repo stays usable).
    """
    path = WORKFLOW_ROOT / SKILL_REPO_REL
    if (path / "skills").is_dir():
        if force:
            proc = _run(["git", "-C", str(path), "pull", "--ff-only", "origin", "main"])
            if proc.returncode != 0:
                print(
                    "bootstrap: WARN git pull failed; using local skill repo as-is: "
                    f"{proc.stderr.strip() or proc.stdout.strip()}"
                )
        return path

    print(f"bootstrap: cloning skill repo -> {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    proc = _run(["git", "clone", SKILL_REPO_URL, str(path)])
    if proc.returncode != 0 or not (path / "skills").is_dir():
        print(
            f"ERROR: failed to clone skill repo: {proc.stderr.strip() or proc.stdout.strip()}\n"
            "  (private repo; platform access required)",
            file=sys.stderr,
        )
        return None
    return path


def _materialize_skills(skill_repo: Path, agent_dir: str, force: bool = False) -> bool:
    """Delegate materialization to aixsilicon_skill_repo bootstrap_env.py (single source of truth).

    The delegated script keeps a fingerprint cache and skips the full copy when
    the skill repo HEAD (and working tree) is unchanged; `force=True` bypasses it.
    """
    script = WORKFLOW_ROOT / ENV_SCRIPT_REL
    if not script.is_file():
        print(f"ERROR: aixsilicon_skill_repo bootstrap_env.py not found: {script}", file=sys.stderr)
        return False
    target = _skills_target(agent_dir)
    cmd = [
        sys.executable,
        str(script),
        "materialize-skills",
        "--workflow-root",
        str(WORKFLOW_ROOT),
        "--agent-dir",
        agent_dir,
        "--source",
        str(skill_repo / "skills"),
        "--target",
        str(target),
    ]
    if force:
        cmd.append("--force")
    proc = subprocess.run(cmd, check=False, text=True)
    if proc.returncode != 0:
        return False
    return True


def _ensure(
    force: bool = False,
    agent_dir: str = DEFAULT_AGENT_DIR,
    skip_materialize: bool = False,
) -> bool:
    """Ensure skill repo present (clone/update) + materialize skills. True on success.

    `skip_materialize=True` keeps using already-materialized skills (offline /
    repeated-invocation mode) as long as the delegated aix entry exists.
    """
    skill_repo = _ensure_skill_repo(force=force)
    if skill_repo is None:
        return False
    if skip_materialize and (_skills_target(agent_dir) / SKILL_NAME).is_dir():
        return True
    return _materialize_skills(skill_repo, agent_dir, force=force)


def _run_hook(hook_name: str, agent_dir: str) -> int:
    """Run a guard hook from the materialized skill under <agent-dir>/skills."""
    hook = _skills_target(agent_dir) / HOOKS_REL / hook_name
    if not hook.is_file():
        print(f"bootstrap: ERROR hook not found: {hook} (run --ensure first)", file=sys.stderr)
        return 1
    proc = subprocess.run([sys.executable, str(hook)], check=False)
    return proc.returncode


def _run_aix(argv: list[str], agent_dir: str) -> int:
    # Accept both `bootstrap.py aix wf ...` and `bootstrap.py wf ...`.
    if argv and argv[0] == "aix":
        argv = argv[1:]
    skills_src = _skills_target(agent_dir) / SKILL_NAME / "src"
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
        description=(
            "download skill repo, materialize skills to <agent-dir>/skills (default .roo), "
            "run `aix` or a guard hook."
        ),
    )
    parser.add_argument("--ensure", action="store_true", help="only materialize skills")
    parser.add_argument(
        "--force",
        action="store_true",
        help="also fast-forward skill repo, then force full re-materialization",
    )
    parser.add_argument(
        "--skip-materialize",
        action="store_true",
        help=(
            "skip materialization and reuse <agent-dir>/skills as-is "
            "(for repeated aix invocations; falls back to materialize when missing)"
        ),
    )
    parser.add_argument(
        "--run-hook",
        metavar="HOOK",
        help="run a guard hook from materialized skills (e.g. guard_runtime_paths.py)",
    )
    parser.add_argument(
        "--agent-dir",
        default=None,
        help=(
            f"agent config/skills dir (default from {AGENT_DIR_ENV} env or `{DEFAULT_AGENT_DIR}`; "
            f"known: {', '.join(KNOWN_AGENT_DIRS)})"
        ),
    )
    parser.add_argument("rest", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)

    agent_dir = resolve_agent_dir(args.agent_dir)

    if args.run_hook:
        if not _ensure(force=False, agent_dir=agent_dir, skip_materialize=args.skip_materialize):
            return 1
        return _run_hook(args.run_hook, agent_dir)

    if not _ensure(force=args.force, agent_dir=agent_dir, skip_materialize=args.skip_materialize):
        return 1
    if args.ensure or args.force:
        return 0
    return _run_aix(list(args.rest), agent_dir)


if __name__ == "__main__":
    sys.exit(main())
