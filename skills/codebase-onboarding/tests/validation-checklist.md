# Codebase Onboarding — Validation Checklist

Run this checklist before accepting a repo map as complete.

## Trigger Check

- [ ] Task involves onboarding, architecture mapping, or convention extraction.
- [ ] Task is NOT a targeted patch where exact files are already provided.

## Canonical Section Check

- [ ] Output uses exactly repo_map, entrypoints, conventions, hotspots, and agent_artifacts sections.
- [ ] Every section contains substantive entries or exactly `- none`; no section is omitted or empty.
- [ ] Each entry's description is validated within its own section, not by global counts.

## Repo Map Check

- [ ] Every major domain or package is listed with a one-line responsibility.
- [ ] Inaccessible directories are listed with "INACCESSIBLE" and a reason.

## Entrypoints Check

- [ ] Each entrypoint is a real file or command (not an assumption).
- [ ] Each entrypoint describes what it starts or exposes.

## Conventions Check

- [ ] Each convention is observed from actual files, not assumed.
- [ ] Conventions that could not be verified are marked as unverified.

## Hotspots Check

- [ ] Each hotspot has a concrete reason (churn, cross-cutting, critical path).
- [ ] Hotspots based on shallow clone history are marked as estimates.

## Agent Artifacts Check

- [ ] Artifacts are immediately usable without further clarification.
- [ ] Partial maps include a gap summary and instructions for completing the scan.

## Error Format

```text
error: <what went wrong during scan>
gap: <directory or file that could not be accessed>
recovery: <action taken — e.g., flagged gap and continued with available areas>
```
