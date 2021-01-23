from wired_injector.pipeline import Pipeline
from wired_injector.pipeline import Operator, Result
from wired_injector.pipeline.operators import Attr
from wired_injector.pipeline.results import Found, NotFound

from .conftest import DummyLookupClass


def test_attr_setup() -> None:
    # Ensure it meets the protocol
    meets_protocol: Operator = Attr('title')
    assert meets_protocol

    # Do we store the right things?
    get = Attr('title')
    assert 'title' == get.name


def test_attr_found(dummy_pipeline: Pipeline) -> None:
    attr = Attr('title')
    previous = Found(value=DummyLookupClass())
    result: Result = attr(
        previous=previous,
        pipeline=dummy_pipeline,
    )
    assert isinstance(result, Found)
    assert 'Dummy Lookup Class' == result.value


def test_attr_bogus_first(dummy_pipeline: Pipeline) -> None:
    # Attr shouldn't be the first item in the pipeline, otherwise,
    # it will be trying to pluck from None.
    attr = Attr('title')
    previous = Found(value=DummyLookupClass())
    result: Result = attr(
        previous=None,
        pipeline=dummy_pipeline,
    )
    assert isinstance(result, NotFound)
    assert "Cannot use 'Attr' operator first in the pipeline" == result.msg
    assert Attr == result.value


def test_attr_previous_notfound(dummy_pipeline: Pipeline) -> None:
    # The previous item was a Get() of something that resulted
    # in NotFound. Attr isn't an operator that can handle NotFound,
    # so it should just pass the NotFound through.
    attr = Attr('title')
    previous = NotFound(msg='Not Found', value=DummyLookupClass)
    result: Result = attr(
        previous=previous,
        pipeline=dummy_pipeline,
    )
    assert isinstance(result, NotFound)
    assert DummyLookupClass == result.value
