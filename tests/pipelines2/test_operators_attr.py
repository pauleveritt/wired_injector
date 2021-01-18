from wired_injector.pipeline import Pipeline
from wired_injector.pipeline2 import Operator, Result
from wired_injector.pipeline2.operators import Attr
from wired_injector.pipeline2.results import Found

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
    result: Result = attr(
        previous=DummyLookupClass(),
        pipeline=dummy_pipeline,
    )
    assert isinstance(result, Found)
    assert 'Dummy Lookup Class' == result.value
