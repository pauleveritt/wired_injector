from dataclasses import dataclass, field
from typing import Any, Dict, TypeVar, Type, Optional, Callable, Sequence, NamedTuple

import pytest
from wired_injector.pipeline2 import (
    Container,
    FieldInfo,
    Pipeline,
    Result,
)
from wired_injector.pipeline2.operators import Context
from wired_injector.pipeline2.results import Found
from wired_injector.pipeline2.rules import DefaultFieldInfo

try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol  # type: ignore # noqa: F401

LookupType = TypeVar('LookupType')


@dataclass
class DummyContainer:
    context: Any = None
    fake_lookups: Dict[Any, Any] = field(default_factory=dict)

    def get(self, lookup_value: Type[LookupType], default: Optional[Any] = None) -> Optional[LookupType]:
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
    age: int
    title: str = 'Dummy Target'


class DummyTargetNamedTuple(NamedTuple):
    age: int
    title: str = 'Dummy Target'


def dummy_target_function(
    age: int,
    title: str = 'Dummy Target',
) -> DummyTarget:
    return DummyTarget(age=age, title=title)


@dataclass
class DummyPipeline:
    container: Container = field(default_factory=DummyContainer)
    field_infos: Sequence[FieldInfo] = tuple()
    props: Dict[str, Any] = field(default_factory=dict)
    system_props: Optional[Dict[str, Any]] = None
    target: Callable[..., Any] = DummyTarget

    def lookup(self, lookup_key: Any, default: Optional[Any] = None) -> Optional[Any]:
        """ Type-safe limited usage wrapper around container.get"""
        return self.container.get(lookup_key, default=default)

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
def dummy_title_field() -> FieldInfo:
    df = DefaultFieldInfo(
        field_name='title',
        field_type=str,
        default_value=None,
        init=False,
        operators=tuple(),
    )
    return df


@pytest.fixture
def dummy_annotated_field() -> FieldInfo:
    df = DefaultFieldInfo(
        field_name='title',
        field_type=str,
        default_value=None,
        init=False,
        operators=(Context(),),
        has_annotated=True,
    )
    return df


@pytest.fixture
def dummy_age_field() -> FieldInfo:
    df = DefaultFieldInfo(
        field_name='age',
        field_type=str,
        default_value=None,
        init=False,
        operators=tuple(),
    )
    return df


@pytest.fixture
def dummy_pipeline(
    dummy_age_field: FieldInfo,
    dummy_container: DummyContainer,
    dummy_title_field: FieldInfo,
) -> Pipeline:
    return DummyPipeline(
        container=dummy_container,
        field_infos=(dummy_title_field, dummy_age_field,)
    )
