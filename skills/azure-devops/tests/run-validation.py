#!/usr/bin/env python3
"""run-validation.py

Purpose: Executable validation harness for azure-devops.
Inputs: Repository working tree containing the azure-devops skill directory.
Outputs: PASS lines to stdout; FAIL to stderr with exit code 1 on the first failure.
Side effects: Creates and removes temporary files only; no network calls.

Requires Python 3.9+, standard library only. Run with: python tests/run-validation.py
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
EXAMPLES_DIR = SKILL_DIR / "assets" / "examples"
GOLDENS_PATH = SKILL_DIR / "tests" / "goldens.json"
sys.path.insert(0, str(SCRIPTS_DIR))

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


def check_dry_run_goldens() -> None:
    """Compare write-script dry runs against the pre-refactor baseline."""
    data = json.loads(GOLDENS_PATH.read_text(encoding="utf-8"))
    for fixture in data["fixtures"]:
        result = run_script(fixture["script"], *fixture["argv"], env=NO_PAT_ENV)
        expect_ok(result, f"golden dry-run {fixture['name']} failed")
        actual = json.loads(result.stdout)
        if actual != fixture["expected"]:
            fail(
                f"golden dry-run {fixture['name']} output changed:\n"
                f"  expected: {json.dumps(fixture['expected'], sort_keys=True)}\n"
                f"  actual:   {json.dumps(actual, sort_keys=True)}"
            )
        passed(f"golden dry-run {fixture['name']} unchanged")


def main() -> None:
    for script in [
        "ensure-env.py",
        "parse-pr-url.py",
        "parse-git-remote.py",
        "find-pull-request.py",
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

    check_dry_run_goldens()

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
            "comments": [
                {
                    "id": 9,
                    "text": "<p>Steps tried: <b>restart</b></p>",
                    "createdBy": {"displayName": "Test Author"},
                    "createdDate": "2026-10-01T12:00:00Z",
                    "modifiedDate": "2026-10-02T12:00:00Z",
                }
            ],
            "updates": [
                {
                    "id": 11,
                    "rev": 2,
                    "revisedBy": {"displayName": "Casey Smith"},
                    "revisedDate": "2026-10-01T12:00:00Z",
                    "fields": {
                        "System.State": {"oldValue": "New", "newValue": "Active"},
                        "System.Description": {
                            "oldValue": "<p>Old text</p>",
                            "newValue": "<p>Updated text</p>",
                        },
                    },
                },
                {
                    "id": 12,
                    "rev": 2,
                    "revisedBy": {"displayName": "Casey Smith"},
                    "revisedDate": "2026-10-01T12:01:00Z",
                    "fields": {},
                },
                {
                    "id": 13,
                    "rev": 3,
                    "fields": {"System.Title": {"newValue": "New title"}},
                },
            ],
            "relations": [
                {
                    "rel": "System.LinkTypes.Related",
                    "url": "https://dev.azure.com/example-org/example-project/_apis/wit/workItems/5678",
                    "attributes": {"name": "Related"},
                },
                {
                    "rel": "System.LinkTypes.Hierarchy-Forward",
                    "url": "https://dev.azure.com/example-org/example-project/_apis/wit/workItems/6789",
                    "attributes": {"name": "Child"},
                },
            ],
            "fields": {
                "System.WorkItemType": "Bug",
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
        comment = normalized_json["comments"][0]
        if comment != {
            "id": 9,
            "author": "Test Author",
            "content": "Steps tried: restart",
            "created_date": "2026-10-01T12:00:00Z",
            "modified_date": "2026-10-02T12:00:00Z",
        }:
            fail("work-item comment fields were not normalized")
        history = normalized_json["history"]
        if len(history) != 3 or history[0]["revision"] != history[1]["revision"]:
            fail("work-item history must preserve distinct updates sharing a revision")
        if history[0]["changed_fields"] != [
            {"reference_name": "System.State", "old_value": "New", "new_value": "Active"},
            {"reference_name": "System.Description", "old_value": "Old text", "new_value": "Updated text"},
        ]:
            fail("work-item history changed fields were not normalized")
        if history[1]["changed_fields"] != []:
            fail("work-item history must preserve updates with no field changes")
        if "old_value" in history[2]["changed_fields"][0]:
            fail("missing historical old values must remain absent")
        related_work = normalized_json["related_work"]
        if len(related_work) != 1 or related_work[0]["rel"] != "System.LinkTypes.Related":
            fail("work-item related work must exclude other relation types")
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
        bad_path = json.loads((EXAMPLES_DIR / "work-item-only.json").read_text(encoding="utf-8"))
        bad_path["source"]["repository_id"] = "repo/with-traversal"
        rejected_path = run_validator(json.dumps(bad_path))
        expect_fail_with(rejected_path, "pattern", "schema accepted unsafe repository identifier")
        passed("schema rejects unsafe repository identifiers")

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
                    "author_id": "reviewer-id",
                    "author_unique_name": "reviewer@example.com",
                    "comment_type": "text",
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
                "created_by": {
                    "id": "author-id",
                    "display_name": "Author",
                    "unique_name": "author@example.com",
                },
                "is_draft": False,
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
        legacy_handoff = json.loads(pr_handoff.stdout)
        for key in ("author_id", "author_unique_name", "comment_type"):
            legacy_handoff["pr_comments"][0].pop(key)
        legacy_handoff["pull_request"].pop("created_by")
        legacy_handoff["pull_request"].pop("is_draft")
        expect_ok(run_validator(json.dumps(legacy_handoff)), "legacy PR handoff without optional metadata was rejected")
        if pr_handoff_json["pr_comments"][0]["author_id"] != "reviewer-id" or pr_handoff_json["pr_comments"][0]["comment_type"] != "text":
            fail("handoff omitted optional PR comment metadata")
        if pr_handoff_json["pull_request"]["created_by"]["id"] != "author-id" or pr_handoff_json["pull_request"]["is_draft"] is not False:
            fail("handoff omitted optional PR creator or draft metadata")
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
        import _ado_lib as ado_lib
        class _Response:
            def __enter__(self): return self
            def __exit__(self, *_): return False
            def read(self): return b"{}"
        class _Opener:
            def __init__(self): self.calls = 0
            def open(self, request, timeout):
                self.calls += 1
                if request.method == "POST":
                    raise urllib.error.URLError("ambiguous")
                if self.calls == 1:
                    raise urllib.error.URLError("transient")
                return _Response()
        import urllib.error
        opener = _Opener()
        old_opener, old_pat, old_sleep = ado_lib._HTTP_OPENER, ado_lib.require_pat, ado_lib.time.sleep
        ado_lib._HTTP_OPENER = opener
        ado_lib.require_pat = lambda: "test-current-pat"
        ado_lib.time.sleep = lambda _: None
        try:
            ado_lib.http_get_json("https://dev.azure.com/org/project/_apis/test", label="test", error_code="FETCH_FAILED", error_message="failed", error_recovery="retry")
            if opener.calls != 2:
                fail("GET retry did not retry transient transport failure")
            post_before = opener.calls
            try:
                ado_lib.http_write_json("POST", "application/json", "https://dev.azure.com/org/project/_apis/test", b"{}", label="test")
            except SystemExit:
                pass
            else:
                fail("ambiguous POST transport failure unexpectedly succeeded")
            if opener.calls - post_before != 1:
                fail("ambiguous POST transport failure was replayed")
        finally:
            ado_lib._HTTP_OPENER, ado_lib.require_pat, ado_lib.time.sleep = old_opener, old_pat, old_sleep
        passed("mocked GET retry and non-replayed ambiguous POST transport paths")
        os.environ["AZURE_DEVOPS_PAT"] = "test-current-pat"
        redacted = ado_lib.redact_value({"title": "test-current-pat", "nested": ["Bearer abc.def"]})
        if redacted["title"] != "[REDACTED]" or "[REDACTED]" not in redacted["nested"][0]:
            fail("recursive credential redaction regression")
        passed("recursive current PAT and bearer redaction")
        old_pat = os.environ.get("AZURE_DEVOPS_PAT")
        os.environ["AZURE_DEVOPS_PAT"] = "ordinary-current-pat"
        old_format = "A" * 52
        new_format = "B" * 75 + "AZDO" + "C" * 5
        ordinary_84 = "D" * 84
        plain = ado_lib.redact_text(f"{old_format} {new_format} {ordinary_84} ordinary-identifier")
        if plain != f"[REDACTED] [REDACTED] {ordinary_84} ordinary-identifier":
            fail("plain Azure PAT format redaction regression")
        if old_pat is None:
            os.environ.pop("AZURE_DEVOPS_PAT", None)
        else:
            os.environ["AZURE_DEVOPS_PAT"] = old_pat
        passed("52- and 84-character Azure PAT redaction preserves ordinary identifiers")
        spec = importlib.util.spec_from_file_location("fetch_work_item_regression", SCRIPTS_DIR / "fetch-work-item.py")
        fetch_module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(fetch_module)
        responses = iter([
            {"id": 7, "fields": {}},
            {"value": []},
            {"comments": [{"id": 1, "text": "first"}], "continuationToken": "next"},
            {"comments": [{"id": 2, "text": "second"}]},
        ])
        old_fetch = fetch_module.lib.http_get_json
        old_require = fetch_module.lib.require_pat
        fetch_module.lib.http_get_json = lambda *args, **kwargs: next(responses)
        fetch_module.lib.require_pat = lambda: "test"
        captured = io.StringIO()
        old_argv = sys.argv
        try:
            sys.argv = ["fetch-work-item.py", "org", "project", "7"]
            with contextlib.redirect_stdout(captured):
                fetch_module.main()
        finally:
            sys.argv = old_argv
            fetch_module.lib.http_get_json = old_fetch
            fetch_module.lib.require_pat = old_require
        fetched = json.loads(captured.getvalue())
        if [item["id"] for item in fetched["comments"]] != [1, 2]:
            fail("work-item comment continuation pagination regression")
        passed("mocked work-item fetch preserves two comment pages")
        malformed = iter([{"id": 7, "fields": {}}, {"value": []}, {}])
        fetch_module.lib.http_get_json = lambda *args, **kwargs: next(malformed)
        try:
            sys.argv = ["fetch-work-item.py", "org", "project", "7"]
            fetch_module.main()
        except SystemExit:
            pass
        else:
            fail("malformed comments page was accepted as complete")
        finally:
            sys.argv = old_argv
            fetch_module.lib.http_get_json = old_fetch
        passed("mocked work-item fetch rejects malformed comments pages")
        gen_spec = importlib.util.spec_from_file_location("generate_handoff_regression", SCRIPTS_DIR / "generate-handoff.py")
        gen_module = importlib.util.module_from_spec(gen_spec)
        assert gen_spec.loader is not None
        gen_spec.loader.exec_module(gen_module)
        old_run = gen_module.subprocess.run
        emitted: list[dict] = []
        direction = "work"
        def fake_run(command, **kwargs):
            name = Path(command[1]).name
            if name == "fetch-work-item.py":
                if direction == "auth":
                    return subprocess.CompletedProcess(command, 1, stderr="BLOCKER:\ncode: MISSING_AUTH")
                if direction in {"pr", "both"}:
                    return subprocess.CompletedProcess(command, 1, stderr="ERROR: transient")
                kwargs["stdout"].write('{"id": 7, "fields": {"System.WorkItemType": "Task", "System.Title": "ok", "System.Description": "description"}}')
                return subprocess.CompletedProcess(command, 0, stderr="")
            if name == "normalize-work-item.py":
                return old_run(command, **kwargs)
            if name == "fetch-pr-comments.py":
                if direction == "pr":
                    kwargs["stdout"].write('{"comments": [], "pull_request": {"source_branch": "s", "target_branch": "t"}, "linked_work_items": []}')
                    return subprocess.CompletedProcess(command, 0, stderr="")
                return subprocess.CompletedProcess(command, 1, stderr="ERROR: transient")
            if name == "emit-handoff.py":
                result = old_run(command, capture_output=True, text=True)
                if result.stdout:
                    emitted.append(json.loads(result.stdout))
                return result
        gen_module.subprocess.run = fake_run
        try:
            if gen_module.main(["--organization", "org", "--project", "project", "--repository-id", "repo", "--work-item-id", "7", "--pull-request-id", "9", "--mode", "work-item-plus-pr-comments"]) != 0:
                fail("combined generator did not preserve successful work-item source")
        finally:
            gen_module.subprocess.run = old_run
        if not emitted or emitted[-1]["work_item"]["title"] != "ok" or emitted[-1]["normalization"]["status"] != "partial":
            fail("partial work-item handoff did not preserve source data and status")
        if "pr_comments" not in emitted[-1]["normalization"]["missing_fields"] or not emitted[-1]["normalization"]["warnings"]:
            fail("partial work-item handoff omitted missing-source metadata")
        passed("mocked generator preserves work-item when PR source fails")
        direction = "pr"
        gen_module.subprocess.run = fake_run
        try:
            if gen_module.main(["--organization", "org", "--project", "project", "--repository-id", "repo", "--work-item-id", "7", "--pull-request-id", "9", "--mode", "work-item-plus-pr-comments"]) != 0:
                fail("combined generator did not preserve successful PR source")
        finally:
            gen_module.subprocess.run = old_run
        if not emitted or emitted[-1]["pull_request"]["source_branch"] != "s" or emitted[-1]["normalization"]["status"] != "partial":
            fail("partial PR handoff did not preserve source data and status")
        if "work_item" not in emitted[-1]["normalization"]["missing_fields"] or not emitted[-1]["normalization"]["warnings"]:
            fail("partial PR handoff omitted missing-source metadata")
        direction = "both"
        gen_module.subprocess.run = fake_run
        try:
            try:
                gen_module.main(["--organization", "org", "--project", "project", "--repository-id", "repo", "--work-item-id", "7", "--pull-request-id", "9", "--mode", "work-item-plus-pr-comments"])
            except SystemExit:
                pass
            else:
                fail("combined generator fabricated success when both sources failed")
        finally:
            gen_module.subprocess.run = old_run
        passed("mocked generator rejects combined all-source failure")
        direction = "auth"
        gen_module.subprocess.run = fake_run
        try:
            if gen_module.main(["--organization", "org", "--project", "project", "--repository-id", "repo", "--work-item-id", "7", "--pull-request-id", "9", "--mode", "work-item-plus-pr-comments"]) == 0:
                fail("authentication blocker was incorrectly treated as recoverable")
        finally:
            gen_module.subprocess.run = old_run
        passed("mocked generator keeps authentication blockers fatal")


        remote_cases = [
            ("https://dev.azure.com/contoso/My%20Project/_git/my-repo", ("contoso", "My Project", "my-repo", "https", False)),
            ("https://user@dev.azure.com/contoso/proj/_git/repo", ("contoso", "proj", "repo", "https", False)),
            ("https://dev.azure.com/contoso/_git/repo", ("contoso", "repo", "repo", "https-org-shorthand", True)),
            ("git@ssh.dev.azure.com:v3/contoso/proj/repo", ("contoso", "proj", "repo", "ssh", False)),
            ("ssh://git@ssh.dev.azure.com/v3/contoso/proj/repo", ("contoso", "proj", "repo", "ssh", False)),
            ("https://contoso.visualstudio.com/DefaultCollection/proj/_git/repo", ("contoso", "proj", "repo", "legacy-https", False)),
            ("https://contoso.visualstudio.com/proj/_git/repo", ("contoso", "proj", "repo", "legacy-https", False)),
            ("https://contoso.visualstudio.com/_git/repo", ("contoso", "repo", "repo", "legacy-https-org-shorthand", True)),
            ("contoso@vs-ssh.visualstudio.com:v3/contoso/proj/repo", ("contoso", "proj", "repo", "legacy-ssh", False)),
        ]
        for remote, expected in remote_cases:
            parsed_result = run_script("parse-git-remote.py", stdin_text=remote)
            expect_ok(parsed_result, "remote parser rejected a supported Azure DevOps remote")
            parsed_remote = json.loads(parsed_result.stdout)
            actual = (
                parsed_remote["organization"],
                parsed_remote["project"],
                parsed_remote["repository_id"],
                parsed_remote["remote_url_kind"],
                parsed_remote["inferred_project"],
            )
            if actual != expected:
                fail(f"remote parser mismatch: {actual}")
        for invalid_remote in (
            "https://github.com/o/r",
            "git@github.com:o/r.git",
            "file:///tmp/repo",
            "https://dev.azure.com/contoso",
            "",
        ):
            rejected_remote = run_script("parse-git-remote.py", stdin_text=invalid_remote)
            expect_fail_with(rejected_remote, "INVALID_REMOTE_URL", "unsupported remote was not rejected")
        secret_remote = run_script(
            "parse-git-remote.py",
            stdin_text="https://user:CREDENTIAL_SENTINEL_FOR_TEST@github.com/o/r",
        )
        expect_fail_with(secret_remote, "INVALID_REMOTE_URL", "non-ADO remote was not rejected")
        if "CREDENTIAL_SENTINEL_FOR_TEST" in secret_remote.stdout or "CREDENTIAL_SENTINEL_FOR_TEST" in secret_remote.stderr:
            fail("remote parser disclosed credential-bearing URL input")
        ado_credential_remote = run_script(
            "parse-git-remote.py",
            stdin_text="https://user:CREDENTIAL_SENTINEL_FOR_TEST@dev.azure.com/contoso/proj/_git/repo",
        )
        expect_ok(ado_credential_remote, "credential-bearing Azure DevOps remote was rejected")
        if "CREDENTIAL_SENTINEL_FOR_TEST" in ado_credential_remote.stdout or "CREDENTIAL_SENTINEL_FOR_TEST" in ado_credential_remote.stderr:
            fail("remote parser echoed an embedded credential")
        passed("Azure DevOps remote forms parse without credential disclosure")

        find_spec = importlib.util.spec_from_file_location("find_pull_request_regression", SCRIPTS_DIR / "find-pull-request.py")
        find_module = importlib.util.module_from_spec(find_spec)
        assert find_spec.loader is not None
        find_spec.loader.exec_module(find_module)
        old_search = find_module.lib.http_get_json
        requested_urls = []
        find_module.lib.http_get_json = lambda url, **kwargs: (
            requested_urls.append(url)
            or {"value": [
                {"pullRequestId": 9, "title": "late", "status": "active", "sourceRefName": "refs/heads/feature/x", "targetRefName": "refs/heads/main"},
                {"pullRequestId": 4, "title": "FAKE_TEST_PAT_SENTINEL", "status": "active", "sourceRefName": "refs/heads/feature/x", "targetRefName": "refs/heads/main"},
            ]}
        )
        captured = io.StringIO()
        old_pat = os.environ.get("AZURE_DEVOPS_PAT")
        os.environ["AZURE_DEVOPS_PAT"] = "FAKE_TEST_PAT_SENTINEL"
        old_argv = sys.argv
        try:
            sys.argv = ["find-pull-request.py"]
            with contextlib.redirect_stdout(captured):
                find_module.main(["--organization", "org", "--project", "My Project", "--repository-id", "repo", "--source-branch", "feature/x"])
        finally:
            sys.argv = old_argv
            find_module.lib.http_get_json = old_search
            if old_pat is None:
                os.environ.pop("AZURE_DEVOPS_PAT", None)
            else:
                os.environ["AZURE_DEVOPS_PAT"] = old_pat
        search_result = json.loads(captured.getvalue())
        if [candidate["pull_request_id"] for candidate in search_result["candidates"]] != [4, 9]:
            fail("pull request candidates were not sorted by id")
        if search_result["candidates"][0]["title"] != "[REDACTED]":
            fail("pull request search did not redact the current PAT from a title")
        if "refs%2Fheads%2Ffeature%2Fx" not in requested_urls[0] or "My%20Project" not in requested_urls[0]:
            fail("pull request search URL did not encode branch or project")
        passed("mocked branch-to-pull-request lookup encodes and sorts candidates")
        old_search = find_module.lib.http_get_json
        find_module.lib.http_get_json = lambda url, **kwargs: requested_urls.append(url) or {"value": []}
        empty_output = io.StringIO()
        try:
            with contextlib.redirect_stdout(empty_output):
                find_module.main(["--organization", "org", "--project", "My Project", "--repository-id", "repo", "--source-branch", "refs/heads/feature/x", "--status", "completed", "--top", "500"])
        finally:
            find_module.lib.http_get_json = old_search
        empty_result = json.loads(empty_output.getvalue())
        if empty_result["candidate_count"] != 0 or empty_result["candidates"] != []:
            fail("empty pull request search did not return an empty envelope")
        if "searchCriteria.status=completed" not in requested_urls[-1] or "$top=100" not in requested_urls[-1]:
            fail("status filter or top clamp was not applied")
        if requested_urls[0] != requested_urls[-1].replace("searchCriteria.status=completed", "searchCriteria.status=active").replace("$top=100", "$top=20"):
            fail("refs/heads branch prefix changed the search reference")
        passed("empty lookup, branch normalization, status filter, and top clamp")
        for branch in ("HEAD", "", "feature/\nnew"):
            invalid_branch = run_script(
                "find-pull-request.py",
                "--organization", "org",
                "--project", "project",
                "--repository-id", "repo",
                "--source-branch", branch,
            )
            expect_fail_with(invalid_branch, "code: MISSING_INPUT", "invalid branch was not rejected")
        for flag, value in (("--organization", ".."), ("--organization", "a#b"), ("--project", "a/b"), ("--project", "a%2Fb"), ("--repository-id", "a?b")):
            invalid_segment = run_script(
                "find-pull-request.py",
                "--organization", "org",
                "--project", "project",
                "--repository-id", "repo",
                "--source-branch", "feature/x",
                flag,
                value,
            )
            expect_fail_with(invalid_segment, "code: MISSING_INPUT", "unsafe URL path segment was not rejected")

        fetch_spec = importlib.util.spec_from_file_location("fetch_pr_comments_additions", SCRIPTS_DIR / "fetch-pr-comments.py")
        fetch_module = importlib.util.module_from_spec(fetch_spec)
        assert fetch_spec.loader is not None
        fetch_spec.loader.exec_module(fetch_module)
        flattened = fetch_module._flatten(
            [{"id": 11, "status": "active", "comments": [{
                "id": 12,
                "commentType": "system",
                "author": {"id": "reviewer-id", "displayName": "Reviewer", "uniqueName": "reviewer@example.com"},
            }]}],
            "org",
            "project",
            "repo",
            5,
            {"pullRequestId": 5, "createdBy": {"id": "author-id", "displayName": "Author", "uniqueName": "author@example.com"}, "isDraft": True},
            [],
            False,
        )
        comment = flattened["comments"][0]
        if comment["comment_type"] != "system" or comment["author_id"] != "reviewer-id":
            fail("flattened PR comment omitted type or stable commenter identity")
        if flattened["pull_request"]["created_by"]["id"] != "author-id" or flattened["pull_request"]["is_draft"] is not True:
            fail("flattened PR metadata omitted creator identity or draft state")
        passed("flattened PR comments expose type and stable author identities")


if __name__ == "__main__":
    main()
