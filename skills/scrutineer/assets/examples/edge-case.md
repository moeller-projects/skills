# Edge-Case Example — Scrutineer: Oversized Diff

## Input

Pull request: "Upgrade ORM and migrate all models". 4,800 changed lines across 96 files: 88 mechanical model migrations, 3 handwritten query rewrites, 5 generated snapshots.

## Process

1. Diff is too large for one responsible pass — split explicitly and state the split.
2. Pass 1: the 3 handwritten query rewrites (full scrutiny).
3. Pass 2: a stratified sample of the 88 mechanical migrations (every distinct migration pattern, one file each).
4. Pass 3: generated snapshots — verify generator config only, not the output.

## Output

```text
verdict: request-changes
summary: 96-file ORM migration reviewed in three stated passes (handwritten queries, migration-pattern sample, generator config); one handwritten query loses its index.

findings:
- [blocker] src/reports/usage.ts:44 — rewritten query drops the `WHERE tenant_id = ?` predicate
  why: cross-tenant data leak on the usage report
  suggestion: restore the tenant predicate and add a regression test that asserts row scoping
- [major] src/billing/history.ts:102 — hand-rolled pagination reads unbounded rows into memory
  why: the old ORM lazy cursor was replaced by `findAll()`; history tables are large
  suggestion: use the new ORM's streaming cursor API
- [minor] migration pattern B renames columns without `down()` reversal
  why: rollback of this PR would leave the schema ahead of the code
  suggestion: add `down()` migrations for the pattern-B files (14 files, listed in review comment)

out-of-scope:
- 88 mechanical migrations verified by pattern sample only — full-file review deferred to a second reviewer or follow-up pass
- generated snapshots not line-reviewed; generator config diff was clean

risk:
- Unsampled migration files may contain a fourth pattern variant not present in the sample
```
