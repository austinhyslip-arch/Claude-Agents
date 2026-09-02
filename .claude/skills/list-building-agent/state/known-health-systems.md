# Known large health systems and chains

Running exclusion list for the independence check. A practice whose name matches one of
these (as a location/franchise, e.g. "HCA — Riverside Family Medicine") or whose site /
Apollo parent field names one of these gets excluded before the spreadsheet is built.

This list is seeded with well-known national and large regional systems and chains as a
starting point. Every run adds any newly confirmed system/chain it encounters, so this
should grow. Entries are grouped by specialty since "healthcare, any specialty" pulls in
different consolidators per vertical.

## Hospital systems (multi-specialty, general medical)
HCA Healthcare, Ascension, CommonSpirit Health, Providence, Trinity Health, Kaiser
Permanente, Advocate Health, Tenet Healthcare, Community Health Systems, Universal Health
Services, Mayo Clinic, Cleveland Clinic, Mass General Brigham, NYU Langone, Northwell
Health, Sutter Health, Intermountain Health, Baylor Scott & White, Banner Health, UPMC,
Sanford Health, Piedmont Healthcare, Tower Health, Penn Medicine, Premier Health (Dayton
OH region)

## Dental chains / DSOs
Heartland Dental, Aspen Dental, Pacific Dental Services, Western Dental, Smile Brands,
DECA Dental, Mortenson Dental Partners, MB2 Dental, Dental Care Alliance, Great Expressions
Dental Centers, Benevis, ClearChoice

## Vision / optometry chains
MyEyeDr, National Vision (America's Best, Eyeglass World), EyeCare Partners, Vision Source
(franchise model — check specific location's independence separately), Visionworks,
Warby Parker (retail, not applicable to practice model)

## Physical therapy chains
ATI Physical Therapy, Athletico Physical Therapy, CORA Physical Therapy, US Physical
Therapy (network of partly-owned clinics — verify per location), Select Medical /
NovaCare Rehabilitation, Confluent Health

## Dermatology chains
Forefront Dermatology, U.S. Dermatology Partners, Advanced Dermatology and Cosmetic
Surgery, Schweiger Dermatology Group, Dermatology Associates (multiple regional PE-backed
rollups use this generic name — verify by location/parent before excluding)

## Urgent care / primary care chains
American Family Care, MedExpress (UnitedHealth/Optum), CityMD (Summit Health), NextCare,
CareNow (HCA), Concentra

## Urology rollups
Solaris Health (parent of The Urology Group, Integrated Medical Professionals), Urology
Alliance / UA-supported networks — PE-backed physician practice management, same exclusion
logic as a dental DSO even though the practice keeps its original name after acquisition.

## Veterinary (out of scope per spec, kept here only if scope expands later)
Not applicable — spec scope is human healthcare.

## Confirmed during runs

- **Athens Neurological Associates** (athensneuro.com) — appears directly on Piedmont
  Healthcare's own provider directory (care.piedmont.org) under Piedmont branding, not as a
  referral/near-me listing. Confirmed 2026-09-02 via free web search (website language,
  signal 1). Excluded.
- **MidLantic Urology** (midlanticurology.com) — acquired by The Urology Group / Solaris
  Health, December 31 2020; also a member of Urology Alliance. Confirmed 2026-09-02 via
  free web search (M&A news, signal 4). Excluded.
- **"Premier Orthopaedics and Sports Medicine"** — not a single entity. Every plausible
  match found nationally is system-affiliated: Tower Health / Penn Medicine's "Premier
  Orthopaedic & Sports Medicine Associates Ltd" (Kennett Square / West Chester PA), and
  Premier Health's "Premier Orthopedics" (Dayton OH region). No independent entity by this
  name was found anywhere, including Alabama and New Jersey where the original record
  suggested a match. Confirmed 2026-09-02 via free web search (naming pattern, signal 2).
  Excluded on identity grounds — do not treat as one confirmed independent practice under
  this name in a future run without a city/state to disambiguate.
- **Progressive Dental Concepts** (progressivedentalconcepts.com) — dental support
  organization (DSO), Camp Hill PA, 51-200 employees, provides admin/ops support to a
  network of separately-branded dental practices. Confirmed 2026-09-02 via free web search
  (company's own site description).
- **Anderson Longevity Clinic franchise system** (alcfranchise.com) — franchise model;
  individual locations (e.g. the Phoenix, AZ territory) are run by franchisees, not the
  founding independent owner. Confirmed 2026-09-02 via free web search.
- **OneOncology** — national oncology practice management network. Absorbs formerly
  independent oncology practices (e.g. GenesisCare USA of Florida became SunState Medical
  Specialists under this network). Confirmed 2026-09-02 via free web search.

---

_Add new entries here as they're confirmed during a run, with a one-line note on the run
date and the signal that confirmed it (naming pattern / Apollo parent field / M&A news /
website language). Keep the format simple — a bullet under the right specialty heading is
enough; this file is read by pattern-matching, not parsed structurally._
