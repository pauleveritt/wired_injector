from wired_injector.pipeline import Pipeline
from wired_injector.pipeline2 import Operator, OperatorResult
from wired_injector.pipeline2.operator_results import Found, NotFound
from wired_injector.pipeline2.operators import (
    Attr,
    Get,
)

from .conftest import (
    DummyContainer,
    DummyLookupClass,
    DummyLookupProtocol,
)


def test_get_setup(dummy_pipeline: Pipeline) -> None:
    # Ensure it meets the protocol
    meets_protocol: Operator = Get(DummyLookupClass)
    assert meets_protocol

    # Do we store the right things?
    get = Get(DummyLookupClass)
    assert DummyLookupClass == get.lookup_key
    assert None is get.attr


def test_get_setup_attr(dummy_pipeline: Pipeline) -> None:
    get = Get(DummyLookupClass, attr='title')
    assert 'title' == get.attr


def test_get_class(
    dummy_container: DummyContainer,
    dummy_pipeline: Pipeline,
) -> None:
    # Set the lookup value
    dummy_container.fake_lookups[DummyLookupClass] = DummyLookupClass()

    get = Get(DummyLookupClass)
    result: OperatorResult = get(
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
    result: OperatorResult = get(
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
    result: OperatorResult = get(
        previous=None,
        pipeline=dummy_pipeline,
    )
    assert isinstance(result, NotFound)
    assert result.value == DummyLookupClass


def test_get_attr(
    dummy_container: DummyContainer,
    dummy_pipeline: Pipeline,
) -> None:
    # Set the lookup value
    dummy_container.fake_lookups[DummyLookupClass] = DummyLookupClass()

    get = Get(DummyLookupClass, attr='title')
    result: OperatorResult = get(
        previous=None,
        pipeline=dummy_pipeline,
    )
    assert isinstance(result, Found)
    assert 'Dummy Lookup Class' == result.value


def test_attr_setup(dummy_pipeline: Pipeline) -> None:
    # Ensure it meets the protocol
    meets_protocol: Operator = Attr('title')
    assert meets_protocol

    # Do we store the right things?
    get = Attr('title')
    assert 'title' == get.name


def test_attr_found(dummy_pipeline: Pipeline) -> None:
    attr = Attr('title')
    result: OperatorResult = attr(
        previous=DummyLookupClass(),
        pipeline=dummy_pipeline,
    )
    assert isinstance(result, Found)
    assert 'Dummy Lookup Class' == result.value
