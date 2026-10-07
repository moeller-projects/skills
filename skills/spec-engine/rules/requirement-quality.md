# Rule: Requirement Quality

> Impact: critical

## Description

Require each requirement to be clear, scoped, testable, and free of avoidable ambiguity.

## Apply When

- Turning user intent into formal requirements.

## Checks

- Requirements describe outcomes, not vague aspirations.
- Unclear verbs, missing actors, and hidden dependencies are surfaced.
- The following words and phrases are banned because they make requirements untestable: should, might, maybe, as needed, where appropriate, etc., and so on, user-friendly, better, faster, seamless, intuitive.

## Anti-Pattern

Shipping a spec with fuzzy language like better, faster, or user-friendly and no measurable meaning.

Example of banned language and its correction:

- ❌ "The checkout flow should be faster and more user-friendly."
- ✅ "The checkout flow must complete within 2 seconds on a 4G connection and must not require more than 3 user interactions to submit an order."
