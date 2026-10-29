# Branch and publication safety

## Tool selection

Read installed `skill://azure-devops-cli` and its repos/PR reference before using Azure CLI operations. Availability of a skill is not proof that `az`, the Azure DevOps extension, or authentication works. Check read-only availability and identity first, with automatic extension installation disabled. Do not install extensions, log in interactively, persist CLI defaults, or expose credentials without explicit permission. Supply organization, project, repository, source, and target explicitly rather than relying on mutable defaults or automatic Git detection.

Use `azure-devops` for the normalized handoff consumed by `spec-writing`; do not manufacture its producer envelope from ad-hoc CLI output. Prefer the CLI for supplementary ADO reads and approved draft-PR/link operations. Keep local branch creation, commits, and pushes in Git.

If CLI skill/runtime/authentication is unavailable, use the guarded `azure-devops` write scripts only for capabilities they actually expose. Inspect the installed PR-creation script's documented flags: the current repository version has no draft flag or work-item-link option. Never silently create a ready PR in place of a draft, invent a flag, or create a ready PR then convert it. Finish reachable local work and report draft publication blocked if no supported approved path exists. Do not silently switch authenticated identities or install tools to bypass a blocker.

`humanizer` is an optional installed prose skill, not a bundled dependency. Read it before use; use embedded mode for PR text and file mode for docs. Preserve IDs, refs, SHAs, code, commands, links, evidence, requirements, and MUST/SHALL strength. Apply it before approvals; a semantic edit afterward requires renewed approval. Report unavailable optional skills without claiming they ran.

## Resolve the base and work branch

1. Inspect current branch, worktrees, dirty/staged/untracked paths, remotes, upstream, and relevant existing PRs. Follow `git-workflow` and `git-worktrees`; do not infer isolation from a directory name. Never move, stage, or stash user changes to make the workflow fit.
2. Resolve supplied identities and the selected remote using `azure-devops`'s credential-safe remote parser. Pipe remote URLs on stdin; never put credential-bearing URLs in argv or logs. Confirm inferred ADO organization/project/repository values before network requests. Verify fetch and push repository identity separately, including fork source repositories and name/ID aliases. Same branch names are not identity evidence.
3. For a new branch, use explicit `base_branch` or `origin/dev`. Verify it exists and is a branch ref in the intended repository. Fetch the selected remote branch before recording its start SHA; fetching is not restore/build/test. Do not reset, pull into, or switch the user's base branch. A missing default is a blocker, not permission to choose `main` or the current branch.
4. For a resumed work-item branch, use explicit base input, otherwise workflow provenance, otherwise that branch's verified existing PR target. If those sources conflict, ask. If none exists, ask for the base. Git does not store the creation parent branch; upstream usually names the feature branch's push destination, not its base. Do not derive the base from upstream or branch naming alone, and do not reset an existing branch to a newly supplied base.
5. Normalize a remote-tracking base such as `origin/dev` into local ref `refs/remotes/origin/dev` and PR target `refs/heads/dev` in the confirmed base repository. A local base such as `dev` needs an established remote branch/repository mapping. Refuse ambiguous, non-branch, or unpushable targets. Record the repository, base ref, start SHA, and PR target once; do not recompute the target from whichever branch is checked out later. Different source/target repositories require an explicitly verified supported fork PR path; never approximate one with same-repository commands.
6. Prefer repository branch naming; otherwise use `feat/<id>-<slug>` or `fix/<id>-<slug>` for a bug. Validate the ref name. If a matching branch or worktree exists locally or remotely, show its work-item/PR association and ask to reuse it or stop. A matching slug alone does not establish ownership. Never overwrite it, auto-suffix a duplicate, or adopt another work item's branch. An explicit branch name or PR URL that conflicts with the work item requires clarification.
7. Obtain consent and use `git-worktrees` to create or reuse isolation. Reuse an existing matching isolated workspace rather than nesting another worktree. Record the complete provenance supplied by that skill. New work branches must not track the base as their push upstream; establish the feature-branch upstream only at approved first push. Preserve the original checkout and all existing worktrees.

## Small commits

Use `git-workflow` to choose atomic boundaries. A slice may need multiple independently reviewable commits; keep a behavior change with its required tests/docs rather than splitting it into broken intermediate commits. Do not chase a line-count quota.

Use Conventional Commit subjects with lowercase imperative descriptions, for example:

```text
fix(checkout): reject expired delivery slots

Refs: AB#12345
```

Use breaking-change notation/footer when applicable. Record each task's full SHA/range in the ledger. Inspect staged contents; stage only owned paths or hunks, never blanket-stage a dirty workspace. Do not amend user commits, rewrite published history, or squash a completed series without explicit direction. Review corrections become additional focused commits. There must be no unpublished fix hiding in the working tree at publication.

## Publication action plan

Before approval, verify the latest source/target repository and remote state. Show:

- Work item, verified source repository, explicit push remote/destination branch, and current local HEAD SHA.
- Outgoing commits and whole-branch diff against the recorded PR target, including any commits not produced by this workflow. Unrelated commits must be resolved before publication; never silently publish them.
- Base repository and actual target branch, draft state, PR title/body, and work-item-link action.
- Tests, restore, and build actually run, known failures, unrun verification, and review verdicts.

CLI PR creation has no assumed dry-run. Present a non-executed command/action preview and obtain explicit approval before its write. For `azure-devops` fallback scripts, use their actual dry-run envelope and `--confirm` gate. Approval of the prose is not approval of push or API writes. If HEAD, destination, PR metadata, or proposed body/link changes materially after approval, show the new action and renew that action's approval.

Never silently publish with observed failing checks or unresolved critical/important review findings. Unauthorized verification is a reported gap; it does not imply passing checks. A draft PR with unrun verification is allowed only when the publication approval explicitly includes those gaps. Do not broaden authorized narrow tests into a full suite.

## Push and PR creation

1. Query existing PRs for the exact source repository/branch and target. Respect pagination; empty/incomplete results are not proof that no PR exists. If one matching active PR exists, verify association and reuse it; do not create another. Show multiple matches or a different target and ask. A completed/abandoned PR does not authorize reopening it or reusing its branch for a new PR without a decision.
2. Recheck current HEAD and remote branch immediately before the approved push. For first publication, push the named work branch to the explicitly selected verified remote, establishing that same branch's upstream. For later pushes, use the verified destination explicitly rather than trusting push defaults. Never force. Stop on rejection or divergent history and use `git-workflow` to plan recovery; do not auto-rebase or merge.
3. Verify the remote branch tip equals the approved HEAD. Push success alone is insufficient evidence that the selected destination is correct.
4. For a new same-repository PR, the CLI operation has this shape after resolving all values and approving the title/body:

```text
az repos pr create --organization <org-url> --project <project> --repository <repo-id> --source-branch <work-branch> --target-branch <base-branch-without-remote> --title <approved-title> --description <approved-body> --draft true --work-items <work-item-id> --detect false --output json
```

Pass each value via an argument API, not by concatenating work-item-derived text into shell source. For multiline/long Windows text, follow the installed CLI skill's long-comment guidance and supported file-input path; never invent an `@file` convention. Do not expose secrets through command previews. Do not enable auto-complete, automatic source deletion, votes, or work-item transitions.

5. For an existing matching PR, leave its readiness state unchanged. Show and separately approve any body update or missing work-item link, using supported CLI commands. No change is needed when metadata and link already match. Do not change reviewers, policies, or target as a side effect of reuse.
6. Read back the PR and linked work items. Verify ID/URL, repository, source ref, recorded target ref, draft state for a newly created PR, and work-item association. If an approved link action fails after PR creation, report the existing PR and incomplete linking; do not create another PR.
7. A timeout or unknown create/update outcome requires a read-back lookup before retry. Partial or unavailable lookup blocks retry. Report successful push separately from failed/uncertain PR creation.

Keep the worktree and branch for review feedback. No automatic merge, PR completion, work-item closure, branch deletion, or workspace cleanup belongs to this workflow.
