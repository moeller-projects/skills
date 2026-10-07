#!/usr/bin/env python3
"""emit-handoff.py
Purpose: Assemble the normalized handoff contract from pre-fetched input files and validate it before stdout.
Inputs: CLI flags and environment variables, plus optional normalized JSON files.
Outputs: Validated normalized handoff JSON on stdout; structured BLOCKER/ERROR output on stderr.
Side effects: Reads the supplied input files only.
Requires Python 3.9+, standard library only. Run with: python scripts/emit-handoff.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


def blocker(required: list[str], question: str) -> int:
    print("BLOCKER:", file=sys.stderr)
    print("code: MISSING_INPUT", file=sys.stderr)
    print("required_input:", file=sys.stderr)
    for item in required:
        print(f"- {item}", file=sys.stderr)
    print(f"next_question: {question}", file=sys.stderr)
    return 1


def jq_or(value: Any, fallback: Any) -> Any:
    return fallback if value is None or value is False else value


def parse_json_arg(value: str) -> Any:
    return json.loads(value)


def main(argv: list[str]) -> int:
    work_item_file = ""
    pr_comments_file = ""
    mode = ""
    organization = os.environ.get("ADO_ORGANIZATION", "")
    project = os.environ.get("ADO_PROJECT", "")
    repository_id = os.environ.get("ADO_REPOSITORY_ID", "")
    pull_request_id = os.environ.get("ADO_PULL_REQUEST_ID", "null")
    work_item_id = os.environ.get("ADO_WORK_ITEM_ID", "null")
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg in {"--work-item-file", "--pr-comments-file", "--mode", "--organization", "--project", "--repository-id", "--pull-request-id", "--work-item-id"}:
            if i + 1 >= len(argv):
                print(f"Unknown argument: {arg}", file=sys.stderr)
                return 1
            value = argv[i + 1]
            if arg == "--work-item-file": work_item_file = value
            elif arg == "--pr-comments-file": pr_comments_file = value
            elif arg == "--mode": mode = value
            elif arg == "--organization": organization = value
            elif arg == "--project": project = value
            elif arg == "--repository-id": repository_id = value
            elif arg == "--pull-request-id": pull_request_id = value
            else: work_item_id = value
            i += 2
        else:
            print(f"Unknown argument: {arg}", file=sys.stderr)
            return 1
    if not mode:
        if work_item_file and pr_comments_file: mode = "work-item-plus-pr-comments"
        elif work_item_file: mode = "work-item"
        elif pr_comments_file: mode = "pr-comments"
        else:
            return blocker(["--work-item-file and/or --pr-comments-file"], "Provide normalized input files to emit the handoff contract.")

    work_item: Any = {}
    pr_comments: Any = []
    pull_request: Any = {}
    linked_work_items: Any = []
    if work_item_file:
        with open(work_item_file, encoding="utf-8") as fh:
            work_item = json.load(fh)
    if pr_comments_file:
        with open(pr_comments_file, encoding="utf-8") as fh:
            source = json.load(fh)
        pr_comments = jq_or(source.get("comments") if isinstance(source, dict) else None, source)
        pull_request = jq_or(source.get("pull_request") if isinstance(source, dict) else None, {})
        linked_work_items = jq_or(source.get("linked_work_items") if isinstance(source, dict) else None, [])

    missing: list[str] = []
    warnings: list[str] = []
    status = "pass"
    if mode in {"work-item", "work-item-plus-pr-comments"} and not work_item_file:
        missing.append("work_item")
        status = "partial"
    if mode in {"pr-comments", "work-item-plus-pr-comments"} and not pr_comments_file:
        missing.append("pr_comments")
        status = "partial"
    wi_id = parse_json_arg(work_item_id)
    pr_id = parse_json_arg(pull_request_id)
    if mode in {"work-item", "work-item-plus-pr-comments"} and wi_id is None:
        if "source.work_item_id" not in missing: missing.append("source.work_item_id")
        status = "partial"
    if mode in {"pr-comments", "work-item-plus-pr-comments"} and pr_id is None:
        if "source.pull_request_id" not in missing: missing.append("source.pull_request_id")
        status = "partial"
    if mode in {"work-item", "work-item-plus-pr-comments"} and (not isinstance(work_item, dict) or len(work_item) == 0):
        if "work_item" not in missing: missing.append("work_item")
        status = "partial"
    if mode in {"work-item", "work-item-plus-pr-comments"} and not (work_item.get("title") or ""):
        if "work_item.title" not in missing: missing.append("work_item.title")
        status = "partial"
    if mode in {"work-item", "work-item-plus-pr-comments"} and not (work_item.get("description") or ""):
        if "work_item.description" not in missing: missing.append("work_item.description")
        status = "partial"
    if mode in {"work-item", "work-item-plus-pr-comments"} and not (work_item.get("acceptance_criteria") or ""):
        warnings.append("acceptance criteria missing")
    if mode in {"pr-comments", "work-item-plus-pr-comments"} and (not isinstance(pr_comments, list) or len(pr_comments) == 0):
        if "pr_comments" not in missing: missing.append("pr_comments")
        status = "partial"
    if mode in {"pr-comments", "work-item-plus-pr-comments"} and not (pull_request.get("source_branch") if isinstance(pull_request, dict) else ""):
        if "pull_request.source_branch" not in missing: missing.append("pull_request.source_branch")
        status = "partial"
    if mode in {"pr-comments", "work-item-plus-pr-comments"} and not (pull_request.get("target_branch") if isinstance(pull_request, dict) else ""):
        if "pull_request.target_branch" not in missing: missing.append("pull_request.target_branch")
        status = "partial"

    contract = {"contract_version":"1.0.0", "producer":"ado-gateway", "consumer":"spec-engine", "artifact_type":"ado-normalized", "mode":mode,
      "source":{"platform":"azure-devops", "organization":organization, "project":project, "repository_id":repository_id, "pull_request_id":pr_id, "work_item_id":wi_id, "read_only":True},
      "normalization":{"status":status, "missing_fields":missing, "warnings":warnings, "html_stripped":True, "secret_redactions_applied":True},
      "work_item":work_item, "pr_comments":pr_comments, "pull_request":pull_request, "linked_work_items":linked_work_items}
    validator = Path(__file__).with_name("validate-handoff.py")
    result = subprocess.run([sys.executable, str(validator)], input=json.dumps(contract), text=True, capture_output=True)
    if result.stdout: sys.stdout.write(result.stdout)
    if result.stderr: sys.stderr.write(result.stderr)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
