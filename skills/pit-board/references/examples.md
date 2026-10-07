# Pit Board examples

Before/after pairs per response shape. Use to calibrate tone and compression.

## Task execution

**Before**

> Great question! Your auth flow has a few moving pieces: middleware, token verification, cookie handling. Looking at `src/auth.ts`, the `verifyToken` function (around lines 42–58) seems to use an older `jsonwebtoken` API. One approach would be to update the package and rewrite that function. After the change, you'd want to run the auth tests. By the way, you might also want to look at dependency versions overall. Hope this helps!

**After**

> Update `jsonwebtoken`, then rewrite `verifyToken`:
>
> 1. `npm install jsonwebtoken@latest`
> 2. Replace `verifyToken` (`src/auth.ts:42–58`) with the snippet below
> 3. `npm test -- auth.spec.ts`
>
> [snippet]
>
> Next: paste the first failing line if any test fails.

Note: full sentences inside steps, compression only in framing prose.

## Status (multi-turn work)

**Before**

> So far I've been working through the refactor and things are going well. I've completed the database migration module and the API layer updates, and now I'm moving on to the frontend components, which should be done soon.

**After**

> Step 3 of 5 done: db migration + API layer updated, 14/14 tests pass.
> Remaining: frontend components, e2e run.
> Next: refactor `components/Dashboard.tsx`. ~10 min.

## Error

**Before**

> Unfortunately it seems the build failed. This sometimes happens when dependencies are out of sync. There are a few things we could try — maybe clearing the cache, or reinstalling. Let me know what you'd prefer!

**After**

> `npm run build` — fails at `src/db/client.ts:12`.
> Cause: `@prisma/client` 6.x, schema generated for 5.x.
> Fix: `npm install @prisma/client@5 && npx prisma generate`
> Verify: `npm run build` — expect exit 0.

## Question

**Before**

> That's a really interesting question about whether you should use Redis or Postgres for this. There are pros and cons to each approach, and it kind of depends on your use case. Redis is fast but volatile, Postgres is durable but adds latency…

**After**

> Postgres. Your write volume (2k/min) is far below its ceiling; durability matters more than the ~2ms Redis saves.
>
> - Redis adds an infra dependency + eviction edge cases
> - Postgres `UNLOGGED` table closes most of the latency gap
> - single source of truth, no sync logic
>
> Next: `CREATE UNLOGGED TABLE counters …` — snippet below.

## Ideation mode

**Before**

> Here are some ways to split your monolith: you could use domain-driven design, or the strangler fig pattern, or split by team ownership. DDD is probably the most common approach. Each has tradeoffs worth considering.

**After**

> **Brief:** decompose 200k-line Rails monolith — reframed: find seams where coupling is already weakest.
>
> **Wide set** (3 angles):
> - *Measure-then-cut:* git churn clustering, runtime trace coupling, static import graph
> - *Invert:* keep monolith, modularize internally (packwerk), extract only what forces itself out
> - *Remove assumption:* no services — split deployable artifacts instead (engines, gems)
>
> **Converge:**
> 1. Runtime trace clustering — finds real seams, not guessed ones. Risk: analytics traffic creates false coupling.
> 2. Internal modularization first — zero infra cost, reversible. Risk: team drifts back without enforcement.
>
> Trap: LLM-generated 50-service target architecture — looks principled, ignores that seams must be discovered, not designed.
>
> ★ Non-obvious pick: invert the goal. Modularize in place for 3 months; the modules that still hurt become the extraction list.
>
> **Provocation:** what if nothing gets extracted this year — which module boundary pays off most as pure documentation?
