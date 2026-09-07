---
description: Weekly or monthly ecosystem report. Operational counts as diagnostics, paid seats as the scoreboard.
argument-hint: [weekly|monthly]
allowed-tools: Bash, Read, Glob, Grep
---

Generate the report: $ARGUMENTS (default weekly)

    cd chanty-ecosystem-agent/scripts && python3 -m eco report weekly

Weekly: new organizations, qualified, tier 1, tier 2, outreach, responses, meetings, partnerships, new signals, trials, paid accounts, seats, MRR, best category, best offer, best signal, best contact role, top opportunities, recommendations.

Monthly: archetypes, offers, signals, contact titles, verticals, geographies, partners, seats per partner, revenue per partner, partnership conversion, time to partnership, retention, recommended experiments, recommended lookalikes.

Present the operational numbers as diagnostics and the paid seat number as the metric that matters. Do not lead with emails sent.
