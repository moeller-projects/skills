# Decision Record Example

## Scenario

Team decides to use `jsonschema` for runtime validation instead of hand-rolled checks.

## Expected Output

```text
decision:
  context: The emit-handoff pipeline needed contract validation. Hand-rolled jq checks
           were growing difficult to maintain and had gaps around additionalProperties.
  decision: Use Python jsonschema (stdlib-compatible) for contract validation in
           validate-handoff.py, with a jq structural fallback when unavailable.
  reasoning: jsonschema provides complete Draft-2020-12 coverage including
             additionalProperties, enum, and const constraints. The jq fallback
             preserves zero-dependency operation in constrained environments.
             Alternative considered: fully custom Python walker — rejected because
             it would need to re-implement schema keywords already in jsonschema.
  tradeoffs: Adds a soft dependency on python3-jsonschema. Environments without it
             fall back to the jq path, which covers required fields and enum values
             but not additionalProperties or const.
  reuse_scope: ado-gateway validate-handoff.py; applicable to any skill that needs JSON Schema validation with a constrained-environment fallback.
```

## Why This Is Correct

- All five fields are present.
- `reasoning` names the rejected alternative (custom walker) and why it was rejected.
- `tradeoffs` is honest about the soft dependency.
- `reuse_scope` names the exact file and generalizes the pattern.
