# Edge-Case Example — Test Engine: Unavailable E2E Environment

## Scenario

Developer asks: "Add E2E tests for the checkout flow using Playwright."

## Why This Is an Edge Case

The E2E test environment (staging with payment sandbox) is not available.
The skill must plan the tests and note the gap rather than fabricating passing tests.

## Expected Output

```text
test-plan:
1. Unit: cart total calculation with various item quantities and discounts
2. Integration: order submission API with mock payment provider
3. E2E: full checkout flow — BLOCKED (staging + payment sandbox unavailable)

coverage-gaps:
- E2E checkout flow blocked: staging environment not available
- Payment provider Stripe test mode not configured
- No smoke test for successful order confirmation email (requires email sandbox)

cases:
- case: cart total with two items and 10% coupon
  given: cart=[{price:50, qty:2}, {price:30, qty:1}], coupon=SAVE10
  when: calculateCartTotal is called
  then: returns 117 (130 * 0.9)
  type: unit
  priority: critical

- case: order submission returns 201 with valid payload
  given: valid order payload with mock Stripe token
  when: POST /api/orders is called
  then: returns 201 with orderId in response body
  type: integration
  priority: critical

- case: E2E checkout flow — DEFERRED
  given: staging environment available with Stripe test mode
  when: user adds item, enters card details, confirms purchase
  then: order confirmation page displays with order ID
  type: e2e
  priority: high
  note: BLOCKED — re-enable when staging and Stripe sandbox are configured

risk:
- E2E coverage gap: full checkout flow not validated end-to-end until environment is ready
- Stripe webhook handling not tested (requires integration with webhook simulator)
```

## Why This Is Correct

- E2E tests are planned but explicitly deferred with a reason.
- Coverage gaps are listed so the team knows what is missing.
- Lower-cost unit and integration tests are delivered immediately.
- Deferred case has a clear re-enable condition.
- Risk is stated so stakeholders can decide whether to unblock environment.
