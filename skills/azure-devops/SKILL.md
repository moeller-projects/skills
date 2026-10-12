---
name: azure-devops
description: Use when fetching, parsing, normalizing, or narrowly creating approved Azure DevOps work items and pull request artifacts. Do not use when the task targets GitHub PR review, destructive Azure DevOps actions, or OpenSpec authoring.
allowed-tools: read_file shell
metadata:
  title: Azure DevOps
  version: "1.1.1"
  summary: Read and safely write selected Azure DevOps work items and PR artifacts with deterministic dry-run, approval, and validation gates.
---

# Azure DevOps

## Purpose

Fetch Azure DevOps work item and pull request discussion data through read-only flows, normalize the result, and emit a stable handoff contract for downstream skills. For explicitly requested write workflows, create only the supported Azure DevOps artifacts through dry-run-first scripts with an explicit execution gate.

## Use When

- Fetching a backlog item or work item from Azure DevOps.
- Fetching pull request comments from an Azure DevOps PR URL or explicit identifiers.
- Parsing an Azure DevOps pull request URL into organization, project, repository, and pull request ID.
- Converting Azure DevOps data into a deterministic contract for another skill.
- Creating an Azure DevOps work item after the user clearly requested creation.
- Creating an Azure DevOps work item comment after the user clearly requested it.
- Creating an Azure DevOps pull request after the user clearly requested creation.
- Adding a new Azure DevOps PR comment thread or replying to an existing PR thread after the user clearly requested it.

## Avoid When

- The task requires deleting Azure DevOps data.
- The task requires completing, abandoning, approving, rejecting, or merging a pull request.
- The task requires changing reviewer votes or branch policies.
- The task is a GitHub pull request review.
- The task is generating or validating an OpenSpec file.
- The task is generic REST API work with no Azure DevOps context.

## Read Workflow

1. Identify the source mode: `work-item`, `pr-comments`, or `work-item-plus-pr-comments`.
2. Validate required identifiers and authentication. Accept either explicit Azure DevOps identifiers or a pull request URL.
3. Fetch Azure DevOps data with GET-only scripts, including work-item comments, update history, current related-work links, and PR threads.
4. Normalize work-item fields, comments, changed-field history, related-work links, PR threads, line anchors, and missing values into the shared contract.
5. Emit contract JSON and stop. Do not draft specs or take write actions.

## Write Workflow

1. Confirm the user explicitly asked to create a work item, create a pull request, add a work item comment, add a PR comment, or reply to a PR comment.
2. Build a dry-run action plan first. The dry-run must include method, URL path, body, required PAT scopes, and risk level.
3. Do not execute a write unless the command includes `--confirm`.
4. Run the supported Python scripts with `python`:
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
code: <MISSING_INPUT|MISSING_AUTH|INVALID_PR_URL|WRITE_CONFIRMATION_REQUIRED>
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

- `assets/templates/handoff.json` — canonical shared handoff envelope emitted by read flows for downstream skills such as `spec-writing`
- `assets/templates/blocker.txt` — structured blocker shape for missing inputs, auth, or confirmation gates
- `assets/templates/error.txt` — structured error shape for fetch, parse, normalization, emit, or write failures

## References

- `references/workflow.md` — detailed read execution flow
- `references/write-actions.md` — supported write flows and safety gates
- `references/auth-and-safety.md` — auth handling and safety boundaries
- `references/normalization-rules.md` — field extraction and normalization rules
- `references/handoff-contract.md` — producer requirements for downstream skills
- `references/end-to-end.md` — Python walkthrough from Azure DevOps input to OpenSpec handoff
- `references/rule-order.md` — required read/write stage ordering

## Scripts

- `scripts/generate-handoff.py` — fetch, normalize, and emit the complete handoff; use for normal end-to-end reads.
- `scripts/fetch-work-item.py` and `scripts/fetch-pr-comments.py` — GET-only primitive fetches used when a staged workflow is needed.
- `scripts/parse-pr-url.py` — parse a PR URL into identifiers without fetching.
- `scripts/normalize-work-item.py` — normalize a fetched work-item payload.
- `scripts/emit-handoff.py` — assemble and validate already-fetched/normalized inputs.
- `scripts/validate-handoff.py` — validate a handoff JSON contract.
- `scripts/ensure-env.py` — check PAT availability before a network operation.
- `scripts/format-work-item-mention.py` and `scripts/resolve-ado-user.py` — format a mention or resolve an Azure DevOps identity.
- `scripts/create-work-item.py`, `scripts/create-work-item-comment.py`, `scripts/create-pull-request.py`, and `scripts/create-pr-comment.py` — guarded dry-run-first write operations.
- `scripts/_ado_lib.py` — shared internal helpers imported by the scripts above; do not run directly.

## Example Inputs and Schema

- `assets/examples/work-item-only.json` — normalized work-item example.
- `assets/examples/pr-comments-only.json` — normalized PR-comments example.
- `assets/examples/work-item-plus-pr-comments.json` — combined normalized example.
- `assets/schemas/ado-openspec-handoff.schema.json` — JSON Schema for the handoff contract.
## Rules

- `rules/read-only-boundary.md`
- `rules/write-boundary.md`
- `rules/normalization-precedence.md`
