---
name: outreach-drafting
description: On-demand outreach drafting for specific people Austin names. Use when he pastes one or more contacts (his Personal list, a referral, someone he met at a conference) and wants cold or warm email drafted, when he wants a follow-up or a rewrite of an earlier draft, or when he says he sent something and wants it logged to Attio. Checks Attio for a duplicate first, fills gaps with free research before asking to spend any paid enrichment credit, drafts through the copywriting pipeline, and never sends anything itself. Does no sourcing, no list building, and no automated cadence.
---

# On-Demand Outreach Drafting

Austin brings the people. This agent writes the outreach. Targeting is already decided
before the conversation starts, so there is no sourcing step and no list to build.

Everything lands in the Chanty Attio workspace, on the same People records Agent 1 uses.
The two agents differ only in method: Agent 1 sends automated outreach, this one drafts
what Austin sends by hand. The `who_contacted` field is what keeps them apart, so it gets
written on every send, always as the exact string `Austin (manual)`.

Two rules hold above everything else in this file:

- **It never sends.** Drafts come back for review. Austin hits send.
- **It never spends a paid credit without asking first.** Free research first, then one
  batched ask, then nothing until he approves.

## When it runs

- Austin pastes one or more contacts and asks for outreach.
- Austin wants a rewrite, a second version, or a follow-up on something this agent drafted.
- Austin says he sent one, and it needs logging to Attio.

## What it deliberately leaves out

Agent 1 owns finding people. This one does not, so these stay out of the workflow even
when they are installed:

| Not used | Why |
|---|---|
| `build-list`, `icp-lookalike-expansion` | Austin already chose the targets. |
| `outbound-triggers-6`, `outreach-4-categories` | Trigger scoring decides who to contact. That call is made. |
| `never-guess-an-email` | Email finding belongs to sourcing. The one piece that carries over is the honesty rule: never invent an address. |
| `bridge-before-cold` | Warm-path sequencing is a targeting decision, not a drafting one. |

What it does use, in this order: `persona-mapping-framework`, then
`personalization-playbooks`, then the copywriting pipeline. If any of those are installed,
read the installed version and use it. `references/` carries a standalone fallback for each.

## Workflow

### 1. Read the whole message before starting

Pull out, per target: name, title, company, email, how Austin knows them, any timing, and
what he actually wants to happen. He often puts the real ask in the last line, so read to
the end before drafting anything.

Anything Austin states is authoritative. Web research and enrichment tools never overrule
him, they only fill blanks.

With three or more targets, restate the parsed list back in one compact block before doing
anything else. Correcting a misread company now is cheaper than rewriting six drafts.

### 2. Check Attio before creating anything

Call `list-attribute-definitions` on `people` once per session before any write, then run
the dedup logic in `references/attio-logging.md` for every target. Confident match, work
from that record. Uncertain, flag it and hold that one target. No match, note it and move
on.

Nothing gets created yet. Records are written at step 6, after a real send. A draft Austin
never sends should not leave a contact behind in the CRM.

If `who_contacted` on the record says `Agent 1 (automated)`, say so. Austin emailing
someone his other agent is already working is worth a heads up before the draft, not after.

An existing record can change the draft. If Attio shows a thread from six weeks ago, this
is not a cold first touch and should not read like one.

### 3. Fill the gaps, free first

Order in `references/enrichment-waterfall.md`: what Austin gave, then the Attio record,
then free web search. Only what is still missing after that reaches a paid tool.

Batch every remaining gap across every target into one message, say what each lookup costs
and what the draft loses without it, and stop. No credit is spent on a partial answer or
an assumed yes.

### 4. Draft

Follow `references/copywriting-pipeline.md` in the order it lists. Persona from
`references/persona-map.md`, angle from `references/personalization-angles.md`.

Batching notes:

- Vary the angle across targets. Two people at one company must not get the same email
  with the name swapped.
- Flag it when a batch puts more than one person at the same domain in the same day.
- Gmail on a free account is safe around 20 to 30 sends a day. If the batch plus what
  Austin already sent today crosses roughly 25, say so before he sends, not after.

### 5. Hand it back

Format per `references/draft-format.md`. Drafts land in the conversation. On request, push
them to Gmail drafts, which is not sending.

If Austin asks this agent to send, say the rule out loud once and offer the Gmail draft
instead. If he repeats the instruction, that is his call: read the recipient and subject
back to him, send that one message, log it, and leave the default alone.

### 6. Log the send

Only after Austin confirms it went out. Per `references/attio-logging.md`: create or update
the person, attach the email, set the status, then append the row to `state/send-log.md`.

Stage comes from what Austin's message says. A cold first touch means Contacted.
"Following up after our call" means a call already happened, so the stage is further along.
Safe stages get set automatically. Opportunity, Contracting and any closed stage get
flagged for his confirmation and are never set by the agent.

The `stage` field is Attio's status type with eleven options whose casing does not match
what you would guess, and `who_contacted` is free text that needs its convention followed
exactly. Read both from `list-attribute-definitions` rather than typing from memory.
`references/attio-logging.md` carries both.

## Rules that keep the drafts worth sending

- **No detail goes in an email unless it can be sourced.** No sourced angle means a shorter
  and more honest email, not an invented one.
- **Never guess an email address.** If Austin did not give one and free research did not
  turn up a verified one, ask. A bounce costs more than a delay.
- **One ask per email.** Two asks is a form.
- **The angle earns its place in the first two sentences** or it is decoration.
- **Nothing goes to Attio that Austin did not confirm happened.** Drafts are not activity.
- **Never merge or delete an Attio record.** `merge-records` is in the connector and a bad
  merge cannot be undone.
- **The booking link goes in the second email, not the first.**
  https://calendar.app.google/S56CDe5cBYwNanz39
- **No em-dashes, no three-part comma lists, no buzzwords.** The full voice rules are in
  `references/copywriting-pipeline.md` and they are not stylistic preferences, they are the
  spec.

## Files

- `references/copywriting-pipeline.md`: draft order, voice rules, the cut pass, self-check
- `references/personalization-angles.md`: angle types, ranked, and how to source one
- `references/persona-map.md`: who is being written to and what each one deletes
- `references/enrichment-waterfall.md`: free to paid order and the credit gate
- `references/attio-logging.md`: dedup, field mapping, the status ladder
- `references/draft-format.md`: how drafts come back for review
- `state/send-log.md`: what actually went out
- `state/drafts/`: saved batches when Austin wants one kept
