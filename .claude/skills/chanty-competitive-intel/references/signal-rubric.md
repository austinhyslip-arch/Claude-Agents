# Big Stuff vs. noise

Adapted from the outbound agent's trigger-scoring logic. If `outbound-triggers-6` or
`outreach-4-categories` are installed, read them and use their thresholds instead; this
file is the standalone fallback.

## The six flag categories

Anything matching one of these, on any tracked competitor, is a candidate for the top of
the email:

1. **Pricing change** — new tier, price up or down, plan restructuring, seat-minimum
   change, a feature moved between tiers, a published price replaced by "contact sales".
2. **Major feature launch or product acquisition** — a launch that closes or opens a gap
   against Chanty, a new product line, or buying another product to fold in.
3. **Funding, acquisition, or being acquired** — a round, a majority sale, an IPO step,
   or the company itself being bought.
4. **Significant outage or security incident** — multi-hour or multi-region outage, a
   breach, a disclosed vulnerability with customer impact.
5. **C-suite leadership change** — CEO, CFO, CPO, CTO, CRO departures or hires.
6. **Layoffs or major restructuring** — headcount cuts, office closures, a business unit
   folded or spun out.

## Scoring

Score each candidate; report at the top of the email at **4 or more**.

**Materiality (0-3)** — how much it changes a Chanty sales conversation.
- 3: changes what a prospect pays or whether they can stay (price increase, forced tier
  migration, a breach, a product sunset)
- 2: changes the feature comparison or the vendor's stability story (major launch,
  acquisition, layoffs, CEO change)
- 1: notable but not conversation-changing (minor feature, mid-level exec change)
- 0: routine shipping

**Tier weight (0-2)** — 2 for Tier 1, 1 for Tier 2, 1 for a Tier 3 name Chanty actually
loses deals to, 0 for other Tier 3.

**Confirmation (0-2)**
- 2: primary source — the company's own page, filing, or status page
- 1: two independent secondary sources, or one named-reporter story
- 0: single unnamed source, rumor, one forum comment

**Recency (0-1)** — 1 inside the window, 0 outside it.

An item scoring 0 on confirmation never goes in the email regardless of total. Report it as
a lead in the body only if it is worth Austin knowing someone is saying it, and label it
"unconfirmed".

## Noise — do not flag

- Routine bug-fix releases and mobile app version bumps
- Blog posts, webinars, awards, "we're a leader in the Gartner X" posts
- Brief single-region blips already resolved on the status page
- Conference talks, hiring posts, partner announcements with no product or price effect
- A competitor's marketing claim restated by a content farm
- Anything already reported in a previous run that has not materially escalated

## Escalation exception

An item already reported can be re-reported once when it materially escalates: rumor to
confirmed, announced to live, a price floated to a price charged, an outage to a
postmortem with a root cause worth quoting. Say explicitly that it is an update to a
previously reported item.
