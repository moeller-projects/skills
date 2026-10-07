# Rule: Unknown Exposure

> Impact: critical

## Description

Every unresolved question that affects scope, feasibility, or estimate reliability must be named as an explicit unknown — never buried inside a task description or silently absorbed into an estimate.

## Apply When

- Any part of the plan depends on information that has not been confirmed.

## Checks

- Unknowns are collected in a dedicated section with unique IDs (U-01, U-02, ...).
- Each unknown names what must be resolved and who can resolve it.
- Tasks that depend on an unresolved unknown are marked as blocked until it is resolved.
- If an unknown blocks all tasks, the plan stops at surfacing the unknown — no fabricated plan is produced.

## Anti-Pattern

Burying an assumption inside a task title ("implement auth — assuming OAuth is already configured") so that reviewers commit to an estimate without realising the dependency. Or assigning a confident M estimate to a task that depends on an unresolved architectural decision.
