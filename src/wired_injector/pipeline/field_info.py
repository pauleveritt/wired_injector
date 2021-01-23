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
from typing import Type, Union, TYPE_CHECKING

from wired_injector.pipeline.rules import DefaultFieldInfo

if TYPE_CHECKING:
    pass

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


def function_field_info_factory(parameter: Parameter) -> DefaultFieldInfo:
    field_type = parameter.annotation

    # Is this a generic, such as Optional[ServiceContainer]?
    field_type = _get_field_origin(field_type)

    # Using Annotation[] ??
    has_annotated = hasattr(field_type, '__metadata__')
    field_type, operators = _get_pipeline(field_type)

    # Default values
    if parameter.default is getattr(inspect, '_empty'):
        default_value = None
    else:
        default_value = parameter.default

    return DefaultFieldInfo(
        field_name=parameter.name,
        field_type=field_type,
        default_value=default_value,
        init=True,
        operators=tuple(operators),
        has_annotated=has_annotated,
    )


def dataclass_field_info_factory(field: Field) -> DefaultFieldInfo:
    field_type = field.type

    # Is this a generic, such as Optional[ServiceContainer]?
    field_type = _get_field_origin(field_type)

    # Using Annotation[] ??
    has_annotated = hasattr(field_type, '__metadata__')
    field_type, operators = _get_pipeline(field_type)

    # Default values
    default_value = None if field.default is MISSING else field.default

    return DefaultFieldInfo(
        field_name=field.name,
        field_type=field_type,
        default_value=default_value,
        init=field.init,
        operators=tuple(operators),
        has_annotated=has_annotated,
    )
