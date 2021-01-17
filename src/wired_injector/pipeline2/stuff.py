"""
Process fields in a target to produce argument values.

Targets have a list of arguments. Dataclasses/NamedTuples have fields,
functions have arguments, etc. The injector wants to use a little
DSL that goes through each field and gets the value, handling
problems along the way.

Pipeline
========

All the work to collect a dictionary of values to apply for construction.

FieldPipeline
=============

All the work to get the value for one field.

Rules
=====

An ordered list of simple policies to work through in trying to get
a value.

Operator
========

A sequence of input/outputs to work through in trying to get a value.

While these are each intended to be isolated, pure, atomic, etc., in
some cases you want to rely on something elsewhere. For example, the
passed-in prop to refer to a logo might be used to resolve into a full
relative link.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional, TypeVar, Any

try:
    from typing import Annotated, Protocol
except ImportError:
    from typing_extensions import Annotated, Protocol  # type: ignore # noqa: F401


class OperatorStatus(Enum):
    found = 1
    not_applicable = 2
    not_found = 3


class OperatorResult(Protocol):
    value: Any
    status: OperatorStatus


@dataclass
class Found:
    """ Operation was looked up in the container and found """
    value: Any
    status: OperatorStatus = OperatorStatus.found


@dataclass
class NotFound:
    """ Value was looked up in the container, but nothing matched. """
    value: Any
    status: OperatorStatus = OperatorStatus.not_found


class Operator(Protocol):
    def __call__(
        self,
        previous: Optional[Any],
        pipeline: Pipeline,
    ) -> OperatorResult:
        ...


@dataclass
class Get:
    lookup_type: Any
    attr: Optional[str] = None

    def __call__(
        self,
        previous: Optional[Any],
        pipeline: Pipeline,
    ) -> OperatorResult:
        f = Found(value=99)
        return f


LookupType = TypeVar('LookupType')


class Container(Protocol):
    """ The part of the ServiceContainer behavior we need """

    def get(self, lookup_value: LookupType) -> Optional[LookupType]:
        """ Lookup a type in the container """
        pass


class Pipeline(Protocol):
    pass


@dataclass
class DefaultPipeline:
    pass
