# Attio schema

Attio is the system of record. If something happened to a contact and it is not in Attio,
it did not happen.

## Objects

**Company** (Attio standard object)

| Field | Type | Notes |
|---|---|---|
| Name | text | |
| Domain | domain | dedupe key, strongest match |
| Industry | select | `Healthcare`, `Real Estate`, `Frontline`, `Other` |
| Employee count (est.) | number | always an estimate, never presented as confirmed |
| Employee count basis | select | `site-count`, `linkedin`, `directory`, `stated`, `guess` |
| Sites / locations | number | main size driver in healthcare |
| Time zone | select | `ET`, `CT`, `MT`, `PT`, `AKT`, `HT`, `unknown` |
| Buying power score | number | 0 to 12, see the agent's `lists-and-icp.md` |
| List assignment | select | `Personal`, `Agent`, `Excluded` |
| Trigger | select | from `outbound-triggers-6` |
| Trigger source | url | no URL means no trigger |
| Trigger date | date | |
| Sourcing tag | select | `free-web-search`, `paid-apollo`, `paid-hunter`, `paid-clay` |

**Person** (Attio standard object)

| Field | Type | Notes |
|---|---|---|
| Name | text | |
| Company | record link | |
| Title | text | as written on their own site |
| Persona tag | select | see below |
| Email | email | |
| Email status | select | `verified`, `catch-all`, `unverified`, `bounced` |
| Phone (main line) | phone | company main line is fine |
| Time zone | select | inherited from company unless the person is clearly elsewhere |
| Outreach category | select | `Inbound`, `Postbound`, `Bridgebound`, `Outbound` |
| Bridge path | text | who or what the warm path is, empty when genuinely cold |
| Personalization angle | select | `authored-content`, `engaged-content`, `background`, `company-trigger`, `generic` |
| Personalization source | url | required unless the angle is `generic` |
| Status | select | see the status ladder below |
| Sourcing tag | select | same values as company |
| Last touch | date | |
| Owner | select | `Austin`, `Agent` |

## Persona tags

Set on the person, used by both personalization and copywriting. Keep the list short so it
stays useful.

- `owner-operator`: owns or runs the business, signs the cheque
- `clinical-lead`: physician lead, medical director, clinical director
- `ops-manager`: practice manager, office manager, operations
- `it-security`: IT, security, compliance
- `finance`: CFO, controller, finance lead
- `hr-people`: HR, people ops, staffing
- `frontline-supervisor`: supervises the non-desk staff who would actually use Chanty

## Status ladder

Order matters. Nothing skips a rung without Austin saying so.

`New` → `Queued` → `Sent` → `Replied` → `Meeting Booked` → `Contracting` → `Won` / `Lost`

Side statuses that do not sit on the ladder: `Bounced`, `Held`, `Do Not Contact`.

## Views

Delivery format Austin actually reads:

1. **Personal list, pinned at the top of the view.** Sortable by time zone. Contact info
   visible in the row without opening the record. Sorted by buying power score descending
   inside each time zone.
2. **Agent list, its own section underneath.** Same columns, same sort.

Split by industry first, then region inside it. One view per industry is enough while
healthcare is the only live vertical.

**Fallback.** If the Attio write path is unavailable, produce a spreadsheet with one tab per
list, named `<industry>-<region>-<personal|agent>`, carrying the same columns in the same
order. Say in the run summary that the fallback was used and why, and treat the spreadsheet
as temporary. It gets loaded into Attio once the write path is back.
