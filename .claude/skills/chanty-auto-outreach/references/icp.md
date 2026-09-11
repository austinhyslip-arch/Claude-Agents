# ICP, auto-outreach

Set by Austin on 2026-09-11: **50 to 100 employees, any industry.**

Wider than Agent 1's healthcare ICP on purpose. Agent 1 works healthcare and stages for
approval. This agent works the broad band and sends. They share Attio records, so the
double-touch checks in `send-policy.md` matter more than the targeting does.

## The band

| Estimate | Verdict |
|---|---|
| Under 50 | Out. Too small for a coordination problem worth paying to solve. |
| 50 to 100 | In. |
| Over 100 | Out of this agent's band. Score it for Agent 1 instead if it fits healthcare. |

Headcount is always an estimate. Record the basis, per `.claude/gtm/attio-schema.md`. A
`guess` basis near either edge of the band holds the contact rather than sending on it.

## What actually makes a good target inside the band

Headcount alone is a filter, not a fit. Chanty sells to teams whose people are not at a
desk, so inside the band prefer:

- multiple sites, depots, branches or territories under one business
- shift work, field work, drivers, warehouse, on-premise reps
- a workforce where a chunk of staff have no work computer and possibly no work email
- an operations, HR or office manager findable by name

Weak fits inside the band: single-office professional services where everyone already sits
in front of a laptop all day. They qualify on headcount and rarely feel the problem.

## Hard exclusions

Checked during sourcing, before any credit is spent, because this is where the last run
lost half its list.

- **Owned by a large group.** Hospital systems, national franchisors, roll-ups, PE
  platforms and corporate parents. Two of six accounts in the first test were
  hospital-owned, and a vet hospital that looked independent turned out to be NVA. One
  search answers it: `"<company>" owned by OR acquired OR "part of" OR parent company`.
- **Franchise locations** where the owner-operator is not the buyer.
- Anything already in `state/suppression.md`.
- Anything already worked by Agent 1 or Agent 2 inside the windows in `send-policy.md`.
- Companies with no distributed or shift-based workforce at all.

## Sourcing order

Free sweep first, per `.claude/gtm/sourcing-and-credits.md`. Press releases are the
strongest free source for a named address, then the company's own contact and team pages
now that page fetching works, then directories, then Facebook business pages.

Batch whatever is left and ask before spending. Apollo returned an extrapolated address on
a mismatched company the one time it was used for this, so treat provider output as a
candidate that still has to clear the gate, not as an answer.

## Records

Same fields as Agent 1, per `.claude/gtm/attio-schema.md`. `who_contacted` is
`Agent 3 (auto-send)` so the three agents stay distinguishable in the CRM.
