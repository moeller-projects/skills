# Edge-Case Example — Thinking Engine: Only One Viable Option

## Scenario

Lead asks: "Should we use our existing Postgres DB for the job queue, or add Redis?"

## Why This Is an Edge Case

After assumption audit, only one option is genuinely viable given the constraints.
The skill must state this explicitly rather than manufacturing false alternatives.

## Input Context

- Team: 1 engineer.
- Timeline: must ship in 3 days.
- Infra budget: $0 additional (no new services this quarter).
- Current stack: Postgres already in use; no Redis instance.

## Expected Output

```text
problem:
- restatement: choose a job queue implementation that ships in 3 days with no new infra spend
- constraints: 1 engineer, 3-day deadline, $0 infra budget, no Redis instance
- success-bar: jobs enqueue and process reliably without dropping work on restart

assumptions:
- job volume is low-to-medium (< 1000 jobs/day) — risk: high if volume spikes; revalidate
- Postgres transactional guarantees are sufficient for at-least-once delivery — risk: low
- no Redis means provisioning Redis is not an option this sprint — risk: low (budget constraint confirmed)

options:
1. Postgres-backed queue (e.g., pg-boss or custom advisory lock table): achievable in 3 days with no new infra spend
   pros: uses existing Postgres, fits budget, keeps operational surface area flat
   cons: adds load to the primary DB; may not scale past higher job volume
   cost: low

recommendation:
- choice: Postgres-backed queue
- reason: Redis and hosted queue options are ruled out by hard budget and timeline constraints
- blind-spots: monitor DB load and revisit if volume trends toward >10k jobs/day

next:
- evaluate pg-boss vs custom advisory lock implementation (2 hours)
- open: what is the expected job volume per day? (determines whether Postgres queue
  is safe long-term or a 6-month bridge solution)
```

## Why This Is Correct

- Only one viable option given hard constraints.
- Alternatives ruled out are stated with explicit reasons, not silently dropped.
- Blind spots are called out.
- Open question surfaces the volume assumption that determines long-term viability.
