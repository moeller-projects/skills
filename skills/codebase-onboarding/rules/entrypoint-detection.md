# Rule: Entrypoint Detection

> Impact: high

## Description

Identify the real execution, build, and runtime entry points that a contributor or agent must know before changing behavior.

## Apply When

- A repo map or onboarding artifact is being created.

## Checks

- Include startup scripts, package entry points, workflows, or handlers that initiate execution.
- Distinguish primary entry points from helper modules.

## Anti-Pattern

Listing random source files without highlighting where execution actually begins.
