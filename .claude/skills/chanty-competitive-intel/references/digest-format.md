# Digest format

Every run produces **one HTML file** built from `digest-template.html`, sent as an **email
attachment**. The email body stays short. Gmail strips or mangles the CSS this design
depends on — rotated stamps, layered borders, the paper ground — so the attachment is what
preserves the design when Austin opens it in a browser.

## The file

- Build from `references/digest-template.html`. Keep its structure; replace the content.
- Name it `chanty-competitive-briefing-YYYY-MM-DD.html` (the run date).
- Must stay self-contained — no external CSS, fonts, images, or scripts. It gets opened
  from a mail attachment, sometimes offline.
- Save every digest to `state/digests/` and commit it, whether or not the send succeeded.
  That directory is the archive; the run log points into it.

### Filling the template

| Token | What goes in |
|---|---|
| `{{RUN_TYPE}}` | `Weekly` or `On-Demand` |
| `{{DATE_RANGE}}` | `Aug 18 – Aug 24, 2026` |
| `{{COMPILED_DATE}}` | The run date |
| `{{FLAG_COUNT}}` | Number of Big Stuff items, or `none` |
| `{{COMPETITOR_COUNT}}` | How many competitors have anything this run |
| `{{SOURCES_USED}}` | The sources actually worked this run — not the aspirational list |
| `{{PRICING_SNAPSHOT}}` | Tier 1 + Tier 2 per-seat prices, for diffing next week |
| `{{CAVEATS}}` | Anything unreachable, unverified, or thin. Empty string if genuinely clean. |

Block-level rules:

- **`.flag`** — one per Big Stuff item, in the `#flagged` section, scored 4+ on the rubric.
  Title is `<Competitor> — <what happened>`. First `<p>` is what happened with the numbers
  in it; `.why` is why it moves a Chanty sales conversation. Delete the whole `#flagged`
  section when nothing qualifies, and say so in the colophon instead.
- **`.flag.is-unconfirmed`** with the `.stamp.unconfirmed` variant — for an item worth
  knowing that fails the two-source rule. Say plainly it is not sales-usable yet.
- **`.comp`** — one per competitor with complaints, inside `#complaints`. Each `<li>` opens
  with a `.kind` label (`Pricing` or `Feature`), then the complaint in one or two sentences
  leading with the substance, then `.src` with source, date, and link. Drop competitors
  with nothing; never ship an empty block.
- **`.tabs`** — one `.tab` per `.comp` block plus `All`. The `data-target` must match the
  `.comp` id. Tabs are progressive enhancement: with JS off, every block stays visible.
- **`.sticky`** — the watchlist note. Discovery-month runs only; delete it otherwise.
  New Tier 3 promotions, and any names moved to dormant.
- **`.house`** — Chanty mentions. Keep this section even when empty; one line saying no
  mentions turned up is a real finding.

Before sending, open the file and confirm no `data-sample` attributes and no `{{TOKENS}}`
survive. Either one shipping to Austin means the run failed, not the template.

## The email

**Subject lines**

- Weekly: `[Weekly] Competitive Digest — Aug 24, 2026`
- On-demand: `[On-Demand] Competitive Check — last 24 hours`
- Discovery month: append ` + Discovery`
- Flags present: append ` — N flags`

Example: `[Weekly] Competitive Digest — Aug 24, 2026 + Discovery — 2 flags`

**Body** — short, plain text. Two parts:

1. One line: what is attached and the window it covers.
2. If Big Stuff turned up, the flag headlines as one-line bullets, above everything else,
   so they are visible without opening the attachment. If nothing flagged, one line saying
   so.

```
Weekly competitive digest attached, covering Aug 18-24.

2 flags this week:
- Notion — AI features moved behind Business ($20/seat), effective Aug 11
- Slack — third multi-hour outage this month (Aug 21)

Open the attachment in a browser — the formatting doesn't survive Gmail's renderer.
```

No preamble, no sign-off. Do not restate the complaint sections in the body; that is what
the attachment is for.

## Send path, and what to do when it fails

1. **Attach the HTML file** to the email. This is the intended path.
2. If the Gmail tool available in the session **cannot attach files**: upload the HTML to
   Google Drive, send the body with a link to it, and say in the body that it is a link
   rather than an attachment because attachment support was unavailable.
3. If neither works: send the body with the digest's Big Stuff and complaint text inline as
   plain text, and say the formatted version is committed at `state/digests/<file>`.
4. If Gmail is unavailable entirely: commit the file, and report the failure and its reason
   in the run summary. Never let a run end with the digest neither sent nor archived.

Whichever path was used, record it in `state/run-log.md`.
