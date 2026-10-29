#!/usr/bin/env python3
"""generate-handoff.py
Purpose: Fetch Azure DevOps source data, normalize it, and emit the shared handoff contract.
Inputs: CLI flags and environment variables identifying work items, PRs, and mode.
Outputs: Normalized handoff JSON on stdout; structured BLOCKER output on stderr when inputs are missing.
Side effects: Creates and removes temporary files and directories only.
Requires Python 3.9+, standard library only. Run with: python scripts/generate-handoff.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _ado_lib as lib


def blocker(required: list[str], question: str) -> int:
    lib.emit_blocker("MISSING_INPUT", required, question)
    return 1


def main(argv: list[str]) -> int:
    if "--help" in argv:
        print("usage: generate-handoff.py [--pull-request-url URL] [--organization ORG] [--project PROJECT] [--repository-id ID] [--pull-request-id ID] [--work-item-id ID] [--mode MODE]")
        return 0
    script_dir = Path(__file__).resolve().parent
    pull_request_url = ""
    organization = os.environ.get("ADO_ORGANIZATION", "")
    project = os.environ.get("ADO_PROJECT", "")
    repository_id = os.environ.get("ADO_REPOSITORY_ID", "")
    pull_request_id = os.environ.get("ADO_PULL_REQUEST_ID", "")
    work_item_id = os.environ.get("ADO_WORK_ITEM_ID", "")
    mode = ""
    i = 0
    options = {"--pull-request-url", "--organization", "--project", "--repository-id", "--pull-request-id", "--work-item-id", "--mode"}
    while i < len(argv):
        arg = argv[i]
        if arg in options:
            if i + 1 >= len(argv):
                print(f"Unknown argument: {arg}", file=sys.stderr)
                return 1
            value = argv[i + 1]
            if arg == "--pull-request-url": pull_request_url = value
            elif arg == "--organization": organization = value
            elif arg == "--project": project = value
            elif arg == "--repository-id": repository_id = value
            elif arg == "--pull-request-id": pull_request_id = value
            elif arg == "--work-item-id": work_item_id = value
            else: mode = value
            i += 2
        else:
            print(f"Unknown argument: {arg}", file=sys.stderr)
            return 1
    if pull_request_url:
        parsed = lib.parse_pull_request_url(pull_request_url)
        if parsed is None:
            lib.emit_blocker("INVALID_PR_URL", [lib.PR_URL_HINT], "Provide a valid Azure DevOps pull request URL or explicit identifiers.")
        if not organization: organization = parsed["organization"]
        if not project: project = parsed["project"]
        if not repository_id: repository_id = parsed["repository_id"]
        if not pull_request_id: pull_request_id = str(parsed["pull_request_id"])
    if not mode:
        if work_item_id and pull_request_id: mode = "work-item-plus-pr-comments"
        elif work_item_id: mode = "work-item"
        elif pull_request_id: mode = "pr-comments"
        else:
            return blocker(["work_item_id and/or pull_request_id"], "Provide a work item id, a pull request id, or a pull request URL.")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        warnings: list[str] = []
        work_item_file = ""
        pr_comments_file = ""
        if mode in {"work-item", "work-item-plus-pr-comments"}:
            missing = [name for name, value in (("organization", organization), ("project", project), ("work_item_id", work_item_id)) if not value]
            if missing:
                return blocker(missing, "Provide organization, project, and work item id before fetching the work item.")
            raw_file = tmp_dir / "work-item-raw.json"
            normalized_file = tmp_dir / "work-item-normalized.json"
            fetch = script_dir / "fetch-work-item.py"
            normalize = script_dir / "normalize-work-item.py"
            with raw_file.open("w", encoding="utf-8") as out:
                result = subprocess.run([sys.executable, str(fetch), organization, project, work_item_id], stdout=out, stderr=subprocess.PIPE, text=True, shell=False)
            if result.returncode and "BLOCKER:" in result.stderr:
                sys.stderr.write(result.stderr)
                return result.returncode
            if result.returncode == 0:
                with normalized_file.open("w", encoding="utf-8") as out, raw_file.open("r", encoding="utf-8") as inp:
                    result = subprocess.run([sys.executable, str(normalize)], stdin=inp, stdout=out, stderr=subprocess.PIPE, text=True, shell=False)
                if result.returncode:
                    if mode == "work-item":
                        if result.stderr:
                            sys.stderr.write(result.stderr)
                        return result.returncode
                    warning = "work-item normalization failed; handoff is partial"
                    warnings.append(warning)
                    print(f"WARNING: {warning}.", file=sys.stderr)
                    if result.stderr:
                        print(result.stderr, file=sys.stderr)
                    normalized_file.unlink(missing_ok=True)
                else:
                    work_item_file = str(normalized_file)
            elif result.stderr:
                if mode == "work-item":
                    sys.stderr.write(result.stderr)
                    return result.returncode
                warning = "work-item source unavailable; handoff is partial"
                warnings.append(warning)
                print(f"WARNING: {warning}.", file=sys.stderr)
                print(result.stderr, file=sys.stderr)
            if not work_item_file:
                raw_file.unlink(missing_ok=True)
                normalized_file.unlink(missing_ok=True)
        if mode in {"pr-comments", "work-item-plus-pr-comments"}:
            comments_file = tmp_dir / "pr-comments.json"
            fetch = script_dir / "fetch-pr-comments.py"
            with comments_file.open("w", encoding="utf-8") as out:
                result = subprocess.run([sys.executable, str(fetch), "--organization", organization, "--project", project, "--repository-id", repository_id, "--pull-request-id", str(pull_request_id)], stdout=out, stderr=subprocess.PIPE, text=True, shell=False)
            if result.returncode and "BLOCKER:" in result.stderr:
                sys.stderr.write(result.stderr)
                return result.returncode
            if result.returncode == 0:
                pr_comments_file = str(comments_file)
            else:
                if mode == "pr-comments":
                    if result.stderr:
                        sys.stderr.write(result.stderr)
                    return result.returncode
                warning = "PR source unavailable; handoff is partial"
                warnings.append(warning)
                print(f"WARNING: {warning}.", file=sys.stderr)
                if result.stderr:
                    print(result.stderr, file=sys.stderr)
                comments_file.unlink(missing_ok=True)
        args = [sys.executable, str(script_dir / "emit-handoff.py"), "--mode", mode, "--organization", organization, "--project", project, "--repository-id", repository_id]
        if work_item_id: args += ["--work-item-id", work_item_id]
        if pull_request_id: args += ["--pull-request-id", pull_request_id]
        if work_item_file: args += ["--work-item-file", work_item_file]
        if pr_comments_file: args += ["--pr-comments-file", pr_comments_file]
        for warning in warnings:
            args += ["--warning", warning]
        if not work_item_file and not pr_comments_file:
            lib.emit_error(
                "FETCH_FAILED",
                "fetch",
                "No requested Azure DevOps source could be fetched.",
                "Resolve the source fetch failure and retry; no partial handoff was emitted.",
            )
        result = subprocess.run(args, shell=False)
        return result.returncode


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
