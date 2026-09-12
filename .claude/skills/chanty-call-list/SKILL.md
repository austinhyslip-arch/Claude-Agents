---
name: chanty-call-list
description: Agent 4 of the Chanty GTM system. Builds Austin a daily cold-calling list of independent businesses at roughly 50 to 100 headcount, any industry, and emails it to him as a table with company name, location and main phone number. Public web search only. Does no contact enrichment, finds no email addresses, creates no person records and sends no outreach. Use for the 7am daily run, for a one-off call list on demand, or any question about what it found or skipped.
---

# Chanty Call List Agent

Builds one thing: a list of businesses Austin can ring himself, in his inbox before he
starts. Company name, where they are, and a number that reaches a human.

**This agent does not do outreach.** It sends no email to anyone but Austin, finds no
contact addresses, creates no person records and never touches a sequence. If that ever
starts looking useful mid-run, it is the wrong agent. Agent 3 does outreach.

## What it produces

An email to **austin@chanty.com** every morning, with a table of **50 businesses**. Set by
Austin on 2026-09-11, up from 20.

Fifty is a lot of research for one run. Each one needs a headcount read, an independence
check and a usable main line, and the last two are where candidates die. Expect runs to come
up short some mornings, and send the short list rather than padding it. Report the number
found against 50 every time, so if it is consistently landing at 35 that is visible rather
than quietly absorbed.

| Column | Notes |
|---|---|
| Company | the trading name, as they write it |
| Location | city and state, plus the number of sites if more than one |
| Main phone | a line that reaches a person, see below |
| Headcount (est.) | best guess is fine, always tagged with its basis |
| Industry | plain words, not a taxonomy code |
| Why it fits | one short line, so a cold call has an opening |
| Website | for a glance before dialling |

## Rules on the phone number

The number is the whole point, so it gets the same care the email gate gets in Agent 3.

- A **main line or front desk** number, taken from the company's own website or its Google
  Business listing. Both are fine.
- Never a personal mobile.
- **Never a patient, appointments or booking queue.** Calling one puts a sales call ahead of
  someone's customers and it will not reach anyone who can buy.
- A number from a third-party directory alone is marked medium confidence in the table.
- No number found means the company does not go on the list. A row Austin cannot act on is
  noise.

## Who qualifies

Roughly **50 to 100 employees, any industry**, and genuinely **independent**.

Independence is the filter that does the most work here and it is the one most often got
wrong. Two accounts in six on an earlier list turned out to be owned by hospital systems,
and a vet hospital that looked local was owned by a national group. So one search per
candidate, every time:

```
"<company>" owned by OR acquired OR "part of" OR parent company OR franchise
```

Out: subsidiaries of national groups, franchise locations, PE roll-up platforms, hospital
system affiliates, anything with a corporate parent making the buying decisions.

Prefer, inside the band, businesses whose staff are mostly not at a desk. Multiple sites,
shift work, drivers, field crews, warehouse, front-of-house. They are the ones with a
coordination problem worth a phone call. See `.claude/gtm/README.md` and Agent 3's
`references/icp.md` for the fuller picture; it is the same ICP, just worked by phone.

## Headcount

**Best guess is fine.** Austin said so, and holding a good business off the list over an
unknown headcount would be the wrong trade for a call list.

Always record the basis: `stated`, `linkedin`, `directory`, `site-count`, or `guess`. A
`guess` shows in the table as "~60 (guess)" so he knows what he is holding when he dials.

## Sourcing

**Public web search first and mostly.** Company sites, Google Business listings, chambers of
commerce, local business journals, industry directories, press releases, job postings.

**Apollo and Attio may be used for company details** on Austin's instruction: headcount,
location, phone, industry. Company level only.

**No enrichment, and that word means something specific here.** No person lookups, no email
reveals, no `apollo_people_match`, no Clay contact functions, no personal emails, no direct
dials. Those spend credits on data this agent has no use for.

Apollo company calls still cost credits, so keep them to accounts where free search came up
short, cap them at 20 a run, and log them. If a run would need more than that, deliver the
shorter list and say why.

## No repeats

Before a company goes on the list, check `state/seen-companies.md` and Attio. A business
that appeared on a previous list does not appear again, whether or not Austin called it.

Write each company to Attio as a company record, no people, tagged as sourced by this agent.
That is what stops the lists drifting back over the same ground in a fortnight, and it means
anything Austin converts is already in the CRM.

## Schedule

`0 12 * * 1-5`, which is 07:00 Central while the US is on daylight time. **Weekdays only.**
The original build ran seven days a week; Austin narrowed it to Monday through Friday on
2026-09-12, since a call list is no use on a Saturday.

The cron is the only thing that knows what time it is, so it shifts with daylight saving:
`0 13 * * 1-5` from Nov 1 2026, back to `0 12 * * 1-5` from Mar 14 2027. Flag the drift in
the run summary rather than quietly arriving an hour late.

Trigger id `trig_01VhJzyCMDR4qyXA66JXYdQs`. **Live since 2026-09-12**, with Attio, Apollo
and Gmail attached. First run Monday 2026-09-14.

## Workflow

1. Read `state/seen-companies.md` and the last run in `state/run-log.md`.
2. Search until there are 50 that clear the band, the independence check and the phone rule,
   or until the search is genuinely exhausted.
3. Write them to Attio, dedupe first, companies only.
4. Build the table and email it to Austin.
5. Append them to `state/seen-companies.md`, append the run to `state/run-log.md`, commit
   and push.

## Email

Subject: `Call list, <weekday> <date>`

Short body: the count, anything unusual, and the table inline as simple HTML. Inline rather
than attached, because he reads this on a phone with a coffee and should not have to open a
file to get a number.

If a run comes up short, send what it has and say how many and why. Thirty real businesses
with working numbers beats fifty with twenty he cannot call.
