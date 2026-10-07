# Safety Car — Output Template

```text
status: investigating | mitigated | monitoring | resolved
severity: SEV1 | SEV2 | SEV3

impact:
- <who is affected, how, since when>

timeline:
- HH:MMZ <actor> — <action/observation>

mitigation:
1. <what was done to stop the impact>

root-cause:
- trigger: <what started it>
- root cause: <why it broke>
- contributing: <why it got big>

follow-ups:
- <action> — owner: <team/person>

comms:
- <what was communicated, where>
```

Rules:

- `status` and `severity` come first, always.
- Timeline entries are UTC; reconstructed entries are marked `(est.)`.
- `root-cause:` may say `unknown` — never invent one.
- Every follow-up has an owner.
- During live response, re-emit the contract after each status change.
