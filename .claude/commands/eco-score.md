---
description: Score or rescore organizations against the 0-100 rubric.
argument-hint: <ORG-ID|tier1|all>
allowed-tools: Bash, Read, Glob, Grep
---

Score: $ARGUMENTS

Use the rubric in `chanty-ecosystem-agent/config/scoring.md`. Sub-scores are 0-5 and each one needs a reason grounded in the evidence already on the record. If the evidence is not there, leave the component null rather than guessing, and say which components you could not score.

    cd chanty-ecosystem-agent/scripts && python3 -m eco score <ORG-ID> '<json>'

Report the score, band, coverage, and what research would move the score most.
