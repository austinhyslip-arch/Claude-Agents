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
| Last touch | the date it happened |
| Last touch type | email-sent, reply-received, call, meeting, note |
| GTM status | the rung this touch moved them to, if it moved them |

Plus a dated note saying what happened and who did it.

### On their company, same step

| Field | Set to |
|---|---|
| Last touched | the same date |
| Last touched by | Austin or Agent |
| Touches | existing count plus one |
| Account status | the furthest rung any person at this company has reached |
| Next step | one line on what happens next, or cleared if nothing is pending |

Read `Touches` before writing it. There is no increment operation, so the agent fetches the
current value and writes the new one, and two runs touching the same account in parallel
would otherwise lose a count.

### Rules on the company roll-up

- **Account status only moves forward.** A new cold contact at an account already at
  `Replied` does not drag the company back to `Queued`. Take the furthest rung, never the
  most recent one.
- **Past `Meeting Booked` it stops on its own**, same as the person ladder. `Contracting`,
  `Won` and `Lost` on a company wait for Austin exactly like they do on a person.
- **`Do Not Contact` is the exception that flows both ways.** One person opting out sets
  that person immediately. If they asked on behalf of the business, or they are the owner,
  set the company too and pull every colleague from the queues. When it is ambiguous, set
  the person, flag the company, and let Austin decide.
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

**Reply received.** Set status to `Replied`, log the message on the record, stamp the date,
and roll the touch up to the company per the section above. No confirmation needed. Classify
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

**Bounce.** Set `Email status` to `bounced` and person status to `Bounced`. Remove from any
queue. Do not retry the same address, and do not go guess a replacement pattern.

## What never updates automatically

**Contracting and everything past it.** `Contracting`, `Won` and `Lost` are flagged as a
candidate change and wait for Austin's confirmation.

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
