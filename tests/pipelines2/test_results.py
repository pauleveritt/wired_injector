from wired_injector.pipeline2 import Result
from wired_injector.pipeline2.results import (
    Error,
    Found,
    NotFound,
    Skip,
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
    meets_protocol: Result = NotFound(msg='', value=DummyLookupClass)
    assert meets_protocol

    # Now test construction
    msg = ''
    result = NotFound(msg=msg, value=DummyLookupClass)
    assert msg == result.msg
    assert DummyLookupClass == result.value


def test_not_found_protocol() -> None:
    # Ensure it meets the protocol
    meets_protocol: Result = NotFound(msg='', value=DummyLookupProtocol)
    assert meets_protocol

    # Now test construction
    msg = ''
    result = NotFound(msg=msg, value=DummyLookupProtocol)
    assert msg == result.msg
    assert DummyLookupProtocol == result.value


def test_error() -> None:
    # Ensure it meets the protocol
    meets_protocol: Result = Error(msg='', value=DummyLookupClass)
    assert meets_protocol

    # Now test construction
    msg = ''
    result = Error(msg=msg, value=DummyLookupClass)
    assert msg == result.msg
    assert DummyLookupClass == result.value


def test_skip() -> None:
    # Ensure it meets the protocol
    meets_protocol: Result = Skip(value=DummyLookupClass)
    assert meets_protocol

    # Now test construction
    msg = ''
    result = Skip(value=DummyLookupClass)
    assert DummyLookupClass == result.value