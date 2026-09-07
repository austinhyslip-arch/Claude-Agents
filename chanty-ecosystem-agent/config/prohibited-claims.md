# Prohibited Claims

Anything in this file fails the draft and send gates. The check is implemented in
`scripts/eco/gates.py` and tested in `tests/test_claims.py`.

## Commercial
- Any discount, percentage off, or reduced rate
- "Special pricing", "member pricing", "exclusive rate", "preferred pricing"
- Free accounts, free seats, comped licenses
- Extended or custom trial lengths
- Commissions, referral fees, rev share, kickbacks, spiffs
- Exclusivity of any kind
- Any price other than $3 per seat

## Fabrication
- Invented customer counts, user counts, or growth figures
- Invented case study results or ROI numbers
- Invented partnerships ("we work with...") that are not in the partner records
- Invented endorsements from the organization or its members
- Invented urgency ("limited spots", "this month only", "closing soon")
- Invented events, dates, programs or initiatives
- Stating an estimated audience size as if the organization stated it

## Tone and integrity
- Generic flattery ("I love what you're doing", "big fan of your work")
- Fake familiarity or implied prior contact that did not happen
- Implying an existing relationship, endorsement or approval that does not exist
- Claiming the organization's members already use Chanty without a partner record
- Pressure language, false deadlines, guilt framing

## Regulated topics
- Security, compliance, HIPAA, SOC 2, GDPR, data residency, DPAs, insurance,
  legal terms. The agent does not answer these. It escalates them.

## Literal phrases the gate blocks

Generated from `gates._PROHIBITED_PHRASES`. A draft containing any of these,
in any casing, fails `eco draft-check` and `eco send-check`.

- `discount`
- `% off`
- `percent off`
- `special pricing`
- `special rate`
- `member pricing`
- `member rate`
- `exclusive pricing`
- `exclusive rate`
- `preferred pricing`
- `preferred rate`
- `reduced rate`
- `promo`
- `promotional`
- `free account`
- `free accounts`
- `free seats`
- `comped`
- `no charge`
- `extended trial`
- `custom trial`
- `commission`
- `referral fee`
- `rev share`
- `revenue share`
- `revenue-share`
- `kickback`
- `spiff`
- `exclusivity`
- `exclusive partner`
- `limited spots`
- `limited time`
- `this month only`
- `act now`
- `closing soon`
- `last chance`
- `big fan of`
- `love what you're doing`
- `i've been following you for years`
