from dataclasses import dataclass, field
from typing import Any, Dict, TypeVar, Type, Optional, Callable

import pytest
from wired_injector.pipeline2 import (
    Container,
    Pipeline, Result,
)
from wired_injector.pipeline2.results import Found

try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol  # type: ignore # noqa: F401

LookupType = TypeVar('LookupType')


@dataclass
class DummyContainer:
    context: Any = None
    fake_lookups: Dict[Any, Any] = field(default_factory=dict)

    def get(self, lookup_value: Type[LookupType]) -> Optional[LookupType]:
        return self.fake_lookups.get(lookup_value)


@dataclass
class DummyLookupClass:
    title: str = 'Dummy Lookup Class'


class DummyLookupProtocol(Protocol):
    title: str = 'Dummy Lookup Class'


@dataclass
class DummyContext:
    title: str = 'Dummy Context'


@dataclass
class DummyTarget:
    title: str = 'Dummy Target'


@dataclass
class DummyPipeline:
    container: Container = field(default_factory=DummyContainer)
    props: Dict[str, Any] = field(default_factory=dict)
    system_props: Optional[Dict[str, Any]] = None
    target: Callable[..., Any] = DummyTarget

    def lookup(self, lookup_key: Any) -> Optional[Any]:
        """ Type-safe limited usage wrapper around container.get"""
        return self.container.get(lookup_key)

    def inject(self, lookup_key: Any) -> Optional[Any]:
        """ Type-safe limited usage wrapper around the injector """
        return self.container.get(lookup_key)


@dataclass
class DummyNoOp:
    """
    A fake operator that keeps track of whether it was called.

    To test Error results, we need to ensure the field/rule pipeline
    bails out and does not keep calling operators.
    """

    call_count: int = 0

    def __call__(
        self,
        previous: Optional[Result],
        pipeline: Pipeline,
    ) -> Result:
        self.call_count += 1
        return Found(value=99)


@pytest.fixture
def dummy_container() -> DummyContainer:
    return DummyContainer()


@pytest.fixture
def dummy_pipeline(dummy_container: DummyContainer) -> Pipeline:
    return DummyPipeline(container=dummy_container)
