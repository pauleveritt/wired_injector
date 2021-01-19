from typing import Sequence

import pytest
from wired_injector.pipeline2 import Operator, Pipeline, Result
from wired_injector.pipeline2.field_pipeline import process_field_pipeline
from wired_injector.pipeline2.operators import Attr, Get
from wired_injector.pipeline2.results import (
    Error,
    Found,
    NotFound,
)

from .conftest import DummyLookupClass, DummyNoOp


@pytest.fixture
def single_pipeline(dummy_pipeline: Pipeline) -> Pipeline:
    # Stash one fake registration in the container

    fake_lookups = getattr(dummy_pipeline.container, 'fake_lookups')
    fake_lookups[DummyLookupClass] = DummyLookupClass()
    return dummy_pipeline


def test_field_pipeline_one(single_pipeline: Pipeline) -> None:
    operators = (Get(DummyLookupClass),)
    result: Result = process_field_pipeline(
        operators=operators, pipeline=single_pipeline
    )
    assert isinstance(result, Found)
    assert isinstance(result.value, DummyLookupClass)


def test_field_pipeline_two(single_pipeline: Pipeline) -> None:
    operators: Sequence[Operator] = (Get(DummyLookupClass), Attr('title'))
    result: Result = process_field_pipeline(
        operators=operators, pipeline=single_pipeline
    )
    assert isinstance(result, Found)
    assert 'Dummy Lookup Class' == result.value


def test_field_pipeline_not_found(dummy_pipeline: Pipeline) -> None:
    operators: Sequence[Operator] = (Get(DummyLookupClass),)
    result: Result = process_field_pipeline(
        operators=operators, pipeline=dummy_pipeline
    )
    assert isinstance(result, NotFound)
    assert "No service 'DummyLookupClass' found in container" == result.msg
    assert Get == result.value


def test_field_pipeline_first_op_err(dummy_pipeline: Pipeline) -> None:
    # The first operator generates an error
    no_op = DummyNoOp()
    operators: Sequence[Operator] = (no_op, Get('XXX'))
    result: Result = process_field_pipeline(
        operators=operators, pipeline=dummy_pipeline
    )
    assert isinstance(result, Error)
    assert "Cannot use a string 'XXX' as container lookup value" == result.msg
    assert Get == result.value
    assert no_op.call_count == 1


def test_field_pipeline_second_op_err(dummy_pipeline: Pipeline) -> None:
    # An operator after the first one, generated an error
    no_op = DummyNoOp()
    operators: Sequence[Operator] = (Get('XXX'), no_op)
    result: Result = process_field_pipeline(
        operators=operators, pipeline=dummy_pipeline
    )
    assert isinstance(result, Error)
    assert "Cannot use a string 'XXX' as container lookup value" == result.msg
    assert Get == result.value
    assert no_op.call_count == 0
