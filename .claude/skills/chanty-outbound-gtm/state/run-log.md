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

---

## 2026-09-02 | Setup
- Agent built. No list build, no sourcing, no sends.
- Buying power thresholds are provisional and need recalibrating against Chanty closed-won
  data before the Personal / Agent split can be trusted.
- Non-healthcare verticals blocked pending that same win data.
- Attio schema, Calendly to Attio connection and Gmail sync all still need verifying against
  the live workspace. See SETUP.md.
