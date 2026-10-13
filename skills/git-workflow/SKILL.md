---
name: git-workflow
description: Use when committing changes, choosing a branch or merge strategy, rebasing, resolving merge conflicts, managing stacked or dependent PRs, cleaning history, undoing changes safely, or writing conventional commits. Do not use for reviewing PR content, CI/CD or deployment configuration, live production incidents, or operating the gh stack CLI on stacked PRs; hand those to pr-review, operations, incident-response, or gh-stack.
license: MIT
compatibility: chatgpt, codex, claude-code, cursor, opencode
metadata:
  title: Git Workflow
  version: "1.3.2"
  summary: Plan safe, disciplined Git history, branching, commit, rebase, recovery, and stacked PR operations.
---

# Git Workflow

## Purpose

Produce an executable, safety-first plan for Git history, branches, commits, rebases, merges, conflict recovery, and dependent PRs without executing commands.

## Workflow

1. Inspect repository state, branch publication status, remotes, and collaboration constraints; do not assume a branch is private.
2. Define the logical change and branch/stack topology, then choose atomic commit boundaries and a Conventional Commit message.
3. Select rebase or merge using shared-history and collaboration criteria; document conflict-resolution order for dependent branches.
4. Build ordered operations with exact commands, a risk tier (`safe`, `cautious`, or `destructive`), rationale, and verification checkpoints.
5. Apply the history-safety and recovery rules before any rewrite, conflict recovery, or stack update.
6. Review the diff for unrelated files, secrets, generated debris, and accidental history changes before publication.

## Output Contract

Return a plan using `assets/templates/output.md` with:

- `context`, `branch_strategy`, and `commit_plan`.
- An ordered `operations` list where every item has an exact command, rationale, and risk tier.
- `safety_notes` covering destructive commands and shared-branch constraints.
- `rollback` with a recovery path and exact commands.
- Conventional Commit format: `type(scope): imperative description`; breaking changes use a `BREAKING CHANGE:` footer.
- Never force-push a shared branch; prefer `git revert` over reset for published history.

Every commit item MUST include its own message and breaking footer. Every operation MUST use the next `O-NN` identifier in order and include all required fields. The validator rejects unknown IDs, malformed items, empty sections, invalid messages/footers, and unsafe commands missing destructive risk, confirmation, blast radius, or an exact rollback.

## Handoffs

- Hand off PR content review to `pr-review`.
- Hand off CI/CD, deployment, rollout, or pipeline configuration to `operations`.
- Hand off live production stabilization to `incident-response`.
- Hand off stacked-PR creation, sync, submit, and merge with the `gh stack` CLI to `gh-stack`.
- Hand off isolated-workspace setup before implementation to `git-worktrees`.
- Hand off integration of finished, verified work to `branch-integration`.
- When integrating a worktree, pass the complete recorded provenance from `git-worktrees`; a path alone never authorizes cleanup.

## Error Handling

- If publication or ownership is unknown, stop before destructive commands and mark the operation blocked pending confirmation.
- For conflict or recovery handling, follow `rules/history-safety.md` and `rules/recovery-and-stacks.md`.
- If scope includes PR review, deployment, or incident response, produce only the Git portion and name the handoff.

## Validation Checklist

- [ ] Every operation has an exact command, rationale, and risk tier.
- [ ] Commits are atomic and use valid imperative Conventional Commit subjects, with a footer on each item.
- [ ] Branch naming and stack dependencies are explicit.
- [ ] Rebase-versus-merge choice cites whether history is shared or published.
- [ ] Diff hygiene checks cover unrelated changes, secrets, generated debris, and staged contents.
- [ ] Every destructive operation has explicit confirmation, blast radius, and an exact rollback/recovery command.
- [ ] Published history is reverted rather than reset; shared branches are never force-pushed.

See `tests/validation-checklist.md` for the full checklist.

## Assets

- `assets/templates/output.md` — use for every Git operation plan.
- `assets/examples/happy-path.md` — use as a complete private-branch rebase and stacked-PR example.
- `assets/examples/edge-case.md` — use when undoing a published/shared change safely.
- `scripts/validate-output.py` — run only when test execution is explicitly authorized to validate output mechanics.
- `tests/run-validation.py` — run only when test execution is explicitly authorized to exercise valid and invalid fixtures.
- `tests/validation-checklist.md` — consult when reviewing contract and safety requirements.

## References

- Read `references/workflow.md` when choosing a branch operation or recovery path.
- Read `references/examples.md` when an equivalent commit, rebase, merge, undo, or stacked-PR example is needed.

## Rules

- Read `rules/commit-hygiene.md` when checking commit contents or message hygiene.
- Read `rules/history-safety.md` before rewriting published/shared history.
- Read `rules/branch-strategy.md` when selecting branch topology.
- Read `rules/recovery-and-stacks.md` when resolving conflicts, recovering commits, or updating stacks.
