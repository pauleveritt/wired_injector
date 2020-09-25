"""
Extract field info in different types of signatures.

We want to do injection with functions. We want to do injection
with dataclasses. Perhaps namedtuple. Let's abstract all of that
into something which returns all the info possibly needed
downstream.
"""

import inspect
from dataclasses import Field, MISSING
from inspect import Parameter
from typing import NamedTuple, Optional, get_args, get_origin, Type, Any, Tuple, Union

from wired_injector.operators import Operator


class FieldInfo(NamedTuple):
    field_name: str
    field_type: Type
    default_value: Optional[Any]
    init: bool  # Dataclasses can flag init=False
    pipeline: Tuple[Operator, ...]


def function_field_info_factory(parameter: Parameter) -> FieldInfo:
    field_type = parameter.annotation

    pipeline = ()
    # Is this a generic, such as Optional[ServiceContainer]?
    origin = get_origin(field_type)
    args = get_args(field_type)
    if origin is Union and args[-1] is type(None):
        field_type = args[0]

    # Using Annotation[] ??
    if hasattr(field_type, '__metadata__'):
        field_type, *pipeline = get_args(field_type)

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
        pipeline=tuple(pipeline),
    )


def dataclass_field_info_factory(field: Field) -> FieldInfo:
    field_type = field.type

    # Using Annotation[] ??
    pipeline = ()
    if hasattr(field_type, '__metadata__'):
        field_type, *pipeline = get_args(field_type)

    # Is this a generic, such as Optional[ServiceContainer]?
    origin = get_origin(field_type)
    args = get_args(field_type)
    if origin is Union and args[-1] is type(None):
        field_type = args[0]

    if field.default is MISSING:
        default_value = None
    else:
        default_value = field.default
    return FieldInfo(
        field_name=field.name,
        field_type=field_type,
        default_value=default_value,
        init=field.init,
        pipeline=tuple(pipeline),
    )
