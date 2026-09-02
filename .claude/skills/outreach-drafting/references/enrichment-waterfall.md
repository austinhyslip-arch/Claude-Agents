# Enrichment waterfall and the credit gate

Targeting is already done, so enrichment here has one job: fill the specific blanks that
change the draft. It is not research for its own sake.

Verified September 2, 2026: Apollo and Clay are both connected. Hunter.io is not, and it is
not in the connector directory, so **Apollo carries email reveal and verification**.

## Order

1. **What Austin gave.** Authoritative. Never overwritten by a tool.
2. **The Attio record.** Past notes, synced emails, `last_interaction`, `stage`, `who_contacted`.
   Free, and it is the thing most likely to change the draft.
3. **Free web.** Company site, newsroom, public LinkedIn activity, news search, podcasts,
   conference agendas, open job postings. Most angles come from here for nothing.
4. **Apollo.** `apollo_people_match` for a single person, `apollo_bulk_enrich_people` for a
   batch, `apollo_organizations_enrich` for the company. This is where an email address
   gets revealed and verified. Credit-gated.
5. **Clay.** Last in the waterfall, for the cases where Apollo came back empty.
   `find-and-enrich-list-of-contacts` for a batch. Credit-gated.

Steps 4 and 5 do not run until Austin approves.

## Credit reality

Apollo, read live on September 2, 2026:

| Credit type | Limit | Left | Used for |
|---|---|---|---|
| Lead credits | 135 | 135 | Person enrichment and email reveal. The one that matters here. |
| Export credits | 0 | 0 | None available. Do not plan around exports. |
| Direct dial | 160 | **0** | Exhausted. Phone lookups are not available. |

The cycle runs **two weeks**, not a month. It started September 2 and resets September 16.
135 lead credits across fourteen days is roughly nine a day if spread evenly, which is
plenty for hand-drafted outreach and not plenty for list building.

Check the live balance with `apollo_usage_stats_credit_usage_stats` before quoting a
number. Do not repeat the table above as if it were current. Apollo also returns an
`mcp_credits` block on spending calls, with estimated cost and the new balance. Surface it
to Austin every time, unprompted.

Clay workspace is **Chanty** (1356452). Its free tier is thin, roughly 100 data credits a
month, which is why it sits last.

## What is worth a credit

Worth it:
- A missing or unverified email address on someone Austin actually intends to email.
- A title that free sources disagree on, when the persona choice turns on it.
- Confirming a person is still at the company, when the last signal is over a year old.

Not worth it:
- Filling a field that does not appear in the draft.
- Company headcount, funding totals, or tech stack when the angle does not use them.
- Anything for a target Austin flagged as a maybe.
- Phone numbers. There are no direct dial credits left.

Default to drafting around a gap. A slightly less specific email that goes out today beats
a perfect one waiting on a credit approval.

## The credit gate

Batch every gap across every target into one message. Never ask twice in a run, and never
spend on an assumed yes.

Format:

```
Paid lookups needed. Nothing spent yet. Apollo lead credits: 135 left, resets Sept 16.

1. Jane Doe (Acme) - no email address
   Apollo people_match, 1 lead credit
   Without it: no address to send to.

2. Sam Roe (Beta) - title conflict, LinkedIn says Director, site says VP
   Apollo people_match, 1 lead credit
   Without it: I draft to the more senior read and flag it in the notes.

Approve all, approve a subset, or tell me to draft around them.
```

Always say what the draft loses. That is what makes the answer easy.

## Rules

- **Never guess an email address.** Not from a pattern, not from a domain, not from a
  colleague's address. If Apollo cannot verify it, say so and hand back the draft with the
  address blank.
- **A tool result never overrules Austin.** If Apollo says the title is different from what
  he said, flag the conflict, do not silently switch.
- **Surface the `mcp_credits` block** from every Apollo call that returns one.
- **Log what a lookup cost** in the draft notes, so the two-week window stays visible.
- **A failed paid lookup is still a spent credit.** Say so rather than quietly retrying.
- **No enrichment on a target Austin has not committed to contacting.**
- **Do not use Apollo's sequence, campaign, or send tools.** `apollo_emailer_*` and
  `apollo_sequences_*` are cadence automation, which this agent does not do, and
  `apollo_emailer_messages_send_now` would break the no-send rule outright.
