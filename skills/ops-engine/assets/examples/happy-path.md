# Happy-Path Example — Ops Engine

## Scenario

Team asks: "Add a liveness probe to the `api` Kubernetes deployment."

## Input Context

- Deployment: `api` in namespace `production`.
- App exposes `GET /healthz` returning 200 when ready.
- Current deployment has no probes configured.

## Expected Output

```text
risk:
- Probe misconfiguration restarts healthy pods — medium / high
- Too-short initialDelaySeconds causes restart loop on slow startup — medium / medium

plan:
1. Add livenessProbe to api deployment manifest — engineer
2. Set initialDelaySeconds=30, periodSeconds=10, failureThreshold=3 — engineer
3. Apply to staging first: kubectl apply -f deploy/api.yaml -n staging — engineer
4. Verify pod stays Running for 5 minutes: kubectl get pods -n staging -w — engineer
5. Apply to production with same manifest — engineer (human approval required)

checks:
- [ ] kubectl describe pod <api-pod> -n staging shows livenessProbe configured
- [ ] No CrashLoopBackOff events in kubectl get events -n staging for 5 min
- [ ] GET /healthz returns 200 from inside the pod: kubectl exec <pod> -- curl -s localhost:8080/healthz

rollback:
- Remove livenessProbe block and reapply manifest: kubectl apply -f deploy/api.yaml
- artifact: save current manifest before change: kubectl get deploy api -n production -o yaml > api-backup.yaml

security:
- Probe endpoint /healthz must not expose internal state or secrets
- Restrict /healthz to cluster-internal traffic if not already done
```

## Why This Is Correct

- Risks stated before the plan.
- Staging-first approach reduces production blast radius.
- Human approval explicitly required before production step.
- Rollback includes the preservation artifact.
- Security note addresses the probe endpoint exposure.
