# Edge-Case Example — Code Review: No Profiling Data

## Scenario

Developer asks: "Optimize the `processOrders` function — it feels slow."

## Why This Is an Edge Case

Performance claim is subjective. No profiling data, no benchmark, no production metrics.

## Expected Output

```text
findings:
- none

patch-plan:
1. Profile representative order-processing workloads and record query counts, payload sizes, and timings
2. Reassess optimization candidates only after measurement identifies a confirmed bottleneck

risk:
- No profiling or benchmark data → do not ship a performance patch yet; establish a baseline first

```

## Why This Is Correct

- Records no supported defect while evidence is absent.
- Makes measurement the ordered next step rather than assigning unsupported severity.
- States the need for measurement before claiming the fix works.
- Does not manufacture profiling data or invent metrics.
