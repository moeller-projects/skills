# Edge-Case Example — Repo Engine: Restricted Access

## Scenario

Agent scans a repo but several directories are inaccessible (permissions error) or not available in the shallow clone.

## Why This Is an Edge Case

Partial access means the map is incomplete. The skill must not fabricate the missing areas,
and must flag each gap so downstream consumers know the map is partial.

## Expected Output

```text
repo_map:
- src/api: HTTP layer — partially scanned (see gaps below)
- src/shared: shared utilities — fully scanned
- src/infra: INACCESSIBLE — permission denied

entrypoints:
- src/api/server.ts: Express app entry (confirmed from available files)
- src/infra/: UNKNOWN — directory inaccessible

conventions:
- ESLint: .eslintrc.js present at root with airbnb-base config
- Imports: barrel files (index.ts) in each subdirectory
- NOTE: conventions in src/infra not verified due to access restriction

hotspots:
- src/shared/errors.ts: referenced by 14 files; change here has wide blast radius
- src/api/routes/: high churn based on git log (shallow clone; history limited)

agent_artifacts:
- PARTIAL MAP: gaps in src/infra must be filled before making infrastructure changes
- Re-run scan with full repo access to complete the map

GAPS:
- src/infra/: inaccessible — do not make infrastructure changes without full scan
- git history truncated (shallow clone) — hotspot churn counts are estimates only
```

## Why This Is Correct

- Inaccessible paths are flagged, not skipped silently.
- Partial information is labeled as such.
- Agent artifacts include the partial-map warning.
- Downstream consumer has clear instructions before acting on incomplete data.
