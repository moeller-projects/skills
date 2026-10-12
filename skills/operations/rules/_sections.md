# Rule: Standard Sections

> Impact: medium

## Description

Organize output into risk, plan, checks, rollback, and security so operational decisions are reviewable before execution.

## Apply When

- Producing an infrastructure, release, or threat-model recommendation.

## Checks

- Risks and rollback steps are explicit, not implied.
- Security notes are separated from general operational checks.

## Anti-Pattern

Recommending an ops change with no rollback path or clear validation criteria.
