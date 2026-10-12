# Git Workflow — Validation Checklist

## Trigger Check

- [ ] Request concerns commits, branches, history, rebasing, conflicts, stacks, safe undo, or Conventional Commits.
- [ ] PR content review, operations/deployment, and live incident work are handed off.

## Plan Check

- [ ] Context states publication and collaborators.
- [ ] Branch naming and parent/base are explicit.
- [ ] Commit plan is atomic and uses imperative Conventional Commit subjects.
- [ ] Rebase/merge/revert choice has a rationale.

## Operation Check

- [ ] Every operation has an exact command, rationale, and risk tier.
- [ ] Operations are ordered and include preflight diff and hygiene review.
- [ ] Stacked branches identify parent order and update direction.

## Destructive Safety Check

- [ ] Every `reset --hard`, `rebase`, or `push --force` has confirmation, blast radius, and exact rollback.
- [ ] Published/shared history uses revert rather than reset or force-push.
- [ ] A rescue reference or reflog recovery path is present.
- [ ] Merge/rebase abort command is supplied for conflict failure.

## Error Format

```text
error: <what went wrong>
blocked: <unknown publication, ownership, or conflict state>
recovery: <exact abort, revert, rescue, or reflog command>
```
