# CRM sync rules

Attio is the system of record for every contact-level event. These rules decide what an
agent may change on its own and what it has to bring to Austin first.

## Before creating anything

Check for an existing record with `search-records` before anything else. Match on person
name and on company, and prefer domain as the strongest signal. `upsert-record` keyed on
domain for companies and on email for people handles the ordinary case in one call.

- **Confident match** (same domain plus same person name, or same person name plus same
  company name with no conflicting details): update the existing record. Do not create a
  second one.
- **Uncertain match** (name matches but company differs, company matches but the person is
  new, two records already look like the same human): flag it for Austin and move on. Never
  silently merge. Never create a near-duplicate to sidestep the question. `merge-records`
  exists and is irreversible, so it runs only on Austin's explicit go-ahead.

Flagged matches go in `state/open-approvals.md` under `Uncertain match`, with both record
links and what makes them ambiguous.

## Every touch writes to both records

Any outreach to a person also updates that person's company. One reach-out, two records, in
the same step. This is not optional and it is not a nightly job that catches up later.

A **touch** is any of these: an email sent, a reply received, a call placed, a meeting
booked or held, a LinkedIn or other channel message, a bounce, an opt-out. A staged draft
sitting in the queue is not a touch. Nothing counts until it actually went out or actually
came in.

### On the person

| Field | Set to |
|---|---|
| `stage` | the rung this touch moved them to, if it moved them |
| `who_contacted` | Austin, Agent, or the name of whoever reached out |
| Last touch | the date it happened, once the field exists |
| Last touch type | email-sent, reply-received, call, meeting, note |

`who_contacted` is set on every touch without exception. It is the field that answers "has
anyone here already spoken to this person", and it is worthless the first time it gets
skipped.

Plus a dated note saying what happened and who did it.

### On their company, same step

| Field | Set to |
|---|---|
| Last touched | the same date |
| Who contacted | the same value written on the person |
| Touches | existing count plus one |
| Account stage | the furthest rung any person at this company has reached |
| Next step | one line on what happens next, or cleared if nothing is pending |

**None of these fields exist on Companies yet**, so today this block goes into the company's
`GTM account` note instead, in the format in `attio-schema.md`. Read the note, change the
lines, write it back. It is slower and it is not sortable, but the company record stays
honest from the first touch, and the day the fields appear the agent writes to them instead
with nothing else changing.

Read `Touches` before writing it. There is no increment operation, so the agent fetches the
current value and writes the new one, and two runs touching the same account in parallel
would otherwise lose a count.

### Rules on the company roll-up

- **Account stage only moves forward.** A new cold contact at an account already at
  `Replied` does not drag the company back to `Not Contacted`. Take the furthest rung, never
  the most recent one.
- **Past `Meeting Booked` it stops on its own**, same as the person ladder. `Opportunity`,
  `Contracting`, `WON-Closed` and `LOST-Closed` wait for Austin on a company exactly as they
  do on a person.
- **An opt-out flows both ways.** One person asking not to be contacted is set on that
  person immediately and they come out of every queue. If they asked on behalf of the
  business, or they are the owner, apply it to the company too and pull their colleagues.
  When it is ambiguous, set the person, flag the company, let Austin decide. Note the gap in
  `attio-schema.md`: there is no Do Not Contact status yet, so this currently lands as `Not a
  Fit` plus a note saying what it really was.
- **A bounce is a touch.** It updates both records. An account whose only touches are
  bounces is a data problem, not an engaged account, so `Next step` says so.

### What Attio already does by itself

The stock `last_email_interaction` and `last_interaction` fields exist on both people and
companies, and Attio's Gmail sync fills them in from real mail without the agent doing
anything. Those cover mail sent from the synced mailbox and they roll up to the company on
their own.

They do not cover everything, which is why the fields above still matter. Attio's version
misses calls, anything sent outside the synced mailbox, the touch count, and any notion of
what happens next. Read Attio's fields, do not fight them, and treat a disagreement between
the two as worth flagging rather than silently overwriting.

## What updates automatically

**Reply received.** Set `stage` to `Replied`, set `who_contacted`, log the message on the
record, stamp the date, and roll the touch up to the company per the section above. No confirmation needed. Classify
the reply with `handle-reply`, put the suggested next action on the person record as a note
and in the company's `Next step`, but do not send anything.

**Reply sent by Austin.** Attio's native Gmail sync should catch this. The agent's job is to
verify it actually did, with `search-emails-by-metadata` against recent records. If sent
mail is not landing on records, flag it in the run summary rather than duplicating the
logging by hand.

**Demo booked.** Comes through the Calendly to Attio connection over Zapier. Set status to
`Meeting Booked`. If that connection is not live, cross-check with Attio `search-meetings`
and with Google Calendar `list_events`, then ask Austin to confirm before setting it.
A calendar entry is good evidence, not a confirmation.

**Bounce.** Note the bounce on the record, remove the address, and take the person out of
every queue. There is no bounced status in the ladder, so `stage` stays where it was and the
note carries the fact. Do not retry the address, and do not go guess a replacement pattern.
A bounce is a touch, so it rolls up to the company like any other.

## What never updates automatically

**`Opportunity` and everything past it.** `Opportunity`, `Contracting`, `WON-Closed` and
`LOST-Closed` are flagged as a candidate change and wait for Austin's confirmation.
`Opportunity` is included because it is a judgement about whether a real deal exists, which
is not the agent's call to make.

**Never advance a deal stage off inferred email content alone.** "Sounds good, send me the
contract" is a candidate, not a stage change. The candidate goes in
`state/open-approvals.md` with the quote that prompted it.

**Do Not Contact.** Any opt-out request, however casually worded, sets `Do Not Contact`
immediately and removes the record from every queue. This is the one flag that moves
without asking, and it never gets reversed by an agent.

## Gap filling

Missing contact info on an existing record follows the same order as a new one. Free web
search first, then batch the remainder and ask before any Apollo, Hunter or Clay call. See
`sourcing-and-credits.md`.

## Write discipline

- One record per human. One record per company.
- Do not overwrite a field Austin filled in by hand. If the agent's value disagrees, add a
  note and flag it.
- Estimates stay labelled as estimates. Employee count always carries its basis field.
- Every status change gets a dated note saying what caused it.
