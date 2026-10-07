# Edge-Case Example — Delivery Engine: Unknown-Blocked Plan

## Scenario

Engineer asks: "Break down the work for migrating from REST to GraphQL."
No spec exists. Target schema unknown. Client app ownership unclear.

## Why This Is an Edge Case

The two most critical delivery questions — what the new schema looks like and who
owns the client migration — are unresolved. A fabricated plan would produce
unreliable estimates and a false sense of readiness.

## Expected Output

```text
tasks:
- id: T-01
  title: Spike — audit existing REST endpoints and map to candidate GraphQL schema
  timebox: 2 days
  estimate_reliability: low
  depends_on: []
  done_when: Schema candidates documented; U-01 resolved or escalated.

- id: T-02
  title: Spike — identify client app ownership and coordinate migration strategy
  timebox: 1 day
  estimate_reliability: low
  depends_on: []
  done_when: U-02 resolved; client team committed to migration timeline.

dependencies:
- T-01 and T-02 are parallelizable; all subsequent tasks depend on both being resolved.

risks:
- GraphQL schema design decisions have wide blast radius across all clients — high / high
- REST and GraphQL running in parallel creates dual-maintenance surface — medium / high

critical_path:
- T-01 (parallel T-02) → schema review → implementation tasks (not yet plannable)

unknowns:
- U-01: What is the target GraphQL schema? Who owns schema design decisions?
        owner: tech lead — must be resolved before implementation tasks can be estimated.
- U-02: Which client apps consume the REST API? Who owns each client migration?
        owner: product team — must be resolved before client migration tasks can be planned.

validation:
- Cannot define end-to-end validation until U-01 and U-02 are resolved.
  Re-run delivery-engine after spike outputs are available.
```

## Why This Is Correct

- No implementation tasks are fabricated while blocking unknowns remain open.
- Spikes are the only output when understanding is insufficient for real tasks.
- Each spike has a fixed timebox, not an open-ended estimate.
- The critical path is honest about what is not yet plannable.
- The output explicitly instructs re-running the skill once unknowns are resolved.
