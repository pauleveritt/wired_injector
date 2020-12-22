from dataclasses import dataclass

import pytest
from wired_injector.injector import SkipField
from wired_injector.operators import Get, Attr, process_pipeline, Context

from examples.factories import (
    FrenchCustomer,
    View,
    FrenchView,
    Greeting,
)


def test_get(french_container):
    get = Get(View)
    previous = FrenchView
    result: FrenchView = get(previous, french_container)
    assert result.name == 'French View'


def test_get_injectable_attr(regular_container):
    get = Get(Greeting)
    previous = str
    result: Greeting = get(previous, regular_container)
    assert result() == 'Hello VIEW'


def test_get_attr(french_container):
    get = Get(View, attr='name')
    previous = str
    result: FrenchView = get(previous, french_container)
    assert result == 'French View'


def test_get_failed(french_container):
    class NotFound:
        pass

    previous = FrenchCustomer
    with pytest.raises(SkipField):
        Get(NotFound)(previous, french_container)


def test_attr(regular_container):
    attr = Attr('name')
    previous = FrenchCustomer()
    result = attr(previous, regular_container)
    assert 'French Customer' == result


def test_get_then_attr(french_container):
    get = Get(View)
    start = View
    result1 = get(start, french_container)
    attr = Attr('name')
    result = attr(result1, french_container)
    assert 'French View' == result


def test_pipeline_one(french_container):
    pipeline = (Get(View),)
    result: FrenchView = process_pipeline(
        french_container,
        pipeline,
        start=View,
    )
    assert result.name == 'French View'


def test_pipeline_two(french_container):
    pipeline = (Get(View), Attr('name'))
    result = process_pipeline(
        french_container,
        pipeline,
        start=View,
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
    )
    assert result == 'Some Customer'


def test_context(regular_container):
    pipeline = (Context(),)
    result = process_pipeline(
        regular_container,
        pipeline,
        start=View,
    )
    assert result == regular_container.context


def test_context_attr(regular_container):
    context = Context(attr='name')
    previous = str
    result = context(previous, regular_container)
    assert result == 'Customer'


def test_context_none_attr(regular_container):
    regular_container.context = None
    context = Context(attr='name')
    previous = str
    with pytest.raises(SkipField):
        context(previous, regular_container)
