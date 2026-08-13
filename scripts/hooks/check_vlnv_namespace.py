#!/usr/bin/env python3
"""Guard: reject non-`aixsilicon:` FuseSoC VLNV in living config (ADR-0003).

Scans manifests/, workflows/, changesets/, templates/, policies/, schemas/ for
FuseSoC VLNV of the form `vendor:library:name` where vendor is not `aixsilicon`
(e.g. legacy `aix:`, `company:`, `boyangwang1991-design:`). Decision/plan
markdown that documents the migration is intentionally out of scope.

Usage:
    python scripts/hooks/check_vlnv_namespace.py        # check (CI / pre-commit)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCAN_DIRS = ("manifests", "workflows", "changesets", "templates", "policies", "schemas")
_PATTERN = re.compile(
    r"\b(?:aix|company|boyangwang1991-design):(?:ip|vip|cbb|interface|dv|tool|soc):"
)


def main() -> int:
    bad: list[tuple[Path, int, str]] = []
    for rel in SCAN_DIRS:
        base = ROOT / rel
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if path.suffix not in (".yaml", ".yml", ".json", ".md"):
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except OSError:
                continue
            for lineno, line in enumerate(text.splitlines(), start=1):
                if _PATTERN.search(line):
                    bad.append((path, lineno, line.strip()))

    if bad:
        print("non-aixsilicon VLNV found (ADR-0003):", file=sys.stderr)
        for path, lineno, line in bad:
            print(f"  {path.relative_to(ROOT)}:{lineno}: {line}", file=sys.stderr)
        return 1
    print("vlnv namespace ok (aixsilicon:*)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
