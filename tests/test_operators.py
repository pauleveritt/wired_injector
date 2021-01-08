from dataclasses import dataclass
from typing import NamedTuple

import pytest
from wired_injector.injector import SkipField
from wired_injector.operators import (
    Get,
    Attr,
    process_pipeline,
    Context,
    Field,
)

from examples.factories import (
    FrenchCustomer,
    View,
    FrenchView,
    Greeting,
)


@dataclass
class Target:
    name: str = 'Some Target'


def test_get(french_container):
    get = Get(View)
    previous = FrenchView
    result: FrenchView = get(previous, french_container, Target)
    assert result.name == 'French View'


def test_get_injectable_attr(regular_container):
    get = Get(Greeting)
    previous = str
    result: Greeting = get(previous, regular_container, Target)
    assert result() == 'Hello VIEW'


def test_get_attr(french_container):
    get = Get(View, attr='name')
    previous = str
    result: FrenchView = get(previous, french_container, Target)
    assert result == 'French View'


def test_get_failed(french_container):
    class NotFound:
        pass

    previous = FrenchCustomer
    with pytest.raises(SkipField):
        Get(NotFound)(previous, french_container, Target)


def test_attr(regular_container):
    attr = Attr('name')
    previous = FrenchCustomer()
    result = attr(previous, regular_container, Target)
    assert 'French Customer' == result


def test_get_then_attr(french_container):
    get = Get(View)
    start = View
    result1 = get(start, french_container, Target)
    attr = Attr('name')
    result = attr(result1, french_container, Target)
    assert 'French View' == result


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


def test_context_attr(regular_container):
    context = Context(attr='name')
    previous = str
    result = context(previous, regular_container, Target)
    assert result == 'Customer'


def test_context_none_attr(regular_container):
    regular_container.context = None
    context = Context(attr='name')
    previous = str
    with pytest.raises(SkipField):
        context(previous, regular_container, Target)


def test_field_target_is_dataclass(regular_container):
    field = Field('name')
    previous = str
    result = field(previous, regular_container, Target)
    assert result == 'Some Target'


def test_field_target_is_named_tuple(regular_container):
    class TupleTarget(NamedTuple):
        name: str = 'Some TupleTarget'

    field = Field('name')
    previous = str
    result = field(previous, regular_container, TupleTarget)
    assert result == 'Some TupleTarget'


def test_field_target_is_function(regular_container):
    def FunctionTarget(name: str = 'Some FunctionTarget'):
        return

    field = Field('name')
    previous = str
    result = field(previous, regular_container, FunctionTarget)
    assert result == 'Some FunctionTarget'


def test_field_target_missing_field(regular_container):
    field = Field('bogus')
    previous = str
    with pytest.raises(KeyError) as exc:
        field(previous, regular_container, Target)
    assert str(exc.value.args[0]) == 'No field "bogus" on target "Target"'


def test_process_pipeline(regular_container):
    pipeline = (Context(attr='name'),)
    start = str
    process_pipeline(regular_container, pipeline, start, Target)
