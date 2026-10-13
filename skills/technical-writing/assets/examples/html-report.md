# HTML Report Example

## Scenario

Create a weekly engineering update.

## Expected Output

```text
doc:
- purpose: Help stakeholders review progress and risks.
- audience: product leadership unfamiliar with repository implementation details.
- structure:
  1. Executive summary [explanation] — concise status for stakeholders
  2. Completed work [reference] — delivered items and evidence
  3. Risks and blockers [reference] — current issues and mitigation
  4. Next actions [how-to] — follow-up steps and ownership
- format:
  - type: html
  - reason: read-only stakeholder communication artifact
- artifact:
  - weekly-engineering-update.html

changes:
- weekly-engineering-update.html — add standalone stakeholder report

gaps:
- None
```
