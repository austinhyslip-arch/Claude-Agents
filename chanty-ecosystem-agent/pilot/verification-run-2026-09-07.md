# Live Verification Run, 2026-09-07

One real organization, taken through discovery, dedupe, research, scoring and the
qualification gate against live web sources. Purpose was to check the pipeline
behaves on real pages, not fixtures. No contact was searched for, nothing was
drafted, nothing was sent, nothing was written to Attio.

## Organization

Greater Kansas City Chamber of Commerce, kcchamber.com. Record ID ORG-ZH9POHSH.

Five pieces of A-level evidence, all from the organization's own site: the two
named member publications, the five sponsorship investor tiers, the Centurions
professional development curriculum and Small Business Celebration series, the
stated $795 basic membership, and the named signature events.

## What the run showed

**Dedupe held.** Re-submitting the same organization as "KC Chamber of Commerce"
with `http://kcchamber.com/about` matched the existing record on exact domain and
produced the identical ID. IDs are hashes of the identity seed, so rediscovery is
idempotent.

**Membership size stayed unknown.** No page checked states a member count, so
`audience_size` is null and `audience_confidence` is UNKNOWN. Any future message
to this organization cannot contain a member number, and the personalization gate
enforces that rather than trusting the writer to remember.

**Score 57, NURTURE, coverage 0.90.** Strong distribution (newsletters, events,
sponsorship, member benefits) pulled the score up. Two timing components were
left null because no dated upcoming event was visible, and null scored zero,
which is the designed behaviour. Padding those two components with a guess would
have moved this record into TIER_2 on nothing.

**The gate failed for the right two reasons:** `credible_contact_identified` and
`partnership_hypothesis_exists`. No contact has been looked for and no
opportunity record exists yet. The gate named both, so the next step is obvious.

## Two real-world conditions worth recording

**score.org returns HTTP 403 to automated fetches.** Both the homepage and
/about-us. This will happen with other organizations too. The correct response is
to record the organization as unverified and move on, not to fall back to a
search snippet and write it up as if it came from the source. D-level evidence
cannot support a claim in a message, so a 403 means the organization waits.

**kcchamber.com/events is an archive landing page with no dates.** Signature
events are named, but no scheduled dates are shown without clicking through to
individual calendars. So the events mechanism is recorded as present with an
A-level source, and the timing components are left unscored. Named events are
not the same as a dated signal, and the difference matters when writing "why
now".

## Commands run

    python3 -m eco add-org <json>
    python3 -m eco dedupe-check '{"organization_name":"KC Chamber of Commerce", ...}'
    python3 -m eco transition ORG-ZH9POHSH start_research
    python3 -m eco score ORG-ZH9POHSH <json>
    python3 -m eco transition ORG-ZH9POHSH qualify
    python3 -m eco gate ORG-ZH9POHSH
    python3 -m eco attio-plan ORG-ZH9POHSH
    python3 -m eco status

Ten audit entries were written. The record itself lives in `data/`, which is
gitignored: operational records and anything that could later hold a person's
contact details stay out of the repository.
