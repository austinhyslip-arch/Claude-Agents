# Sourcing companies — free sources first, Apollo as fallback

Order matters, same discipline as enrichment: exhaust the free, referenceable sources for a
given search (e.g. "independent family medicine practices in Little Rock, AR, under 200
staff") before calling Apollo to fill the gap.

## Free sources

1. **Web search** — direct queries like `independent <specialty> practice <city> <state>`,
   `<specialty> clinic <city>` -"hospital" -"health system", chamber-of-commerce and local
   business directory listings, "best <specialty> practices in <city>" local roundups.
2. **NPI Registry (NPPES)** — public, free, healthcare-specific. Good for practice name,
   address, taxonomy/specialty, and the authorized official (often the owner). Query by
   state + taxonomy description + city/zip. **Direct API access
   (`npiregistry.cms.hhs.gov`) was blocked by this environment's egress policy as of this
   skill's build** — confirmed by a direct test fetch. Before relying on it, retest; if
   still blocked, fall back to web search for NPI lookups (`site:npiregistry.cms.hhs.gov
   <practice name>` or `NPI registry <practice name> <city>`) or run this step from a
   session with open egress. Note whichever path worked in the run log.
3. **Facebook business pages** — practice's own page for staff, specialty, location, and
   sometimes a stated staff count in the "About" section.
4. **Company website** — the practice's own site is usually the best source for domain,
   specialty, location, and independence-check language (see `qualification.md`).
5. **Press releases / local news** — practice openings, expansions, community awards,
   "meet the new office manager" pieces.
6. **Google Custom Search API** — the spec calls for this specifically. No Custom Search
   API key is configured in this environment as of this skill's build (checked — no
   relevant env var present). The built-in web search tool available in this session serves
   the same purpose (free, no per-query cost to Austin) and should be used in its place. If
   Austin later provides a Custom Search API key/CSE ID, wire it in and update this note —
   until then, treat "Google Custom Search API" in the original spec as "web search."

## Apollo fallback

Only reach for Apollo's company search (`apollo_mixed_companies_search`) when free sources
haven't surfaced enough qualified candidates for the requested geography/specialty — e.g.
web search and NPI Registry combined return fewer than a handful of independent practices
for a market that should have more. Filter Apollo results to the requested specialty and a
generous employee-count ceiling (a bit above 200, since Apollo's own bucketing can be
imprecise) and run every result through the size and independence checks in
`qualification.md` — Apollo's own data doesn't pre-qualify anything.

Apollo's organization enrich (`apollo_organizations_enrich` /
`apollo_organizations_bulk_enrich`) is also the fallback for company-level fields (staff
count, domain, LinkedIn, parent-company signal) when free sources don't have them — this is
allowed more freely than person-level paid lookups since it's not gated by the per-row
confirmation step in `enrichment.md` (that gate is specifically for contact emails).

## Search scope for one run

A run is scoped by whatever Austin specifies (a metro area, a state, a specialty, or "as
many qualified independent healthcare practices as you can find" for a broader pull).
Confirm the scope at the start of a run if it's ambiguous, and record it in `Summary` sheet
and `state/run-log.md` so repeat runs don't re-source the same market from scratch without
knowing what's already been covered.
