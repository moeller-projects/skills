# Workflow

## Default Flow

1. Define the behavior to prove and the risk if it breaks.
2. Choose the right test level: unit, integration, or end-to-end.
3. Add core, edge, and failure cases with stable setup and assertions.
4. Call out remaining coverage gaps and flake risks.

## Fast Path

1. Write the smallest high-value case for the changed behavior.
2. Add one edge or regression case if risk is non-trivial.

## Escalation

Use more detail only when correctness, safety, or ambiguity requires it.
