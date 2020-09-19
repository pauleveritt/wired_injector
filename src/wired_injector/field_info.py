"""
Extract field info in different types of signatures.

We want to do injection with functions. We want to do injection
with dataclasses. Perhaps namedtuple. Let's abstract all of that
into something which returns all the info possibly needed
downstream.
"""

import inspect
import typing
from dataclasses import Field, MISSING
from inspect import Parameter
from typing import NamedTuple, Optional, get_args, get_origin


class FieldInfo(NamedTuple):
    field_name: str
    field_type: typing.Type
    service_type: Optional[typing.Type]
    default_value: Optional[typing.Any]
    init: bool = True  # Dataclasses can flag init=False


def function_field_info_factory(parameter: Parameter) -> FieldInfo:
    annotation = parameter.annotation

    # Is this a generic, such as Optional[ServiceContainer]?
    origin = get_origin(annotation)
    args = get_args(annotation)
    if origin is typing.Union and args[-1] is type(None):
        field_type = args[0]
    else:
        field_type = annotation

    service_type = None

    if parameter.default is getattr(inspect, '_empty'):
        default_value = None
    else:
        default_value = parameter.default
    return FieldInfo(
        field_name=parameter.name,
        field_type=field_type,
        service_type=service_type,
        default_value=default_value,
    )


def dataclass_field_info_factory(field: Field) -> FieldInfo:
    field_type = field.type

    # Is this a generic, such as Optional[ServiceContainer]?
    origin = get_origin(field_type)
    args = get_args(field_type)
    if origin is typing.Union and args[-1] is type(None):
        field_type = args[0]
    else:
        field_type = field_type

    service_type = None

    if field.default is MISSING:
        default_value = None
    else:
        default_value = field.default
    return FieldInfo(
        field_name=field.name,
        field_type=field_type,
        service_type=service_type,
        default_value=default_value,
        init=field.init,
    )
