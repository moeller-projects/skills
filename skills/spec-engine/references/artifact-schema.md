# Artifact Schema

<!--
risk_tier values:
  Low      — cosmetic or internal-only clarification
  Medium   — additive feature or requirement change
  High     — cross-module behavior change
  Critical — public behavior, API, or security posture change
-->

```json
{
  "output_format": "freeform | openspec",
  "spec": {
    "goal": "string",
    "scope": ["string"],
    "requirements": [
      { "id": "string", "statement": "string" }
    ],
    "acceptance_criteria": [
      { "requirement_id": "string", "criteria": ["string"] }
    ]
  },
  "risk_tier": "Low | Medium | High | Critical",
  "quality_gates": ["string"],
  "open_questions": ["string"]
}
```

When `output_format=openspec`, also include:

```json
{
  "output_format": "openspec",
  "openspec_proposal": {
    "path": "proposals/",
    "change_path": "openspec/changes/<change-name>/",
    "metadata_file": ".openspec.yaml",
    "proposal_file": "proposal.md",
    "delta_spec_files": ["specs/<capability>/spec.md"]
  }
}
```
