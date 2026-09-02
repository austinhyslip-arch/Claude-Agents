# Open approvals

Everything waiting on a decision from Austin. Check this file before raising anything new so
the same question does not get asked twice.

## Credit batches

Gaps that free web search could not fill, batched for one approval. Format:

```
### Batch <n> | YYYY-MM-DD | status: open | approved | declined
- Contacts: <n> (<list>)
- Missing: email <n>, phone <n>, both <n>
- Provider proposed: Apollo
- Est. lookups: <n>
- Contacts: <names and companies>
```

### Batch 1 :: 2026-09-02 :: status: open

- Contacts: 4 named people, plus 3 accounts with no named contact at all
- Missing: email for every one of them. Phones were found for most.
- Provider proposed: Apollo, `apollo_people_bulk_match`, one call for the batch
- Estimated cost: roughly 4 to 7 lead credits
- Apollo balance: 135 lead credits, cycle ends 2026-09-16
- Balance if approved: about 128 to 131

| Person | Company | List |
|---|---|---|
| Alayna Brent, COO | Chord Specialty Dental Partners | Personal |
| Todd Cruse, CEO | Chord Specialty Dental Partners | Personal |
| Amy Overstreet, CHRO | Chord Specialty Dental Partners | Personal |
| Kelly Cashman, Office Manager | Performance Therapy Institute | Agent |

Also unnamed: MPOWER Physical Therapy, Nashville Healthcare Center, Family Practice
Associates all need a contact found before anything can be drafted.

**Worth reading before approving.** Spending here fixes four contacts. It does not fix the
cause, which is that the agent cannot open a company's contact page from this environment.
Open that up and most of these are free. Approve this batch if you want the test to run all
the way through a real send, otherwise the better move is to fix egress first.

## Uncertain matches

Possible duplicates that were not merged. Both record links plus what makes them ambiguous.

_None open._

## Candidate stage changes

Deals that look like they moved past `Meeting Booked` based on email content. These wait for
confirmation. Include the quote that prompted it.

_None open._

## Scope questions from the 2026-09-02 run

1. **Fast Pace Health, 300+ sites, scored 10 and landed on the Personal list.** The ICP
   excludes buyers who purchase through procurement. Does the score need a ceiling, or an
   enterprise exclusion rule? Recommend a rule: over roughly 50 sites or 1,000 employees,
   flag rather than route.
2. **Family Practice Associates may be HCA-owned.** A TriStar Medical Group page carries the
   same address. If it is HCA, it is out of scope. Needs one check.
3. **Excluded accounts were kept out of Attio.** Two scored below 3 and were logged in the
   run log instead. Confirm that is the behaviour wanted.

## Held emails needing input

Usually an unknown time zone or an unverified address. The queue holds them, this is the
list of what would unblock them.

_None open._
