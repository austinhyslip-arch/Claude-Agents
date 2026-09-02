# Sourcing and credit discipline

Applies to every contact either agent touches, whether it is a new record or a gap being
filled on an old one. Credits are the scarce thing here, so the order below is not a
suggestion.

## Order of attempts

**1. Free web search. Always first.**

- **Phone**: the practice, office or company main line, taken from their own website or
  their Google Business listing. Main lines are enough. Nobody needs a personal cell.
- **Email**: the contact, team or about page on the company's own site. A named person's
  address on their own site is the best case. A monitored role address at the right company
  is acceptable when the persona is clear.

Free search is not one query. Before a contact is called a gap, it has had:

- the company site checked directly (contact, team, about, staff, leadership)
- the Google Business listing checked for the main line
- one site-scoped search for the person's name
- for healthcare specifically, the state license lookup or practice directory listing when
  the site is thin

**2. Batch the gaps and ask.**

Whatever free search could not find gets held in a batch. Nothing is bought one contact at
a time. When the batch is ready, ask Austin in a single message: how many contacts, which
list they belong to, what is missing (email, phone or both), and which provider would be
used. Then stop and wait.

Never call Apollo, Hunter or Clay automatically. Not on a schedule, not to finish a list,
not because a run would otherwise come up short of its weekly number. A short list is
fine. An unapproved charge is not.

**3. On approval only, the waterfall.**

| Order | Provider | Use |
|---|---|---|
| 1 | Apollo | first paid attempt |
| 2 | Hunter | verification, and second attempt when Apollo comes back empty or unverified |
| 3 | Clay | last resort, and mostly reserved for the Personal list because the free credit pool is thin |

Stop the moment a verified result comes back. Do not run the same contact through all
three to compare.

## Tagging

Every contact record carries how its contact info was found:

- `free-web-search`
- `paid-apollo`
- `paid-hunter`
- `paid-clay`

Where email and phone came from different places, tag the source of the email, since email
is what gets used for outreach. Note the phone source in the record notes.

This tag is what makes the credit spend auditable later. A record with no source tag is
treated as unverified.

## Verification before send

From `never-guess-an-email`: a pattern-guessed address is not an address. `first.last@domain`
inferred from a colleague's format has not been verified and does not go in the send queue.
It goes in the gap batch.

An email is send-eligible when one of these is true:

- it is published on the company's own site
- a verification provider returned it as valid, not as risky or catch-all or unknown
- it has previously received mail from us without bouncing

Catch-all domains count as unverified. They can still be worth sending to, but they get
flagged as catch-all in the queue so Austin makes that call rather than the agent.

## Credit log

Every approved spend gets appended to the agent's `state/credit-log.md`: date, provider,
how many lookups, which list, and what came back. This is the only record of where the
credits went.
