"""
Extract field info in different types of signatures.

We want to do injection with functions. We want to do injection
with dataclasses. Perhaps namedtuple. Let's abstract all of that
into something which returns all the info possibly needed
downstream.
"""

import inspect
import sys
from dataclasses import Field, MISSING
from inspect import Parameter
from typing import NamedTuple, Optional, Type, Any, Tuple, Union

from wired_injector.operators import Operator

# get_args is augmented in Python 3.9. We need to use
# typing_extensions if not running on an older version
if sys.version_info[:3] >= (3, 9):
    from typing import get_args
else:  # pragma: no cover
    # noinspection PyUnresolvedReferences
    from typing_extensions import get_args

try:
    from typing import get_origin
except ImportError:  # pragma: no cover
    from typing_utils import get_origin  # type: ignore


class FieldInfo(NamedTuple):
    field_name: str
    field_type: Type
    default_value: Optional[Any]
    init: bool  # Dataclasses can flag init=False
    operators: Tuple[Operator, ...]


def _get_field_origin(field_type: Type) -> Type:
    """ Helper to extract generic origin """

    origin = get_origin(field_type)
    args = get_args(field_type)
    if origin is Union and args[-1] is type(None):  # noqa: E721
        return args[0]
    else:
        return field_type


def _get_pipeline(field_type: Type):
    """ If using Annotation, get the pipeline information """
    operators = []
    if hasattr(field_type, '__metadata__'):
        field_type, *operators = get_args(field_type)

    return field_type, tuple(operators)


def function_field_info_factory(parameter: Parameter) -> FieldInfo:
    field_type = parameter.annotation

    # Is this a generic, such as Optional[ServiceContainer]?
    field_type = _get_field_origin(field_type)

    # Using Annotation[] ??
    field_type, operators = _get_pipeline(field_type)

    # Default values
    if parameter.default is getattr(inspect, '_empty'):
        default_value = None
    else:
        default_value = parameter.default

    return FieldInfo(
        field_name=parameter.name,
        field_type=field_type,
        default_value=default_value,
        init=True,
        operators=tuple(operators),
    )


def dataclass_field_info_factory(field: Field) -> FieldInfo:
    field_type = field.type

    # Is this a generic, such as Optional[ServiceContainer]?
    field_type = _get_field_origin(field_type)

    # Using Annotation[] ??
    field_type, operators = _get_pipeline(field_type)

    # Default values
    default_value = None if field.default is MISSING else field.default

    return FieldInfo(
        field_name=field.name,
        field_type=field_type,
        default_value=default_value,
        init=field.init,
        operators=tuple(operators),
    )
