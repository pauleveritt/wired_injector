"""
Operate on the info in a field until a value is produced.
"""
import builtins
import typing
from dataclasses import dataclass
from inspect import getmodule
from typing import Type, Optional, Any, Sequence

from wired import ServiceContainer
from wired_injector.pipeline import Pipeline
from wired_injector.pipeline.field_pipeline import process_field_pipeline

from . import FieldInfo, Operator, Result
from .results import (
    Init,
    Found,
    NotFound,
    Skip,
)


@dataclass
class DefaultFieldInfo:
    """ Default implementation of the ``FieldInfo`` protocol """
    field_name: str
    field_type: Type[Any]
    default_value: Optional[Any] = None
    init: bool = True  # Dataclasses can flag init=False
    operators: Sequence[Operator] = tuple()
    has_annotated: bool = False


@dataclass
class IsInit:
    """ If this is a dataclass field with init=False, skip """

    field_info: FieldInfo
    pipeline: Pipeline

    def __call__(self) -> Result:
        value = self.field_info.field_type
        if self.field_info.init is False:
            # This means dataclasses.field(init=False) which means
            # this field should not be part of injection.
            return Init(value=value)
        return Skip(value=value)


@dataclass
class IsInProps:
    """ If field in passed-in props or system props, return value """

    field_info: FieldInfo
    pipeline: Pipeline

    def __call__(self) -> Result:
        props = self.pipeline.props
        system_props = self.pipeline.system_props
        if props and self.field_info.field_name in props:
            # Props have precedence
            prop_value = props[self.field_info.field_name]
            return Found(value=prop_value)
        elif (
            system_props
            and self.field_info.field_name in system_props
        ):
            # If the "system" passes in props behind the scenes, use it
            prop_value = system_props[self.field_info.field_name]
            return Found(value=prop_value)

        # Nothing matched, so skip
        return Skip(value=self.field_info.field_type)


@dataclass
class IsContainer:
    """ If the field is asking for a ServiceContainer, return it """

    field_info: FieldInfo
    pipeline: Pipeline

    def __call__(self) -> Result:
        if self.field_info.field_type is ServiceContainer:
            return Found(value=self.pipeline.container)

        # Nothing matched, so skip
        return Skip(value=self.field_info.field_type)


@dataclass
class IsSimpleType:
    """ Just a type hint, no annotations """

    field_info: FieldInfo
    pipeline: Pipeline

    def __call__(self) -> Result:
        fi = self.field_info
        if not fi.has_annotated:
            # No annotation, this rule matches

            if getmodule(fi.field_type) in (builtins, typing):
                # Test this because, when you have a field like:
                #   names: Tuple[str, ...] = ('Name 1',)  # noqa: E800
                # ...then wired tries to do obj.__qualname__ and fails
                return Skip(value=IsSimpleType)

            value = self.pipeline.container.get(fi.field_type, default=None)
            if value is None:
                # That field type is not in the container, bail with
                # a NotFound
                lookup_name = fi.field_type.__name__
                msg = f"No service '{lookup_name}' found in container"
                nf = NotFound(msg=msg, value=IsSimpleType)
                return nf
            return Found(value=value)

        # Nothing matched, so skip
        return Skip(value=IsSimpleType)


@dataclass
class AnnotationPipeline:
    """ If field pipeline, process it, else, bail out """

    field_info: FieldInfo
    pipeline: Pipeline

    def __call__(self) -> Result:
        result: Result = process_field_pipeline(
            operators=self.field_info.operators,
            pipeline=self.pipeline,
        )
        return result
