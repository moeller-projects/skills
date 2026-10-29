# State and artifacts

## Paths and ownership

Use the selected implementation workspace as the root, not the original checkout or installed skill directory. Read existing artifacts before creating new ones. An existing spec requires an approved diff before overwrite; ledger updates append observed state rather than replacing history.

| Artifact | Default location | Authority |
|---|---|---|
| ADO normalized handoff | OS temp directory, unique work-item filename | Source snapshot only; do not commit sensitive payloads. |
| Freeform spec | `specs/work-item-<id>.md` | Approved behavior and scope. |
| Task graph | `.lukas/tasks-<id>.md` | Task definitions, dependencies, done conditions, estimates. |
| Execution ledger | `.lukas/ledger-<id>.md` | Observed progress, approvals, provenance, rulings, evidence. |
| OpenSpec change | Explicitly selected change path resolved from CLI/repo policy | Approved capability deltas and lifecycle artifacts. |

Keep normalized data only as long as needed. Record retrieval time and source work-item/PR identity in the ledger without secrets or raw comments. If temp data disappears on resume, refetch rather than inventing it. Do not silently replace a source snapshot used by an approved spec: compare changed requirements and reopen affected approvals.

Follow repository policy on committing specs. Local handoffs and ledgers are not implicitly part of a code commit: check whether `.lukas/` is ignored, and explicitly exclude local state from staging if not. Do not edit `.gitignore` or local Git exclusions without consent. If policy forbids repo-local state, choose a user-approved external directory and record absolute paths. Never put credentials in any artifact.

## Ledger contents

Record these fields as they become known:

- Work-item ID, confirmed ADO organization/project/repository, optional PR context, fetch timestamp, normalization status, and approved handling of missing data.
- Current phase; spec/graph paths and revisions; chosen direction; approved IN/OUT scope and unresolved questions.
- Base repository, remote/ref, start SHA, PR target repository/ref, working branch, and explicit push remote/destination.
- Complete workspace provenance from `git-worktrees`, including origin, owner, creation time, absolute path, branch, and base.
- Separate test, restore, and build authorization decisions with conversation context; commands run and their observed results. Do not collapse them into one verification permission.
- Checkpoints A through E and per-slice decisions: approved artifact revision, task/commit range, destination, body, and action. Record declined actions and straight-through consent separately.
- Per-task status, full commit SHAs/ranges, review verdict, observed evidence or verification gap; rulings on plan defects with rationale and cost if wrong.
- Final whole-branch review, publication preview, approved HEAD SHA, verified remote SHA, PR ID/URL, draft state, work-item link, and any partial failure.

The todo list is a live projection of task progress, not an independent plan or approval record. Keep task IDs stable. Do not mark implementation complete when only a stub exists, or verification complete when it was not run. A reviewed implementation can be recorded separately from unauthorized verification.

## OpenSpec mode

Inspect the target repository's `openspec/specs/` and active changes before authoring behavior changes. Select an existing change explicitly when more than one is active; otherwise choose a focused kebab-case name including the work-item ID where the local convention permits it.

Use `spec-writing` only for authoring/serialization. When available, inspect `openspec list --json`, then `openspec status --change <name> --json` and `openspec instructions <artifact> --change <name> --json` for the selected initialized change. The resolved schema/template paths are authoritative; do not handcraft artifacts that contradict them. Require repository-required lifecycle initialization before issuing commands that need an existing change.

The task graph remains the source for task definitions. Derive `tasks.md` one-way using stable task IDs; this is a real task checklist after planning, not an implementation stub. Apply progress may be reflected in checklist markers without making them a second task-definition source. Preserve completed markers only when commits/evidence support them, and leave unexecuted verification unchecked. Scope changes update the graph first, then regenerate the checklist and obtain affected approvals. Never regenerate away externally recorded apply progress without reconciling it.

Lifecycle work belongs to official OpenSpec workflows. Follow target-repository requirements for apply/verify; if a lifecycle step requires a separate human invocation, stop at that boundary and recommend the exact named change/step rather than silently invoking another user-invoked orchestrator. Validate the active change using the installed CLI's supported change-validation syntax before completion. Do not sync or archive automatically.

## Resume and invalidation

Read the ledger, approved spec/graph, current Git status/log, remote branch, and PR state before acting. Match recorded task SHAs to actual history; absent/unreachable commits are a discrepancy to resolve, not permission to repeat work blindly.

For a new conversation, obtain fresh execution permissions; a stored ledger cannot grant test/restore/build or write authorization. In the same conversation, recheck that an approval still covers the current artifact/action. A changed requirement reopens spec approval and affected task planning; a changed HEAD or destination reopens push approval; a changed PR body/target/link action reopens API-write approval. Preserve approvals for genuinely unchanged independent work only within the conversation that granted them.

If the recorded base cannot be recovered, ask. Never infer it from the feature branch's upstream. When publication partly succeeded, keep the actual remote/PR identity in the ledger and resume from the missing operation, not from creating another branch or PR.
