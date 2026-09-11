# Sent log

Every email this agent has sent. Written before moving to the next recipient, never
batched at the end, so a crash mid-block cannot double-send.

Format: date | time + tz | block | batch | touch | recipient | company | address | subject |
subject variant (A control, B price) | address source | Attio person id

The variant column is the price test in `references/copy.md`. The address source column is
what makes a bounce traceable to the provider that supplied it.

---

_Nothing sent. The agent has not run._
