# Edge-Case Example — Codebase Onboarding: Restricted Access

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
- src/api/server.ts — Express app entry (runtime; confirmed from available files)
- src/infra/ — UNKNOWN; directory inaccessible and requires access before use

conventions:
- ESLint — .eslintrc.js at root uses airbnb-base config
- Imports — barrel files (index.ts) in each subdirectory
- Access gap — conventions in src/infra are not verified due to restriction

hotspots:
- src/shared/errors.ts — referenced by 14 files; changes have wide blast radius
- src/api/routes/ — high churn based on limited shallow-clone history

agent_artifacts:
- PARTIAL MAP — fill src/infra gaps before infrastructure changes
- Re-run scan — obtain full repository access to complete the map
- History caveat — shallow clone limits confidence in churn estimates
```

## Why This Is Correct

- Inaccessible paths are flagged, not skipped silently.
- Partial information is labeled as such.
- Agent artifacts include the partial-map warning.
- Downstream consumer has clear instructions before acting on incomplete data.
