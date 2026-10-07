# Rule: Vertical Slicing

> Impact: critical

## Description

Every task must deliver an independently shippable slice of value end-to-end — from input to observable output — rather than a horizontal layer such as "write all models" or "write all tests."

## Apply When

- Breaking a feature, spec, or refactor into tasks.

## Checks

- Each task can be merged, deployed, and verified independently.
- No task is purely a layer or phase (data layer, service layer, UI layer) with no standalone value.
- A task that cannot be made vertical is either split further or turned into a spike with a timebox.

## Anti-Pattern

Producing tasks like "implement all database migrations" followed by "implement all API endpoints" followed by "implement all UI components" — these are phases, not shippable slices. A reviewer cannot verify progress until the last phase lands.
