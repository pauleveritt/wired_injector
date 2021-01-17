from wired_injector.pipeline import Pipeline
from wired_injector.pipeline2 import Operator, OperatorResult
from wired_injector.pipeline2.operators import Get

from .conftest import DummyLookupClass, DummyContainer


def test_get_setup(dummy_pipeline: Pipeline) -> None:
    # Ensure it meets the protocol
    meets_protocol: Operator = Get(DummyLookupClass)
    assert meets_protocol

    # Do we store the right things?
    get = Get(DummyLookupClass)
    assert DummyLookupClass == get.lookup_type
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
    value: DummyLookupClass = result.value
    assert 'Dummy Lookup Class' == value.title
