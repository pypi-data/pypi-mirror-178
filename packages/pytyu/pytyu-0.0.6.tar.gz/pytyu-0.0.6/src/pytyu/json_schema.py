"""Utilities to type check JSON schemas."""

from collections.abc import Iterable, Sequence
from inspect import get_annotations
import logging
from types import UnionType
from typing import Callable, Dict, List, Optional, Tuple, TypeGuard, Union

from pytyu.json import (
    is_json,
    is_json_key,
    is_json_value,
    is_json_simple_value,
    is_json_list_value,
)

SchemaT = type | UnionType | Tuple[type | UnionType, ...]
CheckSchemaTypeValue = Callable[[object, SchemaT], bool]


def _try_issubclass(subcls: SchemaT, cls: SchemaT) -> bool:
    """Check that a `type` is a subclass of another `type` with error handling.

    `issubclass`_ will raise a `TypeError` if `subcls` or `cls` can't be used in a
    subclass comparison.

    Args:
        subcls: The class to check.
        cls: The class to check against.

    Returns:
        True if `subcls` is a subclass of `cls`. False if `subcls` is not a subclass
        of `cls`, or `issubclass` raises a `TypeError`.

    .. _issubclass:
        https://docs.python.org/3/library/functions.html#issubclass

    """
    try:
        return issubclass(subcls, cls)  # type: ignore
    except TypeError:
        return False


def is_json_schema(value: object, schema: SchemaT) -> TypeGuard[SchemaT]:
    """Type narrow an `object` to a JSON schema.

    Perform a deep check on a `Dict` to ensure that each of its keys is present in
    the schema, and the corresponding value type matches the type for that key in
    the schema.

    Args:
        value: The `object` to narrow. This must be the entire `Dict`.
        schema: An `object` that describes the schema for an entire `Dict`, e.g.,
            a `NamedTuple` or a `TypedDict`.

    Returns:
        True if `value` is a `Dict` that conforms to `schema`.

    """
    res = isinstance(value, Dict) and _is_json_schema_value(value, schema)
    logger.debug("\n\tvalue=%s\n\tschema=%s\n\tres=%s", value, schema, res)
    return res


def _is_json_schema_value(value: object, schema: SchemaT) -> bool:
    """Check that an `object` conforms to a schema type.

    Perform a deep check on an `object` to ensure that it conforms to a schema
    type. A schema type can be:

        - a simple JSON value type
        - an annotated object that describes a schema, i.e., a sub-schema
        - a generic union of JSON value types or other schema types
        - a generic `List` of JSON value types or other schema types
        - a generic `Dict` of str keys and JSON value types or other schema types
        - a `List` of JSON value types
        - a `Dict` of str keys and JSON value types

    Args:
        value: The `object` to check. This may be the entire `Dict`, or one of
            its values.
        schema: An `object` that describes the schema for a value.

    Returns:
        True if `value` conforms to `schema`.

    """
    check_schema_type_value = _select_json_check_schema_type_value(schema)
    res = check_schema_type_value(value, schema) if check_schema_type_value else False
    logger.debug(
        "\n\tvalue=%s\n\tschema=%s\n\tcheck_fn=%s\n\tres=%s",
        value,
        schema,
        check_schema_type_value.__name__ if check_schema_type_value else None,
        res,
    )
    return res


def _select_json_check_schema_type_value(  # pylint: disable=too-many-return-statements
    schema: SchemaT,
) -> Optional[CheckSchemaTypeValue]:
    """Determine the schema type for `schema`.

    Args:
        schema: An `object` that describes the schema for a value.

    Returns:
        The function that checks if a value conforms to the schema type described by
        `schema`. None if `schema` doesn't describe a schema type.

    """
    if isinstance(schema, type):
        if _try_issubclass(schema, str | int | float | bool | None):
            return _is_json_schema_value_simple

        if get_annotations(schema):
            return _is_json_schema_value_annotated

    generic_type = getattr(schema, "__origin__", None)
    generic_params = getattr(schema, "__args__", None)
    if (generic_type is Union or isinstance(schema, UnionType)) and isinstance(
        generic_params, Iterable
    ):
        return _is_json_schema_value_generic_union

    if generic_type is not None and isinstance(generic_params, Sequence):
        if _try_issubclass(generic_type, List) and len(generic_params) == 1:
            return _is_json_schema_value_generic_list

        if _try_issubclass(generic_type, Dict) and len(generic_params) == 2:
            return _is_json_schema_value_generic_dict

    if _try_issubclass(schema, List):
        return _is_json_schema_value_list

    if _try_issubclass(schema, Dict):
        return _is_json_schema_value_dict

    return None


def _is_json_schema_value_simple(value: object, schema: SchemaT) -> bool:
    """Check that an `object` conforms to a simple JSON type.

    Args:
        value: The `object` to check. This must be a simple JSON value.
        schema: A simple JSON value type.

    Returns:
        True if `value` is a simple JSON type.

    """
    return is_json_simple_value(value) and isinstance(value, schema)


def _is_json_schema_value_annotated(value: object, schema: SchemaT) -> bool:
    """Check that an `object` conforms to an annotated schema.

    Args:
        value: The `object` to check. This must be a `Dict`.
        schema: An `object` with annotations that describes the schema, e.g., a
            `NamedTuple` or a `TypedDict`.

    Returns:
        True if `value` is a `Dict` that conforms to `schema`.

    """
    if not isinstance(value, Dict):
        return False

    assert isinstance(schema, type)
    anns = get_annotations(schema)
    return all(
        is_json_key(each_key)
        and _is_json_schema_value(each_value, anns.get(each_key, None))
        for each_key, each_value in value.items()
    )


def _is_json_schema_value_generic_union(value: object, schema: SchemaT) -> bool:
    """Check that an `object` conforms to one of the schema types in a union of
    schema types.

    Args:
        value: the `object` to check.
        schema: A union that consists of other schema types.

    Returns:
        True if `schema` is union of schema types, and `value` conforms to one of
        those types.

    """
    generic_params = getattr(schema, "__args__", None)
    assert isinstance(generic_params, Iterable)
    return any(
        _is_json_schema_value(value, generic_param) for generic_param in generic_params
    )


def _is_json_schema_value_generic_list(value: object, schema: SchemaT) -> bool:
    """Check that an `object` conforms to a `List` of JSON value types or schema types.

    Args:
        value: The `object` to check. This must be a `List`.
        schema: A generic `List` of JSON value types or schema types.

    Returns:
        True if `value` is a `List` that conforms to `schema`.

    """
    if not isinstance(value, List):
        return False

    generic_params = getattr(schema, "__args__", None)
    assert isinstance(generic_params, Sequence)
    return all(
        _is_json_schema_value(each_value, generic_params[0]) for each_value in value
    ) or (generic_params[0] is object and is_json_list_value(value))


def _is_json_schema_value_generic_dict(value: object, schema: SchemaT) -> bool:
    """Check that an `object` conforms to a `Dict` of str keys, and JSON value type
    or schema type values.

    Args:
        value: The `object` to check. This must be a `Dict`.
        schema: A generic `Dict` type of str keys, and JSON value types or schema
            types.

    Returns:
        True if `value` is a `Dict` that conforms to `schema`.

    """
    if not isinstance(value, Dict):
        return False

    generic_params = getattr(schema, "__args__", None)
    assert isinstance(generic_params, Sequence)
    return (
        _try_issubclass(generic_params[0], str)
        and all(
            is_json_key(each_key)
            and _is_json_schema_value(each_value, generic_params[1])
            for each_key, each_value in value.items()
        )
    ) or (generic_params[1] is object and is_json_value(value))


def _is_json_schema_value_list(value: object, _: SchemaT) -> bool:
    """Check that an `object` is a `List` of JSON values.

    Args:
        value: The `object` to check. This must be a `List`.

    Returns:
        True if `value` is a `List` of JSON values.

    """
    return is_json_list_value(value)


def _is_json_schema_value_dict(value: object, _: SchemaT) -> bool:
    """Check that an `object` is a `Dict` of str keys and JSON values.

    Args:
        value: The `object` to check. This must be a `Dict`.

    Returns:
        True if `value` is a `Dict` of str keys and JSON values.

    """
    return is_json(value)


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
