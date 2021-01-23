"""
Protocol "interfaces" used for the pieces in pipelines.

"""
from __future__ import annotations

from typing import Optional, Any, Type, Dict, Callable, Sequence, Mapping

try:
    from typing import Annotated, Protocol
except ImportError:
    from typing_extensions import Annotated, Protocol  # type: ignore # noqa: F401


class Container(Protocol):
    """
    The parts of ``InjectorContainer`` we need for ``Pipeline``.

    The pipeline stores an instance of a ``InjectorContainer``. But
    for testing, we don't want the actual type. Let's make a protocol
    that represents the parts of ``ServiceContainer`` that we need.
    """

    context: Any

    def get(self, key: Any, default: Optional[Any] = None) -> Any:
        pass

    def inject(
        self,
        iface_or_type=Any,
        *,
        cget_props: Optional[Mapping[str, Any]] = None,
        system_props: Optional[Mapping[str, Any]] = None,
        **kwargs,
    ) -> Any:
        ...


class Pipeline(Protocol):
    """
    Sequence of fields which results in arguments to construct.
    """

    container: Container
    field_infos: Sequence[FieldInfo]
    props: Dict[str, Any]
    target: Callable[..., Any]
    system_props: Optional[Dict[str, Any]] = None


class Result(Protocol):
    """
    Result classes which indicate status and hold information.

    Flow of control in operators and rules is hard. We want to
    provide a good developer experience, especially for errors,
    so we have a way for individual units to return back a container
    of resulting information.
    """

    value: Any
    msg: Optional[str] = None


class Operator(Protocol):
    """
    A step in a FieldPipeline.

    """

    def __call__(
        self,
        previous: Optional[Result],
        pipeline: Pipeline,
    ) -> Result:
        ...


class FieldInfo(Protocol):
    """
    Necessary subset of field/parameter metadata for rules.
    """

    field_name: str
    field_type: Type[Any]
    default_value: Optional[Any]
    init: bool  # Dataclasses can flag init=False
    operators: Sequence[Operator]
    has_annotated: bool


class Rule(Protocol):
    """
    Attempt to handle a field or parameter.

    Each field/parameter in a target gets introspected and the
    relevant "field info" is passed through a series of rules.
    Each rule has the chance to handle the value, skip, bail
    out with an error, etc.
    """

    field_info: FieldInfo
    pipeline: Pipeline

    def __call__(self) -> Result:
        ...
