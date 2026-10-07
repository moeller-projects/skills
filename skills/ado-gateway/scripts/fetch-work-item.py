#!/usr/bin/env python3
"""fetch-work-item.py
Purpose: Fetches a single Azure DevOps work item via the REST API (GET only).
Inputs: Organization, project, work item ID, and optional API base URL as positional arguments.
Outputs: Raw work item JSON on stdout; structured BLOCKER or ERROR output on stderr.
Side effects: Performs one authenticated Azure DevOps GET with bounded retries.
Requires Python 3.9+, standard library only. Run with: python scripts/fetch-work-item.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _ado_lib as lib


def main() -> None:
    args = sys.argv[1:]
    if len(args) < 3:
        missing = ["org", "project", "work item id"][len(args):]
        lib.emit_blocker("MISSING_INPUT", missing, "Provide organization, project, and work item ID before fetching.")
    org, project, work_item_id = args[:3]
    base_url = args[3] if len(args) > 3 else "https://dev.azure.com"
    pat = lib.require_pat()
    del pat
    url = f"{base_url}/{org}/{project}/_apis/wit/workitems/{work_item_id}?api-version={lib.API_VERSION}"
    payload = lib.http_get_json(
        url,
        label=f"work item {work_item_id} from {org}/{project}",
        error_code="FETCH_FAILED",
        error_message=f"Failed to fetch work item {work_item_id} from {org}/{project} after bounded retries.",
        error_recovery="Check AZURE_DEVOPS_PAT, organization, project, and network connectivity.",
    )
    import json
    print(json.dumps(payload), end="")


if __name__ == "__main__":
    main()
