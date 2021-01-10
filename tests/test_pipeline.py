from dataclasses import dataclass
from typing import Tuple

import pytest
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
    pipeline: Tuple[Operator, ...],
) -> FieldInfo:
    """ A field with NO default value """
    fi = FieldInfo(
        field_name='title',
        field_type=str,
        default_value=None,
        init=False,
        pipeline=pipeline,
    )
    return fi


def test_process_pipeline(regular_container):
    start = str
    pipeline = Pipeline(
        container=regular_container,
        start=start,
        target=Target,
    )
    results = pipeline(Context(attr='name'), )
    assert results == 'Customer'


def test_pipeline_one(french_container):
    pipeline = Pipeline(
        container=french_container,
        start=View,
        target=Target,
    )
    result: FrenchView = pipeline(Get(View), )
    assert result.name == 'French View'


def test_pipeline_two(french_container):
    pipeline = Pipeline(
        container=french_container,
        start=View,
        target=Target,
    )
    result: str = pipeline(Get(View), Attr('name'))
    assert result == 'French View'


def test_pipeline_two_attr_attr(french_container):
    @dataclass
    class Customer:
        name: str = 'Some Customer'

    @dataclass
    class Config:
        customer: Customer = Customer()

    pipeline = Pipeline(
        container=french_container,
        start=Config(),
        target=Target,
    )
    result = pipeline(Attr('customer'), Attr('name'))
    assert result == 'Some Customer'


def test_context(regular_container):
    pipeline = Pipeline(
        container=regular_container,
        start=View,
        target=Target,
    )
    result = pipeline(Context(), )
    assert result == regular_container.context
