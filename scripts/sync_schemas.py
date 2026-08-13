#!/usr/bin/env python3
"""Sync packaged JSON schemas from the canonical `schemas/` directory.

`schemas/` is the single source of truth. The Python package keeps a copy
under `src/aixworkflow/schemas/` so the installed CLI can validate without
the repo checkout.

Usage:
    python scripts/sync_schemas.py            # sync (write package copy)
    python scripts/sync_schemas.py --check    # verify they match (CI)
"""

from __future__ import annotations

import hashlib
import shutil
import sys
from pathlib import Path

REPO_SCHEMAS = Path("schemas")
PKG_SCHEMAS = Path("src/aixworkflow/schemas")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    if not REPO_SCHEMAS.is_dir():
        print(f"error: canonical schema dir not found: {REPO_SCHEMAS}", file=sys.stderr)
        return 2

    repo_files = sorted(REPO_SCHEMAS.glob("*.json"))
    if not repo_files:
        print("error: no schemas in canonical dir", file=sys.stderr)
        return 2

    check = "--check" in sys.argv[1:]
    mismatched = 0
    PKG_SCHEMAS.mkdir(parents=True, exist_ok=True)

    for src in repo_files:
        dst = PKG_SCHEMAS / src.name
        if check:
            if not dst.is_file() or _sha256(src) != _sha256(dst):
                print(f"MISMATCH {src.name}", file=sys.stderr)
                mismatched += 1
            else:
                print(f"ok       {src.name}")
        else:
            shutil.copy2(src, dst)
            print(f"synced   {src.name}")

    # ensure no stale packaged schemas
    for dst in sorted(PKG_SCHEMAS.glob("*.json")):
        if dst.name not in {f.name for f in repo_files}:
            if check:
                print(f"STALE    {dst.name}", file=sys.stderr)
                mismatched += 1
            else:
                dst.unlink()
                print(f"removed  {dst.name}")

    if check and mismatched:
        print(
            f"\n{REPO_SCHEMAS} and {PKG_SCHEMAS} differ ({mismatched} problem(s)); run without --check",
            file=sys.stderr,
        )
        return 1
    print(f"\nschemas in sync ({len(repo_files)} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
