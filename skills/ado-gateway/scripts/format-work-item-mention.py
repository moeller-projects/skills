#!/usr/bin/env python3
"""format-work-item-mention.py
Purpose: Emit Azure DevOps work-item HTML @mention markup.
Inputs: --mention-id/--user-id/--descriptor and --display-name/--name options.
Outputs: Mention HTML on stdout; structured BLOCKER output on stderr when inputs are missing.
Side effects: None.
Requires Python 3.9+, standard library only. Run with: python scripts/format-work-item-mention.py
"""
from __future__ import annotations

import html
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _ado_lib as lib


def main() -> None:
    mention_id = ""
    display_name = ""
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        arg = args[i]
        if arg in ("--mention-id", "--user-id", "--descriptor"):
            if i + 1 >= len(args):
                print(f"Unknown argument: {arg}", file=sys.stderr)
                raise SystemExit(1)
            mention_id = args[i + 1]
            i += 2
        elif arg in ("--display-name", "--name"):
            if i + 1 >= len(args):
                print(f"Unknown argument: {arg}", file=sys.stderr)
                raise SystemExit(1)
            display_name = args[i + 1]
            i += 2
        else:
            print(f"Unknown argument: {arg}", file=sys.stderr)
            raise SystemExit(1)
    missing = []
    if not mention_id:
        missing.append("mention_id")
    if not display_name:
        missing.append("display_name")
    if missing:
        lib.emit_blocker("MISSING_INPUT", missing, "Provide mention id/descriptor and display name to build the mention markup.")
    safe_id = html.escape(mention_id, quote=True)
    safe_name = html.escape(display_name, quote=False)
    print(f'<a href="#" data-vss-mention="version:2.0,{{{safe_id}}}">@{safe_name}</a>')


if __name__ == "__main__":
    main()
