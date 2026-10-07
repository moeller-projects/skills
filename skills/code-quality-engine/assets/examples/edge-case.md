# Edge-Case Example — Code Quality Engine: No Profiling Data

## Scenario

Developer asks: "Optimize the `processOrders` function — it feels slow."

## Why This Is an Edge Case

Performance claim is subjective. No profiling data, no benchmark, no production metrics.

## Expected Output

```text
findings:
- [medium] orders/processor.ts:88 — N+1 query inside loop fetches product for each order
  why: 1000-order batch = 1001 DB queries; likely cause of perceived slowness
  fix: batch-fetch products before loop with a single SELECT ... IN (...)

- [low] orders/processor.ts:102 — synchronous JSON.stringify on large payload
  why: blocks event loop; low risk unless payloads exceed ~1 MB
  fix: defer to background worker if payload size grows

patch-plan:
1. orders/processor.ts:88 — batch product fetch (highest-value, evidence-backed)
2. orders/processor.ts:102 — defer; revisit only with profiler data showing impact

risk:
- Batch query changes SQL; verify query plan and index coverage on orders.product_id
- No benchmark → cannot confirm speedup; measure before/after with k6 or similar
```

## Why This Is Correct

- Identifies the most probable bottleneck (N+1) without speculating beyond it.
- Defers the lower-value change explicitly with a condition.
- States the need for measurement before claiming the fix works.
- Does not manufacture profiling data or invent metrics.
