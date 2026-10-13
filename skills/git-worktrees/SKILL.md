---
name: git-worktrees
description: Set up an isolated workspace before feature work or plan execution so changes never touch the user's current checkout. Use when starting feature work that needs isolation, before executing an implementation plan, or when the user asks for a worktree. Detect existing isolation first, prefer the harness's native worktree tool, and fall back to git worktree only when no native tool exists. Do not use for branch, commit, rebase, or history planning (use git-workflow), for stacked PRs (use gh-stack), or for deciding how finished work is integrated (use branch-integration).
license: MIT
compatibility: chatgpt, codex, claude-code, cursor, opencode
metadata:
  title: Git Worktrees
  version: "1.0.3"
  summary: Establish an isolated, verified-clean workspace before starting implementation work.
---

# Git Worktrees

## Purpose

Ensure implementation happens in an isolated workspace, protecting the user's current checkout. Detect existing isolation first, prefer native harness tools, and fall back to git worktree — never fight the harness, never eyeball detection.

## Workflow

1. Detect existing isolation — run the checks, never assume:

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
git rev-parse --show-superproject-working-tree 2>/dev/null   # submodule guard
```

   If `GIT_DIR != GIT_COMMON` and not inside a submodule, you are already in a linked worktree — do not create another; report the path and branch and skip to step 4. A submodule checkout is a normal repo, not isolation.
2. If not isolated, get consent before creating anything — unless the user already declared a worktree preference, in which case honor it without asking. If declined, work in place.
3. Create the workspace, in this order of preference:
   - Native harness tool first (an `EnterWorktree`-style tool, a `/worktree` command, or a `--worktree` flag). Native tools own placement, branching, and cleanup; bypassing them creates phantom state the harness cannot see or manage.
   - Only with no native tool available, `git worktree add`. Directory choice: explicit user preference beats an existing project-local `.worktrees/` (preferred) or `worktrees/`, which beats the `.worktrees/` default at project root. For a project-local location, verify the directory is ignored (`git check-ignore`). If it is not ignored, request separate explicit consent before modifying the current checkout's `.gitignore`; do not commit that change without explicit consent. An external location is not subject to the repository's ignore rules and needs no ignore check or `.gitignore` consent.
   - Record provenance immediately: `origin: native|git-worktree`, `owner: harness|this workflow|user`, `created_at`, absolute `path`, `branch`, and `base_branch` (or `detached`). A path alone is not proof of ownership. Pass this record unchanged to `branch-integration`; unknown, user-owned, host-managed, or missing provenance means preserve the workspace.
4. Before any implementation or setup, run `git status --short` and inspect staged, modified, and untracked paths. If the workspace was pre-existing, do not begin unrelated implementation while it contains user changes; report the paths and ask whether to preserve, move, or stop. Cleanliness is independent of test authorization.
5. Run project setup only when separately authorized: dependency installation/restores require an explicit request, and builds require an explicit request. Otherwise report those steps as not run.
6. Verify a clean baseline only when test execution is explicitly authorized. Otherwise report the baseline exactly as `not run — not authorized`. If an authorized baseline fails, report the failures and ask whether to proceed — proceeding past a red baseline is the user's call, not yours.
7. Report the workspace path, branch, provenance record, and baseline result.

## Output Contract

Return exactly these fields:

```text
status: ready|in-place|blocked
workspace:
  path: <absolute workspace path>
  branch: <branch name, or "detached HEAD — externally managed">
  isolation: native|git-worktree|already-isolated|none
  provenance:
    origin: native|git-worktree|unknown
    owner: harness|this workflow|user|host|unknown
    created_at: <timestamp or unknown>
    path: <same absolute path as workspace.path>
    branch: <same branch as workspace.branch>
    base_branch: <confirmed branch, detached, or unknown>
    recorded: yes|no
baseline:
  command: <test command run, or "not run — not authorized">
  result: <pass count / failures observed>
notes:
- <consent state, status paths, or deviation, or "none">
```

`status` MUST be one of the three listed values. `in-place` requires an explicit reason (user declined, or sandbox denial). `ready` requires either an observed green baseline or an explicitly reported `not run — not authorized` baseline. An observed red baseline requires the user's explicit decision to proceed. `ready` also requires a recorded provenance record for a created workspace; otherwise use `blocked` or `in-place`.

## Handoffs

- Hand off branch naming, commit boundaries, and history planning to `git-workflow`.
- Hand off execution of an implementation plan inside the workspace to `plan-execution`.
- Hand off integration of the finished work and workspace cleanup to `branch-integration`, including the complete provenance record.

## Error Handling

1. If `git worktree add` fails with a permission error (sandbox denial), tell the user the sandbox blocked creation and that you are working in place; run setup and baseline only if each operation was explicitly authorized.
2. If an authorized baseline test suite fails, report the failures and ask whether to proceed or investigate first; do not silently build on a red baseline.
3. If the chosen project-local worktree directory is not git-ignored, prefer another ignored or external location. External locations need no ignore check or `.gitignore` consent. Modifying the current checkout's `.gitignore` requires separate explicit consent and committing it requires separate explicit authorization.
4. If both `.worktrees/` and `worktrees/` exist, use `.worktrees/`; if a declared user preference conflicts with observed state, the preference wins.

## Validation Checklist

- [ ] Isolation was detected with the git-dir checks, not assumed.
- [ ] The submodule guard ran before concluding "already in a worktree".
- [ ] An existing isolated workspace was reused, not duplicated.
- [ ] Consent was obtained, or a declared preference was honored without asking.
- [ ] A native harness tool was preferred over manual `git worktree add`.
- [ ] Dependency installation/restores, builds, and baseline tests were each run only with explicit authorization, or reported not run.
- [ ] A red baseline was escalated to the user, not silently overridden.
