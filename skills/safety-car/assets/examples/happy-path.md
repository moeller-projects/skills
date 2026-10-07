# Happy-Path Example — Safety Car: SEV2 API Outage

## Input

Pager alert: checkout-api 5xx rate jumped from 0.1% to 18% at 14:07Z. Deploy 1f42c went out at 14:05Z. No other changes in the window.

## Process

1. Declared SEV2 — checkout degraded for a significant subset, no data loss observed.
2. Mitigated before diagnosing: rolled back 1f42c at 14:16Z, the only change in the window.
3. Timeline captured live; each mitigation attempt and its effect recorded.
4. Diagnosis after stabilization: deploy 1f42c required a config key present in staging, absent in production.
5. Resolved after 9 stable minutes; follow-ups with owners; comms posted to the status page.

## Output

```text
status: resolved
severity: SEV2

impact:
- Checkout API returned 500s for ~18% of requests between 14:07Z and 14:31Z
- No data loss; failed payments were not captured

timeline:
- 14:07Z alerts — elevated 5xx on checkout-api
- 14:10Z on-call — declared SEV2, incident lead: on-call
- 14:13Z on-call — identified deploy 1f42c as only change in window (suspected trigger)
- 14:16Z on-call — rolled back deploy 1f42c
- 14:22Z monitoring — error rate returned to baseline
- 14:31Z on-call — declared resolved after 9 stable minutes

mitigation:
1. Rolled back deploy 1f42c via the standard pipeline (reversible, no data migration involved)

root-cause:
- trigger: deploy 1f42c introduced a required config key that staging had but production lacked
- root cause: deploy pipeline does not validate required config keys against the target environment
- contributing: staging/prod config drift accumulated over three months

follow-ups:
- Add config-key validation to the deploy pipeline — owner: platform team
- Audit staging/prod config drift — owner: platform team
- Permanent fix for the 1f42c feature behind a flag — owner: checkout team (handed to mechanic)

comms:
- Status page: "Elevated checkout errors 14:07–14:31Z, resolved by rollback. No payment data lost."
```
