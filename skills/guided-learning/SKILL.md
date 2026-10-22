---
name: guided-learning
description: User-invoked only: Teach a topic across sessions with a stateful workspace of lessons, references, practice, and learning records.
license: MIT
compatibility: chatgpt, codex, claude-code, cursor, opencode
metadata:
  title: Guided Learning
  version: "1.0.3"
  summary: Teach a topic across sessions with a stateful workspace of lessons, references, practice, and learning records.
  invocation: user
---

# Guided Learning

## Purpose

Teach for retention, not fluency. Deep learning needs three things: **knowledge** from high-trust sources, **skills** built through interactive practice with tight feedback, and **wisdom** from real-world use in a community. This skill runs a stateful teaching workspace that delivers the first two and points at the third.

## The Workspace

State lives in the directory the skill was started in:

- `MISSION.md` — why the user is learning this; grounds every lesson. If it is missing or vague, interviewing for the mission is the first job — ungrounded lessons feel abstract and unmotivated.
- `lessons/NNNN-<dash-case>.html` — the primary unit: one self-contained, short, printable HTML lesson per tightly-scoped outcome.
- `reference/*.html` — compressed cheat-sheets (syntax, algorithms, glossaries) built for quick lookup; lessons are rarely revisited, references are.
- `learning-records/NNNN-<dash-case>.md` — what the user has learned; the input for judging their zone of proximal development.
- `RESOURCES.md` — trusted primary sources found so far. Never trust parametric knowledge for lesson content; gather sources first.
- `assets/` — reusable components shared across lessons (stylesheet first, then quiz widgets and simulators). Reuse is the default: before authoring, read what exists; new reusable pieces become components, never one-off inline code.
- `NOTES.md` — teaching preferences the user has expressed.

## Workflow

1. Establish or revisit the mission; confirm before changing it, and log the change as a learning record.
2. Judge the zone of proximal development from `learning-records/` — the next lesson should challenge just enough. If the user names exactly what they want next, teach that.
3. Gather knowledge from trusted sources (update `RESOURCES.md`); cite them in the lesson.
4. Build the lesson: short enough to complete in minutes, one tangible win, tied to the mission. For knowledge, minimize difficulty — it eats working memory needed for understanding. For skills, difficulty is the tool — design **effortful retrieval** (recall from memory), spacing across sessions, and interleaving of related topics, with the tightest possible feedback loop (immediate, ideally automatic, feedback on every attempt).
5. After each lesson, record separate facts: `delivered` (what the lesson presented), `practice_attempted` (what the learner tried), `feedback` (what was corrected), and `demonstrated` (observable evidence the learner can perform or explain the outcome). Never mark an outcome demonstrated merely because a lesson was authored or delivered; advance difficulty only from demonstrated evidence.
6. Every lesson links related lessons and references, recommends one primary source, and reminds the user to ask follow-up questions.
7. For quiz questions: answer options of equal length and format, correct position varied — no formatting tells.

## Fluency vs Storage

In-the-moment fluency feels like mastery and is not the goal; long-term storage is. When a lesson went smoothly, prefer a retrieval check over another explanation.

## Wisdom

When a question needs real-world judgment, answer what you can, then point at a community (forum, subreddit, local group) where the skill gets tested for real — unless the user declines.

## Output Contract

```text
lesson:
  path: <lessons/NNNN-title.html>
  teaches: <the single outcome>
  mission_link: <why this lesson serves the mission>
practice: <the interactive element and its feedback loop>
learning_record:
  path: <path written>
  delivered: <what lesson presented>
  practice_attempted: <what learner tried>
  feedback: <corrections or "none">
  demonstrated: <observable evidence or "not yet demonstrated">
sources:
- <primary source cited>
next: <suggested next lesson and why it fits the zone of proximal development>
```

## Handoffs

- Hand off project documentation requests to `technical-writing`.
- Hand off fact-gathering the lesson depends on to `research`.

## Error Handling

1. If the mission is unclear, interview before building any lesson.
2. If no trusted sources exist for a claim, mark it as unverified in the lesson rather than asserting it.

## Validation Checklist

- [ ] The lesson serves the stated mission and fits the learner's zone.
- [ ] One tangible win, completable in minutes, printable and self-contained.
- [ ] Skills practice uses retrieval, spacing, and immediate feedback.
- [ ] Claims are cited to sources from `RESOURCES.md`.
- [ ] A learning record was written and shared components reused.
