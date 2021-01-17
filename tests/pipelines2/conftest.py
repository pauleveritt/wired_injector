from dataclasses import dataclass, field
from typing import Any, Dict, TypeVar, Type, Optional

import pytest
from wired_injector.pipeline2 import (
    Container,
    Pipeline,
)

try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol  # type: ignore # noqa: F401

LookupType = TypeVar('LookupType')


@dataclass
class DummyContainer:
    fake_lookups: Dict[Any, Any] = field(default_factory=dict)

    def get(self, lookup_value: Type[LookupType]) -> Optional[LookupType]:
        return self.fake_lookups.get(lookup_value)


@dataclass
class DummyLookupClass:
    title: str = 'Dummy Lookup Class'


class DummyLookupProtocol(Protocol):
    title: str = 'Dummy Lookup Class'


@dataclass
class DummyPipeline:
    container: Container = field(default_factory=DummyContainer)

    def lookup(self, lookup_key: Any) -> Optional[Any]:
        """ Type-safe limited usage wrapper around container.get"""
        return self.container.get(lookup_key)

    def inject(self, lookup_key: Any) -> Optional[Any]:
        """ Type-safe limited usage wrapper around the injector """
        return self.container.get(lookup_key)


@pytest.fixture
def dummy_container() -> DummyContainer:
    return DummyContainer()


@pytest.fixture
def dummy_pipeline(dummy_container: DummyContainer) -> Pipeline:
    return DummyPipeline(container=dummy_container)
