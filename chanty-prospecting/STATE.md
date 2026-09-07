# Chanty prospecting pipeline - working state

Last run: 2026-09-07

## Done

**19 confirmed-email contacts pushed to Attio.** Companies, people, and Pipeline
list entries all created. These were listed as "ready to push" in the handoff but
had never actually made it into Attio - verified by search before writing.

**Sub-20 band, intent pages 1-3 pulled and contact-searched.** 300 companies
covered out of ~565-620 total in the band (the total drifts between calls because
ZoomInfo intent data shifts through the day). Yielded 134 contacts with name,
title, company and domain but no verified email yet - see
`pending-enrichment.tsv`.

## Blocked

Clay's Work Email waterfall returns "Credits are exhausted for this workspace."
Nothing in `pending-enrichment.tsv` can be enriched through Clay until the
workspace is topped up. ZoomInfo `enrich_contacts` is the only other path and it
bills ZoomInfo bulk credits for every contact rather than just Clay's misses.

## Not started

- Sub-20 band, intent pages 4-7 (~265 more companies)
- 20-99 band (titles: Operations Manager, HR Manager, Office Manager,
  Practice Administrator)
- 100-499 band (titles: IT Manager, Director of Operations, HR Manager)
- Email sequence draft

## Notes for the next run

- Company ID 1334374792 (Allianz Commercial) is a large company miscategorised
  into the sub-20 band. It floods contact searches with dozens of "product owner"
  titles. Excluded. Same story for Yale School of Management, LP Building
  Solutions and Aquinas College.
- Capped at 2 contacts per company. Some small companies return 5-6 "owners"
  (Willow Creek III, Personal Travel, Shear Magic) and emailing all of them would
  read as spam.
- Titles containing "Product Owner", "Process Owner" or "General Sales Manager"
  are not buyer titles and were dropped.
- Travis Brown's email `travis@xtremelectrickc.com` sits on a domain one character
  off the company's actual `xtreme-electrickc.com`. Pushed to Attio as given but
  worth checking before anything is sent to him.
- `search_contacts` needs the deprecated `jobTitle` string with OR syntax.
  The `jobTitleList` array silently returns zero rows against multiple company IDs.
- `companyIdList` caps at 50 per call.

## Files

- `pending-enrichment.tsv` - 134 contacts awaiting an email, with ZoomInfo personId
  so they can be enriched without re-searching
- `sub20-company-ids-pages1-3.txt` - the 300 company IDs already contact-searched,
  so a resumed run can skip them
