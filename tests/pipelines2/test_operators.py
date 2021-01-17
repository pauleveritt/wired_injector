from dataclasses import dataclass, field
from typing import Any, Optional, Mapping

from wired_injector.stuff import (
    Operator,
    Get,
    Found,
    OperatorResult,
    OperatorStatus,
    Pipeline,
    DefaultPipeline,
    Container,
    LookupType,
)


class DummyLookupType:
    pass


@dataclass
class DummyPipeline:
    container: Container


@dataclass
class DummyContainer:
    fake_lookups: Mapping[LookupType, LookupType] = field(default_factory=dict)

    def get(self, lookup_value: LookupType) -> Optional[LookupType]:
        return self.fake_lookups.get(lookup_value)


def dummy_pipeline(**kwargs: Any) -> Pipeline:
    dummy_container = DummyContainer(**kwargs)
    dp = DummyPipeline(container=dummy_container)
    return dp


def test_operator_protocols() -> None:
    # Give mypy a chance to see if each operator obeys the
    # operator protocol. Have to make an instance to get
    # mypy to kick in.

    get: Operator = Get(DummyLookupType)
    assert get


def test_get_setup() -> None:
    get = Get(DummyLookupType)
    default_pipeline = DefaultPipeline()
    result: OperatorResult = get(
        previous=None,
        pipeline=default_pipeline,
    )
    assert 99 == result.value


def test_found() -> None:
    f: OperatorResult = Found(value=99)
    assert OperatorStatus.found == f.status
    assert 99 == f.value


def test_container() -> None:
    lookups = dict(Get=Operator)
    dc = DummyContainer(**lookups)
    result = 9
