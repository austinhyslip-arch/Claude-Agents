"""Record store.

One JSON file per record on disk. Attio is the operational system of record;
this store is the working set the agents reason over between syncs, and the
place where evidence and gate results live in full detail.

Every write validates against the schema first. A record that does not validate
does not get written.
"""

import json
import os

from . import audit, paths, validate

_schema_cache = {}


def schema(collection):
    if collection not in _schema_cache:
        with open(os.path.join(paths.SCHEMA_DIR, paths.COLLECTIONS[collection])) as fh:
            _schema_cache[collection] = json.load(fh)
    return _schema_cache[collection]


def _path(collection, record_id, root=None):
    base = os.path.join(root, collection) if root else paths.data_dir(collection)
    return os.path.join(base, record_id + ".json")


def id_field(collection):
    return {
        "organizations": "organization_id",
        "contacts": "contact_id",
        "opportunities": "opportunity_id",
        "signals": "signal_id",
        "partners": "partner_id",
        "outreach": "outreach_id",
        "attribution": "attribution_id",
        "suppression": "suppression_id",
        "executions": "execution_id",
    }[collection]


def put(collection, record, root=None, log=True):
    validate.validate(record, schema(collection))
    rid = record[id_field(collection)]
    path = _path(collection, rid, root)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    existed = os.path.exists(path)
    with open(path, "w") as fh:
        json.dump(record, fh, indent=2, sort_keys=True)
        fh.write("\n")
    if log:
        audit.record(
            action="update_record" if existed else "create_record",
            organization=record.get("organization_id"),
            contact=record.get("contact_id"),
            input={"collection": collection, "id": rid},
            output={"state": record.get("state")},
        )
    return record


def get(collection, record_id, root=None):
    path = _path(collection, record_id, root)
    if not os.path.exists(path):
        return None
    with open(path) as fh:
        return json.load(fh)


def exists(collection, record_id, root=None):
    return os.path.exists(_path(collection, record_id, root))


def all(collection, root=None):
    base = os.path.join(root, collection) if root else paths.data_dir(collection)
    if not os.path.isdir(base):
        return []
    out = []
    for name in sorted(os.listdir(base)):
        if name.endswith(".json"):
            with open(os.path.join(base, name)) as fh:
                out.append(json.load(fh))
    return out


def find(collection, root=None, **criteria):
    matched = []
    for rec in all(collection, root):
        ok = True
        for key, value in criteria.items():
            if rec.get(key) != value:
                ok = False
                break
        if ok:
            matched.append(rec)
    return matched


def delete(collection, record_id, root=None):
    path = _path(collection, record_id, root)
    if os.path.exists(path):
        os.remove(path)
        return True
    return False
