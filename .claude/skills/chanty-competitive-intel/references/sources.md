# Sources and how to work them

Order matters. Company-controlled sources are cheap and authoritative — start there, then
spend the remaining effort on reviews and forums where the complaints live.

## 1. Pricing pages (direct check)
Load the pricing page for every Tier 1 and Tier 2 competitor each run. Compare against the
prices recorded in the previous run's log entry. Record: plan names, per-seat price
monthly and annual, seat minimums, what moved between tiers, and any "contact sales"
wall that replaced a published number. A feature quietly moving up a tier is a pricing
change — flag it as one.

## 2. Changelogs and release notes
Use the URLs in `watchlist.md`. Read only entries dated inside the window. Most entries are
routine; you are looking for launches that change the competitive story — AI features,
new product lines, chat/task features that close a gap against Chanty, or removals.

## 3. G2 and Capterra
- G2: `g2.com/products/<slug>/reviews`, sorted or filtered to most recent.
- Capterra: reach via `site:capterra.com <product> reviews`; filter to recent.
- Read reviews inside the window only. Pull the specific gripe, not the star rating.
- What matters: unexpected charges, renewal shocks, seat minimums, tier confusion,
  missing features, performance and reliability, support quality, migration pain.
- Ignore: generic five-star praise, obvious incentivized reviews, complaints about a
  feature that shipped a fix inside the window.

## 4. Reddit
Subreddits per competitor are listed in `watchlist.md`, plus the standing set: r/saas,
r/projectmanagement, r/Slack, r/sysadmin, r/msp.
Search patterns worth running each week:
- `<competitor> price increase`
- `<competitor> alternative`
- `leaving <competitor>`
- `<competitor> billing`
Weight threads by engagement, not by how angry one comment is. A 200-upvote thread about
per-seat cost is a finding; a single downvoted rant is not.

## 5. Hacker News
Search `hn.algolia.com` for each Tier 1 and Tier 2 name, restricted to the window. HN is
the best early source for outages, security incidents, acquisitions, and pricing backlash
— often hours ahead of the trade press.

## 6. Company blogs and press pages
Per `watchlist.md`. Also check investor-relations pages for the public competitors (Asana,
Monday.com, and Salesforce for Slack) when the window includes an earnings date.

## 7. Google Alerts
Reuse the existing alert setup from the outbound agent; add each Tier 1 and Tier 2 name
plus new Tier 3 promotions as they happen. Alerts are a safety net for anything the
searches above missed, not the primary sweep.

## Discovery pass queries (monthly)
Run all four across G2, Capterra, and general web search:
1. `Slack alternative`
2. `Microsoft Teams alternative`
3. `team chat software`
4. `task management software`

Also sweep the "alternatives to" and comparison lists G2 and Capterra generate for Chanty
and for each Tier 1 competitor. Count a name once per distinct source; a name appearing in
two or more distinct sources gets promoted to Tier 3.

## Window discipline
"Inside the window" means published or posted inside it. A five-month-old review resurfaced
by an algorithm is not this week's news. When a source shows no date, either establish the
date another way or leave the item out.
