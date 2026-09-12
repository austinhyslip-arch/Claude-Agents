# Seen entities

Every entity this agent has already surfaced, across all runs. Checked before any
record is written so the same directory page does not turn into the same candidates
every morning.

The container is rebuilt on every run, so this file is the only dedupe memory that
survives. Append to it and push it at the end of every run.

Format: one row per entity.

| domain | company_name | state | vertical | first_seen | outcome |
|---|---|---|---|---|---|
