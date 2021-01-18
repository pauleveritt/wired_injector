from wired_injector.pipeline import Pipeline
from wired_injector.pipeline2 import Operator, Result
from wired_injector.pipeline2.operators import Context
from wired_injector.pipeline2.results import Found

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
    result: Result = attr(
        previous=DummyLookupClass(),
        pipeline=dummy_pipeline,
    )
    assert isinstance(result, Found)
    assert 'Dummy Context' == result.value
