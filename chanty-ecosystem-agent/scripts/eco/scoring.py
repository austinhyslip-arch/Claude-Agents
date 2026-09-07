"""Organization scoring: 0-100 across five dimensions.

Sub-scores are 0-5 and come from the Intelligence Agent, which must ground each
one in evidence. A dimension nobody researched scores 0. That is deliberate:
it keeps an unresearched organization out of Tier 1 instead of letting silence
average out in its favour.
"""

from . import policy

DIMENSIONS = {
    "audience_fit": {
        "max": 25,
        "components": ["smb_concentration", "employee_size_fit", "team_communication_need",
                       "vertical_relevance", "geographic_reach"],
    },
    "distribution_power": {
        "max": 25,
        "components": ["email_newsletter", "webinars_workshops", "events",
                       "member_client_communication", "community_directory_repeat_exposure"],
    },
    "partnership_compatibility": {
        "max": 20,
        "components": ["technology_sponsors", "member_benefits",
                       "educational_partnerships", "referral_structure"],
    },
    "timing": {
        "max": 15,
        "components": ["upcoming_event", "current_initiative", "leadership_or_program_change"],
    },
    "strategic_value": {
        "max": 15,
        "components": ["multi_chapter_national_leverage", "potential_seat_volume",
                       "lookalike_potential"],
    },
}


class ScoringError(ValueError):
    pass


def _component_score(raw, name):
    if raw is None:
        return 0
    if not isinstance(raw, (int, float)) or isinstance(raw, bool):
        raise ScoringError("%s must be a number 0-5, got %r" % (name, raw))
    if raw < 0 or raw > 5:
        raise ScoringError("%s must be between 0 and 5, got %r" % (name, raw))
    return float(raw)


def score(inputs, policy_path=None):
    """inputs: {dimension: {component: 0-5}}. Returns the full breakdown."""
    breakdown = {}
    total = 0.0
    for dim, spec in DIMENSIONS.items():
        given = inputs.get(dim, {}) or {}
        unknown = set(given) - set(spec["components"])
        if unknown:
            raise ScoringError("unknown components for %s: %s" % (dim, sorted(unknown)))
        raw_points = sum(_component_score(given.get(c), "%s.%s" % (dim, c))
                         for c in spec["components"])
        raw_max = 5.0 * len(spec["components"])
        weighted = raw_points / raw_max * spec["max"]
        breakdown[dim] = {
            "components": {c: given.get(c) for c in spec["components"]},
            "raw_points": raw_points,
            "raw_max": raw_max,
            "weighted": round(weighted, 2),
            "max": spec["max"],
            "missing": [c for c in spec["components"] if given.get(c) is None],
        }
        total += weighted

    total = round(total, 2)
    band = policy.band_for_score(total, path=policy_path)
    scored_components = sum(len(spec["components"]) - len(breakdown[d]["missing"])
                            for d, spec in DIMENSIONS.items())
    all_components = sum(len(spec["components"]) for spec in DIMENSIONS.values())
    return {
        "organization_score": total,
        "priority_band": band,
        "score_breakdown": breakdown,
        "coverage": round(scored_components / all_components, 2),
    }


def partner_tier(band, national_or_local, multi_chapter=False):
    """Partner tier is about leverage, not score alone."""
    if band == "STRATEGIC" or multi_chapter or national_or_local == "national":
        return "A"
    if band == "TIER_1":
        return "B"
    if band == "TIER_2":
        return "C"
    return "D"
