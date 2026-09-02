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
Sanford Health

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

## Veterinary (out of scope per spec, kept here only if scope expands later)
Not applicable — spec scope is human healthcare.

## Confirmed during runs

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
- **UroPartners** — large Chicago-area urology consolidator. "Urology Specialists, S.C."
  in Chicago is one of its branded locations (confirmed via uropartners.com listing the
  same address/phone). Watch for other same-city urology group names sharing this pattern.

---

_Add new entries here as they're confirmed during a run, with a one-line note on the run
date and the signal that confirmed it (naming pattern / Apollo parent field / M&A news /
website language). Keep the format simple — a bullet under the right specialty heading is
enough; this file is read by pattern-matching, not parsed structurally._
