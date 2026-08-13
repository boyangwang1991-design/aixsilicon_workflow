"""`aix` entry point: parse args, dispatch to registered handlers."""

from __future__ import annotations

import sys
from collections.abc import Sequence

from aixworkflow.cli.args import build_parser
from aixworkflow.cli.registry import get_handler, register_all
from aixworkflow.errors import AixError


def main(argv: Sequence[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    register_all()
    try:
        handler = get_handler(args.domain, args.command)
        if handler is None:
            raise AixError(f"unknown command: {args.domain} {args.command}")
        handler(args)
    except AixError as exc:
        prefix = f"[{exc.category}]"
        location = f" repo={exc.repo}" if exc.repo else ""
        stage = f" stage={exc.stage}" if exc.stage else ""
        print(f"{prefix}{location}{stage}: {exc.message}", file=sys.stderr)
        sys.exit(exc.exit_code)
    except KeyboardInterrupt:
        print("interrupted", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    main()
