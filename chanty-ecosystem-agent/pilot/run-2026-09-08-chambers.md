# Run log: /eco-run chambers 20, 2026-09-08

Autonomy level 2. Draft, don't send. Nothing was sent and no enrichment provider
was called.

## Result

    NEW                 18 (19 organizations in the store, including the KC chamber from the 09-07 test)
    QUALIFIED           14
    TIER 1              0
    TIER 2              4   Grand Rapids, Des Moines, Asheville, Boulder
    NURTURE             8
    ARCHIVE             6
    PUBLIC CONTACTS     7
    EMAIL_NOT_PUBLIC    6
    SIGNALS             2
    GMAIL DRAFTS        6
    HUMAN REVIEW        1   Greater Des Moines Partnership, tier A
    ENRICHMENT USED     0

## Drafts written into Gmail

| Organization | Contact | Offer | Observation behind the message |
|---|---|---|---|
| Grand Rapids Chamber | Rick Treur, Director of Talent & Leadership | Workshop | Standalone morning workshops for members, incl. 29 Sept Talent and HR session |
| Lincoln Chamber | Nate Ehmke, Event and Program Director | Event participation | The HIVE small business coffee meetup, next session 24 Sept |
| Greater Sioux Falls Chamber | Carly Reinders, Director of Member Experience | Workshop | Business Education is a named program |
| Asheville Area Chamber | Amy Jackson, Sr Director of Member Engagement | Workshop | Smart Series has 2026 sessions listed |
| Springfield Area Chamber (MO) | Parker Reid, VP of Membership | Member resource | Member News plus several other newsletters |
| Boulder Chamber | Maye Cordero, Sr Director of Events & Programs | Workshop | Business Growth Network is a standing group |

Every observation is A-level evidence read from the organization's own site, with
the URL stored on the draft.

## Stopped at EMAIL_NOT_PUBLIC

The right person was identified at each of these and no public email exists for
them. No address was constructed and no enrichment was used.

| Organization | Person identified | What is public instead |
|---|---|---|
| Boise Metro Chamber | Sandy Anderson, VP Member Services | Contact form, public phone |
| Chattanooga Chamber | Ben Cairns, VP Membership | Public phone only |
| Greater Spokane Inc | Maddie Johnson, Event & Engagement Manager | Obfuscated inbox, contact form |
| Wichita Regional Chamber | Angie Elliott, Chief Program Officer | Staff emails are icon links, general inbox, phone |
| Greater Green Bay Chamber | Marsha Brabant, Membership Director | membership@ inbox, phone |
| FMWF Chamber | Setareh Campion, Director of Programs | info@ inbox, phone |

Wichita is the interesting one. The staff emails are on the page but rendered as
icon links rather than text, so there is no address to read. The pattern is
guessable from other chambers and that is exactly why the rule exists.

## Escalated

**Greater Des Moines Partnership.** States 7,200 regional chamber members and
more than 400 investors, describes itself as the second-largest regional chamber
in the nation, and sits alongside affiliate chambers. Tier A, so no contact was
approached. This is a human-led conversation.

## Two things the run changed in the system

**The tier heuristic had a hole.** Des Moines scored 5/5 on multi-chapter
leverage but came out Tier C, because `partner_tier` only looked at the chapter
and parent fields and Des Moines has neither. Leverage that lives in the score
was invisible to the tier. Fixed: `partner_tier` now reads the strategic_value
sub-score, and a leverage of 4 or 5 forces Tier A. Three tests cover it.

**The outreach schema had no field for a provider-side draft id.** Writing the
Gmail ids in was rejected by the validator, which is the correct outcome for an
ad-hoc field. Added `external_draft_id` and `external_thread_id` properly.

## Organizations that did not make it in

Ann Arbor, Knoxville, Greenville SC and Naperville's staff page returned 404s or
deprecated redirects on the pages checked. Naperville and Columbia MO were
verified from their about pages and are in the store; the other two are not,
because an organization that cannot be verified on its own site does not get a
record.

score.org still returns 403 to automated fetches, same as on 09-07.

## Revision, same day

Austin's review of the six drafts: the writing is right, but the messages have to
say we join learning sessions remotely.

That is a standing constraint rather than a wording fix, so it went into policy
rather than into six files. `delivery_constraints` in `config/policy.json` now
records that live sessions are remote only and that there is no travel budget,
and `gates.check_delivery_disclosure` blocks a workshop or event participation
draft that does not say so. `gmail.build` refuses to produce a payload for one,
so the constraint is enforced before a message can reach a mailbox rather than
after.

Five drafts were revised and updated in Gmail. Springfield was left alone: it
offers a written resource, so there is no live delivery to disclose and the gate
correctly does not apply.

The Lincoln draft changed more than the others. The HIVE is a coffee meetup, and
a remote speaker does not really work at a coffee meetup, so the message now says
that plainly and points at the Face the Chamber slot instead. Better to name the
mismatch than to let them discover it.
