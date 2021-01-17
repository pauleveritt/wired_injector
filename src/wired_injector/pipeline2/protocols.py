"""
Protocol "interfaces" used for the pieces in pipelines.

"""
from __future__ import annotations

from enum import Enum
from typing import Optional, Any

try:
    from typing import Annotated, Protocol
except ImportError:
    from typing_extensions import Annotated, Protocol  # type: ignore # noqa: F401


class OperatorStatus(Enum):
    found = 1
    not_applicable = 2
    not_found = 3


class Pipeline(Protocol):
    """
    Sequence of fields which results in arguments to construct.
    """
    pass


class OperatorResult(Protocol):
    value: Any
    status: OperatorStatus


class Operator(Protocol):
    """
    A step in a FieldPipeline.

    """

    def __call__(
        self,
        previous: Optional[Any],
        pipeline: Pipeline,
    ) -> OperatorResult:
        ...
