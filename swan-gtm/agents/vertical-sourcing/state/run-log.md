# Run log

One row per execution. Keep the last 30 runs, trim older rows.

Columns: date, digest send timestamp, records found per source, records qualified per
vertical, duplicates skipped, records held for review, API calls consumed, remaining
pool estimate, any source that failed.

The send timestamp doubles as the heartbeat. If two consecutive weekdays carry no
successful send, escalate with a separate alert email.

| date | sent (Central) | mfg qualified | muni qualified | dupes skipped | held | google queries | pool estimate | failed sources |
|---|---|---|---|---|---|---|---|---|
