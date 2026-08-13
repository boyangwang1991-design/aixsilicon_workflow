#!/usr/bin/env python3
"""pre-commit hook: refuse runtime/generated paths entering the parent index.

Rejects `repos/`, `build/`, `cache/`, `reports/`, `.aix/`, `generated/`,
`fusesoc.conf`, `edalize_work_root/`, and EDA log/waveform artifacts.
"""

from __future__ import annotations

import subprocess
import sys

FORBIDDEN_PREFIXES = (
    "repos/",
    "build/",
    "cache/",
    "reports/",
    ".aix/",
    "generated/",
    "edalize_work_root/",
)

FORBIDDEN_FILENAMES = ("fusesoc.conf",)

FORBIDDEN_SUFFIXES = (
    ".log",
    ".jou",
    ".wlf",
    ".vcd",
    ".fsdb",
    ".shm",
    ".tmp",
)


def staged_paths() -> list[str]:
    proc = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "-z"],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return []
    return [p for p in proc.stdout.split("\0") if p]


def main() -> int:
    offenders: list[str] = []
    for path in staged_paths():
        norm = path.replace("\\", "/")
        if any(norm.startswith(p) for p in FORBIDDEN_PREFIXES):
            offenders.append(path)
            continue
        name = norm.rsplit("/", 1)[-1]
        if name in FORBIDDEN_FILENAMES:
            offenders.append(path)
            continue
        if name.endswith(FORBIDDEN_SUFFIXES):
            offenders.append(path)
            continue
    if offenders:
        print("pre-commit: refusing runtime/generated paths in the parent repo index:")
        for o in offenders:
            print(f"  - {o}")
        print("Remove them from the index or use `aix wf clean` to remove generated dirs.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
