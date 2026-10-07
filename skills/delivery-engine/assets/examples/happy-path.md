# Happy-Path Example — Delivery Engine

## Scenario

PM shares a confirmed spec: "Add password reset via email. SendGrid is integrated.
No existing reset flow. Postgres user table."

## Why This Is the Happy Path

Scope is clear, dependencies are known, no blocking unknowns.

## Expected Output

```text
tasks:
- id: T-01
  title: Add reset token table and migration
  estimate: S
  estimate_reliability: high
  depends_on: []
  done_when: Migration runs in staging; tokens table exists with correct schema.

- id: T-02
  title: Implement reset request endpoint (POST /auth/reset)
  estimate: M
  estimate_reliability: high
  depends_on: [T-01]
  done_when: Endpoint stores hashed token, returns 200, sends no email yet.
             Unit tests cover happy path and unknown-email no-op.

- id: T-03
  title: Wire SendGrid email for reset link
  estimate: S
  estimate_reliability: high
  depends_on: [T-02]
  done_when: Reset email delivered in staging with correct link and 15-min expiry.
             Verified with SendGrid activity log.

- id: T-04
  title: Implement token validation and password update endpoint (POST /auth/reset/confirm)
  estimate: M
  estimate_reliability: high
  depends_on: [T-03]
  done_when: Valid token sets new password and marks token used.
             Expired or used token returns 410. AC-02 and AC-03 pass.

- id: T-05
  title: Add rate limiting to reset endpoint
  estimate: S
  estimate_reliability: high
  depends_on: [T-02]
  done_when: 6 requests per hour per email rejected with 429. Verified with integration test.

dependencies:
- T-01 → T-02: token table must exist before endpoint can write tokens
- T-02 → T-03: endpoint must exist before email can reference the token
- T-03 → T-04: email flow must work before confirm endpoint is meaningful to test end-to-end
- T-02 → T-05: endpoint must exist before rate limiting can be applied (parallelizable with T-03)

risks:
- SendGrid sandbox vs production behaviour difference — low / medium
- Token generation using non-cryptographic random source — low / critical

critical_path:
- T-01 → T-02 → T-03 → T-04

unknowns: none

validation:
- Run full reset flow in staging: request email, click link, set new password, confirm login works.
- Confirm used and expired tokens return 410.
- Confirm rate limiting rejects at threshold.
```

## Why This Is Correct

- Every task is a vertical slice with a concrete done_when condition.
- T-05 is correctly shown as parallelizable with T-03 — it is off the critical path.
- No unknowns are present but the section is explicit about that.
- Risks name the specific failure mode, not generic concerns.
