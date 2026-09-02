# Run log

Newest first. Every run of every mode gets an entry, including runs that produced nothing.

Entry format:

```
## YYYY-MM-DD | <mode>
- Window / scope:
- Sourced: <n> total (free-web-search <n>, paid <n>)
- Scored: Personal <n>, Agent <n>, Excluded <n>
- Staged: <n> ready, <n> held (<reasons>)
- Sent by Austin: <n>
- Replies: <n> (<classification breakdown>)
- Attio: <records created / updated / flagged>
- Waiting on Austin: <credit batches, uncertain matches, candidate stage changes>
- Notes:
```

---

## 2026-09-02 | Test run, list build + draft

- Window / scope: Healthcare, Central time zone, deliberately small. Search-only sourcing.
- Sourced: 8 accounts examined, 6 written to Attio (free-web-search 6, paid 0)
- Scored: Personal 2, Agent 4, Excluded 2 (not written to Attio, listed below)
- People created: 4 (3 at Chord, 1 at Performance Therapy)
- Staged: 0 ready, 2 held (both for no verified email)
- Sent by Austin: 0
- Replies: 0
- Attio: 2 lists created, 6 companies, 4 people, 6 GTM account notes
- Credits spent: **none**
- Waiting on Austin: gap batch decision, the Fast Pace scope question, the Family Practice
  ownership check, and where Agent 2 reads shared data from

### Written to Attio

| Account | Score | List | People | Email found |
|---|---|---|---|---|
| Chord Specialty Dental Partners | 11 | Personal | Cruse, Brent, Overstreet | none |
| Fast Pace Health | 10 | Personal | none | none |
| Performance Therapy Institute | 5 | Agent | Cashman | none |
| MPOWER Physical Therapy | 4 | Agent | none | none |
| Nashville Healthcare Center | 4 | Agent | none | none |
| Family Practice Associates | 3 | Agent | none | none |

### Scored out, not written

- **Get Better Physical Therapy**, Brentwood TN. Score 2 (size 1, footprint 0, structure 1).
  Single site, so no coordination problem to sell into. Kate Glenn is the office manager if
  it is ever wanted.
- **Nashville Family Medical Clinic**, single site, 18 years trading. Score 1.

Excluded accounts were left out of Attio on purpose. Writing them in would fill a new CRM
with records nobody is going to work. They live here instead. Say if that is the wrong call.

### What the run actually proved

1. **No email addresses, for anyone.** Six accounts, four named people, zero addresses. This
   is the finding. Search returns names, titles, phone numbers and addresses, but the email
   almost always sits on a contact page the agent cannot open from this environment. The
   pipeline runs end to end and then stops at the last step.
2. **The scoring works and has one hole.** The spread came out sensible, with real separation
   between a 1,000-employee DSO and a four-office PT practice. But the score has no upper
   bound, so Fast Pace Health at 300+ sites lands on the Personal list on size alone, when
   the ICP says buyers that size purchase through procurement and are out of the motion.
3. **`guess` basis did its job.** Family Practice Associates got a capped size score because
   the employee number was a guess, and it sorted last as a result.
4. **The one-per-company rule bit immediately.** Chord has four plausible contacts. Only one
   got a draft.
5. **Third-party directories are not sources.** Names surfaced for Fast Pace through a data
   aggregator with unclear titles. No records created from them.
6. **Two accounts need a human check before outreach**, both flagged in their notes: Fast
   Pace on scope, Family Practice Associates on whether it is HCA-owned.

### 2026-09-02, second pass: phones and stage alignment

- Main lines found for all 6 accounts, free web search, no credits spent
- Phones written to the 4 person records and to every `GTM account` note
- **Companies has no phone attribute**, standard or custom, so there is nowhere on a company
  record to put a main line. That is why they live on people and in notes.
- Fast Pace Health address corrected from 550 to 6550 Carothers Pkwy. The first search gave
  the wrong number, a second pass with several corroborating sources gave the right one.
  Worth remembering that one search result is not a source.
- Attio enriched the Fast Pace record on its own: categories, LinkedIn, Twitter, an ARR band
  and a foundation date, none of it asked for. Useful, and worth not duplicating by hand.
- **Austin's custom fields appeared on people mid-run**: `Stage` (11 statuses) and `Who
  Contacted`. The repo's invented status ladder has been replaced with his throughout. All
  four contacts set to `Not Contacted`.
- Three gaps this surfaced: no Do Not Contact status, no company-side touch fields, and a
  ladder that now implies a follow-up cadence which does not exist yet.

### 2026-09-02, third pass: exhaustive free sweep before any paid lookup

Ran every free source on all six accounts. Six searches, no credits spent.

**Found, all published, none assembled**

| Address | Account | Source |
|---|---|---|
| marketing@chordsdp.com | Chord | company press releases |
| justin.olson@fastpacehealth.com | Fast Pace | press releases, CMO |
| Amy.Hornsby@fastpacemedical.com | Fast Pace | older releases, different domain |
| jennm@performancepttn.com | Performance Therapy | practice directory |

**Press releases are the best free email source by some distance.** Media contact lines carry
a named person and a real published address, and every company that has ever announced
anything has one. That source was not in the original checklist and is now first on it.

**Two accounts disqualified, for nothing**

- Family Practice Associates of Southern Hills is HCA-owned through TriStar Medical Group.
  Confirmed, marked out of scope.
- Nashville Healthcare Center appears on Nashville General Hospital's site as one of its
  locations. Likely the same problem, needs confirming.

Two of six hospital-owned in a six-account test. Ownership now gets checked during sourcing
rather than after, because one search disqualifies an account before it can ever cost a
credit.

**The paid batch went from seven contacts to one.** Free search plus disqualification did
that. The one left is Alayna Brent at Chord, and even that is worth holding until page
fetching is fixed.

**Corrections found along the way**

- MPOWER has five locations, not three. Rescored 4 to 5.
- Nashville Healthcare Center main campus is 1818 Albion St, not 1810. Bordeaux has its own
  line, (615) 562-4612.
- Fast Pace street number is now unresolved across three sources: 550, 6550, 6650. Left at
  6550 rather than churning the record on a fourth guess.
- Performance Therapy has three separate disagreements with the record: domain, phone and
  street number. One phone call settles all three for nothing.

**Two limits worth recording**

1. Attio cannot remove a record from a list through this connection, so a disqualified
   account sits in its working list until someone pulls it by hand.
2. A found address does not make someone the right contact. Fast Pace's CMO is a media
   contact, not a person who feels a shift-coordination problem.



---

## 2026-09-02 | Setup
- Agent built. No list build, no sourcing, no sends.
- Buying power thresholds are provisional and need recalibrating against Chanty closed-won
  data before the Personal / Agent split can be trusted.
- Non-healthcare verticals blocked pending that same win data.
- Attio schema, Calendly to Attio connection and Gmail sync all still need verifying against
  the live workspace. See SETUP.md.
