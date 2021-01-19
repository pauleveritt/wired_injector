"""
Operate on the info in a field until a value is produced.
"""
from dataclasses import dataclass
from typing import Type, Optional, Any, Dict, Callable, Sequence

from wired import ServiceContainer
from wired_injector.pipeline2 import Pipeline
from wired_injector.pipeline2.default_pipeline import DefaultPipeline
from wired_injector.pipeline2.field_pipeline import process_field_pipeline

from . import Container, FieldInfo, Operator, Result
from .results import (
    Init,
    Skip,
    Found,
)


@dataclass
class DefaultFieldInfo:
    """ Default implementation of the ``FieldInfo`` protocol """
    field_name: str
    field_type: Type[Any]
    default_value: Optional[Any]
    init: bool  # Dataclasses can flag init=False
    operators: Sequence[Operator]


@dataclass
class IsInit:
    """ If this is a dataclass field with init=False, skip """

    field_info: FieldInfo
    props: Dict[str, Any]
    container: Container
    pipeline: Pipeline
    system_props: Optional[Dict[str, Any]] = None
    target: Optional[Callable[..., Any]] = None

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
    props: Dict[str, Any]
    container: Container
    pipeline: Pipeline
    system_props: Optional[Dict[str, Any]] = None
    target: Optional[Callable[..., Any]] = None

    def __call__(self) -> Result:
        if self.props and self.field_info.field_name in self.props:
            # Props have precedence
            prop_value = self.props[self.field_info.field_name]
            return Found(value=prop_value)
        elif (
            self.system_props
            and self.field_info.field_name in self.system_props
        ):
            # If the "system" passes in props behind the scenes, use it
            prop_value = self.system_props[self.field_info.field_name]
            return Found(value=prop_value)

        # Nothing matched, so skip
        return Skip(value=self.field_info.field_type)


@dataclass
class IsContainer:
    """ If the field is asking for a ServiceContainer, return it """

    field_info: FieldInfo
    props: Dict[str, Any]
    container: Container
    pipeline: Pipeline
    system_props: Optional[Dict[str, Any]] = None
    target: Optional[Callable[..., Any]] = None

    def __call__(self) -> Result:
        if self.field_info.field_type is ServiceContainer:
            return Found(value=self.container)

        # Nothing matched, so skip
        return Skip(value=self.field_info.field_type)


@dataclass
class AnnotationPipeline:
    """ If field pipeline, process it, else, bail out """

    field_info: FieldInfo
    props: Dict[str, Any]
    container: Container
    pipeline: Pipeline
    system_props: Optional[Dict[str, Any]] = None
    target: Optional[Callable[..., Any]] = None

    def __call__(self) -> Result:
        result: Result = process_field_pipeline(
            operators=self.field_info.operators,
            pipeline=self.pipeline,
        )
        return result
