# Ops Engine — Output Template

## Default (risk + plan + checks + rollback + security)

```text
risk:
- <risk description> — <likelihood: low|medium|high> / <impact: low|medium|high|critical>

plan:
1. <step> — <responsible party or tool>
2. <step> — <responsible party or tool>

checks:
- [ ] <pre-condition or post-condition to verify>

rollback:
- <step to undo the change if it fails>
- artifact: <what to preserve before executing>

security:
- <security concern or mitigation>
```

## Minimal (single-step change, same sections)

```text
risk:
- <risk description> — <likelihood> / <impact>

plan:
1. <single change step> — <responsible party or tool>

checks:
- [ ] <one verification step>

rollback:
- <one rollback step>
- artifact: <what to preserve first>

security:
- <security concern or explicit "none identified">
```

## Rules

- List risks before the plan; do not bury them at the end.
- Every destructive or irreversible step must have a rollback entry.
- Stop and request human approval before any production deployment, destructive operation, or irreversible rollback.
- Every check must be a concrete, executable command or observable state.
