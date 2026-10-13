---
name: branch-integration
description: Decide and execute how completed implementation work lands once its tests are green. Use when implementation is complete, the suite passes, and the work needs to be merged, turned into a pull request, kept, or — only on explicit user request — discarded. Covers base-branch confirmation, the integration menu, merged-result verification, and provenance-based worktree cleanup. Do not use while tests are still failing (use debugging), for history or rebase planning (use git-workflow), for stacked PRs (use gh-stack), or for making the completion claim itself (use verification-before-completion first).
license: MIT
compatibility: chatgpt, codex, claude-code, cursor, opencode
metadata:
  title: Branch Integration
  version: "1.1.3"
  summary: Land verified work through a user-chosen integration path with safe cleanup.
---

# Branch Integration

## Purpose

Land completed work safely: verify the suite on the exact tree being integrated, let the user choose the integration path, execute it, and clean up only what this workflow created. Integration is the user's decision — present the options and wait.

## Workflow

1. Run the project's full test suite on the exact tree you are about to integrate only when test execution is explicitly authorized. Otherwise report verification as not run and block integration claims. If an authorized run fails, report the failures and stop; hand off to `debugging`.
2. Detect the environment: normal repo checkout, named-branch worktree, or detached HEAD (`git rev-parse --git-dir` vs `--git-common-dir`). Capture the workspace path now — later steps change directory. Read the worktree provenance record from `git-worktrees`: it MUST include origin, owner, creation time, absolute path, branch, and base branch. A matching path alone is insufficient. Missing, unknown, user-owned, or host-managed provenance means cleanup is preserved, not attempted.
3. Confirm the base branch the work forked from. If it is not recorded in the provenance record, plan, or conversation, state your best guess and ask — merging into the wrong base is expensive to undo.
4. Present exactly these options and wait for the answer:
   - Normal repo or named-branch worktree: (1) merge back to the base branch locally, (2) push and create a pull request, (3) keep the branch as-is.
   - Detached HEAD (externally managed workspace): (1) push as a new branch and create a pull request, (2) keep as-is — local merge is unavailable.
   - Never offer discard unprompted; it exists only in response to an explicit user request.
5. Execute the choice:
   - Merge locally: before switching to the base, updating it, or merging, obtain either separate explicit authorization to run the merged-result test suite or the user's explicit confirmation to skip that run and report it as unrun. If neither decision is available, do not switch or merge. With test authorization, switch to the base from the main repo root, update it, merge, and run the suite on the merged result. With skip-and-report confirmation, switch and merge only after recording that decision, then report the merged-result verification as not run. If the authorized run fails, stop — leave branch and worktree in place and report integration as blocked; nothing has been pushed. Only after an authorized green merged result, clean up and delete the branch when the user selected discard or local merge cleanup.
   - Pull request: push the branch (from detached HEAD, push `HEAD` to a new named remote branch), create the PR against the confirmed base with the forge's tooling and the repo's PR template, write its body with `pr-body`, and report the URL. Keep the worktree — review feedback gets fixed there.
   - Keep as-is: report branch name and workspace path; change nothing.
   - Discard (only after an explicit typed `discard` confirmation): protect user work before switching. In a normal checkout, first run `git status --short`; if staged, modified, or untracked paths exist, do not switch, delete, or reset. Show the paths and preserve the checkout, offering commit, move, or user-directed deletion. In a clean normal checkout, switch only to the confirmed base branch, verify the target is clean, then delete the feature branch. If switching or cleanliness verification is blocked, preserve both branch and worktree.
6. Clean up (local merge and confirmed discard only): remove a worktree with `git worktree remove` plus `git worktree prune` only when the complete provenance record says this workflow created it and its path is under a project-local `.worktrees/` or `worktrees/` directory. Otherwise leave it in place. If removal is refused because of modified or untracked files, never use `--force`; show the file list and ask whether to commit, move, or delete them.

## Output Contract

Return exactly these fields:

```text
status: merged|pr-opened|kept|discarded|blocked
base_branch: <confirmed base the work forked from>
evidence:
- command: <test suite or merge command run>
  result: <observed output>
integration:
  path: <merge | pull request | keep | discard>
  detail: <merge commit, PR URL, or preserved locations>
cleanup:
- <worktree removed / preserved and why; include provenance decision>
open_risks:
- <remaining items, or "none">
```

`status` MUST be one of the five listed values. `merged` requires an observed green test run on the merged result, authorized separately; otherwise report `blocked`. `discarded` requires the user's typed confirmation and a clean, confirmed-base checkout before branch deletion. A normal checkout with user work is preserved and cannot be reported as discarded.

## Handoffs

- Hand off completion-proof and evidence-gate requirements to `verification-before-completion`.
- Hand off history surgery, push safeguards, or conflict-heavy merges to `git-workflow`.
- Hand off stacks of dependent PRs to `gh-stack`.
- Hand off failing suites or failing merged results to `debugging`.
- Hand off incoming feedback on the opened PR to `review-response`.

## Error Handling

1. If the merged-result test decision was neither authorized nor explicitly confirmed as skip-and-report before a local merge, do not switch or merge; report the integration as blocked. If the merged result fails, or a pre-approved skip leaves verification unrun, keep the branch and worktree in place and report the integration as blocked (failures go to `debugging`).
2. If a push is rejected, the remote moved — investigate; follow `git-workflow` safeguards and force-push only on the user's explicit request.
3. If the user asks to discard the work, confirm first with the exact consequences (branch, commit list, worktree path) and require the typed word `discard` before deleting. In a normal checkout, preserve any staged, modified, or untracked paths; only a clean checkout may switch to the confirmed base and force-delete the branch.
4. If worktree removal is refused, show the uncommitted file list and offer: commit them, move them to the main repo root, or delete them (unrecoverable). Carry out only the chosen option; never use `--force`.
5. If the base branch cannot be determined, ask before merging — never guess. If creation provenance is missing or unknown, preserve the workspace and report cleanup as not authorized; do not infer ownership from its path or block an otherwise authorized merge merely to obtain cleanup permission.

## Validation Checklist

- [ ] Initial and merged-result test runs were each explicitly authorized, or reported not run with integration blocked.
- [ ] The base branch was confirmed, not assumed.
- [ ] The option menu matched the detected environment (detached HEAD gets no merge option).
- [ ] The option came from the user; discard was never offered unprompted.
- [ ] Normal-checkout discard checked status before switching, preserved user work, and deleted a branch only from a clean confirmed base.
- [ ] A merged result was retested before any cleanup or branch deletion.
- [ ] Cleanup removed only worktrees created by this workflow under `.worktrees/` or `worktrees/`; unknown, user, or host ownership was preserved.
- [ ] A refused worktree removal was escalated with the file list, never forced.
