from wired_injector.pipeline import Pipeline
from wired_injector.pipeline2 import Operator, OperatorResult
from wired_injector.pipeline2.operators import Get

from .conftest import DummyLookupClass


def test_get_setup(dummy_pipeline: Pipeline) -> None:
    # Ensure it meets the protocol
    meets_protocol: Operator = Get(DummyLookupClass)
    assert meets_protocol

    get = Get(DummyLookupClass)
    result: OperatorResult = get(
        previous=None,
        pipeline=dummy_pipeline,
    )
    assert 99 == result.value
