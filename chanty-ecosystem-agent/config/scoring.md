# Organization Scoring

0-100. The rubric is implemented in `scripts/eco/scoring.py`; this file explains
what each sub-score means so scores stay comparable between runs.

An unscored dimension is 0, not an average. Missing evidence lowers the score,
which is the intended behaviour: we should not reward organizations we failed to
research.

## Audience fit (25)
- `smb_concentration` 0-5. How much of the audience is actually small business.
- `employee_size_fit` 0-5. Are those businesses in the 5-200 employee range where
  a team chat tool gets bought.
- `team_communication_need` 0-5. Do they have teams that coordinate, or are they
  sole operators.
- `vertical_relevance` 0-5. Do the verticals map to shift work, field work,
  distributed teams, or otherwise messy communication.
- `geographic_reach` 0-5. Local, regional, national.

## Distribution power (25)
- `email_newsletter` 0-5
- `webinars_workshops` 0-5
- `events` 0-5
- `member_client_communication` 0-5
- `community_directory_repeat_exposure` 0-5

Score distribution on evidence of the mechanism existing and being used, not on
whether they have a website.

## Partnership compatibility (20)
- `technology_sponsors` 0-5. Do they already take technology sponsors.
- `member_benefits` 0-5. Is there a formal benefits program.
- `educational_partnerships` 0-5. Do outside educators present to their audience.
- `referral_structure` 0-5. Do they refer vendors, or is that culturally off-limits.

## Timing (15)
- `upcoming_event` 0-5
- `current_initiative` 0-5
- `leadership_or_program_change` 0-5

Timing points decay with the signal. A 6-month-old conference is not timing.

## Strategic value (15)
- `multi_chapter_national_leverage` 0-5
- `potential_seat_volume` 0-5
- `lookalike_potential` 0-5

## Bands
| Score | Priority |
|---|---|
| 90-100 | STRATEGIC |
| 80-89 | TIER 1 |
| 65-79 | TIER 2 |
| 50-64 | NURTURE |
| 0-49 | ARCHIVE |

A band is a queue, not a permission. Hard gates still decide who can be contacted.
