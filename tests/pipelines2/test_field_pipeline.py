from wired_injector.pipeline2 import Pipeline, Result
from wired_injector.pipeline2.field_pipeline import process_field_pipeline
from wired_injector.pipeline2.operators import Get
from wired_injector.pipeline2.results import Found, NotFound

from .conftest import DummyLookupClass, DummyContainer


def test_field_pipeline_one(
    dummy_container: DummyContainer,
    dummy_pipeline: Pipeline,
) -> None:
    # Set the lookup value
    dummy_container.fake_lookups[DummyLookupClass] = DummyLookupClass()

    operators = iter([Get(DummyLookupClass), ])
    result: Result = process_field_pipeline(operators=operators, pipeline=dummy_pipeline)
    assert isinstance(result, Found)
    assert isinstance(result.value, DummyLookupClass)


def test_field_pipeline_not_found(dummy_pipeline: Pipeline) -> None:
    operators = iter([Get(DummyLookupClass), ])
    result: Result = process_field_pipeline(operators=operators, pipeline=dummy_pipeline)
    assert isinstance(result, NotFound)
    assert DummyLookupClass == result.value

