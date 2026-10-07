# Rule: Mitigate First

> Impact: critical

## Description

Stop the bleeding before diagnosing the wound. Root-cause analysis during an active outage burns the time mitigation would have saved.

## Apply When

- Any live incident where impact is ongoing.

## Checks

- A mitigation (rollback, flag, failover, rate limit) is attempted or explicitly ruled out before root-cause work begins.
- Mitigations are reversible by default; destructive mitigations require explicit approval.
- Only one mitigation variable changes at a time.

## Anti-Pattern

Reading stack traces for forty minutes while a known-good rollback sits unused.
