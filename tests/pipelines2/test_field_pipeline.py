import pytest
from wired_injector.pipeline2 import Pipeline, Result
from wired_injector.pipeline2.field_pipeline import process_field_pipeline
from wired_injector.pipeline2.operators import Get
from wired_injector.pipeline2.results import Found, NotFound

from .conftest import DummyLookupClass


@pytest.fixture
def single_pipeline(dummy_pipeline: Pipeline) -> Pipeline:
    # Stash one fake registration in the container

    fake_lookups = getattr(dummy_pipeline.container, 'fake_lookups')
    fake_lookups[DummyLookupClass] = DummyLookupClass()
    return dummy_pipeline


def test_field_pipeline_one(single_pipeline: Pipeline) -> None:
    operators = iter([Get(DummyLookupClass), ])
    result: Result = process_field_pipeline(
        operators=operators, pipeline=single_pipeline
    )
    assert isinstance(result, Found)
    assert isinstance(result.value, DummyLookupClass)


def test_field_pipeline_not_found(dummy_pipeline: Pipeline) -> None:
    operators = iter([Get(DummyLookupClass), ])
    result: Result = process_field_pipeline(
        operators=operators, pipeline=dummy_pipeline
    )
    assert isinstance(result, NotFound)
    assert "No service 'DummyLookupClass' found in container" == result.msg
    assert Get == result.value
