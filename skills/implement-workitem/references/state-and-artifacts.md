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
- Output-mode selection and availability evidence; exact OpenSpec change names, selected store/planning root, resolved paths, and whether each change was created by this run or pre-existing. Record verification, sync/archive decisions, resulting archive paths, finalization commits, and publication evidence.
- Base repository, remote/ref, start SHA, PR target repository/ref, working branch, and explicit push remote/destination.
- Complete workspace provenance from `git-worktrees`, including origin, owner, creation time, absolute path, branch, and base.
- Separate test, restore, and build authorization decisions with conversation context; commands run and their observed results. Do not collapse them into one verification permission.
- Checkpoints A through E and per-slice decisions: approved artifact revision, task/commit range, destination, body, and action. Record declined actions and straight-through consent separately.
- Per-task status, full commit SHAs/ranges, review verdict, observed evidence or verification gap; rulings on plan defects with rationale and cost if wrong.
- Final whole-branch review, publication preview, approved HEAD SHA, verified remote SHA, PR ID/URL, draft state, work-item link, and any partial failure.

The todo list is a live projection of task progress, not an independent plan or approval record. Keep task IDs stable. Do not mark implementation complete when only a stub exists, or verification complete when it was not run. A reviewed implementation can be recorded separately from unauthorized verification.

## OpenSpec mode

### Selection and initialization

Resolve the mode before authoring. OpenSpec is available when the CLI is usable and the selected repository or explicitly selected store has an initialized planning root. Read the installed official OpenSpec skill before lifecycle operations. Use its project/store checks (`openspec list --json` and the returned `root`); keep selected-root flags such as `--store <id>` on all applicable subsequent commands. CLI installation or an installed skill alone does not establish project availability.

Default to OpenSpec whenever those checks succeed. Honor explicit freeform output unless repository policy requires OpenSpec. If no CLI/root is available and OpenSpec was neither explicitly requested nor required, use freeform and record the reason. An explicit OpenSpec request or repository requirement instead needs a user decision on setup, store selection, or an allowed fallback. Malformed configuration, unresolved declared stores, and ambiguous roots are blockers, not permission to silently fall back. Never install the CLI, run `openspec init`, or create a root as a side effect without consent.

Inspect existing specs and active changes in the resolved planning root. Create a focused kebab-case change including the work-item ID where convention permits, using official `openspec-new-change` or the supported `openspec new change <name>` command. Reuse a pre-existing change only with explicit selection and association to this work item; multiple active changes require disambiguation, never bulk adoption. Record ownership before writing artifacts.

Use `spec-writing` only for authoring/serialization. Inspect `openspec status --change <name> --json` and `openspec instructions <artifact> --change <name> --json` for the selected initialized change. Resolved planning-home, change-root, artifact, schema, and template paths are authoritative; do not assume repo-local paths or handcraft artifacts that contradict them. Preserve the official workflow's stop points and this controller's approval checkpoints.

The task graph remains the source for task definitions. Derive `tasks.md` one-way using stable task IDs; this is a real task checklist after planning, not an implementation stub. Apply progress may be reflected in checklist markers without making them a second task-definition source. Preserve completed markers only when commits/evidence support them, and leave unexecuted verification unchecked. Scope changes update the graph first, then regenerate the checklist and obtain affected approvals. Never regenerate away externally recorded apply progress without reconciling it.

### Finalization: verify and archive last

Lifecycle work belongs to official OpenSpec workflows. Follow target-repository requirements for apply/verify. If a lifecycle step requires separate human invocation, stop at that boundary and recommend the exact named change/step rather than chaining another user-invoked orchestrator.

After all approved implementation slices, final review, and the publication outcome, finalize every change created by this run, using the recorded names and planning roots. Never archive unrelated or pre-existing changes without separate explicit approval. No created changes means archival is not applicable; blocked or interrupted implementation must leave its changes active.

1. Use official `openspec-verify-change` and the installed CLI's supported change-validation command for the exact change. Respect test/build/restore permissions; do not turn unrun checks into passing evidence or mark unchecked tasks complete. Resolve critical findings; disclose warnings and verification gaps.
2. Use official `openspec-archive-change`, including its sync assessment, prompts, completion checks, and collision handling. If it calls for sync, use official `openspec-sync-specs` synchronously and wait for its verification before archival. Do not copy those procedures into this controller or bypass their confirmations.
3. If official skills are unavailable, inspect installed `openspec --help` and `openspec archive --help`, then use the supported official `openspec archive <name>` command and its checks/prompts. Do not invent flags, force completion, suppress validation, or replace the lifecycle with an ad-hoc move/delete. If neither supported path is available, report finalization blocked.
4. Verify the resolved archive destination and active-change state, and record sync outcome and warnings in the ledger. On timeout or uncertain outcome, inspect both before retrying. Resume from the actual lifecycle state; never archive twice.
5. Review resulting main-spec/archive diffs and commit owned repository changes following `git-workflow`. If already published, show the finalization commits, renew push approval for the new HEAD, push normally, and read back the final remote tip and PR; renew PR-update approval if its body or metadata changes. Never leave archival only in an unpublished working tree while claiming the published branch is final. For keep-local, retain the reviewed local commits. If the planning root is an external store, follow its separately approved commit/publication policy; an implementation-repository push does not publish store changes.

Finalization is the last substantive phase, not permission to merge the PR or close the work item. Report a declined, blocked, or policy-deferred archive as pending with its reason and next official action; do not claim the end-to-end workflow is complete.

## Resume and invalidation

Read the ledger, approved spec/graph, current Git status/log, remote branch, and PR state before acting. Match recorded task SHAs to actual history; absent/unreachable commits are a discrepancy to resolve, not permission to repeat work blindly.

For a new conversation, obtain fresh execution permissions; a stored ledger cannot grant test/restore/build or write authorization. In the same conversation, recheck that an approval still covers the current artifact/action. A changed requirement reopens spec approval and affected task planning; a changed HEAD or destination reopens push approval; a changed PR body/target/link action reopens API-write approval. Preserve approvals for genuinely unchanged independent work only within the conversation that granted them.

If the recorded base cannot be recovered, ask. Never infer it from the feature branch's upstream. When publication partly succeeded, keep the actual remote/PR identity in the ledger and resume from the missing operation, not from creating another branch or PR.
