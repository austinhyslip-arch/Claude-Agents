# Lists, ICP and the buying power score

## Structure

Lists are cut by industry first, then by region, then by list type. Region means US time
zone, because the send window depends on it.

```
<industry> / <region> / Personal
<industry> / <region> / Agent
```

Regions: `ET`, `CT`, `MT`, `PT`. Alaska and Hawaii records keep their real time zone on the
record and sit in the `PT` list, with their send window calculated from the real zone rather
than from Pacific.

**Personal list** is the higher size and buying power accounts. Austin contacts these
directly. The agent still sources, scores, researches and drafts for them, it just never
queues them for its own sending.

**Agent list** is the smaller accounts. The agent handles these end to end, up to the point
of staging, where Austin still presses send.

Which list an account lands on is decided by the score below. It is not assigned by hand. If
a score puts an account somewhere that looks wrong, that is a signal the scoring needs
recalibrating, so raise it rather than overriding one record quietly.

## Weekly targets

Healthcare, 100 per week per list. Default regional split, adjustable:

| Region | Personal | Agent |
|---|---|---|
| ET | 40 | 40 |
| CT | 25 | 25 |
| MT | 10 | 10 |
| PT | 25 | 25 |

Every other vertical is 15 to 20 per week per list, and paused until win data lands.

## Healthcare ICP

Chanty sells team chat and task management to organisations whose staff are mostly not at a
desk. In healthcare that means multi-site outpatient groups where the clinical and front
office staff are on shift, on their feet, and frequently without a work computer or a work
email address.

**In scope**

- multi-site primary care and family medicine groups
- dental groups and DSOs
- urgent care chains
- home health and home care agencies
- behavioral and mental health groups
- physical therapy, chiropractic and rehab groups
- veterinary groups
- imaging and diagnostic centres
- med spa and aesthetics groups
- long term care and assisted living operators

**Out of scope for now**

- solo practices and anything under roughly 10 staff, since there is no coordination problem
  to solve yet
- large integrated health systems, which buy through procurement on a cycle this motion does
  not fit
- hospitals as an entity, though an individual service line inside one can qualify
- anyone already flagged `Do Not Contact`

**Personas to look for**, in rough order of how well they convert a first touch:

`ops-manager`, `owner-operator`, `frontline-supervisor`, `hr-people`, `it-security`,
`clinical-lead`, `finance`.

Practice managers and operations leads feel the pain daily and can usually get a meeting
booked without a committee. Go there first at smaller accounts. At larger ones, map the
committee with `persona-mapping-framework` and pick the entry point rather than the title
with the biggest name on it.

## Buying power score

Twelve points. Score every account. The score drives the split and the sort order inside
each list.

**Size, 0 to 4** (employee count estimate, always tagged as an estimate)

| Estimate | Points |
|---|---|
| under 10 | 0, and usually out of scope |
| 10 to 24 | 1 |
| 25 to 74 | 2 |
| 75 to 199 | 3 |
| 200+ | 4 |

**Footprint, 0 to 3** (sites or locations)

| Sites | Points |
|---|---|
| 1 | 0 |
| 2 to 4 | 1 |
| 5 to 14 | 2 |
| 15+ | 3 |

**Growth, 0 to 2**

- 1 point for open roles posted in the last 60 days
- 1 point for a new location opened or announced in the last 12 months

**Structure, 0 to 2**

- 1 point for a named operations, IT or HR leader findable on their own site
- 1 point for a formal leadership page, which usually means budget sits with someone
  identifiable rather than with whoever is on shift

**Fit, 0 to 1**

- 1 point for clear evidence of a distributed or shift-based workforce, for example multiple
  locations under one brand, posted shift roles, or a staff directory split across sites

### Split threshold

| Score | List |
|---|---|
| 7 to 12 | Personal |
| 3 to 6 | Agent |
| 0 to 2 | Excluded, with the reason recorded |

**These thresholds are provisional.** They were set from the ICP description, not from
Chanty's closed-won data. Once Austin provides real win data, run
`icp-lookalike-expansion` against it and recalibrate. Say in the run summary that the
thresholds are still provisional whenever a list build is delivered.

## Employee count estimates

Never present an estimate as a fact. Record the basis alongside it:

- `site-count`: sites multiplied by a typical staff figure for that setting
- `linkedin`: headcount shown on their company page, which usually undercounts frontline
  staff at multi-site healthcare operators, so treat it as a floor
- `directory`: a practice directory or state registry listing
- `stated`: a number they publish themselves, for example "over 300 employees" on an about
  page
- `guess`: anything else, and a `guess` basis caps the size score at 2

## Record checklist

A contact is not list-ready until it has all of these:

- [ ] company name and domain
- [ ] person name and title as written on their own site
- [ ] persona tag
- [ ] email, with its status set to `verified`, `catch-all` or `unverified`
- [ ] phone, main line is fine
- [ ] employee count estimate with its basis
- [ ] site count
- [ ] time zone, or `unknown` and flagged
- [ ] buying power score with the component numbers in the notes
- [ ] list assignment
- [ ] sourcing tag
- [ ] trigger with source URL and date, or empty

An incomplete record can sit in Attio. It cannot enter the send queue.
