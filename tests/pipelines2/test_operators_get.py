from wired_injector.pipeline import Pipeline
from wired_injector.pipeline2 import Operator, Result
from wired_injector.pipeline2.operators import Get
from wired_injector.pipeline2.results import (
    Error,
    Found,
    NotFound,
)

from .conftest import (
    DummyContainer,
    DummyLookupClass,
    DummyLookupProtocol,
)


def test_get_setup() -> None:
    # Ensure it meets the protocol
    meets_protocol: Operator = Get(DummyLookupClass)
    assert meets_protocol

    # Do we store the right things?
    get = Get(DummyLookupClass)
    assert DummyLookupClass == get.lookup_key
    assert None is get.attr


def test_get_setup_attr() -> None:
    get = Get(DummyLookupClass, attr='title')
    assert 'title' == get.attr


def test_get_class(
    dummy_container: DummyContainer,
    dummy_pipeline: Pipeline,
) -> None:
    # Set the lookup value to use a value that is a class, to simulate
    # injection.
    dummy_container.fake_lookups[DummyLookupClass] = DummyLookupClass

    get = Get(DummyLookupClass)
    result: Result = get(
        previous=None,
        pipeline=dummy_pipeline,
    )
    assert isinstance(result, Found)
    assert result.value == DummyLookupClass


def test_get_class_instance(
    dummy_container: DummyContainer,
    dummy_pipeline: Pipeline,
) -> None:
    # Set the lookup value to use a value that is an instance
    dummy_container.fake_lookups[DummyLookupClass] = DummyLookupClass()

    get = Get(DummyLookupClass)
    result: Result = get(
        previous=None,
        pipeline=dummy_pipeline,
    )
    assert isinstance(result, Found)
    assert isinstance(result.value, DummyLookupClass)


def test_get_protocol(
    dummy_container: DummyContainer,
    dummy_pipeline: Pipeline,
) -> None:
    # Lookup up a protocol, not a class

    # Set the lookup value
    dummy_container.fake_lookups[DummyLookupProtocol] = DummyLookupClass()

    get = Get(DummyLookupProtocol)
    result: Result = get(
        previous=None,
        pipeline=dummy_pipeline,
    )
    assert isinstance(result, Found)
    assert isinstance(result.value, DummyLookupClass)


def test_get_none(
    dummy_container: DummyContainer,
    dummy_pipeline: Pipeline,
) -> None:
    # Lookup fails because nothing is in the container.

    get = Get(DummyLookupClass)
    result: Result = get(
        previous=None,
        pipeline=dummy_pipeline,
    )
    assert isinstance(result, NotFound)
    assert result.msg == "No service 'DummyLookupClass' found in container"
    assert result.value == Get


def test_get_attr(
    dummy_container: DummyContainer,
    dummy_pipeline: Pipeline,
) -> None:
    # Set the lookup value
    dummy_container.fake_lookups[DummyLookupClass] = DummyLookupClass()

    get = Get(DummyLookupClass, attr='title')
    result: Result = get(
        previous=None,
        pipeline=dummy_pipeline,
    )
    assert isinstance(result, Found)
    assert 'Dummy Lookup Class' == result.value


def test_get_error_str(
    dummy_container: DummyContainer,
    dummy_pipeline: Pipeline,
) -> None:
    # Try to do a container lookup on a string instead of a class

    get = Get('WRONG')
    result: Result = get(
        previous=None,
        pipeline=dummy_pipeline,
    )
    assert isinstance(result, Error)
    expected = "Cannot use a string 'WRONG' as container lookup value"
    assert result.msg == expected
    assert result.value == Get
