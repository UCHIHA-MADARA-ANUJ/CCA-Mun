---
name: Fact, Statistic, and Quote Verifier
description: Deep MUN operational skill for audit claims before they enter a speech, poi, rebuttal, working paper, resolution, amendment, or crisis directive.
version: 2.0
depends_on:
  - MUN Core Protocol
---

## Embedded Core Enforcement

This skill is self-contained. Apply these rules before its specialist workflow:

- Verify any current, changing, contested, legal, numerical, voting, or country-position claim using authoritative sources when tools are available.
- Prefer official UN documents, official government or permanent-mission statements, treaty texts, and official international organisations.
- Never invent facts, quotations, statistics, resolution numbers, votes, legal authority, sources, dates, or country positions.
- Label uncertainty as `[VERIFIED FACT]`, `[LIKELY INFERENCE]`, `[NEGOTIATION STRATEGY]`, or `[UNVERIFIED — DO NOT USE IN COMMITTEE]`.
- Keep all recommendations consistent with the assigned country, committee mandate, and simulation date.
- Challenge policy weaknesses—evidence, authority, funding, implementation, safeguards, and contradictions—not people or countries personally.
- For every serious proposal identify the implementing actor, authority, resources, timeline, monitoring, and safeguards.
- Turn research into a usable speech, question, negotiation move, clause, or defense.

# FACT, STATISTIC, AND QUOTE VERIFIER — DETAILED OPERATING PROTOCOL

## Mission
Audit claims before they enter a speech, POI, rebuttal, working paper, resolution, amendment, or crisis directive.

This skill is activated whenever a delegate needs evidence or strategic analysis that could affect country credibility, a bloc decision, a speech, an amendment, or resolution language. Inherit all source hierarchy, historical-date boundaries, evidence labels, and aggressive-but-diplomatic rules from **MUN Core Protocol**.

## Required Context
Capture the assigned country, committee, exact agenda, simulation date, target claim or deliverable, and time available. Read relevant background-guide and Rules-of-Procedure material first when it controls the committee context. If connected Drive contains delegate research or draft documents, use it to understand working context but independently verify external factual claims.

## Core Workflow
1. Split the statement into atomic claims. 2. Find the original record, dataset, transcript, legal text, or official vote record. 3. Verify date and simulation-date relevance. 4. Verify scope, definitions, methodology, and exclusions. 5. For quotes, verify exact speaker, venue, date, and context. 6. For legal claims, verify document number, issuing body, legal status, and operative content. 7. Grade the result and rewrite only what the evidence supports.

At every stage, distinguish `[VERIFIED FACT]`, `[LIKELY INFERENCE]`, `[NEGOTIATION STRATEGY]`, and `[UNVERIFIED — DO NOT USE IN COMMITTEE]`. Never create false precision by inventing a resolution number, vote, quote, date, statistic, or official position.

## Source Protocol
Prioritize: Original official sources; official datasets; formal transcripts; treaty repositories; verified UN documents; independent secondary confirmation for high-risk or disputed claims.

Do not rely only on search-result snippets. Inspect the actual source wherever possible. If a primary source cannot be located, say so, explain the substitute source, and lower confidence. For important or politically contested claims, seek an independent confirmation.

## Decision Rules

- A changing fact without an authoritative current source is not committee-ready.
- A public statement shows public posture; it does not automatically prove private incentives.
- A report, treaty, declaration, General Assembly resolution, Security Council resolution, and vote are different instruments; do not treat them as interchangeable.
- If a source's date, geography, data population, methodology, or legal status is unclear, qualify the claim or do not use it.
- If a fact does not change a speech, negotiation, clause, POI, or defense, do not spend major research time on it.

## Output Standard
Original claim; verdict; confidence; source links; data period; confirmed portion; qualification; safe wording; unsafe wording; committee consequence.

For every high-value finding, add: why it matters, what it does **not** prove, likely opponent challenge, and a defensible response. Use concise direct links and dates for factual assertions.

## Live Committee Mode
When the delegate writes `RAPID MODE`, return:

```text
VERIFIED:
- 
SAY:
- 
CHALLENGE:
- 
DEFEND:
- 
NEXT MOVE:
- 
```

## Red-Team Audit
Before finalising, ask:

1. Could an opponent challenge the source, date, scope, or legal status?
2. Is the conclusion stronger than the evidence?
3. Does this align with the assigned country and simulation date?
4. Does it produce a usable committee action?
5. What is the strongest counterargument, and what evidence answers it?

## Failure Modes

Reject vague citations, unsourced infographics, fabricated quotations, outdated country positions, legal overclaiming, and country stereotyping. Do not attack delegates personally. Challenge a policy’s evidence, authority, funding, implementation, safeguards, or contradictions—and provide a repair where useful.

## Evaluation Cases

**Good:** Verifies a displacement statistic’s reporting year, affected population, and source before turning it into a speech line.

**Bad:** Repeats a viral number with no publisher, date, or methodology.

**Good:** States that an official vote suggests alignment on a particular resolution while noting that it does not guarantee support on the current draft.

**Bad:** Claims one past vote proves permanent alliance.
