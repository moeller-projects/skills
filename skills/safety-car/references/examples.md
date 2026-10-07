# Safety Car — Sample Incident Artifacts

## Example 1: SEV2, mitigated by rollback

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
- Permanent fix for 1f42c feature behind flag — owner: checkout team (handed to mechanic)

comms:
- Status page: "Elevated checkout errors 14:07–14:31Z, resolved by rollback. No payment data lost."
```

## Example 2: Unknown root cause, closed as monitoring

```text
status: monitoring
severity: SEV3

impact:
- Elevated dashboard latency (p95 4s vs 800ms) for EU users, 09:12Z–09:40Z

timeline:
- 09:12Z alerts — dashboard p95 above threshold, EU only
- 09:18Z on-call — declared SEV3; no deploys in window
- 09:25Z on-call — enabled query-result cache for EU dashboard (mitigation)
- 09:33Z monitoring — latency recovering
- 09:40Z monitoring — latency at baseline

mitigation:
1. Enabled the existing query-result cache flag for the EU dashboard

root-cause:
- unknown — no deploy, no traffic anomaly, no database saturation in the window

follow-ups:
- Investigate cache-miss storm hypothesis with 48h of query logs — owner: data team
- Add cache-hit-rate alerting — owner: platform team
- Re-review in one week; close if no recurrence — owner: on-call

comms:
- Internal only; no external impact beyond latency
```
