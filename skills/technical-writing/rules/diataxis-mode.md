# Rule: Diátaxis Mode

> Impact: high

## Description

Every section of a document serves one of four reader needs: to learn (tutorial), to perform a known task (how-to), to look up a fact (reference), or to understand why something is the way it is (explanation). Decide which mode each section is in before writing, and keep the section in one mode. Mixing modes within a single section is the most common reason documentation feels confusing.

## The Four Modes

- **Tutorial** — learning-oriented. A lesson for a newcomer. Encouraging, second-person, takes responsibility for the reader's success. ("Now you'll see the response appear in the terminal.")
- **How-to** — task-oriented. A recipe for someone who knows what they want. Imperative, assumes competence, focused on a single goal. ("To rotate the key, run …")
- **Reference** — information-oriented. A dictionary entry. Austere, neutral, exhaustive within its scope. No narrative. ("`--timeout` (integer, seconds, default 30) — abort the request after N seconds.")
- **Explanation** — understanding-oriented. A discussion of *why*. Discursive, may carry opinion, makes connections. ("We chose JWTs over sessions because …")

The two axes underneath: tutorial and how-to are *practical* (action); reference and explanation are *theoretical* (cognition). Tutorial and explanation serve *acquisition* (study); how-to and reference serve *application* (work). Use the axes to reason about borderline sections.

## Apply When

- Planning the structure of any new document.
- Reviewing an existing document that feels confusing or hard to scan.
- Tagging sections in the `structure:` field of the output contract.

## When Not to Apply

- The artifact is intentionally multi-mode (README, AGENTS.md, landing pages). Tag each section with its mode, but do not split the artifact.
- The document is shorter than a single section — too small for mode to matter.

## Output Format

The four allowed tag tokens (lowercase, exactly as shown): `tutorial`, `how-to`, `reference`, `explanation`.

Annotate each section in `structure:` with its mode in square brackets:

```text
structure:
  1. Running locally [tutorial] — install, configure, start
  2. Common workflows [how-to] — login, refresh, logout flows
  3. Configuration reference [reference] — env vars, defaults
  4. Why JWT [explanation] — why not sessions
```

## Checks

- Every section in `structure:` is tagged with exactly one mode.
- No section is tagged with two modes — if it needs two, split it.
- Section voice matches mode: tutorials are second-person and encouraging, how-tos are imperative, reference is neutral and factual, explanation is discursive.
- The artifact's overall mode mix is intentional. A README with one explanation paragraph dropped mid-tutorial is a smell.

## Anti-Pattern

A tutorial that breaks off mid-lesson to explain deep design reasoning — the reader is trying to learn by doing, and the explanation interrupts the lesson. A reference page that opens "In this guide we will explore…" — reference is not a guide; strip the narrative and present the facts. A how-to that ends with a tutorial-style summary of what the reader just accomplished — how-tos serve people who already knew what they wanted, and the summary is patronizing.
