# Rule: Resilience and Rollback

> Impact: critical

## Description

Every operational plan MUST define failure handling, rollback triggers, and recovery expectations before execution begins.

## Apply When

- The change can affect availability, data integrity, or runtime behavior.

## Checks

- Rollback steps are realistic for the proposed change.
- Recovery checks and stop conditions are clear.

## Anti-Pattern

Approving an ops change because it should work while having no tested path back if it does not.
