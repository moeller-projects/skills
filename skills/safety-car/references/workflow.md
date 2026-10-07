# Safety Car — Detailed Workflow

## 1. Declare

- State severity (SEV1 / SEV2 / SEV3), current impact, and affected population.
- When severity is uncertain, declare the higher tier. Downgrading is cheap; under-declaring is not.
- Establish one incident channel and one incident lead. State both in the first status emission.

## 2. Mitigate

- List available mitigations in order of reversibility: feature flag, config rollback, deploy rollback, failover, rate limit, drain.
- Apply the cheapest reversible mitigation that plausibly stops the impact.
- Change one variable at a time. Record each attempt and its observed effect on the timeline.
- If no safe mitigation exists, escalate and say so — do not experiment in production.

## 3. Capture the timeline

- Format: `HH:MMZ actor — action/observation`.
- Log declarations, mitigations, observations, comms, and status changes.
- Mark reconstructed entries as estimates: `HH:MMZ (est.)`.

## 4. Communicate

- Cadence: every 15–30 minutes for SEV1, hourly for SEV2, once per phase for SEV3.
- Content: impact, current action, next update time. Nothing else.
- Suspected causes are labeled suspected. Blame is never communicated.

## 5. Diagnose

- Only after mitigation is verified stable.
- Separate three things: the trigger (what started it), the root cause (why it broke), contributing factors (why it got big).
- Evidence beats narrative: cite the log line, metric, or commit.

## 6. Resolve and hand off

- Resolution requires verified stable monitoring, not just an applied fix.
- Convert root cause and contributing factors into follow-ups with owners.
- Hand permanent fixes to pit-crew (infrastructure) or mechanic (code); hand the durable postmortem document to press-officer when a wider audience needs it.
- If root cause is unknown, close as `monitoring` with investigation follow-ups. Never fabricate a cause.
