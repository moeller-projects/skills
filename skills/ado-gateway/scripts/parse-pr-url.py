#!/usr/bin/env python3
"""parse-pr-url.py
Purpose: Parse an Azure DevOps pull request URL into organization, project, repository, and PR identifiers.
Inputs: Azure DevOps pull request URL as the first positional argument.
Outputs: Parsed identifier JSON on stdout; structured BLOCKER output on stderr when the URL is missing or invalid.
Side effects: None.
Requires Python 3.9+, standard library only. Run with: python scripts/parse-pr-url.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _ado_lib as lib

_HINT = "Azure DevOps URL in the form https://dev.azure.com/<org>/<project>/_git/<repo>/pullrequest/<id>"


def main() -> None:
    url = sys.argv[1] if len(sys.argv) > 1 else ""
    if not url:
        lib.emit_blocker("MISSING_INPUT", [_HINT], "Provide an Azure DevOps pull request URL or explicit identifiers.")
    parsed = lib.parse_pull_request_url(url)
    if parsed is None:
        lib.emit_blocker("INVALID_PR_URL", [_HINT], "Provide a valid Azure DevOps pull request URL or explicit identifiers.")
    print(json.dumps(parsed))


if __name__ == "__main__":
    main()
