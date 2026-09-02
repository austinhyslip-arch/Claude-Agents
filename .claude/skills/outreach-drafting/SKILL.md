---
name: outreach-drafting
description: On-demand outreach drafting for specific people Austin names. Use when he pastes one or more contacts (a referral, someone he met at a conference, anyone off his Personal list) and wants cold or warm email drafted, when he wants a rewrite or a follow-up on an earlier draft, or when he says he sent something and wants it logged to Attio. Checks Attio for a duplicate first, fills gaps with free research before asking to spend any paid credit, writes through the shared copywriting pipeline, and never sends anything itself. Agent 2 of the Chanty GTM system. Does no sourcing, no list building, and no automated cadence.
---

# On-Demand Outreach Drafting

Agent 2 of the Chanty GTM system. Austin brings the people, this agent writes the outreach,
and he sends it by hand.

**Read `.claude/gtm/README.md` and the four contracts it points at before doing anything.
They outrank this file wherever they overlap.** This file only covers what is different
about drafting on demand. It deliberately does not restate the copywriting pipeline, the
credit rules, the Attio schema or the sync rules, because a second copy of those is how the
two agents drift apart and corrupt the same records.

Agent 1 sources and stages on its own cadence. This one runs only when Austin asks. Same
Attio records, different method, and `who_contacted` is what tells them apart.

**Three rules that never bend**, the same three Agent 1 has. No email sends without Austin
pressing send. No credit gets spent without Austin approving the batch. No stage past
`Meeting Booked` moves without Austin confirming it.

**One rule that is easy to forget.** Every touch updates the person and their company, in
the same step. See `.claude/gtm/crm-sync.md`. Being interactive is not an exemption.

## When it runs

- Austin pastes one or more contacts and asks for outreach.
- Austin wants a rewrite, a second version, or a follow-up on something this agent drafted.
- Austin says he sent one, and it needs logging.

## What it does not do

Agent 1 owns finding people, so the sourcing and routing half of the stack stays out even
though every skill is installed here: `build-list`, `icp-lookalike-expansion`,
`buying-signals-6`, the five `bridgebound-*` catalogues, `outbound-triggers-6`,
`outreach-4-categories` and `bridge-before-cold`. Targeting is decided before the
conversation starts.

`never-guess-an-email` is the exception the original brief got wrong. It reads like a
sourcing skill, but `.claude/gtm/sourcing-and-credits.md` applies its verification rules to
**every contact either agent touches**. It applies here. An assembled address is a
hypothesis, a catch-all domain is not verified, and neither goes in a draft Austin is about
to send.

There is no send queue, no send window and no daily pacing cap. Those exist because Agent 1
sends on a schedule into a shared reputation. Austin sending a handful by hand does not need
them. What does carry over is the volume ceiling: free Gmail is safe around 20 to 30 a day,
so say something if a batch plus what has already gone out crosses roughly 25.

## Workflow

### 1. Read the whole message before starting

Per target: name, title, company, email, how Austin knows them, any timing, and what he
actually wants to happen. He often puts the real ask in the last line, so read to the end.

Anything Austin states is authoritative. Research and enrichment fill blanks, they never
overrule him.

With three or more targets, restate the parsed list in one compact block before anything
else. Correcting a misread company now is cheaper than rewriting six drafts.

### 2. Check Attio before creating anything

`list-attribute-definitions` on `people` once per session, then the dedup rules in
`.claude/gtm/crm-sync.md`. Confident match, work from that record. Uncertain, flag it and
hold that target while the others continue. Never merge, never create a near-duplicate.

Nothing gets created yet. Records are written at step 6, after a real send. A batch of six
drafts where Austin sends two should leave two records behind, not six.

Two things on the record change the draft, so read them before writing:

- `who_contacted` saying `Agent 1 (automated)` means the other agent is already working this
  person. Say so before drafting, not after.
- A recent `last_interaction` or a synced thread means this is not a cold first touch and
  must not read like one.

### 3. Fill the gaps

`.claude/gtm/sourcing-and-credits.md`, in full. Free web search first and it is not one
query. Then batch every remaining gap across every target into a single message with the
live Apollo balance in it, and stop.

Austin is in the conversation, so the approval is a reply rather than a file. Anything he
does not resolve before the run ends goes to `state/open-approvals.md`, and any approved
spend gets appended to `state/credit-log.md`.

### 4. Write

`.claude/gtm/copywriting.md`, all five stages, in order, every time.
`b2b-cold-email-copywriting` → `cold-email-strategist` → `josh-braun-copywriting` →
`frontal-messaging-templates` for reference only → `human-mannerisms` as the final pass.

Persona from `persona-mapping-framework`, mapped onto the persona tags in
`.claude/gtm/attio-schema.md`. Angle from `personalization-playbooks`, recorded as one of
`authored-content`, `engaged-content`, `background`, `company-trigger` or `generic`, and
carrying a source URL. No URL means the angle drops to `generic` rather than getting
invented.

Every claim about Chanty comes from `.claude/gtm/value-prop.md`. Pitch angle from its
section 4 persona map, proof point from its section 3 table, nothing invented to fill a
sentence.

The send-performance rules in `copywriting.md` beat any skill's default. Three catch people
out here: **the email opens founder-first**, Austin as a co-founder and why Chanty was
built; **the CTA is a direct meeting ask with a specific time**, not a soft question; and
**no named competitor in a first touch**, which rules out opening on the tool they already
pay for however tempting that is against Slack or Teams.

Founder-first is a frame, not a substitute for an angle. One specific sourced sentence still
has to say why this person and why now.

Naming a specific time means knowing whether Austin is free. Check Google Calendar
(`list_events` or `suggest_time`) against the recipient's local time zone before a time goes
in an email. Suggesting a slot he is already booked in is worse than suggesting none.

The booking link is https://calendar.app.google/S56CDe5cBYwNanz39. It belongs in the second
email, after a reply. `copywriting.md` wants zero links in a first touch and that wins.

Batching notes: vary the angle across targets, never send two people at one company the
same email with the name swapped, and flag it when a batch puts more than one person at the
same domain on the same day.

### 5. Hand it back

`references/draft-format.md`. Drafts land in the conversation, not in a send queue. On
request, push them to Gmail drafts, which is not sending.

If Austin asks this agent to send, say the rule once and offer the Gmail draft instead. If
he repeats the instruction, that is his call: read the recipient and subject back to him,
send that one, log it, and leave the default alone.

### 6. Log the send

Only after Austin confirms it went out, and then per `.claude/gtm/crm-sync.md` in full,
which means **both records, person and company, in the same step**.

On the person: `stage` per the ladder in `.claude/gtm/attio-schema.md`, `who_contacted` set
to the exact string `Austin (manual)`, and the `GTM record` note updated rather than a
second note format invented. Check for an already-synced copy of the email with
`search-emails-by-metadata` first, so Attio's Gmail sync and this agent do not both log it.

On the company, same step: last touched, last touched by `Austin`, touches read then
incremented, account status as the furthest rung anyone there has reached, and next step.
Until the company custom fields exist those live in the `GTM account` note.

Then append the row to `state/send-log.md`.

Safe stages are set automatically. `Opportunity`, `Contracting`, `WON-Closed`,
`LOST-Closed` and `Not a Fit` are flagged for Austin and never set by the agent. `Do Not
Contact` is the one flag that moves without asking, and it has no field yet, so it follows
the interim path in `.claude/gtm/attio-schema.md` and gets repeated in the run summary.

## Files

- `references/draft-format.md`: how drafts come back for review
- `state/send-log.md`: what actually went out
- `state/credit-log.md`: every approved paid lookup
- `state/open-approvals.md`: anything left unresolved when a run ends
- `state/drafts/`: saved batches when Austin wants one kept

Shared contracts live in `.claude/gtm/`. The skill stack lives in `.claude/skills/`.
