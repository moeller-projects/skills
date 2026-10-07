# Happy-Path Example — Test Engine

## Scenario

Developer says: "Write tests for the `calculateDiscount(price, couponCode)` function."

## Input Context

- Function: `calculateDiscount(price: number, couponCode: string): number`
- Behavior: returns discounted price; 10% for `SAVE10`, 20% for `SAVE20`, no discount for unknown codes.
- No existing tests.

## Expected Output

```text
test-plan:
1. Unit: happy-path discount application for each known coupon
2. Unit: unknown coupon returns original price
3. Unit: edge cases — zero price, negative price, empty coupon string

coverage-gaps:
- No integration test for coupon validation against the database (out of scope for unit tests)
- No test for concurrent coupon use (different concern; flag for integration layer)

cases:
- case: SAVE10 applies 10% discount
  given: price=100, couponCode="SAVE10"
  when: calculateDiscount is called
  then: returns 90
  type: unit
  priority: critical

- case: SAVE20 applies 20% discount
  given: price=100, couponCode="SAVE20"
  when: calculateDiscount is called
  then: returns 80
  type: unit
  priority: critical

- case: unknown coupon returns original price
  given: price=100, couponCode="UNKNOWN"
  when: calculateDiscount is called
  then: returns 100
  type: unit
  priority: high

- case: zero price returns zero
  given: price=0, couponCode="SAVE10"
  when: calculateDiscount is called
  then: returns 0
  type: unit
  priority: medium

- case: empty coupon string returns original price
  given: price=50, couponCode=""
  when: calculateDiscount is called
  then: returns 50
  type: unit
  priority: medium

risk:
- DB coupon validation not covered at unit level — requires integration test
```

## Why This Is Correct

- Unit level chosen as lowest cost for pure function.
- Happy path and edge cases both covered.
- Coverage gaps are explicit, not hidden.
- Every case follows GIVEN/WHEN/THEN.
- Each case is independently runnable.
