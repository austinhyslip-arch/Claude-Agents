"""A small JSON Schema validator.

Only the subset of draft-07 the project's schemas actually use: type, required,
enum, pattern, minimum/maximum, minLength, items, properties,
additionalProperties, $ref to local #/definitions, and nullable unions expressed
as a type array.

Written by hand because the environment has no jsonschema package and the point
of these schemas is to fail closed at write time, not to be an exercise in
dependency management.
"""

import re


class ValidationError(ValueError):
    def __init__(self, errors):
        self.errors = errors
        super().__init__("; ".join(errors))


_TYPES = {
    "object": dict,
    "array": list,
    "string": str,
    "boolean": bool,
    "null": type(None),
}


def _type_ok(value, expected):
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    py = _TYPES.get(expected)
    if py is None:
        return True
    if py is str and isinstance(value, bool):
        return False
    return isinstance(value, py)


def _resolve(schema, root):
    if "$ref" in schema:
        ref = schema["$ref"]
        if not ref.startswith("#/"):
            raise ValueError("only local refs are supported: %s" % ref)
        node = root
        for part in ref[2:].split("/"):
            node = node[part]
        merged = dict(node)
        for k, v in schema.items():
            if k != "$ref":
                merged[k] = v
        return merged
    return schema


def _walk(value, schema, root, path, errors):
    schema = _resolve(schema, root)

    expected = schema.get("type")
    if expected is not None:
        options = expected if isinstance(expected, list) else [expected]
        if not any(_type_ok(value, o) for o in options):
            errors.append("%s: expected %s, got %s" % (path, "/".join(options), type(value).__name__))
            return

    if value is None:
        # A null that passed the type check needs no further checking. enum lists
        # that include null are handled above by the type union.
        if "enum" in schema and None not in schema["enum"] and expected is None:
            errors.append("%s: null is not one of %r" % (path, schema["enum"]))
        return

    if "enum" in schema and value not in schema["enum"]:
        errors.append("%s: %r is not one of %r" % (path, value, schema["enum"]))

    if isinstance(value, str):
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append("%s: %r does not match %s" % (path, value, schema["pattern"]))
        if "minLength" in schema and len(value) < schema["minLength"]:
            errors.append("%s: shorter than minLength %d" % (path, schema["minLength"]))

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append("%s: %r below minimum %r" % (path, value, schema["minimum"]))
        if "maximum" in schema and value > schema["maximum"]:
            errors.append("%s: %r above maximum %r" % (path, value, schema["maximum"]))

    if isinstance(value, list) and "items" in schema:
        for i, item in enumerate(value):
            _walk(item, schema["items"], root, "%s[%d]" % (path, i), errors)

    if isinstance(value, dict):
        props = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value:
                errors.append("%s: missing required field %r" % (path or "<root>", key))
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in props:
                    errors.append("%s: unexpected field %r" % (path or "<root>", key))
        for key, sub in props.items():
            if key in value:
                _walk(value[key], sub, root, ("%s.%s" % (path, key)) if path else key, errors)


def validate(instance, schema):
    """Raise ValidationError with every problem found, not just the first."""
    errors = []
    _walk(instance, schema, schema, "", errors)
    if errors:
        raise ValidationError(errors)
    return True
