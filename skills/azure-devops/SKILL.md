---
name: azure-devops
description: Use when fetching, parsing, normalizing, or narrowly creating approved Azure DevOps work items and pull request artifacts, or when locating the active pull request for a git branch. Do not use when the task targets GitHub PR review, destructive Azure DevOps actions, or OpenSpec authoring.
license: MIT
compatibility: chatgpt, codex, claude-code, cursor, opencode
metadata:
  title: Azure DevOps
  version: "1.2.1"
  summary: Read and safely write selected Azure DevOps work items and PR artifacts, and locate a branch's active PR, with deterministic dry-run, approval, and validation gates.
---

# Azure DevOps

## Purpose

Fetch Azure DevOps work item and pull request discussion data through read-only flows, normalize the result, and emit a stable handoff contract for downstream skills. For explicitly requested write workflows, create only the supported Azure DevOps artifacts through dry-run-first scripts with an explicit execution gate.


## Read Workflow

1. Identify the source mode: `work-item`, `pr-comments`, or `work-item-plus-pr-comments`.
2. When identifiers are missing, follow `references/workflow.md` to resolve a PR from the current local branch or remote; approve inferred organization, project, and repository values before requesting ADO data.
3. Validate required identifiers and authentication. Accept explicit identifiers, a PR URL, or a confirmed PR ID plus repository identifiers.
4. Fetch and normalize Azure DevOps data with GET-only scripts, including work-item comments, update history, related-work links, and PR threads.
5. Emit contract JSON and stop. Do not draft specs or take write actions.

## Write Workflow

1. Confirm the user explicitly asked to create a work item, create a pull request, add a work item comment, add a PR comment, or reply to a PR comment.
2. Build a dry-run action plan first. The dry-run must include method, URL path, body, required PAT scopes, and risk level.
3. Do not execute a write unless the command includes `--confirm`.
4. Run the supported Python scripts with `python` when the user explicitly requests the corresponding write action:
   - `scripts/create-work-item.py`
   - `scripts/create-work-item-comment.py`
   - `scripts/create-pull-request.py`
   - `scripts/create-pr-comment.py`
5. Do not create generic Azure DevOps API clients that can call arbitrary endpoints.
6. Never delete, merge, approve, reject, complete, or abandon via this skill.

7. When creating an inline PR comment thread, supply `--file-path` as a path relative to the repository root and starting with `/` (e.g., `/src/order.ts`). The script normalizes equivalent inputs to this format. Filesystem absolute paths and path traversal segments are invalid and will prevent the thread from anchoring to the diff.

## Supported Write Actions

| Action | Script | HTTP method | Required scope | Default behavior |
|---|---|---:|---|---|
| Create work item | `create-work-item.py` | POST | Work Items: Read & write / `vso.work_write` | dry-run |
| Create work item comment | `create-work-item-comment.py` | POST | Work Items: Read & write / `vso.work_write` | dry-run |
| Create pull request | `create-pull-request.py` | POST | Code: Read & write / `vso.code_write` | dry-run |
| Create new PR comment thread | `create-pr-comment.py --mode thread` | POST | Code: Read & write / `vso.code_write` | dry-run |
| Reply to PR comment thread | `create-pr-comment.py --mode reply` | POST | Code: Read & write / `vso.code_write` | dry-run |

## Handoffs

- Handoff to `spec-writing` when the normalized work item or PR context should be turned into a spec or OpenSpec proposal.
- Stop after emitting the shared handoff contract; downstream interpretation belongs to the receiving skill.

## Output Contract

Read operations return only the shared handoff envelope. Write dry-runs return only the write action envelope:

```json
{
  "action_type": "create-work-item|create-work-item-comment|create-pull-request|create-pr-comment-thread|reply-pr-comment",
  "dry_run": true,
  "requires_confirmation": true,
  "method": "POST",
  "url": "https://dev.azure.com/...",
  "required_scopes": [],
  "body": {}
}
```

## Blocker Format

```text
BLOCKER:
code: <MISSING_INPUT|MISSING_AUTH|INVALID_PR_URL|INVALID_REMOTE_URL|WRITE_CONFIRMATION_REQUIRED>
required_input:
- ...
next_question: ...
```

## Error Format

```text
ERROR:
code: <FETCH_FAILED|PARSE_FAILED|NORMALIZATION_FAILED|WRITE_FAILED>
stage: <fetch|parse|normalize|emit|write>
message: ...
recovery: ...
```

## Human-in-the-Loop

Request explicit approval before:

- Using inferred organization, project, or repository values that were not supplied.
- Returning raw Azure DevOps thread payloads.
- Executing any Azure DevOps write action.

## Assets

- `assets/templates/handoff.json` — read when emitting a canonical handoff envelope.
- `assets/templates/blocker.txt` — read when formatting a missing-input, auth, or confirmation blocker.
- `assets/templates/error.txt` — read when formatting fetch, parse, normalization, emit, or write errors.

## References

- `references/workflow.md` — read when implementing or troubleshooting the staged read flow.
- `references/write-actions.md` — read before any supported write workflow.
- `references/auth-and-safety.md` — read when handling PATs or authorization boundaries.
- `references/normalization-rules.md` — read when normalizing Azure DevOps payloads.
- `references/handoff-contract.md` — read when producing or consuming the handoff contract.
- `references/end-to-end.md` — read for a complete fetch-to-handoff walkthrough.
- `references/rule-order.md` — read when ordering read/write processing stages.

## Scripts

- `scripts/generate-handoff.py` — run for normal end-to-end reads.
- `scripts/fetch-work-item.py` and `scripts/fetch-pr-comments.py` — run as GET-only primitive fetches in a staged workflow.
- `scripts/normalize-work-item.py` — run when normalizing a fetched work-item payload.
- `scripts/emit-handoff.py` — run when assembling and validating already-fetched/normalized inputs.
- `scripts/parse-pr-url.py` — run when parsing a PR URL without fetching.
- `scripts/parse-git-remote.py` — read a remote URL from stdin when mapping an Azure DevOps checkout; never pass a credential-bearing URL as an argument.
- `scripts/find-pull-request.py` — list PRs whose source branch matches the current local branch (GET only).
- `scripts/validate-handoff.py` — run when validating a handoff JSON contract.
- `scripts/ensure-env.py` — run before a network operation to check PAT availability.
- `scripts/format-work-item-mention.py` and `scripts/resolve-ado-user.py` — run when formatting a mention or resolving an Azure DevOps identity.
- `scripts/create-work-item.py`, `scripts/create-work-item-comment.py`, `scripts/create-pull-request.py`, and `scripts/create-pr-comment.py` — run for explicitly requested, guarded dry-run-first writes.
- `scripts/_ado_lib.py` — import as shared internal helpers; do not run directly.

## Example Inputs and Schema

- `assets/examples/work-item-only.json` — read when inspecting a normalized work-item example.
- `assets/examples/pr-comments-only.json` — read when inspecting a normalized PR-comments example.
- `assets/examples/work-item-plus-pr-comments.json` — read when inspecting a combined normalized example.
- `assets/schemas/ado-openspec-handoff.schema.json` — read when validating the handoff contract schema.

## Rules

- `rules/read-only-boundary.md` — read before read-only fetches.
- `rules/write-boundary.md` — read before write workflows.
- `rules/normalization-precedence.md` — read when resolving competing normalized field sources.

## Tests

- `tests/validation-checklist.md` — read when manually checking the skill; do not execute test steps unless the user explicitly requests test execution.
- `tests/run-validation.py` — run only when the user explicitly requests test execution; dependency restore, build, and test authorization remains separate.
- `tests/goldens.json` — read when comparing dry-run write output to the pre-refactor baseline; change only for intentional output changes.
