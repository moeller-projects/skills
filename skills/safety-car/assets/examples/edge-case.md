# Edge-Case Example — Safety Car: Observability Blind Spots

## Input

Users report "the app is down" on social media. Status dashboard shows green. The team has no access to production logs tonight (access rotation in progress), no synthetics cover the mobile API path.

## Process

1. Declared SEV1 — user-visible outage reports at scale, internal monitoring blind; higher severity chosen because impact could not be bounded.
2. Stated the blind spot explicitly: no logs, no dashboard coverage for the reported path.
3. Fell back to user reports and ad-hoc synthetic checks (`curl` against the mobile API from an external network).
4. Mitigation chosen for reversibility: rolled back this morning's CDN config change, the only externally visible change in 24h.
5. Impact resolved; root cause confirmed later once log access returned.

## Output

```text
status: resolved
severity: SEV1

impact:
- Mobile API unreachable (TLS handshake failure) for all users on the EU CDN edge, ~19:02Z–19:47Z
- Web app unaffected; exact affected population unknown due to monitoring gap

timeline:
- 19:02Z user-reports — multiple reports of app failure (monitoring green — blind spot noted)
- 19:06Z on-call — declared SEV1; impact unbounded due to observability gap
- 19:09Z on-call (est.) — external synthetic check confirmed TLS failure on EU edge
- 19:15Z on-call — identified CDN config change at 08:40Z as only externally visible change
- 19:20Z on-call — rolled back CDN config change
- 19:35Z on-call — synthetic checks passing from three external networks
- 19:47Z on-call — declared resolved; user reports stopped

mitigation:
1. Rolled back the morning CDN config change (reversible, config-only)

root-cause:
- trigger: CDN config change deployed an incomplete certificate chain to EU edges
- root cause: CDN deploy validation only checks the US edge; EU edge validation missing
- contributing: log access rotation left the team blind for the first 20 minutes

follow-ups:
- Add EU edge validation to CDN deploy checks — owner: platform team
- Add external synthetics for the mobile API path — owner: platform team (handed to pit-crew)
- Rework access rotation so on-call never loses read access — owner: security team

comms:
- Status page: "Mobile app connectivity issues 19:02–19:47Z caused by a configuration error, now resolved."
- Note: comms posted after explicit approval; no cause speculation included pre-confirmation
```
