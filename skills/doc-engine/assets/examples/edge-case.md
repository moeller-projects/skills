# Edge-Case Example — Doc Engine: Missing Source Material

## Scenario

Developer asks: "Update the AGENTS.md to describe how our agents should handle DB migrations."

## Why This Is an Edge Case

The DB migration process is not documented anywhere, and the developer has not described it.
The skill must avoid inventing steps while still delivering value.

## Expected Output

```text
doc:
- purpose: guide agents through the DB migration workflow without introducing errors
- audience: coding agents operating in this repository
- structure:
  1. When to run migrations [reference] — trigger conditions
  2. Migration commands [how-to] — exact commands with flags
  3. Rollback procedure [how-to] — how to reverse a failed migration
  4. Safety gates [reference] — checks before and after applying

changes:
- AGENTS.md — added "Database Migrations" section (skeleton with gaps marked)

gaps:
- migration tool not identified (Flyway? Liquibase? custom script?) — ask developer
- rollback command not confirmed — do not document until verified
- test environment migration behavior unknown — needs clarification

DRAFT SKELETON (do not publish until gaps are filled):

## Database Migrations

> ⚠️ DRAFT — gaps below must be resolved before merging.

**Run migrations when:** <!-- TODO: confirm trigger -->

**Command:** <!-- TODO: confirm command -->

**Rollback:** <!-- TODO: confirm rollback command -->

**Safety checks:**
- [ ] <!-- TODO: list checks -->
```

## Why This Is Correct

- Delivers a useful skeleton without fabricating unverified steps.
- Marks every gap explicitly with TODO comments.
- Does not publish speculative commands that could break production.
- Flags the draft status clearly so it is not used prematurely.
