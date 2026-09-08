# Chanty Ecosystem Agent

A business development system that finds organizations able to distribute Chanty
to small businesses, researches why they would want to, prepares the approach,
and stops where a person should decide.

Start with `CLAUDE.md`. It is the operating brief.

## Quick start

    cd scripts
    python3 -m eco init
    python3 -m eco status
    python3 -m eco policy chanty_pricing

    cd ../tests
    python3 -m unittest discover -s . -p "test_*.py" -t .

## Current posture

Autonomy level 0, research only. Draft, don't send. Sending is blocked by the
compliance gate until a human fills in three fields in `config/policy.json`.
See `docs/authorization-required.md`.

## Slash commands

`/eco-discover`, `/eco-research`, `/eco-score`, `/eco-contacts`, `/eco-signals`,
`/eco-drafts`, `/eco-review`, `/eco-send`, `/eco-learn`, `/eco-report`,
`/eco-run`. They live in `.claude/commands/` at the repository root.

## The rules that do not bend

$3 per seat, and no other commercial terms. Public sources only for contact
data, with Apollo, ZoomInfo and Clay's contact tools blocked even though they are
connected. Never guess an email. Never state an estimate as a fact. Never send
without a human.

## Layout

    CLAUDE.md      the operating brief
    agents/        eight agent definitions
    config/        policy, offers, claims, scoring, escalation, suppression
    schemas/       nine record schemas, enforced on write
    workflows/     discovery, qualification, outreach, activation, learning, daily
    commands/      what each command does (the files live in .claude/commands/)
    scripts/eco/   the deterministic core and CLI
    tests/         155 tests
    data/          the record store
    logs/          the audit log
    docs/          taxonomy, evidence, integrations, authorization, decisions
    pilot/         the 100-organization targeting plan
