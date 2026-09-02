"""Loads follow-up cadence rules from config/cadence_rules.yaml."""
import yaml


def load_cadence_rules(path: str = "config/cadence_rules.yaml") -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def days_until_followup(classification: dict, rules: dict) -> int | None:
    """Maps a thread's classified stage to a number of days out for the next follow-up.
    Returns None if the stage isn't a follow-up case (e.g. Meeting Booked, Closed)."""
    stage = classification.get("stage")
    stage_rules = rules["rules"]

    if stage in stage_rules and stage_rules[stage].get("days") is not None:
        return stage_rules[stage]["days"]

    if stage in ("WON-Closed", "LOST-Closed", "Not a Fit", "Not Contacted", "Meeting Booked"):
        return None

    return stage_rules["general_follow_up"]["days"]
