"""Append-only audit log.

Every meaningful action lands here as one JSON object per line. The log is the
reason anyone can answer "why did the system do that" three weeks later.
"""

import datetime
import json
import os

from . import paths


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def record(action, agent="orchestrator", organization=None, contact=None,
           input=None, output=None, evidence=None, decision=None,
           state_before=None, state_after=None, human_override=False,
           error=None, log_path=None):
    entry = {
        "timestamp": now(),
        "agent": agent,
        "organization": organization,
        "contact": contact,
        "action": action,
        "input": input,
        "output": output,
        "evidence": evidence or [],
        "decision": decision,
        "state_before": state_before,
        "state_after": state_after,
        "human_override": human_override,
        "error": error,
    }
    path = log_path or paths.audit_log()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a") as fh:
        fh.write(json.dumps(entry, sort_keys=True) + "\n")
    return entry


def read(log_path=None, limit=None):
    path = log_path or paths.audit_log()
    if not os.path.exists(path):
        return []
    with open(path) as fh:
        entries = [json.loads(line) for line in fh if line.strip()]
    return entries[-limit:] if limit else entries
