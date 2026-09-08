"""Resolving a US organization's local timezone.

Needed because outreach must land inside the recipient's working day, and the
recipient's working day is defined by where they are, not by where we are.

The resolution is deliberately conservative. A state whose territory spans two
zones only resolves to KNOWN_FACT when the city is in the override table.
Otherwise it is an ESTIMATE, and the send window narrows by an hour on each side
so an hour of error cannot push a message outside the recipient's day.
"""

STATE_ZONES = {
    "AL": "America/Chicago", "AK": "America/Anchorage", "AZ": "America/Phoenix",
    "AR": "America/Chicago", "CA": "America/Los_Angeles", "CO": "America/Denver",
    "CT": "America/New_York", "DE": "America/New_York", "DC": "America/New_York",
    "FL": "America/New_York", "GA": "America/New_York", "HI": "Pacific/Honolulu",
    "ID": "America/Denver", "IL": "America/Chicago", "IN": "America/New_York",
    "IA": "America/Chicago", "KS": "America/Chicago", "KY": "America/New_York",
    "LA": "America/Chicago", "ME": "America/New_York", "MD": "America/New_York",
    "MA": "America/New_York", "MI": "America/New_York", "MN": "America/Chicago",
    "MS": "America/Chicago", "MO": "America/Chicago", "MT": "America/Denver",
    "NE": "America/Chicago", "NV": "America/Los_Angeles", "NH": "America/New_York",
    "NJ": "America/New_York", "NM": "America/Denver", "NY": "America/New_York",
    "NC": "America/New_York", "ND": "America/Chicago", "OH": "America/New_York",
    "OK": "America/Chicago", "OR": "America/Los_Angeles", "PA": "America/New_York",
    "RI": "America/New_York", "SC": "America/New_York", "SD": "America/Chicago",
    "TN": "America/Chicago", "TX": "America/Chicago", "UT": "America/Denver",
    "VT": "America/New_York", "VA": "America/New_York", "WA": "America/Los_Angeles",
    "WV": "America/New_York", "WI": "America/Chicago", "WY": "America/Denver",
}

# States whose territory spans more than one zone. A city here needs to be in
# CITY_ZONES to count as known.
SPLIT_STATES = {"FL", "ID", "IN", "KS", "KY", "MI", "ND", "NE", "NV", "OR",
                "SD", "TN", "TX", "AK"}

# City overrides, keyed (CITY_UPPER, STATE). Only cities actually verified.
CITY_ZONES = {
    ("BOISE", "ID"): "America/Denver",
    ("COEUR D'ALENE", "ID"): "America/Los_Angeles",
    ("CHATTANOOGA", "TN"): "America/New_York",
    ("KNOXVILLE", "TN"): "America/New_York",
    ("NASHVILLE", "TN"): "America/Chicago",
    ("MEMPHIS", "TN"): "America/Chicago",
    ("GRAND RAPIDS", "MI"): "America/New_York",
    ("DETROIT", "MI"): "America/New_York",
    ("FARGO", "ND"): "America/Chicago",
    ("BISMARCK", "ND"): "America/Chicago",
    ("SIOUX FALLS", "SD"): "America/Chicago",
    ("RAPID CITY", "SD"): "America/Denver",
    ("WICHITA", "KS"): "America/Chicago",
    ("LINCOLN", "NE"): "America/Chicago",
    ("OMAHA", "NE"): "America/Chicago",
    ("SALEM", "OR"): "America/Los_Angeles",
    ("PORTLAND", "OR"): "America/Los_Angeles",
    ("EL PASO", "TX"): "America/Denver",
    ("HOUSTON", "TX"): "America/Chicago",
    ("DALLAS", "TX"): "America/Chicago",
    ("AUSTIN", "TX"): "America/Chicago",
    ("INDIANAPOLIS", "IN"): "America/New_York",
    ("LAS VEGAS", "NV"): "America/Los_Angeles",
    ("PENSACOLA", "FL"): "America/Chicago",
    ("MIAMI", "FL"): "America/New_York",
    ("LOUISVILLE", "KY"): "America/New_York",
}


def resolve(city=None, state=None, country="US"):
    """Return (iana_name_or_None, confidence).

    confidence is KNOWN_FACT, ESTIMATE or UNKNOWN. UNKNOWN means we do not know
    when this organization's working day is, and the send window gate treats
    that as a blocker rather than picking something plausible.
    """
    if country and country.upper() not in ("US", "USA", "UNITED STATES"):
        return None, "UNKNOWN"

    state = (state or "").strip().upper()
    city_key = ((city or "").strip().upper(), state)

    if city_key in CITY_ZONES:
        return CITY_ZONES[city_key], "KNOWN_FACT"
    if state in STATE_ZONES:
        if state in SPLIT_STATES:
            return STATE_ZONES[state], "ESTIMATE"
        return STATE_ZONES[state], "KNOWN_FACT"
    return None, "UNKNOWN"
