from wired_injector.pipeline2 import OperatorResult
from wired_injector.pipeline2.operator_results import (
    Found,
    NotFound,
)

from .conftest import DummyLookupClass


def test_found() -> None:
    # Ensure it meets the protocol
    meets_protocol: OperatorResult = Found(value=99)
    assert meets_protocol

    # Now test construction
    result = Found(value=99)
    assert 99 == result.value


def test_not_found() -> None:
    # Ensure it meets the protocol
    meets_protocol: OperatorResult = NotFound(value=DummyLookupClass)
    assert meets_protocol

    # Now test construction
    result = NotFound(value=DummyLookupClass)
    assert DummyLookupClass == result.value
