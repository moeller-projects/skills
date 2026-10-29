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
from urllib.parse import quote, unquote
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _ado_lib as lib


def main() -> None:
    if "--help" in sys.argv[1:]:
        print("usage: fetch-work-item.py ORG PROJECT WORK_ITEM_ID [BASE_URL]")
        return
    args = sys.argv[1:]
    if len(args) < 3:
        missing = ["org", "project", "work item id"][len(args):]
        lib.emit_blocker("MISSING_INPUT", missing, "Provide organization, project, and work item ID before fetching.")
    org, project, work_item_id = args[:3]
    org_path = lib.quote_segment(unquote(org), name="organization")
    project_path = lib.quote_segment(unquote(project), name="project")
    if not work_item_id.isdecimal():
        lib.emit_blocker("MISSING_INPUT", ["numeric work item id"], "Provide a numeric Azure DevOps work item ID.")
    base_url = args[3] if len(args) > 3 else "https://dev.azure.com"
    pat = lib.require_pat()
    del pat
    url = f"{base_url}/{org_path}/{project_path}/_apis/wit/workitems/{work_item_id}?%24expand=Relations&api-version={lib.API_VERSION}"
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
            f"{base_url}/{org_path}/{project_path}/_apis/wit/workitems/{work_item_id}/updates"
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
    comments: list[dict] = []
    continuation: str | None = None
    while True:
        suffix = "&$top=200" + (f"&continuationToken={quote(continuation, safe='')}" if continuation else "")
        comments_url = f"{base_url}/{org_path}/{project_path}/_apis/wit/workItems/{work_item_id}/comments?api-version=7.1-preview.4{suffix}"
        comments_payload = lib.http_get_json(
            comments_url,
            label=f"comments for work item {work_item_id} from {org}/{project}",
            error_code="FETCH_FAILED",
            error_message=f"Failed to fetch comments for work item {work_item_id} from {org}/{project} after bounded retries.",
            error_recovery="Check AZURE_DEVOPS_PAT, organization, project, and network connectivity.",
        )
        if not isinstance(comments_payload, dict) or "comments" not in comments_payload or not isinstance(comments_payload["comments"], list):
            lib.emit_error("PARSE_FAILED", "parse", "Unexpected comments response: comments must be a list.", "Check the comments endpoint response and retry.")
        comments.extend(comments_payload["comments"])
        continuation = comments_payload.get("continuationToken") or comments_payload.get("nextPageToken")
        if not continuation:
            break
    payload["comments"] = comments
    print(json.dumps(payload), end="")


if __name__ == "__main__":
    main()
