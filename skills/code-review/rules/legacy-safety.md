# Rule: Legacy Safety

> Impact: high

## Description

Respect fragile legacy constraints by preserving behavior, sequencing risky changes carefully, and making modernization incremental.

## Apply When

- Touching old, under-tested, or business-critical code paths.

## Checks

- MUST identify coupling or hidden dependencies that raise migration risk.
- MUST break modernization into safe, reviewable steps.

## Anti-Pattern

Replacing a legacy pattern wholesale without proving compatibility or rollback safety.
