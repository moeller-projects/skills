# Delivery Engine — Validation Checklist

Run this checklist before accepting a delivery plan as complete.

## Trigger Check

- [ ] Scope is confirmed — spec or brief exists before task breakdown begins.
- [ ] Task is NOT writing requirements or acceptance criteria — use spec-engine first.

## Task Quality Check

- [ ] Every task is independently shippable — no horizontal layers (data layer, API layer, UI layer).
- [ ] Every task has a concrete `done_when` condition that is verifiable, not subjective.
- [ ] Tasks that cannot be made atomic are replaced with spikes that have a timebox and a decision-output done condition.

## Estimate Check

- [ ] Every task has an estimate (S / M / L) or a timebox (for spikes).
- [ ] `estimate_reliability: low` is set for any task with unresolved unknowns or unvalidated assumptions.
- [ ] No estimate is fabricated for a task that depends on an unresolved unknown.

## Unknowns Check

- [ ] All unknowns are in the `unknowns:` section with a unique ID (U-01, U-02, ...).
- [ ] Each unknown names what must be resolved and who can resolve it.
- [ ] No unknown is hidden inside a task title or description.
- [ ] If there are no unknowns, the section explicitly states `unknowns: none`.

## Dependencies Check

- [ ] Hard blockers are distinguished from soft ordering preferences.
- [ ] Each dependency states why it is a dependency, not just that it exists.

## Critical Path Check

- [ ] Critical path is listed as an ordered chain of task IDs.
- [ ] Tasks not on the critical path are identifiable as parallelizable.
- [ ] If all tasks are independent, the plan states that explicitly.

## Validation Check

- [ ] Validation steps cover the full delivery, not just individual tasks.
- [ ] Validation is concrete and executable.

## Error Format

```text
error: <what went wrong during planning>
unknown: <what must be resolved before planning can continue>
recovery: <action taken — e.g., replaced tasks with spikes, stopped plan at unknown>
```
