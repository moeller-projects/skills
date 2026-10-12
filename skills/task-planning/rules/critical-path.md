# Rule: Critical Path

> Impact: high

## Description

Identify the dependency chain that determines the earliest possible completion date. Work on the critical path has no slack — any delay there delays the whole delivery. Work off the critical path can be parallelized or deprioritized.

## Apply When

- The task list has two or more tasks with dependencies between them.

## Checks

- The critical path is listed explicitly as an ordered chain of task IDs.
- Tasks on the critical path are identifiable so they receive priority attention.
- Tasks not on the critical path are noted as parallelizable where relevant.
- If all tasks are independent (no hard dependencies), state that explicitly rather than fabricating a critical path.

## Anti-Pattern

Listing tasks in an arbitrary order that implies a serial execution plan when many tasks could be parallelized. Or omitting the critical path entirely so the team discovers the bottleneck only when the deadline is near.
