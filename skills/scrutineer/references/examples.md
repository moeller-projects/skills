# Scrutineer — Sample Reviews

## Example 1: Feature PR with a blocker

Changeset: `src/orders/discount.ts` adds a percentage discount; `src/orders/checkout.ts` applies it.

```text
verdict: request-changes
summary: Adds percentage discounts to checkout; logic is sound except an unguarded division that can produce NaN totals.

findings:
- [blocker] src/orders/discount.ts:14 — division by zero when itemCount is 0
  why: checkout crashes or persists NaN totals for empty carts that pass validation upstream
  suggestion: guard `itemCount === 0` and return the undiscounted subtotal
- [major] src/orders/checkout.ts:42 — discount applied after tax calculation
  why: tax authority expects tax on the discounted amount; current order overcharges tax
  suggestion: apply discount before `computeTax()` and add a regression case
- [nit] src/orders/discount.ts:3 — `pct` is abbreviated while neighbors use full names
  why: consistency with the module's naming convention
  suggestion: rename to `percentage`

out-of-scope:
- src/orders/legacy-pricing.ts still uses floating-point money — pre-existing, ticket separately

risk:
- Existing carts serialized with pre-discount totals will show a one-time price change on re-render
```

## Example 2: Clean changeset

```text
verdict: approve
summary: Renames `fetchUser` to `loadUser` across the app; mechanical, complete, tests updated.

findings:
- none

out-of-scope:
- none

risk:
- External consumers of the internal `api/` barrel export will break on next publish; flag in release notes
```

## Example 3: Unverifiable suspicion becomes a question

```text
verdict: comment
summary: Adds retry logic to the payment webhook; one behavior cannot be confirmed from the diff alone.

findings:
- [minor] src/billing/webhook.ts:31 — question: does the gateway deduplicate retried events by `event_id`?
  why: if not, retries will double-charge
  suggestion: confirm against the gateway docs; if undeduplicated, key retries on `event_id`

out-of-scope:
- none

risk:
- Retry storm possible if the gateway rate-limits; no backoff cap visible in the diff
```
