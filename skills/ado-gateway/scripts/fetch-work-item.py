#!/usr/bin/env python3
"""fetch-work-item.py
Purpose: Fetches a single Azure DevOps work item via the REST API (GET only).
Inputs: Organization, project, work item ID, and optional API base URL as positional arguments.
Outputs: Raw work item JSON on stdout; structured BLOCKER or ERROR output on stderr.
Side effects: Performs authenticated Azure DevOps GETs with bounded retries.
Requires Python 3.9+, standard library only. Run with: python scripts/fetch-work-item.py
"""
from __future__ import annotations

import json
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
    url = f"{base_url}/{org}/{project}/_apis/wit/workitems/{work_item_id}?%24expand=Relations&api-version={lib.API_VERSION}"
    payload = lib.http_get_json(
        url,
        label=f"work item {work_item_id} from {org}/{project}",
        error_code="FETCH_FAILED",
        error_message=f"Failed to fetch work item {work_item_id} from {org}/{project} after bounded retries.",
        error_recovery="Check AZURE_DEVOPS_PAT, organization, project, and network connectivity.",
    )
    updates: list[dict] = []
    page_size = 200
    skip = 0
    while True:
        updates_url = (
            f"{base_url}/{org}/{project}/_apis/wit/workitems/{work_item_id}/updates"
            f"?%24top={page_size}&%24skip={skip}&api-version={lib.API_VERSION}"
        )
        updates_payload = lib.http_get_json(
            updates_url,
            label=f"history for work item {work_item_id} from {org}/{project}",
            error_code="FETCH_FAILED",
            error_message=f"Failed to fetch history for work item {work_item_id} from {org}/{project} after bounded retries.",
            error_recovery="Check AZURE_DEVOPS_PAT, organization, project, and network connectivity.",
        )
        if not isinstance(updates_payload, dict) or not isinstance(updates_payload.get("value"), list):
            lib.emit_error(
                "PARSE_FAILED",
                "parse",
                f"Unexpected history response for work item {work_item_id}.",
                "Check that the Azure DevOps updates endpoint returned a value array and retry.",
            )
        page = updates_payload["value"]
        updates.extend(update for update in page if isinstance(update, dict))
        if len(page) < page_size:
            break
        skip += len(page)
    payload["updates"] = updates
    comments_url = f"{base_url}/{org}/{project}/_apis/wit/workItems/{work_item_id}/comments?api-version=7.1-preview.4"
    comments_payload = lib.http_get_json(
        comments_url,
        label=f"comments for work item {work_item_id} from {org}/{project}",
        error_code="FETCH_FAILED",
        error_message=f"Failed to fetch comments for work item {work_item_id} from {org}/{project} after bounded retries.",
        error_recovery="Check AZURE_DEVOPS_PAT, organization, project, and network connectivity.",
    )
    payload["comments"] = comments_payload.get("comments", []) if isinstance(comments_payload, dict) else []
    print(json.dumps(payload), end="")


if __name__ == "__main__":
    main()
