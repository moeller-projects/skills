# Edge-Case Example — Spec Engine: Conflicting Requirements

## Scenario

Stakeholders disagree on behavior: "User sessions should expire after 30 minutes" (security team)
vs "Users should stay logged in for 30 days" (product team).

## Why This Is an Edge Case

Two requirements directly conflict. The spec must surface the conflict rather than silently
choose one side.

## Expected Output

```text
spec:
- goal: define session lifetime behavior for authenticated users
- scope:
  - IN: session expiration policy, inactivity timeout, remember-me behavior
  - OUT: OAuth token refresh, mobile app session handling
- requirements:
  - REQ-01: CONFLICT — session expiration policy is disputed (see OQ-01)
  - REQ-02: session tokens must be invalidated server-side on logout (agreed)
  - REQ-03: users must be notified 5 minutes before session expiry if the short policy is chosen (security team requirement)
- acceptance_criteria:
  - AC-01 (REQ-02): GIVEN a logout action WHEN completed THEN the session token returns 401 on next use
  - AC-02 (REQ-03): GIVEN 25 minutes have elapsed WHEN short policy is active THEN user receives an expiry warning

quality_gates:
- [ ] Expiration policy decision documented and signed off by security and product
- [ ] Session token storage reviewed: must use httpOnly, Secure, SameSite=Strict cookies

risk_tier: High

open_questions:
- OQ-01: session lifetime — 30 minutes (security) or 30 days (product)? — owner: CTO — due: before implementation starts
  options:
    A: 30-minute absolute expiry with explicit re-authentication
    B: 30-day sliding window with inactivity timeout at 30 minutes
    C: configurable per user (requires additional scope)
```

## Why This Is Correct

- Conflict is surfaced as OQ-01, not silently resolved.
- Both conflicting positions are stated.
- Options are presented to help the decision-maker choose.
- Requirements that are agreed are still captured.
- Implementation is blocked until OQ-01 is resolved.

## OpenSpec Edge-Case Serialization Note

- Keep the conflict as an unresolved item in proposal/scenario content.
- Do not downgrade conflicts into implementation assumptions when converting to OpenSpec.
