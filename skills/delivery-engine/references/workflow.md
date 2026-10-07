# Workflow

## Default Flow

1. Confirm scope, success bar, and constraints before producing any tasks.
2. Break work into vertical slices — each independently shippable end-to-end.
3. Map hard dependencies (blockers) and soft dependencies (ordering preferences) separately.
4. Assign S / M / L estimates; mark `estimate_reliability: low` wherever understanding is incomplete.
5. Define a concrete `done_when` condition for every task.
6. Collect all unknowns with owner names into the unknowns section.
7. Trace the critical path through the dependency graph.
8. List validation steps for the full delivery, not just individual tasks.

## Spike Path

When a task cannot be made atomic because the approach is unknown:

1. Replace the task with a spike.
2. Give the spike a fixed timebox (hours or days), not a size estimate.
3. Define `done_when` as a decision or artifact that unblocks the next real task.
4. Hold all downstream tasks until the spike resolves.

## Fast Path

For small, single-engineer deliveries where full structure adds noise:

1. Write a numbered task list with inline estimates and done conditions.
2. State unknowns and critical path in one line each.
3. Skip the full template unless a reviewer or teammate needs to act on the output.

## Escalation

Use the full template when the work spans more than one engineer, more than one sprint,
or has dependencies that could affect other teams or systems.
