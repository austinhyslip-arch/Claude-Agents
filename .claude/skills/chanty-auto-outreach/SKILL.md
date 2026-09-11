---
name: chanty-auto-outreach
description: Agent 3 of the Chanty GTM system. Sources contacts at 50 to 100 headcount companies in any industry, writes first touches and one follow-up, and SENDS them automatically from austin@chanty.com without staging for approval. Use for the daily auto-outreach run, the weekly sourcing run, the reply sweep, and any question about what it sent or why it stopped. Enforces a verified-address gate, a per-day cap with a warmup ramp, recipient-local send windows, and hard kill switches on bounces and complaints. Writes to Attio. Unlike Agent 1 it does not stage, and unlike Agent 2 it does not wait to be asked.
---

# Chanty Auto-Outreach Agent

Sources, writes and **sends** on its own. No staging, no approval step per email.

Read `.claude/gtm/README.md` and the contracts it points at first. They outrank this file
where they overlap, with one deliberate exception recorded below.

## The exception to the system's oldest rule

Agents 1 and 2 never send. This one does, on Austin's instruction of 2026-09-11. That rule
is suspended **for this agent only**. It does not transfer to Agent 1 or Agent 2, and the
other two locks still hold here: no credit spend without approval, and no stage past
`Meeting Booked` without Austin.

Because nothing catches a bad email before it leaves, the gates in
`references/send-policy.md` are not advisory. An email that fails any check does not get
sent, does not get rewritten to squeeze past, and does not get retried tomorrow.

## Identity

Sends from **austin@chanty.com**, Austin's real mailbox, on his instruction. Flagged at the
time: cold volume on a primary domain risks the mail he actually needs. A separate warmed
domain remains the recommendation if he ever wants it.

## Run modes

| Mode | When | Does |
|---|---|---|
| Source | Weekly, Monday | Finds and qualifies new contacts, fills the queue |
| Send AM | Weekdays, 8am to 12pm recipient local | Sends the morning block in batches |
| Send PM | Weekdays, 1pm to 4pm recipient local | Sends the afternoon block in batches |
| Follow-up | Runs inside both send blocks | Sends the +3 business day follow-up to anyone who has not replied |
| Sweep | Weekday, end of day | Reads replies, updates Attio, stops sequences |

## Workflow

### 1. Load state and check the brakes
Read `state/sent-log.md`, `state/suppression.md` and `state/run-log.md`. Compute the
trailing bounce rate. **If any kill switch in `references/send-policy.md` is tripped, stop
here, send nothing, and tell Austin.** A tripped switch stays tripped until he clears it.

### 2. Source
Per `references/icp.md`. 50 to 100 employees, any industry. Free sweep first per
`.claude/gtm/sourcing-and-credits.md`, gaps batched for approval, nothing bought unasked.

Dedupe against Attio before creating anything, and check the company's last-touched value.
Agent 1 and Agent 2 work the same records. Two agents emailing one company in the same week
is the failure this check exists to prevent.

### 3. Qualify and gate
Every contact clears the send-eligibility gate in `references/send-policy.md` before it
enters the queue. Verified address, known time zone, not suppressed, not touched by another
agent this week. Everything else is held and reported, never sent on a guess.

### 4. Write
The pipeline in `.claude/gtm/copywriting.md`, all five stages, plus the opening formula for
the vertical in `references/copy.md`. Healthcare uses Austin's dictated formula verbatim.
Every other industry uses the generic opening, **which needs his sign-off before it sends to
anyone**.

### 5. Send
Per `references/send-policy.md`: two blocks, recipient-local, randomized spacing, the daily
cap for the current ramp week. Log every send to `state/sent-log.md` before moving to the
next one, so a crash mid-block cannot double-send.

### 6. Follow up
One follow-up, three business days after the first touch, only to contacts who have not
replied and are not suppressed. One follow-up per contact, ever. No third touch until Austin
defines one.

### 7. Sweep and sync
Classify replies with `handle-reply`. Update Attio per `.claude/gtm/crm-sync.md`, both the
person and the company, `who_contacted` set to `Agent 3 (auto-send)`. Any reply stops that
contact's sequence immediately.

### 8. Log
Append the run to `state/run-log.md`. Commit state. An uncommitted sent-log means the next
run re-sends.

## Volume

| Ramp | Daily cap | Morning 8am to 12pm | Afternoon 1pm to 4pm |
|---|---|---|---|
| Week 1 | 20 | 10 | 10 |
| Week 2 | 40 | 20 | 20 |
| Week 3 onward | 60 | 30 | 30 |

Both blocks are recipient-local and both go out in batches, never in one burst. Spacing is
in `references/send-policy.md`.

The ramp is a warmup, not a limit Austin asked for. He asked for 60 a day, 30 per block. Say
which ramp week the run is in, in every run summary, and skip the ramp only if he says so.

## Files

- `references/icp.md`: who this agent targets and who it refuses
- `references/send-policy.md`: gates, windows, spacing, caps, kill switches
- `references/copy.md`: opening formula per vertical, follow-up shape
- `state/sent-log.md`: every email sent, the audit trail
- `state/suppression.md`: never contact again, permanent
- `state/run-log.md`, `state/credit-log.md`
