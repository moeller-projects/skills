#!/usr/bin/env python3
"""ensure-env.py
Purpose: Check optional PAT availability before Radio scripts run.
Inputs: Optional --require-pat flag; current environment variables.
Outputs: Nothing on stdout when valid; structured BLOCKER output on stderr when PAT is missing.
Side effects: None.
Requires Python 3.9+, standard library only. Run with: python scripts/ensure-env.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _ado_lib as lib


def main() -> None:
    if "--require-pat" in sys.argv[1:]:
        lib.require_pat()


if __name__ == "__main__":
    main()
