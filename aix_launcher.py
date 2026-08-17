"""`aix` console entry point → bootstrap launcher.

Kept at the workflow root (with bootstrap.py) so that `uv run aix ...` works
after the canonical `src/` moved to the private skill repo. It materializes the
skill to `/.roo/skills/` and delegates to `aixworkflow.cli:main` from
`/.roo/skills/aixsilicon-workspace-management/src`.
"""

from __future__ import annotations

import sys

import bootstrap


def main(argv: list[str] | None = None) -> None:
    args = list(argv if argv is not None else sys.argv[1:])
    code = bootstrap.main(args)
    if code:
        sys.exit(code)


if __name__ == "__main__":
    main()
