from wired_injector.pipeline2 import Result
from wired_injector.pipeline2.results import (
    Found,
    NotFound,
)

from .conftest import DummyLookupClass, DummyLookupProtocol


def test_found() -> None:
    # Ensure it meets the protocol
    meets_protocol: Result = Found(value=99)
    assert meets_protocol

    # Now test construction
    result = Found(value=99)
    assert 99 == result.value


def test_not_found_class() -> None:
    # Ensure it meets the protocol
    meets_protocol: Result = NotFound(value=DummyLookupClass)
    assert meets_protocol

    # Now test construction
    result = NotFound(value=DummyLookupClass)
    assert DummyLookupClass == result.value


def test_not_found_protocol() -> None:
    # Ensure it meets the protocol
    meets_protocol: Result = NotFound(value=DummyLookupProtocol)
    assert meets_protocol

    # Now test construction
    result = NotFound(value=DummyLookupProtocol)
    assert DummyLookupProtocol == result.value
