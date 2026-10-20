# STE Rule Reference — Categories, Details, and Sources

Read this when you need more than the summary in SKILL.md: the full rule
categories of ASD-STE100 Issue 9 (January 2025), the strict-level details
(tenses, -ing forms, safety text), or citations. This file paraphrases rule
categories. It does not reproduce the standard's text or its dictionary.

Contents:
- What the standard is
- Structure of the standard
- Rule categories in detail
- Tenses and verb forms
- Safety text
- The dictionary gap, and what to do about it
- Sources

## What the standard is

ASD-STE100 is a controlled natural language, first released in 1986 by what is
now ASD (the AeroSpace and Defense Industries Association of Europe). European
airlines — mostly staffed by non-native English speakers — asked for
maintenance documentation that could not be misread, because a misread
instruction on an aircraft can kill people. The standard is maintained by the
Simplified Technical English Maintenance Group (STEMG), has been free to
download since Issue 6 (2013), and is now at Issue 9 (January 2025).

The reader it was built for — no back-channel, no author to call, a real cost
to misreading — matches the position of an AI agent parsing another agent's
output, a translation pipeline, or a non-native reader. That is why the same
rules transfer.

## Structure of the standard

- 53 writing rules across 9 sections: word choice, noun phrases, verbs,
  sentences, procedures, descriptions, warnings/cautions/notes, punctuation,
  and style.
- A dictionary of roughly 900 approved words, each restricted to one meaning
  and one part of speech, plus roughly 1,200 non-approved words with approved
  replacements.
- A terminology allowance: a project may define its own approved technical
  nouns and verbs beyond the base dictionary.

## Rule categories in detail

**Word choice**
- Use approved words only in their approved meaning and part of speech.
- One word maps to one meaning; do not rely on context to disambiguate.
- Prefer the plainer, shorter, more common word over a formal or rare synonym.
- Use a verb for an action, not a noun derived from that verb (Rule 3.7):
  "analyze", not "perform an analysis of".
- No phrasal verbs (Rule 9.3): a verb plus preposition has a meaning the parts
  do not predict ("take off" can mean remove, depart, or deduct).

**Noun phrases**
- Noun clusters are capped at 3 words: "fuel pump valve" is acceptable, "high
  pressure fuel pump inlet valve assembly" is not. Rewrite with a preposition
  or relative clause: "the valve assembly at the inlet of the fuel pump".
- Do not omit articles or "that" to save space. Ellipsis creates ambiguity,
  not brevity: "Files not backed up will be lost" leaves the reader guessing
  which files.

**Voice**
- Procedures and instructions: active voice, always.
- Descriptions: passive is permitted only when the actor is genuinely unknown
  or irrelevant to the reader.

**Sentence structure**
- One instruction per sentence in procedures; one idea per sentence elsewhere.
- Procedures: maximum ~20 words. Descriptions: maximum ~25 words.
- Semicolons are banned outright (Rule 8.1): "You can use all standard English
  punctuation marks but not the semicolon." Write separate sentences. The em
  dash is not banned, but it often marks a sentence that should be split.
- Use vertical lists for sequences, conditions, or 3+ items.

**Paragraphs**
- One topic per paragraph. Maximum ~6 sentences. Main point first.

## Tenses and verb forms

Permitted: infinitive, imperative, simple present, simple past, simple future
("will"), and past participle used only as an adjective ("the damaged valve").

Excluded: present perfect, past perfect, continuous forms. "We received the
report", not "we have received the report". "-ing" forms are allowed only as
(or inside) a technical noun ("the welding torch"), not as a verb form.

Practical exception this skill keeps: where a compound form carries
information the simple form cannot — current relevance ("the job has
finished", so the output is ready now) or a hedge ("may have failed") — keep
it. Removing the auxiliary would delete the uncertainty along with the tense,
and confidence is content.

## Safety text

Strict level formats safety text as the standard does:

- **WARNING** — risk of injury; for software, extend to data loss, security
  risk, or outage.
- **CAUTION** — risk of damage to equipment or data.
- Order: the signal word, then the command, then the risk. Never bury the
  command mid-sentence.

Example: "WARNING: Disconnect the power supply before you open the panel. The
capacitors hold a charge."

Strict level also bans contractions and Latin abbreviations ("e.g.", "i.e.",
"etc."). Standard level permits them.

## The dictionary gap, and what to do about it

The standard is free to obtain but not free to redistribute: Issue 9 permits
reproduction only with ASD's written authority or by listed categories of
organization. That is why no approved-word list is bundled here, and why the
lexical rules are a direction of travel rather than a checkable standard.

Consequences:
- Apply the principle: plainest common word, one meaning, used consistently.
- Within one document, consistency is checkable. The linter flags rotation
  between a small set of close substitutes; it cannot detect every synonym.
- Never claim "STE-compliant" for output. Say "STE-inspired" or "STE-style".
- When exact compliance matters (real maintenance documentation), request the
  standard from the official downloads page and check word by word. Note the
  download is a request form that emails a link, not a direct download.

## Sources

- [ASD-STE100 official site](https://www.asd-ste100.org/)
- [ASD-STE100 — About STE](https://www.asd-ste100.org/about_STE.html)
- [ASD Europe — Simplified Technical English](https://www.asd-europe.org/standards-specifications/simplified-technical-english/)
- [Simplified Technical English — Wikipedia](https://en.wikipedia.org/wiki/Simplified_Technical_English)
- [TechScribe — ASD-STE100 Simplified Technical English](https://www.techscribe.co.uk/techw/asd-simplified-technical-english.htm)
- [SKYbrary — Simplified Technical English (STE)](https://skybrary.aero/articles/simplified-technical-english-ste)
