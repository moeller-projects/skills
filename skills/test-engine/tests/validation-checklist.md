# Test Engine — Validation Checklist

Run this checklist before accepting a test plan as complete.

## Trigger Check

- [ ] Task involves writing, reviewing, or improving tests.
- [ ] Task is NOT pure refactoring with no testing component.

## Test Plan Check

- [ ] Test levels chosen are the lowest cost that prove the behavior.
- [ ] Happy-path cases are present.
- [ ] Failure and edge-case cases are present.
- [ ] E2E tests are noted as deferred if the environment is unavailable.

## Cases Check

- [ ] Every case follows GIVEN/WHEN/THEN format.
- [ ] Every case has a type (unit, integration, e2e) and priority.
- [ ] Every case is independently runnable without shared mutable state.

## Coverage Gaps Check

- [ ] Every behavior not tested is listed in coverage-gaps.
- [ ] Deferred tests have a clear re-enable condition.

## Risk Check

- [ ] Remaining coverage risk is stated after the plan.
- [ ] Gaps that block a release are clearly distinguished from optional coverage.

## Error Format

```text
error: <what went wrong during test design>
gap: <behavior that could not be tested>
recovery: <action taken — e.g., deferred E2E test, noted coverage gap>
```
