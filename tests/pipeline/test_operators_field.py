from typing import NamedTuple

from wired_injector.pipeline import Pipeline
from wired_injector.pipeline import Operator, Result
from wired_injector.pipeline.operators import Context, Field
from wired_injector.pipeline.results import Error, Found

from .conftest import DummyContext, DummyLookupClass


def test_context_setup() -> None:
    # Ensure it meets the protocol
    meets_protocol: Operator = Context()
    assert meets_protocol

    # Do we store the right things?
    context = Context()
    assert None is context.attr


def test_context_setup_attr() -> None:
    context = Context(attr='title')
    assert 'title' == context.attr


def test_context_found(dummy_pipeline: Pipeline) -> None:
    # Set a context on the dummy container
    dummy_pipeline.container.context = DummyContext()

    attr = Context('title')
    previous = Found(value=DummyLookupClass())
    result: Result = attr(
        previous=previous,
        pipeline=dummy_pipeline,
    )
    assert isinstance(result, Found)
    assert 'Dummy Context' == result.value


def test_context_none(dummy_pipeline: Pipeline) -> None:
    # Error() result on container.context=None

    attr = Context('title')
    previous = Found(value=DummyLookupClass())
    result: Result = attr(
        previous=previous,
        pipeline=dummy_pipeline,
    )
    assert isinstance(result, Error)
    assert 'Container context is None' == result.msg
    assert result.value == Context


def test_field_target_is_dataclass(dummy_pipeline: Pipeline) -> None:
    field = Field('title')
    result = field(None, dummy_pipeline)
    assert isinstance(result, Found)
    assert 'Dummy Target' == result.value


def test_field_not_found(dummy_pipeline: Pipeline) -> None:
    # Ask for a field that is not on the target
    field = Field('NOFIELD')
    result = field(None, dummy_pipeline)
    assert isinstance(result, Error)
    assert 'No field "NOFIELD" on target' == result.msg
    assert Field == result.value


class TupleTarget(NamedTuple):
    title: str = 'Some TupleTarget'


def test_field_target_is_named_tuple(dummy_pipeline: Pipeline) -> None:
    dummy_pipeline.target = TupleTarget
    field = Field('title')
    result = field(None, dummy_pipeline)
    assert isinstance(result, Found)
    assert 'Some TupleTarget' == result.value


def FunctionTarget(title: str = 'Some FunctionTarget') -> str:
    return title


def test_field_target_is_function(dummy_pipeline: Pipeline) -> None:
    dummy_pipeline.target = FunctionTarget
    field = Field('title')
    result = field(None, dummy_pipeline)
    assert isinstance(result, Found)
    assert 'Some FunctionTarget' == result.value
