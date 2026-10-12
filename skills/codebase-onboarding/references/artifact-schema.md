# Artifact Schema

```json
{
  "repo_map": [
    { "area": "string", "role": "string" }
  ],
  "entrypoints": [
    { "path": "string", "kind": "runtime|build|test|ci", "why_it_matters": "string" }
  ],
  "conventions": ["string"],
  "hotspots": [
    { "area": "string", "risk": "string", "reason": "string" }
  ],
  "agent_artifacts": ["string"]
}
```
