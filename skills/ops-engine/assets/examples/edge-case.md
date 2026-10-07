# Edge-Case Example — Ops Engine: Unacceptable Risk Without Mitigation

## Scenario

Manager asks: "Deploy the new `payments-service` directly to production — we need it live tonight."

## Why This Is an Edge Case

Threat model surfaces a critical risk with no safe mitigation path available at deploy time.
The skill must abort the plan rather than proceed.

## Expected Output

```text
risk:
- payments-service has no integration tests for the charge flow — high / critical
- No canary or blue/green strategy configured — high / critical
- Rollback requires manual DB migration reversal; no script exists — high / critical

ABORT: deploying without mitigation paths for critical risks is not safe.

Required before proceeding:
1. Charge flow integration tests must pass in staging.
2. A canary or feature-flag strategy must be in place to limit blast radius.
3. A tested rollback script for the DB migration must exist and be verified.
4. Human approval required for the next production deployment after this block is lifted.

plan: BLOCKED — reopen when the three items above are resolved.

checks:
- [ ] Integration tests pass in CI for payments-service
- [ ] Canary strategy documented and reviewed
- [ ] Rollback script tested against a staging DB snapshot

rollback: N/A — plan is blocked; no steps will be executed.

security:
- Payment data in transit must use TLS 1.2+; confirm before unblocking.
- PCI scope of new service must be reviewed before production traffic.
```

## Why This Is Correct

- Threat model identified critical risks with no mitigation path.
- Plan is explicitly aborted, not silently degraded.
- Abort reason is stated clearly with three concrete resolution items.
- Does not proceed to partial steps that would leave the system in an inconsistent state.
