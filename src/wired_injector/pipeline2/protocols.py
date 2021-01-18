"""
Protocol "interfaces" used for the pieces in pipelines.

"""
from __future__ import annotations

from typing import Optional, Any

try:
    from typing import Annotated, Protocol
except ImportError:
    from typing_extensions import Annotated, Protocol  # type: ignore # noqa: F401


class Container(Protocol):
    """
    The parts of ``ServiceContainer`` we need for ``Pipeline``.

    The pipeline stores an instance of a ``ServiceContainer``. But
    for testing, we don't want the actual type. Let's make a protocol
    that represents the parts of ``ServiceContainer`` that we need.
    """

    context: Any

    def get(self, key: Any) -> Any:
        pass


class Pipeline(Protocol):
    """
    Sequence of fields which results in arguments to construct.
    """

    container: Container

    def lookup(self, lookup_key: Any) -> Optional[Any]:
        """ Type-safe limited usage wrapper around container.get"""
        ...

    def inject(self, lookup_key: Any) -> Optional[Any]:
        """Type-safe, replaceable wrapper around the injector """
        ...


class OperatorResult(Protocol):
    value: Any


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
