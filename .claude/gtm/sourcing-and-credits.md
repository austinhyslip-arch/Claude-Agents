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

**1. Free web search. Always first, and it is not one query.**

A contact is not a gap until every applicable source below has been checked and the check
recorded on the record. "Free search found nothing" is only true if this list was worked.
Ranked by what actually produced results in the 2026-09-02 healthcare run.

| # | Source | What it gives | Query shape |
|---|---|---|---|
| 1 | **Press releases and newswires** | the best free source by some distance. Media contact lines carry a named person with a real published address | `"<company>" press release media contact email @<domain>` |
| 2 | Company's own site | contact, team, about, staff, leadership, news pages | site-scoped search, or fetch the pages directly where the environment allows it |
| 3 | Practice and business directories | Yelp, Healthgrades, WebMD, Tebra, Solv, chamber of commerce listings. Often carry an admin email a company never puts on its own site | `"<company>" <city> contact email` |
| 4 | Facebook business page | small practices publish an address here that appears nowhere else, and multi-site groups often run one page per location | `"<company>" facebook contact email` |
| 5 | Google Business listing | main line, hours, address | company name plus city |
| 6 | Patient-facing PDFs and forms | intake forms, new patient packets and billing pages routinely print an office or records email | `"<company>" filetype:pdf email` or `"<company>" new patient forms email` |
| 7 | Job postings | a hiring contact, and the growth points on the score at the same time | `"<company>" jobs "<role>"` |
| 8 | State licensure, registry, NPI | verifies the entity and often the practice address | state board lookup for the discipline |
| 9 | Association and conference listings | member directories and speaker pages carry named people with contact details | `"<company>" OR "<person>" conference speaker OR member directory` |
| 10 | LinkedIn company page | confirms named leaders and the company profile URL that paid tools want later | company name |

**Phone**: the main line from their own site or Google Business listing. Main lines are
enough, nobody needs a personal cell.

**Email**: a named person's published address is the best case. A published role inbox at
the right company is acceptable when the persona is clear, and it gets written as a routing
note rather than a pitch.

Record what was checked. A record that says "no email, checked press releases, directories,
Facebook and the site" is worth something on the next run. One that just says "no email" gets
the whole sweep repeated.

### Check ownership before anything else

Run this while sourcing, not after. In the six-account healthcare test, two turned out to be
owned by hospital systems and one was a 300-site operator that probably buys through
procurement. That is half the list disqualified on a question that costs one search.

`"<company>" owned by OR affiliated OR "medical group" OR health system`

An account that fails this check never reaches the gap batch, so it never costs a credit.
Disqualifying early is the cheapest credit discipline there is.

### What not to treat as a source

Sites offering an "email format" or "email pattern" for a company are pattern generators.
They will happily hand over `first.last@domain` for a person they have never seen. That is a
hypothesis, not a contact, and it stays out of the queue however confident it looks.

**2. Batch the gaps and ask.**

Whatever the full sweep above could not find gets held in a batch. Nothing is bought one
contact at a time, and nothing is bought for a contact whose sweep is incomplete. When the batch is ready, ask Austin in a single message: how many contacts, which
list, what is missing, which provider, the estimated credit cost, and the balance that
would be left. Then stop and wait.

Never call a paid lookup automatically. Not on a schedule, not to finish a list, not
because a run would otherwise come up short of its weekly number. A short list is fine. An
unapproved charge is not.

### Size the batch to the sends, not the records

The most expensive habit is buying an address for every contact on a record. The send rules
allow one cold email per company per week, so an account with four named people needs **one**
address, not four. Buying all four is three credits spent to send one email, and the other
three go stale before they are used.

Buy for the person who is actually getting the first touch. The rest stay as records and cost
nothing until they are needed.

**3. On approval only, the waterfall.**

| Order | Provider | Use | State |
|---|---|---|---|
| 1 | Apollo | first paid attempt | connected |
| 2 | Hunter | verification, and second attempt when Apollo comes back empty | **not connected** |
| 3 | Clay | last resort, mostly the Personal list, thin free pool | connected |

**The order above is the brief's, and it may be wrong.** Clay's workspace carries a **Work
Email** function that cascades across several email providers in sequence, stops at the first
valid result, and only charges for what it finds. That is a waterfall and a pay-on-success
model in one action, which is the verification rung the brief assigned to Hunter. Apollo
charges per record it reveals whether the address is any good or not.

For a small precise batch, Clay first is probably cheaper. For volume, Apollo's per-unit cost
probably still wins. This has not been changed because the order is Austin's call, and the
Clay balance is not visible through the connection so the trade cannot be quantified yet.

Hunter has no connector in this setup, so the middle rung is missing. Until it is added,
the waterfall is Apollo then Clay, and verification falls to whatever the provider itself
returns. Say so in the approval request rather than letting Austin assume a verification
step ran.

Stop the moment a verified result comes back. Do not run the same contact through every
provider to compare.

### A provider returning an address is not the same as finding one

This is the rule the 2026-09-02 run was written to prevent breaking. Apollo answered a
lookup with an address, and the address failed every test that matters:

- `email_status: extrapolated` means Apollo assembled it from a pattern. It is the same
  guess `never-guess-an-email` forbids, made by a vendor instead of by us, and paid for.
- `extrapolated_email_confidence: 0.6` is a probability, not a verification. No confidence
  score turns a hypothesis into a contact.
- `email_domain_catchall: true` means any verifier will answer accept-all, which is the
  documented trap.
- The matched organisation was a similarly named practice in a different state, on a
  different domain. A name match is not an employer match.

**Check these fields on every paid result before the address goes anywhere near the queue:**

| Field | Accept | Reject |
|---|---|---|
| `email_status` | `verified` | `extrapolated`, `guessed`, `unavailable` |
| `email_domain_catchall` | `false` | `true` |
| matched organisation | domain, location and description all match the account | anything else |

A rejected address gets recorded on the person as rejected with the reason, and never
written to the email field. Putting it there makes it look sendable to the next run.

Log the spend either way. A credit that bought a rejected address still cost a credit, and
the log is how the hit rate becomes visible.

**What a rejected lookup can still be worth.** The same call returned a LinkedIn URL, a
corrected job title, a start date and a full work history, one job of which was at another
account on the same list. That was the useful part of the purchase. Read the whole payload
before writing the lookup off.

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
