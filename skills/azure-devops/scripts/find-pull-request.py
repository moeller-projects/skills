#!/usr/bin/env python3
"""find-pull-request.py
Purpose: List Azure DevOps pull requests whose source branch matches a branch (GET only).
Inputs: --organization, --project, --repository-id, --source-branch; optional --status, --top.
Outputs: Candidate JSON on stdout; structured BLOCKER/ERROR output on stderr.
Side effects: Read-only Azure DevOps API request.
Requires Python 3.9+, standard library only. Run with: python scripts/find-pull-request.py
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from urllib.parse import quote

from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import _ado_lib as lib

STATUSES = ("active", "completed", "abandoned", "all")
DEFAULT_TOP = 20
MAX_TOP = 100


class _Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        print(message, file=sys.stderr)
        raise SystemExit(1)


def _int(value: object) -> int | None:
    try:
        if isinstance(value, bool) or value is None:
            return None
        return int(value)
    except (TypeError, ValueError):
        return None


def normalize_branch(value: str) -> str:
    branch = (value or "").strip()
    if branch.startswith("refs/heads/"):
        branch = branch[len("refs/heads/"):]
    invalid = not branch or branch == "HEAD" or len(branch) > 255
    invalid = invalid or any(ord(ch) < 32 or ord(ch) == 127 for ch in branch)
    if invalid:
        lib.emit_blocker(
            "MISSING_INPUT",
            ["a branch name (not detached HEAD)"],
            "Check out the branch that has the pull request, or provide the pull request URL or id.",
        )
    return "refs/heads/" + branch


def _candidate(pr: dict, web_base: str) -> dict:
    created = pr.get("createdBy") if isinstance(pr.get("createdBy"), dict) else {}
    pr_id = _int(pr.get("pullRequestId"))
    return {
        "pull_request_id": pr_id,
        "title": pr.get("title") or "",
        "status": pr.get("status"),
        "is_draft": pr.get("isDraft") if isinstance(pr.get("isDraft"), bool) else None,
        "source_branch": pr.get("sourceRefName") or "",
        "target_branch": pr.get("targetRefName") or "",
        "created_by": {
            "id": created.get("id"),
            "display_name": created.get("displayName"),
            "unique_name": created.get("uniqueName"),
        },
        "creation_date": pr.get("creationDate"),
        "url": f"{web_base}/pullrequest/{pr_id}" if pr_id is not None else None,
    }


def main(argv: list[str]) -> int:
    parser = _Parser(prog="find-pull-request.py", add_help=True)
    parser.add_argument("--organization", default=os.environ.get("ADO_ORGANIZATION", ""))
    parser.add_argument("--project", default=os.environ.get("ADO_PROJECT", ""))
    parser.add_argument("--repository-id", default=os.environ.get("ADO_REPOSITORY_ID", ""))
    parser.add_argument("--source-branch", default="")
    parser.add_argument("--status", choices=STATUSES, default="active")
    parser.add_argument("--top", type=int, default=DEFAULT_TOP)
    args = parser.parse_args(argv)

    missing = [
        name
        for name, value in (
            ("organization", args.organization),
            ("project", args.project),
            ("repository_id", args.repository_id),
            ("source_branch", args.source_branch),
        )
        if not value
    ]
    if missing:
        lib.emit_blocker("MISSING_INPUT", missing, "Provide the missing values to search for the pull request.")

    org = lib.quote_segment(args.organization, name="organization")
    project = lib.quote_segment(args.project, name="project")
    repo = lib.quote_segment(args.repository_id, name="repository_id")
    ref = normalize_branch(args.source_branch)
    top = max(1, min(args.top, MAX_TOP))
    url = (
        f"https://dev.azure.com/{org}/{project}/_apis/git/repositories/{repo}/pullrequests"
        f"?searchCriteria.sourceRefName={quote(ref, safe='')}"
        f"&searchCriteria.status={args.status}&$top={top}&api-version={lib.API_VERSION}"
    )
    response = lib.http_get_json(
        url,
        label="pull request search",
        error_code="FETCH_FAILED",
        error_message=f"Failed to search pull requests for {ref} in {args.organization}/{args.project}/{args.repository_id}.",
        error_recovery="Check AZURE_DEVOPS_PAT, identifiers, and network connectivity.",
    )
    items = response.get("value") if isinstance(response, dict) else None
    if not isinstance(items, list):
        lib.emit_error("PARSE_FAILED", "parse", "Unexpected pull request search response shape.", "Retry; if it persists, check the API version.")

    web_base = f"https://dev.azure.com/{org}/{project}/_git/{repo}"
    candidates = [_candidate(item, web_base) for item in items if isinstance(item, dict)]
    candidates.sort(key=lambda item: (item["pull_request_id"] is None, item["pull_request_id"] or 0))
    result = {
        "organization": args.organization,
        "project": args.project,
        "repository_id": args.repository_id,
        "source_branch": ref,
        "status_filter": args.status,
        "candidate_count": len(candidates),
        "truncated": len(items) >= top,
        "candidates": candidates,
    }
    print(json.dumps(lib.redact_value(result)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
