"""Utilities to type check JSON."""

import logging
from typing import Dict, List, TypeGuard

JSONKey = str
"""JSON key data type."""

JSONValue = (
    str
    | int
    | float
    | bool
    | None
    # Once mypy is able to handle recursive type aliases, we can replace `object` with
    # `JSONValue` in the next two types
    # Note that `is_json_value` will limit lists and dicts to containing valid JSON
    # values, and not arbitrary objects
    | List[object]
    | Dict[JSONKey, object]
)
"""JSON value data type."""

JSON = Dict[JSONKey, JSONValue]
"""JSON data type."""


def is_json(value: object) -> TypeGuard[JSON]:
    """Type narrow an `object` to JSON.

    Perform a deep check on a `Dict` to ensure that its keys are JSON keys, and its
    values are JSON values.

    Args:
        value: The `object` to narrow.

    Returns:
        True if `value` is a `Dict` of JSON keys and values.

    """
    res = isinstance(value, Dict) and all(
        is_json_key(maybe_json_key) and is_json_value(maybe_json_value)
        for maybe_json_key, maybe_json_value in value.items()
    )
    logger.debug("\n\tvalue=%s\n\tres=%s", value, res)
    return res


def is_json_key(key: object) -> TypeGuard[JSONKey]:
    """Type narrow an `object` to a JSON key.

    Ensure that an object is a JSON key, i.e.,  a `str`.

    Args:
        key: The `object` to narrow.

    Returns:
        True if `key` is a JSON key.

    """
    return isinstance(key, JSONKey)


def is_json_value(value: object) -> TypeGuard[JSONValue]:
    """Type narrow an `object` to a JSON value.

    Perform a deep check on an `object` to ensure that it is a JSON value. A JSON
    value can be a valid simple type, e.g., `str` or `int`, a `List` of JSON values,
    or JSON itself, i.e., a `Dict` of JSON keys and values.

    Args:
        value: The `object` to narrow.

    Returns:
        True if `value` is a JSON value.

    """
    return is_json_simple_value(value) or is_json_list_value(value) or is_json(value)


def is_json_simple_value(value: object) -> bool:
    """Check that an object is simple JSON value.

    Args:
        value: The `object` to check.

    Returns:
        True if `value` is a simple JSON type.

    """
    return isinstance(value, str | int | float | bool | None)


def is_json_list_value(value: object) -> bool:
    """Check that an object is `List` of JSON values.

    Performs a deep check on each item of the list.

    Args:
        value: The `object` to check.

    Returns:
        True if `value` is a `List` of JSON values.

    """
    return isinstance(value, List) and all(
        is_json_value(maybe_json_value) for maybe_json_value in value
    )


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
