from dataclasses import dataclass
from typing import Tuple

from wired_injector.field_info import FieldInfo
from wired_injector.operators import (
    Get,
    Attr,
    Context, Operator,
)
from wired_injector.pipeline import Pipeline

from examples.factories import (
    View,
    FrenchView,
)


@dataclass
class Target:
    name: str = 'Some Target'


def field_info_no_default_value(
    operators: Tuple[Operator, ...],
) -> FieldInfo:
    """ A field with NO default value """
    fi = FieldInfo(
        field_name='title',
        field_type=str,
        default_value=None,
        init=False,
        operators=operators,
    )
    return fi


def test_process_pipeline(regular_container):
    operators = Context(attr='name'),
    field_info = field_info_no_default_value(operators)
    pipeline = Pipeline(
        field_info=field_info,
        container=regular_container,
        start=str,
        target=Target,
    )
    results = pipeline()
    assert results == 'Customer'


def test_pipeline_one(french_container):
    operators = Get(View),
    field_info = field_info_no_default_value(operators)
    pipeline = Pipeline(
        field_info=field_info,
        container=french_container,
        start=View,
        target=Target,
    )
    result: FrenchView = pipeline()
    assert result.name == 'French View'


def test_pipeline_two(french_container):
    operators = Get(View), Attr('name')
    field_info = field_info_no_default_value(operators)
    pipeline = Pipeline(
        field_info=field_info,
        container=french_container,
        start=View,
        target=Target,
    )
    result: str = pipeline()
    assert result == 'French View'


def test_pipeline_two_attr_attr(french_container):
    @dataclass
    class Customer:
        name: str = 'Some Customer'

    @dataclass
    class Config:
        customer: Customer = Customer()

    operators = Attr('customer'), Attr('name')
    field_info = field_info_no_default_value(operators)

    pipeline = Pipeline(
        field_info=field_info,
        container=french_container,
        start=Config(),
        target=Target,
    )
    result = pipeline()
    assert result == 'Some Customer'


def test_context(regular_container):
    operators = Context(),
    field_info = field_info_no_default_value(operators)
    pipeline = Pipeline(
        field_info=field_info,
        container=regular_container,
        start=View,
        target=Target,
    )
    result = pipeline()
    assert result == regular_container.context
