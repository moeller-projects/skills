# Code Quality Engine — Validation Checklist

Run this checklist before accepting a code quality review as complete.

## Trigger Check

- [ ] Task is reviewing, refactoring, optimizing, or modernizing code.
- [ ] Task is NOT exclusively documentation, test design, or infrastructure work.

## Findings Check

- [ ] Findings are sorted by severity: critical → high → medium → low.
- [ ] Each finding includes file and line number.
- [ ] Each finding states the issue clearly and why it matters.
- [ ] Each finding has an exact, actionable fix.

## Patch Plan Check

- [ ] Patch steps are listed in safe application order.
- [ ] Each step identifies the file and the action.
- [ ] Performance changes are included only when profiling data exists.
- [ ] Unrelated cleanup is deferred, not mixed into the patch.

## Risk Check

- [ ] Residual risks after applying the patch are listed.
- [ ] Critical-path changes include a verification step.

## Error Format

```text
error: <what went wrong during review>
gap: <what information was missing>
recovery: <action taken — e.g., skipped finding, asked clarifying question>
```
