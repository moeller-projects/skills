# Rule: Estimate Integrity

> Impact: high

## Description

Estimates must reflect actual understanding of the work. When understanding is incomplete, the estimate must be marked unreliable rather than assigned a confident size that will mislead planning.

## Apply When

- Assigning S / M / L estimates to any task.

## Checks

- `estimate_reliability: low` is set for any task where the scope, approach, or dependencies are not fully understood.
- Time-based estimates are only used when they are more meaningful than relative sizing in the given context.
- Spike tasks include a fixed timebox rather than an open-ended estimate.
- No estimate is provided for a task that depends on an unresolved unknown — it is left blank or marked as pending.

## Anti-Pattern

Assigning M to every task to avoid difficult conversations about uncertainty. Or marking a task L because it feels hard, without identifying what specifically makes it hard — which prevents the team from breaking it down further.
