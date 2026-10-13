# Happy-Path Example — Task Planning

## Scenario

PM shares a confirmed spec: "Add password reset via email. SendGrid is integrated.
No existing reset flow. Postgres user table."

## Why This Is the Happy Path

Scope is clear, dependencies are known, no blocking unknowns.

## Expected Output

```text
tasks:
- id: T-01
  title: Ship password-reset request flow end to end
  estimate: M
  estimate_reliability: high
  depends_on: []
  done_when: Users can request a reset, the service stores a hashed 15-minute token, and SendGrid delivers a reset link; staging verification and tests pass.

- id: T-02
  title: Ship password-reset confirmation flow end to end
  estimate: M
  estimate_reliability: high
  depends_on: [T-01]
  done_when: Users can submit a valid link to set a new password and log in; expired or used tokens return 410; staging verification and tests pass.

- id: T-03
  title: Ship password-reset abuse protection end to end
  estimate: S
  estimate_reliability: high
  depends_on: [T-01]
  done_when: Requests are limited to six per hour per email, excess requests return 429, and the limit is verified in an integration test.

dependencies:
- T-01 → T-02: confirmation requires reset tokens and links from the request flow
- T-01 → T-03: rate limiting must wrap the shipped request flow (T-02 and T-03 can proceed in parallel)

risks:
- SendGrid sandbox vs production behaviour difference — low / medium
- Token generation using non-cryptographic random source — low / critical

critical_path:
- T-01 → T-02

unknowns: none

validation:
- Run full reset flow in staging: request email, click link, set new password, confirm login works.
- Confirm used and expired tokens return 410.
- Confirm rate limiting rejects at threshold.

```

## Why This Is Correct

- Every task is a vertical slice with a concrete done_when condition.
- T-03 is correctly shown as parallelizable with T-02 after T-01 ships.
- No unknowns are present but the section is explicit about that.
- Risks name the specific failure mode, not generic concerns.
