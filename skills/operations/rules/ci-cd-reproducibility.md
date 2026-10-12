# Rule: CI/CD Reproducibility

> Impact: high

## Description

Ensure build and delivery workflows are deterministic, pinned where needed, and repeatable across environments and reruns.

## Apply When

- Creating or reviewing CI/CD pipelines.

## Checks

- Inputs, dependencies, and environments MUST be controlled or pinned appropriately.
- The same revision MUST be rebuildable and verifiable consistently.

## Anti-Pattern

Allowing pipelines to depend on mutable state, floating inputs, or hidden local assumptions.
