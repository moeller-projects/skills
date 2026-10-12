#!/usr/bin/env python3
"""fetch-pr-comments.py
Purpose: Fetch and flatten Azure DevOps pull request thread comments (GET only).
Inputs: --pull-request-url or explicit organization/project/repository-id/pull-request-id; optional --include-raw-threads.
Outputs: Flattened pull request and comment JSON on stdout; structured blockers/errors on stderr.
Side effects: Read-only Azure DevOps API requests.
Requires Python 3.9+, standard library only. Run with: python scripts/fetch-pr-comments.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _ado_lib as lib


def _fetch(url: str, label: str, message: str) -> object:
    return lib.http_get_json(
        url,
        label=label,
        error_code="FETCH_FAILED",
        error_message=message,
        error_recovery="Check AZURE_DEVOPS_PAT, identifiers, and network connectivity.",
    )


def _number(value: object) -> int | None:
    try:
        if isinstance(value, bool) or value is None:
            return None
        return int(value)
    except (TypeError, ValueError):
        return None


def _comment_side(thread: dict) -> str:
    context = thread.get("threadContext") or {}
    if context.get("rightFileStart") is not None or context.get("rightFileEnd") is not None:
        return "right"
    if context.get("leftFileStart") is not None or context.get("leftFileEnd") is not None:
        return "left"
    return "general"


def _anchor(thread: dict, side: str, end: bool) -> dict:
    context = thread.get("threadContext") or {}
    key = ("right" if side == "right" else "left") + ("FileEnd" if end else "FileStart")
    value = context.get(key)
    return value if isinstance(value, dict) else {}


def _flatten(threads: list, organization: str, project: str, repository_id: str, pull_request_id: int, pr: dict, work_items: list, include_raw: bool) -> dict:
    comments = []
    for thread in threads:
        if not isinstance(thread, dict):
            continue
        side = _comment_side(thread)
        context = thread.get("threadContext") or {}
        file_path = lib.normalize_repo_root_path(context.get("filePath"))
        start = _anchor(thread, side, False)
        finish = _anchor(thread, side, True)
        for comment in (thread.get("comments") or []):
            if not isinstance(comment, dict):
                continue
            author = comment.get("author") or {}
            comments.append({
                "thread_id": thread.get("id"),
                "comment_id": comment.get("id"),
                "parent_comment_id": comment.get("parentCommentId"),
                "author": author.get("displayName") if isinstance(author, dict) else None,
                "content": lib.redact_text(comment.get("content")),
                "file_path": file_path,
                "side": side,
                "start_line": start.get("line"),
                "end_line": finish.get("line"),
                "start_offset": start.get("offset"),
                "end_offset": finish.get("offset"),
                "thread_status": thread.get("status"),
                "thread_is_deleted": thread.get("isDeleted") or False,
                "comment_is_deleted": comment.get("isDeleted") or False,
                "published_date": comment.get("publishedDate"),
                "last_updated_date": comment.get("lastUpdatedDate"),
            })
    linked = []
    for item in work_items:
        if not isinstance(item, dict):
            continue
        fields = item.get("fields") or {}
        linked.append({
            "id": _number(item.get("id")),
            "title": fields.get("System.Title") or "",
            "type": fields.get("System.WorkItemType") or "",
            "state": fields.get("System.State") or "",
            "url": item.get("url"),
        })
    pull = pr if isinstance(pr, dict) else {}
    result = {
        "organization": organization,
        "project": project,
        "repository_id": repository_id,
        "pull_request_id": pull_request_id,
        "pull_request": {
            "id": pull.get("pullRequestId") if pull.get("pullRequestId") is not None else None,
            "title": pull.get("title") or "",
            "source_branch": pull.get("sourceRefName") or "",
            "target_branch": pull.get("targetRefName") or "",
            "status": pull.get("status") if pull.get("status") is not None else None,
            "creation_date": pull.get("creationDate") if pull.get("creationDate") is not None else None,
            "closed_date": pull.get("closedDate") if pull.get("closedDate") is not None else None,
        },
        "linked_work_items": linked,
        "thread_count": len(threads),
        "comment_count": sum(len(t.get("comments") or []) for t in threads if isinstance(t, dict)),
        "comments": comments,
        "raw_threads": threads if include_raw else None,
    }
    return result


def main(argv: list[str]) -> int:
    pull_request_url = ""
    organization = ""
    project = ""
    repository_id = ""
    pull_request_id = ""
    include_raw = False
    index = 0
    while index < len(argv):
        arg = argv[index]
        if arg in ("--include-raw-threads",):
            include_raw = True
            index += 1
        elif arg in ("--pull-request-url", "--organization", "--project", "--repository-id", "--pull-request-id"):
            if index + 1 >= len(argv):
                print(f"Unknown argument: {arg}", file=sys.stderr)
                return 1
            value = argv[index + 1]
            if arg == "--pull-request-url": pull_request_url = value
            elif arg == "--organization": organization = value
            elif arg == "--project": project = value
            elif arg == "--repository-id": repository_id = value
            else: pull_request_id = value
            index += 2
        else:
            print(f"Unknown argument: {arg}", file=sys.stderr)
            return 1
    if pull_request_url:
        parsed = lib.parse_pull_request_url(pull_request_url)
        if parsed is None:
            lib.emit_blocker(
                "INVALID_PR_URL",
                [lib.PR_URL_HINT],
                "Provide a valid Azure DevOps pull request URL or explicit identifiers.",
            )
        organization = organization or parsed["organization"]
        project = project or parsed["project"]
        repository_id = repository_id or parsed["repository_id"]
        pull_request_id = pull_request_id or parsed["pull_request_id"]
    missing = [name for name, value in (("organization", organization), ("project", project), ("repository_id", repository_id), ("pull_request_id", pull_request_id)) if not value]
    if missing:
        lib.emit_blocker("MISSING_INPUT", missing, "Provide a valid Azure DevOps pull request URL or explicit identifiers.")
    try:
        pr_id = int(pull_request_id)
    except (TypeError, ValueError):
        lib.emit_blocker("MISSING_INPUT", ["pull_request_id"], "Provide a valid Azure DevOps pull request URL or explicit identifiers.")
    base = f"https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repository_id}/pullRequests/{pr_id}"
    threads_response = _fetch(base + f"/threads?api-version={lib.API_VERSION}", "PR threads", f"Failed to fetch PR threads for pull request {pr_id} in {organization}/{project}/{repository_id} after bounded retries.")
    pr_response = _fetch(base + f"?api-version={lib.API_VERSION}", "pull request details", f"Failed to fetch pull request details for {pr_id} in {organization}/{project}/{repository_id} after bounded retries.")
    links_response = _fetch(base + f"/workitems?api-version={lib.API_VERSION}", "linked pull request work items", f"Failed to fetch linked pull request work items for {pr_id} in {organization}/{project}/{repository_id} after bounded retries.")
    link_values = links_response.get("value", []) if isinstance(links_response, dict) else []
    ids = [_number(item.get("id")) for item in link_values if isinstance(item, dict)]
    ids = [item for item in ids if item is not None]
    details = []
    for offset in range(0, len(ids), 100):
        csv = ",".join(str(item) for item in ids[offset:offset + 100])
        url = f"https://dev.azure.com/{organization}/{project}/_apis/wit/workitems?ids={quote(csv, safe='')}&fields=System.Title,System.WorkItemType,System.State&api-version={lib.API_VERSION}"
        batch = _fetch(url, "linked work item details", f"Failed to fetch linked work item details for {pr_id} in {organization}/{project}/{repository_id} after bounded retries.")
        if isinstance(batch, dict): details.extend(batch.get("value") or [])
    threads = threads_response.get("value", []) if isinstance(threads_response, dict) else []
    result = _flatten(threads, organization, project, repository_id, pr_id, pr_response if isinstance(pr_response, dict) else {}, details, include_raw)
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
