# Design Decisions

Notes on the choices that are not obvious from the code.

**Python for the rules, markdown for the reasoning.** Scoring, state transitions,
dedupe, suppression and gates have to behave identically on Tuesday and on
Friday. A model asked to "check the gates" will eventually decide a record is
close enough. So those live in code, and the agents call them. The agents do the
part models are good at: reading a website and working out what an organization
actually does.

**No dependencies.** Standard library only, including a hand-written JSON Schema
validator covering the subset the schemas use. The system has to run wherever it
lands, and a validation layer that fails to import is a validation layer that
does not run.

**Null scores zero.** An unresearched scoring component contributes nothing
rather than being averaged away. Thin research should not float an organization
into Tier 1, and `coverage` makes the thinness visible.

**Gates fail closed and report every failure by name.** A gate that returns
"failed" without saying which check failed is not useful to the next agent. Every
failure is named so the fix is obvious.

**Deterministic IDs.** `organization_id` is a hash of the identity seed, so
rediscovering the same organization produces the same ID and dedupe is idempotent
across runs.

**The chapter rule sits inside dedupe, not beside it.** Two records that differ
in chapter are never duplicates, even on an identical domain, which is the normal
case for a national association whose chapters share a site.

**Apollo and ZoomInfo are blocked by prefix, not by tool name.** A partial block
invites a workaround. Blocking the whole server is blunt and that is the point.
The block is also checked by name at call time, so a newly connected enrichment
server does not become permitted just because nobody updated a vendor list.

**Attio gets a plan, not a write.** MCP tools live in the agent, not in Python,
so the sync module produces reviewable calls and the agent executes them after
approval. It also means the plan is auditable before anything reaches the CRM.

**Missing Attio attributes are listed, not improvised.** The alternative was to
map ecosystem state onto the existing people `Stage` field, which means something
else. A note that is honest beats a field that is wrong.

**Compliance fields ship null.** The send gate fails out of the box. Someone has
to consciously turn sending on, which is the correct amount of friction for the
one irreversible action in the system.
