# Public-source email hunt: test results

Ran 2026-09-07, before spending any enrichment credits.

## What was tried

**Direct site fetch, 7 domains** (esotericdetail.com, fallsheating.com, gctaxlaw.com,
kolbdental.com, regalassociates.com, peaklendingteam.com, victorhayesco.com):
**0 emails found.** Every one used a contact form instead of publishing an address,
or rendered its contact details in JavaScript the fetcher does not execute. This
is normal - small businesses hide addresses to avoid spam harvesting.

**Web search, 6 queries:** one genuinely useful hit, one generic inbox, two masked
patterns, two nothing.

| Target | Result | Usable? |
|--------|--------|---------|
| Tenby Dahman, Peak Lending Team | tenby@coloradomortgageplanner.com | Yes - real find |
| Esoteric Auto Detail | contact@esotericdetail.com | Generic inbox, not the named owner |
| Yvonne Quijano, Guarisco Cordes & Lala | `****@gctaxlaw.com`, format is first@ | Pattern only |
| Christopher Stoll, Audioflare | `c***@audioflare.com` | Pattern only |
| Noreen Tracy, Regal Associates | nothing | No |
| Cj Conway, Esoteric | nothing (rate limited) | No |

## What this means

Roughly **one verified named email per 13 attempts.** At 279 contacts that is
300-800 calls for perhaps 20-30 addresses, so it is not worth running across the
whole list.

Two things make it worse than the raw rate suggests:

1. **Most search results lead back to ZoomInfo, RocketReach or LeadIQ**, which show
   the address masked (`c***@audioflare.com`). That confirms the domain's format
   but not the address - and it is the same data we would be paying ZoomInfo for
   anyway, so it is not an independent source.
2. **What is publicly findable is usually the generic inbox** (contact@, info@),
   not the owner or office manager we actually identified. A generic inbox is a
   much weaker outbound target.

## Where it genuinely earned its place

The Tenby Dahman find is the argument for keeping this in the toolkit. ZoomInfo
missed him because he operates under a second brand (coloradomortgageplanner.com)
that does not match the company domain on his record. No amount of pattern
guessing against peaklendingteam.com would ever have produced that address.
That failure mode - person trades under a different name than the ZoomInfo
company record - is where public search beats a database, and it is worth a
targeted search on high-value contacts rather than a blanket sweep.

## The cheaper free win found along the way

18 of the 73 contacts with no email on file sit at a company where we either
already hold a verified address, or will after enriching a colleague. Their
domain's format is therefore known for free, no web calls needed. Listed in
`pattern-derivable.tsv`. The remaining 55 are in `no-pattern-available.tsv`.

## Caution on derived addresses

A guessed address is not a verified one. Sending to guesses that bounce damages
the sending domain's reputation, which is a real cost to an outbound programme
rather than a free upside. Derived addresses should be run through a verifier
before they enter a sequence, or sent to in a small separate batch away from the
main sending domain.
