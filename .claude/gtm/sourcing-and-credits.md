# Sourcing and credit discipline

Applies to every contact either agent touches, whether it is a new record or a gap being
filled on an old one. Credits are the scarce thing here, so the order below is not a
suggestion.

## What the credit pool actually looks like

Checked 2026-09-02. Apollo is on a two-week cycle, and this one ends **2026-09-16**.

| Apollo credit | Limit | Left |
|---|---|---|
| Lead credits | 135 | 135 |
| Direct dial credits | 160 | 0, all consumed |
| Export credits | 0 | 0 |

Read that against the plan. Healthcare wants 200 contacts a week across both lists, and
Apollo has 135 lead credits a fortnight. Even spending every credit, Apollo covers under a
fifth of the target. Free web search is not the polite first step here, it is the only way
the numbers work. Direct dials are already gone, which is fine, since the brief only ever
wanted main lines.

Clay's pool is thinner still, which is why it stays reserved for the Personal list.

Re-check the balance with `apollo_usage_stats_credit_usage_stats` at the start of any run
that might spend, and put the number in the approval request so Austin is deciding with the
real figure in front of him. Apollo returns an `mcp_credits` block on spending calls. Surface
it every time, unprompted: the estimate before, then the actual spend and new balance after.

## Order of attempts

**1. Free web search. Always first.**

- **Phone**: the practice, office or company main line, taken from their own website or
  their Google Business listing. Main lines are enough. Nobody needs a personal cell.
- **Email**: the contact, team or about page on the company's own site. A named person's
  address on their own site is the best case. A published role inbox at the right company
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
list, what is missing, which provider, the estimated credit cost, and the balance that
would be left. Then stop and wait.

Never call a paid lookup automatically. Not on a schedule, not to finish a list, not
because a run would otherwise come up short of its weekly number. A short list is fine. An
unapproved charge is not.

**3. On approval only, the waterfall.**

| Order | Provider | Use | State |
|---|---|---|---|
| 1 | Apollo | first paid attempt | connected |
| 2 | Hunter | verification, and second attempt when Apollo comes back empty | **unavailable, no connector exists** |
| 3 | Clay | last resort, mostly the Personal list, thin free pool | connected |

Hunter has no connector in this setup and none exists in the connector directory, so this
is not a matter of Austin connecting it. Treat the waterfall as Apollo then Clay
permanently, with verification falling to whatever the provider itself returns. Say so in the approval request rather than letting Austin assume a verification
step ran.

Stop the moment a verified result comes back. Do not run the same contact through every
provider to compare.

### Which tool does which job

**Apollo**, all of these spend credits.

- `apollo_people_match` and `apollo_people_bulk_match`: enrich a known person. Bulk for a
  batch, since one call for twenty people is easier to account for than twenty calls.
- `apollo_organizations_enrich`, `apollo_organizations_bulk_enrich`: company detail.
- `apollo_mixed_people_api_search`, `apollo_mixed_companies_search`: discovery.
- `apollo_organizations_job_postings`: hiring signal, and a genuinely useful one for the
  score's growth points.

**Clay**

- `find-and-enrich-contacts-at-company`, `find-and-enrich-list-of-contacts`,
  `find-and-enrich-company`.
- `list_subroutines` first if the workspace has its own enrichment functions built, since
  a function Austin already configured beats a generic lookup.

### Apollo tools that are off limits

Apollo can send email and run sequences. This agent never does.

Banned outright: `apollo_emailer_messages_send_now`, `apollo_emailer_messages_create`,
`apollo_emailer_campaigns_approve`, `apollo_emailer_campaigns_add_contact_ids`,
`apollo_sequences_create`, `apollo_sequences_update`, `apollo_phone_calls_create`,
`apollo_tasks_bulk_create`.

The no-auto-send rule is not a Gmail rule, it is a rule about the agent. Routing outbound
through Apollo's sender would break it just as thoroughly, and it would do it inside a tool
Austin is not watching.

## Tagging

Every contact record carries how its contact info was found:

- `free-web-search`
- `paid-apollo`
- `paid-hunter`
- `paid-clay`

Where email and phone came from different places, tag the source of the email, since email
is what gets used for outreach. Note the phone source alongside it.

This tag is what makes the credit spend auditable later. A record with no source tag is
treated as unverified.

## Verification before send

From `never-guess-an-email`: the question is whether an address was **published** or
**assembled**. An address you built from a name and a domain is a hypothesis, and no
confidence score turns a hypothesis into a contact. `first.last@domain` inferred from a
colleague's format does not go in the send queue. It goes in the gap batch.

An email is send-eligible when one of these is true:

- it is published on the company's own site or in a registry
- a provider returned it as verified, not as risky or accept-all or unknown
- it has previously received mail from us without bouncing

**Catch-all and accept-all domains do not count as verified**, and a checker saying
"accept all" is the exact trap that skill warns about. Those addresses stay held and go to
the queue Austin works by hand. He can decide to send. The agent does not decide for him.

Where a named person has no address at all, rank the published role inboxes: sales-flavoured
first (`sales@`, `partnerships@`), then neutral (`contact@`, `hello@`), then support last,
because a support inbox is a ticket queue rather than a door. Write to a reception desk
differently, one line asking to be routed to whoever owns this, easy to forward. Where no
address exists in any form, mark the account unreachable by email and route it to a channel
a human works. Do not invent one.

Hard bounce or dead domain means permanent suppression, applied before the next send, and
kept on the record so a later campaign cannot resurrect it.

## Credit log

Every approved spend gets appended to the agent's `state/credit-log.md`: date, provider,
how many lookups, which list, what came back, and the balance left. This is the only record
of where the credits went.
