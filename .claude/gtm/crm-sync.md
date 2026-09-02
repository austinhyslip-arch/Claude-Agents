# CRM sync rules

Attio is the system of record for every contact-level event. These rules decide what an
agent may change on its own and what it has to bring to Austin first.

## Before creating anything

Check for an existing record. Match on person name and on company, and prefer domain as the
strongest signal.

- **Confident match** (same domain plus same person name, or same person name plus same
  company name with no conflicting details): update the existing record. Do not create a
  second one.
- **Uncertain match** (name matches but company differs, company matches but the person is
  new, two records already look like the same human): flag it for Austin and move on. Never
  silently merge. Never create a near-duplicate to sidestep the question.

Flagged matches go in `state/open-approvals.md` under `Uncertain match`, with both record
links and what makes them ambiguous.

## What updates automatically

**Reply received.** Set status to `Replied`, log the message on the record, stamp the date.
No confirmation needed. Classify the reply with `handle-reply` and put the suggested next
action on the record as a note, but do not send anything.

**Reply sent by Austin.** Attio's native Gmail sync should catch this. The agent's job is to
verify it actually did. On each run, spot-check recent sent mail against the records. If
sent mail is not landing on records, flag it in the run summary rather than duplicating the
logging by hand.

**Demo booked.** Comes through the Calendly to Attio connection over Zapier. Set status to
`Meeting Booked`. If that connection is not live, ask Austin to confirm the booking, then
set it manually.

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
