from dataclasses import dataclass

from wired_injector.operators import (
    Get,
    Attr,
    Context,
)
from wired_injector.pipeline import process_pipeline

from examples.factories import (
    View,
    FrenchView,
)


@dataclass
class Target:
    name: str = 'Some Target'


def test_process_pipeline(regular_container):
    pipeline = (Context(attr='name'),)
    start = str
    process_pipeline(regular_container, pipeline, start, Target)


def test_pipeline_one(french_container):
    pipeline = (Get(View),)
    result: FrenchView = process_pipeline(
        french_container,
        pipeline,
        start=View,
        target=View,
    )
    assert result.name == 'French View'


def test_pipeline_two(french_container):
    pipeline = (Get(View), Attr('name'))
    result = process_pipeline(
        french_container,
        pipeline,
        start=View,
        target=Target,
    )
    assert result == 'French View'


def test_pipeline_two_attr_attr(french_container):
    @dataclass
    class Customer:
        name: str = 'Some Customer'

    @dataclass
    class Config:
        customer: Customer = Customer()

    pipeline = (Attr('customer'), Attr('name'))
    result = process_pipeline(
        french_container,
        pipeline,
        start=Config(),
        target=Target,
    )
    assert result == 'Some Customer'


def test_context(regular_container):
    pipeline = (Context(),)
    result = process_pipeline(
        regular_container,
        pipeline,
        start=View,
        target=Target,
    )
    assert result == regular_container.context
