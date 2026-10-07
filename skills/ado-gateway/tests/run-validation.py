#!/usr/bin/env python3
"""run-validation.py

Purpose: Executable validation harness for ado-gateway.
Inputs: Repository working tree containing the ado-gateway skill directory.
Outputs: PASS lines to stdout; FAIL to stderr with exit code 1 on the first failure.
Side effects: Creates and removes temporary files only; no network calls.

Requires Python 3.9+, standard library only. Run with: python tests/run-validation.py
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
EXAMPLES_DIR = SKILL_DIR / "assets" / "examples"

NO_PAT_ENV = {k: v for k, v in os.environ.items() if k != "AZURE_DEVOPS_PAT"}

SCRIPT_TIMEOUT_SECONDS = 30


def passed(message: str) -> None:
    print(f"PASS: {message}")


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    sys.exit(1)


def run_script(
    name: str,
    *args: str,
    stdin_text: str | None = None,
    env: dict | None = None,
) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / name), *args],
        input=stdin_text,
        capture_output=True,
        text=True,
        env=env,
        timeout=SCRIPT_TIMEOUT_SECONDS,
    )


def run_validator(stdin_text: str) -> subprocess.CompletedProcess:
    return run_script("validate-handoff.py", stdin_text=stdin_text)


def expect_ok(result: subprocess.CompletedProcess, message: str) -> None:
    if result.returncode != 0:
        fail(f"{message} (exit {result.returncode}): {result.stderr.strip()}")


def expect_fail_with(result: subprocess.CompletedProcess, needle: str, message: str) -> None:
    if result.returncode == 0:
        fail(message)
    if needle not in result.stderr:
        fail(f"{message} — stderr missing '{needle}': {result.stderr.strip()}")


def main() -> None:
    for script in [
        "ensure-env.py",
        "parse-pr-url.py",
        "normalize-work-item.py",
        "emit-handoff.py",
        "validate-handoff.py",
        "_ado_lib.py",
        "create-work-item.py",
        "create-work-item-comment.py",
        "create-pull-request.py",
        "create-pr-comment.py",
        "format-work-item-mention.py",
        "resolve-ado-user.py",
        "fetch-work-item.py",
        "fetch-pr-comments.py",
        "generate-handoff.py",
    ]:
        if not (SCRIPTS_DIR / script).is_file():
            fail(f"missing {script}")
    passed("required local scripts exist")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)

        for example in sorted(EXAMPLES_DIR.glob("*.json")):
            result = run_validator(example.read_text(encoding="utf-8"))
            expect_ok(result, f"schema-valid example {example.name} rejected")
            passed(f"schema-valid example {example.name}")

        parsed = run_script(
            "parse-pr-url.py",
            "https://dev.azure.com/example-org/example-project/_git/example-repo/pullrequest/123",
        )
        expect_ok(parsed, "parse-pr-url failed on a valid URL")
        identifiers = json.loads(parsed.stdout)
        if identifiers["organization"] != "example-org":
            fail("PR URL organization parse failed")
        if identifiers["project"] != "example-project":
            fail("PR URL project parse failed")
        if identifiers["repository_id"] != "example-repo":
            fail("PR URL repository parse failed")
        if identifiers["pull_request_id"] != 123:
            fail("PR URL id parse failed")
        passed("PR URL parsing is deterministic")

        invalid = run_script("parse-pr-url.py", "https://github.com/org/repo/pull/1")
        expect_fail_with(
            invalid,
            "code: INVALID_PR_URL",
            "invalid PR URL unexpectedly succeeded",
        )
        passed("invalid PR URLs produce blocker output")

        malformed_with_identifiers = run_script(
            "fetch-pr-comments.py",
            "--pull-request-url", "https://github.com/org/repo/pull/1",
            "--organization", "example-org",
            "--project", "example-project",
            "--repository-id", "example-repo",
            "--pull-request-id", "123",
        )
        expect_fail_with(
            malformed_with_identifiers,
            "code: INVALID_PR_URL",
            "malformed PR URL was ignored in favor of explicit identifiers",
        )
        passed("malformed PR URL is rejected even with explicit identifiers")

        work_item_raw = {
            "id": 1234,
            "fields": {
                "System.WorkItemType": "User Story",
                "System.Title": "Checkout supports discount codes",
                "System.Description": "<p>Add <b>discount</b> code support.</p>",
                "Microsoft.VSTS.Common.AcceptanceCriteria": "<ul><li>Apply valid code</li></ul>",
                "System.Tags": "checkout;discount",
                "System.State": "New",
            },
        }
        normalized = run_script(
            "normalize-work-item.py", stdin_text=json.dumps(work_item_raw)
        )
        expect_ok(normalized, "normalize-work-item failed on fixture")
        normalized_json = json.loads(normalized.stdout)
        if not isinstance(normalized_json["id"], int):
            fail("work_item.id must be numeric")
        if normalized_json["description"] != "Add discount code support.":
            fail("HTML description normalization failed")
        passed("work item normalization keeps numeric id and strips HTML")

        bad_example = json.loads(
            (EXAMPLES_DIR / "work-item-only.json").read_text(encoding="utf-8")
        )
        bad_example["work_item"]["id"] = "1234"
        rejected = run_validator(json.dumps(bad_example))
        expect_fail_with(
            rejected,
            "stage: emit",
            "schema accepted string work_item.id",
        )
        passed("schema rejects stringified work_item.id")

        work_item_file = tmp_dir / "work-item-normalized.json"
        work_item_file.write_text(normalized.stdout, encoding="utf-8")
        handoff = run_script(
            "emit-handoff.py",
            "--mode", "work-item",
            "--organization", "example-org",
            "--project", "example-project",
            "--work-item-id", "1234",
            "--work-item-file", str(work_item_file),
        )
        expect_ok(handoff, "emit-handoff work-item mode failed")
        handoff_json = json.loads(handoff.stdout)
        validated = run_validator(handoff.stdout)
        expect_ok(validated, "emitted work-item handoff failed schema validation")
        if not isinstance(handoff_json["source"]["work_item_id"], int):
            fail("source.work_item_id must be numeric")
        if not isinstance(handoff_json["work_item"]["id"], int):
            fail("emitted work_item.id must be numeric")
        passed("emit path validates schema and preserves numeric ids")


        mention = run_script(
            "format-work-item-mention.py",
            "--mention-id", "aad.1234",
            "--display-name", "Ada Lovelace",
        )
        expect_ok(mention, "mention helper failed")
        if mention.stdout.rstrip("\n") != '<a href="#" data-vss-mention="version:2.0,{aad.1234}">@Ada Lovelace</a>':
            fail("mention helper markup output mismatch")
        passed("mention helper emits deterministic markup")


        wi_plan = run_script(
            "create-work-item.py",
            "--organization", "example-org",
            "--project", "example-project",
            "--type", "Bug",
            "--title", "Bug title",
            "--description", "Bug description",
        )
        expect_ok(wi_plan, "create-work-item dry-run failed")
        wi_plan_json = json.loads(wi_plan.stdout)
        if wi_plan_json["dry_run"] is not True:
            fail("work-item dry-run did not mark dry_run=true")
        if wi_plan_json["method"] != "POST":
            fail("work-item dry-run method must be POST")
        if wi_plan_json["body"][0]["path"] != "/fields/System.Title":
            fail("work-item dry-run missing title patch")
        bug_fields = {operation["path"]: operation["value"] for operation in wi_plan_json["body"]}
        if bug_fields.get("/fields/Microsoft.VSTS.TCM.ReproSteps") != "Bug description":
            fail("Bug description must populate repro steps")
        if "/fields/System.Description" in bug_fields:
            fail("Bug description must not populate System.Description")
        task_plan = run_script(
            "create-work-item.py",
            "--organization", "example-org",
            "--project", "example-project",
            "--type", "Task",
            "--title", "Task title",
            "--description", "Task description",
        )
        expect_ok(task_plan, "create-work-item Task dry-run failed")
        task_fields = {operation["path"]: operation["value"] for operation in json.loads(task_plan.stdout)["body"]}
        if task_fields.get("/fields/System.Description") != "Task description":
            fail("Task description must populate System.Description")
        if "/fields/Microsoft.VSTS.TCM.ReproSteps" in task_fields:
            fail("Task description must not populate repro steps")
        passed("create-work-item dry-run produces deterministic action plan")

        pr_plan = run_script(
            "create-pull-request.py",
            "--organization", "example-org",
            "--project", "example-project",
            "--repository-id", "example-repo",
            "--source-branch", "feature/demo",
            "--target-branch", "main",
            "--title", "PR title",
            "--description", "PR description",
        )
        expect_ok(pr_plan, "create-pull-request dry-run failed")
        pr_plan_json = json.loads(pr_plan.stdout)
        if pr_plan_json["dry_run"] is not True:
            fail("pull-request dry-run did not mark dry_run=true")
        if pr_plan_json["body"]["sourceRefName"] != "refs/heads/feature/demo":
            fail("pull-request dry-run did not normalize source branch")
        passed("create-pull-request dry-run produces deterministic action plan")

        wi_comment_plan = run_script(
            "create-work-item-comment.py",
            "--organization", "example-org",
            "--project", "example-project",
            "--work-item-id", "456",
            "--text", "<p>Looks good</p>",
        )
        expect_ok(wi_comment_plan, "create-work-item-comment dry-run failed")
        wi_comment_json = json.loads(wi_comment_plan.stdout)
        if wi_comment_json["dry_run"] is not True:
            fail("work-item comment dry-run did not mark dry_run=true")
        if wi_comment_json["method"] != "POST":
            fail("work-item comment dry-run method must be POST")
        if wi_comment_json["body"]["text"] != "<p>Looks good</p>":
            fail("work-item comment dry-run body text mismatch")
        passed("create-work-item-comment dry-run produces deterministic action plan")

        comment_plan = run_script(
            "create-pr-comment.py",
            "--mode", "thread",
            "--organization", "example-org",
            "--project", "example-project",
            "--repository-id", "example-repo",
            "--pull-request-id", "123",
            "--content", "Review comment",
            "--file-path", "/src/order.ts",
            "--line", "42",
        )
        expect_ok(comment_plan, "create-pr-comment dry-run failed")
        comment_json = json.loads(comment_plan.stdout)
        if comment_json["dry_run"] is not True:
            fail("PR comment dry-run did not mark dry_run=true")
        if comment_json["body"]["threadContext"]["filePath"] != "/src/order.ts":
            fail("PR comment dry-run missing inline file path")
        if comment_json["body"]["threadContext"]["rightFileStart"]["line"] != 42:
            fail("PR comment dry-run wrong start line")
        if comment_json["body"]["threadContext"]["rightFileEnd"]["line"] != 42:
            fail("PR comment dry-run end line should default to start line")
        passed("create-pr-comment dry-run produces deterministic inline action plan")

        range_plan = run_script(
            "create-pr-comment.py",
            "--mode", "thread",
            "--organization", "example-org",
            "--project", "example-project",
            "--repository-id", "example-repo",
            "--pull-request-id", "123",
            "--content", "Range comment",
            "--file-path", "src/order.ts",
            "--line", "10",
            "--end-line", "20",
        )
        expect_ok(range_plan, "create-pr-comment range dry-run failed")
        range_json = json.loads(range_plan.stdout)
        if range_json["dry_run"] is not True:
            fail("PR comment range dry-run did not mark dry_run=true")
        if range_json["body"]["threadContext"]["filePath"] != "/src/order.ts":
            fail("PR comment range dry-run did not normalize file path to repo-root format")
        if range_json["body"]["threadContext"]["rightFileStart"]["line"] != 10:
            fail("PR comment range dry-run wrong start line")
        if range_json["body"]["threadContext"]["rightFileEnd"]["line"] != 20:
            fail("PR comment range dry-run wrong end line")
        passed("create-pr-comment dry-run produces deterministic multi-line range action plan")

        pr_comments_normalized = {
            "comments": [
                {
                    "thread_id": 1,
                    "comment_id": 1,
                    "parent_comment_id": 0,
                    "author": "Reviewer",
                    "content": "Looks good",
                    "file_path": "/src/order.ts",
                    "side": "right",
                    "start_line": 10,
                    "end_line": 10,
                    "start_offset": 1,
                    "end_offset": 1,
                    "thread_status": "active",
                    "thread_is_deleted": False,
                    "comment_is_deleted": False,
                    "published_date": "2026-04-29T08:00:00Z",
                    "last_updated_date": "2026-04-29T08:00:00Z",
                }
            ],
            "pull_request": {
                "id": 123,
                "title": "Demo PR",
                "source_branch": "refs/heads/feature/demo",
                "target_branch": "refs/heads/main",
                "status": "active",
                "creation_date": "2026-04-29T08:00:00Z",
                "closed_date": None,
            },
            "linked_work_items": [
                {
                    "id": 456,
                    "title": "Demo work item",
                    "type": "User Story",
                    "state": "Active",
                    "url": "https://dev.azure.com/example-org/example-project/_apis/wit/workItems/456",
                }
            ],
        }
        pr_comments_file = tmp_dir / "pr-comments-normalized.json"
        pr_comments_file.write_text(json.dumps(pr_comments_normalized), encoding="utf-8")

        pr_handoff = run_script(
            "emit-handoff.py",
            "--mode", "pr-comments",
            "--organization", "example-org",
            "--project", "example-project",
            "--repository-id", "example-repo",
            "--pull-request-id", "123",
            "--pr-comments-file", str(pr_comments_file),
        )
        expect_ok(pr_handoff, "emit-handoff pr-comments mode failed")
        pr_handoff_json = json.loads(pr_handoff.stdout)
        validated_pr = run_validator(pr_handoff.stdout)
        expect_ok(validated_pr, "emitted pr-comments handoff failed schema validation")
        if pr_handoff_json["pull_request"]["source_branch"] != "refs/heads/feature/demo":
            fail("handoff missing pull_request.source_branch")
        if pr_handoff_json["pull_request"]["target_branch"] != "refs/heads/main":
            fail("handoff missing pull_request.target_branch")
        if pr_handoff_json["linked_work_items"][0]["id"] != 456:
            fail("handoff missing linked work item details")
        passed("emit path includes PR branch metadata and linked work item details")

        base_comment_args = [
            "--mode", "thread",
            "--organization", "example-org",
            "--project", "example-project",
            "--repository-id", "example-repo",
            "--pull-request-id", "123",
            "--content", "x",
        ]

        inverted = run_script(
            "create-pr-comment.py", *base_comment_args,
            "--file-path", "src/order.ts", "--line", "20", "--end-line", "10",
        )
        expect_fail_with(
            inverted,
            "end-line must be greater than or equal to",
            "end-line < line unexpectedly succeeded",
        )
        passed("create-pr-comment rejects end-line less than line")

        endline_no_file = run_script(
            "create-pr-comment.py", *base_comment_args, "--end-line", "5",
        )
        expect_fail_with(
            endline_no_file,
            "end-line requires --file-path",
            "--end-line without --file-path unexpectedly succeeded",
        )
        passed("create-pr-comment rejects --end-line without --file-path")

        root_only = run_script(
            "create-pr-comment.py", *base_comment_args,
            "--file-path", "/", "--line", "1",
        )
        expect_fail_with(
            root_only,
            "must include a file path under the repository root",
            "root-only --file-path unexpectedly succeeded",
        )
        passed("create-pr-comment rejects root-only file paths")

        traversal = run_script(
            "create-pr-comment.py", *base_comment_args,
            "--file-path", "/src/../secrets.txt", "--line", "1",
        )
        expect_fail_with(
            traversal,
            "must stay within the repository root",
            "path traversal --file-path unexpectedly succeeded",
        )
        passed("create-pr-comment rejects file paths with traversal segments")

        trailing_traversal = run_script(
            "create-pr-comment.py", *base_comment_args,
            "--file-path", "/src/..", "--line", "1",
        )
        expect_fail_with(
            trailing_traversal,
            "must stay within the repository root",
            "trailing path traversal --file-path unexpectedly succeeded",
        )
        passed("create-pr-comment rejects trailing traversal segments")

        unc_path = run_script(
            "create-pr-comment.py", *base_comment_args,
            "--file-path", "\\\\server\\share\\file.ts", "--line", "1",
        )
        expect_fail_with(
            unc_path,
            "must be repo-root-relative and start with",
            "UNC absolute --file-path unexpectedly succeeded",
        )
        passed("create-pr-comment rejects UNC absolute file paths")

        drive_path = run_script(
            "create-pr-comment.py", *base_comment_args,
            "--file-path", "C:\\repo\\file.ts", "--line", "1",
        )
        expect_fail_with(
            drive_path,
            "must be repo-root-relative and start with",
            "Windows drive --file-path unexpectedly succeeded",
        )
        passed("create-pr-comment rejects Windows drive absolute file paths")

        write_without_pat = run_script(
            "create-work-item.py",
            "--organization", "example-org",
            "--project", "example-project",
            "--type", "Bug",
            "--title", "Bug title",
            "--confirm",
            env=NO_PAT_ENV,
        )
        expect_fail_with(
            write_without_pat,
            "code: MISSING_AUTH",
            "write execution without PAT unexpectedly succeeded",
        )
        passed("write execution requires --confirm and AZURE_DEVOPS_PAT")

    print("\nADO Gateway validation completed successfully.")


if __name__ == "__main__":
    main()
