"""Where things live. Resolved from this file, not from the shell's cwd."""

import os

PKG_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.dirname(PKG_DIR)
ROOT = os.path.dirname(SCRIPTS_DIR)

CONFIG_DIR = os.path.join(ROOT, "config")
SCHEMA_DIR = os.path.join(ROOT, "schemas")
DATA_DIR = os.path.join(ROOT, "data")
LOG_DIR = os.path.join(ROOT, "logs")
AGENTS_DIR = os.path.join(ROOT, "agents")
WORKFLOW_DIR = os.path.join(ROOT, "workflows")

POLICY_FILE = os.path.join(CONFIG_DIR, "policy.json")
PROHIBITED_CLAIMS_FILE = os.path.join(CONFIG_DIR, "prohibited-claims.md")
APPROVED_CLAIMS_FILE = os.path.join(CONFIG_DIR, "approved-claims.md")
AUDIT_LOG = os.path.join(LOG_DIR, "audit.jsonl")

COLLECTIONS = {
    "organizations": "organization.json",
    "contacts": "contact.json",
    "opportunities": "opportunity.json",
    "signals": "signal.json",
    "partners": "partner.json",
    "outreach": "outreach.json",
    "attribution": "attribution.json",
    "suppression": "suppression.json",
    "executions": "agent-execution.json",
}


def data_root():
    """ECO_DATA_DIR lets a test or a dry run point the store somewhere harmless."""
    return os.environ.get("ECO_DATA_DIR") or DATA_DIR


def log_dir():
    return os.environ.get("ECO_LOG_DIR") or LOG_DIR


def audit_log():
    return os.path.join(log_dir(), "audit.jsonl")


def data_dir(collection):
    return os.path.join(data_root(), collection)


def ensure_dirs():
    for c in COLLECTIONS:
        os.makedirs(data_dir(c), exist_ok=True)
    os.makedirs(log_dir(), exist_ok=True)
