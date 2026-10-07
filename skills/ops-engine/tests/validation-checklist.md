# Ops Engine — Validation Checklist

Run this checklist before accepting an operational plan as complete.

## Trigger Check

- [ ] Task involves CI/CD, containers, Kubernetes, deployment safety, or operational risk.
- [ ] Task is NOT pure application refactoring or pure documentation.

## Risk Check

- [ ] Risks are listed before the plan.
- [ ] Each risk includes likelihood and impact level.
- [ ] If any risk is unacceptable without a mitigation path: plan is aborted, not degraded.

## Plan Check

- [ ] Steps are numbered and in safe execution order.
- [ ] Each step has an owner or tool.
- [ ] Staging precedes production for any behavioral change.

## Checks Check

- [ ] Every check is a concrete, executable command or observable state.
- [ ] Pre- and post-conditions are both represented.

## Rollback Check

- [ ] Every destructive or irreversible step has a rollback entry.
- [ ] Rollback includes what artifact to preserve before executing.

## Human Approval Check

- [ ] Human approval is required before any production deployment.
- [ ] Human approval is required before any destructive operation.
- [ ] Human approval is required before any irreversible rollback.

## Error Format

```text
error: <what went wrong during ops planning>
abort-reason: <why the plan was stopped>
recovery: <what must be resolved before the plan can proceed>
```
