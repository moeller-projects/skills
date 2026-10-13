# Rule: Read-Only Boundary

> Impact: critical

## Description

Read-mode scripts may only fetch Azure DevOps data with GET requests and must emit deterministic, normalization-safe output.

## Apply When

- Implementing or updating any read-mode script or read workflow in `azure-devops`.

## Checks

- Read-mode scripts use GET requests only, with bounded retries for GET transport failures.
- Read-mode scripts do not accept mutation flags or execute write actions.
- Read-mode output follows comment continuation tokens and redacts secrets recursively before emission.
- Read-mode output stays deterministic and safe for downstream normalization; incomplete combined sources are explicit partial output.
- Write workflows remain in separate scripts that follow `rules/write-boundary.md`.

## Anti-Pattern

Adding a convenience mutation path to a read script or mixing read and write behavior behind a flag.
