# Run log

Append one entry per run, newest at the top. This is the memory that stops repeat runs from
re-sourcing the same market from scratch and tracks how the funnel narrowed each time.

Entry format:

```
## YYYY-MM-DD — <scope, e.g. "Family medicine, Little Rock AR metro">
Companies considered: N
Excluded (part of a large system/chain): N
  - <Company> — <signal that excluded it>
Included, Pass: N | Borderline: N | Unclear independence: N
Contacts found: N (Matched title: N, Flagged title: N)
Already in Attio: N companies, N people
Needs paid tool (email): N rows

Sourcing notes: <which free sources worked, whether Apollo fallback was needed and why,
any blocked domain / egress issue hit>

Spreadsheet: state/lists/healthcare-prospects-YYYY-MM-DD.xlsx
Pushed to Attio: not yet / yes on YYYY-MM-DD (N companies, N people created)
```

---

## 2026-09-02 — Healthcare, any specialty, nationwide (requested: 100 contacts)
Companies considered: 73 (individually free-source-verified)
Excluded (part of a large system/chain): 3
  - Progressive Dental Concepts — DSO managing a network of branded dental practices
  - Anderson Longevity Clinic — franchise model, contact was a multi-unit franchisee not the founder
  - SunState Medical Specialists — part of the OneOncology national oncology network
Included, Pass: 60 | Borderline (size): 3 | Unclear independence: 7
Contacts found: 70 (Title Match: all Matched — titles came directly from Apollo's title-filtered
  search, so nothing needed fuzzy-flagging this run)
Already in Attio: 0 companies, 0 people (workspace has 16 company / 4 people records, mostly
  demo data plus an unrelated small Nashville-market batch from a different run; no domain or
  name overlap with this run's candidates)
Needs paid tool (email): 13 rows (no confirmed domain, or no last name resolved via free
  sources to build a first.last guess)

Sourcing notes: Free-source company discovery alone could not reach nationwide volume in one
session, so — per Austin's explicit confirmation — Apollo's organization and people SEARCH
endpoints (not reveal/enrich) were used for discovery: apollo_mixed_companies_search and
apollo_mixed_people_api_search, filtered to NAICS 6211/6212/6213 (physician/dental/other health
practitioner offices), US locations, employee ranges 1-10/11-50, and target titles. Apollo masks
last names in search results without a paid reveal, so every contact went through a follow-up
free web search to recover the real full name, confirm the company's domain, and check for
independence red flags (parent org, franchise/DSO/network language, known-chain naming).
No Apollo/Hunter email reveal or verification was used anywhere in this run — every email is
either free-source-found (rare) or a best-guess pattern with a confidence rating, per the
no-paid-lookup-without-confirmation rule. 3 companies newly confirmed as chains/DSOs/franchises
were added to known-health-systems.md.

Housekeeping (unrelated to this run): found an existing Attio company record "Family Practice
Associates of Southern Hills" whose own description says it was disqualified as HCA-owned and
is "still sitting in the Agent list, needs removing by hand" — flagged to Austin, not touched.

Spreadsheet: state/lists/healthcare-prospects-2026-09-02.xlsx
Pushed to Attio: not yet

Notes: Delivered 70 of the requested 100 contacts. Per-contact free-source verification
(independence check + name recovery) is the bottleneck, not company discovery — Apollo can
surface far more than 100 candidates instantly, but each one needs individual checking to be
trustworthy. Rather than pad the list with unverified rows, this run stopped at a batch that's
fully vetted and offered to continue toward 100 in a follow-up run if Austin wants more volume.

---

## 2026-09-02 (continued) — Austin's Unclear/Borderline resolution, via Agent 2

Not a new sourcing run. Austin handed the 2026-09-02 spreadsheet to the outreach-drafting
session and asked it to resolve the 10 flagged rows before drafting. Recorded here so the
next list-building-agent run doesn't re-flag the same names.

**Excluded (3), added to `known-health-systems.md`:**
- Athens Neurological Associates — on Piedmont Healthcare's own provider directory under
  Piedmont branding, not a referral listing.
- MidLantic Urology — acquired by The Urology Group / Solaris Health, Dec 2020; also
  Urology Alliance.
- Premier Orthopaedics and Sports Medicine — no independent entity by this name found
  anywhere; every plausible match nationally (PA, OH) is system-affiliated. Excluded on
  identity grounds, not just ownership.

**Confirmed independent, kept (4):**
Children's Eye Care PC Michigan, Nirschl Orthopaedic Center, The Dermatology Clinic PLLC,
GRiN Pediatric Dentistry & Orthodontics (weakest confirmation of the four — no system
branding found, but ownership structure not independently verified beyond that).

**Size confirmed, kept (3):**
P4 Physical Therapy (51-200 staff per multiple sources, right at the 200-line, keep),
St. Louis Heart and Vascular (86-90 staff), RiverRun Health (12-13 staff — bucket corrected
from the sheet's tentative 51-250 down to 11-50).

**Result:** 67 of the original 70 companies are qualified and clean. 3 excluded.

All 70 original contacts' email addresses, verified or not, remain governed by
`.claude/gtm/sourcing-and-credits.md` regardless of this resolution — qualification and
verification are separate gates. See `references/enrichment.md`.

---

_No sourcing runs before the one above this entry._
