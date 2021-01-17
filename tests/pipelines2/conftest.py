from dataclasses import dataclass

import pytest
from wired_injector.pipeline2 import (
    Container,
    Pipeline,
)

try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol  # type: ignore # noqa: F401


@dataclass
class DummyContainer:
    pass


@dataclass
class DummyLookupClass:
    title: str = 'Dummy Lookup Class'


class DummyLookupProtocol(Protocol):
    title: str = 'Dummy Lookup Class'


@dataclass
class DummyPipeline:
    container: Container


@pytest.fixture
def dummy_container() -> DummyContainer:
    return DummyContainer()


@pytest.fixture
def dummy_pipeline(dummy_container: DummyContainer) -> Pipeline:
    return DummyPipeline(container=dummy_container)
